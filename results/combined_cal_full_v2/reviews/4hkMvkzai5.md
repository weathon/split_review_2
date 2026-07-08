Now I have all the information I need. Let me write the final consolidated review.

## Summary

DeCodec reframes audio codecs as universal disentangled representation learners, introducing a neural codec that decouples speech and background sound (BGS) into orthogonal subspaces via a Subspace Orthogonal Projection (SOP) module and a Representation Swap Training (RST) procedure. Within speech, Semantic Guidance (SG) further decomposes representations into semantic and paralinguistic components. The model demonstrates multi-task capability from a single trained model — reconstruction, speech enhancement, one-shot voice conversion, and feature provision for ASR/TTS.

## Strengths

- **A genuinely novel framing.** The central idea — reframing audio codecs as disentangled representation learners that separate speech and background sound in the learned embedding space rather than through cascaded signal-domain separation — is creative and well-motivated. The limitations of cascaded pipelines (error propagation, distortion, computational cost) are clearly stated in §1, and the proposed alternative of doing separation in the representation domain is a coherent response. This is not an incremental modification of an existing codec.

- **Clean conceptual architecture.** The three-component design (SOP for orthogonal subspace projection, RST for enforcing speech/BGS correspondence, and SG for semantic/paralinguistic decomposition within speech) maps cleanly onto the stated problem. The parallel RVQ design with separate quantizers for speech and BGS is a natural consequence of the subspace approach, not an afterthought.

- **Multi-task capability from a single model.** The paper demonstrates that one trained model can handle reconstruction, speech enhancement (achieving competitive or superior DNSMOS scores vs. dedicated SE models like SELM and StoRM in Table 2), voice conversion with SE, and feature provision for ASR and TTS. Even if individual task performance is imperfect, having these capabilities emerge from a single codec training is noteworthy.

## Weaknesses

### Fatal
None.

### Major

- **Unfair reconstruction comparison (Table 1).** DeCodec operates at 8.0 kbps total (4.0 kbps for speech + 4.0 kbps for BGS), while every baseline uses a substantially lower bitrate: EnCodec at 6.0, HiFi-Codec at 2.0, DAC at 4.5, SpeechTokenizer at 4.0 kbps. The paper claims "the proposed DeCodec achieves the highest SDR for speech reconstruction" (line 188) without acknowledging this disparity — better reconstruction at higher bitrate is expected, not informative. Furthermore, the ablation study (Table 4) shows that Ablation-1 (SOP only, no decoupling) achieves SDR-O of 8.93, far exceeding the full DeCodec-c at 4.62, meaning the decoupling mechanism actively degrades reconstruction quality. The headline reconstruction result conflates a bitrate advantage with architectural merit.

- **Decoupling quality evidence is weak.** The primary metric for BGS extraction quality, SDR-B, hovers near 0 dB in all configurations (Ablation-3: 0.49, DeCodec-c: −1.11, DeCodec: −0.36 in Table 4). An SDR of 0 dB means the extracted signal has roughly equal power to the distortion — this does not convincingly demonstrate faithful BGS extraction. Standard separation metrics (SI-SDRi, SDR improvement over the mixture) are not reported, making comparison with the speech separation literature impossible. While the SE results (Table 2) provide indirect evidence that BGS is being suppressed, the paper's claim of "effective decoupling" (line 252) based on SDR-B values near 0 dB is not well-supported.

### Minor

- **SE evaluation relies solely on DNSMOS**, a learned perceptual metric. Standard objective SE metrics (PESQ, STOI, SI-SDR) are absent, limiting comparability with the broader SE literature where these metrics are standard.

- **The theoretical "proof" in §3.6 is not rigorous.** The argument applies the mean value theorem for vector-valued functions to a quantized, non-convex neural network decoder without establishing Lipschitz or smoothness guarantees. The MVT for vector-valued functions does not yield equality as written, and the derivation treats approximate equalities (Eq. 13–14) as exact identities for subtraction. This should be presented as motivating intuition, not as a formal proof.

- **"Angular matrix" (line 106) is undefined jargon.** The paper states "when the covariance matrix YY^T satisfies the angular matrix" without defining this term, making the orthogonality argument unclear.

- **One-shot VC results are overstated.** While DeCodec achieves 50.46% WER vs. 74.18% for SpeechTokenizer (Table 3), this means every other word is wrong on average — the output is barely intelligible. The SIM value of 0.83 exceeding the reference SIM of 0.69 is unusual and suggests either a metric artifact or a non-apples-to-apples protocol. The paper's claim that this demonstrates effective semantic/paralinguistic decomposition (line 237) is not supported by a 50% WER.

- **SG supervision requires clean speech during training.** Equation (7) uses HuBERT-L9 features from clean speech s as the supervision target, meaning the approach currently requires access to ground-truth clean speech and is limited to supervised synthetic-mixture training. This is not discussed as a limitation.

- **"Universal" is an overstatement.** The model is trained only on speech mixed with BGS from two noise corpora (ESC-50, DNS-Noise). It does not handle music, animal sounds, multi-speaker mixtures, or general audio types. A more accurate descriptor would be "speech-background disentangled codec."

