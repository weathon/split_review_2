Now let me compose the final consolidated review.

## Summary

DeCodec proposes a neural audio codec that learns hierarchically disentangled representations: first separating speech from background sound via a Subspace Orthogonal Projection (SOP) module and a Representation Swap Training (RST) procedure, then further decomposing speech into semantic and paralinguistic components via semantic guidance (SG). The paper demonstrates the single model on reconstruction, speech enhancement, voice conversion, ASR, and TTS — an ambitious unification attempt.

## Strengths

- **Well-motivated problem (Section 1).** The paper correctly identifies that existing neural codecs either entangle all audio types (EnCodec, DAC, UniCodec) or only work on clean speech (SpeechTokenizer, FACodec). Real-world audio is mixed, and downstream tasks need selective access to speech vs. background sound — this framing is compelling and clearly distinguishes the paper from prior work. *(Impact: +9.5)*

- **Technically novel SOP+RST combination (Sections 3.4, 3.6).** The SOP module factorizes the encoder embedding into two orthogonal subspaces via learned linear projections with an orthogonality constraint; the RST procedure then uses a swap-training objective to force those subspaces to correspond to speech and background sound respectively. This two-part design is clean, intuitive, and a genuine architectural contribution. *(Impact: +9.9)*

- **Competitive DNSMOS on speech enhancement (Table 2).** DeCodec achieves the best or tied-best DNSMOS OVL, SIG, and BAK scores in most conditions (including real recordings) compared to dedicated SE models like InterSubNet, StoRM, and SELM — achieved without a separate SE model. *(Impact: +7.0)*

- **Demonstrates a single codec serving multiple tasks** — reconstruction, SE, VC, ASR, and TTS feature extraction — which is an ambitious unification that is noteworthy even if individual results are uneven. *(Impact: +8.4)*

## Weaknesses

### Major

- **Unequal bitrate comparison invalidates the reconstruction claim (Table 1).** DeCodec operates at 8.0 kbps total (4.0+4.0) while every baseline uses a lower total bitrate: EnCodec 6.0, HiFi-Codec 2.0, DAC 4.5, SpeechTokenizer 4.0. The claimed SDR advantage (e.g., 7.61 vs. 6.86 for EnCodec on clean speech) could easily be explained by the extra 2+ kbps of bitrate budget rather than any architectural advantage from disentanglement. On clean speech, the background-sound branch encodes silence at 4.0 kbps — a 100% waste of bitrate that no baseline is permitted. The paper includes no matched-bitrate comparisons and no discussion of this confound. *(Impact: -8.4)*

- **Speech enhancement evaluation relies solely on DNSMOS, omitting standard objective metrics (Section 4.2.2).** The paper reports only DNSMOS (a non-intrusive quality predictor) for SE. Standard evaluations on the DNS Challenge test set include PESQ, STOI, and SI-SNR — objective measures of signal distortion and intelligibility. Their absence is a significant gap because: (a) DNSMOS can be biased toward over-suppression that sounds "clean" but distorts the speech signal; (b) DeCodec is a quantized codec while baselines are continuous SE models — codec compression artifacts could inflate DNSMOS while actually degrading speech quality; (c) without SI-SNR or PESQ the reader cannot assess whether the "enhanced" speech retains the original signal with fidelity. *(Impact: -7.0)*

- **The theoretical justification for RST (Equations 13–16, Section 3.6) is presented as a formal proof but is not rigorous.** The argument invokes the mean value theorem for vector-valued functions in equality form (Equation 16), but the standard MVT for vector functions provides a mean value inequality, not an equality. Additionally, the inference that because "the left side depends on Zs₁ through ξ, while the right side is independent of Zs₁" therefore "Zs₁ must be independent of n₁" does not hold for a nonlinear neural network decoder — the dependence through ξ could be resolved by the network learning a compensating dependence. The approximations in Equations (13) and (14) are optimization targets, not guarantees, so the subtraction in (15) does not carry rigorous force. This should be presented as a motivating intuition, not a theoretical guarantee. *(Impact: -8.7)*

