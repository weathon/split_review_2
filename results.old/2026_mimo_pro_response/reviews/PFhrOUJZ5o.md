## Summary

This paper introduces LAION-Comp, a large-scale (540K images) scene-graph dataset built on LAION-Aesthetics V2 with GPT-4o-generated structural annotations, along with CompSGen Bench (20,838 test samples) for evaluating compositional image generation. The authors train four baseline models (SDXL-SG, SD1.5-SG, SD3.5-SG, FLUX-SG) by integrating a GNN-based scene graph encoder into diffusion/flow-matching backbones, and argue that the lack of explicit structural annotations—rather than model architecture—is the primary bottleneck for compositional generation.

## Strengths

- **Substantial dataset contribution**: LAION-Comp provides 540,005 image–scene-graph pairs, significantly larger than existing SG datasets (COCO-Stuff, Visual Genome). Table 1 shows 216% more meaningful object information when excluding proper nouns, and the dataset contains 77.48% non-spatial relations vs. VG's 41.98% (Section 3.2), demonstrating richer semantic coverage beyond simple spatial configurations.

- **Consistent improvement across multiple architectures**: Tables 2 and 3 show that training on LAION-Comp improves compositional accuracy (SG-IoU, Entity-IoU, Relation-IoU) across SDXL (diffusion), SD3.5, and FLUX (flow matching) backbones. SDXL-SG trained on LAION-Comp achieves SG-IoU of 0.558 vs. 0.546 on VG and 0.497 on COCO (Table 2). This cross-architecture consistency supports the data-centric thesis.

- **Informative ablation on data scaling**: Table 4 shows SDXL-SG improves monotonically from 10% to 100% of LAION-Comp across all metrics. Even at 10% (~48K samples), SDXL-SG outperforms models trained on full VG in Entity-IoU (0.874 vs. 0.800), supporting annotation quality as a key factor beyond mere dataset size.

- **Well-motivated problem framing**: The thesis that compositional generation suffers primarily from a data problem rather than purely an architectural one is compelling and distinguishes this work from prior architectural approaches. The same SG2IM model consistently benefits from LAION-Comp training across three datasets (Table 2), supporting the claim.

## Weaknesses

### Fatal

None

### Major

- **Distributional confound in evaluation weakens the central claim**: The test set (both the 50K test split and CompSGen Bench) is drawn from LAION-Aesthetics, the same image distribution as the training data. When SG2IM baselines (SGDiff, SG-Adapter) trained on COCO or VG are tested on this benchmark, two confounds are inseparable: (a) LAION-Comp may provide better annotations, and (b) test images match LAION-Aesthetics's style/content but are out-of-distribution for COCO/VG-trained models. The paper partially mitigates by comparing the same model across three training datasets (Table 2), showing LAION-Comp wins within each model family. However, a cross-dataset evaluation (testing on COCO or VG) would disentangle these factors and substantially strengthen the central claim.

- **FID degradation is obscured by misleading framing**: Across Tables 2 and 3, every SG-finetuned model shows worse FID than its base T2I counterpart: SDXL 19.3→20.1 (Table 2), SDXL 25.2→26.7 (Table 3). The paper acknowledges this on lines 281–282 ("Fine-tuning pre-trained T2I models inevitably increases FID scores") but then claims on lines 285–286 that "our baseline achieves the best performance among all candidates in both image quality and accuracy" and on line 308 that it "outperforms existing models in terms of image quality." The abstract also claims models "outperform their original prompt-only counterparts" without qualification. These claims are misleading—compositional accuracy improves but FID worsens. The paper should honestly frame this as a tradeoff.

- **Core evaluation metrics are opaque in the main text**: The three accuracy metrics (SG-IoU, Entity-IoU, Relation-IoU) are the backbone of the evaluation, yet their computation is never described in the main text—they are attributed to Shen et al. (2024) with details deferred to Appendix A.2. These metrics presumably require running an object detector and relation classifier on generated images, and their reliability depends entirely on that pipeline's quality. The "+" variants in Table 1 vs. non-plus variants in Tables 2–4 add further confusion. For a paper whose central thesis rests on these metrics, more transparency in the main text is needed.

