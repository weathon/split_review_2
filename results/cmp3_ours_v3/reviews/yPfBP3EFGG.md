## Summary

This paper proposes STNAdam, a stochastic optimization algorithm for "nonconvex + weakly-convex" composite problems. The key idea is a two-track iteration framework that couples Nesterov momentum (extrapolation track) with Adam-style adaptive conditioning (update track). The stochastic gradient can use any variance-reduced estimator (SVRG, SAGA, SARAH). The paper provides convergence analysis under the Kurdyka-Łojasiewicz property and evaluates the method on low-light image enhancement (LIE).

## Strengths

1. **Two-track iteration framework is a genuinely novel algorithmic idea.** The design — maintaining two coupled trajectories (extrapolation via Nesterov momentum, regular update via Adam-style conditioning) — is clearly articulated in Section 2, Figure 1, and Algorithm 1, and is structurally distinct from single-track methods like NAdam or SNAdam.

2. **Convergence analysis is extensive and structurally sound.** The paper builds a complete argument (Lemmas 2–5, Theorems 1–2) under the KL framework, establishing expected decrease of a Lyapunov function, boundedness of subgradients, properties of accumulation points, finite-length property, and explicit convergence rates depending on the KL exponent. This is a nontrivial theoretical contribution given the interacting components (two tracks, adaptive step sizes, variance-reduced estimators, dynamically scheduled parameters).

3. **Framework is flexible with respect to the gradient estimator.** Lemma 1 defines general conditions (MSE bound, geometric decay, convergence of estimator) that any variance-reduced estimator can satisfy, and the main convergence results (Theorems 1–2) rely only on these conditions, covering SVRG, SAGA, SARAH, and SPIDER under a unified analysis.

## Weaknesses

### Fatal

None.

### Major

1. **No ablation study isolating the two-track mechanism.** The paper claims the two-track framework is the key innovation, but there is no experiment comparing STNAdam against a version of itself with the second track removed. The comparison is against *different algorithms* (SGD, Adam, SNAdam), not against ablated versions of STNAdam. This gap is particularly acute because STNAdam-SGD (two-track without variance reduction) only marginally outperforms SNAdam (17.14 → 18.06 PSNR in Table 2), while STNAdam-SARAH (two-track with variance reduction) shows a much larger gain (22.26). This pattern raises the question of whether variance reduction — a well-known technique independent of the paper's claimed innovation — is the primary driver of the reported improvements. Without an ablation, the paper's central algorithmic claim is untested.

2. **Single-task evaluation for a general-purpose optimizer claim.** The experiments evaluate STNAdam on exactly one task (low-light image enhancement) using one dataset (LOL). The paper positions STNAdam as a general optimization algorithm (title, Algorithm 1, Section 1.2 contributions (i)–(ii)), yet standard benchmarks for optimizer papers (CIFAR classification, ImageNet, language modeling) are absent. Even within the paper's stated scope of "nonconvex + weakly-convex" composite problems, additional instances (e.g., sparse regression with nonconvex regularizers, robust PCA) could have been tested. The empirical support for the claimed generality is insufficient.

3. **Citation inconsistency for SAdam.** In Section 4 (line 281), "SAdam" is cited as (Kingma & Ba, 2014) — the original Adam paper. However, the related work (Section 1) discusses SAdam as a distinct algorithm from Le-Duc et al. (2024) and Wang et al. (2019). This makes it unclear whether the baseline in Table 2 is actually Adam (Kingma & Ba) or SAdam (Le-Duc et al.), and the reader cannot properly assess the comparison.

### Minor

4. **No training curves or convergence dynamics shown anywhere in the main text.** For an optimizer paper, this is a significant omission — the reader cannot distinguish between "converges to a better solution" and "happens to produce better final metrics" without seeing the optimization trajectory.

5. **No statistical significance or variance reporting.** Table 2 and Table 3 report single point estimates with no indication of multiple runs, confidence intervals, or variance. With one run per method (as implied), the results could be sensitive to random initialization or data ordering.

6. **Theory–experiment disconnect.** The convergence analysis (Section 3) proves expected decrease of a Lyapunov function, bounds on subgradients, and convergence rates under the KL property. The experiments (Section 4) report final PSNR/SSIM/LPIPS values. There is no attempt to measure any quantity the theory predicts (e.g., gradient gap, finite-length property, convergence rate scaling), so neither validates the other.

7. **Parameter update intervals (6)–(8) depend on problem-dependent constants** (L, τ, V₁, V_T, ρ, s) that are typically unknown in practice. While Remark 3 provides some reassurance that lower bounds can be made positive, the practical computability of these intervals is not fully addressed, and the claim of "removing hand-tuning" is contingent on knowing or estimating these values.

### Trivial

8. SNAdam is cited as (Xie et al., 2024) in the experiments but attributed to (Reddi et al., 2019) in the related work. This citation inconsistency should be resolved.

9. The reported runtimes (2.64e-05 to 7.63e-05 seconds in Table 2) are unexplained in the main text — the unit and measurement setup should be clarified.

## Nice-to-Haves

