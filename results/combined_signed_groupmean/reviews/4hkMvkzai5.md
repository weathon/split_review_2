Here is my final consolidated review.

---

## Summary

DeCodec proposes a neural audio codec that learns to disentangle speech and background sound (BGS) representations via subspace orthogonal projection (SOP) and representation swap training (RST), with further decomposition of speech into semantic and paralinguistic components through semantic guidance (SG). The key claim is that this disentanglement enables controllable feature selection, allowing a single codec to serve as a universal front-end for reconstruction, speech enhancement, voice conversion, ASR, and TTS. The main evidence is: (1) an ablation study (Table 4) showing SOP+RST jointly produce meaningful decoupling where neither alone does, and (2) speech enhancement results (Table 2) that match or exceed dedicated SE models via simple representation substitution.

## Strengths

- **Novel disentanglement mechanism (SOP + RST).** The combination of orthogonal subspace projection and representation swap training is genuinely novel. The ablation study (Table 4) provides convincing evidence that neither component alone produces meaningful decoupling (SDR-B ≈ −10 to −13 dB), while their combination jumps to SDR-B = 0.49 dB. This is a clear, non-obvious synergy. **[impact=+10.00]**

- **Strong speech enhancement results from simple representation manipulation.** Table 2 shows DeCodec achieves DNSMOS OVL scores of 3.39 (simulated) and 3.13 (real), matching or exceeding dedicated SE models (SELM: 3.26/3.12, StoRM: 3.21/2.94). The BAK (background suppression) scores are particularly notable: 4.13/3.99 vs. SELM's 4.10/3.44. This demonstrates that the disentanglement is operationally useful. **[impact=+9.85]**

- **Clean ablation design.** Table 4 clearly separates the effects of SOP alone, RST alone, SOP+RST, and SOP+RST+SG. The progression from SDR-B = −13.15 (SOP only) → −10.67 (RST only) → 0.49 (SOP+RST) is unambiguous evidence that both components are necessary and jointly sufficient for decoupling. **[impact=+9.94]**

## Weaknesses

### Major

