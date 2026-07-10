Now let me compile the final review with the scores properly weighted.

## Summary

This paper proposes AC-DC, a three-stage denoiser (auto-correction via additive Gaussian noise, directional correction via conditional Langevin dynamics, and score-based denoising) for integrating score-based (diffusion) denoisers into the ADMM plug-and-play framework for inverse problems. The paper provides convergence analysis under weak nonexpansiveness and bounded-denoiser frameworks, and demonstrates strong empirical results across six inverse problems on FFHQ and ImageNet.

## Strengths

- **Clear problem identification (Sec. 1–2).** The paper correctly identifies a genuine structural issue: score functions are trained on Gaussian-perturbed data manifolds, but ADMM iterates — especially with dual variables — do not naturally lie on these manifolds. The "manifold mismatch" framing is well-motivated with a specific explanation of why this is harder in a primal-dual (ADMM) setting than in a primal-only setting.

- **Non-trivial convergence analysis (Sec. 4).** Extending the ADMM-PnP fixed-point convergence framework (Ryu et al. 2019; Chan et al. 2016) to score-based denoisers requires handling stochasticity and the absence of a known proximal operator. The weak-nonexpansiveness analysis (Theorems 1, 2) and the bounded-denoiser + adaptive-step-size analysis (Theorem 3) represent genuine technical work that goes beyond what prior ADMM-PnP theory provides for learned denoisers.

- **Consistent empirical improvement across diverse tasks (Table 1).** On 6 inverse problems × 2 datasets, both variants (Ours-tweedie and Ours-ode) achieve best or second-best performance on nearly all metrics. Improvements over DPS, DiffPIR, DDRM, and RED-diff are often substantial (e.g., +2–4 dB PSNR on super-resolution and motion deblur). The qualitative results (Figs. 2–4) are visually consistent with the numbers.

## Weaknesses

### Fatal
None.

### Major

- **Theory-practice gap in noise schedules (Sec. 4.3 vs. Sec. 6).** Theorem 3(b) requires $\lim_{k\to\infty} \sigma^{(k)} = 0$ and $\lim_{k\to\infty} \sigma_{s^{(k)}} = 0$ as necessary conditions for convergence. However, the experimental schedule (line 297) sets $\sigma^{(k)} = \max(0.1, 10 - (10-0.1)k/W)$, so $\sigma^{(k)} \to 0.1$ (not zero), and $\sigma_{s^{(k)}} = 0.1/\sqrt{\sigma^{(k)}} \to 0.1/\sqrt{0.1} \approx 0.316$ (not zero). Theorem 2 further requires $\sigma_{s^{(k)}}^2 + (\sigma^{(k)})^2 < 1/M$ for an unknown data-dependent constant $M$ that is never estimated or verified. The convergence guarantees the paper advertises therefore do not apply to the algorithm that was empirically evaluated. The paper only indirectly acknowledges this in the Limitations (line 379) and does not reconcile the disconnect between the theory's conditions and the experimental setup. **This is the most significant weakness** — it means the theoretical contribution, while technically sound under its stated assumptions, is not matched to the actual algorithm that produced the empirical results.

- **Missing computational cost comparison (Sec. 6).** The method requires up to 1000 Adam iterations per outer ADMM iteration for subproblem (7a), plus $J=10$ score evaluations for DC Langevin steps and additional Tweedie/ODE denoising. No runtime, NFE count, or any compute-cost measure is reported alongside the quality metrics. Without this context, the reader cannot assess whether the quality gains reflect genuine algorithmic improvement or simply a larger computational budget.

### Minor

- **DC stationarity assumption in main theorems (Theorems 2, 3).** Both theorems explicitly assume the Langevin DC step reaches its stationary distribution for each iteration $k$ (lines 183, 205), yet only $J=10$ steps are used in practice. While a footnote (line 207) points to Appendix E.2 for relaxed versions, the main theoretical results presented rely on this strong assumption, creating a gap between what is proven and what is run.

- **Limited ablation of denoiser components (Sec. 6, Fig. 5).** The DC step ablation is only qualitative and only on the phase retrieval task. There is no quantitative ablation across multiple tasks isolating each stage's contribution. The AC stage in particular has no dedicated comparison (e.g., with vs. without the AC step while keeping other components fixed).

- **Inconsistent naming and missing task results.** (a) The baseline listed as "DAPS" in Table 1 appears as "DAPS-4K" in figure captions without explanation. (b) Task (g) "deblurring under nonlinear blurring" is described (line 293) but no quantitative results appear for it in the main paper.

### Trivial

- Minor table formatting issues: Some "PMC" rows in Table 1 appear duplicated or have empty cells (e.g., in the Gaussian Blur and Box Inpainting sections).

## Nice-to-Haves

- Verify whether experimental hyperparameters satisfy the theoretical conditions (e.g., estimate or bound $M$ for the datasets used).
- Either adjust the noise schedule to satisfy Theorem 3's conditions ($\sigma^{(k)} \to 0$, $\sigma_{s^{(k)}} \to 0$) or relax the theorem's conditions to match the actual schedule.
- Add quantitative ablation of both the AC and DC stages across multiple tasks.
- Report NFE and/or wall-time comparisons with baselines.

## Removed Points

These points were flagged in the input review but removed during consolidation with justifications:
- **DPIR listed as baseline but absent from results**: Results may be in the appendix (which is stripped by the parser). Per guidelines, criticisms about content that may reside in the appendix are removed.
- **Hyperparameter $W$ unspecified**: Per guidelines, undisclosed hyperparameters are treated as a reproducibility nitpick and removed.
- **Theoretical justification approximations for DC step (Eq. 10)**: The criticism was speculative about the validity of a Gaussian approximation without checking whether the stated condition ($\text{Var}(\mathbf{s}^{(k)})^{1/2} \ll \sigma^{(k)}$) holds; not a concrete verified flaw.
- **Various section-by-section speculative notes** (e.g., "could the metric be measuring a proxy?") removed as area-of-concern sweeps without concrete anchors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Align the convergence theory with the practical algorithm: either adjust the noise schedule to satisfy Theorem 3's conditions or relax the theorem to match the actual schedule. At minimum, explicitly state which theoretical conditions are violated by the experimental setup and discuss the implications.
- Report compute cost (NFEs and/or wall time) for the proposed method and each baseline to make the quality-vs-cost tradeoff interpretable.
- Add quantitative ablation of both the AC and DC stages across multiple tasks.
- Resolve the DAPS/DAPS-4K naming inconsistency and either provide results for the nonlinear deblurring task or remove it from the task description.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>