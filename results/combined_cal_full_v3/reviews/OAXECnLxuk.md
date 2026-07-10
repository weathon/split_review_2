Now I have all the information needed. Here is the final consolidated review.

---

## Summary

This paper introduces DaVinci, an MLLM for parsing raster scientific diagrams into TikZ code, using a two-stage SFT+RL framework. The main contributions are: (1) a curated dataset TikZ-30K with optimized drawing order and comment annotations, (2) a hybrid RL reward that leverages PDF vectorized representations to extract text and geometric primitives without OCR errors, and (3) strong empirical results including a 97.60% compile rate. The approach is evaluated on the DATiKZ_v3 benchmark against proprietary and open-source models.

## Strengths

- **Reward design using vectorized representations (Section 3.3):** The core technical idea — extracting text and geometric primitives from PDF vectorized representation rather than relying on OCR — is genuinely well-motivated and well-executed. Using PyMuPDF to directly access ground-truth text objects and geometric metadata avoids a real source of error that would plague any OCR-based reward. The two-step exact-then-fuzzy matching for text and Hungarian-algorithm-based geometric matching are sensible implementations. This is the paper's clearest technical contribution.

- **Data quality improvements (Section 3.2):** The identification of two underexplored issues — noisy drawing order and missing comment annotations — is insightful. The ablation in Table 4 convincingly shows their impact: code reordering alone improves compile rate by 9.04 percentage points (69.74% → 78.78%), and adding comments brings another 5.72 points (78.78% → 84.50%). These are meaningful, well-isolated gains that validate the direction.

- **Strong compile rate after RL (Table 1):** DaVinci-7B's 97.60% Pass@1 compile rate is clearly the best among all compared models, including proprietary ones (next best: Claude-Sonnet-4-Thinking at 86.90%). This is a genuine engineering achievement that substantially advances the state of the art in compile reliability for TikZ generation.

- **Human evaluation methodology (Section 4.4):** The use of Best-Worst Scaling with six annotators, reporting split-half reliability (0.72 and 0.79), is more rigorous than typical BWS reporting in the diagram-generation literature and adds credibility to the subjective evaluation.

- **Ablation study of reward components (Table 5):** The paper systematically ablates each reward component, showing that adding R_text and R_geom progressively improves textual and geometric accuracy metrics while maintaining or improving image quality metrics. This provides clear evidence for the contribution of each component.

## Weaknesses

### Fatal
None.

### Major

- **Selective framing of claims against proprietary models:** The abstract and conclusion state DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4." While this is accurate for those two models, Gemini-2.5-Pro-Thinking beats DaVinci on 4 of 8 automatic metrics (DreamSim, SigLIP, SSIM, LPIPS) and dominates in human evaluation (BWS score 0.50 vs −0.01). The paper acknowledges Gemini's strength in Section 4.4 ("Gemini-2.5-Pro-Thinking significantly outperforms all other models in both groups"), but this acknowledgment is absent from the abstract and conclusion, creating a misleading impression of overall superiority. The human evaluation Group 2 (Table 3) further contextualizes this: DaVinci-7B's BWS score is −0.01 (p_best=0.20, p_worst=0.21) — essentially at chance level against the proprietary model set. While DaVinci outperforms GPT-5-Default and Claude-Sonnet-4-Thinking in this group, the headline claim needs recalibration to honestly reflect the trade-off: DaVinci achieves a far superior compile rate, but Gemini produces outputs human evaluators substantially prefer.

- **No systematic error analysis of successfully compiled but visually wrong outputs:** The paper reports 97.60% compile rate but provides no taxonomy of errors in compiled outputs that are visually incorrect (wrong text labels, misplaced elements, missing components, color errors, etc.). The only failure case discussed (scatter plots exceeding context length) does not constitute a systematic analysis. A TikZ diagram can compile perfectly while being semantically wrong. The human evaluation partially addresses this gap, but a structured error categorization (e.g., a 200-sample manual analysis) would substantially strengthen the paper by revealing what kinds of errors remain and whether the RL reward components adequately address them.

### Minor

- **The "error-free" claim is overstated:** The paper uses "extraction-error-free" and "error-free" (lines 34, 40, 52, 106, 122) to describe the PDF-based extraction. While the *extraction* step (reading PDF metadata via PyMuPDF) is indeed exact, the downstream *matching* steps are heuristic: Levenshtein distance with an adaptive threshold (text matching), Hungarian algorithm with an unreported-cost-function (geometric matching), and Distance-IoU tie-breaking. These can produce false or missed matches. The paper should clarify that the extraction is error-free but the matching pipeline is not, to avoid overclaiming.

- **Unweighted reward components with different scales (Equation 2):** The hybrid reward sums R_text, R_geom, R_img, and R_pass without weighting coefficients. R_img combines DreamSim (~0–1) with a clipped MSE term (range −1 to 1), while R_text and R_geom are normalized to [0,1] and R_pass is effectively binary (zero on failure). These components have different ranges and distributions, so unweighted summation likely means R_img dominates numerically. The paper says "we do not set special weights" (line 118) but should either justify why no weighting is needed or report empirical ranges of each component during training.

