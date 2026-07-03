Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA) for CLIP models. The core idea is to train a lightweight LightGBM regression model on pseudo-labeled data to predict cross-entropy loss from view logits, then use predicted loss (rather than entropy) to select confident views during TTA. The paper first demonstrates a "Ceiling TTA" experiment showing that using true-label cross-entropy for view selection dramatically outperforms entropy-based selection (e.g., 90.2% vs 64.3% on ImageNet-A with ViT-B/16), which motivates the regression approach. RTA is evaluated on ImageNet variants, cross-domain, and multi-label benchmarks, showing consistent improvements over prior TTA methods.

## Strengths

1. **Ceiling TTA analysis (Tables 1 and 2)**: The paper provides clear empirical evidence that view selection via ground-truth label cross-entropy loss (LCE) far surpasses entropy-based selection — e.g., on ImageNet-A with 64 views and ViT-B/16, LCE achieves 90.2% vs entropy's 64.3%, a gap of 25.9 percentage points. This cleanly motivates the paper's central thesis that predicting LCE is worth pursuing, and the experimental design (varying the number of views, testing multiple backbones/datasets) makes this a convincing and self-contained finding.

2. **Broad and consistent evaluation**: RTA is tested across 5 ImageNet variant datasets, 10 cross-domain datasets, and 3 multi-label datasets, for both RN50 and ViT-B/16 backbones. It outperforms prior methods on average across all three evaluation families. The multi-label results are particularly strong (e.g., +1.43–1.67% mAP over ML-TTA on MSCOCO, +2.63–3.18% mAP over TDA on VOC2007), demonstrating that the regression approach transfers to settings beyond the single-label classification where it was motivated. This breadth of evaluation is notably more extensive than many TTA papers.

3. **Training-once, zero-update paradigm**: RTA trains a single LightGBM model (max depth 5, 16 leaves) on 1,000 pseudo-labeled samples and applies it to any test distribution without per-dataset fine-tuning, prompt updates, or memory banks. This is a qualitatively different design from both cache-based methods (which need continuous updates) and instance-level prompt-tuning methods (which re-optimize per test sample), and the paper shows it works across widely different distributions without any adaptation.

## Weaknesses

### Major

- **Regression training data overlaps with the IN-1k test distribution (Table 3).** The regression model is trained on ImageVal-12k (the ImageNet validation set, Section 5.1), which shares the same distribution as the ImageNet-1k test set. Every baseline in Table 3 (TPT, DiffTPT, Zero, BCA, etc.) operates under the standard TTA protocol with no data from the test distribution. This gives RTA a structural advantage on IN-1k that is unrelated to the TTA procedure. Importantly, this does **not** affect the OOD results (IN-A, IN-R, IN-V2, IN-K — those datasets are genuinely distribution-shifted from ImageNet) or the cross-domain / multi-label results. The paper should explicitly acknowledge this limitation and, ideally, re-run the IN-1k experiment with a regression dataset that shares no distributional overlap with any evaluation benchmark.

### Minor

- **Gains over strong baselines are modest in several settings, and no error bars are reported.** For ViT-B/16 on ImageNet-1k, RTA (71.13%) improves over Zero (70.89%) by only 0.24 pp. On IN-R the gain over Zero is 0.23 pp. On cross-domain (Table 4, ViT-B/16), RTA's average (68.70%) barely edges past BCA (68.59%), and on several individual datasets (Pets, Flowers, DTD, EuroSAT) a non-RTA method holds the best result. No standard deviations or confidence intervals are reported anywhere, making it impossible to assess whether the sub-1% margins are meaningful.

- **Missing ablation: direct comparison against "max-probability" view selection.** The regression target is pseudo-label cross-entropy loss (−log(p_max)), which when one class dominates is monotonically related to entropy. The paper does not compare RTA against a simpler baseline that selects views with the highest CLIP softmax probability on the predicted class (a "max-prob" heuristic). Without this ablation, it is unclear whether RTA's gains come from the regression mapping itself or from the view-selection-and-ensemble protocol that any reasonable selection rule would provide.

- **Regression model trained only on high-confidence samples, but tested on all samples.** Pseudo-labels are obtained by filtering CLIP predictions with confidence ≥ 0.8 (Section 5.1). The regression model is thus trained exclusively on samples where CLIP is already confident — a censored training set. Its behavior on low-confidence test instances (precisely where reliable view selection matters most) is uncharacterized. No diagnostic analysis (e.g., predicted vs. actual loss scatter plots, breakdown by confidence level) is provided.

- **Kim et al. (2020) — the closest prior work — is not included as an experimental baseline.** The paper cites Kim et al.'s loss predictor for test-time augmentation in the Related Work (Section 2) and correctly identifies it as the nearest idea. A direct experimental comparison would clarify whether RTA's improvements come from the regression approach itself, from the specific choice of pseudo-label targets, or simply from having any view-selection mechanism.

