## Summary

This paper develops a minimax decision-making framework for acting on partially calibrated forecasts. It formalizes the ambiguity set of outcome distributions consistent with a given ℋ-calibration guarantee, characterizes the optimal robust policy via a duality argument (Theorem 3.1), and shows a striking result: when ℋ contains the decision-calibration indicators (only |𝒜| test functions), the robust policy collapses to simple plug-in best response—the same guarantee as full calibration, but with a tractable condition. The paper also derives robust policies for self-orthogonality (automatic from squared-error training) and bin-wise calibration, with illustrative experiments on regression datasets.

## Strengths

- **A clean formal bridge between ℋ-calibration and robust decision making.** The paper systematically treats optimal decision-making from partial calibration information using a minimax criterion. The framing in Section 2 (ambiguity set 𝒬, robust policy eq. 5, interpolating property) is clear and well-motivated, setting up the problem crisply.

- **The decision-calibration collapse result (Theorems 4.1–4.2) is crisp and significant.** The paper shows that decision calibration—a tractable condition with only |𝒜| test functions—recovers the same minimax optimality as full calibration. This upgrades the known swap-regret guarantee of decision calibration to full policy-class optimality, which is a genuinely stronger statement.

- **The self-orthogonality observation (Proposition 4.4) turns a standard training condition into usable structure.** Any model with a linear final layer trained to stationarity under squared loss automatically satisfies ℋ-calibration for ℋ = {h(v) = v}. This gives the framework an immediate practical audience at no additional algorithmic cost.

- **Closed-form characterization for bin-wise calibration (Proposition 4.5)** provides a simple post-hoc route to robust policies via piecewise-constant actions based on bin means, bridging theory to standard recalibration practices.

## Weaknesses

### Fatal
None.

### Major

- **The central theoretical result (decision calibration → plug-in minimax optimality) is not experimentally validated.** The paper's headline contribution is Theorems 4.1–4.2, yet the experiments in Section 5 test only a strictly weaker ℋ (self-orthogonality, ℋ = {h(v)=v}), which falls short of decision calibration and for which the robust policy differs from plug-in. The paper honestly scopes its experiments (Contribution 4: "evaluate both the best-response decision rule and the robust decision rule that results from the self-orthogonality condition"), but the most striking theoretical finding remains without any empirical support. An experiment where a forecaster is post-processed to be decision-calibrated and then evaluated against forecast-based adversaries would directly validate the core claim but is absent.

- **The adversarial evaluation construction is critically underspecified.** Section 5 describes two adversarial scenarios—a worst case tailored to the plug-in policy and one induced by the robust dual—but never explains how these distributions are actually constructed (e.g., by reweighting test points, resampling outcomes, or a parametric model). Whether the adversary is finite-sample or population-level, and whether test features are retained or transformed, is not stated. Without this information, the experimental results in Table 1 cannot be reproduced or properly interpreted as reflecting the claimed saddle-point property.

### Minor

- **No statistical uncertainty reported in Table 1.** The reported mean utilities lack standard errors, confidence intervals, or significance tests. The differences between plug-in and robust policies are small (≈0.01–0.02 on utility scales of 0.1–0.4), making it impossible to assess whether these reflect real performance gaps or noise from a single 60/20/20 split. This weakens the empirical claims.

- **The "sharp transition" framing exceeds what is formally proved.** Theorems 4.1–4.2 prove sufficiency (if ℋ contains decision-calibration indicators → plug-in optimal). They do not prove necessity (if ℋ does not → plug-in not optimal). The paper labels this a "sharp transition" (lines 143, 195, Figure 2), but without necessity it is a sufficient condition rather than a proven threshold. The claim is technically accurate as stated ("as soon as ℋ contains this class"), but the framing implies more than is established.

- **The exact-calibration assumption vs. practical approximation is acknowledged but not discussed in the main text.** The theory assumes exact ℋ-calibration (equations 2–3 with equality to 0). The paper mentions approximate calibration only in passing (line 85, deferred to Appendix B). Given that the experiments use an MLP that only "approximately satisfies" ℋ-calibration (line 293), the practical behavior of the framework under approximation error is unclear.

### Trivial
None.

## Nice-to-Haves

1. **Validate Theorems 4.1–4.2 experimentally.** Post-process a forecaster to be decision-calibrated (e.g., using Noarov et al. 2023) on a multi-class task and verify that plug-in best response achieves minimax optimality against forecast-based adversaries. This would directly test the paper's central claim.

2. **Spell out the adversarial construction** used in the experiments—whether it follows from the dual-optimal q* of Theorem 3.1 and how it is computed/applied.

3. **Add uncertainty quantification** to Table 1 (standard errors over multiple splits or bootstrap).

4. **Discuss the effect of approximate ℋ-calibration** in the main text: what happens when calibration holds only up to tolerance ε? Is the robust policy's advantage continuous in ε?

## Removed Points

- **Criticism that decision-calibration indicators don't form a linear subspace (Section 3):** The span of {1_{R_a} : a ∈ A} is a finite-dimensional vector space (dim ≤ |A|), so Theorem 3.1 applies straightforwardly. This criticism is factually incorrect.
- **Criticism about dual dimension:** The paper's claim of finite-dimensional concave maximization is correct; the dimension scales with k×d, which is a natural consequence, not a flaw.
- **Practical significance of collapse result (task-specificity):** The paper explicitly addresses this with Corollary 4.3 (simultaneous calibration) and calls decision calibration a "task-specific threshold" (line 197). The paper's scope excludes developing methods for achieving ℋ-calibration (line 103).
- **Demanding additional baselines:** The experiments test robust vs. plug-in for the self-orthogonality case, which directly tests the theoretical prediction for that setting. Additional baselines are beyond the paper's stated scope.
- **Formatting/style nitpicks, missing related works, and missing appendix content** are removed per policy.

## Novel Insights

None beyond the paper's own contributions. The reviews identify gaps in experimental validation and framing precision that the paper itself could address, rather than contributing novel analytical observations beyond what the paper already provides.

## Suggestions

The paper's theoretical contribution (the minimax framework and the decision-calibration collapse result) is strong and publishable. To strengthen the paper: (1) add uncertainty quantification to Table 1 and clarify the adversarial construction in the experiments; (2) either provide an experiment validating Theorems 4.1–4.2 or explicitly reframe the empirical section as solely supporting the self-orthogonality case; (3) soften the "sharp transition" language or add a necessity result.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>