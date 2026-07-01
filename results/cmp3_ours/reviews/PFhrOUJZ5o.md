Now let me write the final merged review.

## Summary

This paper introduces LAION-Comp, a large-scale dataset of 540K+ aesthetic images annotated with structured scene graphs (objects, attributes, relations) via GPT-4o prompting with partial human verification. It also presents CompSGen Bench, a 20K-sample evaluation benchmark for complex scene generation, and demonstrates the dataset's utility by training four baseline models (SD1.5-SG, SDXL-SG, SD3.5-SG, FLUX-SG) with a GNN-based SG encoder. Experiments show that models trained on LAION-Comp outperform prompt-only counterparts and prior scene-graph-based methods on both the new benchmark and existing ones (COCO-Stuff, Visual Genome, T2I-CompBench).

## Strengths

- **Large-scale structured dataset addressing a genuine bottleneck.** The paper correctly identifies that existing text-image datasets lack explicit inter-object annotations, and prior work has focused on architectural patches while leaving the data-level issue unaddressed. LAION-Comp (540K SG-image pairs) is substantially larger than existing annotated SG datasets (COCO-Stuff, Visual Genome) and is built on high-quality LAION-Aesthetics V2 (6.5+) images. The decision to build on an existing high-quality image pool rather than curating from scratch is sensible.

- **Thoughtful annotation design with verified quality.** The GPT-4o prompt engineering shows genuine care: unique IDs for object disambiguation, requiring abstract adjectives (not object names) for attributes, using precise verbs rather than generic spatial relations, and avoiding anthropomorphism. Human verification reports high accuracies: 98.8% for objects, 97.5% for attributes, 95.7% for relations (Sec. A.5).

- **Ablation study provides clean evidence (Table 4).** Scaling from 10% to 100% of LAION-Comp monotonically improves SG-IoU (0.530 → 0.558) and Rel-IoU (0.837 → 0.856). Even at 10%, LAION-Comp outperforms training on the full Visual Genome dataset, demonstrating that annotation quality — not just scale — drives improvement.

- **Transfer evaluation partially addresses the in-distribution concern.** While CompSGen Bench shares its annotation pipeline with the training data, the paper also evaluates on COCO-Stuff and Visual Genome (Table 2), where models trained on LAION-Comp consistently outperform those trained on those datasets. This transfer evidence helps disentangle dataset quality from annotation-pipeline artifacts.

## Weaknesses

### Major

- **Evaluation confound: CompSGen Bench originates from the same annotation pipeline as the training data.** The benchmark's 20,838 test samples are drawn from the LAION-Comp test split and annotated by GPT-4o using the same prompt template used for training. The key metrics (SG-IoU, Entity-IoU, Relation-IoU) compare generated images against these GPT-4o annotations. This means the evaluation partially measures how well models reproduce a specific annotation style rather than how well they capture true compositional scene structure. The paper mitigates this by also evaluating on human-annotated COCO-Stuff and Visual Genome (Table 2), where models trained on LAION-Comp still win — but the gap between "trained and evaluated on LAION-Comp" vs. "trained on LAION-Comp, evaluated on human annotations" is never disentangled. A held-out human-annotated test set or an analysis correlating GPT-4o-based SG-IoU with human judgment would significantly strengthen the claims.

### Minor

- **The 216% object-count claim is not adequately explained and contains an internal inconsistency.** The paper states: "the average number of objects per sample is 5.33, with 38% of these being proper nouns" — implying ~3.30 non-proper-noun objects. However, Table 1 reports the "w/o Proper Noun" count as 2.02 ± 3.01 for LAION captions. The 216% figure = (6.39 − 2.02) / 2.02 relies on the 2.02 value, which is inconsistent with a 38% proper-noun rate (which would give 3.30). The paper should clarify the exact methodology for counting objects, identifying proper nouns, and computing this figure.

- **CLIP score is used in a non-standard way.** Section 3.3 states "the CLIP score calculates the similarity between the generated and ground truth images." Standard CLIP score in the T2I evaluation literature measures image-text alignment (between generated image and prompt). Using CLIP as an image-image similarity metric is not the field norm and conflates compositional accuracy with visual similarity to a specific reference image — there are infinitely many valid renderings of a scene graph that would not resemble the particular LAION reference. The paper should either switch to image-text CLIP score (with the scene graph as text) or explicitly justify the image-image variant. That said, this does not affect the paper's core claims, which rest on SG-IoU, Entity-IoU, and Relation-IoU.

- **Spatial vs. non-spatial categorization criteria are not specified.** The paper reports 77.48% non-spatial relations in LAION-Comp vs. 41.98% in VG, but the top relations include "surrounded by" (3.78%), "adjacent to" (3.1%), and "near" (2.09%) — all spatial or spatial-adjacent. Without stating the exact categorization methodology, the reader cannot verify whether the 77.48% figure is reasonable or inflated by how borderline relations were classified.

- **Attribute vocabulary contains suspicious artifacts.** In Figure 4(b), "female" (184,718) and "young" (184,718) have identical counts, suggesting either a data-processing artifact or that GPT-4o frequently outputs these as a paired default. Additionally, "women" (178,447) and "female" (184,718) both appear in the top 10, indicating inconsistent gender normalization. These should be acknowledged and explained.

