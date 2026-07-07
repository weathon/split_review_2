Here is my final review.

## Summary

This paper develops a framework for parameterizing equivariant machine learning models on tensors using invariant theory, characterizing polynomial (and entire) functions that are equivariant under the diagonal action of the orthogonal group O(d), the Lorentz group O(s, d-s), and the symplectic group Sp(d). The key theoretical result (Theorem 1 and its corollaries) expresses any such equivariant function as a combination of tensor products of inputs with isotropic tensors, avoiding Clebsch–Gordan coefficients. The framework is demonstrated on three problems: stress-strain constitutive modeling, path signature estimation, and sparse vector recovery.

## Strengths

- **Clean theoretical characterization via invariant theory.** Theorem 1 and its corollaries provide an explicit, structurally transparent parameterization of equivariant tensor-to-tensor functions that avoids Clebsch–Gordan coefficients. The connection to classical results on isotropic tensors (Kronecker deltas, Levi-Civita symbol, and their analogs for indefinite orthogonal and symplectic groups) is well explained. (draft weight: +3.85)

- **Generality across classical Lie groups is a genuine advance.** Existing representation-theoretic methods (e3nn, escnn) are specific to SO(d)/O(d) for d = 2, 3. The paper's framework applies to O(d) for any d, the Lorentz group O(s, d-s), and the symplectic group Sp(d) — a meaningful expansion of scope. (draft weight: +4.45)

- **Three diverse demonstration problems.** The applications — stress-strain constitutive modeling, path signature estimation, and sparse vector recovery — span different scientific domains and illustrate different aspects of the framework (Corollary 1 for vector-to-tensor, Corollary 2 for symmetric-matrix-to-symmetric-matrix, Corollary 3 for Lorentz equivariance). (draft weight: +3.56)

## Weaknesses

### Major

- **No experimental comparison against the most directly relevant prior work (e3nn, escnn).** The related work section (lines 31–35) explicitly discusses e3nn, escnn, and Domina et al. (2025) as the closest existing methods, and makes comparative claims: "those methods are more memory efficient than our general formulation in Theorems 1 and 2, but they are comparable to our Corollaries 1 and 3" and "the computational and approximation power should be equivalent." Yet none of the three experiments compares against e3nn, escnn, or any representation-theoretic equivariant method. The stress-strain experiment (Table 1) compares only against an MLP baseline, MLP with 4-rotation data augmentation, and the TFENN baseline. The path signature experiment (Table 2) compares against MLP baselines and a hand-crafted discrete baseline. The sparse vector experiment (Table 3) compares against SoS methods and an MLP baseline. Without comparison against the closest equivariant methods, the empirical sections demonstrate primarily that "an equivariant model beats a non-equivariant model," which is already well established in the literature, and do not demonstrate that *this particular parameterization* has any advantage over the alternatives the paper itself identifies as closest. (draft weight: -7.70)

- **Internal inconsistency in the sparse vector results that is unexplained.** In Table 3, the reduced "Ours (Diag)" variant — which uses only vector norms and discards all pairwise cross-product information — *outperforms* the full "Ours" method in 6 out of 12 settings (e.g., Bernoulli-Gaussian with Diagonal Σ: 0.914 vs 0.463; Bernoulli-Gaussian with Identity Σ: 0.908 vs 0.342; Corrected Bernoulli-Gaussian with Diagonal Σ: 0.550 vs 0.460). Since the full model has strictly more information and expressive power, this pattern suggests overfitting or optimization failure that the paper does not discuss or explain, and it undermines the claim that the full equivariant parameterization is the best choice for this problem. (draft weight: -2.82)

### Minor

- **The TFENN baseline uses reported numbers, not a re-implementation.** Table 1 states "The TFENN errors are the results reported in Garanger et al. (2024)" (line 219). The paper does not confirm whether the same data splits, training procedure, or evaluation metric were used. Differences in training protocol can easily account for reported gaps, making this not a controlled comparison. (draft weight: -2.44)

- **No symplectic group experiments are reported.** Corollary 3 explicitly covers Sp(d), and line 264 mentions symplectic equivariance for the path signature task, but only O(d) and Lorentz experiments appear in Table 2. This leaves the claimed symplectic generality unvalidated. (draft weight: -2.26)

- **Data augmentation baselines use only 4 random rotations/transformations** (lines 243, 264). This is a very small number — a standard data augmentation comparison would typically use 20–50 transformations. (draft weight: -2.43)