- **Unfair reconstruction comparison due to bitrate mismatch (Table 1).** DeCodec operates at 8.0 kbps (4.0 kbps SRVQ + 4.0 kbps BRVQ) while the baselines run at 2.0–6.0 kbps — 1.3× to 4× lower bitrate. The paper never acknowledges this disparity or controls for it (e.g., by evaluating baselines at matched bitrates or presenting rate-distortion curves). The headline SDR improvements (7.61 vs. EnCodec's 6.86 on clean speech, 5.21 vs. 4.88 on noisy speech) are modest given this bitrate advantage. The abstract's claim that "DeCodec maintains advanced signal reconstruction" relies on this comparison and is therefore unsupported without controlling for bitrate. This is an addressable issue — the paper's core contribution (disentanglement) does not depend on being a better codec — but as presented, Table 1 conflates architectural advantage with bitrate budget. **[impact=-10.00]**

### Minor

- **Theoretical proof in Section 3.6 is not mathematically valid.** The mean value theorem for vector-valued functions gives an inequality on the norm, not the component-wise equality used in Eq. (16). The subtraction of Eq. (13) from Eq. (14) assumes decoder nonlinearity cancels in a way that does not generally hold: $\text{Dec}(A+B) - \text{Dec}(A+C) \neq \text{Dec}(B-C)$ in general. The conclusion that "$\mathbf{Zs}_1$ must be independent of $\mathbf{n}_1$" does not follow from the stated equations because the Jacobian depends on $\mathbf{Zs}_1$ through $\xi$ in a coupled way. However, the strong empirical evidence (Table 4) independently supports the decoupling claim, so this does **not** threaten the paper's core contribution — the proof should be removed or reframed as intuitive motivation rather than rigorous argument. **[impact=-6.56]**

- **SG causing decreased decoupling quality left unexplained.** Table 4 shows that adding SG (DeCodec-c vs. Ablation-3) decreases both SDR-B (0.49 → −1.11) and SDR-S (7.90 → 5.70). The paper acknowledges "a slight decrease in SDR" but does not discuss *why* semantic guidance interferes with speech/BGS decoupling. Since SG is a core claimed contribution, understanding this trade-off matters. **[impact=-0.00]**

- **"Blank audio" mechanism underspecified.** Section 4.2.2 states that BGS representations are replaced with those "of a blank audio with the same length" but never defines what constitutes blank audio (zero-padding? a silent recording encoded through the codec? something else?) or how its BGS representations are obtained. This makes the SE procedure difficult to reproduce. **[impact=-0.90]**

### Trivial

- No confidence intervals or variance reported for any metric in any table.

## Nice-to-Haves

- Reporting computational cost (parameters, FLOPs, inference speed) would contextualize the efficiency claim in the introduction.
- Evaluating the quality of extracted BGS representations on BGS-specific tasks (e.g., sound event classification) would further validate the disentanglement.
- A deeper analysis of the causal vs. non-causal version trade-offs (latency, quality degradation) would be useful for practitioners.

## Removed Points

The following points from the harsh critic review were removed (with justification):

- **Missing appendix / downstream results (ASR, TTS):** REMOVED — The parser strips appendix sections from all papers; these exist in the original submission.
- **Architectural parameters not specified:** REMOVED — The paper states it adopts DAC's architecture and refers to that paper, which is standard practice.
- **Analogy to auditory cortex "suggestive rather than mechanistic":** REMOVED — The paper uses this as high-level inspiration, not a mechanistic claim.
- **"Preservation of original signal integrity" misleading:** REMOVED — This refers to avoiding front-end separation distortion (from cascaded SS pipelines), not claiming lossless encoding.
- **VC protocol unusual:** REMOVED — The paper clearly describes its approach and honestly reports the 50.46% WER with an explanation.
- **No confidence intervals:** REMOVED — Single-run DNSMOS evaluation is standard in this field.
- **No computational cost / BGS evaluation / causal analysis:** MOVED to Nice-to-Haves — These are outside the paper's stated scope or not standard requirements.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe or repair the reconstruction evaluation.** Either: (a) compare DeCodec to baselines at matched total bitrate, (b) present rate-distortion curves across multiple bitrates, or (c) honestly acknowledge the bitrate disparity and dial back claims about reconstruction superiority, making SE and disentanglement the headline contributions.
2. **Remove or substantially rewrite Section 3.6.** Rely on the strong ablation evidence (Table 4) instead of an incorrect proof.
3. **Explain why SG reduces decoupling quality** (the SDR-B and SDR-S drops in Table 4).
4. **Define "blank audio"** precisely in the SE procedure.
5. **Report confidence intervals** for at least the main results to assess statistical reliability.

## Score and Decision

**Calibration anchors (all retrieved):**

| Anchor | Score | Round | Itemized? | Comparison to DeCodec |
|--------|-------|-------|-----------|----------------------|
| gwZ90hFSL2.md (NLP/humanoid robots) | 1.0 | R1 | No | Unrelated topic |
| nSDOkm0SKo.md (finance) | 1.0 | R1 | No | Unrelated topic |
| u1cQYxRI1H.md (illumination) | 0.5 | R1 | No | Unrelated topic |
| 5lUdTogEL3.md (person re-ID) | 1.0 | R1 | No | Unrelated topic |
| **UFwefiypla.md (DM-Codec)** | **3.0** | **R1** | **Yes** | Speech tokenizer with fundamental length-mismatch flaw. DeCodec is substantially stronger — its core method works and is validated. |
| mlPTNEIsgb.md (audio inverse) | 3.25 | R1 | No | Different problem |
| JOBokGDcX0.md (chunking) | 2.5 | R1 | No | Different problem |
| nhgTmx1TZJ.md (UniAudio) | 3.0 | R1 | No | Different framing |
| **Id2JMVSQHZ.md (USC)** | **4.8** | **R1, R2** | **Yes** | Privacy-preserving disentangled codec. Comparable flaws (missing baselines) but DeCodec has stronger ablation and more novel method. DeCodec is slightly stronger. |
| KCVv3tICvp.md (Codec-LM) | 5.0 | R1 | No | Different focus (codec-LM co-design) |
| xJc3PazBwS.md (disentangling) | 3.75 | R1 | No | Different approach (information bottleneck) |
| **C53xlgEqVh.md (Vec-Tok Speech)** | **5.2** | **R1** | **Yes** | Multi-task speech codec. Comparable scope; DeCodec has stronger novelty in SOP+RST but bitrate issue is more prominent. Comparable quality. |
| 1p6xFLBU4J.md (GenSE) | 6.0 | R1 | No | SE via LMs — different approach |
| **uxDFlPGRLX.md (FlowDec)** | **7.0** | **R1** | **Yes** | High-quality audio codec, rigorous evaluation. Stronger overall paper. DeCodec is below this. |
| ale56Ya59q.md (self-supervised SE) | 7.0 | R1 | No | Different problem |
| UXALv0lJZS.md (separate+diffuse) | 6.0 | R1 | No | Different approach |
| j7b4mm7Ec9.md (watermarking) | 7.6 | R1 | No | Unrelated |
| CxXGvKRDnL.md (compression) | 8.0 | R1 | No | Unrelated |
| tyEyYT267x.md (diffusion LM) | 8.0 | R1 | No | Unrelated |
| GMwRl2e9Y1.md (VQ rotation) | 8.0 | R1 | No | Unrelated |
| **LfDUzzQa3g.md (RepCodec)** | **5.5** | **R2** | **Yes** | Speech representation codec. Novelty concerns (VQ on SSL features). DeCodec has a more novel method. Comparable quality. |
| 868masI331.md (HALL-E) | 6.4 | R2 | No | Hierarchical codec LM — different approach |
| b57IG6N20B.md (biosignals) | 6.6 | R2 | No | Different domain |

**Round-1 bracket:** 4.0–6.0.  
**Narrowing:** Compared itemized impact scores of closest anchors. DeCodec's strengths (+10.00, +9.85, +9.94) are stronger than USC's (highest +9.61 but mostly lower) and RepCodec's (highest +9.05 but mostly lower). However, DeCodec's dominant weakness (−10.00 for the bitrate mismatch) is more severe than RepCodec's top weakness (−10.00 for lack of novelty) because DeCodec's weakness is methodological (unfair comparison) rather than a novelty judgment. The net effect places DeCodec slightly above USC (4.8) and comparable to RepCodec (5.5) and Vec-Tok Speech (5.2).

The paper's core contribution — speech/BGS disentanglement via SOP+RST — is genuinely novel and well-validated by the ablation study and SE results. The bitrate mismatch in Table 1 is a real but addressable flaw: it undermines one set of claims (reconstruction superiority) but not the main contribution. The flawed theoretical proof is minor because the empirical evidence stands on its own. With a fair reconstruction comparison, this paper would comfortably reach the borderline-accept range.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>