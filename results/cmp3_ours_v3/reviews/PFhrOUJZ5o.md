Now let me finalize the review with calibration.

**Calibration Analysis:**

**Round 1 Bracket:** Score range 5.0–7.0

**Anchor papers used for calibration:**
1. **SG-Adapter** (KCYDpqSpqg, avg 5.50, Reject) — Directly related (SG-guided generation). Small dataset (309 images), limited experiments. The current paper is substantially stronger (540K images, scaling ablation, multi-backbone). But the current paper shares some evaluation framing issues.
2. **MedTrinity-25M** (IwgmgidYPS, avg 6.00, Accept) — Large-scale multimodal dataset paper. Had real data quality concerns (85% annotation accuracy) but was accepted for its scale and value. The current paper has a similar profile (valuable large-scale dataset + some limitations).
3. **Davidsonian Scene Graph** (ITq4ZRUT4a, avg 6.00, Accept) — Evaluation benchmark paper. Strong contribution but focused on evaluation, not data scaling.
4. **LivingThings/KG CLIP** (hQY03s8rOm, avg 5.33, Reject) — Automated dataset construction for CLIP. Domain-specific, smaller scale. Rejected partly due to limited scope.

**Comparison reasoning:** The LAION-Comp paper is stronger than SG-Adapter (5.5, Reject) because it provides a dataset that is three orders of magnitude larger and a more thorough scaling analysis. It is comparable to MedTrinity-25M (6.0, Accept) in terms of contribution type (large-scale dataset + models + benchmark), though MedTrinity had better score consistency (all 6s). The current paper's weaknesses (framing emphasis, modest gains, missing details) are more about presentation than fundamental flaws, making it stronger than the rejected LivingThings-KG paper (5.33) but not quite at the level of the cleanest accept papers.

**Final Score: 6.0 (Borderline Accept)**

---

## Summary

This paper introduces LAION-Comp, a large-scale dataset of ~540K images with scene graph (SG) annotations built on LAION-Aesthetics V2 (6.5+), a suite of SG-conditioned generation models using a GNN-based SG encoder integrated into diffusion and flow-matching backbones (SD1.5, SDXL, SD3.5, FLUX), and CompSGen Bench, a benchmark of 20,838 complex-scene samples (≥4 relations) for evaluating compositional generation. The central thesis is that large-scale, high-quality SG annotations improve compositional generation over both text-only conditioning and existing SG datasets.

## Strengths

- **Large-scale open-vocabulary SG dataset.** LAION-Comp provides 540K SG-annotated images, ~4–5× the scale of Visual Genome (~108K). The distribution analysis (Fig. 4, Table 1 in the paper) shows the most frequent relation accounts for only 3.78% of all relations and the top attribute only 7.36%, supporting the claim of open-vocabulary coverage.

- **Clear scaling evidence.** The ablation study (Table 4) is the paper's strongest experiment. Training SDXL-SG on 10% → 20% → 50% → 100% of LAION-Comp with constant iterations shows monotonic improvement across FID, SG-IoU, Ent-IoU, and Rel-IoU. This directly supports the thesis that more SG training data improves compositional generation.

- **Multi-backbone validation across four architectures.** The SG encoder is demonstrated on SD1.5, SDXL, SD3.5 (diffusion), and FLUX (flow matching), showing the approach generalizes beyond a single architecture.

## Weaknesses

### Major

- **Framing overemphasizes the T2I-vs-SG2IM comparison.** The paper foregrounds the result that SG2IM models outperform T2I models on SG metrics (abstract: "outperform their original prompt-only counterparts"). This comparison conflates input modality with dataset quality — a T2I model never receives structured object/relation information, so lower SG-IoU is expected and has been the stated motivation for the work. The fair comparison (SG2IM trained on LAION-Comp vs. SG2IM trained on COCO/VG) shows genuine but modest gains: e.g., SDXL-SG SG-IoU improves from 0.546 (VG) to 0.558 (LAION-Comp), or ~2.2% relative; SG-Adapter from 0.515 to 0.538 (~4.5%). These improvements are real, and the scaling ablation confirms that data scale matters, but the narrative inflates the headline result by emphasizing the unsurprising T2I gap. (Applies to Abstract, Sec. 5.1, Table 2.)

### Minor

- **FID narrative inconsistency.** The paper states "fine-tuning pre-trained T2I models inevitably increases FID scores" (Sec. 5.1, citing prior work). SDXL → SDXL-SG (19.3 → 20.1) is consistent with this, but FLUX.1-Dev → FLUX-SG (26.2 → 24.7) shows FID *improvement*, contradicting the claimed inevitability. This contradiction is not addressed.