- **No wall-clock training time, parameter count, or memory comparisons are reported**, making it difficult to assess practical overhead. The paper acknowledges the O(k'! n^{k'} (Q d n² + d^{k'})) complexity but does not provide empirical runtime or memory data to contextualize it. (draft weight: -0.11)

### Trivial

None.

## Nice-to-Haves

- An ablation study showing how performance degrades as the output tensor order M increases in the path signature experiment would be directly relevant to the complexity discussion.
- A limitations section explicitly discussing (i) the computational cost for high-order output tensors, (ii) the restriction to vector inputs in the practical formulation (Corollaries 1, 3), and (iii) that only simulated data was tested would improve the paper's framing.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Universally expressive" claim not matched by experimental scope** — REMOVED: The universality claim is theoretical (Stone–Weierstrass, Remark 1) about the architecture's capacity, not an empirical claim about benchmark performance. The criticism conflated theoretical expressivity with the scope of experimental validation.
- **Metric definition has "d_F/d_F" formatting error** — REMOVED: This is a parser artifact, not a paper error.
- **Pearce-Crump (2023) scope distinction** — REMOVED: The paper already addresses this distinction (line 35).
- **Missing limitations section** — REMOVED: Structure nitpick.
- **Missing appendix/supplementary content** — REMOVED: The parser strips these sections from all papers; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a comparison against e3nn/escnn on at least one problem** — ideally the stress-strain task where the group is O(3) and e3nn/escnn operate directly. This is the single most impactful improvement and would directly support the comparative claims made in the related work.
2. **Explain or address the Ours(Diag) > Ours results** in the sparse vector task — discuss whether the full model is overfitting and consider regularization or reduced capacity.
3. **Re-implement TFENN** in the same pipeline rather than citing reported numbers from another paper with unknown training details.
4. **Report wall-clock time and parameter counts** to allow practical comparison with baselines.
5. **Add at least one symplectic group experiment** to validate the claimed generality.
6. **Use a more standard number of augmentations** (e.g., 20–50) for the data augmentation baselines.

## Score and Decision

**Calibration summary.** Six anchor papers were retrieved and compared:

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| kyVzYpDxHg (earlier version of this paper) | 5.75 | 1,2 | Yes | Same paper with fewer experiments; was rejected. Current paper improves scope but still misses key comparison. |
| tzpXhoNel1 (GRepsNet) | 4.25 | 1 | Yes | Similar architecture paper with missing competitor comparisons (weight -7.36); current paper is clearer and stronger. |
| 79FVDdfoSR (Characterization Theorem) | 7.00 | 1 | No | Strong theory paper with clear contribution; less directly comparable. |
| NxLWeK4P3q (Unified Universality Theorem) | 5.00 | 2 | Yes | Theory-heavy paper with readability issues; rejected. Current paper has stronger experimental scope. |
| LvTSvdiSwG (EquiLoPO Network) | 5.00 | 2 | No | Novel architecture; accepted despite 5.0. |
| 0aaaM31hLB (Learning Symmetries) | 5.25 | 2 | No | Empirical study of equivariance; rejected. |

**Weighted-item comparison.** My draft's heaviest negative weight is the missing e3nn/escnn comparison (-7.70), comparable in magnitude to the "missing SOTA competitors" criticism in GRepsNet (-7.36) and the "limited experiments" criticism in the earlier paper version (-5.40). My draft's positive weights (+3.56 to +4.45) are comparable to the earlier version's (+3.49 to +5.53). The missing comparison gap is the decisive factor: it is a structural flaw in the evaluation that prevents the paper from supporting its comparative claims, and the earlier version of this paper was rejected despite a similar strength profile and a slightly higher average score (5.75).

**Score: 5.0** — The theoretical contribution is genuine, original, and well-executed. The invariant-theoretic parameterization for tensor-to-tensor functions across O(d), Lorentz, and symplectic groups is a meaningful advance. However, the experimental evaluation has a structural gap: the paper makes explicit comparative claims about being comparable to e3nn/escnn in computational and approximation power, yet never actually compares against these methods. Combined with the unexplained Ours(Diag) > Ours anomaly, reliance on externally reported TFENN numbers, and absence of symplectic experiments, the empirical validation is insufficient to support the full set of claims advanced. The paper is best evaluated as a theoretical methods contribution with demonstrations, and on those terms the theory is solid — but the gap between the theoretical contribution and the experimental claims is too wide.

**Decision: Reject**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>