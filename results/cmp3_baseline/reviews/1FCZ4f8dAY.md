## Summary
The paper develops a general framework for constructing machine learning models that are equivariant with respect to the diagonal action of the orthogonal, Lorentz (indefinite orthogonal), and symplectic groups on tensors. Using classical invariant theory, the authors characterize all equivariant polynomial (and entire) functions from multiple tensor inputs to tensor outputs in terms of isotropic tensors (Kronecker delta, Levi-Civita, and their group-specific analogues). Practical corollaries for vector inputs yield architectures where invariant inner products are input to small MLPs, whose outputs linearly combine fixed tensor products of inputs and identity-like tensors. The method is demonstrated on three diverse problems: stress-strain tensor prediction in materials science, learning path signatures from sparse samples in time series, and sparse vector estimation in a random subspace, consistently outperforming non-equivariant baselines and, in certain regimes, theoretical sum-of-squares methods.

## Strengths
- **Novel and general theoretical characterization.** The paper provides a clean, invariant-theory–based parameterization of equivariant tensor-to-tensor functions for classical Lie groups (O(d), Lorentz, Symplectic). This approach avoids Clebsch–Gordan decompositions and works for arbitrary dimensions, whereas prior equivariant tensor architectures (e.g., e3nn) are often limited to SO(d)/O(d) in low dimensions.
- **Practical architectures with clear derivation.** Corollary 1 and its generalizations yield simple, implementable models: MLPs over invariant pairwise inner products combined with outer products of input vectors and fixed isotropic tensors. The connection to invariant theory makes the architectural design principled and easy to extend to other groups.
- **Consistent experimental improvement across diverse domains.** The equivariant models outperform non-equivariant MLPs (including data augmentation) on all three tasks: stress-strain (materials), path signature estimation (time series), and sparse vector estimation (theoretical CS). The gains are substantial and statistically significant, demonstrating the value of the inductive bias.
- **Clear and well-structured exposition.** The paper carefully defines tensor operations, parity, and group actions, making the theoretical sections accessible. Illustrative examples (Example 1, Figure 1) help bridge theory to practice.

## Weaknesses
### Fatal
None.

### Major
- **No comparison to other equivariant tensor architectures.** For the stress-strain problem, the paper only compares to a specialized method (TFENN) and plain MLPs. A direct comparison to a generic equivariant architecture such as e3nn (Geiger & Smidt, 2022) or similar would have strengthened the claim that the invariant-theory parameterization is practically competitive.
- **Limited scaling analysis.** The computational complexity of the general construction grows combinatorially with output tensor order k' (O(k'! n^{k'} …)). While the paper notes this is practical only for small k', it does not quantify practical limits (e.g., memory/time for k'=4, n=100) nor discuss strategies (e.g., pruning terms) to handle larger settings.

### Minor
- **No experimental validation for the symplectic group.** The theoretical framework covers the symplectic group, but none of the experiments use it. While Lorentz experiments are included, a symplectic example (e.g., in a Hamiltonian dynamics setting) would have demonstrated full breadth.
- **Synthetic nature of all experiments.** All three problems use synthetic or simulation data. The paper would be strengthened by one real-world tensor dataset (e.g., from physics or engineering) to confirm the method transfers to realistic noise and distribution shifts.
- **Ablation on the role of pairwise inner products.** The sparse vector experiment includes a variant using only norms (“Ours (Diag)”), which sometimes outperforms the full version. An analysis explaining when full pairwise interactions help versus hurt would be informative.

### Trivial
None.

## Nice-to-Haves
- On the path signature problem, a comparison to a recurrent or transformer baseline that processes the sampled points as a sequence would provide context for how much the equivariant inductive bias alone contributes.
- A discussion of how to choose between the diagonal (norm-only) and full pairwise versions based on dataset characteristics.

## Novel Insights
Beyond the paper’s own contributions, a genuinely novel insight is that the parameterization of O(d)-equivariant tensor functions directly mirrors the functional dependence of isotropic material models (e.g., the stress-strain relation only depends on invariants of C). The paper makes this connection explicit and generalizes it to other groups, revealing a deep link between classical invariant theory, continuum mechanics, and modern equivariant ML. This observation could inspire new physics-informed architectures beyond the three examples shown.

## Suggestions
1. For the stress-strain experiment, include a comparison to e3nn or similar equivariant network to benchmark against existing generic equivariant architectures.
2. Provide a brief complexity table (e.g., time/memory for k′=2,3,4 and n up to 100) to guide practitioners on when the method is feasible.
3. Add a small symplectic experiment, perhaps on a simple Hamiltonian system, to demonstrate the full generality of Theorem 2.

## Score and Decision
Score: 7.5

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>