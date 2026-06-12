## Summary

This paper proposes Steady Thought (ST), a thought-level preference optimization framework to mitigate the "under-thinking" phenomenon in Large Reasoning Models (LRMs), where models excessively switch between reasoning trajectories and fail to commit to promising thoughts. ST operates in three stages: (1) segmenting model responses into thought sequences using entropy-based detection, (2) generating coherent completions of individual thoughts by suppressing switching tokens during decoding, and (3) performing fine-grained preference optimization (STPO) that treats the completed thought trajectory as preferred and the original switching trajectory as dispreferred. Experiments across multiple models (1.5B-14B) and datasets show ST reduces output length by up to 39.3% while improving accuracy by up to 5.3%, with strong generalization to out-of-distribution code tasks.

## Strengths

- **Novel problem formalization**: The paper formalizes under-thinking as a preference optimization problem at the thought level, providing a principled framework that goes beyond simple suppression of switching behavior. This is a meaningful conceptual contribution that reframes the issue from "how to suppress switching" to "how to learn when to commit vs. switch."

- **Well-designed three-stage pipeline**: The ST framework is logically structured—segmentation, completion, then preference optimization—with each stage addressing a specific subproblem. The entropy-based thought segmentation is particularly clever, using model uncertainty as a natural signal for thought boundaries.

- **Strong empirical results across multiple scales**: The method demonstrates consistent improvements across three model sizes (1.5B, 8B, 14B) and four datasets, including an out-of-distribution code benchmark (LiveCode). The accuracy improvements (up to 5.3%) combined with substantial token reductions (19-39%) represent a genuine Pareto improvement over baselines.

- **Thoughtful ablation studies**: The analysis of entropy thresholds (Section 4.4.3), comparison of training methods (Section 4.4.4), and metrics on thought switching behavior (Section 4.4.2) provide solid evidence for the design choices and validate that ST actually changes reasoning patterns rather than just memorizing shorter responses.

## Weaknesses

### Major

- **Limited comparison to state-of-the-art baselines**: The paper compares against NoThink, NOWAIT, and SEAL, but these are relatively simple or early methods. More recent and stronger approaches for controlling reasoning length/quality (e.g., L1-control from Aggarwal & Welleck 2025, which is cited but not compared against) should be included. The absence of comparison to methods that also use preference optimization for reasoning (e.g., step-level DPO variants) weakens the empirical contribution.

- **Potential data contamination concern**: The training data (omni-math) and evaluation datasets (MATH-500, AIME 2024, GSM8K) are all math benchmarks with significant topical overlap. While LiveCode serves as an OOD test, the paper would benefit from evaluation on non-math reasoning tasks (e.g., science QA, logical reasoning) to demonstrate broader applicability of the framework.

- **The thought completion stage relies on a heuristic (suppressing trigger words) that may be brittle**: The method pre-defines specific trigger words like "wait" and "alternatively" to suppress during decoding. This approach may not generalize well to models or domains where thought switching is signaled by different linguistic patterns. The paper does not analyze how sensitive results are to the choice of trigger words or whether this list is comprehensive.

### Minor

- **The entropy threshold analysis is limited to one model**: Table 3 only shows results for DeepSeek-R1-Distill-Qwen-1.5B. While the appendix is mentioned for more results, the main paper would benefit from showing threshold sensitivity for at least one additional model to demonstrate robustness.

- **The "proportion of correct thoughts" metric (PCT) in Table 2 requires more careful interpretation**: A lower PCT after ST could also indicate that the model is prematurely committing to incorrect thoughts (i.e., it's switching less but not necessarily more wisely). The paper should discuss this alternative interpretation and provide evidence that the reduced switching is indeed beneficial.

- **The paper claims ST "preserves the ability to explore necessary alternatives" but doesn't directly test this**: The analysis focuses on showing reduced switching, but there's no experiment demonstrating that ST-trained models can still effectively switch when the current thought is unpromising. This is a key claimed advantage over suppression-based methods.

### Trivial

- The table header in Table 1 uses "↓" arrows for both accuracy (where higher is better) and tokens (where lower is better), which is slightly confusing.

## Nice-to-Haves

- An analysis of which types of problems benefit most from ST (e.g., by difficulty level or mathematical domain) would help practitioners understand when to apply this method.
- A comparison of computational cost between ST training and the inference-time savings would strengthen the practical motivation.
- Visualizing the entropy dynamics during reasoning (e.g., a sample response with entropy plotted over tokens) would make the segmentation method more intuitive.

## Novel Insights

The key insight is that under-thinking can be addressed not by globally suppressing switching behavior (which risks discarding useful exploration), but by teaching models a more nuanced policy: commit to promising thoughts while preserving the ability to explore when needed. The thought-level preference optimization framework operationalizes this by creating training pairs that isolate the decision point (whether to continue or switch) from the rest of the reasoning process. This is conceptually cleaner than token-level or representation-level interventions and provides a natural way to balance exploration and exploitation in reasoning. The finding that this approach generalizes to code tasks despite being trained only on math data suggests the method teaches a generalizable reasoning discipline rather than domain-specific patterns.

## Suggestions

- Add comparisons to at least one more recent method for controlling reasoning length (e.g., L1-control or other RL-based approaches) to strengthen the empirical evaluation.
- Include an experiment that explicitly tests whether ST-trained models can still switch effectively when the current thought is incorrect (e.g., by analyzing cases where the first thought is wrong and the model needs to switch).
- Provide a more detailed analysis of the trigger word list—either show that the results are robust to different word choices or provide a principled way to identify switching signals.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>