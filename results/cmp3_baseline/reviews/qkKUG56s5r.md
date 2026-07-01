## Summary

This paper introduces Automatic Complementary Separation Pruning (ACSP), a method for pruning convolutional neural networks that combines structured and activation-based pruning. ACSP constructs a graph space encoding each component's separation capability across all class pairs using Jeffries-Matusita distance, then uses k-Medoids clustering with a Mean Simplified Silhouette (MSS) index and Kneedle algorithm to automatically determine the optimal number of components to retain per layer. The method achieves 1.5-2.5× FLOP reduction with minimal accuracy loss across VGG, ResNet, DenseNet, and MobileNet architectures on CIFAR-10/100 and ImageNet.

## Strengths

- **Fully automated pruning extent determination**: ACSP eliminates the need for manual tuning of pruning ratios per layer through its knee-finding approach on the MSS curve, addressing a practical limitation of many existing pruning methods that require user-specified pruning rates or iterative sensitivity analysis.

- **Novel complementary selection principle**: The use of graph-space clustering to enforce diversity among retained components is a principled approach to reducing redundancy. The MSS index specifically designed to measure coverage across the entire graph space (rather than just nearest-cluster separation) is well-motivated.

- **Strong empirical results across multiple architectures**: The method consistently achieves competitive or superior speed-up ratios (e.g., 2.25× on ResNet-50, 2.59× on VGG-16) while maintaining or improving accuracy, demonstrated across 8 model-dataset combinations with comparisons to numerous baselines.

- **Inference latency validation**: Table 2 provides actual wall-clock timing measurements (not just FLOP ratios), showing consistent latency reductions in both batch and single-inference modes, which strengthens the practical relevance of the claims.

## Weaknesses

### Fatal
None.

### Major

- **Computational cost of graph construction scales poorly with number of classes**: The separation matrix has dimensions N_i × (p × p × C(C-1)/2). For datasets like ImageNet-1K with C=1000, this yields approximately 500,000 class pairs per layer. The paper acknowledges this limitation but provides no analysis of actual runtime or memory cost for high-class datasets, nor any experimental results on such scenarios. This significantly limits the method's applicability to large-scale classification tasks.

- **Lack of ablation studies on key design choices**: The paper does not isolate the contribution of the complementary selection mechanism versus the weight-based selection within clusters. Figure 2 shows these can differ, but there is no experiment comparing ACSP with vs. without the complementary selection (e.g., just selecting top-k by weight). Similarly, the choice of JM distance over alternatives is mentioned but not quantitatively compared in the main results.

- **Fine-tuning protocol is underspecified and potentially problematic**: The method fine-tunes after each layer pruning (line 14 of Algorithm 1), which means later layers are fine-tuned multiple times while earlier layers are fine-tuned fewer times. The paper does not discuss whether this sequential fine-tuning introduces confounding effects or how the total fine-tuning budget compares to baselines that typically fine-tune once after full pruning.

### Minor

- **The speed-up metric in Table 1 is FLOP-based, not wall-clock**: While Table 2 provides actual timing, the main comparison table uses FLOP ratios. The paper notes that "wall-clock speed-ups in Table 2 are smaller than the FLOP-based factors," which is expected but means the headline speed-up numbers (e.g., 2.25×) overstate practical gains.

- **Baseline comparisons are not perfectly controlled**: Different baselines report results at different base accuracies (e.g., ResNet-50 base ranges from 76.15 to 76.65). While this is common in pruning literature, it makes direct comparisons of Δ accuracy less reliable.

- **The method requires a forward pass through the entire dataset for each layer**: This is standard for activation-based pruning but should be noted as a computational cost during the pruning phase itself.

### Trivial
- Algorithm 1 line 12 says "top-k' components by weight" but the method description in Section 3.4.2 says the highest-weight component from each cluster is selected, which is not the same as top-k' globally by weight. This inconsistency should be resolved.

## Nice-to-Haves

- An analysis of how the pruning decisions (which components are kept) differ between ACSP and a simple weight-magnitude baseline would help validate the complementary selection principle.
- A discussion of how ACSP handles skip connections or residual blocks where pruning one layer affects the input to another, beyond the sequential layer-by-layer approach.
- Sensitivity analysis of the Kneedle algorithm's polynomial degree choice on pruning outcomes.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Provide runtime analysis of the graph construction step for ImageNet-scale classification (C=1000) to demonstrate practical feasibility, or propose and evaluate the class-pair sampling approximation mentioned in the limitations.
- Add an ablation study comparing: (a) ACSP as presented, (b) ACSP without complementary selection (just top-k by weight), and (c) ACSP with random selection within clusters, to isolate the benefit of the graph-based diversity mechanism.
- Clarify the fine-tuning protocol: report total number of fine-tuning epochs across all layers and compare to the single fine-tuning step used by most baselines.

## Score and Decision

The paper presents a well-motivated and novel approach to automated pruning with a principled complementary selection mechanism. The empirical results are strong across multiple architectures and datasets. However, the scalability concern for high-class datasets and the lack of ablation studies on key design choices are significant enough to warrant caution. The paper makes a clear contribution but requires addressing these issues to fully validate the method.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>