# Split Review

Multi-agent paper reviewer with calibration retrieval against the DeepReview-13K human-review corpus.

## Architecture

The pipeline turns a paper (PDF or extracted markdown/text) into a single
consolidated review with a numeric score and an Accept/Reject decision. The
core is a two-phase, three-agent design implemented in
[code/main.py](code/main.py) (`run_pipeline`).

### Phase 1 — split review (two reviewers, in parallel)

Two reviewers run concurrently (`asyncio.gather`) on the same paper, each with a
deliberately one-sided mandate:

- **Harsh Critic** ([prompts/harsh_critic.md](prompts/harsh_critic.md)) — sweeps
  for weaknesses across method soundness, evaluation validity, comparison
  fairness, evidence strength, etc.
- **Strength Finder** ([prompts/neutral_reviewer.md](prompts/neutral_reviewer.md))
  — surfaces genuine strengths and contributions.

Both read the paper **from disk in chunks** rather than receiving it inline:
each is an `agents.Agent` (OpenAI Agent SDK) given the `read_file` and
`grep_file` tools and a path to the paper, and is instructed to read
section-by-section, reasoning through each chunk before the next
(`PAPER_ACCESS_CHUNKED` in [code/main.py](code/main.py)).

### Phase 2 — merger / meta-reviewer (synthesis + calibration)

The **Merger** ([prompts/merger.md](prompts/merger.md)) receives both Phase-1
outputs and the paper path. Its job is *compression, not union*: it
aggressively filters the harsh critic's noise (every retained weakness must
anchor to a specific sentence/figure/table; speculative or
existence-questioning criticisms are removed) and synthesizes one authoritative
review.

It then **calibrates** the score against the human-review corpus via the
`calibration_search` tool — an iterative RAG protocol
([prompts/cal_with.md](prompts/cal_with.md)): record a draft (`draft_review`),
do a wide *bracketing* pass to find the plausible score band, then one or two
*narrowing* passes (vector search over human reviews, filtered by their average
human score range) to anchor the final score against comparable papers. With
`--no_cal`, this step is skipped ([prompts/cal_without.md](prompts/cal_without.md)).

The merger emits the final review with `<score>` and `<decision>` tags. If
parsing those tags fails, a small DeepSeek call extracts them as a fallback.

### Calibration retrieval

The retrieval tools live in [code/tools.py](code/tools.py). At import time the
selected corpus (default `deepreview`, the DeepReview-13K human reviews) is
loaded and a BM25 index is built. `search_file` / `_search_file_impl` support
two ranking modes — `vector` (Google `gemini-embedding-001` embeddings via
OpenRouter, dot-product against a precomputed embedding matrix) and `bm25` — and
**filter by avg-human-score band first**, then rank. A per-file score index
(`_score_index`) maps each review to its average human score, which is what
makes "find me anchors in the 6–8 band" possible. In benchmark mode, the papers
being scored are excluded from their own calibration pool
(`set_excluded_paper_ids`).

All agent file access goes through a **path allowlist** (`ALLOWED_PATHS`): the
tools refuse to read anything outside the calibration dir and the current
paper's directory (granted per-run via `allow_path`), and the agents are told
not to explore the filesystem.

### Model backends

Each role's model is set independently via env var (`HARSH_MODEL`,
`NEUTRAL_MODEL`, `MERGER_MODEL`, `SUBAGENT_MODEL`). `resolve_model` dispatches by
prefix: bare name → OpenRouter (responses API), `ollama:` → local Ollama,
`featherless:` → Featherless. A `claude_sdk:` prefix on `HARSH_MODEL` /
`MERGER_MODEL` routes that role through the **Claude Agent SDK**
([code/claude_merger.py](code/claude_merger.py)), where the same
read_file/grep_file/calibration_search tools are re-exposed as an in-process MCP
server and the built-in Read/Bash/Write tools are disabled. OpenRouter per-call
cost is tracked via a wrapper installed on the chat-completions client.

### Entry points & data flow

```
                 paper.pdf ──(datalab)──> paper.md/.txt
                                  │
                   ┌──────────────┴──────────────┐
        Phase 1    Harsh Critic            Strength Finder      (parallel, chunked read)
                   └──────────────┬──────────────┘
                                  ▼
        Phase 2              Merger / AC ──► calibration_search ──► human-review corpus
                                  │            (bracket → narrow, score-band filtered)
                                  ▼
                   <score> + <decision> + final review.md
```

