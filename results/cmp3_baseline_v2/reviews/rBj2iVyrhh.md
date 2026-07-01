## Summary
This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework to address modality imbalance in multimodal learning. The method first pre-trains a shared classifier with bidirectional cross-attention and a regularization term that penalizes modality contribution disparities, then freezes this classifier during alternating training while using modality-specific LoRA modules and sample-level secondary updates to enhance weaker modalities. Experiments on CREMA-D, Kinetic-Sound, and MVSA datasets show consistent improvements over state-of-the-art methods.

## Strengths
- **Novel theoretical connection**: The paper draws an insightful analogy between class imbalance and modality imbalance through gradient dynamics analysis, providing a principled motivation for applying classifier-constraining strategies to multimodal learning. This theoretical framing is well-developed and goes beyond typical heuristic approaches.
- **Well-designed two-stage framework**: The approach of pre-training an unbiased classifier and then freezing it during alternating training is conceptually clean and addresses a genuine limitation of prior alternating training methods (MLA) that overlook classifier bias. The integration of LoRA modules to handle distribution mismatch between fused and unimodal features is a practical and elegant solution.
- **Strong empirical results**: CCAT achieves substantial improvements over strong baselines, including +1.35% on CREMA-D, +6.76% on Kinetic-Sound, and +1.92% on MVSA. The ablation study systematically validates each component (classifier freezing, alternating training, secondary updates, LoRA), and the t-SNE visualizations with quantitative clustering metrics provide compelling evidence of improved feature discriminability.

## Weaknesses
### Fatal
None.

### Major
- **Limited evaluation scope**: The paper evaluates on only three datasets, all of which are relatively small-scale (CREMA-D: ~7,442 samples, KS: ~10,000 samples, MVSA: ~4,500 samples). The claim of "over 30,000 samples" is modest by modern standards. The method should be validated on larger-scale multimodal benchmarks (e.g., VGGSound, AudioSet, or large-scale vision-language datasets) to demonstrate scalability and generalizability. Additionally, only audio-visual and text-image modality pairs are tested; the method's applicability to other modality combinations (e.g., video-text, 3D+RGB) is unclear.
- **Missing comparison with important baselines**: Several recent and relevant modality imbalance methods are not compared, including PMR (Fan et al., 2023), AGM (Li et al., 2023), CML (Ma et al., 2023), and MBSD (Liu et al., 2023), all of which are discussed in the related work section. The absence of these comparisons weakens the claim of "consistent SOTA improvements." The paper also does not compare with simple but strong baselines like gradient surgery or uncertainty weighting.
- **Computational cost and efficiency analysis is absent**: The two-stage training with bidirectional cross-attention pretraining, alternating updates, and sample-level secondary updates introduces significant computational overhead. The paper provides no analysis of training time, FLOPs, or parameter count compared to baselines. Given that LoRA is used for efficiency, it is important to quantify the actual efficiency gains or costs.

### Minor
- **Hyperparameter sensitivity is not fully explored**: While grid search results for LoRA rank and threshold β are provided, the paper does not analyze sensitivity to the regularization coefficient λ (fixed at 0.001) or the interaction between hyperparameters. The optimal β varies significantly across datasets (0.05 to 0.30), suggesting the method may require careful tuning for new datasets.
- **The mutual information estimation in Eq. (5) appears heuristic**: The formula uses a log-sum-exp approximation that is not standard mutual information estimation. The paper cites Zhou et al. (2025b) but does not justify why this particular formulation is appropriate or how it relates to true mutual information. This is a potential concern for the theoretical grounding of the contribution regularization.
- **The secondary update mechanism may introduce training instability**: Reprocessing severely imbalanced samples with additional gradient updates could lead to overfitting on those samples or cause the encoder to forget previously learned representations. The paper does not discuss or analyze this potential issue.

### Trivial
- The paper states "faithfully" at the end of the contributions list, which appears to be a typo or formatting artifact.

## Nice-to-Haves
- Analysis of the computational cost (training time, FLOPs, parameter count) compared to baselines.
- Evaluation on larger-scale datasets (e.g., VGGSound, AudioSet, or large vision-language benchmarks).
- Comparison with additional modality imbalance methods (PMR, AGM, CML, MBSD).
- Sensitivity analysis of the regularization coefficient λ.
- Discussion of potential failure cases or scenarios where CCAT might not help (e.g., when both modalities are equally weak, or when one modality is completely uninformative).

## Novel Insights
The paper's key insight is the formal connection between class imbalance and modality imbalance through gradient dynamics, showing that both problems exhibit a recursive cycle of early-dominance bias, gradient suppression, representation degradation, and preference entrenchment. This perspective is genuinely novel and provides a principled justification for transferring classifier-constraining strategies from class imbalance to multimodal learning. The observation that alternating training alone (as in MLA) fails to address classifier-level bias, and that freezing a pre-trained unbiased classifier can serve as a stable decision anchor, is a valuable contribution to understanding the limitations of existing approaches.

## Suggestions
- Add comparisons with PMR, AGM, CML, and MBSD to strengthen the SOTA claim.
- Include training time and parameter count comparisons to demonstrate efficiency.
- Evaluate on at least one large-scale dataset (e.g., VGGSound with >200K samples) to show scalability.
- Provide a more rigorous justification or alternative for the mutual information estimation in Eq. (5).
- Discuss potential overfitting concerns with the secondary update mechanism and how they are mitigated.

## Score and Decision
The paper presents a well-motivated, theoretically grounded, and empirically validated approach to a recognized problem in multimodal learning. The core idea of freezing a pre-trained unbiased classifier during alternating training is novel and addresses a genuine limitation of prior work. The experimental results are strong and the ablation study is thorough. However, the limited evaluation scope (only three small datasets, missing comparisons with several relevant baselines) and lack of computational cost analysis prevent the paper from being a clear accept. The contributions are solid but not transformative, and the evaluation needs to be more comprehensive to fully support the claims.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>