## Summary

This paper introduces GRAID, a framework for generating high-quality spatial reasoning VQA data from images using only 2D bounding boxes from standard object detectors. By explicitly avoiding single-view 3D reconstruction and caption-driven synthesis, GRAID produces datasets with over 91% human-validated accuracy—substantially higher than existing methods like SpatialVLM (57.6%). The framework is applied to BDD100k, NuImages, and Waymo, yielding over 8.5M VQA pairs, and includes SPARQ, a predicate library that accelerates generation up to 1400×. Fine-tuning VLMs on GRAID data yields consistent improvements on benchmarks such as BLINK, A-OKVQA, and RealWorldQA, with strong evidence of cross-dataset and cross-question-type generalization.

## Strengths

- **Clean core insight with practical impact.** The key idea—that qualitative spatial relationships can be reliably determined from 2D bounding boxes, bypassing cascading errors from depth estimation and generative hallucinations—is both novel and elegantly simple. This makes the framework easy to adopt and less error-prone than prior work.

- **Demonstrably higher data quality.** Human evaluation shows 91.16% validity for GRAID-generated VQA pairs versus 57.6% for a SpatialVLM dataset. The quality gap is large and convincingly measured, addressing a critical bottleneck in spatial reasoning training data.

- **Strong evidence of generalization and transfer.** Training on only 6 question types from GRAID-BDD improves performance on 10+ held-out types and on an entirely unseen dataset (GRAID-NuImages). This indicates that models acquire genuine spatial primitives rather than overfitting to template patterns or dataset-specific appearance.

- **Scalable and well-engineered framework.** SPARQ’s predicate-based early rejection yields up to 1400× speedups on expensive templates, enabling generation of millions of VQA pairs in hours. The framework is modular, supports multiple detectors, and is ready for community extension.

- **Comprehensive fine-tuning experiments.** The paper evaluates four different VLMs (Llama 3.2 11B, Gemma 3 4B, Qwen2.5 VL 3B, Qwen3 VL 8B) across multiple established benchmarks. GRAID-fine-tuned models consistently outperform both base models and models fine-tuned on SpatialVLM data, with notable gains on spatial sub-tasks (e.g., +41.13% on BLINK Relative Depth).

## Weaknesses

### Fatal

None.

### Major

- **Limited domain diversity in data generation.** GRAID is claimed to be domain-agnostic, but all generated data comes from autonomous driving datasets (BDD, NuImages, Waymo). While the benchmark evaluations include indoor/outdoor scenes, the paper would be strengthened by also generating data from a non-driving source (e.g., COCO with a YOLO detector) to directly demonstrate domain agnosticism in the generation pipeline. Without this, the claim is somewhat undersupported.

- **Human evaluation scope.** The human evaluation only covers GRAID-BDD (without depth questions) and OpenSpaces (SpatialVLM). The depth-based questions in GRAID are not separately validated, so the 91.16% validity figure may not apply to those variants. Additionally, the sample size (317 VQA pairs) is modest; a larger study would increase confidence in the quality claim.

- **Lack of sanity controls in fine-tuning experiments.** The paper reports large accuracy gains from relatively small-scale fine-tuning (e.g., 200 steps, 6 question types). Without a negative control (e.g., fine-tuning on scrambled labels or random QA pairs), it is unclear how much of the improvement comes from the inherent quality of GRAID data versus mere exposure to any spatial-style questions. This would significantly strengthen RQ1 and RQ2.

### Minor

- **Depth question quality is not evaluated.** The paper includes depth-based question types (e.g., Closer, Farther) that rely on monocular depth estimators, which are known to be noisy. A separate human evaluation or analysis of those questions (e.g., showing validity rates or agreement with ground-truth depth) would clarify their contribution to the overall claims.

- **Statistical significance not reported.** The benchmark results are given as point estimates without confidence intervals or error bars. Given the modest sizes of some benchmark subsets, it would be helpful to know whether the reported gains are statistically reliable.

- **The 91.16% “human-validated accuracy” definition is slightly ambiguous.** The text reports 95.58% valid questions and 93.69% valid answers, then states “over 91.16%” and “less than 9% … invalid or confusing.” Clarifying the exact metric and whether it is a conjunction would avoid confusion.

### Trivial

None.

## Nice-to-Haves

- A direct generation experiment on a general-purpose dataset (e.g., COCO) using a standard detector (e.g., YOLOv8) to demonstrate domain agnosticism.
- Human evaluation of depth-based GRAID questions to confirm they also meet a high validity threshold.
- Ablation studies on the effect of data scale (e.g., how model performance varies with the fraction of GRAID data used).
- Statistical significance tests or bootstrap confidence intervals for benchmark results.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. Perform a negative-control fine-tuning experiment (e.g., training on data with randomly shuffled answers) to isolate the effect of GRAID’s data quality from mere exposure to spatial templates.
2. Add a human evaluation for the depth-based question types in GRAID to substantiate the claimed validity across all template groups.
3. Generate and evaluate a GRAID variant from a non-driving source (e.g., COCO with off-the-shelf detectors) to directly validate the domain-agnostic claim.

## Score and Decision

**Score:** 7.0  
**Decision:** Accept

MY FINAL SCORE: <score>7.0</score>  
MY FINAL DECISION: <decision>Accept</decision>