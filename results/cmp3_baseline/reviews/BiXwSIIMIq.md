## Summary

The paper addresses two challenges in integrating score-based denoisers with ADMM for inverse problems: (i) the mismatch between ADMM iterates and the noisy manifolds on which score functions are trained, and (ii) the lack of convergence guarantees. It proposes the AC-DC denoiser, a three-stage procedure (auto-correction via additive noise, directional correction via Langevin dynamics, and Tweedie/ODE denoising) that brings ADMM iterates closer to score manifolds, and provides convergence analyses under both fixed-step (weakly nonexpansive operators) and adaptive-step (bounded denoiser) settings. Experiments across six inverse problems on FFHQ and ImageNet consistently improve over strong baselines like DPS, DDRM, and DiffPIR.

## Strengths

1. **Well-motivated and clear problem formulation.** The paper clearly identifies the manifold mismatch issue as a core obstacle when plugging score-based denoisers into ADMM—especially the additional distortion from dual variables—and designs a method specifically to address it.

2. **Novel three-stage AC-DC denoiser.** The combination of auto-correction (Gaussian perturbation) and directional correction (conditional Langevin dynamics) before the final score-based denoising is a principled and effective way to align ADMM iterates with the score’s training manifolds. The ablation study (Fig. 5) confirms the critical role of the DC stage.

3. **First convergence guarantees for score-based ADMM-PnP.** The paper extends fixed-point ball convergence (weakly nonexpansive operators) from classical PnP to score-based denoisers, and also provides high-probability convergence under adaptive step sizes without strong convexity. These results are non-trivial given the implicit nature of the score-based denoiser.

4. **Strong and consistent empirical results.** On 6 inverse problems (super-resolution, random/box inpainting, Gaussian/motion deblurring, phase retrieval) over two datasets, both Tweedie and ODE variants of the proposed method achieve the best or second-best PSNR/SSIM/LPIPS in almost all settings, often outperforming popular baselines by a noticeable margin.

5. **Acknowledged limitations and future directions.** The paper honestly discusses its remaining gaps (the need for constant step-size convergence without convexity, the heuristic noise schedules, computational cost) and thereby provides a clear roadmap for follow-up work.

## Weaknesses

### Fatal

None.

### Major

1. **Convergence analysis relies on strong assumptions that are not fully verified for real data distributions.**  
   The proofs require Assumption 2 (smoothness of log data density with constant \(M\)) and Assumption 3 (coercivity of \(-\log p_{\text{data}}\)). For natural images, these properties are not obviously satisfied, and the paper does not discuss why they might hold or how sensitive the bounds are to violations. Theorem 2 and 3 also assume that the DC Langevin dynamics reaches its stationary distribution for each ADMM iteration—a condition that is not met in practice (only a few steps are run). While the authors claim that counterparts without this assumption exist in the appendix (which is stripped), the main text itself does not provide a practical relaxation.

2. **The weak form of convergence (ball convergence) and high-probability guarantees leave practical confidence unclear.**  
   The results guarantee convergence to a neighborhood of a fixed point (not exact convergence) with a probability that depends on a schedule of \(\nu_k\). The conditions for this schedule require \(\sigma^{(k)}\to0\) at a specific rate, which may conflict with the need for sufficient denoising strength early in the algorithm. The practical implications of these bounds—especially the size of the ball \(r\)—are not numerically characterized.

3. **Computational efficiency is not evaluated.**  
   The AC-DC denoiser requires multiple score evaluations per ADMM iteration (e.g., \(J=10\) Langevin steps plus the final Tweedie step). The paper acknowledges this as a limitation but provides no comparison of runtime, number of function evaluations (NFEs), or wall-clock time against baselines. Without this, it is unclear whether the improved metrics come at a prohibitive computational cost.

### Minor

1. **Experimental details are somewhat sparse.**  
   Hyperparameters for baselines (e.g., DPS, DDRM, DiffPIR) are not given in the main text; it is not clear whether those methods were tuned comparably. The paper states that 100 test images are used, but no error bars (standard deviation / confidence intervals) are reported for any metric, making it hard to assess statistical significance.

2. **The scheduling of \(\sigma^{(k)}\) and \(\sigma_{s^{(k)}}\) is heuristic.**  
   The linear decay schedule and the choice \(\sigma_{s^{(k)}} = 0.1/\sqrt{\sigma^{(k)}}\) are empirically motivated and not tied to the theoretical conditions derived in Section 4. The authors label this as a limitation, but it nevertheless weakens the connection between theory and practice.

### Trivial

None.

## Nice-to-Haves

* An empirical study of how the number of DC steps (\(J\)) trades off quality versus runtime would be very helpful for practitioners.
* A sensitivity analysis showing how the convergence ball radius \(r\) (from Theorem 1) behaves for different datasets would increase trust in the theoretical guarantees.
* Including a few confidence intervals or error bars on the quantitative metrics in Table 1 would strengthen the empirical claims.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the mismatch between optimization iterates and score manifolds can be systematically corrected by a two-step “pull-then-refine” procedure: first, adding Gaussian noise to bring iterates into a region where the score is reliable (auto-correction), and second, using conditional Langevin dynamics to align the iterate with the specific noisy manifold corresponding to the current denoising level (directional correction). This separation of concerns—handling distance to the manifold and position within the manifold separately—provides a template that could be adapted to other optimization frameworks (e.g., proximal gradient, FISTA) beyond ADMM.

## Suggestions

1. In the experimental section, report the average number of NFEs and wall-clock time for each method so that readers can judge the practical cost of the AC-DC denoiser.
2. Add a short discussion—even if informal—of why Assumptions 2–3 might be reasonable for image data (e.g., bounded pixel range, smoothness of natural image distributions) or provide a small numerical check (e.g., estimated Lipschitz constant of a trained score on a sample batch).
3. Include an ablation where the DC Langevin steps are replaced by the same number of unconditional Langevin steps (without the conditioning term) to isolate the effect of the directional correction.

## Score and Decision

**Score:** 8  
**Decision:** Accept  

The paper makes a significant contribution by proposing a principled solution to the manifold mismatch problem when using score-based denoisers in ADMM, providing the first convergence analysis for such a combination, and demonstrating consistent empirical improvements across a broad range of inverse problems. While the theoretical analysis relies on assumptions that are not perfectly tailored to practice, and the computational cost is not quantified, the overall novelty, technical depth, and empirical strength justify acceptance at a top venue.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>