Now let me finalize my review with the calibrated score.

**Bracket (Round 1):** 5.5–7.0 — above AddSR (avg 5.0, relevant SR+distillation paper with similar tradeoff critique but more severe novelty concerns), and within the range of accepted papers like InstaRevive (6.0), SiDA (6.25), and Solving Video Inverse Problems (6.5).

**Narrowing:** The paper has a genuinely novel architectural insight, clean experiments across 6 datasets, and a real practical contribution. The weaknesses are all minor/addressable. This places it solidly in the 6.0 range — borderline accept, but on the stronger side.

## Summary

This paper proposes AdcVSR, a compressed one-step diffusion model for real-world video super-resolution (Real-VSR). The key ideas are: (1) replacing heavy 3D spatio-temporal DiTs (teacher DOVE) with a pruned 2D SD backbone augmented with lightweight 1D temporal convolutions ("2D+1D"), and (2) a dual-head, dual-discriminator adversarial distillation scheme that explicitly disentangles detail richness and temporal consistency into separate adversarial signals. The result is a model with 95% fewer parameters and 8× speedup over DOVE while maintaining competitive quality across 6 datasets.

## Strengths

1. **Clear, well-motivated architectural insight (Section 3.2).** The paper identifies that 3D spatio-temporal DiTs are overkill for Real-VSR because the LR input already supplies much of the long-range spatio-temporal structure — the problem is primarily about synthesizing details and ensuring temporal consistency. The resulting "2D+1D" design is specific, falsifiable, and supported by ablation (Table 2): the 2D+1D model achieves better temporal consistency ($E_{\text{warp}}^*$ 1.67 vs. 2.53) than even the pruned 3D DiT teacher while using 93% fewer parameters.

2. **Well-designed dual-head adversarial scheme (Section 3.3).** The detail-consistency conflict is a known problem, but this paper constructs explicit disentanglement at the discriminator level: two heads share a backbone but produce separate adversarial signals for detail realism and temporal consistency, each with carefully curated labeled data. The five-data-type curation (Eq. 5) is thoughtful, and ablation Table 3 cleanly shows that single-head or single-domain variants collapse on one of the two objectives.

3. **Strong empirical coverage.** Evaluations span 6 datasets (3 synthetic, 3 real-world) with 9 metrics covering fidelity, perceptual quality, temporal consistency, and video quality. The compressed model (0.57B params, 0.55s for 25-frame 512×512) delivers competitive quality with order-of-magnitude efficiency gains over most competitors.

4. **Component-level ablations.** Tables 2–4 separately test the network design, the discriminator configuration, and the distillation setup, each on a different dataset, showing consistent patterns that each component provides identifiable gains.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Quality-efficiency tradeoff understated relative to teacher DOVE.** The paper repeatedly states that AdcVSR "maintains competitive video quality" against DOVE. On UDM10 (Table 1), however, the full-reference perceptual metrics show notable degradation: LPIPS increases by +15.8% (0.2648→0.3065) and DISTS by +21.9% (0.1732→0.2112). While these numbers are not hidden — they appear in the table — the paper's framing ("maintaining competitive video quality while striking a balance") obscures the magnitude of the sacrifice on these two metrics. The efficiency gains are genuinely large and the tradeoff may be acceptable, but a candid, quantitative statement of which metrics improve, which degrade, and by how much would strengthen credibility.

2. **The 2D backbone is pre-compressed (AdcSR), creating a confound in the ablation for Claim (2).** The 2D backbone is initialized from AdcSR, which itself was produced by compressing PiSA-SR via adversarial distillation for Real-ISR. This means the "2D" row in Table 2 is not a randomly initialized or uncompressed 2D SD network — it already contains compression knowledge. Consequently, the improvement from 2D to 2D+1D (DISTS 0.2418→0.2112, $E_{\text{warp}}^*$ 4.43→1.67) could partly reflect the 1D convolutions acting as a better feature adaptation mechanism for the pre-compressed backbone, rather than purely providing temporal modeling. Starting from a differently compressed or uncompressed 2D backbone would help isolate this effect. (This does not invalidate the contribution — using AdcSR is a practical choice — but it tempers the strength of the claim that a 2D backbone + 1D convs alone suffice.)

