## Summary

This paper proposes the AC-DC denoiser, a three-stage score-based denoiser (Auto-Correction via additive Gaussian noise, Directional Correction via conditional Langevin dynamics, and Tweedie/ODE denoising) designed for integration within the ADMM plug-and-play framework. The method addresses manifold mismatch between ADMM iterates and the noisy manifolds on which diffusion score functions are trained. The authors provide convergence analysis extending ADMM-PnP theory and evaluate on 7 inverse problems across 2 datasets against 8+ baselines.

## Strengths

1. **The AC-DC denoiser is a conceptually clean three-stage design (Algorithm 1, Figure 1).** The decomposition into AC (additive Gaussian noise to bring iterates nearer to some $\mathcal{M}_{\sigma(t)}$), DC (conditional Langevin dynamics to refine alignment), and final Tweedie/ODE denoising is well-motivated by the manifold mismatch diagnosis. The ablation in Figure 5 (phase retrieval with J=0 vs J=10 vs J=20) provides direct evidence that the DC stage contributes to recovery quality.

2. **Broad and thorough experimental evaluation (Table 1, Figures 2–4).** The paper evaluates on 7 inverse problems (super-resolution, random/box inpainting, Gaussian/motion deblurring, phase retrieval, HDR) × 2 datasets (FFHQ, ImageNet) × 3 metrics × 8+ baselines. Both Ours-tweedie and Ours-ode variants consistently achieve best or second-best results across most settings. This breadth substantially exceeds most PnP papers and provides reasonable evidence of effectiveness across diverse conditions.

3. **Honest and thorough limitations discussion (Section 7).** The paper candidly acknowledges that the constant step-size theory does not cover the nonconvex problems tested, that convergence guarantees are about stability not recovery quality, that noise schedules are empirical, and that the method is computationally expensive. This transparency helps readers assess the scope of the contributions.

## Weaknesses

### Fatal

None.

### Major

1. **Undefined parameter $\sigma_{z_t}^2$ in Algorithm 1 (reproducibility gap).** Algorithm 1 line 5 uses $\frac{1}{\sigma_{z_t}^2}(z_{\text{ac}}^{(k)} - \mathbf{w}^{(k,j)})$ in the Langevin update. The quantity $\sigma_{z_t}^2$ is never defined in the main paper — it does not appear in the hyperparameter settings (Section 6, line 297), is not derived from the Gaussian approximation described in Section 3, and the text explanation (line 135) instead uses the notation $-\frac{1}{\sigma_{\text{ac}}^{(k)}}$ with a subscript mismatch and missing exponent. The hyperparameters list $\sigma^{(k)}$, $\eta^{(k)}$, and $\sigma_{s^{(k)}}$, but not $\sigma_{z_t}$ or $\sigma_{\text{ac}}^{(k)}$. A reader cannot implement the algorithm from the main paper alone, and the sensitivity of results to this parameter cannot be assessed.

2. **Missing critical control baseline.** The paper compares AC-DC ADMM against DPS, DiffPIR, DDRM, RED-diff, etc., which differ in both the denoiser and the optimization framework. The most informative baseline — ADMM-PnP with the same score-based Tweedie denoiser but *without* the AC-DC stages (i.e., directly applying $D_{\sigma^{(k)}}(\tilde{z}^{(k)})$ in ADMM, no AC, no DC) — is absent. The ablation in Figure 5 shows DC vs no-DC (J=0 still has the AC step), but does not isolate the AC contribution or compare against a "vanilla ADMM + Tweedie" baseline. Without this, it is difficult to attribute the reported improvements specifically to the AC-DC mechanism rather than the ADMM framework or hyperparameter tuning.

3. **Computational cost not reported.** The AC-DC denoiser requires ~12 score evaluations per ADMM iteration (1 AC + 10 DC Langevin + 1 final Tweedie/ODE), with the ADMM outer loop running $K = W+10$ iterations and each x-subproblem (7a) running up to 1000 Adam iterations. Neither NFEs nor wall-clock time are reported relative to baselines. The limitations section mentions the issue qualitatively, but a quantitative comparison is needed for practitioners to assess the quality-cost trade-off.

### Minor

