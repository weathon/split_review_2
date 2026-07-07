Now I have enough to draft the review. Let me proceed.## Summary
DeCodec proposes a neural audio codec that decouples mixed-audio representations into orthogonal subspaces for speech and background sound, then further decomposes speech into semantic and paralinguistic components. The two technical innovations are a Subspace Orthogonal Projection (SOP) module and a Representation Swap Training (RST) procedure, enabling the codec to serve as a universal front-end for speech enhancement, voice conversion, ASR, and TTS tasks simultaneously.

## Strengths
- **RST procedure is genuinely novel and principled**: Taking two mixed samples (y₁₁=s₁+n₁, y₂₂=s₂+n₂), swapping background representations, and supervising the decoder to produce s₁+n₂ creates an elegant implicit test for disentanglement — any leakage of n₁ information into Zs₁ would directly increase the RST loss when n₂≠n₁. No adversarial component is needed.
- **Ablation in Table 4 is informative and demonstrates genuine synergy**: SOP alone yields SDR-B of −13.15 dB, RST alone yields −10.67 dB, while SOP+RST jointly achieves +0.49 dB — a non-linear improvement that establishes neither component alone is sufficient.
- **SE results (Table 2) are competitive with specialized models**: DeCodec achieves the highest OVL, SIG, and BAK on the DNS "without reverb" test, and highest OVL and BAK on real recordings, outperforming dedicated SE models (InterSubNet, StoRM, SELM) while operating as a general-purpose codec.

## Weaknesses

### Fatal
None.

### Major
- **Bitrate inequality in Table 1 renders the reconstruction headline misleading**: DeCodec uses 4.0+4.0 = 8.0 kbps (two parallel RVQ streams) while the strongest baselines operate at 6.0 kbps (EnCodec) and 4.5 kbps (DAC). DeCodec claims the highest SDR on both clean and noisy speech in this table, but at nearly twice DAC's bitrate, this comparison cannot answer the relevant question: does disentanglement impose a reconstruction cost at matched bitrate? The paper does not acknowledge the disparity anywhere. A fair comparison would include baselines at 8 kbps, or a DeCodec variant at 4–5 kbps total.

- **The "theoretical proof" in Section 3.6 does not establish its conclusion**: After deriving Equation (16) via the mean value theorem, the paper asserts: "The left side depends on Zs₁ through ξ, while the right side is independent of Zs₁. Therefore, for consistency ∀n₁,n₂, Zs₁ must be independent of n₁." This is a non-sequitur — consistency of an equation does not imply independence of its components. The conclusion does not follow from the premises as stated. The RST procedure has strong empirical and intuitive justification; this proof should be replaced with a properly stated formal result (with explicit assumptions) or presented as informal motivation rather than a theorem.

### Minor
- **SE baseline comparison involves unacknowledged training-distribution mismatch**: SE baselines are taken "from the paper" (Section 4.1, footnote), trained specifically on DNS Challenge data. DeCodec is trained on a heterogeneous mix (LibriTTS, VCTK, AISHELL3, ESC-50, DNS-Noise). This difference should be acknowledged rather than presenting the comparison as fully matched.

- **SOP orthogonality guarantee relies on an unverified assumption**: Section 3.4 states that Pₛ Pₙᵀ = 0 follows "when the covariance matrix YYᵀ satisfies the angular matrix" (feature channels mutually independent). This condition is an assumption, not enforced or empirically verified, and the paper does not discuss performance implications when it is only approximately satisfied.

- **Paired clean/noisy training data requirement for SG is not acknowledged**: Equation (7) computes H as the HuBERT-L9 representation of "corresponding clean speech s" — requiring paired training data. This limits flexibility in purely unsupervised or in-the-wild training scenarios and should be disclosed.

- **VC superiority over StoRM-SpeechTokenizer is not robustly established**: WER difference of 50.46 vs. 52.73 (~2.3 points) on a task where both systems produce >50% WER is presented as evidence that "representation-domain decoupling introduces less error" without statistical testing. The comparison to plain SpeechTokenizer (WER 74.18) is valid; the pairwise advantage over StoRM-SpeechTokenizer is insufficiently supported at this margin.

### Trivial
None.

