Now I have all the information needed to produce the final consolidated review. Let me verify one more detail about the abstract's σ_K definition.

The abstract (line 25) states σ_K(x) = x²/(K-1+x²), while Section 3 (line 73) defines σ_K(x) = e^x/(K-1+e^x). These are indeed different functions. The reviewer caught this correctly.

Now let me write the final review.

---

## Summary

This paper studies how to aggregate answers from multiple LLMs by moving beyond simple majority voting. It proposes two principled algorithms: **Optimal Weight (OW)**, which is proven to be Bayesian-optimal when each LLM's accuracy is known (Theorem 1), and **Inverse Surprising Popularity (ISP)**, which uses second-order information (pairwise answer correlations) and is shown to have higher expected advantage than majority voting (Theorem 2). The paper provides simulation validation, evaluations on UltraFeedback and MMLU, and a real-world healthcare deployment (ARMMAN). The theoretical framework is clean and Theorem 1 is a genuine contribution to the theory of LLM aggregation.

## Strengths

- **Clean theoretical framework with a clear optimality result.** Theorem 1 proves that OW (with weights inverse-logistic in accuracy) is Bayesian-optimal among all possible aggregators under the stated model. This pins down exactly what weighting scheme is optimal given knowledge of accuracies. The connection to the Bradley-Terry model (Corollary 1) provides relevance to the RLHF community.

- **Non-obvious insight about SP vs. MV in LLM settings.** The paper clearly identifies and explains why the Surprisingly Popular rule underperforms majority voting in LLM settings (Section 4.1), precisely because LLMs lack the systematic biases that make SP work in human crowds. This is a conceptually interesting and well-supported finding.

- **ISP is a well-motivated algorithmic adaptation.** The counterfactual construction in ISP (using the probability of agent i's answer conditional on other agents reporting different answers than they did) is a principled way to amplify the signal that SP was designed to capture, in a setting where the signal is weak. The closed-form expressions for expected advantage differences in Theorem 2 are explicit and useful.

- **Real-world healthcare deployment on ARMMAN.** The evaluation on a real maternal health dataset (ARMMAN) demonstrates the method works outside standard NLP benchmarks and addresses a meaningful practical problem.

## Weaknesses

### Fatal
None.

### Major

- **Missing relevant baselines.** The paper cites Chen et al. (2023a) and Fu et al. (2025) showing that confidence-weighted aggregation improves LLM accuracy, yet does not compare against confidence-weighted voting or log-probability averaging as baselines. Without these, the reader cannot determine whether ISP/OW-L/OW-I's gains (0.5–1.5% absolute on real data) are specific to the proposed mechanisms or achievable with simpler weighting schemes. This weakens the empirical contribution substantially.

### Minor

- **Gap between Theorem 2 and accuracy claims.** Theorem 2 proves that E[Adv_ISP(s*)] ≥ E[Adv_MV(s*)] — i.e., ISP has higher _expected advantage_ for the true label. The paper argues this implies ISP outperforms MV at aggregation (lines 205–206). However, a higher expected advantage for the true label does not directly imply a higher probability that the true label maximizes the advantage function (which determines accuracy). The empirical results in Table 2 do support the accuracy claim, but the theoretical link between the theorem and the accuracy claims is not fully bridged.

- **Modest empirical gains on real datasets.** Absolute improvements over MV are 0.54–1.45% on real data. On MMLU, the Single Best oracle (91.02%) outperforms all aggregation methods (90.37%). While improvements are consistent and statistically significant across 16 model ensembles, practical significance is modest.

- **Heuristic nature of best-performing real-data methods.** The best real-world results come from OW-L and OW-I, which estimate accuracies from second-order information heuristically. The paper acknowledges this (Section 5.2), but the theoretical guarantees from Theorem 1 (OW) do not transfer to these variants. The theory and the best practical performance are partially decoupled.

- **No error analysis or failure case study.** For a method with 0.5–1.5% improvement, understanding _when_ it helps versus hurts would strengthen the paper considerably. Table 4 hints at this (e.g., OW-L gets 2,545 right where MV was wrong but gets 1,727 wrong where MV was right on UltraFeedback), but there is no qualitative analysis of these cases.

### Trivial

- **Inconsistent σ_K definition between abstract and Section 3.** The abstract (line 25) defines σ_K(x) = x²/(K-1+x²), while Section 3 (line 73) defines σ_K(x) = e^x/(K-1+e^x). These are different functions; the abstract formula appears to be a typo and does not match what the algorithm actually uses.

## Nice-to-Haves

- Adding confidence-weighted voting and log-probability averaging as baselines would be the single highest-leverage empirical addition.
- Reporting variance across the 16 model ensembles would provide a clearer picture of robustness.
- A brief discussion of ISP's computational complexity (O(N²K²) pairwise conditional tables) for larger ensembles.

## Removed Points

These points from the input review were removed or significantly weakened after cross-checking against the paper:

1. **"Theorem 2 proves the wrong quantity and this is a structural/fatal issue"** — REMOVED as overstatement. Theorem 2 explicitly states it compares expected advantage (line 207: "outperforms...in expectation"). The paper is careful about this. The gap between expected advantage and accuracy is real but not a fatal or structural flaw; the empirical results in Table 2 already validate the accuracy claim directly. Kept as a minor weakness above.

2. **"The practical algorithm tested on real data is a heuristic, not the theoretically grounded method"** — WEAKENED. The paper explicitly acknowledges this limitation (abstract lines 27–29, Section 5.2 lines 257–275). The characterization is factually correct but the paper does not hide or misrepresent this. Kept as a minor weakness above.

3. **Formatting artifact criticism (line 82)** — REMOVED per hard rules on formatting/style nitpicks.

4. **"No variance/confidence intervals reported"** — REMOVED. Single-run evaluation on LLM benchmarks is standard practice in this community.

5. **"Statistical significance with large sample sizes coexists with small effect sizes"** — REMOVED as duplicative of the "modest gains" weakness.

## Novel Insights

The reviewer's observation that Theorem 2 proves a statement about expected advantage rather than accuracy is valid, but the gap is narrower than claimed. Since the advantage function determines the aggregator's output (the maximizer over labels), a higher expected advantage for the correct label creates a meaningful — though not formally guaranteed — statistical tendency toward higher accuracy. The empirical evidence in Table 2 already provides direct accuracy validation. The more significant issue is not this theoretical gap but the missing baselines, which prevent the reader from assessing whether the proposed mechanisms provide unique value over simpler alternatives.

## Suggestions

- Add confidence-weighted voting and log-probability averaging as baselines across all experiments. This is the single most important addition.
- Explicitly discuss the gap between expected advantage and accuracy, or add a bound on accuracy in terms of the expected advantage gap.
- Add a qualitative error analysis of cases where the aggregation methods disagree with MV.
- Include a brief discussion of computational complexity for ISP.

## Score and Decision

The paper presents a clean theoretical contribution (Theorem 1 is a genuine result), a well-motivated algorithm (ISP), and a non-obvious conceptual insight about why SP fails in LLM settings. However, the empirical evaluation has a significant gap: the most natural baselines (confidence-weighted methods, which the paper itself cites as effective for LLMs) are absent. Without these, the practical contribution is harder to assess. The paper is a borderline case: the theory is solid and interesting, but the empirical evidence for the methods' practical value is incomplete in its current form.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>