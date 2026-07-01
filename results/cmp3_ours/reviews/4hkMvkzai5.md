Now let me write the final consolidated review.

## Summary

The paper proposes DeCodec, a neural audio codec that learns hierarchically disentangled representations of speech and background sound (and within speech, semantic vs. paralinguistic components) via subspace orthogonal projection (SOP), representation swap training (RST), and semantic guidance (SG). Evaluated on reconstruction, speech enhancement, and one-shot voice conversion, DeCodec shows competitive SE performance and ablation evidence supporting its core decoupling mechanism.

## Strengths

1. **Ablation study (Table 4) convincingly demonstrates the necessity of joint SOP+RST design.** Ablation-1 (SOP only) and Ablation-2 (RST only) both yield decoupling SDRs below –10 dB (SDR-B) and near-zero SDR-S, while Ablation-3 (SOP+RST) jumps to SDR-B=0.49, SDR-S=7.90. This cleanly shows the two components are synergistic, not redundant, and provides strong empirical evidence for the core technical claim. This is the strongest evidence in the paper.

2. **Speech enhancement results (Table 2) are genuinely competitive with dedicated SE models.** DeCodec achieves the highest BAK scores on both simulated (4.13) and real-recordings (3.99) test sets, and the highest OVL (3.39, 3.13). That a codec model — simultaneously doing quantization, reconstruction, and representation learning — matches or exceeds discriminative and diffusion-based SE models is a notable and surprising result.

3. **Well-grounded problem and biologically-motivated architecture.** The paper identifies a genuine limitation of monolithic codecs for mixed speech+noise signals and builds on a compelling biological analogy (A2 cortical region) that directly informs the architecture rather than being decorative.

## Weaknesses

### Fatal
None.

### Major

1. **The reconstruction comparison (Table 1) is confounded by bitrate mismatch and anomalously low baseline SDR values.** DeCodec operates at 4.0+4.0 = 8.0 kbps while baselines use 2.0–6.0 kbps. Higher bitrate directly benefits SDR regardless of disentanglement, so the comparison does not support the claim that "DeCodec maintains advanced signal reconstruction" while adding disentanglement. Additionally, DAC reports SDR=0.60 on clean speech, far below published DAC results (~8 dB at 3 kbps), suggesting either a test-set mismatch, incorrect checkpoint configuration, or a systematic metric issue. A matched-bitrate comparison (e.g., DeCodec with only the speech branch at 4.0 kbps vs. DAC at a comparable rate) is necessary before the reconstruction claim can be evaluated.

2. **The one-shot VC results (Table 3) do not support the claim of "effective" voice conversion in the abstract and conclusion.** The best WER is 50.46% — approximately every other word is incorrect. Even the cascaded baseline (StoRM-SpeechTokenizer) achieves 52.73% WER. The improvement over baseline is marginal (2.27 percentage points), and both are far from usable. The paper acknowledges the high WER in the text but does not temper the broad claim made in the abstract.

### Minor

3. **The attempted "theoretical proof" of RST decoupling (Section 3.6, Eqs. 13–16) is not mathematically valid.** The mean value theorem for vector-valued functions yields an inequality, not the equality used in Eq. (16). Furthermore, the conclusion — that "Zs₁ must be independent of n₁" — does not follow from the equations presented; the decoder could depend on Zs₁ in ways that make the approximation hold for training data without implying formal independence. The paper calls this a "proof" (line 138), which overstates its rigor. The empirical ablation evidence is sufficient on its own; this section should be reframed as intuition.

4. **The "angular matrix" discussion in Section 3.4 (Eq. 6) uses undefined terminology.** "Angular matrix" is not a standard term and is never defined. The claim that "different feature channels being mutually independent" follows from the encoder design is unsubstantiated. The L_perp loss (Eq. 5) is a sufficient soft constraint; the mathematical development around Eq. (6) obfuscates rather than clarifies.

5. **Ablation-1 (SOP only) achieves higher overall SDR-O (8.93) than the full DeCodec-c (4.62), a near-halving of reconstruction quality.** The paper does not discuss why adding RST and SG reduces reconstruction quality so substantially. This trade-off (cross-sample constraints for disentanglement at the cost of fidelity) should be explicitly acknowledged.

