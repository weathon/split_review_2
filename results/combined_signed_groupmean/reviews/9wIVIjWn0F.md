Now I have all the calibration data. Let me compile the final review.

## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA), a method that trains a LightGBM regression tree on pseudo-labeled diverse data to predict view quality (cross-entropy loss) from CLIP logits, then uses these predictions to select confident augmented views at test time. The CLIP model itself remains frozen. Experiments across ImageNet variants, 10 cross-domain datasets, and 3 multi-label datasets show RTA outperforming existing entropy-based TTA methods.

## Strengths

- **Comprehensive evaluation across diverse benchmarks.** The paper evaluates on five ImageNet variants, ten cross-domain datasets, and three multi-label datasets (Tables 3–6), using two CLIP backbones (RN50, ViT-B/16). This coverage is substantially wider than many TTA papers and provides a thorough empirical assessment.

- **Simple and computationally efficient.** The method uses a LightGBM regression tree trained once on 1,000 samples offline, then applied at test time with negligible overhead (single forward pass + tree evaluation). This is a genuine practical advantage over per-instance backpropagation methods like TPT or DiffTPT.

- **Consistently strong empirical results.** RTA achieves the best or near-best performance in almost every setting across both backbones. On challenging OOD datasets the gains are nontrivial (e.g., RN50 on ImageNet-A: 36.79% vs. DiTPT's 31.06%). The results are too consistent across settings to dismiss as noise.

## Weaknesses

### Fatal

None.

### Major

- **The regression model predicts a quantity computable exactly from its inputs, and this core mechanism is unvalidated against simpler baselines.** The regression target is the pseudo-label cross-entropy loss of CLIP's most confident class: pseudo-LCE = -log(max(softmax(logits))). This is a deterministic function of the logit vector — specifically, log(Σ exp(sₖ)) - max(sₖ) — computable exactly without any training. The paper provides no ablation comparing RTA's regression-based view selection against training-free alternatives computed from the same logits, such as: (a) selecting top-k views by max-softmax probability, (b) selecting by the gap between top-1 and top-2 logits, or (c) selecting by the negative log-likelihood of the top-1 class. If these simpler criteria perform comparably, the regression model adds no value and the paper's central claim is unsupported. This is the single most important missing experiment. *(Verified from Eqs. 3–4 and the training procedure in Section 4.2: the pseudo-label is the argmax class with confidence ≥ 0.8, and the loss in Eq. 4 is -log(softmax of that class) = -log(max(softmax)), which is a deterministic function of the logit vector.)*

- **The multi-label extension is undefined, yet multi-label results are reported.** The method description (Section 4) defines the regression target only for single-label classification: a single pseudo-label and its cross-entropy loss (Eq. 4). For multi-label classification, where each image has multiple positive labels and the loss is typically binary cross-entropy summed over classes, the paper specifies nothing about how pseudo-labels are obtained per class, how the regression target is defined, or how the regression model's scalar predictions are interpreted for multi-label view selection. Tables 5–6 report multi-label results (MSCOCO, VOC2007, NUSWIDE) with no methodological explanation. *(Verified: the method section only covers single-label; multi-label results appear in Tables 5–6 with no corresponding method description.)*

- **No ablation studies isolating the regression model's contribution.** The paper contains no ablation section. There is no experiment that: (a) compares against training-free view-selection criteria on the same frozen CLIP model with the same augmentations, (b) analyzes sensitivity to key hyperparameters (confidence threshold 0.8, LightGBM depth/leaves), or (c) isolates what the regression mechanism adds over the augmentation ensemble alone. The "Further Analysis" section only studies the number of views and number of regression samples — neither tests whether the regression model is necessary. *(Verified: grep for "ablation" returns no matches; the Further Analysis section covers only view count and sample count.)*

### Minor

- **"ImageVal-12k" is not defined.** The paper states it "select[s] ImageVal-12k as the regression mapping data" (line 332) but never explains what this dataset is. If it is a subset of the ImageNet validation set, this weakens the claim that the method is "independent of downstream tasks" (line 330), since the regression data shares the same domain as one of the test distributions. The paper should clarify the source and ideally evaluate with regression data from a truly unrelated distribution.

- **The regression model is trained on unaugmented original images only (line 126), yet must predict for heavily augmented views at test time.** The justification ("the original image itself can actually be regarded as a view") is weak — augmented views differ systematically (cropped, color-shifted, etc.). While the experimental results suggest the model generalizes, this gap in analysis should be addressed.

- **No error bars, confidence intervals, or standard deviations are reported.** Some gains are small (e.g., ViT-B/16 on IN-1k: RTA 71.13% vs. Zero 70.89%, a 0.24% absolute improvement), making it impossible to assess statistical significance.

### Trivial

None.

## Nice-to-Haves

- An experiment using regression training data drawn from a distribution truly unrelated to any test domain (e.g., LAION subsets, mixed-domain data) to demonstrate the claimed distribution-agnostic generalization.
- Ablation on the confidence threshold (0.8) used for pseudo-label filtering.
- Comparison against the deep neural network loss predictor of Kim et al. (2020) to contextualize the LightGBM design choice.

## Removed Points

- **"This is not TTA; it is a pre-trained view selector."** Removed. Zero (Farina et al., 2024), published at NeurIPS 2024 as a TTA method, also selects views without updating model parameters. RTA's framing is consistent with this established precedent.
- **"Ceiling TTA motivation is a straw man."** Removed. The paper's logical chain (LCE works well → can we predict LCE without labels? → train a regression model) is coherent and reasonable. The gap between Ceiling TTA and the actual method is exactly what the method attempts to bridge.
- **"Missing comparison with Kim et al. loss predictor."** Removed. Kim et al. requires supervised training on target-domain data — a different setting. The absence of this comparison is not a flaw within the paper's scope.
- **"Sampling strategy not explained."** Removed. The paper provides the key details (confidence threshold ≥ 0.8, 1,000 samples from 5,000 candidates), which are sufficient for reproducibility.
- **Formatting, style, and typographical nitpicks.** Removed per instructions (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions. The observation that a regression tree trained on pseudo-labeled diverse data can predict view quality from logits is the paper's core empirical finding. However, because the predicted quantity is deterministically computable from the input features, the most critical control experiment is absent, making it impossible to tell whether the finding reflects genuine method value or merely recovers a known function.

## Suggestions

1. **Essential:** Add an ablation that replaces the regression model with training-free view-selection criteria computed from the same logits (max-softmax, top-1 vs top-2 gap, negative log-likelihood of top-1 class). If RTA outperforms these, the regression model's value is validated. If it does not, the paper's contribution needs substantial reframing.
2. Clarify the multi-label extension: specify how pseudo-labels are obtained and how the regression target is defined for multi-label data.
3. Define "ImageVal-12k" explicitly and ideally include an experiment using regression data from a distribution unrelated to ImageNet.
4. Add ablation on the confidence threshold (0.8) and LightGBM hyperparameters.
5. Report error bars or statistical significance measures, especially for small-gap comparisons.

## Score and Decision

### Calibration Report

**Round 1 bracket:** 3.5 – 5.0.

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| pdzHpQbGrn.md (Active TTP) | 2.50 | R1 | Yes | Weaker than RTA: poor writing, marginal gains. RTA is clearly stronger. |
| Rc3RP9OoEJ.md (InCPL) | 5.00 | R1 | Yes | Stronger than RTA: has ablation studies, clearer method, but similar evaluation breadth. RTA is weaker due to missing key ablation. |
| kIP0duasBb.md (RLCF) | 6.67 | R1 | Yes | Stronger than RTA: validated across three task types (classification, retrieval, captioning), clearer contribution. RTA lacks comparable validation. |
| yD2JMeKumt.md (DOTA) | 6.00 | R1 | Yes | Stronger than RTA: clearer contribution (distribution estimation), better method justification. RTA's core weakness is more fundamental. |
| TPZRq4FALB.md (READ) | 8.00 | R1 | Yes | Much stronger than RTA: novel problem, extensive experiments, thorough validation. RTA does not approach this quality level. |
| 75PhjtbBdr.md (ML-TTA) | 6.25 | R2 | Yes | Stronger than RTA: clear multi-label contribution with proper method definition. RTA's undefined multi-label extension is a gap. |
| 0vtftmYQGV.md (SNAP-TTA) | 5.75 | R2 | Yes | Stronger than RTA: practical contribution with latency evaluation. RTA's core methodological gap is more severe. |
| JIlIYIHMuv.md | 2.50 | R1 | No | Less relevant (continual learning), weaker quality. RTA is stronger. |
| HfJxXbXlYJ.md | 3.00 | R1 | No | Less relevant (CLIP extension via LLMs). Not directly comparable. |
| lF9QXpfNHm.md | 4.67 | R1 | No | Open-world TTA setting, different problem scope. |
| TD3SGJfBC7.md | 6.25 | R1 | No | Few-shot TTA, different setting. |

**Final score placement:** The paper sits between the 2.5–3.0 reject anchors and the 5.0 InCPL anchor. It is clearly stronger than the active-TTP paper (2.5) due to thorough evaluation and strong results. However, it is weaker than InCPL (5.0) because InCPL provides ablation studies and has a clearer methodological contribution, while RTA's core regression mechanism is unvalidated against simpler baselines. The deterministic-target weakness (impact -10.00 in my draft) is decisive: the paper cannot support its central claim without the missing ablation. This places the paper in the borderline-reject range.

**Score:** 4.0  
**Decision:** Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>