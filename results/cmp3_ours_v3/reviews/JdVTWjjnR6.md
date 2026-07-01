Now I have my calibration. Let me produce the final review.

## Summary

This paper proposes HiTNet, a dual-stream architecture for multimodal sentiment analysis under frame-level missing data. The hippocampal-inspired intra-modal stream uses a key-value semantic memory module with sparse activation to recover modality-specific information, while the thalamic-inspired inter-modal stream uses a confidence-perception module to guide adaptive cross-modal completion. Experiments on MOSI, MOSEI, and SIMS benchmarks show generally competitive results, with particularly strong gains on the modality-level missingness analysis.

## Strengths

1. **Well-motivated problem framing.** Frame-level missingness (partial loss within each modality, across all modalities) is distinct from the more commonly studied modality-level missingness. Section 1 (Figure 1) makes this distinction clearly, and it is a genuine gap in the multimodal sentiment analysis literature.

2. **Reasonably thorough ablation study (Table 3).** Each major component (SMM, CPM, Intra stream, Inter stream) and each auxiliary loss (ℒ_ubl, ℒ_cp, ℒ_rec) is systematically removed on two datasets. The consistent degradation supports the claim that the architecture's components contribute positively and are not decorative.

3. **Modality-level missingness analysis (Table 4) is a strong addition.** Under the harder regime of entire modalities being absent, HiTNet achieves ~59% Acc-2 on visual-only and audio-only conditions versus ~49-55% for baselines — approximately 10% gains that are the most striking quantitative result in the paper. This tests the method beyond its core design scenario.

4. **Completion feature visualization (Figure 4).** The Euclidean distance analysis provides a useful sanity check that the intra- and inter-modal streams actually reduce the distance to complete features, beyond end-task accuracy.

## Weaknesses

### Fatal

None.

### Major

1. **Overstated headline claims not supported by tabulated results.** The abstract and contributions claim "1.5%–2.0% average accuracy improvements over state-of-the-art methods across all missing rates." However:
   - On **MOSEI Acc-7**, HiTNet (47.19) is essentially tied with CENET (47.18) — a 0.01% difference.
   - On **MOSEI Acc-2**, the gain over P-RMF (78.14→78.29) is 0.15%.
   - On **SIMS**, P-RMF actually beats HiTNet on MAE (0.500 vs. 0.504) and Corr (0.414 vs. 0.389).
   - Only a subset of MOSI metrics approach 1.5% (e.g., Acc-2: 74.12 vs. 72.81 = 1.31%).

   Furthermore, the paper claims "a substantial 2.56% gain in Acc-7 on MOSEI" (Section 4.4, line 189). Against the strongest baseline CENET (47.18), the gain is 0.01%. The 2.56% is relative to Self-MM (44.70), a weaker baseline. Similarly, the "4.53% improvement in Acc-3 on SIMS" is against P-RMF (54.75→59.28), while the strongest Acc-3 baseline LNLT (57.14) yields a 2.14% gain. These are cases of cherry-picking the weakest comparison point, and the central quantitative claim in the abstract does not hold consistently across datasets.

2. **No statistical significance or variance information despite paper-thin margins.** Section 4.3 states that experiments use 3 random seeds and averages are reported, but no standard deviations, confidence intervals, or significance tests appear anywhere. With margins as small as 0.01% (MOSEI Acc-7) and 0.15% (MOSEI Acc-2), the reader cannot determine whether these differences are meaningful or noise. For a paper whose case rests on outperforming prior work, this is a critical omission.

3. **Baseline results appear erroneous.** The TETFN row in Table 1 shows nearly identical values for MOSI and MOSEI: Acc-7=30.30, Acc-2=69.76/67.68, F1=65.69/63.29, MAE=1.087 — all identical across both datasets. Only Acc-5 (34.34 vs. 47.70) and Corr (0.507 vs. 0.508) differ. This pattern strongly suggests a copy-paste error where MOSEI values were accidentally overwritten with MOSI values. A corrected Acc-7 for TETFN on MOSEI would likely be substantially higher than 30.30, which would change the comparison landscape. Additionally, ALMT on MOSEI shows Acc-7=40.92 and Acc-5=40.92 (identical), which is also suspicious. The paper states baselines are "reported as in LNLTN," but the authors are responsible for verifying reproduced numbers.

