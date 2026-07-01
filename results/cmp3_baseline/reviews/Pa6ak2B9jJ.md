## Summary

The paper introduces AUTO-RT, a reinforcement learning framework for automatic jailbreak strategy exploration in large language models. It formulates attack strategy generation as a sequential decision process and proposes two key techniques—Dynamic Strategy Pruning (DSP) and Progressive Reward Tracking (PRT) with a First Inverse Rate (FIR) metric—to improve exploration efficiency and attack effectiveness. Experiments across 16 white-box and 2 black-box LLMs demonstrate improved attack success rates, diversity, and efficiency over several baselines.

## Strengths

- **Novel problem formulation.** The paper reframes automatic red-teaming as strategy-level exploration rather than prompt-level optimization, enabling discovery of attacks that are both highly exploitable and severe. This is a meaningful departure from existing template-based or fixed-policy approaches.
- **Well-motivated techniques.** Both DSP and PRT directly address identified challenges (overwhelming safe signals and sparse rewards) in a principled manner. The FIR metric provides a practical method for selecting an informative downgrade model without requiring extensive calibration.
- **Extensive and systematic evaluation.** Experiments cover a wide variety of model families (Llama, Mistral, Yi, Gemma, Qwen, etc.) in both white-box and black-box settings. The ablation study cleanly isolates the contributions of each component, and the diversity metrics (SeD and DeD) go beyond standard ASR.
- **Significant empirical gains.** AUTO-RT consistently outperforms all baselines in effectiveness, diversity, and sustained attack capability. On several models the improvements are large (e.g., Vicuna-7B from 31.95% RL to 56.40% ASR, Gemma-2-2B from 6.15% to 48.15%).

## Weaknesses

### Fatal

None.

### Major

1. **Limited baseline comparison.** The main experimental comparison (Table 1) includes only simple baselines (FS, IL, RL). Stronger existing methods like AutoDAN-turbo, PAIR, or TAP are acknowledged in the text but not directly compared in the main table. The separate comparison with human-crafted templates (Table 3) is averaged across models and lacks per-model detail, making it difficult to assess relative strengths.
2. **Computational cost not reported.** The paper uses 8×A100 clusters for PPO training and 9,000 episodes, but provides no runtime or cost comparison with baselines. Without such analysis, it is unclear whether the improvements come at a prohibitive computational overhead that could limit practical adoption.
3. **Questionable theoretical grounding for DSP.** The paper cites Sun et al. (2021) for the guarantee that early-terminated CMDPs preserve optimal policies with sufficiently small penalties, but applies this to diversity and consistency constraints that are not formally defined as constraint functions. The validity of this guarantee in the proposed setting is not established.

### Minor

1. **Dependence on downgrade model quality.** The PRT method requires constructing a series of downgrade models (M1–M6) and selecting one based on FIR patterns. While FIR is clever, the choice of what constitutes a “sharp increase” is described heuristically. The robustness of the method to different model families or data distributions is not explored.
2. **Black-box results are preliminary.** The black-box setting uses in-context learning to produce downgrade models. The achieved ASR (~14-15%) is notably lower than white-box results, and only two models of similar scale are tested. More diverse black-box scenarios (e.g., API-based LLMs with different safety postures) would strengthen the claim of generality.
3. **Safety evaluator reliability.** The paper relies solely on Llama-Guard2-8B for safety evaluation. The sensitivity and specificity of this classifier are not analyzed, and errors could bias ASR comparisons, especially for models with different safety distributions.

### Trivial

- The reward shaping formulation in Equation 4 uses integer values 0/1/2; the exact relationship to the original reward is not discussed in terms of potential bias or sensitivity.

## Nice-to-Haves

- A direct comparison with a state-of-the-art method like AutoDAN-turbo under the same evaluation budget would greatly strengthen the paper.
- An analysis of the computational overhead (e.g., wall-clock time, number of API calls) for each method would help practitioners assess trade-offs.
- A discussion of potential failure modes of the consistency judge (e.g., adversarial rephrasings that preserve meaning but are flagged as inconsistent) would improve the robustness analysis.

## Novel Insights

Beyond the paper’s own contributions, the idea of using a *weakened* reference model to provide denser reward signals in red-teaming is conceptually interesting and could apply to other adversarial training or safety evaluation settings. The FIR metric, which identifies the point at which safety alignment begins to degrade inconsistently, offers a principled way to calibrate such aids without exhaustive search.

## Suggestions

- Include a comparison with at least one strong black-box attack method (e.g., PAIR or TAP) to contextualize the effectiveness claims.
- Add a table or figure reporting the total number of target model queries and training time for each method.
- Conduct a sensitivity analysis of the FIR threshold to show that performance is robust to small variations in the definition of “sharp increase.”

## Score and Decision

Score: 7.0  
Decision: Accept

MY FINAL SCORE: <score>7.0</score>  
MY FINAL DECISION: <decision>Accept</decision>