import argparse
import asyncio
import json
import random
import re
import time
from pathlib import Path

import dotenv

ROOT = Path(__file__).parent.parent
FINAL = ROOT / "final_results"

METHODS = {
    "ours_cmp3_ours_v2": {"dir": FINAL / "ours_cmp3_ours_v2" / "reviews", "kind": "single_md"},
    "nocal_cmp3_nocal_v3": {"dir": FINAL / "nocal_cmp3_nocal_v3" / "reviews", "kind": "single_md"},
    "baseline_cmp3_baseline_v2": {"dir": FINAL / "baseline_cmp3_baseline_v2" / "reviews", "kind": "single_md"},
    "cspaper": {"dir": FINAL / "cspaper", "kind": "cspaper_md"},
    "DeepReviewer_14B": {"dir": FINAL / "DeepReviewer_14B", "kind": "deepreviewer_json"},
    "DeepReviewer-v2-openai": {"dir": FINAL / "DeepReviewer-v2-openai", "kind": "single_md"},
}

OUT_DIR = Path(__file__).parent / "hivemind_outputs"
OUT_DIR.mkdir(exist_ok=True)

JUDGE_MODEL = "claude-sonnet-5"
MAX_RETRIES = 5
RETRY_DELAY = 5

PROMPT = """You are comparing two paper reviews written by the SAME reviewer agent on TWO DIFFERENT papers. Identify each item in the WEAKNESS section of review 1 and, for each one, decide whether review 2 contains a SIMILAR weakness item — the same kind of methodological/presentation complaint applied to the other paper (e.g. "missing ablation", "no statistical significance", "overclaimed novelty", "writing/typos", "weak baselines").

Two items match if they describe the SAME KIND of problem, even when applied to different content. They do NOT match merely because both mention the same topic.

For each weakness item in review 1, output the item text and either the matching item summary from review 2, or null if there is no match.

=== REVIEW 1 (paper {pid1}) ===
{r1}

=== REVIEW 2 (paper {pid2}) ===
{r2}

Respond with ONLY a JSON object matching this exact shape, no other text, no markdown code fences:
{{"review1_weakness_items": [{{"text": "<weakness item text from review 1>", "match_in_review2": "<matching item summary from review 2, or null>"}}]}}
"""

CSPAPER_RE = re.compile(r"^(.+)__ICLR_main_2026_2\.md$")


def list_papers(method_name):
    cfg = METHODS[method_name]
    d = cfg["dir"]
    if cfg["kind"] == "single_md":
        return {f.stem for f in d.iterdir() if f.suffix == ".md"}
    if cfg["kind"] == "cspaper_md":
        ids = set()
        for f in d.iterdir():
            m = CSPAPER_RE.match(f.name)
            if m:
                ids.add(m.group(1))
        return ids
    if cfg["kind"] == "deepreviewer_json":
        return {f.name[: -len(".txt.json")] for f in d.iterdir() if f.name.endswith(".txt.json")}
    raise ValueError(cfg["kind"])


def load_review(method_name, pid, rng):
    cfg = METHODS[method_name]
    d = cfg["dir"]
    if cfg["kind"] == "single_md":
        p = d / f"{pid}.md"
        return p.read_text() if p.exists() else None
    if cfg["kind"] == "cspaper_md":
        p = d / f"{pid}__ICLR_main_2026_2.md"
        return p.read_text() if p.exists() else None
    if cfg["kind"] == "deepreviewer_json":
        p = d / f"{pid}.txt.json"
        if not p.exists():
            return None
        data = json.load(open(p))
        reviews = data["results"][0]["reviews"]
        if not reviews:
            return None
        return rng.choice(reviews)["text"]


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return json.loads(text)


async def _query_claude_sdk(prompt: str) -> str:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

    options = ClaudeAgentOptions(
        model=JUDGE_MODEL,
        allowed_tools=[],
        permission_mode="bypassPermissions",
        disallowed_tools=["Read", "Glob", "Grep", "Bash", "Edit", "Write", "WebSearch", "WebFetch"],
        max_turns=1,
        cwd="/tmp",
    )

    result_text = ""
    async with ClaudeSDKClient(options=options) as sdk_client:
        await sdk_client.query(prompt)
        async for message in sdk_client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        result_text += block.text
    return result_text


