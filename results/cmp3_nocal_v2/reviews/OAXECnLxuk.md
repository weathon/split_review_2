## Summary

This paper introduces DaVinci, a two-stage framework (SFT followed by GRPO-based RL) for parsing rasterized scientific diagrams into executable TiKZ code. The contributions are threefold: (1) TiKZ-30K, a curated dataset with semantically reordered code and injected comment annotations as planning scaffolds, (2) a hybrid reward function that leverages PDF vectorization (via PyMuPDF) to extract textual and geometric primitives for precise reward signals, and (3) strong empirical results showing a 7B model achieving 97.6% compile rate and competitive visual fidelity against much larger proprietary and open-source models.

## Strengths

1. **Novel and well-motivated reward design using PDF vectorization (Section 3.3, R_text and R_geom).** Extracting text and geometric primitives from the PDF compilation of TiKZ code—rather than running error-prone OCR on rendered images—is a genuinely clever idea. The paper provides concrete failure cases of OCR in the appendix and demonstrates a clean workaround using PyMuPDF to access ground-truth vector metadata. This is the most technically interesting contribution.

2. **Clear evidence that code reordering and comment injection substantially improve SFT (Table 4).** The ablation is clean: Original30K → Reordering30K → TikZ30K yields Pass@1 improvements of 69.74% → 78.78% → 84.50%. The 9.04% gain from reordering alone and the additional 5.72% from comments directly validate the paper's core data-side thesis. This is the strongest evidence in the paper.

3. **Impressive compile rate (97.60%) from a 7B model.** Achieving near-perfect compilability with a 7B open-weight model, while much larger proprietary models lag significantly (GPT-5-Default: 72.88%, Gemini-2.5-Pro-Thinking: 69.93%), is a meaningful practical achievement with clear deployment advantages.

4. **Well-designed human evaluation using Best-Worst Scaling with split-half reliability reporting.** BWS avoids the calibration problems of Likert-scale ratings. Reporting SHR values (ρ=0.72, 0.79) gives readers a quantitative handle on annotator agreement, which is more rigorous than most human evaluations in the MLLM literature.

5. **Thoughtful data release strategy.** The paper respects licensing constraints by providing diff files and reproducible scripts for non-redistributable sources, rather than ignoring license terms or avoiding release altogether.

## Weaknesses

### Fatal
None.

### Major
None. The issues below are real but addressable without changing the method or invalidating the core claims.

### Minor

1. **Abstract/conclusion framing overstates the case against proprietary models.** The abstract says DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" and the conclusion repeats similar language. The body does acknowledge that Gemini-2.5-Pro-Thinking outperforms DaVinci on human evaluation (score 0.50 vs. -0.01 in Group 2, Table 3) and on several automatic metrics (DreamSim, SigLIP, SSIM, LPIPS, TED in Table 1). The claims about GPT-5 and Claude-Sonnet-4 are factually correct, but the overall narrative glosses over Gemini's superior performance. The paper should either explicitly limit the headline claim to the specific models it beats, or discuss the Gemini tradeoff in the abstract. This is a framing issue, not a methodological flaw.

