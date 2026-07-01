## Summary

This paper identifies and formalizes a new problem in multi-modal entity alignment (MMEA) called Dual-level Noisy Correspondence (DNC), where both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences can be noisy. The authors propose RULE, a framework that estimates correspondence reliability via uncertainty and consensus principles, uses robust fusion and discrepancy elimination during training, and incorporates a test-time correspondence reasoning module leveraging a large MLLM to uncover latent attribute connections. Experiments on five benchmarks show consistent and substantial improvements over seven state-of-the-art methods across multiple noise levels.

## Strengths

- **Novel and practical problem formulation.** The paper clearly identifies and motivates the DNC problem, which is under-explored in MMEA. The empirical demonstration that real-world benchmarks contain significant noise (e.g., over 50% in ICEWS) and that existing methods degrade substantially under such noise is compelling and well-supported.
- **Comprehensive and principled method.** RULE addresses both training-time and test-time robustness with well-motivated components: reliability estimation via uncertainty (Dempster-Shafer theory) and consensus (marginal contribution), a dually robust loss that handles different noise subsets differently, robust attribute fusion weighted by reliability, and a test-time reasoning module that uses chain-of-thought prompting to uncover latent attribute connections.
- **Strong and consistent empirical results.** RULE outperforms all seven baselines across five datasets under three noise settings (inherent, 20%, 50%) on both Non-name and All-attributes protocols. The gains are substantial (e.g., 10+ H@1 points on ICEWS-WIKI under inherent DNC) and the method shows significantly slower performance degradation as noise increases (Figure 3a).
- **Thorough analysis and ablation.** The paper provides insightful visualizations of reliability distributions (Figure 3b), uncertainty-consensus separation (Figure 4), and reliability weights during fusion (Figure 5). The ablation study (Table 3) cleanly isolates the contributions of each component (DRL, DRF, TTR) and shows that both uncertainty and consensus are necessary.

## Weaknesses

### Fatal
None.

### Major
- **Heavy reliance on a very large MLLM for test-time reasoning.** The test-time correspondence reasoning module uses Qwen2.5-VL-72B-Instruct, a 72B-parameter model. The paper does not discuss the computational cost, inference latency, or practical feasibility of this component. This raises concerns about whether the reported gains are primarily due to the MLLM's power rather than the proposed training-time robustness mechanisms. An ablation using a smaller MLLM or a simpler reasoning method would help isolate the contribution of the training-time components.
- **The contribution of the proposed training-time components is conflated with the power of pre-trained encoders.** The method uses CLIP for feature extraction and the MLLM for reasoning. The baselines also use CLIP, but the test-time reasoning module is unique to RULE. The ablation study (Table 3) shows that removing TTR drops H@1 from 58.2 to 56.5 on Non-name, while removing DRL drops it to 31.6. This suggests the training-time components are critical, but the paper would benefit from an ablation that removes both the MLLM and the training-time components to show the net contribution of the training-time design alone.

### Minor
- **Ablation study is conducted on only one dataset (ICEWS-WIKI).** While the main results are comprehensive, the ablation study would be more convincing if repeated on at least one additional dataset (e.g., DBP15K_ZH-EN) to demonstrate that the component contributions generalize.
- **Hyperparameter sensitivity is not discussed in the main paper.** The threshold β and trade-off λ are fixed across all experiments, but the paper only provides sensitivity analysis in the appendix. Given the complexity of the method, a brief discussion of sensitivity in the main text would be helpful.
- **The theoretical justification is weak.** Theorem 1 (low uncertainty does not imply correct correspondence) is trivial and does not provide deep insight. The consensus modeling and greedy strategy (Eq. 7) are heuristic and lack rigorous guarantees. The paper would benefit from a more formal analysis or at least a discussion of limitations.
- **The performance gap between Non-name and All-attributes settings is very large** (e.g., RULE achieves 64.2 vs 98.9 H@1 on ICEWS-WIKI under inherent DNC). This suggests that the name attribute dominates the alignment signal. The paper does not discuss how the method's robustness generalizes when the name attribute is unavailable or noisy.

### Trivial
- The claim "one of the first methods to enhance test-time robustness for the MMEA task" is a minor contribution and could be softened.

## Nice-to-Haves

- Provide inference time and computational cost comparisons with baselines to quantify the overhead of the MLLM reasoning module.
- Include an ablation using a smaller MLLM (e.g., 7B) or a non-MLLM reasoning method to better isolate the contribution of the proposed training-time components.
- Show ablation results on at least one additional dataset (e.g., DBP15K_ZH-EN) to strengthen generalizability claims.
- Discuss the sensitivity of the method to the quality of the pre-trained encoders (e.g., using different CLIP variants or training from scratch).

## Novel Insights

Beyond the paper's own contributions, the key insight is that noisy correspondences in MMEA occur at two distinct levels (intra-entity and inter-graph) and that these two levels interact: inter-graph attribute-attribute noise is a byproduct of intra-entity entity-attribute noise and inter-graph entity-entity noise. This observation motivates a unified reliability estimation that can simultaneously handle both levels. The use of uncertainty (from evidential theory) and consensus (from marginal contribution) as complementary signals is a practical and effective way to distinguish clean from noisy pairs without requiring explicit noise labels. The test-time reasoning module further demonstrates that even after robust training, latent attribute connections (e.g., "football player" and "Mexico") can be missed by simple similarity measures, and that MLLMs with chain-of-thought prompting can recover these connections.

## Suggestions

- Add a discussion of the computational cost and practical limitations of using a 72B MLLM, including inference time and memory requirements. Consider including results with a smaller MLLM to demonstrate that the training-time components alone provide significant gains.
- Include ablation results on at least one additional dataset (e.g., DBP15K_ZH-EN) to show that the component contributions are not dataset-specific.
- Provide a brief sensitivity analysis of the key hyperparameters (β, λ) in the main paper, or at least state the range over which performance is stable.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>