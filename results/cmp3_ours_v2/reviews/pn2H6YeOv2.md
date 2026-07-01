Now I have enough calibration context. Let me write the final consolidated review.

## Summary

This paper proposes Pi-CCA, a replay-free continual learning framework for vision-language models that preserves cross-modal alignment geometry (canonical correlations and subspaces) via a compact CCA certificate. The method constrains spectral and subspace drift through dedicated losses while achieving prompt robustness via perturbation averaging. Evaluated across four VL-CL tracks (MTIL, X-TAIL, VLCL, ConStruct-VL), Pi-CCA achieves state-of-the-art results among replay-free methods.

## Strengths

- **Conceptually principled core idea.** The paper reframes forgetting in VL-CL as alignment-geometry drift and directly preserves CCA structure (spectrum + subspace) rather than regularizing proxy signals (similarities, logits, parameters). This is a genuinely different angle from prior work, and Sections 3.2–3.3 develop it with appropriate technical machinery (spectral preservation via sorted pairing, subspace-angle preservation via sketched projectors).

- **Thorough evaluation breadth.** The method is evaluated on four distinct VL-CL tracks (MTIL, X-TAIL, VLCL, ConStruct-VL), covering classification, retrieval, and structured-concept matching. This is broader coverage than typical for a single VL-CL paper.

- **Systematic ablation study.** Table 3 removes each component individually and reports drops across four metrics. The ablations confirm that both spectral and subspace terms are needed, and the pattern of drops is internally consistent (spectral + subspace removal causes largest drops).

- **Task-order sensitivity analysis.** Figure 5 reports results across 20 random task orders with narrow IQRs and per-order means from 3 seeds, ruling out the concern that performance depends on a favorable ordering.

## Weaknesses

### Major

- **Figure 3 geometry–performance correlation reports impossible values.** The figure annotates Pearson r = 1.00 and Spearman ρ = 1.00 for three of four panels (r = 0.99 / ρ = 1.00 for the fourth). These are mathematically perfect or near-perfect correlations, yet the caption mentions "realistic scatter" and shows 95% confidence intervals — which require variance. Any real empirical measurement sweeping multiple independent perturbation dimensions (certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type — at least 7 dimensions listed on lines 222–223) will not produce r = 1.00. This analysis is presented as a key contribution (abstract: "we furnish analyses linking alignment-geometry stability to retention/transfer trends"; conclusion: "stability of the canonical subspace/spectrum reliably predicts downstream performance"), but the evidence as reported is not credible. The values suggest either (a) very few data points (making the correlation estimate unreliable), (b) mathematical dependence between the drift and performance measures (making the correlation a tautology), or (c) misreporting. The authors must show the raw scatter plots with labeled points, report the number of distinct configurations, and verify that drift and performance are measured independently. This is the most significant weakness because it undercuts a stated contribution.

- **Table 1 (MTIL/X-TAIL classification results) lacks variance estimates.** Table 1 reports no standard deviations, error bars, or seed counts, while Table 2 (VLCL, ConStruct-VL) reports ± values. The improvements over the next-best replay-free method are modest: +1.6 on MTIL Avg, +1.7 on MTIL Last, +1.8 on X-TAIL Avg. Given that the similar VLCL results in Table 2 show standard deviations of ±1.0–1.7 for the same method, these gains could fall within noise. The paper's task-order analysis (Figure 5) uses 3 seeds, so the data presumably exists — it needs to be reported. The claim of state-of-the-art performance on MTIL and X-TAIL is unverifiable without variance information.

### Minor

- **"Invariant" framing vs. EMA-updated certificate.** The paper calls the certificate an "invariant" (abstract: "optimizing alignment invariants"; Section 3.2: "spectral invariants" and "directional invariants"; conclusion: "invariants of image-text alignment") yet refreshes it every step via EMA (Eq. 13), described as "controlled plasticity." Since the target itself moves, the method is performing slow tracking of a changing alignment target rather than preserving a fixed invariant. This does not undermine the method's performance, which the authors correctly identify as a design choice, but the "invariant" language is somewhat imprecise. The paper would be more accurate describing the certificate as a slowly-adapting alignment target.

### Trivial

None.

## Nice-to-Haves

