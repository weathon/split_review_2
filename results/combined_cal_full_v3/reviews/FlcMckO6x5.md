## Summary

This paper makes three contributions to the theoretical understanding of separable neural networks (SepNNs): (1) a universal approximation theorem (Section 2) proving that CP, TT, and Tucker SepNNs can approximate any continuous multivariate function, proven via Stone-Weierstrass; (2) an NTK analysis (Section 3) establishing two asymptotic regimes (deterministic NTK under infinite width+infinite rank, random NTK under infinite width+fixed rank) with spectral bias characterization; and (3) a separable preconditioned gradient descent method (SepPGD, Section 4) that leverages the separable structure to reduce preconditioner application from O(n^D) to O(nD) for grid data, with empirical validation on KRR, INRs, and PINNs.

## Strengths

- **Universal approximation theorem (Theorem 1) is a genuine contribution.** The proof technique — using Stone-Weierstrass to show density of the separable function class A in C(X), then approximating univariate components with MLPs — is elegant and unifies CP, TT, and Tucker forms under a single argument. This cleanly extends prior bivariate results (Cho et al., 2023) to D ≥ 2 with a simpler proof than prior activation-specific approaches.

- **The NTK regime analysis (Lemma 1, Theorem 2, Corollary 1) provides a genuinely novel characterization.** The decomposition of the SepNN NTK into a sum over factor MLP NTKs (Lemma 1) is non-trivial, and the distinction between the deterministic NTK (infinite width + infinite rank) and random NTK (infinite width + fixed rank) regimes is well-motivated by practice, since rank is typically kept small for generalization. The empirical validation (Figure 1) with ten runs and variance reporting supports the theory.

- **The computational complexity of SepPGD (Remark 4, Table 1) is genuinely impressive.** Reducing preconditioner application from O(n^D) to O(nD) for grid-structured data, and construction from O(n^{3D} + n^{2D}P) to O(D(n³ + n²P)), is a dramatic efficiency gain when D ≥ 2. The SepPGD algorithm itself is clever and its complexity advantage is the paper's strongest practical selling point.

## Weaknesses

### Fatal
None.

### Major

- **The "provably adjusts NTK spectrum" claim is not supported by the evidence presented.** The abstract and introduction state that SepPGD "provably adjusts the eigenvalue distribution of NTK matrix," but the main text's argument (lines 200-201) has several gaps. (i) Lemma 2 (the equivalence to classical PGD) is proven only for D=2; extension to D>2 is stated as "it is believed" — a statement of belief, not a proof. (ii) The spectral argument chains from "S̃ has better spectrum than K̃" to "K·S̃ has better spectrum than K" by supposing K̃ ≈ K (referenced to Lemma 3 in the appendix), but even assuming this approximation holds, the inference about the product K·S̃ having better conditioning than K is not rigorously carried out. (iii) The paper's own language vacillates: the main text says "could provably" while the abstract and introduction assert "provably" without hedging. The SepPGD method may well work (experiments suggest it does), and its complexity advantage stands regardless, but the framing as a *provable* spectral bias alleviation method is stronger than what the evidence supports. This is the paper's most significant weakness and requires recalibration of claims.

### Minor

- **No error bars or variance reporting for any method-evaluation experiment.** The convergence curves in Figures 2 and 4, and the quantitative PSNR/IoU/MSE results in Figures 3-4, appear to be single-run point estimates without standard deviations or confidence intervals. Given that some improvements are modest (e.g., PINN MSE 0.042 → 0.037, surface IoU 0.983 → 0.992), statistical significance cannot be assessed. The only figure with variance reporting is Figure 1 (NTK theory validation), which uses ten runs.

- **Scope mismatch between the paper's broad title and the actual technical scope of the latter two contributions.** The NTK analysis (Lemma 1, Theorem 2, Corollary 1) and SepPGD (Definition 1) are developed only for CP SepNNs, not TT or Tucker. The paper acknowledges this (Footnote 1: "we believe it can be readily extended"), but two of the three advertised contributions apply only to a subset of SepNN architectures, while the universal approximation theorem genuinely covers all three.

- **The KRR experiments' baseline specification is unclear.** The text says it compares against "the classical NTK-based PGD" and "the modified spectrum kernel (MSK)," but the figures display "MLP (MSK)" and "SepNN (MSK)" without a distinct "PGD" baseline line. Since Geifman et al. (2024) propose both MSK and a separate PGD method, it is ambiguous which is being compared, making it harder to assess fairness.

### Trivial

- **Definition 1 (Equations 7-8) is notationally dense** with nested ⊕, ⊗, unfold_d, ×_d operators. A pseudocode algorithm box alongside the mathematical definition would substantially improve clarity and reproducibility.

## Nice-to-Haves

- Include SepNN(PGD) baseline for a small D=2 problem to empirically validate Lemma 2's equivalence and implementation correctness.
- Demonstrate SepPGD on at least one problem with D > 3 to substantiate the O(nD) scalability claim (the paper shows D=2 and D=3 but not higher).
- Provide an empirical plot or analysis of when the Kronecker approximation K̃ ≈ K breaks down as a function of width, rank, and D.
- Discuss practical limitations of the O(n^{D-1}) term in Equation (8) for large n or D.

## Removed Points

*These points from the input review are flagged as removed; treat them with caution:*

1. **"Table 1 comparison is misleading about Hessian methods"** — REMOVED. The table header explicitly states "in terms of applying the preconditioner." The Hessian row's O(P) is the per-iteration application cost, consistent with all other rows. Construction costs are discussed separately in Remark 4 for all methods.

2. **"No experiments on D > 2 are presented"** — REMOVED as factually incorrect. The PINN experiments on the 3D diffusion equation use D=3 (3D spatial coordinates). The correct observation (D > 3 not shown) is moved to Nice-to-Haves.

3. **"Footnote 3 about O(n^{D-1}) being hand-wavy"** — REMOVED. The paper transparently acknowledges this additional cost and reasonably explains why it is not the dominant term relative to NTK construction costs.

4. **"SepPGD not defined for non-grid inputs"** — REMOVED. The paper discusses non-grid input formulation on line 201: "Lemma 2 can also be extended to non-grid inputs."

5. **"Provably claim is fatal/structural"** — DEMOTED from fatal to major. The overclaiming is a significant presentation problem but does not invalidate the paper's core contributions (the algorithm itself is sound, the complexity analysis is correct, and the theoretical contributions in Sections 2-3 stand independently).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Recalibrate the "provably" language throughout the paper.** Present SepPGD as an efficiently computable preconditioner motivated by NTK structure, with proven equivalence to classical PGD for D=2 (Lemma 2). Drop the "provably" from the abstract and introduction, or replace with precise statements about what is actually proven.
- Add error bars / variance reporting to all quantitative experimental results.
- Add a pseudocode algorithm box for SepPGD alongside Definition 1.
- Clarify the baseline specification in KRR experiments: explicitly state which methods (PGD vs MSK) are being compared and whether they are applied to MLP or SepNN.

## Score and Decision

**Calibration summary:** Round 1 bracketing (5.5–7.5) was based on comparing the paper's items (strength favorability 9.87–10.92, weakness favorability 2.32–3.91) against anchors in each score band. Round 2 narrowing compared against four itemized anchors: "Connecting NTK and NNGP" (6.00, rejected; weaker presentation rigor than the reviewed paper), "lpNTK" (6.67, accepted; comparable strength/weakness profile but the reviewed paper has cleaner theory), "Generalization Bounds for KAN" (6.20, accepted; similar architecture-specific theory paper but the reviewed paper has broader experiments), and "Debiasing Mini-Batch Quadratics" (6.75, accepted; stronger execution but narrower scope). The reviewed paper's strength favorability (10+) is at the upper end of these anchors, while its main weakness on overclaiming (2.33) is comparable to the most significant weaknesses in the accepted anchors. The paper's two theoretical contributions are well-executed and independently valuable. The SepPGD algorithm is computing-efficient and empirically effective; only its "provably" framing is overclaimed. On balance, the paper merits acceptance with required revisions to recalibrate the SepPGD claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>