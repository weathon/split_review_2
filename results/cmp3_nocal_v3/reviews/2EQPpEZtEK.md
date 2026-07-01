## Summary

DiSTAR proposes a zero-shot TTS framework that operates entirely in the discrete RVQ code space, coupling an autoregressive language model (drafts block-level tokens) with a masked diffusion model (fills in each patch in parallel). The paper also introduces stochastic layer truncation for variable-bitrate inference without retraining and identifies a "tail-first bias" with lightweight decoding correctives. On two benchmarks (LibriSpeech-PC and Seed-TTS test-en), DiSTAR-medium achieves the lowest WER among all compared systems.

## Strengths

1. **Well-motivated discrete-domain design.** The paper correctly identifies a tension in RVQ-based TTS: existing approaches either flatten the depth axis (sacrificing structure), use delay patterns (limiting parallelism), or operate in the continuous domain (introducing domain sensitivity). Keeping everything in the discrete RVQ space while coupling AR drafting with masked diffusion addresses this tension directly. Sections 3.1.1–3.1.2 lay this out clearly.

2. **Stochastic layer truncation for test-time bitrate control.** Randomly dropping top RVQ layers during training so the model learns to operate at varying depth, then pruning layers at inference without retraining (Section 3.4, Figure 2), is clean and practically useful. The empirical pattern—WER saturates around 6 layers while speaker similarity continues to improve—is consistent with the known division of labor across RVQ layers.

3. **Tail-first bias diagnosis and lightweight decoding tricks.** The observation that non-autoregressive training makes later positions within a patch overconfident (Section 3.4), and the three correctives (layer-wise temperature shaping, position-wise temperature shaping, hybrid sampling), show genuine empirical insight. Table 3 shows WER dropping from 2.11 to 1.91 with these adjustments.

4. **Best WER on both benchmarks.** DiSTAR-medium achieves WER 1.66% on LibriSpeech-PC and 1.32% on Seed-TTS test-en—the lowest among all compared systems. This result holds against baselines using equal or higher NFE (e.g., E2TTS at NFE=32, F5TTS at NFE=32), suggesting a genuine robustness advantage.

## Weaknesses

### Fatal

None. The core idea (AR draft + masked diffusion entirely in the discrete RVQ space) is sound, and the WER results are strong against multiple baselines. No single verified flaw invalidates the central contribution.

### Major

1. **The WER comparison with DiTAR is confounded by NFE, and the inference-cost claim is unmeasured.**  
   DiSTAR-medium (NFE=24) is compared against DiTAR (NFE=10, marked ♦ from the original paper, not re-run). For diffusion-based methods, increasing NFE typically improves quality. The paper does not show DiSTAR at NFE=10 or DiTAR at NFE=24. Without a matched-NFE comparison, the WER advantage over DiTAR specifically (1.66 vs 2.39 on LibriSpeech; 1.32 vs 1.78 on Seed-TTS) may partly reflect compute budget rather than architectural superiority.  
   Separately, the abstract and introduction claim DiSTAR "maintain[s] the inference cost close to its continuous counterpart DiTAR," yet the paper provides **zero** wall-clock, FLOPs, or real-time-factor measurements. Section 4.4 is titled "Inference Efficiency and Controllability" but only shows quality-vs-RVQ-layers trade-offs, not actual efficiency numbers. This claim is asserted without evidence.

2. **Subjective evaluation (Table 2) omits the most relevant baseline.**  
   DiTAR—the paper's closest predecessor and direct competitor—is absent from the listening test. IndexTTS is also absent. The subjective results (SMOS/CMOS) therefore cannot tell us whether human listeners prefer DiSTAR over the method it most directly extends and claims to outperform. Given that DiTAR achieves the best UTMOS on Seed-TTS test-en (4.15, Table 1), this omission weakens the subjective evidence substantially.

3. **Ablation study does not ablate the core architectural decisions.**  
   Table 3 only varies decoding strategies (temperature settings, greedy vs. sampling). It does not ablate:
   - The AR drafter: what if the model uses pure autoregressive decoding without the masked diffusion refiner?
   - Discrete vs. continuous diffusion: what if the same pipeline used continuous denoising (the DiTAR setup) while keeping everything else fixed?
   - The overlapping window design or the aggregator architecture.
   
   The paper's central thesis is that discrete-domain AR+masked-diffusion is superior to alternatives. Without isolating these components, the evidence for this claim is incomplete.

### Minor

