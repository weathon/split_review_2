Now let me write the final consolidated review.

## Summary

This paper proposes Patch-wise and Keyword-Aware Attention (PKA) for efficient multi-condition control in Diffusion Transformers. It decomposes the expensive full attention between noisy image tokens and multiple visual conditions into two specialized modules: Position-Aligned Attention (PAA) for spatial-aligned conditions (one-to-one per-patch attention, O(N) complexity) and Keyword-Scoped Attention (KSA) for subject-driven conditions (masked attention using keyword-derived relevance masks). A Condition Cache exploits the isolation of condition self-attention to cache K/V projections after the first denoising step. Combined with an early-timestep training sampling strategy, the method achieves up to 10× inference speedup and 5.12× VRAM reduction on the attention module while maintaining or improving generative quality across three multi-condition tasks.

## Strengths

1. **Attention sparsity analysis directly motivates the architecture (Figures 2–3)**. The paper provides empirical evidence that multi-condition attention is highly redundant in a condition-type-dependent way — attention is concentrated along the diagonal for spatial conditions and sparse for subject-driven conditions. This grounds the design of PAA (one-to-one attention) and KSA (keyword-scoped masking) in observed behavior rather than generic efficiency intuition.

2. **Strong quantitative evidence that efficiency gains do not degrade quality (Table 1)**. Across three multi-condition tasks and seven metrics, PKA achieves the best score on 7 of 9 metrics. FID improves substantially (e.g., 53.01 vs 67.40 for UniCombine on Canny-Depth) while CLIP-I and DINOv2 also improve. This directly substantiates the central claim that the 10× speedup and 5.12× VRAM reduction do not come at the cost of quality.

3. **Condition Cache is a clean architectural enabler (Section 3.2, Figure 4a)**. The structural choice to have condition tokens only attend within their own condition cleanly enables caching of condition K/V projections after the first denoising step — a specific, measurable benefit not present in concatenate-and-attend baselines.

4. **Ablation against Sliding Window Attention for PAA (Section 4.3.1)**. Rather than only comparing against full attention, the paper benchmarks against SWA at multiple window sizes. PAA beats the best SWA variant (SWA-1) in both latency (13.63s vs 14.00s) and VRAM (237MB vs 276MB), providing a fair and informative comparison.

5. **Temporal perturbation analysis motivating early-timestep sampling (Figure 5)**. The SSIM-based experiment provides quantitative evidence that perturbing early timesteps degrades conditional control more than perturbing late timesteps, motivating the shifted logit-normal training distribution.

## Weaknesses

### Fatal
None.

### Major

1. **Early-timestep sampling ablation lacks quantitative validation (Section 4.3.3, Figure 11).** The early-timestep sampling strategy is presented as a co-contribution alongside PKA (line 48: "methodological advancements to improve both inference and training efficiency"), yet its evaluation is purely qualitative — visual comparisons across different (μ,δ) settings at varying iteration counts. No quantitative metrics (FID, CLIP-I, DINOv2, or controllability metrics) are reported for this ablation. Given the claim that this strategy "accelerates convergence and enhances control fidelity," quantitative evidence is needed to match the rigor of the inference-side contributions.

2. **KSA mask update schedule is underspecified (Section 3.2.2, Eqns. 3–4).** The paper states that a binary relevance mask is generated at timestep t and reused at timestep t+1. It does not specify what happens at timesteps t+2, t+3, etc.: is the mask computed once and reused for the entire 28–50 step denoising trajectory, periodically recomputed, or updated every step? The temporal-consistency assumption (Zhou et al., 2025) is cited but not empirically validated for the full trajectory. Since the noisy image changes substantially across the denoising process, a mask from early steps may not remain accurate at later, cleaner stages. The paper should specify the exact schedule and provide evidence (e.g., mask IoU over timesteps) that the chosen schedule is valid.

### Minor

1. **Subject-Canny F1 gap is misleadingly characterized (Table 1, line 249).** On the Subject-Canny task, PKA achieves F1=0.414 vs UniCombine's 0.551 — a ~25% relative difference, the single largest metric gap in the table. The paper describes this as "a minor exception of a narrow margin." While PKA dominates on every other metric for this task (FID 52.99 vs 61.03, SSIM 0.553 vs 0.493, CLIP-I 0.945 vs 0.912, DINOv2 0.926 vs 0.901), the F1 framing understates the specific controllability trade-off on edge detection. The paper should acknowledge this gap more precisely and ideally offer analysis (e.g., does PAA's one-to-one alignment lose edge information that a sliding window would capture?).

