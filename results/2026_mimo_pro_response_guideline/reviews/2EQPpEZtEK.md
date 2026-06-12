Now I have enough calibration data. Let me finalize the review.

**Round 1 Bracket:** 6.0–7.0. DiSTAR is clearly stronger than MaskGCT (5.25, Accept), DiffAR (5.75, Accept), and VALL-E 2 (5.0, Reject), and comparable to CLaM-TTS (6.4), HALL-E (6.4), and DiTTo-TTS (6.25).

**Round 2 Narrowing:** The 5.5–7.0 range anchors confirm DiSTAR sits near the top of this band. Its WER results are stronger than all the 6.x anchors, its architecture is more novel, and it has more comprehensive ablations. However, the two major weaknesses (no efficiency data despite claims, codec confound) prevent it from reaching 7+. Final score: **6.5**.

---

## Summary

DiSTAR is a zero-shot TTS framework that couples an autoregressive patch-level language model with a masked diffusion model, operating entirely in discrete RVQ code space. It eliminates forced alignment and duration predictors, achieves state-of-the-art WER on LibriSpeech-PC and Seed-TTS benchmarks, and supports test-time variable bitrate via RVQ layer pruning.

## Strengths

- **Best WER across both benchmarks (Table 1):** DiSTAR-medium (0.3B) achieves 1.66% WER on LibriSpeech-PC (vs. 2.02% F5TTS, 2.39% DiTAR) and 1.32% on Seed-TTS test-en (vs. 1.35% F5TTS, 1.78% DiTAR), with consistent margins. The 0.15B base model already outperforms several larger baselines.

- **Strong subjective evaluation (Table 2):** Highest CMOS (0.22±0.13) and SMOS (3.31±0.25) on Seed-TTS test-en, indicating best naturalness and speaker similarity among compared systems. The CMOS advantage over F5TTS (0.01±0.12) is practically meaningful.

- **Test-time variable bitrate/compute via RVQ layer pruning (Figure 2, Section 3.4):** Stochastic layer truncation training enables smooth quality–compute tradeoff at inference by pruning upper RVQ layers without retraining—a practical capability absent from most prior TTS systems.

- **Novel architectural combination with clear advantages:** The AR drafting + masked diffusion infilling decomposition in discrete space is well-motivated (Section 3.1.1) and supported by results: DiSTAR-medium at 0.3B outperforms DiTAR at 0.6B on WER at half the parameter count, suggesting the discrete code space avoids optimization fragility of continuous-latent systems.

- **Effective decoding strategy design and ablation (Table 3, Section 3.4):** The identification of the "tail-first bias" artifact and its three targeted mitigations (layer-wise/position-wise temperature shaping, hybrid sampling) is a genuinely useful contribution, reducing WER from 2.11 to 1.91 while improving speaker similarity.

- **No duration predictor or forced alignment needed (Section 3.1.2):** The discrete EOS token enables natural termination, simplifying the pipeline relative to systems like DiTAR and CosyVoice.

## Weaknesses

### Fatal
None.

### Major
- **Unsubstantiated efficiency claim:** The abstract claims "comparable or lower computational cost" (line 37) and Section 4.4 is titled "Inference Efficiency and Controllability," yet no wall-clock inference time, FLOPs, or real-time factor is reported for any system. The paper uses NFE counts as a proxy (24 vs. 32 vs. 10), but per-step costs differ substantially: DiSTAR's NFE=24 involves bidirectional Transformer diffusion passes plus AR module forward passes, while F5TTS's NFE=32 operates over lighter continuous features. Section 4.4 only reports Figure 2 on RVQ layer pruning—which demonstrates controllability, not efficiency. This gap is the paper's most significant weakness because an entire section is devoted to a claim that has no direct evidence.

- **Custom RVQ codec confounds attribution of gains:** DiSTAR uses a bespoke ~0.3B-parameter Transformer-based streaming RVQ codec (9 stages, 65K codebooks) built on MAGICODEC (Section 3.5.1). The "RVQ resynthesized" row in Table 1 (WER 1.83, SIM 0.66 on LibriSpeech) shows this codec nearly matches human quality on its own. Baselines use different codecs or continuous representations. Without an ablation evaluating DiSTAR's generator atop an off-the-shelf codec or a baseline atop DiSTAR's codec, it is unclear how much of the 0.36pp WER improvement over F5TTS reflects the generator architecture versus the codec quality.

### Minor
- **Subjective evaluation confidence intervals overlap:** SMOS for DiSTAR (3.31±0.25) and E2TTS (3.29±0.19) overlap substantially. CMOS for DiSTAR (0.22±0.13) vs. F5TTS (0.01±0.12) has slight boundary overlap (0.09 vs. 0.13). The objective WER results are unambiguous; the subjective results are suggestive but the paper presents them as definitive SOTA without acknowledging overlap.

- **Unsupported diversity claim:** The abstract claims "maintaining rich output diversity" but no diversity metrics (e.g., multi-sample embedding variance, inter-utterance similarity, mode coverage) are reported.

- **Scaling trajectory claim rests on two data points:** Table 1 shows only base (0.15B) and medium (0.3B). Claiming a "healthy scaling trajectory" from two model sizes over a narrow parameter range is premature.

