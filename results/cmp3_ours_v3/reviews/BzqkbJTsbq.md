## Summary

This paper proposes DPG, a unified framework for diffusion-based imperfect-label guidance that covers style transfer (weak-label), super-resolution, and deblurring (degraded-label). The method introduces two components: (1) "data knowledge" — injecting noisy variants of the imperfect label into the early reverse diffusion process via weighted interpolation of both latents and noise predictions, and (2) "process knowledge" — enforcing a margin constraint that each timestep's prediction must improve over the previous one. Experiments across three tasks compare against 10–11 baselines per task.

## Strengths

1. **Broad and current baseline coverage.** The paper compares DPG against 10–11 methods per task, including very recent work (2024–2025) such as FlowDPS, FlowChef, DOC, StyleShot, and StyleStudio. This is a genuine effort at comprehensive empirical positioning, which is uncommon for a multi-task paper.

2. **Conceptually clean framework.** The separation into "data knowledge" (injecting processed label information into the diffusion path) and "process knowledge" (enforcing monotonic improvement across timesteps) is a clear organizing principle. While neither component is radically novel in isolation, the packaging provides a useful lens for thinking about imperfect-label guidance.

3. **Large-scale style-transfer evaluation.** The style transfer evaluation uses 40,000 stylized images (200 texts × 200 style images), which is substantially larger than typical evaluations in this area and provides a solid basis for the style transfer claims.

## Weaknesses

### Major

1. **Identical LPIPS values across Tables 1(b) and 1(c) — a clear data error.** The LPIPS row in the super-resolution table and the deblurring table contains *exactly the same sequence of numbers* for every shared method (DPG: 0.2236, ImSR/DCDP: 0.2325, PSLD: 0.2675, …, FreeDom: 0.6764). This is impossible for two different tasks with different inputs, different targets, and different degradation processes. It indicates a copy-paste error in the table. Because it is the perceptual metric (LPIPS) that is affected, the quantitative comparisons for super-resolution and deblurring — which are central to the paper's claims of generality — cannot be trusted as reported. The PSNR and SSIM values differ between the two tables, so the error appears confined to LPIPS, but it is a serious integrity concern that must be corrected before any acceptance.

### Minor

2. **SSIM text contradicts Table 1(b).** The paper states that for super-resolution, DPG's SSIM is "slightly lower than FPS-SMC" (line 314). However, Table 1(b) shows DPG SSIM = 0.8323 and FPS-SMC SSIM = 0.8283 — DPG's is strictly *higher*. This is a factual error in the text that, while small, further erodes confidence in the quantitative reporting.

3. **Ablation Text Score anomaly not discussed.** In the style-transfer ablation (Table 2), the variant *without* process knowledge (w/o P) achieves a Text Score of 0.3008, which is *higher* than the full DPG (0.2952). The paper reports this value in bold (the table convention for best results) but the text discussion (Section 4.3) only says process knowledge is "essential and effective" and cites the Style Loss and CLIP Loss improvements, without acknowledging this countervailing evidence. A valid ablation study must address metrics that do not support the conclusion, not only those that do.

4. **Computational cost not reported.** DPG requires two parallel U-Net forward passes per timestep (Eq. 7) plus gradient backpropagation through the decoder (Eq. 9) for every timestep. This is substantially more expensive than standard sampling or most loss-guided approaches. No wall-clock time, FLOPs, or relative overhead comparisons are provided. This is a significant practical consideration for any practitioner evaluating the method.

5. **No discussion of limitations.** The conclusion does not discuss any limitations of DPG despite the method's task-specific components, computational overhead, and mixed ablation results. A limitations paragraph is standard practice and would improve the paper's credibility.

6. **Overclaimed novelty.** The paper states it is "the first study to analyze the gap between weak-label and degraded-label guidance tasks and to propose a unified approach to bridge it" (line 84). However, the paper's own Related Work describes TFG (Ye et al., 2024) as a framework that "unifies loss-guidance methods and provides a parameter search strategy" applicable to the same imperfect-label tasks, and FreeDoM (Yu et al., 2023) as a "multi-conditional energy-function guidance method." The paper should more precisely characterize what aspects of its approach are novel relative to these existing unified frameworks rather than claiming blanket priority.

7. **Pixel-space vs. latent-space baseline fairness.** Some baselines (FPS-SMC, SITCOM, DOC, TFG, FreeDom in super-resolution/deblurring) operate in pixel space while DPG operates in latent space. The paper marks these with asterisks but does not discuss how architectural differences (different operating spaces, different computational budgets) might affect comparison fairness.

### Trivial

None.

## Nice-to-Haves

