Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper introduces PI-CCA, a replay-free continual learning framework for vision-language models that preserves cross-modal alignment by directly constraining the canonical correlation spectrum and subspaces (captured via compact random sketches), rather than optimizing proxy signals like logits or similarities. The method additionally incorporates prompt invariance through projector averaging. Evaluated on four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL), PI-CCA achieves state-of-the-art results among replay-free methods, even surpassing a synthetic-replay approach (GIFT) on some metrics.

## Strengths

- **Conceptual clarity and principled framing.** The paper's core insight — recasting forgetting in VL-CL as alignment-geometry drift rather than degradation of proxy signals — is genuinely novel and well-motivated. The paper clearly articulates this in Sections 1 and 3, and follows through by directly regularizing the canonical correlations and subspaces of the whitened cross-covariance, which is the actual object underlying CLIP's zero-shot behavior. (Weight: +6.73)

- **Technically sound and well-engineered method.** The machinery is sensible: a compact certificate using random sketches (Section 3.2) for constant-size storage of the CCA spectrum and subspaces; streaming EMA estimation of the cross-covariance (Section 3.4) to avoid replay; and a prompt-invariance mechanism via projector averaging (Eq. 5–6, 11) that handles the sign/rotation ambiguity without Procrustes alignment. The differentiable SVD via block power iteration (Section 3.4) makes end-to-end training feasible. (Weight: +5.72)

- **Comprehensive experimental evaluation.** The paper evaluates on four established VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL) with comparisons against 10+ recent baselines. The ablation study (Table 3) isolates each component's contribution, the Pareto analysis of certificate capacity (Fig. 2) provides practical guidance, and the task-order sensitivity test (Fig. 5) addresses a standard concern. (Weight: +3.03)

- **Consistent SOTA results.** PI-CCA achieves the best results among replay-free methods across all benchmarks. Notably, it surpasses GIFT (which uses synthetic replay via diffusion) on VLCL and ConStruct-VL — a meaningful result suggesting that the geometry-preservation approach has advantages over synthetic-replay alternatives. (Weight: +6.65)

## Weaknesses

### Major

- **Geometry→performance correlation analysis reports implausible correlation values.** Figure 3 reports Pearson r = 1.00 and Spearman ρ = 1.00 (or 0.99) for the relationship between geometry drift and performance drop. These perfect/near-perfect correlations on real experimental data involving stochastic optimization are not credible without explanation. The paper (Section 4.3) does not report how many configurations were evaluated, and the correlation could be artificially inflated by a small number of configurations or a self-correlation artifact (both axes share a common cause through the swept hyperparameters). This analysis supports one of the paper's claimed contributions ("furnish analyses linking alignment-geometry stability to retention/transfer trends") and needs honest re-presentation with proper uncertainty quantification. The core method and main empirical results are **not** threatened by this issue, but this supporting evidence is presented in a misleading way. (Weight: -0.09)

### Minor

- **Table 1 (MTIL/X-TAIL) lacks confidence intervals.** Table 2 reports standard deviations via ± notation, but Table 1 reports only point estimates without any uncertainty quantification across multiple seeds. This makes it impossible to assess whether the reported improvements over methods like C-CLIP (+1.6% on MTIL Avg, +1.8% on X-TAIL Avg) are statistically reliable. The inconsistency between the two tables should be fixed. (Weight: -0.30)

- **Framing of "preserving invariants" versus the EMA-based certificate refresh is slightly overstated.** The certificate is updated every step via a slow EMA (Eq. 13, controlled by α). The ablation in Table 3 transparently shows that disabling EMA (α=0) costs 1.2 points on MTIL Avg and 0.9 on VLCL R@1, so some drift is beneficial. The paper acknowledges this as "controlled plasticity" (line 133), which is accurate, but the abstract and contribution language ("preserve pre-trained cross-modal generalization," "preserves alignment as an invariant") overstates the degree of preservation relative to what is actually implemented. The method maintains coherence through slow adaptation of the reference rather than freezing the original alignment. This is a rhetorical calibration issue — the method itself is sound and the ablation is transparent. (Weight: +1.64)

### Trivial

- **The "time-continual study on TiC-YFCC/RedCaps"** mentioned in Section 4.1 (line 145) is listed as part of the setup but no results appear in the main paper. If deferred to the appendix, a brief pointer in the main text would help. (Weight: +1.38)