- `python code/main.py --single_paper <path>` — one paper (PDFs are converted to
  markdown via the Datalab SDK first); writes a review under `code/reviews/`.
- `python code/main.py --benchmark <data_dir>` — run over a labeled dataset
  (`ratings.csv` + `papers/`), with random or `--balanced` stratified sampling,
  resumable CSV output, and MAE against ground-truth scores.

### Related scripts

[code/baseline.py](code/baseline.py) / [code/baseline_claude.py](code/baseline_claude.py)
are single-agent baselines (one direct review call, no split/merge).
[code/pairwise_score.py](code/pairwise_score.py) scores via pairwise comparison
against score-banded anchors (Bradley–Terry).
[code/rebuttal.py](code/rebuttal.py) generates author rebuttals.
[code/metric.py](code/metric.py) holds the correlation/MAE/AUROC statistics.
The `code/build_*.py` scripts regenerate the calibration corpus and embeddings.

## Layout

```
code/        Python implementation (main.py, tools.py, claude_merger.py, ...)
prompts/     Agent system prompts (markdown)
datasets/    DeepReview-13K calibration + test splits.
             The embeddings/score-index pickles are NOT in git — they are
             auto-downloaded on first use from
             https://huggingface.co/datasets/weathon/paper_embeddings
results/     Benchmark CSVs and scatter plots from prior runs
scripts/     Convenience launchers
```

Path resolution lives in [code/paths.py](code/paths.py). All defaults assume the
layout above; override with `REVIEW_REPO_ROOT`, `REVIEW_PROMPTS_DIR`,
`REVIEW_DATASETS_DIR`, `REVIEW_RESULTS_DIR`.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # then fill in keys
```

The two embedding pickles are downloaded automatically from the HuggingFace
dataset repo `weathon/paper_embeddings` on first run (cached in `datasets/`).
Override with `REVIEW_HF_REPO` if you fork/mirror them.

Required env vars (in `.env`):

- `OPENROUTER_API_KEY` — calibration embeddings & default model traffic
- `OPENAI_API_KEY` — Weave tracing
- `ANTHROPIC_API_KEY` — only if `MERGER_MODEL=claude_sdk:...`

## Run

```bash
./scripts/run_deepreview.sh
```

Or directly:

```bash
python code/main.py \
  --benchmark datasets/deepreview_13k_test/ \
  --n_samples 200 \
  --seed 42
