Now I have sufficient calibration data. Let me compile the final review.

Let me specify the round-1 bracket and round-2 analysis.

**Round 1 Bracket:** After comparing my draft's item favorabilities with the anchors, the paper clearly sits above the 5-7 range (where papers have negative-favorability weaknesses or much lower strength favorabilities) and in the 7-8 range.

**Round 2 Narrowing:** Comparing with the 7.00 anchors (Align With Purpose, Out-Of-Domain Unlabeled Data):
- Those anchors have some weaknesses with negative favorability (-4.87, -3.26, etc.)
- This paper has NO negative favorability weaknesses (minimum is 4.46)
- This paper's minimum strength favorability (11.91) exceeds most anchors' maximum strengths

Comparing with the 8.00 anchor (Realistic Evaluation SSL):
- That anchor is a benchmark paper with different evaluation criteria
- Its strengths max at 14.62 and min at 7.70
- This paper's strengths range 11.91-15.98, which is a tighter high cluster

The paper under review is a strong method paper with clear contributions. It's better characterized as a solid accept (~8.0) rather than a borderline accept (~6.0).

Now let me write the final review.

---

Let me be very precise about the anchors I used for my comparison.

Anchors retrieved and compared:
1. CR-CTC (CIs9x2ZRgh.md) - 6.75 - Itemized - CTC consistency regularization for ASR. Less comprehensive evaluation, narrower scope.
2. Align With Purpose (fUGhVYPVRM.md) - 7.00 - Itemized - CTC alignment optimization. Has negative-favorability weaknesses not present in this paper.
3. CAV2vec (WEQL5ksDnB.md) - 6.75 - Itemized - AVSR corruption robustness. Similar domain but different methodology.
4. Cross-Lingual PL (4lOWCkhr4g.md) - 5.25 - Itemized - Unsupervised ASR via pseudo-labeling. Much weaker evidence.
5. Out-Of-Domain Unlabeled Data (Bo6GpQ3B9a.md) - 7.00 - Itemized - Theory paper on SSL with OOD data. Not directly comparable.
6. Realistic Evaluation SSL (RvUVMjfp8i.md) - 8.00 - Itemized - SSL benchmark/evaluation paper. Different contribution type.

Now let me produce the final review.## Summary

This paper proposes USR 2.0, addressing two key limitations of the prior USR framework for unified speech recognition (ASR, VSR, AVSR): (1) the computational bottleneck of autoregressive pseudo-label decoding during self-training, and (2) decoupled CTC/attention supervision that increases OOD brittleness. The core idea — CTC-driven teacher forcing, where greedily-decoded CTC pseudo-labels are fed into the decoder to generate attention targets in a single forward pass — is cleverly motivated by the insight that global coherence is unnecessary in the self-training loop because teacher and student share the same CTC prefix. A mixed sampling strategy mitigates exposure bias. The result is ~2× faster training, strong OOD robustness gains, and state-of-the-art results across all three tasks at scale (0.8% AVSR WER on LRS3 with a Huge model).

## Strengths

- **A genuinely novel and well-motivated technical idea (Section 4.1).** The insight that CTC-driven teacher forcing works for pseudo-labelling even though the resulting attention-based sequences lack global coherence — because teacher and student are conditioned on the same coherent CTC prefix — is clever and non-obvious. The reasoning that "coherence is unnecessary in the self-training loop" is the kind of observation that, once stated, seems obvious in hindsight, which is a hallmark of a good idea. [favorability=15.68]

- **Addresses a real bottleneck in semi-supervised speech recognition.** The computational cost of autoregressive decoding during iterative pseudo-labelling is a well-known practical obstacle. The paper demonstrates a ~2× training speedup (Section 6, Figure 5), partitioned into faster per-step decoding and faster convergence (fewer epochs). This is a practically meaningful improvement. [favorability=14.64]

- **Comprehensive, multi-condition evaluation.** The paper evaluates across three tasks (ASR, VSR, AVSR) on in-distribution (LRS3), noise-perturbed (Table 1, four SNR levels), long-utterance (Figure 3, 50–600 frames), and cross-dataset OOD (Table 3, LibriSpeech, WildVSR, AVSpeech) settings. The noise evaluation with multiple SNR levels and the long-utterance analysis with bucketed lengths go beyond what most speech papers provide. [favorability=11.91]

