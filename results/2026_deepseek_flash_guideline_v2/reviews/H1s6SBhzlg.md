## Summary

This paper addresses the problem of aggregating answers from multiple LLMs in unsupervised settings (no ground-truth labels available). It proposes two algorithms: Optimal Weight (OW), a weighted voting scheme proven to be Bayes-optimal when accuracies are known (Theorem 1), and Inverse Surprising Popularity (ISP), a novel adaptation of the surprisingly popular rule that leverages second-order information (cross-model answer correlations) and provably dominates majority voting in expectation (Theorem 2). Practical heuristics (OW-L, OW-I) that estimate first-order accuracies from second-order information are then evaluated on simulations, UltraFeedback, MMLU, and a healthcare dataset.

## Strengths

1. **Closed-form theoretical comparison of ISP, MV, and SP (Theorem 2, Section 4.2).** The paper derives exact, interpretable expressions for the expected advantage differences: E[Adv_ISP(s\*) − Adv_MV(s\*)] = Σ_i Σ_{j≠i} (Kx_i−1)(Kx_j−1)² / [(N−1)K(K−1)³]. This is a concrete result that directly ties the improvement to agent accuracies and the number of options K, and it is the paper's strongest theoretical contribution.

2. **Novel and well-motivated ISP algorithm.** The idea of "inverting" the SP score by conditioning on counterfactual answers (Eq. 4–5) is a clean adaptation with a clear intuition: amplifying prediction bias to recover the signal that SP misses in finite, heterogeneous LLM ensembles. The scaling analysis (ISP vs. MV ≍ Θ(1/K), MV vs. SP ≍ Θ(1)) is informative.

3. **Practical bridging from theory to deployment.** The paper devises two unsupervised methods (OW-L via ERM on second-order probabilities, OW-I via ISP pseudo-labels) to estimate the accuracies needed for the Bayes-optimal OW algorithm, enabling the theory to be used in realistic label-free settings.

4. **Diverse empirical validation.** Experiments span three distinct domains (LLM preference annotation with K=2, multiple-choice reasoning with K=4, healthcare dropout prediction with K=2) using 8 LLMs from 4 families. All proposed methods consistently outperform majority voting, and the per-question breakdown (Table 4) provides finer-grained evidence.

## Weaknesses

### Major

None. The core claims (ISP provably > MV, OW-based methods > MV in practice) are supported by theory and evidence. The most concerning empirical issue is fixable with explanation.

### Minor

1. **Unexplained identical OW-L and OW-I results (Tables 3, 4).** OW-L (ERM-based accuracy estimation) and OW-I (ISP pseudo-label-based accuracy estimation) produce identical accuracy on *all three* datasets (73.66%, 90.37%, 85.78%) and identical per-question comparison counts (2545/1727, 1821/659, 264/195). These are fundamentally different estimation strategies operating on the same data; their outputs matching exactly across all three datasets is highly unusual and unexplained. The paper should either (a) report more decimal places to show they are close but not equal, (b) explain the theoretical conditions under which they coincide, or (c) acknowledge and discuss the coincidence. This does not undermine the paper's core claim (OW methods beat MV), but it weakens the presentation of OW-L and OW-I as distinct contributions.

2. **σ_K inconsistency between abstract and technical section.** The abstract (line 25) defines σ_K(x) = x²/(K−1+x²), while Section 3 (line 73) defines σ_K(x) = e^x/(K−1+e^x). These are different functions with different inverses (√-based vs. log-odds). The technical section gives the mathematically correct definition (consistent with Bayes-optimality under conditional independence), so the abstract should be corrected to match. Minor presentation fix.

3. **No variance or uncertainty reported.** No standard deviations, confidence intervals, or standard errors are reported for any experiment. The t-statistics (12.53, 23.39, 3.22) are mentioned without degrees of freedom or specification of test type (paired? which specific comparison?). While large-scale benchmarks often report point estimates, the lack of any uncertainty quantification makes it hard to assess stability, especially for the more modest gain on ARMMAN (85.78% vs. 85.24%).

