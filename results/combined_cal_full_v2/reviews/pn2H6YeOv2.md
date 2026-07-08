Now I have all the information needed. Let me compile the final review.

**Round-1 bracket assessment:** The paper sits between the C-CLIP anchor (6.50, the most directly comparable method paper) and the Concept Drift paper (7.00). It is clearly stronger than the 3.80-5.67 anchors and weaker than 8.0+ CLIP analysis papers.

**Final score comparison with C-CLIP (6.50):** Pi-CCA has higher-weighted strengths (10.47-10.98 vs C-CLIP's 9.32-10.75 range) and its weaknesses are all moderate positive weights (3.22-5.60) rather than the strongly negative weights C-CLIP incurred (down to -2.76 for delivery issues). The main Fig. 3 weakness (weight 5.60) is a genuine over-interpretation but does not threaten the core empirical contribution. Pi-CCA's method is more novel and its empirical results are stronger than C-CLIP's. Placing it at 6.5 — above C-CLIP but acknowledging the Fig. 3 weakness keeps it from reaching the 7.0 level.

## Summary

This paper introduces Pi-CCA, a replay-free continual learning framework for vision-language models that preserves the geometry of cross-modal alignment via a compact "CCA certificate" capturing the top-k canonical correlations and sketched subspaces. The method uses spectral and subspace-angle preservation losses plus a prompt-invariance regularization term. Across MTIL, X-TAIL, VLCL, and ConStruct-VL benchmarks, Pi-CCA achieves state-of-the-art results among replay-free methods, outperforming recent approaches like C-CLIP, LADA, and DIKI.

## Strengths

- **Conceptually novel framing.** The paper recasts forgetting in VL-CL as alignment-geometry drift — drift in the canonical correlation structure of the whitened cross-covariance — rather than drift in proxy signals (logits, similarities, weights). The CCA certificate (spectrum + sketched subspaces) is a principled way to operationalize this reframing, and the paper demonstrates it is effective in practice. **[weight=10.90]**

- **Consistent SOTA results across four benchmarks.** Tables 1 and 2 show Pi-CCA outperforming all replay-free baselines on MTIL (76.8 vs. 75.2 next-best), X-TAIL (68.1 vs. 67.4), VLCL retrieval (48.6 vs. 47.3), and ConStruct-VL (75.2 FA / 2.7 AF). The improvements over strong recent methods like C-CLIP, LADA, and DIKI are meaningful and hold across both classification and retrieval tracks. **[weight=10.98]**

- **Thorough component ablation.** Table 3 cleanly separates the contribution of each term. The largest drops come from removing spectral or subspace preservation, confirming both parts of the certificate matter. The ablation also shows the sorted surrogate for spectral matching is nearly lossless vs. exact Hungarian pairing, and Gaussian vs. SRHT sketches behave similarly. **[weight=10.47]**

- **Task-order robustness analysis (Fig. 5).** Testing 20 random permutations of the 11-domain MTIL sequence and showing narrow IQRs (roughly ±0.5 p.p.) is a strong check that the method does not depend on a favorable ordering. **[weight=9.40]**

## Weaknesses

### Fatal
None.

### Major

- **Over-interpreted geometry-performance correlation evidence (Fig. 3).** The paper reports near-perfect Pearson/Spearman correlations (r=0.99–1.00, ρ=1.00) — values that are not credible for real experimental data with multiple, independently varying configuration parameters. More importantly, the experimental design is structurally confounded: the drift measures (D_ang = Σ sin² θ_i, D_ρ = ‖ρ̂ − ρ*‖₂) are exactly the quantities Pi-CCA's regularization losses penalize, and the configurations swept are hyperparameters that directly control how strongly these quantities are regularized. When varying these, both drift and performance move together because they are coupled through the same loss terms — not because the paper has independently discovered that "geometry predicts retention." The claim in §4.3 and conclusion that "stability of the canonical subspace/spectrum reliably predicts downstream performance" is broader than what this experimental design supports. This weakens a sub-claim about mechanism but does not invalidate the core empirical results (Tables 1–3). **[weight=5.60]**

### Minor

- **Confounded prompt invariance evaluation.** The ablation (Table 3) removes both λ₃ and M together (λ₃=0, M=0). The stress test (Fig. 4) compares Pi-CCA (λ₃=0.2, M=4) to the same ablated variant. In neither case is λ₃ ablated while keeping M>0, or M reduced while keeping λ₃>0. This means the observed benefit could come entirely from multi-prompt averaging (M>0) rather than from the dispersion-contraction term in L_pi. The prompt invariance component is not as rigorously validated as the spectral and subspace terms. **[weight=4.94]**

- **Missing standard deviations for MTIL/X-TAIL.** Table 1 does not report standard deviations or confidence intervals for MTIL/X-TAIL results, while Table 2 does for VLCL/ConStruct-VL. This inconsistency makes it harder to assess whether the MTIL gains are statistically significant against baselines. **[weight=5.02]**

- **Missing comparison of computational cost against baselines.** The Pareto analysis (Fig. 2) compares Pi-CCA configurations against each other across memory and time, but does not show where baselines sit on this frontier. The method requires computing whitened cross-covariance, top-k SVD, sketch projections, and four loss terms per step — substantially more computation than simpler regularization methods. Without per-step wall-clock time or total training time vs. each baseline, the reader cannot assess the cost of the SOTA gains. **[weight=3.22]**

### Trivial
None.

## Nice-to-Haves
- A sensitivity analysis over intermediate values of λ₁, λ₂, λ₃ (not just the λ=0 extreme) would strengthen practical recommendations.
- A plot showing how the canonical correlations and subspace angles evolve across the task sequence would help the reader understand whether the certificate EMA is working as intended.
- A brief discussion of scenarios where the certificate may fail (e.g., very long task sequences, domains where the assumption of fixed low-rank alignment structure breaks down) would improve the paper's completeness.

## Removed Points
- **Criticism about the paper's "proxy signals" framing being overstated.** This is a stylistic preference, not a technical weakness. The paper's framing is appropriate for emphasizing its contribution.
- **Speculative criticism about EMA covariance conditioning over long sequences.** No evidence this is an actual problem; the paper already addresses conditioning with ridge shrinkage and eigenvalue flooring (§3.1).
- **Criticism about missing α value in main text.** This is standard appendix content.
- **Criticism about CLAP4CLIP not being in tables.** Minor omission from a supplemental table; main comparisons are complete.
- **Criticism about GIFT framing.** The paper already marks GIFT with † for synthetic replay and clearly contextualizes the comparison.
- **Criticism about missing limitations paragraph.** Absence is a presentation choice, not a technical flaw.
- **Generic/superficial strengths** about addressing an important problem or being practical — these lack specific evidence tied to the paper's content.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Fix the correlation analysis in Fig. 3: (a) compute correlations on genuinely independent runs with different random seeds per configuration to show variability, (b) report the number of data points and standard error of the correlation estimate, (c) acknowledge the coupling between drift measures and regularization, re-framing this as a consistency check rather than a causal discovery. Consider an experiment where drift is independently manipulated (e.g., by artificially perturbing the certificate) to strengthen the mechanistic claim.
- Isolate the prompt invariance component: test λ₃ > 0 with M = 1 (single perturbation, so the dispersion term is zero), and also test λ₃ = 0 with M > 1 (multi-prompt averaging without the loss).
- Add per-step wall-clock time and total training time for Pi-CCA vs. each baseline.
- Add standard deviations or confidence intervals to Table 1 for consistency with Table 2.

**Calibration anchors used across rounds:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sb7qHFYwBc.md` (C-CLIP, avg 6.50, Round 1&2, itemized) — Directly comparable VL-CL method that Pi-CCA outperforms. Pi-CCA has more novel method and stronger empirical results but its Fig. 3 weakness keeps it close to this anchor.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TLADT8Wrhn.md` (TiC-CLIP, avg 6.25, Round 1&2, itemized) — Benchmark-focused CLIP continual learning paper. Less comparable but anchors the 6–7 range.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/G9Ea7mlqGO.md` (CLIP as Efficient Online CL, avg 3.80, Round 1, itemized) — Lower-scored VL-CL method paper. Pi-CCA is clearly stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/b20VK2GnSs.md` (Adapting MLLM to Concept Drift, avg 7.00, Round 2, itemized) — Upper anchor. Pi-CCA is slightly below this level due to the Fig. 3 issue.
- Other anchors from calibration_search not itemized: `JIlIYIHMuv.md` (LVLM-CL, 2.50), `WM5G2NWSYC.md` (Projected Subnetworks, 2.00), `gNoqEdT2wO.md` (MCIL benchmark, 2.33), `k9NYnsC4Mq.md` (Proof, 5.67), `wE1I9IGqeH.md` (Complementary Memory, 6.00) — all used for bracketing.

**Weighted item comparison:** Pi-CCA's highest-weight weaknesses (Fig. 3 at 5.60, Table 1 stddevs at 5.02) are comparable in impact to C-CLIP's top weaknesses (limited backbone at 6.27, limited tasks at 6.13). But Pi-CCA's strengths (10.47–10.98) are consistently higher than C-CLIP's (9.32–10.75 range), reflecting the stronger conceptual novelty and more comprehensive empirical evaluation. The paper sits above C-CLIP (6.50) but the Fig. 3 over-interpretation issue prevents it from reaching the 7.0 level of the Concept Drift anchor, which had stronger validation methodology despite its own issues.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>