The calibration search tool appears to have a persistent file access issue. I'll proceed with careful manual calibration based on my knowledge of typical ICLR scoring standards. Let me now write the final consolidated review.

**Manual calibration reasoning:** Based on the paper's content, the efficiency gains (3.9-10× speedup, 2.46-5.12× VRAM reduction) are genuinely impressive. The method is empirically motivated by attention-pattern analysis, and the architectural contributions (PAA, KSA, condition cache) are concrete. The quality metrics largely improve over baselines. However, the understated F1 trade-off, underspecified baseline training protocol, and purely qualitative early-timestep sampling evaluation are non-trivial issues that prevent a score in the strong accept range (8-10). Conversely, the core idea is sound and well-demonstrated enough to be above the reject range (1-4). The paper sits in the borderline-to-accept range (5.5-7).

Here is the final consolidated review:

## Summary
This paper proposes Patch-wise and Keyword-Aware Attention (PKA), a framework for efficient multi-condition control in Diffusion Transformers (DiTs). PKA decomposes the expensive "concatenate-and-attend" computation into two specialized sparse-attention modules: Position-Aligned Attention (PAA) for spatial conditions (one-to-one attention at aligned positions) and Keyword-Scoped Attention (KSA) for subject conditions (attention only in keyword-activated regions). A condition KV cache reuses Key/Value projections across denoising steps, and an early-timestep sampling strategy shifts the training distribution to prioritize high-noise phases. Evaluated on FLUX.1 with multiple multi-condition tasks, PKA achieves 3.9-10× inference speedup and 2.46-5.12× VRAM reduction while improving or maintaining generation quality on most metrics.

## Strengths
1. **Empirically motivated architectural design via attention-pattern analysis** — The paper does not assume sparsity generically; it explicitly analyzes attention matrices in prior multi-condition DiTs (Section 1, Figures 2-3), confirming that spatial-condition attention is diagonally concentrated while subject-condition attention is sparse and keyword-correlated. This analysis directly drives the design of two distinct modules (PAA and KSA) rather than applying a generic sparsity heuristic.

2. **Condition Cache mechanism enabled by structural attention decomposition** — By redesigning the attention structure so condition tokens perform self-attention only within their own condition type (Figure 4b), the paper unlocks a practical KV cache: Key/Value projections are computed once at the first denoising step and reused in all subsequent steps (Section 3.2). This is a concrete architectural novelty beyond token pruning or layer removal.

3. **Simultaneous efficiency gains and quality improvements on multiple tasks** — Table 1 shows PKA not only reduces computation (Figures 7-8: up to 10× speedup, 5.12× VRAM reduction) but also improves FID, SSIM, CLIP-I, and DINOv2 scores over both OminiControl2 and UniCombine across Subject-Canny, Subject-Depth, and Canny-Depth tasks. For instance, on Subject-Canny, FID drops from 61.03 (UniCombine) to 52.99 (Ours), and DINOv2 rises from 0.901 to 0.926.

4. **Perturbation analysis grounding the early-timestep sampling** — Figure 5 provides direct empirical evidence that perturbing early (high-noise) timesteps degrades SSIM substantially more than perturbing late timesteps, supporting the claim that visual conditions exert strongest influence early in denoising and motivating the shifted logit-normal training distribution (Section 3.3).

5. **PAA ablation against sliding window attention (SWA)** — Section 4.3.1 compares PAA not only against full attention but also against SWA with window sizes 1, 2, and 3, showing PAA achieves lower latency (13.63s vs 14.00s for SWA-1) and lower VRAM (237MB vs 276MB) while producing qualitatively comparable outputs.

6. **KSA threshold ablation showing graceful trade-off** — Figure 10 varies the KSA mask threshold ε from 0.2 to 0.8 and reports both efficiency metrics (latency drops from 16.99s to 15.23s, VRAM from 368MB to 230MB) and qualitative results, showing subject fidelity degrades only in subtle fine-detail differences rather than collapsing abruptly.

## Weaknesses

### Fatal
None.

### Major
1. **Subject-Canny F1 drop is significantly understated.** On the Subject-Canny task (Table 1), canny controllability (F1) drops from 0.551 (UniCombine) to 0.414 (Ours) — a ~25% relative decline and the largest single gap in the entire table. The paper describes this as "a narrow margin" (line 249). This is a meaningful cost of the efficiency gain: in PKA, spatial and subject conditions are processed independently with no cross-attention between them, so spatial controllability degrades noticeably when a subject condition is also present. The paper neither acknowledges this structural limitation nor discusses it as a trade-off. This does not invalidate the core contribution, but the presentation is misleading and the limitation should be honestly characterized.

