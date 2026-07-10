## Summary

This paper introduces TD-JEPA, a novel temporal-difference (TD) latent-predictive representation learning method for zero-shot reinforcement learning. The key idea is to use TD-based, policy-conditioned multi-step prediction trained from offline, reward-free transitions to jointly learn state encoders, task encoders, and successor-feature predictors. The method is grounded in theory (Theorems 1–4) connecting the latent-predictive losses to successor measure factorization for multiple policies, and evaluated across 65 tasks on 13 datasets from ExoRL and OGBench. The standout result is on pixel-based DMC (628.8 ± 5.5 vs BYOL-γ* at 582.4 ± 9.8, non-overlapping CIs).

## Strengths

- **Genuinely novel synthesis.** Combining TD-based latent-predictive learning with policy-conditioned multi-step prediction for zero-shot RL (Eq. 7, 9) is novel and well-motivated. The off-policy TD formulation enables learning from offline, reward-free transitions while predicting multi-step, policy-dependent dynamics, and cleanly connects to successor features.

- **First theoretical connection between latent-predictive TD losses and successor measure factorization for multiple policies.** Theorems 1 and 3 extend prior single-policy theory (Blier et al., 2021; Lan et al., 2023) to a multi-policy setting. Theorem 2's non-collapse guarantee for the "doubly latent-predictive" TD loss is also a new result extending Tang et al. (2023).

- **Strong empirical result on pixel-based DMC.** TD-JEPA achieves 628.8 ± 5.5 vs the best baseline BYOL-γ* at 582.4 ± 9.8, with non-overlapping confidence intervals. This is a genuinely challenging setting (zero-shot RL from pixels) and the ~8% improvement is substantial and clean.

- **Thorough evaluation scope.** 65 tasks across 13 datasets (ExoRL and OGBench), covering locomotion, navigation, and manipulation with both proprioceptive and pixel observations, plus offline and online fine-tuning experiments. The probability-of-improvement analysis (Fig. 2) provides a useful corrective to aggregate means.

## Weaknesses

### Major

- **The "matches or outperforms" framing oversells the OGBench results.** The abstract and introduction claim TD-JEPA "matches or outperforms state-of-the-art baselines" across all settings, but this conclusion is largely driven by DMC_RGB. On OGBench proprioception, TD-JEPA (37.98) is tied with HILP (37.98) and behind FB (39.04). On several individual OGBench tasks, TD-JEPA performs substantially worse than the best method (antmaze-me: 20.20 vs FB's 51.60; cube-single: 34.20 vs HILP's 74.20 and BYOL-γ*'s 79.40; scene: 38.44 vs ICVF*'s 65.40). The probability-of-improvement analysis partially addresses this, but the main claims in the abstract and introduction do not reflect the variation. A more honest characterization would note that TD-JEPA is clearly best on DMC_RGB, competitive on DMC, and mixed on OGBench.

- **Theory relies on restrictive assumptions, particularly symmetric dynamics.** Theorems 1 and 3 require (A3) symmetric transition matrices P^{π_z}, which rules out non-reversible dynamics common in most RL settings. The paper notes these assumptions are standard in the literature and can be relaxed (App. C), but the practical relevance of theoretical guarantees that require symmetric dynamics is unclear. The conclusion acknowledges this as future work, but the theory section is presented as a key contribution and the gap between the idealized setting and the practical algorithm is large.

### Minor

- **Author-designed *-marked baselines.** BYOL*, BYOL-γ*, and ICVF* are novel zero-shot instantiations designed by the authors, not established methods from the literature. The paper is transparent about this (line 251), and the core DMC_RGB result does not depend on them (TD-JEPA also substantially exceeds FB's 456.2 and HILP's 391.2), but comparisons against these baselines carry less weight than comparisons against standard methods.

- **Abstract slightly oversells scope of zero-shot optimization.** The abstract claims "zero-shot optimization of any reward function at test time" (line 9), but the method is limited to rewards in the linear span of ψ (standard for successor-feature approaches). This is correctly clarified in Sec. 3.3, making the abstract slightly imprecise.

