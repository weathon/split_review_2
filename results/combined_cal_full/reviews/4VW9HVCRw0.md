## Summary

This paper tackles the grasp-centric bias of existing HOI generation research by introducing the task of **Free-Form HOI Generation** — producing controllable, diverse, and physically plausible hand-object interactions beyond stable grasps, including non-grasping actions like pushing, poking, rotating, and tipping. The authors contribute (1) **WildO2**, a dataset of 4.4k in-the-wild 3D HOI samples reconstructed from internet videos (92 intents, 610 object categories), built via a clever O2HOI frame-pairing strategy; and (2) **TOUCH**, a three-stage framework (contact-map CVAE prediction → multi-level conditioned diffusion → physical refinement) that enables fine-grained semantic control over hand pose generation.

## Strengths

- **The task formulation addresses a genuine limitation.** The paper correctly identifies that existing HOI generation is overwhelmingly grasp-centric and that non-grasping interactions (pushing, poking, tipping, rotating) are pervasive in daily life but absent from prior work. This is a meaningful expansion of the problem space (Sections 1, 2.3).

- **The O2HOI frame-pairing strategy for dataset construction is clever and practical.** Extracting object-only frames from the same video to obtain clean object masks, then transferring them to interaction frames via dense correspondence matching (Section 3.1), avoids both the geometric inconsistency of diffusion-based inpainting and the scalability limits of manual completion. The core insight — that video datasets provide natural "object-only" reference frames — is well exploited.

- **The coarse-to-fine conditioning architecture is well-motivated and ablated convincingly.** Injecting global context (SSCs, global geometry) in early diffusion stages and local detail (DSCs, contact-point features) in later stages (Section 4.2, Eq. 4–5) is principled. The ablation study (Table 2) provides direct evidence: removing multi-level structure drops P-IoU from 0.728 to 0.525.

- **The WildO2 dataset is a substantial resource.** 4.4k unique interactions across 92 intents and 610 object categories with multi-level annotations (SSCs, DSCs, contact maps, 17-part hand segmentation) supports a new research direction in free-form HOI generation.

## Weaknesses

### Major

- **Self-contained evaluation with no cross-benchmark validation.** Every quantitative result (Tables 1, 2) is computed on the WildO2 test set — the authors' own dataset. Both baselines (ContactGen, Text2HOI) are adapted and re-trained on WildO2. There is zero evaluation on any existing HOI benchmark (GRAB, OakInk, HO4D, etc.). While evaluating on a new dataset for a new task is legitimate, the paper claims "superiority" (Section 5.2, Conclusion) without demonstrating that TOUCH retains competitive performance on standard grasping tasks. The adapted baselines may be inherently disadvantaged on this data. Without a supplementary evaluation on an existing benchmark, the reader cannot determine whether TOUCH's design sacrifices grasp quality for free-form capability, or whether it simply performs well on the authors' own reconstruction pipeline's outputs.

- **No variance or reliability statistics reported.** Neither Table 1 nor Table 2 reports standard deviations, confidence intervals, or the number of independent runs for any metric. For diffusion-based generative models that are inherently stochastic, single-run results are not a meaningful basis for comparison. The user study uses "10 users" (PS metric in Table 1) with no inter-rater agreement, demographic information, or evaluation protocol described. The VLM-assisted evaluation is mentioned (Section 5.1) but not specified — which VLM, what prompt, what procedure? These details are essential for reproducibility.

- **Ground-truth evaluation data has uncharacterized noise.** The WildO2 reconstruction pipeline (Section 3.2) has a 55% success rate (Figure 3a). The 4,414 samples underwent "manual inspection and refinement" but the paper does not describe inspection criteria, rejection rate, or number of annotators. Contact maps are computed algorithmically (Section 3.3: "combining relative and absolute distance thresholds with bidirectional nearest-neighbor filtering"), not annotated by humans. The evaluation metrics (P-IoU, P-F1, MPVPE) all use these same algorithmically-derived contact maps and reconstructed meshes as ground truth. If the reconstruction or contact computation has systematic errors, the metrics will favor methods whose outputs happen to align with those systematic errors — a particular concern for MPVPE, which measures distance between predicted hand vertices and *reconstructed* ground-truth hand vertices.

### Minor

- **Several implementation details are underspecified:** (a) how the hand-part mask is initialized from fine-grained text **T**<sub>DSC</sub> (Section 4.1) — mapping free-form text to a 17-part hand mask is itself a nontrivial problem; (b) the IoU threshold for switching between coarse and fine camera alignment phases (Section 3.2); (c) the value of *N*<sub>tta</sub> iterations in test-time adaptation (Section 4.3); (d) sensitivity of results to the 10% conditional dropout rate.

- **No failure case analysis.** All visualizations show successful examples (Figures 5–9), with no analysis of failure modes, types of interactions or objects the method struggles with, or cases where generated poses are unrealistic. This limits understanding of the method's practical boundaries.

- **No inference speed, computational cost, or model size reported.** The three-stage pipeline (CVAE forward pass, diffusion denoising, test-time optimization) has practical cost implications that are not quantified.

### Trivial

None.

## Nice-to-Haves

- A dataset validation study comparing automatically reconstructed 3D samples against a small set of manually annotated or mocap-captured ground truth (even 50–100 samples) would provide an upper bound on reconstruction noise and strengthen confidence in the metrics.
- An ablation varying the 10% conditional dropout rate would clarify sensitivity to this hyperparameter.
- Reporting the text encoder ablation with the same variance statistics as the main results would strengthen the comparison.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Something-Something V2 filtering criteria not described"** — REMOVED: the paper states "details in Appendix" and the appendix was stripped by the parser; this is a parser artifact, not a paper deficiency.
2. **"P-FID gap for Text2HOI (15.72 vs 4.13) warrants scrutiny"** — REMOVED: this is an observation about baseline behavior, not a paper weakness; the gap likely reflects that Text2HOI had its temporal axis removed during adaptation.
3. **"Abstract overstates prior limitation without concrete examples"** — REMOVED: the paper cites specific references (Taheri et al., 2020; Zhang et al., 2025a;b) for the grasp-bias claim; the motivation is reasonably supported.
4. **"Refiner dependency concern (diffusion alone is poor)"** — REMOVED: the paper explicitly acknowledges this in Section 5.3 ("the hand drifts away") and explains this is by design — the refiner is intended to address known pose drift.
5. **"Text encoder differences are modest"** — REMOVED: noting Qwen-7B (0.728) slightly outperforms CLIP (0.713) is an observation about results, not a weakness.

## Novel Insights

The most insightful point across the reviews is the **evaluation-loop concern**: the paper's central comparative claim rests entirely on a self-contained evaluation where the method, baselines, task definition, dataset, and metrics are all controlled by the same authors. There is a more subtle second-order issue: the ground-truth data (reconstructed meshes and algorithmically computed contact maps) and the evaluation metrics share the same reconstruction pipeline. If the reconstruction has systematic biases (e.g., systematic misalignment, contact over/under-estimation), the metrics will favor methods whose outputs align with those biases. This goes beyond the standard "new dataset, no external benchmark" critique and questions whether the metrics measure what they claim to measure. Additionally, the 55% reconstruction success rate means the dataset represents only the easier half of interaction frames — the harder cases (with occlusion or complex geometry) are systematically excluded, and it is unclear how this affects the generalization claims.

## Suggestions

1. Add evaluation on at least one established HOI benchmark (GRAB or OakInk) using standard protocols, even if only for the grasping subset of interactions, to demonstrate that TOUCH retains competitive performance on standard tasks and that free-form capability does not come at a cost to grasp quality.
2. Report all quantitative results with standard deviations over at least 3 random seeds.
3. Specify the VLM used for evaluation, the prompt design, and the user study protocol (interface, instructions, inter-rater agreement).
4. Characterize the manual inspection process for WildO2: number of annotators, criteria, rejection rate.
5. Add a failure case analysis figure and discuss common failure modes.
6. Report inference runtime, number of denoising steps, and *N*<sub>tta</sub> value.
7. Specify the IoU threshold in camera alignment and the hand-part mask initialization procedure.

## Score and Decision

**Score calibration.** Round 1 bracketing used 6 topical queries across score bands. The two most relevant anchors were **HOI-Diff** (5.25, reject) — a text-driven HOI generation paper with a similar modular coarse-to-fine design, criticized for missing SOTA comparisons and lacking physical plausibility — and **3D Interacting Hands Diffusion Model** (5.50, reject) — a generative diffusion model for interacting hands, criticized for limited novelty and evaluation gaps. Both were rejected at ICLR. A higher-scored anchor, **Ready-to-React** (7.00, accept), also had an "only one dataset" weakness (-3.64) but scored higher due to extensive experiments and strong method novelty. My paper's task novelty is stronger than HOI-Diff (truly new task formulation vs. incremental modular design), and its weighted items show a comparable distribution: positive weights of +6.08 (coarse-to-fine ablation), +3.96 (O2HOI strategy), +3.29 (WildO2 dataset), +2.02 (task importance); negative weights of -7.95 (self-contained evaluation), -6.69 (no variance stats), -5.34 (uncharacterized GT noise). The dominant negative concern (self-contained evaluation) is heavier than HOI-Diff's missing-baseline concern (-5.56) but is fixable through additional experiments. The paper sits between these anchors — above HOI-Diff due to stronger task novelty and clearer ablation evidence, but below Ready-to-React due to the more severe evaluation gaps.

**Final score: 5.5. Decision: Reject.** The paper makes genuine contributions (new task formulation, clever data pipeline, well-ablated architecture), but the evaluation is not yet commensurate with the strength of the claims. The three major concerns — no cross-benchmark validation, no variance reporting, and uncharacterized ground-truth noise — collectively undermine confidence in the quantitative results and comparative claims. These are fixable through additional experiments, and I would encourage the authors to address them and resubmit.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>