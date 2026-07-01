## Summary

This paper proposes quantum algorithms to accelerate the Frank-Wolfe (conditional gradient) method for projection-free sparse convex optimization. For vector domains with ℓ₁ norm or simplex constraints, the authors achieve query complexity of O(√d/ε) using a function value oracle, providing a √d speedup over classical methods. For matrix domains with nuclear norm constraints, they develop two complementary algorithms—one using quantum top singular vector extraction (QTSVE) and another using a quantum power method (QPM)—that achieve time complexity improvements of at least O(√d) over classical approaches for computing the update direction.

## Strengths

- **Broad and systematic treatment**: The paper addresses both vector and matrix domains with multiple constraint types (ℓ₁ ball, simplex, latent group norm, nuclear norm), providing a comprehensive investigation of quantum acceleration for Frank-Wolfe methods.

- **Novel quantum subroutines**: The development of quantum procedures for dominant atom finding under latent group constraints (computing dual norms coherently across all groups via quantum superposition) and the quantum maximum finding approach for top singular vector extraction represent genuine algorithmic contributions.

- **Error propagation analysis**: The authors establish rigorous error bounds for dual norm computation under gradient approximation using Hölder's inequality, enabling precise control of linear subproblem accuracy throughout the Frank-Wolfe iterations.

- **Clear exposition of speedups**: The comparison tables (Table 1 and 2) clearly document the dimensional speedups, and the paper explicitly identifies where the quantum advantage comes from in each setting.

## Weaknesses

### Major

- **Unrealistic oracle model for practical speedup**: The paper relies on a function value oracle (Assumption 3) that provides exact floating-point function values. In practice, evaluating f(x) is typically the same cost as evaluating the gradient. The claimed O(√d/ε) query complexity advantage does not translate to an actual runtime advantage if each query requires O(d) operations classically. The paper never addresses whether the quantum oracle can be implemented with a total gate count lower than the classical O(d) per-iteration cost for the overall algorithm.

- **Missing end-to-end resource analysis**: The paper reports query complexity and gate counts separately but never provides an end-to-end complexity accounting. For the vector case, Theorem 1 claims O(√d log(C_f/ε)) queries per round with O(√d) gates, but the quantum gradient circuit requires O(d) qubits and must evaluate f(x + σe_i) for each coordinate. The paper does not explain how evaluating all d coordinates in superposition avoids the O(d) effective classical cost when you account for the need to read out the result.

- **Lack of comparison with existing quantum optimization approaches**: The paper does not compare with quantum algorithms for convex optimization (e.g., quantum gradient descent, quantum accelerated gradient methods) that might achieve better or comparable rates. Without this context, it is unclear whether the Frank-Wolfe quantum speedup is meaningful relative to other quantum optimization paradigms.

- **Incomplete treatment of tomography cost**: In the matrix case (Theorems 3 and 4), the ℓ₂-norm quantum state tomography (Lemma 6) requires O(d log d/δ²) time. When δ is set to O(ε/(σ₁(M))), this introduces a d-dependence that appears to offset the claimed √d speedup in several regimes. The paper's complexity statements combine these factors in ways that obscure whether the net speedup is maintained.

### Minor

- **The quantum power method analysis (Theorem 4)** has a dependence on γ'ₘᵢₙ (the lower bound of ‖(MᵀM)ⁱb‖) that is not easily interpretable or estimable in practice. The claim of at least O(√d) speedup relies on favorable values of this parameter that may not hold.

- **The paper uses different comparison baselines for the vector case (query complexity) and matrix case (update computation complexity)**, making it difficult to directly assess whether the reported speedups are of the same nature or practical significance.

- **Assumption 4 (quantum access to matrix)** requires a specific QRAM-like data structure that is expensive to build (O(d² log d) initialization) and assumes the gradient matrix is already computed and stored. This sidesteps the gradient computation cost entirely.

## Nice-to-Haves

- A discussion of how the proposed algorithms would fare with a quantum gradient oracle (as in Jordan's algorithm) versus the classical gradient oracle would help clarify when the speedup is real.
- An empirical demonstration on a small-scale quantum simulator for a concrete problem (e.g., Lasso or matrix completion) would substantiate the practical claims.
- A comparison with the quantum SDP solvers (Brandão & Svore, 2017) that also leverage singular value estimation would help position this work.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the Frank-Wolfe linear subproblem, which classically requires scanning O(d) atoms or computing an SVD (O(d³)), can be reframed as a quantum search or quantum singular value estimation problem. This reframing is possible because the linear subproblem reduces to finding the extreme point of a convex hull—a combinatorial search that quantum algorithms can accelerate quadratically. The observation that the iterative sparsity structure of Frank-Wolfe (each iterate has at most t nonzeros) enables efficient quantum state preparation with cost decoupled from dimension is also noteworthy. However, whether these advantages survive in an end-to-end accounting that includes oracle implementation costs remains an open question that the paper does not fully resolve.

## Suggestions

1. Provide an end-to-end quantum gate count or qubit depth analysis that accounts for all components (function evaluation oracle implementation, gradient estimation, maximum finding, tomography) to demonstrate that the asymptotic speedup in query complexity translates to actual runtime improvement.

2. Clarify how the quantum function value oracle (Assumption 3) can be implemented with O(poly(log d, 1/ε)) gates for realistic ML objective functions. Without this, the query complexity speedup is vacuous.

3. Include a comparison table against other quantum convex optimization methods (quantum gradient descent, quantum accelerated methods) to contextualize the Frank-Wolfe approach.

4. In the matrix case, explicitly compute the net speedup when all factors (including tomography overhead) are accounted for, rather than reporting only the update step complexity.

## Score and Decision

The paper makes a genuine algorithmic contribution in formulating quantum subroutines for Frank-Wolfe linear subproblems and provides rigorous theoretical analysis. However, the fundamental issue is that the claimed speedups rely on oracle models whose quantum implementation costs are either not accounted for or would likely negate the advantage. The query complexity speedup in the vector case requires a function value oracle that can evaluate f at superposition inputs—a strong assumption whose implementation cost in qubits and gates is O(d) or worse for typical ML objectives. Similarly, the matrix case's observed speedup is for the update step only, with the gradient computation and classical tomography costs potentially dominating. These issues prevent the paper from convincingly demonstrating that quantum Frank-Wolfe algorithms would outperform classical ones in practice. 

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>