## Summary
This paper develops a general framework for building equivariant machine learning models on tensors under the diagonal action of the orthogonal, Lorentz (indefinite orthogonal), and symplectic groups. The authors characterize polynomial and entire equivariant functions from tensor inputs to tensor outputs using invariant theory, showing that such functions can be expressed as linear combinations of tensor products of inputs with isotropic tensors (contracted appropriately). They provide practical corollaries for the common case of vector inputs, and demonstrate the effectiveness of their approach on three problems: stress-strain tensor prediction in materials science, path signature approximation for time series, and sparse vector estimation.

## Strengths
- **Generality and theoretical depth**: The paper provides a unified treatment of three different groups (O(d), Lorentz, symplectic) with rigorous theoretical characterizations. The generalization to entire functions (Theorem 2) and the extension beyond O(d) to indefinite orthogonal and symplectic groups is novel and valuable.
- **Clean bridge between invariant theory and ML architectures**: The derivation from invariant theory (isotropic tensors built from Kronecker delta, Levi-Civita, and their group-specific analogues) to practical equivariant architectures is elegant and well-explained. Corollaries 1 and 3 provide concrete, implementable formulas.
- **Strong empirical results across diverse domains**: The method consistently outperforms non-equivariant baselines (MLPs, augmented training) across three very different problems. The improvements are often dramatic (e.g., orders of magnitude on the stress-strain task, and large margins on the path signature task). The sparse vector results are particularly informative as they show when the learned equivariant model excels over theory-based methods (SoS) and when it does not.
- **Clear relation to prior work**: The authors carefully distinguish their invariant-theoretic approach from Clebsch-Gordan/representation-theory approaches (e3nn, escnn), acknowledging the trade-offs (generality vs. memory efficiency) rather than claiming superiority on all axes.

## Weaknesses
### Fatal
None.

### Major
- **Scalability and computational cost are not adequately addressed**: The paper mentions that evaluating the general form of Corollary 1 has complexity O(k'! n^{k'} (Q d n^2 + d^{k'})) and is "only practical for small values of k'." However, the experiments only use very small output tensor orders (k'=2 for stress-strain and path signature, k'=d for sparse vector). The method's practicality for higher-order outputs (k' >= 4) or larger n is unclear, and no experiments or scaling analysis is provided. This limits the claimed generality.
- **Missing comparisons with representation-theory-based equivariant methods (e.g., e3nn) on the actual tasks**: The paper contrasts its approach with e3nn/escnn in related work, but never compares empirically against them. Since those methods are also designed for equivariant tensor-to-tensor maps and are applicable for O(d) (especially d=3), a direct comparison on the stress-strain or path signature tasks would be informative. The authors only compare against non-equivariant baselines and a domain-specific method (TFENN).
- **The path signature experiment is underspecified**: It is unclear how the ground-truth path signatures were computed, what class of paths was used, and how the input points were sampled. The Lorentz group results are presented without explaining what Lorentz-equivariant paths look like or why that symmetry would arise in a time-series context. The practical significance of Lorentz-equivariant signature approximation is not motivated.

### Minor
- The architecture choices for the q functions (shared MLP across all t, sigma, J) are described briefly in the appendix, but it is not discussed why this sharing is reasonable or how it affects expressivity compared to having separate MLPs.
- The sparse vector experiment uses a metric (langle v, hat{v} rangle^2) that is natural, but the paper does not report any uncertainty estimates beyond standard deviation across 5 trials. Given the high variance across sampling methods, this is acceptable but it would be stronger to see significance tests.
- The "Ours (Diag)" variant (which only uses norms of input vectors) is introduced in the sparse vector experiment but not in the other experiments, and its motivation is somewhat unclear until reading the appendix. It would be cleaner to either introduce it earlier or explain its role in the main text.

### Trivial
- The paper says "an arrow points to a 4x4 grid" in the Figure 1 caption but the caption appears to be a mix of description and OCR artifacts. (Not a flaw per the instructions, but the figure is not particularly informative as printed.)

## Nice-to-Haves
- An ablation or analysis comparing the expressivity of the shared-MLP architecture vs. separate MLPs for each (t, sigma, J) combination.
- A discussion or experiment showing the behavior of the method as the output tensor order k' grows (e.g., k'=3, 4) to give a sense of where the method breaks down.
- A brief comparison on the stress-strain task with an e3nn-based model of similar capacity would strengthen the claim that the approach is competitive with representation-theory methods.

## Novel Insights
Beyond the paper's own contributions (the general equivariant characterization and its application), the most striking insight is the equivariant reparameterization of the sparse vector problem. This reveals that the function mapping a random subspace basis to an estimate of the planted sparse vector is O(d)-equivariant, which explains why enforced equivariance drastically improves generalization over a plain MLP. This connection between a non-obvious symmetry structure and improved learning is a valuable illustration of the method's reach. The neat observation that pure symmetry obviation allows learned models to outperform theoretically-guaranteed SoS methods when the SoS assumptions are violated is also noteworthy.

## Suggestions
1. Add a scaling experiment showing wall-clock time or parameter count vs. output tensor order k' (e.g., for k'=1,2,3,4) to give practitioners a concrete sense of the method's limits.
2. Compare against a representation-theory-based equivariant method (e.g., e3nn's simplest equivariant map for O(3)) on at least the stress-strain task (d=3).
3. Clarify the path signature experiment: (a) how are ground-truth signatures computed? (b) what family of paths are used? (c) what does Lorentz-equivariance mean in this context and why would a path satisfy it?
4. Add a brief paragraph in the main text explaining the "Ours (Diag)" variant and its motivation.

## Score and Decision
This is a strong paper with a clean theoretical contribution, three diverse empirical validations, and a clear writing style. The weaknesses are about scope of validation (scalability, comparison with representation-theory methods) rather than fundamental flaws. The paper is suitable for ICLR.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>