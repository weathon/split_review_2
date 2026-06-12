## Summary

This paper addresses modality imbalance in multimodal learning by proposing Classifier-Constrained Alternating Training (CCAT). The method first pre-trains a shared classifier with a regularization term that penalizes large disparities in modality contributions, then freezes this classifier during alternating training to prevent dominant modalities from biasing the decision boundary. Modality-specific LoRA adapters and sample-level secondary updates for severely imbalanced samples further enhance weak modality learning. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over state-of-the-art methods.

## Strengths

- **Clear identification of a key limitation in existing alternating training methods**: The paper convincingly demonstrates that encoder-level interventions alone are insufficient because the shared classifier develops an entrenched bias toward faster-converging modalities. This insight is well-motivated and supported by empirical tracking of modality contributions.
- **Novel analogy between class imbalance and modality imbalance**: Drawing a formal parallel through gradient dynamics (Section 3.1) provides a fresh theoretical perspective that connects two previously separate problems, offering a principled justification for applying classifier-constraining strategies to multimodal learning.
- **Well-designed two-stage framework with complementary components**: The combination of (1) contribution-aware classifier pretraining, (2) frozen classifier with LoRA adapters during alternating training, and (3) sample-level secondary updates is logically structured and each component is ablated to show its contribution.
- **Strong empirical results**: CCAT achieves substantial gains over strong baselines (e.g., +6.76% on Kinetic-Sound, +1.92% on MVSA) and the ablation study confirms that all components contribute to the final performance. The t-SNE visualizations with quantitative clustering metrics further support the claim that the fixed classifier yields more discriminative features.

## Weaknesses

### Major

- **Theoretical connection is not rigorously established**: Section 3.1 presents gradient approximations for class and modality imbalance, but the derivation assumes a linear classifier and ignores non-linearities, interactions, and the role of the encoder. The claimed "profound theoretical isomorphism" is more an intuitive analogy than a formal proof. The paper would benefit from a more careful treatment (e.g., discussing when the approximation holds, or providing empirical evidence of the similarity in gradient dynamics).
- **Mutual information estimation for contribution scores is under-justified**: Equation (5) uses a simplified estimator that may be biased and sensitive to batch size and feature dimensionality. The paper does not discuss the accuracy of this estimator, its variance, or whether alternative contribution measures (e.g., gradient norms, attention weights) would yield similar results. This is critical because the contribution scores drive both the regularization term and the sample-level secondary updates.
- **Hyperparameter sensitivity across datasets**: The optimal LoRA rank \(r\) and imbalance threshold \(\beta\) vary significantly across datasets (e.g., \(\beta=0.15\) for CREMA-D, \(\beta=0.30\) for KS, \(\beta=0.05\) for MVSA). This suggests the method may require careful tuning for new datasets, and the paper does not provide guidance on how to set these hyperparameters without a validation set. The sensitivity analysis (Figure 4) shows non-monotonic behavior, which could indicate instability.

### Minor

- **Limited baseline coverage**: The paper compares against methods up to 2024 (MLA, MMPareto, LFM) but does not include more recent 2025 works that also address modality imbalance (e.g., some methods cited in the paper itself, like Zhou et al. 2025b). Additionally, LFM results are missing on MVSA without explanation.
- **Inference procedure is a specific design choice**: The method uses decision-level fusion of unimodal predictions during inference. While this is consistent with the alternating training setup, it may not be optimal for all tasks, and the paper does not compare against feature-level fusion alternatives within the same framework.
- **Computational overhead not discussed**: The pretraining stage, LoRA modules, and secondary updates add computational cost. The paper does not report training time, parameter counts, or FLOPs compared to baselines, making it difficult to assess the efficiency trade-off.

### Trivial

- The word "faithfully" appears at the end of the contributions list (Section 1) as a stray word.
- Figure captions are duplicated in the extracted text (parser artifact).

## Nice-to-Haves

- An analysis of when the frozen classifier strategy might fail (e.g., when modalities are highly correlated or when the pretrained classifier itself is biased due to limited data).
- A comparison with alternative contribution estimation methods (e.g., gradient-based influence, attention weights) to validate the choice of mutual information.
- Experiments on a tri-modal dataset to test scalability, as mentioned in the Future Work section.

## Novel Insights

Beyond the paper's own contributions, the key insight is that modality imbalance and class imbalance share a common underlying mechanism: early dominance of one component (modality or class) biases the classifier, creating a self-reinforcing cycle that suppresses weaker components. This perspective suggests that techniques developed for class imbalance (e.g., classifier freezing, re-weighting) can be systematically transferred to multimodal learning, opening a new direction for cross-pollination between these fields.

## Suggestions

- Strengthen the theoretical section by either providing a more rigorous derivation (e.g., analyzing gradient dynamics in a simplified two-modality linear model) or reframing it as an empirical observation with supporting experiments (e.g., tracking gradient norms of each modality over time).
- Add a discussion of the mutual information estimator's limitations and consider ablating with alternative contribution measures to demonstrate robustness.
- Report computational cost (training time, parameter count) for CCAT and key baselines to help practitioners assess the trade-off.
- Include the missing LFM results on MVSA or explain why they are omitted.

## Score and Decision

**Score**: 6  
**Decision**: Accept

The paper addresses an important problem with a well-motivated solution, provides solid empirical validation, and offers a novel perspective that bridges class and modality imbalance. The weaknesses (theoretical rigor, sensitivity to hyperparameters, limited baseline coverage) are significant but not fatal; they can be addressed in a revision or future work. The contribution is above the acceptance threshold for ICLR.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>