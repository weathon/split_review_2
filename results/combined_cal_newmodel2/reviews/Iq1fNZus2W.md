## Summary

This paper introduces PKA (Patch-wise and Keyword-Aware Attention), a framework for efficient multi-condition control in Diffusion Transformers. It decomposes the costly "concatenate-and-attend" strategy into two specialized attention modules: Position-Aligned Attention (PAA), which reduces complexity from O(N²) to O(N) for spatial conditions by computing attention only between aligned patches, and Keyword-Scoped Attention (KSA), which restricts subject-driven attention to keyword-activated regions via temporal mask reuse. The paper also proposes an early-timestep sampling strategy to accelerate fine-tuning. Evaluated on the FLUX.1 model, PKA reports up to 10× inference speedup and 5.12× VRAM reduction for the attention module while maintaining or improving generative quality.

## Strengths

- **Well-motivated problem with empirical evidence of attention sparsity (Figures 2, 3).** The paper identifies two distinct redundancy patterns — diagonal-localized attention for spatial conditions and sparse region-localized attention for subject conditions — and directly justifies the PAA and KSA designs from these observations. This is the paper's strongest aspect: the method follows naturally from observed sparsity rather than being an arbitrary efficiency hack.

- **Principled decomposition of attention into PAA and KSA.** Reducing complexity from O(N²) to O(N) for spatial conditions via PAA, and using temporal mask reuse for subject conditions via KSA, are both clean, well-matched to the two condition types. The module designs follow naturally from the observed sparsity patterns.

- **Condition KV cache is a clean structural consequence** of the redesigned attention flow (conditions attend only to themselves), not an add-on trick. This is a genuine architectural advantage that emerges naturally from the decomposition.

- **KSA threshold ablation (Figure 10)** provides a clear efficiency-quality trade-off curve, helping users make informed deployment decisions. The study of ε shows a graceful quality-efficiency trade-off rather than an abrupt drop.

## Weaknesses

### Major

- **Ablation studies (PAA in Figure 9, KSA in Figure 10) report only efficiency metrics (latency, VRAM) and qualitative image comparisons.** No quantitative quality metrics (FID, SSIM, CLIP-I, DINOv2) are provided for the ablation conditions. The paper's central claim of "maintaining generative quality" is not quantitatively tested in the ablations — we cannot tell whether the PAA and KSA modules preserve quality relative to full-attention baselines because the evidence is purely visual. This is the most significant evaluation gap.

- **The condition KV cache, a major contributor to the reported speedup, is never ablated separately.** The paper does not decompose the efficiency gains into contributions from PAA, KSA, and the cache, making it impossible to attribute the improvements. The cache is a simple optimization (compute KV once, reuse thereafter) that could be applied to many methods; isolating its effect is important for understanding the genuine contribution of the proposed attention modules.

- **The baseline comparison protocol is underspecified.** Section 4.1 describes training details (LoRA, 20K iterations, Prodigy optimizer) for the authors' method but does not state whether OminiControl2 and UniCombine were also fine-tuned on the same Subject200K subset with the same training budget, or whether off-the-shelf checkpoints were used. Without this information, the quality comparisons in Table 1 could reflect training data disparity rather than architectural merit.

### Minor

- **The scope of efficiency claims is ambiguous.** The abstract claims "up to a 10× inference speedup" without qualification, while the VRAM claim (5.12×) is explicitly scoped to "attention module." Figure 7 measures "Time consumption" but does not state whether this is attention-only or end-to-end inference time; Figure 8 explicitly labels "VRAM consumption of attention mechanism," creating an inconsistency. If the 10× figure is attention-only, the end-to-end speedup would be substantially smaller. The paper should clarify what is being measured and ideally report end-to-end numbers.

- **The early-timestep sampling strategy (Section 3.3) is evaluated only qualitatively (Figure 11).** No quantitative comparison (FID, SSIM, CLIP scores) is provided for models trained with vs. without this strategy. While the motivation (shifting training toward early timesteps) is plausible, the claimed benefit is not supported by measurements.

- **FID scores in Table 1 (52.99–80.20) are unusually high.** The test set size is not reported, nor are confidence intervals provided. While the relative ordering between methods is consistent (Ours < UniCombine < OminiControl2 across all tasks), the absolute values raise questions about the evaluation protocol and metric stability on this dataset.

- **Key methodological details are missing:** (a) how keyword tokens K are identified/extracted from the text prompt for KSA (Section 3.2.2), (b) the specific μ and δ values used for early-timestep sampling in the main experiments, (c) the size of the training/test subset from Subject200K. These affect reproducibility.

- **The MSE values for depth controllability in Table 1 (e.g., 366, 312, 160, 114) are unnormalized** and presented without context, making it impossible to assess what constitutes a "good" score.

### Trivial

None.

## Nice-to-Haves

- Report end-to-end inference time and total GPU memory alongside attention-specific numbers to clarify the scope of efficiency claims.
- Ablate the condition KV cache separately to decompose efficiency gains.
- Provide quantitative quality metrics (FID, SSIM, CLIP-I) for the PAA and KSA ablations.
- Normalize MSE values for depth controllability or provide calibration context.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. Criticism about the early-timestep perturbation study adding noise to the image vs. conditions: The paper states "Visual condition perturbation" — the reviewer's claim about noise being added to the image rather than the condition is not verifiable from the paper text and may reflect a misunderstanding.
2. PAA assumes same-resolution alignment: This is by design for the intended use case, not a weakness.
3. Observation about OminiControl2's VRAM approaching UniCombine's at high condition counts: This concerns baseline behavior, not a weakness of the proposed method.
4. Missing LoRA rank, image resolution, number of denoising steps: These are standard implementation details considered trivial per the nitpick rule.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add quantitative quality metrics (FID, SSIM, CLIP-I) to the PAA and KSA ablations to substantiate the "maintaining quality" claim.
2. Ablate the condition KV cache separately to decompose efficiency gains into cache vs. PAA vs. KSA contributions.
3. Clarify whether the time measurements in Figure 7 are attention-only or end-to-end, and report end-to-end numbers if not already doing so.
4. Specify the keyword extraction process and report μ/δ values used in experiments.
5. Report the test set size and consider bootstrapped confidence intervals for FID.
6. State explicitly whether baselines were fine-tuned on the same data with the same budget.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| UniCon | uJqKf24HGN.md | 7.00 (Accept) | R1 | Yes | Similar topic (efficient DiT control); fewer/weaker weaknesses; higher score |
| Qihoo-T2X | lTrrnNdkOX.md | 6.40 (Accept) | R1 | Yes | Similar topic (efficient DiT via token reduction); one major missing-ablation weakness (fav 0.17) comparable to our 0.21; accepted |
| LEGO Bricks | qmXedvwrT1.md | 6.67 (Accept) | R2 | Yes | Efficient reconfigurable diffusion; similar weakness profile (fav 0.14 for limited experiment scope); accepted |
| LinFusion | D2as3jDmRA.md | 6.25 (Reject) | R1 | Yes | Linear attention for diffusion; similar missing-ablation weakness (fav 0.72, 0.89); rejected despite 6.25 |
| MDiT | leBbjaUxut.md | 5.00 (Reject) | R2 | Yes | Multi-scale DiT architecture; missing ablation weakness (fav 0.20); rejected |
| Highlight Diffusion | Jt1gGIumJo.md | 3.00 (Reject) | R1 | Yes | Attention-guided acceleration for T2I; much weaker method and results |

Round-1 bracket: 5.5–7.5.

Round 2 narrowed to ~6.0 by comparing rated items: our paper's four strengths (fav 9–12) are comparable to Qihoo-T2X and LEGO Bricks (both accepted at ~6.4–6.7). However, our paper has more weaknesses than either: two very low favorability items (0.21 for missing quality metrics in ablations, 0.37 for cache not ablated) and several moderate items (2.6–4.1). This places it slightly below those anchors. Against LinFusion (6.25, rejected), our paper has stronger core novelty (specialized attention decomposition based on sparsity analysis vs. adapting existing linear attention), which justifies a similar score with a different outcome. The evaluation gaps are fixable and do not invalidate the core contribution.

**Final score: 6.0** — borderline accept. The method is novel, well-motivated, and the efficiency gains are real. However, the evaluation has several gaps (ablation studies missing quantitative quality metrics, condition cache not isolated, baseline protocol unclear) that prevent the evidence from fully supporting the strength of the claims. The paper would be strengthened by addressing the Major weaknesses listed above.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>