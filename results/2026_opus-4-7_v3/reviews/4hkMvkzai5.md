Now let me verify a few more specific claims — the bitrate details, the SE evaluation section, and the ablation.Now I have a thorough understanding of the paper. Let me construct the draft review based on my verified findings.Now let me run calibration Round 1 — bracketing pass across score bands:Let me read a few of the most relevant anchors to calibrate my score:Now I have enough information to form my calibration bracket and produce the final review. Let me analyze the anchors:

**Round 1 Bracket Analysis:**
- DeCodec is clearly above the 1-3 range (stronger novelty, broader evaluation than DM-Codec at 3.0)
- DeCodec is above the privacy-preserving speech codec (4.80) — more novel architecture, better ablations
- DeCodec is comparable to GenSE (6.0, Accept) and Codec-LM Co-design (5.0, Reject) — similar novelty levels
- DeCodec is below FlowDec (7.0, Accept) — less rigorous evaluation, unfair comparisons

**Initial bracket: 5.0–6.5**

The core novelty (RST+SOP synergy with strong ablation evidence) pushes toward the higher end. The bitrate comparison issue, theoretical overclaiming, and SE evaluation gaps pull toward the lower end.

Now let me write the final consolidated review:

---

## Summary
DeCodec proposes a neural audio codec that disentangles speech from background sound in representation space via two innovations: a Subspace Orthogonal Projection (SOP) module that projects encoder embeddings into orthogonal subspaces, and a Representation Swap Training (RST) procedure that forces these subspaces to correspond to speech and background sound respectively. Within the speech branch, semantic guidance (SG) further decomposes into semantic and paralinguistic components, enabling multi-task capabilities (reconstruction, speech enhancement, voice conversion, ASR/TTS support) from a single model via representation recombination.

## Strengths

- **Representation Swap Training is a genuinely novel and well-validated mechanism.** RST (Section 3.6) uses cross-sample representation recombination as a training objective: by taking speech from y₁₁ and background from y₂₂, then requiring reconstruction of s₁ + n₂, the system receives direct gradient signal forcing branch-specific encoding. This is distinct from standard signal-domain separation losses. The ablation (Table 4) confirms this is critical and synergistic with SOP: SOP alone yields SDR-B of −13.15, RST alone yields −10.67, while SOP+RST yields 0.49 — neither component alone suffices.

- **Thorough ablation study isolates component contributions.** Table 4 systematically demonstrates that (1) SOP and RST individually fail but jointly succeed at disentanglement, and (2) SG trades modest SDR for substantially better semantic purity (WER* drops from 41.9 to 25.8). This is the most informative experiment in the paper and directly validates the architectural design decisions.

- **Multi-task capability from representation recombination without task-specific fine-tuning.** The paper demonstrates reconstruction, SE, background extraction, and one-shot VC all from a single model by recombining disentangled representations. This concretely validates the paper's thesis that disentangled codecs enable flexible downstream use, and is a practical advantage over cascaded pipelines.

- **Competitive SE performance against dedicated models.** On the DNS Challenge test set (Table 2), DeCodec achieves the highest overall DNSMOS scores (OVL=3.39, BAK=4.13 without reverb), outperforming dedicated SE methods like SELM and StoRM in background suppression (BAK), despite being a general-purpose codec rather than a specialized SE system.

## Weaknesses

### Fatal
None

### Major

- **Unfair bitrate comparison in codec reconstruction (Table 1).** DeCodec operates at 4.0+4.0 = 8.0 kbps while baselines range from 2.0 kbps (HiFi-Codec) to 6.0 kbps (EnCodec). The paper claims "the proposed DeCodec achieves the highest SDR for speech reconstruction" without acknowledging this 33–300% bitrate advantage. While the two streams serve different purposes (speech vs. background), the paper neither discusses this asymmetry nor provides rate-matched ablations (e.g., 2+2 or 3+3 kbps) to show whether the architecture itself — rather than extra bandwidth — explains the SDR gains. The narrative that DeCodec "performs comparably to existing codec models in reconstruction" is misleading given the significant bitrate gap.

