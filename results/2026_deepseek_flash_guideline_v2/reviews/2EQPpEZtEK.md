The calibration search tool encountered an issue with the dataset. I'll proceed with my best judgment based on the paper content and reviews, calibrating against my knowledge of typical ICLR scores.

Let me now write the final consolidated review.

---

## Summary

DiSTAR proposes a zero-shot text-to-speech framework that operates entirely in a discrete RVQ code space, coupling an autoregressive language model for block-level drafting with a masked diffusion model for parallel intra-patch infilling. The system avoids explicit duration predictors, supports test-time RVQ layer pruning, and achieves competitive WER on standard benchmarks. The core architectural idea — combining an AR sketcher with masked diffusion in the discrete RVQ domain — is well-motivated and clearly described.

## Strengths

- **Lowest WER on both benchmarks (Table 1):** DiSTAR-medium (0.3B) achieves WER 1.66% on LibriSpeech test-clean and 1.32% on SeedTTS test-en — the best among all systems shown — while using fewer or comparable parameters to baselines. Notably, DiSTAR's WER improves over that of its own codec resynthesis (1.83 and 1.71 respectively), confirming that the generative model adds value beyond codec quality.

- **Test-time RVQ layer pruning without retraining (Section 3.4, Figure 2):** Training with stochastic layer truncation enables graceful quality-compute trade-offs at inference by simply dropping upper RVQ layers, with WER staying roughly stable (~2.18 to ~1.98) across 2–9 layers while speaker similarity increases. This capability is not demonstrated by the baselines.

- **Fully discrete pipeline eliminates duration predictors (Section 1, Section 3.1.2):** The [EOS] token for patch-level termination removes explicit duration predictors or forced alignment used in continuous-domain systems — a genuine architectural simplification.

- **Leading subjective scores on SMOS and CMOS (Table 2):** DiSTAR achieves SMOS of 3.31 (highest among all systems, including E2TTS at 3.29) and a positive CMOS of 0.22 (the only system with positive CMOS relative to human reference). These results come from human listening tests and provide controlled evidence of quality.

- **Diagnostic analysis of non-autoregressive decoding pathology (Section 3.4):** The paper identifies a "tail-first" bias in parallel decoding and proposes three lightweight, RVQ-specific mitigation strategies, with ablation evidence (Table 3) showing their effectiveness. This level of detail goes beyond generic "we used CFG" reporting.

## Weaknesses

### Fatal
None.

### Major

- **Uncontrolled comparison confounds SOTA claims (Table 1):** Baseline numbers (DiTAR, E2TTS, F5TTS, IndexTTS) are taken from published papers without retraining under the same conditions. The systems use different neural codecs (with different bitrates and reconstruction qualities), different training datasets, and different compute budgets. The paper's own codec resynthesis WER (1.83 on LibriSpeech, 1.71 on SeedTTS) already surpasses several baselines, meaning the WER gap could partly reflect codec quality differences rather than generative modeling superiority. The paper does not acknowledge this limitation in the comparison methodology.

- **Missing ablations of the core architectural design (Table 3):** The central contribution is coupling AR drafting with masked diffusion in RVQ space, yet no experiment isolates whether this hybrid outperforms (a) a pure-AR baseline on the same RVQ codes (flat or delay-pattern decoding) or (b) a pure masked-diffusion baseline without the AR sketcher. Without these ablations, the reader cannot attribute the observed results to the proposed architecture rather than to engineering choices or codec quality.

- **Computational efficiency claims are unsupported (Section 1, Section 4):** The paper asserts inference cost "close to its continuous counterpart DiTAR" but uses NFE=24 vs. DiTAR's NFE=10 (2.4× more diffusion steps). No wall-clock latency, throughput, or FLOPs comparison is provided to substantiate the "blockwise parallelism" advantage.

### Minor

- **Speaker similarity trails several baselines on objective SIM (Table 1):** DiSTAR-medium achieves SIM of 0.67/0.66 vs. E2TTS's 0.70/0.71 and F5TTS's 0.68/0.68 on LibriSpeech/SeedTTS. While the paper characterizes this as "on par" (which is fair), the objective SIM data consistently places DiSTAR behind continuous-representation systems. The subjective SMOS advantage exists but with overlapping confidence intervals (3.31±0.25 vs. 3.29±0.19 for E2TTS).

