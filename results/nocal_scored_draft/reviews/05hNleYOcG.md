Now let me assemble the final review.

## Summary

PLAGUE proposes a modular, plug-and-play framework for multi-turn jailbreak attacks, decomposing the attack into three phases (Planner → Primer → Finisher) with a lifelong-learning memory component. The framework design allows existing attacks (GOAT, Crescendo, ActorBreaker) to be substituted as modules, enabling systematic analysis of individual components. Empirical results show high ASR (81.4% on o3, 67.3% on Claude Opus 4.1) with competitive query budgets, and the ablation study demonstrates monotonic improvements from adding each component.

## Strengths

- **The plug-and-play modular design is a genuine contribution.** Prior multi-turn jailbreak methods (Crescendo, GOAT, ActorBreaker) were each monolithic proposals. PLAGUE's decomposition into Planner, Primer, and Finisher, with the ability to substitute individual modules (e.g., swapping GOAT for Crescendo as the Finisher), enables systematic analysis of what makes each component effective. This is demonstrated concretely in Table 4 (where swapping Finishers yields very different results on Claude Opus 4.1) and Table 3 (components added incrementally).

- **The ablation study in Table 3 is well-structured:** adding Backtracking, Reflection, Planner, and Retrieval of Successful Strategies in sequence, showing ASR improvement at each step. The finding that different components matter more for different target models (Reflection helps o3 more; Backtracking helps Claude more) is a genuinely interesting empirical observation (Section 5.1).

- **The paper takes computational budget seriously.** Table 5 reporting Target, Evaluator, and Planner LLM call counts is a rarity in adversarial attack papers and demonstrates that PLAGUE's gains are not simply from throwing more queries at the target.

- **The reported ASR numbers are high and competitive:** 81.4% on o3 and 67.3% on Claude Opus 4.1, two models considered highly resistant to jailbreaks.

## Weaknesses

### Fatal

None.

### Major

- **Baseline implementations are modified in ways that could reduce their performance, and the paper provides no data confirming these modifications are harmless.** Specifically: (a) GOAT is run "without history enabled for the Attacker" — the authors claim the impact is "negligible" (Section 4, Baselines) but do not report the comparison with history enabled; (b) ActorBreaker is limited to K=2 actors, whereas the method was designed to use multiple actors; (c) Crescendo has "explicit backtracking counts" removed. Without evidence that these modifications do not harm baseline performance, it is unclear whether PLAGUE outperforms the baselines or outperforms crippled versions. The disclosure is appreciated, but data is needed.

- **Diversity is claimed as a key motivation and a demonstrated strength** — the paper states "diversity improves by 15% (Figure 3)" and lists diversity as one of three design desiderata in the Introduction — but **no diversity metric is defined anywhere in the paper body** and no diversity measurement, score, or comparison table appears in the extracted text. The paper repeatedly motivates diversity and claims it as a benefit, but provides no concrete evidence or definition, making a central part of the argument unsubstantiated.

### Minor

- **The Rubric Scorer (R) serves dual roles:** providing intermediate feedback to guide the attack and determining whether the attack succeeded (score > 8/10 triggers early stopping and memory storage), using the same rubric. While the external Evaluator Judge (J) using StrongREJECT provides independence for final metrics, the binary "success" decision that governs the lifelong learning memory is made by R. If R's scoring has any systematic bias, it could inflate the apparent success rate stored for retrieval. The paper should report the correlation between R's scores and J's evaluation.

- **The "lifelong learning" component is standard retrieval-augmented memory** (vector database with cosine similarity search), not lifelong learning in a technical sense. There is no parameter update, no mechanism to prevent catastrophic forgetting over a sequence of tasks, and no evidence of learning across attack objectives beyond the retrieval mechanism itself. The framing overstates what is implemented, though this does not invalidate the retrieval mechanism's practical utility.

- **No variance or confidence intervals are reported** anywhere in the results (Tables 2–5) despite only averaging over 3 runs with inherently stochastic LLM-based attacks. For small margins (e.g., PLAGUE vs GOAT on Deepseek-R1 SRE at 0.978 vs 0.978), this makes it impossible to assess significance.

- **The similarity threshold of 0.6 and the limit of 2 retrieved examples** are presented without ablation or justification.

- **The paper has no limitations section**, which is a meaningful omission given the interpretative challenges and modifications to baselines noted above.

### Trivial

None.

## Nice-to-Haves

- Explicitly confirm in the Baselines section that all methods used the same Attacker model (Deepseek-R1). The paper currently says "across all our experiments" (Section 4, Models) which strongly implies uniformity, but explicit confirmation in the Baselines section would eliminate ambiguity.
- Ablate the similarity threshold (0.6) and retrieval limit (2 examples).
- Report the correlation between R's scores and J's evaluation.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Attacker model confound (from Harsh Critic Issue 1):** The critic claimed "the paper does not state what attacker model the baselines use" and that "the attacker model is not held constant." In fact, Section 4 (Models) states: *"We use Qwen3-235B-A22B-fp8 as our Evaluator Model and Deepseek-R1 as our primary Attacker model across all our experiments."* The phrase "across all our experiments" indicates uniformity. The paper could be more explicit in the Baselines section, but the claim of a hidden confound is not supported by the text. A softened clarity note is kept in Nice-to-Haves.
- **Duplicate ActorBreaker row in Table 2:** This is a parser/formatting artifact, not a paper error.
- **Missing Figure 3 / diversity figure absent from body:** Figures are stripped by the parser; they exist in the original submission. The remaining concern (no diversity metric defined in text) is retained in Major.
- **Request for larger dataset, more models:** Generic scope-creep; the HarmBench 200-sample set and model zoo are adequate.
- **Speculation about Claude Opus resistance to GOAT being unsubstantiated:** The authors explicitly offer this as a theory ("We theorize that this is because of extensive alignment..."), not a factual claim.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report the comparison of GOAT with vs. without history enabled to justify the "negligible impact" claim.
- Define and report a diversity metric (e.g., embedding diversity, n-gram diversity, or the metric used by ActorBreaker's authors) to substantiate the 15% improvement claim.
- Report standard deviations or confidence intervals for main results given the 3-run average and inherent stochasticity.
- Include a limitations section.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>