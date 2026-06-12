## Summary

This paper introduces **LAION-Comp**, a large-scale dataset of 540K+ images from LAION-Aesthetics annotated with detailed scene graphs (objects, attributes, relations) via GPT-4o and partial human verification. The authors train several diffusion and flow-matching baseline models (SDXL-SG, SD3.5-SG, FLUX-SG) augmented with a GNN-based scene graph encoder, and propose **CompSGen Bench** (20,838 samples) for evaluating complex compositional generation. Experiments show that models trained on LAION-Comp outperform prompt-only counterparts and existing SG2IM methods on multiple benchmarks.

## Strengths

- **Large-scale structured dataset**: LAION-Comp fills a critical gap by providing high-quality, open-vocabulary scene graph annotations at a scale (540K) far exceeding existing SG datasets like Visual Genome. The distribution analysis (high diversity of relations/attributes, increased object count vs. captions) convincingly shows the dataset’s richness.
- **Comprehensive experimental validation**: Models are trained on three backbones (SDXL, SD3.5, FLUX) and evaluated on multiple benchmarks (CompSGen, COCO, VG, T2I-CompBench). Ablations on data proportion and comparisons with several existing SG2IM methods (SGDiff, SG-Adapter) consistently demonstrate the advantage of LAION-Comp. The qualitative examples (Figure 5) are compelling.
- **Clear motivation and framing**: The paper correctly identifies that the bottleneck in compositional generation is data-level (lack of structured annotations) rather than purely architectural, and supports this claim with evidence that SG2IM models benefit more from LAION-Comp than from prior SG datasets.
- **Benchmark contribution**: CompSGen Bench provides a focused, challenging test set for complex scenes (≥4 relations) that will be useful for future research.

## Weaknesses

### Fatal
None.

### Major

1. **Evaluation metrics rely on a biased scene graph detector**. SG-IoU, Entity-IoU, and Relation-IoU are computed using a detector trained on Visual Genome. LAION-Comp has a substantially different relation distribution (77.5% non-spatial vs. 58% spatial in VG). This mismatch likely underestimates the accuracy of models trained on LAION-Comp because the detector may fail on relation types unseen in VG, making the quantitative comparisons potentially unreliable. The paper should validate metrics with a detector updated to handle evidence from LAION-Comp or use a stronger, open-vocabulary evaluator.

2. **Human verification is insufficient**. Only 300 out of 540K samples were verified, and the claimed accuracies (98.8% objects, 97.5% attributes, 95.7% relations) are suspiciously high for automated annotation. With such a small verification set, these numbers are not statistically robust and likely overstate the true annotation quality. The paper should clearly report confidence intervals, or acknowledge that these figures are initial estimates from a tiny sample.

3. **The primary benchmark (CompSGen) shares distribution with training data**. The test set is derived from the same LAION-Aesthetics pool as the training set, which inflates performance on this benchmark. Although evaluation on COCO and VG partially addresses this, the core claim of “best performance” is largely based on CompSGen results where models trained on LAION-Comp naturally have an unfair advantage over models trained on different distributions. The paper should discuss this limitation more prominently.

4. **FID results contradict the claim of “best image quality”**. In Table 2, SDXL (T2I baseline) achieves FID 19.3, while SDXL-SG achieves 20.1—worse. The paper acknowledges that fine-tuning often increases FID, but then still claims “best performance in both image quality and accuracy” for SDXL-SG. This is misleading. The main strength is clearly improved accuracy metrics, not overall image quality.

### Minor

- The annotation pipeline relies on GPT-4o, a proprietary model whose exact behavior may change over time or vary across API versions. While the prompts are provided, full reproducibility is limited.
- The ablation study (Table 4) only explores data proportion, not variations in the model architecture (e.g., GNN vs. no GNN, different integration strategies). This would strengthen the claim that the SG encoder design is beneficial.

### Trivial

- Some figure captions are verbatim from the figure text (e.g., Figure 3, Figure 4), making the caption repetitive.

## Nice-to-Haves

- Release of LAION-Comp annotations, model checkpoints, and evaluation code will be highly valuable to the community.
- Expanding the human verification to a larger sample (e.g., a few thousand) would greatly strengthen confidence in annotation quality.
- Exploring post-hoc filtering of low-confidence scene graphs from the automated pipeline could further improve dataset quality.

## Novel Insights

The central insight—that explicit structural annotations (scene graphs) at scale are more effective than text-only data for compositional generation—is empirically validated through consistent improvements across multiple architectures and benchmarks. The analysis of annotation length vs. accuracy (Figure 3) provides a concrete demonstration that scene graphs achieve higher semantic precision per unit length compared to captions. However, this observation is largely expected from the design of scene graphs and does not constitute a deep theoretical finding beyond the paper’s own contributions.

## Suggestions

- Reproduce the key quantitative comparisons (Table 2, Table 3) using an open-vocabulary scene graph detector or human evaluation to mitigate the metric bias concern.
- Clearly state in the abstract or introduction that the primary advantage is in *compositional accuracy* rather than overall image quality (FID).
- Add a more detailed discussion of the limitations of the automated annotation pipeline (e.g., potential hallucinations from GPT-4o, failure cases) in the main paper rather than relying on the appendix.

## Score and Decision

This paper addresses an important problem (lack of structured data for compositional generation) and provides a large-scale dataset, several trained models, and a benchmark. The experiments are extensive and consistently show the value of LAION-Comp. However, the major concerns about evaluation metric bias, insufficient human verification, and the distribution overlap between training and test data weaken the strength of the conclusions. These issues are solvable, but as presented, they prevent the paper from being a strong accept.

MY FINAL SCORE: 6.0  
MY FINAL DECISION: Accept