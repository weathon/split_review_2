The calibration search is unavailable due to missing files in the calibration directory. I will proceed with scoring based on my direct analysis of the paper and reviews.

Let me finalize my review.

## Summary

This paper proposes AC-DC (Auto-Correction / Directional Correction), a three-stage score-based denoiser for integration within ADMM Plug-and-Play. The core idea addresses the manifold mismatch between ADMM iterates and the noisy data manifolds on which score functions are trained. The three stages are: (1) additive Gaussian noise injection (AC), (2) conditional Langevin dynamics to steer iterates toward the score manifold (DC), and (3) Tweedie or ODE-based denoising. The paper provides convergence analysis showing the AC-DC denoiser is weakly nonexpansive, enabling fixed-point ball convergence. Experiments across seven inverse problems on two datasets show quantitative improvements over several baselines.

## Strengths

1. **Novel three-stage AC-DC denoiser that specifically addresses ADMM's dual-variable manifold mismatch.** Prior score-based PnP methods (Zhu et al., 2023; Li et al., 2024; Mardani et al., 2024) rely primarily on noise injection before applying the score function. The paper identifies that the dual variable in ADMM further distorts the geometry of the iterates (lines 24, 113–117), making noise injection alone insufficient. The DC stage — Langevin dynamics targeting \(p(\mathbf{z}_{\sigma^{(k)}}|\mathbf{z}_{\text{ac}}^{(k)})\) — is a specific mechanism to refine alignment with the score manifold. Figure 5 shows that removing the DC step (\(J=0\)) leaves severe artifacts, while adding it progressively improves reconstruction.

2. **Convergence analysis that relaxes strict nonexpansiveness required by prior ADMM-PnP theory.** Prior work (Ryu et al., 2019) requires the denoiser residual to be strictly contractive. The paper proves that the AC-DC denoiser satisfies a weakly nonexpansive condition (Assumption 1, Theorem 2), allowing a non-zero \(\delta\) slack while still guaranteeing fixed-point ball convergence. Theorem 2 provides explicit high-probability bounds on \(\epsilon_k\) and \(\delta_k\) (equations 15–16) depending on score smoothness \(M\) and noise schedules. Theorem 3 further removes the strong convexity assumption on \(\ell\) using the adaptive step-size scheme of Chan et al. (2016). These are nontrivial extensions because score-based denoisers do not naturally satisfy contractiveness.

3. **Consistent quantitative improvements across a broad suite of inverse problems.** Table 1 reports PSNR, SSIM, and LPIPS for super-resolution, Gaussian deblurring, motion deblurring, random inpainting, box inpainting, and phase retrieval on FFHQ and ImageNet. "Ours" variants achieve the best or second-best metric in nearly every setting — e.g., random inpainting FFHQ: 32.844 PSNR (Ours-tweedie) vs 31.652 (next best DAPS); phase retrieval FFHQ: 27.944 vs 26.707 (DAPS). The pattern holds consistently across both datasets.

## Weaknesses

### Major

1. **The convergence theory is partially decoupled from the implemented algorithm.** Several conditions required by the theorems are not met in the experiments:
   - **Theorem 3(b) requires \(\sigma^{(k)} \to 0\) and \(\sigma_{s^{(k)}} \to 0\).** The actual schedule is \(\sigma^{(k)} = \max(0.1, 10 - (10-0.1)k/W)\), clipped at 0.1 (line 297). The paper does not remark on this discrepancy — the condition needed for the convergence guarantee is not satisfied.
   - **Theorems 2 and 3 assume the DC step reaches the stationary distribution of the Langevin dynamics at each ADMM iteration** while only \(J=10\) steps are used. The paper acknowledges this in a footnote (line 207, "for notation conciseness") and refers to Appendix E.2 for relaxed counterparts, but the main-text guarantees as stated describe an idealized algorithm rather than the implemented one.
   - **Theorem 1 requires \(\ell\) to be \(\mu\)-strongly convex**, which holds for some tasks (denoising, deblurring) but not for phase retrieval, inpainting, or compressed sensing. Theorem 3 relaxes this under adaptive step sizes, but experiments use constant step sizes for nonconvex objectives. The limitations section (line 379) acknowledges this is "desirable" but does not clarify the gap between the stated convergence guarantees and what is actually verified by the experimental setup.
   
   These issues do not invalidate the theory, but the paper's framing of "convergence guarantees" is stronger than what is empirically instantiated. The paper would benefit from clearly delineating which parts of the theory are verified by the experiments and which hold under idealized conditions.

2. **RED-diff baseline results are implausibly low and likely indicate an unfair comparison.** RED-diff (Mardani et al., 2024) achieves 16.833 PSNR on FFHQ super-resolution and 16.821 on FFHQ Gaussian deblur (lines 322, 353) — ≈13–14 dB lower than the proposed method. Even simple baselines like bicubic interpolation would typically score in the mid-20s on these tasks. The paper provides no explanation for this dramatic gap. Since RED-diff is arguably the most directly comparable existing score-based PnP method, this magnitude of underperformance without justification undermines confidence that the baselines were fairly configured. The paper also does not describe hyperparameter configurations for any baseline, making it impossible to assess fairness.

