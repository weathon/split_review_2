import concurrent.futures
import json
import os
import random
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_ROOT = Path(__file__).resolve().parents[1]

FINAL = REPO_ROOT / "final_results"
PAPER_DIR = REPO_ROOT / "datasets" / "iclr2026_new" / "papers"
GUIDELINE_PATH = SCRIPT_ROOT / "outputs" / "weakness_reliability_guideline.md"
OUTPUT_PATH = SCRIPT_ROOT / "outputs" / "final_results_weaknesses_glm52.jsonl"
SAMPLED_IDS_PATH = SCRIPT_ROOT / "outputs" / "final_results_subset_ids.json"

MODEL = "z-ai/glm-5.2"
TEMPERATURE = 1.0
PARALLEL = 30
SAMPLE_SIZE = None  # None = use the whole common population
SEED = 0

METHODS = {
    "ours_cmp3_ours_v2": {"dir": FINAL / "ours_cmp3_ours_v2" / "reviews", "kind": "single_md"},
    "nocal_cmp3_nocal_v3": {"dir": FINAL / "nocal_cmp3_nocal_v3" / "reviews", "kind": "single_md"},
    "baseline_cmp3_baseline_v2": {"dir": FINAL / "baseline_cmp3_baseline_v2" / "reviews", "kind": "single_md"},
    "cspaper": {"dir": FINAL / "cspaper", "kind": "cspaper_md"},
    "DeepReviewer_14B": {"dir": FINAL / "DeepReviewer_14B", "kind": "deepreviewer_json"},
    "DeepReviewer-v2-openai": {"dir": FINAL / "DeepReviewer-v2-openai", "kind": "single_md"},
}

CSPAPER_RE = re.compile(r"^(.+)__ICLR_main_2026_2\.md$")

ERROR_TYPE_TABLE = """| Error Type | Explanation |
|---|---|
| Misunderstanding | The reviewer misinterprets claims or ideas presented in the paper, leading to inaccurate or irrelevant comments. |
| Neglect | The reviewer overlooks important details explicitly stated in the paper, resulting in unwarranted questions or critiques. |
| Vague Critique | The review lacks specificity, claiming missing components without clearly identifying what is missing. |
| Out-of-scope | The reviewer suggests additional methods, experiments, or analyses that are beyond the intended scope of the paper. |
| Invalid Criticism | The reviewer's criticism is considered invalid, especially when suggesting impractical experiments or trivializing results. |
| Superficial Review | The reviewer appears to have only skimmed the paper, providing generic or unsupported comments about the presence or absence of weaknesses. |
| Unstated statement | Statements made in the review are not supported by content in the paper. |
| Excessive demands | if the weaknesses are just asking for excessive things that are not necessary for a good paper. |
| Generic comment | weaknesses are just generic comments that can apply to any paper, without really pointing out the specific problems of the paper. |"""

VALID_ERROR_TYPES = {
    "Misunderstanding", "Neglect", "Vague Critique", "Out-of-scope",
    "Invalid Criticism", "Superficial Review", "Unstated statement",
    "Excessive demands", "Generic comment", "",
}


class Weakness(BaseModel):
    weakness: str
    reliable: int
    error_type: str
    justification: str


class WeaknessList(BaseModel):
    items: list[Weakness]


def progress(event, **fields):
    print(json.dumps({"event": event, **fields}, ensure_ascii=False), file=sys.stderr, flush=True)


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


