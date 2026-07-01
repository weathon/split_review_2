## Summary

The paper proposes DGNet, a self-supervised learning framework for EEG-based dementia classification. The core design decomposes EEG signals into five canonical frequency bands (delta through gamma), processes each band with an independent CNN encoder, and applies a SimCLR-style contrastive loss with per-band adaptive temperature. The model is evaluated on a resting-state EEG dataset for Alzheimer's disease vs. cognitively normal classification using Leave-One-Subject-Out cross-validation.

## Strengths

- **Principled architectural design for EEG.** The multi-band approach with independent encoders per frequency band directly encodes the known neurophysiology of dementia (spectral slowing), where patterns in delta, theta, alpha, beta, and gamma bands carry differential diagnostic information. This is a sensible inductive bias that distinguishes the work from monolithic approaches.

- **Ablation covers the main design axes.** Table 3 systematically varies SSL pretraining, single-vs-multi-head processing, augmentation, temperature adaptation, and regularization. While some conditions need clarification (see Weaknesses), the structure of the ablation is appropriate for understanding what matters in the framework.

- **Table 2 provides a grounded prior-work comparison.** Unlike Table 1, the comparison with prior methods evaluated on the same dataset (lines 182–195) shows the proposed method achieving 92.90% vs. the best prior result of 91.25% (BI-MCGNN), suggesting the approach is at least competitive.

## Weaknesses

### Fatal
None.

### Major

- **Baseline comparison in Table 1 is not credible and undermines the central claim.** Multiple well-established EEG models perform at or below chance on a binary classification task: EEGNet 46%, Deep4Net 49%, EEGInception 39%, FBCNet 48%, TIDNet 44%, S-JEPA 50% (lines 158–170). These results are inconsistent with prior work on the *same dataset* cited in Table 2, where simpler methods such as Random Forest achieve 80–89% accuracy (lines 186, 192). This pattern strongly suggests a configuration problem, training mismatch, or data processing discrepancy that systematically disadvantages the baselines. Table 1 is presented as the primary evidence of superiority (line 154: "significantly outperforming all comparison models"), but it cannot support that claim when the comparison set includes models that cannot beat a trivial majority classifier.

- **No variance reported for any result.** Tables 1, 2, and 3 report only point estimates. LOSO cross-validation on 65 (AD+CN) subjects produces a per-subject accuracy distribution, and reporting standard deviation or confidence intervals is standard practice—indeed, BI-MCGNN in Table 2 reports ±0.38 (line 192). Without variance, the reader cannot assess whether the 1.65 percentage point gap over BI-MCGNN (92.90 vs. 91.25) is meaningful, nor whether any ablation contrast in Table 3 exceeds evaluation noise.

- **Key numerical claims in the abstract cannot be verified from the reported data.** The abstract (line 9) states "31.5% relative performance improvement over training from scratch, and a 25.4% improvement over the single-head approach." Computing relative improvement from the values in Table 3: (92.90 − 63.35) / 63.35 = 46.6% (not 31.5%), and (92.90 − 73.52) / 73.52 = 26.4% (not 25.4%). The paper does not specify the formula used, and the discrepancy calls into question how carefully the quantitative results have been constructed.

### Minor

- **Ablation conditions are insufficiently specified for interpretation.** The "Multi-head (5 heads)" row (79.55%) is 13.35 percentage points below the full model (92.90%), but the paper does not clearly state whether this variant uses SSL pretraining, the same augmentation pipeline, or the same encoder architecture as the full model (line 199). The row "w/o self-supervised learning" (63.35%) is separately listed, suggesting "Multi-head (5 heads)" does use SSL, but the specific differences between this row and the full model are not enumerated. Without clarity on what is being ablated, the reader cannot determine which design choice accounts for the gap.

- **Confusion about the downstream evaluation setup.** Section "Downstream Task" (line 80) describes two approaches: (i) frozen encoder + train classifier, and (ii) "linear evaluation" defined as updating *all* parameters including the encoder. The experimental section (line 124) then reports using the frozen-encoder approach but calls it "linear evaluation," which contradicts the earlier definition. Two approaches are described but only one is evaluated, and the terminology is inconsistent, making it difficult to interpret what the reported numbers measure.

- **Pretraining data is never specified.** The paper states that SSL pretraining is performed on "unlabeled EEG data" (line 38) but never identifies the source, quantity, or composition of this data. Since the labeled dataset contains only 88 subjects and SSL's benefit typically scales with data volume, this is a critical missing detail for evaluating the pretraining setup.

- **Novelty is modest relative to the claims.** The method applies SimCLR (Chen et al., 2020) to EEG signals decomposed into standard frequency bands, with a per-band projection head and an adaptive temperature mechanism explicitly adopted from Wang et al. (2024) (lines 102, 215). The SOTA claim is qualified as "in multi-head approaches" (line 9), which is never formally defined and is essentially self-referential. The contribution is a reasonable engineering combination of existing components rather than a novel method.

### Trivial
None.

## Nice-to-Haves

- Report variance (standard deviation or confidence intervals) for all LOSO results.
- Clarify the source and size of the unlabeled pretraining data.
- Fix the inconsistent use of "linear evaluation" in the downstream-task description vs. the experimental section.
- Provide statistical significance tests (e.g., paired test across LOSO folds) for the comparison against BI-MCGNN and for the key ablation contrasts.
- Clarify the exact configuration of the "Multi-head (5 heads)" ablation row relative to the full model.

## Removed Points

- **"The framing is disproportionately long"** — This is a subjective style observation, not an evidence-based weakness.
- **"Relevant and timely motivation"** (from Strengths) — Generic; applies broadly to any clinical AI paper and is not specific to this paper's contribution.
- **Several speculative claims about why baselines failed** (e.g., "the baselines were not properly configured") — The *fact* that baselines are at/below chance is kept as a weakness; speculation about the specific cause is removed.
- **Critique that augmentation parameters were chosen heuristically** — Minor and speculative; a reasonable practice in exploratory work.
- **"The three listed contributions are restatements of the same architectural choice"** — Partially valid but folded into the novelty assessment.
- **The comment about Equation 1 vs. Equation 2 being inconsistent** — While observationally accurate, this is more about presentation clarity and is subsumed by other issues.

## Novel Insights

The review surfaces a critical pattern: the baseline evaluation in Table 1 is internally inconsistent with prior results on the same dataset (Table 2). This creates a structural evidentiary gap where the paper's primary claim (state-of-the-art performance) rests on a comparison that cannot be trusted. Beyond the paper's own contributions, the key takeaway is that for SSL-based medical time-series papers, careful baseline verification against known results on the same data is essential before claiming superiority.

## Suggestions

- **Fix the baseline evaluation.** Re-run all Table 1 baselines with proper hyperparameter tuning on this dataset, report variance, and verify that the results are consistent with any published results on the same data. If the gap remains, the claim becomes credible; if it shrinks, report honestly.
- **Clarify the pretraining data.** Specify exactly what unlabeled data was used for SSL pretraining, including the number of subjects/segments and whether it came from the same distribution as the labeled evaluation set.
- **Correct the abstract numbers** or provide a clear formula for the claimed 31.5% and 25.4% relative improvements.
- **Report variance** for all LOSO results and include a statistical significance test for the main comparison against BI-MCGNN.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>