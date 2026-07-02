## Summary

This paper introduces DaVinci, a multimodal LLM for scientific diagram parsing (raster image → TikZ code) using a two-stage pipeline: (1) supervised fine-tuning on TikZ30K, a curated dataset with reordered drawing sequences and injected comment annotations, followed by (2) GRPO-based reinforcement learning with a hybrid reward function that leverages vectorized PDF representations for "extraction-error-free" text and geometry matching. The main contributions are the identification of drawing order and comment annotations as impactful data features, and the use of vectorized (PDF) representations to construct precise spatio-textual and geometric rewards that avoid OCR errors. DaVinci-7B achieves 97.6% Pass@1 compile rate on the DATiKZ_v3 benchmark, substantially ahead of all baselines, and outperforms GPT-5 and Claude-Sonnet-4 on most metrics.

## Strengths

- **Use of vectorized representations for reward computation (Section 3.3).** The insight that PDF-format vectorization from TikZ compilation provides exact text and geometry metadata—sidestepping OCR errors—is clever and well-motivated. The Spatio-Textual reward (Eq. 3) and Geometric reward (Eq. 4) that operate on vector primitives rather than raster pixels are a genuine methodological improvement over prior pixel-level or OCR-based rewards. The ablation in Table 5 cleanly demonstrates incremental gains from each reward component.

- **Code reordering and comment injection ablation (Section 3.2, Table 4).** The observation that TikZ code ordering is largely irrelevant to rendering but matters for autoregressive training is a legitimate and underexplored issue. The ablation showing +9.04% Pass@1 from reordering and another +5.72% from comments is clean evidence that these augmentations matter. The isolation in the ablation study is well done, and the passing rate for post-verification (29,859/30,000) is quantified.

- **Near-perfect compile rate with strong evidence.** DaVinci-7B achieves 97.60% Pass@1, far above all baselines including proprietary models (next best is Claude-Sonnet-4-Thinking at 86.90%). Since non-compiling code is worthless in practice, this is a practically meaningful improvement, and the ablation study convincingly attributes the gain to the data strategy rather than just the base model.

## Weaknesses

### Fatal
None.

### Major

- **Baseline evaluation protocol is underspecified (Sections 4.1–4.2).** The paper does not state what prompt template was used for each baseline model, nor the decoding parameters (temperature, top-p, max tokens) for any baseline including GPT-5, Claude, Gemini, Qwen, GLM, DetikZify-V2, or DiagramAgent. Whether baselines received the same instruction, the same number of attempts, or the same context is not specified. For a benchmark paper that makes competitive claims against proprietary models, these details are essential for reproducibility and fairness assessment. DaVinci's own training settings are referenced to Appendix E.3, but zero evaluation protocol details for baselines appear anywhere in the visible paper.

### Minor

- **Headline claims are selective in their framing.** The abstract and conclusion repeatedly state that DaVinci "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4." This claim is factually true for those two specific models: DaVinci-7B beats GPT-5-Default on 6/8 automatic metrics and Claude-Sonnet-4 on 7/8 metrics, and achieves a higher human-preference score than both. However, Gemini-2.5-Pro-Thinking—also evaluated in the same tables—outperforms DaVinci on 5/8 automatic metrics and achieves a human score of 0.50 vs. DaVinci's -0.01. The paper acknowledges Gemini's strength in Section 4.4 ("Gemini-2.5-Pro-Thinking significantly outperforms all other models") but the headline framing does not reflect this. A more precise claim (e.g., "surpasses GPT-5 and Claude-Sonnet-4 while being competitive with Gemini-2.5-Pro on compile rate and MSE") would better match the evidence.

- **Potential test set overlap between training data and DATiKZ_v3 is not fully addressed.** The paper ensures "strict temporal separation from the DATiKZ_og test set" (training data restricted to sources published by December 2023; DATiKZ_og test set is from January 2024 onward — Section 3.2). However, evaluation is performed on **DATiKZ_v3** (Section 4.2), not DATiKZ_og. The paper does not clarify whether the DATiKZ_v3 test set shares the same temporal boundary. If DATiKZ_v3 contains samples from pre-2024, those could overlap with the independently collected training data drawn from the same sources (arXiv, TeX.SE, GitHub). The contamination risk is likely low, but the paper should explicitly confirm temporal separation for the actual evaluation set.

- **Inclusion of TED as a metric creates a tension with the paper's own argument.** Section 4.3 ("High Code Similarity Is Not Necessary") argues that visually equivalent outputs can come from syntactically diverse TikZ code, making strict code-level similarity undesirable. Yet TED (Text Edit Distance on code) is included as a main metric in Table 1. If code similarity is not the goal, measuring it and ranking models by it is inconsistent. The paper should either justify TED's inclusion or relegate it to an auxiliary role.

- **No statistical significance or confidence intervals for automatic metrics (Table 1).** The main automatic evaluation table reports single point estimates without any measure of variability. For a comparison involving multiple models and multiple metrics, confidence intervals or significance tests would substantially strengthen the reliability assessment. The human evaluation uses BWS with split-half reliability, but the automatic evaluation has no equivalent.

### Trivial

- **"Extraction-error-free" language is slightly overstated.** The paper claims that text and geometry extraction from the vectorized PDF representation is "error-free" (lines 34, 40, 122). Within the stated scope—extraction from TikZ-generated PDFs using PyMuPDF—this is substantially more reliable than OCR and the claim is defensible. However, absolute language like "error-free" is unnecessary and invites nitpicking about edge cases (encoding issues, ligature handling, embedded paths). Softening to "extraction without the errors introduced by OCR" or similar would be more precise.

## Nice-to-Haves

- Provide the exact prompt templates and decoding settings for all baselines. This is the single highest-impact addition for reproducibility.
- Add confidence intervals, error bars, or significance tests to the automatic evaluation in Table 1.
- Confirm the temporal boundary of the DATiKZ_v3 test set explicitly (or demonstrate non-overlap via other means).
- Soften the "error-free" language to avoid absolute claims that are unnecessary for the contribution.

## Removed Points

The following points from the input review were removed after verification against the paper:

- "Code reordering success rate not quantified" — **Removed.** The paper states "29,859 passed post-verification" out of 30,000 (≈99.5%), which is quantified.
- "Human evaluation has low statistical power / low std suggests poor discrimination" — **Removed.** Low std with differentiated scores (DaVinci -0.01 vs. GPT -0.13 vs. Claude -0.35) indicates good discrimination, and the BWS design with 100 items × 6 raters is standard for this line of work (following prior DATiKZ/Detikzify papers). The split-half reliability values of 0.72–0.79 are reasonable.
- "DaVinci's negative human eval score should be acknowledged" — **Removed.** The paper transparently reports the -0.01 score alongside p_best and p_worst and compares it fairly against other models.
- "Missing limitation about reward requiring ground-truth data" — **Removed.** All supervised RL requires ground-truth data; this is inherent to the method, not a unique limitation. The paper does not claim the approach works without ground truth.
- Several section-by-section notes that were speculative (e.g., "assuming Y is the case…") or requested scope extensions (e.g., extending the method to scenarios outside its stated scope).

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an unexpected cross-cutting observation that changes how the contribution should be interpreted; they primarily sharpen the framing of existing claims.

## Suggestions

1. **Specify the baseline evaluation protocol.** For every baseline model, state the exact prompt (include it verbatim), temperature, top-p, max tokens, and any post-processing. This is a requirement for a benchmark paper making competitive claims.
2. **Re-calibrate the headline claims.** Replace "surpasses leading proprietary models like GPT-5 and Claude-Sonnet-4" with a more precise statement that acknowledges Gemini's standing while still highlighting the strong showing against GPT-5 and Claude. Example: "DaVinci-7B achieves state-of-the-art compile rates (97.6%) and competitive image quality, outperforming GPT-5 and Claude-Sonnet-4 on most metrics while being competitive with Gemini-2.5-Pro."
3. **Address the DATiKZ_v3 temporal boundary** explicitly in the experimental setup section.
4. **Either justify TED's inclusion in the main table** or move it to supplementary, given the paper's own argument that code similarity is not the goal.
5. **Add a brief limitation paragraph** acknowledging that the vectorization-based rewards require ground-truth TikZ compilation (available during training but not at inference time), and that extending to purely raster scenarios remains future work.

## Score and Decision

**Score:** 6  
**Decision:** Accept

The paper's core contributions—the use of vectorized representations for reward computation in diagram parsing and the identification of drawing order/comments as impactful data features—are sound, novel, and well-supported by clean ablation studies. The 97.6% compile rate is a practically meaningful improvement. The primary weaknesses (underspecified baseline evaluation protocol and selective framing) are substantial but fixable in a rebuttal/revision. The methodological core is not threatened, and the paper would bring clear value to the ICLR community. A higher score would require the evaluation protocol details to be provided; a lower score would be warranted if those details revealed unfair comparisons.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>