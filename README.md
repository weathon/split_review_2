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

### 4-way comparison: baseline vs ours vs no-cal vs deepseek baseline (deepseek-v4-flash, full 393)

Four runs on the full ICLR-2026 set (393 papers), scored `pred_score` vs `gt_avg_score`:
- **baseline** (`cmp3_baseline`) — single-call reviewer (`code/baseline.py`).
- **ours** (`cmp3_ours`) — split-agent pipeline + deepreview calibration retrieval.
- **no-cal** (`cmp3_nocal`) — ours with calibration disabled (`--no_cal`) ablation.
- **good_base** (`deepreview_baseline`) — earlier same-config deepseek-flash single-call baseline.

Pearson r on the common overlap (n = 389 papers scored by all four; `pred_score == -100`
"no score found" sentinels excluded — this dropped 1 row from `ours`):

| run | Pearson r |
|---|---|
| baseline | 0.5015 |
| ours | 0.6313 |
| no-cal | 0.5548 |
| good_base | 0.5440 |

Dependent (Steiger) test for the four overlapping, gt-sharing correlations — t / p, df = 386:

| | baseline | ours | no-cal | good_base |
|---|---|---|---|---|
| baseline | — | −4.09 / 0.000 | −1.47 / 0.142 | −1.12 / 0.262 |
| ours | +4.09 / 0.000 | — | +2.63 / 0.009 | +2.71 / 0.007 |
| no-cal | +1.47 / 0.142 | −2.63 / 0.009 | — | +0.30 / 0.767 |
| good_base | +1.12 / 0.262 | −2.71 / 0.007 | −0.30 / 0.767 | — |

pred-pred: r(baseline,ours)=0.6773, r(baseline,no-cal)=0.6203, r(baseline,good_base)=0.5862,
r(ours,no-cal)=0.7217, r(ours,good_base)=0.6588, r(no-cal,good_base)=0.6030.
Ours beats all three others significantly (vs baseline p≈0.00005, vs no-cal p≈0.009, vs
good_base p≈0.007). baseline, no-cal, and good_base are mutually indistinguishable (all p > 0.14).

**cmp3_baseline vs deepreview_baseline (both deepseek-flash single-call, full 393).**
Same code/prompt/model — matched n = 390: `cmp3_baseline` r = 0.5017 vs `deepreview_baseline`
r = 0.5439, Steiger t = −1.11, p = 0.266 (pred-pred r = 0.585). The two same-config baseline
draws differ only by run-to-run stochasticity (not significant).

### Pooled 3-draw comparison with cluster bootstrap (headline result)

Every arm was run 3 times end-to-end (baseline: `cmp3_baseline` / `deepreview_baseline` /
`cmp3_baseline_v2`; ours: `cmp3_ours` / `_v2` / `_v3`; no-cal: `cmp3_nocal` / `_v2` / `_v3`).
The 3 draws per arm are pooled as datapoints (376 common papers × 3 draws = 1128 points per
arm; `pred_score == -100` sentinels excluded), so no arm's number depends on a lucky draw:

| arm | pooled Pearson | pooled Spearman |
|---|---|---|
| baseline | 0.5216 | 0.4851 |
| no-cal | 0.5592 | 0.5097 |
| ours | 0.6154 | 0.5539 |

Significance via **paper-level cluster bootstrap** (10,000 resamples; papers resampled with
replacement, each carrying all 3 draws of every arm — this preserves within-paper dependence
so no effective-n/df assumption is needed):

| comparison | Δr | 95% CI | bootstrap p |
|---|---|---|---|
| ours − baseline | +0.0938 | [+0.049, +0.140] | 0.0002 |
| ours − no-cal | +0.0563 | [+0.022, +0.093] | 0.0002 |
| no-cal − baseline | +0.0376 | [−0.012, +0.087] | 0.142 |

Ours beats both the single-call baseline and its own no-calibration ablation; no-cal does not
significantly beat the baseline. The split-agent structure alone does not explain the gain —
the calibration retrieval carries it. (For reference, dependent Steiger tests on the pooled
vectors give ours-vs-baseline p = 0.0048 even at the worst-case df of n = 376 papers.)

### Reporting rule for cross-method comparisons: median draw

Pooling requires every compared method to also be run 3×, which is not practical for external
comparison methods. So for headline tables that compare against other methods (each run once),
report the **median-Pearson draw** of each of our arms, not the pooled value and not the best
draw. On the 376 common papers the median draws are:

