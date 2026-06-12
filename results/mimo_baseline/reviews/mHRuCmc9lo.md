## Summary

The paper develops a minimax robust decision-making framework for acting on predictions that satisfy partial (weaker-than-full) calibration guarantees, parameterized by a test class H. The authors characterize the optimal robust decision rule via duality and establish a central "sharp transition" result: once H contains the decision-calibration test class (one indicator per action), the minimax-optimal policy collapses to the plug-in best response, matching the trustworthiness semantics of full calibration under a far more tractable condition. They also derive robust policies for calibration conditions structurally induced by standard training pipelines and provide empirical validation on two datasets.

## Strengths

- **Sharp and novel characterization of decision calibration's role.** Theorem 4.1 establishes that decision calibration—not just a swap-regret guarantee—is sufficient for plug-in best response to be minimax optimal over all forecast-based policies. This is strictly stronger than the prior regret guarantees of Zhao et al. (2021) and Noarov et al. (2023), which only bound swap regret (ruling out improved *action-remapping* policies) but do not preclude better general policies. The collapse from the full minimax optimization (Eq. 5) to simple best response (Eq. 1) at the decision-calibration level is a crisp, surprising, and practically useful insight.

- **Elegant theoretical framework with practical implications.** The duality-based characterization (Theorem 3.1) yields pointwise computable robust actions via a finite-dimensional dual program. The "sharp transition" result (Theorems 4.1–4.2) provides a clear operational target: a forecaster satisfying decision calibration for multiple downstream tasks simultaneously enables plug-in optimality for all of them (Corollary 4.3). This has immediate practical relevance for ML systems serving heterogeneous decision-makers.

- **Structural results for free calibration from training pipelines.** Proposition 4.4 shows that models with linear heads trained to squared-loss stationarity automatically satisfy self-orthogonality calibration, and Proposition 4.5 derives closed-form robust policies for bin-wise calibration obtainable from standard post-hoc methods. These bridge the gap between the theory and existing practice without requiring new calibration algorithms.

- **Clear and well-organized exposition.** The paper is structured as a clean narrative: motivation → framework → general characterization → specialization to decision calibration → beyond → experiments. Figures 1 and 2 effectively communicate the interpolating property and the sharp transition. The theoretical statements are precise and well-interpreted.

- **Empirical validation confirms theoretical predictions.** The experiments (Table 1) demonstrate that the robust policy dominates the plug-in policy under adversarial evaluation (as predicted by minimax optimality), while incurring only a modest cost under nominal i.i.d. evaluation. The two-stage evaluation—nominal vs. worst-case—is methodologically sound and directly tests the paper's claims.

## Weaknesses

### Fatal

None.

### Major

- **Linearity assumption on utility.** Assumption 2.1 restricts the framework to utilities linear in the outcome. The authors acknowledge this, noting that risk-averse utilities depending on variance fall outside the framework. This is standard in the calibration literature and the authors provide reasonable justification (some nonlinear utilities can be linearized over a basis), but it is a genuine limitation that excludes many practically relevant decision settings (e.g., risk-sensitive finance, medical decisions with asymmetric costs). This weakens the generality of the claims somewhat.

- **Perfect calibration assumed in theory; only approximate in practice.** The main theorems assume exact H-calibration. In practice, models approximately satisfy these constraints. The sharp transition result for decision calibration (Theorem 4.1) could degrade qualitatively under even small calibration errors—the collapse to best response depends on exact cancellation in the proof. While Appendix B apparently discusses approximate calibration, the main body does not provide quantitative bounds on how the minimax optimality degrades with calibration error, which would be important for practitioners.

### Minor

- **Limited empirical scope.** The experiments involve only two regression datasets with very small action sets (3 actions each). While sufficient to validate the core theory, larger action sets and classification/regression settings with more realistic decision problems would strengthen the empirical contribution. The experiments also only test the self-orthogonality condition (H = {h(v) = v}), not decision calibration or bin-wise calibration.

- **No comparison to existing baselines.** The empirical evaluation compares only plug-in best response vs. the robust policy. Comparison to alternative approaches (e.g., direct uncertainty estimation, conformal prediction-based decision rules, or other robust optimization methods) would contextualize the practical value.

### Trivial

None.

## Nice-to-Haves

- A brief discussion or experiment demonstrating the behavior under approximate calibration, with quantitative characterization of utility loss as a function of calibration error ε.
- Extension or at least discussion of the framework for continuous or large action sets, where decision calibration's tractability advantage over full calibration is less clear.
- Empirical evaluation of the bin-wise calibration result (Proposition 4.5), which provides the most practically accessible version of the robust policy.

## Novel Insights

The paper's central novel insight is the identification of decision calibration as the precise threshold at which minimax robust decision making collapses to simple plug-in best response. This reveals that decision calibration—previously understood only through the weaker lens of swap-regret guarantees—is in fact sufficient for full minimax-optimal "trustworthiness" semantics. The practical upshot is significant: a decision-calibrated forecaster is simultaneously minimax-optimal for all downstream decision makers whose task-specific indicators it calibrates, without any of them needing to compute or deploy robust policies. This sharp transition, from the gradual interpolation one might naively expect, is a genuinely novel structural finding that connects the tractable calibration literature to the classical decision-theoretic foundations of calibration.

## Suggestions

- Provide a quantitative robustness-to-error analysis: for decision calibration with maximum calibration error ε, bound the gap between the robust policy's utility and the best-response utility. This would make the sharp transition result more robust to practical imperfections.
- Expand the experiments to include datasets with larger action sets (e.g., 10–50 actions) to test whether the computational and practical advantages hold in more realistic decision settings.
- Include comparison against baseline approaches such as conformal prediction intervals + conservative action selection, or direct posterior uncertainty estimation methods.

## Score and Decision

This is a strong theoretical contribution that establishes a clean, surprising, and practically relevant result. The connection between decision calibration and minimax optimality of plug-in best response goes meaningfully beyond prior work, which only established regret-based guarantees. The theoretical framework is elegant, the exposition is excellent, and the empirical validation—while limited—confirms the theoretical predictions. The main limitation (linearity of utility) is standard and well-acknowledged, and the gap between exact and approximate calibration analysis, while important, does not undermine the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>