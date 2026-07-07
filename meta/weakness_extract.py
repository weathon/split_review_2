"""STAGE 1 — extract weakness items and label validity from AC meta-review.

Working set: the 197 forum ids present in ALL of datasets/iclr2026_new/{human_reviews,ac_reviews,papers}.
Raw reviews come from all_notes.json (each paper's human_reviews[].weaknesses).
AC meta-review comes from ac_reviews/<id>.json (fields: summary, reviewer_concerns, reviewer_scores).

Per weakness item, deepseek-v4-flash decides:
  - ac_status: resolved / unresolved / not_mentioned   (grounded ONLY in what the AC explicitly says)
  - needs_editing: whether addressing it requires changing the paper (new experiments/results/rewrite)
                   vs. mere clarification / an arguable point that needs no edit.

Label (assigned in code, not by the model):
  resolved   & not needs_editing -> invalid
  resolved   & needs_editing     -> excluded (dropped)
  unresolved                     -> valid
  not_mentioned                  -> skipped (AC never spoke to it)

Output: one json per paper at meta/weakness_validity_out/stage1/<id>.json holding the raw model items.
Resume: skip a paper whose output file already exists.
Run: python meta/weakness_extract.py
"""
import json
import os
import time
from pathlib import Path

import dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

ROOT = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(ROOT / ".env")

DATA = ROOT / "datasets" / "iclr2026_new"
OUT = Path(__file__).parent / "weakness_validity_out" / "stage1"
OUT.mkdir(parents=True, exist_ok=True)

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
MODEL = "deepseek/deepseek-v4-flash"
MAX_RETRIES = 5
RETRY_DELAY = 5


class Item(BaseModel):
    weakness_text: str
    reviewer_index: int
    ac_status: Literal["resolved", "unresolved", "not_mentioned"]
    ac_evidence: str  # the exact AC sentence that establishes the status; "" only when not_mentioned
    needs_editing: bool


class Extraction(BaseModel):
    items: list[Item]


PROMPT = """You are given the official reviewer WEAKNESSES for one paper and the Area Chair (AC) meta-review of the same paper. The paper is post-rebuttal; the AC meta-review is the authoritative statement of which reviewer concerns were resolved during discussion and which remain.

Do two things.

1. Split the reviewers' weaknesses into DISTINCT weakness items. Keep each item's wording verbatim from the review (you may trim to the single concern, but do not paraphrase). Record which reviewer (0-indexed, in the order given) it came from.

2. For each weakness item, decide, grounded ONLY in what the AC meta-review explicitly says (never your own reading of the rebuttal):
   - ac_status:
       "resolved"      -> the AC explicitly states this specific concern was addressed / resolved / no longer a concern.
       "unresolved"    -> the AC explicitly lists this specific concern as remaining / still a problem / a reason weighing against the paper.
       "not_mentioned" -> the AC meta-review does not speak to this specific concern either way.
     Do NOT infer resolution from the reviewers or from score changes; require an explicit AC statement.
   - ac_evidence: the exact AC sentence that establishes the status (empty string only when not_mentioned).
   - needs_editing: whether actually satisfying this concern requires CHANGING THE PAPER (running new experiments, adding results, restructuring, correcting content). Set false when the concern is a request for clarification, a misunderstanding, or an arguable point that can be settled by explanation without editing the paper.

=== REVIEWER WEAKNESSES ===
{weaknesses}

=== AC META-REVIEW ===
{ac}
"""


def working_ids():
    ac = set(f[:-5] for f in os.listdir(DATA / "ac_reviews") if f.endswith(".json"))
    pap = set(f[:-4] for f in os.listdir(DATA / "papers") if f.endswith(".txt"))
    hum = set(f[:-3] for f in os.listdir(DATA / "human_reviews") if f.endswith(".md"))
    return sorted(ac & pap & hum)


notes = {x["paper_id"]: x for x in json.load(open(DATA / "all_notes.json"))}

ids = working_ids()
print(f"working set: {len(ids)} papers")

for pid in ids:
    out_path = OUT / f"{pid}.json"
    if out_path.exists():
        continue

    reviews = notes[pid]["human_reviews"]
    weakness_blocks = []
    for i, r in enumerate(reviews):
        weakness_blocks.append(f"--- Reviewer {i} ---\n{r['weaknesses']}")
    weaknesses_text = "\n\n".join(weakness_blocks)

    ac_notes = json.load(open(DATA / "ac_reviews" / f"{pid}.json"))
    ac_parts = []
    for n in ac_notes:
        for k, v in n["content"].items():
            ac_parts.append(f"[{k}] {v['value']}")
    ac_text = "\n".join(ac_parts)

    prompt = PROMPT.format(weaknesses=weaknesses_text, ac=ac_text)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.chat.completions.parse(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format=Extraction,
                extra_body={"reasoning": {"enabled": True}},
            )
            parsed = resp.choices[0].message.parsed
            break
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise
            print(f"  retry {attempt}/{MAX_RETRIES} {pid}: {type(e).__name__}: {e}")
            time.sleep(RETRY_DELAY * attempt)

    record = {
        "paper_id": pid,
        "decision": notes[pid]["decision"],
        "n_reviewers": len(reviews),
        "items": [it.model_dump() for it in parsed.items],
        "usage": resp.usage.model_dump() if resp.usage else None,
    }
    json.dump(record, open(out_path, "w"), indent=1)
    print(f"{pid}: {len(record['items'])} items")

print("stage 1 done")