| arm | median draw | Pearson | Spearman |
|---|---|---|---|
| baseline | `cmp3_baseline_v2` | 0.5230 | 0.4787 |
| no-cal | `cmp3_nocal_v3` | 0.5578 | 0.5085 |
| ours | `cmp3_ours_v2` | 0.6138 | 0.5498 |

(Per-arm draw ranges: baseline 0.500–0.546, no-cal 0.550–0.570, ours 0.597–0.635 — every ours
draw beats every baseline draw. The pooled + bootstrap section above remains the significance
analysis; the median draw is only the single-run reporting metric.)

### Inter-run variance (3 draws per arm, same 376 papers)

- run-level r-vs-gt std: baseline 0.023, ours 0.019, no-cal 0.010.
- prediction stability between draws: pred-pred r baseline ≈ 0.61, no-cal ≈ 0.70, ours ≈ 0.79;
  per-paper score std across draws: baseline 0.89 pts (P90 1.73), no-cal 0.61, ours 0.45 (P90 0.76).

The pipeline is not only better-correlated with gt but roughly 2× more reproducible per paper
than the single-call baseline; calibration retrieval stabilizes scoring, not just improves it.

### External baselines (`~/split_review_ablation/baselines/`), same 393-paper set

Three external tools were confirmed to score the identical 393-paper ICLR-2026 set (`cspaper`:
393 papers, one stray `submissions.json`; `DeepReviewer_14B`: 393; `DeepReviewer-v2-openai`:
393, 1 failed job skipped). Our three median-draw runs were completed to 393/393 (3 papers per
run were never sampled due to duplicate rows in `ratings.csv` shifting the seeded sample; they
were filled by running the identical pipeline on exactly those papers). All methods below are
evaluated on the single shared subset scored by every method — n = 392 of 393 (the one
DeepReviewer-v2 failed job is the only gap):

| method | n | Pearson | Spearman |
|---|---|---|---|
| cspaper | 392 | 0.7592 | 0.7757 |
| ours (median draw) | 392 | 0.6154 | 0.5525 |
| no-cal (median) | 392 | 0.5602 | 0.5101 |
| DeepReviewer-v2-openai | 392 | 0.5539 | 0.5148 |
| DeepReviewer_14B | 392 | 0.5284 | 0.4548 |
| baseline (median) | 392 | 0.5212 | 0.4734 |

**Paired bootstrap: ours vs each non-leaked method** (papers resampled jointly, 10,000
resamples, shared n = 392; single draw per method — cspaper excluded due to the leakage
caveat below):

| ours vs | metric | Δ | 95% CI | boot p |
|---|---|---|---|---|
| baseline (median) | Pearson | +0.0942 | [+0.028, +0.160] | **0.0044** |
| | Spearman | +0.0791 | [−0.002, +0.158] | 0.0554 |
| DeepReviewer_14B | Pearson | +0.0870 | [+0.002, +0.174] | **0.0446** |
| | Spearman | +0.0977 | [+0.006, +0.189] | **0.0378** |
| DeepReviewer-v2-openai | Pearson | +0.0614 | [−0.003, +0.130] | 0.0618 |
| | Spearman | +0.0377 | [−0.038, +0.116] | 0.3194 |
| no-cal (median) | Pearson | +0.0552 | [−0.003, +0.117] | 0.0652 |
| | Spearman | +0.0424 | [−0.026, +0.111] | 0.2286 |

Ours significantly beats the single-call baseline on Pearson (p = 0.004; Spearman marginal at
0.055) and DeepReviewer_14B on both metrics; vs DeepReviewer-v2-openai and no-cal the edge is
consistent but marginal on Pearson (~0.06) and not significant on Spearman. These are
single-draw-vs-single-draw tests; for baseline and no-cal the pooled 3-draw cluster bootstrap
above (p = 0.0002 both) is the stronger evidence — the external methods only have one draw.

**cspaper coverage note.** cspaper's pre-review gate desk-rejects some papers with no numeric
score (`main_score_norm: N/A`). Initially 24/393 were desk-rejected; suspecting an over-desk-reject
bug, the same 24 PDFs were resubmitted to the CSPaper platform API. 14/24 came back with a real
score on rerun (confirming the bug — same paper, same gate, opposite outcome); the remaining
9 were rerun with `desk_rejection_enabled=false` (documented API flag) and all returned scores
(0.0–0.4, i.e. genuinely weak papers). Final coverage: **393/393 scored** (up from 369).

**⚠️ cspaper's number above is likely invalid — probable decision leakage.** cspaper's
`main_score_norm` sits almost perfectly on the correct side of the accept/reject boundary (0.5),
far beyond what score-only reasoning would produce:

