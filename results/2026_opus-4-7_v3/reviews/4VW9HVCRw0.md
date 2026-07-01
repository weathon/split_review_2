Now let me verify specific claims from the reviewer more carefully by re-reading key sections.Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me run Round 1 calibration search — bracketing across score bands:Let me read the most relevant calibration anchors to compare. The HOI-Diff paper (score 5.25) is the closest topically.Now I have enough calibration data. Let me finalize the review.

**Round 1 Bracket Analysis:**

Key anchors from most to least relevant:
- **HOI-Diff** (ZYwLfi50GI, avg 5.25, Reject): Text-driven 3D HOI synthesis with diffusion and contact. Very close topical match. Rejected for limited baselines, missing comparisons, and coarse contact modeling. TOUCH is stronger: has a novel dataset pipeline, finer contact modeling, more thorough ablations (9 variants vs limited).
- **ViTaM-D** (J4D5WVoc5g, avg 4.50, Reject): HOI reconstruction with tactile sensing and new dataset. Rejected for poor presentation and missing ablations. TOUCH is clearly stronger.
- **Interactive-Action Image Gen** (OWIk5E4lJs, avg 5.20, Reject): Synthetic dataset + diffusion pipeline. Similar dataset+method structure; rejected.
- **DICE** (rfrtFwnF62, avg 6.00, Accept): Hand-face interaction, limited novelty but solid execution. Accepted at 6,6,6.
- **Ready-to-React** (mm0cqJ2O3f, avg 7.00, Accept): Online interaction generation, stronger evaluation. Accepted.

**Initial bracket: 5.0–6.5.** TOUCH is clearly stronger than HOI-Diff (5.25) due to the dataset contribution and better ablations, but has evaluation gaps (self-referential, limited baselines) that DICE (6.0) doesn't have as much.

Now let me write the final review:## Summary
This paper introduces Free-Form HOI Generation, a task that extends hand-object interaction synthesis beyond grasping to diverse actions (pushing, poking, rotating). It contributes WildO2, a 4.4k-sample in-the-wild 3D HOI dataset built from internet videos via a novel O2HOI frame-pairing pipeline, and TOUCH, a three-stage framework combining contact map prediction CVAEs, multi-level conditioned diffusion, and physics-based refinement for text-guided HOI generation. Experiments on WildO2 show improvements over two adapted baselines across contact accuracy, physical plausibility, diversity, and semantic consistency metrics.

## Strengths

- **Practical dataset construction pipeline.** The O2HOI frame-pairing strategy (Sec. 3.1) — extracting an unoccluded object frame and an interaction frame from the same video, then using dense feature matching (Edstedt et al., 2024) for mask transfer — is an elegant, scalable solution to the occlusion problem in in-the-wild HOI reconstruction. It avoids both the geometric inconsistencies of diffusion-based inpainting and the cost of manual completion. This design is a standalone contribution with value beyond this specific paper.

- **Well-validated contact guidance.** The ablation in Table 2 demonstrates that removing contact guidance ("✗ hoc.") drops P-IoU from 0.728 to 0.492, a dramatic degradation confirming that explicit contact maps are a critical intermediate representation for constraining the high-DoF free-form interaction space. The paper also thoughtfully notes that penetration metrics can be misleading without contact (Sec. 5.3: the "✗ refiner" variant has deceptively low PD/PV because the hand drifts away entirely).

- **Multi-level conditioning design validated by ablation.** The coarse-to-fine injection (Eqs. 4–5), where early Transformer blocks receive SSC/global geometry and later blocks receive DSC/local contact features, is supported by a clear ablation: flattening this hierarchy ("✗ mul.") drops P-IoU from 0.728 to 0.525 (Table 2). The text encoder comparison (Sec. 5.4.1) further validates the Qwen-7B choice over CLIP, BERT, and MPNet alternatives.

- **Emergent force-semantics association.** The finding in Sec. 5.4.3 and Fig. 9 — that the model implicitly associates "firmly" with larger/denser contacts and "gently" with sparser/marginal contacts, with a quantified 22–25% contact area difference — demonstrates genuine implicit semantic controllability beyond what was explicitly supervised. This is a concrete, specific, and interesting emergent property.

## Weaknesses

### Fatal
None

### Major

