Now I have a solid set of calibration anchors. Let me write the final review.

## Summary

This paper makes three contributions to separable neural networks (SepNNs): (1) a universal approximation theorem for multivariate (D≥2) CP, TT, and Tucker SepNNs; (2) an NTK analysis showing two distinct regimes (deterministic kernel under infinite width+infinite rank, random kernel under infinite width+fixed rank); and (3) a separable preconditioned gradient descent (SepPGD) algorithm that exploits the separable structure to apply O(nD) preconditioning for n^D grid-structured training samples.

## Strengths

1. **The universal approximation theorem (Theorem 1) is a genuine theoretical advance.** Prior work only covered bivariate (D=2) SepNNs via orthogonal basis constructions. This paper extends to multivariate SepNNs with D≥2 for CP, TT, and Tucker architectures using a clean Stone-Weierstrass proof strategy. The proof sketch is clearly described and constitutes a systematic advance over Cho et al. (2023).

2. **The discovery of two distinct NTK regimes — deterministic under infinite rank, random under fixed rank — is novel and practically relevant.** Since SepNNs are used with small rank in practice, the observation that the NTK remains random (does not converge to a deterministic kernel) in that regime is non-obvious. The empirical validation in Figure 1 provides reasonable support, and the paper honestly acknowledges the limitation this imposes on convergence analysis (Remark 3).

3. **The computational complexity argument for SepPGD (O(nD) vs. O(n^D)) is clearly correct and impactful.** For grid-structured data, applying D separate n×n preconditioners rather than one n^D×n^D preconditioner is a genuine efficiency gain. Table 1 makes this comparison transparent, and the paper validates the practical advantage by plotting MSE vs. wall-clock time.

## Weaknesses

### Major

1. **The "provably" claim about spectral bias alleviation is unsupported.** The abstract and contributions list state that SepPGD "provably adjusts the eigenvalue distribution of NTK matrix." However, the paper's own reasoning in Section 4 (line 201) uses speculative language: "This can possibly be verified," "We can ultimately show that K\tilde{S} has better spectrum than K," and concludes "This is left for future research." The chain of reasoning would require: (i) showing that K (the true NTK) is close to \tilde{K} (Kronecker-sum kernel), (ii) showing that K\tilde{S} has better conditioning than K. Neither step is proven; the paper even acknowledges the second is future work. The word "provably" in the abstract and contributions overstates what is actually established, which is a heuristic motivated by linear algebra intuition.

### Minor

2. **PINN experiments lack preconditioning baselines.** For the PINN experiments (Figure 4), SepPGD is compared only against plain PINN and SepPINN (without preconditioning). No comparison against PINN with NTK-based preconditioning (Geifman et al., 2024; Shi et al., 2025) or other spectral bias mitigation methods is provided. Since the paper motivates SepPGD as more efficient than prior PGD methods, their absence in the PINN evaluation weakens this claim. (Note: the KRR and INR experiments do include MSK baselines, so this gap is specific to the PINN results.)

3. **No variance or error bars for experimental results in Figures 2-4.** The convergence curves and final metrics (MSE, PSNR, IoU) are presented without error bars or multiple-seed statistics. While Figure 1 reports variance over seeds, the main experimental plots do not, making it impossible to assess the statistical reliability of the reported improvements.

4. **NTK analysis covers only CP SepNN with two-layer factor MLPs.** The approximation theorem covers CP, TT, and Tucker architectures, but the NTK analysis (Lemma 1, Theorem 2, Corollary 1) is developed only for CP SepNN with two-layer factor MLPs. The paper notes these are "readily extended" (footnote 1, Remark 1), but the analysis as presented is narrower than the title and framing suggest.

### Trivial

5. **Definition 1 (equations 7-8) is dense and notationally heavy.** The construction of M_d uses nested \bigoplus, \bigotimes, unfold_d, and \times_d operators. While the D=2 case in Lemma 2 provides intuition, the general definition is hard to parse on first reading.

## Nice-to-Haves

- A bound on how rank R must scale with ε and D in Theorem 1 would increase practical utility (though the paper correctly notes this is standard for universal approximation theorems).
- A wall-clock breakdown of preconditioner construction vs. application costs would help quantify when the O(nD) advantage translates to real speedup in practice.
- Extending the NTK analysis to TT/Tucker architectures, even as a brief discussion of why it does not straightforwardly extend, would match the paper's scope.

## Removed Points

These points from the input review are flagged for removal. Treat them with caution:

