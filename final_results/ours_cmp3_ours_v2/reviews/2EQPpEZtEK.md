Now let me write the final consolidated review.

**Calibration Round 1 Bracket:** After reviewing anchors — Simple-TTS (3.00), Fox-TTS (3.00), VALL-E 2 (5.00), Codec-LM Co-design (5.00), MaskGCT (5.25), DiTTo-TTS (6.25) — the narrowest plausible range for DiSTAR is **4.5–6.5**. DiSTAR has stronger architectural novelty than any of these anchors, but its evaluation rigor is weaker than DiTTo-TTS and MaskGCT due to overclaiming, missing subjective baselines, and unsupported efficiency claims.

---

## Summary

DiSTAR proposes a zero-shot TTS framework that operates entirely in discrete RVQ code space, coupling an autoregressive language model (AR) across patches with a masked diffusion Transformer within patches. This avoids continuous latent bottlenecks, duration predictors, and forced alignment. The core idea — handling RVQ's joint time-depth structure by decomposing it into AR cross-patch modeling and masked-diffusion intra-patch infilling — is architecturally novel and well-motivated. On standard benchmarks, DiSTAR achieves state-of-the-art Word Error Rate (1.66% on LibriSpeech-PC, 1.32% on SeedTTS test-en).

## Strengths

1. **Novel architectural coupling in discrete RVQ space (Sec 3.1–3.3).** The paper's core contribution — combining an AR language model with a masked diffusion Transformer entirely within discrete RVQ code space, without a continuous latent bottleneck — is well-motivated and genuinely novel. Prior work either operates on continuous latents (DiTAR, F5TTS) or uses single-codebook discrete tokens (VALL-E). The paper correctly identifies the joint time-depth structure of RVQ as a modeling challenge and proposes a natural decomposition: AR across patches, masked diffusion within patches.

2. **Strong WER results (Table 1).** DiSTAR-medium achieves the lowest Word Error Rate on both benchmarks (1.66% on LibriSpeech-PC, 1.32% on SeedTTS test-en), substantially ahead of competing systems. This is the paper's strongest empirical claim and is well-supported by the evidence.

3. **Well-motivated engineering contributions (Sec 3.2, 3.4).** The overlapping patch aggregation (stride < patch size), stochastic layer truncation for variable-bitrate inference without retraining, and embedding transplantation from the codec's codebook are sensible practical design choices that demonstrably contribute to performance.

## Weaknesses

### Major

1. **Overbroad state-of-the-art claims.** The abstract states DiSTAR "surpasses state-of-the-art zero-shot TTS systems in robustness, naturalness, and speaker/style consistency" and the conclusion claims "SOTA robustness, speaker similarity, and naturalness." However, Table 1 shows DiSTAR is only state-of-the-art on WER (robustness). On speaker similarity (SIM), E2TTS outperforms DiSTAR on both LibriSpeech (0.70 vs 0.67) and SeedTTS (0.71 vs 0.66). On the automatic quality metric (UTMOS), IndexTTS (4.35) and DiTAR (4.15) outperform DiSTAR (4.27 and 4.05 respectively). The paper's attempt to soften this in Section 4.2 ("DiSTAR yields SIM on par with the best alternatives") is inaccurate — a 0.03–0.05 gap in speaker similarity is meaningful. The claims in the abstract and conclusion outrun the evidence, and this requires revision.

