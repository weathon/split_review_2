## Summary

This paper studies how a decision-maker should act when given forecasts that satisfy only partial (ℋ-)calibration guarantees, rather than full calibration. The authors characterize the minimax-optimal robust policy via a duality argument (Theorem 3.1) and identify a sharp threshold: when ℋ contains the decision-calibration test class (size |𝒜|, independent of outcome dimension d), the robust policy collapses to simple plug-in best response (Theorems 4.1–4.2). For guarantees weaker than decision calibration — in particular, the self-orthogonality condition that arises naturally from squared-loss training (Proposition 4.4) — the robust policy remains efficiently computable. The paper is primarily a theoretical contribution, with illustrative experiments on two regression datasets.

## Strengths

1. **Sharp transition at decision calibration (Theorems 4.1–4.2) is a genuine and non-obvious theoretical result.** The insight that a test class of size |𝒜| (independent of outcome dimension d) suffices to recover the same decision-theoretic guarantee as full calibration is the paper's strongest contribution. The proof mechanism — invariance of the plug-in policy's expected utility under decision-calibration constraints — is clean.

2. **Duality-based characterization (Theorem 3.1) is elegant and practically useful.** Showing that the minimax-optimal policy reduces to best-responding to an adversarially tilted belief, computable via a finite-dimensional dual program, provides a concrete and pointwise-computable procedure. This synthesis of robust optimization and calibration is a genuine contribution.

3. **Honest and appropriately scoped framing.** The paper clearly distinguishes what it contributes (decision-making consequences of given calibration guarantees) from what it does not (new algorithms for achieving calibration). The abstract's statement that experiments evaluate "a natural one that applies to any regression model solved to optimize squared error" correctly signals what is being tested.

4. **Corollary 4.3 (simultaneous optimality across multiple decision problems) is a useful practical upshot.** The observation that a single decision-calibrated forecaster can serve multiple downstream decision-makers, each optimally best-responding in the minimax sense, is a genuinely useful design principle.

## Weaknesses

### Fatal
None.

### Major

1. **The adversarial distributions used in the experiments are not described, making the empirical evaluation non-reproducible.** Section 5 states that two types of adversarial evaluations are performed — "a worst case tailored to the plug-in policy" and "a worst case induced by the robust dual" — but never specifies the optimization problem, decision variables, constraints, or computational procedure used to construct them. The paper merely says they "respect the ℋ-calibration constraints" (lines 269–270). Without this information, the reader cannot assess whether the adversarial evaluations are meaningful or whether they constitute a fair test of the theory. Table 1's entire empirical comparison depends on this unspecified construction. *This is a significant reproducibility gap; the experimental section cannot be validated as written.*

### Minor

2. **The experiments test a secondary case (self-orthogonality, Section 4.2) rather than the headline theoretical result (decision calibration, Section 4.1).** The paper's core contribution is that decision calibration suffices for plug-in best-response optimality. The experiments use ℋ = {h(v) = v}, which falls short of decision calibration, so the robust policy does *not* collapse to plug-in. The paper is transparent about this (the abstract states the experiments evaluate the squared-loss case), but the disconnect means the experiments provide no direct empirical validation of the paper's central theoretical claim. A synthetic experiment where decision calibration is explicitly enforced would substantially strengthen the paper.

3. **No statistical uncertainty is reported.** Table 1 reports only point estimates (mean utility) with no standard deviations, confidence intervals, or significance tests. With test set sizes on the order of ~4,100 (California Housing) and ~730 (Bike Sharing), and relative differences as small as ~2% (0.410 vs. 0.402), single-point estimates could be influenced by noise. This is acceptable for illustrative theory-paper experiments but weakens the empirical claims.

4. **The gap between population-level theory and finite-sample practice is acknowledged but unquantified.** The paper correctly notes that the forecaster "approximately satisfies" ℋ-calibration (line 293) because Proposition 4.4 holds at a first-order stationary point of the *population* squared loss. However, there is no analysis of how finite-sample error in the self-orthogonality condition propagates to the robust policy's guarantees. Reporting the empirical correlation between f(X) and Y − f(X) on the calibration split would help assess how well the ℋ-calibration assumption actually holds.

5. **The efficiency claim for the dual formulation ("efficiently computable," line 53) depends on the dimension k of ℋ, but scaling is not discussed.** For the decision-calibration class k = |𝒜| (small), this is fine. For richer ℋ (e.g., approaching full calibration), k could be enormous, making the claim relative. A brief discussion of when the dual remains tractable would improve clarity.

### Trivial

None.

## Nice-to-Haves

- A synthetic experiment where decision calibration is explicitly enforced (e.g., via post-processing) to directly validate Theorems 4.1–4.2 empirically.
- A comparison with simple baselines such as the constant minimax strategy (a_minimax) or the bin-wise calibration policy with few bins, to calibrate how much the robust policy improves over pure conservatism.
- An experiment with at least one additional ℋ class on the same datasets to show how the robust policy changes as ℋ is enriched.
- A brief discussion of when the dual dimension k becomes too large for practical computation.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"The experiment design is too simple"* — This is a generic criticism that overlaps with more specific points already retained (no decision-calibration experiment, missing baselines, no error bars). The specific sub-criticisms are addressed in the weaknesses above.
- *"The paper does not discuss how the number of dual variables k scales"* — This was demoted from the original review's section notes to minor weakness 5 above.
- *"Missing related works"* — Removed per hard rules; related-work gaps cannot be authoritatively judged without external sources.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the sharp transition result (Theorems 4.1–4.2) and the duality characterization (Theorem 3.1) are the paper's main intellectual contributions, and that the weaknesses are concentrated in the experimental component rather than the theory.

## Suggestions

1. Provide a full, explicit description of how the adversarial test distributions are constructed: what optimization problem is solved, what variables are optimized, what constraints are imposed, and how the result is computed from the calibration split.
2. Add a synthetic experiment where decision calibration is explicitly enforced (e.g., by post-processing the forecaster to satisfy the decision-calibration moment conditions) and verify that the robust and plug-in policies coincide, directly validating Theorems 4.1–4.2.
3. Report standard deviations or confidence intervals for the experimental results, and quantify the empirical degree of self-orthogonality (e.g., the correlation between f(X) and Y − f(X) on the calibration split).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>