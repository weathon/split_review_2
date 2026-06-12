## Summary

This paper introduces the Signal Dice Similarity Coefficient (SDSC), a structure-aware reconstruction metric for time-series self-supervised representation learning. SDSC extends the Dice Similarity Coefficient from segmentation to continuous signals by quantifying structural agreement based on signed amplitude intersections, and is used as a replacement for MSE loss in the reconstruction branch of SimMTM. Experiments on forecasting and classification benchmarks show that SDSC-based pre-training achieves comparable or improved performance relative to MSE, particularly in in-domain and low-resource scenarios with frozen encoders.

## Strengths

- **Novel and well-motivated metric**: The paper identifies a genuine limitation of MSE-based reconstruction in time-series SSL—its insensitivity to waveform polarity and structural shape—and proposes SDSC as a principled alternative grounded in the Dice coefficient. The illustrative examples in Figure 1 and Table 1 convincingly demonstrate cases where MSE fails to distinguish semantically different signals.

- **Clean experimental design**: By replacing only the reconstruction loss in SimMTM while keeping the contrastive objective (InfoNCE) fixed, the paper isolates the effect of the reconstruction objective. This controlled setup allows clear attribution of performance differences to the loss function rather than architectural or contrastive learning changes.

- **Comprehensive evaluation across multiple objectives**: The paper compares SDSC against MSE, SoftDTW, PCC, and SI-SNR across forecasting and classification tasks, including both in-domain and cross-domain settings, frozen and fine-tuned encoders. The hybrid loss combining SDSC and MSE is a practical contribution that addresses the amplitude-structure trade-off.

## Weaknesses

### Fatal
None.

### Major

- **Modest and inconsistent performance gains**: While SDSC shows improvements in some settings (e.g., frozen encoder in-domain classification), the gains are small (e.g., ~1% accuracy improvement) and not consistent across all settings. In fine-tuning classification and cross-domain scenarios, MSE or PCC often match or outperform SDSC. The paper's claim that SDSC "achieves comparable or improved performance" is accurate, but the improvements are marginal and the evidence for SDSC being a clearly superior alternative is weak.

- **Limited scope of evaluation**: The paper only evaluates SDSC within a single backbone (SimMTM). While this is justified for controlled comparison, it limits the generalizability of the findings. The paper acknowledges this as future work but does not provide any evidence that SDSC benefits other SSL frameworks (e.g., TS2Vec, TI-MAE, contrastive-only methods). The claim that SDSC is a "promising metric for structure-aware learning" would be stronger with at least one additional backbone.

- **The hybrid loss often performs similarly to MSE alone**: In many results (e.g., Table 4, Table 6), the hybrid loss achieves nearly identical performance to MSE. This raises the question of whether SDSC is actually contributing meaningful signal beyond what MSE already captures, or whether the hybrid simply defaults to MSE behavior. The paper would benefit from an ablation showing the contribution of SDSC in the hybrid loss (e.g., by varying λ_sdsc systematically).

### Minor

- **The differentiable Heaviside approximation is not thoroughly analyzed**: The paper introduces a sigmoid-based approximation with sharpness parameter α and sets α=10 based on Appendix A.3, but does not discuss sensitivity to this choice or provide convergence analysis. The discontinuity issue is acknowledged but not empirically characterized (e.g., gradient variance, training stability).

- **Computational complexity comparison is mentioned but not quantified**: The paper claims SDSC is "lightweight" and "alignment-free" compared to SoftDTW, but does not provide wall-clock time or FLOPs comparisons. Given that SDSC involves element-wise operations and a Heaviside approximation, a brief complexity analysis would strengthen the practical motivation.

### Trivial
- The paper states "SDSC is therefore alignment-free and computationally linear" but does not define what "computationally linear" means in terms of sequence length.

## Nice-to-Haves

- Evaluate SDSC on at least one additional SSL backbone (e.g., TS2Vec, TI-MAE) to demonstrate generalizability.
- Provide an ablation study on the hybrid loss weight λ_sdsc to understand the contribution of SDSC.
- Include wall-clock training time comparisons between MSE, SDSC, and SoftDTW.
- Analyze the gradient properties of the Heaviside approximation (e.g., gradient norm, variance) during training.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Consider evaluating SDSC in a purely reconstruction-based SSL framework (without contrastive loss) to isolate its effect more directly.
- Provide a sensitivity analysis of the sharpness parameter α on downstream performance and training stability.
- Include a qualitative visualization of reconstructions from MSE vs. SDSC-trained models to illustrate the structural differences claimed in the paper.

## Score and Decision

The paper presents a well-motivated and cleanly evaluated metric for time-series SSL. However, the performance gains are modest and inconsistent, and the evaluation is limited to a single backbone. While the idea is novel and the experimental design is sound, the evidence does not yet support SDSC as a clearly superior alternative to MSE in practice. The paper is a solid contribution that would benefit from broader validation.

**Score**: 6

**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>