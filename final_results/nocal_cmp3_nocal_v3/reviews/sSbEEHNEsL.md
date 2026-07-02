## Summary

This paper proposes USR 2.0, a semi-supervised speech recognition framework that replaces the autoregressive pseudo-labelling bottleneck of the prior USR method with CTC-driven teacher forcing: greedily-decoded CTC outputs from the teacher are fed into the decoder as a prefix to generate attention-based pseudo-labels in a single forward pass. A mixed sampling strategy (alternating between CTC-driven and autoregressive modes) mitigates train-test mismatch. The method achieves ~2× faster training, substantial out-of-distribution robustness gains (long utterances, noise, cross-dataset), and state-of-the-art in-distribution results across ASR, VSR, and AVSR with a single unified model.

## Strengths

1. **Genuinely clever technical insight with clear motivation (Section 4.1).** The core observation — that in a pseudo-labelling setting, global coherence of the teacher's attention outputs is unnecessary because teacher and student operate under the same forced CTC inputs — meaningfully breaks the assumed dependency between pseudo-label quality and generation mode. This is a conceptual contribution, not an engineering tweak. The idea is cleanly motivated by the two specific limitations diagnosed in USR (decoupled supervision causing OOD brittleness; AR decoding as a speed bottleneck).

2. **Comprehensive and well-structured empirical validation.** The paper evaluates along four distinct axes: (a) OOD robustness on long utterances (Figure 3), noise at four SNR levels (Table 1), and cross-dataset transfer (Table 3); (b) in-distribution performance across three modalities and multiple resource settings (Table 2); (c) training efficiency (~2× wall-clock speedup, Figure 5); and (d) scaling to a Huge model. This is a complete evaluation package that directly supports the claimed advantages.

3. **Results that are both clean and impactful.** The OOD improvements are large and consistent (e.g., Table 3: LibriSpeech 15.4% vs. USR's 25.3%; WildVSR 73.7% vs. 80.0%). The long-utterance robustness (Figure 3a) is striking: USR 2.0 maintains ~35% WER at 600 frames while USR climbs to ~80% under greedy decoding. The in-distribution SOTA results confirm that OOD gains do not come at the cost of ID performance.

4. **Ablations that isolate key design choices (Table 4, Figure 4).** The ablation of PL targets per branch in both CTC-driven and AR modes cleanly shows: (a) both CTC and attention targets are needed for the decoder (neither alone suffices), (b) CTC targets are especially important for OOD robustness, (c) AR mode degrades sharply on OOD compared to CTC-driven mode. The mixed-sampling ablation (Figure 4) shows the expected tradeoff curve and supports the default choice of 0.5.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Training speedup claim conflates two factors without decomposition (Section 6, Figure 5).** The paper reports ~2× faster training and correctly identifies two contributing factors: faster per-step decoding (CTC-driven teacher forcing avoiding AR) and faster convergence (50 epochs vs. USR's 75). However, these are not decomposed quantitatively — the reader cannot tell what fraction of the total speedup comes from each source. Since the epoch reduction (50 vs. 75) could partially reflect a hyperparameter choice (it is not obvious whether USR could converge in fewer epochs with tuning), the headline claim would benefit from reporting per-iteration wall-clock time separately. The practical speedup is real, but the claim is less precise than it should be.

2. **Huge model results lack computational budget details (Section 6).** The paper reports state-of-the-art Huge model results (17.6% VSR, 0.9% ASR, 0.8% AVSR) but does not report the computational budget (GPU-hours, distributed setup, training duration). While model architecture details and hyperparameters are deferred to Appendix A (stripped by the parser), compute budget is absent from the text entirely. For a paper that prominently reports these numbers in the abstract, this omission makes it harder for practitioners to assess practical feasibility or to reproduce the results.

3. **Whisper-as-oracle evaluation on VoxCeleb2 could benefit from explicit caveat discussion (Section 5.1).** The paper discloses that VoxCeleb2 samples are "automatically transcribed" using Whisper (line 192) and that AVSpeech samples are "transcribed using Whisper" (line 241). However, the paper does not discuss potential limitations of this approach — e.g., whether Whisper's own errors could correlate with utterance length, potentially biasing the long-utterance WER curves. Since the same qualitative trends hold on LibriSpeech (which uses standard ground truth), this does not invalidate the conclusions, but a brief caveat would strengthen the paper's rigor.

### Trivial

1. **"Seen Lengths" column in the Figure 3 table is unexplained.** The table in Section 5.1 includes a fifth column labeled "Seen Lengths" with values matching the USR 2.0 column. The caption does not define this column. (This may be a parser artifact from the PDF extraction; either way it should be clarified.)

## Nice-to-Haves

- **Decompose the training speedup quantitatively:** report per-iteration wall-clock time for CTC-driven vs. AR pseudo-labelling separately from total training epochs, so readers can assess how much of the speedup is architectural versus due to early stopping.
- **Add qualitative examples / error analysis:** a few sample transcriptions showing where USR 2.0 succeeds and USR fails (e.g., on long utterances or noisy inputs) would help readers understand the error patterns being avoided.
- **Clarify the distinction from scheduled sampling:** the paper states its method is "similar to scheduled sampling (Bengio et al., 2015) but for a different type of exposure bias" (line 114). A brief explanation of what is different about this setting compared to classic scheduled sampling would help readers situate the contribution.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"Statistical significance is not reported":** The reported differences (e.g., USR 2.0 2.9% vs. USR 3.0% AVSR) are small in some cases, but significance testing is not standard practice for large-benchmark evaluations in this field, and the key comparisons (OOD results) show large, unambiguous gaps. Removed as a generic expectation mismatch.
- **"Scheduled sampling comparison needs clearer explanation":** The paper explicitly states the difference — "a different type of exposure bias" (line 114) — which is sufficient for context. The reviewer's request for more detail is reasonable as a suggestion but not a weakness. Moved to Nice-to-Haves.
- **"Missing related works":** Cannot be verified without external sources; removed per policy.
- **"Huge model hyperparameters not described":** The paper states "full details, including model sizes and hyperparameters, are given in Appendix A" (line 157). The appendix is stripped by the parser but exists in the original submission. Removed per policy on missing appendix content.
- **Formatting/style nitpicks and parser artifacts:** Removed per policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Decompose the training speedup by reporting per-iteration wall-clock time separately from total training time/epochs, so the reader can separate architectural gains from early-stopping effects.
- Add a brief discussion of limitations when using Whisper as an oracle for evaluation (e.g., potential bias on long utterances).
- Report the computational budget (GPU-hours, distributed setup) for the Huge model experiments.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>