- A wall-clock time comparison against top baselines (C-CLIP, ZSCL, RAIL) on the same hardware would strengthen the practicality claim, beyond the Pareto analysis that only sweeps Pi-CCA's own (k, h) configurations.
- A sensitivity analysis for the loss weights λ₁, λ₂, λ₃ and the EMA rates α, β would be useful; the paper currently sweeps only k and h in the main text.
- An ablation comparing Pi-CCA against a simpler baseline (e.g., L_task + weight decay or embedding L2 penalty) would help isolate whether the CCA-specific losses matter more than any additional regularization.

## Removed Points

These points from the harsh critic input are removed with justification:
- **Criticism about garbled notation in Eq. (12):** This is a parser artifact from PDF extraction, not an author error.
- **Missing hyperparameters in the main text:** The paper references Appendix §A.3 for hyperparameter details; the appendix is stripped by the parser. Key parameters (k, h) are given in Figure 2 caption.
- **"Simple" claim inconsistent with method complexity:** Subjective language nitpick; "simple" is relative to generator-based alternatives.
- **Per-step cost comparison with baselines:** This is a nice-to-have, not a core weakness.
- **Proxy-signal distinction "overdrawn":** Subjective opinion about framing quality, not a verifiable weakness.
- **The "Strengthening the Paper on Its Own Terms" section:** These are constructive suggestions, not weaknesses, and are largely covered in the "Nice-to-Haves" section above.

## Novel Insights

The most penetrating observation from the review is that the r=1.00 correlations in Figure 3 are internally inconsistent with the "realistic scatter" and 95% CI also reported in the same figure — a perfect linear relationship has no variance, making a confidence interval meaningless. This suggests either a data-aggregation artifact (e.g., plotting centroids rather than raw points) or a mathematical dependency between the drift and performance measures. Either way, a central piece of evidence for the claim that "geometry drift explains performance" needs careful re-examination. Beyond this, the paper's own contributions — the CCA-certificate approach to replay-free VL-CL — stand as the main intellectual novelty.

## Suggestions

1. **Re-report Figure 3 honestly.** Show raw scatter plots with every perturbed configuration as a labeled point. Report the number of distinct configurations (N). Verify that the drift measures (D_ang, D_ρ) and performance drops (ΔAvg, ΔR@1) are measured from independent computations, not derived from shared quantities in a way that forces a linear relationship. If the correlation is genuinely high, demonstrate it with an honest accounting; if it weakens, calibrate the claim accordingly.

2. **Add variance to Table 1.** Report standard deviations over ≥3 seeds (consistent with the task-order analysis at line 254, which uses 3 seeds). Without this, the SOTA claims on MTIL and X-TAIL cannot be evaluated.

3. **Recalibrate the "invariant" framing.** Either explain in what formal sense the EMA-updated certificate is an invariant, or replace the term with "slowly-adapting alignment target" to match what the method actually does (Eq. 13).

## Score and Decision

**Score calibration anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| C-CLIP (sb7qHFYwBc) | 6.50 | R1 | Direct baseline in the paper; Pi-CCA has a more novel idea but weaker evidence reporting |
| TiC-CLIP (TLADT8Wrhn) | 6.25 | R1 | Strong benchmark paper with experimental design concerns; Pi-CCA's issues are more fixable |
| "Learning without Forgetting for VLMs" (k9NYnsC4Mq) | 5.67 | R1 | Rejected; Pi-CCA has a clearer contribution and broader evaluation |
| Gramian Multimodal Repr. (ftGnpZrW7P) | 7.00 | R1 | Strong paper with cleaner evidence; Pi-CCA's evidential issues prevent reaching this level |
| "CLIP model is an Efficient Online Continual Learner" (G9Ea7mlqGO) | 3.80 | R1 | Rejected; Pi-CCA is clearly stronger in novelty and evaluation depth |

**Round 1 bracket:** 5.5–7.5. Paper clearly above the 3.5–5.5 band papers but below the 7+ level due to evidential issues.

**Final score rationale:** The paper has a genuine conceptual contribution (CCA-geometry preservation for replay-free VL-CL) and the strongest evaluation breadth among replay-free methods I have seen in this area. However, the geometry–performance correlation evidence (a stated contribution) is reported with impossible r=1.00 values, and the main classification results lack variance estimates. These are fixable reporting problems, not structural flaws, but they prevent the paper from scoring higher. Comparable to C-CLIP (6.50) in scope but with more novel methodology offset by less reliable evidence presentation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>