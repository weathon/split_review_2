Now let me read the remaining sections for complete verification:Now I have all the information needed. Let me draft the review.Now let me proceed with calibration. Round 1 — Bracketing:Let me read a few key anchors to calibrate:Now I have enough anchors to form my initial bracket. Let me assess:

**Round 1 Bracket Assessment:**
- vs. Highlight Diffusion (3.0): PKA is far superior — much larger speedups (10× vs 1.52×), better method design, broader evaluation. PKA is clearly above this.
- vs. Enhanced Controllability (3.75): PKA is cleaner, has stronger results, fewer hyperparameters, and a more principled design.
- vs. Qihoo-T2X (6.4): Very comparable — both propose efficient attention for DiTs, exploit spatial redundancy, and both were criticized for lacking quality-vs-efficiency ablations. Qihoo-T2X had broader scope (T2I/T2V/T2MV), but PKA has stronger efficiency gains and a novel condition-type-aware insight.
- vs. Würstchen (8.0): PKA is weaker — less comprehensive evaluation, missing ablation quality metrics, narrower scope. Würstchen had user studies, thorough comparisons, and code release.

**Initial bracket: 5.5 – 6.5**

The paper sits around the borderline accept zone. Let me now write the final review.Now I have enough to write the final calibrated review.

## Summary
This paper proposes PKA (Patch-wise and Keyword-Aware Attention), a framework for efficient multi-condition control in Diffusion Transformers (DiTs). It introduces two specialized attention modules—Position-Aligned Attention (PAA), which reduces spatial-condition attention to position-wise one-to-one computation, and Keyword-Scoped Attention (KSA), which confines subject-condition attention to keyword-relevant image regions via a dynamic binary mask. An early-timestep sampling strategy biasing training toward high-noise stages is also proposed. The method achieves 3.9–10× inference speedup and 2.46–5.12× VRAM reduction for the attention module while largely maintaining or improving generation quality across three multi-condition tasks.

## Strengths
- **Well-grounded empirical motivation (Figures 2–3):** The paper does not merely assert redundancy — it visualizes the specific structure of attention sparsity for spatial conditions (diagonal concentration, Figure 2) and subject conditions (keyword-localized activation, Figure 3). The two modules are directly derived from these distinct observed patterns, which is a stronger motivational chain than typical efficiency papers.

- **Condition-type-aware architectural decomposition:** Recognizing that spatial and subject conditions exhibit *structurally different* sparsity patterns and designing separate mechanisms (PAA for spatial locality, KSA for semantic locality) is a genuine and novel insight. Prior DiT-based multi-condition methods (OminiControl, UniCombine) treat all conditions uniformly through concatenate-and-attend. This decomposition also enables the condition-cache mechanism (Section 3.2, Figure 4a), where condition KV projections are computed once and reused across all denoising steps.

- **Strong quality and consistency metrics (Table 1):** Across all three tasks, the proposed method achieves the best FID (52.99/62.08/53.01 vs. next-best 61.03/70.22/67.40) and SSIM, and substantially better CLIP-I and DINOv2 subject consistency scores. These are not marginal improvements — FID drops of 8–14 points are meaningful. On Canny-Depth controllability (F1: 0.411 vs. 0.369; MSE: 114 vs. 250), the method is also best.

- **Practical and well-characterized efficiency gains (Figures 7–8):** The efficiency scaling curves across 1–16 conditions are transparent, showing gains at moderate (3.90× at 4 conditions) and high condition counts. The method outperforms both UniCombine (full attention) and OminiControl2 (which uses its own efficiency techniques).

## Weaknesses

### Fatal
None.

### Major
1. **Ablations of PAA and KSA report only efficiency metrics, omitting quality/controllability (Figures 9–10)** — The PAA ablation (Figure 9) compares full attention, PAA, and sliding-window attention variants but reports only latency and VRAM. The KSA ablation (Figure 10) varies ε and similarly reports only visual comparisons plus efficiency numbers. The paper's central claim is that efficiency comes "without compromising generative performance" (abstract), yet the individual-module ablations do not measure generation quality (FID, SSIM, F1, CLIP-I, etc.). This is the paper's most significant evidential gap: the main table (Table 1) shows results for the *complete system*, but does not decompose how much quality each module independently costs or preserves. A quantitative ablation table (e.g., full attention → PAA → PAA+KSA) with quality and controllability metrics would directly close this gap.

