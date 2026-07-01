## Summary

This paper introduces PLAGUE, a modular three-phase framework (Planner, Primer, Finisher) for automated multi-turn jailbreak attacks against LLMs, augmented with a lifelong learning component that stores and retrieves successful attack strategies. The framework achieves state-of-the-art attack success rates (ASR) across multiple frontier models including 81.4% on OpenAI o3 and 67.3% on Claude Opus 4.1, outperforming existing multi-turn attacks by substantial margins under comparable query budgets.

## Strengths

- **Strong empirical results under controlled budgets**: PLAGUE achieves significant improvements over existing methods, with absolute ASR gains of ~20 percentage points on o3 and Opus 4.1, and near-saturated performance on Deepseek-R1 (97.8%) and Llama 3.3-70B (95.8%). The evaluations are conducted with careful baseline alignment (e.g., limiting ActorBreaker to K=2 actors, standardizing turn limits) which increases confidence in the comparisons.

- **Thorough and well-designed ablation study**: Table 3 progressively adds components (Backtracking, Reflection, Planner, Retrieval) to GOAT as the base Finisher, cleanly isolating the contribution of each module. The finding that different components matter for different models—reflection is crucial for o3, backtracking for Claude—is a genuinely actionable insight for red teams.

- **Modular framework design enables useful flexibility**: The plug-and-play integration of existing attacks (GOAT, Crescendo, ActorBreaker) as drop-in components is demonstrated and quantitatively evaluated (Table 4 showing 67.3% ASR on Opus 4.1 with Crescendo Finisher vs. 46.5% with GOAT). This supports the claim that the framework can serve as a practical tool for red teaming.

- **Efficiency analysis is honest and informative**: Table 5 shows that PLAGUE's total LLM call count is comparable to Crescendo and within one turn of GOAT, despite incorporating additional phases. This addresses a natural concern that adding components would inflate the budget.

## Weaknesses

### Fatal
None.

### Major

**1. The "lifelong learning" claim is substantially overstated.** The mechanism described (storing strategy embeddings, retrieving via cosine similarity on goal embeddings, using retrieved examples as in-context learning) is standard retrieval-augmented generation (RAG) with a memory bank. There is no evidence of progressive acquisition of capabilities, no mechanism to prevent catastrophic forgetting beyond the memory bank itself, and no demonstration that the system improves over time beyond what simple retrieval would provide. For a framework named after and centrally motivated by lifelong learning, this gap between framing and implementation is significant. The paper acknowledges that AutoDAN-Turbo's similar approach "seems to yield a discernible improvement...only from human-generated strategies" (Section 2.1), which undermines confidence that PLAGUE's retrieval provides genuine adaptation rather than just static retrieval utility.

**2. Evaluation relies entirely on LLM-as-judge without addressing known reliability issues.** The primary metrics (StrongREJECT and binary-ASR) are computed using Qwen3-235B-A22B-fp8 as the evaluator. Jailbreak evaluation using LLM judges is known to have high false positive rates and sensitivity to prompt phrasing, evaluator model choice, and scoring rubric design. The paper provides no human validation on a subset of examples, no calibration analysis, and no discussion of when or why the evaluator might fail. Given that the paper's central claim is achieving SOTA jailbreaking rates, this methodological gap weakens the reliability of the reported numbers.

**3. Algorithmic novelty is primarily at the framework/integration level rather than introducing fundamentally new techniques.** The three phases each draw directly from existing methods: ActorBreaker for plan generation, Crescendo-style reflection and backtracking, GOAT-style strategy libraries. The Primer phase (removing the final plan step and building context) is the most novel design choice, but its motivation is underdeveloped—the paper states the final step is removed because it is "always highly correlated with the goal" (Section 3.4), but it is not clear why the Finisher cannot use the plan's final step directly or why n-1 steps could not be generated explicitly. For ICLR, where methodological contribution is weighted heavily, this level of novelty may be marginal.

### Minor

**4. The paper uses relative percentage improvements ("factor of 32.14%") which inflate the perceived contribution.** The absolute gains are 19.8pp on o3 and 19.3pp on Opus 4.1—these are genuinely impressive, and the paper would be better served by leading with absolute numbers. The relative framing (especially when baselines are lower, as with Claude Opus 4.1) can mislead readers who do not check the base rates.

**5. The plug-and-play claim is demonstrated on only two component swaps (Crescendo/GOAT as Finisher, ActorBreaker/Our Planner).** The paper does not show that other potential components (e.g., different reflection modules, different scoring rubrics, different backtracking strategies) can be easily integrated, nor does it provide clear guidelines for what makes a component compatible. The claim is partially supported but not thoroughly validated.

**6. No statistical significance or variance reporting beyond averaging over three runs.** Confidence intervals, standard deviations, or individual run results would strengthen the reliability claims, especially given the inherent randomness in LLM-based attacks.

### Trivial

**7. The method description in Section 3.1 states that summarization "serves as short-term memory" but this capability is not evaluated or ablated, making it unclear whether it contributes to the reported results.**

## Nice-to-Haves

- Human evaluation on a random subset of 50-100 attacks per model to calibrate the LLM judge's reliability would substantially strengthen the empirical claims.
- A clearer delineation of which parts of the framework are novel vs. adapted from prior work, perhaps in a table comparing each design decision to the closest existing method.
- An analysis of how the lifelong learning memory grows over the course of 100+ attack objectives and whether retrieval quality degrades as the library grows.

## Novel Insights

Beyond the paper's own contributions, the observation that different models exhibit distinct vulnerability profiles to different attack components (reflection vs. backtracking vs. planning initialization) is genuinely interesting and suggests that safety alignment strategies may differentially impact these mechanisms. The finding that Claude Opus 4.1 is specifically resistant to GOAT-style strategies but vulnerable to Crescendo-style escalation hints at a possible alignment gap in the types of adversarial patterns covered during training. This model-level heterogeneity in vulnerability to attack components deserves further study and could inform more targeted red-teaming as well as more comprehensive safety evaluations.

## Suggestions

1. Reframe or rename the lifelong learning component to accurately reflect its nature as a retrieval-augmented memory system, and add an ablation where the memory module is disabled to isolate its actual contribution.
2. Add human validation or correlation analysis with a known reliable evaluator (e.g., show agreement rates between your Qwen-based judge and human raters on a held-out subset).
3. Clarify the design rationale for removing the final plan step in the Primer phase and consider adding an ablation comparing Primer with n-1 vs. n steps.
4. Report absolute percentage point gains alongside relative improvements in the abstract and introduction to avoid inflating perceptual impact.
5. Include confidence intervals or bootstrapped estimates in the main tables.

## Score and Decision

This is a solid empirical paper with a practical framework and strong results, but the overstated "lifelong learning" framing, reliance on uncalibrated LLM-as-judge evaluation, and primarily integration-level novelty limit its impact. The contribution is useful to the safety community but falls short of the methodological depth typically expected for top-tier acceptance at ICLR.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>