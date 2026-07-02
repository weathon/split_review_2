## Summary

This paper introduces CrowdFM, a foundation model for crowdsourced label aggregation that uses a bipartite graph neural network pretrained on domain-randomized synthetic data. The model achieves cross-dataset generalization without requiring dataset-specific retraining, and experiments on 22 real-world benchmarks show it matches or surpasses bespoke methods in accuracy while being more efficient. Additionally, the learned representations support downstream tasks like worker assessment and task assignment.

## Strengths

- **Novel and well-motivated problem framing**: The paper clearly identifies the gap between dataset-specific methods (accurate but non-scalable) and majority voting (scalable but suboptimal), and proposes a foundation model approach that combines the advantages of both. This is a genuinely important direction for the crowdsourcing community.

- **Comprehensive experimental evaluation**: The paper evaluates on 22 real-world datasets, compares against 12 baselines including both traditional probabilistic methods and modern deep learning approaches, and provides statistical significance tests (Wilcoxon signed-ranks test). The downstream task experiments (worker assessment, task assignment) further demonstrate the model's versatility.

- **Thoughtful architectural design**: The size-invariant initialization (shared learnable vectors for workers/tasks) is a clever solution to the variable-size problem across datasets. The attention-based message passing over worker-task-option triples is well-motivated for capturing annotation heterogeneity.

- **Strong empirical results**: CrowdFM achieves 83.41% average accuracy, competitive with the best dataset-specific methods (EBCC at 84.08%) while being significantly faster (0.53s vs 2.95s) and requiring no per-dataset training. The model outperforms MV on 21/22 datasets with an average improvement of +1.64%.

## Weaknesses

### Fatal
None.

### Major

- **Limited comparison with state-of-the-art methods**: The paper compares against several baselines but notably omits recent deep learning methods like CoNAL (Chu et al., 2021), Max-MIG (Cao et al., 2019), and other modern label aggregation approaches from the last 3-4 years. The most recent deep learning baseline (GOVERN, 2024) is included, but the field has seen several important developments. This weakens the claim of "matching or surpassing state-of-the-art."

- **The synthetic data generator's realism is not rigorously validated**: While Appendix F provides some quantitative comparison between synthetic and real datasets, the analysis is superficial. The paper claims the generator "faithfully reflect real-world crowdsourcing patterns" but only shows that synthetic data has similar accuracy ranges to real data. A proper validation would require demonstrating that the synthetic data captures the same statistical properties (e.g., worker confusion matrices, label distributions, inter-annotator agreement patterns) as real crowdsourcing data. The 3PL model, while standard in psychometrics, may not capture the full complexity of real annotation behavior (e.g., systematic biases, spamming, cultural differences).

- **The "foundation model" claim is overstated**: The paper uses the term "foundation model" but CrowdFM is pretrained only on synthetic crowdsourcing data and evaluated only on label aggregation tasks. True foundation models (like LLMs) demonstrate broad capabilities across diverse, unrelated tasks. The downstream adaptations shown (worker assessment, task assignment) are closely related to the primary task and use the same encoder. The paper does not demonstrate generalization to fundamentally different tasks (e.g., different annotation types, different domains with different noise structures).

### Minor

- **The ablation study is limited**: Only two architectural components are ablated (attention mechanism and synthetic data generator). The paper does not ablate other important design choices such as: the 3PL model vs simpler noise models, the size-invariant initialization vs alternative approaches, or the attention mechanism design choices (e.g., number of heads, different aggregation functions).

- **Runtime comparison is incomplete**: The paper reports average runtime but does not account for the significant pretraining cost of CrowdFM. While inference is fast, the total cost including pretraining should be acknowledged. Additionally, the runtime comparison with dataset-specific methods is somewhat unfair since those methods include training time while CrowdFM's pretraining time is excluded.

- **The performance on Senti dataset**: CrowdFM underperforms MV on Senti by 0.08%. The paper attributes this to domain shift but does not analyze why the model fails on this particular dataset. Understanding failure cases would strengthen the paper.

### Trivial
- The paper mentions "Codes are available at" but the URL is missing.
- Figure 2 has a table below the figure that appears to be a duplicate of the figure data, which is redundant.

## Nice-to-Haves

- A more thorough analysis of when CrowdFM fails (e.g., which datasets or conditions lead to poor performance) would be valuable for practitioners.
- The paper could benefit from a discussion of the model's limitations in terms of the types of crowdsourcing tasks it can handle (e.g., only classification, not ranking or structured outputs).
- An analysis of the computational cost of pretraining (GPU hours, data size) would help readers assess the practical feasibility.

## Novel Insights

The paper's key insight is that a GNN with size-invariant initialization can learn universal aggregation principles from synthetic data that transfer to real crowdsourcing datasets. This is a significant departure from the traditional dataset-specific paradigm and opens up the possibility of truly scalable, retraining-free label aggregation. The finding that attention-based message passing over worker-task-option triples can capture annotation heterogeneity without dataset-specific features is particularly noteworthy. However, the insight is somewhat limited by the narrow scope of the synthetic data generator and the lack of rigorous validation of its realism.

## Suggestions

1. Add comparisons with more recent deep learning methods for label aggregation (e.g., CoNAL, Max-MIG, or other post-2020 approaches) to strengthen the claim of state-of-the-art performance.
2. Provide a more rigorous validation of the synthetic data generator by comparing statistical properties (e.g., worker confusion matrices, label entropy, inter-annotator agreement) between synthetic and real datasets.
3. Include an analysis of the pretraining cost (GPU hours, data size) and discuss the total cost of deploying CrowdFM vs dataset-specific methods.
4. Add an ablation study on the 3PL model vs simpler noise models to justify this design choice.
5. Analyze the failure case on the Senti dataset to understand when the model struggles.

## Score and Decision

The paper addresses an important and well-motivated problem, proposes a novel approach with thoughtful architectural design, and provides comprehensive empirical evaluation. The main weaknesses are the limited comparison with recent methods, the lack of rigorous validation of the synthetic data generator, and the somewhat overstated "foundation model" claim. However, these issues do not invalidate the core contribution, which is a significant step toward scalable, transferable label aggregation. The paper is technically sound and the results are convincing.

Score: 7

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>