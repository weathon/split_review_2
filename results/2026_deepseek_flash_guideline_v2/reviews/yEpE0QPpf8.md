## Summary
This paper introduces grounding-IQA, a new IQA paradigm that integrates spatial grounding (bounding boxes) into multimodal LLM-based image quality assessment. It proposes two subtasks — GIQA-DES (grounded description) and GIQA-VQA (grounded visual question answering) — constructs a 168K-sample dataset (GIQA-160K) via an automated annotation pipeline, and evaluates on a 250-sample human-annotated benchmark (GIQA-Bench). Experiments show that fine-tuning four different MLLMs on GIQA-160K equips them with combined grounding-and-quality capabilities.

## Strengths
1. **IQA-Filter addresses a specific failure mode of generic detectors.** The paper identifies that standard object detectors cannot distinguish same-class objects with different quality (e.g., one blurry hand vs. one clear hand). The IQA-Filter (Alg. 1, Stage-3) uses Q-Instruct to verify each detected box with a quality-specific question. Tab. 2a shows this improves mIoU from 0.5624→0.5851 and Tag-Recall from 0.5045→0.5497, with concrete evidence of the pipeline's effectiveness.

2. **Grid-based coordinate discretization reduces token cost while preserving accuracy.** The discretization (Eq. 1–2, n=m=20) cuts box representation from 21 tokens to at most 9 tokens. Tab. 2b shows Disc-Coord achieves nearly identical Tag-Recall (0.5497 vs. 0.5490) and improves BLEU@4 (23.67 vs. 22.03) relative to normalized continuous coordinates — a practical engineering contribution.

3. **Multi-task joint training produces clear synergy.** Tab. 3 shows that joint training on GIQA-DES + GIQA-VQA yields GIQA-VQA Tag-Recall of 0.7372 vs. 0.4872 for Only-VQA, and LLM-Score of 63.00 vs. 38.50. This demonstrates that the two subtasks reinforce each other rather than competing.

4. **Consistent improvement across four distinct MLLM architectures.** Tab. 4 shows that fine-tuning on GIQA-160K lifts all four base models (LLaVA-v1.5-7B/13B, LLaVA-v1.6-7B, mPLUG-Owl2-7B) substantially — e.g., Acc (Total) from 0.4733→0.6850, 0.4433→0.6950, 0.5067→0.7250, 0.5633→0.7417. This cross-architecture generalization supports the claim that the dataset is versatile.

5. **The benchmark evaluates across four model groups with six metrics.** Tab. 5 compares 16 model variants across General, Grounding, IQA, and Ours categories, with metrics covering description quality, VQA accuracy, and grounding precision — more comprehensive than prior IQA benchmarks.

## Weaknesses

### Fatal
None.

### Major
1. **Evaluation-model overlap.** The LLM-Score for GIQA-DES (line 232) and Acc (W) for GIQA-VQA (line 234) both use Llama3 as the evaluator. Llama3 is also used in Stage-1 (object tag extraction, line 131) and GIQA-VQA generation (line 168). While the LLM is asked to judge relevance to human-annotated ground truth (not self-similarity), this overlap creates a risk that models fine-tuned on Llama3-generated data receive inflated scores. A human evaluation (mentioned as supplementary) or an independent LLM evaluator would substantially strengthen the claims.

2. **No uncertainty quantification on a small benchmark.** GIQA-Bench consists of 100 images, 100 DES samples, and 150 VQA samples (line 226). Results are reported as point estimates to four decimal places without confidence intervals, standard deviations, or significance tests. Given the small sample size (especially for VQA subgroups: 35 "Yes" and 55 "No" — line 226), small differences between methods (e.g., mIoU 0.6302 vs. 0.6458) may not be meaningful. Single-run reporting with no variance is a material gap.

3. **Omission of the most directly comparable prior work.** Q-Ground (Chen et al., 2024b) is cited as "achiev[ing] degradation region grounding but lacking referring capabilities" (line 60) — making it the closest existing method — yet it is not included in Tab. 5 comparisons. The paper should include Q-Ground under fair conditions or explain why comparison is infeasible.

4. **The "more fine-grained quality assessment" claim is not directly tested.** The paper shows that models produce bounding boxes alongside quality descriptions after fine-tuning on GIQA-160K, but never tests whether quality assessment itself becomes more accurate *because of* grounding. The LLM-Score and BLEU@4 are computed with coordinates stripped (line 232), measuring description quality without grounding signal. Tab. 3 shows joint training helps, but the paper doesn't directly compare IQA accuracy with vs. without grounding (e.g., fine-tuning on GIQA-160K vs. the same data without bounding boxes). The contribution is better framed as "models can additionally localize quality-relevant regions" rather than "grounding makes quality assessment more fine-grained."

