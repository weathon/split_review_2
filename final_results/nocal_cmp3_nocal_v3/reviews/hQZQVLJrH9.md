Here is the final consolidated review.

## Summary

This paper establishes a first-order mathematical equivalence between activation steering vectors and influence-function-based training-data re-weightings. It proposes Influence-Aligned Steering (IAS), a construction that bridges the two, along with a diagnostic γ (principal-angle cosine between Jacobian subspaces) that quantifies when steering can substitute for weight-space editing. The paper also provides a spectral optimality result for choosing steering directions and generalization bounds for low-rank interventions.

## Strengths

1. **Genuine theoretical unification.** The observation that activation steering and influence functions are first-order projections of the same underlying sensitivity structure is genuinely novel. The primal–dual framing (Section 3) provides a clean lens, and Theorem 4.2 (steering–influence equivalence) is a nontrivial theoretical contribution that connects two previously disconnected literatures.

2. **Principled diagnostic γ.** Using the smallest principal angle between the Jacobian subspaces Im(J_{θ→y}) and Im(J_{h→y}) to characterize when steering can substitute for weight-space editing (Theorem 5.1, Theorem 6.2) is elegant and practically useful. The empirical trend of γ increasing with layer depth (Figure 2) provides actionable guidance for practitioners. The diagnostic is cheap to compute (two Jacobian-vector products).

3. **Honest cost model and limitations.** The paper clearly states that all computations reduce to Jacobian-vector products and a rank-d pseudoinverse, and explicitly acknowledges that the theory is first-order and may break down for large perturbations (Conclusion). The computational cost analysis is straightforward and credible.

## Weaknesses

### Major

1. **Data-attribution claim is asserted without experimental validation.** The paper prominently claims (abstract, contribution (i), Corollary 1) that the framework yields a constructive algorithm for mapping steering vectors back to causal training examples and pinpointing "the *fewest* training examples to relabel/remove/examine." Line 130 explicitly says "see Section 7" for this, but **Section 7 contains no such experiment** — no table of top-weighted examples, no ablation showing that removing those examples mimics the steering effect, no validation of causal relevance. Similarly, the promised "practical workflow" (contribution (iv): "steer first, trace provenance, edit weights only when the geometry demands it," line 275) is never tested end-to-end. For a paper whose selling points include a unified workflow, the absence of evidence for these practically salient claims is a serious gap between what the paper promises and what it demonstrates.

2. **Unexplained slope anomaly in the central linearity experiment.** Figure 1 reports that predicted vs. actual logit shifts have a cosine of 0.978 but a **slope of 1.50** — meaning the actual logit shift is consistently 50% larger than the first-order prediction. The paper describes this as "consistent with the expected linear regime" (line 239), but a slope of 1.50 is not a trivial calibration issue. It indicates that second-order (or higher) effects are systematically nonzero even in the claimed small-edit regime. If the first-order theory were governing the behavior, the slope should be near 1.0 (up to noise). The paper does not discuss this discrepancy, does not attempt to explain it (e.g., as an artifact of the damping λ, the Gauss-Newton approximation, or the perturbation magnitude), and does not test whether the slope approaches 1.0 at smaller α. This weakens confidence in the empirical validity of the first-order approximation under the conditions tested.

3. **IAS underperforms the only baseline without discussion.** In the detoxification experiment (Table 1), IAS is *worse* than CAA on both metrics: higher toxicity (0.0164 vs. 0.0150) and higher perplexity (13701 vs. 13291). The paper presents the numbers without commentary. If IAS is meant to be a principled alternative, the fact that it is outperformed by a simple existing baseline on the only comparison task is a material issue that requires discussion. Moreover, there is no comparison against random steering directions, against other standard steering baselines (e.g., Turner et al. 2023's other methods), or against the actual data re-weighting that IAS is supposed to approximate.

### Minor

4. **Spectral optimality experiment is under-reported.** Figure 3 shows one ImageNet class (horse, class 339) on ResNet-50 with p=0.00498 and z=3.55, but the paper does not specify: (a) how many random directions were sampled, (b) how the p-value was computed (bootstrapped, parametric, permutation?), (c) whether this class was selected post-hoc or pre-registered. The experiment demonstrates the concept but lacks the methodological detail needed to assess its validity.

5. **Limited model scope.** Experiments only use GPT-2 Medium (354M parameters) and ResNet-50. The paper claims its tools "scale to billion-parameter models" (line 25) but does not validate this claim on any modern large language model (e.g., LLaMA-2-7B, Mistral-7B).

6. **Variance/confidence intervals missing.** Table 1 reports point estimates for toxicity and perplexity over 500 TOXIGEN prompts without any uncertainty quantification. Given the stochasticity in sampling, the reported differences (e.g., 0.0150 vs. 0.0164 for toxicity) may not be statistically significant.

### Trivial

7. **Equation (2) inconsistency.** Line 84 writes "Δh^* = J_{h→y}^⊤ J_{θ→y} Δθ" as the solution of the dual program. Substituting λ^* from the same line gives Δh^* = -J_{h→y}^⊤ (J_{h→y} J_{h→y}^⊤)^† J_{θ→y} Δθ, which differs from what is written. The pseudoinverse structure and the sign appear to be missing (may be a parser artifact).

## Nice-to-Haves

- Validating the data-attribution claim (contribution (i)) with an experiment: train a model with known spurious correlations, construct a steering vector that suppresses the spurious behavior, compute ρ_s, and show the top-weighted examples are indeed those containing the spurious correlation.
- Rerunning the linearity experiment at smaller α values to show that slope approaches 1.0 as α → 0, or diagnosing whether the slope reflects an artifact (damping λ, Gauss-Newton approximation).
- Expanding experiments to at least one modern LLM (e.g., LLaMA-2-7B or Mistral-7B) to support scalability claims.
- Specifying the steering magnitude α and damping λ used in each experiment.
- Reporting wall-clock time or iteration count for the spectral power iteration.

## Removed Points

- **"No code release or reproducibility details"** — Removed per hard rules on reproducibility nitpicks about undisclosed implementation details. Core hyperparameters (α, λ) are moved to Nice-to-Haves since they directly affect the validity of the first-order approximation.
- **"Corollary 1 proof sketch is circular"** — Removed because the paper labels it "Idea of the proof," suggesting a complete version may exist in the parser-stripped appendix.
- **"Theorem 6.1 essentially plugs Pinto et al.'s bound"** — This characterizes the contribution's scope rather than a concrete weakness, and the paper does not claim it as a primary result.
- **"Missing comparison against data re-weighting"** — Partially subsumed into Major Weakness 3 as a narrower point about missing baselines; the broader "should compare against full influence-based re-weighting" is scope creep since the paper's primary operational space is activation steering.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Either remove the unvalidated data-attribution and workflow claims (contributions (i) and (iv)) from the paper's headline contributions, or add experiments that support them.
2. Address the slope=1.50 anomaly directly: test at smaller α, discuss likely causes (damping λ, Gauss-Newton approximation, nonlinearity at the steering layer), or adjust the claims about the linear regime.
3. Add variance/confidence intervals to Table 1 and expand the baseline comparison to include random steering directions and at least one additional steering method.
4. Provide methodological details for the spectral experiment (number of random samples, p-value computation method).

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>