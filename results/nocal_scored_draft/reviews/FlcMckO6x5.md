Based on the favorability signals (strengths consistently 0.89-1.00, weaknesses at 0.00-0.33 for major issues, 0.59-0.66 for minor), the paper has clear theoretical value but the experimental statistical rigor and the overclaimed "provably" claim are significant weaknesses. The core theoretical contributions (approximation theorem, NTK regimes) are strong and undisputed, while the weaknesses are fixable with revisions. This places the paper at borderline accept.

## Summary

This paper provides theoretical foundations for separable neural networks (SepNNs) and proposes an efficient training algorithm. It proves a universal approximation theorem for CP, TT, and Tucker SepNNs (extending prior bivariate-only results to arbitrary D), characterizes SepNN NTK under two asymptotic regimes (deterministic under infinite width+rank, random under infinite width+fixed rank), and proposes SepPGD—a preconditioned gradient descent method that exploits the separable structure to reduce complexity from O(n^D) to O(nD) for n^D grid samples. Experiments on kernel ridge regression, image/surface INRs, and PINNs show improved convergence.

## Strengths

- **Universal approximation theorem (Theorem 1).** The proof uses Stone-Weierstrass to show that separable function classes (CP, TT, Tucker) are dense in the continuous functions, then reduces factor approximation to standard UAT for vector-valued MLPs. This cleanly extends prior bivariate-only results (Cho et al., 2023) to arbitrary D and multiple tensor decomposition formats.

- **NTK analysis with two asymptotic regimes (Theorem 2, Corollary 1).** Lemma 1 derives the SepNN NTK as a sum over factor MLP NTKs weighted by products of other factor outputs. The contrast between the infinite-rank deterministic limit and the fixed-rank random limit correctly identifies the role of the rank parameter. The Kronecker-product structure of the SepNN NTK on grid data (Section 3) is a useful observation that directly motivates the algorithm design.

- **SepPGD complexity advantage (Table 1, Remark 4).** The O(nD) complexity for n^D grid samples is a substantial improvement over O(n^D) (Geifman et al., 2024) and O(n^D/p) (Shi et al., 2025). The insight of decomposing a large preconditioner into smaller factor preconditioners via the equivalence (C^⊤ ⊗ A)vec(B) = vec(ABC) (Lemma 2) is technically sound.

## Weaknesses

### Fatal
None.

### Major
- **Overclaiming of "provably" for spectral bias alleviation.** The abstract and contributions list (lines 9, 50) state that SepPGD "provably adjusts the eigenvalue distribution of NTK matrix," but the actual argument in Section 4 (lines 200-201) contains acknowledged gaps: (i) the reasoning relies on Ḱ (a separable approximation) being "close" to the true NTK K, which is asserted rather than derived; (ii) even closeness in norm does not guarantee that preconditioning properties transfer; (iii) the paragraph ends with "This is left for future research." The paper provides a plausible heuristic and partial motivation (Lemma 2 establishes equivalence to a Kronecker-sum preconditioner, and S̃ has better spectrum than Ḱ), but this falls short of a proof. The language in the abstract and contributions should be revised to match what is actually demonstrated.

- **Experimental evaluation lacks statistical rigor.** (a) The main experimental results (Figs 2-4) report single PSNR (33.30 vs 26.48), single IoU (0.992 vs 0.983), and single MSE values without error bars or variance estimates, even though the NTK verification in Fig. 1 does report variance over ten seeds. Given the known sensitivity of NTK-based methods to initialization and hyperparameters, this is a serious omission. (b) The image representation result (Fig. 3) shows a single bird image. (c) There is no ablation on the hyperparameter k (eigenvalue cutoff in the preconditioner construction), which controls how many eigenvalues are modulated—sensitivity to this choice is important for practical use.

### Minor
- **Grid-structured data limitation understated.** The core complexity advantage of SepPGD (O(nD) vs O(n^D)) depends on grid-structured inputs. While this is acknowledged in footnote 2 and briefly at the end of Section 4, non-grid inputs are noted to "become equivalent to standard networks." This limitation should be stated more prominently (e.g., in the main claims or conclusion) rather than in a footnote.

- **Unquantified complexity claim.** Footnote 3 asserts that the matrix product in (8) is "orders of magnitude less expensive" based on reasoning about relative costs. While plausible, the paper would benefit from a concrete complexity breakdown or empirical timing comparison to support this claim.

### Trivial
None.

## Nice-to-Haves
- Adding error bars/confidence intervals to all main experimental results (Figs 2-4) and testing on multiple images for the INR experiment.
- A sensitivity analysis on the eigenvalue cutoff hyperparameter k.
- Showing convergence curves in terms of iteration number (alongside wall-clock time) to separate lower-per-step-cost from improved per-step progress.
- NTK eigenvalue plots of the preconditioned system to directly visualize the claimed spectral improvement.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Missing baselines (Adam/SGD with momentum)": Removed. The paper's NTK/GD framework makes standard GD the natural baseline; Adam comparison would be a separate contribution.
- "Corollary 1 not used afterward": Removed. Theoretical contributions characterizing different asymptotic regimes are valuable independently.
- "Joint limit dependency not discussed": Removed. Minor theoretical subtlety that does not threaten core claims.
- "Experimental details in appendix": Removed. Standard practice for ICLR page limits.
- Various formatting/presentation nitpicks: Removed per formatting-artifact rules.

## Novel Insights
None beyond the paper's own contributions. The primary synthesis from the reviews is that the paper has two solid theoretical contributions (universal approximation, NTK regimes) and a practical algorithm with a clear complexity advantage, but the "provably" claim about spectral bias is not supported by the presented argument and the experimental evaluation needs statistical rigor to match the strength of the claimed results. These issues are fixable with reframing and additional experiments.

## Suggestions
1. Revise the abstract and contributions to replace "provably adjusts" with "effectively adjusts" or "empirically alleviates," since the theoretical gap is explicitly acknowledged as future work.
2. Add confidence intervals or variance estimates (multiple seeds) to all experimental plots in Figs 2-4.
3. Include a sensitivity analysis for the eigenvalue cutoff k.
4. Move the grid-data limitation from a footnote to a prominently stated position in the main text (e.g., early in Section 4 or in the conclusion).
5. Provide a concrete complexity comparison or empirical timing breakdown to support the claim in footnote 3.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>