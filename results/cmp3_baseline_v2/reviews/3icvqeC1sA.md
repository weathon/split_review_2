## Summary

This paper introduces ChaosNexus, a foundation model for forecasting chaotic dynamical systems. The key innovation is a U-Net-inspired Transformer architecture (ScaleFormer) that explicitly captures multi-scale temporal structure through hierarchical patch merging and expansion, augmented with Mixture-of-Experts layers and wavelet-based frequency fingerprints. The model is pretrained on a large corpus of synthetic chaotic ODEs and demonstrates strong zero-shot and few-shot forecasting performance on both synthetic benchmarks and real-world weather data, with a scaling analysis revealing that generalization benefits more from system diversity than per-system data volume.

## Strengths

- **Novel architectural contribution**: The ScaleFormer design with hierarchical patch merging/expansion, axial attention, and MoE layers is a well-motivated approach to address the multi-scale nature of chaotic dynamics. The U-Net-inspired encoder-decoder structure with skip connections is a principled way to capture both fine-grained fluctuations and coarse-grained trends simultaneously.

- **Comprehensive evaluation**: The paper evaluates on a large-scale testbed of 9,000+ synthetic chaotic systems with multiple metrics (sMAPE, correlation dimension error, KL divergence, Lyapunov exponent error) that assess both point-wise accuracy and long-term attractor statistics. The real-world weather forecasting experiments with zero-shot and few-shot settings provide compelling evidence of practical utility.

- **Strong empirical results**: ChaosNexus achieves state-of-the-art zero-shot performance on synthetic benchmarks, particularly on long-term statistical metrics (D_step, D_lyap, ME_LRW). The weather forecasting results are striking—zero-shot MAE below 1°C for 5-day global temperature forecasts, outperforming baselines trained on 473K samples from the target domain.

- **Insightful scaling analysis**: The finding that generalization improves with system diversity rather than per-system trajectory volume is a valuable design principle for scientific foundation models. This goes beyond simply confirming prior work by providing a controlled comparison between the two scaling dimensions.

## Weaknesses

### Major

- **Limited architectural ablation**: The paper does not provide a clean ablation study isolating the contribution of each component (ScaleFormer multi-scale design, MoE layers, wavelet fingerprint, MMD regularization). Without ablations, it is difficult to attribute the performance gains to the claimed multi-scale innovation versus other design choices. For instance, how much does the U-Net structure matter compared to a single-scale Transformer with the same MoE and wavelet components?

- **Missing comparison to Panda with comparable compute**: The primary baseline Panda uses a simpler architecture. The paper does not control for model size, training compute, or data augmentation when comparing ChaosNexus to Panda. The reported improvements could partially stem from larger model capacity or longer training rather than the multi-scale design specifically.

- **Statistical significance concerns**: While the paper reports p-values for ChaosNexus vs. Panda on some metrics, the box plots show substantial overlap in distributions for sMAPE and D_frac. The practical significance of the improvements on point-wise metrics appears modest, and the paper would benefit from clearer reporting of effect sizes and confidence intervals for all comparisons.

### Minor

- **The weather forecasting comparison is asymmetric**: ChaosNexus benefits from pretraining on synthetic chaotic systems, while the baselines (CrossFormer, FEDFormer, etc.) are trained from scratch on the weather data. A fairer comparison would include Panda or Chronos-S-SFT (which are also pretrained on chaotic data) in the weather experiments. The paper mentions these results are in the appendix but does not prominently feature them.

- **Limited analysis of failure cases**: The paper does not discuss which types of chaotic systems ChaosNexus struggles with, or whether certain dynamical regimes (e.g., high-dimensional chaos, systems with extreme parameter sensitivity) pose particular challenges.

### Trivial

- The paper uses "REVISE" markers in the text, suggesting incomplete editing or formatting artifacts from the submission process.

## Nice-to-Haves

- An ablation study that systematically removes each component (multi-scale design, MoE, wavelet fingerprint, MMD loss) and measures the impact on both point-wise and statistical metrics.
- A controlled comparison where Panda is scaled to the same parameter count as ChaosNexus to isolate the benefit of the architectural innovation.
- Analysis of computational cost (training time, inference speed, memory usage) relative to baselines.
- Visualization of the learned expert specialization in the MoE layers—which experts activate for which types of dynamical systems?

## Novel Insights

Beyond the paper's own contributions, the most interesting insight is the scaling behavior result: cross-system generalization in chaotic dynamics is driven by the diversity of training systems rather than the volume of trajectories per system. This has practical implications for data collection strategies in scientific ML—it suggests that investing in covering a wider range of dynamical regimes is more valuable than collecting longer trajectories from a few systems. This principle may extend beyond chaotic systems to other scientific domains where the underlying dynamics vary across systems.

## Suggestions

- Add a systematic ablation study isolating the contribution of the multi-scale ScaleFormer design, MoE layers, wavelet fingerprint, and MMD regularization. This is essential to validate the paper's central claim that multi-scale representation is the key innovation.
- Include a controlled comparison where Panda is scaled to match ChaosNexus's parameter count, to disentangle architectural benefits from scale benefits.
- Report effect sizes and confidence intervals for all comparisons, not just selected ones.
- Discuss the computational cost of the proposed architecture relative to baselines.

## Score and Decision

The paper presents a well-motivated architectural contribution to an important problem (chaotic system forecasting) with strong empirical results on both synthetic and real-world benchmarks. The scaling analysis provides a valuable design principle. However, the lack of proper ablation studies makes it difficult to attribute the performance gains to the claimed multi-scale innovation versus other design choices or simply larger model capacity. This is a significant weakness that prevents full confidence in the paper's central claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>