- **The SG module's reconstruction cost is understated (Table 4, Ablation study).** Adding SG to SOP+RST reduces SDR-O from 6.68 (Ablation-3) to 4.62 (DeCodec-c) — a 31% relative reduction. The paper describes this as "a slight decrease in SDR," which is misleading. A 2.06 dB drop is substantial and indicates that forcing the first RVQ layer to match HuBERT features significantly interferes with reconstruction quality. The paper never addresses whether this tradeoff is acceptable or whether the SG loss could be tuned less aggressively. *(Impact: -6.3)*

- **One-shot VC results do not support the claimed capability (Table 3, Abstract).** The abstract claims "effective one-shot voice conversion," but the converted speech achieves a WER of 50.46% — meaning approximately half the words are wrong and the speech is largely unintelligible. The baseline SpeechTokenizer (74.18% WER) and StoRM-SpeechTokenizer (52.73% WER) also fail, and DeCodec's marginal improvement does not constitute a working VC system. Claiming "effective" capability based on this result is an overstatement. *(Impact: -8.6)*

### Minor

- **The term "angular matrix" in Section 3.4 is introduced without definition.** The paper states that when YY^T satisfies the "angular matrix" then P_S P_N^T = 0, but never defines what an "angular matrix" is. This makes the derivation from Equation (6) to the claimed orthogonality of the projection matrices unclear. *(Impact: -0.9)*

- **The ablation study (Table 4) reports SDR-B and SDR-S but does not explain how the reference signals for these metrics are obtained.** Since the noisy test set is mixed from clean speech and noise, the references would be the original clean sources, but this is not stated, leaving ambiguity about the evaluation protocol. *(Impact: -0.8)*

- **The SE baseline comparisons (Table 2) use results taken from published papers** rather than running all models in a unified evaluation pipeline. This introduces uncontrolled variables in inference configuration and test conditions. *(Impact: -3.0)*

### Trivial

None.

## Nice-to-Haves

- Run DeCodec at a matched total bitrate (e.g., 2.0+2.0 = 4.0 kbps) to fairly compare reconstruction with SpeechTokenizer and other baselines.
- Add PESQ, STOI, and SI-SNR to the speech enhancement evaluation.
- Reformulate the RST justification as a motivating intuition or provide a rigorous analysis (e.g., showing the RST loss upper-bounds mutual information between Zs and the noise component).
- Address the SG-reconstruction tradeoff explicitly — run an ablation with reduced SG loss weight and report the Pareto frontier.
- On clean speech, the BRVQ branch encodes silence at a full 4.0 kbps — a mechanism to detect/skip encoding of absent components would improve efficiency.

## Removed Points

- **Causal vs. non-causal claim**: The critic noted causal DeCodec (6.79 SDR) is slightly worse than causal EnCodec (6.86 SDR). The paper's claim of "comparable" performance is reasonable given the 0.07 dB difference. Removed — not a meaningful weakness.
- **Mel distance / DAC comparison**: The paper explicitly acknowledges DAC is better on Mel distance ("second only to DAC"). Removed — the paper does not overlook this.
- **Missing perceptual metrics (VISQOL, POLQA)**: Requesting additional metrics beyond what the paper already reports (SDR, Mel distance, WER) is scope creep; these are standard codec evaluation metrics. Removed.
- **"Paralinguistic" used loosely**: The VC experiment directly tests whether SRVQ-2:8 encodes speaker characteristics (via SIM), and the ASR experiment tests semantic preservation. The concern is overstated. Removed.
- **BRVQ efficiency**: Moved to Nice-to-Haves.
- **Formatting/typo/grammar nitpicks**: All parser artifacts. Removed per instructions.
- **Reproducibility nitpicks**: Removed per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run matched-bitrate comparisons.** This is the single most important experiment: evaluate DeCodec at a total bitrate of ~4.0 kbps (e.g., 2.0+2.0) against SpeechTokenizer (4.0 kbps) and EnCodec (6.0 kbps) to separate the benefit of disentanglement from the benefit of extra bitrate.
2. **Add PESQ, STOI, and SI-SNR** to the speech enhancement evaluation to address the DNSMOS-only gap.
3. **Reformulate the RST justification** as a motivating intuition rather than a formal proof.
4. **Address the SG-reconstruction tradeoff explicitly** — the 31% SDR drop needs justification or mitigation.
5. **Provide qualitative examples** (spectrograms/audio) for the voice conversion experiment.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>