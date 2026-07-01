## Summary

This paper proposes Steady Thought (ST), a thought-level preference optimization framework to mitigate the "under-thinking" phenomenon in Large Reasoning Models (LRMs), where models frequently abandon promising reasoning trajectories through excessive thought switching. The framework operates in three stages: (1) entropy-based thought segmentation, (2) thought completion via logit suppression of switch-indicating tokens, and (3) fine-grained preference optimization (STPO) that trains models to commit to promising thoughts. Experiments across multiple model sizes (1.5B-14B) and benchmarks show accuracy improvements of up to 5.3% with token reductions of 19.0-39.3%.

## Strengths

- **Novel problem formalization**: The paper provides a clean mathematical formulation of under-thinking as a preference optimization problem, distinguishing between commit trajectories and switch trajectories, which provides a principled foundation for the proposed method.
- **Well-designed framework**: The three-stage pipeline (segmentation, completion, preference optimization) is logically coherent and addresses the limitations of prior suppression-based approaches by preserving the model's ability to explore when necessary while encouraging commitment to promising thoughts.
- **Strong empirical results**: The method demonstrates consistent improvements across multiple model architectures (DeepSeek-R1-Distill-Qwen-1.5B/14B, Qwen3-8B) and diverse benchmarks including out-of-distribution generalization to code tasks (LiveCode), with both accuracy gains and substantial token reductions.
- **Comprehensive analysis**: The ablation studies on entropy thresholds, training methods, and the analysis of thought switching behavior (Table 2, Figure 2) provide strong evidence that ST genuinely modifies the model's reasoning patterns rather than simply memorizing shorter responses.

## Weaknesses

### Major

- **Limited baseline comparisons**: The paper compares against only three test-time efficiency methods (NoThink, NOWAIT, SEAL) and does not include other preference optimization approaches (e.g., DPO applied at the response level, or other step-level methods like Step-DPO). This makes it difficult to assess whether the thought-level granularity is the key innovation or if similar gains could be achieved with simpler approaches.
- **Potential data contamination concern**: The training data (omni-math) and evaluation datasets (MATH-500, AIME 2024, GSM8K) are all math benchmarks. While LiveCode serves as an OOD test, the paper does not discuss potential overlap between training and test sets, which is a known concern in the math reasoning literature.
- **Computational cost of thought completion stage**: The thought completion stage requires running the model multiple times per training example (once for each segmented thought) with logit suppression, which could be computationally expensive. The paper mentions this in Appendix E but does not provide quantitative analysis of the training overhead.

### Minor

- **Entropy threshold sensitivity**: The optimal entropy threshold (3.0) is determined through hyperparameter tuning, but the paper only shows results for one model on two datasets. The generalizability of this threshold across different model architectures and task types is unclear.
- **Limited analysis of failure cases**: The paper does not discuss scenarios where ST might hurt performance (e.g., problems that genuinely require multiple thought switches) or provide analysis of cases where accuracy decreased.

### Trivial

- The paper could benefit from more explicit discussion of how the thought completion stage handles cases where the segmented thought is inherently incorrect or insufficient to reach the correct answer.

## Nice-to-Haves

- Comparison with step-level preference optimization methods (e.g., Step-DPO, Process Reward Models) would strengthen the claim that thought-level optimization is the key innovation.
- Analysis of training data efficiency (how many training examples are needed) and the relationship between training data size and performance gains.
- Discussion of how the method might extend to non-math domains (e.g., scientific reasoning, multi-hop QA) where thought switching patterns may differ.

## Novel Insights

The paper's key insight is that under-thinking in LRMs can be addressed through fine-grained preference optimization at the thought level rather than through global suppression of switching behavior. The formalization of the problem as a preference between commit and switch trajectories, combined with the three-stage pipeline for constructing preference pairs, provides a principled approach that preserves model flexibility while encouraging deeper reasoning. The finding that ST leads to more rational switching (fewer invalid switches) and deeper exploration (higher proportion of last thought) offers a nuanced understanding of how to balance exploration and exploitation in reasoning models.

## Suggestions

- Include comparisons with response-level DPO/SimPO and step-level preference optimization methods to isolate the benefit of thought-level granularity.
- Provide quantitative analysis of the computational cost of the thought completion stage and discuss potential optimizations.
- Add analysis of cases where ST decreases accuracy to understand the method's limitations.

## Score and Decision

The paper presents a well-motivated, technically sound approach to an important problem (inefficient reasoning in LRMs) with strong empirical results across multiple models and benchmarks. The main limitations are the narrow set of baselines and potential computational overhead, but these do not invalidate the core contribution. The work is likely to be of significant interest to the ICLR community given the current focus on reasoning efficiency in large language models.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>