Given the impact signals — the core theoretical contributions (ContrastiveCAMs) score very high (+8.7), the practical robustness experiment scores extremely high (+9.7), and the largest weakness only reaches -4.3 (moderate) — the paper is clearly on the accept side. The weaknesses are real but addressable; none threaten the core claims.

## Summary

This paper identifies a theoretical limitation of HiResCAMs — they are not uniquely determined due to softmax shift-invariance (Theorem 3.2) — and proposes ContrastiveCAMs to resolve this ambiguity (Theorem 3.5, Proposition 4.1). It leverages this principled explanation method to design Core-Focused Cross-Entropy (CFCE), a training loss that penalizes non-core region contributions and encourages feature alignment. Experiments on Hard-ImageNet, Oxford Pets, and PASCAL VOC demonstrate improved core-region alignment (IoU) and downstream segmentation transfer, with robustness to approximate masks (SAM, bounding boxes).

## Strengths

- **A clean theoretical observation about HiResCAMs (Theorem 3.2).** The paper correctly identifies that because HiResCAMs are defined on logits while predictions are determined through softmax (which is shift-invariant), infinitely many HiResCAMs can correspond to the same prediction. This is articulated formally and clearly — a genuine structural limitation of a widely used method.

- **ContrastiveCAMs are a theoretically principled fix (Theorem 3.5, Proposition 4.1).** The pairwise subtraction formulation naturally removes the M-ambiguity. Proposition 4.1 showing that softmax probabilities can be expressed directly as a function of ContrastiveCAMs (not just logits) grounds the explanation in what the model actually outputs — a strong correctness guarantee.

- **Comprehensive experimental design across settings.** The evaluation spans multiclass (Hard-ImageNet), multiclass 37-way breeds (Oxford Pets), binary (Oxford Pets cat/dog), and multilabel (PASCAL VOC) classification. The downstream segmentation transfer experiment (Figure, line 318) provides strong evidence that CFCE-trained backbones learn genuinely better features beyond the training task.

- **Robustness to approximate masks (Section 5.2).** The Oxford Pets experiments showing that SAM-generated masks or bounding boxes can substitute for ground-truth masks without catastrophic degradation substantially improves the paper's practical credibility. A method requiring perfect pixel-level masks would be unusable in most real settings.

## Weaknesses

### Fatal
None.

### Major

- **The ~4% un-ablated accuracy drop on Hard-ImageNet is under-discussed.** CE achieves 94.25% un-ablated accuracy; CFCE drops to 90.53% (−3.72%), CFCE+KL to 90.35% (−3.90%). This drop is larger than competing core-region methods (CORM: 92.91%, CORM+DFR: 91.31%). The paper describes this as "at the cost of some un-ablated performance" (line 244), which understates the degradation. The paper does not analyze whether the model is genuinely learning better core features or simply having non-core reliance regularized away at the expense of overall predictive power. The downstream segmentation experiment partially addresses this, but only on one dataset.

- **Computational cost of CFCE training is never acknowledged or quantified.** Computing ContrastiveCAMs during training requires gradient computations (∇_{A_j} f_c) at each step for the loss, then another backward pass for weight updates. The paper provides no analysis of training time, memory overhead, or wall-clock cost relative to standard CE training. For a proposed training method, this is a significant omission.

### Minor

- **ContrastiveCAM IoU is not reported for the CE baseline in Table 2** (shown as "—"). The paper explains (line 257) that GradCAMs were used for consistency with baselines, but without the CE baseline's ContrastiveCAM IoU, the reader cannot assess whether the headline numbers (89–93%) represent a meaningful improvement over what CE models already achieve on this metric.

- **Baselines CORM, DFR, and CORM+DFR in Table 2 are reported as point estimates without variance/error bars**, while CFCE methods include ± values. This makes it difficult to assess whether differences between methods are statistically significant.

- **The "Pareto improvement" claim for PASCAL VOC (line 306) is slightly over-stated.** While validation AP and IoU both improve (87.32%→88.39%, 44.50%→82.07%), training AP drops from 99.75% to 98.38% (CFBCE), so the improvement is not strictly Pareto-dominant across all metrics.

### Trivial
None.

## Nice-to-Haves
- An out-of-distribution robustness evaluation (e.g., ImageNet-A, ImageNet-R) would help distinguish whether the accuracy-IoU tradeoff reflects genuine core-feature learning or mere regularization.
- An ablation decomposing the CFCE loss components (core contrast term vs. non-core penalty term) would clarify how each contributes.
- Reporting training wall-clock time and GPU memory for CFCE vs. CE would help practitioners assess feasibility.

## Removed Points
These points were flagged for removal from the input review. Treat them with caution:
- *Criticism about mask supervision limiting applicability* — already discussed in Section 5.2 (SAM/BBOX experiments). Removed as already addressed.
- *Criticism that "cross-entropy can motivate feature misalignment" is overstated* — the section title says "Can Motivate" (weaker claim), Proposition 4.2 correctly shows CE is indifferent, and Table 1 provides empirical support. Removed as not a genuine weakness.
- *Criticism that Theorem 4.6 is a tautology* — it establishes consistency of surrogate loss with the constrained objective, a standard result type. Removed.
- *Criticism that SAM/BBOX results are "much closer to CE baseline"* — factually incomplete: in multiclass setting SAM (85.16%) and BBOX (84.61%) show ~5% improvement over CE (80.16%). Removed.
- *Missing hyperparameters (λ1, λ2, λ3)* and *Hard-ImageNet masks not specified* — likely in stripped appendices; per rules, missing appendix content is not penalized. Removed.
- *Formatting/style nitpicks, grammar, missing related works* — removed per instructions.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add an honest discussion of the accuracy-IoU tradeoff on Hard-ImageNet with analysis of whether the accuracy drop reflects genuine core-feature learning or regularization (e.g., test on OOD datasets).
2. Report training computational cost (time per epoch, memory) to help readers assess practical feasibility.
3. Include ContrastiveCAM IoU for the CE baseline in Table 2 to enable direct comparison.
4. Add variance estimates for all baselines in Table 2.
5. Clarify the "Pareto improvement" claim for PASCAL VOC.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>