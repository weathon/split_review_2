## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA) for CLIP models, which replaces entropy-based confident view selection with a regression model that predicts cross-entropy loss from augmented-view logits. By training a lightweight decision tree (LightGBM) offline on pseudo-labeled data, RTA selects views with the lowest predicted loss at test time, demonstrating consistent improvements over existing TTA methods across single-label, multi-label, and cross-domain benchmarks.

## Strengths

- **Strong motivating analysis:** The "Ceiling TTA" experiments (Tables 1–2) convincingly show that label cross-entropy loss–based view selection massively outperforms entropy-based selection (e.g., ViT-B/16 on IN-A: 90.2% vs 64.3% with 64 views), providing clear motivation for the regression mapping approach.

- **Novel framework for view selection:** The core insight—that the mapping from logits to cross-entropy loss can be learned offline and used as a "free lunch" for view selection—offers a genuinely new direction for TTA research that departs from the entropy-minimization paradigm. This is supported by t-SNE visualizations (Figure 2) and Spearman correlation analysis (Figure 3).

- **Comprehensive and consistent empirical results:** RTA achieves state-of-the-art or competitive results across diverse benchmarks including ImageNet variants, 10 cross-domain datasets, and 3 multi-label datasets, using both RN50 and ViT-B/16 backbones. Multi-label gains are particularly strong (e.g., +3% mAP on NUSWIDE for RN50 over ML-TTA).

- **Simplicity and efficiency:** The approach requires only one offline training phase using 1,000 pseudo-labeled samples with a lightweight tree model (LightGBM, 100 rounds), and introduces negligible additional cost at test time—a practical advantage over methods requiring per-sample prompt updates or memory bank maintenance.

## Weaknesses

### Fatal
None.

### Major

- **Class-set mismatch between training and evaluation is unaddressed:** The regression model is trained on ImageVal-12k (ImageNet classes, 1000 classes), but evaluation spans datasets with different class sets (Pets: 37, Flowers: 102, Aircraft: 100, etc.). Since the decision tree operates on the logit vector whose dimensionality equals the number of classes, the regression model cannot directly generalize across class sets. The paper does not explain how this mismatch is handled—whether the model is retrained per dataset (contradicting "train once, adapt to any test distribution"), or whether all evaluations use a fixed class prompt set. This ambiguity affects the credibility of the generalization claims and the "train once" advantage emphasized throughout the paper.

- **Cross-domain gains are marginal and inconsistent:** For ViT-B/16 on the 10 cross-domain datasets, RTA achieves 68.70% average accuracy versus BCA's 68.59%—a difference of only 0.11%. Moreover, RTA loses to BCA on 5 out of 10 individual datasets (Pets: −0.45%, Flowers: −1.32%, DTD: −3.04%, EuroSAT: −2.98%, SUN: −0.29%). The paper does not acknowledge these losses or discuss where the method falls short, presenting only the average comparison.

### Minor

- **Multi-label method extension is not described:** Multi-label results are presented in Tables 5–6 with significant gains, but the method section only details the single-label formulation (Equations 2–10, Algorithms 1–2). It is unclear how the regression loss is computed for multi-label settings (binary cross-entropy per class? which classes?), how pseudo-labels are obtained, and whether the same regression model handles both single- and multi-label scenarios.

- **Gap between regression and ceiling remains large:** For ViT-B/16 on IN-A with 64 views, the ceiling (LCE) is 90.2% while RTA achieves 65.65%—a 24.55% gap. While this validates the potential for improvement, it also raises the question of whether a more expressive regression model (e.g., neural network) could significantly close this gap, which would strengthen the contribution.

- **Limited regression model exploration:** The paper uses only LightGBM without ablation on alternative regression models (neural networks, random forests, etc.). Given that the non-linear relationship shown in Figure 2 is a key claim, comparison with non-linear alternatives would strengthen the methodological contribution.

### Trivial
None.

## Nice-to-Haves

- A visualization of the regression-predicted loss vs. actual loss on held-out data to quantify how well the regression model approximates LCE across different domains.
- Analysis of failure cases or domains where RTA underperforms entropy-based methods.
- Discussion of sensitivity to the pseudo-label confidence threshold (0.8) used for regression data selection.

## Novel Insights

The paper's most valuable insight is that the information needed for confident view selection is not limited to the current test instance's probability distribution—the logits of augmented views contain structural information about their predictive quality that can be captured by a regression model trained offline on diverse data. This reframes TTA view selection as a supervised learning problem (learn a mapping from logits to loss) rather than an unsupervised one (minimize entropy), which is a conceptual shift that could inspire follow-up work using more sophisticated regression models or alternative supervision signals.

## Suggestions

- Clearly describe how the regression model handles different class sets across evaluation benchmarks, and ensure the "train once" claim accurately reflects the experimental setup.
- Add an explicit multi-label formulation section or subsection explaining the loss computation and pseudo-labeling for multi-label scenarios.
- Report per-dataset results in the cross-domain comparison with honest acknowledgment of datasets where RTA underperforms baselines.
- Include ablation experiments comparing LightGBM with at least one neural regression model to justify the choice.

## Score and Decision

The paper introduces a genuinely novel framework for TTA view selection that departs from entropy minimization, supported by strong motivating analysis. However, the unresolved class-set mismatch question, marginal cross-domain improvements, and incomplete method description for multi-label settings prevent a stronger recommendation. The consistent improvements on ImageNet variants and multi-label benchmarks, combined with the simplicity of the approach, place this at the borderline.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept