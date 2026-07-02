## Summary
This paper introduces PLAGUE, a plug-and-play framework for generating multi-turn jailbreak attacks against LLMs. The framework decomposes an attack into three phases—Planner, Primer, and Finisher—and incorporates lifelong learning through a memory bank of successful attack strategies. Evaluations on strong models (OpenAI o3, Claude Opus 4.1, DeepSeek-R1, GPT-4o, Llama 3.3) show that PLAGUE achieves over 30% improvement in attack success rate compared to previous state-of-the-art multi-turn attacks, reaching 81.4% ASR on o3 and 97.8% on DeepSeek-R1 under a six-turn budget.

## Strengths
- **Addresses an important and underexplored problem:** Multi-turn jailbreaking is more realistic and less studied than single-turn attacks. The paper provides a principled decomposition of what makes multi-turn attacks effective, which is valuable for both red-teaming and defense.
- **Strong empirical results:** PLAGUE outperforms a comprehensive set of baselines (GOAT, Crescendo, ActorBreaker, AutoDAN-Turbo, X-Teaming, FITD) across five frontier models, often by large margins. The improvements on o3 (32%) and Claude Opus 4.1 (40.2%) are particularly striking.
- **Well-designed ablations:** Table 3 shows step-by-step ablation of each component (backtracking, reflection, planning, strategy retrieval) on two models, clearly attributing the gains to specific mechanisms. The plug-and-play nature is demonstrated by swapping finishers (GOAT → Crescendo) to handle model-specific weaknesses.
- **Efficiency analysis:** Table 5 reports target, evaluator, and planner LLM call counts, showing that PLAGUE’s performance gains come with only modest inference overhead compared to baselines.

## Weaknesses

### Major
- **Only one attacker model is used throughout all experiments:** All PLAGUE results use DeepSeek-R1 as the attacker LLM. While the framework is described as plug-and-play, the paper does not ablate with different attacker models (e.g., smaller or differently-aligned models). This raises questions about whether the observed performance is an artifact of DeepSeek-R1’s capabilities rather than the PLAGUE framework itself.
- **Lifelong learning contribution is modest and not deeply evaluated:** The lifelong learning component (RSS) provides only a 2–5% absolute ASR improvement in the ablation (Table 3). The paper does not analyze the impact of memory size, retrieval quality, or catastrophic forgetting. Given that “lifelong learning” features in the title and abstract, the depth of evaluation is insufficient.

### Minor
- **Comparison to GOAT is slightly unfair in terms of calling overhead:** GOAT uses no evaluator calls and achieves the lowest total LLM call count, yet PLAGUE is compared as “within one extra call.” The cost of evaluator calls (which are part of PLAGUE’s overhead) is non-trivial; a more detailed cost-benefit analysis would strengthen the efficiency claims.
- **Planner phase diversity claim is not directly quantified:** The paper states that PLAGUE improves diversity over ActorBreaker by 15% (Figure 3) but does not describe the diversity metric or show the actual numbers in the main text. Without clear definition and reporting, this claim is hard to assess.
- **Lack of failure case analysis:** The paper does not discuss why or when attacks fail. Understanding failure modes (e.g., which goals are hardest, how often semantic drift occurs) would provide actionable insights for defenders.

## Nice-to-Haves
- Ablate with different attacker LLMs (e.g., GPT-4o, Llama-3) to demonstrate that PLAGUE generalizes beyond DeepSeek-R1.
- Provide a more thorough evaluation of the lifelong learning memory: measure retrieval quality, effect of memory size, and compare against random strategy retrieval.
- Include a clear definition and experimental results for attack diversity.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Add at least one ablation experiment that changes the attacker LLM (e.g., use GPT-4o or Llama-3 as the attacker while keeping the framework fixed).
- Clarify the diversity metric used in the ActorBreaker comparison and report numerical values alongside Figure 3.
- Provide a supplementary analysis of failure cases: which HarmBench categories are most resistant, and why?

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>