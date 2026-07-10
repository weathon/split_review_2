Now let me compile the final review based on the verified evidence and the favorability signals.

## Summary

DiSTAR proposes a zero-shot TTS framework that operates entirely in discrete RVQ code space, coupling an autoregressive language model (patch-level drafter) with a masked diffusion model (intra-patch infiller). The architecture targets the joint temporal-depth dependency problem inherent to RVQ representations, avoiding explicit duration predictors. Empirically, DiSTAR achieves the best WER on LibriSpeech test-clean (1.66%) and Seed-TTS test-en (1.32%), and leads on subjective CMOS (0.22). Practical contributions include stochastic layer truncation for test-time bitrate/compute control and RVQ-aware decoding heuristics.

## Strengths

- **Well-motivated architecture for the RVQ setting (Sec 3.1, Fig 1).** The paper correctly identifies the joint temporal-depth dependency challenge in RVQ-based TTS and designs a coherent solution: an AR LM handling cross-patch sequential dependencies (where autoregression is natural) and a masked diffusion model handling intra-patch parallel refinement (where bidirectional context helps). This design has clear internal logic.

- **Best WER across both standard benchmarks (Table 1).** On LibriSpeech test-clean, DiSTAR-medium achieves 1.66% WER vs next-best F5TTS at 2.02%. On Seed-TTS test-en, it achieves 1.32% vs F5TTS at 1.35%. This is a clear and practically meaningful robustness advantage — the WER gap (0.36 and 0.03 percentage points respectively) is consequential for deployment.

- **Leading subjective CMOS scores (Table 2).** DiSTAR achieves CMOS 0.22 on Seed-TTS test-en, well ahead of the next best (F5TTS at 0.01, E2TTS at −0.08), indicating consistent listener preference in A/B comparisons. This is a strong signal of perceptual quality improvement.

- **Practical engineering contributions.** The stochastic layer truncation for test-time RVQ pruning (Sec 3.4) and the RVQ-aware decoding heuristics (layer-wise and position-wise temperature shaping) are genuine practical innovations that address real deployment constraints without retraining.

## Weaknesses

### Fatal

None.

### Major

- **Speaker similarity SOTA claim is overclaimed relative to the evidence.** The abstract, intro, and conclusion claim "state-of-the-art... speaker/style consistency" / "SOTA... speaker similarity", but Table 1 objective SIM shows DiSTAR ranks 3rd on both benchmarks: E2TTS 0.70 > F5TTS 0.68 > DiSTAR-medium 0.67 on LibriSpeech; E2TTS 0.71 > F5TTS 0.68 > DiSTAR-medium 0.66 on Seed-TTS. While DiSTAR leads on subjective SMOS (3.31 vs E2TTS 3.29), the confidence intervals overlap substantially (±0.25 vs ±0.19), so this advantage is not clearly significant. The claims should be calibrated: DiSTAR's demonstrable strength is robustness (WER) and subjective naturalness (CMOS), while speaker similarity is competitive but behind the best continuous-flow systems on objective metrics.

- **The "rich output diversity" claim is unsupported.** The abstract claims "rich output diversity" and Sec 1 claims "fine-grained control over the diversity-determinism trade-off," yet the paper reports zero diversity metrics. Table 3 compares decoding configurations on WER and SPK only — this quantifies a quality trade-off, not diversity. No pairwise similarity distributions, distinct-n metrics, or variation analysis across multiple generations from the same text are provided. This claim is currently an assertion without evidence.

- **NFE mismatch confounds the DiTAR comparison and the inference-cost claim is unverified.** DiSTAR-medium uses NFE=24 while DiTAR uses NFE=10 (Table 1). The paper claims "inference cost close to its continuous counterpart DiTAR" (line 31) but provides no FLOPs analysis, wall-clock timing, or ablation at matched NFE to support this. Since DiTAR (0.6B params, NFE=10) and DiSTAR-medium (0.3B params, NFE=24) differ in both model size and step count, we cannot tell whether DiSTAR's advantages come from its discrete formulation or simply from using more sampling steps. DiTAR results are also marked as "from DiTAR paper" (♦), meaning they come from a potentially different evaluation pipeline. The paper should either run DiSTAR at NFE=10, run DiTAR at NFE=24, or at minimum provide a compute-equalized comparison.

### Minor

- **Ablation study is thin in the main paper.** Section 4.3 contains exactly one table (Table 3) comparing three decoding configurations. The main paper lacks ablations of: (a) whether the AR component is needed, (b) the effect of stochastic layer truncation during training, (c) NFE count, and (d) patch size — though some of these may appear in the appendix (which was stripped by the parser). For a paper making several architectural design claims, the ablation evidence presented in the main paper is limited.

- **Some baseline comparisons are not fully controlled.** DiTAR's scores are from a different paper (♦ symbol), so evaluation pipelines (ASR model, preprocessing, etc.) may differ. It is also ambiguous whether E2TTS, F5TTS, and IndexTTS were retrained on the same Emilia data or use pre-trained models from different training distributions. This should be clarified.

### Trivial

- **Equation (1) frames the model at the frame-code level** (p_θ(C|X) = ∏ p_θ(c_i | c_{<i}, X)), while the actual method operates at the patch level. The equation is imprecise as written.

- **The WER curve in Figure 2 is non-monotonic** (WER rises at 8 layers before dropping at 9 layers) but this is not discussed in the text, only briefly noted in the figure caption.

## Nice-to-Haves

- Equalize NFE between DiSTAR and DiTAR and compare.
- Add diversity evaluation: generate multiple samples per prompt, compute pairwise similarity distributions.
- Ablate the AR module: compare against a diffusion-only baseline.
- Measure and report wall-clock inference speed (real-time factor or samples/second).
- Test on longer-form speech passages (the paper claims long-form synthesis but evaluates only short utterances).
- Report statistical significance for WER and SIM differences.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Brittle under distribution shift" framing untested**: This is a motivation statement about prior work (line 9), not an experimental claim about DiSTAR. The paper does not claim to demonstrate this; it uses it to motivate the discrete design choice. Not a weakness.
- **Human WER exceeds DiSTAR WER** (Table 1): This is a noteworthy observation but not a weakness. If anything, it may indicate evaluation noise in the ASR model.
- **Tail-first bias explanation is speculative**: The paper itself says "A likely reason is that..." (line 140), explicitly framing it as a hypothesis. Not a weakness.
- **Table 2 missing baselines (IndexTTS, DiTAR)**: These systems may not have been available for subjective listening tests. Acknowledgeable as a limitation but not a core weakness.
- **Missing baselines in subjective evaluation**: Same as above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Calibrate the SOTA claims: replace "SOTA robustness, speaker similarity, and naturalness" with "SOTA robustness, competitive speaker similarity, and leading subjective naturalness."
- Add diversity metrics (pairwise WER variance, distinct-n scores) to substantiate the diversity claims.
- Add an ablation removing the AR sketcher (run diffusion on the full sequence without AR) to measure its contribution.
- Provide wall-clock timing or FLOPs analysis to support the inference-cost claim relative to DiTAR.

## Score and Decision

The paper has genuine contributions — a well-motivated architecture and practically meaningful WER/CMOS advantages — but the evaluation has significant gaps: SOTA speaker similarity is claimed despite objective SIM ranking 3rd, diversity claims are made without any supporting evidence, and the comparison with DiTAR is confounded by a 2.4× NFE gap without compute-equivalence verification. These issues are addressable but need to be resolved for the paper's claims to match its evidence.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>