2. **Subject-Canny F1 gap is understated** — On the Subject-Canny task, the proposed method's F1 is 0.414 vs. UniCombine's 0.551 (Table 1), a ~25% relative gap. F1 measures edge adherence — precisely the metric testing spatial control fidelity that PAA is designed to preserve. Section 4.2.3 dismisses this as "a narrow margin on the Subject-Canny task," which is misleading for this magnitude. Notably, on the Canny-Depth task (no subject condition), the method achieves the *best* F1 (0.411 vs. 0.369), suggesting the degradation may stem from the interaction between subject and spatial conditions rather than PAA alone. But this hypothesis is never explored or analyzed in the paper. This is a real and reportable gap in the paper's claimed "maintaining or improving controllability."

### Minor
3. **KSA keyword identification mechanism is unspecified** — Section 3.2.2 references a keyword set 𝕂 containing "just 1 to 2 tokens" (line 128), and Section 4.1 mentions "ensuring each image caption contains a descriptive keyword," but the paper never explains *how* the keyword tokens are identified from a text prompt at inference time. Is this manual specification by the user? An automatic parser? This is a practical requirement for deployment that affects the method's generality.

4. **Early-timestep sampling ablation is only visual (Figure 11)** — For a contribution listed as one of three main contributions, the supporting evidence is thin: Figure 11 shows cherry-picked visual examples at different (μ, δ) settings with no quantitative metrics (FID, SSIM, etc.) across settings. The specific (μ, δ) values used for the main results in Table 1 are also not stated in the main text, though Figure 11 tests three combinations.

5. **Undefined "Norm" in Eq. 3** — The normalization operation used to generate the binary mask M_t is not defined. Whether this is min-max, softmax, L2, or another normalization affects how the threshold ε should be interpreted and makes the KSA formulation under-specified.

6. **Baseline training protocol ambiguity** — Section 4.1 states "To ensure a fair comparison, we fine-tune the FLUX.1 model using LoRA" but it remains unclear whether baselines (OminiControl2, UniCombine) were retrained under identical conditions (same data subset, iterations, optimizer) or whether their released checkpoints were used. This is important for the validity of the Table 1 comparison.

### Trivial
None.

## Nice-to-Haves
- Quantitative ablation tables showing quality and controllability metrics for PAA and KSA independently (full attention → PAA → PAA+KSA → full PKA). This is the single highest-impact improvement the authors could make.
- Analysis of why F1 degrades on Subject-Canny but not Canny-Depth — if this is a subject-spatial interaction effect, discussing the tradeoff honestly would strengthen the paper.
- Evaluation on a second DiT backbone beyond FLUX.1 or a second dataset beyond Subject200K to strengthen generalization claims.
- Isolating the condition-cache mechanism's contribution to overall speedup.
- A quantitative table for the early-timestep sampling ablation showing final model metrics at convergence across different (μ, δ) settings.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"PAA's one-to-one attention is fundamentally too aggressive"** — While the one-to-one design is aggressive, it is well-motivated by Figure 2's diagonal dominance. The method achieves best F1 on Canny-Depth (0.411) and best MSE on Subject-Depth (160), showing spatial control is preserved in most settings. The concern is already captured by the F1 gap issue above; framing PAA as structurally flawed overstates what the evidence shows.

- **"KSA's temporal mask consistency is under-examined"** — The reviewer speculates about mask accuracy degradation across steps, but the paper cites temporal consistency from Zhou et al. (2025), and Figure 10 shows the approach works robustly across threshold values. This is speculation about failure modes not demonstrated in the paper.

- **"Headline efficiency numbers at extreme condition counts"** — The paper reports the full range (3.90×–10×) in Section 4.2.1 and provides transparent scaling curves in Figures 7–8. While the abstract highlights the upper end, this is standard practice and the paper provides enough information for the reader to assess gains at any condition count.

- **"The overall model still has O((M+N)²) attention"** — The paper explicitly states the complexity reduction applies to condition attention (Section 3.2.1), never claiming to reduce total model complexity.

- **"Notation ambiguity in Eq. 4 (hat on K_SJ)"** — Minor notation issue that does not affect understanding of the mechanism.

- **"Test set size not reported / no confidence intervals"** — Removed as reproducibility nitpick; standard single-run evaluation practice in the field.

## Novel Insights
The paper's core insight — that different condition types in multi-condition DiTs exhibit structurally different attention sparsity patterns (diagonal for spatial, keyword-localized for subject) and that these can be exploited with condition-type-aware sparse attention — is genuinely novel. Prior efficient-attention methods for DiTs (token pruning, caching, downsampling) treat all conditions uniformly. The observation that this structural prior also enables a clean condition-cache mechanism (because condition tokens are restricted to self-attention only) adds practical value beyond the attention efficiency itself. None beyond the paper's own contributions.

