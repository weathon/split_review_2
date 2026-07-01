## Summary

This paper presents PLAGUE, a plug-and-play framework for generating multi-turn jailbreak attacks against LLMs. The framework decomposes the attack into three phases—Planner (generates a plan using retrieved successful strategies), Primer (builds adversarial context through seemingly benign questions), and Finisher (delivers the final attack)—and incorporates a lifelong learning component that stores successful strategies for future retrieval. Experiments on multiple state-of-the-art models (OpenAI o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3) show that PLAGUE achieves attack success rates (ASR) of up to 97.8%, outperforming existing multi-turn attacks by 30%+ on the hardest models.

## Strengths

- **Timely and important problem**: Multi-turn jailbreaking is less explored than single-turn attacks, yet it is the dominant mode of LLM interaction. The paper addresses a critical gap in red-teaming research.
- **Modular plug-and-play design**: The framework cleanly separates planning, context-building, and finishing phases, allowing existing attacks (GOAT, Crescendo, ActorBreaker) to be integrated as components. This enables systematic ablation and customization.
- **Comprehensive evaluation**: Experiments cover five leading models (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3) with two metrics (StrongREJECT and binary-ASR), controlled budgets, and multiple baselines. The ablation studies (Tables 3 and 4) clearly isolate the contribution of each component.
- **Efficiency analysis**: Table 5 shows that PLAGUE achieves higher ASR with comparable or fewer total LLM calls than baselines, demonstrating practical efficiency.
- **Novel lifelong learning component**: The memory bank with cosine-similarity retrieval of successful strategies is a novel addition to multi-turn attacks, and the ablation shows it provides meaningful gains (RSS in Table 3).

## Weaknesses

### Fatal
None.

### Major
1. **Lifelong learning is not demonstrated over a lifetime**: The paper claims "lifelong learning" but the experiments only evaluate per-goal attacks. The memory bank is populated with two initial strategies, and retrieval is tested in a single-goal setting. There is no experiment showing that the agent improves over a sequence of multiple goals by learning from past successes. The term "lifelong learning" is overclaimed relative to what is actually shown.
2. **Rubric scorer reliability is unvalidated**: The intermediate scoring rubric (compliance, practicality, level of detail, relevance) is used for backtracking and reflection decisions, but no inter-annotator agreement, human validation, or analysis of scoring consistency is provided. The paper does not demonstrate that the rubric scores are reliable or correlate well with final evaluation.
3. **Lack of diversity metrics**: The paper claims that the planning module improves diversity (citing Figure 3, which is not in the provided content) but does not report any quantitative diversity measure (e.g., embedding diversity, strategy diversity, semantic diversity of generated plans). Without such metrics, the diversity claim is unsupported.
4. **Potential data contamination not discussed**: The HarmBench dataset is used for evaluation, but the paper does not address whether the target models may have been exposed to these harmful prompts during training or alignment. This is a known concern in jailbreak evaluation and should be acknowledged.
5. **Attacker model choice not ablated**: All experiments use Deepseek-R1 as the attacker model. The results may be highly dependent on the attacker's capabilities. An ablation with a weaker attacker (e.g., Llama 3.1-8B) would strengthen the claim that the framework itself drives improvements.

### Minor
1. **ASR@2 metric may favor certain methods**: The paper uses best-of-2 attempts for all methods, but some baselines (e.g., ActorBreaker with multiple actors) may naturally have more attempts within the budget. The paper should clarify how the budget constraint interacts with the ASR@K metric.
2. **Claude Opus 4.1 results are split across tables**: The main table (Table 2) shows PLAGUE with GOAT finisher (46.5% SRE), while the best result (67.3%) is in Table 4 with Crescendo finisher. This presentation is confusing and could mislead readers about the overall performance on Claude.
3. **Figure 1 contains placeholder text**: The diagram shows "Goal: GOAT, Goal: GOAT, Goal: GOAT" which appears to be a placeholder and is not explained.
4. **Binary-ASR vs. SRE relationship not analyzed**: The paper uses both metrics but does not discuss how they correlate or why both are needed beyond "completeness."

### Trivial
None.

## Nice-to-Haves
- A true lifelong learning experiment where the agent attacks multiple goals sequentially and shows improvement over time (e.g., ASR on later goals vs. earlier goals).
- Diversity analysis using embedding distances or strategy-type distributions.
- Human validation or inter-annotator agreement for the rubric scorer.
- Ablation of the attacker model (e.g., using a smaller or different LLM as the attacker).
- Discussion of potential defenses against PLAGUE-style attacks and ethical considerations for releasing the framework.

## Novel Insights

The paper's key insight is that decomposing multi-turn attacks into planning, priming, and finishing phases, combined with retrieval of successful strategies from memory, yields substantial improvements over monolithic attack methods. The observation that different models have distinct vulnerabilities (e.g., Claude Opus 4.1 resists GOAT-based attacks but is more vulnerable to Crescendo-based attacks) is practically valuable for red-teamers. The plug-and-play design also reveals that the relative importance of components (backtracking, reflection, planning, retrieval) varies across models, offering a nuanced understanding of model-specific weaknesses.

## Suggestions
- Conduct a lifelong learning experiment: run PLAGUE on a sequence of 50+ goals and measure whether ASR improves over time as the memory bank grows.
- Report diversity metrics (e.g., average pairwise embedding distance of generated plans, number of distinct strategies used).
- Validate the rubric scorer by comparing its scores with human judgments on a subset of 50 samples.
- Ablate the attacker model by replacing Deepseek-R1 with a smaller model (e.g., Llama 3.1-8B) and report the impact on ASR.
- Clarify the budget enforcement for each baseline and how ASR@2 is computed within the 6-turn limit.

## Score and Decision

The paper makes a solid contribution to multi-turn jailbreaking with a well-designed modular framework and extensive experiments. However, the overclaimed "lifelong learning" (not demonstrated over multiple goals), unvalidated rubric scorer, and lack of diversity metrics prevent it from being a top-tier paper. The work is above average and brings value to the community, but the major weaknesses warrant a borderline accept.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>