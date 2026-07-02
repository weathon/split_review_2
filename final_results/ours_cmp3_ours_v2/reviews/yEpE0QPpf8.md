## Summary

This paper proposes grounding-IQA, a new IQA paradigm that integrates spatial grounding (bounding boxes) with quality assessment via two subtasks: GIQA-DES (description with localization) and GIQA-VQA (referring/grounding QA). The authors construct GIQA-160K (~168K samples, ~43K images) through an automated annotation pipeline using Llama3, Grounding DINO, and Q-Instruct, and introduce GIQA-Bench (100 images, 250 test samples). Fine-tuning four MLLMs on GIQA-160K produces models with measurable grounding-IQA capabilities.

## Strengths

1. **Well-motivated task formulation.** Integrating spatial grounding with IQA addresses a genuine gap — existing MLLM-based IQA methods describe quality without localizing the regions driving those judgments. Sections 1 and 3.1 make this case clearly with concrete examples (Fig. 2) showing why language-only descriptions are insufficient for fine-grained assessment.

2. **Large-scale automatically annotated dataset.** GIQA-160K is a substantial resource. The automated pipeline (Sec. 3.2) is thoughtfully engineered: it uses Llama3 for object tag extraction, Grounding DINO for detection, and Q-Instruct for IQA-based box filtering (Alg. 1). The coordinate discretization scheme (Eq. 1–2, 20×20 grid) reduces token count from 21 to 9 while remaining practically usable.

3. **Consistent improvement across four base models.** Table 4 shows that fine-tuning LLaVA-1.5-7B/13B, LLaVA-1.6-7B, and mPLUG-Owl2-7B on GIQA-160K consistently improves performance across nearly all metrics (e.g., LLaVA-1.5-7B Acc (Total) from 0.4733 to 0.6850). This demonstrates the dataset's compatibility with diverse architectures.

4. **Well-designed ablations on pipeline components.** The box refinement ablation (Tab. 2a) shows IQA-Filter and Box-Merge improve mIoU (0.5624→0.5851) and Tag-Recall (0.5045→0.5497). Fig. 6 shows refinement shifts box area distribution closer to human annotations. The discrete vs. continuous coordinate comparison (Tab. 2b) is informative, showing the coarser representation actually improves description quality (BLEU@4: 22.03→23.67).

## Weaknesses

### Fatal
None.

### Major

1. **No ablation isolates the value of grounding from additional IQA training data.** The paper claims grounding-IQA enables "more fine-grained quality perception." However, no experiment compares fine-tuning on GIQA-160K (with grounding boxes) against fine-tuning on an equivalent amount of non-grounding IQA description data (e.g., the original Q-Pathway/DQ-495K descriptions without boxes). The improvements in Table 4 could be driven simply by more task-specific IQA training data rather than the grounding component. Table 3 compares Only-DES vs. Only-VQA vs. combined, but all three use GIQA-160K (grounding) data. Without this control, the central claim that grounding specifically enables finer-grained perception is not directly supported. The paper's core contributions (dataset, pipeline, paradigm) are not invalidated, but this gap weakens the strongest claim made for the paradigm.

2. **Table 5 comparisons conflate training data with model capability.** Table 5 compares Ground models (Shikra, Kosmos-2, Ferret, GroundingGPT) evaluated off-the-shelf and IQA models (DepictQA-Wild, Q-Instruct) fine-tuned on different datasets against "Ours" (same base models fine-tuned on GIQA-160K). The text states "our method outperforms existing MLLMs" (line 341). This conflates "trained on the target task data" with "superior architecture." The comparison is useful for showing existing models cannot perform grounding-IQA without task-specific training, but it does not support a claim of architectural superiority. The paper would be more accurate to fine-tune comparison models on GIQA-160K (or at least acknowledge that the comparison is between trained-on-task and not-trained-on-task).

### Minor

3. **Small benchmark with limited statistical power.** GIQA-Bench contains only 100 images and 250 test samples (100 GIQA-DES, 150 GIQA-VQA). For a benchmark intended to establish a new task paradigm, this is limited. No confidence intervals or statistical significance tests are reported. The benchmark's GIQA-DES annotations are manually determined (line 228), which mitigates evaluation bias concerns, but the small size makes the reported metrics potentially sensitive to the specific test set.

