Now let me form the final review. I have a clear picture of the paper and the calibration landscape.

**Calibration bracket round 1:** Based on the anchors, I estimate this paper sits between **5.5 and 6.5**. It is clearly stronger than AddSR (5.00, rejected) and "Does Diffusion Beat GAN in SR?" (5.75, rejected) — those papers had experimental gaps or inconclusive contributions, while this paper has a tangible novel method and clear positive results. It is comparable to "Solving Video Inverse Problems" (6.50, accepted) and "Solving Diffusion ODEs" (6.67, accepted), which both had some experimental limitations but were accepted on the strength of their methodological contributions. The current paper's ablation confound is a genuine issue but does not invalidate its core contribution.

Now let me write the final review.

---

## Summary

This paper proposes an improved Adversarial Diffusion Compression (ADC) method for real-world video super-resolution (Real-VSR). It distills a large 3D spatio-temporal DiT teacher (DOVE) into a compact student with a 2D SD backbone augmented by lightweight 1D temporal convolutions. The core methodological contribution is a dual-head, dual-discriminator adversarial distillation scheme that disentangles detail richness and temporal consistency supervision. The resulting AdcVSR model achieves 95% parameter reduction and 8× speedup over DOVE while maintaining competitive video quality across 6 datasets.

## Strengths

1. **Well-motivated architectural insight (Sec. 3.2).** The paper provides a clear rationale for why heavy 3D spatio-temporal attention in DiTs is over-provisioned for Real-VSR: the LR input already supplies global structure and temporal continuity, so a 2D backbone + lightweight 1D temporal convs should suffice. Tab. 2 supports this with concrete numbers: the 2D+1D student (0.55B params, DISTS 0.2112) nearly matches a pruned 3D DiT (8.36B params, DISTS 0.2098) on DISTS while using 7% of the parameters.

2. **Dual-head discriminator design (Sec. 3.3) is the paper's most novel component.** The idea of disentangling detail and consistency discrimination via separate linear heads with five curated data types (videos, shuffled videos, static pseudo-videos, mismatched frames) and head-specific real/fake labels is genuinely clever and directly addresses the known detail-consistency conflict in video generation. The ablation in Tab. 3 provides reasonable evidence: dual-head dual-domain (CLIP-IQA 0.6861, E_warp* 2.22) outperforms single-head (0.6745, 6.32) and single-domain (0.6421, 3.59) variants.

3. **Efficiency gains are substantial and cleanly measured.** The 95% parameter reduction (10.55B → 0.57B) and 8× speedup (4.42s → 0.55s) over DOVE are verified on identical hardware and the same 25-frame × 512² benchmark (Tab. 1). The comparison against 10 competing methods across 6 datasets and multiple metrics is comprehensive.

## Weaknesses

### Fatal
None.

### Major

1. **The "2D+1D is sufficient" claim is confounded with the improved training pipeline (Tab. 2, Sec. 4.3).** Tab. 2 compares: (i) a pruned 3D DiT trained with "the original ADC approach," (ii) the 2D AdcSR backbone (trained with its own original method), and (iii) the proposed 2D+1D trained with the full improved pipeline (dual-head distillation + DOVE teacher). Because training methods differ across all three rows, the table cannot attribute the performance gap to architecture alone. The 3D model's worse E_warp* (2.53) than 2D+1D (1.67) could be partly because the original ADC training is suboptimal for video, not because 3D attention is inherently worse at temporal consistency. The 2D model's collapse (DISTS 0.2418, E_warp* 4.43) could be partly due to the absence of adversarial distillation improvements rather than the absence of temporal convolutions. **What is needed:** a controlled experiment training the 2D+1D architecture with the original ADC protocol and comparing against the 2D backbone with the same protocol, then showing the marginal gain from the improved distillation. This weakness does not invalidate the full system's results, but it means the first contribution claim (Sec. 1, contribution 2) is less well-supported than the second (contribution 3).

### Minor

2. **The student outperforming its teacher on several metrics is under-explained (Tab. 1).** On UDM10, AdcVSR surpasses its teacher DOVE on CLIPIQA (0.6818 vs. 0.5420), MUSIQ (63.88 vs. 60.68), and E_warp* (1.67 vs. 2.22). A compressed student exceeding its teacher on metrics relevant to the teacher's own objectives is unusual and deserves explicit analysis. The paper mentions this only as "competitive." The most plausible explanation is that the GAN post-training injects sharpness that boosts no-reference metrics but may trade off fidelity (lower PSNR/SSIM). The E_warp* result is even more puzzling — if the student achieves better temporal consistency than the teacher it was distilled from via L1 regression, the adversarial phase and 1D convolutions must be doing qualitatively different temporal modeling. An ablation comparing Stage 1 (pure distillation) vs. Stage 2 (adversarial) metrics would clarify whether the GAN phase drives these improvements.

3. **The dual-head discriminator ablation (Tab. 3) is thin.** It reports only CLIP-IQA and E_warp* on a single dataset (YouHQ40). A more thorough evaluation with additional metrics (LPIPS, MUSIQ, DOVER) across multiple datasets would strengthen the claim that dual-head dual-domain discriminators are broadly beneficial.

