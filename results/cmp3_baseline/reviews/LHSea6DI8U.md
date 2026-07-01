## Summary

The paper proposes STBP, a framework for continual spatio-temporal forecasting that combines a frozen general-purpose backbone (with frequency-domain processing and dual-stream linear graph attention) with an expandable contextual pattern bank. The backbone captures stable spatio-temporal patterns, while the pattern bank incrementally expands to adapt to new nodes and distribution shifts, mitigating catastrophic forgetting. Experiments on three real-world datasets show significant improvements over state-of-the-art baselines, including both standard STGNNs and dedicated continual forecasting methods.

## Strengths

- **Well-motivated and relevant problem.** Continual spatio-temporal forecasting under evolving graph structures and distribution shifts is an important and timely challenge for real-world smart city applications. The paper clearly identifies the limitations of existing static-graph STGNNs and the weaknesses of current CSTF methods.

- **Strong empirical performance.** STBP achieves substantial improvements over the best baselines: 21.44% and 21.93% average MAE reduction on PEMS-Stream and CA-Stream, and consistent gains on AIR-Stream. The few-shot forecasting results (Table 2) are particularly impressive, demonstrating robust knowledge transfer under low-resource conditions.

- **Principled design for continual learning.** The separation of a frozen backbone (retains general knowledge) and an expanding pattern bank (handles node-specific adaptation) is a clean and effective strategy. The prompt-based gating and attention mechanisms provide a well-integrated way to inject pattern bank information into the backbone.

- **Thorough experimental evaluation.** The paper provides comprehensive results: main comparisons, ablation studies, parameter sensitivity, case studies with t-SNE visualization, real forecast visualizations, and efficiency analysis. The ablation variants clearly isolate the contributions of each component.

- **Efficient architecture.** The frequency-domain network and linear attention reduce computational complexity to O(N), making the method scalable to large graphs. The efficiency study (Figure 8) confirms that STBP maintains competitive training time and memory while delivering significantly better accuracy.

## Weaknesses

### Major

1. **Incremental novelty of individual components.** Frequency-domain processing for temporal modeling and linear attention for spatial modeling have been explored in prior STGNN work (e.g., ST-Norm, FEDFormer, Katharopoulos et al.). The contextual pattern bank with prompt-based guidance is reminiscent of prompt-tuning approaches in continual learning for vision/language (e.g., L2P, DualPrompt). The paper's main contribution is the specific integration of these components for CSTF, but the novelty is somewhat incremental rather than foundational.

2. **Limited domain diversity in experiments.** All three datasets are from traffic and meteorology. While the results are strong, claims about the framework being a "general spatio-temporal backbone" would be strengthened by evaluation on additional domains such as energy, social networks, or mobility. The paper would benefit from at least one dataset outside the traffic/air quality domain.

3. **Comparison to conventional methods may be unfair.** GWNet, STID, and iTransformer are adapted to continual learning via retraining or online fine-tuning, but these adaptations may not be optimal. For example, applying elastic weight consolidation (EWC) or other regularization to STID would be a more rigorous baseline. However, the comparison to existing CSTF methods is fair and shows clear advantage.

### Minor

1. **Memory consumption of pattern bank.** The pattern bank stores N×d parameters per time step and grows linearly with the node set. While the efficiency study shows linear overhead, the paper does not discuss strategies for compressing or pruning the pattern bank for extremely large graphs (e.g., >100k nodes). This could be a practical limitation.

2. **Hyperparameter sensitivity limited to channel dimension.** Only the feature dimension d is tested (Figure 5). Other important hyperparameters (e.g., number of pattern bank groups, learning rate schedule, expansion vs. consolidation trade-off) are not analyzed.

3. **Privacy/storage claims not validated.** The paper states that the pattern bank stores "high-level abstractions" offering advantages in privacy and storage efficiency, but no experiment or analysis supports this claim. Without evidence, this remains a speculative advantage.

4. **Single-task setting.** The conclusion acknowledges that the method currently supports continual learning in a single-task setting, and the paper focuses on single-task (node expansion within the same domain). The cross-domain setting is left for future work, which limits the scope of the claimed "general" backbone.

### Trivial

- Table 1 formatting has some apparent misalignments (likely parser artifacts, not a paper flaw).  
- Figure labels could be clearer (e.g., "Toy dataset" in Figure 8 is not defined in the main text).

## Nice-to-Haves

- Ablation on the number of pattern bank groups (three groups used) or the effect of each group (P^{(0)}, P^{(1)}, P^{(2)}).
- Comparison with replay-based continual learning methods that store raw samples, to empirically support the storage efficiency claim.
- Analysis of how the pattern bank handles node deletion or edge rewiring (not just expansion).
- Code release to facilitate reproducibility.

## Novel Insights

Beyond the paper's own contributions, the key insight is that for continual spatio-temporal forecasting, a frozen general backbone combined with an expandable, node-specific pattern bank provides a natural separation of stable knowledge (periodic patterns, long-range correlations) and adaptable knowledge (node-level heterogeneity, emerging behaviors). The t-SNE visualization (Figure 6) empirically shows that the pattern bank autonomously clusters nodes with similar temporal dynamics without explicit clustering supervision, suggesting that the prompt-based interaction with the backbone inherently discovers functional groupings in the data. This observation could inspire simpler methods for handling distribution shift in streaming graphs.

## Suggestions

- Add at least one dataset from a non-traffic/air-quality domain (e.g., energy consumption, human mobility) to strengthen the claim of generality.
- Include an analysis of pattern bank memory vs. predictive performance trade-off, or discuss potential compression strategies (e.g., low-rank approximation).
- Acknowledge the similarity to existing prompt-based continual learning work and clearly differentiate the contributions for the spatio-temporal domain.

## Score and Decision

The paper tackles an important problem with a well-designed and empirically validated solution. The improvements over baselines are substantial and consistent. The weaknesses are about the depth of novelty and scope of experiments rather than any fatal flaw. For ICLR, the practical significance and soundness of the method make it a strong candidate for acceptance.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>