## Summary

This paper introduces DaVinci, a multimodal LLM for parsing raster-based scientific diagrams into structured TikZ code. The method uses a two-stage framework: supervised fine-tuning on a curated dataset (TikZ30K) with optimized drawing order and comment annotations, followed by reinforcement learning (GRPO) with a hybrid reward function that leverages vectorized representations for error-free spatio-textual and geometric feedback. Experiments show DaVinci-7B achieves a 97.60% compile rate and outperforms both open-source and proprietary models including GPT-5 and Claude-Sonnet-4 on diagram parsing benchmarks.

## Strengths

- **Novel and well-motivated two-stage framework**: The combination of SFT with code reordering/comment injection followed by RL with a carefully designed hybrid reward is a principled approach to the diagram parsing problem. The identification of drawing order noise and comment scaffolding as underexplored data features is insightful and empirically validated.

- **Strong empirical results**: DaVinci-7B achieves a 97.60% compile rate, significantly outperforming all baselines including proprietary models like GPT-5 (72.88%) and Claude-Sonnet-4 (84.87%). The human evaluation confirms these gains, with DaVinci-7B scoring highest among non-proprietary models and competitive with Gemini-2.5-Pro.

- **Innovative reward design**: The use of vectorized PDF representations to extract text and geometric primitives in an "error-free" manner is a clever solution to the OCR error propagation problem. The spatio-textual and geometric rewards provide more precise feedback than pixel-level or perceptual metrics alone.

- **Comprehensive evaluation**: The paper includes both automatic metrics across code and image levels, human evaluation using Best-Worst Scaling with strong inter-annotator agreement, and thorough ablation studies validating each component.

## Weaknesses

### Major

- **Limited base model scale and generalizability**: The experiments are conducted only on Qwen2.5-VL-7B. While the results are impressive, it is unclear whether the proposed techniques generalize to other base models (e.g., LLaVA, InternVL) or larger scales. The paper claims superiority over 72B and 106B models, but this is achieved with a 7B model, which is notable but raises questions about whether the gains are specific to this particular base model or the training recipe.

- **Potential data contamination concerns**: The training data is sourced from arXiv papers and TeX.SE up to December 2023, while the test set (DATiKZv3) includes data from January 2024 onward. However, the paper does not provide sufficient analysis of the semantic overlap between training and test distributions. Since both are scientific diagrams from similar sources, there may be structural similarities that inflate performance. A more rigorous contamination analysis (e.g., measuring nearest-neighbor similarity between train and test images) would strengthen the claims.

- **Incomplete comparison with Gemini-2.5-Pro**: The human evaluation (Group 2) shows Gemini-2.5-Pro-Thinking significantly outperforms DaVinci-7B (score 0.50 vs -0.01), yet the paper's abstract claims DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" without mentioning Gemini. The automatic metrics also show Gemini leading on DreamSim, SigLIP, SSIM, and LPIPS. The paper should be more transparent about where Gemini outperforms DaVinci and discuss the trade-offs (compile rate vs. visual fidelity).

### Minor

- **RL training details are sparse**: The paper mentions 500 steps of GRPO training on 8×H100-80G but does not report training curves, reward convergence, or the impact of the rollout number (G=10) on performance. These details would help practitioners reproduce the work.

- **The "error-free" claim is slightly overstated**: While PDF vectorization avoids OCR errors, the matching procedure (Algorithm 1) still uses Levenshtein distance with an adaptive threshold, which can introduce matching errors. The paper acknowledges this indirectly but the term "error-free" in the abstract and contributions is too strong.

- **Code efficiency metrics are relegated to appendix**: Table 7 (mentioned in the text) is not included in the main paper. Given the practical importance of code efficiency for downstream editing, these results should be in the main body.

### Trivial

- The paper uses "TiKZ" and "TikZ" inconsistently throughout (e.g., "TiKZ30K" vs "TikZ code"). Standard capitalization is "TikZ".

## Nice-to-Haves

- Analysis of which types of diagrams (flowcharts, neural network diagrams, plots, etc.) benefit most from each component of the method
- Ablation on the number of rollout samples G in GRPO
- Qualitative failure case analysis beyond "context limit exceeded"
- Discussion of inference cost (tokens generated, time) compared to baselines

## Novel Insights

The key insight is that for structured code generation tasks like diagram parsing, the code itself serves as an implicit reasoning process, making explicit "thinking" traces unnecessary and potentially harmful (as shown by the GLM-4.5V-Thinking degradation). This challenges the prevailing trend of adding reasoning chains to MLLMs and suggests that task-specific structural priors (drawing order, comments as planning scaffolds) are more effective than general-purpose reasoning. Additionally, the finding that high code similarity (cBLEU) is not necessary for high-quality diagram parsing—and can even be anti-correlated with visual fidelity after RL—is a valuable observation for the image-to-code community.

## Suggestions

- Add a contamination analysis showing the distribution of nearest-neighbor distances between training and test images, or perform a temporal split analysis to verify that performance does not degrade on diagrams from significantly different time periods.
- Include training curves (reward, compile rate over RL steps) to demonstrate convergence and stability.
- Report results on at least one additional base model (e.g., LLaVA-NeXT or InternVL2) to demonstrate generalizability of the two-stage framework.
- Add a discussion of the computational cost of the reward computation (PDF parsing, Hungarian matching) and whether it scales to larger batch sizes.

## Score and Decision

The paper presents a well-executed, novel approach to a challenging problem with strong empirical results. The two-stage framework, data augmentation strategies, and hybrid reward design are all technically sound and clearly motivated. The main limitations are the single base model evaluation and the incomplete comparison with Gemini-2.5-Pro, which actually outperforms DaVinci on several metrics. However, the core contributions are significant and the paper is clearly written. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>