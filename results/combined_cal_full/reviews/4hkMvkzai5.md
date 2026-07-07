## Summary

This paper proposes DeCodec, a neural audio codec that learns to decouple audio representations into orthogonal subspaces for speech and background sound through a subspace orthogonal projection (SOP) module and a representation swap training (RST) procedure. Within the speech subspace, semantic guidance (SG) further decomposes representations into semantic and paralinguistic components. The goal is to serve as a universal front-end for multiple audio tasks (reconstruction, SE, VC, ASR, TTS).

## Strengths

- **Well-motivated problem (Section 1, Figure 1).** The paper correctly identifies that real-world audio mixes speech and background, that different tasks require selective access to these components, and that existing codecs either entangle everything (EnCodec, DAC) or handle only clean speech (SpeechTokenizer). The limitations of cascaded separation pipelines (error propagation, signal distortion, computational cost) are stated concretely.

- **Ablation study cleanly validates the SOP+RST combination (Table 4).** This is the strongest empirical result. Ablation-1 (SOP only): SDR-B = -13.15 dB — effectively no background reconstruction. Ablation-2 (RST only): SDR-B = -10.67 dB — also failure. Ablation-3 (SOP+RST): SDR-B jumps to **+0.49 dB** and SDR-S to **+7.90 dB**. This non-linear interaction where two individually ineffective components become effective together provides convincing evidence that the joint design is doing something real.

- **The SOP+RST mechanism is technically interesting.** The idea of using orthogonal projection layers followed by a swap-training procedure to enforce subspace specialization, applied within a codec framework (rather than as a separate separation module), is a sensible and novel architectural choice.

## Weaknesses

### Major

- **Bitrate confound in reconstruction comparison (Table 1).** DeCodec operates at **8.0 kbps total** (4.0 kbps for SRVQ + 4.0 kbps for BRVQ), while baselines use substantially lower bitrates: EnCodec at 6.0 kbps, HiFi-Codec at 2.0 kbps, DAC at 4.5 kbps, SpeechTokenizer at 4.0 kbps. Higher bitrate directly improves SDR for reconstruction, but the paper never acknowledges this confound and claims DeCodec "achieves the highest SDR for speech reconstruction" without noting the asymmetric rate budget. A proper comparison would match bitrates — either by reducing DeCodec's rate (e.g., fewer RVQ layers) or retraining baselines at matching rates. This does not invalidate the decoupling claim (which is supported by the internally-controlled ablation), but it makes the SDR ranking in Table 1 uninformative.

### Minor

- **Voice conversion results are weak and overclaimed (Section 4.2.3, Table 3).** A WER of 50.46% means roughly half the words are incorrect — the converted speech is largely unintelligible. The improvement over StoRM-SpeechTokenizer (52.73%) is only 2.3 percentage points, and speaker similarity is identical (0.83). The abstract's claim of "effective one-shot voice conversion on noisy speech" overstates these results.

- **No direct source separation baseline for the core decoupling claim.** The paper criticizes cascaded pipelines for "error propagation" and "signal distortion" (Section 1) but does not compare against a dedicated speech separation method (e.g., Conv-TasNet, DPRNN-TasNet) for separation quality. The StoRM-SpeechTokenizer comparison in the VC experiment partially addresses this, but a direct comparison with intrusive separation metrics (SI-SNR, SDR for separated components) is absent.

- **The theoretical proof in Section 3.6 (Eq. 13–16) is not rigorous.** The paper claims to "theoretically prove" that L_RST forces Zs to be speech-only representations. The MVT argument concludes Zs must be independent of n₁ because "the left side depends on Zs₁ through ξ, while the right side is independent of Zs₁." This reasoning assumes the decoder Jacobian w.r.t. Zn does not depend on Zs in a way that would break the argument — an assumption not justified for a standard nonlinear convolutional decoder. The argument is heuristic, not a valid proof, and should be reframed as such.

- **Overclaimed "first time" and unclear terminology (Section 1, Section 3.4).** The claim of achieving explicit decoupling "for the first time" depends on a narrow definition of "feature domain" that is not defended. Additionally, the phrase "When the covariance matrix YY^T satisfies the angular matrix" (Section 3.4) is never defined and makes the derivation of P_S and P_N being orthogonal projection matrices unverifiable.

