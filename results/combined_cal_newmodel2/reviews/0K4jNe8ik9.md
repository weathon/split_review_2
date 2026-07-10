## Summary

This paper proposes DGNet, a multi-head SimCLR adaptation for EEG-based dementia classification. The core idea is to decompose EEG into five canonical frequency bands (delta, theta, alpha, beta, gamma), learn separate representations per band via independent CNN encoders with adaptive temperature parameters, and then evaluate on AD vs. CN classification using linear evaluation with Leave-One-Subject-Out (LOSO) cross-validation on an 88-subject dataset. The paper reports 92.90% accuracy, claiming large improvements over baselines.

## Strengths

- **Clinically motivated framing (Section 1).** The paper correctly identifies the diagnostic bottleneck in dementia screening, makes a well-reasoned case for EEG as a scalable alternative to MRI/PET, and grounds the multi-band design in known neurophysiological signatures of Alzheimer's disease (spectral slowing — increased delta/theta, decreased alpha/beta/gamma). The neurophysiological motivation is accurate and specific.

- **Plausible architectural choice.** Decomposing EEG into canonical frequency bands with independent per-band encoders (Section 2.1) is a reasonable inductive bias that respects the distinct neurological significance of each band and prevents cross-band interference. The multi-band encoding with five parallel 1D conv encoders is clearly described.

- **Ablation study covers multiple components.** Table 3 systematically ablates SSL pretraining vs. training from scratch, single-head vs. multi-head, augmentation, adaptive temperature (τ=0.1), and regularization, providing diagnostic insight into which components drive performance.

## Weaknesses

### Major

- **Potential data leakage from ambiguous pre-training / LOSO protocol.** The paper describes a two-stage process (Section 3, lines 124-125): first "pre-training" on unlabeled data, then "linear evaluation" with LOSO. Nowhere does it specify whether pre-training was performed once on the entire 88-subject dataset or nested within each LOSO fold. The sequential framing ("During the pre-training stage… In the subsequent linear evaluation stage…") and the singular definite article ("the pre-trained encoder weights") strongly imply a single pre-trained model used for all folds. If pre-training used all subjects' data, then in each LOSO fold the held-out subject's data was already seen during pre-training, violating subject independence. The paper claims LOSO "prevents data leakage between subjects and ensures complete independence between the training and validation sets" (line 148), making this ambiguity especially critical to resolve. Without clarification, the main results cannot be interpreted.

- **Baseline performance at or below chance on a binary task is unexplained.** In Table 1, 8 of 12 established EEG baselines perform at or below chance (39-54%) on AD vs. CN classification (~50% baseline). EEGInception (39%), EEGNet (46%), Deep4Net (49%), FBCNet (48%), and TIDNet (44%) are all below or at chance. These architectures have been validated across dozens of EEG studies. Their simultaneous near-chance performance does not indicate the proposed method is unusually strong — it indicates the evaluation setup or hyperparameter configuration may be systematically flawed. This must be diagnosed and explained before the comparison can be considered informative.

### Minor

- **No variance reported for the proposed method.** Tables 1 and 2 report the proposed method's accuracy (92.90%) and F1 (92.85%) as bare point estimates with no variance. For LOSO on 88 subjects, per-fold variance is standard and expected. Notably, Table 2 includes "91.25 ± 0.38" for BI-MCGNN, showing that variance reporting was possible, yet the proposed method's results lack it. Without variance, the reader cannot assess result stability.

- **Discrepancy in classifier dimensions.** The Figure 1 caption states the linear evaluation classifier uses "two linear layers (with 612 and 256 units respectively)." Section 2.1 (line 82) states "the first hidden layer contains 512 nodes, and the second hidden layer contains 256 nodes." The first-layer dimension differs (612 vs. 512), changing the model's parameter count. This must be resolved for reproducibility.

- **Confounded ablation.** The "w/o augmentation" condition (Table 3, line 199) does not simply remove augmentations from the contrastive pipeline. Instead, it replaces the entire training objective: "we masked 15% of the EEG signal and trained the encoder model to reconstruct it using mean squared error (MSE) loss." This changes the objective (contrastive → reconstruction), the loss function (NT-Xent → MSE), and the data processing (augmentations → masking) simultaneously. It therefore does not isolate the effect of data augmentation.

- **Missing FTD evaluation.** The dataset (Section 3.1) contains three diagnostic groups: 36 AD, 23 FTD, and 29 CN. Only AD vs. CN binary classification is reported. FTD is an important differential diagnosis for AD. The paper's framing about "dementia diagnosis" implies broader scope than the binary AD vs. CN task actually evaluated. Reporting AD vs. FTD or three-way classification would substantially strengthen clinical relevance.

- **Mismatched relative improvement numbers in abstract.** The abstract claims "a 31.5% relative performance improvement over training from scratch." From Table 3, the actual improvement is (92.90 − 63.35) / 63.35 × 100 = 46.6%, not 31.5%. Similarly, "25.4% improvement over the single-head approach" should be (92.90 − 73.52) / 73.52 × 100 = 26.4%. These numbers should be consistent.

