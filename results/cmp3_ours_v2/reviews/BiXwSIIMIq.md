Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes AC-DC, a three-stage score-based denoiser (additive Gaussian noise for auto-correction, conditional Langevin dynamics for directional correction, then Tweedie/ODE denoising) designed to mitigate the manifold mismatch between ADMM iterates and the noisy data distributions score functions are trained on. The authors provide convergence analysis establishing weakly nonexpansive fixed-point ball convergence and bounded-denoiser guarantees, and evaluate on 7 inverse problems across 2 datasets with several baselines.

## Strengths

1. **The manifold-mismatch problem in ADMM-PnP with score denoisers is genuinely identified and well-motivated.** The paper correctly identifies that ADMM dual variables distort the noise geometry beyond what primal-only PnP methods face (Sec. 2, "Challenges — Manifold Mismatch and Convergence"), and argues that simple noise injection alone is insufficient to resolve this.

2. **The AC-DC three-stage denoiser is a novel and structurally reasonable design.** The idea of adding noise (AC), running conditional Langevin dynamics (DC) to steer the iterate toward the score's training manifold, and then applying Tweedie denoising is coherently presented in Algorithm 1. Figure 5 provides direct evidence that increasing DC steps (J=0 vs. J=10 vs. J=20) meaningfully improves reconstruction quality.

3. **The convergence analysis is non-trivial and extends a known line of work.** Theorems 2 and 3 adapt the ADMM-PnP convergence framework (Ryu et al. 2019; Chan et al. 2016) to a score-based denoiser, which is not a standard proximal operator. The high-probability weakly nonexpansive bound (Eq. 14) and the bounded-denoiser result (Theorem 3a) represent genuine theoretical effort on a hard problem.

4. **Broad experimental evaluation.** The method is evaluated on 7 inverse problems (super-resolution, Gaussian/motion deblurring, random/box inpainting, phase retrieval, and a nonlinear deblurring task described in the appendix) across two datasets (FFHQ and ImageNet 256×256), which is more comprehensive than many PnP papers.

## Weaknesses

### Major

1. **The convergence guarantees require noise parameters to vanish asymptotically, creating a gap between theory and the practical regime.** Theorem 2(b) requires \(\lim_{k\to\infty} (\sigma^{(k)})^2 \nu_k = 0\) (forcing \(\sigma^{(k)}\to 0\)), and Theorem 3(b) explicitly requires \(\lim \sigma^{(k)} = 0, \lim \sigma_{s^{(k)}} = 0\). When \(\sigma\to 0\), the AC step adds negligible noise, the Langevin drift is negligible, and Tweedie denoising approaches the identity — meaning the asymptotic convergence guarantees apply most directly when the denoiser is least active. The paper acknowledges this partially in the Limitations ("does not directly explain the reason why the AC-DC denoiser attains high-quality recovery"), but the abstract and introduction frame the guarantees as stronger than they are. The practical algorithm runs with \(\sigma\) decaying from 10 to 0.1 over a finite horizon (\(K = W+10\)), so the asymptotic theory does not directly cover the finite-horizon regime where \(\sigma > 0\). Theorem 2(a) provides per-iteration finite-\(\sigma\) bounds, but these require the condition \(\sigma_{s^{(k)}}^2 + (\sigma^{(k)})^2 < 1/M\), which may not be satisfied at early iterations with \(\sigma=10\) if \(M\) (the smoothness constant of \(\log p_{\text{data}}\)) is large.

2. **No statistical uncertainty is reported for any experimental result, making it difficult to assess significance.** Table 1 reports a single PSNR/SSIM/LPIPS value per method per task averaged over 100 images, with no standard deviation, confidence interval, or other variance measure. Many differences between the proposed method and the second-best baseline are modest (e.g., super-resolution FFHQ: 30.44 vs. 29.53 for DAPS — a 0.9 dB gap; phase retrieval FFHQ: 27.94 vs. 26.71 for DAPS — a 1.2 dB gap). Without error bars, the reader cannot assess whether these improvements are meaningful or within noise.

### Minor

3. **Computational cost is not reported or controlled.** Each ADMM iteration uses up to 1000 Adam iterations for subproblem (7a), plus J=10 Langevin steps (each evaluating \(s_\theta\)) for the DC stage, plus additional score evaluations for denoising. By contrast, methods like DPS, DDRM, and DiffPIR run a single diffusion reverse process per image. The paper acknowledges high NFE cost in the Limitations but does not report wall-clock time, total score evaluations, or a PSNR-vs-compute curve. Without this, it is impossible to determine whether improved metrics reflect a genuinely better prior or simply more computation.

4. **A key hyperparameter (W, the decay window length) is unspecified.** The \(\sigma\) schedule is defined as "linear schedule … over \(W\) decay window" and \(K = W + 10\), but \(W\) is never given a value. This breaks reproducibility of the core algorithm.

5. **The symbol \(\sigma_{z_t}\) in the DC drift term (Algorithm 1, line 5) is not defined anywhere in the paper.** The surrounding text (Eq. 9–10 and the Gaussian approximation discussion) mentions \(\sigma_{\text{ac}}^{(k)}\) but never \(\sigma_{z_t}\), leaving a gap in the algorithm specification.

6. **Several baseline inconsistencies in Table 1.** DPIR is listed as a baseline (Sec. 6) but does not appear in any table column. DDPM appears in the Gaussian blur block but was not listed among the baselines. "DiPIR" in the table appears to be a typo for "DiffPIR". Empty cells for PMC across several tasks are unexplained.

### Trivial

None.

## Nice-to-Haves

