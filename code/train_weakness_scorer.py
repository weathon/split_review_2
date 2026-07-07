"""LoRA-finetune Qwen/Qwen3-Embedding-4B + linear head to score papers.

Each paper's strength/weakness items are embedded (last-token pooling),
scored by a linear head (unbounded), and averaged into a paper score.
Loss: weighted MAE, w = 1 + |gt - 5|.

Resumable per epoch: checkpoints/weakness_scorer/epoch{N}/ with adapter + head.
"""

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

import json
import math
import random

import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

import torch
import torch.nn as nn
import tqdm
import wandb
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModel, AutoTokenizer

from paths import DATASETS_DIR

MODEL_NAME = "Qwen/Qwen3-Embedding-4B"
TRAIN_PATH = DATASETS_DIR / "weakness_score_train.jsonl"
VAL_PATH = DATASETS_DIR / "weakness_score_val.jsonl"
CKPT_DIR = (DATASETS_DIR / ".." / "checkpoints" / "weakness_scorer").resolve()

EPOCHS = 2
LR = 1e-4
LORA_R = 16
LORA_ALPHA = 32
GRAD_ACCUM = 8  # papers per optimizer step
MAX_LEN = 2048  # truncation authorized by user; expected never triggered
SEED = 0


def forward_paper(model, head, tokenizer, items, device):
    batch = tokenizer(
        items, padding=True, truncation=True, max_length=MAX_LEN,
        return_tensors="pt", padding_side="left",
    ).to(device)
    hidden = model(**batch).last_hidden_state  # [n_items, seq, h]
    pooled = hidden[:, -1]  # left padding -> last token is EOS
    item_scores = head(pooled.float()).squeeze(-1)  # [n_items]
    return item_scores.mean()


def main():
    random.seed(SEED)
    torch.manual_seed(SEED)
    device = "cuda"

    train_data = [json.loads(l) for l in open(TRAIN_PATH)]
    val_data = [json.loads(l) for l in open(VAL_PATH)]
    print(f"train {len(train_data)} papers, val {len(val_data)} papers")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    base = AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16)

    start_epoch = 0
    for e in range(EPOCHS, 0, -1):
        if (CKPT_DIR / f"epoch{e}" / "done").exists():
            start_epoch = e
            break
    if start_epoch == EPOCHS:
        print(f"all {EPOCHS} epochs already done at {CKPT_DIR}")
        return

    head = nn.Linear(base.config.hidden_size, 1)
    if start_epoch > 0:
        resume_dir = CKPT_DIR / f"epoch{start_epoch}"
        print(f"resuming from {resume_dir}")
        model = PeftModel.from_pretrained(base, str(resume_dir), is_trainable=True)
        head.load_state_dict(torch.load(resume_dir / "head.pt"))
    else:
        lora_cfg = LoraConfig(
            r=LORA_R, lora_alpha=LORA_ALPHA,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj"],
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

    run = wandb.init(project="weakness-score", config={
        "model": MODEL_NAME, "epochs": EPOCHS, "lr": LR, "lora_r": LORA_R,
        "lora_alpha": LORA_ALPHA, "grad_accum": GRAD_ACCUM, "max_len": MAX_LEN,
        "start_epoch": start_epoch,
    })
    print(f"wandb run: {run.url}")

    for epoch in range(start_epoch, EPOCHS):
        model.train()
        order = list(range(len(train_data)))
        random.Random(SEED + epoch).shuffle(order)
        optimizer.zero_grad()
        for step, idx in enumerate(tqdm.tqdm(order, desc=f"epoch {epoch + 1}")):
            sample = train_data[idx]
            pred = forward_paper(model, head, tokenizer, sample["items"], device)
            gt = sample["gt"]
            loss = (1 + abs(gt - 5)) * (pred - gt).abs()
            assert not torch.isnan(loss), f"NaN loss at paper {sample['paper_id']}"
            (loss / GRAD_ACCUM).backward()
            if (step + 1) % GRAD_ACCUM == 0:
                optimizer.step()
                optimizer.zero_grad()
            if step % 20 == 0:
                wandb.log({"train/loss": loss.item(),
                           "train/abs_err": abs(pred.item() - gt),
                           "epoch": epoch + step / len(order)})
        optimizer.step()
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

        ckpt = CKPT_DIR / f"epoch{epoch + 1}"
        ckpt.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(str(ckpt))
        torch.save(head.state_dict(), ckpt / "head.pt")
        (ckpt / "done").write_text(f"val_mae={val_mae}\n")
        print(f"saved {ckpt}")

    run.finish()


if __name__ == "__main__":
    main()
