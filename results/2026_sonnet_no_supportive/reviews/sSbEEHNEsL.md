Let me read one of the 6.75 AVSR anchor papers for calibration:**Round 1 bracket:** Based on the calibration anchors and paper quality, USR 2.0 sits between **7.0 and 7.5**. It is significantly stronger than the 6.75 AVSR anchor (CAV2vec): it has SOTA results across multiple benchmarks, a well-evidenced ~2× speedup, large and consistent OOD gains, and a genuinely novel mechanism. The one major weakness (greedy-only OOD comparison) is acknowledged by the paper and partially mitigated in Figure 3b/3c. The 8.0 anchors appear cleaner in terms of methodological completeness. I'll land at **7.5**.

---

## Summary
USR 2.0 proposes CTC-driven teacher forcing as a drop-in replacement for autoregressive pseudo-label generation in the Unified Speech Recognition (USR) framework. Instead of decoding the teacher's attention branch autoregressively, it feeds the teacher's greedily decoded CTC outputs as a fixed prefix into the decoder, enabling a single parallel forward pass. A mixed sampling strategy (50% CTC-driven, 50% standard AR) mitigates the resulting train-test mismatch. The result is approximately 2× faster training, large OOD robustness improvements, and state-of-the-art results on LRS3/LRS2/WildVSR across ASR, VSR, and AVSR with a single unified model.

## Strengths
- **Elegant, non-obvious core idea with direct mechanistic justification.** Section 4.1 argues that global coherence is unnecessary in the pseudo-labelling setting because teacher and student share the same CTC-derived forced prefix — matched conditioning makes token-wise cross-entropy valid even if the full sequence lacks global coherence. This reframes the standard objection to non-autoregressive teaching and is directly consistent with its stated motivation.
- **Large, multiply-supported OOD robustness gains.** Table 3 shows 39% relative improvement on LibriSpeech (25.3→15.4%), 7.9% on WildVSR (80.0→73.7%), and 28% on AVSpeech (34.7→25.0%) under greedy decoding. Figure 3a shows categorical stability of USR 2.0 on utterances up to 600 frames while USR degrades dramatically beyond 200 frames, supported by multiple baselines (AV-HuBERT, BRAVEn).
- **Concrete, well-evidenced ~2× training speedup.** Figure 5 shows wall-clock curves across Base, Large, and Huge models all converging to equivalent WER in approximately half the time. The mechanism is precisely quantified (0.013s CTC vs. 0.471s AR per sample, Figure 1).
- **Well-designed ablations.** Table 4 isolates each PL type's contribution to each branch under each mode with internally consistent results. Figure 4 presents a genuine tradeoff curve across AR sampling probability, not a single cherry-picked operating point.
- **Strong in-distribution results and scalability.** USR 2.0 achieves state-of-the-art at every model scale tested (Base through Huge), including 17.6%/0.9%/0.8% VSR/ASR/AVSR with a single unified Huge model, outperforming modality-specific baselines.

## Weaknesses

### Fatal
None.

### Major
- **OOD evaluation in Table 3 uses greedy decoding only, which is the condition most favorable to USR 2.0 relative to USR.** The paper explicitly demonstrates (Figure 3b, 3c) that beam search substantially recovers USR's performance on long VoxCeleb2 utterances. Standard inference uses beam size 40 with joint CTC rescoring. However, the beam-search comparison is limited to VoxCeleb2 long utterances and is not extended to the Table 3 benchmarks (LibriSpeech, WildVSR, AVSpeech). The claim "USR 2.0 outperforms all baselines by a wide margin" (Section 5.3) may overstate the practical gap when all systems use matched standard inference conditions. This is an evidential limitation, not a structural flaw — the OOD advantage is likely real — but the magnitude of gains under matched beam-search conditions on these benchmarks is unknown.

### Minor
- **Mixed sampling's contribution is modest and its role is overstated in abstract/introduction.** Figure 4 shows pure CTC-driven training (AR prob = 0.0) yields 3.2% ID / 24.2% OOD AVSR WER, while the default 50% mixture yields 2.9% ID / 25.0% OOD. The ID improvement is 0.3 absolute and OOD is slightly worse. CTC-driven teacher forcing is the dominant factor; mixed sampling provides incremental ID benefit at a minor OOD cost. The paper treats mixed sampling as a co-equal contribution in its framing, though it does present Figure 4 transparently.
- **In-distribution gains are absent in the pure ID unlabelled setting.** Table 2 (Base/LRS3, no VoxCeleb2) shows USR 2.0 VSR at 36.2% vs. USR's 36.0% — essentially identical. USR 2.0's in-distribution benefit depends on OOD unlabelled data being present, which is stated but could be emphasized more clearly.
- **AVSpeech WER measures agreement with Whisper, not ground-truth accuracy.** Section 5.3 notes transcriptions are Whisper-derived; the relative comparison is valid, but absolute WERs are Whisper-agreement metrics, and this is only briefly mentioned.

### Trivial
None.

