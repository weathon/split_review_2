## Summary

This paper introduces Content-Aware Mamba (CAM), a state-space model that dynamically adapts its processing to image content for learned image compression. CAM overcomes two key limitations of standard Mamba: (1) a content-adaptive token permutation mechanism that reorders tokens based on feature similarity rather than spatial proximity, and (2) a global-prior prompting mechanism that injects sample-specific global priors into the SSM to mitigate strict causality without multi-directional scans. The resulting model, CMIC, achieves state-of-the-art rate-distortion performance, surpassing VTM-21.0 by 15.91%, 21.34%, and 17.58% BD-rate on Kodak, Tecnick, and CLIC datasets respectively, while maintaining moderate complexity.

## Strengths

- **Novel and well-motivated approach**: The paper identifies two fundamental limitations of Mamba for image compression—content-agnostic scanning and strict causality—and proposes principled solutions (content-adaptive token permutation and global-prior prompting) that are directly motivated by the compression task. The clustering-based permutation and prompt dictionary are clever adaptations of existing ideas (VQ-VAE, MambaIRv2) tailored to compression.

- **Strong empirical results**: CMIC achieves state-of-the-art BD-rate reductions across three standard datasets, outperforming both prior Mamba-based models (MambaVC, MambaIC) and strong transformer-based models (FTIC, TCM-L, MLIC++). The gains are consistent across all bitrates and datasets, and the model also shows competitive MS-SSIM performance.

- **Thorough ablation and analysis**: The paper provides comprehensive ablation studies isolating the contributions of each component (CTP and GPP), comparisons with alternative architectures (Conv, 2D Mamba, attention-only), and insightful visualizations of effective receptive fields, clustering results, and non-causality. These analyses convincingly demonstrate that both components are necessary and complementary.

- **Favorable complexity-performance trade-off**: CMIC achieves its performance gains with moderate parameter count (69.11M), FLOPs (2.39T), latency (0.405s), and peak memory (4.44GB), significantly outperforming prior Mamba-based models in efficiency while maintaining competitive complexity against transformer-based models.

## Weaknesses

### Minor

- **Lack of statistical significance reporting**: The BD-rate results are reported as single numbers without confidence intervals or error bars. Given the variability in compression performance across images, providing standard deviations or statistical significance tests would strengthen the claims of superiority over baselines.

- **Limited discussion of clustering stability**: The paper mentions that the EMA-based codebook update ensures training stability, but does not provide quantitative evidence (e.g., convergence plots, centroid drift over training) to demonstrate that the clustering remains stable and meaningful throughout training, especially in early stages when features are noisy.

- **Comparison fairness with MambaVC/MambaIC**: While the paper includes many baselines, the comparison with MambaVC and MambaIC may not be entirely fair if those models use different entropy models or architectural choices. The paper does not discuss whether the performance gap is due to the proposed CAM components or other architectural differences (e.g., different channel sizes, number of blocks).

### Trivial

- The paper uses "CMiC" and "CMIC" interchangeably; consistency would improve readability.

## Nice-to-Haves

- An analysis of how the clustering centroids evolve across different stages of the network (e.g., whether early stages capture low-level patterns and later stages capture semantic patterns) would deepen understanding of the content-adaptive mechanism.

- A discussion of the sensitivity to the number of K-Means iterations (T) during training and whether fewer iterations suffice would be useful for practitioners.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the rigid scanning order of Mamba is fundamentally misaligned with the redundancy structure of natural images, where semantically related regions may be spatially distant. The paper demonstrates that by reordering tokens based on feature similarity and injecting global priors, the SSM can effectively capture long-range dependencies that are critical for compression, while maintaining linear complexity. This suggests that the success of Mamba in vision tasks may depend more on how the sequence is structured than on the SSM architecture itself, opening avenues for content-adaptive sequence design in other vision applications.

## Suggestions

- Add confidence intervals or standard deviations to the BD-rate results in Table 1 to quantify the variability across images.
- Provide a brief analysis of clustering convergence during training (e.g., centroid movement, assignment consistency) to further validate the stability of the EMA-based update.
- Clarify whether the comparison with MambaVC and MambaIC uses the same entropy model and training setup, or note any differences that could affect the comparison.

## Score and Decision

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>