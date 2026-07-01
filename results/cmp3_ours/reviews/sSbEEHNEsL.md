Now let me finalize the review with calibration anchors and score.

**Round 1 bracket:** Based on comparison with the retrieved anchors, the narrowest plausible score range is [7.0, 8.0].

The paper is clearly stronger than topically similar anchors in the 6.5-7.0 band (CR-CTC at 6.75, Multi-Task Corrupted Prediction for AVSR at 6.75, Align With Purpose at 7.0) because it presents a more novel methodological contribution with broader scope (unified model across three modalities), more comprehensive OOD evaluation, and a clear practical advantage (2× faster training). The weaknesses are genuine but minor — they do not threaten the core contribution. At the same time, the paper is not at the 8+ level, which would require exceptional impact and essentially no weaknesses.

**Narrowing:** Comparing against CR-CTC (6.75, scores 6,5,8,8) and Align With Purpose (7.0, scores 6,6,8,8) — both accepted at ICLR-like venues for modest but sound contributions — this paper has a stronger, more novel core idea and more thorough evaluation. This places it solidly above those anchors. A score of **7.5** reflects that this is a clear accept with a genuine contribution and minor presentation issues, but not flawless.

**Anchor papers retrieved:**
- CR-CTC (6.75, Round 2): Consistency regularization for CTC. Smaller-scope contribution; this paper's core idea is more novel.
- Multi-Task Corrupted Prediction (6.75, Round 2): AVSR robustness via corrupted prediction. Comparable evaluation breadth but less novel methodology.
- Align With Purpose (7.0, Round 2): CTC alignment optimization framework. Solid but narrower contribution.
- Scaling Speech-Text Pre-training (7.0, Round 2): Synthetic interleaved data. Different sub-area.
- Cross-Lingual Pseudo-Labeling (5.25, Round 1): Pseudo-labeling for ASR. Less novel, narrower scope.
- Sylber (6.75, Round 2): Syllabic speech representation. Different sub-area.
- DM-Codec (3.0, Round 1): Speech tokenization. Different topic.

Final review:

## Summary

USR 2.0 proposes CTC-driven teacher forcing and mixed sampling to improve the efficiency and robustness of pseudo-labelling for Unified Speech Recognition (USR). The core idea is to use CTC-decoded outputs as decoder input during teacher pseudo-labelling (avoiding slow autoregressive decoding), and to alternate between this CTC-driven mode and standard AR mode to mitigate exposure bias. The method achieves ~2× faster training, strong OOD robustness gains, and competitive in-distribution results across ASR, VSR, and AVSR with a single unified model.

## Strengths

1. **Clean, well-motivated core idea.** The insight that CTC pseudo-labels can serve as decoder input during teacher pseudo-labelling because global coherence is unnecessary when teacher and student share the same conditioning is genuinely clever and clearly articulated (Section 4.1). The claim that CTC is ~40× faster and far more OOD-robust than AR decoding is concretely demonstrated (Figure 1), making the motivation precise.

2. **Comprehensive OOD robustness evaluation.** The paper evaluates OOD robustness across three distinct axes: long utterances (Figure 3), additive babble noise at multiple SNR levels (Table 1), and cross-dataset generalization (Table 3). The finding that USR 2.0 maintains stable WER on sequences far beyond the labelled training length (155 frames) while USR degrades catastrophically (Figure 3a) is striking and well-supported.

3. **Informative ablations with clear design choices.** Table 4 systematically ablates which pseudo-label types are used for each branch in each mode, cleanly separating ID and OOD effects. Figure 4's sweep over the mixed-sampling probability reveals the expected trade-off between ID performance, OOD robustness, and training time, with the default of 0.5 empirically justified.

4. **Training efficiency is documented, not just claimed.** Figure 5 shows WER vs. wall-clock time across model scales. The 2× speedup is decomposed into faster per-step execution (CTC-driven mode avoids AR) and reduced epoch count (50 vs. 75). This is the right kind of evidence for an efficiency claim.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Marginal ID gains in the lowest-resource setting, with a small VSR regression.** In the Base LRS3 low-resource setting (Table 2, left), USR 2.0 achieves VSR WER of 36.2% vs. USR's 36.0% — a regression. ASR improves 3.2→3.0% and AVSR improves 3.0→2.9%. These improvements are modest (0.1–0.2 WER). The abstract's claim of "surpassing USR" is not uniformly accurate across all settings; the paper would benefit from a more precise characterization of where the method helps most.

2. **The Huge model results lack an equivalently-scaled USR baseline.** The Huge model (Table 2, right) achieves strong results (17.6%/0.9%/0.8%) using ~2500h of unlabelled data, but there is no USR Huge baseline to compare against — comparisons are against other methods' Large models. Without an ablated USR Huge baseline, it is difficult to fully attribute the Huge model's performance to the method rather than to increased model and data scale. An explicit acknowledgment of this limitation would improve credibility.

3. **The "global coherence" argument is asserted but not empirically analyzed.** Section 4.1 argues that global incoherence is harmless because teacher and student share the same conditioning. This is theoretically plausible but the paper does not provide direct analysis of pseudo-label quality (e.g., WER of CTC-driven attention PLs vs. AR attention PLs against ground truth, or characteristic error patterns). Such analysis would strengthen mechanistic understanding of why the method works.

### Trivial
None.

## Nice-to-Have

- The OOD long-utterance evaluation (Section 5.1) uses Whisper-transcribed references as an oracle. A brief discussion of potential systematic bias from Whisper's errors (especially on OOD/long audio) would strengthen the analysis, though the paper does acknowledge this by describing Whisper as an oracle.
- An ablation of the confidence threshold for CTC PLs (Section 4.3) would be useful in principle, since CTC's conditional independence yields probabilities that may not be calibrated like AR token probabilities.
- The noise evaluation (Table 1) uses only babble noise from NOISEX; one additional noise type would strengthen the robustness claim, though this is a minor point given the existing breadth of OOD evaluation.

## Removed Points
- Criticisms about table readability (gray shading stripped by parser, dense row labels) → removed as formatting artifacts from PDF parsing.
- Criticism about "parallel" terminology imprecision (Section 4.1, line 106) → removed as a minor terminology nitpick.
- Criticism about missing statistical significance/confidence intervals → removed; single-run evaluation is standard in this literature and the paper follows community norms.
- Criticism about "padding" in conclusion's broader applications → removed; stating potential future directions is standard and appropriate.
- Strength about "addressing an important problem" → removed as generic and not specific to this paper.
- Criticism about Whisper oracle noise as a "critical issue" → demoted to Nice-to-Have; the paper acknowledges this explicitly ("treating Whisper...as an oracle"), and the criticism is speculative about potential systematic bias without evidence.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. Add a more precise characterization of where USR 2.0 improves over USR and where gains are marginal, especially in the abstract and introduction. The VSR regression in the Base LRS3 setting (36.2 vs 36.0) should be acknowledged.
2. If feasible, run an ablated USR Huge baseline at the same scale, or explicitly state the computational limitations and temper the SOTA claim for the Huge setting accordingly.
3. Add a direct comparison of pseudo-label quality (e.g., per-token accuracy or WER against ground truth) between CTC-driven attention PLs and AR attention PLs on a labeled held-out set to validate the global coherence argument empirically.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>