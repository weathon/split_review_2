Now let me re-read key experimental sections more carefully to verify claims.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me run Round 1 calibration — bracketing across score bands with topic-relevant queries.Let me read the most relevant anchor papers for calibration. I'll focus on MaskGCT (5.25, very similar topic), Simple-TTS (3.00, rejected TTS), DiTTo-TTS (6.25, accepted TTS), and the interpolating AR+diffusion paper (8.00).Now I have enough information to form my bracket and finalize the review. Let me assess:

**Round 1 Bracket:**
- DiSTAR is clearly much stronger than rejected TTS papers at 3.0 (Simple-TTS, Fox-TTS) — those had poor audio quality, weak baselines, or overclaimed novelty.
- DiSTAR seems stronger than MaskGCT (5.25, accepted) — DiSTAR introduces a more novel AR+masked-diffusion coupling and has cleaner practical contributions.
- DiSTAR is comparable to DiTTo-TTS (6.25, accepted) — both have clean contributions and good experiments, though DiTTo-TTS had more exhaustive ablations.
- DiSTAR is clearly not at the level of the interpolating AR+diffusion paper (8.00) which had deep theoretical contributions.

**Initial bracket: 5.5 – 7.0**

Now let me write the final review.

---

## Summary
DiSTAR is a zero-shot text-to-speech framework that operates entirely in discrete RVQ (residual vector quantization) code space, coupling an autoregressive language model (for inter-patch temporal dependencies) with a masked diffusion Transformer (for intra-patch parallel decoding in the layer-time RVQ domain). The system eliminates duration predictors and forced alignment, and offers practical features including variable bitrate via RVQ layer pruning and robust greedy decoding. Experiments on LibriSpeech-PC and SeedTTS test-en demonstrate state-of-the-art WER and strong subjective quality scores.

## Strengths

- **Best robustness (WER) across both benchmarks.** DiSTAR-medium achieves 1.66% WER on LibriSpeech-PC (vs. human 1.80%) and 1.32% on SeedTTS test-en (vs. human 1.47%), clearly leading all baselines in Table 1. This is a strong, concrete result.
- **Strong subjective evaluation results.** Table 2 shows DiSTAR achieves the highest SMOS (3.31±0.25, exceeding E2TTS's 3.29 and CosyVoice 2's 3.07) and CMOS (0.22±0.13, the only system with a meaningfully positive score). This establishes perceptual quality beyond what objective metrics alone can show.
- **Parameter efficiency.** DiSTAR-medium (0.3B) outperforms DiTAR (0.6B) on WER across both benchmarks while using half the parameters (Table 1), demonstrating efficient use of capacity.
- **Clean architectural contribution.** The coupling of AR drafting with LLaDA-style discrete masked diffusion for RVQ codes (Section 3.1.1, Eq. 1–2) is a well-motivated design that avoids continuous-latent optimization issues while naturally handling the joint time-depth structure of RVQ. The formulation is rigorous.
- **Practical controllability.** Stochastic layer truncation during training (Section 3.4) enables test-time RVQ layer pruning for variable bitrate without retraining, demonstrated in Figure 2 with graceful degradation across 2–9 layers. Greedy decoding produces competitive results (Table 3), a practical advantage over systems requiring careful sampling.

## Weaknesses

### Fatal
None

### Major
- **NFE mismatch undermines efficiency claims.** DiSTAR uses NFE=24 while the most directly comparable system, DiTAR, uses NFE=10 (Table 1). The paper claims "inference cost close to its continuous counterpart DiTAR" (Section 1, final paragraph) but provides no wall-clock time, real-time factor, or FLOPs comparison. With 2.4× more diffusion steps, DiSTAR may actually be substantially slower despite using fewer parameters. This makes the efficiency narrative unsubstantiated as written.
- **Speaker similarity (SIM) gap is understated.** DiSTAR-medium achieves 0.67/0.66 SIM on LibriSpeech/SeedTTS, while E2TTS reaches 0.70/0.71 and F5TTS reaches 0.68/0.68 (Table 1). The paper states "SIM on par with the best alternatives" (Section 4.2), which overstates the objective result. While subjective SMOS is strong (3.31), the 0.03–0.05 objective SIM gap to flow-matching baselines is non-trivial and deserves honest discussion rather than being glossed over.

### Minor
- **Limited main-paper ablations.** The ablation study (Section 4.3) covers only decoding strategies (Table 3, three rows). Key architectural choices — aggregator design, overlapping vs. non-overlapping patches, the scalar gate for scale mismatch (Section 3.3), embedding initialization from codebook channels (Section 3.4) — are not ablated. Some analyses are deferred to appendix (patch size in Appendix D, CFG in Appendix C), but the main paper's ablation section is thin relative to the number of design decisions made.
- **Inconsistent baseline sets across evaluation tables.** Table 1 (objective) includes DiTAR and IndexTTS but not FireRedTTS or CosyVoice 2; Table 2 (subjective) includes FireRedTTS and CosyVoice 2 but not DiTAR or IndexTTS. This asymmetry makes it difficult to form a complete picture of any single baseline's standing relative to DiSTAR.
- **Decoding heuristic complexity.** The inference strategy (Section 3.4) involves six interacting hyperparameters (T_layer=0.8, T_time=0.95, top-k=50, top-p=0.9, temperature annealing 1.0→0.1, P_r=4 repetition window, 50/50 hybrid sampling/greedy). While the paper acknowledges the "half-half scheme to avoid over-tuning," no sensitivity analysis is provided, leaving it unclear how brittle these choices are.
- **English-only evaluation.** The training corpus (Emilia) is multilingual, but all evaluation is on English subsets. No evidence is provided that the approach generalizes across languages, limiting the scope of the "zero-shot TTS" claim.