### Minor

- **No limitations section**: The paper has no discussion of limitations. Key unacknowledged limitations include: reliance on GPT-4o for annotation (proprietary, potentially biased), the FID-accuracy tradeoff, and the evaluation distributional confound. For a dataset paper, honest accounting of limitations is important.

- **Ablation design confound**: Table 4 uses constant total training iterations across data proportions, meaning smaller subsets receive more epochs. The paper states this is "for fairness" but it could actually benefit smaller datasets through more passes, partially confounding the scaling interpretation.

- **Benchmark design choices under-justified**: The ">4 relations" threshold for CompSGen Bench (line 191) is not motivated. Why is 4 the right cutoff for "complex"? This choice determines which 20,838 of 50,000 test samples are included.

### Trivial

None

## Nice-to-Haves

- Cross-dataset evaluation on COCO/VG test sets to disentangle annotation quality from image distribution.
- Ablation isolating the GNN component (e.g., SG with simple MLP vs. SG with GNN) to show structural processing matters beyond simple concatenation.
- Brief description in main text of how scene graphs are extracted from generated images for computing accuracy metrics.
- Bringing human verification details (sample size, methodology) from Appendix A.5 into the main text.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Cherry-picked qualitative examples (Figure 5, 4 examples)**: Standard practice for qualitative comparisons in image generation papers; not a substantive criticism.
- **Missing related works**: Cannot verify existence of claimed missing works without external sources.
- **Reproducibility concerns about GPT-4o**: The paper cites GPT-4o and it exists per our rules.
- **Appendix-deferred content**: The paper explicitly defers editing framework, detailed metrics, and verification details to appendix due to space. The parser strips appendices; they exist in the original submission.
- **Formatting artifacts**: All are parser issues, not paper problems.
- **CLIP score marginal difference (0.005)**: Mentioned only in passing; not a central claim.

## Novel Insights

The paper's core thesis—that the bottleneck for compositional generation is data quality (lack of structural annotations) rather than model architecture—is genuinely valuable and supported by the cross-architecture consistency of results. The finding that even 10% of LAION-Comp outperforms full VG training on Entity-IoU (Table 4 vs. Table 2) provides concrete evidence that annotation quality matters as much as or more than quantity, which is a useful insight for the community. The analysis showing LAION-Comp has 77.48% non-spatial relations vs. VG's 41.98% also highlights that existing datasets have been spatially biased.

## Suggestions

1. **Add cross-dataset evaluation**: Train on LAION-Comp but test on COCO/VG test sets. If results still favor LAION-Comp, the data-quality claim becomes much stronger.
2. **Reframe FID results honestly**: State that structural conditioning improves compositional accuracy at a small cost to FID, which is an acceptable tradeoff for the target use case.
3. **Add a brief description in the main text** of the evaluation pipeline (how scene graphs are extracted from generated images to compute SG-IoU etc.).
4. **Add a limitations section** acknowledging the distributional confound, GPT-4o dependency, and FID tradeoff.

---

## Calibration Report

**All retrieved anchors across rounds:**