1. **Convergence theory assumptions are restrictive relative to the experimental regime.** Theorem 1 requires $\mu$-strong convexity of $\ell$, which excludes several test problems (phase retrieval is nonconvex, inpainting with a binary mask is rank-deficient, HDR involves clipping/nonlinearities). Theorem 2 assumes the Langevin DC step "reaches the stationary distribution for each $k$," while only $J=10$ steps are used (the paper notes a relaxed version in Appendix E.2, but the main theorem's stated guarantee relies on this strong assumption). The dimension-dependent bounds in (15)–(16) scale with $d$ ($d=65536$ for $256\times256$ images), making the theoretical $r$-ball potentially enormous in practice. The paper's own limitations section acknowledges that the theory "does not directly explain the reason why the AC-DC denoiser attains high-quality recovery." These gaps mean the guarantees as stated do not cover the actual operating regime of the experiments. That said, ADMM-PnP convergence theory for score-based denoisers is acknowledged as challenging, Theorem 3 provides a relaxation without strong convexity (with adaptive step sizes), and Appendix E.2 provides a relaxation of the stationary distribution assumption — the paper is honest about these gaps.

### Trivial

- The "manifold" terminology is imprecise: $\mathcal{M}_{\sigma(t)} = \text{supp}(\mathbf{x}_t) = \mathbb{R}^d$ for Gaussian noise with full support. The paper's intended meaning is that the score is accurate near the *typical set* of $p(\mathbf{x}_t)$, not on a low-dimensional manifold.

## Nice-to-Haves

- Report NFEs and wall-clock time for a fair computational cost comparison against baselines.
- Add a sensitivity analysis for $J$ (number of DC steps) on more than one task (beyond phase retrieval in Figure 5).
- Add sensitivity analysis for the $\sigma_{z_t}$ parameter once it is defined.
- Clarify the notational issues in Section 3 (Equation 9 and surrounding text).

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Strength: "The problem is genuine and well-motivated"** — generic; applies to most papers.
- **Harsh critic's Issue 1 framed as "Structural/Fatal" (convergence theory disconnected from practice)** — downgraded to Minor because (a) the paper acknowledges these gaps in the limitations section, (b) Theorem 3 addresses nonconvex $\ell$ with adaptive steps, and (c) Appendix E.2 relaxes the stationary distribution assumption. The weakness is real but not fatal — the paper's core contribution is the AC-DC denoiser design and empirical results, with theory as supporting evidence.
- **Weakness about missing related works** — removed per meta-reviewer policy (cannot verify external sources).
- **Formatting artifact complaints about Table 1** — parser issues, not author errors.
- **Weakness about score approximation error (Assumption 2 being about true data density, not learned score)** — a generic concern about all methods using pre-trained score functions, not specific to this paper's contribution.
- **Strength about convergence analysis extending prior theory** — partially kept implicitly (the theory is mentioned in Minor weakness 1 as a real but limited contribution).
- **Notational inconsistency in Equation 9 (circular $s^{(k)}$ definition)** — partially a parser artifact; the written intent is understandable.

## Novel Insights

None beyond the paper's own contributions. The review surfaces the tension between the paper's theoretical claims and its practical implementation (the undefined parameter in Algorithm 1 is the most concrete manifestation of this gap), but this is a standard verification finding rather than a novel insight about the science.

## Suggestions

1. **Define $\sigma_{z_t}$ explicitly.** Add this parameter to the hyperparameter settings in Section 6. If $\sigma_{z_t} = \sigma^{(k)}$ or $\sigma_{z_t} = \sigma_{\text{ac}}^{(k)}$ (where $\sigma_{\text{ac}}^{(k)}$ is itself a function of $\sigma^{(k)}$), state this clearly. Alternatively, rename the variable to avoid confusion with the notation used in the text derivation.
2. **Add the missing control baseline.** Run ADMM-PnP with the same score-based Tweedie denoiser applied directly to $\tilde{z}^{(k)}$ (no AC, no DC), under otherwise identical hyperparameters. Report the results in a new column in Table 1 or as a dedicated ablation. This directly isolates the contribution of the AC-DC mechanism.
3. **Report NFEs or wall-clock time.** A table comparing computational cost across methods would greatly aid practitioners in assessing the quality-cost trade-off.
4. **Consider relaxing the stationary-distribution assumption in the main text** or providing empirical diagnostics (e.g., trace plots showing the Langevin chain mixes in $\leq 10$ steps) for the tasks considered.

---

### Calibration Report

**Round 1 bracket:** [5.0, 6.5]

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `HXjXPQU3yJ.md` (Prior Mismatch and Adaptation in PnP-ADMM) | 6.25 | Round 1 | Very similar topic (PnP-ADMM with denoiser mismatch), weaker experiments (SR and deblurring only), stronger theory (nonconvex analysis). Current paper has broader experiments but a reproducibility gap. |
| `1YO4EE3SPB.md` (Variational Perspective on Solving Inverse Problems with Diffusion Models) | 5.50 | Narrow | Similar area (diffusion-based inverse problem solving). Accepted despite theory concerns. Weaker experiments but no undefined parameters. |
| `66arKkGiFy.md` (Plug-and-Play Posterior Sampling under Mismatched Models) | 5.75 | Round 1 | PnP theory paper. Accepted with scores 6,5,6,6. Similar theory-practice gap concerns but no algorithmic contribution. |
| `kNPcOaqC5r.md` (What's in a Prior? Learned Proximal Networks) | 5.75 | Narrow | Learned proximal operators for inverse problems. Accepted. Stronger theory, weaker experiments. |
| `Z9Odi09Rv9.md` (Fast and Noise-Robust Diffusion Solvers) | 4.75 | Round 1 | Diffusion-based inverse solver with technical errors and unfair comparisons. Rejected. |
| `x7d1qXEn1e.md` (A Restoration Network as an Implicit Prior) | 6.25 | Round 1 | Similar PnP extension. Accepted despite experimental concerns. |
| `nHESwXvxWK.md` (Monte Carlo guided Denoising Diffusion) | 4.00 | Round 1 | Highly mixed reviews (1,8,1,6). SMC+diffusion for inverse problems. Accepted despite low average. |

**Calibration reasoning:** The paper under review sits between the 5.50 and 6.25 anchors. It has broader experiments than the "Prior Mismatch" paper (6.25, rejected) but also has a genuine reproducibility gap (undefined parameter) that the compared papers do not have. The algorithmic contribution (AC-DC) is real and well-motivated. The final score of **5.5** reflects a borderline paper with non-fatal but significant issues that should be resolved before acceptance.

**Score justification:** The paper makes a genuine algorithmic contribution with broad empirical support, but the undefined $\sigma_{z_t}^2$ parameter (reproducibility gap), missing control baseline, and unreported computational cost are material weaknesses that prevent acceptance in the current form. None of these are fatal errors, and all are fixable with additional writing, experiments, and analysis.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>