2. **Missing training reproducibility details (Section 4.1).** The paper specifies LoRA fine-tuning but does not report LoRA rank, learning rate schedule, or the exact size of the Subject200K subset used for training. These details are important for reproducing the fine-tuning regime.

3. **PAA ablation vs. SWA may conflate caching benefit (Section 4.3.1, Figure 9).** The comparison against Sliding Window Attention does not state whether the SWA baselines also leverage the Condition Cache (enabled by condition self-attention isolation). If SWA baselines do not use caching, part of the latency/VRAM advantage attributed to PAA may reflect caching benefits rather than the one-to-one attention design itself.

### Trivial
- The paper states that efficiency numbers are for the attention module (abstract, Section 4.2.1), which is transparent. Including end-to-end generation time and VRAM would help readers calibrate practical impact.

## Nice-to-Haves
- A complexity breakdown for typical token counts separating PAA, KSA, and the retained X↔T full attention.
- Discussion of KSA threshold ε sensitivity across a wider range of tasks beyond what is shown in Figure 10.

## Removed Points

The following points from the input reviews were identified as noise and are removed here but kept for reference:

1. **"Efficiency numbers are attention-module-specific, not end-to-end"** — REMOVED. The paper is transparent about this; it consistently states "attention mechanism" and "attention module" in the abstract, Section 4.2.1, and Figure 8 caption. This is not a weakness.

2. **"The (X, T) full attention is not motivated"** — REMOVED. The paper states this design choice; it is reasonable because text attention is standard in DiTs and the method's focus is visual conditions. Full text attention is needed for prompt following.

3. **"KSA threshold ε ambiguity (no guidance on selection)"** — REMOVED. The paper provides an ablation study (Figure 10) across ε ∈ {0.2, 0.4, 0.6, 0.8} and explicitly frames ε as a user-controllable parameter with a graceful quality-efficiency trade-off. This is sufficient.

4. **"PAA complexity still requires X↔T attention so overall reduction is less"** — REMOVED. The paper correctly states PAA reduces spatial condition attention from O(N²) to O(N). The retained X↔T attention for text is standard and the paper acknowledges this design choice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide quantitative results (FID, CLIP-I, controllability metrics) for the early-timestep sampling ablation across different (μ,δ) settings.
2. Clarify the KSA mask update schedule precisely (once, periodic, or every step) and include mask IoU analysis over timesteps to validate the temporal-consistency assumption.
3. Report LoRA rank, learning rate schedule, and dataset subset size.
4. Reframe the Subject-Canny F1 result to acknowledge the gap and offer a hypothesis for the trade-off.
5. Clarify whether the SWA baselines in Section 4.3.1 use the Condition Cache.

### Calibration

**Round 1 anchors (bracketing):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Jt1gGIumJo.md` (Highlight Diffusion) | 3.00 | R1 (1.5–3.5) | Training-free attention acceleration; much simpler method, weaker empirical evaluation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iG7qH9Kdao.md` (Efficient Scaling of DiTs) | 5.00 | R1 (3.5–5.5) | Empirical scaling study, different contribution type; less direct architecture contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/leBbjaUxut.md` (Multi-Scale Image DiT) | 5.00 | R1 (3.5–5.5) | Uses explainability to design efficient DiT; weaker quantitative efficiency results |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lTrrnNdkOX.md` (Qihoo-T2X) | 6.40 | R1 (5.5–7.5) | **Most comparable anchor.** Proxy-tokenized DiT with similar motivation (attention redundancy). **Paper under review has stronger quantitative quality validation (Table 1) and more targeted architectural design.** |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/D2as3jDmRA.md` (LinFusion) | 6.25 | R1 (5.5–7.5) | Linear attention for diffusion. Similar efficiency goals. **Paper under review has cleaner quality preservation across metrics.** |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OvoCm1gGhN.md` (Differential Transformer) | 8.00 | R1 (7.5–8.5) | Very clean, broad-impact general attention mechanism. **Paper under review is more applied (multi-condition specific) and has less polished evaluation.** |

**Round 1 bracket:** 5.5 – 7.5. The paper's core contribution is well-validated and clearly motivated, placing it above the reject-range papers. However, two real gaps (qualitative-only validation of the training contribution, underspecified KSA schedule) prevent it from reaching the 8.0+ tier.

**Final calibrated score: 6.5.** This reflects a paper with a well-motivated, clearly presented method, strong core efficiency and quality results, but with two fixable gaps that prevent full acceptance at the 8.0 level. It sits between "borderline accept" and "accept" — above the 6.0–6.4 range of comparable papers like Qihoo-T2X (6.40) and LinFusion (6.25) due to cleaner empirical validation of the main contribution, but below 8.0 due to the noted gaps.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>