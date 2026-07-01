## Summary

This paper introduces DaVinci, a 7B-parameter MLLM for parsing raster scientific diagrams into structured TikZ code, trained in two stages: supervised fine-tuning on a curated dataset (TikZ-30K) with drawing-order normalization and comment injection, followed by GRPO-based reinforcement learning using a hybrid reward function. The key technical contribution is a vectorized-PDF-based reward that extracts text and geometry from compiled PDF output in an error-free manner, avoiding OCR error propagation. Experiments on the DATiKZv3 benchmark show strong results on compile rate (97.60% Pass@1) and competitive visual fidelity metrics against both specialized and proprietary models, with a human evaluation study providing additional validation.

## Strengths

- **Vectorized-PDF-based reward design (Section 3.3) is genuinely novel and well-engineered.** The insight that TikZ-generated PDFs retain exact geometric and typographic metadata as native vector elements, which can be exploited for extraction-error-free text and geometry matching during RL, is clever. The two-step exact-then-vague matching for text (Levenshtein + Distance-IoU) and bipartite Hungarian matching for geometric primitives are principled implementations that cleanly sidestep OCR error propagation.

- **Drawing order normalization and comment injection (Section 3.2) are well-motivated with clear empirical validation.** Figure 2 convincingly demonstrates the ordering noise problem, and the ablation (Table 4) provides clean evidence: reordering improves compile rate by +9.04% over baseline, and comments add another +5.72%.

- **Human evaluation is carefully performed.** Using Best-Worst Scaling with two separate comparison groups, reporting split-half reliability (0.7227 and 0.7878), and providing annotator demographics — these choices exceed the rigor common in this area.

- **The cBLEU/compile rate divergence insight (Section 4.3) is an honest and scientifically interesting finding.** The paper documents that after RL training, DaVinci-7B's cBLEU score decreases while visual fidelity and compile rate improve, explicitly noting that strict code-level similarity is neither necessary nor always desirable.

## Weaknesses

### Fatal
None.

### Major

1. **Abstract and conclusion frame the proprietary-model comparison selectively, creating a misleading impression.** The abstract states DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" (line 9), and the conclusion repeats the claim (line 275). However, the paper's own data show that Gemini-2.5-Pro-Thinking — also a leading proprietary model included in the evaluation — decisively outperforms DaVinci in human evaluation (BWS score 0.50 vs. -0.01 in Table 3) and achieves the best scores on multiple automatic metrics (DreamSim, SigLIP, SSIM, LPIPS in Table 1). The body text is transparent about this (line 218: "Gemini-2.5-Pro-Thinking significantly outperforms all other models"), but the dominant impression left by the abstract and conclusion omits this nuance. This is a framing problem, not a technical one, but it undermines credibility. The paper's genuine technical contributions stand on their own merit against open-source specialized baselines; the proprietary comparison would be more honestly presented as mixed rather than as an unqualified advance.

### Minor

2. **Undefined evaluation metrics in the reward ablation (Table 5).** The columns labeled "Texual ↑" and "Geometry ↑" in Table 5 are never defined in the paper. If these are the R_text and R_geom reward values computed as evaluation metrics on the test set, this is circular — the metric and the training objective would be the same function. If they are independent evaluation measures, the paper needs to describe them. Either way, readers cannot interpret the table without this information.

3. **No variance reporting on automatic metrics (Table 1).** All automatic metrics (Pass@1, DreamSim, SigLIP, SSIM, MSE, LPIPS) are reported as point estimates without confidence intervals or standard deviations. For a 542-sample test set, the Pass@1 compile rate (a binary outcome) carries a standard error of roughly ±1.3% under a binomial model. Without variance, it is impossible to assess whether gaps between models are meaningful or within noise. The paper reports std for the human evaluation (Tables 2-3) but omits it from the main automatic benchmark.

4. **Human evaluation Group 1 omits the base Qwen2.5-VL-7B model.** The non-proprietary comparison (Table 2) includes DetikZify-V2-8B, Qwen2.5-VL-72B, and DaVinci-SFT-7B, but not the base Qwen2.5-VL-7B from which DaVinci is fine-tuned. Including this control would strengthen the claim that improvements come from the DaVinci training pipeline rather than model architecture alone.

