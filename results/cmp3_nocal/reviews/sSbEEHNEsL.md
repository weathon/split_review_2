## Summary

This paper proposes USR 2.0, which replaces the autoregressive pseudo-labelling in Unified Speech Recognition (USR) with **CTC-driven teacher forcing**: greedily decoded CTC outputs are fed into the decoder to generate attention-based pseudo-labels in a single parallel forward pass, eliminating the AR bottleneck. A mixed-sampling strategy (50% CTC-driven, 50% AR) mitigates the resulting train-test mismatch. The method achieves ~2× training speedup, substantially improved OOD robustness (long utterances, noise, domain shift), and state-of-the-art results on LRS3, LRS2, and WildVSR across ASR, VSR, and AVSR with a single unified model.

## Strengths

- **Clean, well-motivated core idea with a principled justification (Section 4.1).** The insight that global coherence of CTC-driven attention outputs is irrelevant in pseudo-labelling because teacher and student share the same conditioning is genuinely clever and theoretically grounded. This turns an apparent limitation into a non-issue.

- **Large, well-documented training speedup (~2×) directly attributable to the method (Figure 5, Section 6).** The speed advantage is visually unambiguous across multiple model scales. The paper attributes it to both faster per-step decoding and fewer epochs (50 vs. 75), with concrete evidence.

- **Comprehensive robustness evaluation across three OOD axes: input length (VoxCeleb2), noise (NOISEX at multiple SNRs), and unseen datasets (LibriSpeech, WildVSR, AVSpeech).** The evaluation covers both greedy and beam-search decoding, and the consistent gains are compelling. The flat WER curve for long utterances (Figure 3a) is striking.

- **Transparent ablations (Table 4, Figure 4).** Table 4 separately tests each PL-target configuration for both modes, cleanly showing the individual contribution of CTC and attention PLs. Figure 4 exposes the ID/OOD/efficiency trade-off controlled by the mixed-sampling probability.

## Weaknesses

### Fatal
None.

### Major

- **OOD evaluation on VoxCeleb2 (long-utterance experiments, Figure 3) and AVSpeech (Table 3) relies on Whisper-generated "ground truth" without any analysis of how transcription noise could affect comparisons.** The paper acknowledges these are "automatically transcribed" and treats Whisper "as an oracle," but Whisper itself makes errors. If USR 2.0's outputs happen to correlate more closely with Whisper's systematic biases (e.g., because CTC-based models share properties with Whisper's training pipeline), some of the reported advantage could reflect agreement with a proxy rather than genuine WER reduction. This concern does *not* apply to the in-distribution LRS3 results (ground-truth labels), the noise experiments (Table 1, also on LRS3 with ground truth), or the LibriSpeech evaluation (standard ground truth). The overall pattern of results is still convincing, but the absolute WER numbers on these OOD sets should be interpreted with caution.

### Minor

- **No statistical significance or variance reported for any result.** All WERs in every table and figure are point estimates with no error bars, confidence intervals, or multiple-seed results. Since several comparisons involve small margins (e.g., Table 2: USR 2.0 ASR 1.3 vs. USR ASR 1.2 in Large high-resource; USR 2.0 VSR 36.2 vs. USR VSR 36.0 in Base low-resource), variance information would substantially strengthen the precision of the claims. This is noted as a limitation, though single-run evaluation is standard in this community.

- **The framing against self-supervised baselines (AV-HuBERT, BRAVEn, etc.) understates the methodological differences.** USR and USR 2.0 are semi-supervised methods that leverage unlabelled data *during fine-tuning* via pseudo-labelling, whereas the baselines use unlabelled data only during *pre-training* followed by supervised fine-tuning. The paper acknowledges this implicitly via the "shared params" column and different unlabelled data amounts, but the presentation ("surpassing... self-supervised baselines") does not explicitly discuss the paradigm advantage. A clearer separation of in-paradigm (USR vs. USR 2.0) and cross-paradigm comparisons would improve the scientific framing.

- **No USR baseline at the Huge model scale.** The paper reports a Huge USR 2.0 model (17.6% VSR, 0.9% ASR, 0.8% AVSR) but does not train an equivalent-scale USR model. This means the scaling results demonstrate feasibility but not relative improvement over the prior method at the largest scale.

### Trivial
None.

## Nice-to-Haves

- **Quantify the impact of Whisper transcription noise.** A simple control experiment on LRS3 (with ground truth) comparing method rankings under ground-truth vs. Whisper-transcribed labels would bound the concern raised above.
- **Report 3+ random seeds for the main in-distribution settings** (Table 2), which is the single most impactful improvement for rigor.
- **Provide a concrete measure of "global incoherence"** (e.g., perplexity or BLEU of CTC-driven vs. AR attention PLs on a sample of teacher outputs) to make the theoretical argument more tangible.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"No discussion of student-decoder conditioning at inference time"* — The paper explicitly discusses this in Section 4.2 (lines 114–115): "it introduces a mismatch: the decoder is trained using inputs derived from the teacher's CTC predictions, whereas at inference time it autoregressively conditions on its own past outputs." The mixed-sampling strategy is designed specifically to address this.
- *"Relative contribution of faster training steps vs. fewer epochs not quantified"* — The paper provides concrete numbers: 50 vs. 75 epochs (33% reduction) and cites Appendix C.5 for details.
- *"Non-autoregressive transformers discussion is thin"* — A brief treatment in the Related Work section is appropriate; this is scope creep.
- *"Global coherence theoretical subtlety about local token predictions"* — The ablation in Table 4 already shows this is not a practical problem (ID WER 3.3 vs. 3.2). The reviewer's own assessment says it is "not a significant problem in practice."
- *"Equation (4) clarification needed"* — The paper is sufficiently clear about the parallel forward pass.
- *"Table 2 formatting is difficult to parse"* — Parser artifact; no weight in evaluation.
- *"LRS2 results deferred to appendix"* — Appendix is stripped by the parser; cannot be evaluated as a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a short sensitivity analysis comparing method rankings under ground-truth vs. Whisper-transcribed labels on a held-out set (e.g., a subset of LRS3) to bound the Whisper noise concern.
2. Report variance (e.g., 3 random seeds) for the main in-distribution results in Table 2.
3. Include a USR baseline at the Huge scale, or at least explicitly acknowledge its absence as a limitation when discussing scaling results.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>