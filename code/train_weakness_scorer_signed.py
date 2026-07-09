"""LoRA-finetune Qwen/Qwen3.5-4B (causal LM) + linear head, SIGNED item scores.

Each item is wrapped in a favorability-judging prompt; the head reads the last
token's final hidden state.

Each item is scored with a sign forced by its kind:
  magnitude = 10 * sigmoid(head)  -> smooth (0,10), gradient everywhere
  signed    = +magnitude for a "strength:" item, -magnitude for a "weakness:" item
             -> strength in (0,10), weakness in (-10,0), 0 is the good/bad boundary
  paper score = 5 + mean(signed items)   (NOT clipped during training, so the
             gradient is never killed; a paper with strong strengths / few
             weaknesses lands high, the reverse lands low)
Loss (on the paper score): weighted MAE (w=1+|gt-5|) + 0.5*margin_ranking + 0.5*ranknet.

Interpretable: the agent can read each item's signed score directly (how much this
strength adds / this weakness subtracts, 0-10 magnitude).

Resumable: checkpoints/weakness_scorer_signed/latest/ every CKPT_EVERY groups.
"""

import os
import json
import random
import shutil

import dotenv

dotenv.load_dotenv()

import torch
import torch.nn as nn
import tqdm
import wandb
from datasets import load_dataset
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModel, AutoTokenizer, get_cosine_schedule_with_warmup
from pathlib import Path

MODEL_NAME = "Qwen/Qwen3.5-4B"
DATASET_NAME = "weathon/weakness-score"
HUB_REPO = "weathon/review_scoring_signed_qwen4b"
CKPT_DIR = (Path.cwd() / "checkpoints" / "weakness_scorer_signed_qwen4b").resolve()

# Qwen3.5-4B is an instruct model: the judging question goes in a user turn via
# the chat template, add_generation_prompt=True appends the assistant header, and
# the head reads that last token's final hidden state (where the model would
# begin its favorability answer) rather than a bare embedding.
PROMPT = """You are judging one point from a paper review.
How favorable is this point toward the paper?

Point: {item}"""

EPOCHS = 3
LR = 1e-4
LORA_R = 64
LORA_ALPHA = 64
MAX_LEN = 2048
SEED = 0
CKPT_EVERY = 200
ITEM_BATCH = 32
WARMUP_FRAC = 0.03

PAIR_B = 8
MARGIN_LAMBDA = 0.5
RANKNET_LAMBDA = 0.5


