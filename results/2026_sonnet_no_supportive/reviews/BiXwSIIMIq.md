Now I have sufficient understanding of the paper. Let me write the draft review.Based on Round 1, my initial bracket is **6.0–7.5**. The paper is clearly stronger than the 3.5–5.5 range papers (which lack convergence theory or have only heuristic contributions), and comparable to the 5.75–6.75 band — most closely matching "PnP Posterior Sampling under Mismatched Models" (5.75) and "DiffStateGrad" (6.75). Let me read one 6-range and one 8-range anchor.**Round 1 bracket: 6.0–7.5.** DiffStateGrad (6.75, accepted) has a similar manifold-alignment motivation but no convergence theory; Variational Diffusion Posterior Sampling (8.0) has stronger theoretical rigor and NFE reporting. The paper under review sits above DiffStateGrad (it has genuine convergence theory) but below the 8.0 anchor (the NFE omission and dimension-scaling issue are real weaknesses). Final estimate: **6.5**.

---

## Summary

The paper proposes ADMM Plug-and-Play (ADMM-PnP) with the AC-DC denoiser for solving inverse problems. The denoiser has three stages: (1) Auto-Correction (AC) via additive Gaussian noise to pull iterates toward the trained manifolds {M_{σ(t)}}, (2) Directional Correction (DC) via Langevin dynamics targeting p(z_{σ^(k)} | z_ac^(k)) to refine manifold alignment while preserving measurement information, and (3) Tweedie/ODE denoising. The paper also establishes convergence guarantees: Theorem 1 gives fixed-point ball convergence for weakly nonexpansive denoisers; Theorem 2 shows the AC-DC denoiser satisfies this condition; Theorem 3 handles the non-convex case with adaptive step sizes. Experiments span 7 inverse problem tasks, 2 datasets, and 8 baselines.

---

## Strengths

- **Principled AC+DC combination.** The DC step is the genuine advance over AC-only approaches (DiffPIR, RED-diff, SNORE). The key insight from Eq. (9)/(10) — that supp(z_{σ^(k)} | z_ac^(k)) ⊆ M_{σ^(k)} — simultaneously places iterates on the correct manifold and retains measurement information from z_ac^(k). This decomposition is cleanly motivated and non-trivial.

- **Non-trivial extension of ADMM-PnP convergence theory.** Prior results (Ryu et al., 2019; Chan et al., 2016) required strictly contractive denoiser residuals. Theorems 1–3 relax this to weakly nonexpansive (ε ≤ 1 plus bounded additive slack δ), recovering ball convergence and then full fixed-point convergence with adaptive step sizes. The two-theorem structure is clean and the relaxation is meaningful.

- **Comprehensive empirical evaluation.** Seven inverse problem tasks (random/box inpainting, super-resolution, Gaussian/motion deblurring, phase retrieval, HDR) over two 100-image datasets (FFHQ, ImageNet) with comparison to eight baselines across PSNR/SSIM/LPIPS. Ours-tweedie and Ours-ode are at or near top on the vast majority of task-metric-dataset combinations in Table 1. The ablation in Fig. 5 directly isolates the DC stage's contribution on phase retrieval.

---

## Weaknesses

### Fatal
None.

### Major

- **Convergence ball radius potentially vacuous at image scale.** From Eq. (16), δ_k² = 3(2(σ^(k))²(d + 2√(dν_k) + 2ν_k) + ...), so δ_k = O(√d · σ^(k)). For a 256×256 image (d ≈ 196,608), the ball radius r ∝ δ/√(1−ε̄²) scales as √d. Theorem 2(b) does show δ_k → 0 as σ^(k) → 0 asymptotically, so the limiting guarantee is valid; but the finite-iteration bound may be comparable to the entire image-space diameter. The paper's Limitations section (Section 7) does not acknowledge this dimensional scaling, leaving the reader unable to assess how tight the bound is for any practical schedule. At minimum, a remark that the convergence ball collapses in the σ^(k) → 0 limit (rather than offering a meaningful finite-iteration guarantee) is warranted.

- **NFE count not reported; fairness of comparison with DAPS-4K is unclear.** DAPS is labeled "DAPS-4K" in Figures 3–4, explicitly signaling a fixed NFE budget of 4,000. The proposed method uses J=10 Langevin steps per outer iteration, up to 1000 Adam gradient steps for the x-subproblem, and K=W+10 total ADMM iterations, with Ours-ode additionally running a 10-step ODE denoiser — none of this is aggregated into a total NFE figure in Table 1 or elsewhere. Section 7 (Limitations) acknowledges "each iteration of AC-DC denoiser needs multiple score evaluations" as a concern without quantifying it. Without reporting NFEs alongside metrics, it is impossible to determine whether Table 1 performance gains reflect method quality or a larger compute budget.

### Minor

- **Stationary distribution assumption of the DC step.** Theorems 2 and 3 are formally stated under the assumption that the DC step reaches its stationary distribution (footnote 1, Appendix E.2 handles the relaxed version). In practice, J=10 Langevin steps at η^(k) = 5×10⁻⁴σ^(k) in image-dimensional space almost certainly does not reach stationarity. The headline theorems therefore rest on a premise the practical algorithm never satisfies. The appendix counterpart exists but is not prominently flagged in the main text. A more prominent acknowledgment — or a bound on the mixing gap's effect on δ — would make the theory honest.

- **Gaussian approximation for the DC step not tested in adverse regimes.** The DC update (Algorithm 1, line 5) relies on approximating p(z_ac | z_σ) as Gaussian, justified when Var(s^(k))^{1/2} ≪ σ^(k) (Section 3). No experiment or analysis addresses what happens when this condition fails (e.g., early iterations when σ^(k) is large and the approximation is poorest). An assessment of graceful degradation would strengthen the empirical story.

