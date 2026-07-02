## Summary

This paper proposes Regression-based Test-time Adaptation (RTA) for CLIP-based image classification. The key insight is that ground-truth label cross-entropy loss (LCE) is a dramatically better criterion for selecting confident augmented views than Shannon entropy (Ceiling TTA experiments in Tables 1–2 show gains of 20+ points over entropy). To exploit this without labels, RTA trains a LightGBM regression model on pseudo-labeled data (ImageVal-12k, filtered by CLIP confidence ≥ 0.8) to predict LCE from per-view logits. During TTA, views with the lowest predicted loss are selected for ensembling. The method is evaluated on single-label (5 ImageNet variants), cross-domain (10 datasets), and multi-label (3 datasets) benchmarks with two backbones.

## Strengths

1. **Well-motivated core insight with compelling upper-bound evidence (Tables 1–2).** The Ceiling TTA experiments cleanly demonstrate that LCE-based view selection far exceeds entropy-based selection — e.g., CLIP ViT-B/16 with 64 views reaches 90.2% on ImageNet-A via LCE vs. 64.3% via entropy. This motivates the pursuit of a learnable loss predictor effectively.

2. **Broad and thorough evaluation scope.** The paper covers 5 ImageNet variants (single-label), 10 cross-domain datasets, and 3 multi-label benchmarks (MSCOCO, VOC2007, NUSWIDE) with two architectures (RN50, ViT-B/16). Few TTA papers offer this breadth.

3. **Convincing multi-label improvements (Tables 5–6).** RTA shows its strongest relative gains in multi-label classification — e.g., +1.67% mAP over ML-TTA on MSCOCO (RN50) and +1.47% on VOC2007 (ViT-B/16). These are the paper's most empirically compelling results.

