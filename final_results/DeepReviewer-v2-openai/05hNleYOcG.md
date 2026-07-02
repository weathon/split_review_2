## Summary
# Final Review Report

## Summary

This paper presents PLAGUE, a plug-and-play framework for generating multi-turn jailbreak attacks against Large Language Models. The framework decomposes the attack process into three phases—Planner (strategy retrieval and plan generation), Primer (adversarial context building), and Finisher (goal-directed query execution)—connected by a lifelong-learning component that stores successful strategies in an embedding-indexed memory. The core claimed contributions are: (C1) a modular three-phase decomposition that disentangles planning, context escalation, and final attack delivery; (C2) a lifelong-learning mechanism that retrieves successful past strategies via goal-embedding similarity; and (C3) a plug-and-play design that allows existing attacks (GOAT, Crescendo, ActorBreaker) to be used as interchangeable Finisher or Planner modules.

The paper evaluates PLAGUE on the HarmBench benchmark against 5 frontier LLMs (OpenAI o3/o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B) and 5 baselines, reporting StrongREJECT ASR improvements of up to 32% on o3 and 40% on Claude Opus 4.1. The experimental design includes ablation studies isolating the contributions of backtracking, reflection, planning, and strategy retrieval components.

The work has merit in formalizing multi-turn attack design and demonstrating empirical gains under controlled budgets. However, several concerns affect the current presentation: baseline modifications that undermine fair comparison, insufficient justification for key design choices (scoring thresholds, planner initialization, feedback adaptation), and rhetorical overclaim in novelty and SOTA positioning. Novelty verification is deferred due to Retrieval-Disabled Mode.

## Strengths
1. **Well-defined problem framing.** The paper correctly identifies that multi-turn jailbreaking is an underexplored but practically important attack surface, given that most LLM interactions are now conversational. The motivation is timely and the gap is real.

2. **Systematic three-phase decomposition.** The Planner-Primer-Finisher breakdown is a natural and useful abstraction for understanding multi-turn attack design. It provides a structured vocabulary (plan initialization, context escalation, goal-directed finishing) that prior work lacked. This decomposition alone is a contribution to the red-teaming methodology.

3. **Comprehensive empirical evaluation across frontier models.** The paper evaluates on 5 different production LLMs (o3, o1, Deepseek-R1, Claude Opus 4.1, Llama 3.3-70B) using the HarmBench dataset, providing a broad picture of attack effectiveness. The use of both StrongREJECT and binary-ASR metrics, along with ASR@K reporting, adds robustness to the evaluation.

4. **Thoughtful ablation study.** Table 3 provides a clear additive ablation (GOAT -> +BT -> +R -> +P -> +RSS) that shows the marginal contribution of each component. This is a strength because it allows readers to understand which design choices drive the reported gains (e.g., reflection matters most for o3; backtracking matters most for Claude).

5. **Efficiency analysis with LLM call budgets.** Table 5 compares total API calls across methods, demonstrating that PLAGUE's gains do not come from simply consuming more budget. The per-method breakdown into Target, Evaluator, and Planner calls is informative for practitioners.

6. **Plug-and-play modularity demonstration.** The paper shows that different Finisher modules (GOAT vs Crescendo) yield different model-specific results (Table 4), validating the claim that component substitution is practical. This finding—that model vulnerability patterns differ—is an interesting empirical insight.

## Weaknesses
### W1. Baseline modifications compromise fair comparison (Major)

The paper claims "apples-to-apples comparison" but modifies baseline implementations in ways that may systematically disadvantage them:
- **GOAT** is run without conversation history (authors claim negligible impact but provide no evidence) and with a per-round Rubric Scorer that was not part of the original design.
- **Crescendo** has backtracking counts removed, which is a core feature of the official implementation.
- **ActorBreaker** is limited to K=2 actors, whereas more actors typically increase both coverage and compute cost.
- **AutoDAN-Turbo**, a single-turn attack, is evaluated in a 6-round multi-turn setting that it was not designed for.

Without ablation studies showing that these modifications do not harm baseline performance, the reported margins of improvement (30-40%) may be inflated by artificially weakened baselines. **Required action:** Provide side-by-side comparisons of original vs. modified baseline configurations, or justify each modification with targeted sensitivity analysis.

### W2. Design parameter choices lack validation (Major)

The PLAGUE framework introduces numerous design parameters whose values are asserted without evidence:
- **Scoring thresholds:** Primer backtracking at 7/10, Finisher backtracking at 3/10, success at 8/10. No sensitivity analysis is provided. The >2x discrepancy between Primer and Finisher thresholds is unexplained.
- **Plan length:** Two-step plans are used because authors "find this to be the best-performing setting," but no ablation across 1-step, 2-step, 3-step, or 4-step plans is reported.
- **Strategy retrieval threshold:** Cosine similarity threshold of 0.6 with a maximum of 2 retrieved examples. The choice of 0.6 is not justified, and the small library (initialized with only 2 strategies) means early retrievals are nearly random.
- **Rubric scoring conditional dependencies:** The rule that relevance=0 forces practicality and detail to 0 effectively creates a 6-point maximum score when relevance fails, but this design is not analyzed.