### Minor

3. **Ablation is thin and primarily qualitative.** The only ablation (Figure 5) varies the number of DC steps \(J\) on a single task (phase retrieval) and reports only visual results — no quantitative PSNR/SSIM/LPIPS for the ablation. There is no ablation isolating the AC step (no AC vs. AC vs. AC+DC), no sensitivity analysis for key hyperparameters (\(\sigma^{(k)}\) schedule, \(\eta^{(k)}\), \(\sigma_{s^{(k)}}\)), and no comparison of the AC-DC denoiser inside ADMM versus the same denoiser in a simpler proximal-gradient framework. The claim that the three-stage design is responsible for improvements is not rigorously supported by the ablation provided.

4. **Missing or ambiguous baseline comparisons.** (a) DPIR (Zhang et al., 2022) is listed as a baseline (line 295) but does not clearly appear in Table 1 — the table contains "DiPIR" which could be a typo for either DiffPIR or DPIR; either way, one listed baseline is missing from quantitative results. (b) "DDPM" appears as a row in the Gaussian blur section (line 352) but was never listed as a baseline. (c) Tasks mentioned in the introduction (nonlinear deblurring, HDR) do not appear in Table 1. (d) Blank PMC rows appear in multiple table sections. These inconsistencies in the central results table are concerning.

5. **The DC step's Gaussian approximation (Eq. 10) is not validated.** The DC Langevin step relies on approximating \(\nabla \log p(\mathbf{z}_{\text{ac}}^{(k)}|\mathbf{z}_{\sigma^{(k)}})\) with a Gaussian form (line 135). The paper does not empirically check the accuracy of this approximation, how it degrades as scheduling assumptions weaken, or whether the resulting \(\mathbf{z}_{\text{dc}}^{(k)}\) actually lies on \(\mathcal{M}_{\sigma^{(k)}}\). Since the DC step is the primary novel component, this approximation deserves at least some empirical justification.

### Trivial

6. Minor presentation issues: The algorithm box references \(\sigma_{z_t}^2\) without defining it (line 106); the table has inconsistent naming ("DiPIR", "Impainting" instead of Inpainting) and empty PMC rows. Some are likely PDF extraction artifacts.

## Nice-to-Haves

- Computational cost comparison (NFEs or wall-clock time) between methods would help assess whether the PSNR gains come at disproportionate cost.
- Statistical significance measures (standard deviations, confidence intervals) for the 100-image averages.
- Sensitivity analysis for the key hyperparameters (\(\sigma^{(k)}\) schedule, \(\eta^{(k)}\), \(\sigma_{s^{(k)}}\)).

## Removed Points

These points were flagged but removed for the reasons stated:
- "Theorem 2 requires reaching stationary distribution" — The paper explicitly acknowledges this in a footnote (line 207) and defers to Appendix E.2. Kept as a minor issue about the theory-practice gap, not a fatal omission.
- "Weakly nonexpansive framework expressions are hard to interpret" — This is a presentation preference, not a substantive weakness.
- Several formatting critiques about table garbling (DiPIR, Impaining, PMC duplicates) — Partially parser artifacts. Kept as trivial inconsistency issues but not overstated.
- "Missing related works" — Cannot verify and removed per instruction.
- "Missing proofs in appendices" — Appendices stripped by parser, removed per instruction.
- Generic concerns about "confounders not controlled" — No specific anchor in the paper, removed per instruction.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Close the theory-practice gap:** Either adjust the \(\sigma^{(k)}\) schedule to go to (or sufficiently near) zero, or restate the theoretical claims to precisely delineate which conditions are met and which are not, noting where the theory serves as a guide under idealized conditions rather than a guarantee for the exact implementation.

2. **Revisit the RED-diff comparison:** Verify the RED-diff parameters, report the configuration used, explain the 13–14 dB gap, or remove the baseline if a fair comparison cannot be assured. The same care should be applied to all baselines.

3. **Add quantitative ablation:** Report PSNR/SSIM for AC-only vs. AC+DC on at least 2–3 tasks, and sensitivity to \(J\), \(\sigma^{(k)}\) schedule, and \(\eta^{(k)}\).

4. **Clean up the baseline table:** Either add DPIR results or remove it from the baselines list; clarify the "DDPM" row; report or explicitly defer the nonlinear deblurring and HDR results to the appendix.

5. **Validate the DC step approximation:** Provide some empirical check of the Gaussian approximation used in Eq. (10), even if only a controlled synthetic test.

## Score and Decision

Based on my analysis, this paper makes genuine contributions — a well-motivated denoiser design for ADMM-PnP addressing a real problem (manifold mismatch), non-trivial convergence analysis extending prior theory, and competitive results across many tasks. However, the paper has significant issues: the convergence theory as presented is partially disconnected from the actual experimental instantiation, the RED-diff comparison is implausibly low and unexplained (undermining empirical claims), and the ablations are too thin to substantiate the design choices. These are fixable with a major revision. I rate this as borderline, needing substantive changes before acceptance.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>