2. **Missing baselines in subjective evaluation.** Table 2 compares DiSTAR against FireRedTTS, CosyVoice 2, E2TTS, and F5TTS, but excludes DiTAR (the paper's main architectural predecessor and closest system) and IndexTTS (the strongest competitor on UTMOS and competitive on SIM). DiTAR shares the same patch-wise paradigm, and without it in subjective tests, the paper cannot substantiate claims of perceptual superiority over the most directly related prior work.

3. **Unsupported efficiency claims.** The paper claims "inference cost close to its continuous counterpart DiTAR" (Section 1) and "comparable or lower computational cost" (contributions list), but provides no FLOPs, latency, or throughput measurements. DiSTAR uses NFE=24 vs DiTAR's NFE=10 — 2.4× more diffusion steps per patch — and parameter count alone (0.3B vs 0.6B) does not determine inference cost when NFE is the dominant factor. Without runtime numbers, these efficiency claims are unsubstantiated.

### Minor

4. **DiTAR scores are not reproduced under controlled conditions.** DiTAR results in Table 1 are marked with a ♦ ("scores reported in DiTAR paper"), meaning they were obtained with different training data, codec, and evaluation pipelines. Without a controlled reproduction under the same training setup (Emilia dataset, same codec), the head-to-head comparison is weakened and open to confounds.

5. **Tail-first bias requires multiple heuristic corrections without proper ablation.** Section 3.4 describes a structural bias where "tokens near the end of each patch often receive higher confidence early in decoding," requiring three ad-hoc decoding heuristics (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling) with multiple hyperparameters (T_layer=0.8, T_time=0.95, half-half sampling schedule). Table 3 varies two factors simultaneously (T_time and T_layer, plus sample vs. greedy), making it impossible to isolate each heuristic's marginal contribution. Furthermore, the "Greedy" row still uses T_time=0.95 and T_layer=0.8, so the paper's claim of "robust quality under purely greedy settings" (Section 1) is not evaluated without these shaping heuristics.

### Trivial

None.

## Nice-to-Haves

- Include a controlled comparison against DiTAR at matched NFE (e.g., run DiSTAR at NFE=10) to separate the effect of discrete representation from additional compute.
- Add a diversity metric (e.g., word-level diversity, pitch variation across repeated samples) to substantiate diversity claims.
- Provide individual ablations for each decoding heuristic (T_layer, T_time, hybrid sampling separately) in the ablation study.
- Include inference speed/latency numbers (e.g., real-time factor or seconds per utterance) to support efficiency claims.

## Removed Points

- *Criticism that "WER improvements could equally be attributed to better training data, model capacity, or evaluation protocol"* — This is speculative without evidence that such confounds exist. The paper trains on a controlled dataset and compares against published results; this does not constitute a concrete weakness.
- *Criticism about Equation (1) factorization not explicitly capturing RVQ depth* — The paper's decomposition is clear: AR handles cross-patch and masked diffusion handles intra-patch (including depth). Not a weakness.
- *Criticism about WER surpassing resynthesis raising questions about metric validity* — Speculative. WER surpassing resynthesis can reflect genuine denoising or codec limitations rather than metric artifact.
- *Formatting/style nitpicks and missing appendix content* — Parser artifacts, not author errors.

## Novel Insights

The most penetrating observation from the reviews is that the paper's core technical achievement — state-of-the-art WER from a fully discrete RVQ-space model — coexists with clearly second-place results on speaker similarity and naturalness metrics. This pattern suggests a genuine architectural trade-off: operating entirely in RVQ code space may confer advantages for content preservation (low WER) while inherently limiting acoustic detail reconstruction compared to continuous-latent approaches, as evidenced by the resynthesis upper bound on SIM (0.66 vs E2TTS's 0.70). The decoding heuristics (tail-first bias corrections) further suggest the masked diffusion formulation in RVQ space has structural peculiarities that the paper treats as engineering tweaks rather than analyzing as intrinsic properties of the representation. A deeper analysis of why discrete RVQ space helps WER but hurts SIM would be more valuable than the current framing of "SOTA across all dimensions."

## Suggestions

1. Revise the abstract, contributions list, and conclusion to match what the evidence actually supports: state-of-the-art robustness (WER) with competitive but not SOTA speaker similarity and naturalness.
2. Add subjective evaluation against DiTAR or provide a strong justification for its omission.
3. Provide runtime measurements (latency, real-time factor) to substantiate or correct efficiency claims.
4. Run DiSTAR at NFE=10 and compare directly with DiTAR at NFE=10 for a controlled quality comparison.
5. Expand the ablation study (Table 3) to isolate the effect of each decoding heuristic individually.

## Score and Decision

The paper presents a genuinely novel architecture and achieves state-of-the-art WER results. However, the systematic overclaiming, missing key baselines in subjective evaluation, unsupported efficiency claims, and NFE mismatch with the closest competitor prevent the paper from meeting the acceptance bar in its current form. The core contribution is real and a revised version with honest claims and proper comparisons would be a strong paper.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>