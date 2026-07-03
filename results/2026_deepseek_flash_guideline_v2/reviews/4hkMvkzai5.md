Now I have all the cross-verification I need. Let me produce the final review.

## Summary

DeCodec proposes a neural audio codec that learns to disentangle speech and background sound (BGS) in the latent space via a subspace orthogonal projection (SOP) module and a representation swap training (RST) procedure. Within the speech subspace, semantic guidance (SG) further decomposes speech into semantic and paralinguistic components. This hierarchical disentanglement is designed to let a single codec serve multiple downstream tasks (reconstruction, speech enhancement, voice conversion, ASR, TTS) by selecting the appropriate latent subspace components.

## Strengths

1. **Ablation study provides causal evidence that both SOP and RST are jointly necessary for decoupling (Table 4).** SDR-B (BGS extracted from the BGS stream) jumps from −13.15 dB (SOP-only) and −10.67 dB (RST-only) to 0.49 dB (SOP+RST). SDR-S (speech from the speech stream) jumps from −1.91/3.03 to 7.90 dB. This controlled experiment isolates the contribution of each component and convincingly shows neither works alone.

2. **DeCodec achieves competitive or superior DNSMOS scores vs. dedicated speech enhancement models (Table 2).** As a codec operating at 8 kbps, it outperforms Inter-SubNet, StoRM, and SELM on OVL (3.39 vs. 3.26) and BAK (4.13 vs. 4.10) on the DNS Challenge without-reverb set, with similar results on real recordings. This demonstrates that decoupling in the representation domain enables controllable background-sound suppression that is competitive with purpose-built SE methods.

3. **One-shot VC on noisy speech succeeds where prior speech decomposition codecs collapse (Table 3).** SpeechTokenizer applied to noisy speech yields WER = 74.18% (essentially unintelligible), while DeCodec achieves WER = 50.46% and SIM = 0.83, matching the cascaded StoRM-SpeechTokenizer pipeline (WER = 52.73%) without requiring a separate denoising front-end. This demonstrates noise-robust semantic/paralinguistic decomposition that prior speech tokenizers explicitly lack.

4. **Causal variant maintains competitive performance.** DeCodec-c (causal) achieves SDR = 4.62 on noisy speech (Table 1), DNSMOS OVL = 3.31/2.99 (Table 2), and BAK = 4.09/3.94 — all while being causal, which is practically relevant for real-time applications.

## Weaknesses

### Fatal

None.

### Major

1. **Reconstruction comparison is confounded by bitrate disparity (Table 1).** DeCodec operates at 8.0 kbps (4.0+4.0) while baselines use 2.0–6.0 kbps. The paper states that "the proposed DeCodec achieves the highest SDR for speech reconstruction" without any qualification about the bitrate difference. Against EnCodec (6.0 kbps, 33% lower), the SDR margin is only 0.75 dB on clean speech and 0.33 dB on noisy speech — underwhelming given the bitrate advantage. Without a controlled comparison at matched bitrate, the claim of superior reconstruction is not supported as stated.

2. **The theoretical proof in Section 3.6 is not rigorous and overclaimed.** The paper claims to "theoretically prove" that the RST loss forces Zs to contain only speech information and Zn to contain only BGS information. The proof (Equations 13–16) has several gaps: (a) the mean value theorem for vector-valued functions does not straightforwardly yield the claimed form; (b) the straight-through gradient estimators used for RVQ break differentiability, invalidating the Jacobian argument; (c) the crucial inference that "Zs₁ must be independent of n₁" does not follow because ξ (where the Jacobian is evaluated) depends on Zs₁ through the decoder's nonlinearity; (d) the proof treats minimized loss approximations as exact equalities. The paper would be better served presenting this as intuition rather than a formal guarantee.

3. **Decoupling quality for background sound is marginal.** SDR-B (BGS extracted from the BGS stream) is −0.36 dB for the full non-causal model and −1.11 dB for the causal version (Table 4). An SDR below 0 dB means the error exceeds the signal power — the "decoupled" background sound is barely above chance. Even Ablation-3 (SOP+RST, no SG) only achieves SDR-B = 0.49 dB. While SDR-S (speech from speech stream) at 6.73–7.90 dB is reasonable, this asymmetry suggests the BGS subspace captures limited useful content. The paper also reports no direct information-leakage metric (e.g., mutual information between subspaces or a probe classifier to predict BGS category from the speech stream). The downstream task results are encouraging but do not substitute for a direct decoupling measurement.

4. **Training data distribution mismatch advantages DeCodec in head-to-head comparisons.** DeCodec is trained on ~700h of speech mixed with BGS at random SNRs (−5 to 40 dB), while baselines (EnCodec, DAC, HiFi-Codec, SpeechTokenizer) are evaluated from their official pretrained checkpoints, which were trained on very different distributions (typically clean speech or general audio at scale). On noisy speech, these baselines are at a natural disadvantage that has nothing to do with the presence or absence of disentanglement. A controlled comparison would at minimum fine-tune the baselines on the same noisy training set or report DeCodec's performance when trained on clean data.

### Minor