4. **Tag-Recall metric is underspecified.** The paper states Tag-Recall requires "object name similarity exceeds a 0.5 threshold" (Sec. 3.4, line 236) but never defines what "object name similarity" means — exact match? embedding cosine similarity? ROUGE-L? This makes all grounding precision results not reproducible.

5. **IQA-Filter creates a circular dependency with unanalyzed bias.** Stage-3 uses Q-Instruct to verify boxes by asking "Is the image quality <T_q>?" (Alg. 1). Any systematic biases in Q-Instruct (e.g., toward certain distortion types or object classes) propagate into the training data. The paper does not analyze the IQA-Filter's precision/recall or failure cases, so the extent of this issue is unknown.

### Trivial

6. **Inconsistent acronym usage and a typo.** The paper uses both "IQA" and "IQG" inconsistently — the Table 5 group header labels IQA models as "IQG" (line 324), the text refers to "IQG models" (line 341) and "new IQG task paradigm" (line 349). "DepictIQa-Wild" (line 324) appears to be a typo for "DepictQA-Wild."

## Nice-to-Haves

- Add a control experiment: fine-tune the same base model on the original Q-Pathway/DQ-495K descriptions (without boxes) vs. GIQA-160K (with boxes), controlling for data quantity. If the GIQA-160K model outperforms on description quality metrics (BLEU@4, LLM-Score), this would directly validate the claim that grounding improves quality perception.
- Report bootstrap confidence intervals for the main results given the small benchmark size.
- Analyze the IQA-Filter's precision/recall and failure cases to help users gauge dataset quality.
- Quantify the impact of the 20×20 coordinate discretization on practical grounding precision for downstream tasks (e.g., image editing requiring finer localization).

## Removed Points

The following points from the input review were removed for the stated reasons:
- **Issue 3 "evaluation bias" (shared annotation methodology)**: Removed because GIQA-Bench's GIQA-DES annotations are manually determined by humans with bounding boxes "manually determined" (line 228), not generated by the automated pipeline. The GIQA-VQA questions use the pipeline but are "refined and answered by humans." This criticism overstated the overlap.
- **Figure 1 caption duplicate entries**: Moved from weakness to removed because the parser likely duplicated text from the figure. HPLUS-Duo-7B may be discussed in the (stripped) appendix.
- **"IQG"/"IQA" interchangeability in abstract/intro**: Kept as a trivial weakness since the table and conclusion use "IQG" which is inconsistent with the paper's title and abstract.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add the critical control experiment (non-grounding IQA data vs. GIQA-160K) to isolate the effect of spatial grounding on quality perception.
2. Specify the "object name similarity" metric used in Tag-Recall.
3. Reframe the claims about Table 5 to acknowledge it shows existing models lack grounding-IQA capability without task-specific training, rather than claiming architectural superiority.
4. Expand GIQA-Bench or at minimum report confidence intervals for key results.
5. Analyze IQA-Filter error cases to surface potential biases in the dataset.

## Score and Decision

**Anchors used for calibration:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Q-Adapt | 5.25 | R1 | Similar genre (IQA + instruction tuning); rejected with comparable weaknesses in experimental validation |
| Enhancing Descriptive IQA | 5.75 | R1 | Dataset+paradigm IQA paper; rejected as a data extension; current paper has stronger novelty but weaker validation |
| Dog-IQA | 4.75 | R1 | Zero-shot IQA; rejected due to limited novelty; current paper has clearer contribution |
| EvalAlign | 4.75 | R1 | SFT for evaluation; rejected with experimental design concerns; comparable severity of issues |
| Q-Bench | 7.33 | R1 | MLLM benchmark for low-level vision; accepted with extensive, comprehensive experiments; current paper is notably weaker on this front |

**Round 1 bracket:** 4.5–6.0. The paper sits between Dog-IQA (4.75) and EDQA (5.75). It has stronger novelty than EDQA but weaker experimental validation. The missing control experiment (grounding vs. non-grounding data) is the most significant gap, but the dataset, pipeline, and paradigm contributions are real.

**Final score:** 5.0. The paper proposes a genuinely novel task paradigm and contributes a substantial dataset. The automated pipeline is well-engineered and the ablations are informative. However, the experimental validation has two significant gaps: (1) no control experiment isolating whether grounding (vs. just more IQA data) drives the reported improvements, and (2) Table 5 comparisons frame models trained on different data as directly comparable. These gaps prevent the paper from convincingly supporting its central claim about "more fine-grained quality perception." With the addition of the proper control experiment and revised comparison framing, this could be a solid contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>