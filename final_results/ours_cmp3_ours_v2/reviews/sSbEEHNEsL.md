Now let me write the final consolidated review.

## Summary

This paper proposes USR 2.0, which addresses two key limitations of the USR semi-supervised framework for unified speech recognition: the computational bottleneck of autoregressive pseudo-label generation and the brittleness of decoupled CTC/attention supervision under distribution shift. The core idea — CTC-driven teacher forcing — replaces slow AR decoding with parallel attention label generation conditioned on greedily decoded CTC outputs, exploiting the insight that global coherence is unnecessary for self-training when teacher and student share the same conditioning prefix. Combined with a mixed sampling strategy to mitigate exposure bias, USR 2.0 achieves ~2× training speedup, substantially improved OOD robustness, and state-of-the-art results on LRS3, LRS2, and WildVSR benchmarks.

## Strengths

1. **Well-articulated limitations of prior work (Section 3).** The paper isolates two concrete failure modes in USR: (i) autoregressive pseudo-labelling requires one forward pass per output token at every training step, and (ii) decoupled CTC/attention supervision causes greedy AR decoding errors to compound through the self-training loop. These are traced to specific architectural and algorithmic choices, not vague hand-waving.

2. **Principled and non-obvious core idea.** The observation that greedily decoded CTC outputs can feed into the decoder to generate attention targets in parallel, and that the resulting lack of global coherence is harmless in pseudo-labelling (because teacher and student share the same conditioning prefix), is a genuine insight that reframes a constraint imposed by inference as irrelevant for training.

3. **Evaluation covers the right ground.** The paper tests its claims along four axes aligned with the stated motivations: OOD robustness (long utterances, noise, cross-dataset), in-distribution accuracy, training efficiency (wall-clock time), and scaling. The long-utterance results (Figure 3), noise robustness (Table 1), and OOD datasets (Table 3) directly probe the claimed robustness benefit.

4. **Ablation study (Table 4, Figure 4) is informative and not cherry-picked.** The contrast between CTC-driven mode and AR mode on OOD data (24.2% vs. 40.1% WER) cleanly supports the method's central thesis. The mixed-sampling sweep (Figure 4) is presented as a trade-off with three dimensions (ID accuracy, OOD robustness, training time) rather than only the chosen operating point.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **VSR regression on Base/LRS3 is not discussed.** In the low-resource Base setting (Table 2), USR 2.0's VSR WER (36.2%) is *worse* than USR's (36.0%) — a 0.2% regression. The paper reports the ASR (3.0 vs. 3.2) and AVSR (2.9 vs. 3.0) gains in this setting but does not acknowledge the VSR reversal. While it may be noise, the absence of discussion or multi-run variance estimates prevents the reader from assessing this.

2. **No explicit limitations discussion.** The conclusion projects broadly to handwriting recognition, music transcription, and DNA sequencing, but never discusses settings where the method might underperform — e.g., when the teacher's CTC head is itself poor under extreme domain shift, or when clean in-distribution data makes AR pseudo-labels already sufficient. This omission makes the paper read as though the method has no downsides.

3. **Huge model result lacks a same-scale USR baseline.** The Huge model (Table 2, right column) achieves strong SOTA results, but USR was not scaled to this size. This makes it hard to attribute the gains specifically to the proposed method rather than to increased capacity or the larger unlabelled corpus. The paper is transparent about the missing baseline, but the claim that improvements are due to the method itself is weakened.

4. **Whisper-transcribed OOD evaluation has an acknowledged but unaddressed limitation.** For the long-utterance experiment (VoxCeleb2, Section 5.1) and the AVSpeech evaluation (Table 3), "ground truth" comes from Whisper rather than human transcription. The paper is transparent about this (calling it "automatically transcribed" and "treating Whisper as an oracle"), but it does not discuss how Whisper's systematic biases could correlate with the methods being evaluated. The LibriSpeech evaluation in the same Table 3 uses human labels and shows a large gap (15.4 vs. 25.3), which mitigates this concern for the core OOD claim.

### Trivial