- **Well-designed ablations.** Table 4 cleanly separates the contribution of each pseudo-label type per branch under both CTC-driven and AR modes. The ablation reveals that (a) both CTC and attention targets are needed in CTC-driven mode for different reasons (OOD robustness vs. ID accuracy), and (b) the OOD gap between the two modes is large (24.2% vs. 40.1%), convincingly showing that CTC-driven teacher forcing genuinely improves robustness. Figure 4's sweep over mixed-sampling probability with both ID and OOD curves is informative. [favorability=15.98]

- **Scaling to a Huge model with ~2500h unlabelled data yields 0.8% AVSR WER on LRS3**, demonstrating that the method works at practical scale — a genuinely impressive result. [favorability=15.71]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **VSR regression on Base/LRS3 is not acknowledged.** In Table 2 (left, low-resource), USR 2.0 Base achieves VSR WER 36.2 vs. USR's 36.0 — a regression. The paper's text says "matches or outperforms" and notes gains "are more pronounced with VoxCeleb2 pre-training," which is true for larger settings but glosses over this one case where USR 2.0 is slightly worse. The improvement is contingent on having additional unlabelled data (VoxCeleb2); when only LRS3 unlabelled data is available, the VSR gain does not materialize. This is consistent with the paper's own thesis (robustness matters more when unlabelled data is OOD), but the framing should be more precise. [favorability=6.67]

- **OOD evaluation partly depends on automatically generated Whisper transcriptions (acknowledged by authors).** For the long-utterance experiment (VoxCeleb2, Section 5.1) and the AVSpeech OOD evaluation (Section 5.3), the reference transcriptions are Whisper-generated. The paper acknowledges this, but ASR errors on challenging OOD data (e.g., WildVSR with 73–82% WER) could be substantial and uneven across methods. This is mitigated by the fact that all methods are compared on the same transcripts, but the absolute WER numbers should be treated with some caution. [favorability=5.76]

- **No variance or statistical significance estimates reported for any main result.** For comparisons where the gap is small (e.g., ASR 1.3 vs. 1.2 on Large, high-resource), it is unclear whether the difference is meaningful or within run-to-run noise. This is a common issue in speech recognition papers but weakens confidence in marginal improvements. [favorability=4.46]

- **The confidence-based filtering threshold (0.8, inherited from USR) is not ablated or discussed beyond a single sentence in Section 4.3.** Since pseudo-label quality is central to the method's success, it would be informative to know whether USR 2.0's different PL generation characteristics (CTC-driven vs. AR mode) interact with this threshold. [favorability=5.06]

### Trivial
None.

## Nice-to-Haves

1. **A controlled ablation isolating the benefit of coupled CTC-attention supervision** from the benefit of having *any* better supervision. Comparing against USR with added robustness techniques (e.g., SpecAugment, noise injection) would strengthen the claim that the *coupling itself* is responsible for the OOD gains.
2. **A per-utterance breakdown or qualitative analysis of when CTC-driven teacher forcing produces poor pseudo-labels**, since 50% of training steps use CTC-driven mode.
3. **Reporting of pseudo-label discard rates by the confidence filter** for each mode, to verify that the effective amount of training data does not differ systematically between modes.

## Removed Points
These points are flagged to be removed; treat them with caution:

- "SOTA on LRS2 and WildVSR referenced to Appendix C.1 cannot be verified": REMOVED per rules — the parser strips appendix sections from all papers; they exist in the original submission. The LRS3 results are comprehensively reported in the main text.
- "Missing related works": REMOVED per rules — I cannot confirm the existence of missing references without external sources.
- Various formatting/style nitpicks from the input: REMOVED per rules — these are parser artifacts, not author errors.

## Novel Insights
None beyond the paper's own contributions. The review surfaces that the paper's thesis — coupling CTC and attention supervision during pseudo-labelling improves both efficiency and robustness — is convincingly supported, and that the ablations cleanly demonstrate the complementary roles of CTC (OOD robustness) and attention (ID accuracy) targets.

## Suggestions

