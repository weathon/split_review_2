## Summary

This paper introduces RADAR, a neural framework that augments existing constructive VRP solvers to handle asymmetric distance matrices. It addresses two aspects of asymmetry: *static asymmetry* via an SVD-based initialization that encodes directional node roles from the cost matrix, and *dynamic asymmetry* via Sinkhorn normalization in the encoder attention to enforce balanced bidirectional flows. Extensive experiments on 17 synthetic and 3 real-world VRP variants show that RADAR consistently outperforms strong baselines, generalizes well to larger instances, and maintains robust performance under distribution shift.

## Strengths

- **Well-motivated and practically relevant problem.** Most neural VRP solvers assume symmetric Euclidean distances, which is unrealistic for many real-world routing scenarios. The paper clearly articulates this gap and targets a genuine bottleneck for deploying NCO in practice.
- **Principled and technically sound method.** The SVD-based initialization provides a theoretically grounded way to extract directional information from the asymmetric distance matrix into compact node embeddings (Definition 1 and Eq. 5). The Sinkhorn normalization is a natural choice for enforcing doubly stochastic attention, which captures global neighborhood context that row-wise softmax misses.
- **Extensive and rigorous evaluation.** The paper evaluates on 17 synthetic VRP variants (including ATSP and 16 asymmetric variants from RouteFinder) and 3 real-world datasets, comparing against a wide range of baselines (LKH, HGS, MatNet, ICAM, ELG, ReLD, RRNCO, etc.). Ablation studies clearly isolate the contribution of each component, and analyses on asymmetry levels, demand distributions, and the role of coordinates provide deep insight.
- **Strong empirical results.** RADAR achieves the best performance among learning-based methods across nearly all settings, with particularly impressive zero-shot generalization to larger instances (e.g., 0.72% gap on ATSP100, 1.01% on ATSP200, 2.13% on ATSP500). On real-world datasets, it outperforms RRNCO by a clear margin and approaches the performance of traditional solvers.
- **Clear exposition of static vs. dynamic asymmetry.** The paper provides a useful conceptual framework for thinking about asymmetry in neural VRP solvers, and the two proposed components directly address these distinct aspects.

## Weaknesses

### Fatal
None.

### Major
- **Limited discussion of the low-rank assumption.** The SVD-based initialization truncates the distance matrix to rank \(k=10\), which captures ~85% of the matrix information. The paper does not discuss scenarios where the effective rank is high (e.g., noisy or non-Euclidean matrices) and the potential failure modes of this approximation. A more thorough analysis of when low-rank decomposition is appropriate would strengthen the paper.
- **Multitask evaluation is narrow.** In the multitask setting (Table 2), only two neural baselines (RF and RF-NN) are compared. Given that the paper claims strong generalizability across 16 variants, a broader comparison (e.g., including MatNet-based variants or RRNCO adapted to this setting) would be more convincing. The paper should explain why other baselines are not included.

### Minor
- **The concept of "dynamic asymmetry" could be better justified.** The paper argues that Sinkhorn normalization captures dynamic asymmetry by making attention scores aware of both nodes' neighborhoods. While plausible, the paper does not provide direct empirical evidence (e.g., visualizing attention matrices or showing that Sinkhorn produces more asymmetric attention patterns than softmax). A simple analysis would strengthen this claim.
- **The choice of \(k=10\) for SVD is somewhat arbitrary.** The paper shows that top-10 captures ~85% of information and that larger \(k\) improves in-distribution but hurts generalization. However, the optimal \(k\) may vary across datasets. The paper could discuss adaptive selection or provide a sensitivity analysis on real-world data.
- **Runtime analysis is relegated to the appendix.** The paper mentions runtime profiling for SVD and Sinkhorn but does not include the figures or detailed discussion in the main text. Given that computational overhead is a practical concern, a brief summary in the main paper would be helpful.

### Trivial
None.

## Nice-to-Haves

- A theoretical analysis connecting SVD-based initialization to spectral graph theory or low-rank matrix completion would deepen the contribution.
- Visualizations of the learned embeddings (e.g., PCA projections) to show that they capture directional roles (source vs. destination) would be illuminating.
- An adaptive method for selecting the SVD rank \(k\) based on the singular value spectrum could improve robustness across different problem types.

## Novel Insights

The paper's core insight is that asymmetric distance matrices can be effectively encoded into neural VRP solvers by decomposing the problem into static and dynamic asymmetry. The SVD-based initialization provides a principled way to convert edge-level directional information into node-level embeddings that are compact, generalizable, and compatible with attention mechanisms. The Sinkhorn normalization further ensures that attention scores reflect the full neighborhood context of both interacting nodes, which is particularly important when the distance structure cannot be recovered from coordinates. The empirical finding that coordinates are not necessary for good performance in asymmetric settings (Section 5.4) is a useful practical insight.

## Suggestions

- Discuss the limitations of the low-rank assumption and provide guidance on when SVD-based initialization may be less effective (e.g., high-rank or highly noisy matrices).
- In the multitask setting, include additional baselines or clearly justify why only two are compared.
- Provide a direct comparison of attention patterns (e.g., asymmetry of attention scores) between Sinkhorn and softmax to empirically support the "dynamic asymmetry" claim.
- Consider reporting the sensitivity of results to the SVD rank \(k\) on real-world datasets, not just synthetic ones.

## Score and Decision

The paper addresses an important and under-explored problem, proposes a technically sound and well-motivated method, and provides extensive experimental validation. The contributions are significant for the NCO community, and the paper is clearly written. The weaknesses are not fatal and can be addressed in future work or discussion. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>