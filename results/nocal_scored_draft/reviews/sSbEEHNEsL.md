Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper proposes USR 2.0, which improves the USR semi-supervised framework for unified speech recognition (ASR/VSR/AVSR) by replacing the expensive autoregressive pseudo-label generation with CTC-driven teacher forcing and a mixed sampling strategy. The method halves training time, substantially improves OOD robustness, and achieves state-of-the-art in-distribution results across all three tasks with a single unified model.

## Strengths

- **Well-motivated, practical solution to two genuine bottlenecks in USR: AR decoding cost and decoupled supervision brittleness.** The core idea of CTC-driven teacher forcing directly targets both problems simultaneously.
- **Comprehensive OOD evaluation across three distinct distribution shifts** (long utterances on VoxCeleb2, additive babble noise on LRS3, cross-dataset generalization to LibriSpeech/WildVSR/AVSpeech) — substantially more thorough than most papers in this area.
- **Mixed sampling ablation (Figure 4) honestly reveals the trade-off among ID accuracy, OOD robustness, and training time**, showing that OOD degrades sharply at high AR probabilities while ID is relatively flat. This is an informative empirical finding that supports the method's design.
- **Two sources of speedup are identified and distinguished** (faster per-step decoding + faster convergence needing fewer epochs), which is valuable and rare in efficiency-focused papers.
- **State-of-the-art results across ASR, VSR, and AVSR on LRS3, LRS2, and WildVSR** using a single unified model, including at scale (Huge model with ~2500h unlabelled data).

## Weaknesses

### Fatal
None.

### Major

1. **The 2× training speedup claim confounds per-step efficiency gains with different stopping criteria (50 vs. 75 epochs, line 275).** While the paper identifies both factors, the main text does not isolate them — the reader cannot tell how much of the speedup is attributable to the method's per-step advantage versus simply stopping 25 epochs earlier. A clean comparison (e.g., running USR for 50 epochs to match USR 2.0's epoch count) would resolve this. The paper references Appendix C.5, but the main presentation should separate these factors.

2. **The theoretical framing in Section 4.1 (lines 108–111) overstates the sufficiency of the 'coherence' argument and underplays the essential role of mixed sampling.** The paper claims "global incoherence of the teacher-generated sequence does not hinder learning" in CTC-driven mode, but Figure 4 shows that pure CTC-driven mode (0% AR) achieves 3.2% ID WER while the best mixed sampling achieves 2.8% (and pure AR mode achieves 2.9%). Mixed sampling is not a minor mitigation — it is empirically essential for closing the train-test gap on ID performance. The framing would be more accurate by explicitly stating upfront that CTC-driven teacher forcing introduces exposure bias, which mixed sampling then resolves.

### Minor

1. **No variance or statistical significance reporting.** All WERs (Tables 1–4) are reported as single numbers without confidence intervals or run-to-run variance. Several key ID comparisons involve small margins (e.g., USR 2.0 vs USR at 0 dB AVSR: 14.0% vs 14.8%; ASR Base LRS3: 3.0% vs 3.2%) where the significance of the difference cannot be assessed. Single-run reporting is common in speech recognition benchmarks, but the small-margin claims would benefit from variance estimates.

2. **The loss weighting choices (0.5/0.5 for attention vs. CTC decoder targets in CTC-driven mode, Equation 5) are not justified.** Why 0.5? And why is the decoder supervised with collapsed CTC targets (which are frame-level) in a decoder that typically operates on token-level sequences? An ablation of this weighting would strengthen the presentation.

3. **No direct ablation isolating whether the gains come from the CTC-driven conditioning itself vs. the new loss formulation.** The paper does not include a baseline that applies the same loss weighting from Equations 5–6 to the original USR framework without CTC-driven teacher forcing.

4. **No pseudo-label quality analysis.** The paper asserts that CTC-driven teacher forcing produces better pseudo-labels but never directly measures pseudo-label accuracy (e.g., by comparing teacher outputs to ground truth on a held-out set), which would validate the claimed mechanism behind the downstream gains.

### Trivial
None.

## Nice-to-Haves

- **Disentangle the two speedup factors:** run USR for 50 epochs (matching USR 2.0's epoch count) and report its performance.
- **Reframe the coherence argument:** acknowledge upfront that CTC-driven teacher forcing introduces exposure bias, and present pure-CTC-driven mode as an efficiency-only variant with an ID accuracy trade-off.
- **Justify (or ablate) the 0.5 weighting choices** in Equations 5–6.
- **Add a pseudo-label quality analysis** (e.g., WER against ground truth on a held-out subset) to validate the claimed mechanism.

## Removed Points

- **Concern about Whisper as an oracle for VoxCeleb2 transcription:** The paper clearly discloses this and applies it consistently across all methods. The critic themselves noted it is "clearly disclosed."
- **Missing cross-modal analysis (attributing gains to audio vs. video vs. fusion):** This asks the paper to address a modality-attribution question outside its stated scope (the paper is about a pseudo-labelling method, not modality analysis).
- **AVSpeech OOD comparison less informative:** The claim that AV-HuBERT's 26.0% is "essentially comparable" to USR 2.0's 25.0% ignores that USR 2.0 still outperforms it, and the other two OOD datasets (LibriSpeech: 15.4% vs 29.1%; WildVSR: 73.7% vs 82.4%) show large, unambiguous advantages.
- **Request for pure CTC-only pseudo-labelling baseline (no attention targets):** This would discard the paper's decoder supervision entirely — not a standard or informative ablation for a method that is fundamentally about combining CTC and attention.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface observations about the paper that the authors had not already made.

## Suggestions

1. Disentangle the two speedup factors by running USR for 50 epochs (matching USR 2.0's epoch count) and reporting its performance.
2. Reframe the coherence argument to explicitly acknowledge CTC-driven teacher forcing's exposure bias and present mixed sampling as essential (not auxiliary) for ID performance.
3. Report variance (2–3 runs or confidence intervals) for the key small-margin ID comparisons.
4. Justify or ablate the 0.5 weighting choices in Equations 5–6.
5. Add a pseudo-label quality analysis to validate the claimed mechanism behind downstream gains.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>