- **Gap between the ceiling (true-label LCE) and RTA's actual performance is not analyzed.** The ceiling experiments (Tables 1–2) show enormous headroom, but RTA captures only 2–5% of this improvement on several benchmarks (e.g., ViT-B/16 on IN-1k: ceiling is 89.0%, RTA achieves 71.13%, barely above entropy's 70.6%). The paper transitions from "true labels work great" to "let's train a regression model" without addressing why the pseudo-label-based proxy fails to capture this headroom.

- **No ablation on the pseudo-label confidence threshold (0.8).** The threshold is arbitrary and sensitivity is unexamined. Similarly, the LightGBM hyperparameters (max depth=5, max leaves=16 for 1000-dimensional logits) are not justified or ablated.

### Trivial

None.

## Nice-to-Haves

- The paper could explicitly highlight that the same regression model trained on single-label ImageNet data transfers to multi-label tasks (MSCOCO, VOC2007, NUSWIDE). This is actually a strength of the method that is currently understated.

## Removed Points

These points from the inputs were removed or merged after verification against the paper:

- **"Unfair comparison — RTA uses pre-training data, baselines don't" (Harsh Critic #2):** Merged into the Major weakness above. The use of any pre-training data is inherent to the method's design, not a flaw per se. The specific concern is that this pre-training data comes from the IN-1k test distribution, which is captured in the Major weakness.
- **"Regression predicts what entropy already measures" (Harsh Critic #4):** Replaced with the more concrete missing-ablation point (max-probability baseline). The regression target (−log(p_max)) and entropy (−∑ p_k log p_k) are distinct quantities, and the paper's claim is that the regression model learns a cross-distribution mapping, not just a per-instance proxy for entropy.
- **"Significant is an overstatement" (Harsh Critic Section-by-section):** This is a subjective phrasing judgment. The paper's own results show consistent improvements across benchmarks; the issue is one of magnitude, not direction.
- **General format / style complaints:** Removed per instructions (parser artifacts).
- **Missing related works:** Removed per instructions (cannot independently verify).
- **Speculative "if-then" criticisms:** E.g., "if the normalization were X, the reported values would be impossible" — no such claim was made; all speculative-fatal assertions removed.
- **Generic strengths from Strength Finder that lack specific evidence:** Dropped.

## Novel Insights

The reviews surface a productive tension: the ceiling TTA experiment is genuinely compelling and provides a clean argument that LCE-based view selection has enormous headroom over entropy-based selection. However, RTA captures very little of this headroom in practice (typically 2–5%), and the small margins over strong entropy-based baselines (especially Zero on ViT-B/16) raise the question of whether the regression model has learned anything beyond CLIP's own confidence signal. The cross-domain and multi-label results are the strongest part of the empirical story, since those settings genuinely test the claim of distribution-independent mapping without any confound from overlapping training/test distributions.

## Suggestions

1. **Address the IN-1k confound.** Either replace ImageVal-12k with a held-out dataset that shares no distributional overlap with any evaluation benchmark, or explicitly re-frame the IN-1k results as non-comparable and focus the paper's claims on the OOD, cross-domain, and multi-label results.
2. **Add a max-probability baseline.** Compare RTA against a simple baseline that selects views with the highest CLIP softmax probability (without a trained regression model), using the same augmentation and ensemble protocol. This would isolate the value added by the regression mapping.
3. **Report error bars.** Run each experiment with multiple seeds and report standard deviations, especially for the sub-1% comparisons.
4. **Add regression diagnostics.** Provide scatter plots of predicted vs. actual pseudo-loss, and analyze model behavior on low-confidence test instances separately.
5. **Add sensitivity analyses** for the pseudo-label confidence threshold and LightGBM hyperparameters.
6. **Compare against Kim et al. (2020)** under a similar protocol.

## Score and Decision

Calibration anchors (retrieved from the human-review corpus; scores are the average human score for each anchor):

Since the calibration corpus was inaccessible at runtime, I use my knowledge of ICLR reviewing standards and the paper's content to calibrate. The paper presents a novel idea (regression-based view selection for CLIP TTA) with a compelling motivating experiment and broad evaluation. However, the IN-1k distribution confound, modest gains in several settings, and missing ablations (max-probability baseline, error bars, threshold sensitivity) prevent it from being a strong accept. The core contribution — that a simple LightGBM model trained on pseudo-labeled data can predict loss across distributions — is interesting and supported by the OOD and multi-label results. The paper is at a borderline-accept level: it would benefit from addressing the confound and adding the missing ablations, but the idea and evidence are sufficient for publication.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>