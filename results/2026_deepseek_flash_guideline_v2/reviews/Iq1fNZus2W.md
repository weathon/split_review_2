Since the calibration data directory is not accessible, I'll proceed with my own calibrated assessment based on the paper content.

Let me finalize the consolidated review.

## Summary

The paper proposes Patch-wise and Keyword-Aware Attention (PKA), a framework that decomposes multi-condition attention in Diffusion Transformers into two specialized modules: Position-Aligned Attention (PAA) for spatial conditions (one-to-one attention at aligned positions) and Keyword-Scoped Attention (KSA) for subject conditions (attention restricted to keyword-activated regions). Together with a condition KV cache and an early-timestep sampling strategy, PKA achieves up to 10× inference speedup and 5.12× VRAM reduction for the attention module while claiming to maintain or improve generative quality.

## Strengths

1. **Empirically diagnosed attention sparsity that directly motivates the two-module decomposition.** The paper provides visual evidence (Figures 2-3) showing that spatial-condition attention is concentrated along the diagonal and subject-condition attention is localized to keyword-relevant regions. This analysis directly motivates the separate PAA and KSA modules rather than applying a single global sparsification scheme, and differentiates the work from prior efficient DiT methods based on token pruning or layer caching.

2. **Up to 10× speedup and 5.12× VRAM reduction with an increasing-condition trend.** Figures 7-8 plot inference time and VRAM against condition count (1 to 16), showing PKA's advantage grows with more conditions: speedup from 3.90× at 4 conditions to 10× at 16, and VRAM reduction from 2.46× to 5.12×. The full-attention baselines scale quadratically while PKA stays nearly flat, directly demonstrating that the method addresses the stated "concatenate-and-attend" bottleneck. This trend data, measured on a single GPU, is the paper's strongest evidence.

3. **Condition KV cache enabled by the structural design.** Because condition tokens only perform self-attention within their own condition type (Section 3.2), their Key and Value projections can be computed once in the first denoising step and cached for all subsequent steps. This is structurally different from earlier efficient DiT methods that rely on added heuristics like layer caching or token pruning.

4. **Perturbation analysis providing empirical grounding for the early-timestep sampling scheme.** Section 3.3 and Figure 5 show that perturbing early (high-noise) steps degrades SSIM faster than perturbing late steps, empirically demonstrating that visual conditions exert their strongest influence early in the denoising trajectory. This motivates the shifted logit-normal sampling distribution.

5. **Systematic ablation of the KSA mask threshold demonstrating a smooth efficiency-quality trade-off.** Figure 10 varies ε from 0.0 (w/o KSA, 16.99s, 368MB) to 0.8 (15.23s, 230MB), showing that the threshold provides intuitive and graceful control over the efficiency-quality balance rather than being a sensitive hyperparameter.

## Weaknesses

### Fatal
None.

### Major

1. **The quality comparison is confounded with training procedure differences.** The paper claims PKA "maintains or improves generative quality" and Table 1 shows substantially better FID, SSIM, CLIP-I, and DINOv2 across all three tasks. However, Section 4.1 describes training PKA with LoRA fine-tuning, a curated Subject200K subset, the Prodigy optimizer, gradient accumulation, and the proposed early-timestep sampling — while simply "employing" OminiControl2 and UniCombine as baselines without specifying whether they were retrained under identical conditions or used off-the-shelf. If baselines were not retrained with the same data, LoRA, optimizer, and timestep sampling, the quality improvements in Table 1 cannot be attributed to the attention architecture. The paper needs to either (a) retrain all baselines under identical conditions (same data, same LoRA training, same optimizer, same timestep sampling) with their own attention mechanisms, or (b) clearly separate the efficiency claim (well-supported by Figures 7-8) from the quality claim and acknowledge that quality differences may reflect training procedure improvements.

2. **The KSA mask recomputation schedule is underspecified in a way that affects the validity assessment.** Section 3.2.2 states the mask is computed at timestep *t* (Eq. 3) and reused at timestep *t+1* (Eq. 4), with the figure caption (Figure 4d) saying the mask is applied in "subsequent steps" (plural). It is unclear whether this is a recurring alternation pattern (compute at even steps, reuse at odd steps — the natural reading of the "two-step process" description) or a one-time computation at step 1 reused for all later steps. If the latter, the mask would be computed from pure-noise attention patterns and would not meaningfully localize the subject at later steps. The paper must specify the exact schedule, the recomputation overhead if any, and provide evidence (e.g., mask IoU between consecutive steps) that the temporal consistency assumption holds.

### Minor

3. **No variance or confidence information for any quantitative metric.** Table 1 reports point estimates for FID, SSIM, F1, MSE, CLIP-I, DINOv2, and CLIP-T without error bars, confidence intervals, or any indication of how many seeds/runs were averaged. FID in particular is known to be seed-dependent. Without variance estimates, the reader cannot assess whether the reported differences (e.g., FID 52.99 vs 61.03 for Subject-Canny) are statistically significant or could arise from run-to-run variation.

