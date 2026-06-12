## Summary

This paper establishes a first-order equivalence between activation steering and influence functions in neural networks. The authors prove that any steering vector can be represented as an influence weighting over training data and vice versa, providing an "Influence-Aligned Steering (IAS)" framework. Key contributions include: a closed-form duality mapping, an alignment diagnostic γ that characterizes when perfect equivalence is possible, a spectral optimality result for choosing steering directions under norm budgets, and generalization bounds for low-rank steering interventions. The paper bridges two previously disconnected lines of interpretability research.

## Strengths

- **Theoretical unification of two important areas**: The paper provides a clean, rigorous mathematical connection between activation steering and influence functions—two popular but previously disparate techniques in interpretability and model control. This is a genuinely novel contribution that adds theoretical clarity to both fields.

- **Practical diagnostic tool (γ)**: The alignment cosine γ offers a simple, computationally cheap scalar that tells practitioners when steering can succeed (γ close to 1) versus when weight-space editing is necessary (γ small). Computing γ requires only two JVP/VJPs, making it scalable to large models.

- **Constructive recipes**: The IAS construction, spectral steering direction via power iteration, and the mapping from steering vectors back to training examples are all explicit and implementable. The paper provides concrete algorithms that practitioners can apply.

- **Experimental verification of first-order equivalence**: Figure 1 shows a cosine of 0.978 between predicted and actual logit shifts on GPT-2 Medium, convincingly demonstrating that the linear approximation holds in the small-edit regime.

## Weaknesses

### Major

1. **Thin experimental section**: The empirical evaluation is limited to one small experiment (GPT-2 Medium detoxification), one scatter plot, one layer-depth ablation, and one ResNet-50 spectral direction significance test. The paper claims a "practical workflow" but only demonstrates a tiny fraction of it. There are no experiments showing:
   - The mapping from a steering vector back to causal training examples (the headline claim of item 1 in the introduction)
   - The γ diagnostic being used to decide between steering and parameter-space editing in practice
   - Comparison against baselines beyond CAA
   - Scaling to larger models (e.g., GPT-2 XL, LLaMA)
   - Any ablation on the damping parameter λ
   
   For a paper with "practical workflow" as a claimed contribution, the empirical support is notably sparse.

2. **Overclaiming without sufficient evidence**: The abstract and introduction claim the framework "scales to billion-parameter models" and enables a workflow where practitioners can "(i) prototype with steering, (ii) identify the responsible training examples, and (iii) decide—with γ—whether weight-level editing is necessary." However, neither scaling results nor any demonstration of steps (ii) and (iii) are actually provided. The experiments only validate the first-order linearity and show γ increasing with layer depth.

3. **Missing practical details for influence function computation**: The paper assumes access to the empirical Hessian H_θ and its inverse, which is well-known to be problematic for large neural networks (as documented by Basu et al., 2021, cited by the authors). The damping regularizer λ is mentioned but not evaluated. Given that influence functions are known to be fragile in deep learning, the paper should address when the proposed equivalence breaks down due to Hessian approximation errors.

### Minor

- **Table 1 shows IAS underperforms CAA** on the detoxification task (higher toxicity, higher perplexity). The paper does not discuss why this happens despite the theoretical optimality claims.

- **The Rademacher complexity result (Theorem 6.1)** is labeled a "blow-up" but the actual bound shows only an αL√(2k/dn) increase, which vanishes as d and n grow. The term "blow-up" is misleading for what is actually a benign bound.

- **Layer composability lemma**: Lemma 5.4 gives a simple multiplicative bound (γ₁₂ ≥ γ₁γ₂), but the statement looks circular and its practical relevance is unclear without showing how to implement multi-layer IAS.

### Trivial

- The slope of 1.50 in Figure 1 (vs. identity line y=x) indicates a systematic scaling mismatch, which the paper does not explain. If the theory predicts exact first-order matching, why does the empirical fit have slope 1.5?

## Nice-to-Haves

- Ablation on α (steering magnitude) to show when the linear approximation breaks down
- Experiments on a model larger than GPT-2 Medium (e.g., GPT-2 XL, LLaMA-7B) to support the billion-parameter claim
- A concrete example of the mapping from a steering vector back to specific training examples (Corollary 1)
- Comparison of γ diagnostic against actual steering success across multiple models/layers

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Add the missing workflow experiments**: Demonstrate at least one end-to-end example where a steering vector is constructed, γ is computed, and the top-5 causal training examples are identified. This is the paper's central practical claim and should be validated.

- **Acknowledge limitations of influence functions**: Add a discussion of when influence function approximations are reliable (or not), and how this affects the practical utility of the equivalence. The paper currently treats H_θ as if computing its inverse is straightforward.

- **Explain the slope discrepancy in Figure 1**: The 1.5x slope between predicted and actual shifts needs explanation—is it due to second-order effects, damping, or something else?

- **Scale up experiments**: Show results on at least one model with >1B parameters, or qualify the claims about scaling.

## Score and Decision

The paper presents a genuinely novel and theoretically clean unification of two important areas. The core mathematical contribution is strong and will likely be of interest to the interpretability community. However, the experimental validation is far too thin for the ambitious claims made about practical workflows and scaling. The paper reads more like a theoretical contribution with insufficient empirical support. Given ICLR's standards for both theory and experiments, the paper cannot be accepted in its current form.

**Score**: 4 (borderline reject)

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: Reject