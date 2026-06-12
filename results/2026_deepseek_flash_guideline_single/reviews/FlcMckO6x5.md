## Summary

This paper makes three contributions to separable neural networks (SepNNs): (1) a universal approximation theorem for multivariate SepNNs (D≥2) covering CP, TT, and Tucker decompositions, extending prior bivariate results; (2) an NTK analysis showing that the SepNN's kernel converges to a deterministic kernel only when both width and rank diverge, and to a random kernel under fixed rank; (3) a separable preconditioned gradient descent (SepPGD) method that achieves O(nD) complexity for n^D grid-structured training samples, compared to O(n^D) for prior NTK-based PGD.

## Strengths

- **Clean universal approximation theorem extending prior art (Theorem 1).** Prior work (Cho et al., 2023) established approximation for bivariate SepNNs (D=2). This paper extends to general D≥2 and three tensor decomposition architectures (CP, TT, Tucker). The proof — combining Stone-Weierstrass with universal approximation — is elegant and provides a unified treatment. This is a genuine advance over the state of the art.

- **Non-trivial NTK derivation revealing rank-dependent regime distinction (Theorem 2, Corollary 1).** The paper derives the SepNN's NTK (Lemma 1) and shows that under infinite width, the NTK converges to a deterministic kernel only when the rank also diverges, whereas with fixed rank it converges to a random kernel. This distinction does not arise in standard MLP NTK analysis and is conceptually interesting. The empirical confirmation in Figure 1(a)-(c) is credible.

- **SepPGD complexity reduction is substantial (Section 4, Table 1).** Reducing the preconditioner cost from O(n^D) to O(nD) for grid-structured data is not incremental — it can be the difference between feasible and infeasible. The core insight of decomposing the large preconditioner into D smaller ones operating on factor networks is well-motivated. Lemma 2's formal equivalence to classical NTK-based PGD for D=2 provides firm theoretical grounding for the approach.

## Weaknesses

### Fatal
None.

### Major

1. **The "provably" claim for spectral bias alleviation is not supported by the analysis presented.** The abstract states SepPGD "provably adjusts the eigenvalue distribution of NTK matrix, effectively alleviating spectral bias," and the introduction (line 50) repeats this. However, the analysis in Section 4 does not constitute a proof:

   - Lemma 2 establishes equivalence between SepPGD and classical PGD *only for D=2*. The extension to D>2 is handwaved: "It is believed that the result in Lemma 2 (and the analysis following) can be readily extended" (line 201).
   - The spectral improvement argument requires that the sum-of-Kronecker-product matrix \tilde{K} is "close to" the true NTK matrix K, referenced to Lemma 3 (in the appendix). Even if Lemma 3 exists and establishes norm proximity, the step from "close in norm" to "K\tilde{S} has better condition number than K" is not logically justified — proximity of two matrices does not imply that multiplying by \tilde{S} improves the spectrum of one relative to the other in any controlled way.
   - The text itself uses hedged language ("could provably," "can possibly be verified," "would have better spectrum"), which conflicts with the definitive claim in the abstract and introduction. This gap between advertised rigor and actual evidence undermines the paper's central algorithmic claim.

2. **Experimental evaluation conflates cost advantage with preconditioning quality.** The convergence curves (Figure 2) plot MSE vs. wall-clock time, which inherently favors SepPGD due to its cheaper per-iteration cost. While SepNN+MSK (classical NTK-based PGD from Geifman et al.) is included as a baseline, per-iteration convergence curves are not reported, making it impossible to isolate whether SepPGD provides better preconditioning *per step* or simply wins on lower cost. Additionally, no ablation studies on key hyperparameters (eigenvalue truncation count k, preconditioner update frequency) appear in the main paper, making it difficult to assess robustness of the method.

### Minor

1. **NTK theory-practice disconnect.** The NTK analysis is asymptotic (W,R → ∞ or W→∞ with fixed R), while SepPGD is used with finite width and typically small rank. The paper acknowledges this gap in Remark 3 but does not resolve it. This leaves SepPGD's theoretical motivation somewhat disconnected from its practical operating regime.

2. **Theorem 1 lacks approximation rates.** The universal approximation theorem guarantees existence of some rank R achieving ε-accuracy but provides no bound or rate. For practitioners, knowing how large R must grow with desired accuracy would be more useful. Without rates, the theorem provides limited actionable insight.

3. **Spectral analysis for D>2 is speculative.** The paper states "It is believed that the result in Lemma 2 (and the analysis following) can be readily extended to multivariate cases D > 2" without concrete justification or sketch of how the Kronecker-sum structure generalizes.

### Trivial
None.

## Nice-to-Haves

- Per-iteration convergence curves alongside wall-clock curves to distinguish preconditioning quality from cost advantage.
- Ablation studies on k (number of eigenvalues clipped) and preconditioner update frequency.
- Approximation rate bounds for Theorem 1 (even coarse bounds on required rank).

## Removed Points

These points were removed from the input review with justification:

- **"Missing baseline: SepNN+classical NTK-based PGD"** — The paper explicitly compares "SepPGD with the classical NTK-based PGD, the modified spectrum kernel (MSK) (Geifman et al., 2024; Shi et al., 2025)" and the figures show "SepNN (MSK)," which IS SepNN trained with classical NTK-based PGD. This criticism is factually incorrect. *Removed per hard rules.*

