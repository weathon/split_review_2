"""Build the weakness/strength scoring training set from DeepReview-13K.

Items are split by an LLM (openai/gpt-oss-120b via OpenRouter, cerebras/fp16)
instead of a regex: each item is one atomic reviewer point; lead-ins, pure
citation lists, duplicates and section headers are discarded.

Resampling first (needs only ratings), then split only the kept papers.
Per-paper split results are cached to datasets/oss_split_cache/<id>.json so the
run is resumable and the expensive LLM calls are never repeated.

Output:
  datasets/weakness_score_train.jsonl   (integer-bin resample, cap 400/bin)
  datasets/weakness_score_val.jsonl     (5% split, natural distribution)
"""

import json
import os
import random
from concurrent.futures import ThreadPoolExecutor

import dotenv
import tqdm

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from datasets import load_dataset
from openai import OpenAI

from paths import DATASETS_DIR

TRAIN_OUT = DATASETS_DIR / "weakness_score_train.jsonl"
VAL_OUT = DATASETS_DIR / "weakness_score_val.jsonl"
CACHE_DIR = DATASETS_DIR / "oss_split_cache"

SPLIT_MODEL = "openai/gpt-oss-120b"
MAX_RETRIES = 4
CONCURRENCY = 16

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])

SPLIT_PROMPT = """You are given the Strengths and Weaknesses that MULTIPLE reviewers wrote for one paper. Reformat them into two flat lists of atomic items.

Rules:
- Each item is ONE distinct point a reviewer made (usually one bullet or numbered entry). Keep a multi-sentence point together as a single item; do NOT split one point into separate sentences.
- If one block actually contains several separate enumerated points, split them into separate items.
- DISCARD anything that is not itself a substantive strength/weakness: lead-in sentences ("The following are the weaknesses:", "See questions."), pure reference/citation list lines (e.g. "[1] Foo et al. 2023..."), duplicated sentences, standalone section headers, pure typo-only enumerations.
- Preserve the reviewer's original wording, INCLUDING inline citation markers like [1].
- Do not invent content. Merge points from different reviewers into the same list but keep them as separate items.

Return ONLY a JSON object: {"strengths": ["...", ...], "weaknesses": ["...", ...]}.

Reviews:
"""


def format_reviews(reviewer_comments: list[dict]) -> str:
    parts = []
    for i, rc in enumerate(reviewer_comments, 1):
        content = rc["content"]
        block = [f"## Reviewer {i}"]
        for field, header in (("strengths", "### Strengths"), ("weaknesses", "### Weaknesses")):
            text = content[field]
            if text:
                block.append(f"{header}\n{text}")
        if len(block) > 1:
            parts.append("\n".join(block))
    return "\n\n".join(parts)


def llm_split(paper_id: str, reviews_text: str) -> dict:
    cache_path = CACHE_DIR / f"{paper_id}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.chat.completions.create(
                model=SPLIT_MODEL,
                messages=[{"role": "user", "content": SPLIT_PROMPT + reviews_text}],
                response_format={"type": "json_object"},
                extra_body={"provider": {"only": ["cerebras"], "quantizations": ["fp16"]}},
            )
            out = json.loads(resp.choices[0].message.content)
            result = {"strengths": list(out["strengths"]), "weaknesses": list(out["weaknesses"])}
            cache_path.write_text(json.dumps(result))
            return result
        except Exception as e:  # transient API error or malformed JSON -> retry
            last_err = e
            print(f"  [split] {paper_id} attempt {attempt}/{MAX_RETRIES} failed: {e}")
    print(f"  [split] SKIP {paper_id}: {last_err}")
    return None


def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ds = load_dataset("WestlakeNLP/DeepReview-13K", token=os.environ["HF_TOKEN"])["train"]

    papers = []
    seen = set()
    skipped_bad_scores = 0
    skipped_empty = 0
    for ex in tqdm.tqdm(ds, desc="collect"):
        pid = ex["id"]
        if pid in seen:  # each paper appears 3x (mode fast/standard/best)
            continue
        seen.add(pid)

        raw = ex["rating"]
        try:
            if isinstance(raw, str):
                raw = json.loads(raw)
            scores = [int(s.split(":", 1)[0].strip()) if isinstance(s, str) else int(s)
                      for s in raw]
        except (ValueError, TypeError):
            print(f"skip {pid}: unparseable rating {ex['rating']!r}")
            skipped_bad_scores += 1
            continue
        if not scores:
            print(f"skip {pid}: empty rating list")
            skipped_bad_scores += 1
            continue

        reviewer_comments = json.loads(ex["reviewer_comments"])
        reviews_text = format_reviews(reviewer_comments)
        if not reviews_text.strip():  # no strengths/weaknesses at all
            skipped_empty += 1
            continue

        papers.append({"paper_id": pid, "gt": sum(scores) / len(scores),
                       "reviews_text": reviews_text})

    # resample on gt alone (independent of splitting)
    rng = random.Random(0)
    rng.shuffle(papers)
    n_val = round(len(papers) * 0.05)
    val_papers, train_pool = papers[:n_val], papers[n_val:]

    bins = {}
    for p in train_pool:
        bins.setdefault(round(p["gt"]), []).append(p)
    train_papers = []
    for b in sorted(bins):
        train_papers.extend(bins[b][:400])
    rng.shuffle(train_papers)
    print("train bin counts after cap:",
          {b: min(len(v), 400) for b, v in sorted(bins.items())})

    selected = val_papers + train_papers
    print(f"splitting {len(selected)} papers with {SPLIT_MODEL} ...")
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex_pool:
        list(tqdm.tqdm(ex_pool.map(lambda p: llm_split(p["paper_id"], p["reviews_text"]), selected),
                       total=len(selected), desc="split"))

    def assemble(paper):
        split = llm_split(paper["paper_id"], paper["reviews_text"])  # cache hit
        if split is None:
            return None
        items = [f"strength: {s}" for s in split["strengths"] if s.strip()] \
            + [f"weakness: {w}" for w in split["weaknesses"] if w.strip()]
        if not items:
            return None
        return {"paper_id": paper["paper_id"], "items": items, "gt": paper["gt"]}

    train = [a for a in map(assemble, train_papers) if a is not None]
    val = [a for a in map(assemble, val_papers) if a is not None]

    with open(TRAIN_OUT, "w") as f:
        for s in train:
            f.write(json.dumps(s) + "\n")
    with open(VAL_OUT, "w") as f:
        for s in val:
            f.write(json.dumps(s) + "\n")

    n_items = [len(s["items"]) for s in train + val]
    print(f"papers written: train {len(train)}, val {len(val)}")
    print(f"skipped: bad_scores={skipped_bad_scores}, empty_fields={skipped_empty}")
    print(f"items/paper: min={min(n_items)} mean={sum(n_items)/len(n_items):.2f} max={max(n_items)}")


if __name__ == "__main__":
    main()
