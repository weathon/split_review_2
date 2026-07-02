## Summary

This paper introduces LLM4GCL, the first comprehensive benchmark for evaluating Large Language Models (LLMs) and Graph-enhanced LLMs (GLMs) on Graph Continual Learning (GCL) tasks. The authors identify a critical flaw in existing GCL evaluation setups—task ID leakage in local testing—and propose a more realistic global testing protocol. They systematically evaluate 9 methods across 7 text-attributed graph datasets and propose SimGCL, a simple method combining graph-prompted instruction tuning with training-free prototype classification that significantly outperforms existing GNN-based and LLM-based baselines.

## Strengths

- **Important problem identification**: The paper convincingly demonstrates that the prevalent local testing setup in GCL suffers from task ID leakage, which fundamentally undermines the validity of prior evaluations. The simple experiment showing that mean pooling achieves 100% task ID prediction accuracy and zero forgetting is a strong empirical demonstration of this flaw.

- **Comprehensive and systematic benchmark**: The paper evaluates 9 methods (GNN-based, LLM-based, and GLM-based) across 7 diverse text-attributed graph datasets spanning multiple domains, scales, and densities. This provides a valuable resource for the community and establishes a standardized evaluation protocol.

- **Strong empirical results**: SimGCL achieves substantial improvements over existing methods, with up to ~20% absolute improvement over the previous SOTA on certain datasets. The ablation studies and analysis of scaling behavior (Figure 3) and session configurations (Table 4) provide useful insights into when and why the method works.

- **Clear and actionable insights**: The paper distills several key observations (Obs. 1-8) that provide practical guidance for future research, such as the limitations of GNN-based methods, the superiority of prototype-based approaches, and the challenges faced by current GLMs in continual learning settings.

## Weaknesses

### Major

- **Limited novelty of SimGCL**: The proposed method combines two well-established techniques—LoRA fine-tuning with instruction tuning and training-free prototype classification. While the combination is sensible and effective, the individual components are not novel. The paper would benefit from a clearer articulation of what specific design choices are critical and why, beyond the straightforward combination.

- **Incomplete analysis of the task ID leakage issue**: While the paper correctly identifies the flaw in local testing, it does not fully explore the implications. The claim that "even using a basic mean pooling operation to get prototypes achieves flawless task ID prediction" is demonstrated only on the specific datasets and settings used. A more rigorous analysis of when and why task ID leakage occurs, and whether there are scenarios where local testing might still be informative, would strengthen the contribution.

- **Limited evaluation of SimGCL's limitations**: The paper notes that SimGCL underperforms on Arxiv-23 and in FSNCIL settings, attributing this to sparse graph structure and overfitting to the initial session. However, the analysis is superficial. The paper does not investigate whether alternative prompt designs, different LoRA configurations, or other prototype aggregation strategies could mitigate these issues. This limits the practical guidance for future work.

- **Missing statistical significance and variance reporting**: The results in Tables 2, 3, and 4 are reported as single numbers without standard deviations or confidence intervals. Given the stochastic nature of LLM fine-tuning and the variability in continual learning evaluations, this is a significant omission that makes it difficult to assess the reliability of the reported improvements.

### Minor

- **The paper claims "first comprehensive benchmark" but does not fully justify the comprehensiveness**: While 9 methods and 7 datasets are reasonable, the paper does not discuss why these specific methods and datasets were chosen over others, nor does it provide a systematic analysis of coverage (e.g., different types of graph structures, different LLM architectures, different continual learning strategies).

- **The paper's observations are somewhat redundant**: Observations 1-8, while useful, often restate what is already visible in the tables. For example, Obs. 1 ("GNN-based methods exhibit persistent limitations") and Obs. 2 ("LLMs demonstrate higher performance") are directly evident from the numbers. The paper could be more concise.

### Trivial

- The paper uses inconsistent notation for metrics (e.g., $\bar{\mathcal{A}}$ vs $\bar{A}$, $\mathcal{A}_N$ vs $A_N$) across tables and text.

## Nice-to-Haves

- An analysis of the computational cost (training time, inference time, memory) of SimGCL compared to baselines would be valuable for practitioners.
- A discussion of the sensitivity of SimGCL to the choice of LLM backbone (beyond scaling) and to the prompt template design would strengthen the practical guidance.
- An investigation into whether the task ID leakage issue also affects other GCL settings (e.g., graph-level tasks, link prediction) would broaden the impact.

## Novel Insights

None beyond the paper's own contributions. The key insight—that local testing in GCL suffers from task ID leakage—is well-demonstrated but is a critique of existing practice rather than a novel theoretical or methodological contribution. The finding that prototype-based methods (Cosine, SimpleCIL, SimGCL) are particularly effective for GCL is consistent with prior work in other continual learning domains and is not surprising.

## Suggestions

- Report results with standard deviations or confidence intervals across multiple runs to establish statistical significance.
- Provide a more detailed analysis of when and why SimGCL fails (e.g., on Arxiv-23), including ablation studies on prompt design, LoRA rank, and prototype aggregation strategy.
- Clarify the novelty of SimGCL relative to existing prototype-based continual learning methods (e.g., SimpleCIL) and explicitly state what new design choices are introduced.

## Score and Decision

The paper makes a valuable contribution by identifying a critical flaw in existing GCL evaluation protocols and providing a comprehensive benchmark. The empirical results are strong and the proposed SimGCL method is effective. However, the methodological novelty is limited, the analysis of the task ID leakage issue is incomplete, and the lack of statistical significance reporting weakens the reliability of the claims. The paper is a solid contribution to the GCL community but does not rise to the level of a top-tier ICLR paper.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>