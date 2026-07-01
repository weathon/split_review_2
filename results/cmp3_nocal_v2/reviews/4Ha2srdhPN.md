## Summary

GRAID presents a framework for generating high-quality spatial VQA training data by operating exclusively on 2D bounding boxes, deliberately avoiding the cascading errors of single-view 3D reconstruction and the hallucinations of caption-based generation. The paper instantiates 22 VQA templates on BDD100k, NuImages, and Waymo, producing 8.5M+ VQA pairs, introduces SPARQ (a predicate-based efficiency mechanism), and demonstrates that fine-tuning on GRAID data yields transferable spatial reasoning gains — most notably that training on just 6 question types improves performance on 10+ held-out types and an entirely unseen dataset.

## Strengths

1. **Principled core insight (Sec. 3.1).** The observation that qualitative spatial relationships (left/right, closer/farther, counting, size ranking) can be deterministically derived from 2D bounding-box geometry is simple but effective. By sidestepping depth estimation and camera calibration, GRAID avoids the error-amplification cascade that plagues metric-space methods. This design choice is clearly motivated and well-executed.

2. **Strong generalization evidence from RQ2 (Sec. 5, Figure 3).** Training a Llama 3.2 11B model on only 6 question types from GRAID-BDD and observing accuracy improvements on 10+ held-out types — including the entirely unseen GRAID-NuImages dataset (+38.0pp) — is the paper's most compelling result. It demonstrates that the data teaches transferable spatial reasoning primitives rather than template-specific patterns.

3. **Large-scale dataset release.** Generating 8.5M VQA pairs across three real-world driving datasets with diverse geographies and conditions is a substantial engineering contribution. The SPARQ predicate library (up to 1400× per-template speedups) addresses a real scalability concern.

4. **Extensible, domain-agnostic framework.** GRAID's support for Detectron2, MMDetection, and Ultralytics, combined with a template interface that decouples predicates from question realization, makes the framework reusable beyond the driving domain. The paper is honest that the 22 templates are a demonstration, not an exhaustive set.

5. **Honest reporting of regressions.** The paper explicitly notes regression on *LessThanThresholdHowMany* and *MoreThanThresholdHowMany* (Sec. 5, RQ2), lending credibility to the experimental reporting.

## Weaknesses

### Fatal
None.

### Major

1. **The headline human evaluation comparison (91.16% vs 57.6%) has confounds that are not adequately discussed.** The comparison conflates two differences simultaneously: (a) GRAID asks qualitative yes/no questions with answers deterministically computable from bounding-box coordinates, while SpatialVLM asks metric estimation questions requiring accurate depth; and (b) GRAID uses ground-truth object detection annotations (line 155: "we select to directly leverage these high-quality labels"), while the SpatialVLM comparison uses a community implementation with estimated depth and detections. The 91.16% figure is not surprising — a question whose answer is a logical consequence of ground-truth annotations can hardly be wrong unless the annotations themselves are wrong. Meanwhile, the 57.6% figure reflects the difficulty of metric estimation from noisy single-view depth. The paper presents these numbers as a head-to-head quality comparison but does not control for these confounds. This weakens the strongest empirical claim but does not invalidate GRAID's contribution, which rests on more than this single comparison.

