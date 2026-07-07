"""Stage 2 — Claude-SDK classifier over the weakness-validity dataset.

For each (paper_id, review_idx) group in meta/weakness_validity/dataset.jsonl, reconstruct the full
review text (from all_notes.json human_reviews[review_idx]) and the ordered list of that review's
labeled weakness items, then ask claude-sonnet-5 (given the paper-text FILE PATH — not inlined,
SDK content-limit bug — plus the full review) to predict valid/invalid for EACH item.

Concurrency 2. Read tool enabled so the model opens the paper file itself. The predictions are
aligned to the gold items by item_index, with a hard assertion (raise on any mismatch — no
padding/truncation). Output: meta/weakness_validity/predictions.jsonl.

Run: python meta/weakness_validity_classifier.py
"""
import asyncio
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "datasets" / "iclr2026_new"
OUT_DIR = ROOT / "meta" / "weakness_validity"
MODEL = "claude-sonnet-5"
CONCURRENCY = 2


def review_text(hr):
    parts = []
    for k in ["summary", "strengths", "weaknesses", "questions"]:
        v = hr.get(k)
        if v:
            parts.append(f"[{k}]\n{v}")
    return "\n\n".join(parts)


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # With the Read tool the model emits narration before the final JSON object.
        i, j = text.find("{"), text.rfind("}")
        if i == -1 or j == -1:
            raise
        return json.loads(text[i:j + 1])


PROMPT = """You are judging whether the weaknesses a reviewer raised about a scientific paper are VALID or INVALID.

First, read the full paper. It is on disk at:
{paper_path}
Use the Read tool to read that file before answering.

Here is the reviewer's full review:
=== REVIEW ===
{review}

Below are the specific weakness items extracted from this review. For EACH item, decide:
- "valid"  = a genuine, substantiated weakness of THIS paper that would require the authors to change/improve the paper.
- "invalid" = an acceptable / arguable / non-blocking point (a misunderstanding, an already-addressed concern, a matter of clarification, or an unreasonable demand) that should NOT count against the paper.

=== WEAKNESS ITEMS ===
{items}

Return ONLY JSON, no prose, no code fences:
{{"predictions": [{{"item_index": <int>, "prediction": "valid" or "invalid"}}]}}
Return exactly one prediction object per weakness item, using the item_index shown above."""


async def query_claude(prompt):
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

    opts = ClaudeAgentOptions(
        model=MODEL,
        allowed_tools=["Read"],
        permission_mode="bypassPermissions",
        disallowed_tools=["Glob", "Grep", "Bash", "Edit", "Write", "WebSearch", "WebFetch"],
        max_turns=6,
        cwd="/tmp",
    )
    text = ""
    async with ClaudeSDKClient(options=opts) as sdk:
        await sdk.query(prompt)
        async for m in sdk.receive_response():
            if isinstance(m, AssistantMessage):
                for b in m.content:
                    if isinstance(b, TextBlock):
                        text += b.text
    return text


async def classify_group(sem, wlock, fout, key, group, hr):
    pid, ridx = key
    paper_path = group[0]["paper_path"]
    items_txt = "\n".join(f"{i}. {row['weakness']}" for i, row in enumerate(group))
    prompt = PROMPT.format(paper_path=paper_path, review=review_text(hr), items=items_txt)
    for attempt in range(3):
        try:
            async with sem:
                out = await query_claude(prompt)
            preds = extract_json(out)["predictions"]
            by_idx = {p["item_index"]: p["prediction"] for p in preds}
            if len(by_idx) != len(group) or set(by_idx) != set(range(len(group))):
                raise RuntimeError(f"misalignment: got {sorted(by_idx)}, expected 0..{len(group)-1}")
            rows = [{
                "paper_id": pid,
                "review_idx": ridx,
                "item_index": i,
                "weakness": row["weakness"],
                "gold": row["label"],
                "pred": by_idx[i],
            } for i, row in enumerate(group)]
        except Exception as e:
            print(f"  retry {pid} r{ridx} attempt {attempt+1}: {type(e).__name__}: {str(e)[:120]}")
            continue
        async with wlock:
            fout.write("".join(json.dumps(r) + "\n" for r in rows))
            fout.flush()
        return len(rows)
    print(f"  SKIP {pid} r{ridx} after 3 tries")
    return None


async def main():
    notes = {r["paper_id"]: r for r in json.load(open(DATA / "all_notes.json"))}
    data = [json.loads(l) for l in open(OUT_DIR / "dataset.jsonl")]
    groups = {}
    for row in data:
        groups.setdefault((row["paper_id"], row["review_idx"]), []).append(row)

    pred_path = OUT_DIR / "predictions.jsonl"
    done = set()
    if pred_path.exists():
        for l in open(pred_path):
            r = json.loads(l)
            done.add((r["paper_id"], r["review_idx"]))
    todo = {k: g for k, g in groups.items() if k not in done}
    print(f"dataset rows: {len(data)} | groups: {len(groups)} | already done: {len(done)} | todo: {len(todo)}")

    sem = asyncio.Semaphore(CONCURRENCY)
    wlock = asyncio.Lock()
    with open(pred_path, "a") as fout:
        tasks = [
            classify_group(sem, wlock, fout, key, group, notes[key[0]]["human_reviews"][key[1]])
            for key, group in todo.items()
        ]
        res = await asyncio.gather(*tasks)
    ok = sum(1 for x in res if x is not None)
    skipped = [k for k, x in zip(todo.keys(), res) if x is None]
    print(f"classified groups this run: {ok} | skipped groups: {len(skipped)}")
    if skipped:
        print("skipped:", skipped)
    print(f"wrote/appended {pred_path}")


if __name__ == "__main__":
    asyncio.run(main())
