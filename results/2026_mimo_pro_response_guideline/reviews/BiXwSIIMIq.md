Now I have good calibration data. Let me finalize.

**Round 1 Bracket:** Based on the most relevant anchors — HXjXPQU3yJ (PnP-ADMM mismatch analysis, 6.25, Reject), x7d1qXEn1e (restoration network implicit prior, 6.25, Accept), kRBQwlkFSP (diffusion state-guided projected gradient, 6.75, Accept), and 66arKkGiFy (PnP-ULA mismatch, 5.75, Accept) — I initially bracket between 6.0 and 7.5. Our paper is clearly stronger than the 5.75-6.25 anchors (more novel mechanism, broader experiments) but has a notable gap (missing compute analysis) that prevents it from reaching 7.5+.

**Round 2 Narrowing:** The additional anchors DsEhqQtfAG (6.50), kRBQwlkFSP (6.75) confirm the 6.5-7.0 range for diffusion inverse problem papers with moderate novelty. Papers scoring 7.5+ (U3PBITXNG6, j8hdRqOUhN) tend to have cleaner theoretical setups or broader benchmarks without the compute gap. Our paper's AC-DC mechanism is more novel than most in the 6.5-7.0 range, but the missing computational cost analysis pulls it back. I converge on **7.0**.

Now let me write the final review with calibration reporting.

---

## Summary
This paper proposes the AC-DC denoiser, a three-stage score-based denoiser for the ADMM plug-and-play framework that addresses manifold mismatch between ADMM iterates and score-trained distributions. The stages are: auto-correction (additive noise), directional correction (conditional Langevin dynamics targeting p(z_σ|z_ac)), and score-based denoising (Tweedie or ODE). The paper provides convergence guarantees under both fixed step size (strongly convex loss, Theorems 1–2) and adaptive step size (nonconvex loss, Theorem 3), and demonstrates consistent improvements across seven inverse problems on two datasets.

## Strengths
- **Principled DC mechanism via conditional Langevin dynamics (Section 3, Eq. 10, Algorithm 1):** The DC step targets p(z_σ|z_ac), whose support is provably contained within M_σ, guaranteeing manifold alignment. This is a genuine advance over prior noise-injection-only approaches (DiffPIR, SNORE, RED-diff), which add noise but do not guarantee alignment with score manifolds. The conditional score decomposition in Eq. (10) yields a practical closed-form approximation.

- **Convergence theory extending ADMM-PnP to score-based denoisers (Theorems 1–3, Eqs. 15–16):** Theorem 2 proves with explicit high-probability bounds that the AC-DC denoiser satisfies weak nonexpansiveness (Assumption 1), generalizing Ryu et al. (2019) which required strict contractiveness. Theorem 3 extends convergence to nonconvex losses (e.g., phase retrieval) via adaptive step sizes. This is the first convergence analysis for ADMM-PnP with score-based denoisers.

- **Broad experimental validation (Table 1):** Consistent best or near-best performance across super-resolution, random/box inpainting, motion/Gaussian deblurring, and phase retrieval on both FFHQ and ImageNet, with substantial gains over strong baselines (e.g., phase retrieval FFHQ PSNR 27.94 vs. 26.71 for DAPS).

- **Honest limitations discussion (Section 7):** The authors explicitly acknowledge the stability-vs-recoverability gap, the practical limitations of adaptive step sizes, the efficiency cost of multiple score evaluations, and the heuristic nature of noise schedules.

## Weaknesses

### Fatal
None

### Major
- **Missing computational cost analysis (Section 6):** Each ADMM iteration requires up to 1000 Adam steps for the x-subproblem (Eq. 7a), 10 DC Langevin steps each requiring a score evaluation, and a final denoising step — totaling 11+ score evaluations per outer iteration. Baselines like DiffPIR and DPS use approximately 1 score evaluation per iteration. Without wall-clock time, FLOPs, or NFE comparisons, it is impossible to determine whether quality improvements stem from a better algorithmic principle or simply from more computation per iteration. The authors acknowledge this gap in Section 7 but do not address it experimentally.

### Minor
- **Overstated claim of consistent best/second-best performance (Section 6, line 303):** The text states "both of our variants achieve the best or second-best performance in terms of all metrics," but Table 1 shows counterexamples in box inpainting: DCDP achieves PSNR 25.230 vs Ours-tweedie 24.025 on FFHQ, and DCDP achieves LPIPS 0.195 vs Ours-tweedie 0.222 on ImageNet. The claim should be qualified.

- **Qualitative-only DC ablation on a single task (Fig. 5):** The DC ablation is only qualitative and only on phase retrieval. Quantitative metrics (PSNR/SSIM/LPIPS vs. J) across multiple tasks would much more convincingly demonstrate the DC step's marginal contribution versus the AC step alone.

- **Task list inconsistencies (Sections 1, 6):** The introduction lists "high dynamic range (HDR)" as a separate application (line 28), but it is actually a preprocessing step within the random inpainting task (line 293). Nonlinear deblurring is described in the task setup (line 293) but has no corresponding results in Table 1. Either add these results or correct the task descriptions.