### Trivial

None.

## Nice-to-Haves

- Report the ASR and TTS results (currently in appendices) in the main paper, since they support the "universal front-end" claim.
- Add waveform or spectrogram visualizations showing the effect of manipulating individual subspaces to give qualitative intuition for what "decoupled" means perceptually.

## Removed Points

These points are flagged to be removed; treat them with caution:
1. **Missing appendices (ASR in Appendix F, TTS in Appendix G):** Removed per policy — the parser strips appendices from all papers; they exist in the original submission.
2. **SE evaluation asymmetry (replacing BGS with blank audio):** Removed — the trained scoring model assigns this item near-zero weight (+0.22), indicating it is not a genuine weakness. DeCodec presents a novel SE approach using its disentangled representations, and DNSMOS is a standard evaluation metric; comparing against SE baselines is a valid demonstration.
3. **Statistical significance / confidence intervals:** Removed — single-run evaluation is standard for codec/SE benchmarks.
4. **Training SNR range (-5 to 40 dB) concern:** Removed — the paper evaluates at -5 to 20 dB, a valid test distribution.
5. **Mel Distance framing criticism:** Removed — the paper accurately states DAC is best on Mel distance and DeCodec is "second only to DAC."
6. **"Blank audio" SE procedure underspecified:** Removed — the procedure is described in Section 4.2.2; it refers to the BGS representation of a silent clip.
7. **No audio samples / qualitative analysis:** Removed as a nice-to-have that does not affect core evaluation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Match bitrates** in the reconstruction comparison: either configure DeCodec at a lower bitrate (e.g., 2.0+2.0 = 4.0 kbps) or retrain baselines at 8.0 kbps to make Table 1's SDR comparison meaningful.
2. **Add a direct speech separation baseline** (e.g., Conv-TasNet, DPRNN-TasNet) evaluated on SDR-B and SDR-S to substantiate the claim that DeCodec's approach is superior to cascaded pipelines.
3. **Reframe the theoretical argument** in Section 3.6 as heuristic motivation rather than a formal proof, and explicitly state the required assumptions about decoder structure.
4. **Tone down the VC claims:** the 50% WER is too high to call "effective one-shot voice conversion"; add failure analysis and discuss limitations.
5. **Improve the reconstruction comparison** by acknowledging the bitrate difference and contextualizing the SDR results accordingly.

## Score and Decision

**Calibration anchor comparison:**
- `UFwefiypla.md` (DM-Codec, avg 3.00): Very similar domain (speech codec tokenization). Had severe technical flaws (-10.72, -7.42) about alignment and fundamental methodology. This paper's weaknesses are less severe — no comparable technical flaw exists. **My paper is above this anchor.**
- `Id2JMVSQHZ.md` (USC, avg 4.80): Disentangled speech codec for privacy. Had severe novelty concerns (-9.20, -8.98) about being similar to prior work. This paper's SOP+RST approach is genuinely novel; its negatives are milder. **My paper is above this anchor.**
- `KCVv3tICvp.md` (Codec-LM Co-design, avg 5.00): Codec-LM interaction, different focus. Comparable score range. **My paper sits near this anchor.**
- `uxDFlPGRLX.md` (FlowDec, avg 7.00): Full-band audio codec with strong experimental rigor (retrained baselines, comprehensive evaluation). This paper has more and stronger negatives. **My paper is below this anchor.**
- `1p6xFLBU4J.md` (GenSE, avg 6.00): Generative SE via language models. Had -9.16 and -9.55 novelty concerns but was balanced by strong experiments. **My paper sits below this anchor due to weaker experimental control.**

The paper has a genuinely novel core idea (SOP+RST) with a convincing ablation study, but the experimental evaluation has significant gaps: the bitrate confound makes the reconstruction comparison unfair, the VC results are too weak to support the claimed effectiveness, and the theoretical proof is not rigorous. These issues are addressable but prevent the paper from reaching the clear accept threshold. **Score: 5.5.**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>