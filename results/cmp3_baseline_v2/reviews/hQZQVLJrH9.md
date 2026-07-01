## Summary

This paper proposes a unified first-order framework bridging activation steering and influence functions. It proves that, to first order, any steering vector can be mapped to an influence weighting over training data and vice versa, subject to a geometric alignment condition measured by the smallest principal angle between Jacobian subspaces. The theory yields a constructive algorithm (Influence-Aligned Steering, IAS), a spectral recipe for optimal low-norm steering directions, and generalization bounds for low-rank interventions. Experiments on GPT-2 detoxification and ResNet-50 image classification provide partial empirical support.

## Strengths

- **Novel theoretical connection** – The paper is the first to formally link activation steering and influence functions through a primal-dual optimization lens, adding clarity to two previously separate research strands.
- **Geometric diagnostic (γ)** – The principal-angle cosine γ(x) provides a simple, interpretable pre-check that tells practitioners when steering can faithfully mimic influence, and when it cannot.
- **Clean mathematical formulation** – The problem is reduced to linear algebra of Jacobian subspaces, making the core ideas transparent and the proofs straightforward.
- **Practical cost profile** – All key quantities (IAS vector, diagnostic γ) are computable with two Jacobian-vector products and a small SVD, which is genuinely feasible for moderately sized layers.

## Weaknesses

### Major

1. **Overclaiming in abstract and Theorem 4.2** – The abstract states "any steering vector can be represented as an influence weighting over training data and vice versa" without caveats. Theorem 4.2 claims the converse mapping always exists (‖s_w‖ = O(ε)), but the subsequent text admits a nonzero residual when subspaces do not match. The main theorem statement is thus misleading; the "vice versa" part holds only approximately, and the approximation error depends on γ(x) in a nontrivial way. This weakens the core claim.

2. **Corollary 1 proof is flawed** – The proof sketch for ℓ₁-minimality of ρ𝐬 is unsound: scaling down ρ𝐬 would proportionally reduce the logit shift, so it cannot be used to contradict minimality of the original α. A correct proof must rely on the norm of the dual variable or the KKT conditions of the primal program, which is not provided. This calls into question the claimed practical payoff of identifying "fewest training examples."

3. **Limitations of first-order approximation not validated** – The paper restricts to the small-edit regime but never measures how small α must be for the approximation to hold. The experiment in Figure 1 shows high cosine (0.978) but a slope of 1.5 (not 1), indicating a systematic first-order bias, which is never discussed. Without a calibration or error bound on real tasks, the practical value of the equivalence is unclear.

4. **Missing key experimental validation** – The most practically interesting claim is that a steering vector can be mapped back to causal training examples. The paper provides no experiment demonstrating this: no example of tracing a steering direction to specific toxic/neutral documents, no human evaluation of the identified training examples, and no comparison with existing data attribution methods. The language-model detoxification experiments only compare IAS with CAA on aggregate metrics, not on the data-map**ing capability.

### Minor

- The generalization bound (Theorem 6.1) assumes the loss is L-Lipschitz in its first argument; cross-entropy loss does not satisfy this globally. The bound is therefore not directly applicable to standard language modeling losses.
- The spectral direction (Theorem 5.3) requires averaging over the Hessian inverse, which is notoriously unstable for deep networks. The paper references damping but provides no sensitivity analysis.
- Experiments are limited to GPT-2 Medium (355M) and ResNet‑50; the theory should scale to larger models but no evidence is given. The detoxification results show IAS performing between baseline and CAA, not clearly better.

## Nice-to-Haves

- A demonstration of the steering-to-data mapping on a concrete example (e.g., bias in an LLM) would greatly strengthen the paper.
- An ablation studying how the quality of the first-order approximation degrades with steering magnitude α, including a practical guideline for choosing α.
- Comparison with alternative data attribution baselines (e.g., TracIn, Grad‑Dot) when mapping back to training examples.

## Novel Insights

None beyond the paper’s own contributions. The geometric characterization via principal angles is the most novel theoretical element, but the rest largely follows from standard linear algebra (projections, pseudo-inverses, Rayleigh quotients) applied to Jacobians. The idea that steering and influence are first-order equivalent in the aligned regime is clean but not surprising given both are linear approximations.

## Suggestions

- Correct the abstract and Theorem 4.2 to clearly state the residual caveat. Define γ(x) upfront and only claim exact equivalence when γ(x) = 1.
- Provide a rigorous proof for Corollary 1 or lower the claim to a heuristic.
- Calibrate the first-order linearity by reporting the residual norm (not just cosine) for various α. Show that when α is typical in steering practice, the bound still holds.
- Include a concrete example of tracing a steering vector to training examples, even as a toy case, to substantiate the main practical workflow.

## Score and Decision

The paper presents a clean theoretical connection but suffers from overclaiming, a flawed proof in a central corollary, and insufficient experimental validation of its most advertised benefit. The contributions are modest and not fully substantiated.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>