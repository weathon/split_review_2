Now let me read the limitations and conclusion section more carefully:Now I have enough information to draft my review. Let me submit the draft and then calibrate.Now let me do Round 1 calibration — bracketing across score bands:Let me read the most relevant anchors in detail:Now let me do Round 2 to narrow within my initial bracket of **5.5–7.0**:Now I have sufficient calibration data. Let me synthesize my final review.

**Round 1 bracket**: 5.5–7.0

**Round 2 narrowing**: Based on the closest anchors:
- HXjXPQU3yJ (6.25, Reject): PnP-ADMM with mismatch/convergence — paper under review is clearly stronger (novel method, broader experiments)
- x7d1qXEn1e (6.25, Accept): Restoration network as implicit prior with convergence theory — similar quality
- DsEhqQtfAG (6.50, Accept): Decomposed Diffusion Sampler — similar novelty + theory + experiments
- kRBQwlkFSP (6.75, Accept): DiffStateGrad — slightly more practical/polished

**Final bracket**: 6.0–6.5

---

## Summary
This paper proposes the AC-DC denoiser for integrating score-based diffusion models into ADMM-PnP for solving inverse problems. The three-stage denoiser—auto-correction (AC) via Gaussian noise injection, directional correction (DC) via conditional Langevin dynamics, and score-based denoising—addresses the manifold mismatch between ADMM iterates and the noisy data manifolds on which score functions are trained. The paper provides convergence guarantees (δ-ball convergence under strong convexity; fixed-point convergence under adaptive step sizes without convexity) and demonstrates strong empirical performance across seven inverse problems on two datasets.

## Strengths
- **Principled method design addressing a real problem.** The manifold mismatch issue (ADMM iterates $\tilde{z}^{(k)} = x^{(k+1)} + u^{(k)}$ incorporating dual variable information that distorts the noise geometry away from $\mathcal{M}_{\sigma(t)}$) is clearly identified. The DC step targeting $p(z_{\sigma^{(k)}} | z_{\text{ac}}^{(k)})$ (Eq. 10) is genuinely novel: its support is contained in $\mathcal{M}_{\sigma^{(k)}}$ by construction while retaining measurement information via conditioning. This is more principled than noise-injection-only approaches of DiffPIR or SNORE.

- **Non-trivial convergence analysis extending prior work.** Theorem 1 generalizes Ryu et al. (2019) from strictly contractive to weakly non-expansive residuals, recovering the prior result as the special case $\delta = 0$. Theorem 3 removes the strong convexity requirement using adaptive step sizes. These are genuine extensions of the ADMM-PnP convergence literature.

- **Comprehensive experiments with strong results.** Table 1 covers seven inverse problems (SR, random/box inpainting, Gaussian/motion deblurring, phase retrieval, and more), two datasets (FFHQ, ImageNet), three metrics, and eight baselines. The method achieves best or second-best in nearly all settings, with large margins on challenging tasks (e.g., phase retrieval on FFHQ: 27.94 PSNR vs. 26.71 for DAPS).

- **DC ablation validates the core claim.** Figure 5 shows that removing DC ($J=0$, AC-only) leaves severe artifacts in phase retrieval while increasing $J$ progressively cleans reconstructions, confirming that DC is doing meaningful work beyond noise injection alone.

## Weaknesses

### Fatal
None

### Major
- **Theory-practice gap on stationary distribution assumption.** Theorems 2 and 3 assume "the DC step reaches the stationary distribution for each $k$" (lines 183, 205). In practice, only $J=10$ Langevin steps are used (Section 6) in $d \approx 196{,}608$ dimensions. The footnote (line 207) directs to Appendix E.2 for relaxed versions, but the main text never states what those relaxed results look like or how they affect the convergence guarantees. If the relaxed versions introduce large error terms proportional to the mixing-time gap, the guarantees could become uninformative for the practical regime.

- **Convergence ball may be vacuously large.** The $\delta_k^2$ term (Eq. 16) contains $3 \cdot 2(\sigma^{(k)})^2(d + 2\sqrt{d\nu_k} + 2\nu_k)$, which for $d \approx 2 \times 10^5$ is enormous even with moderate $\sigma^{(k)}$. The paper never estimates $r$ for any experimental setting, leaving it unclear whether the convergence guarantee meaningfully constrains the iterates' behavior or is consistent with them wandering across the entire image space.

