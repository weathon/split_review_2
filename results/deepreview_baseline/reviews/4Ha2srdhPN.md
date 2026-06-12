## Summary

GRAID is a framework that generates high-quality spatial reasoning VQA data using only 2D bounding boxes from standard object detectors, deliberately avoiding 3D reconstruction errors and caption-based hallucinations. By operating on 2D geometry alone and employing a lightweight predicate system (SPARQ) for early filtering, the authors generate over 8.5 million VQA pairs from three driving datasets with 91.16% human-validated accuracy, and show that fine-tuning VLMs on this data improves performance on multiple spatial reasoning benchmarks.

## Strengths

- **Key insight is well motivated and effective**: The core idea that qualitative spatial relationships can be determined reliably from 2D bounding boxes alone is simple yet powerful. The human evaluation convincingly shows that this approach yields much higher data validity (91.16%) compared to a depth-estimation-based pipeline (57.6%), directly supporting the main motivation.
- **Large-scale, high-quality dataset**: Producing over 8.5M VQA pairs with high human-validated accuracy is a practical contribution that the community can leverage. The three source datasets cover diverse driving conditions, and the 22 question templates span a useful range of spatial reasoning skills.
- **Clear evidence of transfer learning**: The fine-tuning experiments (RQ1 and RQ2) demonstrate that models trained on GRAID data generalize across datasets (BDD → NuImages) and across question types not seen during training, indicating that genuine spatial concepts are learned rather than dataset-specific patterns. The improvements on external benchmarks (BLINK, A-OKVQA, VSR, RealWorldQA) further validate practical utility.

## Weaknesses

### Major

1. **Limited baseline comparisons in human evaluation**: Only the community implementation of SpatialVLM is quantitatively compared in the human evaluation. SpatialRGPT and SpaRE are discussed but not included in the head-to-head human study. Without comparing against these methods under the same evaluation protocol, the claim that GRAID produces “datasets that are of higher quality than existing tools” is only partially supported.

2. **Narrow domain scope despite claim of domain-agnosticism**: All three source datasets are from autonomous driving. Although the authors assert the method is domain-agnostic, the paper lacks a demonstration on non-driving images (e.g., indoor scenes from COCO, ScanNet, or general web images). The transfer only goes one way (driving → general via benchmarks); generation on general images is untested, which limits confidence in the claimed generality.

3. **Lack of robustness analysis to detection noise**: All experiments use ground-truth bounding boxes from the AV datasets. In practice, users would apply an object detector. The paper does not evaluate how GRAID’s data quality and downstream performance degrade when predicted boxes are used instead of ground-truth. This gap weakens the claim that GRAID requires only “object detection outputs” with no further quality control.

4. **SPARQ contribution is overstated**: While the predicate approach yields speedups, it is a straightforward engineering optimization (early rejection of infeasible class-pairs). The claimed 1400× speedup applies only to a single, already-cheap template; average speedups are much smaller (≈9×). Listing SPARQ as a core contribution alongside the dataset and framework inflates its significance.

### Minor

- The human evaluation sample sizes are small (317 for GRAID, 250 for SpatialVLM). The paper should report confidence intervals and inter-annotator agreement to strengthen reliability.
- The fine-tuning experiments use LoRA with limited steps (200) and a fixed hyperparameter set. No ablation studies are provided to examine sensitivity to learning rate, rank, or training steps.
- The paper does not compare against simply fine-tuning on existing spatial VQA datasets (e.g., VSR, BLINK training sets), leaving it unclear what unique value GRAID data adds beyond what is already available.
- Results on Qwen3 VL 8B show “lesser gains” but this is not analyzed. Understanding why some backbones benefit more than others would improve the paper.

### Trivial

- The sentence “Table 1 offers a comparison…” appears twice in the introduction.
- Figure 2 and Figure 3 have excessively long captions that repeat content from the text.
- Some question template names (e.g., “Not Co”) are cryptic and could be clarified.

## Nice-to-Haves

- An experiment that applies GRAID to an indoor dataset (e.g., COCO) with predicted boxes would substantially strengthen the domain-agnostic claim.
- A comparison with SpaRE in the human evaluation (same images, same annotators) would fill an important gap.
- An analysis of how detection accuracy (mAP) affects GRAID’s data validity and downstream performance would increase practical utility.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Include a human evaluation that compares GRAID to at least one additional method (SpatialRGPT or SpaRE) under identical conditions, with larger sample sizes and reported inter-annotator agreement.
- Demonstrate GRAID on a non-driving dataset (e.g., images from COCO or Visual Genome) using an off-the-shelf detector to show generality.
- Add an ablation that replaces ground-truth boxes with outputs from a detector of varying accuracy to understand sensitivity to detection noise.
- Benchmark against existing spatial VQA training data (e.g., VSR train set) to clarify the unique advantage of GRAID.

## Score and Decision

**Score**: 6.0

**Decision**: Accept

This paper makes a solid contribution by introducing a practical, high-quality spatial VQA generation framework that avoids common errors in prior work. The core insight is well validated, and the generated dataset is immediately useful. However, the evaluation is limited in breadth (baseline comparisons, domain coverage, robustness to detection noise), which prevents a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>