def run_item(client, guideline, method, paper_id, review_text, paper_text):
    progress("sample_start", method=method, paper_id=paper_id)
    user_content = f"""Weakness reliability guideline (error type table + human-annotated examples):
{guideline}

Paper id: {paper_id}

=== PAPER TEXT ===
{paper_text}
=== END PAPER TEXT ===

=== REVIEW TO EVALUATE ===
{review_text}
=== END REVIEW ===

Task:
Extract every weakness claim that the review makes about the paper, then judge whether each weakness is reliable BY CHECKING IT AGAINST THE PAPER TEXT ABOVE.

Ignore any item that is explicitly labeled as "Nice-to-Have" / "Nice-to-Haves" (e.g. items under a Nice-to-Have section or explicitly marked as nice-to-have) — do not extract those as weakness items. Only apply this to items explicitly said to be nice-to-have; do NOT infer or reclassify weakness items as nice-to-have.

For each weakness, return:
- weakness: one specific weakness, flaw, limitation, or criticism of the paper that appears in the review.
- reliable: 1 if this weakness is genuinely supported by the paper (the flaw really exists, the omission is real, the critique is well-grounded). 0 if it matches one of the error patterns in the guideline (Misunderstanding/Neglect/etc. -- e.g., the reviewer overlooked something explicitly in the paper, misread a claim, asked for something out-of-scope, or made a vague/generic/excessive criticism).
- error_type: if reliable=0, choose the single best-matching label from {sorted(t for t in VALID_ERROR_TYPES if t)}. If reliable=1, use an empty string.
- justification: 1-2 sentences. If reliable=0, cite the specific paper passage that contradicts the weakness or explain why it is vague/excessive/generic. If reliable=1, point to the gap in the paper that supports the weakness.

Be strict. The paper is available to you -- if the reviewer's claim contradicts something explicitly in the paper, mark it Neglect/Misunderstanding. If you cannot find supporting evidence in the paper for what the reviewer claims is missing, double-check the paper before marking reliable=1.
"""
    completion = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"""You are an expert NLP/ML conference meta-reviewer. You will be given a paper and a review of that paper. Your job is to extract each weakness claim in the review and judge whether it is reliable, USING THE PAPER TEXT as ground truth.

Error type table:
{ERROR_TYPE_TABLE}"""},
            {"role": "user", "content": user_content},
        ],
        temperature=TEMPERATURE,
        response_format=WeaknessList,
        extra_body={"reasoning": {"effort": "none", "exclude": True}},
    )
    parsed = completion.choices[0].message.parsed
    if parsed is None:
        raise ValueError(f"No parsed response for {method}/{paper_id}")
    rows = []
    for w in parsed.items:
        et = w.error_type.strip()
        if et not in VALID_ERROR_TYPES:
            raise ValueError(f"Invalid error_type {et!r} for {method}/{paper_id}")
        rows.append({
            "method": method,
            "paper_id": paper_id,
            "weakness": w.weakness,
            "reliable": w.reliable,
            "error_type": et,
            "justification": w.justification,
            "status": "ok",
        })
    progress("sample_done", method=method, paper_id=paper_id, weaknesses=len(rows))
    return rows


load_dotenv(REPO_ROOT / ".env")
api_key = os.environ["OPENROUTER_API_KEY"]
guideline = GUIDELINE_PATH.read_text(encoding="utf-8").strip()

method_papers = {m: list_papers(m) for m in METHODS}
for m, s in method_papers.items():
    print(f"{m}: {len(s)} papers", file=sys.stderr)
paper_ids = {p.stem for p in PAPER_DIR.glob("*.txt")}
common = set.intersection(*method_papers.values()) & paper_ids
print(f"common across all methods + paper text: {len(common)}", file=sys.stderr)
common_sorted = sorted(common)
if SAMPLE_SIZE is None:
    sampled = common_sorted
else:
    if len(common_sorted) < SAMPLE_SIZE:
        raise RuntimeError(f"Only {len(common_sorted)} papers, need {SAMPLE_SIZE}")
    rng = random.Random(SEED)
    sampled = rng.sample(common_sorted, SAMPLE_SIZE)
print(f"sampled: {len(sampled)}", file=sys.stderr)
SAMPLED_IDS_PATH.parent.mkdir(parents=True, exist_ok=True)
SAMPLED_IDS_PATH.write_text(json.dumps(sorted(sampled), indent=2))

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
done_keys = set()
if OUTPUT_PATH.exists():
    with OUTPUT_PATH.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if row["status"] == "ok":
                done_keys.add((row["method"], str(row["paper_id"])))

tasks = []
for method in METHODS:
    for pid in sampled:
        if (method, pid) in done_keys:
            continue
        tasks.append((method, pid))

progress("batch_start", total_tasks=len(METHODS) * len(sampled), pending=len(tasks), done=len(done_keys))

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={"X-Title": "final_results weakness reliability evaluation glm-5.2"},
)

with OUTPUT_PATH.open("a", encoding="utf-8") as out:
    with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL) as executor:
        futures = {}
        for method, pid in tasks:
            item_rng = random.Random(f"{SEED}-{method}-{pid}")
            review_text = load_review(method, pid, item_rng)
            paper_path = PAPER_DIR / f"{pid}.txt"
            paper_text = paper_path.read_text(encoding="utf-8").strip()
            if review_text is None:
                progress("sample_failed", method=method, paper_id=pid, error="missing review")
                continue
            futures[executor.submit(run_item, client, guideline, method, pid, review_text.strip(), paper_text)] = (method, pid)
        for future in concurrent.futures.as_completed(futures):
            method, pid = futures[future]
            try:
                rows = future.result()
            except Exception as e:
                progress("sample_failed", method=method, paper_id=pid, error=repr(e))
                continue
            for row in rows:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()

progress("batch_done", output=str(OUTPUT_PATH))

by_method = {}
with OUTPUT_PATH.open(encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        by_method.setdefault(row["method"], []).append(row)
print("\n=== reliability rate (fraction of weakness claims marked reliable=1) ===", file=sys.stderr)
for m in METHODS:
    rows = by_method.get(m, [])
    if rows:
        rate = sum(r["reliable"] for r in rows) / len(rows)
        print(f"  {m}: reliable_rate={rate:.3f} n_weaknesses={len(rows)}", file=sys.stderr)
    else:
        print(f"  {m}: no data", file=sys.stderr)
