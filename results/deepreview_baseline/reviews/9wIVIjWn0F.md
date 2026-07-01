## Summary

The paper proposes **Regression-based Test-time Adaptation (RTA)** for vision-language models (e.g., CLIP). Instead of using entropy to select confident augmented views, RTA learns a decision-tree regression model that maps from view logits to cross-entropy loss (w.r.t. pseudo-labels). Trained once offline on diverse unlabeled data, the regressor predicts the loss for each augmented view at test time; the top-\(k\) views with smallest predicted loss are ensembled. Extensive experiments on single-label, multi-label, and cross-domain benchmarks show that RTA outperforms existing entropy-based TTA methods with negligible additional cost.

## Strengths

- **Novel perspective on TTA view selection**: Shifting from entropy-based confidence to a learned regression mapping between logits and cross-entropy loss is a well-motivated and original idea. The “ceiling” analysis using ground-truth loss clearly demonstrates the potential of this approach.
- **Strong empirical performance**: RTA achieves state-of-the-art or competitive accuracy across a wide range of benchmarks (ImageNet variants, 10 cross-domain datasets, multi-label datasets) for both RN50 and ViT-B/16 backbones, often with clear margins.
- **Practical efficiency**: The regression model (LightGBM) is trained once on a small subset (1,000 samples) of a diverse dataset, and test-time inference is simple—no prompt updates, no memory caches, no per-instance fine-tuning. This makes the method lightweight and easy to deploy.
- **Thorough ablation and analysis**: The paper examines the effect of the number of augmented views and the number of regression samples, providing practical guidance and confirming that performance saturates gracefully.

## Weaknesses

### Fatal
None.

### Major
1. **Bias from pseudo-labeled training data**: The regression model is trained on pseudo-labels obtained from CLIP predictions filtered at confidence ≥0.8. This biases the mapping toward samples that CLIP already classifies confidently, potentially missing the relationship for challenging, low-confidence views that TTA most needs to evaluate. The paper does not discuss the impact of incorrect pseudo-labels or how the mapping might fail for out-of-distribution views.
2. **Training vs. inference input mismatch**: The regression model is trained on logits from original (non-augmented) images, but applied at test time to logits from augmented views. Augmented views can have very different logit distributions (especially under strong augmentation). The paper provides no analysis or justification that the mapping learned on original images transfers reliably to augmented views.
3. **Lack of theoretical grounding**: The claim that the view-loss mapping is distribution-agnostic is supported only by Spearman correlation on a few examples and t-SNE visualizations. No theoretical analysis or formal guarantee is given, so the method’s robustness across diverse unseen distributions remains an empirical observation without deeper understanding.

### Minor
- Notation inconsistency in Section 4.3: Equation (8) uses \(x_i^{\text{reg}}\) when it should refer to test instances.
- The paper states that the original image “can be regarded as a view” to justify training on non-augmented images, but this simplification is not validated experimentally.
- In several tables (e.g., Table 4, RN50), RTA results are bolded even when the method does not achieve the best accuracy on that specific dataset, which could mislead readers about fine-grained comparisons.
- The claimed “negligible additional cost” is not quantified (e.g., runtime in milliseconds per instance compared to entropy-based methods).

### Trivial
- Figure captions are duplicated and contain extra explanatory text that seems intended for the actual figures.

## Nice-to-Haves

- An ablation comparing the regression mapping trained on original images vs. on augmented views would clarify the training-inference gap.
- A per-sample analysis showing when the predicted loss correlates well (or poorly) with the actual loss, especially on OOD cases.
- A discussion or experiment on the effect of different pseudo-label confidence thresholds and how they trade off between quantity and correctness of training samples.

## Novel Insights

The core insight—that a pre-trained regressor on logits can predict “which augmented views are likely to have low cross-entropy loss” without seeing the label—is a fresh alternative to entropy minimization. It reframes TTA view selection as a regression problem that can leverage offline data, separating the confidence estimation from the current test instance. This opens the possibility of building task-agnostic confidence predictors for TTA, though the paper’s dependence on pseudo-labels and the original-image training scheme needs further validation.

## Suggestions

- Provide a direct comparison of the regression model’s predicted loss vs. actual loss on a held-out set of augmented views to verify generalization.
- Include a brief runtime analysis (e.g., ms per instance) comparing RTA to entropy-based methods to substantiate the “negligible cost” claim.
- Discuss potential negative impact of pseudo-label noise and consider using soft labels or uncertainty-aware training for the regressor.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>