"""Stage 1 — build the weakness-validity dataset.

For the 393-paper working subset (papers with datasets/iclr2026_new/papers/<id>.txt) that also
have a cached AC meta-review (datasets/iclr2026_new/ac_reviews/<id>.json), extract each human
reviewer's weaknesses and label them from the AC meta-review ONLY:

  INVALID = the AC explicitly says the concern was resolved/addressed AND it needed no paper edit
            (a clarification / an arguable point the AC dismisses).
  VALID   = the AC explicitly says the concern was NOT resolved / still stands.
  EXCLUDE = anything else (AC silent on it, or resolved only by editing the paper) -> dropped.

deepseek-v4-flash (OpenRouter) does extraction + labeling. No live OpenReview calls. Output:
meta/weakness_validity/dataset.jsonl + a saved HF dataset (local, no push).

Run: python meta/weakness_validity_dataset.py
"""
import asyncio
import json
import os
from pathlib import Path
from typing import Literal

import dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from datasets import Dataset

ROOT = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(ROOT / ".env")

DATA = ROOT / "datasets" / "iclr2026_new"
PAPER_DIR = DATA / "papers"
AC_DIR = DATA / "ac_reviews"
OUT_DIR = ROOT / "meta" / "weakness_validity"
MODEL = "deepseek/deepseek-v4-flash"
CONCURRENCY = 8

client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])


class Item(BaseModel):
    weakness: str
    label: Literal["invalid", "valid", "exclude"]
    ac_evidence: str
    needs_edit: bool


class Items(BaseModel):
    items: list[Item]


# OpenRouter's .parse() helper returns malformed output for deepseek-v4-flash, so we send an
# explicit strict json_schema via create() and validate the raw JSON with Items.
SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "weakness": {"type": "string"},
                    "label": {"type": "string", "enum": ["invalid", "valid", "exclude"]},
                    "ac_evidence": {"type": "string"},
                    "needs_edit": {"type": "boolean"},
                },
                "required": ["weakness", "label", "ac_evidence", "needs_edit"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


PROMPT = """You are labeling the weaknesses raised in ONE human review of an ICLR paper, using ONLY what the Area Chair (AC) meta-review explicitly says about each concern.

=== REVIEWER'S REVIEW ===
{review}

=== AC META-REVIEW (the ground truth — the ONLY thing you may use to decide resolved/unresolved) ===
{ac}

Instructions:
1. Extract each DISTINCT substantive weakness the reviewer raised (from the weaknesses and questions). EXCLUDE trivial items entirely: typos, grammar, wording, formatting, notation, missing citations, presentation/clarity nits.
2. For each weakness assign exactly one label, deciding ONLY from the AC meta-review's explicit statements (do NOT use your own judgement about whether the concern is valid):
   - "invalid": the AC explicitly states this concern was resolved / addressed / dismissed AND the resolution needed NO change to the paper (a clarification, or an arguable point the AC disagrees with / considers non-blocking). Set needs_edit=false.
   - "valid": the AC explicitly states this concern was NOT resolved / still stands / remains a problem. Set needs_edit as appropriate.
   - "exclude": the AC meta-review does not explicitly address this concern either way, OR the AC says it was resolved only by editing/adding to the paper (new experiments, added content, fixes). Set needs_edit=true if resolved-by-edit.
3. For every "invalid" and "valid" item, quote the exact AC sentence you relied on in ac_evidence. If you cannot cite an explicit AC sentence, the label MUST be "exclude".

Return the structured list of items."""


def review_text(hr):
    parts = []
    for k in ["summary", "strengths", "weaknesses", "questions"]:
        v = hr.get(k)
        if v:
            parts.append(f"[{k}]\n{v}")
    return "\n\n".join(parts)


def ac_text(node):
    c = node["content"]
    parts = []
    for k in ["summary", "reviewer_concerns", "reviewer_scores"]:
        v = c.get(k, {})
        val = v.get("value", "") if isinstance(v, dict) else v
        if val:
            parts.append(f"[{k}]\n{val}")
    return "\n\n".join(parts)


async def label_review(sem, pid, ridx, hr, ac, rec):
    parsed = None
    last = ""
    for attempt in range(3):
        async with sem:
            resp = await client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": PROMPT.format(review=review_text(hr), ac=ac)}],
                response_format={"type": "json_schema", "json_schema": {"name": "Items", "strict": True, "schema": SCHEMA}},
            )
        content = resp.choices[0].message.content or ""
        last = content
        try:
            parsed = Items.model_validate_json(content)
            break
        except Exception:
            i, j = content.find("{"), content.rfind("}")
            if i != -1 and j != -1:
                try:
                    parsed = Items.model_validate_json(content[i:j + 1])
                    break
                except Exception:
                    pass
    if parsed is None:
        raise RuntimeError(f"deepseek returned non-JSON for {pid} review {ridx} after 3 tries: {last!r}")
    rows = []
    for it in parsed.items:
        if it.label == "exclude":
            continue
        rows.append({
            "paper_id": pid,
            "review_idx": ridx,
            "weakness": it.weakness,
            "label": it.label,
            "ac_evidence": it.ac_evidence,
            "needs_edit": it.needs_edit,
            "decision": rec["decision"],
            "gt_binary": rec["gt_binary"],
            "paper_path": str(PAPER_DIR / f"{pid}.txt"),
        })
    return rows


async def main():
    notes = {r["paper_id"]: r for r in json.load(open(DATA / "all_notes.json"))}
    pids = sorted(
        p.stem for p in PAPER_DIR.glob("*.txt")
        if (AC_DIR / f"{p.stem}.json").exists() and p.stem in notes
    )
    print(f"papers: {len(pids)}")

    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = []
    for pid in pids:
        rec = notes[pid]
        ac = ac_text(json.load(open(AC_DIR / f"{pid}.json"))[0])
        for ridx, hr in enumerate(rec["human_reviews"]):
            tasks.append(label_review(sem, pid, ridx, hr, ac, rec))
    print(f"review-level deepseek calls: {len(tasks)}")

    rows = [r for sub in await asyncio.gather(*tasks) for r in sub]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "dataset.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    Dataset.from_list(rows).save_to_disk(str(OUT_DIR / "hf_dataset"))

    n_valid = sum(1 for r in rows if r["label"] == "valid")
    n_invalid = sum(1 for r in rows if r["label"] == "invalid")
    n_acc = sum(1 for r in rows if r["gt_binary"] == "Accept")
    print(f"rows: {len(rows)} | valid: {n_valid} | invalid: {n_invalid} | accept-paper rows: {n_acc} | reject-paper rows: {len(rows)-n_acc}")
    print(f"wrote {OUT_DIR/'dataset.jsonl'} and {OUT_DIR/'hf_dataset'}")


if __name__ == "__main__":
    asyncio.run(main())
