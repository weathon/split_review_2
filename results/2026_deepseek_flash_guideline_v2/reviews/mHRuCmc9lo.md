Now let me finalize my review with my calibrated judgment.

## Summary

This theory paper proposes a minimax robust decision-making framework for acting on forecasts that satisfy partial (ℋ-)calibration guarantees, which are weaker and more tractable than full calibration. The authors characterize the minimax-optimal decision policy via a duality argument (Theorem 3.1), and identify a sharp transition: once ℋ contains the decision-calibration tests (indicator functions of each action's best-response region), the optimal policy collapses to simple plug-in best response (Theorems 4.1–4.2). They also show that standard squared-loss training yields a "free" self-orthogonality calibration condition (Proposition 4.4), and provide experiments validating the robust policy against the plug-in baseline on two regression datasets.

## Strengths

- **Sharp theoretical transition at decision calibration (Theorems 4.1–4.2)**: The paper proves that the minimax-optimal policy collapses to plug-in best response once ℋ contains the decision-calibration indicators—a crisp and non-obvious result showing that the substantially weaker and more tractable notion of decision calibration suffices for the "trustworthiness" semantics of full calibration in a minimax sense. This directly answers the paper's central question and provides a clear target for practitioners who can influence the forecaster's training pipeline.

- **Closed-form duality characterization with efficient computation (Theorem 3.1)**: Converts the infinite-dimensional minimax problem into a finite-dimensional concave dual over k×d Lagrange multipliers followed by a pointwise convex minimization over [0,1]^d. Both stages are solvable by standard methods (projected subgradient ascent), and the pointwise computability property—evaluating a_robust at a given forecast requires only two low-dimensional optimizations without constructing the full mapping—is a practical advantage over naive robust approaches.

- **Self-orthogonality from standard training (Proposition 4.4)**: Identifies that any model with a linear last layer trained to MSE stationarity automatically satisfies ℋ-calibration for ℋ={h_j(v)=e_j^T v}. This bridges theory to practice by showing the framework applies to many off-the-shelf regression models without any calibration-specific intervention—the experiments directly exploit this property.

- **Simultaneous plug-in optimality across multiple decision problems (Corollary 4.3)**: Shows a single forecaster can be decision-calibrated for a collection of downstream decision problems with different action sets and utility functions, and plug-in best response will be minimax-optimal for all of them. A practically useful insight for model providers.

## Weaknesses

### Major

- **Experimental results lack variance estimates and statistical rigor.** Table 1 reports only point estimates of mean utility with no standard deviations, confidence intervals, or mention of multiple runs or train/calibration/test splits. The differences between policies are on the order of 0.01–0.02 utility units (e.g., 0.166 vs 0.155 for California Housing under the plug-in-tailored adversary). Without any uncertainty quantification, these differences could lie within the noise of a single 60/20/20 split. For experiments that claim "the results match theory" (line 295), the absence of basic variance information substantially weakens the evidential value of the table.

- **The adversarial evaluation procedure is underspecified.** The paper describes two adversarial settings—"a worst case tailored to the plug-in policy" and "a worst case induced by the robust dual, tailored to the robust policy" (line 269)—but never explains how these distributions are actually constructed from the data. Since the experiments' purpose is to demonstrate the robust policy's advantage under ℋ-calibration-respecting worst-case distributions, the construction method is essential for interpretation and reproducibility. Without it, the reader cannot tell whether this is a principled saddle-point evaluation or an ad hoc perturbation, making Table 1 a black box.

### Minor

- **The paper's headline theoretical result (decision calibration collapse, Theorems 4.1–4.2) is not experimentally evaluated.** The experiments test the self-orthogonality condition (ℋ={h(v)=v}), which is strictly weaker than decision calibration. While the self-orthogonality case is a valid and interesting test of the framework, the paper's most striking conceptual finding—that plug-in best response is minimax-optimal under decision calibration—goes entirely untested. An experiment with a decision-calibrated forecaster (e.g., via the algorithm from Noarov et al. 2023) would have directly illustrated Theorem 4.1 and significantly strengthened the paper.

- **Finite-sample estimation of the dual variables λ* is not discussed.** The multipliers in Theorem 3.1 are defined in terms of population expectations, but in practice they must be estimated from finite calibration data. The paper notes (line 293) that it "use[s] the calibration data to substitute any population level expectation," but does not discuss how estimation error in λ* affects the robust policy's performance or its worst-case guarantees. Since the framework is motivated by distributional uncertainty, this additional layer of finite-sample uncertainty deserves at least a qualitative comment.

- **Limited experimental scope:** Only one ℋ class (self-orthogonality) and one model type (two-layer MLP with squared loss) are tested. The comparison is only between the robust policy and the plug-in rule; no fully conservative minimax baseline (constant safest action) is included to help calibrate how much the ℋ-calibration information is worth. The utility parameter choices (α=0.9, C(·) values) are presented without any sensitivity analysis; the paper claims "qualitative conclusions remain the same under other reasonable parameter choices" (line 291) but provides no evidence.

### Trivial

None.

## Nice-to-Haves

- Add diagnostics verifying that the self-orthogonality condition (Proposition 4.4) approximately holds on the calibration split (e.g., report the magnitude of E[f(X)·(Y−f(X))]).
- Include a fully conservative minimax baseline to help calibrate the value of ℋ-calibration information.
- Consider evaluating the decision-calibration collapse result directly with a decision-calibrated forecaster.

## Removed Points

These points are flagged to be removed; treat them with caution:

- Harsh critic's comment about inability to verify proofs due to the appendix being stripped by the parser: Removed per instructions (missing appendix content should not be flagged as a weakness, as it is present in the original submission).
- Harsh critic's comment about the ambiguity set Q being defined by population-level moments rather than finite-sample estimates: This is a restatement of the finite-sample issue already kept as a minor weakness, but the original framing was generic rather than specific to the paper's claims; the more specific version is retained above.
- Strength Finder's claim about "Empirical validation confirming saddle-point predictions (Table 1)": Downgraded from "strength" to the weakness category because the lack of error bars and underspecified adversarial construction prevent Table 1 from serving as strong validation; the directionality of the numbers is consistent with theory, but the evidence is too thin to be called a strength.
- Strength Finder's generic framing of the importance of the problem: Removed as a generic/superficial strength that lacks specific evidential content tied to the paper's execution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add standard deviations or confidence intervals to Table 1, computed over multiple train/calibration/test splits or bootstrap resamples. This is the single most impactful improvement for the experiments.
2. Explicitly describe how the two adversarial distributions are constructed from the calibration data and the dual variables—a few sentences would dramatically improve reproducibility.
3. Add a discussion (even brief) of how finite-sample estimation error in λ* affects the robust policy's guarantees.
4. Consider including at least one experiment with a decision-calibrated forecaster (e.g., via the algorithm from Noarov et al. 2023 or Zhao et al. 2021) to directly illustrate Theorem 4.1.
5. Add a fully conservative minimax baseline to help readers assess the value of ℋ-calibration information.

## Score and Decision

**Calibration Note**: The calibration database was unavailable due to missing files, so I rely on direct judgment calibrated against my knowledge of the ICLR standards. The paper makes a genuine theoretical contribution—the decision-calibration collapse result is non-obvious, the duality characterization is clean, and the self-orthogonality connection to standard training is practically relevant. The theory is sound and well-structured. The main weaknesses are in the experimental section: lack of error bars and underspecified adversarial construction weaken the evidential value of Table 1, but these are addressable and do not threaten the core theoretical claims. For a primarily theoretical paper, the experiments serve an illustrative role, and the theory is sufficiently strong to merit publication even with modest experiments. The paper is clearly above the rejection threshold (no fatal flaws) but the experimental shortcomings prevent it from being a strong accept.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>