5. **Benchmark independence concern.** GIQA-Bench descriptions are "from Q-Pathway and adjusted, with key objects and bounding boxes manually determined" (line 228). Q-Pathway is also the source of GIQA-160K training data. If the benchmark descriptions share stylistic patterns with the training data, the benchmark may not detect overfitting. The paper should clarify what "adjusted" means and whether annotators had access to GIQA-160K.

### Minor
1. **Ferret-7B outperforms Grounding-IQA on some grounding metrics.** Tab. 5 shows Ferret-7B achieves Tag-Recall of 0.6778 on GIQA-DES, higher than any Grounding-IQA variant (best: 0.5981). On mIoU, Ferret (0.6458) beats three of four Grounding-IQA variants. The claim that "our method outperforms existing MLLMs" (line 341) overstates without hedging; improvement is on combined quality+grounding metrics, not all individual metrics.

2. **No human evaluation of dataset quality.** The automated pipeline is described in detail, but there is no analysis of what fraction of automatically generated bounding boxes are correct, or how often the Q-Instruct-based IQA-Filter makes correct vs. incorrect quality judgments.

3. **Tag-Recall's object name similarity metric is not defined.** Line 236 requires "IoU > 0.5 and object name similarity > 0.5" but does not specify the similarity metric (exact match? embedding cosine?), hindering reproducibility.

### Trivial
1. The term "IQG" appears in lines 324, 341, 343, and 349 instead of "IQA" — a residual naming inconsistency.
2. Figure 1 caption text appears to be OCR-extracted from the figure image, referencing models (HPLUS-Duo-7B, Grounded-HPLUS-Duo-7B) not used in experiments; this should be cleaned up.

## Nice-to-Haves
- A direct comparison of IQA accuracy with vs. without grounding capability (same data with/without bounding boxes) would directly test the core claim.
- Multi-run evaluation with confidence intervals on GIQA-Bench.
- Including Q-Ground (Chen et al., 2024b) in Tab. 5 comparisons.

## Removed Points
The following points from the Harsh Critic were removed:
- **Criticism about coordinate discretization precision (5% grid cells):** The paper already addresses this by showing Disc-Coord performs comparably to Norm-Coord (Tab. 2b), and the critic acknowledges this mitigation.
- **Criticism about Stage-3 IQA-Filter depending on Q-Instruct accuracy:** This is the intended design; the ablation (Tab. 2a) demonstrates effectiveness, and the critic provides no evidence of actual errors.
- **Criticism about T_o=95% overlap threshold:** The reviewer notes this is for near-duplicate detection (line 137); the overall pipeline is validated by ablation.
- **Criticism about "N/A" formatting in Tab. 4:** Not a substantive issue.
- **Criticism about "HPLUS-Duo-7B" and "grounding-GPT" terms:** These appear to be parser-extracted OCR text from figures, not part of the paper's authored text.
- **Generalized "areas of concern" framing** without concrete anchors (e.g., "could the metric be measuring a proxy?") — removed as speculation.

## Novel Insights
None beyond the paper's own contributions. The reviews do not surface any observation that the paper itself does not already make.

## Suggestions
1. Replace or supplement Llama3-based evaluation (LLM-Score, Acc W) with evaluation using a different, independent LLM (e.g., GPT-4) or a human evaluation on a subset of GIQA-Bench.
2. Report confidence intervals or per-sample variance on all GIQA-Bench metrics; run multiple evaluation seeds.
3. Include Q-Ground as a baseline or provide a clear justification for its absence.
4. Tone down the "more fine-grained quality assessment" framing to match what is actually measured: models gain grounding capability alongside quality assessment, but it is not shown that grounding improves assessment accuracy. Revise "our method outperforms existing MLLMs" to acknowledge where grounding-specialized models (Ferret-7B) achieve higher individual metrics.
5. Clarify the object name similarity metric used in Tag-Recall.
6. Clarify the relationship between GIQA-Bench and Q-Pathway annotations, and whether annotators had access to GIQA-160K during benchmark construction.

## Score and Decision
After reviewing the paper and filtering the reviewer inputs, this paper presents a novel task formulation (grounding-IQA), a substantial dataset (GIQA-160K) with a well-designed automated annotation pipeline, and a multi-perspective benchmark. The experiments convincingly show that fine-tuning on GIQA-160K equips four different MLLMs with combined grounding-and-quality capabilities. However, the paper has several substantive weaknesses that prevent a strong accept: the evaluation uses the same model family (Llama3) that generated the training data, the benchmark is small with no uncertainty quantification, the most directly comparable prior work (Q-Ground) is omitted from comparisons, and the central claim about "more fine-grained" assessment is not directly tested. These issues are addressable in revision. The paper sits in a borderline accept range — the contributions are real and the methodology is sound in conception, but the evaluation needs strengthening. Calibration search was unavailable, but based on the standards of ICLR and comparison with typical accept-level papers, the appropriate score is **6** (borderline accept).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>