4. **Confidence-perception module's training signal undermines its claimed function.** Section 3.5 (Equation 8) trains the confidence score s_m with L2 loss against ŝ_m = 1 - r_m, where r_m is the known missing ratio. The module is trained to output a deterministic function of the known missing rate — it does not learn anything about the quality or reliability of the remaining features. This is a fundamentally simpler capability than "confidence perception" or "assessing modality reliability," and the module could be replaced by the known missing rate itself.

5. **LNLN baseline results in Table 4 are internally inconsistent.** LNLN shows identical Acc-2 (49.03) for {V} (visual only), {A} (audio only), and {V,A} (both visual and audio). Having both modalities should provide strictly more information than either alone; identical performance across all three conditions is implausible and suggests a reporting error that affects the comparison.

### Minor

1. **Per-sequence retrieval mismatch with frame-level missingness framing.** The semantic memory module (Equation 2) uses a mean-pooled query to retrieve a single memory slot per modality per sample. All frames in a sequence receive the same retrieved value after gating. For a problem defined as *frame-level* missingness — where individual frames within a sequence are missing — a per-sequence retrieval cannot complete frame-by-frame.

2. **High hyperparameter sensitivity across datasets.** The loss weight γ (reconstruction loss) is 0.1 for MOSI and SIMS but 9.0 for MOSEI — a 90× difference. α ranges from 1.5 to 10. This variability suggests dataset-specific tuning is important and raises questions about general applicability. The paper defers sensitivity analysis to the appendix.

3. **Selective reporting of SIMS results.** The text claims HiTNet "delivers state-of-the-art or highly competitive results" on SIMS but glosses over that P-RMF achieves better MAE (0.500 vs. 0.504) and Corr (0.414 vs. 0.389). The strength on SIMS is primarily in Acc-3 (59.28 vs. 57.14 for LNLT) while other metrics are mixed.

4. **Bio-inspiration framing gap.** The semantic memory module is a key-value lookup with mean-pooled query, argmax cosine-similarity retrieval, and a learned sigmoid gate — not a high-dimensional associative pattern completion mechanism like Sparse Distributed Memory or Hopfield Networks. The gap between the claimed neurobiological inspiration and the actual mechanism is large, and the bio-inspiration terminology does not drive design decisions.

### Trivial

1. **SIMS Table 2 bold formatting is inconsistent.** P-RMF's F1 (74.65) is bolded despite HiTNet having a higher F1 (77.33), and HiTNet's MAE (0.504) and Corr (0.389) are bolded even though P-RMF has better values on both metrics.

## Nice-to-Haves

- **Memory capacity analysis.** The memory stores only 64 slots, each representing ~255 training examples on MOSEI. Analysis of memory utilization (how many slots are actually used, overwrite frequency, performance variation with N) would clarify whether the memory is doing meaningful work or acting primarily as a learned bias.
- **SAN marginal contribution over SMM alone.** The ablation removes the entire Intra stream but does not isolate the sparse activation network's contribution from the semantic memory module's.
- **Discussion of the missing-rate sampling design choice.** Half the training samples are set to zero missing rate (Section 4.2); the rationale and necessity of this strategy could be clarified.

## Removed Points

- *"72.20% accuracy at 90% missing appears only in the abstract with no table."* This value likely comes from the appendix, which is stripped by the PDF parser. The paper mentions "Detailed performance in different missing rates is provided in Appendix B.3." Not a valid criticism given parser limitations.
- *"Missing related work engagement"* and *"No comparison to generative imputation methods."* The first is excluded per policy (DO NOT mention missing related works). The second is scope creep — the paper compares to SOTA baselines in its domain (LNLN, P-RMF, CENET, TETFN, ALMT, etc.).
- *"Reconstruction module is standard."* The reviewer acknowledges this is standard, not a weakness. The module is an auxiliary loss, not a claimed novelty.
- *"Missing frames per-sample is fine for training but requires complete data at test time."* The paper explicitly states this is a training-time auxiliary supervision (Section 3.6). During inference, only the incomplete input is used.

