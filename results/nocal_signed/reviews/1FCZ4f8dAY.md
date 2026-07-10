Based on the impact analysis, the two major weaknesses (-8.2, -8.3) are significant but not fatal — they concern the scope of validation relative to the theory, not errors in the theory itself. The strengths are very strong (+9.9, +9.0, +7.7, +7.0), and the minor weaknesses have much lower impact scores (-0.4 to -3.7), with the Discussion section being the exception at -6.9 (which is still a presentation issue, not a scientific flaw). The balance clearly favors acceptance.

Let me now produce the final consolidated review.

## Summary

This paper provides a novel, invariant-theoretic parameterization of $O(d)$-, Lorentz- ($O(s,d-s)$), and $Sp(d)$-equivariant polynomial (and analytic) functions mapping tensors to tensors. Theorems 1 and 2 characterize all such equivariant maps using isotropic tensors (Kronecker deltas, Levi-Civita symbols, and their group-specific analogs) combined with outer products and contractions, avoiding the Clebsch–Gordan decompositions used by existing methods like e3nn/escnn. Practical architectures are derived as corollaries (Corollary 1 for vector inputs, Corollary 2 for symmetric 2-tensors, Corollary 3 for the Lorentz/symplectic groups) and are validated on three problems: stress-strain prediction in materials science, path signature estimation for time series, and sparse vector estimation.

## Strengths

- **Theoretical contribution is genuinely general and clean.** Theorem 1 (Section 3) and Theorem 2 (Section 4) give a complete parameterization of equivariant polynomial maps between arbitrary-order tensor spaces for $O(d)$, $O(s,d-s)$ (including the Lorentz group), and $Sp(d)$. The invariant-theoretic approach (Jeffreys' isotropic tensor construction) avoids Clebsch–Gordan decompositions and natively handles groups (Lorentz, symplectic) that e3nn/escnn cannot. This is a principled advance over Villar et al. (2021) and Pearce-Crump (2023).

- **Practical architecture is directly usable.** Corollary 1 reduces the general parameterization to a sum over outer products of input vectors and Kronecker deltas, with coefficients given by scalar functions of pairwise inner products. The paper provides computational complexity analysis ($O(k'!\, n^{k'})$) and honestly acknowledges the limitation to small output tensor rank $k'$.

- **Stress-strain experiment shows dramatic improvement (Table 1).** The proposed method outperforms the plain MLP baseline by roughly two orders of magnitude, the augmented MLP by roughly one order, and the equivariant TFENN baseline by roughly one order, across all three dataset sizes ($n=5,000, 20,000, 40,000$). These results are unambiguous.

- **Fair and precise positioning against related work.** The paper explicitly acknowledges that e3nn/escnn are more memory-efficient for $\text{SO}(3)/O(3)$ and states that computational and approximation power should be equivalent for vector-input settings. It does not overclaim superiority where it cannot support it.

## Weaknesses

### Fatal
None.

### Major

- **Experimental scope is narrower than the theoretical framework advertised.** Theorems 1 and 2 characterize general tensor-to-tensor maps with arbitrary input tensor orders, but every experiment tests only the simplified special cases: Corollary 1 (vectors as inputs) for path signature and sparse vector estimation, and Corollary 2 (symmetric 2-tensors as inputs) for stress-strain. While the stress-strain experiment does use tensor inputs (symmetric matrices), there is no experiment testing a general non-symmetric higher-order tensor input or mixed input types. The paper does suggest focusing on Corollary 1 on first reading, but the headline claim ("generic recipe for equivariant models mapping from tensors to tensors") is experimentally validated only for vectors and symmetric matrices. This is a gap between theoretical generality and empirical coverage, not a flaw in the theory itself.

- **No symplectic group experiment.** The paper presents $Sp(d)$ equivariance as a key differentiator from e3nn/escnn (which cannot handle symplectic symmetries), yet all experiments test only $O(d)$ or the Lorentz group. The symplectic construction remains purely theoretical with no experimental validation.

### Minor

- **Missing e3nn baseline where feasible.** The paper asserts that its method and e3nn have comparable computational and approximation power for $O(d)$. For problems where $d=2$ or $3$ (e.g., the path signature problem), an e3nn baseline would directly test this claim. Its absence leaves the practical comparison against representation-theoretic methods on their home turf unquantified.

- **Sparse vector results are more mixed than the narrative suggests.** While the method outperforms the MLP baseline in all settings, it loses to SoS in ~5/12 settings (including some non-Identity settings like Bernoulli-Gaussian/Random). The paper acknowledges this in the table caption, but the abstract and introduction's framing ("can handle settings where theoretical guarantees have yet to be developed") is only partially supported — SoS still wins in several settings where its assumptions are met.

- **Data augmentation baseline uses only 4 random transformations.** Since the equivariant architecture enforces exact equivariance (effectively infinite augmentation), a baseline with only 4 augmented examples is weak. A stronger augmentation baseline (50–100 transformations) would more fairly test whether the benefit comes from equivariance per se versus the particular parameterization.

- **Discussion section is too brief (one paragraph) and lacks any limitations section.** There is no discussion of computational cost scaling with tensor order, failure modes, settings where the approach should not be used, or expressivity/efficiency tradeoffs versus Clebsch–Gordan methods beyond what appears in the related work section.

- **No runtime or parameter counts reported in the main text.** The paper gives asymptotic complexity but provides no actual measurements of training time, inference time, or model sizes for any experiment.

### Trivial
None.

## Nice-to-Haves

- Add at least one experiment using the general tensor-input form of Theorem 1 (e.g., learning the stress-strain map directly from the 2-tensor $C$ using general isotropic tensors rather than the eigenvalue-based Corollary 2 shortcut) to further validate the framework's generality.
- Add a small symplectic group experiment.
- For the path signature problem at $d=3$, add an e3nn baseline.
- Strengthen the data augmentation baseline with many more random transformations.
- Report actual runtimes and parameter counts.

## Novel Insights

Beyond the paper's own contributions, the key synthesis from the review is that the invariant-theoretic approach to equivariant tensor functions offers a genuinely different route from the dominant Clebsch–Gordan / spherical-harmonic paradigm. Its primary advantage lies not in outperforming CG methods on $O(3)$ (where both approaches should be comparable), but in (1) applicability to groups (Lorentz, symplectic) where CG methods do not apply, and (2) the conceptual simplicity of avoiding irreducible decompositions. However, this advantage is currently supported only theoretically — the Lorentz experiment is the sole nontrivial validation of the cross-group generality, and the symplectic case has no experimental support.

## Suggestions

- Add a brief limitations paragraph to the Discussion section covering computational scaling, failure modes, and tradeoffs versus Clebsch–Gordan methods.
- Test at least one setting that uses the general tensor-input parameterization (Theorem 1) rather than the simplified corollaries, to validate the architecture's claimed generality.
- Consider a small-scale symplectic experiment (even synthetic) to validate the $Sp(d)$ construction presented as a key contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>