### Trivial
None

## Nice-to-Haves
- Wall-clock time / RTF measurements at matched NFE and quality levels, or at minimum an NFE sweep showing the quality-latency tradeoff for DiSTAR.
- Ablation of the aggregator overlap mechanism and the scalar gate conditioning.
- At least one non-English evaluation to demonstrate multilingual generalizability.
- Analysis of failure modes or long-form synthesis robustness beyond standard short-utterance benchmarks.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- *(No explicit harsh critic input was provided, so no specific points were filtered out. The review above was constructed directly from paper reading.)*

## Novel Insights
The core insight of DiSTAR — that masked discrete diffusion (LLaDA-style) can serve as an effective intra-patch decoder for multi-codebook RVQ codes while AR handles inter-patch temporal dependencies — is a genuinely novel architectural decomposition for speech synthesis. This avoids the known optimization difficulties of continuous diffusion over high-dimensional latents while preserving the stability and interpretability of discrete token modeling. The stochastic layer truncation training trick for enabling test-time compute/bitrate control without retraining is a practical and transferable contribution.

## Suggestions
- Provide wall-clock time or RTF measurements to substantiate the efficiency claim. If DiSTAR is indeed slower than DiTAR at NFE=24, an NFE sweep showing comparable quality at lower NFE would strengthen the paper.
- Report SIM results honestly — acknowledge the gap to flow-matching baselines and discuss whether this is an inherent tradeoff of the discrete RVQ representation or an area for improvement.
- Add ablations for the aggregator design (overlapping vs. non-overlapping) and the scalar gate, as these are design choices specific to DiSTAR.
- Align the baseline sets between objective and subjective evaluations so readers can form complete comparisons.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to DiSTAR |
|-------|------|-----------|-------|---------------------|
| Simple-TTS | m4mwbPjOwb.md | 3.00 | 1 | Much weaker: poor audio quality, weak baselines, overclaimed end-to-end nature |
| Fox-TTS | pWdkM9NNCA.md | 3.00 | 1 | Much weaker: limited novelty, less comprehensive evaluation |
| DM-Codec | UFwefiypla.md | 3.00 | 1 | Different focus (codec design), weaker results |
| Blind Audio Problems | mlPTNEIsgb.md | 3.25 | 1 | Different domain, not directly comparable |
| DLPO | WzrkZeDxrM.md | 4.25 | 1 | Weaker: narrower contribution (RL fine-tuning for TTS diffusion) |
| Zero-Shot TTS Streaming | RK3Gj9J5my.md | 4.60 | 1 | Different focus (streaming), weaker evaluation |
| Diffusion Language Models | Qn4HEhezKW.md | 5.00 | 1 | Different domain (text), comparable novelty but DiSTAR has stronger empirical results |
| MaskGCT | ExuBFYtCQU.md | 5.25 | 1 | Similar topic; DiSTAR has a cleaner AR+diffusion coupling and stronger practical features, but MaskGCT had 100K hrs training |
| DiffAR | GTk0AdOYLq.md | 5.75 | 1 | Similar concept (AR+diffusion for speech); DiSTAR operates in discrete space with stronger results |
| RADD | sMyXP8Tanm.md | 6.20 | 1 | Different domain (text diffusion theory); DiSTAR is more applied but with strong empirical results |
| DiTTo-TTS | hQvX9MBowC.md | 6.25 | 1 | Comparable: both are accepted TTS papers with clean contributions; DiTTo-TTS had more thorough ablations, DiSTAR has better WER results |
| SEDD | 71mqtQdKB9.md | 6.60 | 1 | Different domain (discrete diffusion for text); stronger theoretical depth but DiSTAR has strong applied results |
| Interpolating AR+Diffusion | tyEyYT267x.md | 8.00 | 1 | Clearly stronger: deeper theoretical contribution with strong experimental validation |

**Round 1 bracket: 5.5 – 7.0**

DiSTAR sits comfortably above MaskGCT (5.25) due to its cleaner architectural contribution and stronger empirical results. It is comparable to DiTTo-TTS (6.25) — DiSTAR has better WER results and a more novel architecture, but DiTTo-TTS provided more thorough ablations. DiSTAR does not reach the level of the interpolating AR+diffusion paper (8.00) which had substantial theoretical contributions.

The paper's strengths — SOTA WER, strong subjective scores, clean architecture, practical features — push it toward the upper end of this bracket. The weaknesses — NFE mismatch obscuring efficiency claims, understated SIM gap, limited ablations — are real but addressable and do not undermine the core contribution. The NFE mismatch is the most concerning issue as it affects a key claimed advantage, but it is a presentation/evaluation gap rather than a fundamental flaw.

**Final score: 6.0** — Borderline accept. The paper makes a solid empirical contribution with a clean architectural design and strong results on standard benchmarks. The core AR+masked-diffusion idea is well-motivated and the discrete RVQ approach avoids known issues with continuous latent modeling. However, the evaluation has notable gaps (no timing data despite efficiency claims, NFE mismatch with the primary comparison system, understated SIM results, thin ablations), which prevent a confident accept. The contribution is real and the paper would benefit the community, but the presentation of results could be more honest and the experimental analysis more thorough.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>