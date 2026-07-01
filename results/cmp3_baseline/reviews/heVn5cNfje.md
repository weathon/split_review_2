## Summary

This paper introduces High-Entropy Sum (HES), a training-free metric for data selection in LLM reasoning training. HES sums the entropy of only the top 0.5% highest-entropy tokens in each reasoning sample, focusing on critical "forking points" to better capture reasoning quality. The authors validate HES across SFT, RFT, and RL training paradigms, showing that training on top-HES-ranked data matches or exceeds full-dataset performance while using only a fraction of the data, and that HES-based selection outperforms existing training-free metrics like average entropy, length, and difficulty.

## Strengths

- **Simple yet effective metric**: HES is elegantly simple—summing entropy of only the top 0.5% highest-entropy tokens—and the intuition that critical reasoning decisions occur at high-entropy "forking points" is well-motivated and grounded in prior work (Wang et al., 2025). The metric requires no additional model training or external reward models.

- **Comprehensive empirical validation across three paradigms**: The paper evaluates HES across SFT, RFT, and RL, which is rare and demonstrates the metric's generality. The experiments are extensive, covering multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B, Qwen3-0.6B), multiple datasets (Open-Math-Reasoning, Open-R1-220k, DeepScaleR), and multiple domains (math, code, STEM). The consistent improvements across all settings are compelling.

- **Strong results with practical implications**: Training on just the top 20% of HES-ranked data matching full-dataset performance, and pruning the bottom 20% to surpass full-dataset performance, has direct practical value for reducing training costs. The small-to-large model transfer result (using Qwen3-0.6B to screen data for Qwen3-8B) is particularly impactful for practitioners.

- **Well-designed ablation studies**: The paper systematically compares HES against multiple baselines (random, length, difficulty, average entropy, entropy sum, average high-entropy entropy, absolute threshold HES) and includes careful controls like Lowest-HES to validate that the metric captures quality rather than some confound.

## Weaknesses

### Fatal
None.

### Major

- **Limited novelty relative to existing work**: The core idea—that high-entropy tokens in reasoning paths are critical and that summing their entropy correlates with reasoning quality—is directly inspired by Wang et al. (2025), who already identified "forking tokens" as key drivers of performance improvement. The paper's main contribution is operationalizing this insight into a data selection metric, but the conceptual advance is incremental. The paper would benefit from a clearer articulation of what is novel beyond the forking-token observation.

- **The 0.5% threshold appears arbitrary and insufficiently justified**: The paper uses the top 0.5% of highest-entropy tokens throughout, but the sensitivity analysis (Figures 3 and 4) only compares 0.005, 0.05, 0.5, and 1.0 ratios. The choice of 0.5% (0.005) is not derived from any principled criterion, and the analysis shows that 0.005 and 0.05 perform similarly in many cases. A more rigorous justification or a data-driven method for selecting this threshold would strengthen the paper.

- **The RL experiments use a very small model (1.5B) and show modest absolute gains**: The RL results in Table 6 show that Pos-High, Neg-Rand achieves 21.30% average accuracy versus 20.63% for Full-Batch—a gain of 0.67 percentage points. While the relative improvement is notable, the absolute performance is low, and it's unclear whether these findings would scale to larger models (e.g., 7B or 70B) where RL is typically applied. The paper should acknowledge this limitation more explicitly.

- **Missing analysis of computational cost**: The paper claims HES is "training-free" and "efficient," but computing token-level entropy requires a forward pass through the model for each candidate response. For large candidate pools (e.g., 32 rollouts per query in RL), this adds non-trivial inference cost. The paper should provide a quantitative comparison of the computational overhead of HES versus alternative methods (e.g., training a small reward model, using an external LLM for scoring).

### Minor

- **The RFT results show modest improvements over random baselines**: In Table 5, the average gain of Highest-HES over Random in per-query selection is only about 1-1.7 percentage points. While consistent, the practical significance of these gains is debatable, especially given the additional computation required to compute HES for all candidates.

- **The paper does not compare against learned reward models or process reward models**: Given that the paper claims HES can serve as a "training-free reward signal," it would be informative to compare HES-based selection against simple learned reward models (e.g., a small classifier trained on correctness) to understand the trade-offs.

- **The "Forking-Only" baseline in SFT (Table 1) is not clearly explained**: The paper states this method applies "gradient updates only to the high-entropy tokens" but does not specify how this is implemented or why it achieves 32.51% average (comparable to full-dataset). This result seems interesting but is not discussed.

### Trivial
None.

## Nice-to-Haves

- An analysis of what types of reasoning problems or response characteristics lead to high vs. low HES scores, to build intuition about what the metric captures.
- A comparison against data selection methods based on model confidence or prediction margin, which are also training-free and capture uncertainty.
- An investigation of whether HES correlates with human judgments of reasoning quality.

## Novel Insights

None beyond the paper's own contributions. The paper's main insight—that summing entropy of only the highest-entropy tokens provides a better signal for reasoning quality than averaging over all tokens—is a useful operationalization of the forking-token concept, but it does not introduce a fundamentally new understanding of reasoning or data selection.

## Suggestions

- Provide a more principled justification for the 0.5% threshold, perhaps by analyzing the distribution of token entropies across different models and tasks and showing that the optimal threshold is stable.
- Include a computational cost comparison (e.g., FLOPs or wall-clock time) for computing HES versus alternative selection methods, to substantiate the claim of efficiency.
- Add experiments with larger models (e.g., 7B or 14B) in the RL setting to demonstrate scalability.
- Discuss the limitations of HES more explicitly: it requires access to the model's token-level probability distribution, which may not be available for API-only models, and it may not generalize to tasks where reasoning quality is not well-captured by token-level uncertainty.

## Score and Decision

The paper presents a simple, well-motivated, and empirically validated metric for data selection in LLM reasoning training. The experiments are comprehensive across three training paradigms, multiple models, and multiple domains, and the results consistently support the effectiveness of HES. However, the conceptual novelty is limited given the direct inspiration from prior work on forking tokens, and the 0.5% threshold lacks principled justification. The practical impact is real but incremental. The paper is a solid contribution that would benefit the community, but it does not represent a breakthrough.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>