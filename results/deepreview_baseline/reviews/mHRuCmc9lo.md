## Summary

This paper studies how a decision maker should act when given forecasts that satisfy only partial (H-calibration) guarantees, rather than full calibration. The authors formulate a minimax robust decision problem over distributions consistent with the calibration constraints, characterize the optimal policy via duality, and show a sharp transition: once the test class includes the decision-calibration indicators (a tractable condition), the optimal robust policy collapses to the simple plug-in best response. They also derive tractable robust policies for common pipeline-induced guarantees (e.g., self-orthogonality from squared-loss training) and provide empirical validation on two regression datasets.

## Strengths

- **Novel and well-motivated framework.** The paper formalizes a natural question—how to act on partially calibrated forecasts—that bridges calibration theory and robust decision making. The minimax perspective is principled and yields actionable policies.
- **Sharp theoretical result.** The collapse to plug-in best response under decision calibration (Theorem 4.1) is surprising and practically important. It identifies a tractable target for forecaster design that recovers the full-calibration decision-theoretic guarantee.
- **Efficient characterization.** Theorem 3.1 provides a closed-form dual characterization for finite-dimensional H, making the robust policy computable via standard convex optimization. The pointwise structure is elegant.
- **Clear exposition.** The paper is well-structured, with intuitive figures, precise problem statements, and a logical flow from general theory to specific instantiations. The assumptions are stated explicitly.

## Weaknesses

### Major

- **Limited empirical evaluation.** The experiments are confined to two regression datasets with small action sets (3 actions each). The evaluation only tests one specific H (self-orthogonality from squared loss). More extensive experiments—including synthetic data to directly validate the theory, larger action spaces, multiclass settings, and comparisons with alternative baselines—would strengthen the empirical claims.
- **Restrictive linear utility assumption (Assumption 2.1).** Many decision problems involve risk aversion, variance-sensitive utilities, or other nonlinearities. The paper acknowledges this as a limitation but does not explore how far the results extend (e.g., via basis expansion). This limits the practical scope.

### Minor

- **Perfect calibration assumption.** The main results assume exact H-calibration. While Appendix B discusses approximate calibration, the core theory relies on exact moment equalities. In practice, calibration guarantees are approximate; the robustness of the results to approximation error is not fully explored.
- **Finite-dimensional H assumption for Theorem 3.1.** The characterization requires H to be a finite-dimensional linear space. While this covers many cases of interest (decision calibration, bin-wise calibration, linear functions), the paper could discuss extensions to infinite-dimensional H (e.g., via kernel methods) or note that the finite case is already rich enough for the main insights.
- **Computational details for general H.** The paper states that the dual can be solved efficiently but does not provide concrete algorithms, complexity analysis, or guidance on choosing the number of test functions k. For practitioners, more implementation details would be helpful.

### Trivial

- The experiments use a two-layer MLP; the self-orthogonality property holds exactly only at a global optimum of squared loss. The paper could briefly discuss the effect of approximate stationarity on the calibration guarantee.

## Nice-to-Haves

- Extend the framework to non-linear utilities via basis expansion (as mentioned in the conclusion) and provide conditions under which the collapse result still holds.
- Provide a detailed algorithm (e.g., pseudocode) for computing the robust policy for a general finite H, including how to solve the dual and the pointwise minimization.
- Discuss how to obtain decision calibration in practice more concretely, referencing existing algorithms and their sample complexity.

## Novel Insights

The paper’s central insight is that the decision-theoretic “trustworthiness” of full calibration can be recovered by a much weaker and more tractable condition—decision calibration—when viewed through a minimax lens. This is not obvious a priori: one might expect a gradual improvement as H is enriched, but the paper shows a sharp transition. This reframes the goal for trustworthy ML: rather than pursuing full calibration (which is intractable in high dimensions), one can target decision calibration for the specific downstream decision problem and still guarantee that best-responding to the forecasts is minimax optimal. The duality-based characterization also provides a unified way to derive robust policies for any finite H, revealing that the optimal policy is always a best response to an adversarially tilted belief.

## Suggestions

1. Expand the experimental section to include synthetic data with known ground-truth distributions, allowing direct verification of the minimax optimality and the collapse phenomenon. Include comparisons with baselines such as the constant minimax policy and the plug-in policy under distribution shift.
2. Add a discussion of the computational complexity of solving the dual for general H (e.g., number of iterations, dependence on k and d). Provide pseudocode or a reference implementation.
3. Clarify the relationship between the minimax optimality guarantee and existing swap regret guarantees for decision calibration. The paper states that minimax optimality is stronger; a brief technical comparison would be illuminating.

## Score and Decision

**Score:** 8  
**Decision:** Accept

The paper makes a significant theoretical contribution to the intersection of calibration and decision making. The results are novel, well-supported, and clearly communicated. The limitations (linear utility, limited experiments) are acknowledged and do not undermine the core contribution. The paper will be of high value to the ICLR community, particularly researchers working on trustworthy ML, calibration, and decision-focused learning.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>