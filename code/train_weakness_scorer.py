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

EPOCHS = 2
LR = 1e-4
LORA_R = 16
LORA_ALPHA = 32
GRAD_ACCUM = 8
MAX_LEN = 2048
SEED = 0
CKPT_EVERY = 200
ITEM_BATCH = 32
WARMUP_FRAC = 0.03


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
    steps_per_epoch = len(train_data) // GRAD_ACCUM + 1
    total_steps = EPOCHS * steps_per_epoch
    scheduler = get_cosine_schedule_with_warmup(
        optimizer, num_warmup_steps=round(WARMUP_FRAC * total_steps),
        num_training_steps=total_steps,
    )
    if latest.exists():
        optimizer.load_state_dict(torch.load(latest / "optimizer.pt"))
        scheduler.load_state_dict(torch.load(latest / "scheduler.pt"))

    run = wandb.init(project="weakness-score", config={
        "model": MODEL_NAME, "epochs": EPOCHS, "lr": LR, "lora_r": LORA_R,
        "lora_alpha": LORA_ALPHA, "grad_accum": GRAD_ACCUM, "max_len": MAX_LEN,
        "ckpt_every": CKPT_EVERY, "warmup_frac": WARMUP_FRAC, "total_steps": total_steps,
        "start_epoch": start_epoch, "start_step": start_step,
    })
    print(f"wandb run: {run.url}")

    for epoch in range(start_epoch, EPOCHS):
        model.train()
        order = list(range(len(train_data)))
        random.Random(SEED + epoch).shuffle(order)  # deterministic, so mid-epoch resume can skip forward
        optimizer.zero_grad()
        skip = start_step if epoch == start_epoch else 0
        for step in tqdm.tqdm(range(skip, len(order)), desc=f"epoch {epoch + 1}",
                              initial=skip, total=len(order)):
            sample = train_data[order[step]]
            pred = forward_paper(model, head, tokenizer, sample["items"], device)
            gt = sample["gt"]
            loss = (1 + abs(gt - 5)) * (pred - gt).abs()
            assert not torch.isnan(loss), f"NaN loss at paper {sample['paper_id']}"
            (loss / GRAD_ACCUM).backward()
            if (step + 1) % GRAD_ACCUM == 0:
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
            if step % 20 == 0:
                wandb.log({"train/loss": loss.item(),
                           "train/abs_err": abs(pred.item() - gt),
                           "train/lr": scheduler.get_last_lr()[0],
                           "epoch": epoch + step / len(order)})
            if (step + 1) % CKPT_EVERY == 0:
                save_checkpoint(latest, model, head, optimizer, scheduler, epoch, step + 1)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

        model.eval()
        abs_errs = []
        with torch.no_grad():
            for sample in tqdm.tqdm(val_data, desc=f"val epoch {epoch + 1}"):
                pred = forward_paper(model, head, tokenizer, sample["items"], device)
                abs_errs.append(abs(pred.item() - sample["gt"]))
        val_mae = sum(abs_errs) / len(abs_errs)
        wandb.log({"val/mae": val_mae, "epoch": epoch + 1})
        print(f"epoch {epoch + 1}: val MAE = {val_mae:.4f}")

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
    print(f"pushed {latest} -> https://huggingface.co/{HUB_REPO}")


if __name__ == "__main__":
    main()
