## Summary

This paper formalizes critical KV cache selection for LLM inference from an output perturbation perspective. It derives an upper bound on attention output perturbation (Theorem 3.3) that involves both attention weights and projected value states ||V_i W^O||_1, then proposes a perturbation-constrained selection algorithm scoring entries by the product A_i × ||V_i W^O||_1. Integrated with three existing eviction methods (SnapKV, AdaKV, HeadKV) across three LLMs (7B–32B) and 29 datasets from Ruler and LongBench, the method consistently reduces compression loss with negligible computational overhead.

## Strengths

1. **Theoretically grounded selection criterion.** Theorem 3.3 derives an upper bound on output perturbation that naturally incorporates projected value states VW^O, formally demonstrating that attention-weight-only selection is suboptimal. This is a genuine intellectual contribution over prior heuristic methods and provides a principled rationale for the proposed scoring function.

2. **Consistent and large empirical gains with broad coverage.** Across 3 LLMs (7B–32B), 3 base methods, 2 benchmarks (29 datasets), and multiple cache sizes, the "w/ ours" variant nearly always outperforms the base method (e.g., Mistral-7B Ruler: AdaKV jumps from 34.88 to 69.17 at 40% cache; Qwen2.5-32B: HeadKV loss drops from 13.7% to 3.4%). The claim of "reducing compression loss by more than half on average" is substantiated by the reported numbers.

3. **Minimal computational overhead.** The additional operation is ||VW^O||_1 (a linear projection). TTFT increase is ~0.06s at batch size 1 and ~0.04s/request at batch size 4 — negligible relative to the quality gains. The method can be dropped into existing pipelines.

4. **Empirical validation of the perturbation mechanism.** Section 4.7's head-wise (92% of heads show lower perturbation), layer-wise (progressive reduction), and budget-wise (robust across 2.5%–40% cache sizes) analysis provides direct evidence that the theoretical bound translates to reduced actual perturbation, closing the loop between theory and practice.

## Weaknesses

### Major

1. **Evaluation confounds query-source change with score-function change.** This is the most significant weakness. The base methods (SnapKV, AdaKV, HeadKV) select entries using accumulated attention weights from an observation window — averaging over multiple query positions and applying pooling (Algorithm 2, lines 3–4). Algorithm 1 ("our selection") computes attention from a **single** query q (line 2). Two things differ: (a) query source (accumulated window → single query) and (b) score function (attention alone → attention × value norm). The paper attributes all gains to (b), but (a) could be driving some or most of the improvement — single-query attention may simply be a better signal for the current decoding step. The paper never isolates this. An ablation using the *same* accumulated attention Ā (as the baseline) with the value-norm product Ā_i × ||V_i W^O||_1 is needed to support the central claim that value-state norms are responsible. Without this, the experimental design does not establish the paper's claimed mechanism. This is verified directly from the paper: Algorithm 2 line 3 uses `A = softmax(Q̂ K^T); Ā = A.mean(dim=0)` (accumulated), while Algorithm 1 line 2 uses `A = softmax(q K^T)` (single query).

2. **Internal inconsistency between α specification, algorithm logic, and sensitivity results.** Three separate problems converge here: (a) Algorithm 1's header specifies α = 0.25 (line 132) while all experiments use α = 0.5 (Section 4.1). (b) The two-stage algorithm (select top b' by score, remove, then select top b'' from remainder) uses the same scoring function 𝒜 in both stages, making the overall result equivalent to a single Top-K on 𝒜 regardless of α. The paper's theoretical framing (Assumption 3.4 + Theorem 3.5) is therefore decorative — the two-stage split does not change which entries are selected. (c) Critically, the α sensitivity results (Table 4) contradict this equivalence: on Mistral at 20% cache, α = 0 yields avg 31.94 while α = 0.5 yields 42.85. If the algorithm is truly equivalent to single Top-K on 𝒜, α should not affect the selected set. The paper's explanation ("violation of Assumption 3.4") does not resolve this, because Assumption 3.4 concerns a condition on attention weights, not a mechanism for changing the selected set. This means either the implementation differs from the pseudocode (e.g., Stage 1 may actually select by attention weights alone, despite the pseudocode showing 𝒜) or there is an unstated algorithmic dependency. Either way, the paper as written contains an internal contradiction that undermines confidence in both the algorithm description and the experimental results.

### Minor

3. **No variance or significance reporting.** Ruler evaluates 100 samples per task and LongBench has multiple datasets per domain, yet no standard deviations, confidence intervals, or significance tests are reported anywhere. Given that Ruler tasks like NIAH can have high variance, this is a notable omission that would be expected for a paper making strong comparative claims.

4. **H2O baseline is simulated.** The paper acknowledges that H2O is simulated by observing only the last 256 tokens' attention (due to FlashAttention-2 incompatibility). This is a reasonable practical compromise, but the H2O numbers are used as a reference point without sufficient caveating that they may not reflect the original method's performance.

5. **SCBench evaluation is narrow.** Only one model (Llama-3.1-8B) and one base method (AdaKV) on three SCBench tasks. Gains on Retr.KV are small in absolute terms (19.40 → 19.80 at 40%). While the multi-turn setting is welcome, the limited scope of this experiment reduces its evidentiary value.

6. **Decoding latency only reported for SnapKV.** The paper states that "SnapKV (with or without our algorithm) achieves 0.0332s" for decoding, but does not report decoding latency for AdaKV or HeadKV with the algorithm. If only SnapKV supports the batched decoding optimization, the efficiency comparison across methods is incomplete.

### Trivial

7. **α = 0.25 in Algorithm 1 header vs α = 0.5 used throughout experiments.** This is a clear typographical inconsistency that should be corrected.

## Nice-to-Haves

- An ablation isolating the value-norm contribution while keeping the accumulated attention computation unchanged (see Major Weakness #1). This is the single most impactful addition the authors could make.
- Reporting standard deviations or confidence intervals for main benchmark results.
- A limitations paragraph discussing the confound identified above and settings where the method may underperform.

## Removed Points

These points from the input review were removed with justification:
- **"No comparison to KIVI/GEAR"** — these are quantization methods, not selection methods; the paper correctly scopes its comparison to selection-based eviction.
- **"Missing related works"** — cannot verify without external sources per review guidelines.
- **"No discussion of limitations"** — this is a presentation suggestion, not a scientific weakness; moved to Nice-to-Haves.
- **Pure formatting/style nitpicks** — these are parser artifacts, not author errors.
- **Speculation about unverified appendix content** — per guidelines, appendix content is assumed to exist.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Deconfound the evaluation.** Add an ablation where the score Ā_i × ||V_i W^O||_1 uses the *same* accumulated attention Ā as the baseline, and compare to the baseline Ā_i alone. This would directly isolate whether the value-norm term is responsible for the gains, supporting the paper's central claim.

2. **Clarify the algorithm.** Resolve the α inconsistency (0.25 vs 0.5). Explain why α sensitivity results differ if the algorithm is equivalent to single Top-K — or correct the pseudocode if Stage 1 actually uses a different criterion (e.g., attention weights alone as suggested by the text).

3. **Add variance estimates.** Report standard deviations or confidence intervals for the main experimental results, particularly for Ruler tasks that can exhibit high variance.

## Score and Decision

**Score bracket (Round 1):** [5.0, 6.5]

**Anchors used for calibration:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lRTDMGYCpy.md` — avg 5.75 (R1). An earlier version of this same paper; rejected. The current version is substantially expanded (added Ruler, Qwen2.5-32B, HeadKV) but has new issues (confound, α inconsistency).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jZVNmDiU86.md` — avg 5.60 (R1, R2). PyramidKV, rejected. Less theoretical depth and narrower evaluation than the current paper.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FJFVmeXusW.md` — avg 6.50 (R1). HeadKV/Not All Heads Matter, accepted. Comparable sub-area, accepted with minor concerns.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BQwsRy1h3U.md` — avg 6.00 (R1). MatryoshkaKV, accepted. Similar area, accepted despite missing baselines and runtime concerns.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NcKUcd4EkA.md` — avg 5.25 (R2). Different caching sub-problem, rejected.

The current paper has stronger theoretical grounding than any anchor paper and more comprehensive evaluation than PyramidKV or MatryoshkaKV. However, the structural confound in the evaluation (Major #1) prevents attribution of gains to the claimed mechanism, and the α inconsistency (Major #2) is an internal contradiction that needs resolution. These weaknesses are more significant than those in the accepted anchors (HeadKV at 6.50, MatryoshkaKV at 6.00). The paper sits between PyramidKV (5.60, rejected) and MatryoshkaKV (6.00, accepted), and slightly below the earlier version's score (5.75) because while the experiments have expanded, the confound and α issues are newly identified problems that were not present in the earlier version's evaluation.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>