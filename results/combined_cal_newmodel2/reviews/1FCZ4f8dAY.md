## Summary

This paper develops a general theoretical framework for parameterizing equivariant tensor functions under the diagonal action of the orthogonal group O(d), the indefinite orthogonal group O(s,d−s) (including the Lorentz group), and the symplectic group Sp(d). Using invariant theory, Theorem 1 and Theorem 2 characterize polynomial/entire equivariant functions from tuples of tensors to tensors. Corollaries 1 and 3 translate this into a practical architecture: a linear combination of (tensor products of input vectors and isotropic tensors) whose coefficients are functions of pairwise inner products. Experiments on stress–strain tensor prediction, path signature approximation, and sparse vector recovery demonstrate the framework across diverse domains.

## Strengths

- **A genuinely general theoretical framework for equivariant tensor functions.** The paper provides a clean characterization (Theorem 1, Theorem 2) of polynomial/entire equivariant functions under O(d), O(s,d−s), and Sp(d), without requiring precomputation of Clebsch–Gordan coefficients. This covers groups beyond SO(3)/O(3) with d=2,3, handles non-symmetric tensors, mixed-parity tensors, and multiple input tensors — generalizing beyond existing CG-based methods (e3nn, escnn) and the symmetric-tensor-only results of Kunisky et al. (2024).