1. **No variance reporting.** WER results are reported as single numbers without confidence intervals or standard deviations. This is standard practice in large-benchmark speech recognition, but it makes it impossible to assess whether the small VSR regression or some of the modest gains (e.g., AVSR 2.9 vs. 3.0 on Base/LRS3) are meaningful.

## Nice-to-Haves

- Multi-seed experiments for the Base/LRS3 setting where USR 2.0 regresses on VSR, to clarify whether the difference is systematic or noise.
- Direct analysis of attention PL quality from CTC-driven teacher forcing (e.g., PL WER against ground truth as a function of input length or SNR) to test the claimed mechanism more directly than downstream results alone.
- A brief discussion of Whisper transcription quality for the OOD evaluations — e.g., a small human-verified subset or Whisper's WER on a known benchmark.

## Removed Points

These points were considered but removed as they reflect speculation, scope creep, or misreading:

- **"The mixed sampling strategy adds complexity and a hyperparameter that must be tuned"** — The paper already acknowledges this and characterizes the trade-off via Figure 4, concluding the default of 0.5 offers a strong balance. The hyperparameter dimension is inherent to the design choice and is addressed.
- **"CTC-driven teacher forcing depends on the teacher's CTC quality"** — Speculative concern about a failure mode not tested in the paper; could apply to any method that relies on its own outputs. Not specific enough to be a concrete weakness.
- **"Missing related work"** — Not verifiable without external sources; the paper's related work section is adequate for the scope.
- **Formatting/style nitpicks** — Removed per policy (parser artifacts, not author issues).

## Novel Insights

None beyond the paper's own contributions. The reviews largely converge on the same assessment: the paper makes a clear, well-supported contribution with minor presentational gaps.

## Suggestions

1. Add a brief "Limitations" paragraph discussing regimes where the method may not help (e.g., when the CTC head is unreliable, or when clean in-distribution unlabelled data makes AR teacher forcing already adequate).
2. Report multi-seed WER with standard deviations for the Base/LRS3 setting where USR 2.0 shows a VSR regression.
3. For the Whisper-transcribed evaluations, include a one-sentence caveat about potential systematic bias and, if possible, provide a small human-verified subset for calibration.

## Score and Decision

Now let me calibrate using the retrieved anchors.

**Bracket (Round 1):** Based on comparison with anchors, this paper sits between 6.5 and 8.0.

**Anchors used for calibration:**

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| CR-CTC (CIs9x2ZRgh) — consistency regularization for CTC ASR | 6.75 | 1 | Similar domain, accepted. Our paper has broader evaluation (3 modalities, OOD), clearer motivation, and larger empirical gains. Marginally stronger. |
| Unsupervised ASR via Cross-Lingual PL (4lOWCkhr4g) | 5.25 | 1 | Limited novelty, narrow scope. Our paper is substantially stronger in all dimensions. |
| Sylber (FyMjfDQ9RO) — syllabic speech representation | 6.75 | 1 | Different contribution type (representation learning). Claims about downstream benefits were questioned. Our paper has stronger empirical validation. |
| Align With Purpose (fUGhYVPVRM) — CTC controllability | 7.00 | 1 | Method paper for CTC, accepted. Similar rigor; our paper has slightly broader scope (multi-modal) and more comprehensive ablations. |
| Weakly-supervised Audio Separation (4N97bz1sP6) | 6.67 | 1 | Different sub-area. Similar evaluation breadth. |
| Realistic SSL Evaluation (RvUVMjfp8i) | 8.00 | 1 | Different contribution type (benchmark+theory), not directly comparable. |

**Narrowing:** The paper is stronger than CR-CTC (6.75) and comparable to Align With Purpose (7.00). The weaknesses are all minor — none threaten the core claims. The OOD robustness results are particularly strong. A score of 7.0 reflects a solid method paper with real contributions and well-executed evaluation, while accounting for the minor issues noted above.

**Final Score: 7.0** — This is a strong paper with a clear, well-motivated contribution and solid experimental validation. The weaknesses are minor and addressable. The CTC-driven teacher forcing idea is genuinely insightful, and the OOD robustness results coupled with ~2× training speedup represent a clear advance over the prior state of the art.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>