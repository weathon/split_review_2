Now I have all the information I need. Let me write the final review.

## Summary

This paper addresses "under-thinking" in Large Reasoning Models (LRMs), where models discover a promising reasoning trajectory early but switch away excessively. The authors propose Steady Thought (ST), a three-stage pipeline: (1) entropy-based segmentation of responses into thoughts, (2) suppressed-decoding completion from each thought to assess promise, and (3) thought-level preference optimization (STPO) treating the completion as chosen and the original continuation as rejected. Experiments across three model sizes (1.5B, 8B, 14B) and four datasets show accuracy improvements up to 5.3% with token reductions up to 39.3%.

## Strengths

1. **Well-motivated problem with clear evidence.** Figures 1a/1b empirically demonstrate that the first correct thought appears early in the chain while models continue switching, making the "under-thinking" phenomenon concrete. This is a real and practically relevant issue.

2. **Consistent results across multiple models and datasets.** Table 1 shows accuracy improvements and token reductions across three model sizes and four datasets, including an out-of-distribution coding benchmark (LiveCode). The improvement direction is consistent across nearly every setting.

3. **Sensible architectural decoupling.** The three-stage pipeline (segmentation → completion → preference optimization) cleanly separates data construction from training. Using suppressed decoding only during data generation while relying on preference optimization to internalize behavior at inference is a principled distinction from prior inference-time suppression methods.

4. **Informative ablation studies.** Section 4.4.4 (Table 4) usefully compares STPO against SFT and DPO, showing that SFT on short chosen responses degrades accuracy and that DPO's length sensitivity is problematic when chosen/rejected lengths differ substantially—directly motivating the length-normalized objective.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or confidence reporting despite small test sets.** The paper reports "the average of eight test runs for the AIME 2024 test set" (line 143) but provides only point estimates with no standard deviations or confidence intervals. AIME 2024 has only 30 problems—the reported improvement for DeepSeek-R1-Distill-Qwen-1.5B (27.5% → 31.2%) represents roughly 1 more correct problem out of 30. Without measures of variance, it is impossible to assess whether the observed differences are genuine or within the noise of stochastic sampling. This gap weakens every quantitative claim in the paper and is especially problematic for the small AIME test set where random variation is largest.

2. **The NOWAIT baseline shows unexplained catastrophic failure on Qwen3-8B.** On MATH-500, NOWAIT achieves 61.0% accuracy vs. Vanilla's 91.4% while tokens increase from 4,724 to 13,274 (Table 1). On GSM8K, it achieves 73.3% vs. 95.6% with tokens surging from 1,759 to 12,369. The method's design is to suppress switching (which should reduce tokens), yet it does the opposite while cratering accuracy. The paper provides no explanation or discussion of this failure. While this does not invalidate other baselines or the ST results, the omission is concerning: readers cannot tell whether this reflects an implementation error or a genuine model-specific incompatibility.

### Minor

1. **The STPO objective is SimPO with different conditioning.** Equation 7 is identical to Equation 3 (SimPO) except that conditioning is on (Q, T_i) rather than just x. The paper (line 270) writes "we contribute STPO, a novel preference optimization framework," but the novelty lies in the data construction pipeline and the thought-level framing, not in the optimization objective itself. The paper would benefit from more precise language.

2. **The PCT analysis infers switching quality rather than measuring it directly.** Section 4.4.2 argues that a lower proportion of correct intermediate thoughts (PCT) implies fewer "invalid switches." However, PCT could decrease for other reasons (e.g., the model finds the correct answer earlier, reducing intermediate thought count, or the segmentation changes after training). The paper's central claim of "more rational switching" (abstract) rests on this correlational evidence rather than a direct measurement of switching decisions.

3. **Threshold tuning evidence is thin in the main paper.** Table 3 tests only three threshold values (2.8, 3.0, 3.2) on one model (DeepSeek-R1-Distill-Qwen-1.5B). The improvements at 3.0 vs. 2.8 are modest (84.4% vs. 83.4% on MATH-500; 31.2% vs. 29.2% on AIME 2024), and the appendix reference provides no evaluation in the main paper.