**Required action:** Add sensitivity analyses for the key thresholds (scoring, plan length, similarity) and report how ASR changes with each parameter. At minimum, provide a held-out validation set for threshold selection.

### W3. Efficiency analysis omits attacker-side compute cost (Major)

Table 5 reports Target, Evaluator, and Planner LLM calls, but PLAGUE's Primer phase requires multiple internal Attacker LLM invocations that are not counted. The total computational cost (tokens consumed) for the attacker-side model (Deepseek-R1) across the Primer and Finisher phases could be substantially higher than baselines that lack such components. The paper claims PLAGUE achieves its gains with "minor inference overheads" but does not measure the overhead of the attacker model itself, only the target model. **Required action:** Report total Attacker LLM token consumption per attack and, ideally, a cost-normalized ASR metric (ASR per dollar or per 100K tokens).

### W4. Unverifiable novelty and "first" claims (Major)

The paper makes strong novelty claims that cannot be verified under Retrieval-Disabled Mode:
- "PLAGUE is the **first** multi-turn attack to feature a lifelong-learning component" (Section 2.3). AutoDAN-Turbo already uses lifelong learning for single-turn attacks, and the boundary between single-turn and multi-turn lifelong learning is not a clear qualitative gap. Concurrent work may also claim this feature.
- "State-of-the-art jailbreaking results" (Abstract). Without comprehensive literature comparison, this is an assertion, not a validated finding.
- "Most comprehensive evaluation of multi-turn attacks to date" (Section 5.1). This self-attributed superlative is editorializing.

**Required action:** Downgrade "first" to "to our knowledge, the first" and provide explicit differentiation from AutoDAN-Turbo's lifelong learning approach. Replace SOTA claims with bounded comparative language. Remove or qualify self-attributed superlatives.

### W5. Text-figure inconsistency and missing evidence (Minor-Major)

- **GPT-4o mention:** The Introduction claims 97.8% on "Deepseek-R1, GPT-4o and Meta's Llama 3.3-70B" but Table 2 does not include GPT-4o results. This inconsistency erodes trust.
- **Figure 3 (diversity) is referenced but not provided** in the available manuscript text. The diversity measurement methodology (how 15% improvement is computed) cannot be verified.
- **Algorithms 1-3 are referenced but not included** in the manuscript body; the reader cannot verify notation consistency or implementation details.

**Required action:** Add GPT-4o results to the main table or remove the reference. Include Figure 3 and diversity metrics with clear definitions. Provide algorithms in the main text or appendix.

### W6. Methodological ambiguity in feedback adaptation (Minor-Major)

The Finisher phase backtracks when score < 3/10 and feeds "score, score feedback, attempted query, response and response summary" to the Attacker for re-attempt. The mechanism by which the Attacker integrates this feedback is not specified—whether the feedback is prepended as a text prompt, used to modify the query generation process, or processed through a structured template. This underspecification makes the method difficult to reproduce independently. **Required action:** Provide the exact prompt template used for feedback incorporation and a representative example of how the Attacker's output changes after receiving feedback.

### W7. Unsupported claim about system robustness in Conclusion (Minor)

The Conclusion states that PLAGUE "advance[s] the frontiers of building robust LLM systems for a more faithful mode of conversation—multi-turn." This claim is not supported by any experiment in the paper, which evaluates PLAGUE exclusively as an attack tool, not as a defense framework. **Required action:** Remove or rephrase to describe the actual contribution: enabling systematic vulnerability identification.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and practically important problem (multi-turn LLM jailbreaking) with a systematic three-phase framework that represents a genuine methodological contribution. The empirical evaluation is broad, covering 5 frontier models with ablation studies that isolate component contributions. The plug-and-play modularity demonstration (GOAT vs Crescendo Finisher) yields model-specific insights that are valuable for the red-teaming community.

However, the score is constrained by several factors that affect the paper's reliability and scientific rigor:

1. **Comparison fairness (validity risk):** Baseline modifications (removing Crescendo's backtracking, disabling GOAT's history, limiting ActorBreaker's actors) are not validated as harmless. The claimed 30-40% improvements may partially reflect artificially weakened baselines.

2. **Unvalidated design parameters (reproducibility risk):** Key thresholds (scoring bars, plan length, retrieval similarity) are asserted without sensitivity analysis. The framework's performance may be brittle to these choices.

3. **Novelty uncertainty:** Strong "first" and "SOTA" claims cannot be independently verified under Retrieval-Disabled Mode. The lifelong learning component, while novel for multi-turn attacks, shares conceptual inheritance with AutoDAN-Turbo's single-turn lifelong learning.

4. **Omitted cost accounting:** The efficiency analysis does not count attacker-side LLM compute, which may be substantial for the Primer phase.

5. **Presentation issues:** Text-figure inconsistency (GPT-4o mention without table entry), missing algorithm listings and diversity figure, and several rhetorical overclaims.

All identified weaknesses are fixable with moderate revision effort. The core framework and empirical findings are valuable enough to warrant publication after addressing the fairness, validation, and presentation concerns.

**Post-Revision Target: 7/10** (achievable with baseline justification, threshold sensitivity analysis, and claim bounding).