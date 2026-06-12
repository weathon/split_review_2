## Summary
This paper proposes DGNet (Delta2Gamma), a multi-head SimCLR-based self-supervised learning framework for EEG-based dementia classification. EEG signals are decomposed into five canonical frequency bands (δ, θ, α, β, γ), each processed by independent CNN encoders and projection heads with adaptive temperature contrastive loss, achieving 92.90% accuracy on AD vs. CN classification using LOSO cross-validation on a dataset of 88 participants.

## Strengths
- **Relevant application domain**: EEG-based dementia screening addresses an important and practical problem, and the paper clearly motivates why EEG is preferable to MRI/PET for scalable early detection.
- **Thorough ablation study**: Table 3 systematically evaluates each component (SSL, single-head vs. multi-head, augmentation, adaptive temperature, regularization), providing clear evidence that each contributes to performance.
- **Physiologically grounded design**: Decomposing EEG into standard clinical frequency bands and processing them independently is well-motivated by established neurophysiology of dementia (increased low-frequency power, decreased high-frequency power).

## Weaknesses

### Fatal
- **Pre-training data leakage**: The experimental protocol appears to pre-train the encoder on all subjects (including test subjects) *before* applying LOSO evaluation with the encoder frozen. This means the encoder has already learned representations from the test subjects' data, invalidating the claim of evaluating generalization to unseen subjects. A rigorous LOSO protocol requires excluding the held-out subject from *both* pre-training and fine-tuning. This potentially inflates all reported results and undermines the paper's central claim.

### Major
- **Unfair baseline comparisons in Table 1**: Many established architectures (EEGNet, Deep4Net, EEGInception) achieve near-chance accuracy (39-57% for a two-class problem), which strongly suggests they were not properly configured, tuned, or evaluated under the same protocol. The paper does not clarify whether Table 1 baselines use the same dataset, preprocessing, or evaluation protocol as the proposed model, making the claimed superiority unreliable.
- **No confidence intervals or variance reporting**: With only 88 subjects and LOSO cross-validation, the variance across folds is critical for interpreting the results. Reporting point estimates of accuracy/F1 without standard deviations or confidence intervals makes it impossible to assess statistical significance of differences.
- **Very small dataset**: 88 participants (36 AD, 29 CN, 23 FTD) with only ~59 subjects used for binary AD/CN classification is small, and the results are likely sensitive to individual outliers. The paper does not acknowledge this limitation.

### Minor
- **FTD data unused**: The dataset includes 23 FTD patients, but experiments only evaluate AD vs. CN binary classification. This is a missed opportunity and leaves open the question of whether the method generalizes to multi-class dementia classification.
- **Adaptive temperature is not novel**: The adaptive NT-Xent loss with regularization is directly attributed to Wang et al. (2024), reducing the paper's algorithmic novelty to the specific application of this loss with multi-band heads for EEG.
- **Table 1 vs. Table 2 protocol ambiguity**: Table 1 and Table 2 appear to report slightly different numbers (93% vs. 92.90%) for the proposed model without clearly explaining what differs between the two evaluations.

### Trivial
- Duplicate figure captions (Figures 1-4 each appear twice in the text, likely a parser artifact).
- The "state-of-the-art in multi-head approaches" claim is overly narrow and difficult to verify.

## Nice-to-Haves
- A protocol where pre-training also uses LOSO (excluding test subjects from pre-training each fold) would be the most important improvement.
- Evaluation on additional benchmarks or datasets to demonstrate generalizability beyond one 88-subject cohort.
- Per-fold accuracy distribution to show whether performance is consistent or driven by a few easy subjects.

## Novel Insights
The paper's core observation—that independently processing EEG frequency bands with separate contrastive heads improves representation quality for dementia classification—is intuitively appealing and supported by the ablation. However, the combination of existing components (SimCLR, bandpass decomposition, adaptive temperature from Wang et al. 2024) does not yield a fundamentally novel insight. The most interesting finding is the relative contribution of multi-band heads vs. single-band heads in the ablation, but the pre-training leakage concern undermines confidence in these numbers.

## Suggestions
- **Rerun experiments with proper LOSO pre-training**: Exclude each test subject from the pre-training phase in each fold to ensure valid generalization claims.
- **Report mean ± std across LOSO folds**: This is essential given the small sample size.
- **Reproduce baselines carefully**: Ensure all comparison models in Table 1 use the same dataset, preprocessing, and evaluation protocol, and report their performance with comparable rigor.
- **Clarify the relationship between Table 1 and Table 2**: Explain what experimental differences account for the different reported numbers.

## Score and Decision
The paper tackles an important problem and the multi-band contrastive learning framework is reasonable. However, the apparent pre-training data leakage is a critical methodological flaw that likely inflates the reported results, the baseline comparisons in Table 1 appear unfair, and the small dataset without variance reporting limits confidence. These issues collectively prevent acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>