| | n | accuracy of `(score > threshold)` vs `gt_binary` |
|---|---|---|
| **cspaper** (`main_score_norm > 0.5`) | 390 | **92.3%** (accepted papers scored >0.5 in 88.7% of cases; rejected papers scored <0.5 in 94.8%) |
| ours (`cmp3_ours_v2`, `pred_score > 5`) | 387 | 64.6% |
| baseline (`cmp3_baseline_v2`, `pred_score > 5`) | 390 | 60.0% |
| deepreview_baseline (`pred_score > 5`) | 390 | 59.2% |

The strongest evidence: cspaper's score predicts the final decision **better than the human
reviewers' own average score does** (all on n = 390, each metric at its own optimal threshold):

| | AUROC vs decision | accuracy at fixed cutoff | max accuracy (optimal threshold) |
|---|---|---|---|
| cspaper `main_score_norm` | 0.9279 | 92.3% (> 0.5) | **92.3%** (> 0.4) |
| human average score | 0.9310 | 84.9% (> 5) | **85.9%** (> 4.8) |

The human panel's average score misses ~14% of decisions (borderline papers where the
meta-review overrode the scores); cspaper lands on the correct decision side in most of those
too. A model scoring purely from paper content cannot systematically beat the reviewers' own
average at predicting the reviewers' final decision — that extra information has to come from
outside the paper.

Decomposing cspaper's correlation: a predictor that only knows the binary accept/reject decision
(no score-level information at all) would already achieve r = 0.6858 against `gt_avg_score` on
this set — i.e. **most of cspaper's headline r = 0.7587 (full-overlap) is explained by decision
knowledge alone**, not fine-grained scoring skill. Within-bucket, cspaper still discriminates
somewhat (r = 0.5187 within accepted papers, r = 0.5195 within rejected papers, n=159/231), so
it isn't purely a coin flip on the decision — but the ~92% decision-side accuracy is far above
what any of our arms achieve (59–65%). This is not "cspaper infers the decision first, then sets
the score to match" (a reasoning artifact) — the ~92% decision-side accuracy is far too high to
be explained by review quality and is best explained as **decision leakage**: the ground-truth
accept/reject outcome for these ICLR 2026 papers is highly likely already present in cspaper's
training data or retrieval context (e.g. via OpenReview), and `main_score_norm` is contaminated
by it directly, independent of the review reasoning shown in its output. **Do not report cspaper's
correlation as a fair comparison point without this caveat**, and prefer the within-bucket
correlations (~0.52) as the more honest estimate of its actual paper-quality-scoring skill,
which is roughly in line with the other baselines.

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

### Weakness-reliability AI judge — validation against human labels (overlap set)

The weakness-reliability judge (Sonnet-5, ICLR error-type guideline) scores each review
weakness on a 0–1 reliability scale. To validate it we use the ReviewCritique human-annotated
overlap set: weakness segments that two reviewers of the same paper both raised, so each has a
human reliable/unreliable label. The judge scored all **815 unique overlapped segments**; we
measure it against the human label, treating **No/unreliable as the positive class**.

**Grade the judge against the *same* segment's human label** (the segment it actually scored) —
not the paired other reviewer's label. On the whole overlap set:

| judge guideline | set | AUROC | F1-max | prec | rec | n (pos) |
|---|---|---|---|---|---|---|
| with examples | whole 815-seg | 0.639 | 0.362 | 0.256 | 0.618 | 815 (144) |
| with examples | strict same-issue subset | 0.642 | 0.373 | 0.247 | 0.760 | 299 (50) |
| definitions only (no examples) | 60-pair look | 0.721 | 0.514 | 0.375 | 0.818 | 58 (11) |
| with examples | 60-pair look | 0.764 | 0.552 | 0.444 | 0.727 | 58 (11) |

For reference, grading against the *other* (cross-reviewer) human label collapses AUROC to
chance (~0.50, F1-max ~0.31 whole set) — expected, since the two reviewers' segments are only
approximately the same issue and the same 2-annotator team disagrees with itself across
presentations, so the cross-reviewer label is a noisy target.

**Leakage caveat.** The guideline's few-shot examples and the judged overlap segments are both
drawn from `ReviewCritique.jsonl`; 24/815 judged segments (3%) appear verbatim as guideline
examples (all as *unreliable*). This inflates the with-examples numbers slightly. The
downstream `final_results` critics eval is unaffected — those reviews are on the ICLR-2026 paper
set, disjoint from ReviewCritique.

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