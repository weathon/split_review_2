## Summary

This paper introduces DaVinci, a two-stage SFT+RL framework for parsing scientific diagram images into TikZ code. The key contributions are: (1) identifying and remediating drawing-order noise and comment sparsity in training data (TiKZ-30K dataset), (2) a hybrid reward function for RL that extracts text and geometric primitives from PDF vector representations rather than using OCR, and (3) showing that GRPO-based post-training substantially improves compile rate and visual fidelity. The approach is evaluated on the DATiKZ_v3 benchmark against open-source and proprietary models.

## Strengths

- **Novel vectorized-representation-based reward design.** The paper extracts text content, bounding boxes, and geometric primitives directly from the PDF vector representation (via PyMuPDF) rather than relying on OCR over raster images. This is a concrete improvement over prior work (Section 3.3), as OCR on diagrams is error-prone for mathematical symbols and overlapping elements — a failure mode the paper documents (Appendix E.4). This avoids a real bottleneck faced by prior methods.

- **Drawing-order-noise remediation is well-motivated and effective.** Section 3.2 identifies that TikZ code ordering is largely independent of rendering order, creating an arbitrary mapping between visual content and token sequences. The ablation in Table 4 confirms the impact: code reordering improves Pass@1 by +9.04% (69.74 → 78.78), and adding comment annotations yields a further +5.72% gain (78.78 → 84.50). These are clean, interpretable improvements.

- **Ablation study cleanly isolates reward components.** Table 5 shows each addition (R_text, R_geom) produces measurable improvements on the targeted metrics. The textual reward improves textual alignment (+4.35 over base), and adding the geometric reward further improves geometric alignment (+2.66). This supports the paper's claims about the reward design.

## Weaknesses

### Fatal
None.

### Major

- **Only one test set (DATiKZ_v3, 542 samples), raising generalization concerns.** The test set is drawn from the same data distribution (arXiv, TeX.SE, GitHub) as the training data. The paper claims temporal separation (training ≤ Dec 2023, test ≥ Jan 2024), but this does not guarantee distributional independence — identical or near-identical diagram patterns could appear across dates, and no deduplication analysis is reported. For a paper making comparative claims against proprietary models, a single test set from the same distribution is not sufficient to establish generalization. A cross-dataset evaluation would substantially strengthen the claims.

### Minor

- **Selective framing in the abstract and conclusion.** DaVinci is described as "surpassing leading proprietary models like GPT-5 and Claude-Sonnet-4" (abstract, introduction, conclusion) without mentioning Gemini-2.5-Pro-Thinking, which outperforms DaVinci-7B on 5 of 8 automatic metrics (DreamSim, SigLIP, SSIM, TED, LPIPS) and decisively wins the human evaluation (score 0.50 vs DaVinci's -0.01). The paper *does* acknowledge this in Sections 4.3 and 4.4, making the omission in the narrative framing a selective-presentation issue. The specific claims about GPT-5 and Claude-Sonnet-4 are supported by the data, but the overall narrative should be more balanced.

- **"Extraction-error-free" claim is overstated.** The paper repeatedly describes the PDF-vector-based extraction as "error-free" (lines 34, 40, 52, 106, 122). While PDF text extraction is much more reliable than OCR, it has known failure modes (rotated text, ligatures, font-subsetting issues, symbols encoded as paths). The paper's own use of a Levenshtein-distance fallback matching stage (Section 3.3) implicitly acknowledges limitations. The framing should be softened to something like "extraction-error-free relative to OCR," with the limitations acknowledged.

- **No variance/confidence estimates for automatic metrics (Table 1).** All entries are point estimates, and with only 542 test samples, the reader cannot assess whether observed differences between models are reliable. Standard deviations or confidence intervals would strengthen the comparisons.

- **"No special weights" claim is imprecise.** Line 118 states "we do not set special weights for each reward component," but the components operate at different numerical scales: R_text and R_geom are bounded [0,1] by normalization, while R_img combines unbounded DreamSim and clipped MSE (roughly [-1, 2]). This means components are implicitly scaled differently. While this is common practice, the paper should acknowledge it.

### Trivial
None.

## Nice-to-Haves

- A semantic failure analysis beyond compile rate (e.g., a taxonomy of visual-semantic errors such as misplaced text, wrong colors, missing elements) would help characterize remaining weaknesses, especially given the 97.60% compile rate but near-zero human preference score against Gemini.
- Tracking individual reward components during GRPO training (how R_text and R_geom evolve over the 500 steps) would strengthen the claim that the multi-component reward works as intended.
- A cross-dataset evaluation on diagrams from a different source would address the single-test-set concern.

## Removed Points

These items from the input review were removed per filtering rules:

- **Data release status concerns**: The paper states code, datasets, and models will be released with license compliance details. Removed per rule: "REMOVE any criticism that questions the existence, release status, or availability of any cited entity."
- **Criticism about dependency on Qwen3-Coder-480B-A35B for reordering being "a source of errors or stylistic biases"**: Speculative — no concrete evidence from the paper supports this.
- **"No failure analysis beyond compile rate" / "No analysis of reward during RL training"**: These request additional experiments, not identified flaws. Moved to Nice-to-Haves.
- **Criticism about 100-item/6-annotator human evaluation**: This follows standard practice from prior work; SHR values of 0.72/0.79 indicate acceptable agreement.
- **58k sample size not justified**: The paper states "stratified sampling by token length over the 225,648 filtered samples, yielding a balanced subset" — a reasonable justification.
- **Formatting, grammar, presentation nitpicks**: Removed per rules as parser artifacts.
- **The critic's framing of the "surpassing" claim as a "Critical Issue" / "fatal"**: Demoted to Minor after verification — the claim about GPT-5 and Claude-Sonnet-4 specifically IS supported by the data (DaVinci beats GPT-5 on 6/8 metrics and Claude on 7/8). The issue is selective omission of Gemini from the framing.
- **Generic strengths** (e.g., "addressed an important problem"): Removed as not concrete evidence of paper quality.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Rewrite the abstract and conclusion to acknowledge Gemini's stronger performance on perceptual metrics, situating DaVinci as competitive on compile rate and selected metrics while noting where it lags.
2. Add a second evaluation set — even a smaller manually curated set from a different source — to demonstrate generalization beyond DATiKZ_v3's distribution.
3. Add bootstrap confidence intervals or standard deviations to Table 1.
4. Soften the "extraction-error-free" claim to reflect the actual limitations of PDF text extraction.

## Score and Decision

The paper presents genuinely novel technical contributions — particularly the vectorized-representation-based reward and the data-quality insights about drawing order — supported by well-structured ablations. The main weaknesses are a single-test-set evaluation and selective framing in the abstract, neither of which invalidate the core contributions. The issues are addressable.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>