- **Theoretical claims presented as proofs but containing logical gaps.** Section 3.6 states "we theoretically prove that the proposed L_RST can further force Zs to be speech representations only." The argument applies the mean value theorem to the nonlinear decoder (Eq. 16), then concludes Zs₁ must be independent of n₁ because "the left side depends on Zs₁ through ξ, while the right side is independent of Zs₁." However, for a general neural network decoder, the Jacobian ∂Dec/∂Zn evaluated at ξ does depend on the full input including Zs₁, invalidating the independence conclusion as a formal proof. Similarly, Section 3.4 derives P_S P_N^T = 0 only under the unverified assumption that YY^T is an "angular matrix" (line 106). These should be presented as motivating intuitions rather than formal proofs — the empirical evidence (Table 4) adequately supports the approach regardless.

### Minor

- **SE evaluation uses only non-intrusive metrics.** Table 2 reports only DNSMOS for SE evaluation. While the DNS Challenge blind test sets lack ground truth (precluding intrusive metrics there), the paper also created a simulated noisy test set with known clean references (Section 4.1). Reporting SI-SDR or PESQ on that set would strengthen the SE claim, particularly since DNSMOS may not capture codec-specific artifacts.

- **P_S + P_N = I is stated (Eq. 4) but not enforced.** The two linear projection layers are trained only with the orthogonality loss L_⊥ (Eq. 5) — no architectural constraint ensures their outputs sum to Y. If they don't, information may be lost by neither projection, potentially explaining the SDR-O drop when adding SOP+RST (8.93 → 6.68 in Table 4). An architectural enforcement (e.g., P_N = I − P_S) could address this.

- **"Universal" framing overclaims demonstrated scope.** The title describes DeCodec as "an universal disentangled representation learner," but it is only trained and evaluated on speech + environmental noise. Music — a major audio category — is absent. "Speech-and-background-sound disentangled codec" would more accurately reflect the demonstrated scope.

- **Voice conversion WER is high in absolute terms.** DeCodec achieves WER=50.46% on one-shot VC (Table 3), meaning roughly half the words are lost. While this outperforms the cascaded baseline StoRM-SpeechTokenizer (52.73%) and the paper provides a reasonable explanation (mismatched voicing times), the high absolute WER limits practical VC utility claims.

### Trivial
None

## Nice-to-Haves
- Rate-matched ablations at different SRVQ/NRVQ budget splits (e.g., 2+2, 3+3, 4+4 kbps) to isolate architectural gains from bandwidth gains.
- Intrusive SE metrics (SI-SDR, PESQ) on the simulated noisy test set.
- Quantitative measurement of information leakage between branches (mutual information, probing classifiers) beyond SDR proxies.
- Computational cost comparison with cascaded pipelines (the paper motivates efficiency over cascading but never measures inference time, parameters, or FLOPs).
- Analysis of performance at extreme SNRs (very low or very high).

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Neuroscience analogy is "window dressing"**: Removed as a stylistic/presentation preference. The A2 cortex analogy serves as motivation and does not affect technical content or claims.
- **Training data size (700h) is modest compared to baselines**: This observation cuts both ways — if DeCodec performs well with less data, it could suggest data efficiency. Moreover, using official pretrained checkpoints for baselines is standard practice. Removed as insufficiently directional.
- **Additive-noise-only limitation (no reverberation, overlapping speakers)**: The paper explicitly scopes its problem as y=s+n (Section 3.1). Criticizing the absence of reverberant handling is scope creep per the paper's stated formulation.
- **SIG score on real recordings (3.45) below SELM (3.59)**: The paper explicitly acknowledges this limitation in the text (Section 4.2.2: "slightly inferior to SELM in real recordings, possibly because the proposed method...includes discretization quantizers"). The overall DNSMOS scores still favor DeCodec. Removed as already addressed.
- **No comparison against dedicated VC systems**: VC is demonstrated as an emergent capability from representation recombination, not the paper's primary contribution. Demanding comparison against specialized VC systems is scope creep.

