## Summary

This paper introduces Content-Aware Mamba (CAM) for learned image compression (LIC), a state-space model architecture that addresses two fundamental limitations of standard Mamba when applied to images: its content-agnostic fixed scan order and its strict causality. The proposed mechanisms—Content-Adaptive Token Permutation (clustering-based sequence reordering) and Global-Prior Prompting (sample-specific global conditioning)—enable the model to prioritize interactions between content-similar tokens regardless of spatial distance and to relax causal constraints without multi-directional scans. The resulting CMIC model achieves state-of-the-art rate-distortion performance, surpassing VTM-21.0 by 15.91%–21.34% BD-rate across Kodak, Tecnick, and CLIC datasets while maintaining computational efficiency.

## Strengths

- **Well-motivated and novel contributions**: The paper clearly identifies two key mismatches between standard Mamba and image compression requirements (rigid scan order, strict causality) and proposes principled, complementary solutions (CTP and GPP) that directly address these issues. The integration of codebook-based clustering for content-adaptive scanning and centroid-tied prompts for global conditioning is both novel and technically sound.
- **State-of-the-art empirical performance**: CMIC consistently outperforms a comprehensive set of baselines—including traditional codec VTM-21.0, transformer-based methods (FTIC, TCM-L), and prior Mamba-based codecs (MambaVC, MambaIC)—with substantial BD-rate margins (e.g., 15.91% vs VTM on Kodak). The gains are consistent across multiple datasets and distortion metrics (MSE, MS-SSIM).
- **Thorough experimental validation**: The paper provides extensive ablation studies isolating each component, comparisons with alternative structures (Conv, 2D Mamba, attention-only), ERF visualizations showing increased and content-adaptive receptive fields, clustering visualizations demonstrating semantic grouping, and complexity benchmarks (FLOPs, latency, memory). Each claim is supported with concrete evidence.
- **Favorable complexity-performance trade-off**: CMIC achieves its superior RD performance with moderate parameters (69M), low FLOPs (2.39T), and practical inference latency (0.405s on 2K images), significantly outperforming larger models like MambaIC (157M, 5.56T) and MLIC++ (116M, 2.64T) while using less compute.

## Weaknesses

### Fatal
None.

### Major

- **Clustering hyperparameter sensitivity insufficiently explored**: The method introduces several clustering hyperparameters—number of clusters K, number of K-Means iterations T, EMA decay λ—but only K is ablated (at values 32, 64, 128). The sensitivity to T and λ, and their impact on training stability and final performance, is not investigated. Since the clustering is a core component, understanding robustness to these choices is important for reproducibility and practical deployment.

### Minor

- **Quantification of non-causality is qualitative**: The claim that GPP "relaxes strict causality" is supported only by ERF visualizations (Figure 9). While these are informative, a quantitative measure—e.g., computing the influence of tokens that appear later in the scan order on earlier token representations, or comparing the effective time horizon of the SSM with and without GPP—would provide stronger evidence. This is a relatively minor gap given the visual evidence and ablation results.
- **Applicability in entropy model limited**: The ablation (Appendix A.3.2) notes that adding CAM to the entropy model yields negligible gains while increasing latency, which the authors acknowledge as a limitation. While this does not weaken the core contribution (CAM in transforms), it suggests the method may not be universally beneficial for all components of an LIC pipeline. A brief discussion of why this might be the case would strengthen the paper.

### Trivial
None.

## Nice-to-Have Suggestions

- Provide quantitative metrics for non-causality (e.g., average influence of future tokens on current token representation) to strengthen the claim about causality relaxation.
- Ablate sensitivity to T (number of K-Means iterations) and λ (EMA decay) to demonstrate robustness.
- Visualize or discuss why CAM does not benefit the entropy model—this could yield insights into the differential roles of long-range dependencies in transform versus entropy modeling.

## Novel Insights

Beyond the paper’s own contributions, the results offer a broader insight: the limitations of SSMs for 2D data stem less from the inherent linear-time recursion and more from the mismatch between the 1D causal scan order and the non-causal, spatially distributed redundancy structure of images. By replacing the fixed scan with a content-adaptive permutation and injecting global priors, the paper shows that SSMs can be made highly effective for image compression without resorting to quadratic attention or multiple directional scans. This suggests that similar content-adaptive scanning strategies could benefit other vision tasks where semantic correlation matters more than spatial adjacency, such as segmentation or inpainting. The codebook-based clustering approach also demonstrates that discrete latent representations can guide SSM modeling in a stable, learnable way—a promising direction for general vision Mamba research.

## Suggestions

- Include a sensitivity analysis of the clustering hyperparameters (T and λ) to demonstrate training stability and ease of use.
- Add a quantitative evaluation of non-causality (e.g., compute the gradient or influence score of a token at position i on tokens at positions < i versus > i in the scan order, with and without GPP).
- Briefly discuss why CAM benefits the transform networks more than the entropy model, providing insight into the role of long-range dependency in different LIC components.

## Score and Decision

Score: 8

Decision: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>