6. **No statistical significance reported for DNSMOS scores (Table 2).** The DNSMOS comparison lacks confidence intervals or significance tests, making it unclear whether the reported advantages over baselines are meaningful.

### Trivial
None.

## Nice-to-Haves
- Compare DeCodec's decoupling quality (SDR-B, SDR-S) against a dedicated speech separation model (e.g., Conv-TasNet) to contextualize the trade-off between representation-domain and time-domain decoupling.
- Report model size, FLOPs, and latency, since the paper proposes DeCodec as a "universal front-end" where efficiency matters.
- Evaluate extracted background sound quality from the BRVQ output, not just speech enhancement (which only tests one direction of the decoupling).

## Removed Points
- **ASR/TTS results in missing appendix:** Per policy, appendix sections are stripped by the parser and exist in the original submission; this cannot be evaluated from the reviewed version.
- **UniCodec characterization as "dismissive":** A subjective opinion about positioning, not a factual error.
- **Lack of speech separation baselines:** A scope-expansion suggestion; the paper already compares to SE models, and SS comparisons would be a nice addition but not a missing requirement.
- **Computational cost not discussed:** Minor omission that doesn't affect core claims; moved to Nice-to-Haves.
- **Request for matched-bitrate DeCodec (4.0+0.0) vs. DAC 4.0:** Subsumed by Major weakness #1 (bitrate confound); the matched experiment is a reasonable request, not a separate weakness.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Fix the reconstruction evaluation.** Run matched-bitrate experiments (e.g., DeCodec speech-branch-only at 4.0 kbps vs. DAC at 4.0 kbps; DeCodec full at 8.0 kbps vs. a DAC or EnCodec variant at 8.0 kbps). Verify DAC SDR values using the official checkpoint under identical conditions.
2. **Reframe or remove the "proof" in Section 3.6.** The ablation study already provides sufficient evidence; present the RST argument as intuition or motivation.
3. **Tone down the VC claim.** Replace "effective one-shot voice conversion" with a description that honestly reflects the 50% WER, and add analysis diagnosing the failure modes (is it semantic content, paralinguistic transfer, or both?).
4. **Define "angular matrix" or remove that discussion.** The L_perp loss stands on its own.
5. **Discuss the SDR-O drop from Ablation-1 (8.93) to full DeCodec-c (4.62) explicitly**, acknowledging the fidelity-disentanglement trade-off.

## Score and Decision

**Calibration anchors (retrieved from /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/):**
- **DM-Codec** (avg 3.00, reject): Speech tokenization via distillation; incremental over SpeechTokenizer, technical issues. *DeCodec has a more novel technical contribution (SOP+RST is genuinely new) and stronger ablation evidence.*
- **Universal Semantic Disentangled Privacy-preserving Speech Representation Learning** (avg 4.80, reject): Codec-based disentanglement for speaker privacy. Shared weaknesses (missing baselines, claim overreach). *DeCodec has stronger ablation evidence and competitive SE results, placing it slightly higher.*
- **Vec-Tok Speech** (avg 5.20, reject): Speech codec with semantic/acoustic tokens + LM. Stronger downstream evaluation. *DeCodec is weaker in terms of downstream integration and VC quality.*
- **FlowDec** (avg 7.00, accept): Full-band audio codec with flow matching, no disentanglement. *Different focus; not directly comparable but demonstrates the score level for a clean, well-evaluated codec paper.*

**Round-1 bracket:** 4.0 – 5.5.
**Final assessment:** The paper has a genuine technical contribution (SOP+RST validated by a clean ablation) and surprisingly competitive SE results. However, the reconstruction comparison is confounded by bitrate mismatch, the VC results are overclaimed, and a flawed "proof" is presented as rigorous. These issues are addressable but limit the paper in its current form.

**Calibrated score: 5.0.** This reflects a borderline paper with solid core ideas and one strong result (SE) but evaluation weaknesses that prevent clear acceptance. The paper sits between the 4.80 and 5.20 anchors: above Universal Semantic Disentangled due to better empirical support for the core technical innovation, but below Vec-Tok Speech due to weaker downstream evaluation and overstated claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>