The calibration corpus is not accessible. I will proceed with my best judgment calibrated against my knowledge of ICLR standards.

Let me finalize the review now.

## Summary

This paper introduces LAION-Comp, a dataset of 540K+ images from LAION-Aesthetic V2 (6.5+) annotated with scene graphs (objects, attributes, inter-object relations) using GPT-4o with partial human verification. The authors also release CompSGen Bench (20,838 samples for complex scenes with >4 relations) and train four SG-conditioned models (SD1.5-SG, SDXL-SG, SD3.5-SG, FLUX-SG) via a GNN-based scene graph encoder. The core claim is that high-quality structural annotations at scale are the bottleneck for compositional generation, not model architecture.

## Strengths

- **Controlled cross-dataset comparison isolates dataset quality as the causal factor**: Table 2 holds the architecture constant (SDXL-SG) while varying only the training dataset (COCO, VG, LAION-Comp). LAION-Comp consistently outperforms on SG-IoU (0.558 vs 0.497/0.546), Entity-IoU (0.884 vs 0.842/0.813), and Relation-IoU (0.856 vs 0.833/0.800). This is a clean experiment that directly validates the dataset's value—no confound with training status because all three use the same fine-tuning procedure.

- **Data-scaling ablation proves that quality advantage is separable from scale**: Table 4 trains SDXL-SG on 10%, 20%, 50%, 100% of LAION-Comp with constant total iterations. At just 10% (~48K samples—less than VG's training size), SG-IoU (0.530) and Entity-IoU (0.874) already match or exceed full VG results (0.546, 0.813). This provides direct evidence that LAION-Comp's annotation quality, not just its larger scale, drives the gains.

- **Quantified non-spatial relation diversity substantially exceeds prior SG datasets**: 77.48% of relations in LAION-Comp are non-spatial (e.g., "holding", "wearing") vs. only 41.98% in Visual Genome. The top relation accounts for just 3.78% of all relations, demonstrating broad coverage beyond geometric/locational focus. This is concretely attributable to the annotation pipeline's prompt design (Sec. 3.1), which explicitly requires concrete verbs and discourages spatial-only relations.

- **Annotation efficiency validated on identical images**: Table 1 and Figure 3 compare LAION-Comp SG annotations vs. original LAION captions on the same set of images. The SG format achieves higher SG-IoU+ (0.422 vs 0.306), Entity-IoU+ (0.810 vs 0.631), and Relation-IoU+ (0.749 vs 0.557), controlling for image content and isolating structural format as the source of higher fidelity.

- **Generalization across four backbones and two architectural families**: The SG encoding approach yields consistent improvements over prompt-only baselines on SD1.5, SDXL (diffusion), SD3.5, and FLUX (flow matching) on CompSGen Bench (Table 3). This demonstrates the method is not architecture-specific.

## Weaknesses

### Fatal
None.

### Major

- **The T2I vs. SG2IM comparison conflates conditioning modality with additional fine-tuning**: The paper's headline claim (Abstract, Sec. 5.1) that SG2IM models "outperform their original prompt-only counterparts" is supported by Table 2, where T2I baselines (SDXL, SD3.5-Medium, FLUX.1-Dev) are evaluated as off-the-shelf checkpoints with zero fine-tuning on LAION-Comp, while the SG2IM models undergo additional training on 480K LAION-Comp image-SG pairs. This confound means the observed SG-IoU improvements (e.g., SDXL: 0.371→SDXL-SG: 0.558) could be partially or fully driven by additional training on curated, high-aesthetic-quality images, independent of whether the conditioning is a scene graph or a caption. **The paper's core contribution—dataset quality—is not undermined by this confound**, because the cross-dataset comparison (SDXL-SG on COCO vs VG vs LAION-Comp) is a clean experiment that holds training status constant. However, the specific claim about structural vs. textual conditioning cannot be evaluated from the presented evidence. The paper acknowledges this issue obliquely ("Fine-tuning pre-trained T2I models inevitably increases FID") but does not run the necessary control: fine-tuning the text-only baselines on the same LAION-Comp images with their original captions.

### Minor

- **Human verification protocol lacks essential detail in the main text**: The paper reports "high accuracies of 98.8% for objects, 97.5% for attributes, and 95.7% for relations" from "partial human verification" (Sec. 3.1) but does not state the sample size, sampling strategy (random, stratified, or otherwise), inter-annotator agreement, or specific criteria used for judging correctness. These are deferred to sec. A.5. For a dataset contribution where annotation quality is foundational, this information should be summarized in the main paper.

- **SG-IoU/Entity-IoU/Relation-IoU computation is not explained in the main text**: The paper describes these as measuring "the overlap between the generated images and the real annotations in terms of scene graphs, objects, and relations" (Sec. 3.3) and cites Shen et al. (2024). However, computing IoU between a generated image and a ground-truth scene graph requires either parsing the generated image back into a graph (which would conflate generation quality with predictor quality) or human annotation of generated images. The procedure's validity is central to the paper's quantitative conclusions, and the main text should provide enough detail for the reader to assess it, rather than fully deferring to Sec. A.2.

- **No statistical uncertainty reported**: All results in Tables 2, 3, and 4 are point estimates without standard deviations, confidence intervals, or significance tests. Generative model outputs are inherently stochastic, and it is unclear whether reported differences (e.g., SG-IoU differences of 0.01–0.03 between variants) are meaningful or within evaluation noise.

- **Editing framework listed as a co-equal contribution but absent from the main text**: Contribution (2) in the introduction describes an "SG-based image editing framework," but all discussion is deferred to Sec. A.1 with "Due to space limitation." If this is a primary contribution, it deserves main-text space; if secondary, it should not be listed alongside the dataset and benchmark as co-equal.

### Trivial
None.

## Nice-to-Haves

- Fine-tuning text-only counterparts (SDXL, SD3.5, FLUX) on LAION-Comp images with their original captions, to enable a clean comparison that isolates whether SG conditioning provides benefits beyond additional training on curated data.
- Comparison against layout-conditioned baselines (e.g., GLIGEN with bounding boxes) to situate scene graphs vs. spatial layouts as conditioning modalities.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Proper nouns like 'John Singer Sargent' carry rich visual information—they are not noise"** (Harsh Critic): This is a matter of interpretation. The paper's framing that proper nouns offer "limited guidance during model training" is defensible for the stated goal of structural, compositional annotations. Removed as opinion, not weakness.
- **"FID contradiction (SD3.5-SG has better FID than SD3.5-Medium contradicts claim that fine-tuning increases FID)"** (Harsh Critic): The paper says fine-tuning "typically" elevates FID—not universally—and compares different base architectures (SDXL vs SD3.5) evaluated in different contexts (Table 2 vs Table 3 use different test sets). Removed as misreading.
- **"The editing framework is not discussed in the main text"** (partial removal): Retained as a Minor weakness above, but the harsh critic's stronger framing ("should not be listed as co-equal contribution") is removed as excessive. Deferring secondary content to the appendix is standard practice.
- **Various speculative reproducibility and format criticisms**: Removed per hard rules (appendix-stripping artifacts, parser errors, questioning existence of cited systems).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run the controlled experiment**: Fine-tune SDXL, SD3.5, and FLUX on LAION-Comp images using only their original captions, then compare to the SG-conditioned variants. This is the single highest-leverage improvement—it would either cleanly validate the structural-conditioning claim or bound its magnitude.
2. Report the human verification sample size, sampling strategy, and inter-annotator agreement in the main text.
3. Briefly explain in the main text how SG-IoU/Entity-IoU/Relation-IoU are computed from generated images (e.g., whether a scene graph predictor is used, and if so, which one).
4. Report confidence intervals or standard deviations across multiple inference seeds for the main quantitative results.

## Score and Decision

The paper makes a useful dataset contribution (540K high-aesthetic images with diverse, detailed scene graph annotations) that is validated by a clean cross-dataset comparison (same model, different training data) and a well-designed ablation study (data proportion with constant iterations). The four-backbone generalization and the analysis of non-spatial relation diversity provide additional support. However, the headline claim about SG conditioning outperforming text conditioning is confounded by asymmetric fine-tuning, and several important experimental details (human verification protocol, SG metric computation) are deferred to the appendix. The paper is a solid borderline-to-accept: the dataset resource is real and useful, but the paper's strongest stated claim needs better support.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>