2. **DetikZify-V2-8B comparison is missing a key detail about inference configuration.** The paper mentions DetikZify's MCTS-based inference (Section 2, line 30) but does not state whether the numbers reported in Table 1 include MCTS or not. If DetikZify-V2-8B is evaluated without its characteristic inference-time optimization, the comparison is unfair to DetikZify. If it includes MCTS, the paper should state this explicitly, as it compares training-time optimization (DaVinci's RL) against test-time compute (DetikZify's MCTS), which is informative only if disclosed.

3. **Reward ablation shows limited independent metric improvement, raising a mild circularity concern.** In Table 5, the Base (R_img + R_pass) condition already achieves strong results. Adding R_text and R_geom produces mixed changes on independent metrics (DreamSim: 85.00 → 84.75; SigLIP: 93.67 → 93.93; SSIM: 73.07 → 74.01). The largest improvements are on the paper's own Textual (37.23 → 42.28) and Geometry (41.44 → 44.10) metrics, which are computed using the same PDF-vectorization matching procedure that R_text and R_geom optimize. This is a clear case where the evaluation metric and the reward are measuring the same thing. The paper should acknowledge this and clarify what independent signal the geometric/textual rewards add beyond DreamSim+MSE.

4. **Pass@1 compile rate is not reported in the reward ablation (Table 5).** Since the 97.60% compile rate is one of DaVinci's headline results, it is essential to show whether adding R_text and R_geom affects compilability relative to the Base (R_img + R_pass) condition. This is a one-line addition to the table.

5. **No statistical significance testing or confidence intervals in automatic evaluation (Table 1).** With 542 test samples, it is impossible to tell whether DaVinci-7B's DreamSim score of 84.83 is meaningfully different from DetikZify-V2-8B's 82.63 or Claude-Sonnet-4's 83.81. Reporting confidence intervals or significance tests would strengthen the paper.

6. **Prompt template for baseline models is not specified.** The quality of outputs from instruction-tuned proprietary models is highly sensitive to prompt phrasing. The paper shows a prompt in Figure 3's caption but does not state whether the same template was used for all baselines. This is a reproducibility concern.

### Trivial

1. **"Extraction-error-free" phrasing could be more precise.** The paper uses "extraction-error-free" (lines 34, 40, 52, 122) to describe the process of reading text/geometric metadata from PDF vectorization—and this step genuinely avoids OCR errors. However, the subsequent matching between predicted and ground-truth elements (Levenshtein distance with adaptive threshold, Hungarian algorithm) necessarily involves heuristics. A reader may conflate extraction with matching. The paper should clarify that "extraction" is error-free (from PDF metadata), while "matching" between two sets of extracted elements remains approximate.

## Nice-to-Haves

- **Inference cost or latency analysis.** The paper does not discuss inference cost, which is relevant for practical deployment, especially compared to MCTS-based methods like DetikZify that use test-time compute.
- **Qualitative error taxonomy beyond compile failures.** The paper mentions that remaining compile failures involve dense scatter plots exceeding context limits, but does not analyze cases where code compiles but produces poor visual output.
- **Hold-out validation on different diagram domains.** Results are reported on a single benchmark (DATiKZv3, 542 samples). While this is the standard benchmark, testing on held-out sources would strengthen claims of generalization. The temporal cutoff (December 2023) provides some protection, but a distribution overlap concern remains.

## Removed Points

The following points from the input review were assessed and moved here with justification:

- **"Error-free characterization is overstated and conflates extraction with matching"** (from Critical Issue 2): The paper uses "extraction-error-free" specifically—the extraction from PDF vectorization genuinely avoids OCR errors. The reviewer conflated extraction with matching. The paper is reasonably clear about the distinction, though minor phrasing tightening is noted as Trivial above. The stronger version of this criticism is invalid.
- **Data distribution overlap concern:** The paper explicitly addresses this with a temporal cutoff (sources published by December 2023, test set from January 2024 onward). This is well-handled.
- **"Low variance suggests reward components contribute less than claimed":** The milder version of this concern is retained as Minor weakness #3. The "contradicts the paper's claims" framing is too strong given that Textual/Geometry metrics do improve meaningfully (37.23→42.28, 41.44→44.10), even if independent metrics show smaller gains.
- **Various section-by-section notes about Qwen-2.5-VL-32B evaluator bias, stratified sampling rationale, and Qwen3-Coder-480B cost:** These are implementation details that do not undermine the paper's claims. The paper's reasonable handling of these choices is noted but does not rise to the level of a weakness.
- **"Implicit weighting scheme analysis" for reward components:** The paper states rewards are summed with "no special weights" (line 118). Further analysis would be nice but is not a weakness—the paper's ablation (Table 5) empirically evaluates the contribution of each component.
- **"Related work on SVG generation is thin":** Removing per the instruction not to mention missing related works.

## Novel Insights

None beyond the paper's own contributions. The reviews confirmed the paper's strengths (PDF vectorization for reward signals, data reordering/comments) and raised some constructive clarity concerns, but did not surface a novel meta-level insight about the approach or the problem.

## Suggestions

1. **Reframe the abstract and conclusion.** Either explicitly limit claims to GPT-5 and Claude-Sonnet-4, or add a brief qualifier noting that Gemini-2.5-Pro-Thinking shows stronger performance on some visual fidelity metrics and in human evaluation, while DaVinci leads on compile rate and open-weight accessibility.

2. **Clarify the DetikZify-V2-8B comparison.** State explicitly whether the reported numbers include MCTS-based inference, and discuss what this means for interpreting the comparison.

3. **Add Pass@1 to the reward ablation table.** This is a one-line addition that directly addresses whether the RL reward components preserve compilability.

4. **Acknowledge the circularity between reward terms and evaluation metrics.** Discuss what independent signal the textual and geometric rewards provide beyond what DreamSim+MSE capture, and ideally validate that these reward components correlate with human judgments (the human evaluation data already exists).

5. **Specify the prompt template** used for all baseline models, either in the main text or in the appendix.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>