## Nice-to-Haves
- A direct disentanglement metric (e.g., a classifier's accuracy at predicting background category from Zs alone, or mutual information between Zs and the background sound) would independently validate the "orthogonal subspaces" claim without relying on downstream task proxies.
- An audio quality evaluation of the isolated background-sound stream (BRVQ output) — not just SE performance on the combined signal — would directly validate the disentanglement claim.
- Reporting VC results with multiple target speakers and mean ± std would enable the StoRM-SpeechTokenizer comparison to be stated with appropriate confidence.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **"First time" framing concern**: Reviewer noted that representation-domain speech separation exists in AV-sep and other works. Removed — we cannot confirm existence of external works, and the codec formulation of the problem appears novel in its own right.
- **Music/soundscape generalization**: Reviewer suggested testing on music-mixed-with-speech. Removed as scope creep — the paper explicitly targets speech + background sound (noise).
- **Strength about "important problem"**: The generic framing "this addresses an important gap" is removed per filtering discipline; strengths retained only where backed by concrete evidence from the paper.

## Novel Insights
The RST procedure reveals an important design principle: architectural constraints on representation structure (like SOP's orthogonal projection) are insufficient to direct *which* subspace carries *which* audio modality — an explicit cross-sample training signal (RST) is needed to assign semantic identity to each subspace. The ablation (Table 4) provides clean empirical evidence for this interaction. This suggests a general recipe for latent-space disentanglement: (1) constrain geometry via an orthogonality loss, and (2) use a swap-based training objective to assign modality roles to the constrained subspaces. This pairing of architectural constraint + curriculum-style training signal is underexplored and could transfer to other multimodal disentanglement problems.

## Suggestions
- Add a Table 1 row for DAC/EnCodec at 8 kbps, or train a DeCodec variant at 4–5 kbps total, and add a one-paragraph discussion of the bandwidth-disentanglement trade-off.
- Replace Section 3.6's "proof" with clearly labeled intuition or informal motivation, or add a formal lemma with explicit assumptions about Dec's differentiability and the Jacobian structure.
- Add a sentence in Section 3.5 acknowledging that SG training requires paired clean/noisy speech.
- Report VC WER as "comparable to StoRM-SpeechTokenizer" rather than claiming directional superiority at the ~2-point margin.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| UFwefiypla (DM-Codec) | 3.00 | R1 | Speech tokenization with multimodal representations; weaker novelty, more limited evaluation |
| KCVv3tICvp (Codec-LM Co-design) | 5.00 | R1 | Codec + LM co-design; incremental rather than novel disentanglement |
| Id2JMVSQHZ (USC disentangled) | 4.80 | R1/R2 | Speaker-disentangled speech codec; narrower scope, clean speech only |
| C53xlgEqVh (Vec-Tok Speech) | 5.20 | R1/R2 | Speech vectorization with semantic/acoustic decomposition; narrower |
| 1p6xFLBU4J (GenSE) | 6.00 | R1/R2 | Generative SE via LMs; comparable novelty level, cleaner evaluation |
| uxDFlPGRLX (FlowDec) | 7.00 | R1 | Neural audio codec with flow postfilter; strong theory, matched bitrate comparisons |
| ale56Ya59q (VQScore SE) | 7.00 | R1 | VQ-based speech quality/SE; more rigorous evaluation |
| LfDUzzQa3g (RepCodec) | 5.50 | R2 | Speech representation codec; narrower scope |
| OW332Wh9S5 (DC-Spin) | 4.75 | R2 | Speaker-invariant tokenizer; narrower scope |
| TtKN1TpvUu (T2V2) | 6.25 | R2 | Unified ASR+TTS model; comparable multi-task scope |
| yj9lLwMjnE (UniWav) | 6.00 | R2 | Unified pre-training for speech; comparable scope |
| jDy2Djjrge (LauraGPT) | 5.50 | R2 | Audio LLM; multi-task but incremental |

**Round 1 bracket**: 5.0 – 6.5. Papers at 5 (codec-LM, disentangled codec) are narrower and more incremental. Papers at 6–7 (GenSE, FlowDec, UniWav) have comparable scope but cleaner evaluations and tighter methodology.

**Round 2 narrowing**: DeCodec has genuine novelty in the RST+SOP combination (clearly above the 5.0 cluster) and competitive multi-task results. However, the misleading Table 1 comparison (bitrate disparity unacknowledged) and invalid proof in Section 3.6 are real methodological problems that prevent it from reaching the 6.5–7 tier occupied by FlowDec or VQScore. The core contribution is sound but the evaluation design has a structural gap that would need to be addressed. Calibrating at **5.5** — above borderline-reject papers that lack novelty, below clean-accept papers with rigorous evaluations.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>