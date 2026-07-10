"""LoRA-finetune Qwen/Qwen3-Embedding-4B + linear head to score papers.

Each paper's strength/weakness items are embedded (last-token pooling),
scored by a linear head (unbounded), and averaged into a paper score.
Loss: weighted MAE, w = 1 + |gt - 5|.

Resumable: checkpoints/weakness_scorer/latest/ (adapter + head + optimizer +
step position) written every 200 steps; epoch{N}/ kept as end-of-epoch records.
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

MODEL_NAME = "Qwen/Qwen3-Embedding-4B"
DATASET_NAME = "weathon/weakness-score"
HUB_REPO = "weathon/review_scoring"
CKPT_DIR = (Path.cwd() / "checkpoints" / "weakness_scorer").resolve()

EPOCHS = 3
LR = 1e-4
LORA_R = 32
LORA_ALPHA = 32
MAX_LEN = 2048
SEED = 0
CKPT_EVERY = 200
ITEM_BATCH = 32
WARMUP_FRAC = 0.03

PAIR_B = 8          # papers per group: intra-group pairs + one optimizer step
MARGIN_LAMBDA = 0.5   # total = MAE + MARGIN_LAMBDA*margin_ranking + RANKNET_LAMBDA*ranknet
RANKNET_LAMBDA = 0.5


def save_checkpoint(ckpt, model, head, optimizer, scheduler, epoch, step):
    # write to tmp then rename, so a crash mid-save never corrupts the resume point
    tmp = ckpt.parent / (ckpt.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    model.save_pretrained(str(tmp))
    torch.save(head.state_dict(), tmp / "head.pt")
    torch.save(optimizer.state_dict(), tmp / "optimizer.pt")
    torch.save(scheduler.state_dict(), tmp / "scheduler.pt")
    (tmp / "state.json").write_text(json.dumps({"epoch": epoch, "step": step}))
    if ckpt.exists():
        shutil.rmtree(ckpt)
    tmp.rename(ckpt)


def forward_paper(model, head, tokenizer, items, device):
    chunk_scores = []
    for i in range(0, len(items), ITEM_BATCH):
        batch = tokenizer(
            items[i:i + ITEM_BATCH], padding=True, truncation=True, max_length=MAX_LEN,
            return_tensors="pt", padding_side="left",
        ).to(device)
        hidden = model(**batch).last_hidden_state
        pooled = hidden[:, -1]  # left padding -> last token is EOS
        chunk_scores.append(head(pooled.float()).squeeze(-1))
    return torch.cat(chunk_scores).mean()


def main():
    random.seed(SEED)
    torch.manual_seed(SEED)
    device = "cuda"

    ds = load_dataset(DATASET_NAME, token=os.environ["HF_TOKEN"])
    train_data = list(ds["train"])
    val_data = list(ds["validation"])
    print(f"train {len(train_data)} papers, val {len(val_data)} papers")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    base = AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16)

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
    else:
        start_epoch, start_step = 0, 0
        lora_cfg = LoraConfig(
            r=LORA_R, lora_alpha=LORA_ALPHA,
            target_modules="all-linear",
        )
        model = get_peft_model(base, lora_cfg)
    model.print_trainable_parameters()
    model.to(device)
    head.to(device)
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()

    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad] + list(head.parameters()),
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
        "warmup_frac": WARMUP_FRAC, "total_steps": total_steps,
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
            preds = torch.stack([forward_paper(model, head, tokenizer, train_data[j]["items"], device)
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
                           "train/pair_acc": pair_acc,
                           "train/lr": scheduler.get_last_lr()[0], "epoch": epoch + g / n_groups}
                print(metrics)
                wandb.log(metrics)
            if (g + 1) % CKPT_EVERY == 0:
                save_checkpoint(latest, model, head, optimizer, scheduler, epoch, g + 1)

        model.eval()
        val_preds, val_gts = [], []
        with torch.no_grad():
            for sample in tqdm.tqdm(val_data, desc=f"val epoch {epoch + 1}"):
                pred = forward_paper(model, head, tokenizer, sample["items"], device)
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

        save_checkpoint(latest, model, head, optimizer, scheduler, epoch + 1, 0)
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
