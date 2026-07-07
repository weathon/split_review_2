Now I have sufficient calibration data. Let me produce the final consolidated review.

## Summary

This paper proposes AdcVSR, an improved adversarial diffusion compression method for real-world video super-resolution. The key contributions are: (1) a "2D + 1D" architecture combining a pruned SD2.1 backbone with lightweight 1D temporal convolutions, motivated by the insight that 3D spatio-temporal attention is partially redundant when the LR video already provides structural/temporal information; and (2) a dual-head, dual-discriminator adversarial distillation scheme that disentangles detail richness and temporal consistency optimization through separately labeled data types. The resulting model achieves 0.57B parameters and 0.55s inference for 25-frame 512×512 video, with competitive quality against much larger one-step VSR models like DOVE (10.55B).

## Strengths

- **Novel and well-validated dual-head adversarial distillation scheme (§3.3, Tables 3&4).** The dual-head discriminator design that disentangles detail and consistency assessment via separate linear projection heads (192 and 64 channels respectively) is the paper's most technically novel contribution. The five-type curated data labeling scheme (Eq. 4-5) — using temporally shuffled videos as "fake for consistency," static pseudo-videos from images as "real for both," and randomly cropped sequences as "real for details but fake for consistency" — is methodologically creative and goes well beyond standard adversarial training tricks. The ablation in Table 3 directly validates the design: dual-head/dual-domain achieves CLIP-IQA 0.6861 and E_warp* 2.22, compared to single-head (0.6745, 6.32) and single-domain (0.6421, 3.59) variants.

- **Well-motivated architectural hypothesis with clean empirical support (§3.2, Table 2).** The core insight — that 3D spatio-temporal attention is partially redundant for Real-VSR because the LR input already provides structural and temporal information — is clearly articulated. The "2D + 1D" design follows directly from this reasoning. Table 2 shows the 2D+1D design achieves E_warp* of 1.67 vs 4.43 for the pure 2D backbone and 2.53 for a pruned 3D DiT, with minimal parameter overhead (0.55B vs 0.52B for 2D), cleanly validating the architectural thesis.

- **Genuine and practically significant efficiency gains.** AdcVSR (0.57B params, 0.55s for 25-frame 512×512) is substantially lighter and faster than existing one-step VSR models: DOVE (10.55B, 4.42s), SeedVR2 (8.24B, 60.61s), and DLoRAL (1.30B, 6.36s). These gains are meaningful for real-world deployment.

