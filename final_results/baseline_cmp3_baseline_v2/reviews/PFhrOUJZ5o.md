## Summary

This paper introduces LAION-Comp, a large-scale dataset of 540K+ images with structural scene graph annotations (objects, attributes, relations) built on top of LAION-Aesthetics V2. The authors train several baseline models (SDXL-SG, SD3.5-SG, FLUX-SG) that incorporate a GNN-based scene graph encoder into diffusion and flow-matching backbones, and propose CompSGen Bench, a benchmark of 20,838 samples for evaluating compositional generation. Experiments show that models trained on LAION-Comp outperform prompt-only counterparts and existing scene-graph-based methods on compositional benchmarks.

## Strengths

- **Addresses a fundamental data-level problem**: The paper correctly identifies that the core limitation in compositional image generation is not just model architecture but the lack of structured annotations in training data. This is a well-motivated and important research direction.
- **Large-scale, high-quality dataset construction**: LAION-Comp provides 540K scene graph annotations with high human-verified accuracy (98.8% objects, 97.5% attributes, 95.7% relations), significantly larger than existing SG datasets like Visual Genome and COCO-Stuff. The annotation pipeline using GPT-4o with carefully designed prompts is practical and scalable.
- **Comprehensive evaluation across multiple backbones**: The paper demonstrates consistent improvements across diffusion (SDXL, SD3.5) and flow-matching (FLUX) backbones, showing the generality of the approach. The ablation study on data proportion (10%-100%) convincingly shows the value of scale.
- **New benchmark for compositional generation**: CompSGen Bench provides a dedicated evaluation suite with 20,838 complex samples, filling a gap in existing benchmarks that focus primarily on text-based generation.

## Weaknesses

### Major

- **Limited novelty in the model architecture**: The GNN-based scene graph encoder is a straightforward application of existing techniques (similar to SGDiff, SG-Adapter). The core contribution is the dataset, not the model. The paper would be stronger if it acknowledged this more clearly and focused on the dataset as the primary contribution.
- **FID scores are not directly comparable across methods**: The paper reports that fine-tuning increases FID (which is expected), but the FID comparison between T2I models (SDXL: 19.3) and SG2IM models (SDXL-SG: 20.1) is confounded by the fact that T2I models are evaluated on their original training distribution while SG2IM models are fine-tuned. The claim that "our baseline achieves the best performance among all candidates in both image quality and accuracy" is weakened by this apples-to-oranges comparison.
- **Missing analysis of failure cases and limitations**: The paper does not discuss scenarios where LAION-Comp-trained models still fail, or what types of compositional relationships remain challenging. This would strengthen the paper's scientific rigor.

### Minor

- **The editing framework is relegated to the appendix** (Sec. A.1) but mentioned as a contribution in the abstract and introduction. Without seeing the appendix, it's difficult to evaluate this claim. The paper should either include it in the main text or remove it from the core contributions.
- **The comparison with existing SG datasets (COCO, VG) is not entirely fair**: LAION-Comp is built on LAION-Aesthetics (high-quality, aesthetic images) while COCO and VG contain more diverse, lower-quality images. The performance gains could partially come from the image quality of the base dataset rather than the annotation quality alone.
- **The paper claims "first to propose a compositional generation benchmark based on scene graphs"** but this is a relatively incremental contribution given existing benchmarks like T2I-CompBench.

### Trivial

- The paper uses "LAION-Comp" as the dataset name but the title uses "LAION-COMP" (inconsistent capitalization).

## Nice-to-Haves

- A human evaluation study comparing generations from LAION-Comp-trained models vs. baselines would strengthen the claims about perceptual quality.
- Analysis of which specific relation types (spatial vs. non-spatial) benefit most from the structured annotations would provide deeper insight.
- Discussion of potential biases in the GPT-4o annotation pipeline (e.g., cultural biases in attribute descriptions) would be valuable.

## Novel Insights

None beyond the paper's own contributions. The key insight—that structured scene graph annotations at scale improve compositional generation—is valuable but not surprising given prior work on scene-graph-to-image generation. The paper's main novelty is in demonstrating this at scale with a practical annotation pipeline.

## Suggestions

1. Restructure the paper to clearly separate the dataset contribution (primary) from the model contribution (secondary/standard). The current framing over-emphasizes model novelty.
2. Include a more rigorous comparison where T2I models and SG2IM models are evaluated on the same held-out test set with matched conditions, or clearly acknowledge the comparison limitations.
3. Add a dedicated limitations section discussing what types of compositional scenes remain challenging (e.g., very dense scenes, rare relations, abstract concepts).
4. Consider releasing the GPT-4o annotation prompts and human verification protocol as part of the dataset documentation to facilitate reproducibility.

## Score and Decision

The paper makes a solid contribution through the LAION-Comp dataset, which addresses a genuine bottleneck in compositional image generation. The experiments are thorough and the results are convincing. However, the model architecture contribution is incremental, and the evaluation comparisons have some fairness issues. The paper is a clear accept for a dataset/benchmark contribution but not at the highest tier.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>