2. **Baseline training procedure is underspecified.** The paper states "To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA" (lines 197-198) but does not clarify whether OminiControl2 and UniCombine underwent the same LoRA fine-tuning on the same data subset, or were used as pre-trained off-the-shelf models. If baselines were not comparably fine-tuned, the quality metrics (FID, SSIM, CLIP-I, DINOv2) could reflect dataset distribution mismatch rather than genuine method superiority. This must be clarified in the rebuttal.

3. **The early-timestep sampling contribution lacks quantitative validation.** Section 3.3 presents early-timestep sampling as a methodological contribution on par with PKA (it appears in the contribution list in the introduction). However, Figure 11 shows only qualitative image grids for different (μ, δ) configurations at varying iteration counts. There are no quantitative metrics — no FID, SSIM, convergence curves, or controllability scores — to support the claims that the strategy "accelerates convergence" and "enhances control fidelity." A quantitative ablation on at least one task is necessary to validate this as a distinct contribution.

### Minor
4. **Unexplained "swa condition" column in PAA ablation.** Figure 9 includes a column labeled "swa condition" that achieves better efficiency than the proposed PAA (13.58s, 198MB vs. PAA's 13.63s, 237MB). The paper provides no explanation of what this variant is, how it differs from the other SWA variants (window sizes 1, 2, 3), or why it is not preferred if it is both faster and more memory-efficient. This omission undermines the clarity of the ablation analysis.

5. **KSA's dependency on text-to-image attention map accuracy not discussed.** KSA (Section 3.2.2) uses text keyword attention maps to generate a mask that localizes subject-driven attention. If the text keyword is ambiguous (e.g., "person" in a crowd scene with multiple people), or if the description does not precisely localize the visual subject, the mask may be incorrect and subject-condition information applied to wrong regions or omitted entirely. This failure mode is not discussed.

6. **Condition Cache quality impact not analyzed.** The condition KV cache (Section 3.2) reuses condition token K/V projections after the first denoising step for all subsequent steps. While the noisy image changes significantly across the denoising trajectory, no analysis is provided on whether this caching approximation degrades quality relative to recomputing condition representations at each step.

7. **No statistical significance or variance reported.** All quantitative results appear to be from single runs. Without variance estimates, it is impossible to assess whether observed differences between methods (including the F1 gap on Subject-Canny) are reliable.

8. **KSA threshold ablation lacks quantitative subject consistency scores.** Figure 10 varies ε from 0.2 to 0.8 and reports efficiency metrics, but does not report corresponding quantitative subject consistency scores (CLIP-I, DINOv2). The claim that "the generated image remains highly faithful" at higher ε relies entirely on visual inspection of two examples.

### Trivial
None.

## Nice-to-Haves
- An end-to-end latency breakdown at realistic condition counts (2-4 conditions) would help practitioners assess practical speedup.
- A controlled experiment varying whether spatial and subject conditions are redundant, complementary, or conflicting would clarify whether the F1 drop is fundamental or can be mitigated.

## Removed Points
These points were flagged during review but removed; treat them with caution:

- **FID computation is "not the standard protocol"** — REMOVED. Computing FID between generated and ground-truth image sets is a standard evaluation for conditional generation. The high absolute values are likely due to the small evaluation subset, and the relative comparison across methods (all using the same protocol) is valid.
- **Abstract should distinguish peak vs typical speedup** — REMOVED. The abstract states "up to a 10× inference speedup," which correctly indicates the peak case. This is standard practice.
- **PAA vs SWA-1 improvements are "incremental"** — REMOVED. While individual module improvements are modest, the main contribution is the full system (PAA+KSA+Cache), which achieves substantial end-to-end gains.
- **Missing related works** — REMOVED per policy (cannot be independently verified).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a controlled experiment and explicit discussion of the Subject-Canny F1 trade-off, including analysis of when spatial and subject conditions may conflict.
2. Clarify the baseline training protocol: state explicitly whether OminiControl2 and UniCombine were fine-tuned with LoRA on the same subset, or used off-the-shelf.
3. Add quantitative metrics (FID, controllability scores) for the early-timestep sampling ablation in Figure 11.
4. Explain the "swa condition" column in Figure 9.
5. Add variance estimates (e.g., over multiple seeds) to key quantitative results.
6. Discuss failure modes of KSA when keyword attention maps are inaccurate.
7. Add an ablation or analysis of the condition cache approximation's impact on generation quality.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>