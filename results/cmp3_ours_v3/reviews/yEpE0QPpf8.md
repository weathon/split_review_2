## Summary

This paper introduces grounding-IQA, a new IQA task paradigm that integrates multimodal referring and grounding with image quality assessment. It defines two subtasks: GIQA-DES (descriptions with bounding boxes for quality-relevant regions) and GIQA-VQA (quality QA with spatial localization). The authors construct GIQA-160K (167K instruction-tuning samples from 43K images) via an automated four-stage annotation pipeline, and GIQA-Bench (100 images, 250 test samples) for evaluation. Fine-tuning four MLLMs (LLaVA-v1.5, LLaVA-v1.6, mPLUG-Owl2) on GIQA-160K consistently improves their performance across description quality, VQA accuracy, and grounding precision metrics.

## Strengths

1. **Well-motivated problem.** The paper identifies a genuine limitation in prior MLLM-based IQA methods: they lack spatial precision in quality descriptions (Fig. 2). The grounding-IQA paradigm is a sensible extension that addresses a real gap.

2. **Carefully engineered annotation pipeline.** The four-stage pipeline — object tag extraction with quality triples (Stage 1), descriptive-phrase-based detection using $\mathcal{T}_r$ rather than object names (Stage 2), IQA-Filter + Box-Merge refinement (Stage 3), and coordinate discretization (Stage 4) — shows systematic attention to error propagation. Using the descriptive phrase for detection (Fig. 4) is a practical design choice that addresses multi-instance ambiguity.

3. **Meaningful dataset scale and diversity.** GIQA-160K provides 167K instruction-tuning samples from 43K images spanning in-the-wild, AI-generated, and artificially degraded domains. The balanced distribution across question types (25K Yes, 25K No, 50K What/Why/How) supports diverse training.

4. **Consistent improvement across architectures.** Table 4 shows that fine-tuning on GIQA-160K improves four different base models (LLaVA-v1.5-7B, LLaVA-v1.5-13B, LLaVA-v1.6-7B, mPLUG-Owl2-7B) across all four metrics. This consistency strengthens the case for the dataset's broad utility.

## Weaknesses

### Fatal
None.

### Major