- **Human verification sample size unreported in main text.** The paper reports accuracies of 98.8% (objects), 97.5% (attributes), and 95.7% (relations) from "partial human verification" (Sec. 3.1), deferring details to Sec. A.5 (stripped appendix). Without knowing whether the sample was 100, 500, or 2000 images, these numbers are difficult to interpret. The error bars at these levels (e.g., ~±3% for n=100) are material to the claimed precision.

- **SG-IoU metrics depend on an external detection pipeline not described in the main paper.** The three accuracy metrics (SG-IoU, Entity-IoU, Relation-IoU) are computed by detecting objects and relations in generated images using a pipeline cited to Shen et al. (2024). The paper does not describe this detector, its accuracy, or whether it might favor certain generation styles. The scores reflect joint generation+detection quality. Consistent use across methods mitigates this for relative comparisons, but the paper does not confirm this in the main text.

- **"First to propose a compositional generation benchmark based on scene graphs" overstates novelty.** Existing SG2IM evaluation protocols on COCO and VG have been used for years. CompSGen Bench's novelty is in its scale and focus on complex scenes (≥4 relations), which is a genuine contribution — but claiming to be "first" is inaccurate and should be qualified.

- **Missing variance estimates.** No error bars or confidence intervals are reported on any metric in Tables 2, 3, or 4, which is below ICLR standards for empirical work.

### Trivial

- **"CLIP score" is defined as image-image similarity** (Sec 3.3: "similarity between the generated and ground truth images"), which is a non-standard use of the term. Standard CLIP score measures image-text alignment; the paper's usage should be clarified or renamed.

## Nice-to-Haves

- A discussion of failure cases in the GPT-4o annotation pipeline (e.g., hallucinated objects, missed relations, inconsistent annotations) and their downstream effects.
- OOD evaluation on prompts not derived from LAION-Aesthetics test images, to test generalization beyond the training distribution.
- Comparison with other structured conditioning approaches (e.g., layout-to-image like GLIGEN) under comparable data scales, if the claim is about the value of "structure" broadly.

## Removed Points (with justifications)

- "FID comparison across modalities is invalid because T2I and SG2IM use different inputs" — FID is a distributional distance metric comparing generated and real image distributions; comparing FIDs across conditioning modalities is standard practice. **REMOVED (factually incorrect).**
- "FID computed against LAION images may not reflect OOD generalization" — generic criticism applicable to most FID evaluations. **REMOVED.**
- "No comparison to non-SG structured methods (GLIGEN, etc.)" — scope creep; the paper is specifically about scene graphs. **REMOVED.**
- "Editing contribution not in main paper" — the paper explicitly points to Sec. A.1 for editing; the appendix is stripped by the PDF parser and was present in the original submission. **REMOVED.**
- "Failure cases not discussed" — not a core weakness. **MOVED to Nice-to-Haves.**
- "CLIP score measures wrong thing" — the paper clearly defines it as image-image similarity; the critic assumed standard image-text CLIP. **REMOVED (misreading).**
- Section-by-section editorial observations that are not concrete weaknesses (e.g., "The description is brief but sufficient", "The discussion of SG2IM is thorough"). **REMOVED.**
- "The paper does not engage substantively with the concurrent work (Chen et al., 2024b)" — this is about a contemporaneous effort mentioned only briefly; the paper cannot be penalized for limited discussion of a work cited in passing. **REMOVED.**

## Novel Insights

The most compelling finding is the scaling relationship in Table 4: SG-IoU improves monotonically (0.530 → 0.558 for SDXL-SG) as LAION-Comp training data increases from 10% to 100% at constant iterations, establishing that data quantity and quality in SG annotations directly drive compositional generation performance. This is the paper's cleanest causal evidence. Additionally, the relation-type distribution analysis (77.48% non-spatial in LAION-Comp vs. 41.98% in VG) provides a useful diagnostic showing that LAION-Comp captures richer, more functional semantics than prior SG datasets.

## Suggestions

1. **Re-frame the evaluation to lead with the within-SG2IM comparison** (LAION-Comp vs. COCO vs. VG) as the primary result. Move the T2I comparison to a secondary role or clearly identify it as an expected baseline rather than a novel finding.
2. **Report the human verification sample size** in the main paper, and ideally provide accuracy broken down by scene complexity (e.g., ≤5 objects vs. >10 objects).
3. **Add error bars or variance estimates** (multiple runs) to all quantitative tables.
4. **Qualify the "first" claim** to "first large-scale benchmark specifically designed for complex scene generation from scene graphs."
5. **Resolve the FID inconsistency**: either revise the "inevitably increases FID" claim or explain why FLUX-SG improves over its T2I counterpart.
6. **Clarify the CLIP score definition** or rename the metric to avoid confusion with the standard image-text CLIP score.

---

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>