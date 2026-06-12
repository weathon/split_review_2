## Summary

This paper proposes FF-Erase, the first machine unlearning framework designed specifically for Forward-Forward (FF) models. The key insight is that conventional gradient-based unlearning methods fail on FF models due to their layer-wise independent training and sensitivity to parameter tuning, causing model collapse. FF-Erase introduces a goodness-guided strategy using a guidance model to stabilize unlearning via KL-divergence-based goodness shifting, and proposes G-MIA, a goodness-based membership inference attack for verifying unlearning effectiveness in FF models.

## Strengths

- **Genuine problem identification**: The paper is the first to formalize machine unlearning for FF models and clearly articulate why existing unlearning methods fail (sensitivity to parameter tuning, independent layer-wise optimization causing divergent update directions). This is a timely and well-motivated research direction given the growing interest in FF algorithms as biologically plausible alternatives to backpropagation.

- **Well-structured methodology with practical flexibility**: The FF-Erase framework offers two guidance model strategies (mini-retrained and fast-distilled) that provide meaningful efficiency-performance trade-offs, as demonstrated in the ablation study (Table 1). The algorithm is clearly presented with pseudocode (Algorithm 1) and illustrative figures.

- **Novel verification tool**: G-MIA exploits FF-specific properties (layer-wise goodness vectors) to construct a black-box attack that outperforms standard black-box MIAs and, in some configurations, approaches white-box attack performance (Figure 3). This is a useful contribution for the FF research community beyond just unlearning verification.

## Weaknesses

### Fatal
None.

### Major

- **Thin main experimental evaluation**: The unlearning comparison (Section 6.2, Figure 4) is presented only for VGG13 on CIFAR-10, with other results deferred to the appendix. For a paper claiming to establish "an efficient foundation for FF unlearning," demonstrating generalizability across multiple dataset-architecture combinations in the main text is essential. The ablation study (Table 1) is similarly limited to this single setting.

- **G-MIA discriminative power is weak near unlearning boundaries**: The G-MIA scores for all unlearning methods post-unlearning cluster tightly around 0.52-0.55 (Figures 4c and 5c), which is barely above random chance (0.5). This raises a fundamental concern: if the verification tool cannot sharply distinguish between effective unlearning (RE/FF-Erase) and ineffective unlearning (GA with poor λ), then G-MIA may not be providing reliable verification signals. The paper does not adequately discuss this limitation or provide confidence intervals/statistical tests for the G-MIA scores.

- **Insufficient baseline comparison**: The only baselines are retraining from scratch and direct gradient ascent. There is no comparison with more sophisticated approximate unlearning methods such as influence-function-based approaches, SCRUB, Fisher forgetting, or other recent gradient-based methods that could potentially be adapted to FF models (even with modification). This makes it difficult to assess whether the challenges the paper identifies for FF models are truly fundamental or whether simpler modifications to existing methods could suffice.

### Minor

- The paper claims G-MIA "matches the performance of white-box attacks" (in the contributions), but Figure 3 consistently shows white-box methods (ST, GAP) outperforming G-MIA, with G-MIA only matching in specific cases. This claim is overstated.

- The efficiency analysis in Section 4.3 relies on empirical estimates ("about 15% of t_ret" and "10 to 20% of t_ret") that should be more rigorously supported with actual measurements across different settings rather than single-point observations.

- The privacy/forgetting guarantees are empirical only, verified through accuracy metrics and G-MIA. While this is common in approximate unlearning, the paper should more explicitly discuss the absence of formal guarantees and the limitations this entails.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis of the learning rate η during unlearning, since FF models are described as highly sensitive to parameter tuning.
- Discussion of whether FF-Erase extends to other FF variants (e.g., FF-LSTM, FORWARDGNN) mentioned in the related work.
- Analysis of the quality of the guidance model's goodness distributions relative to the ideal retrained model, to better understand how much approximation the mini-retrained and fast-distilled strategies introduce.

## Novel Insights

The paper's core novel insight is that FF models' layer-wise independent training creates a unique challenge for unlearning: unlike BP models where gradient ascent updates all layers coherently via the chain rule, FF layers may diverge in update directions, causing some layers to over-forget while others retain. The proposed solution—using a guidance model to provide target goodness distributions that stabilize the unlearning trajectory—is a sensible approach that leverages the FF architecture's defining feature (goodness scores) as the control mechanism. The idea of G-MIA, using goodness vectors as membership features, is also a genuine contribution that could have broader applications in FF model privacy analysis.

## Suggestions

- Expand the main experimental section to include results across at least 2-3 dataset-architecture combinations to demonstrate generalizability of FF-Erase's advantages.
- Provide confidence intervals or error bars on all G-MIA scores and accuracy measurements, and discuss the statistical significance of differences between methods.
- Include at least one adapted approximate unlearning baseline beyond naive gradient ascent to provide a stronger comparison point.
- Add a discussion on the limitations of empirical verification and the gap between empirical metrics and formal unlearning guarantees.

## Score and Decision

The paper addresses a genuinely unexplored problem with a reasonable approach, clear writing, and a useful verification tool. However, the experimental evidence is too thin (single main setting), the verification tool's discriminative power is questionable near the decision boundary, and the baseline comparisons are insufficiently thorough. These issues collectively weaken confidence in the paper's core claims about effectiveness and reliability. The technical novelty is moderate—the core mechanism is essentially distillation-like guidance applied to a new domain. The contribution is valuable as a first step but needs stronger empirical support.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject