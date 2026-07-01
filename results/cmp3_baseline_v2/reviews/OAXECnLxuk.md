## Summary

The paper introduces **DaVinci**, a multimodal large language model (MLLM) for parsing raster-based scientific diagrams into structured TikZ code. It proposes a two-stage framework: (1) supervised fine-tuning (SFT) on a curated dataset **TikZ30K** with enhanced code ordering and comment annotations, followed by (2) reinforcement learning (GRPO) guided by a hybrid reward function that uses **vectorized PDF representations** to extract text and geometric elements in an error-free manner for precise feedback. The approach achieves strong results, outperforming open-source MLLMs and competing with or surpassing proprietary models like GPT-5 and Claude-Sonnet-4 on the DATiKZₜₕ test set, with a notable near-perfect compile rate after RL.

## Strengths

- **Novel and well-motivated problem formulation** – Parsing diagrams into structured, editable code is an important task with clear practical value. The paper identifies two under-explored data features (drawing order and comment annotations) and demonstrates their importance through ablation.

- **Technically sound and comprehensive methodology** – The two-stage SFT→RL framework is logically structured. The hybrid reward function that leverages vectorized representations from PDFs for extraction-error-free spatio-textual and geometric rewards is a clever design that avoids OCR/parser-induced noise.

- **Strong empirical results** – DaVinci-7B achieves a 97.60% compile rate, the highest among all compared models, and performs competitively on image-similarity metrics. Ablation studies convincingly validate each contribution (code reordering, comments, reward components).

- **Thoughtful analysis** – The paper provides insightful discussion points (e.g., "high code similarity is not necessary", "to think or not to think") that go beyond simple leaderboard comparison.

- **Human evaluation** – Best-Worst Scaling with strong inter-annotator agreement (split-half reliability >0.72) adds credible qualitative evidence.

- **Open-source release** – Code, dataset construction scripts, and model weights are publicly released with careful attention to licensing compliance.

## Weaknesses

### Major

- **Potential test-set contamination risk** – The paper states that training data is restricted to sources published **by December 2023** to ensure temporal separation from the DATiKZₒ test set (which includes data from January 2024 onward). However, the **evaluation is performed on the DATiKZₜₕ test set**, not the DATiKZₒ test set. It is unclear whether the DATiKZₜₕ test set also exclusively contains post-January 2024 data. If the test set includes diagrams from the same pre-2024 arXiv papers, TeX.SE posts, or GitHub repos used for training, then contamination is unresolved and could inflate reported results, especially the near-perfect compile rate. This concern is heightened by the paper’s own admission that they “reproduce the collection process of the DATiKZ series” – the same sources may appear in both training and test splits.

- **Overclaiming relative to Gemini-2.5-Pro** – The abstract and conclusion state that DaVinci “surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4,” but the human evaluation shows **Gemini-2.5-Pro-Thinking** significantly outperforms all other models including DaVinci-7B (score 0.50 vs -0.01 in Group 2). The automatic metrics also show Gemini leading in several image-similarity dimensions (DreamSim, SigLIP, SSIM, LPIPS). While the paper does not explicitly claim to beat Gemini, the narrative around “surpassing proprietary models” is incomplete without acknowledging this gap.

- **Single-benchmark evaluation** – All experiments are conducted on a single test set (DATiKZₜₕ, 542 examples). Generalizability to other diagram types, sources, or distributions is not demonstrated. The paper would be strengthened by at least one additional evaluation setting (e.g., cross-dataset, synthetic diagrams, or real-world user studies).

### Minor

- **Reproducibility of data construction** – The data pipeline relies on reproducing the DATiKZ series collection process, which involves scraping arXiv, TeX.SE, and GitHub. While diff files and scripts are provided, the exact composition of the final TikZ30K set may be difficult to reproduce precisely, and the filtering (using Qwen-2.5-VL-32B for quality scores and Qwen3-Coder for reordering/comment injection) introduces dependencies on proprietary models and their potential biases.

- **Reward weights not explored** – The hybrid reward is summed without learned or tuned weights. While the paper states “we do not set special weights,” it does not provide analysis of whether equal weighting is optimal or whether some components dominate training.

- **Limited RL hyperparameter analysis** – Details of GRPO training (e.g., KL penalty coefficient, learning rate schedule, reward normalization) are relegated to the appendix, which is missing from the main paper body. Without these, it is hard to assess training stability or sensitivity.

### Trivial

- The caption in Figure 2 (the block-by-block rendering description) is overly verbose and duplicates the figure text.

## Nice-to-Haves

- Test on an independent held-out dataset collected from a different time period or source to confirm generalization and contamination-free evaluation.
- Provide a comparative analysis showing the cost (compute time, API calls) of the data augmentation pipeline (reordering, comment injection) against its benefit.
- Experiment with learned reward weights (e.g., via a small validation set) to provide insight into how different reward components contribute during training.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that **code ordering in drawing languages is arbitrary but not harmless** – unlike Python, TikZ rendering is order-independent, yet autoregressive language models benefit strongly from a canonical, semantically-guided drawing order. This insight can transfer to other image-to-code tasks (e.g., SVG generation, UI code generation). Additionally, the demonstration that **explicit thinking traces are not uniformly beneficial** for structured code generation (GLM-4.5V-Thinking dropped compile rate) suggests that for code-oriented tasks, the act of code generation itself serves as implicit planning.

## Suggestions

1. **Clarify and verify test-set separation** – Provide explicit evidence that no diagram in the DATiKZₜₕ test set can appear in the training data. The current temporal filtering against the DATiKZₒ test set is insufficient because the evaluation uses a different test set. A simple analysis: show that if you train on the pre-2024 subset and evaluate on the post-2024 subset (or vice versa), performance remains strong.

2. **Adjust claims** – Replace “surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4” with a more precise statement, e.g., “achieves competitive or superior performance compared to several leading proprietary models, while trailing Gemini-2.5-Pro in human preference.” This better reflects the full results.

3. **Add additional evaluation** – Even a small-scale test on 50–100 diagrams from a different source (e.g., manually drawn figures, diagrams from Wikipedia Commons, or a held-out portion of DATiKZ from a different year) would significantly strengthen the generalizability claim.

4. **Discuss limitations of “error-free” extraction** – Acknowledge that PDF parsing with PyMuPDF can fail for certain TikZ constructs (e.g., custom paths, decorations, overlaid objects). Provide failure-case statistics from the data.

5. **Include RL training details in the main paper** – At minimum, report the learning rate, KL penalty coefficient, and number of GRPO steps to allow readers to assess training stability.

## Score and Decision

The paper presents a well-executed and novel approach to diagram parsing, with careful ablations and strong empirical results. The major concern is insufficient evidence that the test set is contamination-free, which could undermine the validity of the results. Additionally, the comparison with Gemini-2.5-Pro shows a clear gap that should be honestly reflected. If the contamination issue is satisfactorily resolved, the paper would merit a higher score. In its current form, it is on the borderline.

MY FINAL SCORE: 6.0score  
MY FINAL DECISION: Reject