5. **Encoder architecture is ambiguous.** Section 3.4 says "two trainable linear projection layers **followed by the encoder**" (singular), suggesting one shared encoder with two linear projections. However, the Figure 2 caption says "The input y is split into **two encoders (Enc)** to produce Yl and Yr." If two full encoders are used, this doubles encoder parameters relative to baselines — a significant computational cost that goes unmentioned and uncompared.

6. **UniCodec is discussed as closely related but never evaluated as a baseline.** The Introduction and Related Work sections critique UniCodec for failing to decouple noisy speech, yet UniCodec is absent from all experimental tables (1–4). Given that it is the closest existing work in terms of domain-aware coding, this is a noticeable gap.

7. **VC results show high absolute WER (50.46%) with marginal improvement.** Half of all words are incorrect, and the improvement over StoRM-SpeechTokenizer is only 2.27 percentage points. The SIM scores are identical (0.83). The paper acknowledges the high WER but does not establish practical significance at these error rates.

8. **The ablation reveals a clear fidelity-decoupling tradeoff that is not discussed.** Ablation-1 (SOP only) achieves SDR-O = 8.93 dB — *higher* than the full model's 4.62–5.21 dB. The disentanglement mechanisms cost a 30–50% reconstruction SDR drop. The paper presents this as a minor side effect rather than characterizing the tradeoff directly.

### Trivial

None.

## Nice-to-Haves

- Report reconstruction performance at a matched total bitrate (e.g., 6.0 kbps) to enable a fair comparison with EnCodec.
- Add direct information-leakage metrics: train a classifier to predict the BGS category (e.g., from ESC-50) using only the speech subspace representation Zs, and vice versa.
- Report parameter counts, FLOPs, and latency for DeCodec and all baselines — these are standard for codec papers.
- Specify K_s and K_n (number of RVQ layers for each stream) explicitly in the main text.
- Include UniCodec as a baseline, or explain why it was excluded.

## Removed Points

These points were flagged for removal; treat with caution:

- **"DAC's SDR is implausibly low"** — The paper uses official checkpoints; the low SDR is attributable to distribution shift (clean-trained model on noisy speech), not an evaluation error. Merged into Weakness 4.
- **"RST's uncorrelated requirement is underspecified"** — Random batching with random SNR mixing makes this a practical non-issue. Too minor to retain.
- **"Orthogonality does not guarantee independence"** — This is a known limitation of all orthogonal projection approaches and is not specific to this paper.
- **"Missing training details (loss weights, optimizer, K_s/K_n)"** — The appendix was stripped during ingestion; per protocol, criticisms of content that may reside in the stripped appendix are removed.
- **"Missing model size and compute"** — A legitimate omission but may be in the appendix; demoted to nice-to-have.
- **"SE comparison is apples-to-oranges"** — The comparison is interesting precisely because DeCodec is a codec performing SE as a byproduct; this is a feature, not a flaw.

## Novel Insights

None beyond the paper's own contributions. The joint SOP+RST approach for forcing subspace specialization in a codec latent space is the paper's genuine technical contribution, but the reviews do not surface a deeper insight not already articulated in the paper.

## Suggestions

1. **Run a controlled reconstruction experiment at matched bitrate.** Train a version of DeCodec at ~6.0 kbps total by reducing RVQ layers, and compare directly with EnCodec. If disentanglement overhead forces a fidelity drop, report it transparently.
2. **Directly probe the subspaces for information leakage.** Train a classifier to predict the BGS category (from ESC-50) given only Zs, and a classifier to predict speech content given only Zn. Chance-level performance would be far more convincing than the current evidence chain.
3. **Clarify the encoder architecture.** State whether one or two encoders are used, and if two, report the parameter count impact.
4. **Characterize the fidelity-decoupling tradeoff explicitly.** The ablation data shows a clear tradeoff; discussing it directly would strengthen rather than weaken the paper.
5. **Add UniCodec to the experimental comparison** or explain its omission given the extensive discussion of it.

## Score and Decision

The paper tackles a genuinely interesting problem — learning a codec whose latent space separates speech from background sound for flexible downstream use. The SOP+RST combination is a novel architectural contribution, and the ablation study convincingly demonstrates that both components are necessary. The downstream SE and VC results are interesting demonstrations of the utility of this disentanglement.

However, the paper's claims substantially outrun its evidence in several respects. The reconstruction comparison is unfair (2–4× bitrate advantage for DeCodec). The theoretical "proof" is not rigorous. The BGS decoupling metrics are marginal (SDR-B near or below 0 dB). The baselines are evaluated in settings that systematically disadvantage them due to training data mismatch. These are real problems, but they do not invalidate the core contribution — they instead call for more careful, controlled evaluation.

The core idea is novel and the ablation evidence for the joint SOP+RST design is solid. With the controlled experiments suggested above, the paper could be significantly strengthened. As it stands, the contribution is real but the evidence is not yet commensurate with the strength of the claims.

**Score: 5.5** — borderline accept. The paper has a genuine technical contribution that advances the state of the art in codec-based disentanglement, but the evaluation has significant confounds and overclaims that prevent it from being a clear accept.

**Decision: Accept**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>