- **Computational efficiency claim is unsubstantiated.** The paper claims "computational efficiency via feature selection rather than differential extraction" (§1) but provides no FLOPs, parameter counts, or runtime comparisons. Given the two-encoder design and parallel RVQ streams, DeCodec is likely more expensive than standard codecs — this claimed advantage is not quantified.

### Trivial
None.

## Nice-to-Haves

- Add a same-bitrate baseline (e.g., DAC or EnCodec at 8.0 kbps) to Table 1 to enable a fair reconstruction comparison.
- Report SI-SDRi or SDR improvement over the mixture for both speech and BGS extraction to substantiate the decoupling claim.
- Add standard objective SE metrics (PESQ, STOI) alongside DNSMOS.
- Compare against a cascaded pipeline (standard codec + time-domain separation front-end) on the same downstream tasks to directly test the claim that representation-domain decoupling introduces less distortion.
- Ablate the two-encoder design vs. a single shared encoder with two projection heads.

## Removed Points

These points from the input review are removed per filtering rules:

- **Missing reproducibility details (optimizer, learning rate, batch size, GPU hours, code availability):** Removed per instruction to treat undisclosed hyperparameters as nitpicks.
- **Hyperparameter choices not justified (why 4.0 kbps per RVQ, why two encoders, LSTM layers, projection initialization):** Removed per instruction about trivial implementation details.
- **Missing critical baselines (retrained DAC at 8 kbps, Conv-TasNet comparison, two-encoder ablation):** Partially subsumed under the bitrate fairness issue; remaining items moved to Nice-to-Haves.
- **RST shortcut discussion (model learning to ignore BGS quantizer):** Speculative concern without evidence in the paper.
- **Reference to Appendix H / stripped appendix content:** Parser artifact; the appendix exists in the original submission.
- **Formatting, style, and typo nitpicks:** Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a same-bitrate baseline to the reconstruction comparison to disentangle the effect of bitrate from architectural merit.
2. Report standard separation metrics (SI-SDRi) for both speech and BGS extraction to make the decoupling claim more concrete.
3. Add PESQ and STOI to the SE evaluation to complement DNSMOS.
4. Present the theoretical argument in §3.6 as motivating intuition rather than a formal proof, and either define or remove the "angular matrix" terminology.
5. Quantify computational cost (FLOPs, parameters, RTF) to support the efficiency claim.
6. Tone down the "universal" claim to reflect the actual training domain (speech + BGS from two noise corpora).

## Score and Decision

**Calibration summary (all anchors retrieved):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|---|
| DM-Codec | .../UFwefiypla.md | 3.00 | R1 | Yes | Speech tokenization paper with similar scope but weaker novelty; DeCodec is clearly stronger |
| Universal Semantic Disentangled | .../Id2JMVSQHZ.md | 4.80 | R1 | Yes | Disentangled codec for privacy; comparable scope, similar evaluation gaps but less novel core idea |
| Towards Codec-LM Co-design | .../KCVv3tICvp.md | 5.00 | R2 | Yes | Codec-LM design strategies; comparable quality with more negative-weighted weaknesses |
| RepCodec | .../LfDUzzQa3g.md | 5.50 | R2 | Yes | Speech tokenization; stronger evaluation but less conceptual novelty |
| Vec-Tok Speech | .../C53xlgEqVh.md | 5.20 | R2 | Yes | Speech vectorization/tokenization; comparable multi-task scope, similar evaluation gaps |
| Separate and Diffuse | .../UXALv0lJZS.md | 6.00 | R1 | Yes | Speech separation with diffusion; stronger theoretical grounding and evaluation |
| TIGER | .../rzx3vcvlzj.md | 5.83 | R1 | No | Speech separation; stronger efficiency analysis |
| FlowDec | .../uxDFlPGRLX.md | 7.00 | R1 | Yes | Full-band audio codec; far stronger evaluation with listening tests and same-bitrate comparisons |
| HALL-E | .../868masI331.md | 6.40 | R1 | No | Hierarchical neural codec LM; stronger TTS evaluation |

**Bracket (Round 1):** Between 4.0 and 6.0.

**Narrowing (Round 2):** The weighted-item comparison places DeCodec closest to the 4.8–5.5 anchors. Compared to the Universal Semantic Disentangled paper (4.8), DeCodec has a more novel core idea and its most negative-weighted weakness (−2.30 for VC WER) is less severe than that paper's −4.20 (limited contribution). Compared to Codec-LM Co-design (5.0), DeCodec's negative weights are less severe overall (−2.30 vs. −3.58, −3.69). However, DeCodec's two major weaknesses — the unfair bitrate comparison and the weak decoupling evidence — are genuine problems that meaningfully weaken its support. The strengths have strong positive weights (8–10), comparable to the 5.0–5.5 anchors.

**Final score:** 5.0. The paper presents a genuinely novel and well-motivated idea with a clean architecture and demonstrated multi-task capability. However, the reconstruction comparison is unfairly configured (mismatched bitrates), the decoupling evidence is weaker than claimed (SDR-B near 0 dB), and several claims are not fully supported by the experiments. The paper's contribution is promising but requires substantial evaluation improvements to meet the acceptance bar.

**Decision:** Reject (borderline — could be acceptable after revisions addressing the major weaknesses, particularly adding same-bitrate baselines and stronger decoupling metrics).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>