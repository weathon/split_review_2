## Summary

This paper introduces DaVinci, a multimodal LLM for parsing rasterized scientific diagrams into structured TikZ code. The approach uses a two-stage training framework: supervised fine-tuning on a curated dataset (TikZ30K) featuring drawing order normalization and comment injection, followed by reinforcement learning with GRPO guided by a hybrid reward function that leverages vectorized PDF representations for error-free spatio-textual and geometric evaluation. DaVinci-7B achieves a 97.6% compile rate on the DATiKZv3 benchmark, outperforming both open-source models and proprietary systems like GPT-5 and Claude-Sonnet-4 on most metrics.

## Strengths

- **Strong empirical results**: DaVinci-7B achieves 97.6% Pass@1 compile rate, significantly outperforming all baselines including Claude-Sonnet-4-Thinking (86.90%) and GPT-5-Default (72.88%). The improvement is substantial and robust across multiple metrics.
- **Novel reward design**: The hybrid reward function that extracts text and geometric primitives from vectorized PDF representations in an "extraction-error-free" manner is an elegant solution to the OCR error propagation problem that plagues prior work. Using the PDF metadata directly rather than OCR provides principled and accurate feedback.
- **Careful data construction**: The identification of drawing order noise and comment injection as critical data quality issues is insightful and well-motivated. The ablation study confirming that reordering (+9.04%) and comments (+5.72%) each contribute substantially to compile rate improvements validates the approach experimentally.
- **Comprehensive evaluation**: The paper includes both automatic metrics (at code and image levels) and human evaluation using Best-Worst Scaling with good inter-annotator agreement (SHR > 0.72). The ablation studies for different reward components are thorough and clearly demonstrate the contribution of each term.

## Weaknesses

### Fatal
None.

### Major
- **Metric inconsistencies undermine claimed superiority**: The paper states "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" in the abstract, but Table 1 shows Gemini-2.5-Pro-Thinking outperforms DaVinci-7B on **5 out of 8** metrics (DreamSim 88.20 vs 84.83, SigLIP 95.59 vs 93.93, SSIM 75.86 vs 73.65, TED 53.77 vs 55.13, LPIPS 21.64 vs 22.32). While DaVinci dominates on compile rate (97.60 vs 69.93), the selective reporting in the abstract and conclusion is misleading. The human evaluation (Table 3) further shows Gemini-2.5-Pro-Thinking scores 0.50 vs DaVinci-7B's -0.01 in Group 2, indicating human raters strongly prefer Gemini's outputs.
- **Limited baseline inclusion for RL comparison**: The paper does not compare against DetikZify-V2-8B or other baselines with RL post-training, making it impossible to attribute improvements specifically to the DaVinci method versus the general benefit of applying GRPO with image-based rewards to any base model on this task.
- **No discussion of GPT-5 and Claude-4 release dates**: The paper compares against "GPT-5" and "Claude-Sonnet-4" without noting these are likely earlier models available during the paper's development. By the time of publication, GPT-5o or Claude-5 might have superseded them, weakening the claimed SOTA against commercial systems.
- **Generalization concern**: The model is trained and evaluated primarily on DATiKZ-series data with temporal separation, but the scope of "scientific diagrams" tested (542 samples from DATiKZv3) is narrow. Generalization to out-of-distribution diagram types (e.g., network diagrams, Feynman diagrams, chemical structures) is not explored.

### Minor
- **7B parameter model used**: While the paper mentions scaling to 32B or 72B in future work, the current results are limited to 7B parameters. This potentially understates the approach's ultimate capability but also limits the strength of comparisons against larger proprietary models.
- **Missing analysis of RL training stability**: The paper reports 500 training steps on 8×H100-80G but does not discuss reward variance, training collapse risks, or whether the GRPO rollout of 10 is sufficient for stable optimization on this task.
- **Compile success reward design details**: The paper states `R_pass` assigns minimum values to other rewards on compile failure, but doesn't specify the exact values or whether this creates training instability when compilation fails early in training.

### Trivial
- The paper uses "TiKZ" and "TikZ" inconsistently throughout the text (both spellings appear).

## Nice-to-Haves

- Comparison against a version of DaVinci-SFT-7B fine-tuned on Original30K but with RL post-training, to disentangle RL benefits from data quality improvements.
- Evaluation on out-of-distribution diagrams, e.g., from biology, physics, or medical domains not represented in TikZ30K.
- Analysis of failure cases: the paper mentions scatter plots exceeding context limits but doesn't systematically characterize failure modes.

## Novel Insights

The key insight is that vectorized representation (PDF metadata) provides an error-free signal for both text placement and geometric primitive matching, which is fundamentally more accurate than OCR-based approaches for reward computation in diagram generation. The paper also demonstrates that for structured code generation, explicit "thinking" or reasoning traces are not beneficial—and can be harmful—relative to well-structured code with injected planning comments as implicit reasoning.

## Suggestions

1. Revise the abstract and conclusions to accurately characterize the relationship to Gemini-2.5-Pro-Thinking, noting that DaVinci-7B leads on compile rate and several code-level metrics while Gemini leads on most image-level perceptual metrics. Claiming to "surpass" all proprietary models is factually incorrect given the presented evidence.
2. Include a comparison where RL post-training is applied to a baseline model (e.g., Qwen2.5-VL-7B fine-tuned on Original30K) to isolate the benefit of the DaVinci data pipeline from the RL method itself.
3. Add a brief qualitative analysis of Gemimi-2.5-Pro's failures to contextualize its lower compile rate despite higher perceptual scores.

## Score and Decision

The paper presents a well-motivated method with strong empirical results on the compile rate metric, careful data construction, and novel reward design. However, the selective reporting that overstates superiority over all commercial models (when Gemini-2.5-Pro-Thinking clearly outperforms on most metrics) is a significant concern. The contribution is still meaningful—the data curation innovations and vectorized reward design are valuable—but the paper's framing needs substantial correction.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>