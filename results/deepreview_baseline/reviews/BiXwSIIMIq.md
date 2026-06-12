## Summary

This paper proposes AC-DC, a three-stage score-based denoiser (auto-correction via additive Gaussian noise, directional correction via conditional Langevin dynamics, and score-based denoising) designed for integration within the ADMM plug-and-play (PnP) framework for solving inverse problems. The authors address the manifold mismatch between ADMM iterates and the noisy data manifolds on which score functions are trained, and provide convergence guarantees for ADMM-PnP with the AC-DC denoiser under both fixed and adaptive step-size schedules. Experiments on multiple inverse problems (inpainting, deblurring, super-resolution, phase retrieval) demonstrate improved solution quality over several baselines.

## Strengths

- **Novel denoiser design addressing a genuine challenge:** The paper identifies a real and important problem—the mismatch between ADMM iterates (especially with dual variables) and the noisy manifolds score functions are trained on. The three-stage AC-DC denoiser is a principled attempt to bridge this gap, with clear motivation for each stage (AC for noise injection, DC for manifold alignment via Langevin dynamics, and final Tweedie denoising).
- **Convergence analysis for score-based ADMM-PnP:** The paper provides two convergence results: (1) weakly nonexpansive fixed-point ball convergence under constant step size with strongly convex losses, and (2) convergence under adaptive step sizes without convexity. This extends prior ADMM-PnP theory (Ryu et al., 2019; Chan et al., 2016) to the score-based setting, which is nontrivial given the stochastic nature of the denoiser.
- **Strong empirical performance:** The method consistently achieves best or second-best results across a wide range of inverse problems (super-resolution, random/box inpainting, motion/Gaussian deblurring, phase retrieval) on both FFHQ and ImageNet datasets, with clear qualitative improvements visible in the figures.
- **Ablation on DC steps:** Figure 5 provides a clean ablation showing that increasing the number of DC steps progressively improves reconstruction quality, validating the importance of the directional correction stage.

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical gap between analysis and practical algorithm:** The convergence analysis relies on the assumption that the DC step reaches the stationary distribution for each ADMM iteration (Theorems 2 and 3). In practice, only a small fixed number of Langevin steps (J=10) is used, which is far from convergence to stationarity. The paper acknowledges this assumption "for notation conciseness" and refers to Appendix E.2 for counterparts removing it, but the main text's theoretical claims are built on an assumption that is not satisfied in experiments. This significantly weakens the practical relevance of the convergence guarantees.

2. **Convergence results are relatively weak:** The main convergence result (Theorem 1) establishes convergence to a *ball* (not a fixed point), with the ball radius depending on δ. While the paper acknowledges this, the practical meaning of "convergence to a ball" is limited—it essentially guarantees that iterates do not diverge, but does not guarantee they approach a meaningful solution. The adaptive step-size result (Theorem 3) does achieve fixed-point convergence, but adaptive step sizes are acknowledged as "arguably less appealing in practice."

3. **Computational cost is not adequately addressed:** The AC-DC denoiser requires multiple score evaluations per ADMM iteration (J=10 DC steps plus the final denoising step). The paper mentions this as a limitation but provides no runtime comparisons or analysis of the trade-off between computational cost and quality improvement. Given that baselines like DPS and DiffPIR are already computationally expensive, it is important to understand whether the improved quality justifies the additional cost.

4. **Limited comparison with recent score-based PnP methods:** The baselines include DPS, DDRM, DiffPIR, RED-diff, and DAPS, but several recent score-based PnP methods (e.g., SNORE, DDNM, GDP, PnP-Diffusion) are not compared. Given that the paper's contribution is specifically about integrating score denoisers into ADMM, a more comprehensive comparison with other score-based PnP approaches would strengthen the empirical evaluation.

### Minor

1. **The notation in Section 3 (Eq. 9) is confusing and appears garbled:** The decomposition of z_ac^(k) and the definition of s^(k) are unclear. The equation seems to have typesetting issues (e.g., "z_σ^(k) is denoised signal of z̃^(k), z_σ^(k) = z_σ^(k) + σ^(k)n_1" is circular). This makes the theoretical motivation for the DC step harder to follow.

2. **The relationship between σ^(k) and the score model's noise levels is not specified:** The paper uses a linear schedule for σ^(k) from 0.1 to 10, but it is unclear how this relates to the noise levels used during training of the score model. The effectiveness of the AC-DC denoiser depends on σ^(k) matching the trained noise levels, but this connection is not discussed.

3. **The adaptive step-size schedule is not specified:** Theorem 3 references the "p-increasing rule" from Chan et al. (2016), but the paper does not describe how this is implemented or whether it was used in experiments (the experiments use constant step size). This makes it unclear whether the adaptive step-size convergence result has any empirical validation.

### Trivial
None.

## Nice-to-Haves

- A runtime comparison table showing average inference time per image for each method would help practitioners assess the practical trade-offs.
- An analysis of how the number of DC steps (J) affects both quality and convergence speed would strengthen the practical guidance.
- Visualizing the manifold alignment (e.g., via t-SNE or by tracking the distance to the nearest training manifold) could provide empirical support for the claimed mechanism of the AC-DC denoiser.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is that the dual variables in ADMM exacerbate the manifold mismatch problem for score-based denoisers, making primal-dual methods particularly challenging for PnP with diffusion models. This insight—that the noise geometry of ADMM iterates is fundamentally different from that of primal methods—explains why score-based denoising has rarely been combined with ADMM and motivates the need for specialized correction mechanisms like AC-DC. The paper's approach of using conditional Langevin dynamics to "steer" iterates toward the correct manifold while preserving measurement information is a clever way to address this issue.

## Suggestions

- **Clarify the practical validity of the convergence analysis:** Either provide the results from Appendix E.2 (without the stationary distribution assumption) in the main text, or explicitly state the gap between theory and practice and discuss what the theory implies for the practical algorithm (e.g., that with enough DC steps, convergence is plausible).
- **Add runtime comparisons:** Include a table or figure showing average inference time per image for all methods, along with the quality metrics, so readers can assess the cost-benefit trade-off.
- **Expand the baseline comparison:** Include more recent score-based PnP methods (e.g., SNORE, DDNM) to better contextualize the empirical contribution.
- **Clarify the noise schedule alignment:** Discuss how the chosen σ^(k) schedule relates to the trained noise levels of the score model, and whether the results are sensitive to this choice.

## Score and Decision

The paper addresses a genuine and important challenge (manifold mismatch in score-based ADMM-PnP) with a well-motivated denoiser design and provides convergence analysis that extends prior theory. The empirical results are strong across multiple tasks and datasets. However, the convergence analysis has a significant gap between theoretical assumptions (stationary distribution for DC) and practical implementation (J=10 steps), and the computational cost is not adequately evaluated. The paper makes a solid contribution but has room for improvement in bridging theory and practice.

**Score: 6** (borderline accept)

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>