- **Convergence theory gap between fixed and adaptive schedules (Theorems 1 vs. 3):** Theorem 1 requires strong convexity of ℓ (restricting to problems like deblurring). Theorem 3 removes this but requires σ^(k) → 0, making the denoiser converge to identity and the convergence statement effectively about stability rather than recoverability. The practical regime where ℓ is nonconvex and σ is fixed remains theoretically uncovered. The authors acknowledge this in Section 7.

## Nice-to-Haves
- Report variance/standard deviations for the 100-image averages in Table 1.
- Sensitivity analysis for noise schedules (σ^(k), η^(k), σ_{s^{(k)}}), which are currently heuristic.
- Compute-normalized comparisons: run key baselines for more iterations to match total NFE budget and verify the advantage persists.
- Quantitative ablation of inner optimization budget (sensitivity to the 1000 Adam iteration cap).

## Removed Points
These points are flagged to be removed, treat them with caution:
- The harsh critic flagged empty PMC entries in Table 1 as potentially incomplete data. These are PDF parsing artifacts — the original table had multi-row PMC entries. Not a real issue.
- The harsh critic raised a circularity concern about the Gaussian approximation condition (Var(s^(k))^{1/2} ≪ σ^(k)). While the condition is related to the iterate being close to the manifold, the Langevin dynamics in the DC step targets the correct conditional distribution regardless of the Gaussian approximation's exactness — the approximation only affects the form of the conditional score used in practice, not the fundamental mechanism. This is a theoretical nuance, not a practical problem.
- The harsh critic noted the stationary distribution assumption for DC (Theorems 2–3). The authors provide counterparts without this assumption in Appendix E.2 and explicitly note this (footnote, line 207). The assumption is acknowledged and addressed.

## Novel Insights
The paper's genuinely novel contribution is the conditional Langevin dynamics mechanism (DC step) for bridging manifold mismatch. Unlike prior approaches that rely solely on additive noise injection, the DC step provably targets a distribution supported on the noisy data manifold M_σ (since supp(z_σ|z_ac) ⊆ supp(z_σ) = M_σ). This provides a principled correction that goes beyond heuristic noise addition, and when combined with the first convergence analysis for ADMM-PnP with score-based denoisers, represents a meaningful advance in understanding and improving PnP methods with diffusion priors.

## Suggestions
- Add wall-clock time and NFE comparisons between the proposed method and key baselines (at minimum DiffPIR, DAPS, DPS) across representative tasks.
- Add quantitative DC ablation: report PSNR/SSIM/LPIPS vs. J for at least 3-4 tasks.
- Fix the "best or second-best" claim to accurately reflect box inpainting results.
- Either add nonlinear deblurring results to Table 1 or remove it from the task descriptions.

## Calibration Report

**Round 1 anchors (topically relevant):**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| HXjXPQU3yJ | 6.25 | 1 | "Prior Mismatch in PnP-ADMM" — Same problem area, but only analyzes mismatch without proposing a solution; our paper is more novel and comprehensive |
| x7d1qXEn1e | 6.25 | 1 | "Restoration Network as Implicit Prior" — Related PnP convergence work, narrower experiments (SR + deblurring only) |
| 66arKkGiFy | 5.75 | 1 | "PnP Posterior Sampling under Mismatch" — Related PnP mismatch analysis, more theoretical but less practical |
| kNPcOaqC5r | 5.75 | 1 | "Learned Proximal Networks" — Related PnP convergence work with different focus |
| Z9Odi09Rv9 | 4.75 | 1 | "Fast Diffusion Solvers" — Related diffusion inverse problems, had soundness issues |
| DsEhqQtfAG | 6.50 | 1 | "Decomposed Diffusion Sampler" — Diffusion inverse problems, different approach (Krylov subspace) |
| kRBQwlkFSP | 6.75 | 1 | "Diffusion State-Guided Projected Gradient" — Related manifold mismatch issue, uses projection instead of Langevin |

**Round 2 anchors:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| U3PBITXNG6 | 7.50 | 2 | "InverseBench" — Benchmarking paper across scientific inverse problems, broader but no new method |
| 6EUtjXAvmj | 8.00 | 2 | "Variational Diffusion Posterior Sampling" — Stronger theoretical contribution, all 8s |
| j8hdRqOUhN | 7.50 | 2 | "Latent Diffusion with Hard Data Consistency" — Novel resampling scheme, cleaner setup |
| SOd07Qxkw4 | 7.50 | 2 | "Improved Convergence Rate for Diffusion" — Theoretical convergence rate, different focus |

**Bracketing:** Round 1 placed the paper between 6.0 and 7.5. Round 2 confirmed: papers scoring 7.5+ have cleaner theoretical setups or stronger empirical programs without the compute analysis gap. Our paper's AC-DC mechanism is more novel than most 6.5–7.0 anchors, but the missing compute analysis pulls it back from 7.5. Final score: 7.0.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept