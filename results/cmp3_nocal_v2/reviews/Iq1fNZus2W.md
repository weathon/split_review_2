Now I'll write the final consolidated review.

## Summary

This paper tackles the computational bottleneck of multi-condition control in Diffusion Transformers (DiTs), where the standard "concatenate-and-attend" approach causes quadratic scaling with the number of conditions. The authors propose Patch-wise and Keyword-Aware Attention (PKA), which decomposes full attention into two specialized modules: Position-Aligned Attention (PAA) for spatially-aligned conditions (reducing O(N²) to O(N) per condition) and Keyword-Scoped Attention (KSA) for subject-driven conditions (pruning attention to keyword-relevant regions). These are complemented by a condition KV cache and an early-timestep sampling strategy for training. The paper reports up to 10× inference speedup and 5.12× VRAM reduction against a full-attention baseline.

## Strengths

1. **Well-motivated sparsity analysis.** The paper provides direct empirical evidence (Figures 2–3) that attention in multi-condition DiTs is highly sparse, with diagonal-dominant patterns for spatial conditions and localized activation for subject conditions. This analysis is concrete and convincingly justifies the architectural choices that follow. It is the paper's strongest contribution.

2. **Clean conceptual decomposition.** Categorizing conditions as "spatial-aligned" (layout maps, depth, edges) versus "subject-driven" (reference images) and designing separate mechanisms (PAA and KSA) that exploit different sparsity patterns is conceptually sound and grounded in the observed data. The two modules are genuinely different in approach.

3. **Practical condition KV cache.** Caching Key and Value projections for condition tokens after the first denoising step (enabled by the structural design where conditions only self-attend) is a practical insight that contributes substantially to the reported speedup. This is a clean extension of a known LLM technique to the DiT multi-condition setting.

## Weaknesses

### Fatal

None.

### Major

1. **Quality evaluation and efficiency evaluation operate in fundamentally different regimes.** Quality is assessed only on 2-condition tasks (Table 1: Subject-Canny, Subject-Depth, Canny-Depth). Efficiency scaling is shown up to **16 conditions** (Figures 7–8), where the largest speedups (6.46×, 10×) are claimed. The paper's central narrative — that PKA achieves large efficiency gains "while maintaining or improving generative quality" — is unsupported at the condition counts where those efficiency gains are largest. The 2-condition regime is precisely where full attention is least onerous and where PKA's speedup is most modest. Without quality evaluation at higher condition counts (e.g., 4+, 8+), the paper's primary claim linking efficiency and quality is incomplete. *(Section 4.1 vs. Figures 7–8)*

2. **The headline efficiency numbers are framed without adequate context.** The abstract, introduction, and conclusion present "up to a 10× inference speedup" without specifying the baseline. The experiments section (4.2.1) correctly states this is "compared to the full-attention mechanism in UniCombine" — a method with no caching or sparsity. Against the more relevant efficiency-optimized baseline OminiControl2, the speedup at 16 conditions is **~1.6×** (Figure 7: ~40s → ~25s). The paper does not prominently acknowledge this difference. A reader of the abstract alone would reasonably assume a 10× gain over all baselines. This is a significant framing problem. *(Abstract, lines 9–10; Introduction, line 43; Section 4.2.1, line 225)*

### Minor

3. **Controllability trade-off on Subject-Canny is downplayed.** On Subject-Canny, the F1 score (edge controllability) is 0.414 vs. UniCombine's 0.551 — a ~25% relative deficit. The paper dismisses this as "the minor exception of a narrow margin" (Section 4.2.3). This is not narrow. While FID, SSIM, and consistency metrics favor the proposed method, the controllability gap is substantial and suggests a real trade-off that deserves honest discussion rather than minimization. *(Table 1, line 258)*

