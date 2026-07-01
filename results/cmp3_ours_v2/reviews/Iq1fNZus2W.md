Now I have a good calibration picture. Let me finalize the review.

## Summary
This paper tackles the quadratic computational bottleneck of multi-condition control in Diffusion Transformers (DiTs). The authors propose Patch-wise and Keyword-Aware Attention (PKA), which decomposes full attention into two specialized modules — Position-Aligned Attention (PAA, O(N) for spatial conditions) and Keyword-Scoped Attention (KSA, mask-pruned for subject conditions) — plus a condition KV cache and an early-timestep training sampling strategy. The method achieves up to 10× inference speedup and 5.12× VRAM reduction while maintaining or improving generative quality on a Subject200K subset.

## Strengths
1. **Well-motivated design from empirical attention analysis.** Figures 2 and 3 directly show diagonal-dominant attention for spatial conditions and localized activation for subject conditions, providing concrete evidence that full multi-condition attention is wasteful. The PAA/KSA decomposition follows naturally from this observation.
2. **Large, clearly documented efficiency gains.** Figures 7 and 8 show near-constant latency and VRAM as conditions scale from 1 to 16, while both baselines (OminiControl2, UniCombine) scale steeply. A 10× speedup and 5.12× VRAM reduction at 16 conditions is a genuine practical advance for multi-condition DiTs.
3. **Quality maintained despite substantial efficiency savings.** Table 1 shows PKA outperforms both baselines on most quality metrics (FID, SSIM, CLIP-I, DINOv2) across three multi-condition tasks, and is competitive on controllability (F1, MSE) and text fidelity (CLIP-T). This is non-trivial — efficient approximations often degrade quality visibly.

## Weaknesses

### Fatal
None.

### Major
1. **Multiple interacting components not ablated on the main quality benchmarks.** PKA bundles at least three mechanisms: (i) condition-only self-attention enabling a cross-timestep KV cache, (ii) PAA, and (iii) KSA. The existing ablations (Figures 9, 10) only compare variants on efficiency metrics (latency/VRAM), not on the quality metrics from Table 1 (FID, CLIP-I, DINOv2, F1, MSE). There is no ablation that isolates the condition KV cache contribution (e.g., PKA with the cache disabled but PAA/KSA retained), tests PKA with only one of PAA/KSA while the other uses full attention, or reports any Table 1 metric for an ablated configuration. Since the condition KV cache is a significant architectural departure enabled by the design choice that "condition tokens only perform self-attention within their respective conditions" (Section 3.2, line 81), its contribution to the headline efficiency and quality numbers is not separable from the rest of the system. This weakens the decomposition claims in Section 1.

2. **Early-timestep sampling strategy is evaluated only qualitatively.** The paper claims (Section 3.3, line 148–149) that this strategy "accelerates convergence and enhances the final model's control fidelity" and lists it as a contribution (Section 1, line 48). However, Section 4.3.3 and Figure 11 provide only visual comparisons across different μ and δ values. No FID, CLIP-I, controllability, or any other quantitative metric is reported comparing models trained with vs. without this strategy. Since the strategy is used in the main experiments, its contribution is baked into the Table 1 numbers without any way for the reader to assess whether it matters.

### Minor
1. **No variance or statistical significance reported.** All numbers in Table 1, Figure 9 (latency/VRAM), and Figure 10 (latency/VRAM) are single values with no standard deviations, confidence intervals, or indication of the number of independent runs. For generative models where quality and efficiency can vary across seeds/runs, this makes it difficult to assess whether small reported differences (e.g., CLIP-T: 0.352 vs. 0.349 vs. 0.348) are meaningful.

2. **FID scores are very high and not contextualized.** FID values range from 52.99 to 80.20, far above the <10–20 range typical of text-to-image models on standard benchmarks like MS-COCO. The paper does not report a text-only baseline (generation without visual conditions) on the same data or FID on a standard benchmark for calibration. While the relative comparison between methods is valid (all share the same evaluation setup), readers cannot interpret what these absolute numbers indicate about generation quality.

3. **KSA mask update schedule is underspecified.** KSA generates a mask at step t and reuses it at step t+1 citing "temporal consistency" (Zhou et al., 2025). The paper does not specify whether the mask is recomputed every two steps, every N steps, or only once at the first step, nor does it provide empirical validation of the reuse assumption (e.g., how much the mask changes between consecutive steps).

### Trivial
None.

## Nice-to-Haves
- Ablations isolating the condition KV cache and reporting quality metrics (Table 1 metrics) for each ablated configuration would sharply strengthen the evidence.
- Quantitative evaluation of the early-timestep sampling (FID/CLIP-I curves comparing shifted vs. standard logit-normal sampling).
- Reporting FID on a standard benchmark (e.g., MS-COCO with synthetic conditions) or a text-only baseline to contextualize absolute values.
- Clarifying the KSA mask recomputation frequency and providing empirical support for the reuse assumption.
- Reporting variance over multiple runs for key quantitative results.

## Removed Points
- The harsh critic's point that "the paper bundles at least four distinct contributions" was kept but the framing was adjusted. The condition KV cache is not listed as a separate contribution — it's a consequence of the architectural design. The core issue (missing component-level ablations) is retained as Major Weakness #1.
- The harsh critic's note about "O(c²n²) scaling not formally derived" is a minor presentational preference, not a substantive weakness. Removed.
- The harsh critic's note about "whether PAA/KSA could be combined with prior techniques" is scope creep — the paper is evaluated on what it proposes. Removed.
- The harsh critic's note about "KSA mask mechanism relies on text keywords being present in the prompt" — the paper explicitly curates a subset where captions contain keywords (Section 4.1, line 195), which is a valid experimental design choice. Removed.
- The harsh critic's note about "number of conditions in Table 1 not reported" — this is a reasonable question but was handled as a Nice-to-Have rather than a weakness.
- The harsh critic's note about "the specific values of μ and δ used in experiments are not stated" — Figure 11 shows μ=0.5, δ=1.5. The paper states μ>0, δ>1 generally. Demoted to a minor clarification, folded into Weakness #2 framing.
- All formatting, typo, and style nitpicks removed per instructions (these are parser artifacts, not author errors).
- Strengths that were generic ("the problem is real," "the problem is important") were merged into the existing concrete strengths.

## Novel Insights
The harsh critic insightfully identifies that the condition KV cache (enabled by condition-only self-attention) is a significant architectural departure from the bidirectional "concatenate-and-attend" paradigm — not just an optimization trick. Condition representations are computed without any influence from the noisy image or other condition types, yet the paper does not discuss whether this unidirectional information flow could limit the model's ability to jointly reason across conditions and generation. This observation correctly identifies a gap between how the paper frames PKA as a unified framework and what has actually been demonstrated about individual component contributions.

## Suggestions
1. Add ablations that isolate the condition KV cache: train PKA with the cache disabled (recompute condition KVs at each step) while retaining PAA/KSA, and report both efficiency (latency/VRAM) and quality (FID, CLIP-I, DINOv2) metrics.
2. Add an ablation training PKA with only PAA or only KSA (the other module using full attention) and report the main Table 1 metrics for each configuration.
3. Provide quantitative metrics (FID, CLIP-I, controllability) comparing models trained with the proposed early-timestep sampling vs. standard logit-normal sampling.
4. Report standard deviations over multiple runs for the key quantitative results in Table 1.
5. Add a text-only generation baseline or FID on a standard benchmark to contextualize the reported FID values.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>