- **"Texual" and "Geometry" metrics in Table 5 are not defined:** The ablation table reports "Texual ↑" and "Geometry ↑" metrics but Section 4.2 (Metrics) does not define how these are computed or what the reported values (e.g., 42.28) represent. These likely reflect text/geometry matching accuracy from the reward functions, but this needs explicit definition.

### Trivial
None.

## Nice-to-Haves

- A structured error analysis of successfully compiled outputs (e.g., manual categorization of 200 samples) would strengthen the paper by showing remaining failure modes.
- Reporting the empirical ranges of each reward component during RL training would clarify whether the unweighted sum is dominated by any one component.
- The "Gemini significantly outperforms all other models in both groups" phrasing in Section 4.4 is slightly imprecise since Gemini only appears in Group 2; rewording would improve clarity.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Test set distributional overlap:** Removed. The paper explicitly addresses temporal separation (training data pre-December 2023, test set from January 2024 onward). The concern about distributional similarity across time periods from the same sources is speculative and generic — the paper cannot be expected to test generalization to entirely different diagram sources when evaluated on the established benchmark.
- **Qwen-based reordering bias:** Removed. The paper ablates this (Table 4 shows improvements over non-reordered data) and the concern is speculative (Qwen3-Coder-480B ≠ Qwen2.5-VL-7B).
- **Missing GRPO hyperparameters:** Removed. The paper reports batch size, rollout number, and steps. Requesting learning rate, KL coefficient, etc., is a nice-to-have but not a weakness.
- **No inference cost comparison:** Removed. Scope creep — the paper does not claim efficiency improvements.
- **No split criterion for 30K/28K SFT/RL split:** Removed. Trivial implementation detail.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Reframe the headline claims:** Replace "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" with a more precise statement: "achieves a near-perfect 97.60% compile rate, substantially outperforming all baselines on code correctness, while being competitive with proprietary models on visual metrics, with Gemini-2.5-Pro-Thinking showing superior human preference scores despite a lower compile rate." The trade-off between compilability and human-judged visual quality is itself an interesting finding worth exploring.
- **Define the missing metrics:** Add definitions for "Texual" and "Geometry" in Section 4.2.
- **Add an error taxonomy:** Even a small-scale manual categorization of errors in compiled outputs would help readers understand the model's failure modes.

## Score and Decision

Let me calibrate against anchors.

**Round 1 bracket (exploratory):** I searched six score bands for topically similar papers. The most relevant anchors are AutomaTikZ (avg 6.50, accepted) and Sketch2Diagram (avg 6.25, accepted) — both tackle TikZ diagram generation. The Coarse-Tuning with RL Feedback paper (avg 4.75, rejected) is methodologically similar (RL + code + compiler feedback). No highly related papers scored above 8.5. **Initial bracket: 4.75 – 6.50.**

**Round 2 narrowing:** I examined itemized favorability ratings from the anchors.

- **AutomaTikZ (6.50):** Strength favorabilities 7.14–12.39; weakness favorabilities −4.15 to 6.84. Weaknesses were about modest technical contribution and limited ablation — genuine but not central.
- **Sketch2Diagram (6.25):** Strength favorabilities 8.16–8.55; weakness favorabilities −0.08 to 6.46. Weaknesses were about missing comparisons and minor technical contribution.
- **Coarse-Tuning RL (4.75):** Strength favorabilities 7.80–10.90; weakness favorabilities −3.36 to 4.84 (including "not comparing to GPT-3/4" at −3.36 and "limited to Java" at −0.12). Weaknesses were more fundamental (incomplete comparisons, limited scope).

**My paper's itemized favorability:** Strengths 9.84–10.81 (strong, comparable to anchors). Weaknesses at 0.32 (human eval chance level) and 2.73 (selective framing) are more damaging than any weakness in the accepted anchors — the lowest favorability weakness in AutomaTikZ was −4.15 (modest technical contribution) and in Sketch2Diagram was −0.08 (no open-source comparison). Both the 0.32 and 2.73 items address the central claim of the paper. The remaining weaknesses (4.15–6.79) are more typical minor issues.

My paper clearly surpasses Coarse-Tuning RL (4.75) in scope, depth, and completeness. However, the accepted TikZ anchors (6.25, 6.50) did not have a weakness that directly undermined their headline claim. The framing issue and chance-level human evaluation in Group 2 create a real gap between this paper's claimed scope and its demonstrated evidence.

**Final score: 5.5** — borderline. The technical contributions are genuine and well-validated through careful ablation. However, the paper overstates its competitive position relative to proprietary models in the abstract and conclusion, and the human evaluation Group 2 result shows DaVinci at chance level when compared against the strongest proprietary model. These are addressable issues: reframing the claims and adding a structured error analysis would significantly strengthen the paper.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>