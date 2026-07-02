## Summary

This paper proposes STNAdam, a stochastic optimizer for "nonconvex + weakly-convex" composite optimization that maintains two intertwined iteration trajectories — an extrapolation track via Nesterov momentum and a regular update track via Adam-style adaptive conditioning. The stochastic gradient can be supplied by any variance-reduced estimator (SVRG, SAGA, SARAH, SPIDER). Under the Kurdyka–Łojasiewicz property, the authors establish almost-sure convergence to a stationary point with explicit rates, and parameters are scheduled within iterate-dependent intervals derived from the analysis. Experiments on low-light image enhancement (LOL dataset) are presented.

## Strengths

- **Novel two-track algorithmic architecture (Algorithm 1, Section 2).** The core idea — maintaining two coupled iteration trajectories where an extrapolation track promotes a larger update neighborhood while the regular track refines the direction — is a genuine structural extension beyond single-track methods like NAdam and SNAdam. The coupling mechanism is clearly motivated and non-trivial.

- **Generality of the theoretical framework (Lemma 1, Section 3).** The convergence analysis accommodates arbitrary variance-reduced gradient estimators (SVRG, SAGA, SARAH, SPIDER) under a unified set of conditions. This is a meaningful theoretical contribution, as most existing convergence results for Adam variants assume a specific gradient estimator (typically SGD). The analysis also covers the "nonconvex + weakly-convex" composite setting, which is strictly more general than the "nonconvex + convex" setting handled by prior work.

- **Explicit convergence rates (Theorem 2).** The rates distinguish between the KL exponent cases (\(\vartheta \in (0,1/2]\) yielding linear convergence, \(\vartheta \in (1/2,1)\) yielding sublinear), which is well-executed standard KL-based analysis.

## Weaknesses

### Fatal
None.

### Major

- **Empirical evaluation is critically insufficient to support the claimed practical superiority.** The paper lists "favorable practical performance" as one of its three main contributions (Section 1.2, item iii), yet evaluates on a single task (low-light image enhancement) on a single dataset (LOL). There are **no convergence curves** (loss vs. iterations or wall-clock time), **no variance reporting** (all results in Tables 2 and 3 are point estimates with no standard deviations, confidence intervals, or number of random seeds), and **no ablation studies** isolating the contributions of the two-track framework, bias-corrected Nesterov momentum, adaptive parameter scheduling, and variance-reduced gradient estimators. For a stochastic optimization algorithm, the absence of any statistical reporting is a serious omission — the observed improvements could plausibly be within run-to-run noise. Additionally, hyperparameters for baselines (SGD, Adam, SNAdam learning rates, momentum, schedules, batch sizes) are not disclosed in the main text, making it impossible to assess whether baselines were reasonably tuned.

- **Confounded comparison: two-track framework vs. variance reduction.** STNAdam-SAGA and STNAdam-SARAH use variance-reduced gradient estimators (SAGA, SARAH), while the baselines SGD, SAdam, and SNAdam all use the standard SGD estimator. Thus, comparing STNAdam-SAGA against SNAdam conflates two differences: the two-track framework *and* the gradient estimator. The only clean comparison is STNAdam-SGD vs. SNAdam (both SGD-based), where the margin is modest (18.06 vs. 17.14 PSNR) with no variance reported. This undermines attributing gains to the two-track architecture specifically.

- **Citation inconsistency for the SNAdam baseline.** The Related Work (line 33) states: "Reddi et al. (2019) incorporated Nesterov-acceleration technique into Adam, named SNAdam." However, the contributions list (line 50) and experiments section (line 281) cite SNAdam as "Xie et al. (2024)." This internal inconsistency makes it impossible to determine which algorithm was actually used as a baseline, undermining the experimental comparison's validity.

### Minor

- **Comparison with LIE-specific algorithms is ambiguous.** Table 2 compares STNAdam variants against NPE, DeHz, LIME, Retinex-Net, and LR3M — specialized algorithms for low-light image enhancement. The paper does not clarify whether these methods solve the same optimization model (14) as STNAdam or use their own formulations. If they solve different models, the comparison reflects model quality rather than optimizer quality and is irrelevant to the optimizer claim. The paper's main empirical claim does not depend solely on these comparisons, but the presentation conflates two different evaluation dimensions.

- **"Removing hand-tuning" claim is misleading (Section 2, Equations 6–8).** The parameter update intervals depend on global quantities (\(L\), \(\tau\), \(V_1, V_2, V_\Upsilon, \rho\)) that are unknown for practical problems. Remark 3 further admits that moduli "must be appropriately increased if necessary," which makes the scheduling conditional on manual adjustment of these constants — replacing hand-tuning of learning rates with hand-estimation of different constants, which is at least as difficult.

- **No discussion of limitations.** The paper does not discuss when STNAdam might fail or when simpler methods would be preferable — e.g., the overhead of maintaining two trajectories, sensitivity to the intervals in (6)–(8), or how the extra hyper-parameters compare to standard Adam in practice.

### Trivial
- **Time column units unclear (Table 2).** Reported values (2.64e-05 to 7.63e-05 seconds) are consistent with per-iteration times, but this is not explicitly stated. Total wall-clock convergence time would be more informative.

## Nice-to-Haves

- Test STNAdam on at least one additional optimization task from a different domain (e.g., image classification with a CNN, or training a small transformer) to demonstrate general-purpose utility rather than fit to a single LIE model.
- Include ablation studies isolating each component (two-track framework, bias correction, adaptive parameter scheduling, variance-reduced estimators).
- Report convergence curves (objective value vs. iteration and vs. wall-clock time) with confidence intervals over multiple seeds.
- Add controlled baselines: compare STNAdam-SGD against a "single-track SNAdam-SGD" that uses the same gradient estimator but without the two-track structure, to isolate the two-track contribution.

## Removed Points

These points were raised in the input review but are not included as weaknesses in the final review:

- **"Convergence results conditional on KL property"** — The reviewer correctly notes this is standard in nonconvex optimization theory and not a flaw per se. Removed as not a genuine weakness.
- **"Energy function complexity and deferred coefficients"** — The coefficients \(A_1\)–\(A_8\) are deferred to the appendix (Lemma A.1), which the parser strips from all papers. Criticizing content that exists in the original submission but was removed by the extraction tool is not valid. Removed.
- **"No standard deep learning benchmarks (CIFAR, ImageNet)"** — This is subsumed by the more specific evaluation weakness above; the core problem is insufficient evidence for the claimed contribution, not the absence of any particular benchmark.

## Novel Insights

None beyond the paper's own contributions. The key synthesis from the reviews is that the algorithmic novelty and theoretical analysis are independently interesting, but the experimental evaluation does not meet the standard required to substantiate the claimed empirical superiority.

## Suggestions

1. Resolve the SNAdam citation inconsistency to make clear which baseline was used, or better, implement and compare against *both* Reddi et al. (2019) and Xie et al. (2024) versions to cover both possibilities.
2. Add at least one controlled comparison that isolates the two-track framework from the choice of gradient estimator (e.g., SNAdam with SAGA/SARAH estimators vs. STNAdam with the same estimators).
3. Report results with standard deviations over multiple random seeds, or at minimum state the number of runs performed.
4. Clarify in the main text what optimization problem the LIE-specific algorithms (NPE, DeHz, LIME, etc.) actually solve, and whether the comparison is between optimizers, models, or both.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>