| Anchor Paper | Avg Human Score | Round | Comparison |
|---|---|---|---|
| u1cQYxRI1H (IC-Light) | 0.50 | R1 | Unrelated topic; irrelevant anchor |
| 5lUdTogEL3 (Clothing-Irrelevant L-ReID) | 1.00 | R1 | Completely different domain |
| gwZ90hFSL2 (Humanoid Robots NLP) | 1.00 | R1 | Unrelated |
| 8QTpYC4smR (LLM Systematic Review) | 1.00 | R1 | Unrelated survey |
| V73W8MXnNW (Progressive Visual Relationship) | 3.00 | R1 | Related topic (visual relationships) but weaker contribution |
| TCSaLeANpN (SYNBUILD-3D) | 3.00 | R1 | Dataset paper, rejected; our paper has stronger downstream evaluation |
| TJHB4ySVZM (Data Extrapolation for T2I) | 3.40 | R1 | T2I data paper, rejected; our paper has larger contribution |
| ZVOGMy8Sd8 (Knowledge Enhanced Captioning) | 3.00 | R1 | Different domain |
| hQY03s8rOm (Leveraging Knowledge Graphs for CLIP) | 5.33 | R1 | Dataset construction, rejected for limited scope; our paper is broader |
| dZsjj4vQjl (Multi-Grained Concept Annotations) | 4.50 | R1 | Annotation dataset, rejected; our paper has more comprehensive evaluation |
| UwbX8KOZgK (PixelProse) | 4.20 | R1 | Large dataset paper, rejected for insufficient downstream experiments; our paper is stronger |
| M4J8OtcqT0 (Strategy-centric Synthesis) | 3.80 | R1 | Dataset construction, rejected |
| ITq4ZRUT4a (Davidsonian Scene Graph) | 6.00 | R1 | Scene graph + T2I evaluation, accepted; our paper has bigger dataset but more evaluation issues |
| 5BCFlnfE1g (Demystifying CLIP Data) | 6.75 | R1 | Data curation, accepted; comparable contribution scope |
| hss35aoQ1Y (InstructDET) | 5.75 | R1 | Data-centric method, accepted |
| GcJE0HPy4X (Automatic Dataset Construction) | 6.00 | R1 | Dataset construction, rejected despite avg 6.0 |
| WyEdX2R4er (Visual Data-Type Understanding) | 8.00 | R1 | Different topic |
| 07yvxWDSla (Synthetic Continued Pretraining) | 8.00 | R1 | Different topic |
| SctfBCLmWo (Decade's Battle on Dataset Bias) | 8.00 | R1 | Different topic |
| 3i13Gev2hV (Compositional Entailment Learning) | 8.00 | R1 | Compositional VLM, different focus |
| KCYDpqSpqg (SG-Adapter) | 5.50 | R2 | Most directly comparable: SG adapter + small dataset, rejected. Our paper has ~10x larger dataset and multi-architecture evaluation |
| ITq4ZRUT4a (Davidsonian Scene Graph) | 6.00 | R2 | Already listed above |
| xLPakPOKDX (Causally Motivated Diffusion) | 5.00 | R2 | Diffusion + bias paper, rejected |
| r6XqXoRT6N (PCIG: LLMs + Knowledge Graphs) | 4.20 | R2 | T2I + knowledge graphs, rejected |
| TWnUgSAWNw (Revisit Image-Caption Data) | 6.00 | R2 | Dataset contribution for multimodal models, accepted |
| CjPt1AC6w0 (Synthetic Data for Transfer Learning) | 6.25 | R2 | Synthetic data paper, rejected |
| jZsN9zo8Qi (Interleaved Image-Text) | 6.50 | R2 | VLM dataset + benchmark, accepted |
| TMYxJIcdgS (What Makes ImageNet Unlike LAION) | 5.25 | R2 | Dataset analysis, rejected |
| 5BSlakturs (Reliable Random Seeds for Compositional T2I) | 7.33 | R2 | Compositional T2I, accepted with strong scores |
| 0NruoU6s5Z (CompoDiff) | 5.25 | R2 | Composed image retrieval + dataset |
| gBHZAAwcgT (ComboStoc) | 5.40 | R2 | Diffusion combinatorial paper |
| 4w99NAikOE (IterComp) | 6.80 | R2 | Compositional T2I, accepted |

**Round 1 bracket: 5.5–6.5.** The paper is clearly stronger than SG-Adapter (5.50, rejected) due to ~10x larger dataset and comprehensive multi-architecture evaluation. It's comparable to Davidsonian Scene Graph (6.00, accepted) and Revisit Large-Scale Image-Caption Data (6.00, accepted) in contribution scope. It's below IterComp (6.80, accepted) and Enhancing Compositional T2I with Reliable Random Seeds (7.33, accepted), which are cleaner methods contributions with fewer evaluation concerns.

**Narrowing to final score: 6.0.** The paper has a genuine and substantial dataset contribution, cross-architecture consistency, and a well-motivated problem framing. The evaluation confounds (distributional, FID framing) and metric opacity are real but not fatal—they weaken the evidence for the stronger claims without invalidating the core contribution. A 6.0 places it alongside comparable dataset/benchmark contributions that were accepted, with the understanding that the evaluation issues should be addressed in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>