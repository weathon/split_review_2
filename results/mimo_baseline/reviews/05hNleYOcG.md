## Summary
The paper introduces PLAGUE, a modular three-phase framework (Planner, Primer, Finisher) for generating multi-turn jailbreak attacks against LLMs, augmented with a lifelong-learning memory component that stores and retrieves successful attack strategies. The framework achieves high attack success rates (e.g., 81.4% SRE on OpenAI o3, 67.3% on Claude Opus 4.1) while remaining competitive in query efficiency with existing methods. The key contribution is demonstrating that decomposing multi-turn attacks into modular phases with planning, context-building, and feedback yields measurable improvements, and that existing methods like GOAT, Crescendo, and ActorBreaker can be mixed and matched within the framework.

## Strengths
- **Well-structured modular framework with plug-and-play flexibility.** The decomposition of multi-turn attacks into Planner, Primer, and Finisher phases is conceptually clean and practically useful. The paper demonstrates concretely (Tables 3 and 4) that swapping different finisher modules (GOAT vs. Crescendo) or planning modules (their planner vs. ActorBreaker's) yields different improvements depending on the target model, providing actionable insights for red-teamers.

- **Comprehensive and controlled evaluation.** The paper evaluates across five diverse models (o3, o1, DeepSeek-R1, Claude Opus 4.1, Llama 3.3-70B) using consistent budgets, two complementary metrics (SRE and binary ASR), and reports ASR@K averaged over three runs. The efficiency analysis (Table 5) tracking Target, Evaluator, and Planner LLM calls across all methods is thorough and fair.

- **Insightful per-model component analysis.** The ablation studies (Table 3) reveal that different components matter for different models — reflection drives the largest gains for o3 while backtracking is most impactful for Claude Opus 4.1. This is genuinely useful for understanding model-specific vulnerabilities and is more than just incremental.

- **Controlled incremental ablation.** Table 3's stepwise addition of components to GOAT clearly demonstrates the marginal contribution of each element (backtracking, reflection, planning, strategy retrieval), providing transparency about what drives improvements.

## Weaknesses
### Fatal
None.

### Major
- **Claims are overstated relative to actual results.** The abstract claims "improving attack success rates by more than 30% across leading models," but this is not uniform. On DeepSeek-R1, PLAGUE (0.978 SRE) is essentially identical to GOAT (0.978 SRE) — a 0% improvement. On Llama 3.3-70B, PLAGUE (0.958) barely exceeds GOAT (0.950) — less than 1% improvement. The substantial gains are concentrated on o3 (+22.7pp over GOAT, +44pp over Crescendo) and o1 (+13.3pp). The phrase "improvement by a factor of 32.14%" is misleading language (factors are multiplicative, this is an additive percentage point improvement from 0.616 to 0.814 SRE over ActorBreaker). These overstated claims undermine credibility.

- **Binary ASR results tell a different story than SRE for several models.** On DeepSeek-R1, GOAT's binary ASR (0.937) nearly matches PLAGUE (0.945). On Llama 3.3-70B, GOAT (0.932) and PLAGUE (0.942) are similarly close. The claimed dominance is heavily metric-dependent, yet the paper glosses over this by using "ASR and SRE interchangeably" (Section 4), which obscures important nuances in the evaluation.

- **Lifelong learning contribution is underspecified and limited in evidence.** The strategy library is initialized with "two strategies adapted from examples in Crescendo," and the paper does not report how many strategies accumulate over time or demonstrate improvements across successive attack runs. The claim of being "the first multi-turn attack to feature a lifelong-learning component" is not substantiated with longitudinal experiments showing the system actually learning and improving over multiple goal evaluations.

- **Baseline comparisons involve non-trivial modifications.** GOAT is run "without history enabled," ActorBreaker is limited to K=2 actors, and Crescendo is run with modified backtracking. While the paper is transparent about these changes, the cumulative effect of these modifications on baseline performance is not quantified, making it difficult to attribute PLAGUE's superiority to its framework design versus favorable baseline configuration.

### Minor
- **Evaluation methodology has internal inconsistencies.** The paper uses two evaluators (Qwen3-235B for binary ASR, StrongReject for SRE) but the rubric scorer (R) also uses a specific model (not clearly stated). The scoring thresholds (7/10 for Primer, 3/10 and 8/10 for Finisher) appear arbitrary and their sensitivity is not explored. Different threshold choices could substantially affect the results.

- **Missing diversity analysis.** Figure 3 is referenced ("diversity improves by 15%") but diversity metrics are not consistently reported across all configurations in the main tables. This makes it impossible to evaluate the diversity-efficiency tradeoff systematically.

- **The "novel insights" about what makes multi-turn attacks work are limited.** Despite the introduction's promise of "formal investigation," the findings (modular design helps, context freezing prevents drift, strategy retrieval helps on some models) are reasonable but not particularly surprising.

### Trivial
None worth noting.

## Nice-to-Haves
- A longitudinal analysis showing strategy library growth and corresponding ASR improvements over multiple attack campaigns would substantially strengthen the lifelong learning claims.
- Reporting confidence intervals or standard deviations alongside mean ASR values (since the paper already runs three seeds) would enable readers to assess statistical significance of improvements.
- A dedicated diversity metric (e.g., distinct n-grams, embedding diversity of generated attacks) reported consistently across all configurations.

## Novel Insights
The paper's most novel observation is the identification of model-specific vulnerability patterns through the ablation studies: reflection is the most impactful component for OpenAI's o3 while backtracking dominates for Claude Opus 4.1, suggesting these models have fundamentally different safety failure modes. This has practical implications for designing targeted red-teaming strategies. The observation that GOAT as a finisher performs poorly against Claude 4.1 (likely due to alignment training on GOAT-like patterns) but Crescendo succeeds is also genuinely informative for the safety community.

## Suggestions
- Calibrate claims to match empirical evidence. Replace "improving ASR by more than 30% across leading models" with a more accurate statement about the magnitude and concentration of improvements.
- Run GOAT and Crescendo with their default configurations alongside the modified versions to provide both "fair comparison" and "default performance" baselines.
- Expand the lifelong learning section with multi-campaign experiments showing strategy accumulation and its effect on ASR over time.
- Clarify the relationship between the rubric scorer thresholds and final ASR through a sensitivity analysis.

## Score and Decision

The paper presents a well-motivated modular framework for multi-turn jailbreaking with a controlled and comprehensive evaluation. The per-model component analysis provides genuine insights, and the ability to compose existing methods within the framework is practically valuable. However, the empirical improvements are highly concentrated on a subset of models (primarily o3 and o1), the lifelong learning contribution is underdeveloped, and claims consistently overstate the breadth and magnitude of improvements. For ICLR, where novelty and rigor are paramount, these issues — particularly the gap between claims and evidence — weigh against acceptance. The contribution sits in the incremental range: a useful engineering framework with some genuine insights, but not a breakthrough in understanding or methodology.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject