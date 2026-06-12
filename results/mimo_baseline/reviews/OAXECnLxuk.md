## Summary

This paper introduces DaVinci, a multimodal LLM for scientific diagram parsing that uses a two-stage training framework: supervised fine-tuning on a curated TiKZ-30K dataset (featuring drawing order normalization and comment injection) followed by reinforcement learning with a hybrid reward function that leverages vectorized PDF representations for error-free text and geometric element extraction. The approach achieves a 97.6% compile rate and competitive image fidelity, outperforming most open-source and several proprietary models on the DATiKZ benchmark.

## Strengths

- **Well-designed reward function using vectorized representations.** The core methodological contribution—extracting text and geometric primitives directly from PDF metadata via PyMuPDF rather than relying on OCR—is genuinely motivated by real failure cases (Appendix E.4 examples cited). The bipartite matching for text (exact-then-fuzzy with Levenshtein distance) and Hungarian algorithm for geometric elements are principled approaches that cleanly avoid OCR/heuristic extraction errors. Ablation results in Table 5 show each reward component contributes incrementally and consistently across all metrics.

- **Effective data engineering with strong ablation support.** Drawing order normalization and comment injection are well-motivated by autoregressive training dynamics (noisy orderings produce multiple arbitrary code sequences for similar visuals, degrading SFT). Table 4 cleanly isolates each contribution: reordering alone yields +9.04% compile rate, comments add +5.72%. The use of a 5-point quality scoring via Qwen-2.5-VL-32B and rule-based filtering is a practical and reproducible quality control pipeline.

- **Insightful observation on code similarity vs. visual fidelity.** The finding that RL training *decreases* cBLEU while improving all visual and compilation metrics (Table 1, DaVinci-SFT-7B vs. DaVinci-7B) is a valuable contribution to the image-to-code community, demonstrating that strict code-level similarity is neither necessary nor sufficient for visual quality.

- **Comprehensive evaluation methodology.** The paper reports results across 8 automatic metrics spanning code-level and image-level quality, conducts two rounds of human evaluation with Best-Worst Scaling including inter-annotator reliability (SHR > 0.72), and provides thorough ablation studies. The evaluation is more rigorous than typical for this venue.

## Weaknesses

### Fatal
None.

### Major

- **Abstract claim about surpassing proprietary models is selective.** The abstract states DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4," and while this holds for automatic metrics and human evaluation (Table 3: DaVinci -0.01 vs. GPT-5 -0.13 and Claude -0.35), Gemini-2.5-Pro decisively outperforms DaVinci in both human evaluation (0.50 vs. -0.01) and on key perceptual metrics (DreamSim: 88.20 vs. 84.83; SigLIP: 95.59 vs. 93.93). The abstract and title framing could be more transparent about the remaining gap with the strongest proprietary model.

- **"Error-free" extraction characterization is overstated.** The text repeatedly describes the vectorized extraction as "error-free," yet the matching pipeline involves Levenshtein distance with an adaptive threshold and Hungarian matching with heuristically defined cost functions. While this avoids OCR classification errors, the matching procedure introduces its own failure modes (e.g., ambiguous one-to-many text matches, imperfect geometric attribute weighting). Quantifying the matching accuracy or providing error analysis of the reward signals themselves would strengthen this claim.

- **Single model scale explored.** All DaVinci variants are trained from Qwen2.5-VL-7B-Instruct. Given that the baselines include 72B and 106B models (which are generally outperformed by DaVinci-7B but approach it), demonstrating that the framework's gains persist or improve with larger base models would significantly strengthen the contribution's generality.

### Minor

- **No weighting ablation for hybrid reward.** Equation 2 uses equal weights for all four reward components, but these operate on different scales (compile success is binary 0/1, image fidelity is continuous). An ablation on weighting strategies or learned weights could potentially yield further improvements.

- **Limited failure analysis.** Beyond mentioning scatter plots as failure cases, there is no systematic error categorization. A taxonomy of failure modes (e.g., text-heavy diagrams, complex curved geometries, dense visualizations) with frequencies would be valuable for guiding future work.

- **GRPO hyperparameter sensitivity.** With rollout number=10, batch size=256, and 500 steps on 8×H100, the sensitivity to these choices is not discussed. Given the relatively short training, even rough ablation would be informative.

## Nice-to-Haves
- A version of DaVinci at 32B or 72B scale to demonstrate the framework's scalability
- Quantitative analysis of the vectorized extraction matching accuracy (e.g., human-verified precision/recall of text and geometric element matching)
- Error taxonomy with frequency analysis across diagram types

## Novel Insights

The paper's most novel insight is that diagram parsing benefits from a reward signal derived directly from vectorized PDF representations rather than from pixel-level comparison or OCR-based extraction. By exploiting TikZ's compilation to PDF—where text objects retain exact typographic metadata and geometric primitives are preserved as native vector elements—the authors construct reward signals that are more precise than image-based alternatives while avoiding the noise of visual recognition pipelines. This insight is generalizable: any system that generates vector graphics could benefit from similar vectorized reward extraction for RL training.

## Suggestions

- Consider adding a brief comparison with equal-weight vs. weighted reward combinations in the ablation to justify the design choice
- Acknowledge the gap with Gemini-2.5-Pro more explicitly and discuss potential reasons (model scale, training data diversity, architectural differences)
- Include a small-scale experiment or analysis suggesting the framework transfers to larger base models

## Score and Decision

The paper presents a solid and well-executed contribution to diagram parsing with genuine methodological innovations (vectorized reward extraction, data ordering/comments) supported by thorough ablations and evaluation. The main weaknesses are selective framing of results relative to the strongest proprietary model and some overclaimed properties of the extraction pipeline, but these do not invalidate the core contributions. The work is well-positioned as a strong empirical study with practical impact for the image-to-code community.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>