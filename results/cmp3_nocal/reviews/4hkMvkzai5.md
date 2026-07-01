## Summary

DeCodec rethinks the neural audio codec as a universal disentangled representation learner, proposing a codec architecture that decomposes mixed audio into orthogonal subspaces for speech and background sound (BGS), with further decomposition of speech into semantic and paralinguistic components. The two key technical innovations are a Subspace Orthogonal Projection (SOP) module that factorizes embeddings into orthogonal subspaces, and a Representation Swap Training (RST) procedure that enforces correspondence between subspaces and signal sources. Experiments demonstrate applications in speech enhancement, voice conversion, ASR, and TTS.

## Strengths

1. **Well-motivated problem (Section 1).** The paper correctly identifies that existing neural codecs either entangle everything (EnCodec, DAC) or handle only clean-speech disentanglement (SpeechTokenizer, FACodec). Real-world audio with mixed speech and background sound is an underexplored setting, and the paper's framing of a "universal disentangled representation learner" is a genuinely novel angle.

2. **Convincing ablation design (Table 4, Section 4.2.4).** The ablation cleanly demonstrates that neither SOP alone (Ablation-1: SDR-B = -13.15) nor RST alone (Ablation-2: SDR-B = -10.67) achieves meaningful decoupling, while their combination (Ablation-3: SDR-B = 0.49, SDR-S = 7.90) produces a clear jump. The SG ablation also shows the expected trade-off (slightly worse SDR, much lower downstream WER). This is the paper's strongest evidence that SOP and RST work synergistically.

3. **Strong background-sound suppression in SE (Table 2).** DeCodec achieves the highest BAK scores on both simulated (4.13) and real (3.99) recordings, outperforming dedicated SE models including SELM (4.10 / 3.44). This suggests representation-level decoupling enables genuinely cleaner background removal than end-to-end SE models.

## Weaknesses

### Fatal
None.

### Major

1. **Unfair reconstruction comparison (Table 1).** The paper evaluates baselines (EnCodec, HiFi-Codec, DAC, SpeechTokenizer) from official checkpoints — all trained on clean speech — against DeCodec, which is trained on ~700 hours of noisy speech (mixed with BGS at SNRs from -5 to 40 dB). On noisy test sets, DeCodec's advantage (e.g., SDR 5.21 vs EnCodec 4.88) reflects training data distribution mismatch more than architectural superiority. On clean speech, where the comparison is fairer, DeCodec (SDR 7.61) is comparable to EnCodec (6.86). To make the reconstruction comparison informative, the baselines would need to be retrained or fine-tuned on the same noisy mixture data, at matched bitrates. As presented, Table 1 should not be interpreted as "DeCodec outperforms prior codecs" — only that its reconstruction is adequate.

2. **Unsound theoretical proof (Section 3.6, Equations 13–16).** The paper attempts to prove that the RST procedure guarantees $\mathbf{Zs}$ contains no BGS information and $\mathbf{Zn}$ contains no speech information. This derivation has multiple gaps: (i) Subtracting outputs of a nonlinear decoder with RVQ does not give simple component subtraction ($\text{Dec}(\mathbf{Zs}_1+\mathbf{Zn}_2) - \text{Dec}(\mathbf{Zs}_1+\mathbf{Zn}_1) \approx \mathbf{n}_2 - \mathbf{n}_1$ in Eqn. 15 is unjustified — the decoder processes the sum as a single input, not as separable additive channels). (ii) The mean value theorem in the form used (Eqn. 16) does **not** hold for vector-valued functions $\mathbb{R}^n \to \mathbb{R}^m$ with $m>1$; the standard MVT asserts existence of a point with Jacobian times difference equaling the function difference only for scalar-valued functions. (iii) Even setting aside these issues, the conclusion that $\mathbf{Zs}_1$ must be independent of $\mathbf{n}_1$ does not follow from the stated premises. The paper should not claim a theoretical guarantee. The ablation study (Table 4) already provides sufficient *empirical* evidence that SOP+RST works — remove the attempted proof or rewrite it with correct mathematics.

3. **Overclaimed VC results (Table 3, Abstract).** The abstract and introduction claim "effective one-shot voice conversion on noisy speech." Table 3 reports WER of 50.46% (roughly half the words incorrect). While the paper acknowledges "relatively high WER" in the discussion and offers an explanation (voicing mismatch), this directly contradicts the "effective" framing. The claim should be corrected to reflect that VC is demonstrated in principle but not at a practically useful level.

