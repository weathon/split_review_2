Now let me produce the final review.

## Summary

DeCodec proposes a neural audio codec architecture that learns disentangled representations of speech and background sound via a subspace orthogonal projection (SOP) module and a representation swap training (RST) procedure. The model further decomposes speech into semantic and paralinguistic components using semantic guidance (SG) with HuBERT. The paper demonstrates the utility of this disentangled representation on reconstruction, speech enhancement, voice conversion, ASR, and TTS tasks.

## Strengths

1. **The RST procedure is a genuinely clever and well-motivated idea (Section 3.6).** Swapping predicted speech and background-sound representations from different mixtures and training the decoder to reconstruct the swapped combination (s₁+n₂) is an elegant unsupervised method to enforce that each pathway carries only its designated information. This is the paper's most distinctive contribution and is not present in prior codec-based disentanglement works.

2. **DNSMOS results on speech enhancement are competitive with dedicated SE models (Table 2).** DeCodec achieves OVL=3.39/SIG=3.64/BAK=4.13 on the without-reverb set and BAK=3.99 on real recordings, matching or exceeding task-specific models like SELM and StoRM despite being primarily a codec. This is a non-obvious and practically valuable result that validates the speech pathway's decoupling.

3. **The breadth of downstream validation is impressive.** Showing that a single codec can support reconstruction, SE, VC, ASR, and TTS — even if some results are modest — demonstrates the value of the disentanglement approach and lends credence to the "universal front-end" framing.

## Weaknesses

### Fatal

None.

### Major

1. **The evidence for background-sound decoupling is weak relative to the paper's central claim (Table 4).** The paper claims "explicit decoupling representation of speech and background sound" (abstract, line 39), but the ablation study reports SDR-B (reconstruction quality of the background-sound pathway) of only 0.49 dB for Ablation-3 (SOP+RST), -1.11 dB for DeCodec-c (full causal), and -0.36 dB for DeCodec (full non-causal). An SDR-B near or below 0 dB means the reconstructed background sound is barely distinguishable from the original mixture; a negative value means it is *worse* than using the mixture directly as the estimate. While the relative improvement over ablation baselines (-13.15 and -10.67 dB) is noteworthy, the absolute values do not support the central claim of "explicit decoupling." The speech pathway is well-validated (strong DNSMOS results, SDR-S of 6.73–7.90 dB), but the background-sound pathway lacks equivalent evidence. Furthermore, no standard source separation metrics (SI-SDRi, PESQ, STOI) are reported, making it difficult to contextualize these numbers against the broader literature.

2. **Reconstruction comparison is not bitrate-controlled, inflating DeCodec's apparent advantage (Table 1).** DeCodec uses 8.0 kbps (4.0+4.0) while EnCodec uses 6.0 kbps, DAC uses 4.5 kbps, HiFi-Codec uses 2.0 kbps, and SpeechTokenizer uses 4.0 kbps. Higher bitrate predictably yields better SDR, so the claim that DeCodec "achieves the highest SDR" (7.61 vs EnCodec's 6.86) is not informative without matched-bitrate comparisons. The Mel distance metric further undercuts the claim: on clean speech, DeCodec (0.89) is worse than both DAC (0.65) and SpeechTokenizer (0.76). To make a fair comparison, the authors should either train baselines at comparable bitrates or train a version of DeCodec at a matched total bitrate (e.g., 4.0+2.0 = 6.0 kbps to match EnCodec).

3. **The theoretical "proof" in Section 3.6 is not mathematically sound.** The derivation attempts to use the mean value theorem for vector-valued functions ℝⁿ→ℝᵐ in a simple form that does not hold generally — the standard MVT extends only via an inequality for vector-valued codomains, not the equality form used in Equation (16). The paper cites "Russell, 2020" but the cited reference would confirm the inequality form, not the equality used. Moreover, the leap from "the left side depends on Zs₁ through ξ" to "Zs₁ must be independent of n₁" is logically unsupported. Even if the left side depends on Zs₁, this only means the Jacobian evaluated at ξ (which involves Zs₁) times the difference (Zn₂−Zn₁) approximates (n₂−n₁) — this does not force Zs₁ to be independent of n₁. The presentation of this section as a "theoretical proof" overstates what has been established; it should be reframed as heuristic motivation.

### Minor

1. **VC results show limited practical intelligibility (Table 3).** The WER of 50.46% for one-shot VC means roughly every other word is incorrect. While the paper acknowledges this ("As for the relatively high WER..."), the abstract's claim of "effective one-shot voice conversion on noisy speech" is overstated given that the improvement over the StoRM-SpeechTokenizer baseline (52.73% → 50.46%) is modest and the absolute error rate remains very high.

