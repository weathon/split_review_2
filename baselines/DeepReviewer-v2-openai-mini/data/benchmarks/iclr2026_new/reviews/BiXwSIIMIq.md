## Summary
# Final Review Report

## Summary

This paper presents AC-DC, a three-stage score-based denoiser designed for integration into the ADMM plug-and-play (PnP) framework for solving inverse problems. The denoiser consists of auto-correction (AC) via additive Gaussian noise, directional correction (DC) via conditional Langevin dynamics, and score-based denoising (Tweedie or ODE). The key motivation is to address the manifold mismatch between ADMM iterates (whose distribution includes dual-variable distortions) and the noisy data manifolds on which pre-trained score functions operate.

On the theoretical side, the authors establish convergence properties under two settings: (1) weakly nonexpansive denoiser residuals leading to fixed-point ball convergence under constant step size with strongly convex data-fidelity terms; (2) bounded denoiser property leading to convergence under adaptive step-size schedules without convexity. Empirically, the method is evaluated on FFHQ and ImageNet across six inverse problems (super-resolution, Gaussian/motion deblurring, random/box inpainting, phase retrieval) and compared against 7-8 baselines.

The paper addresses a well-motivated problem and provides both algorithmic innovation and theoretical analysis. However, several issues in experimental rigor, notation consistency, and theory-practice gap require attention before the paper can be considered fully convincing.

## Strengths
1. **Well-motivated problem.** The paper identifies a genuine challenge in score-based PnP methods: the mismatch between the noise manifolds on which score functions are trained and the geometry of ADMM iterates (especially due to dual variables). This is a nuanced problem that prior work has not systematically addressed, and the AC-DC denoiser provides a principled three-stage solution.

2. **Novel algorithmic design.** The AC-DC denoiser's three-stage structure (AC for approximate manifold alignment via Gaussian noise injection, DC for Langevin-based refinement, and score-based denoising) is a reasonable approach to the stated problem. The use of conditional Langevin dynamics to target p(z_{σ^{(k)}} | z_{ac}^{(k)}) is technically interesting, as it aims to bring iterates closer to score-manifold points while retaining measurement information.

3. **Sound theoretical framework.** The paper provides convergence analysis under two complementary settings (fixed step size with convexity, adaptive step size without convexity), extending prior ADMM-PnP theory (Ryu et al., 2019; Chan et al., 2016) to score-based denoisers. The high-probability bounds and the concept of weak non-expansiveness are appropriate tools for the stochastic nature of the denoiser.

4. **Broad empirical evaluation.** The method is tested on six inverse problems across two datasets (FFHQ, ImageNet), comparing against 7-8 baselines including DPS, DDRM, DiffPIR, RED-diff, DAPS, DCDP, and PMC. The results consistently place the proposed method at or near the top across most tasks.

5. **Good candidate for related-work positioning.** The paper situates itself well within the existing literature, clearly distinguishing itself from posterior-sampling methods (DPS, DDRM) and PnP optimization methods (DiffPIR, RED-diff, SNORE).

## Weaknesses
### W1. Undefined symbols and notation inconsistency in Algorithm 1 (Page 1 - Method)
Algorithm 1, line 5 uses the symbol $\sigma_{z_t}$ which is never defined in the paper. Based on context, this should be $\sigma^{(k)}$ or $\sigma_{ac}^{(k)}$, but the current notation makes the algorithm ambiguous and harms reproducibility. Additionally, the noise variable $\mathbf{n}$ is overloaded: it appears both as the AC noise (line 1, $\sigma^{(k)}\mathbf{n}$) and as the Langevin noise (line 5, $\sqrt{2\eta^{(k)}}\mathbf{n}$), without explicit statement that these are independent draws. This is a **major** issue because the algorithm is the paper's central contribution and must be precisely specified for reproduction.

### W2. Missing variance and statistical significance in Table 1 (Page 1 - Experiments)
Table 1 reports only point estimates (PSNR, SSIM, LPIPS) without any standard deviations, confidence intervals, or significance tests. For a 100-image sample, reporting standard errors is standard practice. Many performance differences between the proposed method and the second-best baseline are small (e.g., Super-resolution FFHQ: Ours-tweedie 30.439 vs DAPS 29.529, delta ~0.9 dB; Box inpainting FFHQ: DCDP 25.230 actually *exceeds* Ours-tweedie 24.025). Without variance information, readers cannot determine whether the reported advantages are statistically reliable. This is a **major** weakness that undermines the empirical claims.

### W3. Critical theory-practice gap: stationary distribution assumption (Page 1 - Theorem 2)
Theorems 2 and 3 assume that the DC Langevin dynamics reaches its stationary distribution at each ADMM iteration. However, the experiments use only J=10 DC steps. In high-dimensional image spaces (e.g., 256×256 = 196,608 dimensions), 10 Langevin iterations are orders of magnitude too few to approach stationarity. The paper does not discuss this gap or provide any empirical evidence that the iterates approximately satisfy the required conditions. This substantially weakens the relevance of the convergence theory to the actual algorithm being evaluated.

