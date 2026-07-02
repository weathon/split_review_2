Now let me finalize my review with calibrated scoring.

## Summary

DaVinci introduces a two-stage SFT+RL framework for parsing scientific diagrams into TiKZ code. Key contributions are: (1) a curated TikZ30K dataset featuring LLM-based code reordering and comment injection as planning scaffolds, validated via ablation to yield +14.76% Pass@1; (2) a hybrid reward for GRPO that uses PDF vectorized representations (PyMuPDF) to extract textual and geometric primitives, combined with DreamSim+MSE image fidelity and a compile-pass gate; (3) a 7B model achieving 97.60% Pass@1 compile rate, substantially above prior specialized models (DetikZify-V2-8B at 78.60%).

## Strengths

- **Dramatic compile-rate improvement is practically meaningful.** The jump from DetikZify-V2-8B (78.60% Pass@1) to DaVinci-7B (97.60%) is the paper's strongest result. Table 4 confirms this gain is attributable to the paper's specific data choices (reordering +9.04%, comments +5.72%) rather than just using a stronger base model.

- **Hybrid reward design using PDF vectorization is well-motivated and validated.** The insight that PDF vectorized representations provide exact geometric and text metadata — eliminating OCR errors for *extraction* — is architecturally sound. Table 5 validates that each reward component contributes, with $R_{\text{text}} + R_{\text{geom}}$ together producing the best results across all metrics.

- **Drawing order normalization and comment injection are novel data insights.** Table 4 cleanly demonstrates that code reordering yields +9.04% Pass@1 and comments add another +5.72%. This is a non-obvious finding — prior work treated TiKZ as order-independent (technically correct for rendering), but the paper correctly identifies that order-independence harms autoregressive language model training.

- **Strong evaluation methodology.** Human evaluation uses Best-Worst Scaling with split-half reliability (>0.72 in both groups), temporal separation between training (pre-December 2023) and test (post-January 2024) data, and compares against both general-purpose MLLMs and specialized TiKZ models. Ablation studies isolate each contribution separately.

## Weaknesses

### Major

- **The claim of "surpassing leading proprietary models" is selective and could mislead readers.** The abstract states DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4." This is literally true for those two models on several metrics, but the human evaluation (Table 3) tells a more complex story: Gemini-2.5-Pro-Thinking scores +0.50 (dominating), while DaVinci-7B scores −0.01 — essentially indistinguishable from chance. The automatic metrics (Table 1) reinforce this: Gemini leads in DreamSim (88.20 vs. 84.83), SigLIP, SSIM, and LPIPS. DaVinci's decisive advantage is compile rate (97.60% vs. 69.93%), where Gemini is uncharacteristically weak. The paper acknowledges Gemini's superiority in the Section 4.4 text, but the abstract and conclusion use phrasing that implies broad superiority. This framing should be tempered.

### Minor

- **The LLM-based code reordering pipeline is underspecified for reproducibility.** A core data contribution depends on using Qwen3-Coder-480B-A35B-Instruct to reorder TiKZ code "following a semantics-guided, logically constructive drawing protocol" (Section 3.2). The paper does not disclose the prompt used, what constitutes the "protocol" (rules vs. prompt template), or any quantitative rendering-agreement metric between original and reordered outputs (beyond passing post-verification). Since 29,859/30,000 SFT samples depend on this step, the quality control details matter.

- **The "error-free" claim conflates extraction with matching.** The paper states the approach extracts textual and geometric primitives in an "error-free manner" (abstract, Section 3.3). This is accurate for the *extraction* step (PyMuPDF reads exact PDF metadata). However, the matching pipeline uses Levenshtein distance with adaptive thresholds (Algorithm 1, Section 3.3) and a Hungarian algorithm with weighted cost functions (Algorithm 2), both of which introduce approximation. The "exact-then-vaguely" text matching procedure can produce false matches or misses. The claim should be qualified to distinguish error-free *extraction* from approximate *matching*.

- **Reward component scale imbalance is not discussed.** Equation (2) states no special weights are used, but DreamSim outputs unbounded similarity scores while the MSE term is clipped to [-1, 1]. If DreamSim varies over a wider range than the clipped MSE term, the image fidelity reward could be dominated by DreamSim regardless of intent. The paper does not report empirical ranges of each reward component during RL training.

### Trivial

None.

## Nice-to-Haves

- Compare text reward computed via PDF vectorization against an OCR-based variant to quantify the practical benefit of the "error-free" extraction approach.
- Report confidence intervals for Pass@1 and other automatic metrics on the 542-sample test set.
- Analyze potential reward hacking (e.g., generating invisible elements that satisfy geometric matching at the expense of visual quality).
- The "thinking analysis" paragraph in Section 4.3 draws observations from model variants that differ in both thinking mode and prompting; these confounds make the comparison hard to interpret.

## Removed Points

These points were removed from the input review with justification:

- **Comparison against untuned base models inflates apparent gap:** The inclusion of raw Qwen2.5-VL in the comparison table is standard practice — every fine-tuning paper shows the base model to demonstrate the effect of training. The paper also compares against genuinely specialized models (DetikZify-V2-8B, DiagramAgent-7B) where DaVinci still outperforms. No misleading inflation.

- **"Statistical significance not reported":** Soft methodology preference; confidence intervals are not standard for this type of benchmark evaluation in the MLLM community.

- **"Thinking analysis is a digression":** Subjective; the paragraph is one section of a short subsection and makes a relevant observation.

- **Missing ablation of OCR vs. PDF vectorization:** A nice-to-have, not a core weakness; included as a Nice-to-Have.

- **Reward hacking analysis:** Speculative concern; included as a Nice-to-Have.

- **Pure formatting/style nitpicks and requests for details that may reside in the stripped appendix.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reword the abstract and conclusion to accurately scope the proprietary model comparison. For example: "achieves competitive results with proprietary models on visual quality while substantially exceeding them in compile reliability (97.60% Pass@1)" rather than the current blanket claim.
- Disclose the prompt used for LLM-based code reordering, report the rendering-agreement rate between original and reordered outputs, and define what the "logically constructive drawing protocol" entails.
- Replace "error-free" with "extraction-error-free" to precisely scope the claim to the PyMuPDF extraction step, distinguishing it from the approximate matching procedures.
- Report the empirical ranges of $R_{\text{text}}$, $R_{\text{geom}}$, $R_{\text{img}}$, and $R_{\text{pass}}$ during RL training to verify that no single component dominates the hybrid reward by virtue of scale.

## Score and Decision

**Calibration anchors used (all rounds):**

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| AutomaTikZ | v3K5TVP8kZ | 6.50 | R1 | Most comparable: SFT on TiKZ with dataset release. DaVinci has more sophisticated training (RL) and stronger methodology |
| Sketch2Diagram | KvaDHPhhir | 6.25 | R1, R2 | Similar domain: image-to-TiKZ with data augmentation. DaVinci has stronger results and more thorough ablations |
| ScImage | ugyqNEOjoU | 5.33 | R1 | Benchmark paper in related domain. DaVinci has stronger technical contribution |
| Delving SVG | pwlm6Po61I | 5.67 | R2 | Related: SVG-based code gen. DaVinci is more rigorous and narrowly focused |
| Text2Reward | tUM39YTRxH | 7.00 | R2 | Different but methodologically related (RL reward design). DaVinci slightly below in overall significance |

**Round-1 bracket:** [5.5, 7.0]

**Final calibration:** DaVinci sits at the high end of the band, comparable to or slightly above AutomaTikZ (6.50) in experimental rigor and result quality, but with a notable framing issue that reduces confidence in its claims. The core technical contributions are sound and well-validated; the weaknesses are fixable framing and specification issues rather than fundamental flaws.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>