4. **Consistent OOD improvements.** RTA outperforms all baselines on ImageNet-A (e.g., RN50: 36.79% vs. BCA's 30.35%, a +6.44% gain) and achieves top average OOD accuracy across ImageNet variants, demonstrating genuine robustness to distribution shift.

## Weaknesses

### Major

1. **Distribution overlap between regression training data and the ImageNet-1k test set.** The regression model is trained on ImageVal-12k (a subset of the ImageNet validation set), while the IN-1k test data in Table 3 is also drawn from the ImageNet validation set. This means the ImageNet-1k results partially reflect in-distribution evaluation, not the "arbitrary test distribution" generalization the paper claims. This does not affect the OOD benchmarks (ImageNet-A, V2, R, Sketch, cross-domain), which are more credible, but it weakens the most standard benchmark result. The paper should explicitly acknowledge this and ideally train the regression model on a genuinely separate dataset for the IN-1k evaluation.

2. **The regression model's predictive accuracy is not directly validated.** The paper shows that RTA's final accuracy improves over baselines, but never directly verifies that the regression model is accurately predicting LCE. There is no scatter plot of predicted vs. actual LCE on held-out views, no R² or Spearman correlation between predicted and true loss, and no analysis of how prediction error varies with pseudo-label quality. The t-SNE (Fig 2) and Spearman correlation (Fig 3) establish a relationship between logits and LCE in the input space, but these do not measure the trained model's predictive fidelity. This is a gap: if the regression model is the core contribution, its actual predictive behavior should be validated directly, not only through downstream accuracy.

### Minor

3. **The regression model's improvements over strong baselines are uneven and sometimes very small.** While RTA consistently outperforms baselines, the margins vary widely. On cross-domain benchmarks with ViT-B/16, RTA's average is 68.70% vs. BCA's 68.59% (+0.11%). On IN-1k with ViT-B/16, RTA achieves 71.13% vs. Zero's 70.89% (+0.24%). These tiny margins raise the question of statistical significance (no error bars are reported anywhere in the paper). Conversely, on ImageNet-A with RN50, RTA's +6.44% over BCA is substantial. The paper would benefit from acknowledging this variability and discussing why the method excels on some distributions more than others.

4. **No ablation against simple confidence-based view selection.** The regression model is trained on pseudo-labeled data filtered by CLIP confidence ≥ 0.8, and is effectively learning a proxy for CLIP's own confidence. The paper never compares against the simplest baselines: (a) selecting top-k views by max softmax probability, (b) selecting by max logit value, or (c) a linear regression from logits to loss. Without these, it is unclear whether the non-linear regression structure adds value beyond a roundabout version of confidence-thresholding. This is an important ablation for understanding what RTA actually contributes mechanistically.

5. **Pseudo-label quality is unexamined.** The regression training depends entirely on CLIP's own high-confidence predictions as pseudo-labels (threshold ≥ 0.8). The paper does not report the accuracy of these pseudo-labels on ImageVal-12k, how the threshold of 0.8 was chosen, or what fraction of samples are below threshold. If pseudo-labels are noisy, the regression target is noisy, which would explain the gap between RTA and the LCE ceiling. This analysis is needed to assess the method's limitations.

6. **"Free lunch" framing overstates the simplicity.** Training the regression model requires running CLIP forward passes on a separate dataset, storing the regression model, and loading it during TTA. While the per-instance cost is low, the setup is not zero-cost. The framing should be toned down.

### Trivial

7. **Minor imprecision in method description.** Section 4.2 and Algorithm 1 describe fitting a single "regression decision tree" (Eqs. 5–7), but the implementation uses LightGBM, which trains a gradient-boosted ensemble of trees. While each individual tree has the form described, the overall model is a sum of trees. This should be clarified for reproducibility.

## Nice-to-Haves

- Train the regression model on a dataset completely unrelated to ImageNet (e.g., only on domain-general data) to demonstrate that the logits-to-loss mapping truly generalizes across arbitrary distributions, strengthening the paper's core claim.
- Show scatter plots and R² / Spearman correlation between predicted LCE and actual LCE (using ground-truth labels on a held-out set) to directly validate that the regression model is learning the intended mapping.
- Report error bars or confidence intervals for main results, especially where margins over baselines are small (<0.5%).
- Analyze feature importance from the LightGBM model to understand which logit dimensions are most predictive of LCE.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Criticism that t-SNE shows correlation for original images, not augmented views (Critic's Sec-by-Sec notes).** The paper explicitly states (line 112) that t-SNE was performed on "all views of individual instances" — i.e., augmented views. This criticism is factually incorrect.
- **Criticism framed as "empirical contribution not commensurate with stated motivation" / "structural issue" about RTA not reaching the LCE ceiling.** The LCE ceiling uses ground-truth labels and is explicitly presented as an unattainable upper bound. RTA uses pseudo-labels and outperforms all strong baselines. The observation that RTA doesn't reach the oracle is not a flaw — it is expected. The core claim is that RTA outperforms entropy-based methods, which it does. The underlying concern about limited improvement magnitude is preserved in Weakness #3 (above), but the framing as a "structural/fatal" issue is removed as it misreads the paper's stated goals.
- **Request for error bars as a standalone weakness.** Merged into Weakness #3 as part of the discussion of small margins.
- **Comment about missing related work (confidence-based TTA approaches).** Per policy, missing related work is not flagged. The paper already discusses the closest prior work (Kim et al. 2020, Zero, TPT, etc.).

## Novel Insights

None beyond the paper's own contributions. The harsh review's central observation — that the gap between the LCE oracle ceiling and RTA's actual results is large — is valid as a discussion point but does not constitute a novel insight about the paper beyond what is already evident from the results tables.

## Suggestions

1. **Validate the regression model directly.** Add a scatter plot of predicted vs. actual LCE on held-out views (with ground-truth labels for evaluation only), and report the Spearman correlation or R². This is the single most important addition to support the paper's mechanistic claims.
2. **Add simple baseline ablations:** compare against max-softmax-probability view selection and a linear regression predictor. This isolates whether the non-linear tree structure adds value.
3. **Address the distribution overlap.** Either train the regression model on a non-ImageNet dataset for the IN-1k evaluation, or explicitly acknowledge the overlap and discuss its impact.
4. **Report pseudo-label accuracy** on the ImageVal-12k pool and justify the 0.8 threshold choice.
5. **Add error bars** (at least for the main Table 3 results) and discuss statistical significance, especially for results with sub-0.5% margins.
6. **Clarify that LightGBM is an ensemble of trees** in Section 4.2, not a single tree, and update Algorithm 1 accordingly.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>