### W4. Coefficient inconsistency in ADMM update (Page 1 - Method)
Equation (7b) presents the $\mathbf{z}$-subproblem with coefficient $2/\rho$, whereas standard ADMM derivation for the augmented Lagrangian in Eq. (6) would produce a coefficient of $\gamma/\rho$. The regularization parameter $\gamma$ is introduced in Eq. (6) but never explicitly defined or used elsewhere. This inconsistency makes the optimization problem formulation ambiguous and hinders reproducibility.

### W5. Insufficient component ablation (Page 1 - Experiments)
The ablation study only examines the DC step count (J = 0, 10, 20) on a single task (phase retrieval) with only visual comparison. There are no quantitative ablation results, no ablation of the AC step alone, no separation of Tweedie vs ODE denoising effects, and no ablation across multiple tasks. Given that the AC-DC denoiser is the paper's primary claimed contribution, the component analysis is too thin to convincingly attribute the performance gains to the proposed design.

### W6. Unverified Gaussian approximation in DC step (Page 1 - Method)
The DC Langevin step relies on approximating $\nabla\log p(\mathbf{z}_{ac}^{(k)}|\mathbf{z}_{\sigma^{(k)}}) \approx -1/\sigma_{ac}^{(k)}(\mathbf{z}_{\sigma^{(k)}} - \mathbf{z}_{ac}^{(k)})$, which requires $\text{Var}(\mathbf{s}^{(k)})^{1/2} \ll \sigma^{(k)}$. This condition is asserted without any theoretical justification or empirical verification. If this condition is violated during ADMM iterations (especially early ones), the Langevin dynamics may target the wrong distribution, potentially degrading performance.

### W7. Missing hyperparameter $W$ (Page 1 - Hyperparameter Settings)
The noise schedule $\sigma^{(k)} = \max(0.1, 10 - (10-0.1)k/W)$ depends critically on the decay window $W$, but $W$ is never specified. The iteration count $K = W + 10$ is therefore also unknown. This omission makes the experimental setup unreproducible. Reviewers and readers cannot run the method without guessing $W$.

### W8. Table 1 quality issues (Page 1 - Experiments)
The main result table contains several anomalies: (a) "DiPIR" and "DiffPIR" are used inconsistently across tasks; (b) "DDPM" appears as a baseline in Gaussian blur but was not listed in the Baselines paragraph; (c) "PMC" rows have inconsistent formatting with many empty cells (e.g., random inpainting - PMC has all blanks); (d) the "Superresolution" section lists two PMC entries with contradictory metrics. These issues reduce confidence in the reported numbers.

### W9. Overclaim in abstract (Page 1 - Abstract)
The abstract states "ensuring high-probability fixed-point *ball convergence*" without noting that Definition 2 explicitly characterizes this as a weaker property than fixed-point convergence (the iterate stays within a $\delta$-ball, not converging to a point). The abstract also claims "consistently improves solution quality," but Table 1 shows several tasks where the method is second-best (e.g., box inpainting FFHQ: DCDP outperforms Ours-tweedie). The abstract should be revised to accurately bound the scope of the theoretical and empirical claims.

### W10. Limitations section omissions (Page 1 - Conclusion)
The limitations paragraph acknowledges several gaps but omits the most critical one: the stationary-distribution assumption in Theorems 2-3. It also claims "our experiments suggest that constant step sizes also perform well for nonconvex objectives" without providing any supporting evidence or references. This claim should either be backed by experimental data or removed.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a well-motivated and timely problem with a technically interesting algorithmic contribution (AC-DC denoiser) and provides both convergence analysis and broad empirical evaluation. However, several significant weaknesses prevent a higher score:

- **Notation and reproducibility issues (W1, W4, W7, W8):** The core algorithm contains undefined symbols ($\sigma_{z_t}$), inconsistent coefficients in the ADMM update, and missing hyperparameter $W$ that together make reproduction difficult.

- **Statistical rigor gap (W2):** The absence of any variance reporting or significance testing makes it impossible to assess whether the reported performance gains are statistically meaningful, especially for tasks where margins are small or where the method is second-best.

- **Theory-practice disconnect (W3, W6):** The convergence analysis relies on strong assumptions (Langevin stationarity, unverified Gaussian approximation) that are almost certainly violated in practice, substantially weakening the practical relevance of the theoretical contributions.

- **Insufficient ablation (W5):** The component analysis is too limited to convincingly attribute gains to the proposed AC-DC design, which is the paper's central algorithmic contribution.

- **Honest but incomplete limitation discussion (W10):** The limitations section is candid about some issues but omits the most critical gap (stationary distribution assumption).

**Novelty assessment (deferred — Retrieval-Disabled Mode):** External literature verification was unavailable in this run. The paper's conceptual contributions (AC-DC denoiser, convergence analysis extending Ryu et al. 2019 to score-based denoisers) appear meaningful, but a definitive novelty judgment requires manual comparison against the complete set of score-based PnP methods. The authors should verify that the AC-DC design is not substantially overlapped with existing manifold-correction techniques in the diffusion inverse-problem literature.

The paper has solid foundations and addresses an important problem. Addressing the reproducibility, statistical rigor, and ablation gaps would significantly strengthen the contribution.