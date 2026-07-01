## Summary

This paper provides three theoretical and algorithmic contributions to separable neural networks (SepNNs): (1) a universal approximation theorem for CP, TT, and Tucker forms of SepNNs, (2) an NTK analysis revealing deterministic and random kernel regimes along with spectral bias characterization, and (3) an efficient separable preconditioned gradient descent (SepPGD) method with \(\mathcal{O}(nD)\) complexity for \(n^D\) grid training samples, designed to alleviate spectral bias. Experiments on kernel ridge regression, implicit neural representations, and physics-informed neural networks demonstrate that SepPGD accelerates convergence and improves representation quality.

## Strengths

- **Fills a theoretical gap:** The universal approximation theorem for multivariate SepNNs (CP, TT, Tucker) is a clean and needed extension; the proof via Stone–Weierstrass is elegant and unifies multiple tensor decomposition forms.
- **Novel NTK analysis for SepNNs:** Deriving both deterministic (infinite width & infinite rank) and random (infinite width & fixed rank) NTK regimes is new and provides meaningful insight into how SepNNs behave under gradient descent, including spectral bias characterization.
- **Practical and efficient algorithm:** SepPGD exploits the separable structure to reduce preconditioner construction and application cost from \(\mathcal{O}(n^{3D})\) / \(\mathcal{O}(n^D)\) to \(\mathcal{O}(D n^3)\) / \(\mathcal{O}(nD)\), which is a substantial improvement over existing NTK-based preconditioning methods.
- **Clear experimental benefit:** The empirical results across KRR, INRs, and PINNs show that SepPGD yields faster convergence and often better final accuracy compared to standard SepNN training and the MSK baseline, with visual improvements clearly visible.

## Weaknesses

### Fatal

None.

### Major

- The claim that SepPGD “provably adjusts its NTK spectrum” is overstated. Lemma 2 only establishes equivalence to a Kronecker-sum preconditioner for the bivariate case, and the subsequent argument that \(\mathbf{K}\tilde{\mathbf{S}}\) has better spectrum relies on the approximation \(\tilde{\mathbf{K}} \approx \mathbf{K}\) and the assumption that factor preconditioners improve each factor’s NTK spectrum. A rigorous proof that the composite preconditioner guarantees improved convergence rate is missing.
- The NTK convergence results (Theorem 2, Corollary 1) lack precise specification of the limit order (width \(W\) and rank \(R\) going to infinity jointly or sequentially). Whether the two limits commute is not discussed, and the “simultaneous” phrase is ambiguous. This weakens the theoretical foundation for the claimed deterministic vs. random regimes.

### Minor

- The experimental evaluation does not include standard optimizers such as Adam or SGD with momentum for SepNNs, making it unclear whether the advantage of SepPGD is due to preconditioning or simply to better default hyperparameters. The only comparison is against MSK preconditioning.
- The complexity claim of \(\mathcal{O}(nD)\) per iteration for SepPGD is reported without accounting for the preconditioner construction overhead (eigenvalue decomposition of \(D\) \(n\times n\) matrices, \(\mathcal{O}(D n^3)\)). While this construction can be done infrequently, it should be explicitly discussed in the complexity analysis.
- The universal approximation theorem, while useful, is a relatively direct application of Stone–Weierstrass combined with the universal approximation of MLPs; the novelty is moderate compared to the existing bivariate result.

### Trivial

- The abstract mentions “Weierstrass-based approximation” but the proof actually uses the Stone–Weierstrass theorem. This is a minor imprecision.
- In Lemma 2, the notation for \(\tilde{\mathbf{S}}\) uses Kronecker products without explicitly noting the dimensions of the identity matrices, which could be clarified.

## Nice-to-Haves

- Extend the SepPGD analysis to non-grid inputs with convergence guarantees, or at least provide a more thorough theoretical justification of why the Kronecker-sum preconditioner adjusts the spectrum.
- Include experiments comparing SepPGD with standard optimizers (Adam, SGD) for SepNNs to better isolate the benefit of preconditioning.
- Provide an ablation study on the effect of the rank \(R\) on the NTK spectrum and the effectiveness of SepPGD in practice.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. Clarify the limit order in Theorem 2 and Corollary 1: state whether \(W\) and \(R\) go to infinity jointly under a specific scaling or sequentially, and provide conditions under which the limits commute.
2. Strengthen the theoretical justification for SepPGD by either proving that the preconditioned NTK matrix \(\mathbf{K}\tilde{\mathbf{S}}\) has a strictly smaller condition number than \(\mathbf{K}\), or acknowledge the heuristic nature of the claim.
3. Add experiments with standard optimizers (Adam) for SepNNs in the main paper to give a more complete picture of where SepPGD stands relative to common practice.
4. Report the number of iterations used in each experiment alongside execution time to allow direct comparison of convergence speed.

## Score and Decision

**Score:** 6.0  
**Decision:** Accept

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>