- **DiTAR not re-evaluated under controlled conditions:** DiTAR numbers are marked ♦ as "reported in DiTAR paper" (Table 1), meaning different evaluation setups. As the closest prior work (AR+diffusion over continuous latents), a controlled comparison would be more convincing.

### Trivial
None.

## Nice-to-Haves
- Report inference latency (seconds per utterance) for DiSTAR, F5TTS, and DiTAR on the same hardware.
- Add an ablation isolating the AR+diffusion decomposition: pure AR vs. pure masked diffusion vs. AR+diffusion over the same RVQ codes and codec.
- Report subjective evaluation on LibriSpeech-PC in addition to Seed-TTS.
- Ablate the overlapping patch mechanism: the default uses S=P=8, so the overlap feature is declared but not demonstrated.
- Report bootstrap confidence intervals for objective metrics on finite test sets.

## Removed Points
These points are flagged to be removed, treat them with caution.
- "Many inference knobs" — The paper is transparent about hyperparameters (temperature, top-k, top-p, CFG); these are standard in the field.
- "Training data not matched across baselines" — Standard practice; DiSTAR is trained on Emilia, baselines use public checkpoints.
- "No variance for objective metrics" — Nice-to-have, common in TTS literature.
- "Missing related works" — Cannot verify external references; removed per policy.

## Novel Insights
The paper's key insight is that operating entirely in discrete RVQ code space with an AR+diffusion decomposition avoids the optimization fragility of continuous-latent systems while retaining patch-level parallelism. The "tail-first bias" observation—where non-autoregressive training causes overconfidence at later patch positions—and its mitigation through layer-wise and position-wise temperature shaping is a genuinely useful contribution for practitioners deploying masked diffusion models.

## Suggestions
- Add a table reporting wall-clock inference time and/or real-time factor for DiSTAR and at least F5TTS and DiTAR on the same hardware. This directly substantiates the efficiency claim and takes one table.
- Add one controlled ablation isolating the contribution of the custom RVQ codec: evaluate DiSTAR's generator on an off-the-shelf codec or a baseline generator on DiSTAR's codec.
- Either add diversity metrics or soften the "rich output diversity" claim in the abstract.
- Expand the scaling analysis beyond two model sizes.

## Reporting — All Retrieved Anchors

| Anchor Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| gwZ90hFSL2 (Humanoid robots / Chinese NLP) | 1.00 | 1 | Irrelevant topic, far below DiSTAR |
| Uj0h13lVrR (GFlowNets KL divergence) | 1.00 | 1 | Fundamentally flawed paper, far below |
| 5lUdTogEL3 (Lifelong person re-ID) | 1.00 | 1 | Flawed paper, far below |
| u1cQYxRI1H (Diffusion illumination harmonization) | 0.50 | 1 | Outlier; actually scores 10 but retrieval mismatch |
| m4mwbPjOwb (Simple-TTS) | 3.00 | 1 | Simpler latent diffusion TTS, much weaker results |
| UFwefiypla (DM-Codec) | 3.00 | 1 | Speech tokenization, weaker contribution |
| pWdkM9NNCA (Fox-TTS) | 3.00 | 1 | Zero-shot TTS, weaker results |
| vK8C37eHXM (Sample what you can't compress) | 3.20 | 1 | Different domain (image compression) |
| ExuBFYtCQU (MaskGCT) | 5.25 | 1 | Closest prior work on masked codec TTS; DiSTAR is more novel and achieves better WER |
| 0bcRCD7YUx (VALL-E 2) | 5.00 | 1 | Neural codec LM; rejected for limited novelty; DiSTAR is substantially stronger |
| C53xlgEqVh (Vec-Tok Speech) | 5.20 | 1 | Speech vectorization; weaker empirical results |
| KCVv3tICvp (Codec-LM co-design) | 5.00 | 1 | Codec-LM co-design; comparable topic, weaker results |
| ofzeypWosV (CLaM-TTS) | 6.40 | 1+2 | Probabilistic RVQ TTS; comparable contribution level, DiSTAR has better WER |
| hQvX9MBowC (DiTTo-TTS) | 6.25 | 1+2 | DiT-based TTS; comparable but DiSTAR has stronger results |
| 868masI331 (HALL-E) | 6.40 | 1+2 | Hierarchical codec LM; focused on long-form, DiSTAR addresses broader concerns |
| GTk0AdOYLq (DiffAR) | 5.75 | 1+2 | Diffusion AR for speech; simpler contribution |
| xmgvF0sLIn (Design space of TTA) | 6.00 | 2 | Text-to-audio design space; different focus |
| sL2F9YCMXf (Energy-Based Diffusion LM) | 6.75 | 2 | Diffusion LM theory; different domain |
| 71mqtQdKB9 (SEDD) | 6.60 | 2 | Discrete diffusion LM; different domain |
| sMyXP8Tanm (RADD) | 6.20 | 2 | Absorbing discrete diffusion; different domain |

**Bracket:** Round 1 established 6.0–7.0. Round 2 confirmed this range with additional 5.5–7.5 anchors. DiSTAR is clearly above MaskGCT (5.25) and DiffAR (5.75), comparable to DiTTo-TTS (6.25), CLaM-TTS (6.4), and HALL-E (6.4), but limited by the two major weaknesses from reaching 7+. Final score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>