4. **KSA's temporal mask reuse is an unvalidated architectural assumption.** KSA generates a binary mask at step \(t\) and reuses it at step \(t+1\) (Eq. 3–4), citing "temporal consistency of the denoising process." Diffusion models make large changes to latents between consecutive steps, especially in early (high-noise) timesteps where conditioning presumably matters most. The paper provides **no analysis** of mask stability — no IoU between consecutive masks, no comparison against an oracle that computes fresh masks at each step, and no analysis of how mask staleness propagates. The ablation in Figure 10 tests threshold \(\epsilon\) sensitivity, not the temporal reuse assumption. *(Section 3.2.2, lines 124–137)*

5. **The early-timestep perturbation experiment does not isolate conditioning-specific effects.** Figure 5 shows that perturbing early timesteps (High-to-Low) reduces SSIM more than perturbing late timesteps (Low-to-High). The paper interprets this as "visual conditions exert their strongest influence during the early, high-noise stages." An equally parsimonious explanation is general error propagation: any perturbation applied earlier in a sequential generative process has more steps to compound. Without a control (e.g., perturbing random tokens vs. condition tokens at the same timesteps), the evidence does not uniquely support the conditioning-specific conclusion. *(Section 3.3, Figure 5)*

6. **No variance or statistical significance reported.** Table 1 and all ablation tables report single-point estimates without standard deviations, confidence intervals, or significance tests. Some differences are small (e.g., CLIP-T: 0.349 vs. 0.352 on Subject-Canny), making it impossible to assess whether they reflect systematic effects or noise. *(Table 1, Figures 9–10)*

### Trivial

None.

## Nice-to-Haves

- Disentangle the sources of speedup: isolate the contribution of (a) PAA alone, (b) KSA alone, (c) condition cache alone, and (d) all combined.
- Validate KSA's temporal mask reuse by computing IoU between masks at consecutive steps across the full trajectory.
- Even if not evaluating quality at high condition counts in this version of the paper, add a clear limitation statement acknowledging that quality was only tested at 2 conditions.

## Removed Points

These points were raised in the input review but are removed with justification:

- *Missing experimental details (denoising steps, μ/δ hyperparameters, keyword selection procedure, test set size):* The parser strips appendix content from all papers. These details may exist in the original submission's appendix and cannot be verified or used as the basis for a weakness.
- *"Condition cache is not a novel contribution":* The cache mechanism is enabled by the paper's architectural redesign (conditions only self-attend), which is part of the contribution. KV caching in this specific setting is a reasonable contribution.
- *"PAA assumes perfect alignment (brittle)":* This is a stated design choice for spatial-aligned conditions, not an oversight. The method is explicitly scoped to conditions that can be spatially aligned. Criticizing it for not handling misaligned conditions is scope creep.
- *"The 10× comparison against UniCombine is a strawman":* UniCombine is a published baseline. Comparing against it is legitimate. The issue is framing (captured in Major weakness #2), not the legitimacy of the comparison.

## Novel Insights

The main novel insight from the reviews is that the paper's strongest evidence (the sparsity analysis in Figures 2–3) and its primary weakness (quality evaluated only at 2 conditions) are observationally connected: the sparsity analysis is performed on the same 2-condition setting, so it is unclear whether the observed sparsity patterns generalize to higher condition counts where efficiency claims are largest. If attention becomes less sparse with more conditions, the architectural assumptions underpinning PAA and KSA may not hold in the regime the paper highlights. This connection between the evidence gap and the motivating analysis is not made explicit in the input reviews but is worth noting.

## Suggestions

1. Add quality evaluation (FID, controllability metrics) at 4+ and 8+ condition settings to support the claim that quality is maintained at high condition counts.
2. Reframe the headline efficiency numbers to always specify the comparison baseline, or use the speedup over the strongest efficient baseline (OminiControl2) as the primary figure and relegate the UniCombine comparison to the supplement.
3. Provide variance estimates (≥3 seeds) for at least the main quantitative results.
4. Validate or discuss the KSA temporal mask reuse assumption directly.
5. Honestly discuss the F1 trade-off on Subject-Canny rather than characterizing it as a minor exception.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>