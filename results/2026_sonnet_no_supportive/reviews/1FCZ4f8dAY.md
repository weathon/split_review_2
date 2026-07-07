Now I have enough to draft the review. Let me proceed.## Final Review

## Summary
The paper develops universally expressive equivariant machine learning architectures for functions mapping tensors to tensors, covering the orthogonal group O(d), the indefinite orthogonal (Lorentz) group O(s,d−s), and the symplectic group Sp(d). The core theoretical contributions are Theorems 1 and 2 — unified invariant-theory characterizations of all polynomial (respectively entire) equivariant tensor maps — together with practically implementable Corollaries 1–3 for the vector-input special case. Experiments on stress-strain tensors in materials science, path signature estimation for time series, and sparse vector recovery demonstrate compelling empirical benefits.

---

## Strengths

- **Unified invariant-theoretic framework (Theorems 1 & 2).** A single algebraic recipe characterizes all polynomial equivariant tensor maps for O(d), O(s,d−s), and Sp(d) simultaneously. Prior CG-based methods (e3nn, escnn, Domina et al. 2025) handle only SO(d)/O(d) for d=2,3 and require group-specific harmonic analysis and CG coefficient computation. The invariant-theory approach naturally generalizes to Lorentz and symplectic groups where no standard spherical harmonics exist — a genuine broadening of the field's toolbox.

- **Directly actionable Corollary 1 (Eq. 11).** The vector-input specialization reduces equivariance to: compute pairwise inner products, feed them into MLPs to get scalar coefficients, take linear combinations of tensor products of inputs and Kronecker deltas. This requires no custom CUDA kernels or CG tables and is directly used in two of three experiments.

- **Stress-strain experiment (Table 1).** A 5–13× reduction in squared Frobenius error over TFENN across all dataset sizes. The ground-truth function (Eqs. 22–23) falls precisely within Corollary 2's scope, validating that the parameterization works in practice and outperforms a specialist equivariant method designed for this exact task.

- **Lorentz-group path signature result (Table 2).** MLP with the same number of parameters achieves 0.450; the equivariant model achieves 0.005 — a ~90× improvement. This is the cleanest demonstration that the Lorentz-group extension adds real empirical value beyond what CG-based methods can provide.

---

## Weaknesses

### Fatal
None.

### Major

- **Gap between general theory and experiments.** Theorems 1 and 2 characterize equivariant maps with arbitrary-order tensor inputs. However, all three experiments use only the vector-input corollaries (Corollary 1 or 3) or the symmetric-matrix eigenvalue reduction (Corollary 2). The paper itself notes (after Theorem 1) that the full general parameterization is computationally impractical for large tensor orders. This leaves the headline claim of handling "arbitrary tensor inputs" without any experimental instantiation. Even a small synthetic regression from genuine 2-tensor inputs (beyond what Corollary 2 captures) would close this gap and show Theorem 1 is usable, not just theoretically elegant.

- **Absence of CG-based baselines in O(d) experiments.** The Related Work explicitly states CG-based methods (e3nn, escnn, Domina et al. 2025) "should be equivalent" in computational and approximation power to the practical corollaries for O(d). Since the paper positions itself as an *alternative* parameterization, including at least one CG baseline in the stress-strain or path-signature O(d) experiment would confirm empirical comparability and validate the claimed equivalence. Their absence leaves this claim unverified.

### Minor

- **Section 6 Discussion does not acknowledge structured variation in Table 3.** The claim "The equivariant models outperform all non-equivariant baseline models" is accurate (comparing "Ours" against the MLP baseline across all rows, higher-is-better). However, the Discussion does not acknowledge that "Ours (Diag)" — a simpler, diagonal-norm variant — outperforms "Ours" under Diagonal and Identity covariance settings. The table caption partially explains this pattern, but the Discussion should explicitly frame this as a complementarity between equivariant models and SoS, rather than leaving the reader to piece this together from the caption. This would make the paper's narrative more honest and more informative.

- **Missing standard deviation in Table 2 (O(d), MLP augmented).** The entry 0.007 is reported without ±, while "Ours" reports 0.002 also without ±. The gap is small enough that variance estimates would help interpret whether the comparison is meaningful. All other entries have standard deviations.

- **Sparse vector equivariance justification deferred entirely to appendix.** The claim that the sparse vector problem is O(d)-equivariant is load-bearing for interpreting Table 3 results, yet is deferred entirely to Appendix J.2 with no in-text sketch. At least one sentence in Section 5 should explain the equivariance argument.

### Trivial
None.

---

## Nice-to-Haves

