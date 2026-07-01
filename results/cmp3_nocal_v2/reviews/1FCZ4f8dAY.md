Here is the final consolidated review.

---

## Summary
This paper develops a theoretical framework — grounded in classical invariant theory — for constructing G-equivariant functions from tensors to tensors, where G is the orthogonal group, the indefinite orthogonal (Lorentz) group, or the symplectic group. The theory is translated into practical parameterizations (Corollaries 1–3) for the vector-input case, and demonstrated on three applications: learning stress-strain relationships, estimating path signatures from sparse samples, and sparse vector estimation.

## Strengths
1. **Generality across groups.** The paper extends the invariant-theoretic approach beyond O(d) to the Lorentz group O(s,d−s) and the symplectic group Sp(d). For these groups, explicit learnable equivariant tensor architectures are genuinely scarce in the ML literature, making this a concrete advance.

2. **Clean mathematical characterization.** Theorem 1 (and its generalization Theorem 2) provides a precise structural result: every G-equivariant polynomial tensor function decomposes into tensor products of inputs with isotropic tensors, followed by contractions. Corollaries 1 and 3 translate this into implementable parameterizations for the vector-input case, and Corollary 2 handles symmetric 2-tensor inputs. The proofs are grounded in established invariant theory (Jeffreys, Roe Goodman).

3. **Avoids Clebsch–Gordan machinery.** By using invariant theory (isotropic tensors built from Kronecker deltas and invariant bilinear forms) instead of irreducible representations and Clebsch–Gordan coefficients, the framework is conceptually simpler and does not require specialized representation-theory software. This is a genuine simplification over the e3nn/escnn pipeline.

4. **Strong empirical margins against non-equivariant baselines.** In all three applications, the equivariant models substantially outperform non-equivariant MLPs (Table 1: stress-strain error 4e−6 vs. 1.6e−4 at n=5,000; Table 2: path signature error 0.002 vs. 0.071 for same-parameter-count MLP under O(d)). The stress-strain experiment additionally includes a comparison against TFENN (Garanger et al., 2024), itself an equivariant method, and outperforms it by roughly an order of magnitude.

## Weaknesses

### Fatal
None.

### Major
1. **Missing comparison against Clebsch–Gordan-based equivariant architectures (e3nn, escnn) for O(d) problems.** The paper discusses e3nn, escnn, and Domina et al. (2025) at length as closely related approaches, noting that "the computational and approximation power should be equivalent" and that the methods are "comparable" for the vector-input corollaries. Yet none of these methods are used as baselines in any experiment. The stress-strain experiment includes TFENN (an equivariant method specific to that problem), but the path signature and sparse vector experiments compare only against non-equivariant MLPs (with or without data augmentation) and, in the sparse case, SoS methods. This means the experiments cannot distinguish whether the performance gains come from *equivariance in general* (which any equivariant architecture would provide) versus something specific to *this particular parameterization*. Since the paper positions itself as providing a practical *alternative* to Clebsch–Gordan methods — and even makes comparative statements about memory efficiency — the absence of a direct comparison with e3nn or escnn on at least one O(d) problem weakens the empirical validation of the method as a practical alternative.

### Minor
1. **Scalability analysis is not contextualized with experimental data.** The paper acknowledges that Corollary 1 has complexity O(k'! n^{k'} (Q d n^2 + d^{k'})) and is "only practical for small values of k'." However, the actual values of n, k', M (truncation level), the number of terms in the Corollary 1 sum that were used, model parameter counts, and training/inference costs are not reported for any experiment. For the path signature and sparse vector problems (which use Corollary 1), this makes it hard for readers to assess practical feasibility beyond the paper's qualitative statement.

2. **No explicit limitations discussion.** Section 6 (Discussion) ends without addressing known limitations of the approach: the combinatorial scaling of Corollary 1 with k' and n, the restriction to diagonal group actions, and the fact that the general Theorem 1 is computationally impractical so only the specialized vector-input corollaries are feasible. The paper would be strengthened by an explicit limitations paragraph.

3. **Sparse vector results show a more nuanced picture than the narrative suggests.** While the paper's framing is largely balanced (points (i)–(iii) on line 268 accurately describe the pattern), SoS wins in 5 of 12 settings and the proposed method wins in 5 of 12 (with a diagonal variant winning 2). In settings where SoS assumptions are met (Bernoulli-Gaussian + Identity covariance, achieving 0.962), the proposed method scores only 0.190–0.342. The contribution "equivariant models can operate where theory cannot" is genuine, but a reader scanning the bolded entries could overestimate the method's dominance.

### Trivial
None.

## Nice-to-Haves
- An ablation on the q function parameterization (e.g., linear vs. MLP for q_{t,σ,J}) would help disentangle the benefits of the equivariant structure from the capacity of the shared MLP.
- Reporting n and k' explicitly for each experiment, along with the number of terms actually computed in the Corollary 1 sum, would aid reproducibility and practical assessment.

## Removed Points
These points were identified in the input review but removed after verification against the paper:
- **"No limitations or failure case discussion" was a "Critical Issue" in the input** — downgraded to Minor because the limitations are implicitly clear from the complexity analysis and the paper does not overclaim practicality.
- **"First work claim is undermined by Pearce-Crump (2023)"** — removed because the paper qualifies the claim with "at this level of generality" and explicitly distinguishes Pearce-Crump as handling only tensor-power inputs/outputs. The claim is defensible.
- **"Stone–Weierstrass argument creates a theoretical gap"** — removed because this reasoning is standard in ML theory (it is an existence/universality argument, which is the appropriate use). All universal approximation guarantees have this character.
- **"Metric in Table 2 contains d_F/d_F, which should reduce to 1"** — removed as a parser formatting artifact.
- **"MLP baseline column is flat across all 12 settings (0.196–0.242)"** — removed because the Bernoulli-Rademacher rows show MLP scores of 0.845–0.923, contradicting the flatness claim. The MLP is flat only in 9/12 settings.
- **"Sparse vector narrative overstates competitiveness"** — partially removed. The paper's own framing (lines 268–269) is balanced and accurate. Retained only the narrower observation that a casual reading could overestimate dominance.

## Novel Insights
The reviews surface one observation worth noting: the experimental design conflates two effects — (a) the benefit of equivariance as an inductive bias, and (b) the specific parameterization choices (shared MLP for q functions, particular summation truncation). Without a comparison against an alternative equivariant parameterization (e.g., e3nn), one cannot fully disentangle which factor drives the performance gains over non-equivariant models. This is a structural limitation of the experimental validation, not of the theory itself.

## Suggestions
- Add at least one comparison against e3nn or escnn on an O(d) benchmark (e.g., the stress-strain problem, or path signature in d=3) to validate the claim that this parameterization is a practical alternative.
- Report n, k', M, number of Corollary 1 terms used, model parameter counts, and training/inference times for each experiment.
- Add an explicit limitations paragraph to Section 6.

## Score and Decision
MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>