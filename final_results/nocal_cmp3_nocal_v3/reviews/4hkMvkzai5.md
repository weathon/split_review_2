Now I have verified the key claims. Let me write the final consolidated review.

## Summary

DeCodec proposes a neural audio codec that explicitly decouples speech from background sound in the representation domain via subspace orthogonal projection (SOP) and a representation swap training (RST) procedure, and further decomposes speech into semantic and residual paralinguistic components through semantic guidance (SG). The model is evaluated on reconstruction, speech enhancement, one-shot voice conversion, and downstream ASR/TTS.

## Strengths

1. **Novel and well-motivated approach.** The paper identifies a genuine gap (Section 1): existing universal codecs (EnCodec, DAC) entangle everything, while speech-specific decoupling codecs (SpeechTokenizer) fail on noisy inputs. The idea of solving decoupling in the representation domain of a single codec rather than via a cascaded pipeline is compelling and the neuroscience analogy (A2 cortical processing) gives a clear conceptual framing.

2. **The ablation study (Table 4) is informative and honestly reported.** Ablation-1 (SOP only) gives SDR-B = -13.15 and SDR-S = -1.91; Ablation-2 (RST only) gives SDR-B = -10.67 and SDR-S = 3.03; Ablation-3 (SOP+RST) jumps to SDR-B = 0.49 and SDR-S = 7.90. This cleanly demonstrates that the two components are genuinely synergistic, which is the strongest evidence for the decoupling mechanism.

3. **Competitive SE results (Table 2).** DeCodec achieves the highest OVL (3.39), SIG (3.64), and BAK (4.13) on the without-reverb set, and the highest OVL (3.13) and BAK (3.99) on real recordings. That a codec at 8 kbps with quantized representations matches or exceeds dedicated SE models (StoRM, SELM, Inter-SubNet) is the paper's most concrete practical result.

4. **The RST procedure is a clever training trick.** Swapping speech and background components between two mixtures and reconstructing the cross product (s₁+n₂) provides a clean inductive bias that directly enforces correct subspace assignment, and this design choice is well-described (Section 3.6, Equations 8–12).

## Weaknesses

### Fatal
None.

### Major

1. **The extracted background sound quality is poor relative to the "background sound extraction" claim.** The full DeCodec achieves SDR-B = -0.36 (non-causal) and -1.11 (causal) in Table 4. A negative SDR means the estimated BGS is worse than silence — the extracted background component cannot be used for any realistic purpose. The paper lists "background sound extraction" as a capability (Abstract, line 42) and claims "explicit decoupling representation of speech and background sound" as a headline contribution (line 39). While the decoupling *does* work for the speech component (SDR-S = 6.73) and for BGS suppression in SE, the BGS *extraction* claim is not supported by the evidence. The paper should either demonstrate that the BGS component preserves usable non-speech information (e.g., via listening tests or spectrograms) or calibrate this claim to what the evidence supports.

2. **The theoretical proof in Section 3.6 (Equations 13–16) is not mathematically valid as presented.** The argument attempts to prove that the RST loss forces Zs to be independent of n₁ by applying the mean value theorem to the difference Dec(Zs₁+Zn₂) − Dec(Zs₁+Zn₁). Two issues: (a) The mean value theorem for vector-valued functions of several variables does not give an exact equality of the form claimed — it yields a mean value inequality, not the equality used in Equation (16). (b) Even if one accepts the form, the Jacobian at ξ is itself a function of Zs₁ (since Dec takes both Zs and Zn as arguments and ξ lies between Zn₁ and Zn₂), so the step "the left side depends on Zs₁ through ξ, while the right side is independent of Zs₁, therefore Zs₁ must be independent of n₁" is a non-sequitur. The paper presents this as a formal proof when it is at best an intuition. Remove the proof framing or provide a rigorous argument.

### Minor

3. **The reconstruction comparison is confounded by bitrate differences.** DeCodec operates at 8.0 kbps (4.0+4.0) versus EnCodec at 6.0 kbps and SpeechTokenizer at 4.0 kbps. Given the well-established rate-distortion relationship, higher bitrate is expected to yield better SDR. The SDR improvement over EnCodec on clean speech is modest (~0.75 dB for a 33% bitrate increase), and on mel distance DeCodec (0.89) is *worse* than both DAC (0.65) and HiFi-Codec (0.75) on clean speech. The paper does not acknowledge this confound. Since the dual-RVQ design is inherent to the method, the paper should at minimum discuss whether the modest SDR gains are justified by the architecture's additional functionality.

