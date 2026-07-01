## Summary

This paper proposes Neural Predictor-Corrector (NPC), an RL framework that learns step-size and termination policies for homotopy/continuation solvers. It unifies four problem families (graduated non-convexity, Gaussian homotopy, homotopy continuation, and annealed Langevin dynamics) under a common predictor-corrector lens, then replaces hand-crafted heuristics with learned policies trained via PPO. Experiments across four domains—robust optimization, global optimization, polynomial root-finding, and sampling—show consistent reductions in corrector iterations (70–80%) while maintaining comparable solution quality, with cross-instance generalization.

## Strengths

- **Broad and genuinely diverse experimental scope.** NPC is evaluated across four substantially different problem families (GNC for robust optimization, Gaussian homotopy for global optimization, homotopy continuation for polynomial root-finding, annealed Langevin dynamics for sampling), each with multiple tasks/datasets. This breadth demonstrates that the core idea—learning predictor-corrector parameters via RL—generalizes beyond any single domain.

- **Large and consistent efficiency improvements.** Across nearly all tasks, NPC reduces iterations by 70–80% relative to the "Classic" version of each solver (e.g., ~70–80% fewer for GNC point cloud registration, ~80% fewer for HC, ~73–75% fewer for ALD) while maintaining comparable accuracy. These improvements are practically meaningful in magnitude.

- **Cross-instance generalization design.** Training on one dataset/problem class and testing on different ones (e.g., training on Aquarius, testing on bunny/cube/dragon for GNC; training on randomized Ackley, testing on fixed Himmelblau/Rastrigin for GH) provides a non-trivial test of generalization beyond in-distribution evaluation.

## Weaknesses

### Fatal

None.

### Major

- **No uncertainty quantification across all experiments.** Every result table reports averages over 50 trials with no standard deviations, confidence intervals, or other measures of variance (line 230: "All results represent the average over 50 independent trials"). For a paper making comparative claims ("outperforms," "superior"), the reader cannot assess whether observed differences (e.g., NPC's 0.05 vs. Classic GH's 0.07 on Ackley in Table 3; NPC's 11.91 vs. Classic ALD's 11.57 W₂ on 40-mode GMM in Table 5) are reliable or within noise. This is the single largest evidential gap and undermines the strength of the comparative claims.

### Minor

- **"Superior stability" claim is not supported by the presented evidence.** The abstract and conclusion claim "superior stability" (lines 9, 349), but the results consistently show NPC achieving accuracy **comparable** to the appropriate baselines, not superior:
  - GNC (Tables 1–2): log-error differences of ~0.01–0.12 vs. Classic GNC — comparable.
  - HC (Table 4): both methods achieve 100% success.
  - ALD (Table 5): W₂ and KSD values are comparable to Classic ALD.
  The claim should be softened to reflect what the data actually show.

- **The state representation is too impoverished to support the strong adaptivity framing.** The policy observes only four scalars: (t_{n-1}, ε_{n-1}, i_{n-1}, τ_{n-1}) — the homotopy level, previous tolerance, previous iteration count, and a scalar convergence velocity (Algorithm 1, line 146). The current solution estimate **x** and any geometric information about the trajectory (curvature, residual structure) are absent. The paper frames NPC as learning "adaptive strategies" that "adapt to varying solution trajectories" (lines 133–135), but with this state, the policy can at best learn a coarse schedule that depends on homotopy progress and a scalar summary of recent convergence speed. A non-RL learned schedule (Δt = φ(t)) might achieve similar results; this baseline is not tested.

- **The "unification" contribution is primarily expositional.** The paper's first claimed contribution (line 36) is unifying diverse problems under the homotopy paradigm. However, no single algorithmic framework is instantiated: NPC trains four domain-specific policies with different state definitions, action parameterizations, and reward functions. The observation that GNC, Gaussian smoothing, homotopy continuation, and annealed Langevin all use a homotopy interpolation is a useful pedagogical framing but is not a technical contribution — the paper itself cites prior works (Bates et al., 2013; Allgower & Georg, 2012) that have noted these relationships. The substantive contribution is the empirical demonstration that RL can improve PC solver efficiency; the paper would be stronger framed around this.

- **Algorithm 1 contains a suspect while-loop condition.** Line 149: `while H(x_{t_n}, t_n) ≤ ε_n and i_n ≤ t_n^{max} do`. A corrector loop should iterate while the residual is *above* tolerance (H > ε), not below. As written, the loop would either not execute (if H is already below tolerance) or would continue correcting after convergence. This appears to be an inversion of the intended condition.

- **Training cost is never reported.** The paper does not state the number of training episodes, environment steps, or wall-clock time required to train NPC for any of the four domains. This is a basic descriptor of any RL pipeline and is needed to assess the practical overhead of the approach.

- **Baseline comparisons have asymmetric treatment in some cases.** (a) CPL (Table 3): CPL's reported runtime includes per-instance training time (line 244), but NPC's training time is not reported, making the comparison asymmetric — the two methods use fundamentally different cost models (per-instance vs. amortized). (b) iDEM (Table 5): iDEM achieves substantially better W₂ values (7.42 vs. NPC's 11.91 on 40-mode GMM) but is excluded from runtime comparison due to different hardware. The presence of iDEM highlights a quality gap that is not discussed as a limitation.

### Trivial

None.

## Nice-to-Haves

- **Analyze what the learned policy actually does.** Visualizing learned step sizes and tolerances as a function of homotopy level across different instances would either substantiate the adaptivity claims or reveal the policy as a learned schedule. Either outcome would be informative.
- **Compare against a non-RL learned baseline** (e.g., a learned schedule Δt = φ(t) that is a function of homotopy level alone). If this simpler baseline achieves similar results, the benefit may come from learned schedules rather than adaptive decision-making. If it performs worse, it strengthens the case for RL.
- **Sensitivity analysis for λ₁, λ₂.** The accuracy-efficiency trade-off is determined by these coefficients, yet no sensitivity analysis is presented.

## Removed Points

These points were flagged during merging but removed per filtering rules (the removed details are retained here for traceability):

1. **"Missing appendix hyperparameter details"** — The critic noted that λ₁, λ₂, r_t^acc definition, and reward scaling are deferred to Appendix A. Removed per rule: the parser strips appendix sections from all papers; they exist in the original submission.
2. **"Policy network is extremely small"** — The critic noted the policy is a 2×16 MLP. Removed: this describes the architecture but does not constitute a weakness — a small network is appropriate for a 4-dimensional state.
3. **"SLGH_d and PGS are said to 'fail'"** — The critic noted these methods converge to inferior local minima rather than diverge. Removed: this is a semantic distinction about the word "fail"; it does not change the results.
4. **Pure formatting/style nitpicks** from the section-by-section notes were removed per rules.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's contributions (broad domain coverage, consistent efficiency gains) and surface evidential concerns (lack of variance reporting, claim overreach on stability) that the authors should address, but do not introduce novel perspectives not already evident in the paper.

## Suggestions

1. **Add standard deviations or confidence intervals** to all results tables. This is the highest-priority revision, directly affecting the credibility of comparative claims.
2. **Temper the "superior stability" claim** to "comparable stability" or "robust performance" to match the evidence.
3. **Report training cost** (episodes, steps, wall-clock time) for all four domains.
4. **Fix the while-loop condition** in Algorithm 1 (H > ε instead of H ≤ ε) or clarify the notation if a different convention is intended.
5. **Add an analysis section** showing the learned policy's behavior (step sizes, tolerances) as a function of homotopy level across different instances.

## Score and Decision

The paper has a legitimate and well-demonstrated contribution: learning PC solver parameters via RL yields consistent, large efficiency improvements across diverse homotopy problems. The breadth of evaluation is a genuine asset, and the cross-instance generalization design strengthens the findings. The main weaknesses (lack of variance reporting, claim overreach on stability, and some comparison asymmetries) are real but addressable and do not invalidate the core empirical finding. The paper meets the threshold for acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>