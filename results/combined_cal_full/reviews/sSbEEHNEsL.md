Now I have enough information to produce the final review. Let me write it.

## Summary

This paper proposes USR 2.0, which addresses two key limitations of the prior USR semi-supervised framework for unified speech recognition (ASR, VSR, AVSR): the computational cost of autoregressive pseudo-labelling and the decoupled CTC/attention supervision that causes OOD brittleness. The core idea is **CTC-driven teacher forcing** — feeding greedily-decoded CTC outputs as input to the attention decoder to generate attention-based pseudo-labels in a single forward pass, eliminating the autoregressive bottleneck. A mixed-sampling strategy mitigates train-test mismatch. The method achieves ~2× faster training, substantially improved OOD robustness (7–10 point WER gains on out-of-domain data), and state-of-the-art in-distribution results across multiple benchmarks with a single unified model.

## Strengths

- **A genuinely creative core idea.** CTC-driven teacher forcing — feeding greedily-decoded CTC outputs as input to the attention decoder to generate pseudo-labels in a single forward pass — is non-obvious and clever. The insight that global coherence of attention outputs is unnecessary in pseudo-labelling because teacher and student share the same conditioning (Section 4.1) is well-articulated and distinguishes this from naive teacher forcing.

- **Directly addresses a concrete bottleneck with measurable impact.** The paper identifies two clear limitations of USR (slow AR decoding, and decoupled supervision causing OOD brittleness) and resolves both simultaneously. This is not an incremental tweak — it changes the training loop architecture and delivers a ~2× training speedup.

- **OOD robustness results are striking and clearly attribute to the method.** Table 3 shows USR 2.0 achieving 15.4% WER vs. USR's 25.3% on LibriSpeech under greedy decoding, 73.7% vs 80.0% on WildVSR, and 25.0% vs. 34.7% on AVSpeech. These large gaps (7–10 points) cannot be explained by noise and are consistent with the paper's mechanism: coupling CTC and attention supervision prevents the decoder from drifting under domain shift.

- **Ablations are informative and support design claims.** Table 4 cleanly demonstrates that both CTC-based and attention-based targets contribute to performance in different regimes (CTC for OOD robustness, attention for ID quality). Figure 4's analysis of mixed-sampling probability shows a clear trade-off and justifies the default choice of 0.5.

- **Training efficiency is convincingly demonstrated.** Figure 5 and Section 6 show ~2× faster training, decomposed into faster steps (CTC-driven teacher forcing) and fewer epochs (50 vs. 75). This is an unusually practical contribution — many papers claim speedups without isolating the sources.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **No variance or uncertainty reporting.** The paper reports all WERs as single numbers with no standard deviations, confidence intervals, or replication runs. While single-run WER reporting is standard practice in speech recognition, several in-distribution comparisons in Table 2 are very close: e.g., Base LRS3 VSR 36.0 (USR) vs. 36.2 (USR 2.0, a regression), Large LRS3+Vox2 ASR 1.3 (USR 2.0) vs. 1.2 (USR, a regression). Without variance information it is impossible to determine whether these differences are meaningful or within noise. The OOD claims (7–10 point gaps) are clearly robust to this concern, but the in-distribution comparisons should be qualified where differences are narrow.

- **Whisper-based evaluation for OOD datasets is not discussed as a limitation.** Both the VoxCeleb2 long-utterance evaluation (Section 5.1, Figure 3) and the AVSpeech evaluation (Section 5.3, Table 3) use Whisper-generated transcriptions as ground truth. The paper treats Whisper as an oracle but does not discuss how Whisper transcription errors could differentially bias the comparison. This is not a fatal issue — Whisper is domain-general and both USR and USR 2.0 are evaluated against the same references — but the limitation should be acknowledged. (Note: LibriSpeech test-clean in Table 3 uses human-verified transcriptions, so this concern only applies to VoxCeleb2 and AVSpeech.)

- **Missing USR Huge baseline for the scaling results.** The Huge model results (VSR 17.6%, ASR 0.9%, AVSR 0.8%) are presented as evidence of scalability, but there is no USR Huge comparison. The improvements at Base and Large scales are well-controlled, so the trend is consistent, but the absolute Huge numbers conflate method and scale. The paper should either provide a USR Huge comparison (even partial) or clearly caveat that these numbers demonstrate scale feasibility rather than method superiority at that scale.

- **Incomplete disentanglement of coupling vs. pseudo-label quality.** The paper argues USR 2.0's gain comes from coupling CTC and attention supervision, but USR 2.0 changes two things simultaneously: the coupling mechanism and the pseudo-labels themselves (CTC-derived vs. AR). The ablation in Table 4 provides partial disentanglement but does not fully isolate whether the gain comes from better-quality pseudo-labels or from the coupling itself. If CTC pseudo-labels happen to have lower WER than AR pseudo-labels on OOD data, that alone would explain much of the improvement without the coupling story. The paper's mechanistic argument is plausible and the ablations are helpful, but this confound is not explicitly addressed.

### Trivial
None.

## Nice-to-Haves
- A direct analysis comparing the WER of CTC-derived pseudo-labels vs. AR pseudo-labels would strengthen the mechanistic claims.
- A brief limitations paragraph discussing when CTC-driven teacher forcing might struggle (e.g., when CTC predictions are very poor) would preempt an obvious criticism.

## Removed Points
1. **"Self-supervised baseline comparisons lack precision about paradigm differences"** — The paper's related work adequately covers the landscape; the distinction between pre-training (self-supervised methods) and fine-tuning (USR) use of unlabelled data is implicit. This is scope creep.
2. **"Equation (5) equal weighting justification needed"** — A minor presentation suggestion, not a weakness. Equal weighting is a reasonable default that is ablated in the mixed-sampling analysis.
3. **"No analysis of pseudo-label quality"** — A nice-to-have additional analysis, but not a required element for a systems paper whose main metric is final task performance.
4. Several generic strengths from the input review (e.g., "addresses an important problem") were removed as lacking specific evidence or conflicting with verified weaknesses.

## Novel Insights
None beyond the paper's own contributions. The reviews largely confirmed the paper's framing and did not surface contradictions or alternate interpretations that the authors missed.

## Suggestions
1. Add uncertainty information (bootstrap confidence intervals or std across test-set splits) for in-distribution comparisons where differences are small.
2. Acknowledge the Whisper-oracle limitation explicitly in the OOD evaluation sections, noting that both methods are evaluated against the same references and that LibriSpeech uses human labels.
3. Provide a partial USR Huge checkpoint comparison, or explicitly caveat the Huge results as demonstrating scale feasibility rather than method-level improvement.
4. Add a limitations paragraph discussing boundary conditions (e.g., low-quality CTC predictions, aggressive confidence thresholds).

## Score and Decision

Let me calibrate against the retrieved anchors. The most relevant anchors are:

| Anchor | Avg Score | Relevance | Comparison |
|--------|-----------|-----------|------------|
| CR-CTC (CIs9x2ZRgh.md) | 6.75 | High (CTC-based ASR) | Both improve CTC training; CR-CTC has several heavily-negative weighted items (−7.01 for missing citations, −2.40 for unclear generalizability). Our paper has no negatively-weighted items. Our paper's strengths are universally strong (>+4), while CR-CTC has mixed weights. |
| Align With Purpose (fUGhVYPVRM.md) | 7.00 | Moderate (CTC modification) | Has heavy negatives (−9.48 for unclear benefit, −6.95 for missing baselines, −6.30 for marginal improvements). Our paper has no such issues and the practical speedup contribution is stronger. |
| Unsupervised ASR via Cross-Lingual PL (4lOWCkhr4g.md) | 5.25 | Moderate (PL for ASR) | Severe novelty concerns (−9.42, −9.15). Our paper has a genuinely novel core idea with strong validation. |

**Weighted-item comparison:** My draft's items have no negative weights (all weakness weights are +0.85 to +1.97, meaning the model considers them weak concerns). All strength weights are strongly positive (+4.27 to +5.72). This places the paper above CR-CTC (6.75) which had multiple heavy negatives, and above Align With Purpose (7.00) which also had heavy negatives. The closest comparison is CR-CTC (6.75), but our paper has uniformly stronger weighted items.

Round 1 bracket: [6.75, 8.5]. The narrowest plausible range after comparison with anchors is [7.0, 8.0].

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>