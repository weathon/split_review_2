Here is my final consolidated review.

---

## Summary

This paper proposes AC-DC, a three-stage score-based denoiser (Auto-Correction → Directional Correction → Denoising) designed to mitigate the manifold mismatch between ADMM iterates and the noisy manifolds on which pre-trained score functions operate. The authors embed this denoiser into ADMM-PnP, provide convergence analysis (weakly nonexpansive fixed-point ball convergence under constant step size and strong convexity; bounded-denoiser convergence under adaptive step size), and evaluate on seven inverse problems across two datasets.

## Strengths

- **Well-motivated problem.** The paper clearly articulates why integrating score-based denoisers into ADMM is nontrivial (Section 2, lines 72–73): ADMM iterates, especially through dual variables, do not lie on the noisy manifolds the score was trained on, and existing PnP convergence theory assumes contractive/nonexpansive denoisers that score-based denoisers do not satisfy. This is a genuine gap in the literature.

- **Non-trivial theoretical analysis.** The extension of ADMM-PnP convergence theory (Ryu et al., 2019; Chan et al., 2016) to score-based denoisers is a real technical contribution. Theorem 1 generalizes from strict contractivity to weak contractivity with a δ offset, and Theorems 2–3 connect denoiser properties (boundedness, weak nonexpansiveness) to the AC-DC parameters under explicit smoothness and coercivity conditions.

- **Broad experimental coverage.** The evaluation spans seven inverse problems (super-resolution, random/box inpainting, Gaussian/motion deblurring, phase retrieval, HDR) on FFHQ and ImageNet (100 images each), with three metrics (PSNR, SSIM, LPIPS) against eight baselines. This is reasonably comprehensive for a methods paper.

## Weaknesses

### Fatal
None.

### Major

- **Theory-practice gap under constant step size.** Theorem 1 requires ℓ to be μ-strongly convex, but several evaluated tasks — inpainting (box/random), phase retrieval — do not satisfy this. Theorem 3 removes convexity but requires an adaptive step-size scheme, which the paper itself calls "arguably less appealing in practice" (line 379). All experiments use constant step sizes, including for nonconvex tasks. The paper acknowledges this (line 379: "our experiments, however, suggest that constant step sizes also perform well for nonconvex objectives") but this is an empirical observation with no theoretical backing. The central claim of a "convergent plug-and-play framework" therefore applies to a different algorithmic configuration than what is tested.

- **Vanishing noise schedule condition violated.** Theorem 3(b) requires σ⁽ᵏ⁾ → 0 and σ_{s⁽ᵏ⁾} → 0 as k→∞ to guarantee convergence. The practical schedule (line 297) clips σ⁽ᵏ⁾ at 0.1 indefinitely (max(0.1, …)), never converging to zero. This gap between the vanishing-noise requirement and the non-vanishing experimental schedule is acknowledged in the limitations but not bridged; the theory does not cover the regime actually evaluated.

- **No computational cost comparison.** The AC-DC denoiser per ADMM iteration requires up to 1000 Adam iterations for the x-subproblem (7a) plus J=10 Langevin steps with score evaluations, plus an additional ODE/Tweedie denoising step. With K = W+10 total ADMM iterations (W not stated), total cost could reach tens of thousands of score evaluations per image. Baseline methods (DPS: ~1000 NFEs; DiffPIR: ~100 score evaluations × ~100 iterations) are far cheaper. No runtime, NFE count, or wall-clock comparison is reported anywhere. Without this, it is unclear whether quality improvements reflect algorithmic superiority or simply higher computational budget.

### Minor

- **Table 1 reporting inconsistencies.** (a) "DDPM" appears as a baseline under Gaussian Blur (line 352) but is not listed in the baselines enumeration (line 295). (b) The table uses "DiPIR" throughout, while the text and baselines list both "DiffPIR" and "DPIR"; it is unclear whether "DiPIR" is a typo for DiffPIR, and DPIR never appears in the table. These inconsistencies suggest incomplete quality control on the experimental reporting.

### Trivial