- **Strong temporal consistency results with supporting evidence.** AdcVSR achieves the best (lowest) E_warp* on both UDM10 (1.67 vs DOVE's 2.22) and VideoLQ (6.74 vs DOVE's 8.41). The qualitative temporal profiles in Figure 3 visually support reduced flickering. DOVER scores (0.4878 vs DOVE's 0.4731 on UDM10) provide converging evidence that temporal quality is genuinely improved, not merely an artifact of over-smoothing.

- **Clean, informative ablation structure.** Tables 2, 3, and 4 each isolate a single variable of interest (architecture, discriminator design, teacher choice) and provide clear, interpretable evidence. Table 4 is particularly well-designed: removing the teacher (HR GT only) drops MUSIQ from 61.48 to 50.32, and removing adversarial loss drops LPIPS from 0.3337 to 0.3596, cleanly demonstrating the value of both components.

## Weaknesses

### Major

- **No statistical significance or variance reported.** Across all experiments, the paper reports only point estimates without standard deviations, confidence intervals, or even a statement about whether metrics are single-run or averaged. Several comparisons involve small differences (e.g., UDM10 CLIPIQA: AdcVSR 0.6818 vs PiSA-SR 0.7055; VideoLQ MANIQA: AdcVSR 0.6121 vs HYPIR 0.6424) where it is unclear if differences are meaningful or within noise. While single-run evaluation is common practice in this subfield, the omission is notable given the paper's competitive claims.

- **The teacher-student performance asymmetry on real-world data is not discussed (§4.2).** On UDM10 (synthetic), AdcVSR underperforms its teacher DOVE on fidelity metrics (PSNR 25.36 vs 26.00, LPIPS 0.3065 vs 0.2648). Yet on VideoLQ (real-world), the student dramatically outperforms the teacher on no-reference metrics (MANIQA 0.6121 vs 0.4336, CLIPIQA 0.6024 vs 0.3258). The paper attributes this improvement to adversarial training on real data but does not explore *why* the student exceeds its own teacher in a domain the teacher was also trained on. This is an interesting scientific question that goes unremarked, and the paper would be strengthened by an explicit hypothesis or analysis.

### Minor

- **Framing of compression claims could mislead about attribution.** The paper's headline claims of "95% parameter reduction" and "8× speedup over DOVE" (abstract, contribution list, conclusion) are numerically correct but the compression mechanism itself (structural pruning of the SD backbone from 10.55B to 0.46B) is inherited from AdcSR (Chen et al., 2025a). The novel contributions (1D temporal convs, dual-head discriminators) actually increase parameters from 0.46B to 0.57B. The paper does cite AdcSR and states it builds on this prior work, but the framing could be read as implying greater novelty in compression than is warranted. Separating inherited compression from novel technical contributions would improve clarity.

- **No discussion of failure cases or limitations.** The paper presents only positive results. Every method has failure modes — for instance, a model optimized for low warping error might over-smooth under conditions requiring fine-grained texture maintenance across frames. A brief limitations paragraph would improve scientific completeness.

- **Dual-head channel asymmetry not discussed (§4.1).** The "detail" head uses 192 output channels while the "consistency" head uses 64 (a 3:1 ratio). The paper does not discuss whether this ratio was tuned, its effect on gradient balance, or whether it could bias optimization toward detail quality. An ablation varying this ratio would strengthen the design's empirical grounding, but the absence is not a structural flaw.

### Trivial

- **Naming inconsistency.** The model is called "AdcVSR" in most of the paper but appears as "AdeVSR" in Figure 3's caption and several surrounding text passages (lines 179, 181, 185, 189, 191, 193, 195).

## Nice-to-Haves

- The training cost (8 × H20 GPUs × 96GB × ~1 day = ~768 GPU-hours of high-memory compute) is non-trivial and would provide useful context alongside the inference efficiency claims.
- The paper's claim that 3D attention is "redundant" (§3.2) is presented as a hypothesis without direct evidence from activation pattern analysis. An investigation of feature redundancy would strengthen this claim beyond the indirect validation in Table 2.
- On the E_warp* metric, a controlled experiment measuring warping error on artificially blurred versions of outputs could help establish discriminant validity (distinguishing genuine temporal consistency from over-smoothing). This concern is partially mitigated by the DOVER scores and qualitative temporal profiles.

## Removed Points

- "Table 1 formatting makes rankings hard to parse" — this is a parser artifact; formatting is likely clear in the original PDF.
- "The 95% claim is factually wrong" — the claim is numerically correct (10.55B → 0.57B ≈ 94.6%), as verified in Table 1; the concern is about attribution, not accuracy.
- "The model name 'AdeVSR' appears in Figure 3 caption" — retained as a trivial naming inconsistency above.
- Various generic framing concerns from the harsh critic that were already addressed by the paper's own citations and descriptions — the paper clearly states it builds on AdcSR, so the criticism of conflation is about presentation emphasis, not factual omission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a short paragraph in §4 (or Conclusions) explicitly separating what is inherited from AdcSR vs. what is novel in this work.
- Report variance across at least 3 runs (or state the seed used for a single run) for the main results in Table 1.
- Add a brief discussion of the teacher-student performance asymmetry on real-world data — even a hypothesized explanation would strengthen the scientific narrative.

## Score and Decision

**Calibration.** Round 1 bracket: the paper sits between 6.0 and 7.5. Compared to AddSR (avg 5.00) where the most severe weakness had weight -9.85, the current paper's most severe weakness (-6.03 for no statistical significance) is substantially less critical. Compared to SiDA (avg 6.25, top weakness -8.12 for novelty), this paper has stronger positive weighted items (max +7.49 vs +4.63) and less severe negatives. Compared to InstaRevive (avg 6.00, top weakness -6.76), this paper again has higher positive weights. The weighted-item comparison confirms the paper is above the 6.0 anchor and likely sits around 6.5: the dual-head discriminator design (+7.49) and architectural hypothesis (+5.98) are genuinely strong contributions that the comparably-scored anchors lack, while the most severe weakness (no statistical significance, -6.03) is a procedural gap rather than a flaw in the core method.

**Final score: 6.5.** This is a solid, well-executed paper with a clearly motivated architectural design, a novel and well-ablated technical contribution (dual-head adversarial distillation), and practically significant efficiency gains. The weaknesses are real but manageable — the framing of compression could be clearer, variance reporting is absent, and the analysis stops short of fully explaining the interesting teacher-student performance asymmetry. These do not undermine the core claims but prevent a higher score. The paper merits acceptance.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>