5. **The asymmetry between DaVinci (fine-tuned in-domain) and proprietary models (zero-shot) is not adequately discussed.** DaVinci is trained on ~58K diagram-TikZ pairs from arXiv, TeX.SE, and GitHub — the same distribution as the test set — while GPT-5, Claude, and Gemini are general-purpose models evaluated zero-shot. This does not invalidate the comparison, but the paper would benefit from explicitly acknowledging this structural advantage and contextualizing the proprietary-model results accordingly, rather than featuring them as the headline result.

### Trivial

6. The "minimum possible value" assignment in R_pass (line 148) is not precisely specified. R_text ∈ [0,1] and R_geom ∈ [0,1], while R_img includes DreamSim (unbounded) and clipped MSE ∈ [-1,1], so the effective penalty for non-compiling code is not clearly defined. This should be specified for reproducibility.

## Nice-to-Haves

- A brief analysis of the computational cost of the reward computation during RL (extracting text/geometry from PDF via PyMuPDF plus Hungarian matching) would help readers assess practicality.
- A breakdown of DaVinci-7B's remaining failure modes (beyond the note about scatter plots exceeding context limits) would be informative.
- The data ablation (Table 4) only reports Pass@1; reporting image-level metrics would strengthen the evidence that code reordering helps visual fidelity, not just compilability.

## Removed Points

- **"Critical Issue 4: comparison against proprietary models is structurally unfair"** — downgraded from Fatal/Major to Minor (point 5 above). The reviewer presented this as a major methodological gap, but comparing specialized fine-tuned models against general-purpose ones is standard practice in the field. The paper should acknowledge the asymmetry more clearly, but this is not a methodological flaw.
- **Temporal separation/distributional independence concern** — removed. This is a speculative concern that the same arXiv authors could span the pre-2024/post-2024 boundary. The paper already implements strict temporal separation, which is best practice. The critic offers no evidence that actual contamination occurs, and the concern is too hypothetical to retain as a weakness.
- **TED directionally opposite issue** — removed. The paper explicitly addresses this in Section 4.3 ("High Code Similarity Is Not Necessary"), and the critic acknowledges this addressal. Retaining the criticism would be a strawman.
- **Test set size concern (542 samples)** — removed. This is a standard benchmark size for this task (DATiKZv3 official test set), and the critic provides no evidence it is insufficient.
- **Base model choice discussion** — removed. The paper chooses Qwen2.5-VL-7B; questioning why this specific model was chosen without knowing the authors' rationale is scope creep.
- **Generic strengths about addressing an important problem** — removed. Only strengths with specific, concrete evidence are retained.

## Novel Insights

The reviews surface a genuine tension that the paper does not fully engage with: DaVinci-7B achieves a near-perfect compile rate (97.60%), yet in human evaluation against proprietary models (Table 3) it scores essentially neutral (-0.01 BWS), while Gemini (69.93% compile rate) scores 0.50. This suggests that when compilation succeeds, the proprietary models — especially Gemini — produce output that human evaluators strongly prefer, and that the compile rate advantage alone may not translate to human-perceived quality. The paper's automatic metrics partially reflect this (Gemini leads on DreamSim, SigLIP, SSIM), but the human evaluation makes the gap stark. This disconnect between compile-dominant and visual-fidelity-dominant paradigms in diagram parsing is worth deeper investigation, as the paper's current framing prioritizes the compile rate story.

## Suggestions

1. **Revise the abstract and conclusion** to accurately reflect the mixed proprietary-model comparison — e.g., "DaVinci achieves state-of-the-art results among open-source diagram parsing models and is competitive with leading proprietary systems on several metrics, while Gemini-2.5-Pro-Thinking achieves higher human preference scores."
2. **Define the "Textual" and "Geometry" columns in Table 5** explicitly, explaining whether they are the R_text/R_geom reward functions applied as evaluation metrics, and if so, why this is not circular.
3. **Add variance estimates** (confidence intervals or standard deviations) to Table 1's automatic metrics.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>