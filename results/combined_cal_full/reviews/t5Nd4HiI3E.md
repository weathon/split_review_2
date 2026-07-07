Now let me write the final consolidated review.

## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs), where the statistically correct marginal objective over reasoning traces is intractable, and the common single-trace proxy suffers from high gradient variance. The authors propose **BVPO**, which forms a convex combination of a high-variance trace-based gradient and a low-variance "empty-trace" gradient (obtained by disabling reasoning trace generation). Theoretically, the paper proves variance reduction, derives an MSE-optimal mixing coefficient, and connects these results to SGD convergence bounds. Empirically, BVPO shows consistent gains over DPO and SimPO across three LRM sizes (1.5B, 7B, 8B) on Arena-Hard, AlpacaEval 2, and six math reasoning benchmarks.

## Strengths

1. **Well-motivated problem (Section 3.2).** The paper identifies a genuine and underexplored issue: aligning LRMs via preference optimization introduces high gradient variance because the correct marginal objective over reasoning traces is intractable and the single-trace proxy fluctuates dramatically. This frames an important bottleneck that prior DPO-based alignment work has not addressed.

2. **Simple and intuitive method (Section 3.3).** BVPO's core idea — mixing a high-variance trace-based gradient with a low-variance empty-trace gradient via convex combination — is conceptually clean, computationally lightweight (no extra model, no additional sampling beyond two forward passes), and directly targets trace-induced variance rather than relying on generic regularization or data augmentation.

3. **Consistent empirical gains across multiple models and benchmarks (Tables 1, 2).** BVPO improves over DPO and SimPO on essentially every metric and mode (Thinking/NoThinking) for all three model sizes (1.5B, 7B, 8B). The gains on Arena-Hard and AlpacaEval 2 (up to ~7-8 points) are non-trivial. The finding that alignment on general conversational data improves math reasoning (up to +4.0 average points) is noteworthy and suggests the method stabilizes training beyond mere variance reduction.

4. **Rigorous theoretical framing (Section 4).** The bias-variance decomposition, MSE-optimal convex combination (Theorem 2, Corollary 1), and the connection to SGD convergence bounds (Theorems 3, 4) provide a principled language for what the method aims to do. The theoretical results are correctly stated and the reasoning is sound.

## Weaknesses

### Fatal
None.

### Major

1. **Missing α=0 baseline (empty-trace-only training).** The paper compares BVPO (0<α<1) against DPO and SimPO (effectively α=1), but does not report results for a model trained solely with the empty-trace loss L_e. Without this comparison, the claim that the *combination* dominates either component alone (Corollary 1) is not empirically validated. The observed gains could come primarily from the L_e component, and the reader cannot assess whether the mixing mechanism is the source of improvement. This is the most direct experiment the paper owes to support its central claim.

2. **No variance or uncertainty estimates despite the paper's thesis being about variance reduction.** Tables 1 and 2 report only point estimates with no standard deviations, confidence intervals, or multiple seeds. When a paper claims to reduce gradient variance and improve training stability, the absence of any reported variance measure in the experimental results is a significant omission. The reported gains (3–7 points) could be within the noise range of these benchmarks, and without uncertainty estimates the statistical reliability cannot be assessed.

3. **The mixing weight α is not reported in the main experimental section (Section 5.1).** The paper does not state what value of α was used, how it was chosen (grid search, estimated from data via Theorem 2's closed-form, or fixed ad-hoc), or whether it varied per model. No ablation or sensitivity analysis over α is visible in the main text. Given that the paper's framing promises "optimal" mixing, this is a critical gap in empirical reporting. (Note: if these details appear in the appendix — which was stripped by the parser — the authors should move them to the main text.)

### Minor

4. **Theoretical gaps between optimality guarantees and practical implementation.** (a) Theorem 2's optimal α* requires population moments of g_t and g_e; the paper does not state whether these are estimated during training or if α is simply tuned as a hyperparameter. (b) Theorem 4 requires ηL=1, but the paper does not discuss whether this condition approximately holds in the actual training setup (learning rates for LLM fine-tuning are typically far from the inverse Lipschitz constant). (c) The bias b_e of the empty-trace estimator could be large — the paper acknowledges the bias-variance trade-off but provides no analysis or bound on the magnitude of b_e.

5. **Empty-trace implementation is asserted but not verified.** The paper states that appending `