4. **The temporal consistency metric E_warp* measures smoothness, not correctness.** As the paper itself notes, Real-ISR methods without temporal modeling get high warping errors (PiSA-SR: 6.96, HYPIR: 10.68), but a model that blurs or averages frames could also achieve low warping error. The paper partially addresses this with DOVER scores and temporal profile visualizations (Fig. 3), but an additional metric (e.g., tOF or learned video quality) or a small user study would strengthen the temporal consistency claims.

### Trivial

5. **Naming inconsistency:** The paper uses "AdcVSR" throughout most sections but "AdeVSR" in Fig. 3, Fig. 4, and several surrounding paragraphs (lines 179–195). These should be harmonized.

6. **Table 4 typo:** The dataset is listed as "MYSR4x" in the table header (line 229) but is "MVSR4x" in the text (line 167).

## Nice-to-Haves

- A limitations discussion (failure cases, e.g., fast motion, extreme degradations) would be a helpful addition.
- The sensitivity of the dual-head discriminators to the choice of frozen backbones (ConvNeXt from OpenCLIP for pixel domain, augmented SD UNet for feature domain) is not discussed. A brief analysis would improve reproducibility.

## Removed Points

These points were considered but excluded from the main weaknesses for the reasons noted:

- **"Missing statistical significance / error bars."** — Single-run evaluation is standard for large-scale diffusion model benchmarks in this field; demanding confidence intervals would be imposing a standard not used by the community. Moved to nice-to-have.
- **"Per-dataset breakdown only shows 2 of 6 datasets in main paper."** — The appendix (standard practice for this venue) is stripped by the parser; we cannot verify whether the remaining 4 datasets are deferred there. Removed as unverifiable.
- **"Missing related works."** — Cannot be confirmed without external sources. Removed by rule.
- **"Missing appendix / proofs."** — The parser strips the appendix from all papers. Removed by rule.
- **"Criticism about unfair comparison with baselines."** — Where comparisons favor baselines (e.g., PiSA-SR and HYPIR lead on CLIPIQA/MUSIQ), the asymmetry works against the author's method, which is allowed by rule.
- **"The discriminator backbone sensitivity is not discussed."** — This is a minor speculation that doesn't rise to a genuine weakness; moved to nice-to-have.
- **"The paper claims about providing 'a systematic recipe' and 'practical guidelines' is a reach."** — This is a phrasing preference, not a substantive weakness.

## Novel Insights

The most interesting observation from this review is the tension between the paper's two main claims. The architectural claim ("2D+1D is sufficient") is confounded with the training pipeline, while the distillation claim (dual-head discriminators resolve the detail-consistency conflict) is independently validated. This suggests the paper's strongest and most novel contribution is the dual-head adversarial distillation scheme rather than the architectural innovation per se — a point the authors might lean into more explicitly. Additionally, the student-outperforming-teacher phenomenon on E_warp* hints that the 1D temporal convolutions, despite their simplicity, may be doing something qualitatively different from the teacher's 3D attention for temporal consistency, which could be a direction for future work.

## Suggestions

1. **Run a controlled ablation holding training method constant:** Train the 2D (AdcSR) backbone and the 2D+1D student using exactly the same pipeline (same teacher, same distillation losses, same dual-head adversarial training). This would cleanly isolate the marginal contribution of the 1D temporal convolutions.
2. **Analyze the two-stage training:** Compare metrics after Stage 1 (pure distillation) vs. Stage 2 (adversarial fine-tuning) to explain which stage drives the student's outperformance of the teacher on no-reference metrics and E_warp*.
3. **Expand Tab. 3 to include additional metrics and datasets.**
4. **Harmonize the "AdcVSR"/"AdeVSR" naming** and correct the "MYSR4x" typo.

## Score and Decision

**Score: 6.0 — Borderline Accept**

**Decision: Accept**

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|------------------------|
| AddSR (BpKbKeY0La) | 5.00 | R1-bracket | Weaker: less novel contribution (ADD adaptation vs. novel dual-head design), less thorough evaluation |
| Does Diffusion Beat GAN (46mbA3vu25) | 5.75 | R1-bracket | Weaker: comparison study with inconclusive findings vs. tangible method with clear positive results |
| Solving Video Inverse Problems (TRWxFUzK9K) | 6.50 | R1-bracket | Comparable: similar novelty level, accepted despite some experimental gaps |
| Solving Diffusion ODEs (BtT6o5tfHu) | 6.67 | R1-bracket | Similar: accepted despite low PSNR and missing SSIM; this paper has stronger empirical results but a confounded ablation |
| Flexible Residual Binarization (MEbNz44926) | 8.00 | R1-bracket | Stronger execution: cleaner ablation design, but still rejected; this paper's confounded ablation prevents reaching this tier |
| Sample what you can't compress (vK8C37eHXM) | 3.20 | R1-bracket | Weaker: less convincing contribution |
| Dissecting Arbitrary-scale SR (QO3yH7X8JJ) | 5.25 | R1-bracket | Weaker: overclaimed novelty, less thorough evaluation |

**Bracket: Round 1 → 5.5–6.5 → Final: 6.0.** The paper has a genuine novel contribution (dual-head discriminator), impressive efficiency gains, and thorough evaluation. The confounded ablation is a significant weakness that prevents a higher score, but it does not invalidate the overall contribution.

**MY FINAL SCORE:** <score>6.0</score>
**MY FINAL DECISION:** <decision>Accept</decision>