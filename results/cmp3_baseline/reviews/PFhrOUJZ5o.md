## Summary

This paper introduces LAION-Comp, a large-scale dataset of 540K+ images from LAION-Aesthetics annotated with detailed scene graphs (objects, attributes, relations) using GPT-4o with partial human verification. The authors train several baseline models (SDXL-SG, SD3.5-SG, FLUX-SG) that incorporate a GNN-based scene graph encoder into diffusion and flow-matching backbones, and propose CompSGen Bench, a benchmark of 20,838 complex scene samples for evaluation. Experiments show that models trained on LAION-Comp outperform prompt-only counterparts and existing scene-graph-based methods on compositional generation metrics.

## Strengths

- **Addresses a fundamental data-level limitation**: The paper correctly identifies that the core bottleneck in compositional image generation is not model architecture but the lack of structured annotations in training data. This reframing is valuable and well-motivated.
- **Large-scale, high-quality dataset construction**: LAION-Comp provides 540K scene graph annotations with 98.8% object accuracy, 97.5% attribute accuracy, and 95.7% relation accuracy (verified via human evaluation). The annotation pipeline using GPT-4o with carefully designed prompts is practical and scalable.
- **Comprehensive evaluation across multiple backbones**: The paper demonstrates consistent improvements across diffusion (SDXL, SD3.5) and flow-matching (FLUX) backbones, showing the approach generalizes beyond a single architecture. The ablation study on data proportion (10%-100%) convincingly shows the value of scale.

## Weaknesses

### Major

- **Limited novelty in the method**: The core technical contribution—using a GNN to encode scene graphs and injecting embeddings into diffusion/flow-matching backbones—is largely an engineering adaptation of existing SG2IM approaches (SGDiff, SG-Adapter). The paper does not introduce fundamentally new architectural components or training techniques. The main novelty is the dataset itself, not the method.
- **FID comparisons are misleading**: The paper acknowledges that fine-tuning pre-trained T2I models "inevitably increases FID scores" (Section 5.1), yet Table 2 shows SDXL (19.3 FID) outperforms all SG2IM models including SDXL-SG (20.1 FID). The authors claim their models are better while FID suggests the opposite. The argument that FID increase is "inevitable" weakens the quantitative case for image quality. The paper would benefit from a more principled discussion of when FID is appropriate for comparison.
- **Missing critical baselines**: The paper does not compare against recent compositional generation methods that use layout conditioning (e.g., GLIGEN, Ranni) or LLM-assisted layout planning. These are mentioned in related work but not included in experiments. Since these methods also address compositional generation, their absence makes it unclear whether LAION-Comp provides advantages over alternative conditioning approaches.

### Minor

- **The editing framework is relegated to appendix**: The paper claims SG-based editing as a contribution but provides no details in the main text. Given that editing is presented as a key advantage of structural annotations, this should at least be summarized in the main paper.
- **CompSGen Bench selection criteria**: The benchmark selects samples with "over four relations" from the test set. The rationale for this threshold is not justified, and it's unclear how sensitive results would be to different thresholds.

### Trivial

- The paper uses "Ent.-IoU" and "Entity-IoU" interchangeably in tables, which is a minor inconsistency.

## Nice-to-Haves

- A comparison with text-only models fine-tuned on LAION-Aesthetics captions (without scene graphs) would isolate the benefit of structured annotations from simply having more training data.
- Analysis of failure cases where scene graph conditioning still produces incorrect outputs would strengthen the paper.

## Novel Insights

None beyond the paper's own contributions. The key insight—that structured annotations improve compositional generation—is well-established in prior SG2IM work. The paper's main contribution is scaling this insight to a larger, higher-quality dataset.

## Suggestions

- Add comparisons with layout-based methods (GLIGEN, Ranni) to contextualize the advantages of scene graph conditioning over other structured inputs.
- Provide a more nuanced discussion of FID results, including FID on the original LAION-Aesthetics test set (not just CompSGen Bench) to better isolate the effect of fine-tuning.

## Score and Decision

The paper makes a solid contribution through the LAION-Comp dataset, which is large-scale, high-quality, and likely to be a useful resource for the community. The method itself is competent but not novel. The experimental evaluation is thorough in some dimensions but missing key baselines. Overall, this is a useful dataset paper with adequate technical contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>