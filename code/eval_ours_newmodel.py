"""Step 1 eval: score final_results/ours_cmp3_ours_v2 with the freshly trained
scorer, using gpt-oss-120b to split each AI review into atomic items.

Per-paper: gpt-oss split (cached) -> new scorer scores each item -> mean = pred.
Correlation/MAE vs gt_avg_score from scores.csv. Resumable (append per paper).
"""

import os
import json
import csv

import dotenv
dotenv.load_dotenv("/home/wg25r/split_review_opus_repro/.env")

import torch
import torch.nn as nn
import tqdm
from openai import OpenAI
from huggingface_hub import snapshot_download
from peft import PeftModel
from transformers import AutoModel, AutoTokenizer
from scipy.stats import pearsonr, spearmanr

BASE = "/home/wg25r/split_review_opus_repro/final_results/ours_cmp3_ours_v2"
OUT = "/home/wg25r/split_review_opus_repro/datasets/ours_newmodel_ossplit_preds.jsonl"
SPLIT_CACHE = "/home/wg25r/split_review_opus_repro/datasets/ours_ossplit_cache"
MAX_LEN = 2048
ITEM_BATCH = 32
CKPT = "weathon/review_scoring"

oai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])

SPLIT_PROMPT = """You are given the Strengths and Weaknesses sections of a paper review. Reformat them into two flat lists of atomic items.

Rules:
- Each item is ONE distinct point (usually one bullet or numbered entry). Keep a multi-sentence point together as a single item; do NOT split one point into separate sentences.
- If one block actually contains several separate enumerated points, split them into separate items.
- DISCARD anything that is not itself a substantive strength/weakness: lead-in sentences, pure reference/citation list lines, duplicated sentences, standalone section headers, pure typo-only enumerations.
- Preserve the original wording, INCLUDING inline citation markers like [1].
- Do not invent content.

Return ONLY a JSON object: {"strengths": ["...", ...], "weaknesses": ["...", ...]}.

Review:
"""


def section(md, header):
    start = md.find(header)
    if start == -1:
        return ""
    start += len(header)
    end = md.find("\n## ", start)
    return md[start:end] if end != -1 else md[start:]


def oss_split(pid, review_text):
    cache = os.path.join(SPLIT_CACHE, f"{pid}.json")
    if os.path.exists(cache):
        return json.loads(open(cache).read())
    for _ in range(4):
        try:
            resp = oai.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": SPLIT_PROMPT + review_text}],
                response_format={"type": "json_object"},
                # extra_body={"provider": {"only": ["cerebras"], "quantizations": ["fp16"]}},
            )
            out = json.loads(resp.choices[0].message.content)
            result = {"strengths": list(out["strengths"]), "weaknesses": list(out["weaknesses"])}
            open(cache, "w").write(json.dumps(result))
            return result
        except Exception as e:
            print(f"  [split] {pid} retry: {e}")
    print(f"  [split] SKIP {pid}")
    return None


os.makedirs(SPLIT_CACHE, exist_ok=True)
gt = {}
with open(f"{BASE}/scores.csv") as f:
    for row in csv.DictReader(f):
        gt[row["paper_id"]] = float(row["gt_avg_score"])
print(f"{len(gt)} papers in scores.csv")

done = set()
if os.path.exists(OUT):
    done = {json.loads(l)["paper_id"] for l in open(OUT)}
todo = [p for p in gt if p not in done]
print(f"resuming with {len(done)} done, {len(todo)} to do")

if todo:
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-4B")
    base = AutoModel.from_pretrained("Qwen/Qwen3-Embedding-4B", torch_dtype=torch.bfloat16)
    ckpt = snapshot_download(CKPT, token=os.environ["HF_TOKEN"],
                             allow_patterns=["adapter_*", "head.pt", "state.json"])
    print("state.json:", open(os.path.join(ckpt, "state.json")).read())
    model = PeftModel.from_pretrained(base, ckpt)
    head = nn.Linear(base.config.hidden_size, 1)
    head.load_state_dict(torch.load(os.path.join(ckpt, "head.pt")))
    model.to("cuda").eval()
    head.to("cuda").eval()

    def score(items):
        s = []
        for i in range(0, len(items), ITEM_BATCH):
            b = tokenizer(items[i:i + ITEM_BATCH], padding=True, truncation=True,
                          max_length=MAX_LEN, return_tensors="pt", padding_side="left").to("cuda")
            s.append(head(model(**b).last_hidden_state[:, -1].float()).squeeze(-1))
        return torch.cat(s)

    with torch.no_grad(), open(OUT, "a") as f:
        for pid in tqdm.tqdm(todo):
            md = open(f"{BASE}/reviews/{pid}.md").read()
            s_text = section(md, "## Strengths")
            w_text = section(md, "## Weaknesses")
            if not s_text.strip() and not w_text.strip():
                print(f"skip {pid}: no S/W sections")
                continue
            split = oss_split(pid, f"### Strengths\n{s_text}\n### Weaknesses\n{w_text}")
            if split is None:
                continue
            items = [f"strength: {x}" for x in split["strengths"] if x.strip()] \
                + [f"weakness: {x}" for x in split["weaknesses"] if x.strip()]
            if not items:
                continue
            pred = score(items).mean().item()
            f.write(json.dumps({"paper_id": pid, "gt": gt[pid], "pred": pred,
                                "n_items": len(items)}) + "\n")
            f.flush()

preds, gts = [], []
for l in open(OUT):
    r = json.loads(l)
    preds.append(r["pred"])
    gts.append(r["gt"])
errs = [abs(p - g) for p, g in zip(preds, gts)]
print(f"n = {len(preds)}")
print(f"pearson  = {pearsonr(preds, gts).statistic:.4f}")
print(f"spearman = {spearmanr(preds, gts).statistic:.4f}")
print(f"MAE      = {sum(errs)/len(errs):.4f}")
print(f"pred: min={min(preds):.2f} mean={sum(preds)/len(preds):.2f} max={max(preds):.2f}")