2. **No inter-annotator reliability for the human evaluation.** Four evaluators each assessed a different random subset of 317 GRAID VQA pairs (seeded by their names), meaning every pair was evaluated by exactly one person. There is no overlap and therefore no measure of agreement (e.g., Fleiss' κ). Given the weight this evaluation carries for the paper's headline validity claims, this is a significant methodological gap. The paper should report agreement statistics or provide evidence that the judgments are reliable.

### Minor

1. **Misaligned metric definitions in the headline comparison.** The abstract and introduction report "91.16% human-validated accuracy" for GRAID (a combined question+answer validity rate: 28 unique issues out of 317 pairs) alongside "57.6%" for OpenSpaces — but the 57.6% is the answer-incorrectness rate from Section 4 (144/250 answers incorrect), not a combined validity metric. Meanwhile, the abstract also calls 57.6% a "human validation rate" (line 9) and the introduction says "only 57.6% of questions are valid" (line 51). These are different quantities being compared. While the paper provides sufficient raw data for a careful reader, the side-by-side framing is imprecise and could mislead.

2. **No experiment with non-ground-truth object detectors.** The paper intentionally uses ground-truth annotations to "evaluate GRAID's effectiveness in isolation" (line 155). This is a reasonable design choice, but it means the 91.16% validity figure reflects the quality of BDD annotations plus GRAID's template design, not GRAID's robustness to realistic detector noise. An experiment feeding estimated (e.g., YOLO) detections through the same pipeline would clarify how much of the quality gap is attributable to GRAID's approach vs. the input quality difference.

3. **No discussion of label noise amplification.** Since GRAID's answers are deterministically derived from annotations, any single annotation error (the paper found 5 labeling errors in BDD) can propagate into every question involving that object. With 8.5M pairs from tens of thousands of images, the paper should discuss whether the template structure amplifies labeling errors.

4. **Speedup framing could be more precise.** The "up to 1400× speedups" claim is a per-template statistic for `LargestAppearance` (where the predicate takes 0.02ms and realization takes 46.95ms, and the predicate succeeds 78.8% of the time). The paper provides this context but does not clarify that this is not a pipeline-level speedup. The framing is technically correct but could be read as implying end-to-end savings of that magnitude.

### Trivial
None.

## Nice-to-Haves

- Adding inter-annotator agreement analysis for the human evaluation.
- An experiment running GRAID with estimated (non-ground-truth) detections to separate input quality from method quality.
- Explicitly aligning the metric definitions when comparing GRAID's and SpatialVLM's human evaluation results.
- A brief discussion of label noise amplification at scale.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Abstract mixes RQ1 and RQ2 results"** — REMOVED as factually incorrect. The abstract says "models fine-tuned on 6 question types" which maps to RQ2, and the numbers (47.5%, 37.9%) match RQ2's Δ+47.5pp and Δ+38.0pp. RQ1 numbers (49.7%, 29.1%) are not in the abstract. No mixing occurred.

- **"Missing related work on bounding-box methods"** — REMOVED (scope creep; the paper cites Wang et al. 2023, Yang et al. 2023b, Peng et al. 2023, Rasheed et al. 2024, Zhang et al. 2025a in the "Leveraging existing data" paragraph, and the critic's demand for deeper positioning is a matter of degree, not omission).

- **"Learning rate $2^{-4}$ formatting concern"** — REMOVED (parser artifact; the original submission's formatting is not verifiable from the extracted text).

- **"Tables 4-6 missing"** — REMOVED (the parser strips the appendix; these tables exist in the original submission).

## Novel Insights

The reviews surface one genuine insight beyond the paper's own framing: that the paper's strongest contribution is not the 91.16% validity rate but the RQ2 generalization result (6 → 10+ held-out types with cross-dataset transfer). The paper would benefit from restructuring its narrative to center this result, treating the human evaluation as secondary supporting evidence. Additionally, the observation that the validity comparison is fundamentally between two different kinds of questions (qualitative classification vs. metric regression) reframes what the paper is actually demonstrating: that qualitative spatial questions are a more robust data modality for training, not just that GRAID's specific pipeline is better engineered.

## Suggestions

1. Reframe the headline comparison to transparently acknowledge the confounds: (i) qualitative vs. metric question types, and (ii) ground-truth vs. estimated inputs. Consider running GRAID with a realistic detector to show that the quality advantage holds even without oracle annotations.
2. Add inter-annotator agreement statistics for the human evaluation, or at minimum have multiple annotators evaluate a shared subset.
3. Align the metric definitions when comparing GRAID and SpatialVLM — report the same quantity (e.g., answer correctness or combined validity) for both methods in the abstract and introduction.
4. Add a brief discussion of how annotation errors propagate through the template structure.

## Score and Decision

The paper makes a genuinely useful contribution: the core insight is sound, the RQ2 generalization results are convincing, the dataset scale is substantial, and the framework is well-architected for reuse. The weaknesses are real but addressable and do not undermine the paper's core contribution. The comparison issues and missing inter-annotator reliability can be corrected in a revision without changing the experimental outcomes.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>