3. **Feature-domain discriminator shares the generator's architecture without discussion.** The feature-domain discriminator uses "the same augmented SD UNet as our designed AdcVSR" as its frozen backbone (Section 3.3). Although the backbone is frozen, the discriminator evaluates features produced by the student generator using the same architectural family, which could cause it to learn representational biases specific to the UNet rather than general video realism. The paper does not discuss this design choice or compare it with an alternative (e.g., ConvNeXt in both domains, or a structurally different backbone).

4. **Predictor-corrector training dynamics underspecified for reproducibility.** The paper describes the dual-head discriminator architecture and loss but does not specify the adversarial training schedule (e.g., number of discriminator updates per generator update, whether gradient penalty or spectral normalization is used). These details matter for reproducing the adversarial training.

5. **The detail-consistency conflict is cited from prior work but not demonstrated in the paper's own setup.** Section 3.1 motivates the conflict by citing prior work, but no experiment in this paper shows directly that a single-head discriminator causes collapse on the authors' own data (Table 3 addresses this only post-hoc and on a different dataset). A small diagnostic experiment would strengthen the motivation.

### Trivial
None.

## Nice-to-Haves
- A dedicated figure or paragraph quantifying the quality-efficiency tradeoff against DOVE across all metrics.
- Ablation starting from an uncompressed SD2.1 backbone to isolate the effect of 1D temporal convolutions from the pre-compressed initialization.
- Comparison with other lightweight temporal modeling approaches (TSM, TAM, small-kernel 3D convolutions) to strengthen the "1D convs are sufficient" claim.
- Variance or confidence intervals for no-reference metrics (MANIQA, CLIPIQA, MUSIQ), which are known to be content-sensitive.

## Removed Points
- **"AdeVSR"/"AdcVSR" naming inconsistency**: Removed per hard rules about formatting/parser artifacts.
- **"MYSR4x" vs "MVSR4x" table header**: Removed per hard rules about formatting/parser artifacts.
- **Real-ISR methods inflate top-three counts**: The paper transparently includes these baselines and acknowledges the distinction; this is not a flaw.
- **Ablations on different datasets prevent cross-comparison**: Running each ablation on a different dataset demonstrates robustness; this is a design choice, not a weakness.
- **Missing related work / missing appendix sections**: Removed per hard rules (parser strips these sections).
- **Reproducibility nitpicks about trivial hyperparameter details**: Removed per hard rules.

## Novel Insights
The most notable observation from the review process is that the "2D+1D" design choice, while appearing simple, is non-trivially motivated: the paper correctly identifies that 3D DiTs are over-provisioned for Real-VSR because the LR input already supplies global spatio-temporal structure. This insight is specific to Real-VSR and does not trivially follow from efficiency concerns alone. The pre-compressed backbone confound (Weakness #2) is a genuine methodological observation not discussed in the paper — the analysis of Claim (2) is partly conflated with prior compression knowledge inherited from AdcSR. Beyond these, no novel insight emerges beyond the paper's own contributions.

## Suggestions
1. Add a dedicated paragraph or figure that directly compares AdcVSR quality vs. DOVE quality across all metrics with explicit quantification (e.g., "AdcVSR improves no-reference metrics by X% and $E_{\text{warp}}^*$ by Y%, while LPIPS increases by 15.8% and DISTS by 21.9%"). This would strengthen credibility and help practitioners assess the tradeoff.
2. Add a brief discussion or small ablation addressing the feature-domain discriminator architecture choice — even a sentence explaining why the generator's UNet was chosen over alternatives would address a genuine methodological curiosity.
3. Include a note on discriminator training dynamics (update ratio, normalization) for reproducibility.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>