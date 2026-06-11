## Summary
# Final Review Report

## Summary

This paper addresses the task of controllable hand-object interaction (HOI) generation, moving beyond the grasp-centric paradigm that dominates existing work. The authors introduce **Free-Form HOI Generation**, targeting diverse non-grasping interactions (pushing, poking, rotating) conditioned on fine-grained textual intent. Three contributions are presented: (1) **WildO2**, the first in-the-wild 3D HOI dataset with 4.4k interactions across 92 intents and 610 object categories, sourced from internet videos via an automated O2HOI frame-pairing and reconstruction pipeline; (2) **TOUCH**, a three-stage framework combining contact-map-predicting CVAEs, a Transformer-based DDPM with coarse-to-fine conditioning, and a cycle-consistency refinement module; (3) quantitative results on WildO2 showing improvements over adapted baselines (ContactGen, Text2HOI) in contact accuracy, physical plausibility, diversity, and semantic consistency.

**Strengths:** The task formulation (free-form HOI beyond grasping) addresses a genuine gap in the literature. The O2HOI mask transfer strategy using reference frames is an elegant solution to the occlusion problem in 3D reconstruction from video. The coarse-to-fine conditioning design for the diffusion model is technically sound, and the cycle-consistency loss for contact refinement is a novel self-supervised contribution.

**Weaknesses:** Several aspects require attention: (1) The text-to-hand-part-mask conversion in the CVAE is underspecified, harming reproducibility. (2) The evaluation metrics (diversity entropy, VLM score, perceptual score) lack full methodological specification — what distribution entropy is computed over, which VLM and prompt protocol is used, and variance/confidence intervals for perceptual scores are missing. (3) The cycle-consistency loss relies on a nearest-neighbor bijectivity assumption that may break down for large-area contacts (e.g., palm); this limitation is not discussed, and λ_cycle is not ablated. (4) The camera alignment in the dataset pipeline uses a hard IoU threshold to switch optimization phases, risking instability. (5) The conclusion overclaims by stating "addressed the limitations" when the work is better described as "took a step toward addressing." (6) Novelty/comparison conclusions are deferred to manual verification due to external literature search being unavailable in this run.

**Score rationale:** The paper has a clear, well-motivated task formulation, a technically competent method design, and reasonable experimental validation. The main weaknesses are in specification completeness, metric rigor, and boundary-condition analysis rather than fundamental flaws. The dataset contribution (WildO2) is likely to be a useful resource for the community. The score reflects solid technical work with room for improvement in reproducibility and evaluation rigor.

**Final Score: 7/10**

> **Note:** This review was produced under Retrieval-Disabled Mode. Novelty and comparison conclusions relative to external literature are intentionally deferred and should be verified manually by the authors or by a reviewer with access to paper search. No external citations are used in this report.

## Strengths
1. **Well-motivated task formulation.** The paper identifies a genuine limitation of existing HOI generation — the pervasive grasp-centric bias — and defines a clear, actionable alternative: free-form HOI generation with fine-grained textual control. This re-framing is timely and could influence future research directions in human-scene interaction synthesis.

2. **Elegant dataset construction strategy.** The O2HOI frame-pairing approach (object-only reference frame + interaction frame) is a practical and scalable solution to the occlusion challenge in 3D HOI reconstruction from video. Mask transfer via dense matching avoids the geometric inconsistency of inpainting-based methods and is more scalable than manual completion. The resulting WildO2 dataset, with its multi-level annotations (SSCs, DSCs, 17-part hand segmentation, contact maps), is a valuable resource for the community.

3. **Technically sound method architecture.** The three-stage design (contact prediction → multi-level conditioned diffusion → physical refinement) is coherent and each stage addresses a specific sub-problem. The coarse-to-fine conditioning in the Transformer DDPM — where global features and coarse text (SSCs) guide early denoising and local features with fine text (DSCs) refine later stages — is a principled approach for semantic-to-geometric alignment. The cycle-consistency loss for contact refinement is a novel self-supervised contribution.

4. **Comprehensive quantitative evaluation.** The paper evaluates from four perspectives (contact accuracy, physical plausibility, diversity, semantic consistency) with multiple metrics per perspective. The ablation study is thorough, covering component removal (hoc., refiner, multi-level), text encoder ablation (CLIP, BERT, MPNet vs Qwen-7B), and multi-level text ablation (SSC-only, DSC-only).

5. **Out-of-domain generalization demonstration.** The experiments on Objaverse CAD models (Sec. 5.4.2) and the controllable semantic generation results (Sec. 5.4.3) suggest that the method generalizes beyond the Something-Something V2 distribution, which is an encouraging sign of practical applicability.

6. **Clear and well-structured presentation.** The paper is clearly written, with good use of figures (framework overview, dataset statistics, qualitative comparisons) and a logical flow from motivation to method to experiments.

## Weaknesses
### W1 — Reproducibility-critical underspecification in the text-to-hand-part-mask conversion (Major)
*Page 1 — Section 4.1 (Contact Map Prediction)*