## Suggestions
- Provide quantitative ablation tables for PAA (compare full attention, PAA, SWA variants on F1, FID, SSIM, MSE) and KSA (compare ε values on CLIP-I, DINOv2, SSIM). These directly address the paper's most significant evidential gap.
- Analyze the Subject-Canny F1 gap honestly: is it a PAA limitation, a subject-spatial interaction effect, or a training tradeoff? The divergence between Subject-Canny (worse F1) and Canny-Depth (better F1) deserves investigation.
- Specify how keyword tokens 𝕂 are identified and define the "Norm" operation in Eq. 3.
- Report quantitative metrics for the early-timestep sampling ablation and state the (μ, δ) values used for the main experiments.
- Clarify whether baselines were retrained under identical conditions.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Highlight Diffusion | Jt1gGIumJo | 3.0 | 1 | Also attention-guided acceleration for diffusion, but much weaker (1.52× speedup, one backbone, poor writing). PKA is far superior. |
| Pixel-Aware Reverse Diffusion | W4djmqKZC6 | 3.0 | 1 | Diffusion acceleration with limited evidence. PKA is clearly above. |
| Optimizing Attention | vnp2LtLlQg | 3.0 | 1 | Generic attention optimization; minimal overlap with PKA's contribution. |
| REPA (Representation Alignment) | DJSZGGZYVi | 3.0 (listed) / 9.0 (actual) | 1 | Different domain (representation alignment for DiTs); not directly comparable. |
| Enhanced Controllability | kALZASidYe | 3.75 | 1 | Multi-condition diffusion; weaker design (many hyperparameters, unclear scalability, no ablation). PKA is substantially better. |
| APCtrl | yPxhj1FKhG | 3.67 | 1 | Conditional control via projection; less practical. PKA is stronger. |
| Dreamguider | Hpu3KIX8Am | 4.0 | 1 | Training-free conditional guidance; different focus. PKA has stronger results. |
| Compositional VQ Sampling | gKui6QvvfK | 5.25 | 1 | Compositional multi-condition generation; borderline. PKA has clearer contribution and stronger efficiency gains. |
| VD3D | 0n4bS0R5MM | 6.20 | 1 | Camera control for video DiTs. Accepted with similar mixed scores. Comparable quality level. |
| Qihoo-T2X (PT-DiT) | lTrrnNdkOX | 6.40 | 1 | Most comparable — also efficient attention for DiTs exploiting spatial redundancy. Accepted with scores 6/6/6/6/8. Had similar ablation gaps. Broader scope (T2I/T2V/T2MV) but PKA has stronger efficiency gains and a more novel condition-type-aware insight. |
| Diffusion Transformer Theory | MbM1BqGpZu | 6.75 | 1 | Theory paper; less comparable. |
| Efficient-3Dim | 3eFMnZ3N4J | 7.25 | 1 | Efficient diffusion for novel view synthesis; accepted with 5/8/8/8. Stronger evaluation. Above PKA. |
| Würstchen | gU58d5QeGv | 8.0 | 1 | Efficient text-to-image architecture with comprehensive evaluation. Clearly above PKA. |
| One Step Diffusion | OlzB6LnXcS | 8.0 | 1 | Different topic (few-step generation); not directly comparable. |
| IC-Light | u1cQYxRI1H | 10.0 (listed as avg 0.50 due to score range mismatch) | 1 | Not comparable; illumination harmonization. |

**Round 1 bracket: 5.5 – 6.5**

The paper under review is most comparable to Qihoo-T2X (6.4), which also proposes efficient attention for DiTs, exploits spatial redundancy, and had similar ablation gaps (lacking quality-vs-efficiency tradeoff analysis). Qihoo-T2X was evaluated more broadly (T2I, T2V, T2MV across multiple resolutions) but had less novel insight. PKA has a more original condition-type-aware decomposition but narrower evaluation (one backbone, one dataset, one task family). The F1 gap on Subject-Canny is a concrete weakness Qihoo-T2X didn't have.

Compared to the 5.25-scored Compositional VQ (rejected), PKA is clearly stronger in motivation, method design, and efficiency results. Compared to 6.2-scored VD3D and 6.4-scored Qihoo-T2X (both accepted), PKA is roughly comparable — strong core idea with some evaluation gaps.

**Final calibrated score: 6.0**

The paper makes a genuine and novel contribution (condition-type-aware sparse attention for multi-condition DiTs) with strong efficiency results and mostly strong quality results. The ablation gaps (Major weakness #1) and the understated F1 degradation (Major weakness #2) prevent higher confidence, but these are addressable in a rebuttal and do not invalidate the core contribution. The paper sits at the borderline-accept threshold.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>