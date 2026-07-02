Now I have a clear calibration picture. Let me write the final review.

## Calibration Summary

**Anchors inspected (all rounds):**

| Anchor | Avg Score | Comparison to DeCodec |
|--------|-----------|----------------------|
| DM-Codec (UFwefiypla) | 3.00 (Reject) | Less novel: just SpeechTokenizer + LM distillation; DeCodec has stronger novelty |
| Universal Semantic Disentangled (Id2JMVSQHZ) | 4.80 (Reject) | Similar domain (disentangled codec), but DeCodec has more novel technique (SOP+RST) |
| DC-Spin (OW332Wh9S5) | 4.75 (Reject) | Speaker-invariant tokenizer; DeCodec addresses a different problem with more novel architecture |
| RepCodec (LfDUzzQa3g) | 5.50 (Reject) | Stronger novelty than RepCodec (which is SoundStream applied to SSL features), but weaker evidence |
| Vec-Tok Speech (C53xlgEqVh) | 5.20 (Reject) | Comparable: both have novel architectures but incomplete evidence |
| Towards Codec-LM Co-design (KCVv3tICvp) | 5.00 (Reject) | Engineering tricks vs. DeCodec's more fundamental architectural novelty |
| Vevo (anQDiQZhDP) | 5.50 (Accept) | Different domain (voice imitation); accepted with 5.50 — shows 5.5 can be accept |
| FlowDec (uxDFlPGRLX) | 7.00 (Accept) | Much stronger evidence, rigorous evaluation, no claim-evidence gap |
| HALL-E (868masI331) | 6.40 (Accept) | Strong empirical results with thorough TTS evaluation |

**Round-1 bracket:** 4–6

**Narrowing:** DeCodec has stronger novelty than the 3–5 range papers but suffers from claim-evidence gaps worse than than the 5.5–7 range papers. The SDR-B being negative directly contradicts the "explicit decoupling" central claim, and the bitrate disparity weakens the reconstruction comparison. This pushes it below the strong-baseline papers (FlowDec, HALL-E) but above the incremental papers (DM-Codec, RepCodec-type). 

**Final score:** 5.0 — the core idea is novel and the SE application is clever, but the evidence for the central claim of decoupling is weak, and key comparisons are invalidated by unacknowledged advantages.

---

## Summary

DeCodec proposes a neural audio codec that learns to decouple audio representations into orthogonal subspaces for speech and background sound via a Subspace Orthogonal Projection (SOP) module and Representation Swap Training (RST) procedure, and further decomposes speech into semantic and paralinguistic components via semantic guidance. The paper demonstrates this hierarchical disentanglement for speech enhancement, one-shot voice conversion, ASR, and TTS.

## Strengths

1. **Genuinely novel formulation.** The idea of learning orthogonal subspaces within a neural codec to separately represent speech and background sound, then further decomposing speech into semantic and paralinguistic components, is original. No prior codec work attempts this joint hierarchical disentanglement. The integration of SOP with RST is a non-obvious design that differs from prior speech decomposition work (SpeechTokenizer, FACodec) and universal audio coding (EnCodec, DAC).

2. **Competitive speech enhancement from a codec.** The SE application (Section 4.2.2) — replacing the BGS subspace representation with that of blank audio — achieves DNSMOS scores competitive with dedicated SE models (BAK 4.13/3.99 simulated/real, Table 2). This demonstrates practical value from the decoupled representation in a concrete downstream task.

3. **Informative ablation study.** Table 4 cleanly shows the synergy between SOP and RST: neither works alone (SDR-B < -10 dB for Ablation-1 and Ablation-2), but together they produce meaningful decoupling (Ablation-3: SDR-B=0.49, SDR-S=7.90). This non-obvious interaction is the strongest empirical evidence for the joint design.

## Weaknesses

### Major

1. **Unacknowledged bitrate disparity in reconstruction comparison (Table 1).** DeCodec operates at **8.0 kbps** total (4.0 speech + 4.0 BGS), while baselines use 2.0–6.0 kbps for the entire signal (EnCodec: 6.0, DAC: 4.5, SpeechTokenizer: 4.0). This 33%–300% bitrate advantage can explain much of the SDR improvement (DeCodec 7.61 vs. EnCodec 6.86 on clean speech). The paper claims DeCodec "performs comparably to existing codec models in reconstruction" without acknowledging this disparity. A controlled ablation at matched total bitrate is needed to isolate the cost of the decoupling mechanism from the bitrate advantage.

2. **Weak decoupling metrics contradict the paper's strongest claims.** The paper claims "explicit decoupling representation of speech and background sound" (Section 1, Contributions). Yet the full non-causal DeCodec achieves **SDR-B = -0.36 dB** (Table 4) — a negative SDR means the extracted background sound has more distortion than signal. The causal version (DeCodec-c) is worse at SDR-B = -1.11 dB. SDR-S = 6.73 dB is modest. These numbers indicate partial decoupling at best: the BGS subspace fails to capture clean BGS, and the speech path retains BGS contamination. The SE application works because replacing BGS with blank audio is a coarse operation that requires clean speech-path representations, not cleanly-extracted BGS — so the SE results do not validate the decoupling claim as strongly as implied.

