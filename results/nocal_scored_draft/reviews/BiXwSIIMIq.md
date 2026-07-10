Now let me compose the final review based on my verification and the favorability signals.

## Summary

The paper proposes AC-DC, a three-stage (auto-correction, directional correction, score-based denoising) denoiser designed to mitigate manifold mismatch when integrating score-based generative priors into ADMM for solving inverse problems. The method is evaluated on seven inverse problems across two datasets against eight baselines, achieving best or second-best results on most tasks. Convergence guarantees are provided under both constant step sizes (for strongly convex objectives) and adaptive step sizes (for nonconvex cases).

## Strengths

- **Clear problem diagnosis.** The paper correctly identifies that ADMM dual variables compound the manifold mismatch problem beyond what prior PnP methods face — a genuine insight that motivates the algorithmic design (Section 3, lines 115–117). [(favorability: 0.95)]

- **Broad empirical scope.** The method is tested on seven inverse problems (super-resolution, Gaussian deblur, motion deblur, two forms of inpainting, phase retrieval, nonlinear deblurring) across two datasets (FFHQ, ImageNet 256×256) against eight baselines. Table 1 shows the method achieves best or second-best results on most task/dataset combinations. [(favorability: 1.00)]

- **Honest limitations discussion.** Section 7 openly acknowledges that the adaptive-step-size convergence result is "arguably less appealing in practice," that the analysis addresses stability not recovery quality, that noise schedules are empirically guided, and that per-iteration cost is high. This candor is rare and valuable for future work. [(favorability: 0.77)]

## Weaknesses

### Fatal
None.

### Major

- **Missing internal control experiment.** The paper never evaluates ADMM + direct Tweedie denoising (applying the score denoiser from Eq. 4 directly to the raw ADMM iterate without AC or DC). The ablation in Fig. 5 compares AC-only (J=0) vs AC-DC (J>0), but AC itself is a non-standard addition of noise. Without the ADMM+Tweedie-only baseline, the contribution of AC-DC cannot be separated from that of the ADMM framework. Comparisons against *different algorithms* (DPS, DDRM, DiffPIR) using different optimization frameworks do not substitute for this control, because any observed gains could partly reflect ADMM being a stronger optimizer rather than AC-DC specifically improving denoising. [(fav: 0.06)]

- **Gap between convergence theory assumptions and experimental practice.** (a) Theorems 2 and 3 require the DC step to "reach the stationary distribution" for each k, but experiments use only J=10 Langevin steps with no evidence that this mixes to stationarity on 256×256 image distributions. The paper's footnote referencing Appendix E.2 for counterparts removing this assumption does not bridge the gap for the main results. (b) Theorems 1 and 2 (constant-step-size results) require ℓ to be μ-strongly convex, which is violated by several tested tasks (phase retrieval, inpainting). Theorem 3 relaxes convexity via adaptive step sizes that the paper itself calls "arguably less appealing in practice," yet all experiments use constant ρ. The paper acknowledges these gaps in the limitations section but does not resolve them. [(fav: 0.00, 0.10)]

- **Computational cost not quantified.** Each ADMM iteration involves up to 1000 Adam iterations for subproblem (7a), then J=10 Langevin steps (each with a score network evaluation), then a final denoising step. No runtime, FLOPs, or NFE comparisons against baselines are reported. Since gains over the strongest baselines (DAPS, DCDP) are often modest (~0.6–0.9 dB PSNR), the practical trade-off cannot be assessed without cost data. [(fav: 0.13)]

### Minor

- **Unusual convergence criterion unexplained.** Subproblem (7a) detects convergence "when the loss value increases more than Δ_tol = 1e-3 consecutively for 3 iterations" (line 297). Detecting loss *increase* as a convergence signal is atypical and the rationale is not provided. [(fav: 0.35)]

- **Theoretical novelty is incremental.** The convergence theory extends existing ADMM-PnP analysis (Ryu et al., 2019; Chan et al., 2016) by relaxing strict contractiveness to weak contractiveness, yielding δ-ball convergence instead of fixed-point convergence. The paper accurately scopes this as an extension (line 227), and the verification that AC-DC fits this framework is legitimate, but the machinery is inherited from prior work. [(fav: 0.00)]

### Trivial
None.

## Nice-to-Haves

- Sensitivity analysis for key hyperparameters (σ schedule, W, J) would strengthen confidence in robustness.
- Numerically estimating the convergence radius r for the experimental settings would clarify whether the theoretical guarantee is meaningfully tight or vacuously large.
- Extending the DC-step ablation (Fig. 5) to larger J values (50, 200) on one task would indicate whether J=10 is near stationarity or far from it.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **(Removed: formatting/parser artifacts)** Notation issues with σ_{z_t} and σ_ac^{(k)}, garbled equation (9), and Table 1 formatting — these are PDF extraction artifacts, not author errors.
2. **(Removed: factually inaccurate)** The claim that DDRM and DiffPIR are "competitive" — Table 1 shows Ours-tweedie leads DDRM by ~2.5–3.5 dB PSNR and DiffPIR by larger margins. The paper's claim of outperforming them is accurate.
3. **(Removed: analysis beyond scope)** Requests to numerically instantiate the convergence radius or provide exhaustive hyperparameter sensitivity analysis — these are nice-to-haves, not weaknesses.
4. **(Removed: speculation)** The critique about the "loss increases" convergence criterion being a safeguard against overfitting — this is speculation about an unexplained design choice; the lack of rationale is noted above instead.

## Novel Insights

The reviewers' central insight is that the paper's evidential structure has a blind spot: the AC-DC denoiser is evaluated as a package with ADMM against other complete algorithms, but the *marginal* contribution of AC-DC over a standard Tweedie denoiser within the same ADMM framework is never measured. This makes it impossible to rule out the possibility that ADMM itself (rather than the AC-DC mechanism) drives the improvements. The convergence theory, while technically competent, relies on assumptions (stationarity of the DC chain, strong convexity for the main result) that are not verified or satisfied in the experimental settings, creating a gap between the guarantees stated and the actual protocol used.

## Suggestions

1. Add the ADMM + direct Tweedie denoising baseline (no AC, no DC) to isolate AC-DC's contribution.
2. Report wall-clock runtime or NFE alongside quality metrics.
3. Provide empirical evidence on J-step sufficiency for stationarity (e.g., vary J from 0 to 200+ on one task).
4. Clarify the convergence detection logic for the inner Adam loop.
5. Add sensitivity analysis for key hyperparameters (σ schedule range, W, J).

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>