- The DC ablation (Fig. 5) is shown only for phase retrieval. Showing it across more tasks would strengthen evidence for the DC stage's general importance.
- The theoretical condition \(\sigma_{s^{(k)}}^2 + (\sigma^{(k)})^2 < 1/M\) could be checked against the practical parameter settings (\(\sigma^{(k)}\) starting at 10) to clarify when during the iterations the theory's guarantees apply.
- A more substantive comparison with the manifold-constrained guidance of Chung et al. (2022), which the paper currently only mentions in passing, would help position the AC-DC contribution relative to other manifold-alignment strategies.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **C1 as "Fatal"**: The original harsh critic labeled the convergence-theory gap as structural/fatal. I demoted it to Major because (a) Theorem 2(a) provides a finite-iteration probabilistic bound for any \(\sigma\) (Eq. 14), which is not vacuous even when \(\sigma>0\); (b) asymptotic \(\sigma\to 0\) requirements are standard in PnP convergence theory; (c) the paper explicitly acknowledges this gap in the Limitations. It is a serious weakness but not fatal.
- **Missing comparison with Chung et al. (2022) manifold constraint**: The paper does mention Chung et al. (2022) in the Related Works section (line 263). The criticism was that the comparison is not substantive enough — moved to Nice-to-Haves.
- **Satisfiability of Theorem 1's compound condition**: The reviewer questioned whether the condition is satisfiable but provided no evidence it is not. Speculative concern without verifiable flaw.
- **Langevin mixing concern with J=10 steps**: The paper footnotes a counterpart without the stationary-distribution assumption in Appendix E.2. Since the appendix is stripped by the parser, this cannot be confirmed from the main text, but the paper does claim to address it.
- **Dimension-dependent bound scaling (\(\sqrt{d}\))**: Inherent to high-dimensional probability bounds in this literature; not a specific weakness of this paper.
- **Abstract claim overstated**: Subsumed by Major weaknesses #1 and #2.
- **Missing related works / formatting/style nitpicks**: Removed per review guidelines.

## Novel Insights

The review process surfaces a structural tension that the paper does not fully reckon with: the convergence theory requires noise parameters to vanish for the asymptotic guarantees to apply, but the practical effectiveness of the AC-DC denoiser depends on operating at non-negligible noise levels where the theory's assumptions may not hold or the ball radius may be too large to be meaningful. This tension between tractability and applicability is common in the PnP convergence literature, but it is particularly salient here because the paper's core algorithmic contribution (the AC-DC mechanism) is explicitly designed around noise-aware manifold alignment. A secondary insight is that the paper's empirical claims would be substantially more convincing with basic statistical reporting (error bars on the 100-image averages) and computational cost accounting — neither of which requires additional experiments.

## Suggestions

1. **Report standard deviations or 95% CIs on all entries in Table 1.** The 100-image evaluations already have the data; this requires only post-processing.
2. **Report either wall-clock time or total number of score evaluations (NFEs) per image** for each method, and ideally a PSNR-vs-NFE plot.
3. **Specify the value of \(W\)** used in the experiments.
4. **Define \(\sigma_{z_t}\)** in Algorithm 1 (or reconcile it with the \(\sigma_{\text{ac}}^{(k)}\) notation from the text).
5. **Clarify the empirical values of \(M\)** (the smoothness constant of \(\log p_{\text{data}}\)) relevant to image distributions, and whether the condition \(\sigma_{s^{(k)}}^2 + (\sigma^{(k)})^2 < 1/M\) is satisfied at early iterations.
6. **Reconcile the baseline list** (DPIR, etc.) with what actually appears in Table 1, and explain empty PMC cells.

## Score and Decision

### Calibration Anchors

Retrieved anchors (PnP-ADMM / diffusion-based inverse problem papers from the 13k calibration corpus):

| Path | Avg Human Score | Round | Comparison to this paper |
|------|----------------|-------|------------------------|
| Prior Mismatch in PnP-ADMM (HXjXPQU3yJ) | 6.25 (Reject) | R1 | Very similar topic (PnP-ADMM with denoiser mismatch + convergence). Had cleaner theory but narrower experiments (2 tasks). Comparable quality. |
| Restoration Network as Implicit Prior (x7d1qXEn1e) | 6.25 (Accept) | R1 | Theory + experiments; no error bars. Similar contribution level. |
| Plug-and-Play Posterior Sampling (66arKkGiFy) | 5.75 (Accept) | R2 | Theory on mismatched PnP-ULA. Similar weaknesses (unclear practical implications of bounds). |
| PnP-Flow (5AtHrq3B5R) | 5.50 (Accept) | R2 | Flow matching + PnP. Similar breadth of experiments. |
| Variational Perspective (1YO4EE3SPB) | 5.50 (Accept) | R2 | Diffusion models for inverse problems. |
| Fast Noise-Robust Diffusion Solvers (Z9Odi09Rv9) | 4.75 (Reject) | R2 | Comparable experimental issues. |

**Round 1 bracket**: [4.0, 6.5] — based on similarity to PnP-ADMM anchors at 6.25 and lower-end diffusion inverse problem solvers at 4.75.

**Final calibration**: The paper sits near the upper end of the bracket. Its AC-DC mechanism is more novel than the analyses in the 5.5-5.75 anchors, and its experimental breadth exceeds most. However, the theory-practice gap (denoiser vanishing asymptotically) is a more significant weakness than any single issue in those accepted anchors, and the reporting gaps (no error bars, no compute comparison) are shared with that tier. Weighting these factors yields a score in the borderline-accept range.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>