### Minor

4. **DNSMOS-only SE evaluation (Table 2).** The speech enhancement evaluation relies entirely on DNSMOS, a non-intrusive perceptual estimator. The SE community standard includes intrusive metrics such as SI-SDR, PESQ, and STOI, which directly measure signal distortion and noise suppression. DNSMOS has known blind spots, and without corroborating metrics it is unclear whether DeCodec's competitive scores reflect genuinely better enhancement or a different artifact profile that DNSMOS happens to favor. Adding at least one intrusive objective metric would substantially strengthen the SE claims.

5. **No experimental comparison with UniCodec.** UniCodec (Jiang et al., 2025) is discussed at length in Related Work (Section 2) as the closest prior work in the "universal audio codec" space, and its specific limitation (classifying noisy speech as "sound") is correctly identified. Yet no experimental comparison against UniCodec is provided. Given that UniCodec is the most directly comparable approach, this is a missed opportunity to demonstrate DeCodec's advantage.

6. **Undiscussed reconstruction quality drop from decoupling (Table 4).** Ablation-1 (SOP only, no RST, no SG) achieves Overall SDR-O of 8.93 — substantially *higher* than the full DeCodec-c at 4.62 (a ~4 dB drop). The paper does not comment on this. It suggests that the decoupling mechanisms trade off raw reconstruction quality for disentanglement, which is expected, but the magnitude deserves discussion.

7. **Missing variance/confidence intervals (all tables).** No standard deviations, confidence intervals, or statistical significance tests are reported for any metric (SDR, WER, DNSMOS, SIM). Given known variability in audio metrics across different test samples, this is a noticeable omission.

### Trivial
None.

## Nice-to-Haves

- **Retrain baselines on matched training data** at matched bitrates for a fair reconstruction comparison.
- **Add SI-SDR and/or PESQ** to the SE evaluation to corroborate DNSMOS results.
- **Correct the VC framing** to report "preliminary feasibility" rather than "effective" conversion.
- **Add qualitative analysis** — such as a visualization showing that speech representations contain no BGS information and vice versa — to strengthen the decoupling claim beyond aggregate metrics.

## Removed Points

These points were flagged for removal and should be treated with caution:

1. **"Mel distance framing is misleading"** — Removed. The paper says DeCodec is "second only to DAC" on mel distance. This is factually correct: on the noisy set DAC=0.69, DeCodec=0.81/0.82, and all other baselines are ≥0.84. The critic misread the claim.
2. **"Introduction claim (1) about signal integrity"** — Removed. The claim is about avoiding front-end separation distortion *relative to cascaded pipelines*, not about achieving perfect reconstruction. Quantization distortion is a separate and expected trade-off.
3. **"SG training requires clean speech"** — Removed. This is explicitly stated as a supervised training design; it is not a flaw.
4. **"Limitations appendix not accessible"** — Removed. The parser strips appendix content; the original submission contains this.
5. **"Missing qualitative analysis"** — Moved to Nice-to-Haves.
6. **"Bitrate mismatch" framing as structurally fatal** — Demoted. Bitrate differences (DeCodec 8.0 kbps vs baselines 2.0–6.0 kbps) compound the comparison problem but do not independently invalidate results, since part of DeCodec's bitrate is dedicated to BGS encoding that baselines do not provide. Merged into weakness #1 above.

## Novel Insights

The harsh critic's most novel observation is that the attempted theoretical proof in Section 3.6 is mathematically unsound in a way that goes beyond imprecise writing — the standard mean value theorem does not apply to vector-valued functions in the form used, making the claimed guarantee spurious. The critic also correctly identifies that the ablation study's most striking result (SOP-only achieving much higher SDR-O than the full model) is left undiscussed, which is a missed opportunity for intellectual honesty about the quality-disentanglement trade-off. None beyond the paper's own contributions.

## Suggestions

1. Remove the attempted theoretical proof in Section 3.6 (Equations 13–16) or substantially rewrite it with correct vector calculus. The ablation study already provides sufficient empirical support for the method.
2. Retrain (or at minimum fine-tune) the baseline codecs on the same noisy mixture data used for DeCodec, at matched total bitrates, to make Table 1 informative.
3. Add at least one intrusive SE metric (SI-SDR or PESQ) to Table 2.
4. Correct the VC claim in the abstract/introduction to describe the result as "preliminary" or "feasibility demonstration" rather than "effective."
5. Discuss the SDR-O drop between Ablation-1 and the full DeCodec in the ablation analysis.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>