- Report wall-clock time or FLOPs relative to baselines.
- Add confidence intervals or standard deviations over multiple runs for close comparisons (e.g., the 0.004 SSIM gap).
- Include sensitivity analysis for key hyperparameters (α_data, γ_data, α_margin).
- Analyze how often the process-knowledge margin constraint L₂ actually produces a non-zero gradient across timesteps.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Eq. 3 notation "garbling":** The harsh critic flagged a missing operator in Eq. 3. This is a PDF-parser artifact — the original submission does not have this issue. **Removed per hard rules on parser artifacts.**
- **TFG's Text Score "dismissed":** The reviewer claimed the paper dismisses TFG's lead in Text Score, but the paper explicitly says "Despite TFG's marginal lead in Text Score, its Style and CLIP Losses are substantially higher" (line 312). The paper does acknowledge the trade-off. **Removed as factually inaccurate.**
- **Introduction unification conflates (a) vs. (b):** The harsh critic argued the paper conflates a single algorithm with a conceptual framework. The paper is upfront about task-specific components (M(y), f_loss, hyperparameters) and does not claim otherwise. **Removed as scope creep.**
- **Related Work placement preference:** The critic wanted the main comparison with loss-guided methods in Related Work rather than the Introduction. This is a presentational preference, not a substantive weakness. **Removed.**
- **Statistical significance / confidence intervals:** Requesting multiple seeds or confidence intervals for large-scale benchmarks where single-run evaluation is the norm in this community. **Demoted to Nice-to-Have.**
- **Hyperparameter sensitivity:** The paper defers these values to the appendix, which is stripped by the parser. **Demoted to Nice-to-Have.**
- **FFHQ train/test contamination:** The concern that Stable Diffusion may have seen FFHQ test images is speculative and applies to essentially all work using pre-trained diffusion models. **Removed as generic.**
- **Evaluation splits for FFHQ:** The paper states 1,000 randomly selected FFHQ images, which is standard practice. **Removed.**

## Novel Insights

Beyond the paper's own contributions, the reviews surface one genuinely insightful observation: the process-knowledge component (Eq. 11) enforces a margin constraint that may be redundant for many timesteps — the reverse diffusion process naturally brings predictions closer to the target over time, so L₂ may only fire sporadically. The paper does not analyze this activation frequency, leaving it unclear whether the reported improvements come from active correction or from a small number of fortuitous gradient updates. This is a useful point that the authors should investigate.

None beyond the paper's own contributions.

## Suggestions

1. **Fix the LPIPS duplicate values in Tables 1(b) and 1(c).** Re-run the evaluations for both super-resolution and deblurring and report the correct LPIPS values separately for each task. This is the single most important fix.
2. **Correct the SSIM text** to match Table 1(b) — DPG's SSIM is *higher* than FPS-SMC, not lower.
3. **Acknowledge and discuss the Text Score anomaly** in the ablation study. Explain why removing process knowledge improves text-image alignment on this metric even though it hurts Style Loss and CLIP Loss.
4. **Report computational cost** (wall-clock time per image or relative FLOPs) against at least the main baselines.
5. **Reframe the novelty claim** by removing "first" and instead stating that DPG provides a specific two-component framework that differs from existing unified approaches (TFG, FreeDoM) in how it injects data-level information and enforces temporal consistency.
6. **Add a limitations paragraph** to the conclusion covering the computational overhead, task-specific components, and the conditions under which the method may not be the best choice.

## Score and Decision

**Anchors used for calibration:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| VIPaint (dAavOuxZvo) | 3.00 | 1 | Weaker experimental setup (100 images), but DPG has a data integrity error of comparable severity |
| Beyond Transformations (JmGEZXkCH3) | 3.67 | 1 | Unfair comparison settings; DPG has different but comparable issues |
| Text Prompt Diffusion (vTdwuKUc5Z) | 4.25 | 2 | Novelty/comparison issues; DPG has clearer contributions but suffers from a data error |
| Position Embedding Interpolation (H56qXKaNpF) | 4.00 | 2 | General method with limited evaluation scope; DPG is similar in overall quality |
| Distillation-Free One-Step (2ogxyVlHmi) | 4.75 | 2 | Technically solid but incremental; DPG has more conceptual novelty but a data error |
| Does Diffusion Beat GAN (46mbA3vu25) | 5.75 | 1 | Rigorous controlled study with only presentation issues; DPG is clearly weaker |
| Solving Diffusion ODEs (BtT6o5tfHu) | 6.67 | 1 | Strong theory with solid experiments; DPG does not match this quality level |

**Round 1 bracket:** 3.0–5.0 (based on comparisons to VIPaint at the low end and Solving Diffusion ODEs at the high end).

**Narrowing:** The paper's LPIPS data error prevents it from reaching the 5+ range where papers typically need clean quantitative evidence. It sits alongside Text Prompt Diffusion (4.25) and Position Embedding Interpolation (4.00) in quality — papers with interesting ideas but significant issues in the presented evidence. The final score of 4.0 reflects that the paper has a clear and serious data integrity issue (LPIPS duplication) that makes the current quantitative claims unreliable, but the core method and conceptual framework are plausible enough that a corrected submission could be reconsidered.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>