## Novel Insights

The harsh critic's observation about the confidence-perception module being reduced to learning a function of the known missing rate (ŝ_m = 1 - r_m) is the most incisive point. This reveals a mismatch between the claimed functionality ("assessing modality reliability") and the actual training signal (a deterministic label derived from the mask). This type of framing-reality gap is a broader pattern in bio-inspired ML papers and worth surfacing. The observation about TETFN's MOSEI results being copy-pasted from MOSI is also a concrete verification failure that the authors must address.

## Suggestions

1. **Replace inflated claims with precise, metric-by-metric reporting.** The paper's actual contributions — a well-architected dual-stream model with thorough ablations — are strong enough without the "1.5%–2.0% across all settings" framing. A statement like "consistent improvements of 1.0–1.6% on MOSI metrics, competitive results on MOSEI (tied on Acc-7, modest gains on Acc-2), and mixed results on SIMS" would be both accurate and sufficient.

2. **Provide variance information.** Report standard deviations alongside means for all main results. If the MOSEI margins (0.01% on Acc-7) are within noise, acknowledge this; if variance is low, the thin margins become more credible.

3. **Correct or verify the TETFN and ALMT baseline numbers on MOSEI.** The current TETFN MOSEI values are not credible and may significantly affect the comparison landscape.

4. **Reconsider the confidence-perception module's training signal.** Either acknowledge that it learns a function of the missing rate and justify why this is useful beyond a deterministic recalibration, or redesign it to assess the quality of residual features (e.g., via a self-supervised task correlated with information content rather than the known mask).

5. **Verify the LNLN numbers in Table 4.** Identical Acc-2 (49.03) across {V}, {A}, and {V,A} is not plausible and needs correction.

---

**Calibration Report**

*Round 1 bracket:* 3.5 – 5.5

*Anchors retrieved:*
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/a4O528mek9.md` (avg 3.00, Reject) — "Learning Multi-modal Representations Under Incomplete Data" — poorly written, limited experiments. Our paper is better executed.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XTwwtlEfTF.md` (avg 4.50, Reject) — "Robust Multimodal Learning with Missing Modalities" — unclear math, limited diversity. Comparable to our paper in technical quality; our paper has more thorough ablations but more severe claim-evidence mismatch.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iSLDihAfYi.md` (avg 4.80, Reject) — "Sparsely multimodal data fusion" — limited novelty, poor presentation. Our paper is better written and more methodologically detailed.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/IT7LSnBdtY.md` (avg 5.00, Reject) — "SURE" — solid methodology, diverse experiments, but missing related work coverage. Our paper has similar technical depth but more significant claim-evidence issues.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1L52bHEL5d.md` (avg 6.00, Accept) — "Test-Time Adaptation for Combating Missing Modalities" — clean framing, comprehensive, but had an assumption controversy. Our paper has more methodological issues.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/f1uXrAjpOH.md` (avg 5.40, Reject) — "Open-vocabulary Multimodal Emotion Recognition" — mixed reviews, polarized assessment.

*Final score determination:* The paper has genuine contributions (problem framing, thorough ablations, strong modality-level missingness results) but is undermined by: (1) pervasive claim-evidence mismatch, (2) likely erroneous baseline numbers, (3) no variance information, and (4) a confidence-perception module that does not do what it claims. These issues do not invalidate the paper but require substantial revision before it meets the bar. The paper sits between the 4.50 and 5.00 anchors — closer to the former given the severity of the overclaiming.

**Score and Decision**

<score>4.5</score>
<decision>Reject</decision>