4. **Adding SG substantially degrades speech-background decoupling — a trade-off the paper understates.** Comparing Ablation-3 (SOP+RST, no SG) with DeCodec-c (full model) in Table 4 shows SDR-B dropping from 0.49 to -1.11 (−1.60 dB) and SDR-S dropping from 7.90 to 5.70 (−2.20 dB). The paper describes this as "a slight decrease in SDR," but these are non-trivial degradations that push BGS extraction below the usable threshold. The improvement in WER* (41.9 → 25.8) confirms SG helps semantic preservation, but the relationship between speech-background decoupling and semantic-paralinguistic decomposition is in tension under this architecture, not a clean "collaborative optimization." This should be discussed as a limitation.

5. **The derivation of SOP orthogonality (Section 3.4) relies on an undefined term.** Equation (6) says "When the covariance matrix YY^T satisfies the angular matrix" without defining what an "angular matrix" is or what property of YY^T is being assumed. This makes the claim that SOP "ensures the subspaces... to be disentangled" (end of Section 3.4) incomplete — the orthogonality loss L_⊥ directly enforces output orthogonality, but the attempt to derive P_S P_N^T = 0 from L_⊥ via YY^T is not properly justified.

6. **The one-shot VC result (50.46% WER, Table 3) is better than baselines but not practically usable.** A 50% word error rate means roughly every other word is incorrect. The paper acknowledges the cause (voicing time mismatch, Section 4.2.3) but still frames the result as "effective one-shot voice conversion" (Abstract). The comparison against SpeechTokenizer (74.18%) and StoRM-SpeechTokenizer (52.73%) is valid and shows relative improvement, but the absolute performance should be discussed more candidly as a limitation of representation-swapping approaches for VC, not as a practical capability.

### Trivial
None.

## Nice-to-Haves

- Clarify what constitutes a "blank audio" in the SE procedure (Section 4.2.2) — is it literally silence at the sample level or the quantized representation of silence?
- The SE baselines' scores are taken from an external paper (Wang et al., 2024) rather than re-evaluated; while DNSMOS is non-intrusive, the comparison could be strengthened by running baselines in the same evaluation loop.
- Specify the RST pairing strategy during training — are samples drawn uniformly, or are pairs constrained by SNR or speaker identity?

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"First time" claims (lines 39, 42) should be softened.** → Removed per rule: questioning "firstness" touches on related work coverage, which cannot be verified externally. The reviewer framed this as a presentation concern, not a factual error.
- **Missing hyperparameters (K_s, K_n, C, K, M, D, stride factors, codebook sizes, loss weighting).** → Removed per rule: reproducibility nitpicks about implementation details.
- **Missing appendix (ASR/TTS results).** → Removed per rule: appendix sections are stripped by the parser; they exist in the original submission.
- **Which Whisper variant is used.** → Removed per rule: trivial implementation detail.
- **DAC's anomalously low SDR (0.60 on clean speech).** → Removed per rule: the paper uses official checkpoints; the baseline's performance on this specific evaluation setup is not a weakness of the paper under review.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the gap between the paper's boldest claims (background sound extraction, "explicit decoupling") and the actual evidence (negative SDR-B, a non-rigorous proof), but this is a gap analysis rather than a novel insight.

## Suggestions

1. Diagnose why SG degrades decoupling (the drop from Ablation-3 to full DeCodec in Table 4 is the largest negative change in the ablation). If HuBERT supervision pulls the speech encoder away from representations compatible with the additive BGS framework, consider multi-task loss balancing or alternative semantic supervision.
2. Provide qualitative analysis of the BGS component (spectrograms, listening samples) even if SDR-B is negative — this would help readers understand whether the BGS representation captures useful non-speech information despite poor waveform reconstruction.
3. Remove or substantially reframe the theoretical "proof" in Section 3.6 as intuition. The empirical results (ablation study) already provide strong evidence for the decoupling.
4. Discuss the bitrate discrepancy explicitly and add a controlled experiment matching bitrates if feasible.
5. Calibrate the "background sound extraction" and "one-shot VC" claims to match the evidence — the former is not demonstrated at a usable level, and the latter is a relative improvement over very poor baselines.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>