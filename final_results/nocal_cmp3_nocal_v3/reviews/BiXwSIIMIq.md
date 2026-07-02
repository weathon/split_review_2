Now I'll produce the final review.

## Summary

The paper proposes AC-DC, a three-stage score-based denoiser (auto-correction via additive Gaussian noise → directional correction via conditional Langevin dynamics → Tweedie/ODE denoising) designed for integration within ADMM plug-and-play frameworks, addressing the manifold mismatch between score functions trained on Gaussian-perturbed data and ADMM iterates. The authors provide convergence analysis (weakly nonexpansive operators → δ-ball convergence) and evaluate on 7 inverse problems × 2 datasets against 8 baselines.

## Strengths

1. **Well-motivated and logically structured denoiser design.** The AC-DC pipeline directly responds to the genuine problem of manifold mismatch in score-based ADMM: AC brings iterates near the score's operating range, DC refines alignment using conditional Langevin dynamics, and the final Tweedie/ODE step does the actual denoising. The DC step is the genuinely novel component, and its rationale is clearly explained in the paper (Section 3, Algorithm 1).

2. **Broad experimental scope.** The evaluation covers 7 inverse problems (super-resolution, Gaussian/motion deblurring, random/box inpainting, phase retrieval, HDR) on FFHQ and ImageNet with many baselines (DPS, DAPS, DDRM, DiffPIR, RED-diff, DPIR, DCDP, PMC). This is a thorough empirical effort that generally supports the claimed improvements (Table 1).

3. **Non-trivial theoretical contribution.** Extending ADMM-PnP convergence theory (Ryu et al., 2019; Chan et al., 2016) to score-based denoisers via a weakly nonexpansive framework is technically challenging, and the paper provides structured convergence results under both fixed and adaptive step-size schedules (Theorems 1-3).

## Weaknesses

### Fatal
None.

### Major

1. **Theory-practice gap in the DC step.** Theorems 2 and 3 both assume the Langevin dynamics in the DC step "reaches the stationary distribution for each k" (lines 183, 206). In practice, Algorithm 1 uses only J=10 Langevin steps per ADMM iteration (line 297). The paper acknowledges this in a footnote (line 207: "Note that Theorems 2 and 3 use this stationary distribution assumption for notation conciseness. For their counterparts removing this assumption, see Appendix E.2") and points to a relaxed version in the appendix. However, the main text provides no argument or empirical evidence that 10 steps are sufficient for near-stationarity, nor does it bound the error from early termination. A reader of the main text cannot determine whether the practical algorithm satisfies the conditions under which the guarantees hold.

2. **Missing experimental parameters.** Two key parameters are not given numerical values in the main text: (a) the decay window W in the σ⁽ᵏ⁾ schedule (line 297: "over W decay window"), which controls the total number of ADMM iterations; and (b) the ADMM penalty parameter ρ, which controls coupling between subproblems and appears in Theorem 1's convergence conditions. Without these, the experimental setup is incompletely specified.

### Minor

1. **DC ablation is qualitative only.** Figure 5 shows visual improvements from increasing J (DC steps) from 0 to 20, but no PSNR/SSIM/LPIPS values are reported for these ablations. This makes it difficult to quantify the DC step's marginal contribution.

2. **Conditional score approximation is stated without empirical verification.** The paper approximates p(z_ac⁽ᵏ⁾ | z_σ⁽ᵏ⁾) as Gaussian, justified when "Var(s⁽ᵏ⁾)^{1/2} ≪ σ⁽ᵏ⁾" (line 135). The paper does not analyze, bound, or empirically check this condition during ADMM iterations. If the approximation is poor, the DC step may not actually move iterates toward the correct conditional distribution.

3. **Computational cost not reported.** The paper acknowledges in its Limitations (Section 7) that "each iteration of AC-DC denoiser needs multiple score evaluations," but does not report total NFEs, wall-clock time, or runtime versus baselines. Given that each ADMM iteration involves up to 1000 Adam steps for the x-subproblem, J=10 score evaluations for the DC step, plus ODE/Tweedie denoising, the total cost could be substantially higher than methods like DPS or DiffPIR. This information is needed for practitioners to assess the cost–benefit trade-off.

4. **Convergence framing could be clearer.** The abstract states "high-probability fixed-point ball convergence" and "convergence under an adaptive step size schedule." The actual guarantees are: (Theorem 1) δ-ball convergence under strong convexity, and (Theorem 3(b)) fixed-point convergence only as σ⁽ᵏ⁾ → 0 and σ_s⁽ᵏ⁾ → 0 (i.e., the denoising strength vanishes asymptotically). The paper is transparent about these limitations in Section 7, but the abstract and introduction could lead a casual reader to overestimate the strength of the guarantees.

### Trivial
None.

## Nice-to-Haves
- Quantitative DC ablation (PSNR/SSIM/LPIPS for J=0, J=5, J=10, J=20).
- Convergence diagnostics (residual norms over iterations) showing empirical stabilization.
- Sensitivity analysis for key hyperparameters (ρ, J, σ range).

## Removed Points
These points were raised in the input review but removed per the filtering rules:

1. **Notation issues in Eq (9) and Section 4 theorems** — Removed as likely parser-induced formatting artifacts, not author errors.
2. **Table labeling issues ("DiPIR", "DDPM", duplicate PMC entries, blank cells)** — Removed as parser-induced formatting artifacts; the original submission's table formatting is lost in plain-text extraction.
3. **"DPIR from baseline list never appears in Table 1"** — The table contains "DiPIR" entries, which are likely parser-mangled renderings of "DPIR." Removed as a formatting artifact.
4. **Claim that the paper overstates ADMM prevalence in Section 1** — The paper's claim ("score-based denoising has rarely been combined with primal-dual methods") is modest and the paper later discusses DiffPIR's ADMM-like structure. Removed as an over-reading.
5. **"100 test images is modest"** — This is standard practice in the field; removed as a generic criticism.
6. **Missing Appendix E.2 discussion** — The parser strips appendix content. The paper has a footnote pointing to the appendix. Removed per the rule about missing appendix references.
7. **D-AMP comparison could be more precise** — Weak generic criticism about related work positioning. Removed.
8. **Per-image variance not reported** — Generic criticism not standard for this style of benchmark paper. Removed.

## Novel Insights
None beyond the paper's own contributions. The review confirms the paper's main claimed strengths (well-motivated design, broad experiments, nontrivial theory) and identifies a structural gap between the theoretical assumptions and practical implementation, plus several missing experimental details. No new insights emerged that were not already visible from reading the paper.

## Suggestions
1. Add a quantitative ablation table (PSNR/SSIM/LPIPS) for varying J (DC steps), including J=0 to isolate the AC stage's contribution.
2. Report the numerical values of W and ρ in the main text. Clarify the total number of ADMM iterations.
3. Add a computational cost comparison (estimated NFEs or wall-clock time) against baseline methods.
4. Clarify in the main text (not just a footnote) whether the convergence guarantees for J=10 require the relaxed assumptions in Appendix E.2, and if so, what those assumptions entail.
5. Provide at least a brief empirical diagnostic (e.g., for a representative run) showing that the Var(s⁽ᵏ⁾)^{1/2} ≪ σ⁽ᵏ⁾ condition holds during iterations.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>