- **No confidence intervals or variance for objective metrics (Table 1):** WER gaps between systems are as small as 0.3–0.7 percentage points, and SIM gaps are 0.01–0.04. Without bootstrap confidence intervals or multiple-seed runs, it is impossible to assess whether these differences are statistically meaningful — a standard the paper itself adopts for subjective metrics (Table 2).

- **Custom codec quality not compared to standard codecs (Section 3.5.1):** The paper trains a 0.3B-parameter 9-stage RVQ codec but provides no comparison of its reconstruction quality (WER, SIM, UTMOS) against widely-used codecs like EnCodec, HiFi-Codec, or DAC. Since codec quality directly affects all downstream metrics, contextualizing the codec's own performance is needed.

### Trivial

- **Figure 2 shows a non-monotonic WER increase at 8 layers (2.04 vs. 1.88 at 6 layers) with no discussion.**
- **Main text defers layer counts, attention heads, and hidden dimensions entirely to the appendix** without even summary numbers.

## Nice-to-Haves

- Wall-clock latency or throughput comparison for DiSTAR vs. a comparable AR baseline to substantiate the parallelism claim.
- A controlled experiment where a strong baseline (e.g., F5TTS or DiTAR) is adapted to use the same RVQ codec, isolating generative model quality from codec quality.
- Bootstrapped confidence intervals for objective metrics given the small absolute differences.

## Removed Points

These points were flagged by reviewers but removed from the main evaluation for the following reasons:

| Point | Reason for Removal |
|-------|-------------------|
| "Tail-first bias explanation is speculative" | The paper frames this as an observation and provides tested mitigations (Table 3); it is not a core claim requiring formal proof. |
| "Missing ablation for embedding transplantation" | Implementation detail; bootstrapping from codec embeddings is a standard and reasonable design choice. |
| "No subjective results for LibriSpeech-PC" | SeedTTS test-en is a standard subjective benchmark; this omission is not critical. |
| "Missing ablation of cosine mask schedule" | Schedule follows prior work (Chang et al., 2022); not claimed as a contribution. |
| "Comparison unfair because DiTAR uses NFE=10 vs NFE=24" | Re-framed as part of the efficiency weakness; the NFE difference is relevant to efficiency claims but does not invalidate quality comparisons (more steps can improve quality). |

## Novel Insights

None beyond the paper's own contributions. The cross-review synthesis surfaces a structural tension: the paper's strongest evidence for SOTA claims (WER) rests on comparisons where codec quality is not controlled, while its most controlled evidence (subjective evaluation) shows a narrower advantage. This trade-off is familiar from system-paper reviewing and does not constitute a novel observation about the paper's content.

## Suggestions

1. **Acknowledge the uncontrolled comparison explicitly** and temper SOTA claims, or add a controlled experiment (e.g., adapting a baseline to the same codec).
2. **Provide wall-clock latency measurements** to support the efficiency claims and substantiate the "blockwise parallelism" advantage.
3. **Add ablations isolating the AR-and-MDM coupling** vs. pure AR or pure masked diffusion to validate the core architectural claim.
4. **Report confidence intervals for objective metrics** given the small absolute differences.
5. **Compare the custom codec's reconstruction quality** to standard codecs (EnCodec, HiFi-Codec, DAC).

## Score and Decision

Based on my assessment, the paper presents a well-motivated architectural contribution (AR drafting + masked diffusion in discrete RVQ space) with competitive results, particularly on WER and subjective evaluation. However, the evaluation has significant limitations: uncontrolled baseline comparisons, missing ablations of the core design, and unsupported efficiency claims. The speaker similarity results are mixed. These issues prevent the paper from fully substantiating its SOTA claims in the current form.

The paper falls in the borderline reject / borderline accept range. It has genuine novelty and interesting results, but the evidence is not yet commensurate with the strength of the claims. A score of **5** reflects a paper with substantive contributions that needs substantially stronger evaluation to merit full acceptance.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>