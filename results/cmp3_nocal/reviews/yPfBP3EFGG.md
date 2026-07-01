## Summary

This paper proposes STNAdam, a stochastic optimization algorithm for "nonconvex + weakly-convex" composite optimization that combines a two-track iteration framework (extrapolation track + regular update track) with Nesterov momentum, Adam-style adaptive learning rates, and variance-reduced gradient estimators. Convergence theory is provided under the Kurdyka-Łojasiewicz property. Empirical results on low-light image enhancement are reported.

## Strengths

1. **Ambitious theoretical scope.** The paper provides almost-sure convergence analysis under the KL property for a complex algorithm integrating two-track coupling, Nesterov acceleration, adaptive learning rates, and multiple variance-reduced gradient estimators (SVRG, SAGA, SARAH). This is technically nontrivial.

2. **Strong empirical results on the reported task.** On the LOL dataset (Table 2), STNAdam-SARAH achieves substantially better PSNR (22.26), SSIM (0.906), and LPIPS (0.050) than the single-track baselines (best single-track SNAdam: 17.14 PSNR) and task-specific LIE methods (best: Retinex-Net at 18.44 PSNR). The joint denoising results in Table 3 similarly favor STNAdam-SARAH.

3. **Algorithmic generality.** The framework accepts arbitrary variance-reduced gradient estimators (SGD, SAGA, SARAH, SPIDER), and the convergence theory covers this general case.

## Weaknesses

### Fatal

None.

### Major

1. **Two-track design is neither ablated nor quantitatively motivated.** The paper's central claimed novelty—the two-track iteration framework—is described with the vague phrase "promote the formation of a larger update neighborhood, while exploring a better iteration direction continuously" (lines 9, 43, 91). No quantitative definition of "larger update neighborhood" is given, no controlled experiment isolates the two-track mechanism from other design choices, and no comparison is made against a single-track variant with identical gradient estimator and hyperparameters. Without such an ablation, it is impossible to determine whether the reported gains come from the two-track design, the variance-reduced estimator (the SARAH variant far outperforms the SGD variant: 22.26 vs 18.06 PSNR), or some interaction between them.

2. **Empirical evaluation is too narrow for an optimizer paper.** Evaluation is confined to one task (low-light image enhancement) and one dataset (LOL). An optimization algorithm is a general-purpose tool; demonstrating effectiveness on a single application does not constitute a convincing empirical case. Missing are: (a) standard optimization benchmarks (e.g., logistic regression, neural network training on vision or language tasks), (b) ablation studies isolating the two-track mechanism from the choice of variance-reduced estimator, and (c) sensitivity analysis of the random hyperparameter selection. The comparison against five LIE-customized methods (NPE, DeHz, LIME, Retinex-Net, LR3M) is supplementary but conflates model architecture with optimization; the relevant baselines for an optimizer are other optimizers on the same model (which are included—SGD, SAdam, SNAdam—but only on this one task).

3. **Citation inconsistencies for baselines.** The related work states that "Reddi et al. (2019) incorporated Nesterov-acceleration technique into Adam, named SNAdam" (line 33), but the experiments cite SNAdam as "Xie et al. (2024)" (line 281). The introduction defines SAdam as a specific variant by Wang et al. (2019) and Le-Duc et al. (2024) (line 13), but the experiments label the baseline as "SAdam (Kingma & Ba, 2014)" (line 281)—the original Adam paper. These inconsistencies raise questions about whether the baselines were correctly implemented and whether the comparison is valid.

4. **Runtime figures require clarification.** The reported times in Table 2 are on the order of 10⁻⁵ seconds for all eleven methods (e.g., SGD: 2.85e-05 s, STNAdam-SARAH: 2.64e-05 s, Retinex-Net: 7.63e-05 s). Microsecond-scale times for any optimization involving image-sized arrays are surprising. The paper must specify what exactly is being timed (per-iteration? per-patch? per-pixel? total optimization time?) and describe the experimental conditions (image resolution, hardware, number of iterations).