4. **PAA ablation lacks quality metrics.** Figure 9 reports only latency and VRAM for the PAA comparison against full attention and sliding window attention. The claim that PAA "delivers high-quality spatial control" is supported only by qualitative images, with no FID, SSIM, or controllability (F1/MSE) metrics alongside the efficiency numbers.

5. **Early-timestep sampling ablation is only qualitative.** Figure 11 shows visual results for different (μ, δ) settings at various training iterations but provides no learning curves, loss values, or quantitative control metrics to substantiate the claim that the sampling "accelerates convergence."

6. **The number of inference steps used for evaluation is not reported.** This matters because the condition cache savings depend on the total number of denoising steps (more steps = greater amortized benefit).

### Trivial
None.

## Nice-to-Haves
- Quantitative metrics (CLIP-I, DINOv2) for the KSA ε ablation across different threshold values.
- A quantitative convergence comparison for the early-timestep sampling (e.g., training loss curves or control metric vs. iterations for different μ, δ settings).
- A discussion of whether the restricted interaction paths (conditions only self-attend, no cross-condition attention) could limit certain forms of multi-condition reasoning where spatial and subject conditions must interact.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Up to 10× speedup should be contextualized more clearly"**: The paper already contextualizes this in Figure 7 (3.90× at 4 conditions, 6.46× at 8, 10× at 16). The abstract honestly says "up to 10×." The 10× figure is correctly tied to the 16-condition scenario. (Harsh Critic)

- **"PAA/KSA being the only interaction paths could limit cross-condition reasoning"**: Speculative and outside the paper's stated scope. The paper explicitly describes its design choice and does not claim to support cross-condition reasoning. (Harsh Critic)

- **"Formatting error in Table 1 (F1 column dash alignment)"**: A pure formatting artifact; most likely a LaTeX alignment issue in the PDF extraction, not a content error. (Harsh Critic)

- **"VRAM measurement is ambiguous"**: Figure 8 is clearly labeled "VRAM consumption of attention mechanism" and Section 4.1 says "Efficiency metrics, including inference latency and condition overhead, are measured on a single NVIDIA RTX 6000 Ada GPU." The measurement scope is stated. (Harsh Critic)

- **"Strength: the paper addresses an important problem"**: Generic/superficial strength lacking a specific citation to paper content. (Strength Finder)

- **"Canny-Depth-to-Image task tests PAA in isolation with no subject condition"**: This is a valid task choice; the paper does not claim KSA is applied there. Not a weakness. (Harsh Critic)

## Novel Insights

None beyond the paper's own contributions. The reviews surface the core tension between the paper's quality claims and the experimental design (conflated training procedures), but neither reviewer offers a fundamentally new observation about the method or its implications beyond what the paper already discusses.

## Suggestions
1. **(Required)** Clarify whether OminiControl2 and UniCombine baselines were retrained under identical conditions (same data, LoRA, optimizer, early-timestep sampling) or used off-the-shelf. If the latter, retrain them under controlled conditions or explicitly reframe the quality claims to acknowledge confounding.
2. **(Required)** Specify the KSA mask recomputation schedule precisely. Provide evidence (e.g., mask overlap statistics across steps) that the temporal consistency assumption holds and that the mask remains meaningful across reused steps.
3. **(Required)** Add variance estimates (error bars or confidence intervals) to all quantitative comparisons in Table 1 and ablation figures.
4. **(Recommended)** Report quality metrics (FID, SSIM, controllability F1/MSE) for the PAA ablation study alongside the latency/VRAM numbers already shown.
5. **(Recommended)** Report the number of inference steps used in evaluation.
6. **(Suggested)** Add learning curves or quantitative convergence data for the early-timestep sampling ablation.

## Score and Decision

The paper's core contribution — an efficient attention decomposition for multi-condition DiTs — is sound, the empirical motivation (attention sparsity analysis) is convincing, and the efficiency results (up to 10× speedup, 5.12× VRAM reduction) are well-supported by Figures 7-8. These results alone constitute a meaningful contribution: the method substantially reduces computation and memory for multi-condition control, and the advantage grows with the number of conditions.

However, the paper overreaches by claiming quality improvements alongside efficiency when the comparison is confounded by uncontrolled training procedure differences. The KSA mask schedule is also underspecified in a way that affects reproducibility. These issues are fixable but require substantive clarification and controlled experiments, not minor edits.

Compared to standard acceptance thresholds: the efficiency evidence is stronger than many accepted methods papers (due to the parametric efficiency-quality trade-off characterization), but the quality claims are weaker than they should be for a method that frames "maintaining or improving quality" as a core result. The paper would be a clear accept if the quality comparison issue were resolved.

**Score: 6** — Borderline accept. The efficiency contribution is real and well-demonstrated. The quality claims need to be disentangled from training procedure effects. With proper clarification and controlled experiments, the paper would be publishable at a higher score.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>