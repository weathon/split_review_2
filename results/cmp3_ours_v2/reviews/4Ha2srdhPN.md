## Summary

GRAID presents a framework for generating high-quality spatial reasoning VQA data using only 2D bounding box geometry, explicitly avoiding the cascading errors of single-view 3D reconstruction pipelines. Applied to BDD100k, NuImages, and Waymo, it produces 8.5M+ VQA pairs with 91.16% human-validated validity (vs. 57.6% for a community SpatialVLM implementation). Fine-tuning experiments demonstrate cross-dataset and cross-question-type generalization across four VLM families.

---

## Strengths

1. **Clean, well-motivated design choice.** The insight that *qualitative* spatial relationships (left/right, closer/farther, counting) can be reliably determined from 2D bounding boxes alone—avoiding cascading 3D reconstruction errors and generative hallucinations—is genuinely sound and clearly articulated. The paper correctly identifies that metric depth is unnecessary for these queries, and this clarity of analysis is its strongest intellectual move.

2. **Compelling human validation numbers.** The human evaluation (Section 4) reports 91.16% valid VQA pairs for GRAID vs. 57.6% for OpenSpaces, based on a reasonable protocol (317 GRAID pairs, 4 evaluators, with and without bounding boxes to separate comprehension from ground-truth checking). Even accounting for different question formats (qualitative vs. metric), the gap is large enough to be meaningful.

3. **Cross-type generalization (RQ2) is the strongest experiment.** Training Llama 3.2 11B on just 6 question types yields accuracy gains across 10+ held-out types (Figure 3), providing clear evidence the model learns spatial primitives rather than memorizing template-answer mappings. The transfer holds across datasets (BDD → NuImages), strengthening the claim that learned representations are spatial rather than dataset-specific.

4. **SPARQ is a practical contribution.** The predicate-based early-rejection system yielding up to 1400× speedup is non-trivial engineering that makes large-scale generation feasible. The 5.17ms vs. 46.95ms timing breakdown is informative.

5. **Multi-backbone evaluation.** Testing across four VLM families (Llama 3.2, Gemma 3, Qwen2.5-VL, Qwen3-VL) with consistent protocol is good practice and confirms the effect is not model-specific.

---

## Weaknesses

### Fatal
None.

### Major

1. **The RQ3 benchmark evaluation cannot cleanly attribute improvements to spatial reasoning vs. generic SFT or format-compatibility effects.** GRAID-SFT produces a 32.5% improvement on A-OKVQA (a knowledge-based benchmark, not primarily spatial) and 15.94% on BLINK. The paper compares against OpenSpaces (SpatialVLM community) SFT, but OpenSpaces uses metric/numeric answers while GRAID uses binary/natural-language answers. Since the evaluation benchmarks (A-OKVQA, BLINK, etc.) use natural-language answers, the OpenSpaces-trained model may be disadvantaged by format incompatibility rather than by lower data quality. Without a control dataset matched in format (binary VQA) but devoid of spatial content, these benchmark gains cannot be confidently attributed to improved *spatial reasoning* versus generic SFT effects on instruction-following or answer-format calibration. This weakens—but does not invalidate—the RQ3 conclusions, as the human validation and RQ1/RQ2 results are independent and still support the paper's core claims.

### Minor

2. **Evaluation uses only ground-truth annotations, never a real object detector.** The paper explicitly states this choice (Section 4: *"we select to directly leverage these high-quality labels in GRAID's generation rather than train our own object detectors so that we can evaluate GRAID's effectiveness in isolation"*), which is reasonable for controlled evaluation. However, the abstract and conclusion position GRAID as operating *"on 2D bounding boxes from standard object detectors,"* implying practical deployment. The extent to which detector errors (false positives, missed detections, jittery localizations) degrade GRAID's output quality is never measured. A single experiment with YOLO or DETR would establish this practical degradation.

3. **The 91.16% human-validated accuracy is reported from only one dataset variant: GRAID-BDD without depth questions.** The paper does not report human validation for the depth variant (which introduces a new error source from depth estimation models) or for the NuImages/Waymo variants. The conclusion's claim of *"over 91.16% human-verified validity"* overstates what was actually measured, as multiple reviewers have noted the need for broader validation.

4. **The "similar planes" criterion is mentioned but never defined.** Section 3.2 states that object pairs *"should lie on similar planes"* as a necessary condition for spatial relation questions, but no geometric test, threshold, or implementation is specified. This is a gap in the method description.

5. **The SpatialVLM baseline comparison could be more precisely framed.** The paper compares against OpenSpaces (a *community implementation* of SpatialVLM), not the original method's data. While the paper is transparent about this in Section 4, the abstract's phrasing (*"a dataset produced by a current training data generation pipeline has a 57.6% human validation rate"*) could lead readers to infer a direct comparison against the original SpatialVLM. Additionally, the format mismatch between the metric questions in OpenSpaces and the qualitative questions in GRAID is not discussed as a potential confound for the SFT comparison.

### Trivial
None.

---

## Nice-to-Haves