1. **Missing control experiment to isolate the contribution of grounding annotations.** The paper shows that fine-tuning on GIQA-160K (which includes bounding boxes) improves GIQA-Bench performance. However, it does not compare against fine-tuning on the *source* datasets (Q-Pathway, DQ-495K) with the grounding information removed — i.e., using the original text-only descriptions without bounding boxes. Without this control, it is unclear whether the improvement comes from the grounding annotations specifically (the paper's central novelty) or simply from additional in-domain training text. Table 2a compares Ref-Box vs. Raw-Box, but neither is compared against text-only fine-tuning. This is the most consequential gap in the empirical case.

### Minor

2. **Figure 1 / Table 5 model inconsistency.** The radar chart (Fig. 1) compares methods called "HPLUS-Duo-7B" and "Shika-7B" — models that do not appear in the main experimental setup (Table 5) or in any method description in the available paper. Table 5 uses LLaVA-v1.5-7B/13B, LLaVA-v1.6-7B, and mPLUG-Owl2-7B as base models, and lists "Shikra-7B" (different spelling from Fig. 1's "Shika-7B"). Since Fig. 1 is referenced in the abstract and introduction as a key result, this inconsistency undermines the clarity of the paper's empirical claims.

3. **Overstated "outperforms" claim.** The paper states "our method outperforms existing MLLMs" (Sec. 4.3). However, in Table 5, Ferret-7B achieves a higher GIQA-DES Tag-Recall (0.6778) than any Grounding-IQA variant (best: 0.5981), and Ferret's DES mIoU (0.6458) is close to the best Grounding-IQA mIoU (0.6583). The blanket "outperforms" claim is only justified on a subset of metrics and should be calibrated to acknowledge where specialized grounding models remain competitive.

4. **Small benchmark size without confidence measures.** GIQA-Bench contains only 100 images and 250 test samples (100 DES, 150 VQA). With this small size, a difference of a few correct answers can swing metrics by several points (e.g., Acc(Total) ranges from 0.4433 to 0.7417 across methods). No confidence intervals or statistical significance tests are reported, making it hard to assess whether observed differences are reliable.

5. **Q-Ground omitted from comparisons.** Q-Ground (Chen et al., 2024b) is described in Sec. 2.2 as achieving "degradation region grounding in IQA" and is arguably the closest existing work to grounding-IQA. Yet it does not appear in Table 5 or any experimental comparison. The omission should be justified.

### Trivial

6. **Model name typo in Figure 1.** The figure caption spells "Shika-7B" while the text and Table 5 consistently use "Shikra-7B" (matching the cited work Chen et al., 2023).

## Nice-to-Haves

- Human validation rate for the automated annotation pipeline (e.g., random 500-sample review) would strengthen confidence in annotation quality.
- Bootstrapped confidence intervals for GIQA-Bench metrics would clarify the reliability of observed differences.
- Embedding-based metrics (e.g., BERTScore, CLIPScore) as a complement to BLEU@4 for description quality would better capture semantic similarity.

## Removed Points

These points were raised in the input reviews but removed per filtering rules:
- **Criticism about "Code: ." with no URL**: Removed — the truncated URL is a parser artifact; the original submission likely contained a URL.
- **Criticism about missing license / ethical considerations**: Removed — license information may be present in the stripped supplementary material.
- **Criticism about coordinate discretization limiting spatial precision**: Technically correct but the paper explicitly acknowledges this trade-off ("Though the discretization reduces coordinate precision..." — line 149). This is a transparent design choice, not a flaw.
- **Criticism about Q-Instruct filter circularity**: The paper provides empirical evidence that the refinement works (Ref-Box > Raw-Box in Table 2a), partially addressing this concern.
- **Strength about "identified an important problem"**: Removed as generic — the point is subsumed by the more specific Strength #1.
- **Speculative-fatal framing of the Figure 1 inconsistency** ("undercuts the paper's core empirical claims"): Downgraded from fatal to minor because Table 5 is the primary results table and is internally consistent. The figure inconsistency is a presentation issue, not evidence that the core results are invalid.

## Novel Insights

None beyond the paper's own contributions. The reviews surface standard concerns for a dataset/benchmark paper: whether the claimed novelty (grounding annotations) is causally responsible for improvements, whether comparisons are comprehensive, and whether the benchmark is adequately sized for reliable conclusions.

## Suggestions

1. **Add the missing control experiment:** Fine-tune the same base models on the original text-only descriptions from Q-Pathway and DQ-495K (without any grounding annotations) and compare against GIQA-160K fine-tuning on GIQA-Bench. This directly tests whether grounding provides measurable benefit beyond additional in-domain text.
2. **Resolve the Figure 1 / Table 5 model discrepancy:** Either replace the radar chart with one consistent with Table 5, or explain what HPLUS-Duo-7B is and why it differs from the main experiments.
3. **Calibrate the "outperforms" claim** to be precise about which methods and which metrics are being compared.
4. **Include Q-Ground in comparisons** or explain why it cannot be evaluated.
5. **Provide bootstrapped confidence intervals** for the main GIQA-Bench results.

## Score and Decision

**Calibration anchors** (all from DeepReview-13k):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Q-Adapt (KUf2iyin77) | 5.25 | R1 | IQA + LMM adaptation paper, rejected for methodology concerns; this paper has a clearer task-level contribution |
| Dog-IQA (U3EzVIsyiP) | 4.75 | R1 | Zero-shot IQA paper, rejected for novelty concerns; this paper's new paradigm is more novel |
| Q-Bench-Video (VaUy5GZO3f) | 4.80 | R1 | Video quality benchmark, rejected for methodological issues; this paper includes a training dataset in addition to a benchmark |
| Ferret (2msbbX3ydD) | 6.67 | R1 | Seminal grounding MLLM paper, accepted; this paper is far less comprehensive in scope and contribution |
| MMAD (JDiER86r8v) | 6.50 | R1 | Comprehensive anomaly detection benchmark, accepted; this paper's benchmark is significantly smaller |
| MME-RealWorld (k5VHHgsRbi) | 6.80 | R1 | Large-scale MLLM benchmark, accepted; this paper is a narrower contribution |
| MMR (mzL19kKE3r) | 6.00 | R1 | Reasoning segmentation benchmark, accepted; this paper has a smaller benchmark but introduces a new task paradigm |

**Round 1 bracket:** 5.0–6.0 (above the rejected IQA papers at 4.75–5.25, below the accepted dataset/grounding papers at 6.0–6.8).

**Final score rationale:** The paper has a clear and well-motivated contribution (new task paradigm + dataset), but the central claim about the value of grounding annotations is not causally isolated by the experiments. The missing control experiment is a genuine evidentiary gap, and the Figure 1 inconsistency and overstated "outperforms" narrative further weaken the presentation. The contribution is real but the empirical support is incomplete.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>