### Minor

5. **Hyper-parameter scheduling claim is overstated.** The paper claims hyper-parameters "can be dynamically scheduled within some iterate-dependent finite intervals, removing hand-tuning" (line 48). However, the intervals in (6)–(8) depend on theoretical constants (V₁, V_T, ρ, M, s, L, τ) that are not known in practice. Remark 3 implicitly acknowledges the limitation by noting the bounds simply "exceed 0 and do not approach 0," meaning the constraint is essentially vacuous for a practitioner.

6. **Convergence rates are standard for the KL framework.** Theorem 2 gives rates determined entirely by the KL exponent ϑ (linear if ϑ ∈ (0,1/2], sub-linear if ϑ ∈ (1/2,1)), which are standard for any algorithm analyzed via the KL framework (Attouch & Bolte, 2007; Bolte et al., 2014). The theory does not provide algorithm-specific insight into why the two-track design would converge faster or to better points.

7. **No variance or uncertainty reported.** Tables 2 and 3 report only point estimates without standard deviations or confidence intervals. Given the stochastic nature of the algorithm (random mini-batches, random parameter selection), the statistical significance of the reported improvements cannot be assessed.

8. **Three-way split between computed, analyzed, and output sequences is unexplained.** Algorithm 1 computes x^{k+1} (first track) and \bar{x}^{k+1} (extrapolation) and outputs \tilde{x}^{k+1} (second track). Theorem 1 analyzes \bar{x}^k, while Theorem 2 analyzes \tilde{x}^k. The first track x^k is an intermediate computation that is never directly evaluated. The paper does not justify why this particular design—as opposed to a simpler single-track alternative—is beneficial.

### Trivial

None.

## Nice-to-Haves

- An ablation applying the variance-reduced estimator (SARAH) to a single-track baseline (e.g., SNAdam with SARAH) would help disentangle the effect of the two-track mechanism from the gradient estimator.
- Broader evaluation on at least 2–3 standard optimization benchmarks would substantially strengthen the empirical case.
- Reporting results over multiple random seeds with standard deviations would allow assessment of statistical significance.

## Removed Points

- The input review's claim that the two-track design is "unmotivated" was retained but demoted from "fatal/structural" to "Major" because the algorithm IS specified (Algorithm 1) and a qualitative motivation IS stated—the gap is in quantitative motivation and ablation, not complete absence of motivation.
- The input review claimed the runtime issue "calls into question the reliability of the entire experimental setup." This severity was downgraded to "Major" because the times are consistent across all methods, suggesting they may measure a specific sub-component (per-iteration/per-patch); the issue is primarily a lack of clarity in reporting rather than evidence of fabrication.
- The input review's "Section-by-Section Notes" were subsumed into the relevant weaknesses where they identified concrete issues; observations that are purely descriptive (e.g., "notation in Table 1") were dropped.
- The input review's suggestion that the appendix being stripped makes the theory impossible to evaluate was removed per the rule that missing appendix content is a parser artifact, not an author error.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the paper's primary gap is evidential: the two-track design—the claimed innovation—is never isolated via controlled experiments, and the empirical evaluation is too narrow to support broad claims of superiority.

## Suggestions

1. Add a controlled experiment comparing STNAdam-SGD against a single-track variant with identical gradient estimator and hyperparameters (e.g., NAdam with SGD). If the two-track design provides benefit, this ablation should demonstrate it.
2. Resolve the citation inconsistencies: clarify whether the "SAdam" baseline is Kingma & Ba's Adam or the Le-Duc et al. variant, and whether SNAdam follows Reddi et al. (2019) or Xie et al. (2024).
3. Clarify what the "Time(s)" column measures and describe the experimental setup (image resolution, hardware, iteration count).
4. Expand empirical evaluation to include at least 1–2 standard optimization benchmarks.
5. Report results with standard deviations over multiple runs.
6. Tone down the "removing hand-tuning" claim or explain how the parameter intervals are set in practice without knowing the theoretical constants.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>