### Trivial

- The decay window W governing σ^(k) = max(0.1, 10−(10−0.1)·k/W) is not specified in the main text, making the hyperparameter description incomplete without reading the appendix.

---

## Nice-to-Haves

- Report total NFEs per image per method alongside Table 1 metrics. This is the most impactful missing piece.
- Report a normalized convergence radius (δ_k/√d, i.e., RMS perturbation per pixel) in the main text to make the theoretical bound interpretable at image scale.
- Provide a quantitative curve of PSNR vs. J over a range of tasks, with NFE cost at each J. Fig. 5 is qualitative and covers only 2 images; a quantitative version would be the paper's strongest ablation.
- Explicitly verify that the linear σ-schedule used in experiments satisfies lim_{k→∞}(σ^(k))² ν_k = 0 (required by Theorem 2(b)/Theorem 3(b)), so readers can confirm the convergence conditions are met.

---

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Duplicated/empty PMC rows and unexplained DDPM baseline in Table 1** — the harsh reviewer's own note calls these "PDF-extraction artifacts, not paper defects." Removed per hard rules.
- **Decomposition z_q ~ p_data is not computable** — this is standard motivational notation in the diffusion literature; the paper is using it to decompose the signal component intuitively, not claiming computational access to z_q. Removed as misreading.
- **Missing NFE comparison with DAPS is "unfair" in the sense favoring the proposed method** — per the rules, if the asymmetry disfavors baselines (and thus the proposed method shows stronger results), this does not constitute unfairness to the proposed method. The NFE point is retained only because it is unclear whether Ours uses *more* compute than DAPS-4K, not because the comparison is presumptively unfair.

---

## Novel Insights

The key structural insight is the conditional-support argument at Eq. (9)/(10): because supp(z_{σ^(k)} | z_ac^(k)) ⊆ supp(z_{σ^(k)}) = M_{σ^(k)}, the conditional Langevin dynamics automatically restricts the DC output to the correct noisy manifold — without discarding measurement information encoded in z_ac^(k). This is more principled than prior noise-injection or purification heuristics, and the Gaussian approximation of the conditional likelihood provides a computationally tractable implementation. The convergence extension — showing that weakly nonexpansive (rather than strictly contractive) residuals are sufficient for ball convergence — is a meaningful theoretical advance for the broader ADMM-PnP literature.

---

## Suggestions

1. Add a per-method NFE count to Table 1 (or a separate efficiency table).
2. In the discussion following Theorem 2, add a remark that δ_k = O(√d · σ^(k)), so the ball radius is a meaningful finite-k bound only when σ^(k) is small relative to 1/√d; at early iterations (large σ^(k)), the guarantee is a qualitative stability statement.
3. Specify the value of W (decay window) in the main text.
4. Elevate the discussion of Appendix E.2 (finite Langevin steps result) to a brief remark in Section 4, acknowledging the mixing gap and its effect on the practical bound.

---

## Score and Decision

**Anchor summary:**

| Path | Avg Score | Round | Comparison to reviewed paper |
|---|---|---|---|
| u1cQYxRI1H.md | 10.0 | R1 | Illumination diffusion model, not comparable |
| Uj0h13lVrR.md | 1.0 | R1 | Rejected GFlowNet paper, not comparable |
| dAavOuxZvo.md | 3.0 | R1 | VIPaint: diffusion inpainting, no theory, weaker contribution |
| rZzcaduYU1.md | 3.0 | R1 | Score-NP: weaker contribution, no inverse-problem convergence theory |
| Z9Odi09Rv9.md | 4.75 | R1 | Frequentist diffusion solver, rejected; similar scope but weaker theory |
| nHESwXvxWK.md | 4.0 | R1 | SMC + diffusion for linear inverse problems; similar scope |
| 7SFTZwNUQA.md | 5.20 | R1 | Patch-based diffusion for OOD inverse problems; no convergence theory |
| V2x5ZTHMae.md | 4.0 | R1 | DPS enhancement; weaker novelty |
| 66arKkGiFy.md | 5.75 | R1 | PnP-ULA with mismatch analysis; similar scope, less comprehensive experiments |
| 9mX0AZVEet.md | 6.0 | R1 | Optimal posterior covariance for diffusion; comparable scope |
| kRBQwlkFSP.md | 6.75 | R1 (read) | DiffStateGrad: manifold-alignment for inverse problems, no convergence theory — paper under review is stronger theoretically |
| h8GeqOxtd4.md | 6.25 | R1 | Score estimation convergence; orthogonal topic |
| 6EUtjXAvmj.md | 8.0 | R1 (read) | Variational midpoint guidance: comparable scope, thorough experiments, NFE reported — paper here is slightly weaker on NFE transparency |
| sbG8qhMjkZ.md | 8.0 | R1 | SVGD convergence; not directly comparable |
| 6O3Q6AFUTu.md | 8.0 | R1 | NoiseDiffusion interpolation; not comparable |
| fV0t65OBUu.md | 8.0 | R1 | Optimal covariance matching for diffusion; not directly comparable |

**Round 1 bracket:** 6.0–7.5.

**Narrowing:** The paper is above DiffStateGrad (6.75) due to the formal convergence theory contribution; it falls below the 8.0-band anchors primarily because of the missing NFE comparison (which the 8.0 "Midpoint Guidance" paper handles explicitly) and the dimension-scaling issue in the theoretical bounds. The contribution is solid, experiments are thorough, and the theory is a genuine advance — but two major weaknesses (both addressable) prevent a score above 7.0.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>