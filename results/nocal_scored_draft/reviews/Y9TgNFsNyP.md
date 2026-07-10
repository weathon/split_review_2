Now let me finalize the review with the score.

## Summary

This paper introduces FF-Erase, the first machine unlearning method for Forward-Forward (FF) models, along with G-MIA, a goodness-based membership inference attack for verification. The method uses a guidance model (ignorant of forgetting data) to provide stable target goodness distributions, shifting the original model's per-layer goodness toward them via KL-divergence — a distillation-like strategy that prevents the layer-wise divergence and model collapse that occur when naive gradient ascent is applied to FF models. Experiments on CIFAR-10/100, MNIST, and Fashion-MNIST with multiple FF architectures show that FF-Erase achieves 1.9–3.1× speedup over retraining with minor accuracy degradation.

## Strengths

- **Identifies a genuinely new problem.** The paper is the first to formalize machine unlearning for FF models, identifying the specific failure modes (sensitivity to parameter tuning, inconsistent update directions across independently-trained layers) that cause standard gradient-based unlearning methods to collapse. The problem framing in Section 1 and Figure 1 is clear and grounded in FF mechanics.

- **Core methodological idea is well-motivated.** Using a guidance model to provide stable target goodness distributions that the original model shifts toward via KL-divergence directly addresses the divergence issue. The ablation study (Table 1, R.G.M row) confirms that guidance quality is essential: a random guidance model collapses test accuracy to 55.53%. This is not just an incremental adaptation — it is structurally necessary for the FF setting.

- **Concrete efficiency gains.** The 1.9–3.1× speedup over retraining is verified with time-vs-accuracy curves (Figure 4a-b) and supported by the efficiency analysis in Equation (9). The speedups are meaningful and plausibly scale with model size.

- **G-MIA adapts MIA to FF architecture.** G-MIA leverages per-layer goodness vectors — a natural output of FF models — and consistently outperforms standard black-box final-layer MIA (FL) across all tested architectures (Figure 3), sometimes matching white-box attacks on deeper models. This is a concrete empirical finding with practical value for FF unlearning verification.

## Weaknesses

### Major

1. **Insufficient empirical support for the claim that prior methods are infeasible.** The paper asserts that "existing machine unlearning methods are not feasible for FF models" (Section 1) and discusses multiple families — gradient ascent, influence functions, Hessian-based estimation, and teacher-based approaches (Chundawat et al. 2023a "bad teaching") — yet the experiments compare FF-Erase against only one representative (gradient ascent) plus retraining. No attempt is made to adapt any other approach (e.g., the "incompetent teacher" method, which is conceptually adjacent to the guidance-model idea) to the FF setting. This leaves the paper's central motivating claim under-supported by direct evidence.

2. **No statistical variance or significance for any result.** All numbers in Table 1, Figure 3, Figure 4, and Figure 5 are single values with no standard deviations, confidence intervals, or mention of the number of random seeds or trials. Several comparisons hinge on small differences (e.g., G-MIA ACC of 0.568 vs. 0.571 between D-(0.3,0.5) and D-(0.3,0.2) in Table 1; Acc_f of 81.58 vs. 81.61 between D-(0.5,0.5) and RE) that cannot be assessed for statistical reliability. This is a significant evidential gap for a paper making quantitative comparisons.

3. **Evaluation alignment between method and metric.** Both FF-Erase (which shifts goodness distributions toward a non-member guidance model) and G-MIA (which classifies membership based on goodness vectors) operate on the same signal. This alignment could inflate apparent unlearning effectiveness, as FF-Erase explicitly manipulates the very signal G-MIA measures. The paper does report Acc_f (prediction accuracy on the forget set) as an independent signal, which partially mitigates this concern — and Acc_f values are indeed reasonable (81.31% for FF-Erase(D) vs. 81.61% for retraining). However, the effectiveness claims in Section 6.2 and the ablation study in Table 1 anchor primarily to G-MIA scores. An independent verification method operating on a fundamentally different signal would substantially strengthen the evaluation.

### Minor

4. **G-MIA black-box framing.** G-MIA is called a "black-box" attack throughout the paper, but it requires per-layer goodness vectors from all layers — not just the model's final prediction. The paper's own Section 2 defines black-box MIAs as using "only the model's final prediction output," creating an internal inconsistency. Since FF models natively output these vectors for inference, this is a practical and reasonable access assumption, but the terminology should be clarified.

5. **Potential information leakage in fast-distilled guidance model.** The fast-distilled strategy (Section 4.2) uses the original model (trained on all data including forgetting data) as teacher to train the guidance model on remaining data. The paper does not discuss whether shared representations from the original model could leak forgetting-data information into the guidance model, which would partially undermine the guidance model's role as a forgetting-data-agnostic anchor.

### Trivial

None.

## Nice-to-Haves

- An ablation study on the recovery frequency hyperparameter K.
- Discussion of how G-MIA scales with model depth (feature dimensionality grows with the number of layers).
- Sensitivity analysis for different forget-set sizes (the experiments use β=0.2 uniformly).

## Removed Points

The following points from the input review were removed per filtering guidelines:

- **"Only one model-dataset combination in main text"** — The paper explicitly states that other results are in the appendix (which was stripped by the parser). This is a formatting constraint, not an evidential gap.
- **"GA baseline uses λ=10 only... should show other values"** — Already addressed in Section 6.3/Figure 5, which tests six different λ values.
- **"Synthetic data assumption is non-trivial"** — A standard assumption in the MIA literature (Shokri et al. 2017); singling it out as a weakness without FF-specific evidence is not justified.
- **"FF-Erase(D) achieves lower G-MIA than retraining... should be discussed"** — Too fine-grained for a review summary; the absence of discussion is not a weakness.
- Various generic or speculative concerns from the input that lacked specific paper anchors were removed in accordance with filtering discipline.

## Novel Insights

None beyond the paper's own contributions. The merger of the two reviews surfaces a tension that is informative: the paper's core contribution is genuinely novel and the method is structurally well-motivated, but the evaluation is thinner than the boldness of the claims warrants. The harsh critic's concern about evaluation alignment (method and metric sharing the same signal) and the missing-baseline gap reveal that the paper's empirical case does not fully match the scope of its narrative.

## Suggestions

1. **Add variance estimates.** Run all main experiments with at least 3 random seeds and report mean ± std/CI. This is essential for assessing the small numerical differences that underpin several experimental comparisons.

2. **Include at least one adapted alternative baseline.** Adapting the "incompetent teacher" approach (Chundawat et al. 2023a) to the FF setting — e.g., using a randomly initialized model as the teacher for forgetting data — would directly test whether the guidance model is necessary or whether any distillation-like loss suffices. Even demonstrating that this simpler baseline fails would strengthen the paper's core claim.

3. **Use an independent verification signal.** Evaluating FF-Erase with a verification method that does not rely on goodness vectors (e.g., a prediction-only MIA, or measuring the accuracy gap between forget and test sets) would break the conceptual alignment between method and metric and provide more compelling evidence.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>