- **"Missing baseline: mini-batch PGD (Shi et al., 2025)"** — The paper's method is full-batch, and the primary complexity comparison (Table 1) acknowledges this variant. The absence of this experimental comparison is a nice-to-have, not a weakness. *Demoted to nice-to-have.*

- **"No ablation studies on critical hyperparameters" elevated to Critical Issue #4** — Appendix Table 3 is referenced as showing empirical results for small rank, partially addressing this concern. The main paper still lacks ablations on k and update frequency, but this is subsumed into Major weakness #2 rather than a separate critical issue. *Merged into Major #2.*

- **"Gap between theory and practice" elevated to Critical Issue #3** — Remark 3 explicitly discusses this limitation and acknowledges it as a promising future direction. *Demoted to Minor #1.*

- **Generic nitpicks about missing appendix content or proofs** — The parser strips appendix sections from all papers; they exist in the original submission. *Removed per hard rules.*

- **"Approximation rates needed"** — The reviewer raised this as it relates to Theorem 1. This is a valid observation but it's standard for universal approximation theorems to state existence without rates. Kept as Minor #2 (not a critical issue).

## Novel Insights

None beyond the paper's own contributions. The reviews surface the tension between SepPGD's advertised "provably" guarantee and the actual argument presented, which relies on a chain of unverified suppositions. This observation is correct and actionable but does not constitute a novel insight beyond what the paper itself implicitly reveals to a careful reader.

## Suggestions

1. **Reconcile claims with evidence.** Replace "provably adjusts" in the abstract and introduction with language that accurately reflects what is proven: equivalence to classical PGD for D=2 (Lemma 2) and the O(nD) complexity advantage. Be transparent that the spectral improvement for D>2 and the full logical chain from proximity to spectrum improvement rely on unverified assumptions.

2. **Add per-iteration convergence curves.** Reporting MSE vs. iteration number alongside wall-clock time would allow readers to distinguish preconditioning quality from cost advantage, strengthening the paper's claims about spectral bias alleviation.

3. **Ablate k and preconditioner update frequency.** Even a brief ablation would substantially increase confidence in SepPGD's robustness and provide practical guidance for users.

## Score and Decision

**Round 1 bracket: 5.0–6.5.** Based on calibration against 13 anchor papers.

**Anchor papers used for calibration:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| TNYLCF7vZA.md (INR spectral bias) | 4.75 | R1, R2 | Most directly relevant. Rejected due to overclaiming and unclear positioning. Current paper has stronger theory but similar overclaiming issues. |
| 2C3CWCPxNS.md (PINN preconditioning) | 5.00 | R1, R2 | Had a fatal flaw (central theorem considered vacuous by one reviewer). Current paper has no fatal flaw. |
| 5EtSvYUU0v.md (NTK/NNGP unification) | 6.00 | R1 | Had presentation issues and unclear definitions. Current paper is clearer and more self-contained, though less ambitious. |
| 8wAL9ywQNB.md (Generalization bounds) | 6.00 | R1 | Mixed reviews, less directly comparable. Current paper has cleaner theoretical contributions. |
| dpDw5U04SU.md (Min width for universal approx) | 7.00 | R1 | Clean focused theory paper, accepted. Current paper has broader scope but less depth in individual contributions. |
| 8Ju0VmvMCW.md (lpNTK) | 6.67 | R2 | Clean NTK contribution with solid experiments, accepted. Current paper has more breadth but weaker empirical validation for the algorithmic contribution. |
| G2Lnqs4eMJ.md (High-dim approx) | 2.50 | R1 | Weak paper, strong reject. Current paper is far stronger. |
| Oqk1Ui6m0n.md (Hessian-free NGD) | 5.00 | R2 | Similar optimization method paper, comparable quality. |
| 92btneN9Wm.md (SPDER) | 6.33 | R2 | INR architecture paper, accepted. Current paper has more theoretical depth but less polished empirical story. |
| fUz6Qefe5z.md (NTK with derivative labels) | 3.00 | R2 | Weak NTK paper, rejected. Current paper's NTK analysis is cleaner. |
| kOtFuzoA93.md (Novel kernel models) | 4.00 | R2 | Rejected. Current paper is stronger. |
| bWz8aOPwsJ.md (NTK trace evolution) | 3.75 | R2 | Rejected. Current paper is substantially stronger. |
| xpmDc76RN2.md (Operator networks) | 2.33 | R2 | Weak paper. Current paper is far stronger. |

**Final calibration:** This paper has two solid theoretical contributions (approximation theorem, NTK regimes) and a well-motivated algorithmic idea with a genuine complexity advantage. However, the headline "provably" claim for SepPGD is unsupported by the analysis, and the experimental evaluation would benefit from per-iteration comparisons and ablation studies. The paper is stronger than typical 4–5 papers in this area (like TNYLCF7vZA or Oqk1Ui6m0n) but falls short of the clean exposition and thorough validation expected of a clear accept (like 8Ju0VmvMCW at 6.67 or dpDw5U04SU at 7.00).

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>