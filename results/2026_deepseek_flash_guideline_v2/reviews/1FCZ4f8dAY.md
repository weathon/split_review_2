## Summary

This paper develops a theoretical framework for constructing equivariant machine learning architectures for tensor-valued functions using classical invariant theory, applicable to O(d), the Lorentz group O(s,d−s), and the symplectic group Sp(d). The core idea is to parameterize equivariant polynomial tensor functions via isotropic tensors (Kronecker deltas and their group-specific analogs), avoiding the need for Clebsch–Gordan decompositions. Experiments on stress-strain prediction, path signature estimation, and sparse vector recovery show that the equivariant models substantially outperform non-equivariant baselines.

## Strengths

1. **First unified parameterization of equivariant tensor polynomials for O(d), Lorentz, and symplectic groups in ML-ready form (Theorem 1, Corollary 1, Theorem 2, Corollary 3).** Theorem 1 gives a complete characterization of O(d)-equivariant polynomial functions from arbitrary-order tensor inputs to tensor outputs. Corollary 1 specializes this to the vector-input case with an explicit constructive form (Eq. 11). Section 4 extends the theory to O(s,d−s) and Sp(d), replacing the Kronecker delta with the relevant bilinear form. This goes substantially beyond existing work: e3nn/escnn (Geiger & Smidt, 2022; Cesa et al., 2022) are specific to SO(d)/O(d) for d=2,3, and Pearce-Crump (2023) handles a more restricted function class.

2. **Consistent and often large empirical gains across three diverse applications (Tables 1–3).** The experiments span materials science (stress-strain tensors), time series analysis (path signature estimation), and theoretical computer science (sparse vector recovery). In the stress-strain problem (Table 1), the proposed model achieves test error 4.057e−6 at n=5,000 versus 2.020e−5 for the best MLP baseline and 5.3e−5 for the prior equivariant method TFENN — roughly a 5–13× improvement. In the path signature task (Table 2), the method achieves error 0.002 (O(d)) and 0.005 (Lorentz) versus 0.007 and 0.186 for the next-best baselines. In the sparse vector problem (Table 3), the method achieves correlation 0.935–0.957 in settings where sum-of-squares assumptions are violated, substantially outperforming SoS (0.412, 0.526) and MLPs (~0.2).

3. **Elegant reformulation of path signature estimation as an equivariant learning problem.** The paper casts truncated signature estimation as an O(d)- and Lorentz-equivariant function from sampled path points to tensors — a novel connection between rough path theory and geometric deep learning that is likely to be of independent interest.