2. **Architecture ambiguity in Figure 2 caption.** The caption states "the input y is split into two encoders (Enc) to produce Yl and Yr," while the main text consistently describes a single encoder (Section 3.2: "an encoder"; Section 3.3 describes a single encoder architecture; Section 3.4: "two trainable linear projection layers *followed* the encoder"). The text is clear, but the caption contradicts it and should be corrected to avoid confusion about whether the model uses one shared encoder or two independent encoders — which matters for parameter count comparisons.

### Trivial

None.

## Nice-to-Haves

- Report parameter counts and FLOPs for DeCodec versus baselines to contextualize model complexity, especially since the parallel RVQ architecture uses two codebooks.
- Train a version of DeCodec at a matched total bitrate (e.g., 4.0+2.0 = 6.0 kbps) for fair reconstruction comparison with EnCodec.
- Report standard source separation metrics (SI-SDRi, PESQ, STOI) to enable cross-literature comparison with the source separation community.

## Removed Points

- "Angular matrix" not defined as standard term: trivial notation issue, not a substantive weakness.
- BAK score advantage might be caused by blanking operation: speculative, not verifiable from the paper as written.
- "Universal" framing is overstated (paper handles only speech+BGS): scope creep — paper clearly scopes to speech and background sound.
- Notation nitpick about L⊥ = ‖⟨S,N⟩ − 0‖₂: trivial formatting preference.
- Any criticism about missing related work: cannot be externally verified.
- Any formatting/typo/grammar issue: parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Conduct a controlled bitrate comparison (e.g., matching DeCodec's total bitrate to EnCodec's 6.0 kbps) to establish whether the SDR advantage holds under equal bit budgets.
2. Report standard source separation metrics (SI-SDRi, PESQ) for the BGS pathway, or present spectrogram visualizations of separated components, to substantiate the decoupling claim.
3. Reframe Section 3.6's theoretical derivation as a plausibility argument or heuristic motivation, removing the claim of proof.
4. Acknowledge the absolute SDR-B values more honestly — the current framing emphasizes relative improvement without disclosing how weak the absolute numbers are.
5. Tone down the "explicit decoupling" claim to match what the evidence supports: the speech pathway is well-decoupled from BGS (as shown by DNSMOS), but symmetric two-way decoupling is not convincingly demonstrated.

## Score and Decision

**Calibration anchors (all from the deepreview_13k_calibration corpus):**

| Anchor | Avg | Decision | Comparison to DeCodec |
|--------|-----|----------|----------------------|
| DM-Codec (UFwefiypla) | 3.00 | Reject | Similar topic (codec tokenization). DM-Codec was criticized for incremental contribution and fundamental alignment flaw. DeCodec has stronger novelty (RST) but a significant claim-evidence gap. |
| Universal Semantic Disentangled (Id2JMVSQHZ) | 4.80 | Reject | Codec-based disentanglement for privacy. Criticized for missing baselines and unclear advantages. DeCodec has comparable novelty but broader downstream validation. |
| Codec-LM Co-design (KCVv3tICvp) | 5.00 | Reject | Practical co-design strategies. Criticized for incremental techniques. DeCodec has stronger novelty but more central methodological flaws. |
| Separate and Diffuse (UXALv0lJZS) | 6.00 | Accept | Speech separation. Clean execution, strong baselines. DeCodec has broader scope but weaker evidence for core claims. |
| FlowDec (uxDFlPGRLX) | 7.00 | Accept | General audio codec. Clean execution, good evaluation. DeCodec has more novel ideas but less clean evidence. |

**Round-1 bracket:** 4.0–5.5 (lower borderline reject to upper borderline reject)

**Final score:** 4.5 — The paper introduces a genuinely novel idea (RST procedure) and demonstrates competitive speech enhancement results, which are real contributions. However, the central claim of "explicit decoupling representation of speech and background sound" is not well-supported by the evidence: SDR-B values near 0 dB indicate the background-sound pathway is not capturing meaningful BGS information. The reconstruction comparison at unequal bitrates is misleading, and the attempted theoretical proof is mathematically unsound. The paper's contribution is narrower than claimed — it primarily demonstrates noise-robust speech representation rather than symmetric two-way decoupling. With major revisions (matched bitrate comparison, honest characterization of decoupling, removal of the flawed proof), the paper could become acceptable, but in its current form the claims outpace the evidence.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>