The CVAE for hand contact maps takes "a hand-part mask initialized from the fine-grained text T_DSC" as input, but the mechanism for converting natural language (e.g., "Apply thumb pad") to a 778-vertex binary mask on the MANO hand model is not described. This is a core component of the semantic-to-geometric pipeline — without it, the entire conditioning chain from language to contact is a black box. The paper does not state whether this conversion uses keyword matching, an LLM parser, a learned projection, or a fixed lookup table. This gap directly compromises reproducibility.

**Required action:** Specify the exact conversion mechanism (e.g., "we maintain a hand-part-to-vertex mapping table; each of the 17 hand parts is assigned a set of vertex indices on the MANO template; the DSC text is parsed via a rule-based keyword extractor that maps recognized part names to their vertex sets, producing a binary mask over the 778 vertices"). If this information is in the appendix, the main text should provide a clear pointer.

### W2 — Evaluation metric specification lacks methodological detail (Major)
*Page 7 — Section 5.1 (Experimental Settings)*

Three of the four evaluation axes have incomplete methodological specification:

(a) **Diversity (Entropy, Cluster Size):** The paper reports "Ent↑" and "CS↑" but does not specify what distribution the entropy is computed over, the clustering algorithm used, the number of clusters, or the distance metric. Without these details, the diversity numbers are not interpretable or reproducible.

(b) **VLM-assisted evaluation:** The paper reports VLM scores (4.8, 6.5, 7.1) but does not state which VLM is used (Qwen-VL? GPT-4V? CLIP-based?), the evaluation protocol (classification accuracy into 92 intents? pairwise preference? Likert rating?), or the prompt template. A score of 10/10 is not defined, making cross-paper comparison impossible.

(c) **Perceptual Score (PS):** The score from 10 users (e.g., 8.8 for Ours) is reported without variance, confidence intervals, or inter-annotator agreement. With only 10 users, the mean is highly sensitive to individual ratings. A 95% bootstrap CI or Fleiss' kappa should be reported.

**Required action:** Add a paragraph (or appendix section) specifying: (1) clustering algorithm, feature space, distance metric, and number of clusters for diversity; (2) VLM name, exact prompt template, scoring rubric, and whether the VLM sees the rendered 3D scene or 2D projection; (3) perceptual score distribution (box plot or histogram) per method and a measure of inter-annotator agreement.

### W3 — Cycle-consistency loss assumption and hyperparameter not analyzed (Major)
*Page 6 — Section 4.3 (Physical Constraints Refinement)*

The cycle-consistency loss L_cycle enforces bidirectional nearest-neighbor mapping consistency between hand and object contact surfaces. This design implicitly assumes that the nearest-neighbor correspondences (Φ: hand→object, Ψ: object→hand) are approximately bijective. For large-area contacts such as palm-on-flat-surface, many hand points map to the same object region, violating bijectivity. The resulting loss may incorrectly penalize realistic contact patterns. The paper neither discusses this limitation nor reports the weighting hyperparameter λ_cycle (Eq. 7). The ablation table (Table 2) does not include a "✗ L_cycle" variant, so the standalone contribution of the cycle loss to the final performance is unknown.

**Required action:** (a) Add a "✗ L_cycle" row to Table 2; (b) report λ_cycle value and validate with a sweep (λ_cycle ∈ {0, 0.01, 0.1, 1.0}); (c) discuss the bijectivity assumption limitation and propose a fallback (e.g., one-sided Chamfer loss for large-area contact regions).

### W4 — Camera alignment optimization uses a hard threshold that may cause instability (Moderate)
*Page 3 — Section 3.2 (Data Reconstruction Pipeline, Stage 2)*

The camera alignment loss (Eq. 1) switches from coarse phase (L_mask + L_sinkhorn + L_edge) to fine phase (+ λ_fine(L_depth + L_rgb)) based on an IoU threshold. This discrete switch creates a discontinuity in the loss landscape: the optimizer may have converged under one objective and then the sudden addition of two new terms (depth + RGB) can cause divergence. The threshold value and a robustness analysis (does the final alignment quality depend heavily on this threshold?) are not reported.

**Required action:** Replace the hard threshold with a smooth annealing schedule (e.g., λ_fine = min(1, max(0, (IoU - τ_low)/(τ_high - τ_low)))), and report the chosen thresholds or validate that results are stable across a range of threshold values.

### W5 — Conclusion overclaims and limitations are vague (Moderate)
*Page 9 — Section 6 (Conclusion)*

The first sentence, "we addressed the limitations of grasp-centric approaches," overstates the contribution — the paper introduces a new task, dataset, and method, but does not claim to have fully solved all limitations of grasp-centric HOI. A more measured opening such as "we took a step toward addressing" would align better with the evidence presented. Additionally, the limitations paragraph mentions dataset scale as "an area for future growth" without quantifying what scale would be needed. Stating "4.4k samples is modest for training pose diffusion models; scaling to 10k+ would improve generalization" would be more actionable.