- **Missing computational cost reporting.** Each outer ADMM iteration involves up to 1000 Adam inner iterations for subproblem (7a), $J=10$ DC steps (each requiring a score evaluation), and a final denoising step. No wall-clock time, NFE counts, or computational comparisons are provided. The paper's limitations section (line 379) acknowledges this ("Reducing the required NFEs could significantly improve its efficiency"), but the absence makes it impossible to assess whether the quality improvements come at a 2× or 100× cost premium relative to baselines with well-characterized profiles (DPS, DAPS, DiffPIR).

### Minor
- **Limited ablation study.** The DC ablation (Figure 5) is qualitative and limited to a single task (phase retrieval). A quantitative ablation varying $J$ across multiple tasks (reporting PSNR/SSIM/LPIPS) would more rigorously demonstrate DC's contribution across the diverse settings in Table 1.

- **Unexplained blank entries in Table 1.** PMC has numerous empty entries across tasks (e.g., random inpainting, motion deblurring, Gaussian blur, box inpainting). No explanation is provided for whether the baseline failed, is inapplicable, or was omitted for other reasons.

- **Gaussian approximation in DC step not validated.** The approximation $\nabla \log p(z_{\text{ac}}^{(k)}|z_{\sigma^{(k)}}) \approx -1/\sigma_{\text{ac}}^{(k)}(z_{\sigma^{(k)}} - z_{\text{ac}}^{(k)})$ (line 135) is the key design choice distinguishing this from prior noise-injection approaches, but is justified only by the plausibility argument that $\text{Var}(s^{(k)})^{1/2} \ll \sigma^{(k)}$, without empirical or theoretical validation.

### Trivial
None

## Nice-to-Haves
- Estimate the convergence ball radius $r$ for at least one experimental configuration (even order-of-magnitude) to demonstrate the theory is informative.
- Report confidence intervals over the 100 test images, especially for tasks where margins are small (e.g., box inpainting, Gaussian deblurring on ImageNet).
- Empirically validate the Gaussian approximation quality in the DC step (e.g., on a low-dimensional problem).
- A quantitative AC-only ablation (AC + denoising without DC) across multiple tasks to fully disentangle the two stages.

## Removed Points
*These points are flagged to be removed, treat them with caution:*

- **Assumption 2 (M-smoothness of log p_data) unrealistic for manifold-supported distributions**: While valid in principle, this is a standard assumption in the PnP convergence literature the paper extends. The paper's theoretical contribution is precisely in extending existing frameworks under these assumptions. Removed as field-standard.
- **Finite noise schedule not satisfying asymptotic conditions in Theorem 2(b)**: The practical linear schedule has $\sigma^{(k)}$ dropping to 0.1 and staying there. Whether this satisfies the asymptotic condition is moot since the schedule is finite — this gap exists for any asymptotic convergence result applied to finite iterations. Removed as standard theory-practice gap in optimization.
- **"Consistently improves" slight overstatement in abstract**: While DCDP beats the method on box inpainting PSNR (25.23 vs 24.03), the method is best/2nd best in the vast majority of settings. Removed as trivial presentation concern.
- **100-image test set without confidence intervals**: This is standard practice in the field (DPS, DAPS, DiffPIR all use similar setups). Moved to nice-to-have rather than weakness.

## Novel Insights
The paper's central novel insight is that conditioning Langevin dynamics on the AC-perturbed iterate $z_{\text{ac}}^{(k)}$ simultaneously achieves manifold alignment (support of conditional is contained in $\mathcal{M}_{\sigma^{(k)}}$) and measurement information retention — unlike pure noise-injection approaches that treat manifold alignment as a side effect of stochastic regularization. The theoretical contribution of extending ADMM-PnP convergence from strictly contractive to weakly non-expansive residuals (with the special case $\delta=0$ recovering Ryu et al. 2019) also provides a useful framework for future score-based PnP work.