1. **"Neither [Geifman et al. nor Shi et al.] is actually run as a baseline"** — REMOVED (factually incorrect): The paper does compare against "classical NTK-based PGD" and "MSK" in the KRR and INR experiments (Fig. 2, line 221), which are the methods from those works. The PINN-specific gap is retained as Weakness #2.

2. **"The Kronecker product identity does not directly decompose a sum of Kronecker products"** — REMOVED (demoted): The identity applies to each term in \tilde{S} = S_1⊗I_n + I_n⊗S_2 separately. The paper's approach of handling each term via vec(ABC) is standard and valid. The real gap is the spectral argument, not the Kronecker algebra.

3. **"No wall-clock times for preconditioning steps"** — REMOVED: The paper plots MSE vs. execution time (Fig. 2, Fig. 4), which captures overall wall-clock performance.

4. **"The 1/√R scaling factor may change function approximation capacity"** — REMOVED: Footnote 1 explicitly states the scaling "does not affect the universal approximation Theorem 1."

5. **"No bound on how large R must be as a function of ε"** — REMOVED: The critic acknowledges this is standard for universal approximation theorems; it is an inherent limitation, not a flaw.

6. **"The paper should clarify how often grid-input scenarios arise"** — REMOVED: Footnote 2 already addresses this ("coordinate grids of images in INRs... grid collocation points in PINNs").

## Novel Insights

The reviewer synthesis surfaces one insight not fully articulated in the paper itself: the paper's strongest claim ("provably alleviates spectral bias") is contradicted by the paper's own hedging ("This is left for future research"). This disconnect means the paper would be better served by presenting SepPGD as an empirically effective method with heuristic spectral motivation, rather than overclaiming theoretical guarantees. The approximation theorem and NTK regime discovery stand on their own as solid contributions independent of this issue.

## Suggestions

1. Remove or replace "provably" in the abstract and contributions (e.g., with "empirically effective" or "heuristic") or provide a complete theoretical proof of the spectral bias alleviation claim.
2. Add NTK-based preconditioning baselines (Geifman et al./Shi et al.) to the PINN experiments.
3. Report variance over at least 3-5 random seeds for all experimental figures.
4. Consider clarifying in the title or framing that the NTK analysis is for CP SepNNs specifically.

## Score and Decision

### Calibration Anchors

All retrieved papers from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| TNYLCF7vZA (Inductive Gradient Adjustment) | 4.75 (Reject) | 1 | Similar topic (NTK-based preconditioning for spectral bias in INRs). Weaker paper — overlapping contribution with prior work, unclear writing. Current paper has stronger, more novel theory. |
| 2C3CWCPxNS (Preconditioning for PINNs) | 5.00 (Reject) | 1 | Similar topic (preconditioning for PINNs). Had actual mathematical flaws in core theorem. Current paper's theory is sounder; its weakness is overclaiming, not incorrectness. |
| VEJzjAvaIy (Divergence of NTK in Classification) | 5.75 (Accept) | 1 | Pure NTK theory paper. Sound but unsurprising result. Current paper has broader scope and more experimental validation. |
| 5EtSvYUU0v (Connecting NTK and NNGP) | 6.00 (Reject) | 1 | Theoretical unification with poor presentation and missing rigorous definitions. Current paper has cleaner presentation and more concrete theorems. |
| S04xvGXjEs (Collective variables of NTK) | 6.00 (Reject) | 1 | Empirical NTK study with limited novelty and unclear practical utility. Current paper has stronger theoretical contributions. |

### Bracket Analysis

**Round 1 bracket**: [5.5, 6.5]

The paper sits above TNYLCF7vZA (4.75) and 2C3CWCPxNS (5.00) because its theoretical weaknesses are about overclaiming rather than mathematical error, and its primary contribution (the approximation theorem) is genuinely novel and cleanly proven. It is comparable to 5EtSvYUU0v (6.00, Reject) and S04xvGXjEs (6.00, Reject) in overall quality — papers with real contributions undermined by one significant issue. The paper's approximation theorem and NTK analysis are its strongest assets; the main liability is the unsupported "provably" claim. If the authors fix this overclaim and address the experimental gaps, the paper would move comfortably into the 6-7 range.

**Final score**: 5.5 — The approximation theorem and NTK analysis are solid contributions, and the SepPGD complexity argument is clearly correct. However, the central "provably" claim about spectral bias alleviation is not established, the experimental evaluation has gaps (missing PINN baselines, no error bars), and the NTK analysis is narrower than the paper's framing suggests. A revision that softens the claims and fills the experimental gaps would warrant a higher score.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>