- **PMC rows in Table 1.** PMC appears twice in the Superresolution block with different numbers, and several other PMC rows are empty. This may be a PDF parsing artifact, but in the extracted form it creates confusion.

## Nice-to-Haves

- Report computational cost (wall-clock time or NFE) alongside quality metrics.
- Either relax the theory to match the experimental setup (non-vanishing σ, non-strongly convex ℓ) or adjust experiments to match the theory (adaptive ρ, vanishing σ), and clearly delineate which claims are theoretically supported and which are empirical.
- Clarify the table: resolve the DDPM/DiPIR/DPIR confusion.
- State the numerical value of W (decay window) used in experiments.

## Removed Points

These points from the input review were removed with brief justification:

- **"No proper ablation of AC step"** — The paper shows J=0 (AC-only, no DC) in Fig. 5 for phase retrieval, and the baseline comparisons (DiffPIR, RED-diff) serve as vanilla score-based references. The marginal contribution of AC over no-correction is observable by comparing against these baselines.
- **"W not stated"** — W is indeed not numerically specified; this is a missing experimental detail but minor and could be provided without affecting core contributions.
- **"Notation issues in Eq. (9)" and "σ_{z_t} undefined"** — The equation is dense but the surrounding text (lines 127–135) provides explanation; these are presentation issues rather than substantive technical gaps.
- **"Convergence bound contextualization"** and **"Probability dependence"** — These are helpful suggestions or observations, not weaknesses that undermine the paper.
- **"Stationary distribution assumption (J=10 insufficient)"** — The paper references Appendix E.2 for counterparts removing this assumption. Since the appendix is stripped by the parser, this cannot be verified from the extracted text alone, and the critic's claim relies on speculation about the appendix content.
- **"Weak nonexpansiveness bound is vacuous"** — The critic computes δ² ≈ 12000 for the experimental σ=0.1 regime, but Theorem 2(b) requires σ→0; in the vanishing-σ limit δ→0. The bound being large under non-vanishing σ is already covered by the acknowledged theory-practice gap above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report computational cost (NFEs or wall-clock time) alongside quality metrics so readers can assess the quality-efficiency trade-off.
2. Either (a) relax the theory to cover non-vanishing σ and non-strongly-convex ℓ with constant step size, or (b) run a controlled experiment matching the theorem's conditions (adaptive ρ, vanishing σ) to validate the theory and clearly separate what is proven from what is observed empirically.
3. Fix the table notation to ensure consistency between the baselines list and the table entries.
4. State the numerical value of the decay window W.

## Score and Decision

**Calibration:** I compared the paper's weighted items against three anchors retrieved from the human-review corpus. The most relevant anchor, "Prior Mismatch and Adaptation in PnP-ADMM with a Nonconvex Convergence Analysis" (avg 6.25, accepted), had similar strengths (timely topic, theoretical error bound) but its main weaknesses concerned experimental scope and missing comparisons — less fundamental than the theory-practice gap in the current paper. The "What's in a Prior?" anchor (avg 5.75, accepted) had -7.12 and -6.50 weaknesses related to proof correctness and organization. The "A primal-dual algorithm for variational image reconstruction" anchor (avg 5.00, rejected, all 5s) had weakest experiments and insufficient novelty — analogous in severity to our theory-practice gap. Our paper sits below the 5.00 anchor because its theory-practice disconnect cuts to the core claim of "convergence guarantees" in a way that the anchor's weak-baseline issue does not. The round-1 bracket was [3.5, 5.5]; after comparing weighted items against R9W6fFlr8W (5.00, rejected) and HXjXPQU3yJ (6.25, accepted), the final score is narrowed to 4.5.

**Score justification:** The paper has genuine technical contributions (novel AC-DC architecture, non-trivial convergence analysis, broad experiments), but the theory-practice gap is significant: the convergence theorems' conditions (strong convexity, vanishing noise schedule, adaptive step size) are not satisfied by the experimental setup, and the paper's central claim of guaranteed convergence therefore overstates what is actually shown. The missing computational cost comparison further undermines the empirical contribution. These issues are addressable in revision, making the paper a borderline case.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>