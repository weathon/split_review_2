## Summary
# Final Review Report

## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA) for vision-language models (CLIP). The core idea is to train a regression model (LightGBM decision tree) that maps the logits of augmented views to their cross-entropy loss, then select views with the smallest predicted loss for ensembling at test time. The method's key motivation is that using true label cross-entropy (LCE) for view selection dramatically outperforms entropy-based selection (20-30 point gaps), suggesting that approximating this loss function via regression could improve TTA.

The paper demonstrates substantial experimental scope: single-label classification on ImageNet and 5 variants, 10 cross-domain datasets, and 3 multi-label datasets, using both RN50 and ViT-B/16 backbones. Average gains over entropy-based methods are in the range of 1-6 percentage points depending on setting.

**Major strengths:** (1) The core observation—that LCE-based selection far exceeds entropy-based selection—is clearly demonstrated and provides a strong motivation. (2) The method is computationally lightweight (single offline training, fast decision-tree inference). (3) The experimental evaluation is broad, covering single-label, cross-domain, and multi-label settings.

**Major weaknesses:** (1) Several claims exaggerate the scope of validation, particularly "across all distributions" and "arbitrary test distributions" when only ImageNet-family datasets are tested. (2) Statistical significance is unreported—all results are single numbers without variance, making it impossible to assess whether small margins (0.2-1.6 points) are genuine or noise. (3) The pseudo-labeling procedure creates a circular dependency (CLIP's own confidences are used to train the regressor that selects views for CLIP), with no analysis of failure cases when CLIP is confidently wrong. (4) The claim "consistently outperforms" is contradicted by Table 4 where BCA outperforms RTA on 5 of 10 cross-domain datasets. (5) No regression quality metrics (predicted vs. true loss correlation) are reported to validate that the decision tree actually learns the claimed mapping.

## Strengths
1. **Well-motivated empirical observation.** The paper begins with a strong empirical finding: using true label cross-entropy (LCE) for view selection achieves 20-30 percentage points higher accuracy than Shannon entropy (Tables 1-2). This establishes a clear performance upper bound and provides compelling motivation for learning to approximate LCE.

2. **Computationally efficient design.** RTA trains a single LightGBM model once on 1,000 pseudo-labeled samples, then performs zero-shot inference at test time without per-instance adaptation or memory buffers. This is a practical advantage over methods that require per-sample prompt tuning (TPT, DiffTPT) or dynamic cache management.

3. **Broad and consistent evaluation.** The paper evaluates across 18 datasets covering single-label (ImageNet, 4 variants, 10 cross-domain), and multi-label (MSCOCO, VOC2007, NUSWIDE) settings with two backbone architectures (RN50, ViT-B/16). This is substantially more comprehensive than most TTA papers.

4. **Clear writing structure.** The method presentation (Section 4) follows a logical progression: motivation via Ceiling TTA → visualization (t-SNE, Spearman correlation) → regression learning → deployment. Algorithms 1 and 2 provide explicit pseudocode.

5. **Relevant related-work comparison.** The discussion of Kim et al. (2020) as the most closely related prior work correctly identifies the key differences (supervised vs. unsupervised, deep NN vs. tree-based, in-domain vs. cross-domain), helping readers position the contribution.

## Weaknesses
### W1. Exaggerated generalization claims (Severity: Major)
**Evidence:** The paper repeatedly claims RTA can "adapt to test instances with arbitrary distributions" (Page 1 - Introduction, Contribution bullet 3) and that the regression relationship holds "regardless of the distribution of test instances" (Page 1 - Introduction). However, all experiments use ImageNet-family datasets (same 1000-class label space) or standard cross-domain benchmarks with similar visual domains. No evaluation is conducted on truly out-of-domain distributions (medical, satellite, art, or sketch datasets with different label spaces). The regression model is trained on ImageNet validation data (ImageVal-12k), which shares the same label distribution as the test datasets.

**Impact:** Claims of "arbitrary distribution" generalization are unsupported. A reviewer familiar with domain generalization literature will identify this as overclaiming.

**Fix:** Replace "arbitrary" and "all distributions" with bounded language specifying the tested scope (ImageNet-family distributions, standard cross-domain benchmarks). Add caveats about the shared label-space assumption. Conduct at least one experiment on a dataset with a different label space to substantiate broader generalization claims.

### W2. Missing statistical significance (Severity: Major)
**Evidence:** All reported results (Tables 3-6) are single accuracy/mAP numbers without standard deviations, confidence intervals, or significance tests. The improvements are often small—e.g., ViT-B/16 on ImageNet-1k: RTA 71.13% vs. Zero 70.89% (+0.24%), on ImageNet-A: RTA 65.65% vs. Zero 64.03% (+1.62%). Without variance estimates, these margins cannot be distinguished from random seed noise.

**Impact:** Core claim that RTA "significantly outperforms" existing methods is unverifiable. The paper cannot rule out the possibility that gains are within run-to-run variance of CLIP-based methods.

**Fix:** Report mean ± std over at least 3 random seeds for all main results. Add a paired significance test (Wilcoxon signed-rank or paired t-test) comparing RTA against the strongest baseline on each dataset. Mark statistically significant gains.

### W3. Pseudo-label circular dependency (Severity: Major)
**Evidence:** The regression target (pseudo cross-entropy loss) is derived from CLIP's own high-confidence predictions (threshold ≥ 0.8, Page 4 - Regression Mapping Learning). This means the regression model learns to predict low loss for views consistent with CLIP's confident predictions. When CLIP is confidently wrong (a known failure mode on ImageNet-A, where top-1 accuracy is only 23-50%), the regression model will assign low predicted loss to confidently incorrect views.

**Impact:** The fundamental question is whether RTA genuinely selects better views or merely reinforces CLIP's existing confident-but-sometimes-wrong predictions. Without analyzing this failure mode, the method's mechanism remains unclear.

**Fix:** (1) Add an ablation analyzing the accuracy of regression loss predictions (correlation between predicted and true loss on held-out labeled data). (2) Report how often CLIP's high-confidence predictions are incorrect on each dataset, and analyze whether RTA handles these cases differently from entropy-based selection. (3) Compare against a negative control where the regression target is replaced by random pseudo-labels.

### W4. Factual inaccuracy: "consistently outperforms" contradicts Table 4 (Severity: Major)
**Evidence:** Page 7 - Cross-domain classification states RTA "consistently outperforms prior adaptation methods." In Table 4 (ViT-B/16), BCA outperforms RTA on 5 of 10 datasets (Pets 90.43 vs. 89.98, Flowers 73.12 vs. 71.80, DTD 53.49 vs. 50.45, EuroSAT 56.63 vs. 53.65, SUN 68.41 vs. 68.12). RTA only has a higher average because of larger gains on Aircraft, Cars, and Caltech.

**Impact:** This is a factual error that weakens the paper's credibility. Selective reporting of average performance while ignoring individual dataset results is misleading.

**Fix:** Revise the text to honestly report mixed results: "RTA achieves competitive average accuracy and excels on fine-grained tasks (Aircraft, Cars) and large-scale recognition (Caltech), while BCA performs better on texture (DTD), satellite (EuroSAT), and fine-grained pet/flower datasets."

### W5. No regression quality metrics (Severity: Major)
**Evidence:** The paper claims a "strong regression mapping" between logits and label cross-entropy loss (Section 4.1), and trains a decision tree to predict this loss (Section 4.2). However, no metrics are reported to validate how well the regression model predicts the actual loss. The Spearman correlation analysis (Figure 3) only examines top-10 individual logit features, not the full model's predictive accuracy.

**Impact:** Without regression quality validation (e.g., R², Spearman ρ between predicted and true loss on validation data), readers cannot assess whether the decision tree learns a meaningful mapping or overfits to the 1,000 training samples.

**Fix:** Report the correlation between RTA's predicted loss and the actual label cross-entropy loss on a held-out validation set. Show a scatter plot akin to Figure 2 but with predicted vs. actual loss.

### W6. Ceiling TTA gap unquantified (Severity: Minor)
The LCE oracle (Ceiling TTA) achieves 85-90% accuracy while RTA achieves 62-71%—a ~20-point gap. The paper does not discuss how much of this gap RTA recovers or whether the gap is due to regression approximation error or fundamental limitations of the pseudo-label approach.

### W7. Reproducibility gaps (Severity: Minor)
The augmentation pipeline is not specified (what transformations for N=64 views?). The CLIP model version used for confidence filtering is ambiguous. No random seed is reported.

### W8. Multi-label result scope (Severity: Minor)
The multi-label results are compared only against TTA methods, but the text "new optimal result" could mislead readers. Dedicated supervised multi-label methods achieve much higher mAP; this context should be explicitly stated.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a well-motivated idea—regression-based view selection for CLIP test-time adaptation—with broad experimental coverage across 18 datasets. The core observation that label cross-entropy dramatically outperforms Shannon entropy for view selection is compelling and provides clear motivation. The computational efficiency of the method is a practical strength.

However, the paper is held back by five major weaknesses that collectively reduce confidence in the results: (1) generalization claims are exaggerated beyond the tested scope, (2) all results lack statistical variance estimates, making small-margin improvements unverifiable, (3) the pseudo-label circular dependency (training on CLIP's own confident predictions) is not analyzed as a potential failure mode, (4) the claim of "consistently outperforms" is factually contradicted by Table 4 where a baseline beats RTA on 5 of 10 cross-domain datasets, and (5) no regression quality metrics are reported to validate that the decision tree actually learns the claimed mapping.

The paper has potential and the core idea is sound, but the current evidence is insufficient to support the strength of the claims. A major revision addressing statistical rigor, claim calibration, and failure-mode analysis is needed before the paper meets a publishable standard.

**Post-Revision Target: [7, 8]/10** — If the authors address overclaiming (W1, W4), add variance reporting (W2), analyze the pseudo-label circularity (W3), and validate regression quality (W5), the paper could become a solid contribution to the TTA literature.