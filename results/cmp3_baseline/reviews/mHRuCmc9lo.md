## Summary

This paper studies how a decision maker should act when given forecasts that satisfy only partial (H-calibration) guarantees, rather than full calibration. The authors formulate a minimax robust decision problem over distributions consistent with the calibration constraints, characterize the optimal policy via duality, and show a sharp transition: once the test class contains the decision-calibration indicators (a tractable condition), the optimal robust policy collapses to the simple plug-in best response. They also derive tractable robust policies for common training-induced conditions (e.g., self-orthogonality from squared loss) and provide empirical validation on two regression datasets.

## Strengths

- **Important and well-motivated problem.** The paper addresses a fundamental gap: full calibration is intractable in high dimensions, yet decision makers need principled ways to use partially calibrated forecasts. The framing is clear and practically relevant.
- **Novel theoretical characterization.** Theorem 3.1 provides a clean duality-based characterization of the minimax optimal decision rule for any finite-dimensional H-calibration class. This is a non-trivial result that connects robust optimization to calibration.
- **Sharp transition result (Theorems 4.1 and 4.2).** The finding that decision calibration (a weak, tractable condition) suffices to recover plug-in best response optimality is surprising and practically important. It identifies a crisp target for forecaster design.
- **Practical instantiation for common training pipelines.** Proposition 4.4 (self-orthogonality from squared loss) and Proposition 4.5 (bin-wise calibration) show how the framework applies to models trained with standard objectives, making the theory actionable.
- **Clear exposition.** The paper is well-structured, with intuitive figures (Figures 1 and 2) that help convey the interpolating property and sharp transition. The writing is precise and accessible.

## Weaknesses

### Fatal
None.

### Major
- **Empirical evaluation is too limited.** Only two regression datasets are used, with a single MLP model and synthetic adversarial distributions constructed from the dual. There is no comparison to baselines (e.g., standard calibration methods, other robust decision rules, or even the constant minimax strategy). The experiments demonstrate consistency with theory but do not convincingly show practical advantage over simpler alternatives.
- **Assumption of perfect H-calibration.** The main results assume the forecaster is exactly H-calibrated. In practice, calibration is approximate. The paper mentions approximate calibration only in an appendix and does not integrate it into the main analysis or experiments. The robustness of the framework to approximate guarantees is unclear.
- **Restrictive linear utility assumption.** The assumption that utility is linear in the outcome (Assumption 2.1) excludes risk-averse or other non-linear preferences. While common in the calibration literature, this limits the scope of the framework. The paper acknowledges this but does not discuss how to extend it.

### Minor
- **No verification of self-orthogonality in experiments.** The experiments rely on Proposition 4.4 to justify the H-class used, but the paper does not check whether the trained MLP actually satisfies the self-orthogonality condition (or how close it is). This weakens the connection between theory and empirical results.
- **Computational complexity not discussed.** The paper claims the robust policy is efficiently computable but does not analyze runtime or scalability for large H, high-dimensional outcomes, or many actions. This is relevant for practitioners.
- **Related work is somewhat brief.** The connections to distributionally robust optimization and robust control are mentioned but not deeply explored. A more thorough positioning would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- An experiment that compares the robust policy to a simple baseline like the constant minimax strategy or a policy that best-responds to a recalibrated forecast (e.g., via Platt scaling).
- A sensitivity analysis showing how the robust policy's performance degrades as the calibration guarantee becomes approximate (e.g., with increasing calibration error).
- A discussion of how to choose the bin partition in Proposition 4.5 in a data-driven way.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the decision-theoretic "trustworthiness" of calibration does not require full calibration; it only requires that the forecast passes a small set of task-specific tests (the decision-calibration indicators). This reframes the goal of calibration for decision making: instead of pursuing the statistically expensive goal of full calibration, one can target a much weaker condition that still guarantees that best-responding to the forecast is minimax optimal. This suggests a paradigm shift in how we think about calibration for downstream use.

## Suggestions

- Strengthen the empirical section by adding at least one more dataset (e.g., a multi-class classification task) and comparing against a baseline such as the constant minimax policy or a policy that uses a recalibrated forecast.
- Include a brief experiment that measures the actual H-calibration error of the trained MLP (e.g., the magnitude of the moment conditions) to validate the self-orthogonality assumption.
- Add a short discussion on how the framework extends to approximate calibration, perhaps with a bound on the suboptimality of the robust policy as a function of the calibration error.

## Score and Decision

The paper makes a solid theoretical contribution with clear practical implications. The main weaknesses are the limited empirical evaluation and the reliance on perfect calibration. However, the core results are novel, well-proven, and likely to influence future work on calibration for decision making. I recommend acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>