- **Equation in line 129 appears garbled:** M^{(t)} = (∑_{v=1}^t S_v^{(t)})^{-1/2} (∑_{v=1}^t S_v^{(t)})^{-1/2} seems to reference the wrong variables (should likely be Σ_{vv}^{(t)} and Σ_{tt}^{(t)}). This may be clarified in Appendix A.1 but should be corrected in the main text. (Weight: -0.95)

## Nice-to-Haves

- A per-step wall-clock time and peak memory comparison against baseline methods (e.g., C-CLIP, ZSCL, Mod-X) would help readers assess the cost-benefit tradeoff of the CCA computation. The paper's own Pareto analysis (Fig. 2) is valuable but internal to PI-CCA variants.

- A "frozen certificate" comparison (setting α=0 from the start) would clarify whether the EMA refresh is a necessary enabler or a compensation mechanism. The ablation already reports α=0 performance, so this point is partially addressed.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Computational cost underreported (Critic's Issue 3):** The critic argues there is no wall-clock/memory comparison against baselines. The paper provides a Pareto analysis across PI-CCA variants (Fig. 2), which is a standard way to characterize efficiency internally. A head-to-head comparison would be nice but its absence is not a weakness, especially since the method's "constant-memory" claim (O(hk) storage) is principled and verifiable from the architecture. MOVED to Nice-to-Haves.

- **Overlap in error bars on VLCL/ConStruct-VL (part of Critic's Issue 4):** The critic notes that PI-CCA's intervals overlap with GIFT on some metrics. However, GIFT uses synthetic replay (noted with † in Table 2), and the paper's claim is "state-of-the-art among replay-free methods," which is accurate. The intervals also do not undermine the consistent directional advantage. The genuine concern about missing error bars on Table 1 is kept above.

- **CCA being the "right" alignment object (Critic's section note):** The claim that "the paper never fully establishes that CCA spectrum/subspace is the right alignment object" is an open-ended scope request, not a weakness. The paper motivates this choice intuitively and defers theoretical justification to §A.4, which is standard practice.

- **Reproducibility concerns about missing appendix or code release:** Per hard rules, these are removed.

- **Typo in line 129:** This equation looks garbled and is kept as a Trivial weakness above (not removed).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the geometry→performance correlation analysis (Figure 3):** Report the number of configurations evaluated, provide proper uncertainty quantification for the correlations (e.g., bootstrap confidence intervals), and address the potential self-correlation concern. A strong but imperfect correlation (e.g., r ≈ 0.7–0.9) would still support the paper's argument and would be much more credible than the current r=1.00/ρ=1.00 values.

2. **Add standard deviations to Table 1** (MTIL/X-TAIL) for consistency with Table 2.

3. **Calibrate the framing language** in the abstract and introduction to match the actual mechanism — the paper already acknowledges "controlled plasticity" in Section 3.4, which is the accurate description.

4. **Fix the garbled equation in line 129** and add a pointer to the TiC-YFCC/RedCaps time-continual study if it appears in the appendix.

## Score and Decision

**Bracket analysis (Round 1):** The most directly comparable anchor is the C-CLIP paper (sb7qHFYwBc.md, avg 6.50), which addresses the same VL-CL problem and is a direct baseline. PI-CCA has a more novel core idea (geometry preservation vs. proxy signals), broader evaluation across more benchmarks, and cleaner ablations than C-CLIP. C-CLIP's main weaknesses included missing baselines, presentation issues, and code concerns — PI-CCA does not share these issues. In the 5.5–7.5 band, other anchors (TiC-CLIP at 6.25, k9NYnsC4Mq at 5.67, wE1I9IGqeH at 6.00) all have more serious concerns (experimental design flaws, unclear novelty, small gains) than PI-CCA. The only significant vulnerability PI-CCA has is the implausible correlation evidence in Figure 3, which concerns a supporting analysis rather than the core claims — and even there the model weight is barely negative (-0.09). The high positive weights on the strengths (+6.73, +5.72, +6.65) place the paper firmly above the 6.0–6.5 cluster. However, the correlation issue prevents it from reaching the 7.5+ cluster (where papers like uAFHCZRmXk and 3i13Gev2hV at 8.0 have no comparable methodological concerns). Final score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>