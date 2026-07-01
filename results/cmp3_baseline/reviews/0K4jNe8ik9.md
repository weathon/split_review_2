## Summary

This paper proposes DGNet, a self-supervised contrastive learning framework for EEG-based dementia classification. The method decomposes raw EEG signals into five canonical frequency bands (delta, theta, alpha, beta, gamma), processes each band with an independent CNN encoder and projection head, and employs an adaptive NT-Xent loss with per-band learnable temperatures. Pre-training is done via SimCLR-style instance discrimination on unlabeled data, followed by linear evaluation for AD vs CN classification. The authors report 92.90% accuracy and 92.85% F1-score on a dataset of 88 subjects, outperforming several baseline models.

## Strengths

- **Neurophysiologically motivated design.** Decomposing EEG into frequency bands and learning separate representations aligns with known spectral biomarkers of dementia, making the approach principled for the problem domain.
- **Comprehensive ablation study.** The paper systematically ablates self-supervised learning, multi-head architecture, data augmentation, adaptive temperature, and regularization, providing insight into which components matter.
- **Strong reported results.** The claimed accuracy and F1 (both ~93%) are high compared to the baselines listed, suggesting the method has potential.

## Weaknesses

### Fatal
None.

### Major

1. **No error bars or statistical significance anywhere in the main results (Tables 1, 2, 3).** All metrics are reported as point estimates without standard deviations, confidence intervals, or p-values. On a dataset of only 88 subjects, this is a critical omission — readers cannot assess whether the reported gains are reliable or due to chance. This alone undermines the central claim of state-of-the-art performance.

2. **Baseline comparisons are questionable and likely unfair.** Many baseline models (e.g., EEGNet 46%, Deep4Net 49%, EEGInception 39%) perform far below typical AD-vs-CN classification accuracy on similar EEG data (commonly 70–90%). The paper does not describe how these baselines were tuned, whether they used the same data splits, same preprocessing, or same linear evaluation protocol. The suspicion is that the baselines were not properly optimized, making the claimed superiority an artifact of weak comparators.

3. **Inconsistent and potentially incorrect relative improvement numbers.** The abstract states “31.5% relative performance improvement over training from scratch, and a 25.4% improvement over the single-head approach.” Computing from Table 3: (92.90−63.35)/63.35 ≈ 46.6% relative improvement over scratch, and (92.90−73.52)/73.52 ≈ 26.4% over single-head. The reported percentages do not match the data, indicating either a miscalculation or a different formula (e.g., relative to the maximum possible improvement?), which is never explained.

4. **The dataset contains three groups (AD, FTD, CN) but experiments only evaluate AD vs CN.** The paper collects FTD data and mentions it in the dataset description but never reports results for AD vs FTD or three-way classification. This is a missed opportunity to demonstrate clinical relevance and leaves the scope of the claimed “dementia classification” incomplete.

5. **Ablation study structure is confusing and lacks a controlled isolation of SSL.** The row “Multi-head (5 heads)” at 79.55% already includes self-supervised pre-training and multi-head, while the “w/o SSL” row at 63.35% removes SSL entirely. The contribution of SSL itself is not separable from the multi-head architecture in the ablation. The jump from 79.55% to 86.53% (adding adaptive temperature) and from 86.53% to 90.64% (adding regularization) is very large and requires explanation — why would adaptive temperature alone give a 7% gain?

### Minor

- The loss equation (1) is notationally overloaded and appears to contain an outer sum over bands already indexed inside, making it hard to parse. The connection to the standard NT-Xent loss (Equation 2) is not clearly explained.
- The paper claims “state-of-the-art performance in multi-head approaches” but never defines what constitutes a “multi-head approach” in the literature, making this claim unverifiable.
- The introduction is excessively verbose and repetitive, taking many paragraphs to state the well-known motivation of EEG for dementia screening.
- The adaptive temperature mechanism is cited from Wang et al. (2024) but the paper does not clarify what is novel beyond applying it to band-level heads.

### Trivial

- Figure 1 caption appears three times in the PDF (likely a parsing artifact).
- The term “Adaptive Multi-head Contrastive Learning (AMCL)” appears only in the conclusion without being introduced earlier.

## Nice-to-Haves

- Include standard deviations (or confidence intervals) across LOSO folds for every metric in all tables.
- Report results on AD vs FTD and three-way classification to increase clinical utility.
- Provide a detailed description of how each baseline was tuned (e.g., learning rate search, architecture-specific preprocessing) to ensure fair comparison.
- Add an ablation row for “SSL + single head” to isolate the benefit of multi-head from SSL itself.
- Release code to facilitate reproducibility.

## Novel Insights

None beyond the paper’s own contributions. The idea that different EEG frequency bands should be processed by separate encoders and heads in a contrastive learning setup is sensible but not theoretically deepened. No analysis is offered on why adaptive per-band temperatures help, which bands are most discriminative, or how the learned representations differ across bands.

## Suggestions

1. Re-run all experiments and report mean ± std over LOSO folds for every metric. Without this, the paper’s claims are not scientifically defensible.
2. Recompute relative improvements consistently and correct the abstract.
3. Include complete baseline tuning details; if reproducing baselines is difficult, consider using a standardized benchmark (e.g., with pre-extracted features or a public toolbox).
4. Add experiments that leverage the FTD group (AD vs FTD, or three-class) to demonstrate the method’s generality.
5. Restructure the ablation so that each component is added incrementally from a common baseline (e.g., from a vanilla SSL single-head encoder).

## Score and Decision

The core idea is reasonable and the reported numbers are impressive, but the evaluation has major flaws — most critically the absence of any variance measure, questionable baseline comparisons, and inconsistent reporting. These issues prevent the paper from providing reliable evidence for its claims. I recommend rejection in its current form.

MY FINAL SCORE: 4score
MY FINAL DECISION: Rejectdecision