## Novel Insights
The Representation Swap Training procedure is genuinely novel — using cross-sample representation recombination as a training signal to force disentanglement without requiring separated ground truth at the representation level. The key insight that structural bias (SOP for orthogonality) and training-time forcing (RST for semantic grounding) must work synergistically — neither alone achieves disentanglement, as definitively shown in Table 4 — is a meaningful contribution to the representation learning literature that may transfer to other disentanglement problems beyond audio.

## Suggestions
- Soften "we theoretically prove" in Section 3.6 to "we provide theoretical motivation" — the empirical evidence (Table 4) is strong enough to carry the disentanglement claim without overstating the informal reasoning.
- Add rate-matched comparisons or explicitly discuss why total bitrate is not the right comparison axis when encoding two functionally distinct streams.
- Consider enforcing P_S + P_N = I architecturally (e.g., P_N = I − P_S) to guarantee completeness and potentially recover the SDR-O gap observed in ablation.
- Report intrusive SE metrics on the simulated test set to complement DNSMOS.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to DeCodec |
|-------|------|-----------|-------|-----------------------|
| DM-Codec | UFwefiypla | 3.00 | R1 | Much weaker — incremental novelty, technical issues, monotonous experiments; DeCodec is substantially more novel |
| Parrot | 73EDGbG6mB | 3.00 | R1 | Different domain (spoken dialogue); weaker architectural contribution than DeCodec |
| Simple-TTS | m4mwbPjOwb | 3.00 | R1 | TTS system with limited novelty; DeCodec has more novel components |
| Blind Forward/Inverse Audio | mlPTNEIsgb | 3.25 | R1 | Different task; highly variable reviewer scores suggest uncertainty |
| Disentangling Textual/Acoustic | xJc3PazBwS | 3.75 | R1 | Similar disentanglement goal but weaker approach; DeCodec is more comprehensive |
| Universal Semantic Disentangled Privacy | Id2JMVSQHZ | 4.80 | R1 | Most similar — disentangled speech codec, but less novel architecture and weaker evaluation methodology than DeCodec |
| Codec-LM Co-design | KCVv3tICvp | 5.00 | R1 | Similar codec design space; DeCodec has more architectural novelty but comparable evaluation gaps |
| Vec-Tok Speech | C53xlgEqVh | 5.20 | R1 | Speech codec with vectors+tokens; similar scope, DeCodec has a more novel training procedure |
| GenSE | 1p6xFLBU4J | 6.00 | R1 | Accepted with similar novelty level; DeCodec has comparable or slightly more novelty but weaker evaluation rigor |
| HALL-E | 868masI331 | 6.40 | R1 | Higher quality evaluation and positioning; DeCodec has comparable novelty but less polished execution |
| CLaM-TTS | ofzeypWosV | 6.40 | R1 | Better evaluation with strong experimental design; DeCodec's evaluation has more gaps |
| FlowDec | uxDFlPGRLX | 7.00 | R1 | Stronger paper — rigorous evaluation, matched baselines, clear theoretical insights; DeCodec has more novelty but less evaluation rigor |

**Round 1 bracket: 5.0–6.5**

DeCodec is clearly above the 3-5 rejected papers (more novel architecture, better ablations, broader multi-task demonstration). It is comparable to the 5.5–6.5 range papers: it shares GenSE's novelty level but has evaluation gaps (bitrate unfairness, non-intrusive metrics only) and theoretical overclaiming that pull it slightly below clean borderline-accept papers. It is below FlowDec (7.0) which has more rigorous evaluation and better-matched comparisons.

**Narrowing to final score:** The paper has genuine novelty (RST is creative, the SOP+RST synergy is well-ablated, multi-task from single model is demonstrated). However, the unfair bitrate comparison in the primary codec table and the theoretical overclaiming are significant presentation/evaluation issues that reduce confidence. These are addressable in revision but currently undermine the paper's claims. The paper sits at the boundary between the 5.0 rejected papers (which typically lack novelty or have fundamental evaluation flaws) and the 6.0 accepted papers (which typically have cleaner evaluations).

**Final score: 5.5** — The core contribution (RST+SOP for audio disentanglement) is novel and well-ablated, but the evaluation shortcomings (bitrate mismatch, SE metrics, theoretical overclaiming) prevent confident acceptance in current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>