- Add a small synthetic experiment using genuine higher-order tensor inputs to instantiate Theorem 1 directly (e.g., learning a known O(d)-equivariant map from 2-tensor inputs beyond Corollary 2's eigenvalue structure).
- Report computational cost (FLOPs or wall-clock time) vs. baselines for at least Table 1, where the improvement is large, to help practitioners assess overhead.
- Clarify in the main text whether Corollary 2's reduction of O(d)-equivariant symmetric-matrix functions to permutation-equivariant eigenvalue functions is a known result (with citation) or a new observation.
- Clarify in the main text which applications require Levi-Civita terms (excluded from practical corollaries) and which do not, since this is a real restriction practitioners need to know about.

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"The Discussion claim is false" (harsh critic major weakness).** The critic asserts "'The equivariant models outperform all non-equivariant baseline models' is false for several rows." On inspection of Table 3 (higher is better), "Ours" beats "MLP baseline" (the only non-equivariant baseline) in *every* row. SoS is a structured algorithmic method with theoretical guarantees, not a "non-equivariant baseline model." "Ours (Diag)" appears to be an equivariant variant. The critic misidentifies SoS as a non-equivariant baseline. Demoted to a minor presentation note.
- **Reproducibility / hyperparameter details** — removed per hard rules.
- **Missing appendix proofs** — removed per hard rules (parser strips appendices from all papers; they exist in the original).
- **Missing related works** — removed per hard rules (no external source to verify existence).

---

## Novel Insights
The paper's most underappreciated observation is that invariant theory and Clebsch-Gordan decomposition are *dual routes* to the same class of equivariant functions for O(d), but the invariant-theory route extends almost for free to O(s,d−s) and Sp(d) — groups for which no convenient Fourier basis exists. This suggests a principled design principle: use invariant theory as the primary language for equivariant architectures whenever the symmetry group is non-compact or lacks a standard spherical harmonics theory. The path-signature Lorentz experiment concretely validates this idea, demonstrating a 90× improvement from Lorentz equivariance alone.

---

## Suggestions

1. Add one synthetic experiment with genuine higher-order tensor inputs to close the gap between Theorem 1 and the practical corollaries.
2. Add CG-based baselines (e.g., e3nn) to the O(d) experiments to empirically confirm the claimed equivalence.
3. Revise Section 6 Discussion to explicitly address the structured pattern in Table 3 (equivariant models vs. SoS under different covariance structures).
4. Add at least one sentence in Section 5 explaining why the sparse vector problem is O(d)-equivariant, rather than fully deferring to the appendix.
5. Report computational costs for at least the stress-strain experiment.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| `kyVzYpDxHg.md` | 5.75 | R1 | Earlier, narrower version of the same paper; only one experiment, no path signatures — current version is substantially stronger |
| `eOCvA8iwXH.md` | 7.00 | R1 | Neural Fourier Transform — accepted; elegant theory + clean experiments; comparable scope but stronger experimental coverage |
| `79FVDdfoSR.md` | 7.00 | R1/R2 | Characterization theorem for equivariant networks — accepted; purely theoretical contribution, less experimental breadth |
| `7PLpiVdnUC.md` | 6.50 | R1 | Lie algebra canonicalization — accepted; general Lie group equivariance for PDEs; comparable generality, experiments less dramatic |
| `p34fRKp8qA.md` | 6.83 | R2 | Lie group decompositions for equivariant networks — accepted; comparable theory depth and application scope |
| `gyfXuRfxW2.md` | 7.00 | R2 | Learning polynomial problems with SL(2,R) equivariance — accepted; equivariance for non-compact group + experiments |
| `64t9er38Zs.md` | 5.75 | R2 | Deep O(n)-equivariant hyperspheres — rejected; narrower scope and weaker theory |
| `tzpXhoNel1.md` | 4.25 | R1 | GRepsNets — rejected; overlapping theme but weaker theory/experiments |
| `NukRlEUICA.md` | 3.00 | R1 | Affine invariance in CNNs — rejected; much narrower, less rigorous |
| `SjufxrSOYd.md` | 8.00 | R1 | Invariant graphon networks — accepted; stronger theoretical depth, cleaner proofs |
| `0aaaM31hLB.md` | 5.25 | R1 | Learning symmetries through loss landscape — rejected; weaker theory |

**Bracketing:** Round 1 placed the paper between 5.75 (previous version, rejected) and 7.00 (accepted equivariant characterization papers). Round 2 confirmed the 6.0–7.0 range. Accepted papers at 7.0 (e.g., Neural Fourier Transform, Characterization Theorem) tend to have either cleaner theory-only contributions or more comprehensive experimental validation. The current paper's major gap — the general theorem not directly instantiated in experiments, and absence of CG baselines — pulls it slightly below the clean 7.0 cluster. The two strong experiments (stress-strain and Lorentz path signature) and the genuine extension to non-compact groups push it above the 5.75 rejection of the prior version.

**Final score: 6.5** — Borderline Accept. The paper makes a genuine theoretical contribution extending equivariant tensor learning to Lorentz and symplectic groups, demonstrates compelling empirical results in two of three experiments, and is substantially more complete than its prior version. The primary unresolved gap (no experiment for the general theorem) and absent CG baselines are real but not fatal. The paper adds value the community lacks elsewhere.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>