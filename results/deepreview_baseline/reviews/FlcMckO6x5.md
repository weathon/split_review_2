## Summary

This paper provides a comprehensive theoretical analysis of Separable Neural Networks (SepNNs), establishing three key contributions: (1) a universal approximation theorem proving SepNNs can approximate any continuous multivariate function with arbitrary precision using CP, TT, or Tucker decompositions; (2) characterization of SepNN training dynamics via Neural Tangent Kernel (NTK) analysis, showing convergence to deterministic or random kernels under different asymptotic regimes; and (3) a computationally efficient Separable Preconditioned Gradient Descent (SepPGD) method that provably alleviates spectral bias with O(nD) complexity for n^D training samples. The theoretical findings are validated through experiments on kernel ridge regression, implicit neural representations, and physics-informed neural networks.

## Strengths

- **Novel theoretical contributions**: The universal approximation theorem for multivariate SepNNs (D ≥ 2) with CP, TT, and Tucker decompositions fills a significant gap in the literature, extending prior work that only covered the bivariate case. The proof technique combining Stone-Weierstrass with universal approximation is elegant and unified across decomposition types.

- **Rigorous NTK analysis**: The paper provides a thorough characterization of SepNN training dynamics, including both deterministic NTK (infinite width and rank) and random NTK (infinite width, fixed rank) regimes. Lemma 1 deriving the NTK structure for CP SepNN is a valuable technical contribution.

- **Computationally efficient preconditioning**: The SepPGD method achieves O(nD) complexity compared to O(n^D) for standard NTK-based preconditioning, representing an exponential improvement in dimensionality. The connection to Kronecker product structure (Lemma 2) provides theoretical grounding for the efficiency gain.

- **Strong empirical validation**: Experiments across multiple domains (KRR, image/surface representation, PINNs) consistently demonstrate SepPGD's effectiveness in accelerating convergence and improving solution quality, with clear visual improvements shown in Figures 3-4.

## Weaknesses

### Major

- **Limited scope of NTK analysis**: The NTK derivation and spectral bias characterization are primarily conducted for CP SepNN with two-layer MLP factor networks. While the paper claims extension to multi-layer MLPs is "straightforward," this is not demonstrated, and the analysis for TT and Tucker decompositions is deferred without concrete results. Given that TT and Tucker are explicitly included in the approximation theory, their absence from the NTK analysis weakens the paper's completeness.

- **Theoretical gap between SepPGD and spectral bias alleviation**: While Lemma 2 shows equivalence between SepPGD and classical NTK-based PGD for D=2, the paper does not provide a rigorous proof that SepPGD actually alleviates spectral bias in the multivariate case (D>2). The argument that "the eigenvalue of a Kronecker product matrix... would have better spectrum" is heuristic and lacks formal guarantees. The convergence analysis and solution consistency are explicitly left for future work.

- **Grid input assumption limits generality**: The SepPGD method and its complexity analysis heavily rely on grid-structured training data. The paper acknowledges this limitation but only briefly discusses non-grid extensions in a single paragraph. Given that many practical applications involve non-grid inputs, this significantly constrains the method's applicability.

### Minor

- **Experimental comparisons are limited**: The experiments compare SepPGD against standard gradient descent and MSK but do not include comparisons with other preconditioning methods (e.g., Adam, L-BFGS, or Hessian-free optimization) that are commonly used in PINNs and INRs. The absence of these baselines makes it difficult to assess whether SepPGD's benefits are unique or could be achieved with simpler optimizers.

- **Scalability demonstration is insufficient**: While the paper claims O(nD) complexity, the experiments use relatively small-scale problems (e.g., 2D images, 3D surfaces). No experiments demonstrate scaling to higher dimensions (D > 3) where the complexity advantage would be most pronounced.

### Trivial

- The notation in Definition 1 and Equation (8) is quite dense and could benefit from a more intuitive explanation or a concrete example for a simple case (e.g., D=2, R=1).

## Nice-to-Haves

- An ablation study showing the effect of different rank values on SepPGD performance would strengthen the practical guidance.
- A theoretical bound on the condition number improvement achieved by SepPGD would make the spectral bias alleviation claim more rigorous.
- Discussion of how SepPGD interacts with common training techniques (learning rate schedules, weight decay, batch normalization) would improve practical utility.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is the connection between separable architectures and efficient preconditioning through Kronecker product structure. The observation that the NTK of a separable network can be decomposed into smaller factor NTKs, and that preconditioning can be performed independently on each factor with exponential savings, reveals a fundamental advantage of separable architectures that extends beyond their well-known forward-pass efficiency. This suggests that separable designs may be inherently more amenable to second-order optimization methods, which could inspire new architectures specifically designed for efficient preconditioning.

## Suggestions

1. Provide NTK analysis for TT and Tucker decompositions, or at minimum, discuss the technical challenges that prevent straightforward extension.
2. Include a formal theorem or proposition establishing the convergence rate improvement of SepPGD over standard gradient descent for SepNNs.
3. Add experiments with higher-dimensional problems (D=4,5) to demonstrate the scaling advantage of O(nD) vs O(n^D).
4. Compare SepPGD against Adam optimizer in the PINN experiments, as Adam is the de facto standard for PINN training.

## Score and Decision

The paper makes solid theoretical contributions to understanding SepNNs and proposes a practically useful algorithm. However, the NTK analysis is incomplete (limited to CP decomposition and two-layer MLPs), and the theoretical justification for spectral bias alleviation via SepPGD is not fully rigorous for the multivariate case. The experimental validation, while positive, lacks comparisons with standard optimizers used in practice. These issues prevent the paper from being a strong accept but do not warrant rejection given the novelty and potential impact.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>