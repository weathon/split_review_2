Now I have enough calibration data. Let me finalize the review with the score.

Based on my analysis:

**Round-1 bracket**: I place this paper between **5.0 and 6.5**. The paper has genuine strengths (principled architectural decomposition, KV-cache application, clear efficiency gains) comparable to the UniCon anchor (7.00) in strength quality, but the weaknesses are more substantial — the quality/efficiency regime mismatch, unclear baseline fairness, and thin early-timestep evidence all drag the score below UniCon.

**Round-2 narrowing**: Comparing against DyDiT (5.50) and Qihoo-T2X (6.40):
- My strengths (9.00–10.34) are comparable to DyDiT's (8.13–10.25) and Qihoo's (6.87–12.90)
- My worst weakness (-0.92, early-timestep lacking validation) is more negative than DyDiT's worst (1.04) but less negative than Qihoo's worst (-3.87)
- My paper has three major weaknesses with negative/low favorability (0.79, -0.04, -0.92), while DyDiT's lowest is 1.04 and Qihoo has some very negative items (-3.87) balanced by very high strength items (12.90)

The deciding factor: the quality/efficiency regime mismatch (favorability=0.79) is a structural validation gap that directly undermines the paper's central claim ("maintaining quality while achieving large efficiency gains"). The baseline fairness issue (-0.04) raises concerns about Table 1's validity. Together these bring the paper to around **5.5**, consistent with a paper that has a solid architectural contribution but incomplete experimental support for its headline claims.

Let me now write the final review.

All anchors retrieved:
1. UniCon (uJqKf24HGN) — avg 7.00, Round 1, itemized ✓ — most directly relevant; about efficient control of DiTs; my paper has similar strength quality but worse weaknesses
2. SANA (N8Oj1XhtYZ) — avg 8.50, Round 1, itemized ✓ — strong efficient DiT paper; my paper is much weaker
3. Efficient Scaling of DiTs (iG7qH9Kdao) — avg 5.00, Round 1, itemized ✓ — empirical scaling study; different type of contribution
4. DyDiT (taHwqSrbrb) — avg 5.50, Round 2, itemized ✓ — efficient DiT inference; my weaknesses are worse than its worst
5. Qihoo-T2X (lTrrnNdkOX) — avg 6.40, Round 2, itemized ✓ — efficient DiT attention; has very negative items (-3.87) but balanced by very strong items
6. Dynamic Diffusion Transformer (from Round 2) also found
7. Others from Round 1 and 2 that are less topically relevant

Let me finalize at 5.5.## Summary

This paper addresses the computational bottleneck of multi-condition control in Diffusion Transformers (DiTs), where the "concatenate-and-attend" strategy leads to quadratic scaling in attention cost. The authors propose Patch-wise and Keyword-Aware Attention (PKA), which decomposes full attention into two specialized modules: Position-Aligned Attention (PAA) for spatial conditions and Keyword-Scoped Attention (KSA) for subject-driven conditions. PAA exploits diagonal-dominant attention patterns by computing attention only between spatially aligned patches, while KSA uses a keyword-derived mask to restrict subject attention to salient regions. A condition KV cache and an early-timestep sampling strategy complement the framework. Experiments on FLUX.1 show up to 10× inference speedup and 5.12× VRAM reduction.

## Strengths

- **Well-motivated problem and clean architectural insight.** The paper identifies that spatial condition attention is diagonal-dominated (Figure 2) and subject condition attention is spatially sparse (Figure 3) in DiTs. Rather than applying a generic pruning heuristic, PAA and KSA directly mirror the observed sparsity patterns — this is a principled approach to efficiency grounded in attention analysis. **[favorability=9.00]**

- **The decomposition enables a useful KV-cache trick.** By restricting condition tokens to self-attention within their own type (Section 3.2), the paper enables caching of condition Key and Value projections after the first denoising step. This is a clean application of a standard LLM technique to the DiT setting, correctly motivated and practically relevant. **[favorability=9.66]**

- **Efficiency numbers are large and clearly visualized.** Figures 7 and 8 show that as the number of conditions increases, the proposed method's cost stays nearly flat while baselines grow steeply. The gap at 16 conditions (10× speedup, 5.12× VRAM reduction for the attention module) is striking and well-presented. **[favorability=10.34]**

## Weaknesses

### Fatal
None.

### Major

- **Quality evaluation mismatch with efficiency regime.** The efficiency comparison (Figures 7–8) uses up to 16 conditions, but the generative quality evaluation (Table 1) tests only 2-condition tasks (Subject-Canny, Subject-Depth, Canny-Depth). At 2 conditions the efficiency advantage is smallest (3.90× speedup, 2.46× VRAM), while the headline claims (10× speedup, 5.12× VRAM) are demonstrated only at 16 conditions with no quality evaluation. The paper's central claim that "quality is maintained while achieving large efficiency gains" cannot be assessed in the regime that produces those large gains. This is the most significant weakness because it means the core claim is untested where it matters most. **[favorability=0.79]**

- **Baseline comparison fairness is unclear.** Section 4.1 states "we fine-tune the FLUX.1 model using LoRA" and separately lists OminiControl2 and UniCombine as baselines, but never specifies whether these baselines were (a) fine-tuned on the same Subject200K subset with the same LoRA/Prodigy setup, or (b) evaluated off-the-shelf with their original weights. If (b), the comparison in Table 1 is unfair: the proposed method benefits from task-specific fine-tuning while the baselines do not, and the qualitative observations ("OminiControl2 suffers from lower visual fidelity", "UniCombine outputs exhibit a muted color palette") are exactly what one would expect from an unfair comparison. **[favorability=-0.04]**

- **Early-timestep sampling lacks quantitative validation.** This is presented as a contribution on equal footing with PAA and KSA (Section 3.3), but its evidence is limited to a qualitative visual comparison in Figure 11 for three (μ, δ) settings. There are no quantitative results: no FID, no CLIP scores, no ablation measuring final model quality with vs. without the shifted distribution. Given that this is claimed to "accelerate convergence and enhance control fidelity," the evidence is insufficient. **[favorability=-0.92]**

### Minor

- **Unexplained data point in PAA ablation.** In Figure 9, the column labeled "swa condition" achieves 13.58s latency and 198MB VRAM — better than PAA on both metrics (13.63s, 237MB). This column is never defined or discussed in the text. The caption lists seven conditions without explaining this entry, making it unclear whether this is an error, an alternative configuration, or a genuine competitor that outperforms the proposed method. **[favorability=2.10]**

- **KSA mask temporal scope is ambiguous.** Section 3.2.2 states the mask is computed at timestep t and reused "at timestep t+1", but the Figure 4 caption says it is "applied in subsequent steps" (plural). The scope of reuse — every other step, or once and forever — is not specified. This matters for both efficiency and reliability: if the mask is reused across many steps while the image changes substantially, it could become stale. **[favorability=7.04]**

- **No variance or confidence intervals on any result.** No error bars are reported for any numeric metric (Table 1, ablation tables). Given that some comparative gains are described as "nuanced," the absence of statistical uncertainty estimates makes it difficult to assess whether observed differences are meaningful. **[favorability=3.09]**

- **Keyword extraction for KSA is not specified.** Section 3.2.2 describes mask generation from keyword tokens but does not explain how keywords are identified from the text prompt. The dataset is curated to ensure each caption "contains a descriptive keyword" (Section 4.1), implying the keyword is known a priori. This sidesteps the harder problem of automatic keyword extraction and limits applicability to arbitrary prompts without manual annotation. **[favorability=1.14]**

### Trivial
None.

## Nice-to-Haves

- Evaluate generative quality (FID, CLIP-I/DINOv2, controllability metrics) at higher condition counts (4, 8, 16) to match the efficiency evaluation regime.
- Clarify baseline training status; if baselines were used off-the-shelf, explain why the comparison is fair and characterize training data overlap.
- Add quantitative ablation results (FID, CLIP scores) for the early-timestep sampling strategy, or reposition it as a minor practical observation.
- Define the "swa condition" column in Figure 9.
- Specify the KSA mask reuse schedule (every step? every k steps? once?) and discuss potential staleness.
- Add failure case analysis for PAA (e.g., spatial conditions requiring non-local interactions) and KSA (e.g., mask accuracy at very early noise levels).

## Removed Points

These points are flagged to be removed, treat them with caution:
- "The FID values in Table 1 are very high (52–80) by modern standards" — Speculative; FID depends on dataset, resolution, and computation protocol, which are not specified in sufficient detail for this criticism to be anchored.
- "The 'Controllability' for Subject-Canny uses F1 while Subject-Depth uses MSE — these are different scales and cannot be compared across tasks" — Different metrics for different modalities (edge vs. depth) is standard practice; this does not weaken the paper.
- "the claim that visual conditions matter most at early timesteps is already well-known... the paper does not acknowledge this prior knowledge" — The paper provides its own empirical evidence (Figure 5, perturbation analysis); whether this is well-known is outside the paper's evaluation scope and cannot be verified from the paper alone.
- General speculation about confounders or proxy measurement — not anchored to specific content in the paper.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the structural gap between the efficiency and quality evaluations (quality tested at 2 conditions, efficiency at up to 16), but this is an observation about the paper's experimental design rather than a novel insight about the method.

## Suggestions

1. **Most important**: Evaluate generative quality at 4, 8, and 16 conditions to match the efficiency regime. This would directly test the paper's central claim.
2. Clarify whether OminiControl2 and UniCombine were fine-tuned on the same data. If not, either re-run the comparison with equivalent fine-tuning or acknowledge the limitation and discuss its implications.
3. Either add quantitative ablation results for early-timestep sampling (FID/CLIP across different μ, δ settings) or demote it from a claimed contribution to a practical observation.
4. Explain the "swa condition" column in Figure 9—resolve whether it's an error or a competitive alternative.
5. Specify the KSA mask reuse schedule precisely and discuss potential staleness over multiple denoising steps.

## Score and Decision

**Anchors used for calibration:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uJqKf24HGN.md` (UniCon) | 7.00 | R1 | ✓ | Most topically similar; both address efficient control of DiTs. My paper has comparable strengths but worse weaknesses (my worst at -0.92 vs UniCon's worst at -0.12). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/N8Oj1XhtYZ.md` (SANA) | 8.50 | R1 | ✓ | Efficient DiT paper with much stronger experimental validation; my paper is significantly weaker. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iG7qH9Kdao.md` (Efficient Scaling) | 5.00 | R1 | ✓ | Empirical study with minimal technical contribution; my paper has stronger method contribution but worse validation gaps. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/taHwqSrbrb.md` (DyDiT) | 5.50 | R2 | ✓ | Efficient DiT inference; my weakest items (-0.92) are more negative than DyDiT's worst (1.04), while strengths are comparable. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lTrrnNdkOX.md` (Qihoo-T2X) | 6.40 | R2 | ✓ | Efficient DiT attention; has very negative items (-3.87) balanced by very strong items (12.90). My paper has less extreme items on both ends. |

**Bracketing**: Round 1 placed the paper between 5.0 and 6.5. Round 2 narrowed by comparing with DyDiT (5.50) and Qihoo-T2X (6.40). My paper's three major weaknesses (favorability 0.79, -0.04, -0.92) are collectively more negative than DyDiT's worst weakness (1.04), which aligns the paper closer to the lower end of the bracket. The paper's strengths (9.00–10.34) are genuine but do not offset the structural validation gap: the central claim about maintaining quality under high-condition-count scenarios is untested where the efficiency gains are largest.

**Final calibration**: The paper has a well-motivated method with clear efficiency gains, but the experimental validation is incomplete in ways that directly affect its core claims. This places it at **5.5** — a borderline paper that presents a solid architectural contribution undermined by incomplete evidence for its headline claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>