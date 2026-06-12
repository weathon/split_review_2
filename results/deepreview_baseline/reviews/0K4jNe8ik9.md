## Summary

The paper proposes DGNet, a self-supervised learning framework for EEG-based dementia classification. It decomposes raw EEG into five frequency bands (delta, theta, alpha, beta, gamma), processes each band with an independent CNN encoder and projection head, and applies SimCLR-style contrastive learning with adaptive temperature and regularization. The framework is evaluated on a resting-state EEG dataset of 88 subjects (AD, FTD, CN) for AD vs CN classification using leave-one-subject-out cross-validation, reporting 92.90% accuracy and 92.85% F1-score.

## Strengths

- **Clinically relevant motivation**: The paper correctly identifies the diagnostic bottleneck for dementia and argues convincingly that EEG-based methods can be more scalable and accessible than MRI/PET. The focus on a practical, deployable technology is timely.
- **Architecture tailored to EEG physiology**: Decomposing signals into the five standard frequency bands and learning independent representations for each band is well-motivated by known neurophysiological signatures of dementia (slowing of oscillations). The multi-head design directly leverages this domain knowledge.
- **Ablation study covers key components**: The ablation systematically evaluates the contribution of SSL, multi-head (vs single-head), augmentation, adaptive temperature, and regularization, showing that each component provides a non-negligible performance gain. This gives confidence that the design choices are meaningful.

## Weaknesses

### Major

1. **Unreliable comparison baselines**  
   Table 1 reports many established EEG models (e.g., EEGNet, Deep4Net, EEGConformer) with accuracy between 39% and 74%. These numbers are far below typical performance of these models on many EEG benchmarks, suggesting the baselines were either not properly tuned, not adapted for the 30-second segment setting, or evaluated under different preprocessing. The contrast with the proposed 93% is therefore inflated. Without a fair and controlled comparison, the claim of state-of-the-art is not substantiated.

2. **No statistical uncertainty reported**  
   All reported results (accuracy, F1, precision, recall, AUC) are given as point estimates without standard deviations, confidence intervals, or per-fold variance, despite using leave-one-subject-out cross-validation. With only 88 subjects and a high-variance evaluation protocol, these results could be unstable. The competing method BI-MCGNN reports ±0.38 accuracy, while DGNet’s uncertainty is absent, making it impossible to judge whether the 1.65% advantage is even significant.

3. **Minimal unlabeled data for pre-training**  
   Self-supervised pre-training is performed on the same 88 subjects that are later used for linear evaluation. This is not the typical regime where SSL excels (large unlabeled corpus). The reported improvement over “training from scratch” (63.35% → 92.90%) is mostly driven by the multi-band architecture itself (63.35% → 79.55%), not SSL. The added value of SSL is modest (79.55% → 92.90%) and may not generalize to larger, more diverse populations.

4. **Loss formulation is unclear and misrepresented novelty**  
   Equation (1) appears to sum over frequency bands inside the per-sample loss, but the notation ℓ_i is ambiguous. The adaptive temperature and regularization are cited from prior work (Wang et al., 2024), yet the paper treats them as part of its own contribution. The actual novelty lies in the multi-band application, not in the loss function. The description of the encoder ( “output [5, C, L/32]”, “128-dimensional embedding”) is inconsistent and hard to follow, especially in the text vs. Figure 2.

### Minor

- **Binary classification only**  
  The dataset contains three diagnostic groups (AD, FTD, CN), but experiments are limited to AD vs. CN. Including FTD vs. CN or three-way classification would substantially strengthen the clinical relevance.
- **Small dataset size**  
  Even with LOSO, 88 subjects is a small sample for deep learning. The reported 93% accuracy, while high, needs replication on larger independent cohorts.
- **Overly verbose introduction**  
  Sections 1 and part of 2 spend many paragraphs on general dementia background and EEG advantages that are well known to the ICLR audience. The technical contributions are buried and could be communicated more concisely.

### Trivial

- No critical issues of this level.

## Nice-to-Haves

- Release code and pre-trained weights to facilitate reproducibility and adaptation by the community.
- Extend evaluation to the full three-class problem (AD vs. FTD vs. CN) and report per-class metrics.
- Compare against a standard SimCLR applied directly to raw EEG (without multi-band) to quantify the benefit of the band-specific design.
- Report per-subject results or show that the high accuracy is not driven by a few easy subjects.

## Novel Insights

None beyond the paper’s own contributions. The observation that multi-band self-supervised learning outperforms single-band and from-scratch training on this particular dataset is consistent with the known physiological relevance of frequency bands in dementia, but does not reveal any unexpected phenomenon or principle that would generalize beyond the presented architecture and dataset.

## Suggestions

1. **Improve baseline fairness**: Re-run all comparison models under identical preprocessing, segmentation, and hyperparameter optimization. Report results with standard deviations to allow meaningful comparisons.
2. **Clarify the pre-training data**: Explicitly state whether the SSL pre-training uses only the 88 subjects or an external unlabeled corpus. If only the 88 subjects, discuss why SSL still helps despite the small dataset.
3. **Clean up technical exposition**: Provide a single, self-contained loss equation without the ambiguous ℓ_i notation. Ensure that Figure 2 and the text agree on the encoder output shape and the point where global pooling is applied.
4. **Add error bars**: Report mean ± std over LOSO folds for all metrics. For the ablation study, include at least one repeat (e.g., fixed random seed) or bootstrapped confidence intervals.

## Score and Decision

**MY FINAL SCORE: 4.0**  
**MY FINAL DECISION: Reject**