- **All quantitative evaluation is self-referential to WildO2.** Since TOUCH introduces both the dataset and the method, all metrics in Table 1 are computed against the paper's own pseudo-ground-truth, which is produced by its own reconstruction pipeline (single-image 3D reconstruction + monocular hand estimation, Sec. 3.2). The paper does not quantify the accuracy of this reconstruction against any measured 3D ground truth, nor does it include any cross-dataset evaluation. This means readers cannot disentangle whether the improvements come from the method or from the dataset being inherently well-matched to TOUCH's architecture. The 55% survival rate of the initial 8k clips (Fig. 3a) further suggests that the surviving samples may be biased toward "easy" interactions where reconstruction succeeds. This does not invalidate the contribution, but it substantially limits confidence in the quantitative results.

- **Limited baseline comparison with ambiguous fairness.** Only two baselines appear in Table 1: ContactGen and Text2HOI, both originally designed for grasping and adapted to this new setting. Text2HOI is explicitly re-implemented ("we remove its temporal axis and adapt it for our setting," Sec. 5.2). Both are augmented with "an optimization-based post-processing module to correct hand poses," but the paper does not specify whether this module is identical to TOUCH's refiner (Sec. 4.3) or a simpler alternative. If simpler, the comparison advantages TOUCH at the architectural level rather than the core generation design. While limited baselines are partly justified by the novelty of the task, the sparse comparison makes it difficult to isolate the sources of improvement.

- **Tension between dynamic-action framing and static output.** The paper's central motivation emphasizes "pushing, poking, and rotating" — inherently temporal actions — yet the method generates only static hand poses. The paper acknowledges this in Sec. 6 ("Our framework currently focuses on static HOI snapshots, which inherently limits its ability to capture the temporal dynamics"). However, the abstract and introduction frame this as generating these actions without qualifying the static limitation upfront, creating a mismatch between what is promised and what is delivered. A static "push" is geometrically similar to a finger touching an object; the contact-geometry diversity the method achieves is real and valuable, but the action-level diversity claim is oversold.

### Minor

- **DSC input is a structured template, not natural language.** Inspection of Figs. 5, 8, and 9 reveals that DSCs uniformly follow the pattern "Apply [hand contact parts] to [verb] the [object contact part] of [object category]…" This is a structured specification, not the free-form natural language suggested by "text-guided." The gap between what a user would naturally say ("tip the bottle over") and the required DSC format is undiscussed. The SSCs are more natural but less informative.

- **Out-of-domain generalization is anecdotal.** Sec. 5.4.2 and Fig. 7 show only four qualitative examples on Objaverse objects, with no quantitative metrics. This makes the generalization claim unsubstantiated beyond visual plausibility.

- **User study is underdescribed.** The perceptual score (PS) from 10 users (Sec. 5.1) lacks protocol details: what participants were shown, scoring criteria, whether comparisons were paired or independent, and inter-rater agreement. This limits its evidentiary weight.

### Trivial
None

## Nice-to-Haves
- Variance/confidence intervals across multiple diffusion sampling runs on the 677-sample test set
- Quantitative cross-dataset evaluation on external HOI benchmarks (e.g., GRAB or OakInk objects) to validate generalization
- An unconditional diffusion baseline on WildO2 to further isolate conditioning design from dataset effects
- A failure-case analysis showing where TOUCH breaks down across the 92 intents
- Validation of the reconstruction pipeline on a small set of interactions where external 3D ground truth exists (e.g., from GRAB)

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Physically plausible" overclaim in abstract:** The paper's justification for not using physics-engine stability metrics is reasonable — force closure doesn't apply to non-grasping interactions (Sec. 5.1). Using penetration depth/volume is standard in HOI generation. Removing this as an inflated concern.

- **Canonical hand point cloud limitation (Sec. 4.1):** Using zero-pose MANO for contact CVAE is a reasonable engineering simplification that doesn't threaten core claims. Mentioned in the review as trivial observation but not weighted.

- **Missing variance/CI reporting:** While technically valid, single-run evaluation is standard practice in 3D HOI generation papers. Moved to nice-to-have rather than weakness.

