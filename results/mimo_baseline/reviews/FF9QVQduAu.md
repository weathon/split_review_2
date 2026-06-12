## Summary

This paper introduces CrowdFM, a foundation model for crowdsourced label aggregation based on a bipartite graph neural network pre-trained on domain-randomized synthetic data generated via a 3PL Item Response Theory model. The model uses size-invariant initialization and attention-based message passing to learn transferable aggregation patterns, enabling zero-shot deployment on unseen real-world datasets. Experiments on 22 real-world benchmarks show CrowdFM is competitive with dataset-specific methods while requiring no per-dataset retraining, and demonstrates versatility through downstream tasks like worker assessment and task assignment.

## Strengths

- **Well-motivated and practically valuable problem**: The paper clearly identifies the tension between Majority Voting (scalable but inaccurate) and dataset-specific methods (accurate but non-transferable), and proposes a compelling solution. The foundation model framing for crowdsourcing is timely and addresses a genuine gap in the literature.

- **Comprehensive evaluation across 22 real-world datasets**: The breadth of evaluation is impressive. CrowdFM outperforms MV on 21/22 datasets (avg. +1.64%) and achieves competitive accuracy against 12 dataset-specific baselines, with runtime (0.53s) comparable to lightweight methods. The Wilcoxon signed-ranks test properly contextualizes statistical significance.

- **Thoughtful synthetic data generation**: The domain-randomized generator using the 3PL model is well-designed, capturing behavioral heterogeneity (worker ability, task difficulty, discrimination, guessing rates), long-tailed participation patterns, and diverse global structures. The ablation (w/o SG in Figure 6a) clearly validates its importance over uniform random generation.

- **Versatile downstream applications**: The demonstrations of worker/task assessment (Figures 3-4 with strong correlations) and intelligent task assignment (Figure 5) effectively argue that CrowdFM learns meaningful, transferable representations beyond label aggregation, strengthening the foundation model narrative.

- **Practical efficiency**: CrowdFM's zero-shot inference at 0.53s per dataset is significantly faster than deep learning baselines (LAA: 223s, GOVERN: 95s, TiReMGE: 27s) and comparable to simple methods like PM (0.47s), making it deployment-friendly.

## Weaknesses

### Fatal
None.

### Major

- **Performance claims are overstated relative to evidence**: The abstract claims CrowdFM "consistently matches or surpasses bespoke, per-dataset methods," but Table 1 shows CrowdFM's average accuracy (83.41%) is lower than EBCC (84.08%) and only marginally above BWA (83.31%). Crucially, CrowdFM is NOT significantly better than EBCC (p=0.90), BWA (p=0.61), DS (p=0.32), IBCC (p=0.37), or GOVERN (p=0.29). The paper's core narrative of superiority is not supported by its own statistical tests. The honest framing should emphasize the zero-shot capability and efficiency advantage while acknowledging competitive (but not superior) accuracy.

- **Missing pretraining details**: For a paper proposing a "foundation model," the pretraining cost is conspicuously absent from the main text. Key questions remain unanswered: How many synthetic datasets were generated during training? What is the total pretraining compute (GPU hours)? How many training steps? What are the full hyperparameter ranges for the synthetic generator? These details are critical for reproducibility and for assessing the practical viability of the foundation model approach.

### Minor

- **Baseline fairness concerns**: LAA and GOVERN failed on several large datasets due to memory issues (noted in Table 1 caption). Their average accuracy and runtime are computed only over "successfully completed runs," which may bias comparisons if the failed datasets are systematically different. A more informative comparison would report per-dataset results more prominently or note which datasets each method failed on.

- **Limited diversity of downstream evaluations**: Worker/task assessment and task assignment are demonstrated primarily on synthetic data or a single real-world dataset (Web). Stronger evidence would include evaluation across multiple real-world datasets with different characteristics to establish robust generalization.

- **3PL model as potential bottleneck**: The synthetic data is generated exclusively via the 3PL model from IRT. If real crowdsourcing data exhibits fundamentally different noise patterns (e.g., adversarial spam, cultural biases, task-specific confusions), the model may be biased toward 3PL-consistent patterns. While Appendix F apparently analyzes this, the paper could benefit from a brief discussion of when 3PL-based pretraining might fail.

### Trivial

- The comparison with HyperLM is somewhat straw-man: HyperLM was designed for programmatic weak supervision (Wu et al., 2023b), not crowdsourced annotation with human workers. Including it is appropriate, but the extended critique (Section 4.2) may give readers an inflated sense of its relevance as a baseline.

## Nice-to-Haves

- A table summarizing pretraining compute, number of synthetic datasets used, and wall-clock training time would significantly strengthen the foundation model contribution.
- Analysis of failure cases: on which datasets does CrowdFM underperform, and what characteristics of those datasets might explain the failure?
- Comparison with LLM-based approaches for label aggregation (briefly mentioned in Section 5 but only deferred to Appendix I).

## Novel Insights

The paper's genuinely novel contribution is demonstrating that the "pretrain on synthetic data, deploy zero-shot" paradigm—well-established in vision and language—can be successfully adapted to crowdsourced label aggregation through careful domain randomization with psychometric models (3PL). The key insight is that crowdsourcing behavioral patterns are sufficiently regular that a model pre-trained on diverse synthetic scenarios can transfer to real-world settings, challenging the long-held assumption that dataset-specific parameter estimation is necessary. The size-invariant initialization strategy is a practical architectural insight enabling this transfer across datasets of varying scales.

## Suggestions

- Revise the abstract and key claims to accurately reflect that CrowdFM is competitive with dataset-specific methods while offering the significant practical advantage of zero-shot deployment, rather than claiming to surpass them.
- Add a dedicated section or table with pretraining details (compute cost, generator parameter ranges, number of synthetic datasets seen during training).
- Include a qualitative analysis of the attention weights or learned embeddings to provide interpretability insights—this would strengthen both the paper and the downstream application claims.

## Score and Decision

The paper presents a well-motivated approach to a practical problem, with thorough experiments across 22 datasets and compelling downstream demonstrations. The zero-shot capability with competitive accuracy and strong efficiency is a genuine contribution. However, the core claims of surpassing dataset-specific methods are not supported by the paper's own statistical analysis, and critical pretraining details are missing from the main text. These overclaims undermine trust in an otherwise solid empirical contribution. The work is borderline: the idea is good, execution is mostly sound, but the paper needs more honest framing and technical details to be fully convincing.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept