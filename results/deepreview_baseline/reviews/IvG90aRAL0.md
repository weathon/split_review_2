## Summary
This paper develops quantum Frank-Wolfe algorithms for projection-free sparse convex optimization, covering both vector domains (ℓ₁-ball, simplex, latent group norm) and matrix domains (nuclear norm). For vectors, the algorithms achieve query complexities \(O(\sqrt{d}/\varepsilon)\) and \(O(1/\varepsilon)\), improving over classical \(O(d)\) by factors of \(O(\sqrt{d})\) and \(O(d)\). For matrices, two complementary quantum subroutines (quantum top singular vector extraction and quantum power method) yield per-iteration time complexities \(\tilde{O}(rd/\varepsilon^2)\) and \(\tilde{O}(\sqrt{rd}/\varepsilon^3)\), reducing dependence on dimension \(d\) by at least \(O(\sqrt{d})\). The work provides theoretical convergence guarantees and claims the first quantum acceleration of Frank-Wolfe for the matrix case.

## Strengths
- **Systematic treatment of both vector and matrix domains** with multiple constraint types (ℓ₁-ball, simplex, latent group norm, nuclear norm), covering a wide range of important machine learning applications.
- **Novel quantum subroutines** adapted for Frank-Wolfe: quantum maximum finding for dominant atom identification, quantum top singular vector extraction via maximum finding on singular values, and a quantum power method for low-rank gradient matrices.
- **Clear speedup claims** supported by theoretical analysis, with explicit comparison tables (Tables 1 and 2) showing polynomial improvements in dimension \(d\) over optimal classical methods.
- **Convergence analysis** that accounts for errors from gradient approximation, singular vector estimation, and tomography, with parameter choices to control error propagation.

## Weaknesses
### Major
1. **Unsubstantiated and inconsistent claim of \(O(1)\) query complexity.** Table 1 lists query complexity \(O(1)\) for Theorem 5 (the Lipschitz continuous case), but the abstract states \(O(1/\varepsilon)\). No proof or adequate reference is provided for “bounded-error Jordan quantum gradient estimation” achieving \(O(1)\) queries per iteration. This appears overstated and undermines the credibility of the comparison table.
2. **Strong and costly quantum access assumptions for the matrix case.** The algorithms require the gradient matrix to be stored in a specific quantum-accessible data structure (Assumption 4) that supports fast state preparation. The cost of constructing or updating this structure each iteration (the gradient changes every round) is not accounted for, potentially negating the claimed speedup. The paper also assumes the gradient is precomputed and excludes its evaluation time, yet a complete quantum algorithm would need to compute the gradient quantumly.
3. **Dependence on rank \(r\) and singular value gaps is underplayed.** The speedup for matrix algorithms depends crucially on the rank \(r\) of the gradient matrix. When \(r\) is large (e.g., dense full-rank gradients), the quantum complexity approaches \(\tilde{O}(d^2/\varepsilon^2)\) or worse, which may not beat classical Lanczos. The paper does not discuss regimes where the quantum advantage is significant versus where it vanishes.

### Minor
4. **No empirical demonstration or simulation.** The paper is entirely theoretical; even a small-scale numerical simulation or resource estimate would help assess practical feasibility and validate the parameter choices.
5. **Ambiguity in the “query complexity” metric.** For the vector case, “query complexity” counts calls to the function value oracle. For the matrix case, the paper switches to “time complexity of computing the update direction.” This inconsistency makes direct comparison across settings difficult.

### Trivial
- None.

## Nice-to-Haves
- A discussion of how to update the quantum data structure efficiently as the iterate changes, or an alternative access model that does not require storing the full gradient each iteration.
- Clarification on whether the Jordan gradient estimation algorithm (if correctly cited) achieves \(O(1)\) queries per iteration or \(O(1/\varepsilon)\), and a careful explanation of its applicability to the Frank-Wolfe setting.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Correct the inconsistency between Table 1 and the abstract regarding the query complexity for the Lipschitz case. Provide a rigorous justification or remove the \(O(1)\) claim if it cannot be supported.
- Add an explicit discussion of the cost of preparing quantum access to the gradient matrix each iteration, including the number of gates and qubits required, and the impact on total runtime.
- Include a numerical toy example (classical simulation) for small \(d\) to illustrate the algorithm’s behavior and error trade-offs.

## Score and Decision
Score: 4.0

Decision: Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>