1. Acknowledge the VSR regression on Base/LRS3 explicitly and discuss why it occurs (e.g., CTC-driven mode may reduce the decoder's ability to model visual-only sequences when unlabelled data is in-distribution).
2. Add variance estimates or confidence intervals for key comparisons (Table 2, Table 3).
3. Include a small human-annotated OOD subset to validate the Whisper-transcribed evaluation numbers.
4. Ablate the confidence threshold used for pseudo-label filtering.
5. Report pseudo-label discard rates per mode to verify training data volume is comparable.

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| CIs9x2ZRgh.md (CR-CTC) | 6.75 | R1, R2 | Yes | Narrower scope (ASR only); has negative-favorability weaknesses; less comprehensive evaluation |
| fUGhVYPVRM.md (Align With Purpose) | 7.00 | R1, R2 | Yes | Has multiple negative-favorability weaknesses (-4.87 to -0.84); this paper has none |
| WEQL5ksDnB.md (CAV2vec) | 6.75 | R1 | Yes | Similar AVSR domain; different methodology (corruption prediction); weaker evidence |
| 4lOWCkhr4g.md (Cross-Lingual PL) | 5.25 | R1 | Yes | Much weaker evidence base; strong negative-favorability weaknesses |
| Bo6GpQ3B9a.md (Out-Of-Domain Unlabeled Data) | 7.00 | R2 | Yes | Theory paper; has negative-favorability weaknesses; not directly comparable |
| RvUVMjfp8i.md (Realistic Evaluation SSL) | 8.00 | R2 | Yes | Benchmark paper; different contribution type; strengths favorability 7.70–14.62 (this paper: 11.91–15.98) |
| 8QTpYC4smR.md | 1.00 | R1 | No | Survey paper; strong reject; not comparable |
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated topic; strong reject |
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated (GFlowNets); strong reject |
| 5lUdTogEL3.md | 1.00 | R1 | No | Unrelated (person re-id); strong reject |
| 5kMwiMnUip.md | 1.40 | R1 | No | Unrelated (LLM jailbreaking); strong reject |
| UFwefiypla.md | 3.00 | R1 | No | Speech tokenization; reject |
| xRi8sKo4XI.md | 3.00 | R1 | No | Unrelated (prompt learning); reject |
| aXSxSu3fvg.md | 3.00 | R1 | No | Unrelated (SSL early stopping); reject |
| gW4bdLwypB.md | 3.40 | R1 | No | Multilingual ASR; mixed scores |
| E0UsEIRBQ8.md | 3.00 | R1 | No | Underwater object detection; reject |
| 4lOWCkhr4g.md | 5.25 | R1 | Yes | Cross-lingual pseudo-labeling; see above |
| eSO9quCgmz.md | 5.00 | R1 | No | Data-centric SSL insights; reject |
| 7NlGsjrEd8.md | 4.50 | R1 | No | CTC alignment modeling; reject |
| MazxSMs6Hs.md | 3.67 | R1 | No | African-accented ASR; reject |
| jjjxp9Wgjp.md | 4.25 | R1 | No | OOD detection with pseudo-labels; reject |
| 4N97bz1sP6.md | 6.67 | R2 | No | Audio separation; accept |
| LrmPGtnros.md | 6.75 | R2 | No | Hybrid-autoregressive transducer; accept |
| TtKN1TpvUu.md | 6.25 | R2 | No | Non-autoregressive model; accept |
| EMpvfnzQqD.md | 5.67 | R2 | No | Optimal transport CTC; reject |
| FyMjfDQ9RO.md | 6.75 | R1 | No | Syllabic speech representations; accept |
| dnqPvUjyRI.md | 6.00 | R1 | No | SSL reward model; accept |
| M8J0b9gNfG.md | 6.20 | R1 | No | Multilingual VSR; reject |
| H4zAFFyoXK.md | 6.25 | R1 | No | Language-speech pre-training; reject |
| 3tukjsVyrE.md | 7.00 | R2 | No | Speech-text pre-training; accept |
| WNZNsyzcaB.md | 6.75 | R1 | No | Deception detection; reject |
| PdaPky8MUn.md | 8.00 | R1 | No | Long-sequence models; accept |
| tyEyYT267x.md | 8.00 | R1 | No | Diffusion language models; accept |
| Fk5IzauJ7F.md | 8.00 | R1 | No | Partial-label learning; accept |
| OeQE9zsztS.md | 8.00 | R1 | No | Kernel regression; accept |

**Score rationale:** Round-1 bracket identified the 7–8 range. Round 2 narrowed by comparison with itemized anchors: this paper's strength favorabilities (11.91–15.98) uniformly exceed those of the 6.75–7.00 anchors, and critically, this paper has zero negative-favorability weaknesses (minimum 4.46), while every 7.00 anchor has at least one weakness below -0.84. The closest 8.00 anchor (Realistic Evaluation SSL) is a benchmark paper with a different contribution type; this paper's strength profile is comparable or slightly higher. The evidence supports a score of **8.0**.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>