- **Corollaries 1 and 3 provide a directly implementable architectural recipe.** The parameterization — a linear combination of (tensor products of input vectors and isotropic tensors) whose coefficients are functions of pairwise inner products — is something a practitioner can implement with a shared MLP. The explicit complexity estimate O(k'! n^{k'} (Q d n^2 + d^{k'})) is given, with honest acknowledgment that it is practical only for small output rank k'.

- **Diverse experimental domains.** Three problems from materials science (stress–strain tensors), time series analysis (path signatures), and theoretical computer science (sparse vector recovery) test the framework on quite different kinds of data, supporting the generality claim. The method outperforms non-equivariant baselines by large margins in most settings (e.g., 4×10⁻⁶ vs 1.6×10⁻⁴ on stress–strain at n=5000; 0.002 vs 0.007 for augmented MLP on path signature O(d)).

## Weaknesses

### Fatal
None.

### Major

- **The TFENN comparison in Table 1 uses published numbers rather than re-implemented baselines.** The paper states: "The TFENN errors are the results reported in Garanger et al. (2024)." The baseline was not re-run under the same train/val/test split, hyperparameters, or data generation pipeline. No variance is reported for TFENN, so statistical significance cannot be assessed. Since the stress–strain results in Table 1 are the paper's strongest quantitative results, this weakens the empirical foundation of the main experimental claim.

### Minor

- **The data augmentation baseline uses only 4 random rotations/transformations.** In both the stress–strain experiment (Table 1) and the path signature experiment (Table 2), the augmented MLP baseline uses 4 random transformations. Standard practice in equivariance benchmarking uses substantially more augmentations; a stronger augmentation baseline could narrow the apparent advantage of explicit equivariance.

- **The sparse vector results (Table 3) show inconsistent behavior between architectural variants that is under-analyzed.** The "Ours" and "Ours (Diag)" variants swap in performance across settings (e.g., Accept/Reject Random: Ours 0.938 vs Ours(Diag) 0.493; Accept/Reject Diagonal: Ours 0.465 vs Ours(Diag) 0.589). The method does not uniformly outperform baselines across all 12 settings, and the reasons for the architectural variant differences are not explained. This limits the interpretability of the empirical contribution.

- **No runtime or memory benchmarks are reported.** The paper provides a complexity analysis acknowledging practical limitations (factorial scaling with output rank k') and claims comparable efficiency to e3nn/escnn for Corollaries 1 and 3, but no actual timing or memory measurements are given to substantiate this. Concrete benchmarks would help practitioners assess the trade-off.

- **The paper lacks a limitations section or discussion of computational constraints.** The method has clear limitations — restriction to small output rank k', factorial complexity, reliance on Stone–Weierstrass for universality rather than a direct characterization of continuous equivariant functions (Remark 1), and absence of experiments for the symplectic/Lorentz groups despite their theoretical treatment. These are not discussed.

- **Some experimental details are missing from the main text.** For the path signature task, the number of sampled points n, truncation level M, and ambient dimension d are not reported in the main text. The practical implications of the two-level approximation (Stone–Weierstrass → polynomial → MLP) and how approximation error compounds are not discussed.

### Trivial
None.

## Nice-to-Haves

- Re-implement the TFENN baseline under identical conditions, or provide evidence that the data generation and evaluation protocol match those of Garanger et al. (2024).
- Show an augmentation-strength-vs-performance curve (4, 10, 50, 200 transformations) for at least one experiment to demonstrate robustness of the advantage.
- Provide runtime, memory, and parameter-count comparisons for all three experiments.
- Analyze the "Ours" vs "Ours (Diag)" discrepancy in the sparse vector task (e.g., which inner-product pairs the learned MLP weights prioritize, or what structural differences drive the performance gap).
- Add a limitations section discussing the practical scope of the method.
- Clarify when Levi-Civita symbols appear in Corollary 1 (or why they do not).

## Removed Points

Points flagged for removal, treated with caution:

- **"MLP outperforms Ours in multiple rows of Table 3"** — REMOVED: a careful check shows Ours wins in 6/12 settings, ties/edges MLP in 2 more, and the reviewer overstated the extent of MLP superiority.
- **"d_F / d_F parser artifact in Table 2 metric"** — REMOVED: this is a parser artifact, not a paper issue.
- **"Bernoulli-Gaussian exception contradicts paper's narrative"** — REMOVED: the paper explicitly addresses this exception and explains why it is consistent with the narrative (high sparsity → SoS assumptions met).
- **"Universally expressive claim is misleading"** — REMOVED: Remark 1 adequately qualifies this.
- **"Two-level approximation practical implications not discussed"** — demoted to Minor (kept but softened).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Re-implement TFENN under identical conditions, or use a publicly available implementation to ensure fair comparison.
2. Report an augmentation-strength-vs-performance curve for at least one experiment to demonstrate that the advantage over data augmentation is robust.
3. Provide runtime and parameter-count benchmarks for all experiments.
4. Analyze the sparse vector task more deeply: what drives the Ours vs Ours(Diag) discrepancy, and under what conditions does the method underperform?
5. Add a limitations section.
6. Report key experimental parameters (n, M, d) for the path signature task in the main text.

## Score and Decision

**Calibration Anchors Used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| .../kyVzYpDxHg.md (predecessor paper) | 5.75 | 1 | Yes | Same theoretical core but fewer experiments. Current paper adds stress–strain and path signature tasks, improving over this version. |
| .../tzpXhoNel1.md (GRepsNet) | 4.25 | 1 | Yes | Broader group coverage but weaker theoretical characterization. Current paper has stronger theory but narrower scope. |
| .../soaOqFTaHJ.md (EKAN) | 4.00 | 1 | Yes | Incremental over EMLP. Current paper's theory is more novel. |
| .../79FVDdfoSR.md (Characterization Theorem) | 7.00 | 1 | Yes | Pure theory paper accepted at ICLR. Current paper has comparable theoretical depth with more experiments but less clean empirical validation. |
| .../vDp6StrKIq.md (Beyond Canonicalization) | 6.33 | 2 | Yes | Applied O(d)-equivariant paper accepted at ICLR. Current paper has stronger theory but weaker experimental rigor. |
| .../gyfXuRfxW2.md (SL(2,R) Equivariance) | 7.00 | 2 | Yes | Theoretical paper with surprising non-universality result. Current paper's theory is less surprising but more generally applicable. |

**Bracketing:** Round 1 placed the paper in [5.5, 7.0] based on similarity to the predecessor paper (5.75), GRepsNet (4.25), and Characterization Theorem (7.00). Round 2 narrowed to [5.75, 6.5] by comparing against accepted papers at 6.33 (Beyond Canonicalization) and 7.00 (SL(2,R) Equivariance / Characterization Theorem).

**Favorability comparison:** The paper's strengths (favorability 13.0–14.7) are competitive with the 7.00 anchors, indicating genuinely strong theoretical value. However, its major weakness (TFENN comparison, favorability 1.45) and the "no limitations section" weakness (favorability 1.08) are significantly worse than the corresponding weaknesses of accepted anchors. The predecessor paper at 5.75 had weaker strengths but also lacked this particular comparison issue. The current paper's additional experiments raise it above 5.75, but the TFENN issue keeps it below the 6.33–7.00 accepted papers.

**Final score: 6.0** — Borderline accept. The theoretical contribution is genuine, general, and practically implementable. The experimental validation, while strong in breadth, is weakened by the TFENN comparison issue and several minor gaps. These are addressable with additional experiments.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>