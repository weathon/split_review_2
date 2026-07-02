## Summary
# Final Review Report

## Summary

This paper introduces DaVinci, a multimodal large language model (MLLM) for parsing rasterized scientific diagrams into executable TiKZ code. The core contributions are: (C1) a two-stage training framework combining supervised fine-tuning (SFT) on curated data followed by reinforcement learning (RL) with GRPO; (C2) the TiKZ30K dataset featuring code reordering and comment annotations as planning scaffolds; and (C3) a hybrid reward function that leverages PDF vectorized representations for extraction-error-free spatio-textual and geometric rewards. 

Extensive experiments on the DATiKZ_v3 benchmark demonstrate that DaVinci-7B achieves a near-perfect compile rate (97.60%), surpassing existing open-source models and several proprietary MLLMs on code-level metrics. However, the claimed superiority over all proprietary models is not fully supported by the evidence — Gemini-2.5-Pro-Thinking leads on perceptual similarity metrics (DreamSim 88.20 vs 84.83, SSIM 75.86 vs 73.65, LPIPS 21.64 vs 22.32) and in human evaluation (score 0.50 vs DaVinci-7B's -0.01 in Group 2). The paper's main strengths lie in its novel data augmentation strategy (code reordering + comments injection) and the vectorized-representation-based reward design. Key weaknesses include overclaimed SOTA results, insufficient methodological detail for reproducibility of the reward functions, and limitations in the human evaluation protocol. Novelty verification is deferred due to external literature search being unavailable in this run.

## Strengths
**S1. Novel data augmentation strategy (code reordering + comment injection).** The identification of drawing order noise as a training impediment for autoregressive code generation is technically sound and well-motivated. Using Qwen3-Coder to reorder TiKZ code into a semantics-guided protocol, and injecting comments as planning scaffolds, addresses a genuine limitation of SFT on raw collected data. The ablation study (Table 4) provides clear evidence: reordering alone improves Pass@1 by +9.04%, and comments add another +5.72%. This is a reproducible, practical contribution that could benefit other code generation domains.

**S2. Vectorized-representation-based reward design.** The hybrid reward function (Eq. 2-5) innovatively uses PDF metadata via PyMuPDF to extract text and geometric elements without relying on error-prone OCR. This is a principled approach that directly addresses the spatial-textual alignment problem in diagram parsing, where OCR failures are common due to diverse symbols and overlapping elements. The ablation of rewards (Table 5) confirms that $R_{\text{text}}$ and $R_{\text{geom}}$ provide complementary signals beyond image-level metrics, improving the textual score from 37.23 to 42.28 and geometry score from 41.44 to 44.10.

**S3. Strong empirical results on compile rate.** DaVinci-7B achieves 97.60% Pass@1 compile rate on the DATiKZ_v3 test set (542 samples), substantially outperforming all baselines including DetikZify-V2-8B (78.60%), Claude-Sonnet-4-Thinking (86.90%), and GPT-5-Default (72.88%). This near-perfect compilation rate is practically significant for downstream usability.

**S4. Comprehensive evaluation with human studies.** The human evaluation using Best-Worst Scaling (BWS) with 6 annotators and split-half reliability checks (SHR 0.7227 and 0.7878) demonstrates methodological rigor beyond automatic metrics alone. The inclusion of two comparison groups (non-proprietary and proprietary) provides a nuanced view of model performance.

**S5. Open-science commitment.** The paper provides a detailed data release plan respecting original licenses (diff files for arXiv content, direct release for permissively licensed sources), which enhances reproducibility while maintaining legal compliance.

## Weaknesses
**W1. Overclaimed state-of-the-art results (major).** The Abstract and Conclusion state that DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" and achieves "state-of-the-art performance." This is not fully supported by the evidence:
- Gemini-2.5-Pro-Thinking (also a leading proprietary model) outperforms DaVinci-7B on DreamSim (88.20 vs 84.83), SSIM (75.86 vs 73.65), SigLIP (95.59 vs 93.93), and LPIPS (21.64 vs 22.32) — 4 out of 8 main metrics.
- In Human Evaluation Group 2 (Table 3), DaVinci-7B scores -0.01 (near chance) while Gemini-2.5-Pro-Thinking scores 0.50. This directly contradicts the "surpasses leading proprietary models" narrative.
- The paper selectively omits Gemini from the proprietary model list in the Conclusion.
- *Repair path:* The Abstract and Conclusion must be revised to bound the claims. A defensible version would state the metric-specific and conditional nature of the results, explicitly noting that Gemini-2.5-Pro leads on perceptual similarity while DaVinci leads on compile rate. (See annotations on Abstract and Conclusion.)

**W2. Missing methodological details for reward reproducibility (major).** Several critical details of the hybrid reward function are underspecified:
- The geometric cost function $C(e_p, e_g)$ in Eq. (4) uses attribute weights that are not reported. The scaling constant $k$ is unspecified.
- The Hungarian matching algorithm's treatment of unmatched elements (false positives/negatives) is not defined — the normalization by $\max(|E_{pred}|, |E_{gt}|)$ implicitly penalizes missing/hallucinated elements, but the matching cost for unmatchable elements is not specified.
- $R_{\text{img}}$ (Eq. 5) adds DreamSim [0,1] and a clipped MSE term [-1,1] without explicit weighting, making the effective contribution of each term dataset-dependent. The normalization parameters ($\mu$, $\sigma$, $s$) are not fully specified.
- The paper states "we do not set special weights for each reward component," implying equal weighting, but the different numerical ranges mean the weights are effectively unequal.
- *Repair path:* Provide exact cost functions with weights, the value of $k$, the matching threshold policy, and a discussion of reward range balancing. (See annotations on Method 3.3.)

**W3. Human evaluation design limitations (major).** The human evaluation has several concerns:
- Only 6 graduate student annotators from a narrow demographic (age 23-29), which may not represent the broader population of diagram users.
- DaVinci-7B appears in both groups but Gemini-2.5-Pro appears only in Group 2, preventing a direct head-to-head comparison. The paper uses this split design to claim superiority over proprietary models, but the Group 2 results actually show DaVinci-7B at -0.01 (near random) vs. Gemini at 0.50.
- The 100-item sample from a 542-item test set may not be fully representative.
- *Repair path:* Add a direct comparison group between DaVinci-7B and Gemini-2.5-Pro, or report the statistical significance of the score differences. (See annotation on Human Evaluation.)

**W4. Dataset representativeness concerns (minor).** The TiKZ30K dataset is filtered heavily from 366K to ~30K (8.2% retention). Critical concerns:
- The Qwen-based quality scoring (scores 4-5 out of 5) could introduce systematic bias against certain diagram categories (e.g., dense plots, complex mathematical diagrams). No category-level retention analysis is provided.
- Stratified sampling by token length is performed, but the final 30K may not represent the full distribution of diagram types in the original pool.
- The temporal cutoff (pre-2024) is properly handled for test set contamination, but diagram styles may shift over time.
- *Repair path:* Report category-level retention rates and discuss potential distribution bias. (See annotation on Data Collection.)

**W5. Incomplete ablation analysis (minor).** The data ablation study (Table 4) evaluates only Pass@1, but the paper's contribution spans multiple quality dimensions. The reward ablation (Table 5) is more thorough but uses a different base setting (DaVinci-SFT-7B + base reward), making it hard to connect data improvements to final visual quality.
- *Repair path:* Report full metrics (DreamSim, SSIM, MSE, textual, geometry) for each data condition (Original30K, Reordering30K, TikZ30K). (See annotation on Ablation Study.)

**W6. Weak novelty positioning (deferred verification).** The paper builds directly on the DATiKZ series (Belouadi et al., 2024a,b; 2025) and Detikzify. The claimed novelties — code reordering, comment injection, and vectorized-representation rewards — are incremental improvements over prior work. Without external literature verification (unavailable in this run), a definitive novelty assessment cannot be made. However, the paper would benefit from:
- A clearer comparison with Detikzify-V2's MCTS-based inference approach and why the RL-based approach is fundamentally different.
- Explicit discussion of overlap and residual novelty relative to ChartMaster (Tan et al., 2025) and Rodriguez et al. (2025b), which also use RL-based rewards for code generation.

## Score
**Final Score: 6.5/10**

*Rationale:* The paper presents technically sound contributions — code reordering as data augmentation and vectorized-representation-based rewards are practical innovations with clear ablation support. The empirical results demonstrate strong compile rate improvements. However, the score is tempered by: (1) overclaimed state-of-the-art results that are contradicted by the paper's own human evaluation and perceptual metrics where Gemini-2.5-Pro leads; (2) insufficient methodological detail for reproducibility of the reward functions; (3) limitations in the human evaluation design that weaken the evidence for superiority over proprietary models; and (4) novelty assessment is deferred due to unavailable external literature verification, meaning the incremental nature over prior work (DATiKZ series, Detikzify) cannot be fully evaluated. The research value of the data augmentation strategy and reward design is solid, but the presentation undermines credibility through selective reporting.