- **Image editing contribution is foregrounded as a headline claim but only appears in the appendix.** The abstract and introduction prominently feature "fine-grained, object-level image editing" as a core capability enabled by structural annotations, yet the entire editing framework and results are in Sec. A.1. For a contribution listed in the paper's bullet points, the main paper should include at minimum some quantitative results or a clear figure. This is a presentational overreach.

### Trivial

- None beyond the reporting issues noted above.

## Nice-to-Haves

- Providing a few concrete examples of raw GPT-4o annotation output vs. human-corrected versions would make the dataset construction more transparent.
- An analysis of GPT-4o annotation failure modes (the kinds of errors in the remaining 1.2% / 2.5% / 4.3%) would be useful for dataset users.
- An ablation comparing the GNN-based SG encoder against a simpler baseline (e.g., concatenating CLIP text embeddings of each triple without a GNN) would clarify whether the architectural design matters or the dataset alone drives improvement.

## Removed Points

- **Method contribution is modest (from Harsh Critic):** The paper's primary contribution is the dataset, not the SG encoder. The paper lists models as a demonstration of dataset utility rather than claiming architectural novelty. This criticism reads as scope creep. Removed.
- **No sample images of annotations / No analysis of GPT-4o failure modes (from Harsh Critic):** These are suggestions, not weaknesses. Moved to Nice-to-Haves.
- **"4 baseline models" count padded (from Harsh Critic):** Applying one method to four backbones is standard practice for demonstrating generalizability. This is not a weakness.
- **FLUX baseline trained on LAION-Comp not reported (from Harsh Critic):** The comparison is between FLUX.1-Dev (pre-trained) and FLUX-SG (fine-tuned on LAION-Comp). The paper's framing is clear about what is being compared. This criticism misunderstands the experimental design.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface a perspective that the authors had overlooked or that reframes the contribution in a fundamentally different way.

## Suggestions

1. Obtain human-written scene graphs for a held-out subset of CompSGen Bench and report SG-IoU vs. these human annotations. At minimum, show that model rankings under GPT-4o annotations correlate with rankings under human annotations. This directly addresses the evaluation confound.
2. Clarify the 216% claim by providing a transparent breakdown of object counting, proper-noun identification, and the exact arithmetic.
3. Either replace the image-image CLIP score with standard image-text CLIP score or explicitly justify its use and cite precedent.
4. Acknowledge the "female"/"young" identical-count artifact and the "women"/"female" normalization issue in the dataset analysis.

## Score and Decision

**Round 1 bracket:** I estimate this paper sits between 5.5 and 7.5 after initial inspection.

**Calibration anchors retrieved across all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Visual Data-Type Understanding (WyEdX2R4er) | 8.00 | R1 | Stronger novel task definition and cleaner evaluation; less relevant topic |
| ISG-Bench (rDLgnYLM5b) | 7.20 | R1 | Similar benchmark+dataset contribution; comparable evaluation rigor |
| Demystifying CLIP Data (5BCFlnfE1g) | 6.75 | R2 | Similar emphasis on data over architecture; accepted despite limited novelty |
| TIPS (DaA0wAcTY7) | 6.50 | R2 | Data-focused paper with solid empirical evaluation |
| MOFI (QQYpgReSRk) | 6.25 | R2 | Large-scale dataset with noisy labels; accepted |
| Enhan. Comp. T2I with Seeds (5BSlakturs) | 7.33 | R2 | Stronger on clean evaluation; less focus on dataset contribution |
| Davidsonian SG (ITq4ZRUT4a) | 6.00 | R1 | Similar topic (scene graphs + T2I evaluation); accepted with noted limitations |
| CtrLoRA (3Gga05Jdmj) | 6.00 | R2 | Controllable generation paper with solid contribution; accepted |
| DreamBench++ (4GSOESJrk6) | 6.00 | R2 | Benchmark paper; accepted |
| Leveraging KG for CLIP (hQY03s8rOm) | 5.33 | R1 | Dataset paper with insufficient experiments; rejected |
| PixelProse (UwbX8KOZgK) | 4.20 | R1 | Large dataset with insufficient empirical validation; rejected |

**Narrowing:** Comparing against Demystifying CLIP Data (6.75) — that paper had limited novelty but a very clean experimental isolation of data effects. The LAION-Comp paper has a stronger dataset contribution and more thoughtful construction methodology, but weaker evaluation due to the annotation-pipeline confound. Against the 6.0–6.5 papers (Davidsonian SG at 6.0, CtrLoRA at 6.0, DreamBench++ at 6.0, MOFI at 6.25, TIPS at 6.50), LAION-Comp has a larger and more directly useful dataset contribution but also a more notable evaluation weakness. Overall, the paper sits between 6.0 and 7.0 — a genuine dataset contribution with evaluation limitations that prevent it from reaching the 7+ tier but are not fatal.

**Final score:** 6.5. The LAION-Comp dataset is a timely and well-executed resource that fills a real gap. The evaluation concerns are real but partially addressed by transfer experiments, and the ablation study provides clean evidence for the core thesis. The paper would be strengthened by addressing the evaluation confound and clarifying the reporting inconsistencies before camera-ready.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>