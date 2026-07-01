## Summary

This paper develops a unified theoretical framework for constructing equivariant tensor-to-tensor functions under the diagonal action of the orthogonal group O(d), the Lorentz group O(s,d-s), and the symplectic group Sp(d). The authors translate classical invariant theory (the classification of isotropic tensors built from Kronecker deltas and Levi-Civita symbols) into practical machine learning architectures, providing explicit parameterizations for polynomial and analytic equivariant functions. The framework is demonstrated on three problems: stress-strain tensor prediction (materials science), path signature approximation (time series), and sparse vector estimation (theoretical computer science).

## Strengths

- **Extension to Lorentz and symplectic groups is a genuine advance.** Prior equivariant tensor architectures (e3nn, escnn, Domina et al.) are restricted to O(d) and SO(d) for d=2,3. Theorem 2 and Corollary 3 extend the characterization to O(s,d-s) (including the Lorentz group) and Sp(d) using the same invariant-theoretic machinery. The path signature experiment (Table 2) demonstrates the framework working under both O(d) and Lorentz equivariance, which existing Clebsch–Gordan-based methods cannot directly handle.

- **Clean theoretical-to-practical pipeline.** The paper structures its presentation well: Theorem 1 gives the general but computationally intractable characterization, then Corollary 1 extracts a tractable special case (vector inputs, tensor outputs) that is used in all experiments. The computational complexity is stated explicitly (Section 3), and the paper is honest about where the bottlenecks are. The connection between general theory and usable architecture is clearly drawn.

- **Strong empirical results on two of three problems.** The stress-strain experiment (Table 1) shows dramatic improvements — roughly an order of magnitude over the TFENN baseline and two orders over the MLP baseline. The path signature experiment (Table 2) shows the equivariant model substantially outperforming data-augmented MLPs (0.002 vs 0.007 for O(d), 0.005 vs 0.186 for Lorentz). These results provide clear evidence that the equivariant inductive bias helps.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **One sentence in the Discussion overstates the sparse vector results.** Section 6 states: "The equivariant models outperform all non-equivariant baseline models." Table 3 shows a more nuanced picture. In the Accept/Reject + Identity setting, the full "Ours" model achieves 0.190 while the MLP baseline achieves 0.196 (higher is better). The variant "Ours (Diag)" does outperform the MLP baseline, so the class of equivariant methods is competitive, but the blanket claim is not accurate for the full model in this specific setting. The Table 3 caption already provides a careful, nuanced interpretation, but the Discussion sentence should be tightened to match it.

2. **The TFENN comparison uses reported rather than reproduced numbers.** The paper states "The TFENN errors are the results reported in Garanger et al. (2024)" — single values without standard deviations from a separate paper. While the improvement magnitude (orders of magnitude) makes the conclusion likely robust, this should be acknowledged as a methodological limitation of the comparison. The paper does not note this anywhere.

3. **No explicit limitations section.** Given the computational complexity scaling (exponential in output tensor rank k', polynomial in number of input vectors n), the restriction to vector inputs in the practical architecture (Corollaries 1 and 3), and the mixed sparse-vector results, a candid limitations discussion would strengthen the paper. The paper mentions the complexity bound and the restriction to small k', but does not synthesize these into a clear statement of the method's practical regime.

4. **The path signature metric normalization is unclear.** Table 2 reports the metric as `(1/M) Σ (d_F/d_F) ||·||_F^2`. The fraction `d_F/d_F` appears to be a formatting artifact and its intended normalization is not explained. This makes it impossible for readers to interpret the absolute scale of the reported errors.

### Trivial
None.

## Nice-to-Haves

- **Stronger baselines for the path signature experiment.** The current baselines are a naive discrete approximation and standard MLPs. While the MLP-augmented baseline (trained with random rotations) is a fair test of approximate equivariance, adding a comparison with an existing learned signature approximation method or adapting e3nn/escnn to this task would help isolate whether the improvement comes from the specific tensor-contraction parameterization versus simply using any well-designed equivariant architecture.

- **A brief discussion of why "Ours (Diag)" sometimes outperforms the full "Ours" model** in the sparse vector experiments. The full model uses all pairwise inner products, while the diagonal variant uses only norms. Cases where the simpler variant wins (e.g., Bernoulli-Gaussian + Identity: 0.908 vs 0.342) suggest the additional features can hurt, likely through overfitting. This observation could guide practitioners on which variant to use.

## Removed Points

- **"The central theoretical result is a translation of known invariant theory rather than a new mathematical result"** — The paper acknowledges this lineage explicitly ("leverages the tensor invariant theory into a format useful for machine learning frameworks") and frames the contribution as translation/extension, not discovery. The novelty is in (i) extending to Lorentz/symplectic groups and (ii) providing a practical parameterization. This is an observation about framing, not a weakness.

- **"Corollary 3 restricts to vector inputs/outputs whereas Theorem 2 is general"** — The reviewer notes the paper is transparent about this, and the situation is symmetric to the O(d) case (Theorem 1 → Corollary 1). This is not a weakness.

- **"No code release"** — Code links may appear in the appendix, which was stripped by the parser.

- **"No comparison with e3nn/escnn"** — The paper explains in Section 1 that e3nn/escnn are restricted to O(d)/SO(d) for d=2,3 and cannot handle the Lorentz/symplectic experiments. On the O(d) tasks, the paper's claim is that the parameterization is different but computationally comparable, not that it outperforms these methods.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Tighten the Discussion sentence about sparse vector results to match the nuanced interpretation already present in Table 3's caption.
2. Acknowledge the methodological limitation of comparing against reported (not reproduced) TFENN numbers.
3. Add a brief limitations paragraph discussing the practical regime (small k', small-to-moderate n), the restriction to vector inputs for non-O(d) groups, and when the diagonal variant may be preferable.
4. Clarify the path signature metric normalization in Table 2.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>