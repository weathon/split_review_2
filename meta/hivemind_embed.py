import argparse
import json
import os
import random
import re
import pickle

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np

import dotenv
from openai import OpenAI
from pydantic import BaseModel
from tqdm import tqdm


class WeaknessItem(BaseModel):
    text: str
    match_in_review2: str | None


class OverlapResult(BaseModel):
    review1_weakness_items: list[WeaknessItem]


dotenv.load_dotenv(Path(__file__).parent.parent / ".env")

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

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

PARSE_MODEL = "deepseek/deepseek-v4-flash"
MAX_RETRIES = 5
RETRY_DELAY = 5

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


def load_review(method_name, pid):
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
        return reviews[0]["text"]

class ParseResponse(BaseModel):
    items: list[str]

PARSE_RESPONSE_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "ParseResponse",
        "strict": True,
        "schema": {**ParseResponse.model_json_schema(), "additionalProperties": False},
    },
}


def prep_review(review_text):
    for i in range(MAX_RETRIES):
        try:
            completion = client.chat.completions.create(
                model=PARSE_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You need to break down the given review into a list of strength and weaknesses items. Do not rephase anything but just break them down.",
                    },
                    {
                        "role": "user",
                        "content": review_text,
                    },
                ],
                response_format=PARSE_RESPONSE_JSON_SCHEMA,
                extra_body={"reasoning": {"enabled": False}, "provider": {"only": ["gmicloud/fp8"]}},
            )

            reviews = ParseResponse(**json.loads(completion.choices[0].message.content)).items

            embedding = client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=list(reviews),
                encoding_format="float"
            ) 
            return np.array([embedding.data[i].embedding for i in range(len(embedding.data))], dtype=np.float32)

        except Exception as e:
            print(f"Error in prep_review: {e}. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY//2)
    raise RuntimeError(f"Failed to process review after {MAX_RETRIES} attempts.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--concurrency", type=int, default=30)
    ap.add_argument("--out", type=str, default=str(OUT_DIR / "overlap_results.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)

    method_papers = {m: list_papers(m) for m in METHODS}
    for m, s in method_papers.items():
        print(f"{m}: {len(s)} papers")
    common = set.intersection(*method_papers.values())
    print(f"common across all methods: {len(common)}")
    common_sorted = sorted(common)

    print(common_sorted)


    def run_one(method, review_id):
        r1 = load_review(method, review_id)
        if r1 == "" or r1 is None:
            raise ValueError(f"Empty review for {method} {review_id}")
        embeddings = prep_review(r1)
        return embeddings, method
    


    embeddings = {}
    if (Path(OUT_DIR / "checkpoint.pkl").exists()):
        with open(OUT_DIR / "checkpoint.pkl", "rb") as f:
            try:
                embeddings = pickle.load(f)
                print(f"Loaded checkpoint with {len(embeddings)} methods.")
            except Exception as e:
                print(f"Failed to load checkpoint: {e}. Starting fresh.")
                embeddings = {}

    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = []
        for review_id in common_sorted:
            for method in METHODS:
                futures.append(ex.submit(run_one, method, review_id))
        for f in tqdm(futures):
            e, method = f.result()
            old = embeddings.get(method, [])
            old.append(e)
            embeddings[method] = old
            if len(old) % 20 == 0:
                with open(OUT_DIR / "checkpoint.pkl", "wb") as f:
                    pickle.dump(embeddings, f)

    # print(embeddings)
    sims = {m: [] for m in METHODS}
    for method in METHODS:
        for a in range(len(embeddings[method])):
            for b in range(len(embeddings[method])):
                set_a = embeddings[method][a]
                set_b = embeddings[method][b]
                set_a = set_a / np.linalg.norm(set_a, axis=1, keepdims=True)
                set_b = set_b / np.linalg.norm(set_b, axis=1, keepdims=True)
                sim_matrix = set_a @ set_b.T
                diag = np.diagonal(sim_matrix) 

                # sim = np.mean(sim_matrix)
                sim = np.mean(np.max(sim_matrix, axis=1))
                sims[method].append(sim)

    with open(OUT_DIR / "overlap_results.pkl", "wb") as f:
        pickle.dump(sims, f)
    print({m:np.mean(sims[m]) for m in METHODS})

if __name__ == "__main__":
    main()
