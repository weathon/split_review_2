## Summary

This paper investigates LLM performance in Dou Dizhu, a popular Chinese three-player card game representing dynamic imperfect information games. The paper makes two contributions: (1) a fair benchmark using a duplicate round-robin tournament to neutralize card-deal luck, and (2) a data-centric framework (GOFA) for fine-tuning a small 4B model using two data curation mechanisms — post-hoc "God's-eye" counterfactual validation and multi-agent real-time feedback scoring. The fine-tuned Qwen3-4B-GOFA model shows a large improvement over its untuned baseline, outperforming much larger Qwen models in the same family.

---

## Strengths

- **Duplicate tournament benchmark is principled.** Borrowing from competitive bridge to neutralize card-luck is a well-justified and underused idea for card-game evaluation. It provides a genuinely fairer comparison than raw win-rate.

- **Strong empirical improvement.** The 4B model improves from an average duplicate score of −65.80 to +17.25, surpassing Qwen models up to 14B. The ablation (Table 5) cleanly decomposes contributions of the two curriculum stages.

- **Decision-efficiency gain.** The fine-tuned model produces the fewest errors and shortest outputs among all compared models, suggesting that the training improves rule adherence and precision, not just score.

- **The GOFA data screening is conceptually creative.** Using omniscient re-evaluation to validate decisions made under partial information is a novel heuristic for selecting high-quality training examples tailored to the structure of imperfect-information games.

---

## Weaknesses

### Fatal
None.

### Major

1. **Methodological conflation of optimality under perfect vs. imperfect information.** The "Globally Optimal Decision Alignment" mechanism discards decisions that look suboptimal when all hands are revealed. But a decision rational under partial information may appear suboptimal with full information (e.g., when the hidden cards happen to be unlucky). Conversely, lucky guesses may pass the filter. This filter does not select for principled Bayesian reasoning; it selects for decisions that were fortunate under the revealed deal. The paper does not address this confound, which weakens the theoretical justification for the mechanism.

2. **Benchmark scale is marginal.** The primary benchmark uses 200 unique deals and 400 matches. With six models, many pairwise comparisons are noisy. No confidence intervals or statistical significance tests are reported for any of the key results (Tables 3, 4, 5). Given that the duplicate score differences between some models are modest (e.g., Gemini at 10.05 vs. GPT-5 at 22.20), the ranking may not be reliable.

3. **No comparison against non-LLM baselines.** DouZero achieves superhuman performance on Dou Dizhu using RL. Without any data point from such systems, it is impossible to contextualize where even the best LLM sits relative to expert-level play. This context is important for evaluating the significance of the fine-tuned model's performance.

4. **The feedback mechanism relies on potentially unreliable judges.** Real-time feedback from virtual opponent/teammate agents (themselves LLMs) is treated as ground truth. However, these models are not verified to be reliable strategic evaluators. This circularity — using possibly flawed LLMs to supervise another LLM — is not acknowledged or validated.

### Minor

1. The surprising result that o4-mini scores lowest despite fewest errors is discussed but not explained with rigor. Understanding *why* low error rate correlates with poor score for this model would be valuable.

2. The teacher models for data generation (DeepSeek R1, GLM-4.5) are not included as baselines in Table 4's comparative experiments, even though GLM-4.5 is the top performer in Table 3. It is unclear whether the 4B GOFA model surpasses or falls below the teacher models.

### Trivial
None worth noting.

---

## Nice-to-Haves

- Reporting confidence intervals or bootstrapped variance across the 20 tournament rounds would strengthen all quantitative claims.
- An analysis of which specific decision types (bidding, playing phase, pass-or-play) benefit most from the GOFA data would clarify the mechanism's effect.

---

## Novel Insights

The duplicate-format benchmark adaption from bridge to Dou Dizhu is a useful methodological contribution transferable to other stochastic multi-agent card games. The more interesting finding — that high error rate does not correlate with poor performance and that a model with the lowest error rate (o4-mini) scores worst — hints that instruction-following ability and strategic reasoning capability are partially orthogonal in current LLMs, a subtle finding worth deeper investigation.

---

## Suggestions

- **Validate the God's-eye filter theoretically or empirically.** Measure what fraction of filtered-out decisions were actually strategically sound under information uncertainty (e.g., by checking whether they were rational given the prior distribution over hidden cards). This would either validate or expose the filter's logic.
- **Add confidence intervals** to all scoring tables.
- **Include DouZero or a similar RL baseline** in the benchmark as an anchor for absolute capability.
- **Validate feedback judges** by checking inter-rater agreement or by replacing them with a rule-based oracle for a subset of hands.

---

## Score and Decision

The duplicate benchmark is a solid methodological contribution and the empirical improvements are genuine and large. However, the central data curation mechanism (God's-eye validation) conflates two different notions of optimality in a way that weakens the paper's theoretical grounding, and the lack of statistical rigor and non-LLM baselines limits interpretability. The work is interesting but not yet fully validated.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>