1. **Speaker similarity (SIM) is below the best alternatives, but the paper claims otherwise.**  
   On LibriSpeech-PC: E2TTS SIM=0.70, DiSTAR-medium SIM=0.67. On Seed-TTS test-en: E2TTS SIM=0.71, DiSTAR-medium SIM=0.66. The paper says DiSTAR "yields SIM on par with the best alternatives" and the conclusion claims "SOTA speaker similarity." Numerically, DiSTAR trails E2TTS on both benchmarks. The SMOS subjective results (Table 2) show DiSTAR and E2TTS within confidence intervals, which supports the "on par" framing for subjective similarity, but the objective SIM overstates the case.

2. **No limitations section.** The paper has no discussion of limitations. Several are worth acknowledging: the reliance on a specific codec with large codebooks (65,536); the heuristic nature of the decoding tricks; the SIM gap relative to continuous-domain systems; and the English-only training.

3. **The relationship between Eq. (1) and the actual training objective is not fully spelled out.**  
   Equation (1) presents a standard code-level AR factorization ($\prod p_\theta(c_i|c_{<i}, X)$), but the model is trained end-to-end with the masked-diffusion loss (Eq. 2), where the AR module produces a conditioning state rather than predicting codes directly. While the paper states "Training minimizes the cross-entropy objective in equation 2" (line 110), it never explains how Eq. (1) relates to Eq. (2) as a variational bound or decomposition. This is a clarity gap, not a technical error, but it makes the method description harder to follow.

4. **Section 4.4 title promises "Inference Efficiency" but delivers only quality-vs-layers trade-offs.** The RVQ layer pruning analysis is informative as a controllability demonstration, but actual efficiency numbers (latency, throughput, FLOPs) are absent.

### Trivial

None.

## Nice-to-Haves

- A matched-NFE comparison with DiTAR (run both at NFE=10 and NFE=24) would directly address the strongest confound in the experimental comparison.
- A pure-AR baseline (removing the masked diffusion module, decoding patch tokens autoregressively) would test whether the diffusion refiner adds value over a strong AR baseline on the same RVQ representation.
- Actual efficiency measurements (FLOPs, wall-clock time, or real-time factor) for DiSTAR vs. DiTAR at matched NFE, to support the inference-cost claim.
- Inclusion of DiTAR and IndexTTS in the subjective listening test.

## Removed Points

These points from the harsh-critic input were filtered out per the meta-reviewer instructions:

- **"Patch size/stride analysis relegated to Appendix D"** — Removed per hard rules: the appendix is stripped by the parser; the paper cannot be penalized for content that exists in the submission but was not accessible.
- **"Statistical significance missing from Table 3"** — Weakened and removed: the WER differences in Table 3 (2.11→1.99→1.91) are material and the pattern is consistent; requesting confidence intervals for single-run decoding ablations is a standard-but-not-universal practice that does not rise to the level of a weakness here.
- **"Codebook size 65,536 not discussed"** — Removed as a speculative concern. The paper describes the codec choice transparently (Section 3.5.1). Whether 65,536 is "unusually large" depends on the design space and the paper does not claim universality.
- **"Human WER of 1.80 seems high"** — Removed as a factual nitpick. The paper provides this as a reference point from the benchmark and typical human WER ranges are within 1.5–2.0%.
- **"Training objective is a mismatch"** — Downgraded from a Critical Issue to Minor (clarity). The paper does describe end-to-end training via Eq. (2) and the AR module's role as conditioning producer. The lack of an explicit connection between Eq. (1) and Eq. (2) is a clarity issue, not a technical mismatch.

## Novel Insights

None beyond the paper's own contributions. The harsh-critic review correctly identifies the empirical structure (best WER, behind on SIM, missing baselines in subjective eval) but does not uncover any novel insight about the method or its failure modes that the paper itself does not discuss.

## Suggestions

1. Add a controlled NFE comparison with DiTAR (run both methods at NFE=10 and NFE=24). This is the single most important piece of missing evidence.
2. Add a pure-AR ablation (replace the masked diffusion refiner with autoregressive decoding of patch tokens) to test whether the diffusion component contributes beyond a strong AR baseline.
3. Report actual efficiency metrics (FLOPs, real-time factor, or wall-clock time) to substantiate the inference-cost claim.
4. Include DiTAR in the subjective evaluation (Table 2).
5. Tone down the SIM framing: acknowledge that DiSTAR trails E2TTS on objective SIM while being competitive on subjective SMOS. Add a limitations paragraph.
6. Clarify the relationship between Eq. (1) and Eq. (2) in the method section—specifically, that Eq. (1) is a conceptual factorization of the overall generative process and that the AR module is trained end-to-end through the diffusion loss to produce conditioning states.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>