4. **Honest complexity analysis and practical guidance.** The paper explicitly states the O(k'! n^{k'} (Q d n² + d^{k'})) complexity of Corollary 1 and transparently notes that evaluation is practical only for k' ≤ 4. This candor about computational limitations strengthens the paper's credibility.

## Weaknesses

### Fatal
None.

### Major

- **No symplectic group experiment despite prominent billing in title and abstract.** The title lists "symplectic" alongside orthogonal and Lorentz groups, and Corollary 3 provides the explicit parameterization. Yet none of the three experiments test a symplectic-equivariant problem. While the Lorentz group (the other non-O(d) group) IS validated, this leaves a headline contribution experimentally unverified. An experiment — even a synthetic one — would substantially strengthen the paper.

### Minor

- **4-augmentation baselines are unconvincing.** Both the stress-strain (Table 1) and path-signature (Table 2) experiments use only 4 random transformations for the data augmentation baseline. With 4 augmentations, the model receives only 5× the original data, which is unlikely to approximate group invariance well. While the performance gaps are large enough that the main conclusions likely survive (especially the order-of-magnitude gap in the stress-strain problem and the 37× gap in the Lorentz path-signature case), a stronger baseline (e.g., 100+ random transformations) would make the comparison more definitive.

- **TFENN baseline taken from literature without re-implementation.** Table 1 reports TFENN errors from Garanger et al. (2024) rather than re-implementing under identical conditions. While this is common practice, differences in train/test splits, hyperparameters, or evaluation protocols could affect the comparison.

- **No direct experimental comparison with Clebsch–Gordan–based methods (e3nn/escnn) on applicable O(d) problems.** The related work discusses e3nn/escnn as closely related approaches that also handle equivariant tensor functions via representation theory. While the stress-strain experiment includes TFENN (itself an equivariant method), a direct comparison on the O(d) path signature or sparse vector problem would help clarify the practical tradeoffs between the invariant-theory parameterization and the CG-based approach for practitioners.

### Trivial
None.

## Nice-to-Haves
- Runtime and parameter-count comparisons to help practitioners understand the practical overhead of the proposed method.
- Statistical significance tests (e.g., paired t-tests) for the main comparisons.
- A brief note explaining the practical difficulty of constructing a symplectic experiment and under what conditions the symplectic theory would be expected to yield improvements.

## Removed Points

These points were raised by one or more of the inputs but are removed with brief justification:

- **"No experimental comparison against any equivariant tensor method."** — Removed as factually incorrect. The stress-strain experiment (Table 1) compares directly against TFENN, which the paper describes as an equivariant method (line 243). The claim that zero equivariant baselines exist among the experiments is false.
- **"Stress-strain experiment does not test the core Contraction + Isotropic Tensor parameterization (Corollary 1)."** — Removed because the paper explicitly and appropriately uses Corollary 2 (eigenvalue-based) for this problem. This is a legitimate specialization of the same theory and does not undermine the paper.
- **"Sparse vector problem does not exercise the tensor-valued nature of the framework."** — Removed because it is a legitimate application of Corollary 1 (vector inputs → matrix output). The stress-strain experiment separately tests the symmetric-tensor-to-symmetric-tensor case via Corollary 2.
- **"Speculative fatal claims about whether results would survive with better baselines."** — Removed because the actual performance gaps in the tables are large enough that the pattern is clear even with weak baselines. Speculating about how much the gap would shrink is not a concrete identified flaw.
- **"Paper does not test whether equivariant architecture benefits beyond data augmentation."** — Partially addressed above (the 4-augmentation issue is kept as a minor weakness); the more extreme framing ("this comparison is artificially favorable") is removed because the gaps are orders of magnitude in several cases, making it unlikely that more augmentations would erase the advantage.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add at least one symplectic-group experiment**, even a synthetic one, to validate the headline claim.
2. **Strengthen the data augmentation baselines** to 100+ random transformations, or provide a sensitivity analysis showing that the gap saturates with fewer augmentations.
3. **Re-implement TFENN under identical conditions** or add a prominent caveat to Table 1 about the comparison.
4. **Include a brief runtime/parameter comparison** with a CG-based method on one O(d) problem to give practitioners a concrete sense of the tradeoffs.

## Score and Decision

The calibration system was unavailable (database files not found), so I proceed without retrieval-based anchors.

The paper makes a genuine theoretical contribution: it provides the first unified, ML-ready parameterization of equivariant tensor functions for O(d), the Lorentz group, and the symplectic group using invariant theory rather than representation theory. The mathematics is sound, the exposition is clear, and the experimental validation shows large and consistent improvements over non-equivariant baselines across three diverse problems.

The main weaknesses are: (1) the absence of a symplectic-group experiment despite prominent billing, (2) weak data augmentation baselines, (3) a literature-sourced rather than re-implemented baseline, and (4) the absence of direct comparison with CG-based methods on O(d) problems. None of these are fatal — the theoretical contribution stands on its own and the core empirical claims (equivariant >> non-equivariant) are well-supported — but they collectively prevent the paper from being a strong accept.

**Score: 6.5** — between borderline accept and accept. A solid paper with a clear theoretical contribution and convincing (if imperfectly controlled) experiments. Addressing the symplectic experiment gap and strengthening the baselines would bring it to the 7.5–8 range.

**Decision: Accept**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>