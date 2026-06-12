## Summary

This paper proposes quantum Frank-Wolfe (QFW) algorithms for projection-free sparse convex optimization over both vector domains (ℓ₁-ball, simplex, latent group norm constraints) and matrix domains (nuclear norm constraints). For vectors, they achieve O(√d/ε) query complexity per iteration via quantum maximum finding for gradient components, improving over classical O(d). For matrices, they propose two algorithms—quantum top singular vector extraction (QTSVE) and quantum power method (QPM)—to solve the linear subproblem in FW with time complexity Õ(rd/ε²) and Õ(√rd/ε³) respectively, achieving at least O(√d) speedups over classical power/Lanczos methods.

## Strengths

- **Systematic and comprehensive framework**: The paper provides a thorough treatment covering multiple constraint types (ℓ₁, simplex, latent group norm, nuclear norm) with tailored quantum subroutines for each, organized through a unified Frank-Wolfe paradigm. This is more than isolated results—it establishes a coherent research program.

- **Novel quantum subroutines with careful error analysis**: The paper develops several technically interesting subroutines: (1) a coherent dual norm computation across all groups in quantum superposition for latent group constraints; (2) quantum maximum finding applied to gradient components with non-uniform input states (Lemma 4); (3) QTSVE combining QSVE with quantum maximum finding to avoid repeated sampling; and (4) QPM for iterative top singular vector extraction. The convergence analyses (e.g., Appendix B.3, B.9, B.11) properly account for how quantum approximation errors propagate through Frank-Wolfe iterations, establishing error bounds via Hölder's inequality for the linear subproblem accuracy.

- **Clear quantum advantages with concrete complexity bounds**: The results are cleanly stated with explicit parameters. Table 1 and Table 2 provide transparent comparisons. For the vector case, the O(√d) speedup in query complexity per iteration is achieved with modest overhead (O(d + log(1/ε)) qubits, O(√d) gates), which is a genuine and well-quantified improvement.

- **First treatment of quantum FW for matrix domains**: The authors correctly identify that prior quantum FW work (Chen & de Wolf, 2023) only addressed vector linear regression with explicit gradient forms. The matrix case requires fundamentally different quantum subroutines (QSVE-based and power method-based), and the results here are novel.

## Weaknesses

### Fatal
None.

### Major

- **Total end-to-end complexity is not clearly established**: The quantum advantages are stated in terms of per-iteration query/time complexity for the linear subproblem or gradient estimation. However, the total number of FW iterations remains O(C_f/ε) regardless of quantum oracles, and the per-iteration overhead includes quantum state preparation, tomography (for matrix case), and classical post-processing. The paper does not provide a complete end-to-end complexity comparison with classical methods, making it difficult to assess when the quantum advantage materializes in wall-clock terms.

- **Spectral gap dependencies in matrix case**: The QTSVE result (Theorem 3) depends on σ₁(M)/(σ₁(M)−σ₂(M)), which diverges when the top two singular values are close. The QPM result (Theorem 4) depends on γ'_min, a lower bound on ‖(M^TM)^i b‖ that can be exponentially small. The paper acknowledges these dependencies in the complexity expressions but does not discuss how restrictive they are in practice or for which application domains these conditions are favorable. This limits the practical significance of the matrix results.

- **Quantum oracle assumptions**: For the vector case, the function value oracle (Assumption 3) requires implementing f as a quantum circuit, which is a strong assumption for general convex objectives. For the matrix case, Assumption 4 requires quantum access to the gradient matrix in a specific block-encoding data structure, and the cost of preparing this structure from classical data is not accounted for. While these are standard assumptions in quantum ML, the paper would benefit from a franker discussion of when these oracles can be efficiently implemented for the stated applications (Lasso, matrix completion, SVMs).

### Minor

- **Jordan algorithm trade-off**: Theorem 5 achieves O(1/ε) query complexity but requires O(d log(d/ε)) qubits and O(d log d) gates, effectively trading query complexity for significantly increased space and gate complexity. For moderate d, this may not represent a practical improvement, and the trade-off deserves more explicit discussion.

- **Comparison granularity**: In Table 1, classical query complexity is listed as O(d) per iteration (total: O(d·C_f/ε)), while quantum is O(√d log(C_f/ε)) per iteration (total: O(√d·C_f/ε · log(C_f/ε))). The logarithmic factor in the iteration count could matter, and the comparison could be more precise about total complexity.

- **Notation inconsistency**: The paper alternates between ε and ϵ for precision parameters across different theorems, which could cause confusion.

### Trivial
None.

## Nice-to-Haves

- A discussion of specific problem instances (e.g., concrete matrix completion datasets) where the spectral gap conditions are favorable and the quantum advantage would be most pronounced.
- A brief complexity-theoretic lower bound argument to establish that the O(√d) speedup is optimal or near-optimal for the quantum setting.

## Novel Insights

The paper introduces a genuinely novel paradigm of applying quantum maximum finding and quantum singular value estimation specifically within the Frank-Wolfe iteration framework. The key insight is that the linear subproblem in FW—finding the extreme point of the constraint set along the gradient direction—naturally maps to a quantum search/optimization problem where Grover-type speedups are applicable. The coherent dual norm computation for latent group constraints (computing norms across all groups in superposition and then quantum-searching for the dominant group) is a particularly elegant construction that goes beyond naively applying existing quantum subroutines. The two complementary matrix algorithms (QTSVE for high-rank gradients, QPM for low-rank gradients) also reflect a thoughtful design that matches algorithm properties to problem structure.

## Suggestions

- Add a dedicated subsection discussing the total end-to-end complexity, including oracle implementation costs, to give readers a complete picture of when quantum advantage is achievable.
- For the matrix case, provide a concrete characterization of problem classes where σ₁/(σ₁−σ₂) = O(poly(d)) and γ'_min = 1/poly(d), so that the speedups are meaningful.
- Include a brief discussion of dequantization results (e.g., Tang, 2019) and whether any of the speedups claimed here are susceptible to similar dequantization.

## Score and Decision

The paper presents a solid theoretical contribution: a systematic study of quantum speedups for Frank-Wolfe algorithms across multiple constraint types, with novel quantum subroutines and careful convergence analyses. The technical content is sound, the results are clearly stated with explicit parameters, and the problem is well-motivated by important applications in ML. The main weaknesses—lack of end-to-end complexity analysis and restrictive spectral conditions for the matrix case—limit practical significance but do not undermine the theoretical contributions. For a theory-heavy paper at ICLR, the results are novel and will be valuable to the quantum optimization community.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept