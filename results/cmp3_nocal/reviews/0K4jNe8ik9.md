Now I have a complete verification of all claims. Let me write the final consolidated review.

---

## Summary

This paper proposes DGNet, a multi-band, multi-head SimCLR-based contrastive learning framework for EEG-based dementia classification. The method decomposes raw EEG signals into five canonical frequency bands (delta, theta, alpha, beta, gamma), learns independent representations per band using separate CNN encoders with adaptive temperature parameters, and evaluates on an 88-subject dataset (AD vs. CN classification).

## Strengths

1. **Neurophysiologically motivated architecture.** The decision to decompose EEG into five canonical frequency bands and learn independent representations per band is grounded in the clinical literature on spectral signatures of dementia (slowing of brain oscillations: increased low-frequency power, decreased high-frequency power), discussed in Section 1. This is a sensible design choice.

2. **Comprehensive ablation study.** Table 3 systematically isolates SSL pre-training vs. training from scratch, single-head vs. multi-head, data augmentation, adaptive temperature, and temperature regularization, showing the contribution of each component. The ablation covers the main architectural decisions.

3. **Thorough documentation of dataset and preprocessing.** Section 3.1–3.3 provides detailed information on the clinical dataset (88 subjects across three groups), recording protocol (19-channel 500Hz EEG), preprocessing (bandpass filter, ICA), and segmentation (30-second windows), enabling reproducibility.

## Weaknesses

### Fatal
None.

### Major

1. **Numerical discrepancy between the abstract and Table 3.** The abstract claims "a 31.5% relative performance improvement over training from scratch, and a 25.4% improvement over the single-head approach." Computing from Table 3: over scratch (63.35% → 92.90%) yields (92.90−63.35)/63.35 = **46.6%** (not 31.5%); over single-head (73.52% → 92.90%) yields (92.90−73.52)/73.52 = **26.4%** (close to 25.4% but not exact). No combination of accuracy, F1, or AUC from Table 3 reproduces "31.5%." This is a factual error that must be corrected.

2. **Baseline methods in Table 1 perform at or below chance, suggesting a confounded comparison.** On a binary classification task (50% chance), several well-established EEG models achieve suspiciously low results: EEGInception 39%, Deep4Net 49%, EEGNet 46%, FBCNet 48%, TIDNet 44%, S-JEPA 50%. These methods have published results substantially above chance on standard EEG benchmarks (e.g., EEGNet on BCI Competition IV-2a reaches ~70% for a harder 4-class task). The most likely explanation is that these baselines received raw EEG inputs while the proposed method receives frequency-band-decomposed inputs, creating a confounded comparison where the benefit of band decomposition — not the multi-head contrastive learning — drives the gap. The paper does not clarify whether baselines received the same input representation. This undermines the SOTA claims drawn from Table 1.

3. **No confidence intervals or variance estimates for the proposed method.** Table 2 reports the proposed method's accuracy as a single point (92.90%) with no error bars, while some comparison methods (e.g., BI-MCGNN: "91.25 ± 0.38") do report standard deviations. Since Leave-One-Subject-Out CV on 88 subjects produces 88 per-fold scores, variance estimates are readily available. Without them, the 1.65pp advantage over BI-MCGNN cannot be assessed for statistical significance.

4. **Evaluation covers only AD vs. CN, despite the paper's scope claiming "dementia classification."** The dataset (Section 3.1) contains three groups: AD (n=36), FTD (n=23), and CN (n=29). All experiments evaluate only AD vs. CN, entirely discarding the FTD group (~26% of subjects). No results are reported for AD vs. FTD, FTD vs. CN, or three-way classification. This makes the paper's title and framing broader than its actual evidence.

### Minor

1. **"Linear evaluation" terminology error (Section 2.1, line 80).** The paper states "the second approach, known as linear evaluation, all parameters of the model including those of the encoder are updated." Linear evaluation standardly means freezing the encoder and training only a linear classifier. The experimental section (line 124) correctly uses a frozen encoder, so the description is inconsistent with both the standard definition and the paper's own implementation.

2. **Ablation study lacks explanation for large performance jumps.** Adaptive temperature accounts for ~7pp improvement (79.55% → 86.53%) and regularization for ~4pp (86.53% → 90.64%). These are substantial gains, but the paper offers no analysis of why — e.g., showing learned temperature values per band to demonstrate they differ meaningfully, or ablating the regularization components.

3. **Missing details on window-level handling in LOSO evaluation.** The paper segments recordings into 30-second windows (Section 3.3) but does not report the total number of windows, how multiple windows from the held-out subject are aggregated at test time (majority vote? averaged logits?), or whether class imbalance at the window level mirrors subject-level labels.

### Trivial

1. **Nested summation in equation (1).** The loss is defined as ℓ = Σ_b ℓ_b (line 102), but equation (1) already has Σ_b on the RHS, yielding ℓ_i = Σ_b (Σ_b ...). This appears to be a typo in notation.

## Nice-to-Haves

- Including FTD-related evaluations (AD vs. FTD, three-way classification) would better match the paper's scope.
- Per-band contribution analysis (e.g., training on one band at a time, or visualizing learned temperature values per band) would substantiate the claim that multi-band processing leverages differential band informativeness.
- A controlled baseline where a standard method receives the same band-decomposed input would isolate the contribution of the multi-head design.

## Removed Points

These points were flagged by the reviewer(s) but are removed from the main evaluation for the reasons stated below. Treat them with caution.

1. **Loss function sign error (reviewer claimed eq (1) has a sign error that would pull negatives toward the anchor).** **Removed** — this criticism is factually incorrect. Equation (1) is: ℓ_i = Σ_b ( **−**1/τ⁺·sim(z,z⁺) **+** 1/τ⁻·max sim(z,z⁻) + ...). When minimized via gradient descent, the positive coefficient on the negative-pair term *decreases* sim(z,z⁻) (pushes negatives away), which is the correct contrastive behavior. The reviewer's claim that this term "would encourage the model to increase similarity with the hardest negative" misapplies the sign convention of gradient descent.

2. **Novelty attribution concern (reviewer stated the paper inadequately delineates what is new vs. from Wang et al. 2024).** **Removed** — the paper explicitly states "Using Adaptive Multi-head Contrastive Learning (AMCL) strategy (Wang et al., 2024)" in the conclusion (line 215) and cites Wang et al. for the adaptive temperature mechanism in Section 2.3. The attribution is present and adequate for a conference paper.

3. **Speculation about appendix content and missing related work.** **Removed** — per the hard rules, criticisms about missing appendices or unknown related work are not admissible, as the appendix is stripped by the PDF parser and the reviewer cannot confirm the existence of missing citations.

## Novel Insights

The reviews surface two genuinely useful diagnostic observations beyond the paper's own contributions. First, the poor performance of established baselines in Table 1 (several below chance) functions as a red flag that the comparison protocol is unlikely to be fair — this is the kind of structural evaluation issue that reviewers should watch for even when the main method appears strong. Second, the authors' internal inconsistency between the abstract's numerical claims and Table 3's data illustrates how easily relative improvement statistics can be miscalculated or misreported without deliberate dishonesty; it is a concrete cautionary example for paper writing.

## Suggestions

1. **Fix the numerical claims in the abstract** to match the data in Table 3 (46.6% and 26.4%, or whatever the correct computation is).
2. **Clarify whether baseline methods in Table 1 received raw EEG or band-decomposed input.** If they received raw EEG, include a control where a standard baseline receives band-decomposed input — this is essential to demonstrate that the multi-head design, not just the front-end decomposition, drives the improvement.
3. **Add error bars** (standard deviation or confidence intervals) for all metrics, computed from LOSO folds.
4. **Include at least one evaluation involving the FTD group** (e.g., AD vs. FTD) or, alternatively, reframe the paper's title and claims to accurately reflect that only AD vs. CN is evaluated.
5. **Correct the "linear evaluation" terminology** on line 80 and the nested Σ_b typo in equation (1).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>