## Summary

This paper investigates the relationship between adaptive optimizers (Adam, AdaGrad, Shampoo) and normalized steepest descent (NSD) methods (SignGD, Muon) through the lens of smoothness. It shows that adaptive optimizers are governed by a stronger "adaptive smoothness" notion, while NSD relies on standard smoothness under the induced norm. The paper extends the theory of adaptive smoothness to the nonconvex setting, proves that adaptive smoothness enables accelerated \(O(T^{-2})\) rates for adaptive optimizers with Nesterov momentum in convex settings, and introduces "adaptive variance" as an analogue to adaptive smoothness for stochastic noise, showing it enables dimension-free convergence rates for NSD that are impossible under standard variance assumptions.

## Strengths

- **Theoretical unification**: The paper provides a unified analysis covering a broad class of adaptive optimizers (AdaGrad, Adam, Shampoo) with general well-structured preconditioner sets, extending previous convex analyses to the nonconvex setting. The convergence rates depend cleanly on the adaptive smoothness \(\Lambda_{\mathcal{H}}(f)\), clarifying how these methods exploit geometry.

- **Novel benefit of adaptive smoothness**: The paper demonstrates that adaptive smoothness enables accelerated \(O(T^{-2})\) rates for adaptive optimizers with Nesterov momentum in convex settings, while standard smoothness under the same geometry cannot achieve better than \(\Omega(T^{-1})\) (citing Guzmán & Nemirovski). This is a clear, non-trivial advantage of the stronger assumption.

- **Introduction of adaptive variance**: The concept of adaptive variance parallels adaptive smoothness in the stochastic noise context. The paper proves that under adaptive variance, NSD achieves dimension-free convergence rates, and provides a matching lower bound under standard variance showing that dimension dependence is unavoidable. This reveals a fundamental gap.

- **Technical contribution**: Lemma 3.3 (novel matrix inequality bounding sums of preconditioned gradient norms) is a technically deep result that enables the extension to arbitrary well-structured preconditioner sets beyond the diagonal case. The handling of noncommutativity is a significant step forward.

- **Clear exposition**: The paper is well-structured, uses concrete examples (Adam/SignGD, \(\ell_\infty\) geometry) to motivate abstract concepts, and clearly positions its contributions relative to existing work.

## Weaknesses

### Fatal

None.

### Major

- **Acceleration result relies on bounded domain assumption**: Theorem 4.3 assumes \(\max_t \|\mathbf{x}_t - \mathbf{x}^*\|_{\mathcal{H}} \leq D\), which requires either prior knowledge of \(D\) or a projected variant (discussed later in the appendix). While the projected variant (Theorem E.5) removes this requirement, the main presentation still carries this limitation. This is a common assumption in convex optimization, but it slightly reduces the impact of the acceleration claim.

- **Lack of experiments**: As a pure theory paper, this is acceptable. However, experiments illustrating the practical implications of the theoretical benefits (e.g., showing the acceleration in practice, or the dimension-free behavior under adaptive noise) would strengthen the paper's claims and broaden its appeal.

### Minor

- **Adaptive variance assumption may be strong**: Definition 4.1 takes a min over \(H \in \mathcal{H}\), meaning the noise is uniformly controlled over the geometry prescribed by each preconditioner. While the paper argues it is weaker than bounded covariance, it is still a more restrictive assumption than standard variance. The paper does not discuss when such an assumption holds in practice for neural network training.

- **The lower bound (Theorem 4.7) is specific to \(\ell_\infty\) norm**: The paper shows that for SignGD, standard variance leads to dimension-dependent lower bound. This convincingly demonstrates the gap for that specific geometry, but it is not a general statement for all well-structured preconditioner sets. A more general lower bound would further strengthen the claim.

- **Some constants and logarithmic factors are not optimized**: The convergence rates contain unspecified constants and \(\tilde{O}\) hiding logarithmic factors. This is typical for such analyses, but it makes precise comparison with lower bounds less straightforward.

### Trivial

- The paper could include a summary table of the key assumptions, rates, and comparisons between adaptive methods and NSD for quick reference.

## Nice-to-Haves

- An empirical validation on a simple problem (e.g., a quadratic with \(\ell_\infty\) smoothness or a small neural network) to illustrate the predicted acceleration and dimension-free behavior would be a valuable addition but is not required for the theoretical contribution.

- A discussion of how adaptive smoothness and adaptive variance relate to empirical observations in deep learning (e.g., why Adam works well with large batch sizes or why SignGD works on certain tasks) would increase the paper's impact.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the strength of an assumption (adaptive smoothness vs. standard smoothness) can paradoxically translate into algorithmic benefit. The paper shows that adaptive smoothness, despite being a stronger condition, enables accelerated convergence because it allows the algorithm to exploit the structure of the preconditioner set more finely. Similarly, adaptive variance, though stronger, removes dimension dependence that otherwise plagues non-Euclidean methods. This insight—that "stronger assumptions can lead to faster rates"—is not new in optimization (e.g., strong convexity), but the paper's demonstration in the context of non-Euclidean geometry and adaptivity is novel and thought-provoking. The duality between the supremum of primal norms and the infimum of dual norms (Lemma 2.2) elegantly explains how adaptive methods automatically select the best geometry.

## Suggestions

- Consider adding a brief empirical illustration in a simple setting (e.g., a quadratic with \(\ell_\infty\) smoothness) to demonstrate the predicted acceleration and dimension-free behavior. This would help bridge theory and practice.
- Clarify the relationship between adaptive variance and the bounded covariance assumption more explicitly in the main text, perhaps with a concrete example showing when adaptive variance holds but bounded covariance does not.
- The projected variant of the accelerated algorithm (Algorithm 8) could be moved to the main text to remove the bounded domain assumption from Theorem 4.3.

## Score and Decision

This is a strong theoretical paper with clear contributions: extending adaptive smoothness theory to nonconvex settings, identifying the acceleration benefit of adaptive smoothness, and introducing adaptive variance to achieve dimension-free rates. The paper is well-written, technically sound, and addresses an important question about the foundations of adaptive optimization. The weaknesses are minor relative to the contributions. I recommend acceptance.

**MY FINAL SCORE:** <score>8</score>
**MY FINAL DECISION:** <decision>Accept</decision>