- An ablation comparing STNAdam against single-track STNAdam with the same gradient estimator and parameter scheduling would directly test the core claim.
- Standard deep learning benchmarks (e.g., CIFAR-10/100 with ResNet, a transformer-based task) would substantially strengthen the empirical case.
- Showing training loss curves (or a proxy) would allow readers to evaluate convergence behavior directly.
- Comparison against variance-reduced versions of the baseline optimizers (e.g., SVRG-Adam, SARAH-Adam) would help disentangle the two-track benefit from the variance reduction benefit.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Missing related works (AdaBelief, AdamW, Adan)"** — Per policy, missing-related-works criticisms are not permitted without external verification.
- **"LIE-specific baselines are irrelevant to general-optimizer claim"** — The paper presents these as additional comparisons; they provide useful context for the LIE application and do not detract from the primary comparison against SGD/Adam/SNAdam.
- **"Experimental details deferred to appendix"** — Per policy, the appendix is stripped by the parser and exists in the original submission; this is not a valid criticism.
- **"Fatally narrow evaluation"** (harsh critic's framing) — Downgraded to Major. The theory contribution is substantial and independent of the experiments, and the paper does demonstrate one well-executed application. The evaluation is insufficient for acceptance but not fatal.
- **"Computational budget not fairly accounted"** — Speculative without appendix details; the reported runtimes are consistent with per-iteration timing on small-batch computations.
- **"SAdam may actually be Adam making comparison unfair"** — This is covered by the retained citation inconsistency weakness (Major #3) but reframed as a reporting error rather than a methodological fairness issue, since the numerical results may still be valid.

## Novel Insights

The two-track iteration idea is the most interesting aspect of this paper. The design — maintaining two coupled trajectories (extrapolation via Nesterov momentum and regular update via Adam-style adaptive conditioning) — is structurally novel relative to single-track methods like NAdam or SNAdam. What is less appreciated in the reviews is the theoretical framing: by using the KL framework (standard for deterministic proximal algorithms but less commonly applied to adaptive stochastic methods like Adam), the paper provides convergence guarantees that hold across a general class of variance-reduced estimators under unified conditions. The tension between these two contributions — an algorithmically novel framework that is practically motivated, and a theoretical analysis that is structurally rigorous but disconnected from the experiments — is the paper's defining characteristic. The paper genuinely advances algorithm design and theory for a specific problem class, but falls short on the validation side.

## Suggestions

1. **Add an ablation study**: compare STNAdam against a single-track version using the same gradient estimator and parameter scheduling (this directly tests whether the two-track mechanism itself drives improvement).
2. **Expand evaluation** to at least 2–3 additional tasks spanning different domains, including at least one standard deep learning benchmark (e.g., CIFAR-100 with ResNet).
3. **Resolve the SAdam/Adam citation inconsistency** in Section 4 — clarify which algorithm was actually used.
4. **Add training curves and multi-seed variance reporting** to the experimental results.
5. **Clarify the practical estimation procedure** for the constants required by parameter intervals (6)–(8), or explicitly acknowledge the limitation.
6. **Consider measuring a computable relaxation** of the Lyapunov energy function from the theory to help bridge the theory–experiment gap.

## Score and Decision

**Calibration anchors** (all paths relative to the calibration directory):
- `mEBSeSk49H.md` — avg 4.25 (Reject): Adam convergence theory with proof issues. Current paper has cleaner theory + novel algorithm → slightly stronger.
- `5nldnvvHfw.md` — avg 2.50 (Reject): AdamE with dynamic decay rates, insufficient novelty. Current paper is substantially more novel.
- `zCZnEXF3bN.md` — avg 6.00 (Accept): Double momentum SGD, accepted despite underbaked empirics but with standard benchmarks. Current paper has narrower experiments.
- `NKotdPUc3L.md` — avg 7.00 (Accept): Heavy-tailed noise theory, no experiments but significant theoretical results. Current paper has more empirics but less impactful theory.
- `YwJkv2YqBq.md` — avg 6.75 (Accept): Nesterov acceleration in non-convex landscapes, clean theory paper. Current paper has more algorithmic novelty but weaker presentation.
- `x45vUUY4nT.md` — avg 5.00 (Reject): SGDM bounds, pure theory, "underbaked" empirics. Current paper has a more complete package (algorithm + theory + some experiments).
- `tsNLIBlG4p.md` — avg 4.00 (Reject): Soft-clipping theory with limited experiments. Similar profile to current paper but less algorithmic novelty.
- `1eMbYu0841.md` — avg 3.67 (Reject): Gradient descent optimizer with auto-controlled learning rates. Weaker theory and less novelty than current paper.

**Round 1 bracket**: 3.5–5.5. The paper is clearly above the strong-reject band (1.0) and the simple Adam-variant band (2.5–3.25), but below the accepted papers (6.0+) whose empirical validation, even when limited, included standard benchmarks.

**Narrowing**: Compared to the 3.67–4.25 papers in the same band, the current paper has a genuinely novel algorithm and more complete theory. However, the empirical gap — no ablation, one task, one dataset — prevents placement in the accept band. The paper reads as a solid submission that is not yet ready for publication.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>