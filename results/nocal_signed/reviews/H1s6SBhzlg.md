Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper studies how to aggregate answers from multiple LLMs more effectively than standard majority voting. It introduces two theoretically grounded algorithms — Optimal Weight (OW), which uses agents' accuracies (first-order information) with a provably Bayesian-optimal linear weighting scheme, and Inverse Surprising Popularity (ISP), which uses cross-agent answer correlations (second-order information) and provably outperforms both majority voting and the standard surprisingly popular rule. The paper provides formal theoretical guarantees (Theorems 1–3), validates the methods on simulations, and shows consistent improvements over majority voting across 16 model combinations on UltraFeedback, MMLU, and a healthcare dataset (ARMMAN).

## Strengths

- **Rigorous theoretical framework connecting information aggregation to LLM ensembles.** The paper proves Bayesian optimality of the OW aggregator (Theorem 1), derives closed-form expected advantage differences among ISP, MV, and SP (Theorem 2), and provides finite-sample guarantees (Theorem 3). Section 3 cleanly characterizes when majority voting is optimal (homogeneous agents, Corollary 2) and when OW strictly dominates any single agent (Proposition 2).

- **Principled derivation of ISP as a counterfactual variant of SP.** The observation that SP underperforms MV in the LLM setting (Section 4.1) and the construction of ISP to flip the conditional predictions (Section 4.2) are well-motivated. Example 1 (Table 1) illustrates a concrete case where ISP succeeds where both MV and SP fail. Theorem 2 then formalizes the ordering ISP ≻ MV ≻ SP in expectation with explicit gap expressions.

- **Real-world evaluation across multiple LLM families and datasets.** The paper uses 16 model combinations from four families (GPT, Qwen, Llama, Phi) across three datasets (UltraFeedback, MMLU, ARMMAN). The finding that MV never achieves the best performance in any of the 16 ensembles (line 313) is a striking empirical result. The healthcare application (ARMMAN) adds practical relevance beyond standard NLP benchmarks.

## Weaknesses

### Fatal
None.

### Major

- **OW-L and OW-I produce identical results across all three datasets with no explanation.** In Table 3, OW-L and OW-I both achieve 73.66%, 90.37%, and 85.78% — exact matches. In Table 4, their per-question discrepancy counts are identical (2545/1727, 1821/659, 264/195). On ARMMAN, ISP also matches at 85.78% with identical counts. OW-L uses empirical risk minimization on second-order conditional probabilities (Eq. 7), while OW-I uses ISP's aggregated predictions as pseudo-labels; two such different pipelines yielding exactly the same correct/incorrect predictions on every question across all datasets is unlikely without explanation. The paper provides no discussion of why this occurs, whether the methods converge to the same weight estimates, or whether one method subsumes the other. This undermines confidence in the experimental pipeline and must be addressed.

### Minor

- **The function σ_K is defined inconsistently between the abstract and Section 3.** The abstract (line 25) defines σ_K(x) = x²/(K−1+x²), while Section 3 (line 73) defines σ_K(x) = eˣ/(K−1+eˣ). Corollary 1 (line 90) uses the logistic σ(x)=eˣ/(1+eˣ) for K=2, consistent with Section 3 but not the abstract. Since all algorithmic content follows the Section 3 definition, the abstract contains an error that could confuse readers about the weight formula.

- **The theoretical results (Theorems 1, 2, 3) are proved under Assumption 1 (conditional independence), which is likely violated by LLMs from different families trained on overlapping data.** The paper acknowledges this (line 63) and states Appendix C extends the results, but the main text does not characterize how robust the guarantees are when the assumption is violated. Since the experiments use real LLMs that may violate this assumption, the gap between theory and practice is not fully bridged in the main text.

- **The t-statistics (12.53, 23.39, 3.22) on line 303 are reported without specifying the test design** — it is unclear whether these are paired per-question tests, per-ensemble tests, or what the unit of observation is. The ARMMAN t-statistic of 3.22 against a 0.54% absolute gain needs contextualization to be interpretable.

- **The label-order invariance assumption (line 51)** — that LLM outputs are unaffected by the ordering of options — is stated without empirical verification for the specific models used. One reference is cited (Guo & Vosoughi, 2024), but position bias in multiple-choice evaluation is well-documented even in recent models, and the paper provides no evidence that these particular models satisfy the property.

### Trivial
None.

## Nice-to-Haves

- Add SP as a baseline in the real-world experiments (Table 3) to complete the empirical validation of Theorem 2's ordering ISP ≻ MV ≻ SP.
- Include a brief cost-accuracy tradeoff discussion: running N=4 LLMs (including GPT-4o) for 0.54–1.45% absolute gains is a practical consideration for practitioners.
- Provide empirical verification of the label-order invariance assumption on the specific models used (e.g., swapping label order on a subset of questions and measuring agreement).
- Compare against a simple confidence-weighted voting baseline if per-token probabilities are available.
- Discuss how large M needs to be for the ISP advantage in Theorem 3 to dominate the estimation error term in practice.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **"The practical improvements are very modest"** — This is a factual observation about the results, not a weakness of the paper. The paper honestly reports its findings (0.54–1.45% absolute gains); the gains are modest but consistent and statistically significant.
- **"Algorithm box formatting issue (line 82)"** — Parser artifact, not an author error. Per guidelines, formatting artifacts are not evaluated.
- **"No SP baseline in real-world Table 3"** — Valid suggestion but not a required baseline; the simulation (Table 2) already validates the ISP ≻ MV ≻ SP ordering. Moved to Nice-to-haves.
- **"No comparison with confidence-weighted aggregation methods"** — The paper's setting is unsupervised (no ground-truth labels). Confidence-based methods typically require different information access. Scope-adjacent suggestion moved to Nice-to-haves.
- **"Cost analysis missing"** — Reasonable suggestion but not a core flaw. Moved to Nice-to-haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Resolve the σ_K inconsistency between the abstract and Section 3 by making the abstract consistent with the body.
- Explain why OW-L and OW-I produce identical predictions across all datasets — either because they converge to the same weight vector (and if so, why) or because of a reporting artifact (and if so, report with more precision).
- Specify the t-test design (paired? per-question? degrees of freedom?) for the hypothesis tests reported on line 303.

## Score and Decision

MY FINAL SCORE: 6
MY FINAL DECISION: Accept