3. **Voice conversion claim is overstated.** The abstract and introduction claim "effective one-shot voice conversion," yet at 50.46% WER (Table 3) on noisy inputs, the converted speech has roughly every other word incorrect. While this improves over baselines (SpeechTokenizer: 74.18%, StoRM-SpeechTokenizer: 52.73%), 50% WER is far from practically usable. This is better characterized as a proof-of-concept that the semantic/paralinguistic decomposition survives speech-BGS decoupling, not "effective" VC.

### Minor

1. **The theoretical "proof" in Section 3.6 is not rigorous.** The MVT-for-vector-functions argument is applied to approximate equalities (from loss minimization, not exact identities). The claim that the left side "depends on Zs₁ through ξ" does not establish statistical independence — the Jacobian at an interpolation point ξ may not depend on Zs₁ in a meaningful way. The paper should present this as intuition, not a theoretical guarantee.

2. **"Angular matrix" is undefined (Section 3.4, line 106).** The claim "When the covariance matrix YY^T satisfies the angular matrix" uses undefined terminology, and the subsequent reasoning about independent channels leading to P_S P_N^T = 0 is hand-wavy.

3. **Adding SG degrades decoupling quality but this is under-discussed.** In Table 4, moving from Ablation-3 (SOP+RST, no SG) to DeCodec-c (with SG) drops SDR-B from 0.49 to -1.11 and SDR-S from 7.90 to 5.70. The paper calls this "a slight decrease in SDR," but SDR-B crossing from positive to negative is a qualitative shift. This trade-off should be discussed transparently.

4. **Inconsistency between text and Figure 2 caption about number of encoders.** The text (Section 3.2) describes a single encoder producing Y, followed by two linear projection layers. The Figure 2 caption says "two encoders (Enc)." Clarify whether there is one shared encoder or two separate encoder copies.

### Trivial

- The SIM score in Table 3 (0.83) exceeding the reference SIM (0.69) is not commented on. This warrants brief discussion.
- "Blank audio" used for SE replacement (Section 4.2.2) is not specified — is it absolute silence or a recorded noise floor?

## Nice-to-Haves

- A matched-bitrate ablation (e.g., reducing SRVQ layers to match DAC at 4.5 kbps or EnCodec at 6.0 kbps total) would cleanly separate bitrate benefit from architectural benefit.
- Direct disentanglement measurement (mutual information between speech/BGS codebook entries, or a classifier probe predicting BGS type from the speech path) would validate the core claim more directly than SDR.
- Computational cost comparison (parameters, inference latency) vs. baselines.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **ASR/TTS results in the appendix:** Removed — parser strips appendices from all papers; they exist in the original submission.
- **No computation cost comparison:** Moved to Nice-to-Haves as it's not standard to report for codec papers.
- **Speculative criticism of SIM metric reliability:** Removed — reference SIM=0.69 is cross-utterance same-speaker similarity and can reasonably be exceeded by VC output.
- **Criticism that the SE application "doesn't require cleanly extracted BGS":** While preserved in the Major weakness about decoupling metrics, the stronger version claiming the SE results are "invalid" as evidence of decoupling was removed — the SE application does demonstrate useful decoupling even if asymmetric.

## Novel Insights

Beyond the paper's own contributions, the most striking observation from the reviews is the **asymmetric decoupling**: DeCodec's SE application works well (suggesting the speech path is reasonably clean) while SDR-B is negative (suggesting the BGS path is poor at capturing true background sound). This asymmetry is not discussed in the paper but may be the key design insight: the RST procedure appears to preferentially protect speech-path purity at the expense of BGS-path fidelity. Future work could investigate whether this asymmetry is inherent or whether a symmetric version is achievable.

## Suggestions

1. **Add a matched-bitrate experiment.** Reduce SRVQ or NRVQ layers to match EnCodec at 6.0 kbps total. Report reconstruction SDR to isolate the cost of decoupling.
2. **Calibrate claims to evidence.** Replace "explicit decoupling" with "partial decoupling" and "effective one-shot VC" with "proof-of-concept VC showing semantic/paralinguistic decomposition survives noise."
3. **Discuss the SG-decoupling trade-off.** Transparently report that SG improves semantic decomposition but degrades speech/BGS separation.
4. **Reframe the theoretical proof.** Remove the "proof" framing or explicitly label it as intuitive motivation. The empirical ablation (Table 4) is the stronger evidence anyway.
5. **Define "angular matrix"** or remove the reference.
6. **Specify the "blank audio"** used for SE.
7. **Resolve the encoder inconsistency** between text (one encoder) and Figure 2 caption ("two encoders").

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>