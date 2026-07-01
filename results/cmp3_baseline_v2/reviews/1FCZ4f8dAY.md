## Summary

This paper develops a general theoretical framework for constructing equivariant machine learning models that map tensors to tensors, with respect to the diagonal action of classical Lie groups (orthogonal O(d), indefinite orthogonal O(s,d-s) including Lorentz, and symplectic Sp(d)). The authors provide explicit parametric characterizations of equivariant polynomial and analytic tensor functions using invariant theory, showing that all such functions can be built from tensor products of inputs contracted with group-isotropic tensors (constructed from Kronecker deltas, Levi-Civita symbols, or their group-specific analogues). They validate their approach on three diverse applications: stress-strain tensor prediction in materials science, path signature estimation for time series, and sparse vector estimation, achieving superior performance over non-equivariant baselines in all cases.

## Strengths

- **Theoretical generality and rigor**: The paper provides a unified, mathematically rigorous characterization of equivariant tensor functions for three distinct symmetry groups (orthogonal, Lorentz, symplectic) at arbitrary tensor orders, generalizing prior work that was limited to specific groups (e.g., SO(d)/O(d) in low dimensions) or specific input types. The derivations of Theorems 1 and 2 and Corollaries 1-3 are clear and grounded in established invariant theory.

- **Practical computational recipes via corollaries**: The authors translate the general (potentially intractable) theoretical characterization into practical, implementable forms (Corollaries 1-3) for the important special case where inputs are vectors (1-tensors). This bridges the gap between abstract theory and usable ML architectures.

- **Strong and consistent experimental validation**: Across three distinct and challenging problems (hyperelastic material modeling, path signature learning, sparse vector recovery), the equivariant models consistently outperform non-equivariant MLP baselines (both standard width, matched parameter count, and data-augmented). The improvements are often dramatic (e.g., orders of magnitude in the stress-strain problem, Table 1). The sparse vector experiments are particularly compelling, demonstrating that learned equivariant models can outperform theoretically-guaranteed SoS methods when the SoS assumptions are violated.

- **Novel combination with path signatures**: Applying equivariant tensor learning to path signature estimation is elegant and well-motivated. The path signature's tensors naturally inherit O(d)-equivariance, making the approach a principled combination of two powerful structures.

## Weaknesses

### Major

- **Computational cost of the general parametrization**: The complexity of the full equivariant model is acknowledged as O(k'! n^{k'} (Q d n^2 + d^{k'})) which is only practical for very small output tensor ranks (k' ≤ 4). While the authors note this and the experiments use small output ranks, the paper does not provide a detailed comparison of computational cost (FLOPs, memory, runtime) with baseline methods for the experiments conducted. Understanding the practical trade-off between improved accuracy and increased cost is important.

- **Limited theoretical analysis of generalization**: The paper convincingly shows empirical gains from equivariance but provides no theoretical analysis of sample complexity or error bounds for the proposed architectures. Given the strong literature on generalization benefits of equivariance (cited by the authors: Elesedy, Bietti et al., Tahmasebi & Jegelka, Huang et al.), some analysis—even for a simplified setting—would substantially strengthen the contribution.

- **Missing analysis on the expressivity of the scalar-function parameterization**: In Corollaries 1 and 3, the functions q are learned MLPs that take inner products as input. While the paper claims this can represent all continuous equivariant functions via Stone-Weierstrass (Remark 1), the actual expressive power of this specific parametrization (MLPs on pairwise inner products) for the full equivariant function class is not formally examined. For instance, can every O(d)-equivariant polynomial be represented with this specific structure regardless of the MLP capacity? The connection between the polynomial degree and the needed width/depth is not discussed.

### Minor

- **The symplectic group is mentioned but not experimentally validated**: The theory covers Sp(d), but the experiments only address O(d) and Lorentz groups. Demonstrating the method on a symplectic-equivariant problem would strengthen the claim of generality, though the authors acknowledge this is left for future work.

- **Limited discussion of failure modes**: The sparse vector problem shows that the "Ours (Diag)" variant sometimes outperforms "Ours" (e.g., under Diagonal covariance), and vice versa. This discrepancy is not analyzed or explained. Understanding when the full pairwise inner product parametrization is beneficial versus harmful would be insightful.

### Trivial

- Figure 1 caption is extremely long and contains part of the description that is essentially a repeat of the main text. It could be shortened.

## Nice-to-Haves

- Provide runtime and memory benchmarks comparing the proposed method against the baselines to give practitioners a clear picture of the computational overhead.
- Include an ablation on the complexity of the shared MLP function q (e.g., varying depth/width) to examine the trade-off between capacity and overfitting.
- Add a brief discussion or experiment on how the method scales with the number of input vectors n, especially for the path signature problem.

## Novel Insights

The paper's central insight—that intertwining invariant theory with ML architecture design yields universal, group-agnostic equivariant tensor functions—is elegantly demonstrated. Beyond the paper's own contributions, the results on the sparse vector problem offer a particularly nuanced perspective: when theoretical guarantees (SoS) exist and their assumptions hold, they can outperform learned models; but the equivariant learning approach provides robust performance precisely where those assumptions break down (e.g., non-isotropic noise, correlated sampling). This suggests that equivariant learning may serve as a practical "bridge" between theory-rich settings (where strong guarantees exist but are brittle) and messy real-world data (where guarantees fail but structure can still be leveraged). The path signature application further highlights how differential geometric objects (path signatures) naturally interface with algebraic symmetry constraints, opening the possibility for principled neural architecture design in rough path theory and stochastic analysis.

## Suggestions

- Consider adding a computational complexity table (FLOPs/runtime) for the experiments to help readers assess the practical cost of the equivariant model.
- Provide a theoretical or experimental analysis on how the expressivity of the learned q functions (MLPs on inner products) relates to the polynomial degree of the overall equivariant function.
- Add a commentary or brief experiment explaining the performance variation between "Ours" and "Ours (Diag)" in the sparse vector experiments under different covariance structures.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>