4. **No discussion of failure cases or limitations.** The conclusion (Section 6) simply claims success. A dedicated limitations section discussing what types of problems or models ST does not help would strengthen the paper.

5. **No evaluation of training data quality.** Stage 2 generates completions using suppressed decoding; the paper does not report what fraction of these completions are correct vs. incorrect. If the correct-completion rate is low, the training signal would be noisy.

### Trivial
None.

## Nice-to-Haves
- Adding a direct measurement of switching decisions (e.g., annotating whether each switch is beneficial or wasteful) would provide stronger evidence for the central claim about "more rational switching."
- Ablating entropy-based segmentation against simpler alternatives (e.g., rule-based splitting on ".\n\n" only) would clarify whether the entropy computation adds value.
- Reporting the computational cost of Stage 2 (the model must generate completions from every segmented thought) would help practitioners assess practicality.

## Removed Points
- **NoThink is a straw man:** Removed. NoThink is a published baseline (Ma et al., 2025). Including it alongside competitive baselines is standard; its poor performance is transparently reported.
- **NOWAIT failure "casts doubt on entire baseline setup":** Removed this framing. One baseline's failure does not logically imply other baselines or the ST results are unreliable. The weakness is specific to the unexplained NOWAIT behavior.
- **"ST worse than SEAL on LiveCode 14B":** Removed. The table transparently reports 74.3% vs. 75.1%; the aggregate "Overall" column averages across datasets as stated. This is not a weakness.
- **Circularity in promising-thought definition:** Removed. The paper defines a promising thought via a straightforward data-labeling procedure (suppressed-decoding continuation yields correct answer). There is no circularity.
- **Figure 2 seeming contradiction (more thoughts on AIME after ST):** Removed. The paper honestly reports and discusses this finding. More (but shorter) thoughts on hard problems is consistent with the method's goals and does not contradict the paper's claims.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Report standard deviations or confidence intervals for all main results, especially AIME 2024 (30 problems, 8 runs). This single change would substantially strengthen the paper.
2. Diagnose and explain the NOWAIT baseline behavior on Qwen3-8B, or replace it with a correctly configured version.
3. Add a limitations section discussing when/where ST does not help.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| TPO | O0sQ9CPzai.md | 6.33 | 1,2 | Yes | Multi-branch preference optimization for reasoning. Stronger on loss-function novelty (+3), but evaluated on only 1 model type vs. our 3. Similar concern about noisy preference data (-4). |
| IUPO | bGGMLWAGMc.md | 5.50 | 2 | Yes | Iterative uncertainty-based preference optimization. Similar level of optimization novelty (both criticized as not sufficiently novel, -4 for IUPO). Comparable evaluation breadth. Our paper's evidentiary gaps (no variance, NOWAIT) are less severe than IUPO's three -4 weaknesses. |
| 3D-Properties | 9Hxdixed7p.md | 6.25 | 1 | Yes | DPO analysis paper. Different contribution type (theoretical analysis vs. method). Less directly comparable. |
| RainbowPO | trKee5pIFv.md | 6.00 | 1 | Yes | DPO component analysis. Meta-study, less directly comparable. |

**Round 1 bracket:** 5.0–6.5. The paper sits between IUPO (5.50, Reject) and TPO (6.33, Accept), with weaknesses less severe than IUPO's (-4 items) but lacking the loss-function novelty of TPO (+3). The primary discrimination is that this paper has two significant evidential gaps—no variance reporting and an unexplained baseline failure—that prevent a clear accept.

**Final placement:** 5.5. The paper identifies a genuine problem and proposes a reasonable pipeline with consistent results. However, the lack of any variance/confidence reporting (despite running 8 trials on AIME's 30 problems) and the unexplained NOWAIT collapse on Qwen3-8B are evidential gaps that prevent acceptance in the current form. The method is promising and the core idea is sound, but the experimental presentation is incomplete.

MY FINAL SCORE: 5.5
MY FINAL DECISION: Reject