async def judge(method, pid1, pid2, r1, r2):
    prompt = PROMPT.format(pid1=pid1, pid2=pid2, r1=r1, r2=r2)
    parsed = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result_text = await _query_claude_sdk(prompt)
            if not result_text.strip():
                raise RuntimeError("empty response")
            parsed = _extract_json(result_text)
            items_raw = parsed["review1_weakness_items"]
            items = [{"text": it["text"], "match_in_review2": it.get("match_in_review2")} for it in items_raw]
            break
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise
            print(f"  retry {attempt}/{MAX_RETRIES} {method} {pid1}/{pid2}: {type(e).__name__}: {e}")
            await asyncio.sleep(RETRY_DELAY * attempt)
    total = len(items)
    matched = sum(1 for it in items if it["match_in_review2"])
    rate = matched / total if total else None
    return {
        "method": method,
        "paper1": pid1,
        "paper2": pid2,
        "n_items_review1": total,
        "n_matched": matched,
        "overlap_rate": rate,
        "items": items,
    }


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n_base", type=int, default=30, help="number of base papers")
    ap.add_argument("--n_partners", type=int, default=3, help="partner papers per base")
    ap.add_argument("--concurrency", type=int, default=5)
    ap.add_argument("--out", type=str, default=str(OUT_DIR / "overlap_results_final_claude_sdk.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)

    method_papers = {m: list_papers(m) for m in METHODS}
    for m, s in method_papers.items():
        print(f"{m}: {len(s)} papers")
    common = set.intersection(*method_papers.values())
    print(f"common across all methods: {len(common)}")
    common_sorted = sorted(common)

    if len(common_sorted) < args.n_partners + 1:
        raise RuntimeError(f"need at least {args.n_partners + 1} papers in common")

    bases = rng.sample(common_sorted, min(args.n_base, len(common_sorted)))
    pairs = []
    for base in bases:
        pool = [p for p in common_sorted if p != base]
        partners = rng.sample(pool, args.n_partners)
        for partner in partners:
            pairs.append((base, partner))

    print(f"sampled {len(pairs)} paper pairs")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_f = open(out_path, "w")
    write_lock = asyncio.Lock()
    sem = asyncio.Semaphore(args.concurrency)

    async def run_one(method, pid1, pid2):
        reviewer_rng = random.Random(f"{args.seed}-{method}-{pid1}-{pid2}")
        r1 = load_review(method, pid1, reviewer_rng)
        r2 = load_review(method, pid2, reviewer_rng)
        if r1 is None or r2 is None:
            print(f"  skip {method} {pid1} {pid2}: missing review")
            return
        async with sem:
            try:
                rec = await judge(method, pid1, pid2, r1, r2)
            except Exception as e:
                print(f"  err {method} {pid1} {pid2}: {type(e).__name__}: {e}")
                return
        async with write_lock:
            out_f.write(json.dumps(rec) + "\n")
            out_f.flush()
        print(f"  done {method} {pid1}/{pid2}: {rec['n_matched']}/{rec['n_items_review1']} rate={rec['overlap_rate']}")

    await asyncio.gather(*(run_one(method, pid1, pid2) for pid1, pid2 in pairs for method in METHODS))
    out_f.close()

    print(f"\nwrote {out_path}")
    by_method = {}
    with open(out_path) as f:
        for line in f:
            r = json.loads(line)
            by_method.setdefault(r["method"], []).append(r)
    print("\n=== mean overlap rate (weakness, review1 -> review2) ===")
    for m in METHODS:
        rs = [r["overlap_rate"] for r in by_method.get(m, []) if r["overlap_rate"] is not None]
        if rs:
            print(f"  {m}: mean={sum(rs)/len(rs):.3f} n={len(rs)}")
        else:
            print(f"  {m}: no data")


if __name__ == "__main__":
    dotenv.load_dotenv(ROOT / ".env")
    asyncio.run(main())
