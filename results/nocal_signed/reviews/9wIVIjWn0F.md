Now let me write the final consolidated review.

## Summary

This paper proposes Regression-based Test-time Adaptation (RTA) for CLIP-based image classification. The key idea is to train a LightGBM regression model offline on pseudo-labeled data to map logits of augmented views to their cross-entropy loss, then at test time use the predicted loss to select confident views for ensembling. The paper is motivated by an oracle analysis showing that view selection using ground-truth label cross-entropy (LCE) dramatically outperforms Shannon entropy selection. RTA is evaluated on single-label ImageNet variants, 10 cross-domain datasets, and multi-label datasets across two CLIP backbones, consistently achieving competitive or best results.

## Strengths

- **Provocative ceiling analysis (Tables 1-2).** The finding that LCE-based view selection outperforms Shannon entropy by massive margins — e.g., 90.2% vs 64.3% on ImageNet-A with ViT-B/16 at 64 views — convincingly establishes that better view selection criteria exist and that the gap is worth pursuing. This oracle characterization is a useful scientific contribution independent of the method.

- **Clean and simple method.** Training a single LightGBM regression tree on a logit-to-loss mapping, then using it for test-time view selection, is refreshingly straightforward relative to the increasingly complex machinery in the TTA literature (diffusion models, reward models, cache mechanisms, etc.). The two-stage framing (offline training + online selection) is well-structured and practical.

- **Comprehensive empirical evaluation.** The paper evaluates on single-label (ImageNet + 4 variants), cross-domain (10 datasets), and multi-label (3 datasets) benchmarks, across both RN50 and ViT-B/16 backbones. RTA achieves top or near-top results on nearly all settings, demonstrating broad applicability.

## Weaknesses

### Fatal
None.

### Major

- **Missing critical baseline (max-softmax confidence selection).** The regression model is trained on pairs (logits, −log(max softmax(logits))) using CLIP's own argmax as pseudo-label. At test time, selecting views with smallest predicted loss is approximately equivalent to selecting views with highest max-softmax probability — a baseline that requires zero training and is never included. The paper must compare RTA against simply picking top-k augmented views by CLIP's raw softmax confidence to establish whether the learned regression adds anything beyond trivial computation. Without this, the paper's core claim — that learning to predict loss from logits improves view selection — cannot be separated from what CLIP already trivially knows about its own outputs (Section 4.2, Algorithms 1-2, Tables 3-6).

### Minor

- **Misleading ceiling framing.** The LCE ceiling (e.g., 90.2% on IN-A with ViT-B/16) is presented as motivation for "directly establishing a regression mapping between augmented views and their corresponding cross-entropy loss." But RTA achieves 65.65% on the same setting — essentially in line with entropy-based Zero (64.03%). The ~25-point gap between the oracle and the delivered method is never bridged or explained, and the language implies a connection that the results do not support.

- **No statistical significance or variance.** All results are single numbers despite stochastic view augmentation. RTA often beats the runner-up by small margins (e.g., 0.34% over BCA on RN50 cross-domain average, Table 4; 1.62% over Zero on IN-A ViT-B/16, Table 3). Without variance estimates across seeds, it is impossible to know whether these gains are meaningful or within noise.

- **Under-specified training data selection.** The paper describes sampling "1,000 examples (sampling by logit-based equal-interval from 5,000 samples with threshold ≥ 0.8)." The term "logit-based equal-interval sampling" is undefined. Since all 5,000 filtered samples are from the ≥0.8 confidence region, the regression model never sees logit patterns from low-confidence or ambiguous predictions during training, which may limit its ability to rank uncertain views at test time (Section 5.1).

- **Train-test input mismatch unexamined.** The regression model is trained on logits from original (unaugmented) ImageNet images, but at test time applied to logits from randomly augmented views on potentially different distributions. The paper does not analyze whether logit distributions of augmented views systematically differ from those of original images, or whether this matters for prediction quality (Section 4.2).

## Nice-to-Haves

- Add a direct measure (e.g., Spearman correlation) of how well RTA's predicted loss correlates with actual label cross-entropy loss on held-out OOD data, to substantiate cross-distribution generalization.
- Ablate the confidence threshold (0.7, 0.8, 0.9) used for pseudo-label filtering.
- Include per-instance runtime comparisons to substantiate the claim of "negligible additional cost."
- Train the regression model on a more diverse data pool (e.g., a mix of datasets) to better justify the claim of "diversely distributed data."

## Removed Points

- **Straw-man claim about the introduction.** The reviewer argued the paper overstates that TTA methods "need to continuously update and maintain dynamically changing historical samples." But the paper says "some excellent works have designed memory modules and cache mechanisms" — a specific qualifier, not a characterization of all TTA. REMOVED (factually incorrect reading).
- **Criticism about training data overlapping with ImageNet test.** Using ImageVal-12k (validation split) for training and ImageNet (test split) for evaluation is standard practice. The OOD evaluations (IN-A, IN-R, cross-domain) are genuinely cross-distribution. REMOVED (not a valid weakness).
- **Demand for a mechanistic explanation of cross-distribution transfer.** The contribution is empirical. The consistent cross-dataset results provide evidence of transfer. REMOVED (scope creep).
- **Generic speculation about confounders or proxy metrics** that did not anchor to a concrete, verifiable problem in the paper. REMOVED (noise).

## Novel Insights

The most instructive observation from the reviewing process concerns what the regression model actually learns. The paper frames RTA as learning to predict "label cross-entropy loss" — evoking the LCE ceiling from Tables 1-2. But in practice, the regression target is −log(max(softmax(logits))) computed using CLIP's own argmax as pseudo-label. This is not an approximation of LCE (which requires true labels); it is a learned proxy for prediction confidence. When this is recognized, the missing max-softmax baseline becomes the decisive comparison: the paper must show RTA outperforms simply picking views by raw softmax confidence, or the claimed contribution dissolves into a complicated way of doing what a one-line argmax already provides.

## Suggestions

1. Add a baseline that selects top-k augmented views by CLIP's own maximum softmax probability — requires no training. Report on all benchmarks (Tables 3-6) and directly compare to RTA.
2. Report all results with variance across at least 3 seeds, especially where margins over baselines are <2%.
3. Clarify the "logit-based equal-interval sampling" procedure and ablate the confidence threshold.
4. Include a direct measure of predicted-loss vs. true-loss correlation on OOD data.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>