4. **Unclear whether second-order estimates are in-sample.** The paper does not clearly state whether the conditional probabilities P̂(A_i|A_j) used in ISP/OW-L are estimated from the same questions used to evaluate accuracy or from a held-out set. For the simulated data (M=10,000), Theorem 3's PAC bound mitigates this concern, but for real datasets a cross-validation or held-out procedure would strengthen confidence that gains are not an artifact of in-sample estimation.

5. **Narrow baseline comparison.** Only majority voting and the original surprisingly popular rule are compared. The paper cites confidence-weighted aggregation methods (Chen et al., 2023a; Fu et al., 2025) in the related work but does not include them as baselines. While these methods may require different settings (e.g., confidence scores from model internals), including at least one additional competitive baseline would better position the empirical results.

### Trivial

None.

## Nice-to-Haves

- **Quantify the theory–practice gap in simulation.** Since ground-truth accuracies are known in the simulated setting (Section 5.1), a direct comparison of OW-L/OW-I estimated weights vs. true optimal weights would cleanly answer "how much of the Bayesian-optimal performance is lost when accuracies must be estimated?"
- **Translate advantage bounds to accuracy bounds.** Theorem 2 compares expected advantage functions, but advantage is a proxy for accuracy. A bound relating advantage differences to accuracy differences would tighten the theoretical link.

## Removed Points

The following points from the reviewer inputs were identified as noise and removed with justification:

- **Position bias concern (Harsh Critic).** The paper explicitly acknowledges this assumption (line 51) and uses random-label shuffling as mitigation. The discussion is reasonable for the paper's scope; the concern is already addressed.
- **Theorem 1 novelty (Harsh Critic).** The observation that log-odds weighting is Bayes-optimal under conditional independence is a known principle, but the paper's packaging with σ_K, the BT model connection, and the LLM-specific setting is a legitimate reframing. This is a judgment call, not a concrete flaw.
- **"Identical OW-L/OW-I undermines the paper's core claim" (Harsh Critic).** This concern was downgraded from "fatal" to minor. The identical results are suspicious, but they do not invalidate the core claim (OW methods beat MV) — both OW-L and OW-I do outperform MV. The issue is about the distinction between OW-L and OW-I, not about whether they work.
- **Generic strength about "addressing an important problem" (Strength Finder).** Removed as not specific enough.
- **Strength about "Section 5.2 practical unsupervised accuracy estimation" — kept** as it is concrete.

## Novel Insights

None beyond the paper's own contributions. The review process did not surface a novel observation that the paper itself does not already make.

## Suggestions

1. **Explain the identical OW-L/OW-I results.** Report more decimal places, or explain the conditions under which the two estimation strategies coincide theoretically. If they genuinely give identical decisions on these datasets, state this and discuss why.
2. **Add uncertainty quantification.** Report confidence intervals (e.g., bootstrap) for all main accuracy numbers, and clarify the t-test procedure (degrees of freedom, test type, which comparison).
3. **Correct the σ_K definition in the abstract** to match the formal definition in Section 3.
4. **Clarify the estimation procedure for real-data experiments** — are second-order probabilities estimated from all data or held-out subsets? Consider a cross-validation approach.

## Score and Decision

Due to calibration database access issues, I was unable to retrieve anchored human reviews for direct comparison. Based on my own judgment calibrated against the ICLR scoring guidelines:

The paper makes a genuine theoretical contribution (ISP algorithm with closed-form advantage expressions, Theorem 2) and provides reasonable empirical evidence across diverse settings. However, the unexplained identical OW-L/OW-I results, the σ_K inconsistency, and the absence of uncertainty quantification prevent the paper from being fully convincing in its current form. These issues are fixable — none are structural — and the core theoretical contribution is solid.

**Score: 6 — Borderline Accept.** The paper has clear merit and the main claims are supported, but the empirical presentation needs cleanup. A revised version addressing the minor weaknesses (especially the OW-L/OW-I identity and the σ_K mismatch) would be suitable for acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>