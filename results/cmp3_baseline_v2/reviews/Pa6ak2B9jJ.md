## Summary
This paper introduces AUTO-RT, a reinforcement learning framework for automatic jailbreak strategy exploration in LLM red-teaming. The key novelty is formulating attack generation as a sequential decision process over high-level strategies rather than individual prompts, and introducing two techniques—Dynamic Strategy Pruning (DSP) to filter redundant/inconsistent branches early, and Progressive Reward Tracking (PRT) with a First Inverse Rate (FIR) metric to shape sparse rewards using downgraded models. Experiments across 16 white-box and 2 black-box LLMs show consistent improvements in attack success rate (up to 16.63% absolute gains in many settings), semantic diversity, and defense generalization compared to several baselines.

## Strengths
- **Novelty and clear framing.** Decomposing the attack model into a strategy generator and a rephraser, and treating jailbreak discovery as a constrained MDP over abstract strategies is a meaningful conceptual advance over prior work that uses fixed templates or direct prompt optimization. This hierarchical formulation reduces the bias of fixed templates and enables broader coverage of the vulnerability space.
- **Two well-motivated technical components.** DSP addresses the "overwhelming safe signals" problem by terminating unpromising branches early with a theoretical guarantee for constrained MDPs. PRT tackles reward sparsity via a carefully designed reward shaping scheme that uses downgraded models, with FIR providing a principled way to select an appropriate downgrade level. Both components are clearly motivated by the challenges identified in Section 2.3.1.
- **Thorough and rigorous experimental evaluation.** The paper evaluates across 18 models of different families and sizes, uses multiple complementary metrics (effectiveness, semantic diversity, defense generalization diversity, efficiency over training stages), includes ablation studies, analyzes the FIR selection mechanism, and compares against human-crafted templates. The results consistently favor AUTO-RT, often by large margins (e.g., from single-digit ASR to ~50% on several models).
- **Ablation validates contributions.** Table 2 clearly shows that both DSP and PRT individually improve over the RL baseline, and their combination yields further gains, confirming that the two components are complementary and effective.

## Weaknesses
### Fatal
None.

### Major
- **No comparison against a non-strategic direct-optimization baseline.** The paper claims that strategy-level exploration is essential, but does not compare AUTO-RT against an RL baseline that optimizes attack queries directly *without* the strategy decomposition (i.e., Equation 1 with PPO over full queries). Such a comparison would directly test the value of the strategy-level formulation itself, rather than only the combined effect of DSP+PRT on top of the decomposition. Without this, the claim that "strategy-level prompt exploration is essential" is not fully supported.

- **Lack of theoretical grounding for PRT's reward shaping.** The paper acknowledges that PRT does not follow a potential-based shaping function (Ng et al., 1999), which typically preserves the optimal policy. The FIR-based selection mitigates this concern empirically, but there is no analysis or guarantee that the shaped reward does not introduce spurious optima or bias the learned policy away from the true objective. The theoretical justification is limited to a heuristic correlation between FIR spikes and good empirical performance.

- **Limited black-box evaluation.** Only two large black-box models (70B, 72B) are tested, and the absolute ASR values are low (14–15%) even though they beat baselines. The black-box setting uses ICL to obtain downgrade models, which may be less reliable than fine-tuning. The study would be stronger with more black-box models and an analysis of how the ICL-based downgrade affects FIR calculation and reward shaping quality.

### Minor
- "Up to 16.63% improvement" in the abstract is imprecise relative to which baseline and which model. The paper should be more explicit about the exact comparison (e.g., "over the best competing method on Gemma-2-2B"). The large gains on some models (e.g., Gemma-2-2B from 5.64% to 48.15%) are impressive and more informative.

- The definition of ASR_st (Equation 6) uses the top 100 strategies *with highest ASR on T_st*. Since T_st is the *test* set, this selection leaks test information when computing the final metric. Ideally, the top 100 should be selected based on a validation set or on T_trn only, and then evaluated on T_st. The paper should clarify whether this could overestimate the true attack effectiveness.

- In the human-based comparison (Table 3), AUTO-RT's ASR_st (38.38%) is lower than AutoDAN (55.23%) but DeD is much higher. The paper claims "near-human-level sustained attack capabilities," but the initial attack effectiveness is substantially lower. The comparison is fair but the phrasing downplays the gap.

### Trivial
- Some figure captions (e.g., Figure 1) contain repeated text from the main body, and the legend in Figure 1 uses symbols not all defined in the caption. The paper would benefit from self-contained figure captions.

## Nice-to-Haves
- A direct comparison against a non-strategic RL baseline (optimizing queries directly, without strategy decomposition) would strengthen the claim about the value of strategy-level exploration.
- An analysis of how the number of intermediate downgrade models (n) affects FIR reliability and downstream ASR would be useful for practitioners.
- The paper could discuss the cost of training downgrade models via toxic fine-tuning, and compare it to the cost of additional exploration in the baseline RL setting.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a baseline experiment that uses PPO to directly optimize attack queries (without the strategy/rephrase decomposition) under the same constraints (diversity, consistency) and the same number of episodes. This would isolate the benefit of the hierarchical formulation itself.
2. Clarify whether the top-100 strategies for ASR_st are selected based on T_st or on a separate validation set, and discuss any potential information leakage.
3. Expand the black-box evaluation to include a few more models (e.g., 7B/13B closed-source APIs if possible) to strengthen the generalizability claims.
4. Provide a brief theoretical or intuitive explanation of why the "first inverse rate" spike marks a good downgrade level, beyond the empirical observation.

## Score and Decision
Score: 8. The paper presents a novel and well-motivated framework, introduces two effective techniques, and supports them with extensive and convincing experiments across many models. The weaknesses (missing theoretical guarantee for PRT, lack of direct comparison against non-strategic optimization, limited black-box evaluation) are notable but do not invalidate the core contributions. The paper makes a clear advance over existing automated red-teaming approaches and is likely to be of high value to the safety community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>