## Suggestions
- Report NFE counts and wall-clock times for all methods to contextualize the performance improvements.
- Add a quantitative ablation table for DC steps (varying $J$) across at least 3 tasks with PSNR/SSIM/LPIPS metrics.
- Provide an order-of-magnitude estimate of the convergence ball radius for one experimental setting to connect theory to practice.
- Explain blank entries in Table 1 (e.g., "PMC does not support nonlinear operators" or "PMC failed to converge").
- Summarize the relaxed convergence results from Appendix E.2 in the main text so readers can assess how the finite-$J$ regime affects guarantees.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| u1cQYxRI1H.md | 0.50* | R1 | Unrelated (illumination). *Avg mislabeled; actual 10.0 |
| Uj0h13lVrR.md | 1.00 | R1 | Much weaker — no real contribution |
| 5lUdTogEL3.md | 1.00 | R1 | Much weaker — fundamental issues |
| bEgDEyy2Yk.md | 1.00 | R1 | Much weaker — trivial implementation paper |
| dAavOuxZvo.md | 3.00 | R1 | Weaker — diffusion inpainting with heuristic approaches |
| W4djmqKZC6.md | 3.00 | R1 | Weaker — less novel, less comprehensive |
| 46tjvA75h6.md | 3.00 | R1 | Weaker — diffusion+EBM, limited novelty |
| 2o58Mbqkd2.md | 3.25 | R1 | Weaker — superposition idea, split reviews |
| Z9Odi09Rv9.md | 4.75 | R1 | Weaker — diffusion inverse problems with unfair baselines, technical errors |
| nHESwXvxWK.md | 4.00 | R1 | Weaker — split reviews (1,8,1,6), narrower scope |
| 7SFTZwNUQA.md | 5.20 | R1 | Weaker — limited novelty, patch-based approach |
| V2x5ZTHMae.md | 4.00 | R1 | Weaker — integrating crafted measurements, moderate contribution |
| 9mX0AZVEet.md | 6.00 | R1 | Similar — optimal posterior covariance, split reviews (5,5,8) |
| 66arKkGiFy.md | 5.75 | R1 | Slightly weaker — PnP-ULA mismatch analysis, somewhat incremental |
| DsEhqQtfAG.md | 6.50 | R1 | Similar — novel theory + diffusion + strong results |
| x7d1qXEn1e.md | 6.25 | R1/R2 | Similar — PnP convergence with novel prior, comparable |
| 6EUtjXAvmj.md | 8.00 | R1 | Stronger — all 8s, more thorough methodology |
| HXjXPQU3yJ.md | 6.25 | R2 | Similar topic (PnP-ADMM mismatch + convergence) but narrower experiments; paper under review is clearly better |
| kBLnxjuKd3.md | 5.75 | R2 | Less relevant — inductive bias of diffusion models |
| ANvmVS2Yr0.md | 6.25 | R2 | Different focus — generalization in diffusion |
| qZwtPEw2qN.md | 6.80 | R2 | Different focus — data scaling laws |
| kRBQwlkFSP.md | 6.75 | R2 | Similar quality — manifold alignment module, slightly more practical |

**Bracket progression:**
- Round 1: 5.5–7.0
- Round 2: 6.0–6.5 (paper is clearly better than the 5.75 incremental PnP analysis, comparable to 6.25–6.50 papers with novel methods + theory + experiments, below the 6.75 and 8.0 papers)

**Final reasoning:** The paper makes a genuinely novel contribution (AC-DC denoiser) supported by non-trivial theory and comprehensive experiments. It is clearly stronger than the rejected PnP-ADMM mismatch paper (HXjXPQU3yJ, 6.25) due to broader scope and more novel method design. It is comparable to "Decomposed Diffusion Sampler" (6.50, Accept) and "Restoration Network as Implicit Prior" (6.25, Accept). The missing computational cost reporting and theory-practice gap prevent it from reaching the 6.75+ range. 

**Score: 6.5**

The paper presents a well-motivated, novel algorithm with formal convergence guarantees and strong empirical results. The weaknesses (theory-practice gap, missing computational cost, limited ablation) are real but addressable in revision and do not invalidate the contribution. This is a borderline accept paper that makes a clear positive contribution to the PnP/inverse problems literature.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>