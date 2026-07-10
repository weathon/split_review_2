Now I have the favorability signals. Let me finalize the review.

---

## Summary

The paper proposes STNAdam, a stochastic optimization algorithm for "nonconvex + weakly-convex" composite problems that maintains two intertwined iteration trajectories (an extrapolation track and a regular update track) combining Nesterov momentum with Adam-style adaptive conditioning. The core contributions are (i) the two-track algorithmic framework, (ii) a convergence analysis under the Kurdyka-Łojasiewicz property that covers generic variance-reduced gradient estimators, and (iii) empirical results on low-light image enhancement showing strong metric improvements over baselines.

## Strengths

- **Rigorous theoretical convergence analysis under the KL framework (Lemmas 1–5, Theorems 1–2):** The paper provides convergence proofs covering almost-sure convergence, finite-length properties, and explicit rates depending on the KL exponent for the nonconvex + weakly-convex composite optimization setting. This is a nontrivial theoretical contribution for a complex algorithm with two coupled iteration sequences, adaptive learning rates, Nesterov momentum, and generic variance-reduced gradient estimators.

- **Flexible integration of variance-reduced estimators:** The method is designed generically so that any variance-reduced estimator (SGD, SAGA, SARAH, SVRG) can be plugged in, and the theory is developed for this general case rather than tied to a single estimator.

- **Strong empirical results on the LIE task:** STNAdam-SARAH achieves PSNR 22.26 vs. the next-best method STNAdam-SAGA at 21.05 and Retinex-Net at 18.44 on the LOL dataset — a substantial margin across PSNR, SSIM, and LPIPS. Visual results in Figure 2 show visibly sharper outputs.

## Weaknesses

### Fatal
None.

### Major

- **No ablation studies isolating the two-track mechanism** — the paper's core claimed innovation. There is no comparison of STNAdam against a single-track variant (e.g., standard NAdam with the same adaptive learning rates and the same estimator) that would allow attribution of gains to the two-track structure rather than to the Adam-style adaptive conditioning, variance reduction, or hyper-parameter choices. STNAdam-SGD does outperform plain SGD (18.06 vs 14.80), but the comparison conflates multiple differences (adaptive learning rates, momentum corrections, two-track structure) simultaneously.

- **Naming/citation inconsistencies for baseline methods impede reproducibility.** SAdam is attributed to Le-Duc et al. (2024) in the related work but cited as Kingma & Ba (2014) in the experiments — Kingma & Ba (2014) is the Adam paper, not SAdam. SNAdam is attributed to Reddi et al. (2019) in the related work but cited as Xie et al. (2024) in the experiments. The reader cannot determine what exact algorithms are being compared.

- **The 'automatic hyper-parameter scheduling' claim (Section 1.2: 'removing hand-tuning') is overstated.** The intervals for γ, λ, α (Equations 6–8) depend on problem-dependent constants L, τ, V₁, V₂, V_Τ, ρ, M, s, etc. The paper gives no guidance on how to set or estimate these constants in practice, and the experimental section does not report what values were used. Tuning has been shifted from the parameters to the constants that define their intervals.

- **The empirical evaluation is narrow for a paper framing a general-purpose optimizer:** only one task (low-light image enhancement) on one dataset (LOL). While the LIE task fits the problem formulation, the generality claim would be much better supported by even one additional diverse problem in the nonconvex + weakly-convex class.

### Minor

- **Baseline comparisons are not controlled for variance reduction:** STNAdam-SARAH and STNAdam-SAGA use variance-reduced estimators, while SGD, Adam, and SNAdam use plain stochastic gradients. The large performance gap could partly reflect variance reduction rather than the two-track framework. The paper does not include Adam+SARAH or Adam+SAGA as controlled baselines. Partially mitigated by the STNAdam-SGD vs. SGD comparison, which shows the two-track structure alone provides benefit even without variance reduction.

- **Runtime reporting is ambiguous:** all times in Tables 2 and 3 are on the order of 10⁻⁵ seconds. The column header "Time(s)" does not specify whether these are per-iteration or total training times, making the numbers uninterpretable.

- **Missing basic experimental reporting:** no indication of independent trials, random seeds, standard deviations/confidence intervals for any metric, hyper-parameter settings for baseline methods, or convergence curves (loss vs. iteration).

### Trivial
None.

## Nice-to-Haves

- Add an ablation comparing single-track NAdam (with the same adaptive learning rates and estimator) vs. the two-track STNAdam to directly isolate the two-track contribution.
- Clarify the role of the regular track x^{k+1} — the paper updates it but outputs only \tilde{x}^{k+1}, and never explains what x^{k+1} contributes to the overall algorithm behavior.
- Report how the interval-defining constants (L, τ, V₁, V₂, V_Τ, ρ) were set in the experiments, and provide a sensitivity analysis.
- Include convergence curves (loss vs. iteration) for the compared algorithms.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about missing appendix/proofs not being verifiable:** Removed per policy (the parser strips appendix sections from all submissions; the full proofs exist in the original submission).
- **Criticism that the related work "cites Adam, NAdam, and SNAdam being evaluated on such tasks":** Factually incorrect — the related work describes algorithms but does not evaluate them on any specific benchmarks.
- **Generic motivation/style nitpicks (e.g., "motivation language is generic", "conclusion is a single paragraph"):** Subjective and not substantive weaknesses to weigh in a decision.
- **Claim about "no comparison against SVRG":** Not a required comparison; the paper demonstrates SAGA and SARAH variants.
- **Requests for standard deep learning benchmarks as mandatory (CIFAR, ImageNet, language modeling):** The paper targets a specific composite optimization setting (nonconvex+weakly-convex), so an additional benchmark would strengthen it but its absence is not a flaw given the paper's stated scope. Re-framed in weaknesses to be more moderate.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Resolve the naming/citation inconsistency: clarify which algorithm corresponds to SAdam and SNAdam in the experiments.
- Specify whether the reported times are per-iteration or total and report wall-clock convergence curves.
- Report the number of independent trials and standard deviations for all metrics.
- Add at least one controlled comparison isolating the two-track mechanism (e.g., STNAdam-SGD vs. NAdam with SGD estimator).

## Score and Decision

The paper has a genuine theoretical contribution in its convergence analysis, and the LIE results are impressive. However, the core claimed innovation — the two-track mechanism — is not empirically isolated by any ablation study, making it impossible to attribute the observed gains to the two-track structure. The naming inconsistencies and overstated "automatic scheduling" claim further weaken reproducibility and credibility. The evaluation is limited to a single task for what is framed as a general optimizer. Major revisions (ablations, additional benchmark, naming fixes, transparent reporting) would be needed to make the paper's empirical case convincing.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>