**Required action:** Rewrite the conclusion opening sentence to use measured language ("took a step toward addressing") and replace the vague dataset-scale limitation with a quantified target.

### W6 — Ablation interpretation could be strengthened (Minor)
*Page 8 — Section 5.3 (Ablation Study)*

The ablation "✗ mul." (removing multi-level structure) shows a dramatic P-IoU drop from 0.728 to 0.525 (28% relative decrease). The paper attributes this to "the multi-level network structure" but does not explain what the ablated model looks like — is it a single-level conditioning variant where all 8 blocks receive only global features? Or a variant without cross-attention to local features? Without a precise description, the reader cannot interpret what architectural factor causes the large drop.

**Required action:** Add a one-sentence description of the "✗ mul." variant (e.g., "removes the hierarchical conditioning by applying only global conditions uniformly across all 8 Transformer blocks and removing all cross-attention to local features").

### W7 — Related work organization lacks analytical depth (Minor)
*Page 2 — Section 2 (Related Work)*

The three related-work subsections read as structured literature summaries rather than critical analyses with explicit gap identification. Section 2.3 traces the evolution from grasp-type control to part-level contact but does not articulate a *progressive gap* at each level that the current paper addresses. The transition sentence "Building on these efforts, we propose..." is too generic and does not specify which limitation is overcome.

**Required action:** Add one sentence per subsection explicitly stating the residual gap that WildO2/TOUCH fills, e.g., "However, all these methods are trained on grasping-only data; our WildO2 dataset and TOUCH framework extend this line of work to non-grasping interactions."

### Deferred Novelty and Comparison Verdict

Due to external literature search being unavailable in this run (Retrieval-Disabled Mode), the following aspects are explicitly deferred for manual verification:

- Whether "Free-Form HOI Generation" as a named task overlaps with prior task formulations in concurrent or earlier work (e.g., activity-conditioned grasp synthesis, functional HOI generation).
- Whether the O2HOI mask transfer strategy (reference frame → interaction frame via dense matching) has been used in prior HOI reconstruction pipelines.
- The relative position of WildO2 against other in-the-wild 3D HOI datasets that may have been released concurrently (e.g., OakInk extensions, HOLD, or other video-to-3D datasets).
- Whether the cycle-consistency loss design is novel or has precedents in the 3D contact optimization literature.

Authors should conduct a thorough literature comparison and discuss the relationship to the closest existing works in their revision.

### Page Coverage Audit

| Page | Annotation Count | Coverage Status |
|------|-----------------|----------------|
| Page 1 (Abstract + Introduction + Related Work + Dataset + Method + Experiments + Conclusion) | 14 | Covered (all substantive paragraphs annotated) |
| Appendix (not available in extract) | 0 | Skipped — appendix content not provided in paper markdown |

All substantive paragraphs in Abstract, Introduction (3 paragraphs), Related Work (3 subsections), Method (3 subsections), Experiments (settings, comparisons, ablation, discussion), and Conclusion are covered by at least one annotation.

## Score
**Final Score: 7/10**

**Scoring rationale (evidence-grounded, prioritizing research value and novelty):**

This paper addresses a well-motivated and timely problem — moving HOI generation beyond grasp-centric interactions. The task formulation is clear, the dataset (WildO2) fills a genuine gap, and the technical framework (TOUCH) is competently designed with several novel components (O2HOI mask transfer, coarse-to-fine conditioning, cycle-consistency loss). The experimental evaluation covers multiple dimensions and includes informative ablations.

The score is constrained to 7/10 rather than higher due to the following:
- **Reproducibility gaps** (W1, W2): Several core components (text-to-mask conversion, metric definitions) are underspecified, meaning the paper cannot be reproduced from the main text alone without significant guessing.
- **Missing boundary-condition analysis** (W3): The cycle-consistency loss, a central contribution, has an unexamined assumption (nearest-neighbor bijectivity) and an unablated hyperparameter (λ_cycle).
- **Metric rigor** (W2): The lack of variance reporting for perceptual scores and underspecified VLM protocol weakens confidence in the reported rankings.
- **Deferred novelty verification**: Without external literature search, the novelty claims (first free-form HOI dataset, first text-guided non-grasping generation) cannot be independently verified.

These weaknesses are fixable with additional specifications, ablations, and analysis — they are not fundamental flaws. If the authors address the reproducibility gaps, analyze the cycle-consistency limitation, and complete a thorough literature comparison, the paper could be suitable for acceptance at a venue like CVPR/ICCV.

**Research value assessment:**
- New knowledge: Moderate. The task re-framing and dataset are novel; the method design is competent but builds on established techniques (CVAEs, DDPMs, FiLM conditioning).
- Reproducibility/reusability: The WildO2 dataset is a reusable resource. Reproducibility of the method is currently limited by specification gaps.
- Potential to change practice/understanding: If the dataset is released and the pipeline is open-sourced, this could shift HOI generation research toward broader interaction modeling.

> **Final Score: 7/10**