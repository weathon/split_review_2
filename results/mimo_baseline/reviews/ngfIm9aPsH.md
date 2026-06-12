## Summary

This paper introduces Object Fidelity Diffusion (OF-Diff), a layout-to-image generation method for remote sensing that extracts structural shape priors via an Enhanced Shape Generation Module (ESGM) and uses online-distillation to transfer fidelity from image-conditioned to shape-only decoders, eliminating the need for real-image references at inference. The method further applies DDPO-based reinforcement learning fine-tuning with KNN and KL-divergence rewards to improve diversity and distributional consistency. Experiments on DIOR, DOTA, and HRSC2016 demonstrate improvements over SOTA methods in fidelity, layout consistency, shape fidelity, and downstream detection mAP.

## Strengths

- **Clear problem formulation and practical motivation.** The paper identifies concrete failure modes of existing RS L2I methods (control leakage, structural distortion, dense generation collapse) with visual evidence in Figure 1, and frames the need to eliminate real-image dependency at inference as a practical bottleneck. This is well-motivated for data augmentation in remote sensing.

- **Comprehensive evaluation with 13 metrics across 4 dimensions.** The evaluation covers generation fidelity (FID, KID, CMMD), layout consistency (CAS, YOLOScore), shape fidelity (IoU, Dice, CD, HD, SSIM), and downstream utility (mAP). This breadth is commendable and provides convincing evidence that improvements are not artifacts of a single metric.

- **Substantial quantitative improvements.** OF-Diff achieves best or near-best results across nearly all metrics on both DIOR and DOTA datasets. The downstream detection gains are meaningful: +2.2% and +1.94% mAP on DIOR and DOTA respectively, with per-class improvements of 8.3%, 7.7%, and 4.0% on airplanes, ships, and vehicles. These are practical improvements for a data augmentation technique.

- **Ablation study provides useful decomposition of contributions.** Table 4 shows that ESGM contributes the largest YOLOScore improvement (~14%), while online-distillation and DDPO each contribute additional gains. The analysis of the consistency loss weight λ in Figures 5(c)-(d) is also informative.

- **Evaluation on unknown layouts (Table 3)** provides evidence of generalization beyond training distributions, which is important for practical deployment.

## Weaknesses

### Fatal
None.

### Major

- **Inconsistency in Table 4 ablation results.** The final two rows of Table 4 both have ESGM ✓, Lc ✓, DDPO ✓, yet report different numbers (FID 37.98 vs 24.92, YOLOScore 47.74 vs 58.99, etc.). This is not explained in the text. One likely explanation is that the first of these rows corresponds to a configuration with caption input and the second without (based on the surrounding discussion), but this is never made explicit. This creates confusion about what the ablation actually shows and whether caption usage is being varied alongside the modules. This should be clarified.

- **The online-distillation mechanism's novelty relative to consistency distillation (Song et al., "Consistency Models") is not adequately discussed.** The consistency loss in Eq. 6 is structurally similar to standard consistency distillation, and the stop-gradient teacher-student formulation is well-established. The paper should more clearly articulate what is architecturally or conceptually novel beyond applying these established techniques to the RS domain with a dual-decoder design.

- **Shape fidelity metrics are computed on Canny edge maps of cropped 64×64 patches.** This is a coarse proxy for shape quality. IoU values in Table 2 are very low (0.04–0.12), suggesting the edge-map comparison may be too noisy to be meaningful as a standalone evaluation. The authors should discuss the limitations of this evaluation protocol and whether the improvements are perceptually significant at this resolution.

### Minor

- **DDPO formulation in Eq. 8–9 is somewhat disconnected from the presentation.** The paper references Appendix A.2 for detailed derivation but Eq. 8 uses importance sampling ratios (p_θ / p_θ') without explaining the role of the old policy θ'. The reward function in Eq. 9 uses KNN and KL but the notation is ambiguous (KNN(x₀, x₀) compares the generated sample to itself?). Clarification is needed.

- **The comparison fairness claim needs nuance.** The paper states all models are re-trained with official settings, but GLIGEN and LayoutDiffusion are general-purpose natural image models. Their remote sensing performance may simply reflect domain mismatch rather than architectural inferiority. The most meaningful comparison is against AeroGen and CC-Diff.

- **The ESGM shape pool mechanism is underspecified.** Section 3.3 mentions "a lightweight mask pool collected during or after training" but the experiments use "masks generated during training." The practical implications of this choice and whether the pool degrades over time are not discussed.

- **Limited diversity analysis.** The paper claims improved diversity via DDPO but Figure 6 (diversity results) is in the appendix. A brief in-paper diversity comparison or quantitative diversity metric would strengthen the claim.

### Trivial

- Table 1 bold/underline formatting inconsistency (some best values bolded, some underlined with no clear convention distinguishing them).

## Nice-to-Haves

- A comparison of inference cost and speed relative to baselines would help assess the practical advantage of eliminating real-image references.
- Analysis of failure cases or categories where OF-Diff does not outperform baselines would provide a more complete picture.
- Sensitivity analysis of DDPO hyperparameters (k in KNN, ω in KL).

## Novel Insights

The paper's most interesting observation is that remote sensing objects exhibit quasi-invariant shapes across viewpoints (unlike natural images), which enables mask-based shape priors to serve as strong conditioning signals without requiring real instance patches at inference. The online-distillation framework that transfers knowledge from an image-conditioned decoder to a shape-only decoder is a reasonable architectural solution to the diversity-fidelity tradeoff. However, the individual components (shape priors from SAM, consistency distillation, DDPO) are established techniques, and the contribution is primarily in their specific combination and adaptation to the remote sensing domain rather than in fundamental methodological novelty.

## Suggestions

- Clarify the two identical-configuration rows in Table 4 — explicitly label which uses captions and which does not.
- Add a brief discussion of the consistency distillation relationship to prior work (e.g., consistency models) and articulate the specific architectural novelty.
- Provide the shape fidelity evaluation at higher resolution or with perceptual studies to validate that edge-map IoU improvements at 64×64 correspond to meaningful visual differences.
- Include inference time comparison to demonstrate the practical benefit of eliminating real-image references at sampling time.

## Score and Decision

The paper presents a solid empirical contribution to remote sensing layout-to-image generation with comprehensive evaluation and meaningful downstream improvements. The methodological novelty is incremental — combining established components (SAM-based shape extraction, consistency distillation, DDPO) in a domain-specific pipeline — but the practical impact for RS data augmentation is demonstrated convincingly. The main concern is the incomplete ablation table and the incremental nature of the technical contributions. Overall, this is a competent application paper with good experimental rigor.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept