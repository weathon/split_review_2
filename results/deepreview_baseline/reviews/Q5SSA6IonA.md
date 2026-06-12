## Summary

This paper proposes Vision Filter (ViF), a generic vision backbone based on a novel Fourier Neural Filter (FNF) operator. FNF extends the standard Fourier Neural Operator (FNO) by introducing an input-dependent kernel function that enables selective activation of local time-domain and global frequency-domain information, addressing the over-smoothing effect and bandwidth bottleneck of FNO. The authors demonstrate that ViF achieves competitive or superior performance compared to Transformer- and Mamba-based backbones across image classification (ImageNet-1K), object detection (COCO), and semantic segmentation (ADE20K), while maintaining favorable computational efficiency.

## Strengths

- **Novel architectural contribution**: The paper introduces a principled extension of FNO with input-dependent kernels (FNF), which is a genuine architectural innovation that bridges time-domain and frequency-domain processing in a unified framework. The theoretical analysis of FNO's limitations (bandwidth bottleneck and over-smoothing) provides clear motivation for the proposed approach.

- **Strong empirical results**: ViF achieves state-of-the-art or competitive results across three major vision tasks. On ImageNet-1K, ViF-T (83.8%) outperforms Swin-T (81.3%), VMamba-T (82.6%), and GFNet-S (80.0%) by significant margins. The improvements are consistent across model scales (T, S, B) and tasks, with particularly strong gains in object detection (e.g., ViF-T: 47.7 AP^b vs. Swin-T: 42.7 AP^b under 1× schedule).

- **Computational efficiency**: The paper demonstrates that ViF achieves better accuracy-throughput trade-offs than Transformer- and Mamba-based models (Figure 1), with quasi-linear complexity O(N log N). This is a meaningful practical advantage for deployment in resource-constrained settings.

- **Comprehensive evaluation**: The experimental setup is thorough, covering three major vision tasks with multiple model scales, training schedules, and comparison against a wide range of baselines (CNN, Transformer, Mamba, and Fourier-based models).

## Weaknesses

### Fatal
None.

### Major

- **Marginal gains over strong baselines on downstream tasks**: While the paper claims "state-of-the-art performance," the improvements over VMamba and LocalVMamba on object detection and segmentation are often marginal (0.2-0.4 mAP/mIoU). For instance, ViF-S achieves 50.1 AP^b vs. VMamba-S 49.9 AP^b under 3× MS schedule—a 0.2 improvement that may not be statistically significant. The paper does not report variance or confidence intervals, making it difficult to assess whether these gains are meaningful.

- **Lack of scalability evaluation**: The paper acknowledges this as a limitation but does not provide any experiments on larger datasets (e.g., ImageNet-22K) or larger model variants. Given that the paper claims ViF as a "generic vision backbone," the absence of large-scale pre-training results (which are standard for modern backbones like Swin, ConvNeXt, and ViT) is a significant gap. The community needs to see whether ViF benefits from scale.

- **Incomplete ablation study**: The ablation study (Table 5) is limited to the Tiny variant and only removes individual components. There is no ablation on: (1) the effect of the number of FNF blocks per stage, (2) the impact of different kernel sizes in local convolutions, (3) the sensitivity to the α and β parameters in adaptive modulation, or (4) whether the improvements come primarily from the FNF module or from the overall architecture design (e.g., hierarchical stages, LPU, FFN). Without these, it's unclear which design choices are critical.

- **Theoretical claims not fully validated**: The paper provides theoretical propositions about bandwidth bottleneck and over-smoothing, but does not empirically validate these claims. For example, there is no spectral analysis showing that ViF preserves more high-frequency information than FNO, nor any visualization of frequency responses. The connection between theory and practice is asserted but not demonstrated.

### Minor

- **Throughput comparison details**: Figure 1 shows throughput on H100 GPU, but many baselines (e.g., ConvNeXt, Swin) were originally benchmarked on different hardware. The paper should clarify whether all models were re-implemented and tested under identical conditions, or if numbers are taken from other sources. The throughput numbers for some baselines appear lower than reported in their original papers.

- **Missing comparison with recent Fourier-based methods**: The paper compares with GFNet and GFNetV2 but does not include more recent Fourier-based vision models such as Focal Frequency Networks or other FNO variants adapted for vision. This limits the assessment of where ViF stands within the Fourier-based vision literature.

- **Complexity analysis**: The paper claims quasi-linear complexity but does not provide a detailed FLOPs breakdown or wall-clock time comparison for the FNF module versus standard FNO or self-attention. The FLOPs numbers in Table 2 show ViF-T has 5.1G FLOPs vs. Swin-T's 4.5G, yet ViF-T achieves higher throughput—this discrepancy warrants explanation.

### Trivial
- The paper states "ViF demonstrates lower computational complexity than Transformer-based models" but does not provide a formal complexity analysis comparing O(N log N) vs. O(N^2) in the context of vision tasks with specific resolutions.

## Nice-to-Haves

- Include confidence intervals or error bars for main results to assess statistical significance of improvements.
- Add spectral analysis visualizations showing frequency response of FNF vs. FNO to empirically validate the theoretical claims about high-frequency preservation.
- Provide ablation on the number of frequency modes retained (K) and its impact on accuracy-efficiency trade-off.
- Include experiments with self-supervised pre-training (e.g., MAE-style) to demonstrate ViF's potential as a backbone for large-scale representation learning.

## Novel Insights

The paper's key insight is that FNO's limitations for vision tasks stem from two distinct issues: (1) the bandwidth bottleneck from fixed spectral truncation, and (2) the over-smoothing effect from multiplicative suppression of high frequencies. The proposed solution—input-dependent gating combined with adaptive modulation—is conceptually elegant because it addresses both issues simultaneously: selective activation (gating) allows the model to dynamically amplify informative high-frequency components while suppressing redundant ones, while adaptive modulation provides non-uniform frequency scaling. This joint time-frequency approach is a genuinely novel perspective that goes beyond prior Fourier-based vision models (which simply replaced attention with fixed frequency filtering) and could inspire further work on adaptive spectral methods for vision.

## Suggestions

- Add statistical significance tests (e.g., bootstrap confidence intervals) for the main results, especially where improvements over strong baselines are small (0.2-0.4 mAP/mIoU).
- Include experiments on ImageNet-22K or at least a larger model variant (ViF-L) to demonstrate scalability, which is critical for a backbone claiming to be "generic."
- Provide empirical validation of the theoretical claims: visualize the frequency spectrum of FNF vs. FNO outputs, and show that ViF preserves more high-frequency information.
- Expand the ablation study to include sensitivity analysis of key hyperparameters (α, β, number of frequency modes, local convolution kernel sizes) and component contributions at different stages.

## Score and Decision

The paper presents a novel and well-motivated architectural contribution (FNF) that addresses genuine limitations of FNO for vision tasks. The empirical results are strong and consistent across multiple tasks and model scales. However, the marginal improvements over strong Mamba-based baselines on downstream tasks, the lack of scalability evaluation, and the incomplete empirical validation of theoretical claims prevent this from being a clear accept. The paper would benefit from additional experiments and analysis to strengthen its claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>