### Trivial

None.

## Nice-to-Haves

- The "w/o augmentation" ablation could be redesigned to isolate augmentation effects. Instead of switching to reconstruction, the natural ablation would remove augmentations and use standard contrastive learning with identity transformations (or simpler augmentations).
- Visualization of learned representations (t-SNE/UMAP) colored by class would help assess whether SSL produces class-discriminative structure.
- Per-subject confusion matrix or accuracy breakdown would reveal whether results are driven by a few subjects or are consistent.

## Removed Points

- **"Modest novelty relative to prior work":** Removed because this is an opinion-based judgment, not a concrete, verifiable weakness. The multi-band SimCLR adaptation with per-band encoders is an architectural contribution; novelty assessments are better reflected by the overall evaluation.
- **"Multi-head (5 heads) vs Adaptive 5 band heads label confusion":** The text (line 199) partially clarifies that "Multi-head (5 heads)" refers to training from scratch while "Adaptive 5 band heads" includes SSL pre-training. Though the table could be clearer, the narrative addresses this. Subsumed under the confounded ablation point for the w/o augmentation row.
- **Strengths removed as generic/superficial:** None — all three kept strengths are specific and evidence-grounded.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the pre-training / LOSO protocol explicitly.** State whether SSL pre-training was performed once on all 88 subjects or nested within each LOSO fold. If it was done once on all data, the evaluation must be redesigned (e.g., subject-disjoint pre-training set or nested cross-validation). If it was nested, describe the procedure clearly.
2. **Diagnose and explain why 8 of 12 baselines perform at or below chance.** Investigate hyperparameter configurations and training procedures for these baselines. Include results from the proposed encoder trained from scratch in a supervised manner within each LOSO fold as a main-table baseline to calibrate expectations.
3. **Report variance (mean ± std) for all LOSO results**, including the proposed method.
4. **Resolve the 612 vs. 512 discrepancy** in classifier dimension.
5. **Fix the relative improvement numbers** in the abstract to match the actual computed values.
6. **Consider adding AD vs. FTD and three-way classification results** to strengthen clinical relevance.

---

**Calibration anchors retrieved across all rounds:**

| Anchor Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| /home/.../5lUdTogEL3.md | 1.00 | R1 | No | Unrelated topic (person re-ID); irrelevant |
| /home/.../u1cQYxRI1H.md | 10.00/0.50† | R1 | No | Unrelated (illumination harmonization); not comparable |
| /home/.../6uReXuDWrw.md | 2.00 | R1 | Yes | UniEEG (SSL EEG pretraining). Poor writing, missing baselines, limited novelty. Our paper has clearer motivation and better architectural grounding, placing it above 2.0. |
| /home/.../TkbjqexD8w.md | 3.00 | R1/R2 | Yes | Invariant Spatiotemporal (EEG SSL for seizure). Single dataset, limited evaluation. Comparable to our paper's evaluation limitations, but our paper has a data leakage concern that this anchor does not. |
| /home/.../YKfJFTiRz8.md | 5.00 | R1/R2 | Yes | EEG-DisGCMAE (SSL graph pretraining for EEG). More thorough evaluation (two datasets, extensive ablations) than our paper. Our paper's evaluation concerns (data leakage ambiguity, baseline anomaly) place it below 5.0. |
| /home/.../cWEfRkYj46.md | 6.00 | R1 | Yes | H2DiLR (SSL for intracranial decoding). Accept with mixed reviews (5,8,3,8). Stronger evaluation methodology than our paper. |
| /home/.../NPNUHgHF2w.md | 6.75 | R2 | No | CBraMod (EEG foundation model). Strong evaluation across multiple tasks. Our paper's concerns are more severe. |

† Score 0.50 was returned but appears to be a data issue with the query's score filter.

**Round 1 bracket:** 3.0–5.0 (between Invariant Spatiotemporal at 3.0 and EEG-DisGCMAE at 5.0)

**Round 2 narrowing:** Comparing against Invariant Spatiotemporal (3.0) and EEG-DisGCMAE (5.0): our paper's strengths (clinical motivation favorability 13.14, ablation study favorability 10.98) are stronger than Invariant Spatiotemporal's strengths (motivation favorability 5.81). However, our paper has the data leakage ambiguity and baseline anomaly (favorability -2.66) which are more severe than typical weaknesses in these anchors. The baseline anomaly (favorability -2.66) is the strongest negative signal and pulls the paper below EEG-DisGCMAE (5.0). But the paper's clear clinical framing and ablation quality keep it above 3.0.

**Final score: 4.0** — grounded in the comparison: the paper's strengths (favorability 9-13) and one serious evaluated weakness (baseline anomaly, favorability -2.66) place it between the 3.0 anchor (weaker strengths, fewer contributions) and the 5.0 anchor (more thorough evaluation).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>