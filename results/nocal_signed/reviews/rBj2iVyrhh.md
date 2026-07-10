Now I have the impact scores from the model. Let me finalize the review with the score and decision.

## Summary

This paper identifies an underappreciated limitation of alternating training methods for multimodal learning: while they mitigate encoder-level gradient interference, they leave a structural classifier bias toward faster-converging modalities. The authors propose Classifier-Constrained Alternating Training (CCAT), a two-stage framework that (1) pretrains a classifier with contribution-regularized bidirectional cross-attention to obtain an unbiased initialization, then (2) freezes this classifier during modality-alternating training while using lightweight LoRA modules to bridge the distribution mismatch between fused features and unimodal features. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over existing methods.

## Strengths

- **Correctly identifies a genuine and underappreciated limitation.** The paper identifies that alternating training methods (MLA et al.) address encoder-level interference but leave classifier-level structural bias toward faster-converging modalities intact. The empirical tracking in Figure 1 supports this, showing MLA's modality contribution ratio only improves from (1.00, 0.00) to (0.90, 0.10) over 100 epochs — a clear residual imbalance that appears to be classifier-driven rather than encoder-driven.

- **Systematic ablation study (Table 2) with high informational value.** All four components (classifier freezing, alternating training, secondary updates, LoRA) are tested individually; each contributes positively to the final method. This is more informative and carefully structured than the ablation studies typical of this area.

- **Consistent improvements across all three benchmarks in the multimodal setting.** CCAT outperforms all baselines including recent SOTA methods (LFM, MMPareto) on CREMA-D (+1.35%), Kinetic-Sound (+6.76%), and MVSA (+1.92%).

- **Clean overall design with well-motivated components.** The two-stage pipeline is coherent: pretrain a balanced classifier via cross-attention + regularization, freeze it during alternating training, and use LoRA modules to handle the resulting fused-to-unimodal feature distribution shift (explicitly discussed in lines 133–135). The sample-level secondary update for severely imbalanced samples is a sensible complementary mechanism.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical contribution is substantially overclaimed.** Section 3.1 (line 59) claims to "establish a unified theoretical framework and provide a proof" of similarity between class and modality imbalance. What is delivered is a simplified gradient decomposition — Eqs. (2) and (3) — that draws a conceptual parallel. There is no theorem, no formal statement, and the analysis of modality imbalance assumes γ₁ ≫ γ₂ (the very condition it purports to explain) as a premise. This is a pedagogical analogy, not a proof or a new theoretical framework. The paper would be significantly stronger if it honestly reframed this as motivating intuition rather than presenting it as a claimed contribution (contribution i in Section 1).

- **No measures of variability reported.** Table 1 states "average test accuracy (%) of three random seeds" but gives no standard deviations, confidence intervals, or per-seed breakdowns. The claimed improvements range from +1.35% (CREMA-D) to +6.76% (KS). Without variance estimates, the 1.35% improvement — which could plausibly fall within one standard deviation — cannot be assessed for statistical significance. This concern is amplified because CCAT's hyperparameters (β, r) were tuned per-dataset via grid search, which can inflate apparent gains.

### Minor

- **The mutual information estimator (Eq. 5) is presented without sufficient justification.** The formula resembles a contrastive objective rather than a standard MI estimator, and its denominator (summing over modalities *l* rather than over samples) is not explained. The paper cites Zhou et al. (2025b) but provides no intuition for why this quantity equals or approximates I(zᵢᵐ; fᵢ) or what assumptions are needed. Since this estimator drives both the regularization term (Eq. 7) and the sample-level secondary update, the lack of clarity is relevant.

- **The disproportionate gain on Kinetic-Sound (+6.76% absolute) is not explained.** This is roughly 3–5× larger than the gains on the other two datasets (+1.35%, +1.92%). The paper offers no discussion of why KS benefits so much more, leaving questions about whether the method's effectiveness is consistent or dataset-dependent in ways that are not understood.

- **The ablation does not include the most directly informative baseline.** Training the classifier from scratch (random initialization) under alternating training, then freezing it, would isolate whether the improvement comes from the pretraining stage, the freezing strategy, or both. The current ablation (Row 1 of Table 2) removes the freezing but keeps the pretrained initialization, conflating these effects.

- **No limitations section or discussion of failure modes.** The paper does not discuss when CCAT might not help — e.g., when both modalities are equally weak, or how the framework extends to scenarios beyond the two-modality scope tested.

### Trivial
- LFM results on MVSA are shown as "-" with no explanation.

## Nice-to-Haves
- **Causal test of classifier bias:** Freeze MLA's classifier at epoch 1 (before bias develops) and compare to unfrozen MLA. This directly tests whether classifier bias is the bottleneck claimed.
- **Pretraining vs. freezing isolation:** Compare (a) frozen pretrained classifier, (b) frozen randomly initialized classifier, (c) unfrozen pretrained classifier to disentangle these effects.
- **Justify or reframe the MI estimator:** Either derive why Eq. 5 estimates mutual information, or reframe it as a heuristic contribution score.
- **Analyze β sensitivity:** The optimal β varies from 0.05 (MVSA) to 0.30 (KS) — a 6× range. Discuss what dataset properties drive this and how to set β in practice.
- **Report computational cost:** The additional pretraining stage, secondary updates, and LoRA modules add overhead; a comparison with baselines in training time or FLOPs would be informative.

## Removed Points
The following criticisms from the original reviews were removed after cross-verification with the paper:
- Claim that Eq. 2 "conflates sample frequency with gradient signal" — the paper explicitly cites frequency as the cause and then analyzes the consequence; the criticism misreads the logical flow.
- Speculation that MLA's high video accuracy on CREMA-D (68.01) implies mild imbalance — not supported by evidence, and the paper's contribution analysis is about relative dynamics, not absolute performance.
- Demand to explore alternative regularization forms (KL divergence, hinge penalties) — scope creep beyond what the paper claims.
- Concern about "cyclic dependency" in the secondary update causing instability — speculative; Algorithm 1 follows a standard two-phase update pattern with no evidence of instability.
- Formatting/style observations — parser artifacts, not author errors.

## Novel Insights
The most striking finding from the merged review is the gap between what the paper claims (a "theoretical framework" and "proof") and what Section 3.1 actually delivers (a useful but elementary gradient analogy). This misalignment is the paper's most significant self-inflicted weakness — the method itself is coherent and the results are promising, but the theoretical section oversells itself in a way that undermines trust. A second notable observation is that the KS gain (+6.76%) is so far outside the range of the other two datasets (+1.35%, +1.92%) that absence of discussion is a real omission — it suggests the method may interact strongly with specific dataset properties that are neither identified nor controlled.

## Suggestions
- Reframe Section 3.1 explicitly as motivating intuition / a conceptual analogy, not a "proof" or "theoretical framework." This honest reframing removes the central mismatch between claim and delivery.
- Add per-seed results or standard deviations to Table 1. Three seeds with individual values is the minimum for assessing whether the 1.35% CREMA-D gain is reliable.
- Add a brief paragraph discussing why KS benefits disproportionately, even if speculative (e.g., dataset-specific imbalance patterns, baseline floor effects).
- Add a limitations paragraph covering scope (two-modality only, β sensitivity, conditions where CCAT may not help).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>