## Nice-to-Haves
- A direct pseudo-label quality measurement (e.g., teacher WER on VoxCeleb2 over training epochs for USR vs. USR 2.0) would directly validate the central claim that CTC-driven PLs degrade less under OOD inputs, removing the need to infer pseudo-label quality indirectly from downstream WER.
- At least one OOD benchmark from Table 3 (e.g., LibriSpeech) evaluated under beam search for both USR and USR 2.0 would make the robustness claims more decisive and remove the decoding-condition ambiguity in the major weakness above.
- A targeted analysis of failure modes — when CTC quality is low enough that the CTC-driven attention pseudo-labels become harmful — would strengthen Section 4.1. This is deferred to Appendix C.4 but warrants brief main-paper treatment given it is a central design concern.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Request for variance/statistical significance testing:** Single-run evaluation is standard practice in large-scale audiovisual ASR benchmarks. Removing as not a community-standard requirement.
- **Concern that mixed sampling does not adequately address exposure bias:** The paper provides a theoretical motivation (Section 4.2) and Figure 4 is transparent about the empirical magnitude. The contribution is real even if modest; not a weakness beyond what is already captured under Minor.
- **Global coherence dismissal insufficient:** The paper provides a formal matched-conditioning argument in Section 4.1 and defers additional analysis to Appendix C.4. The argument is sound at the level presented in the main paper. Removed as the reviewers' concern is addressed.
- **Claim that in-distribution improvement is contingent on OOD unlabelled data (framed as weakness):** The paper explicitly states this hypothesis and it is internally consistent with all results. This is a characterization of scope, not a flaw.

## Novel Insights
The most genuinely novel insight is the reframing of global coherence as a non-requirement in teacher-forcing-based self-training: when teacher and student are conditioned on the same CTC-derived prefix, the student learns valid token-level predictions regardless of whether the full forced sequence is globally coherent. This decouples the question "is this a good sequence?" from "does training on this sequence produce correct conditional distributions?" — a distinction that was implicit in prior work but not systematically exploited. The aligned-target insight (CTC and attention PLs share the same sequence length under CTC-driven forcing, enabling joint prediction in a single decoder pass) is an elegant practical consequence that couples CTC robustness with attention expressiveness without any additional parameters or inference overhead.

## Suggestions
- Include a beam-search OOD comparison for at least one Table 3 benchmark (LibriSpeech test-clean is straightforward to decode with beam search) to let readers assess the gain magnitude under matched inference conditions.
- Add a brief analysis (even one figure) measuring teacher-generated pseudo-label WER on a held-out OOD set (e.g., VoxCeleb2 long utterances) over the course of training for both USR and USR 2.0 — this is the most direct validation of the paper's central claim.
- Clarify in the main text body that AVSpeech WER is relative to Whisper transcriptions (currently mentioned briefly in Section 5.3 but easy to miss).
- State explicitly in the abstract or introduction that the dominant factor is CTC-driven teacher forcing and that mixed sampling provides incremental ID benefit — the current framing overstates mixed sampling as a co-equal contribution.

---

## Score and Decision

**Anchor papers and scores:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| gwZ90hFSL2.md | 1.0 | R1 | Unrelated robotics/NLP paper — strong reject |
| UFwefiypla.md | 3.0 | R1 | Speech tokenization, rejected; narrower scope, no speedup |
| aXSxSu3fvg.md | 3.0 | R1 | Semi-supervised DL early stopping; generic, no speech |
| gW4bdLwypB.md | 3.4 | R1 | Multilingual multi-task ASR; scored 5-10, divergent reviews |
| 4lOWCkhr4g.md | 5.25 | R1 | Unsupervised cross-lingual ASR; decent but narrower |
| baNW94qdsU.md | 4.0 | R1 | Self-training multimodal alignment; borderline |
| TCFtGBTxkq.md | 4.0 | R1 | MUTUD audiovisual deployment; similar domain, weaker results |
| 74IIsh2kM6.md | 5.0 | R1 | AVSR Siamese masked learning; AVSR but weaker contribution |
| M8J0b9gNfG.md | 6.2 | R1 | Multilingual VSR with units; solid but narrower than USR 2.0 |
| WEQL5ksDnB.md | 6.75 | R1 | CAV2vec robust AVSR; good but no speedup, narrower SOTA |
| 4N97bz1sP6.md | 6.67 | R1 | Weakly-supervised audio separation; different problem |
| 5BXWhVbHAK.md | 6.33 | R1 | Cross-modal synergy; different problem |
| TPZRq4FALB.md | 8.0 | R1 | Multi-modal TTA; strong but different setting |
| tyEyYT267x.md | 8.0 | R1 | AR+diffusion interpolation; strong, different domain |

**Round 1 bracket:** 7.0–7.5

USR 2.0 is meaningfully stronger than the 6.75 AVSR anchor (CAV2vec): it achieves SOTA at multiple scales, demonstrates a well-evidenced 2× speedup with a novel and principled mechanism, and delivers large consistent OOD gains. The one major weakness (greedy-only OOD comparison for Table 3) is acknowledged and partially addressed in the paper. No round 2 needed — the bracket is clear at 7.5.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>