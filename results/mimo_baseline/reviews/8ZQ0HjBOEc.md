## Summary

This paper analyzes the behavior of the Neural Tangent Kernel (NTK) for infinitely wide, fully-connected ReLU networks as depth increases, assuming depth grows slower than width. The authors prove that the normalized NTK converges to the all-ones matrix (Theorem 2), yet the prediction expression κ_x κ^{-1} converges to a well-defined, non-trivial limit on the sphere (Theorem 3), using rough differential equation (RDE) machinery to handle the singular limit. They also provide empirical convergence rate evaluations and identify generalizable kernel properties.

## Strengths

- **Novel proof technique via rough differential equations.** The core theoretical innovation is formulating the depth evolution of the kernel prediction expression as a rough differential equation and applying Lyons' Universal Limit Theorem to establish convergence despite the kernel matrix becoming singular. This is a genuinely creative application of rough path theory to NTK analysis that bypasses the invertibility assumptions required by prior work (e.g., Xiao et al. 2020, whose ordered-phase proof fails when the limiting matrix is singular).

- **Resolution of a tension in the NTK literature.** The paper identifies and addresses the interesting phenomenon that while the normalized NTK approaches the all-ones matrix (implying vanishing determinant), the prediction function still has a well-defined limit. This fills a gap between works showing the NTK is in the "ordered phase" (Jacot et al. 2018b) and those showing the kernel becomes singular (Seleznova & Kutyniok 2022), by demonstrating that the singularity does not destroy predictability.

- **Clear identification of generalizable conditions.** Section 6 distills the essential kernel properties (positivity, eventual positive definiteness, vanishing normalized determinant) needed for the results to apply, enabling extension beyond ReLU NTKs to other kernel families (illustrated with a concrete example involving η^{(L)}).

## Weaknesses

### Fatal
None identified.

### Major

- **Limited experimental validation.** The experiments consist solely of convergence rate plots (Figure 1) on one synthetic dataset (n₀ = 128) and MNIST, with no evaluation of what the limiting prediction actually does. There is no comparison with finite-width trained networks, no demonstration that the limiting solution has any practical utility, and no evaluation of generalization performance. For a paper emphasizing practical implications (Section 6–7), the experimental evidence is too thin to assess real-world relevance. At minimum, one would want to see whether the limiting prediction produces reasonable classification accuracy or captures the structure of f*.

- **Practical significance of the depth regime is unclear.** The key assumption L ∈ o(min n_l) means depth grows much slower than width. The paper claims convergence occurs at "small depths" but Figure 1 shows behavior still changing at L = 20–30, and Theorem 2's convergence rate is logarithmic (acknowledged in Section 6). A deeper discussion of what depth-to-width ratios are realistic and whether the limiting regime is meaningfully approached in practice would substantially strengthen the paper.

- **Theorem 3 is difficult to verify from the paper alone.** The proof sketch introduces a complex interpolation (A_n^{(L+1)}(t)) between consecutive kernel matrices and applies Cramer's rule, but several key steps are asserted rather than derived — particularly the convergence of the determinant ratio to zero and the total variation bound on the driving terms. While the full proof is deferred to the appendix, the sketch in the main text should provide enough detail to understand the argument's structure; currently, the reader must take several critical steps on faith.

### Minor

- The paper's abstract and introduction position the results as relevant to understanding overparameterization, but the connection to practical training dynamics (finite width, SGD, non-zero bias) is not discussed even qualitatively.

- The claim that "the convergence for the limiting solution is experimentally fast" (Section 7) is somewhat at odds with the figures, where convergence of the prediction expression κ_x κ^{-1} is still visibly in progress at L = 20. A quantitative convergence rate analysis would be more convincing than visual inspection.

- The stereographic projection extension (mentioned at end of Section 5 and in Section 4) is stated but never formally developed or evaluated, leaving it as an assertion.

### Trivial
None worth noting.

## Nice-to-Haves

- A comparison of the limiting NTK prediction with predictions from finite-width networks trained with gradient descent, to gauge practical relevance.
- Analysis of the convergence rate of the prediction expression as a function of the determinant decay rate (the paper hypothesizes small determinants imply fast convergence but does not prove this).
- Extension to architectures with biases (β ≠ 0), which the paper explicitly excludes.

## Novel Insights

The paper's most novel insight is that the NTK's approach to a singular limit (the all-ones matrix) does not prevent the prediction expression from having a well-defined, non-trivial limit. This is established by reformulating the depth progression as a rough differential equation where the driving terms vanish, so the solution stabilizes. This reveals that singularity of the kernel and degeneracy of predictions are distinct phenomena — a subtle but important distinction for the NTK theory community. The generalization to kernels satisfying the three enumerated properties in Section 6 further broadens the impact.

## Suggestions

- Expand the experimental section to include evaluation of the limiting prediction's quality (e.g., training/test accuracy on classification tasks) and comparison with finite-width networks.
- Add a concrete numerical example showing how the limiting prediction κ_x κ^{-1} behaves for a small dataset (e.g., n = 3, n₀ = 3) where closed-form or high-precision computation is feasible, to build intuition.
- Provide a cleaner proof sketch for Theorem 3 that makes the role of rough path theory more transparent — specifically, clarify why the standard ODE theory is insufficient and what the rough path machinery buys.

## Score and Decision

The paper makes a genuine theoretical contribution by applying rough differential equations to resolve the tension between kernel singularity and prediction convergence in deep NTK theory. The proof technique is creative and the generalization conditions in Section 6 add value. However, the experimental validation is insufficient to establish practical relevance, and the main theorem's proof sketch is difficult to follow without the appendix. As a theory paper, the contribution is solid but the impact is somewhat limited by the narrow setting (fully-connected ReLU, no biases, data on sphere, width much larger than depth).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept