Now let me write the final review based on my thorough analysis of the paper and calibration.

## Summary

This paper proposes Patch-wise and Keyword-Aware Attention (PKA) for efficient multi-condition control in Diffusion Transformers. PKA decomposes full multi-condition attention into Position-Aligned Attention (PAA, O(N) one-to-one correspondence for spatial conditions) and Keyword-Scoped Attention (KSA, keyword-masked sparse attention for subject conditions), complemented by a Condition Cache mechanism and early-timestep sampling strategy. Built on FLUX.1 with LoRA, it reports up to 10× attention-module speedup and 5.12× attention-module VRAM reduction.

## Strengths

- **Well-motivated by concrete attention pattern analysis**: Figures 2 and 3 provide direct empirical evidence that attention in multi-condition DiTs is redundant — diagonal-dominant for spatial conditions and sparse/keyword-correlated for subject conditions. This motivates the PAA/KSA decomposition through observed structure rather than post-hoc rationalization.

- **Significant, scaling efficiency gains with quantitative evidence**: Figures 7 and 8 show speedup from 3.90× to 10× and VRAM reduction from 2.46× to 5.12× as conditions increase from 4 to 16, compared to UniCombine and OminiControl2. The gains grow with condition count, directly addressing the quadratic scaling bottleneck.

- **Best-in-class quality on most metrics across all tasks**: Table 1 shows PKA achieves the best FID (52.99 vs 61.03), SSIM (0.553 vs 0.493), CLIP-I (0.945 vs 0.912), and DINOv2 (0.926 vs 0.901) on Subject-Canny, with similar superiority on Subject-Depth (best FID, SSIM, MSE, CLIP-I, DINOv2) and Canny-Depth (best on all metrics except CLIP-T).

- **Architecturally clean design enabling Condition Cache**: The structural decision that condition tokens (SP, SJ) only self-attend within their own type (Section 3.2, Figure 4(b)) enables a KV cache where condition projections are computed once and reused across denoising steps — a non-trivial design insight contributing substantially to efficiency.

- **Perturbation analysis grounding the training strategy**: Figure 5 provides direct evidence that visual conditions exert strongest influence during early (high-t) denoising stages ("High-to-Low" causes SSIM degradation from 0.50 to 0.38 in 7 steps, while "Low-to-High" remains stable at 0.50 to 0.49), motivating the shifted logit-N(μ, δ) sampling.

## Weaknesses

### Fatal

None

### Major

- **F1 regression on Subject-Canny is the largest single-metric gap but dismissed as "narrow"**: Table 1 shows PKA achieves F1 of 0.414 vs UniCombine's 0.551 on Subject-Canny — a 25% relative drop in edge controllability. The paper describes this as "the minor exception of a narrow margin on the Subject-Canny task" (Section 4.2.3). This is in fact the largest single-method, single-metric gap in the entire table. For a method whose core promise is controllability, this regression in edge-based spatial control demands analysis — e.g., whether PAA's strict one-to-one correspondence (which eliminates cross-patch attention at boundaries where edges are most informative) is the cause, and whether a small local window would recover it. The paper provides no such analysis.

- **Efficiency and quality evaluated in different regimes**: The headline claims (10× speedup, 5.12× VRAM reduction) are measured at up to 16 conditions with 1024 tokens each (Figures 7-8), while all quality evaluations (Table 1, Figure 6) are conducted only on 2-condition tasks. The paper never evaluates whether generation quality is maintained at the condition scales where headline speedup numbers are obtained. Additionally, no end-to-end inference time or total VRAM figures are reported — the abstract's "up to 10× inference speedup" is qualified as attention-module-only only in the conclusion (Section 5). This makes the efficiency claims ungrounded from the quality perspective and vice versa.

- **Ablation studies lack quantitative quality metrics**: The PAA ablation (Figure 9, Section 4.3.1) and KSA ablation (Figure 10, Section 4.3.2) report only latency and VRAM alongside 2 qualitative images each. No FID, SSIM, F1, or other quality metrics from Table 1 are reported. This makes it impossible to assess whether PAA's efficiency gain over SWA or KSA's pruning come at a quality cost — which is the central tradeoff the paper claims to navigate successfully.

### Minor

- **Limited baselines for both efficiency and quality comparison**: The paper compares only against OminiControl2 and UniCombine (both full-attention methods) for quality, and only against these two for efficiency (Figures 7-8). No comparison with general sparse attention baselines or other efficient multi-condition methods like PixelPonder (discussed in Section 2.2) is provided. The PAA ablation includes SWA but only measures efficiency. This makes it difficult to attribute gains to PKA's condition-specific decomposition rather than generic sparsification.

- **No evaluation set specification or statistical reporting**: The paper says it partitions Subject200K into training and testing sets but provides no test set size, number of test images, or confidence intervals. FID scores of 52-80 are relatively high, suggesting a potentially small or narrow-domain evaluation set. Without variance information, differences like FID 52.99 vs 61.03 cannot be assessed for statistical significance.

- **Selective metric interpretation undermines credibility**: The paper calls CLIP-T differences (0.349 vs 0.352) "perceptually negligible" while treating the F1 regression (0.414 vs 0.551) as only a "narrow margin" despite being a far larger relative gap. This asymmetric interpretation of metrics weakens the paper's analytical credibility.

### Trivial

None

## Nice-to-Haves
- Report end-to-end inference time and total VRAM, not just attention-module metrics, for at least the 2-condition scenario evaluated in Table 1.
- Add FID/SSIM/F1 to PAA and KSA ablation tables (Figures 9-10) to make the efficiency-quality tradeoff explicit.
- Investigate the source of the F1 regression on Subject-Canny — test whether a small local window (rather than strict one-to-one) recovers edge controllability.
- Add at least one general sparse-attention baseline with quantitative quality metrics to demonstrate PKA's decomposition is superior to generic sparsification.
- Validate KSA mask stability across timesteps (e.g., mask IoU between consecutive steps).
- Specify test set size and report variance across multiple seeds.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Criticism about KSA temporal consistency assumption being fragile — speculative without evidence it actually fails; the paper cites Zhou et al. 2025 for this property.
- Criticism about early-timestep sampling hyperparameter sensitivity — Figure 11 is sparse (3 settings) but the conclusion "early timesteps matter more" is well-grounded from Figure 5 and consistent with known diffusion dynamics.
- Formatting/style nitpicks from harsh reviewer — removed per filtering rules.

## Novel Insights

The paper's decomposition of multi-condition attention by condition type (spatial vs. subject) into structurally different specialized modules is a genuinely clean architectural contribution. The empirical observation from Figures 2-3 — that spatial conditions produce diagonal-dominant attention while subject conditions produce keyword-sparse cross-attention — effectively motivates two distinct efficiency strategies (one-to-one correspondence for spatial, keyword-masked sparsification for subject) rather than one-size-fits-all approaches. The Condition Cache, enabled by the architectural choice that conditions self-attend only within their type, is a practical design insight.

## Suggestions
- Add FID/SSIM/F1 metrics to the PAA and KSA ablation studies to substantiate the efficiency-quality tradeoff claim.
- Investigate whether PAA's strict one-to-one locality causes the F1 regression on Subject-Canny, and test whether a small local window recovers it.
- Report end-to-end inference time and total VRAM for at least the standard 2-condition scenario.
- Add a general sparse-attention baseline (e.g., windowed attention with quantitative quality) to demonstrate the value of condition-specific decomposition over generic sparsification.

## Calibration Report

**Round 1 anchors retrieved** (all on topic of efficient diffusion transformer attention):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| rnTb9dm9zx (PCPP) | 3.00 | R1 | Parallelism method for diffusion, rejected. Less clean architecture than PKA. |
| Jt1gGIumJo (Highlight Diffusion) | 3.00 | R1 | Attention-guided acceleration, rejected. Less principled than PKA's decomposition. |
| 2o58Mbqkd2 (Superposition) | 3.25 | R1 | Combining diffusion models, different scope. |
| vK8C37eHXM (Sample what you can't compress) | 3.20 | R1 | Autoencoder + diffusion, different topic. |
| 3kADTLbKmm (SparseDM) | 4.00 | R1 | Sparse pruning for DMs. Simple motivation, limited evaluation. Less novel than PKA. |
| vNZIePda08 (Sparse-to-Sparse) | 4.75 | R1 | Sparse training for DMs. Different approach but similar efficiency goal. |
| leBbjaUxut (Multi-Scale DiT) | 5.00 | R1 | Multi-scale DiT. Rejected despite 3× convergence speedup — insufficient experiments. |
| lWGXftRS5h (Inductive Biases in DiT) | 5.00 | R1 | Understanding attention in DiTs, theoretical focus. |
| lTrrnNdkOX (Qihoo-T2X) | 6.40 | R1 | Proxy-tokenized DiT for T2I/T2V. Accepted. 49% reduction vs DiT. Similar efficiency focus but broader task scope. Our paper has cleaner decomposition but narrower scope and worse F1. |
| D2as3jDmRA (LinFusion) | 6.25 | R1 | Linear attention for high-res diffusion. Rejected at 6.25. Better speedup numbers but different mechanism. Our paper has similar evaluation gaps. |
| MbM1BqGpZu (DiT Theory) | 6.75 | R1 | Theoretical DiT analysis. Accepted. Different contribution type. |
| qmXedvwrT1 (LEGO) | 6.67 | R1 | Efficient diffusion backbone. Accepted. Modular architecture, similar efficiency claims. |
| gU58d5QeGv (Würstchen) | 8.00 | R1 | Efficient T2I architecture. Strong accept. Significantly stronger contribution. |
| fV0t65OBUu (OCM) | 8.00 | R1 | Optimal covariance matching for diffusion. Strong accept. Different focus. |
| OvoCm1gGhN (Diff Transformer) | 8.00 | R1 | Differential attention mechanism. Strong accept. Broader impact. |
| zMoNrajk2X (CADS) | 8.00 | R1 | Condition-annealed sampling. Strong accept. Different contribution. |

**Round 1 bracket**: Between 4.5 and 6.5. The paper is clearly stronger than SparseDM (4.0) and the 3.0-rated papers due to its cleaner architecture and better quality results, but has similar evaluation gaps to LinFusion (6.25, rejected). Qihoo-T2X (6.40, accepted) is the closest comparator but has broader scope.

**Final calibration reasoning**: The paper's strongest point is the architectural decomposition motivated by empirical attention analysis, combined with best-in-class quality on most metrics. Its weakest points are the F1 regression (largest metric gap, dismissed), the efficiency-quality regime disconnect, and missing quality metrics in ablations. These weaknesses are similar in nature to issues noted in LinFusion (6.25, reject) and Qihoo-T2X (6.40, accept). The F1 regression being the largest controllability gap for a controllability-focused method, combined with the selective metric interpretation and thin evaluation, place this slightly below the accept threshold. Score of 5.5 reflects a paper with genuine architectural contribution and strong results on most metrics, held back by evaluation gaps and one unexplained regression.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>