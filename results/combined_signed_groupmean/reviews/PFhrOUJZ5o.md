Now let me compile the final review.

## Summary

This paper introduces LAION-Comp, a large-scale dataset of 540K+ aesthetic images with scene graph annotations (objects, attributes, relations) generated via GPT-4o with prompt engineering. The authors also propose CompSGen Bench (20,838 complex-scene test samples) and fine-tune four baseline models (SDXL-SG, SD3.5-SG, FLUX-SG, SD1.5-SG) with a GNN-based scene graph encoder. The main claims are that the dataset's structural annotations enable models to outperform their text-only counterparts and prior scene-graph-based methods.

## Strengths

- **The dataset construction pipeline is thoughtfully designed with specific, evidence-based constraints** (Sec. 3.1): unique object IDs, abstract adjective attributes (avoiding noun-as-attribute confusion), concrete verbs instead of spatial-only relations. These directly address known failure modes of prior SG datasets. The resulting statistics (77.48% non-spatial relations vs. VG's 58.02% spatial skew, line 187) confirm meaningful qualitative differences from existing resources.

- **The ablation study (Table 4) provides clean evidence that LAION-Comp benefits training.** Training SDXL-SG on 10%, 20%, 50%, and 100% of the dataset with constant iterations shows monotonic improvement across FID, SG-IoU, Ent-IoU, and Rel-IoU. This is the cleanest experiment in the paper and convincingly demonstrates the dataset's value as a training resource.

- **CompSGen Bench fills a gap in scene-graph-based compositional evaluation** with 20,838 samples (all having >4 relations). The unified evaluation framework allows comparing SG2IM models trained on different datasets (COCO, VG, LAION-Comp) on a common benchmark, which is a useful community resource.

- **The core thesis is well-motivated:** the paper identifies that compositional generation failures stem at least in part from lack of structured annotations in training data (Sec. 1, lines 15-17), and constructing a large-scale SG dataset is a worthwhile direction.

## Weaknesses

### Major

- **The evaluation confounds SG conditioning with fine-tuning, preventing attribution of gains to structural annotations.** In Table 3 (CompSGen Bench), the proposed models (SDXL-SG, etc.) are fine-tuned on the LAION-Comp training set, while baseline T2I models (SDXL, SD1.5) use their original pre-trained weights with no LAION-Comp exposure. In Table 3, SDXL achieves better FID (25.2 vs. 26.7) and CLIP (0.700 vs. 0.698) than SDXL-SG — the very "image quality and similarity to GT" metrics the paper claims to improve (line 308). The paper acknowledges FID inflation from fine-tuning (line 281-282) but does not run the controlled experiment needed to isolate the effect of SG conditioning: fine-tuning the same base model on the same LAION-Comp data with text-only conditioning vs. SG conditioning, evaluated on the same held-out test set. Without this, the paper cannot distinguish whether improvements on accuracy metrics (SG-IoU, Ent-IoU, Rel-IoU) come from the structural annotations specifically, or simply from additional fine-tuning on in-distribution data, the SG encoder architecture, or some combination.

- **FID values in Table 2 are computed against different reference distributions and are not directly comparable.** T2I models (SDXL, SD3.5, FLUX.1-Dev) are evaluated on a LAION test set, while SG2IM models trained on COCO/VG/LAION-Comp are each evaluated on their respective dataset's test set. The paper makes comparative claims across these rows (line 285: "our baseline achieves the best performance among all candidates in both image quality and accuracy") despite the reference distributions differing. The same issue affects the 10% LAION-Comp vs. VG comparison in the ablation discussion (line 314), where different test sets make FID and IoU values not directly comparable.

- **No controlled ablation isolating conditioning modality.** The ablation study (Table 4) varies only data proportion, keeping conditioning modality (SG) fixed. The paper presents no experiment comparing text-only fine-tuning vs. SG-conditioned fine-tuning on the same LAION-Comp data. This is the single experiment that would directly support the paper's central thesis that structural annotations — not just more/better fine-tuning data — drive the reported improvements.

### Minor

- **The human verification of annotation quality uses only 300 samples (Table 1, line 103) out of 540K (0.056%).** The paper reports 98.8% (objects), 97.5% (attributes), and 95.7% (relations) accuracy — unusually high numbers for a fully automated pipeline on web-crawled images — but does not state whether samples were randomly selected, report inter-annotator agreement, or characterize the error distribution. This limits confidence in the annotation quality claims.

- **The paper does not discuss annotation cost, failure modes, or systematic biases in the GPT-4o-based pipeline.** As a proprietary API, GPT-4o annotations cannot be exactly reproduced if the model is updated or deprecated. The paper also does not analyze what types of images (crowded scenes, abstract art, unusual object combinations) produce poor annotations, which limits users' ability to assess the dataset's limitations.

- **The claim "outperforms existing models in terms of image quality" (line 308) is inconsistent with Table 3 results**, where SDXL (25.2 FID, 0.700 CLIP) beats SDXL-SG (26.7 FID, 0.698 CLIP) on both FID and CLIP. While accuracy metrics (SG-IoU, Ent-IoU, Rel-IoU) favor SDXL-SG, the FID/CLIP direction undercuts the blanket "outperform" claim.

### Trivial

None.

## Nice-to-Haves

- Add a controlled experiment fine-tuning SDXL on LAION-Comp with text-only conditioning vs. SG conditioning to directly isolate the effect of structural annotations.
- When making cross-dataset FID comparisons, evaluate all models on a shared test set; alternatively, clearly state which comparisons are within-dataset and refrain from cross-dataset FID claims.
- Expand the human verification study with larger sample size, stratified sampling, and inter-annotator agreement reporting.
- Report annotation cost (GPT-4o API calls, compute budget) and provide failure case analysis for the annotation pipeline.

## Removed Points

These points were raised by a reviewer but are removed with justification:

- **Issue about CompSGen Bench having "circular dependency" because it uses LAION-Comp annotations as ground truth:** Removed. Using ground-truth annotations as evaluation targets is standard practice across all benchmark evaluations (COCO, VG, etc.). The paper also uses FID and CLIP alongside SG-IoU metrics, mitigating the concern.
- **"First benchmark" claim being debatable:** Removed per standard policy (cannot verify external related works without external sources).
- **Oversimplification of prior work (architecture vs. data):** Removed as a framing opinion that does not affect the paper's technical validity.
- **Attributes as separate nodes creating scalability concerns:** Removed as speculative without demonstrated evidence.
- **Baseline fairness for SGDiff (trained without bbox):** Removed — the paper transparently states this modification (line 280) and uses the official implementation.
- **Statistical significance / error bars:** Demoted to Nice-to-have; single-run evaluation is standard for large-scale generation benchmarks.

## Novel Insights

The harsh critic's central insight — that the evaluation does not isolate SG conditioning from fine-tuning, making the headline claims unsupported — is valid and well-articulated. The critic correctly identifies the missing controlled experiment (text-only fine-tuning vs. SG fine-tuning on LAION-Comp) as the one experiment that would directly support the paper's thesis. The critic's detailed analysis of Table 2's cross-distribution FID comparisons is also correct. However, the critic overstates the "circular dependency" concern about CompSGen Bench, which uses ground-truth annotations as evaluation targets — standard practice. The ablation study (Table 4) remains a clean and valuable experiment that the critic correctly identifies as the paper's strongest evidence.

## Suggestions

1. **Run the missing controlled experiment** before claiming that structural annotations drive improvement: fine-tune SDXL on LAION-Comp with text-only conditioning (using original captions) and compare with SG-conditioned fine-tuning on the same train/test split. This is the single most impactful step.
2. **Reframe the paper primarily as a dataset contribution** (which is well-supported by the ablation study and pipeline quality) and tone down claims that the experiments cannot support.
3. **When making cross-dataset comparisons**, restrict them to metrics that are invariant to test distribution (SG-IoU, Ent-IoU, Rel-IoU) and avoid cross-dataset FID comparisons unless all models are evaluated on a shared test set.
4. **Provide more rigorous annotation quality validation** with a larger, stratified human evaluation sample.

## Score and Decision

**Calibration analysis:** I compared this paper against four anchors retrieved from the calibration corpus. **(1) SYNBUILD-3D** (avg 3.00, scores 5/3/3/1) — a synthetic 3D dataset paper with no baselines; LAION-Comp is clearly stronger due to its baselines and ablations. **(2) Data Extrapolation for T2I** (avg 3.40, scores 3/3/3/5/3) — a data augmentation paper with limited novelty; LAION-Comp has a more concrete contribution. **(3) Knowledge Graphs for CLIP dataset** (avg 5.33, scores 5/6/5) — a dataset paper with loose quality controls; LAION-Comp has stronger pipeline documentation but also more severe evaluation issues (confounded setup, -10.00 impact). **(4) SG-Adapter** (avg 5.50, scores 6/6/5/5) — the most directly comparable paper (scene graph guidance + small dataset); it had similar evaluation concerns (small test set, insufficient experiments) but was rated higher; LAION-Comp has a much larger dataset and benchmark but its evaluation confound is more fundamental to the central claim.

**Round-1 bracket:** 3.5–5.5 based on comparison with SG-Adapter (5.50) and KG-CLIP (5.33) as upper anchors, and SYNBUILD-3D (3.00) and Data Extrapolation (3.40) as lower anchors.

**Round-2 narrowing:** SG-Adapter (5.50) received borderline-accept scores (6/6/5/5) despite a 309-image dataset, because its method experiments were cleaner. LAION-Comp has a much stronger dataset contribution but its central evaluation confound (impact -10.00 and -10.00 for the two related issues) is more severe than SG-Adapter's weaknesses. PixelProse (4.20, scores 5/3/5/3/5) — a 16M-caption recaptioning dataset — was rated lower due to insufficient experimental validation and limited novelty; LAION-Comp's dataset contribution is more novel (SG annotations vs. recaptioning) and has better ablations, but its evaluation issue is equally fundamental.

**Final placement:** Between PixelProse (4.20) and SG-Adapter (5.50). LAION-Comp's decisive evaluation weaknesses (-10.00, -10.00, -9.23 from the impact scorer) pull it below SG-Adapter, but its stronger dataset contribution and ablation study push it above PixelProse.

**Final score:** 4.5 — The dataset contribution (pipeline, scale, benchmark, ablation) is genuine and useful, but the evaluation does not support the paper's central causal claim that structural annotations specifically drive improvement over text-only conditioning. The paper would benefit from being reframed as a dataset paper with more carefully scoped claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>