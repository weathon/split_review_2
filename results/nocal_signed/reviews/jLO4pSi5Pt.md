Now I have all the information needed. Let me compose the final review.

## Summary

This paper introduces L-TTA, the first method designed for Test-Time Adaptation (TTA) of Vision-Language Models under long-tailed test distributions. It proposes three co-designed components: Synergistic Prototypes (dual prototypes for contrastive tail-class enrichment), Rebalancing Shortcuts (learnable cross-attention modules for dynamic adaptation), and Balanced Entropy Minimization (a modification of standard EM to reduce head-class bias). Experiments across 15 datasets, 3 imbalance ratios, 5 backbones, and 11+ baselines show consistent improvements, with notable efficiency advantages.

## Strengths

- **Well-motivated problem with specific, grounded failure analysis.** The paper correctly identifies that existing VLM TTA methods are evaluated on (nearly) balanced test sets, while real-world test streams are long-tailed. The two identified failure modes — Text-induced Tail Erosion and Modality-bias Amplification — provide concrete, testable intuition about why standard EM-based TTA degrades under imbalance.

- **Exceptionally thorough experimental scope.** The evaluation covers 15 datasets across three benchmarks (OOD, Cross-Domain, Corruption), three imbalance ratios (10, 20, 50), six backbone variants (RN50, ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), and 11+ baselines. L-TTA consistently achieves the best or near-best results across nearly all settings.

- **Genuine practical efficiency advantage.** Table 4 shows L-TTA runs in 1.45h with 1.89G memory, achieving higher HM scores (67.20 on LT-CDB, 46.08 on LT-CB) than methods that are faster but weaker (ZERO, MTA, TDA) and far more efficient than methods that are competitive but far more expensive (RLCF: 18.30h, WATT: 27.70h).

- **Demonstrated robustness to dynamic ordering.** The ablation on head/tail class shifts (Table 7) varies the sampling probability ε for tail-class samples and shows nearly flat performance — a realistic and underexplored stress test.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Theoretical propositions lack rigor as presented.** Propositions 1 and 2 use the vague phrase "split C into C_head and C_tail with certain measurements" without specifying a formal threshold, distributional assumption, or condition. While the proofs are deferred to the appendix (stripped by the parser), the main-text claims of being "both intuitively and theoretically interpretable" are overstated given the informality of the statements. This does not undermine the empirical contribution, but the paper should either formalize these or tone down the theoretical claims.

- **No variance or significance reporting.** The paper states "5 runs for each experiment" across all main tables but reports only point estimates without standard deviations, confidence intervals, or significance tests. Since the long-tailed distributions are created by random sampling, different seeds produce different class cardinalities, so variance is inherent. Without this, it is impossible to assess whether the reported improvements (often in the 1–3% range) are reliable.

- **BEM formulation is underspecified.** Equation 9 defines L_BEM using a variable $\tilde{\mathbb{P}}$ that is never explicitly defined in the text. It appears $\tilde{\mathbb{P}}$ should be $\sigma(z)$ (the pre-adjustment softmax), but this is not stated. This imprecision in a core formula damages reproducibility.

- **CRA loss non-differentiability.** Equation 7 uses a hard argmax-based indicator function $\mathbb{1}$ to compute $c_{c,j}(v)$, which is non-differentiable. The paper does not explain how gradients flow through this term (straight-through estimator, Gumbel-softmax, detached forward pass, or otherwise), leaving the optimization mechanism unclear.

- **K hyperparameter inconsistency.** Implementation details (line 208) list $K = 0.3$, but the ablation study (line 334, Figure 4c) identifies $K = 0.2$ as yielding the best performance. The paper should clarify which value was used for the main results and why.

- **Threshold θ EMA update is under-specified.** Line 104 states "we update θ with the minimal entropy in T following the above EMA manner," but the "above EMA manner" refers to an update rule for prototype vectors (Eq. 4), not for a scalar threshold. How exactly θ is updated via EMA is not clear from the text.

- **Class prior estimation feedback loop.** The class prior π in BEM (line 138) is "continually updated based on the current predicted pseudo-labels." This creates a potential self-reinforcing bias loop (biased predictions → biased priors → more biased predictions). The paper does not discuss this risk.

### Trivial
None.

## Nice-to-Haves

- Adding an experiment that combines an existing TTA method (e.g., TDA or DPE) with a simple long-tailed modification (e.g., logit adjustment or loss re-weighting) would strengthen the claim that L-TTA's co-designed components are necessary — rather than the problem being solvable by a simpler patch to existing methods.
- The EP mechanism would benefit from a brief explanation of its contrastive logic: EPs store features improbable for each class (weighted by $\phi_c$), and Eq. 8 subtracts similarity to these to penalize false positives. The current language ("enrich tail class representations") risks misleading readers who may interpret it as positive enrichment rather than contrastive exclusion.

## Removed Points

These points from the input review were removed, treat with caution:
- **EP "structural inconsistency" claim (Harsh Critic Issue 1):** Removed because it misunderstands the mechanism. The EP is designed as a contrastive store (improbable features), and the subtraction in Eq. 8 penalizes similarity to these, which is logically consistent. For actual tail-class samples, the DP term dominates, providing positive signal. The critic's claim that the mechanism "would reduce the model's ability to predict tail classes" does not hold under scrutiny of the full DP+EP formulation. A clarity note is retained in Nice-to-Haves.
- **Missing comparison against adapted LT methods:** The paper already compares against 11+ baselines. Requesting additional non-trivial adaptations of non-TTA LT methods extends beyond standard expectations.
- **Parser artifact complaints (figure caption repetition, formatting):** These are PDF extraction issues, not author errors.
- **"Gains are modest" framing:** Consistent 1-3% gains across 3 benchmarks × 3 imbalance ratios × 5 backbones constitute meaningful empirical signal, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Explicitly define $\tilde{\mathbb{P}}$ in Eq. 9 and state whether it is treated as fixed or differentiable during backpropagation.
2. Report standard deviations or min/max ranges for all main tables.
3. Clarify the $K=0.3$ vs $K=0.2$ discrepancy.
4. Explain how gradients flow through the hard argmax in Eq. 7.
5. Add a brief discussion of the pseudo-label feedback loop in class prior estimation.
6. Add an experiment combining an existing TTA method with a simple LT fix to demonstrate that the co-designed components add value beyond a simple patch.

## Score and Decision

This paper tackles a genuinely underexplored problem with thorough experimental methodology. The weaknesses are real but entirely addressable — none threaten the core empirical contribution. The propositions overclaim what they establish, the BEM formula needs clarification, and variance reporting is needed, but the consistent improvements across a massive evaluation matrix (3 benchmarks × 3 ratios × 5 backbones × 11+ baselines) provide strong evidence that the method works. With minor revisions addressing the formulation clarity and variance reporting, this would be a solid contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>