- **Coupled optimization of the "doubly latent-predictive" TD losses.** Equation 9 involves T_ϕ predicting into ψ-space and T_ψ predicting into φ-space; these losses are coupled. The paper provides no discussion of whether this coupled system converges in practice, beyond the empirical results.

- **Inference via matrix inversion.** The closed-form solution for z_r requires inverting E[ψ(s)ψ(s)^T] (line 136). For high-dimensional ψ, this could be ill-conditioned, but no discussion of potential numerical issues is provided.

### Trivial

None.

## Nice-to-Haves

- Isolate the effect of TD vs MC targets: a direct comparison between Eq. 5 (MC-JEPA) and Eq. 9 (TD-JEPA) with the same encoder architecture would test whether the TD formulation is responsible for the performance gains.
- Analyze the OGBench antmaze-me failure mode (TD-JEPA at 20.20 vs FB's 51.60) to understand whether this reflects a general difficulty with hard exploration tasks.
- Be more explicit about which assumptions are needed for which theorem and how far the claimed relaxations go.
- Analysis of representation quality (e.g., PCA of latent trajectories) and predictor quality (e.g., TD error plots) would strengthen claims about representations capturing "diverse and long-term dynamics."

## Removed Points

These points are flagged to be removed from the input review; treat them with caution.

1. **BC regularization concern.** The critic flagged that BC regularization on OGBench (footnote line 249) was insufficiently discussed and could interact differently with different methods. Removed because the details are in the (parser-stripped) Appendix E.6, the paper describes this as part of the standard experimental setup from Park et al. (2025b) applied to all methods, and the rule forbids using missing appendix content as a weakness.

2. **Missing representation/predictor quality analysis.** Moved to Nice-to-Haves; these are not core flaws but augmentations.

3. **Orthonormality regularization choice motivation.** Moved to Nice-to-Haves as a minor presentation point.

## Novel Insights

The most insightful observation from the harsh critic is that the paper's empirical strength is not uniform: TD-JEPA is dominant on pixel-based DMC but merely competitive (and sometimes substantially worse) on OGBench individual tasks. This pattern — that the method excels specifically in high-dimensional visual domains with high-coverage data — is a genuinely informative finding that the paper does not sufficiently emphasize. The critic's suggestion to isolate TD vs MC targets would directly test whether the core technical innovation (the TD bootstrapping) drives the gains, which would sharpen the paper's already-strong narrative.

## Suggestions

1. **Sharpen the narrative around OGBench.** The abstract should hedge: TD-JEPA "matches or outperforms baselines on aggregate, with the strongest gains on pixel-based DMC." A brief discussion of the antmaze-me failure mode would add credibility.
2. **Add a TD-vs-MC ablation.** Compare Eq. 5 (MC-JEPA) with Eq. 9 (TD-JEPA) under identical architectures to directly attribute the gains to the TD formulation.
3. **Preface the theory with an explicit statement of which assumptions are needed for each theorem and how far they can be relaxed.** The current presentation defers this to the appendix and conclusion.
4. **Add a brief note on the matrix inversion in inference** (line 136), such as the dimensionality of ψ used in experiments and whether any regularization was applied.

## Score and Decision

**Calibration procedure:** I searched across topical anchors in all bands. The closest matches were Proto Successor Measure (6.75, Reject — weaker experiments, stronger theory), Bridging State and History (6.75, Accept — similar theory contribution, weaker experiments), Towards General-Purpose Model-Free RL (7.50, Accept — comparable scope, messier theory and baseline concerns), Conservative World Models (4.75, Reject — significantly less novel), and Zero-Shot Whole-Body Humanoid Control (6.50, Accept — narrower scope, weaker novelty). After itemized calibration comparing favorability ratings, TD-JEPA's strength favorability (10.83–12.28) matches the 7.5 anchor range (10.91–12.75), while its most negative weakness items (-2.38, -0.77) are substantially milder than the anchors' harshest items (-3.80, -4.39). This places TD-JEPA solidly in the Accept range. The restrictive theory assumptions and mixed OGBench results prevent a higher score but do not undermine the core contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>