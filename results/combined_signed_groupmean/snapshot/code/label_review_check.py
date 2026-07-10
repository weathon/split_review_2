import os
import re
import json
import math

import dotenv
dotenv.load_dotenv("/home/wg25r/split_review_opus_repro/.env")

import torch
import torch.nn as nn
from openai import OpenAI
from huggingface_hub import snapshot_download
from peft import PeftModel
from transformers import AutoModel, AutoTokenizer

PAPER_ID = "00ezkB2iZf"
CAL_DIR = "/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration"
OUT_DIR = "/home/wg25r/split_review_opus_repro/results/label_check"
SCORER_CKPT = "weathon/review_scoring_signed_groupmean"
DEVICE = "cuda:2"
MAX_LEN = 2048
ITEM_BATCH = 32

oai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])

OSS_PROMPT = """Split the following review {kind} into a flat list of atomic items. Each item is ONE distinct point; keep multi-sentence points together; split enumerated multi-point blocks. Discard lead-in sentences, pure reference/citation lines, duplicated sentences, standalone headers, typo-only lines. Preserve the original wording including inline citations like [1]. Do not invent content.

Return ONLY JSON: {{"items": ["...", ...]}}.

{kind}:
"""

_SECTION_END = re.compile(
    r"\n(?:### (?:Rating|Rating Number|Confidence|Summary|Strengths|Weaknesses|"
    r"Questions|Limitations|Soundness|Presentation|Contribution)\n|## |---)"
)

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-4B")
base_m = AutoModel.from_pretrained("Qwen/Qwen3-Embedding-4B", torch_dtype=torch.bfloat16)
ckpt = snapshot_download(SCORER_CKPT, token=os.environ["HF_TOKEN"],
                         allow_patterns=["adapter_*", "head.pt", "baseline.pt", "state.json"])
print("state.json:", open(os.path.join(ckpt, "state.json")).read().strip())
baseline = torch.load(os.path.join(ckpt, "baseline.pt"))
print("baseline:", float(baseline))
model = PeftModel.from_pretrained(base_m, ckpt)
head = nn.Linear(base_m.config.hidden_size, 1)
head.load_state_dict(torch.load(os.path.join(ckpt, "head.pt")))
model.to(DEVICE).eval()
head.to(DEVICE).eval()


def score_items(items):
    scores = []
    with torch.no_grad():
        for i in range(0, len(items), ITEM_BATCH):
            batch = tok(items[i:i + ITEM_BATCH], padding=True, truncation=True,
                        max_length=MAX_LEN, return_tensors="pt", padding_side="left").to(DEVICE)
            pooled = model(**batch).last_hidden_state[:, -1]
            scores.extend(head(pooled.float()).squeeze(-1).tolist())
    return scores


def oss_atomize(text, kind):
    label = "Strengths" if kind == "strength" else "Weaknesses"
    resp = oai.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": OSS_PROMPT.format(kind=label) + text}],
        response_format={"type": "json_object"},
        extra_body={"provider": {"only": ["cerebras"], "quantizations": ["fp16"]}},
    )
    return list(json.loads(resp.choices[0].message.content)["items"])


review_md = open(f"{CAL_DIR}/{PAPER_ID}.md").read()

spans = []
for header, kind in (("### Strengths", "strength"), ("### Weaknesses", "weakness")):
    start = 0
    while True:
        idx = review_md.find(header + "\n", start)
        if idx == -1:
            break
        body_start = idx + len(header) + 1
        m = _SECTION_END.search(review_md, body_start)
        body_end = m.start() if m else len(review_md)
        spans.append((body_start, body_end, kind))
        start = body_end
if not spans:
    raise ValueError("no strength/weakness sections found")
spans.sort()

all_signed = {"strength": [], "weakness": []}
out, cur = [], 0
for body_start, body_end, kind in spans:
    out.append(review_md[cur:body_start])
    items = oss_atomize(review_md[body_start:body_end], kind)
    if items:
        raw = score_items([f"{kind}: {t}" for t in items])
        lines = []
        for t, s in zip(items, raw):
            mag = 10 / (1 + math.exp(-s))
            signed = mag if kind == "strength" else -mag
            all_signed[kind].append(mag)
            lines.append(f"- {t} **[impact={signed:+.2f}]** (raw={s:+.3f})")
        out.append("\n".join(lines) + "\n")
    cur = body_end
out.append(review_md[cur:])
annotated = "".join(out)

s_mean = sum(all_signed["strength"]) / len(all_signed["strength"])
w_mean = sum(all_signed["weakness"]) / len(all_signed["weakness"])
pred = float(baseline) + (s_mean - w_mean) / 2
summary = (f"\n\n---\n## Scorer check\n"
           f"- baseline = {float(baseline):.4f}\n"
           f"- mean(strength mags) = {s_mean:.4f} (n={len(all_signed['strength'])})\n"
           f"- mean(weakness mags) = {w_mean:.4f} (n={len(all_signed['weakness'])})\n"
           f"- pred = baseline + (s_mean - w_mean)/2 = {pred:.4f}\n")

os.makedirs(OUT_DIR, exist_ok=True)
path = f"{OUT_DIR}/{PAPER_ID}.md"
open(path, "w").write(annotated + summary)
print(f"wrote {path}")
print(summary)
