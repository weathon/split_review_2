Now let me write the complete final review.

## Summary

This paper proposes AdcVSR, a compressed real-world video super-resolution model obtained by distilling a large 3D DiT teacher (DOVE) into a pruned 2D SD backbone augmented with lightweight 1D temporal convolutions. The core contributions are: (1) a "2D + 1D" architectural insight — that heavy 3D spatio-temporal attention is largely redundant for Real-VSR since the LR video already provides structural layout and temporal continuity, so a 2D backbone plus simple 1D temporal convolutions suffices; and (2) a dual-head, dual-domain adversarial distillation scheme that explicitly decouples the discrimination of detail richness and temporal consistency into separate heads. The resulting model achieves 95% parameter reduction and 8× speedup over DOVE while maintaining competitive video quality across 6 datasets.

## Strengths

- **Well-motivated architectural insight (Sec. 3.2).** The paper identifies that heavy 3D spatio-temporal attention in diffusion Transformers may be redundant for Real-VSR because the LR video already provides structural layout and temporal continuity — the model's job is detail synthesis and consistency enforcement, not generating spatio-temporal structure from scratch. This leads to a principled "2D + 1D" design validated empirically in Tab. 2 (2D+1D achieves E_warp=1.67 vs 4.43 for 2D-only, with only 0.03B additional parameters).

- **Real compression gains with correct supporting numbers.** The paper demonstrates a 95% parameter reduction and 8× speedup over DOVE (10.55B → 0.57B; 4.42s → 0.55s) on 25-frame 512×512 videos. All efficiency claims except one (see weakness) are numerically verified against Tab. 1: 110× vs SeedVR2 (60.61/0.55), 121× vs Upscale-A-Video (66.39/0.55), 59× vs MGLD-VSR (32.34/0.55), and 175× vs STAR (96.38/0.55). These are meaningful efficiency numbers for a practical problem where inference cost is a real barrier.

- **Dual-head discriminator design is creative and well-ablated (Sec. 3.3).** Disentangling detail and consistency into separate discriminator heads with five curated training data types with head-specific labels (Eq. 5) is a clean solution to the known detail-consistency conflict in video generation. The ablation in Tab. 3 demonstrates its value over single-head (E_warp improves from 6.32 to 2.22) and single-domain (CLIP-IQA improves from 0.6421 to 0.6861) alternatives.

## Weaknesses

### Major

- **Numerical error in headline efficiency claim (Sec. 4.2).** The paper states AdcVSR achieves "accelerations of 110× and 308×" over SeedVR2 and DLoRAL respectively. The 110× for SeedVR2 (60.61s/0.55s ≈ 110) is correct. However, DLoRAL's inference time in Tab. 1 is 6.36s, giving 6.36/0.55 ≈ 11.6×, not 308×. This is a factor-of-27 error in a published quantitative claim. All other efficiency numbers in the paragraph (95% param reduction, 8× speedup over DOVE, 110× vs SeedVR2, 121×/59×/175× vs multi-step methods) are verified as correct against Tab. 1. The error only affects the DLoRAL comparison, but a factual error of this magnitude in a headline efficiency claim must be corrected.

### Minor

- **Generator adversarial loss is underspecified (Eq. 2–3).** The discriminators each produce two outputs (detail and consistency heads), as shown in Eq. (4) which properly indexes them as \([\mathcal{D}(\mathbf{s})]_d\) and \([\mathcal{D}(\mathbf{s})]_c\). However, the generator adversarial terms in Eq. (2) and (3) write \(\text{Softplus}(-\mathcal{D}_{\text{pixel}}(\mathbf{x}_{\text{student}}))\) and \(\text{Softplus}(-\mathcal{D}_{\text{feature}}(\mathbf{f}_{\text{student}}))\) as scalar quantities, with no indication of how the two head outputs are combined (summed? averaged? handled separately?). This makes the core loss formulation incompletely specified for exact reproduction.

- **The "pruned 3D DiT" ablation baseline (Tab. 2) lacks sufficient specification.** The paper states it is "obtained by the original ADC approach," but ADC (Chen et al., 2025a) was designed for compressing SD-based image SR networks (OSEDiff). Applying ADC to a DiT-based video model like DOVE requires non-trivial adaptation decisions (handling text conditioning components, 3D VAE encoder removal, pruning ratio) that are not described. This limits the interpretability of this ablation comparison.

### Trivial

None.

## Nice-to-Haves

- **Statistical variance**: Reporting standard deviations across multiple seeds for the main comparisons and key ablations (Tab. 3, Tab. 4) would strengthen confidence in the reported improvements given the inherent stochasticity of adversarial training.
- **Discriminator backbone ablation**: The paper uses ConvNeXt for pixel-domain and augmented SD UNet for feature-domain discriminators. A brief justification or ablation of this design choice would improve completeness.
- **Limitations discussion**: A dedicated paragraph discussing known constraints (e.g., reliance on a large teacher model, evaluation only at 4× upscaling, potential out-of-distribution degradation handling) would strengthen the paper.

## Removed Points

These points were identified during review but removed after verification against the paper:

1. **"No statistical variance reported"** — Moved to Nice-to-Haves. Single-run reporting is standard practice in the Real-VSR literature; not a substantive weakness.
2. **"Selectivity in comparison framing (5th on LPIPS, 8th on DISTS)"** — Removed. The reviewer's specific rankings are incorrect: on UDM10, AdcVSR ranks 3rd on LPIPS (not 5th) and 5th on DISTS (not 8th). The paper's claim of "ranks within the top three in most cases" is factually accurate (8/9 metrics on UDM10 are top-3).
3. **"Qualitative examples are thin (2 examples)"** — Removed. The paper provides extensive quantitative results across 6 datasets with 9 metrics; 2 qualitative examples are reasonable supplementary illustration.
4. **"Label encoding scheme bias (detail head never gets positive from real videos)"** — Removed. The paper explicitly discusses this design choice (line 124: "we leave real video details unlabeled, and rely on real images as the positive supervision for 'detail' head"), so the concern is already addressed.
5. **"Discriminator backbone choice not ablated"** — Moved to Nice-to-Haves. A valid observation but standard practice to ground such choices in prior work.
6. **"Missing limitations section"** — Moved to Nice-to-Haves. Common in conference papers; not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the DLoRAL acceleration claim** from 308× to ~12× (6.36s/0.55s ≈ 11.6). Verify all other efficiency numbers against Tab. 1 before final submission.
2. **Clarify Eq. (2)–(3)** by specifying how the two discriminator head outputs (detail and consistency) are combined into the generator adversarial loss term.
3. **Provide details on how ADC was adapted** to prune the 3D DiT teacher for the ablation baseline in Tab. 2, including pruning ratio and architectural adaptation decisions.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>