```

Outputs land in `results/` (CSV + per-paper review markdown under
`results/bench_reviews/`).

## Building the calibration artifacts from scratch

The pickles in `datasets/` are prebuilt. To regenerate them from the public
HuggingFace `deepreview/DeepReview-13K` dataset:

```bash
python code/build_deepreview.py
```

## Results

### 3-way comparison: baseline vs ours vs no-cal ablation (deepseek-v4-flash, 300 papers)

Three runs on the ICLR-2026 set, scored `pred_score` vs `gt_avg_score`:
- **baseline** (`cmp3_baseline`) — single-call reviewer (`code/baseline.py`).
- **ours** (`cmp3_ours`) — split-agent pipeline + deepreview calibration retrieval.
- **no-cal** (`cmp3_nocal`) — ours with calibration disabled (`--no_cal`) ablation.

Pearson r on the common overlap (n = 292 papers scored by all three; `pred_score == -100`
"no score found" sentinels excluded — this dropped 1 row from `ours`):

| run | Pearson r |
|---|---|
| baseline | 0.5074 |
| ours | 0.6359 |
| no-cal | 0.5397 |

Dependent (Steiger) test for the three overlapping, gt-sharing correlations — t / p, df = 289:

| | baseline | ours | no-cal |
|---|---|---|---|
| baseline | — | −3.71 / 0.000 | −0.79 / 0.430 |
| ours | +3.71 / 0.000 | — | +2.96 / 0.003 |
| no-cal | +0.79 / 0.430 | −2.96 / 0.003 | — |

pred-pred correlations: r(baseline,ours)=0.7091, r(baseline,no-cal)=0.6425, r(ours,no-cal)=0.7410.
Ours beats both the single-call baseline (p≈0.0002) and its own no-cal ablation (p≈0.003);
baseline vs no-cal is not significant (p≈0.43).

### Follow-up analysis (from existing results/snapshots, no new runs)

All correlations below are pred_score vs gt_avg_score with the `pred_score == -100`
"no score found" sentinel (`code/main.py:388`, `code/baseline.py`) excluded.

**1. How does `ours` compare to before?**
`cmp3_ours` (deepseek-v4-flash split-agent pipeline + deepreview calibration — the
`run_deepreview.sh` config, whose default sweep name is `2026_deepseek_flash_guideline_single`)
lands at Pearson r ≈ 0.64 on n ≈ 295. The earlier run of the *same* config,
`2026_deepseek_flash_guideline_single`, was r = 0.673 (n = 100), and
`2026_deepseek_flash_guideline` was r = 0.666 (n = 100). So `ours` is essentially
unchanged — marginally lower, well within run-to-run noise — but now measured on
~3× the sample.

**2. The "very good" vs "very bad" baseline.**
Good baseline: `2026_baseline_claude` (claude-sonnet-4-6 single-call), r = 0.684 (n = 393).
The "very bad" baseline was a **sentinel artifact**, not a real collapse:
- `mimo_baseline`: r = −0.010 (n = 393) with 10 `-100` sentinels → r = 0.659 (n = 383) clean.
- `deepreview_baseline`: r = 0.203 (n = 298, 2 sentinels) → r = 0.578 (n = 296) clean.

So the "very bad" number you remember (~0) was `mimo_baseline` being dragged to zero by
ten unparsed-score rows; cleaned, it is ~0.66.

**3. Did we test baseline + guideline?**
Not as a separate arm. The ICLR official guideline is **already embedded in the
single-call baseline prompt** (`code/baseline.py`, "ICLR Offical Guideline for reference"),
together with a global 2026 score-distribution hint. Every `*guideline*` result directory
(`2026_deepseek_flash_guideline`, `..._single`, `2026_mimo_pro_response_guideline`) is the
**multi-agent (ours) pipeline**, not the baseline. What the baseline never got is the
per-paper *calibration-retrieval* (anchor RAG) that `ours` runs — that arm was not tested.

**4. The old pairs where `ours` barely beat baseline** (matched overlap, clean):
| ours | baseline | n | ours r | baseline r | gap |
|---|---|---|---|---|---|
| 2026_sonnet_repro (sonnet agent) | 2026_baseline_claude (sonnet single) | 393 | 0.7065 | 0.6843 | +0.022 |
| 2026_mimo_pro_response_guideline | mimo_baseline | 344 | 0.6570 | 0.6518 | +0.005 |
| 2026_deepseek_flash_guideline_single | deepreview_baseline | 99 | 0.6539 | 0.5798 | +0.074 |

The sonnet and mimo pairs are the near-ties (+0.02 and +0.005) — the likely reason the
project was set aside. Note the current cmp3 gap (ours ≈ 0.64 vs baseline ≈ 0.52,
Steiger p ≈ 0.001) is large only because `cmp3_baseline` is the *weak* deepseek-flash
single-call baseline; against the *strong* claude baseline (0.68) `ours` has never
opened a clear margin.

## Notes

- `*.pkl` files are tracked via Git LFS (see `.gitattributes`).
- The repo is configured for the DeepReview calibration set only. Older
  ICLR-2025/2026 and NeurIPS position-paper code paths were trimmed.
- **Naming caveat:** `2026_deepseek_flash_guideline_single` (and the other
  `*_guideline*` dirs) is **ours** — the multi-agent split pipeline + calibration
  retrieval (`run_deepreview.sh`, `code/main.py`), *not* a baseline. It is the
  default `SWEEP_NAME` of `run_deepreview.sh`; "guideline" refers to the
  calibration protocol, not a single-call baseline. The single-call baselines are
  the `*_baseline` dirs (`code/baseline.py`). Its high r (0.673, n=100) is a
  small-subset effect: on the same 99 papers `cmp3_ours` scores 0.684, and the
  full-set number is ~0.64.



## TODO
Embedding Emotion Analysis, Embedding Regression, LoRA finetune