## Novel Insights
The decomposition of free-form HOI generation into explicit contact-map prediction followed by contact-conditioned pose synthesis, validated by the large ablation gap (P-IoU drop of ~0.24 without contact guidance), suggests that explicit contact modeling may serve as a generally useful inductive bias for non-grasping manipulation — a finding that extends beyond this specific architecture. The emergent force-semantics association, where the model learns to vary contact density based on force-related language without explicit force supervision, points to an interesting property of joint text-geometry training that could inform other embodied generation tasks.

## Suggestions
- **Reframe the contribution around contact-geometry diversity rather than action diversity.** The static output genuinely achieves diverse spatial hand-object contact configurations conditioned on fine-grained specifications. This is what the method actually does well, and it is valuable as a building block for downstream dynamic systems. The current framing oversells actions and undersells contact geometry.
- **Validate reconstruction pipeline on external 3D GT.** Running the pipeline on a small set of interactions from GRAB or HO-3D where measured 3D data exists would calibrate the reliability of WildO2's pseudo-GT and strengthen all downstream metrics.
- **Specify the baseline post-processing module.** State explicitly whether the optimization applied to ContactGen and Text2HOI is identical to TOUCH's refiner, and if not, describe the differences.
- **Describe the user study protocol** including presentation format, scoring rubric, and inter-rater agreement.

## Score and Decision

### Calibration Anchors (all from Round 1)

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| HOI-Diff | ZYwLfi50GI | 5.25 | R1 | Most topically similar (text-driven 3D HOI with diffusion+contact). TOUCH is stronger: better dataset pipeline, finer contact modeling, more thorough ablations. |
| Interactive-Action Image Gen | OWIk5E4lJs | 5.20 | R1 | Similar dataset+method structure with synthetic priors; rejected for evaluation concerns. TOUCH has a more complete method but similar evaluation limitations. |
| ViTaM-D (HOI reconstruction) | J4D5WVoc5g | 4.50 | R1 | HOI reconstruction with tactile sensing and new dataset; rejected for poor presentation and ablation. TOUCH is clearly stronger in both contribution and execution. |
| GUNet (pose diffusion) | KWo4w1UXs8 | 3.00 | R1 | Pose skeleton generation with diffusion; rejected for limited contribution. TOUCH has substantially more novelty. |
| SyGRID (synthetic dataset) | U6UPhLBTcv | 3.00 | R1 | Synthetic industrial dataset; rejected for marginal contribution. TOUCH's dataset pipeline is more novel. |
| Pseudo-tactile grasping | xcHIiZr3DT | 2.50 | R1 | Very weak paper; TOUCH is incomparably stronger. |
| InterDance | KfkmwYQXWh | 5.60 | R1 | Dance generation with dataset+diffusion; rejected at 5.60. Similar dataset+method combination but TOUCH has more novel task definition. |
| DICE (hand-face) | rfrtFwnF62 | 6.00 | R1 | Accepted with limited novelty but solid execution. TOUCH has more novelty but weaker evaluation. Roughly comparable. |
| Ready-to-React | mm0cqJ2O3f | 7.00 | R1 | Online interaction generation with stronger evaluation. TOUCH is below this level. |
| Sin3DM | U0IOMStUQ8 | 6.00 | R1 | Single 3D shape diffusion; accepted. Different domain but similar novelty level. |
| Gaussian diffusion rendering | rWIrdAo2xC | 2.83 | R1 | Novel view synthesis with direct Gaussian diffusion; rejected. Less relevant. |

**Round 1 bracket: 5.0–6.5**

TOUCH is clearly above HOI-Diff (5.25) and the reject-band papers due to its genuine new task, practical dataset pipeline, and thorough ablations. However, it falls short of DICE's (6.00, Accept) evaluation solidity due to its self-referential evaluation, limited baselines, and framing-delivery mismatch. The paper sits at the borderline: strong contributions (new task, creative dataset pipeline, validated method design) offset by evaluation gaps (no cross-dataset validation, only 2 adapted baselines, pseudo-GT concerns) and oversold framing (dynamic actions from static output, "text-guided" with template input).

The contributions are real and the method design is sound, but the evaluation does not provide sufficient evidence to be confident the method works as well as the numbers suggest. This places the paper in borderline territory, leaning toward accept given the novelty of the task and dataset contributions.

**Final score: 6.0** — The novel task definition, practical dataset pipeline, and well-ablated method represent genuine contributions to the field. The evaluation gaps are real but addressable, and the core ideas are sound. This merits borderline acceptance.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>