def save_checkpoint(ckpt, model, head, baseline, optimizer, scheduler, epoch, step):
    # write to tmp then rename, so a crash mid-save never corrupts the resume point
    tmp = ckpt.parent / (ckpt.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    model.save_pretrained(str(tmp))
    torch.save(head.state_dict(), tmp / "head.pt")
    torch.save(baseline.detach().cpu(), tmp / "baseline.pt")
    torch.save(optimizer.state_dict(), tmp / "optimizer.pt")
    torch.save(scheduler.state_dict(), tmp / "scheduler.pt")
    (tmp / "state.json").write_text(json.dumps({"epoch": epoch, "step": step}))
    if ckpt.exists():
        shutil.rmtree(ckpt)
    tmp.rename(ckpt)


def forward_paper(model, head, baseline, tokenizer, items, device):
    is_strength = torch.tensor([it.startswith("strength") for it in items], device=device)
    prompts = [tokenizer.apply_chat_template(  # kind from raw item, LLM sees the chat-templated prompt
        [{"role": "user", "content": PROMPT.format(item=it)}],
        tokenize=False, add_generation_prompt=True,
    ) for it in items]
    mags = []
    for i in range(0, len(items), ITEM_BATCH):
        batch = tokenizer(
            prompts[i:i + ITEM_BATCH], padding=True, truncation=True, max_length=MAX_LEN,
            return_tensors="pt", padding_side="left", add_special_tokens=False,
        ).to(device)  # chat template already injected special tokens
        hidden = model(**batch).last_hidden_state
        pooled = hidden[:, -1]  # left padding -> last token is the prompt tail
        mags.append(10 * torch.sigmoid(head(pooled.float()).squeeze(-1)))  # (0,10)
    mags = torch.cat(mags)
    # average within each group first, then combine, so the item COUNT is not a
    # prior (a paper with many strengths no longer scores high just from counts).
    # Papers missing either group are filtered out in main(), so both are non-empty.
    return baseline + (mags[is_strength].mean() - mags[~is_strength].mean()) / 2


def main():
    random.seed(SEED)
    torch.manual_seed(SEED)
    device = "cuda"

    ds = load_dataset(DATASET_NAME, token=os.environ["HF_TOKEN"])
    # within-group averaging needs both groups present; drop papers missing either kind
    both = lambda p: any(it.startswith("strength") for it in p["items"]) and \
        any(it.startswith("weakness") for it in p["items"])
    train_data = [p for p in ds["train"] if both(p)]
    val_data = [p for p in ds["validation"] if both(p)]
    print(f"train {len(train_data)} papers, val {len(val_data)} papers "
          f"(dropped {len(ds['train']) - len(train_data)} train / "
          f"{len(ds['validation']) - len(val_data)} val missing a group)")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.truncation_side = "left"  # keep the trailing prompt tail when a long item overflows
    # Qwen3.5-4B is vision+text; this is a text-only item scorer, so drop the
    # vision tower and keep the LM backbone (Qwen3_5TextModel, hidden_size 2560).
    _full = AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16)
    del _full.visual
    base = _full.language_model

    latest = CKPT_DIR / "latest"
    assert not (not latest.exists() and (CKPT_DIR / "latest.tmp").exists()), \
        f"found orphaned {CKPT_DIR / 'latest.tmp'} without latest/; recover it manually"
    head = nn.Linear(base.config.hidden_size, 1)
    if latest.exists():
        state = json.loads((latest / "state.json").read_text())
        start_epoch, start_step = state["epoch"], state["step"]
        if start_epoch >= EPOCHS:
            print(f"all {EPOCHS} epochs already done at {CKPT_DIR}")
            return
        print(f"resuming from {latest} (epoch {start_epoch}, step {start_step})")
        model = PeftModel.from_pretrained(base, str(latest), is_trainable=True)
        head.load_state_dict(torch.load(latest / "head.pt"))
        baseline_init = torch.load(latest / "baseline.pt")
    else:
        start_epoch, start_step = 0, 0
        lora_cfg = LoraConfig(r=LORA_R, lora_alpha=LORA_ALPHA, target_modules="all-linear")
        model = get_peft_model(base, lora_cfg)
        baseline_init = torch.tensor(5.0)
    model.print_trainable_parameters()
    model.to(device)
    head.to(device)
    baseline = baseline_init.detach().to(device).requires_grad_(True)  # learnable baseline
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()

    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad] + list(head.parameters()) + [baseline],
        lr=LR,
    )
    groups_per_epoch = (len(train_data) + PAIR_B - 1) // PAIR_B
    total_steps = EPOCHS * groups_per_epoch
    scheduler = get_cosine_schedule_with_warmup(
        optimizer, num_warmup_steps=round(WARMUP_FRAC * total_steps),
        num_training_steps=total_steps,
    )
    if latest.exists():
        optimizer.load_state_dict(torch.load(latest / "optimizer.pt"))
        scheduler.load_state_dict(torch.load(latest / "scheduler.pt"))

    run = wandb.init(project="weakness-score", config={
        "model": MODEL_NAME, "epochs": EPOCHS, "lr": LR, "lora_r": LORA_R,
        "lora_alpha": LORA_ALPHA, "pair_b": PAIR_B, "margin_lambda": MARGIN_LAMBDA,
        "ranknet_lambda": RANKNET_LAMBDA, "max_len": MAX_LEN, "ckpt_every": CKPT_EVERY,
        "warmup_frac": WARMUP_FRAC, "total_steps": total_steps, "signed": True,
        "start_epoch": start_epoch, "start_step": start_step,
    })
    print(f"wandb run: {run.url}")

    for epoch in range(start_epoch, EPOCHS):
        model.train()
        order = list(range(len(train_data)))
        random.Random(SEED + epoch).shuffle(order)  # deterministic, so mid-epoch resume can skip forward
        n_groups = (len(order) + PAIR_B - 1) // PAIR_B
        skip = start_step if epoch == start_epoch else 0
        for g in tqdm.tqdm(range(skip, n_groups), desc=f"epoch {epoch + 1}",
                           initial=skip, total=n_groups):
            group = order[g * PAIR_B:(g + 1) * PAIR_B]
            preds = torch.stack([forward_paper(model, head, baseline, tokenizer, train_data[j]["items"], device)
                                 for j in group])
            gts = torch.tensor([train_data[j]["gt"] for j in group], device=device, dtype=preds.dtype)
            mae = ((1 + (gts - 5).abs()) * (preds - gts).abs()).mean()
            dp = preds[:, None] - preds[None, :]
            dg = gts[:, None] - gts[None, :]
            mask = dg > 0  # pairs where paper i should score above paper j
            if mask.any():
                margin_rank = torch.relu(dg - dp)[mask].mean()
                ranknet = -nn.functional.logsigmoid(dp[mask]).mean()
            else:
                margin_rank = preds.new_zeros(())
                ranknet = preds.new_zeros(())
            loss = mae + MARGIN_LAMBDA * margin_rank + RANKNET_LAMBDA * ranknet
            assert not torch.isnan(loss), f"NaN loss at epoch {epoch} group {g}"
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
            if g % 20 == 0:
                pair_acc = (dp[mask] > 0).float().mean().item() if mask.any() else float("nan")
                metrics = {"train/loss": loss.item(), "train/mae": mae.item(),
                           "train/margin_rank": float(margin_rank), "train/ranknet": float(ranknet),
                           "train/pair_acc": pair_acc, "train/baseline": baseline.item(),
                           "train/lr": scheduler.get_last_lr()[0], "epoch": epoch + g / n_groups}
                print(metrics)
                wandb.log(metrics)
            if (g + 1) % CKPT_EVERY == 0:
                save_checkpoint(latest, model, head, baseline, optimizer, scheduler, epoch, g + 1)

        model.eval()
        val_preds, val_gts = [], []
        with torch.no_grad():
            for sample in tqdm.tqdm(val_data, desc=f"val epoch {epoch + 1}"):
                pred = forward_paper(model, head, baseline, tokenizer, sample["items"], device)
                val_preds.append(pred.item())
                val_gts.append(sample["gt"])
        vp = torch.tensor(val_preds)
        vg = torch.tensor(val_gts)
        val_mae = (vp - vg).abs().mean().item()
        vmask = (vg[:, None] - vg[None, :]) > 0  # all pairs where gt_i > gt_j
        vdp = vp[:, None] - vp[None, :]
        val_pair_acc = (vdp[vmask] > 0).float().mean().item()
        wandb.log({"val/mae": val_mae, "val/pair_acc": val_pair_acc, "epoch": epoch + 1})
        print(f"epoch {epoch + 1}: val MAE = {val_mae:.4f}, val pair_acc = {val_pair_acc:.4f}")

        save_checkpoint(latest, model, head, baseline, optimizer, scheduler, epoch + 1, 0)
        ckpt = CKPT_DIR / f"epoch{epoch + 1}"
        ckpt.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(str(ckpt))
        torch.save(head.state_dict(), ckpt / "head.pt")
        (ckpt / "done").write_text(f"val_mae={val_mae}\n")
        print(f"saved {ckpt}")

    run.finish()

    from huggingface_hub import HfApi
    api = HfApi(token=os.environ["HF_TOKEN"])
    api.create_repo(HUB_REPO, repo_type="model", private=False, exist_ok=True)
    api.upload_folder(repo_id=HUB_REPO, folder_path=str(latest), repo_type="model")

    base_dir = CKPT_DIR / "base"
    base_dir.mkdir(parents=True, exist_ok=True)
    AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16).save_pretrained(str(base_dir))
    tokenizer.save_pretrained(str(base_dir))
    api.upload_folder(repo_id=HUB_REPO, folder_path=str(base_dir), path_in_repo="base", repo_type="model")
    print(f"pushed {latest} + base -> https://huggingface.co/{HUB_REPO}")


if __name__ == "__main__":
    main()