- Report human validation for the depth variant of GRAID-BDD, to establish whether the `margin_ratio` threshold effectively mitigates depth estimation errors.
- Report inter-annotator agreement (e.g., Fleiss' κ) for the human evaluation.
- Provide total computational cost for generating the full 8.5M-pair dataset (beyond the per-template predicate timing).
- Add a brief discussion of why the ~12 named question types in the main text constitute "22 templates" (the remaining types presumably appear in the appendix, which was stripped during parsing).

---

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Missing appendix content / incomplete paper**: The harsh critic noted the appendix is unavailable and tables 4/5/6 cannot be verified. Per guidelines, the appendix is stripped by the parser; this is not a paper flaw.
- **Code/data not released during review**: The critic noted the dataset is not available for inspection. This is standard practice and not an author error.
- **Various formatting, typo, and stylistic observations**: Parser artifacts, not author errors. Removed per guidelines.
- **Missing related works**: Removed per guidelines (cannot verify external works).
- **"Human evaluators seeing boxes" limitation**: The paper's methodology (showing boxes for ground-truth verification and without boxes for difficulty ratings) is reasonable and well-described. The critic framed this as a limitation, but it is sound methodology for the intended purpose (detecting labeling errors).
- **Waymo dataset being tiny**: This is an observation about dataset size, not a weakness—the paper does not claim to use Waymo for experiments, and the selection strategy is explained.
- **SPARQ predicate reliability**: The critic questioned what happens when a predicate passes but the question cannot be realized. The paper explicitly reports this rate (78.8% for LargestAppearance) and acknowledges variation. This is adequately addressed.
- **Reproducibility concerns about undisclosed hyperparameters**: Per guidelines, trivial implementation details not central to reproduction should not be flagged as weaknesses.

---

## Novel Insights

The most insightful observation emerging from the reviews is that GRAID's strengths and weaknesses occupy different parts of the paper: the strongest evidence (human validation, cross-type generalization in RQ2) supports the data quality and framework claims, while the weakest evidence (benchmark transfer in RQ3) is where the paper makes its broadest "spatial reasoning generalizes" claim. This creates an unusual situation where the paper's practical contribution (a high-quality dataset generation framework) is well-supported, but its scientific claim about *what* the model learns during SFT is underdetermined by the evidence. The depth variant also creates a subtle tension: the paper's crisp "2D only" narrative is partially blurred when depth estimation is introduced, even though the qualitative framing (closer/farther) is more robust than metric approaches.

---

## Suggestions

1. **Add a format-matched control for RQ3.** Fine-tune on a dataset of binary yes/no VQA questions that are *not* spatial (e.g., attribute presence: "Is there a red car?") generated similarly from bounding boxes. If BLINK/A-OKVQA improvements persist, they are not due to spatial reasoning; if they disappear, the spatial-specific claim is strongly supported.

2. **Evaluate with at least one real object detector.** Run the full pipeline with YOLOv8 or DETR on BDD images (without ground-truth annotations), report human validation rates and downstream fine-tuning results. Even one setting would indicate the degradation from realistic inputs.

3. **Qualify the 91.16% number.** Report human validation for the depth variant and at least one NuImages variant. If non-depth variants are all similar, say so explicitly.

4. **Define or remove the "similar planes" criterion.** Either specify the geometric test used or state that it is a placeholder for future work.

5. **Better characterize the baseline.** Add a brief discussion of how the community SpatialVLM implementation differs from the original, and explicitly address the format mismatch (metric vs. binary answers) as a possible confound in the SFT comparison.

---

## Score and Decision

**Calibration anchors (all retrieved from the human-review database):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| STUPD (eqz5aXtQv1) | 4.33 | R1 | Synthetic spatial dataset, no human validation, rejected. GRAID is significantly stronger. |
| SR^2 (2seVGyWZOX) | 5.20 | R1 | 3D point-cloud spatial reasoning, marginal improvements, rejected. GRAID has broader and stronger evidence. |
| MMR Benchmark (mzL19kKE3r) | 6.00 | R2 | Large-scale dataset + baseline for reasoning segmentation, accepted. Similar contribution type and rigor. |
| Does Spatial Cognition Emerge (WK6K1FMEQ1) | 6.75 | R2 | Spatial cognition benchmark, accepted. Different contribution type (evaluation only) but comparable quality. |
| PhysBench (Q6a9W6kzv5) | 8.00 | R1 | Comprehensive benchmark + method for physical world understanding, accepted. Stronger across most dimensions. |
| Do VLMs Represent Space (84pDoCD4lH) | 7.40 | R1 | Evaluation protocol for spatial reasoning in VLMs, accepted. Strong methodology, different contribution type. |

**Bracket:** Round 1 initial range 5.5–7.5; narrowed to 6.0–6.5 based on anchor inspection.

**Final score:** 6.0. The paper has a clean core idea, a substantial dataset contribution (8.5M pairs), compelling human validation, and strong evidence for cross-type/cross-dataset generalization. The RQ3 attribution issue is a significant weakness but does not undermine the core contributions (framework, dataset quality, RQ1, RQ2), which stand independently. Remaining weaknesses are fixable without rethinking the paper's approach. The contribution is real but not extraordinary, placing it solidly in borderline-accept territory.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>