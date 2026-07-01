## Summary

This paper addresses modality imbalance in multimodal learning by proposing Classifier-Constrained Alternating Training (CCAT). The key idea is to: (1) pre-train a shared classifier with a regularization term that penalizes large disparities in modality contributions to obtain an unbiased decision boundary, (2) freeze this classifier during alternating modality-wise training to prevent dominant modalities from biasing the classifier, (3) equip each modality with lightweight LoRA modules for modality-specific adaptation, and (4) apply sample-level secondary updates for severely imbalanced samples. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over state-of-the-art methods, with gains of +2.27%, +6.76%, and +1.92% respectively.

## Strengths

- **Novel connection between class imbalance and modality imbalance**: The paper draws an insightful analogy between these two problems through gradient dynamics analysis, providing a fresh theoretical perspective that motivates the frozen-classifier approach. This bridges two previously separate literatures and offers a principled justification for the proposed method.

- **Well-motivated and well-designed method**: Identifying that alternating training alone fails to address classifier bias (as demonstrated empirically in Figure 1) is a genuine insight. The two-stage framework—pretraining an unbiased classifier then freezing it during alternating optimization—is a clean solution that directly targets the identified limitation. The integration of LoRA modules elegantly resolves the distribution mismatch between fused and unimodal features.

- **Strong empirical results**: CCAT achieves substantial improvements across all three datasets, particularly on Kinetic-Sound (+6.76% over LFM). The ablation study systematically validates each component (classifier freezing, alternating training, secondary updates, LoRA), showing that all contribute to the final performance. The t-SNE visualizations with quantitative clustering metrics (CH, SH, DB) provide compelling evidence that the frozen classifier yields more discriminative feature representations.

- **Clear exposition and thorough experimental setup**: The paper is well-structured, with clear figures illustrating the framework. The baselines are comprehensive, covering simple fusion, modulation-based, and recent state-of-the-art methods. Evaluation includes both multimodal and unimodal performance, giving a complete picture.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical connection lacks rigor**: Section 3.1 argues for a "profound theoretical isomorphism" between class and modality imbalance, but the gradient analysis is a sketch rather than a formal proof. The analysis assumes a linear fusion model with scalar coefficients γ₁, γ₂, which does not reflect how most modern multimodal models (including CCAT's own cross-attention) actually learn modality contributions. The claim that class-imbalance-inspired strategies should transfer to modality imbalance is intriguing but not fully substantiated mathematically.

- **Incomplete evaluation metrics**: The paper reports only accuracy. If the datasets themselves have class imbalance (common in emotion recognition like CREMA-D), accuracy can be misleading. Metrics such as F1-score, AUC, or per-class recall would provide a more robust assessment, especially given that the method explicitly aims to improve representation for weaker modalities—which could be correlated with minority classes.

- **Limited analysis of the MI-based contribution estimation**: Equation (5) defines mutual information estimation but omits important practical details (nearest-neighbor estimator, bias correction, computational complexity). The use of softmax normalization (Eq. 6) on top of this estimate raises questions about whether the resulting "contribution scores" reliably reflect true modality influence, especially given the well-known challenges of MI estimation in high dimensions.

### Minor
- **LoRA motivation could be stronger**: While LoRA is a natural choice for PEFT, the paper does not compare against alternative approaches for handling the distribution mismatch (e.g., separate classifier heads per modality, or fine-tuning the classifier with per-modality batchnorm). The ablation removes LoRA entirely, but does not test whether a simpler adaptation method would suffice.

- **Hyperparameter sensitivity**: The method introduces several hyperparameters (λ for regularization, rank r, threshold β). While grid searches for r and β are shown, λ is fixed at 0.001 without sensitivity analysis. The optimal β varies significantly across datasets (0.05–0.30), suggesting that this threshold requires careful tuning per dataset.

- **Figure 1 caption error**: The caption states "The 'Ours' lines show a more pronounced imbalance" when the data actually shows that Ours achieves better balance (Modality B at 0.35 vs MLA's 0.10). This appears to be a wording error rather than a content flaw.

### Trivial
- The word "faithfully" at the end of the contributions list appears to be a stray artifact from editing.

## Nice-to-Haves

- A comparison against simply fine-tuning the classifier with a separate linear head for each modality (instead of LoRA) would clarify the specific benefits of the LoRA design.
- Analysis of computational overhead (training time, GPU memory) for the two-stage framework and the secondary update pass.
- Discussion of failure cases: when might the frozen classifier constraint hurt (e.g., if the pretrained classifier is itself poor, or if the distribution mismatch is extreme)?
- Per-class accuracy breakdown on CREMA-D to verify that the improvement does not come at the cost of already-well-classified emotions.

## Novel Insights

Beyond the paper's own contributions, the key insight is that *classifier bias can persist even after encoder-level decoupling* in alternating training. While prior work focused on gradient interference between encoders, this paper correctly identifies that the shared classifier retains a structural preference for the dominant modality, creating a bottleneck that weaker modalities cannot overcome. The analogy to class imbalance—where early dominance of majority classes skews decision boundaries—is not just a surface-level similarity but reveals that both problems share an underlying *path-dependent bias amplification* mechanism. This suggests that a broader class of architecture-level interventions (rather than just gradient modulation) may be necessary to achieve truly balanced multimodal learning.

## Suggestions

1. Strengthen the theoretical section by either providing a more formal analysis (e.g., convergence dynamics of the classifier weights under alternating training) or explicitly stating the limitations of the current sketch and framing it as motivation rather than proof.
2. Report F1-score, per-class accuracy, or AUC for all datasets to ensure the accuracy gains are not masking class-level degradation.
3. Add a discussion of how to set the threshold β in practice (e.g., heuristic based on validation set modality contribution percentiles), and include a sensitivity analysis for λ.
4. Briefly discuss the computational cost of the secondary update and pretraining stage relative to baselines like MLA.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: Accept