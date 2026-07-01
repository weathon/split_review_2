## Summary

DiSTAR proposes a zero-shot TTS architecture that operates entirely in the discrete RVQ code space, coupling an autoregressive language model (drafts patch-level tokens) with a masked diffusion transformer (infills intra-patch details in parallel). The core ideas are well-motivated: RVQ codes have a natural time×depth grid structure, and the hybrid AR+MD approach respects this structure while enabling blockwise parallelism without an explicit duration predictor. On two standard benchmarks, DiSTAR achieves the best Word Error Rate among all compared systems (1.66 on LibriSpeech-PC, 1.32 on SeedTTS test-en), and the ablation of inference strategies plus the variable-bitrate capability via layer pruning are clean practical contributions.

---

## Strengths

1. **Well-motivated architectural design for the RVQ setting.** The paper correctly identifies that prior RVQ-based TTS work models the time and depth axes in impoverished ways (flattening, delay patterns, etc.), and proposes a decomposition — AR drafter for coarse temporal structure, masked diffusion for intra-patch depth completion — that natively respects the two-dimensional dependency structure of RVQ codes. This is a genuinely novel coupling, and the discrete-on-discrete design avoids the inter-module mismatch of cascaded continuous-discrete pipelines (Sections 3.1.1–3.1.2, Equations 1–2).

2. **State-of-the-art Word Error Rate.** DiSTAR-medium achieves the best WER on both benchmarks (Table 1: 1.66 on LibriSpeech-PC, 1.32 on SeedTTS test-en), outperforming strong continuous baselines (F5TTS: 2.02/1.35) and the discrete-token baseline DiTAR (2.39/1.78). WER is the most direct measure of intelligibility, and these gains are substantial.

3. **Elimination of duration predictor.** The fully discrete formulation with [EOS] tokens removes the need for an explicit duration predictor or forced alignment, a genuine simplification compared to many continuous TTS pipelines (Section 3.1.2, last paragraph).

4. **Variable bitrate via test-time layer pruning.** Stochastic layer truncation during training (Section 3.4) enables pruning upper RVQ layers at inference without retraining, producing a clean quality-compute trade-off (Figure 2). The finding that upper layers primarily affect speaker similarity rather than WER is empirically grounded and practically useful.

---

## Weaknesses

### Fatal
None.

### Major

1. **Speaker similarity (SIM) is below the strongest baselines, yet the paper overclaims parity.**  
   On LibriSpeech-PC, DiSTAR-medium SIM = 0.67 vs E2TTS 0.70 and F5TTS 0.68. On SeedTTS test-en, DiSTAR-medium SIM = 0.66 vs E2TTS 0.71 and F5TTS 0.68 (Table 1). On SeedTTS, the gap between DiSTAR and E2TTS (0.66 vs 0.71) is a ~7% relative difference on a metric where human score is 0.73. Despite this, the abstract claims DiSTAR "surpasses state-of-the-art zero-shot TTS systems in … speaker/style consistency" and the conclusion claims "SOTA … speaker similarity" (lines 9, 263). The paper says SIM is "on par with the best alternatives" (line 209), which is overstated. Two nuances: (a) on LibriSpeech, DiSTAR (0.67) actually beats the RVQ resynthesis ceiling (0.66), so the gap is not uniform across benchmarks; (b) DiSTAR leads on subjective SMOS (3.31 vs E2TTS 3.29 in Table 2), creating a genuine objective-vs-subjective tension. The paper should acknowledge the objective SIM gap and discuss possible reasons rather than asserting parity.

2. **The core architectural claim — that the AR+MD coupling is beneficial — is never ablated.**  
   The paper's central contribution is the hybrid AR drafter + masked diffusion refiner. Yet Section 4.3 (billed as a "detailed analysis") only compares decoding strategies (greedy vs sampling with different temperatures, Table 3). There is no experiment that removes either the AR component (e.g., replacing the AR drafter's output with a fixed/learned constant) or the MD component (e.g., replacing the MD refiner with a feedforward predictor or full AR roll-out across depth layers). Without these controls, the paper cannot attribute its results to the proposed coupling. The patch-size ablation (Appendix D) and CFG settings (Appendix C) are useful but do not address this gap. This is the single most significant missing piece of evidence for the paper's thesis.

3. **The claim of "inference cost close to DiTAR" is unsupported.**  
   The paper states DiSTAR maintains "inference cost close to its continuous counterpart DiTAR" (line 31) and has "comparable or lower computational cost" (line 37). But DiTAR uses NFE=10 while DiSTAR uses NFE=24 — a 2.4× difference in the number of diffusion steps. No wall-clock time, real-time factor, FLOPs, or throughput measurements are provided anywhere. Parameter count is not a substitute for inference-cost measurement; the bottleneck is the number of diffusion model calls. This claim should be either substantiated with measurements or removed.

### Minor

4. **The ablation study in the main text is thin.** Beyond the missing architectural ablation (point 2 above), several design choices are introduced without evaluation: (i) the embedding transplantation trick (borrowing first 16 channels from the codec's codebook, Section 3.4) — is it necessary? Does training fail without it? (ii) stochastic layer truncation — is there a quality cost when using all 9 layers at inference, compared to training without truncation? (iii) the three tail-first bias mitigation heuristics (layer-wise temperature, position-wise temperature, hybrid sampling) — sensitivity to these hyperparameters is not explored. Each is a reasonable design choice, but none are ablated.

5. **No comparison against a pure-AR RVQ baseline (e.g., VALL-E 2) or a pure-MD RVQ baseline (e.g., SoundStorm-style discrete diffusion).** The paper cites both families in related work but does not compare against them directly. Since the paper's thesis is that the hybrid outperforms either pure strategy, including such baselines would directly support the argument. The current baselines (F5TTS, E2TTS, DiTAR) are strong but mostly continuous-latent systems, making it hard to attribute gains specifically to the discrete AR+MD coupling.

6. **No limitations or failure-case discussion.** The paper has no limitations section, which is notable given the overclaimed claims and the identifiable gaps. A candid discussion of where the approach underperforms (e.g., the SIM gap on SeedTTS) would improve the paper's honesty and completeness.

### Trivial
None.

---

## Nice-to-Haves
- Provide wall-clock time, real-time factor, or FLOPs measurements to support or retract the efficiency claim.
- An analysis of whether the training-objective/inference-procedure granularity mismatch (frame-level AR training vs. patch-level inference, noted in Section 3.1.1) introduces any empirical difficulty.
- Explore sensitivity of the tail-first bias mitigation hyperparameters (layer/position temperature schedules, sampling/greedy ratio).

---

## Removed Points
- The claim that DiSTAR is "worse than its own codec's representation ceiling" — this is only true on SeedTTS (0.66 vs RVQ 0.70); on LibriSpeech, DiSTAR (0.67) actually exceeds RVQ resynthesis (0.66). The point about SIM being below the strongest baselines stands, but the codec-ceiling framing is partially inaccurate.
- The suggestion that "no pure-AR or pure-MD RVQ baseline" is a critical omission — demoted to Minor because the paper already includes strong continuous and hybrid baselines; the missing comparison would strengthen the argument but is not a fatal gap.
- Several "Section-by-Section Notes" commentary (e.g., on Section 2 reading like a survey, on Table 2 confidence intervals) that were editorial observations rather than actionable weaknesses.

---

## Novel Insights
None beyond the paper's own contributions. The reviews surface the central tension (the paper claims SOTA speaker similarity but the objective SIM data contradicts this) and the missing ablation of the core architectural coupling, but do not contribute an alternative interpretation of the method's behavior beyond what is on the page.

---

## Suggestions
1. Add an architectural ablation: (a) fix/randomize the AR drafter's output and let only the MD refiner operate; (b) replace the MD refiner with full AR decoding across depth layers. Compare WER, SIM, and inference cost against the full model.
2. Recalibrate the claims about speaker similarity to match the data: acknowledge the objective SIM gap, discuss the objective-vs-subjective tension, and do not claim "SOTA" on this axis.
3. Either provide compute measurements (wall-clock time/FLOPs/RTF) or drop the efficiency claim.
4. Add a limitations paragraph acknowledging the SIM gap, the lack of pure-AR/pure-MD baselines, and any scenarios where the method struggles.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>