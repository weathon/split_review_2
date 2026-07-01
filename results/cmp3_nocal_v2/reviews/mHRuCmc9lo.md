## Summary

This paper studies how a conservative decision-maker should act under partially calibrated forecasts. It characterizes the minimax-optimal decision rule via duality (Theorem 3.1) and shows a sharp transition: once the calibration class contains the decision-calibration indicators (size = |𝒜|), the robust policy collapses to plug-in best response (Theorems 4.1, 4.2). It also analyzes common intermediate cases (self-orthogonality from squared-loss training, bin-wise calibration) and provides experimental validation on two regression datasets.

## Strengths

1. **Sharp transition result (Theorems 4.1 and 4.2) is genuinely novel and non-obvious.** The finding that minimax-optimal decision-making collapses to plug-in best response precisely at the level of decision calibration—rather than at full calibration—is the paper's strongest contribution. The proof sketch (lines 189–193) is sound: decision calibration pins down the conditional expectation of Y on each decision region, and the best-response policy's utility depends only on these region-weighted moments, so the adversary cannot reduce its utility.

2. **The duality-based characterization (Theorem 3.1) provides a unified, principled framework** that yields a clean two-step procedure: solve a finite-dimensional concave dual for the multipliers λ*, then compute q*(v) via pointwise convex minimization. This elegantly unifies what could have been a case-by-case treatment.

3. **The paper is clearly scoped.** It explicitly states Assumption 2.1 (linear-in-v utility), acknowledges the finite-dimensional ℋ restriction, identifies risk-averse utilities as future work, and disclaims that its focus is on consequences of calibration rather than methods for achieving it (lines 103–104). This self-awareness is a legitimate strength.

4. **Corollary 4.3 (simultaneous optimality across multiple decision problems)** is a practically valuable observation: a single decision-calibrated forecaster supports plug-in optimality for many downstream tasks simultaneously.

## Weaknesses

### Fatal
None. The core theoretical contribution (Theorems 3.1, 4.1, 4.2) is logically sound, and no claim in the paper is invalidated by the weaknesses below.

### Major
None. The weaknesses are addressable and do not undermine the paper's central claims.

### Minor

1. **The experiments provide limited independent evidence beyond what the theory guarantees.** Table 1 reports mean utilities without confidence intervals or variance estimates, baselines are limited to plug-in vs. robust, and the differences are small (0.004–0.019 in absolute utility). The adversarial evaluations are synthetic constructions derived from the same dual optimization that defines the robust policy, so the finding that the robust policy dominates under its own adversary is essentially a consistency check of the saddle-point construction. For a theory paper this is not disqualifying—the experiments are supporting—but the paper would benefit from testing against *real* distribution shifts and reporting uncertainty.

2. **The paper does not address the practical cost of achieving decision calibration in specific settings.** The paper cites work on tractable algorithms (Zhao et al., 2021; Noarov et al., 2023) and scopes itself as focusing on consequences rather than methods (line 103–104). However, the practical significance of the sharp transition result depends on whether decision calibration can actually be guaranteed at acceptable cost in the high-dimensional settings where full calibration fails. A brief discussion of when this is realistic (e.g., sample size relative to |𝒜| and d) would strengthen the paper.

3. **The paper provides only two specific examples of intermediate ℋ (self-orthogonality, bin-wise calibration) rather than a general qualitative characterization of how the robust policy behaves as ℋ weakens.** While Theorem 3.1 gives a computational characterization for any finite ℋ, a practitioner whose forecaster has an unknown partial calibration profile has little guidance on whether the robust policy is worth computing. This is a natural direction for future work rather than a fatal flaw, but acknowledging the gap more explicitly would help readers.

### Trivial
None.

## Nice-to-Haves
- A concrete toy example (d=1, |𝒜|=2) showing the robust policy outperforming plug-in under a miscalibrated forecaster would clarify the practical motivation.
- Sample complexity bounds for achieving decision calibration would increase the paper's usefulness as a practical reference.
- Computational complexity analysis of the dual optimization would be useful for practitioners considering deployment.
- A discussion of whether simultaneous decision calibration for multiple tasks (Corollary 4.3) is harder than single-task calibration when decision regions cut the forecast space differently.

## Removed Points

These points were considered but removed with justification:

1. **"Experiments are better omitted than presented as evidence"** — Overly harsh framing. The experiments are valid as a sanity check of the theory, even if they do not provide strong independent evidence. The paper does not overclaim from them ("The results match theory").

2. **"The paper does not discuss what happens for ℋ strictly weaker than decision calibration but stronger than empty"** — Partially incorrect. The paper *does* discuss this in Section 4.2, which is specifically titled "Beyond Decision Calibration" and gives two detailed examples (self-orthogonality from squared-loss training; bin-wise calibration). The critic's valid remaining point—lack of a *general* qualitative characterization—is kept as Minor weakness #3 above.

3. **"No discussion of multiple decision-makers with conflicting decision regions"** — The paper explicitly addresses the multi-task case in Corollary 4.3. The practical difficulty the critic raises is reasonable but outside the paper's scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add confidence intervals to Table 1 (e.g., bootstrapped or across train/test splits) and include at least one non-synthetic distribution shift (e.g., temporal or covariate shift) to demonstrate that the robust policy helps under realistic conditions.

2. Add a brief paragraph in Section 6 (or a note in Section 4.1) giving rough guidance on when decision calibration is practically achievable: how many samples relative to |𝒜| and d, or reference to known bounds in the cited works.

3. Include a simple 1D toy example (d=1, |𝒜|=2) in Section 2 or an appendix to illustrate the gap between plug-in and robust policies under miscalibration.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>