## Summary

This paper introduces LAION-Comp, a dataset of ~540K SG-image pairs built by annotating LAION-Aesthetics V2 (6.5+) images with scene graphs via GPT-4o with partial human verification. It also introduces CompSGen Bench (20,838 samples with >4 relations) and trains several SG-conditioned models (SDXL-SG, SD3.5-SG, FLUX-SG, SD1.5-SG) using a GNN-based SG encoder. The core claim is that large-scale, high-quality structural annotations enable better compositional generation than text-only conditioning.

## Strengths

1. **Large-scale SG dataset.** LAION-Comp provides 540K SG-image pairs, roughly 5× larger than VG (~108K) and COCO-Stuff (~118K). Section 3.2 documents the scale and train/validation/test splits. This is a potentially valuable community resource.

2. **Ablation with controlled training budget.** Table 4 holds total iterations constant while varying data proportion. The result that 10% of LAION-Comp (48K samples) yields FID and Entity-IoU that beat VG-trained models (108K samples) provides evidence that annotation quality, not just quantity, drives improvement.

3. **Multiple backbone instantiations.** Consistent gains are shown across SDXL, SD3.5 (flow-matching), and FLUX backbones (Tables 2, 3), demonstrating the framework is not architecture-specific.

4. **Targeted benchmark design.** CompSGen Bench (20,838 samples, >4 relations threshold) focuses on complex compositions, a gap not directly addressed by existing SG benchmarks which lack a complexity threshold.

5. **Informative annotation analysis.** Section 3.2 provides useful comparisons: 77.48% non-spatial relations in LAION-Comp vs. 41.98% in VG, top-K frequency (most common relation at only 3.78%), and length-vs-accuracy scatter analysis. These support the diversity claim.

## Weaknesses

### Fatal
None.

### Major

1. **Confound between annotation quality, data scale, and image source quality.** The core comparison (Table 2) pits models trained on LAION-Comp (480K samples from LAION-Aesthetics 6.5+) against the same architectures trained on COCO (~118K) and VG (~108K). The 10% ablation partially addresses this, but LAION-Comp images are drawn from a higher-aesthetic pool than COCO/VG images, so the comparison still conflates image source quality with annotation format quality. A fully controlled comparison would hold images constant and vary only the conditioning format (captions vs. SGs). Without this, the paper cannot cleanly attribute gains to structural annotation quality over raw image quality differences. This weakens the paper's strongest causal claims ("unequivocally demonstrate," "consistently and significantly outperform").

2. **CLIP score usage is undefined and non-standard.** Section 3.3 states: "CLIP score calculates the similarity between the generated and ground truth images." The standard CLIP score measures image-text alignment; using it for image-image similarity is a deviation from common practice with no justification provided. The paper does not describe how this is computed (which CLIP model, which similarity function), making the CLIP column in Table 3 uninterpretable.

3. **No measures of uncertainty in any quantitative table.** Tables 2, 3, and 4 report point estimates only — no confidence intervals, standard deviations, or significance tests. Given that some differences are very small (e.g., Table 2: SD3.5-SG Rel-IoU 0.859 vs. FLUX-SG Rel-IoU 0.859; Table 3: SDXL-SG Ent.-IoU 0.792 vs. SG-Adapter Ent.-IoU 0.771), it is impossible to assess whether reported differences are meaningful.

### Minor

1. **Cross-type comparisons (T2I vs. SG2IM) are not informative for dataset quality.** Tables 2 and 3 compare T2I models (text input) against SG2IM models (SG input) on SG-derived metrics. The paper interprets the gap as evidence that "text provides far less control... compared to structured annotations." This is a trivial consequence of different input modalities — models with more structured input naturally score higher on metrics that reward structural matching. The comparison does not speak to dataset quality and should be clearly separated from the meaningful within-SG2IM comparisons.

2. **Human verification lacks key methodological details in the main text.** Section 3.1 reports 98.8%/97.5%/95.7% accuracy for objects/attributes/relations but defers sample size, sampling strategy, and inter-annotator agreement to Appendix A.5. For a dataset paper, these are central to the quality claim and merit summary statistics in the main body.

3. **Potential test distribution overlap not discussed.** CompSGen Bench is a subset of LAION-Comp's test set, which comes from LAION-Aesthetics. Since public backbones (SDXL, SD3.5, FLUX) were pretrained on LAION-5B, there is a distribution overlap between the backbones' training data and evaluation images that is not acknowledged or analyzed.

4. **Overclaim on "first SG benchmark."** The claim "we are the first to propose a compositional generation benchmark based on scene graphs" (Section 2) is narrowly defensible but overstated — SG2IM evaluation has been performed on VG and COCO-Stuff test sets in prior work. The genuine novelty is the complexity threshold (>4 relations), not the concept itself.

### Trivial
None.

## Nice-to-Haves
- Run human evaluation (the user study in Appendix A.3) as a primary comparison rather than supplementary — this would decouple quality assessment from any metric design choices.
- Hold image source constant: train the same architecture on the same images with either captions or SGs as conditioning, to isolate the effect of annotation structure.
- Report confidence intervals or standard deviations for all quantitative results.
- Test on independently-created SG benchmarks (COCO-Stuff, VG test sets) where ground-truth SGs were created independently of the training annotation pipeline.

## Removed Points
- **Evaluation metric circularity (Critical Issue 1 in the input):** The reviewer claimed the evaluation pipeline uses GPT-4o with similar prompting to the training annotation, creating a circular advantage. The paper uses metrics from Shen et al. (2024) and does not describe the extraction pipeline in the main text. The claim that the extraction uses GPT-4o is speculation — the appendix was stripped by the parser and cannot be verified. Per policy, speculative-fatal claims are removed. The subtler concern about test-distribution overlap (LAION-Aesthetics source) is retained as Minor weakness #3 above.
- **Reproducibility concerns about baseline hyperparameters:** The reviewer asked whether SG-Adapter/SGDiff were hyperparameter-tuned on LAION-Comp. This is a routine implementation detail; removed per policy on trivial reproducibility nitpicks.
- **Criticism of editing section as scope creep:** The reviewer suggested cutting the editing discussion. This is a suggestion, not a weakness, and would narrow rather than strengthen the paper's contribution.
- **General formatting/style nitpicks and speculation about missing appendix proofs:** Removed per policy.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add confidence intervals or standard deviations to all quantitative tables.
2. Justify or replace the CLIP image-image similarity usage with a standard metric.
3. Include a controlled experiment where the same images are used with caption vs. SG conditioning to isolate the effect of annotation structure.
4. Add a brief summary of human verification methodology (sample size, sampling strategy) to the main text.
5. Acknowledge and discuss potential distribution overlap between backbone pretraining data and CompSGen Bench test set.
6. Clearly separate the T2I vs. SG2IM comparison from the meaningful within-SG2IM comparison in the main argumentation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>