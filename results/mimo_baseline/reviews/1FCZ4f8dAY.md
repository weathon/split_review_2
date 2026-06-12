## Summary

This paper develops equivariant machine learning architectures for tensor-valued functions that respect symmetries under classical Lie groups—orthogonal O(d), indefinite orthogonal O(s,d-s) (including the Lorentz group), and symplectic Sp(d)—by leveraging invariant theory rather than the representation-theoretic (Clebsch-Gordan) approaches used in prior work. The authors provide explicit characterizations of equivariant polynomial and analytic functions from multiple tensor inputs to tensor outputs, derive computationally practical corollaries for vector-input cases, and demonstrate improvements over non-equivariant baselines on three applications: stress-strain modeling, path signature estimation, and sparse vector estimation.

## Strengths

- **Solid theoretical foundation with practical corollaries.** The paper provides clean characterizations (Theorems 1–2, Corollaries 1–3) that translate classical invariant theory results into ML-compatible parameterizations. Corollary 1 in particular gives a concrete, implementable recipe: output tensors are linear combinations of outer products of input vectors and Kronecker deltas, with coefficients that are learnable functions of pairwise inner products. This is both mathematically elegant and directly usable.

- **Genuine generalization beyond prior work.** Compared to Villar et al. (2021), this paper handles arbitrary tensor orders, indefinite orthogonal groups (including the Lorentz group), and the symplectic group. Compared to e3nn/escnn methods (Geiger & Smidt, 2022; Cesa et al., 2022), the invariant-theory approach applies to arbitrary d rather than only d=2,3, and the parameterization avoids computing Clebsch-Gordan coefficients.

- **Diverse and convincing experimental validation.** The three applications span materials science (stress-strain tensors), time series analysis (path signature estimation), and theoretical computer science (sparse vector estimation). The equivariant models consistently outperform non-equivariant baselines. For stress-strain (Table 1), the method achieves ~10× lower error than TFENN. For path signatures (Table 2), the method reduces error by orders of magnitude over MLP baselines. The sparse vector experiment (Table 3) provides an honest, nuanced comparison showing that learned equivariant models excel precisely in regimes where SoS theoretical guarantees break down.

## Weaknesses

### Fatal
None.

### Major

- **No direct comparison with representation-theory-based equivariant methods (e3nn, escnn, Domina et al. 2025).** The paper argues that the invariant-theory and representation-theory approaches are "computationally equivalent" for the Corollary cases, but provides no experimental evidence for this claim. A direct comparison on at least one task would substantially strengthen the paper, as it is currently unclear whether the alternative parameterization provides any practical benefit (better conditioning, faster convergence, etc.) beyond extending to more groups and dimensions.

- **Computational complexity limits practical applicability.** The direct evaluation of Corollary 1 has complexity O(k'! n^{k'} (Qdn² + d^{k'})), which restricts the output tensor rank to k' ≤ 4. While the paper acknowledges this and argues that low-rank tensors are practically common, this is a significant limitation not shared by e3nn-style methods that process tensors as structured representations. The experiments only use k' ∈ {1, 2}, so the practical viability at higher ranks remains untested.

### Minor

- **Sparse vector results are mixed in a way that deserves more discussion.** In Table 3, the full "Ours" method performs poorly in several settings (e.g., Accept/Reject with Identity covariance: 0.190; Corrected Bernoulli-Gaussian with Identity: 0.197), sometimes below the naive MLP baseline. The "Ours (Diag)" variant—which uses only norms rather than pairwise products—sometimes outperforms the full method. This suggests the full parameterization may overfit or that the inner-product-based invariant features are not always informative. A deeper analysis of when and why the method fails would be valuable.

- **Path signature experiment uses a single shared MLP for all q functions.** Given that the theoretical parameterization separates different terms by (t, σ, J), it would be informative to test whether using distinct networks for different structural components provides additional benefit.

### Trivial
None.

## Nice-to-Haves

- An ablation studying the effect of the degree of polynomial (number of input tensors combined) on performance across the experiments.
- A comparison of wall-clock training time between the invariant-theory parameterization and e3nn/escnn approaches to validate the claim of comparable efficiency.
- Application to a physics problem where Lorentz or symplectic equivariance is naturally demanded (e.g., relativistic particle physics or Hamiltonian systems), going beyond the path signature case.

## Novel Insights

The key novel insight is that invariant theory provides a complementary route to equivariant ML architectures that is in some ways more modular than the representation-theoretic approach: one separates the equivariant structure (handled by tensor contractions with isotropic tensors) from the learned component (the scalar functions q of inner products). This separation makes the symmetry constraint fully transparent and extendable to new groups (as demonstrated by the progression from O(d) to O(s,d-s) to Sp(d)) without requiring group-specific representation decompositions. The insight that Corollary 2 reduces equivariant functions of symmetric matrices to permutation-equivariant functions of eigenvalues is also a clean and practically useful observation.

## Suggestions

- Add at least one experiment comparing directly against an e3nn or escnn implementation on a standard benchmark (e.g., N-body dynamics, molecular property prediction) to substantiate claims about the alternative parameterization's practical merits.
- Provide an analysis of when the full Corollary 1 parameterization underperforms the diagonal-only variant in the sparse vector experiments—this would guide practitioners on which variant to choose.
- Consider discussing how the architecture composes across multiple layers, as the current experiments appear to use single-layer equivariant maps. Stacking multiple equivariant layers with nonlinearities in between is the standard deep learning paradigm, and understanding depth benefits would strengthen the practical contribution.

## Score and Decision

The paper makes a genuine theoretical contribution by providing the first invariant-theory-based characterization of equivariant tensor maps for O(d), O(s,d-s), and Sp(d) at this level of generality, and translates it into practical ML architectures. The experimental validation across three diverse domains is commendable and the results are consistently positive against non-equivariant baselines. However, the absence of comparison with the most directly competitive approach (e3nn/escnn), the acknowledged computational limitations, and the mixed results in the sparse vector setting prevent a stronger score. The paper is a solid contribution but would benefit from additional experimental depth.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept