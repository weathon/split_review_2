Now I have sufficient calibration data. Let me produce the final review.

**Round 1 bracket:** I estimate this paper sits between 4.0 and 5.5. The method has genuine novelty but the experimental validation has gaps that prevent it from reaching the accept range.

**Anchors considered:**
- VALL-E 2 (avg 5.00, rejected): Similar TTS domain, similar pattern of limited ablations and baseline concerns. DiSTAR has more architectural novelty but also more experimental gaps (NFE mismatch, uncontrolled baselines).
- MaskGCT (avg 5.25, accepted): Closely related topic (discrete codec TTS with masked generation). DiSTAR's method is more novel, but MaskGCT's experimental rigor is higher.
- Fox-TTS (avg 3.00, rejected): Weaker than DiSTAR in both method and evaluation.
- DiTTo-TTS (avg 6.25, accepted): Stronger experimental validation than DiSTAR.
- Controllable TTS MAE (avg 4.20, rejected): Weaker than DiSTAR — no baseline comparisons.

DiSTAR sits between VALL-E 2 (5.00, rejected) and MaskGCT (5.25, accepted). Given the experimental gaps, I calibrate to 4.5.

---

## Summary

DiSTAR proposes a zero-shot text-to-speech framework that operates entirely in the discrete RVQ token domain, coupling an autoregressive language model (patch-level sketching) with a masked diffusion transformer (intra-patch infilling). The core insight — decomposing the RVQ generation problem into a temporal axis handled by AR and a depth axis handled by masked diffusion — is well-motivated and clearly articulated.

## Strengths

1. **Architectural design is well-motivated and clearly presented.** Section 1 and 3.1 accurately diagnose the joint time-depth structure of RVQ speech codes and propose a natural decomposition: a causal AR LM for coarse patch-level temporal structure and a masked diffusion transformer for resolving multi-codebook depth dependencies within each patch. This intellectual framing is the paper's strongest contribution.

2. **Competitive WER results.** DiSTAR-medium achieves the lowest WER among compared systems on both benchmarks (1.66% LibriSpeech, 1.32% SeedTTS), outperforming F5TTS, E2TTS, and DiTAR with fewer parameters (0.3B vs. DiTAR's 0.6B). This is a genuine empirical strength.

3. **Practical engineering contributions are concrete and reproducible.** The RVQ-aware decoding heuristics (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) in Section 3.4 address a real inference pathology and are specified with sufficient detail to be adopted. The stochastic layer truncation technique for variable-bitrate control (Section 3.4) is also practically useful.

## Weaknesses

### Major

1. **Provenance of baseline numbers is not stated, making comparisons uncontrolled.** Table 1 lists results for IndexTTS, E2TTS, F5TTS, DiTAR, FireRedTTS, and CosyVoice 2, but only DiTAR's numbers are explicitly attributed (♦ "reported in DiTAR paper"). For the remaining baselines the paper does not state whether these were retrained on the same Emilia data or taken from prior publications. If the latter, the comparisons are confounded by differences in training data, evaluation pipelines, and potentially test splits. The same ambiguity applies to the subjective evaluation in Table 2 — the paper does not specify whether the listening tests were conducted by the authors or drawn from other papers. This undermines the central SOTA claim.

2. **NFE mismatch invalidates the inference-cost claim relative to DiTAR.** DiSTAR uses NFE=24 for all reported results, while DiTAR (the "continuous counterpart" the paper directly compares against) uses NFE=10 — a 2.4× difference. The abstract and introduction state DiSTAR "maintain[s] the inference cost close to its continuous counterpart DiTAR," but no experiment matches NFEs between the two models. Without this comparison, the computational efficiency claim is unsupported.

3. **Ablation study does not isolate the method's core architectural contributions.** Table 3 compares three decoding strategies (sampling with/without temperature shaping, and greedy). This tests inference heuristics, not the proposed architecture. There is no ablation that removes the masked diffusion module (AR-only on flattened RVQ tokens), removes the AR sketcher (masked diffusion only on full sequences), or compares against a continuous-latent variant of equivalent capacity — yet these are the paper's claimed innovations. Without such ablations, the reader cannot attribute the results to the proposed design rather than to training data, model scale, or engineering details.

4. **SOTA claims are broader than the evidence supports.** The paper claims state-of-the-art in "robustness, speaker similarity, and naturalness" (abstract, conclusion). However, on speaker similarity (SIM), E2TTS consistently outperforms DiSTAR-medium (0.70 vs. 0.67 on LibriSpeech; 0.71 vs. 0.66 on SeedTTS). On UTMOS (an automatic naturalness proxy), DiTAR beats DiSTAR on SeedTTS (4.15 vs. 4.05). DiSTAR's clear advantage is concentrated in WER; the other metrics show competitiveness but not superiority. The subjective results in Table 2 also show substantially overlapping confidence intervals (DiSTAR SMOS 3.31±0.25 vs. E2TTS 3.29±0.19), making statistical significance unclear.

### Minor

1. **No error bars or confidence intervals on objective metrics (Table 1).** Several comparisons are close (e.g., DiSTAR-medium WER 1.66 vs. F5TTS 2.02). Without error bars, it is unclear whether the reported gaps reflect genuine model quality or evaluation noise.

2. **"Without forced alignment or a duration predictor" is not a unique advantage.** Several compared baselines (E2TTS, F5TTS) also operate without duration predictors in the continuous domain. This framing advantage applies primarily to the discrete-AR family, not the continuous baselines DiSTAR claims to surpass.

### Trivial

- The paper reports DiSTAR-medium beating "Human" on WER (1.66 vs. 1.80 on LibriSpeech; 1.32 vs. 1.47 on SeedTTS) without commentary. ASR-based WER and human transcription error rates are different measurements and should not be directly compared without discussion.

## Nice-to-Haves

- Match NFEs between DiSTAR and DiTAR (evaluate both at NFE=10 and NFE=24) to support the inference-cost claim.
- Add architectural ablations: AR-only without masked diffusion, masked-diffusion-only without AR, and a continuous-latent variant.
- Clarify the provenance of every baseline number and whether subjective tests were conducted by the authors.
- Report error bars or confidence intervals for objective metrics.
- Provide subjective evaluation details (number of raters, reference audio for CMOS, randomization procedure).

## Removed Points

*These points are flagged to be removed, treat them with caution*

1. **"Continuous latents 'introduce practical fragilities' is asserted without evidence"** — This appears in the introduction as motivation/framing, not as a claim tested in the experiments. Standard for an introduction section. Removed as strawman.

2. **"Why 1/t weight in Equation (2)? Derivation not provided"** — The paper cites LLaDA for the derivation; deferring technical derivations to citations is standard practice. Removed as a minor presentation nitpick.

3. **"Tail-first bias explanation is speculative"** — The paper writes "a likely reason is that…" which is appropriately hedged. Removed.

4. **"Hybrid sampling 50/50 threshold is unanalyzed"** — The paper states "the greedy/sample schedule is a hyperparameter; we adopt a simple half-half scheme to avoid over-tuning." This is a conscious design choice, not a weakness. Removed.

5. **"Beating Human WER should be discussed more"** — Common in TTS papers; ASR WER and human transcription error rates are different measurements and this is a minor presentational point at most. Removed.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no observation about the method or results that the paper itself does not already state.

## Suggestions

1. **Clarify baseline provenance and calibrate claims.** State explicitly which numbers in Tables 1 and 2 were computed by the authors (and under what conditions) versus taken from prior publications. Acknowledge uncontrolled comparisons. Calibrate the SOTA claim to what the data support: state-of-the-art in WER/robustness, competitive in speaker similarity and naturalness.

2. **Add architectural ablations.** The paper's central contribution is the AR + masked diffusion coupling; this should be isolated by ablating each module. A continuous-latent variant (e.g., replacing the discrete diffusion with a continuous one while keeping the same AR sketch) would directly test the paper's discrete-over-continuous thesis.

3. **Match NFEs when comparing against DiTAR.** Evaluate DiSTAR at NFE=10 and DiTAR at NFE=24, or report full quality-cost Pareto curves.

4. **Report variability.** Add error bars or confidence intervals to Table 1 and clarify the subjective evaluation protocol (raters, reference, randomization).

## Score and Decision

Round 1 bracket: 4.0 – 5.5 (between VALL-E 2 at 5.00/rejected and MaskGCT at 5.25/accepted; below DiTTo-TTS at 6.25/accepted; above Simple-TTS at 3.00/rejected and Fox-TTS at 3.00/rejected).

**Final calibrated score:** 4.5. The method has genuine architectural merit and competitive WER results, but the experimental validation in its current form — uncontrolled baseline comparisons, unaddressed NFE mismatch, missing architectural ablations, and overclaimed results — falls short of the ICLR acceptance bar. These issues are fixable with a major revision.

**Decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>