## Summary

The paper introduces ChaosNexus, a foundation model for forecasting chaotic systems that explicitly handles multi-scale temporal structure via a U-Net-inspired Transformer architecture (ScaleFormer) with hierarchical patch merging/expansion, Mixture-of-Experts layers, and a wavelet-based frequency fingerprint. The model is pretrained on a large corpus of synthetic chaotic ODEs and evaluated on zero-shot and few-shot forecasting tasks, including a real-world weather benchmark, where it demonstrates competitive point-wise accuracy and improved long-term attractor statistics compared to existing baselines. A scaling analysis further suggests that cross-system generalization benefits more from the diversity of training systems than from the volume of trajectories per system.

## Strengths

- **Well-motivated problem and architecture**: The paper correctly identifies that chaotic dynamics exhibit multi-scale temporal structure and that existing foundation models (Panda, DynaMix) operate at a single resolution. The ScaleFormer design with hierarchical patch merging/expansion is a natural and principled way to address this limitation.
- **Comprehensive evaluation**: The experiments cover zero-shot forecasting on 9.3K synthetic chaotic systems with multiple metrics (point-wise sMAPE, attractor statistics like correlation dimension error, KL divergence, Lyapunov exponent error), few-shot weather forecasting, and scaling analysis. The inclusion of both synthetic and real-world benchmarks strengthens the claims.
- **Strong weather forecasting results**: The zero-shot MAE below 1°C for 5-day global temperature forecasts, outperforming baselines fine-tuned on substantially more in-domain data, is striking and suggests that pretraining on diverse chaotic dynamics provides a powerful inductive bias.
- **Scaling insight**: The analysis showing that increasing the number of distinct systems improves generalization while increasing per-system trajectories does not is a practically useful finding for guiding future data collection and model development.

## Weaknesses

### Fatal
None.

### Major

1. **Incremental improvement over the most relevant baseline (Panda)**: The claimed “notable improvements” in long-term attractor statistics are not clearly supported by the visual evidence in Figure 2. For example, the median correlation dimension error (D_frac) appears nearly identical between ChaosNexus and Panda (~0.203 vs ~0.200), and the KL divergence (D_step) also overlaps substantially. The paper does not report the exact numerical values for Panda in the main text, making it difficult to assess the magnitude of improvement. The point-wise sMAPE improvement (~5 points) is modest. Given that Panda already uses the same pretraining corpus and a Transformer backbone, the added complexity of ScaleFormer should be justified by a more substantial performance gap.

2. **Weather forecasting results require stronger validation**: The zero-shot MAE of ~0.8°C for 5-day global temperature forecasts is surprisingly low compared to baselines that achieve >3°C even after fine-tuning on 473K samples. The paper does not provide a baseline trained on the full WEATHER-5K dataset (which contains millions of samples), nor does it report the performance of a simple climatology or persistence forecast. Without these references, it is unclear whether the baselines are properly tuned or whether the task is unusually easy. Additionally, the paper should discuss why the gap is so large—e.g., whether the synthetic pretraining corpus contains dynamics that transfer exceptionally well to weather, or whether the baselines are underfitting due to insufficient capacity or hyperparameter choices.

3. **Scaling analysis is incomplete**: Figure 4(b) shows that increasing the number of time points (by adding more trajectories per system) does not improve performance, but the x-axis range (0–350M time points) and the fixed number of systems are not clearly stated. The paper should specify how many systems were used in this experiment and whether the total number of time points was varied over a wide enough range. Moreover, the claim that “generalization is driven by diversity, not volume” is a strong statement that would benefit from additional experiments where both diversity and volume are jointly varied, and from a discussion of potential saturation effects.

### Minor

- The paper uses “REVISE” markers in the text, which is unprofessional for a submission.
- Figure 2 is cluttered with many box plots and small text, making it difficult to read the median values and compare distributions.
- The computational cost (training time, inference speed, memory) of ChaosNexus relative to baselines is not reported, which is important for practical deployment.
- The paper does not discuss limitations: e.g., what types of chaotic systems might the model fail on (e.g., systems with very high dimensionality or non-smooth dynamics)?

### Trivial

- Some formatting inconsistencies (e.g., “REVISE” markers, missing punctuation in captions).

## Nice-to-Haves

- Provide an ablation study that isolates the contribution of each component (multi-scale architecture, MoE, wavelet fingerprint, MMD loss) on the synthetic benchmark.
- Include a comparison to a single-scale variant of ChaosNexus (e.g., removing patch merging/expansion) to directly demonstrate the benefit of multi-scale processing.
- Report the performance of a simple persistence or climatology baseline on the weather task to contextualize the MAE values.
- Discuss the choice of hyperparameters (number of experts, patch size, number of scales) and their sensitivity.

## Novel Insights

The paper’s key insight—that cross-system generalization in chaotic dynamics benefits more from the diversity of training systems than from the volume of trajectories per system—is a useful refinement of earlier scaling laws (Lai et al., 2025). However, this finding is not entirely new; the paper itself acknowledges that prior work established the scaling law for system diversity. The novel contribution is the demonstration that per-system data volume yields negligible gains once a sufficient number of systems is used. This insight, if validated across more settings, could guide efficient data collection for scientific foundation models.

## Suggestions

- Clearly report the exact numerical values for all metrics (including Panda) in the main text or a table, and perform statistical significance tests (e.g., paired Wilcoxon) to support claims of improvement.
- For the weather experiment, include a baseline trained on the full training set and a simple persistence forecast to calibrate the difficulty of the task. Also, report the MAE for all five weather variables, not just temperature.
- In the scaling analysis, specify the number of systems used in Figure 4(b) and the number of trajectories per system in Figure 4(c). Consider a joint scaling experiment where both diversity and volume are varied.
- Add a discussion of limitations, such as the model’s applicability to very high-dimensional systems or systems with non-smooth dynamics.

## Score and Decision

The paper addresses an important problem with a well-motivated architecture and provides extensive experiments. However, the improvement over the strongest baseline (Panda) is modest, and the weather results, while impressive, lack sufficient validation to fully rule out alternative explanations. The scaling insight is interesting but not deeply novel. Overall, the paper is solid but not exceptional.

**Score**: 6.0

**Decision**: Accept

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>