## Summary
This paper introduces the task of Free-Form Hand-Object Interaction (HOI) generation, moving beyond the traditional grasp-centric paradigm to generate diverse interactions including non-grasping actions like pushing, poking, and rotating. The authors propose TOUCH, a three-stage framework based on multi-level diffusion with contact prediction and physical refinement, and construct WildO2, a large-scale in-the-wild 3D HOI dataset with 4.4k interactions across 92 intents and 610 object categories with detailed semantic annotations built from internet videos.

## Strengths
- **Novel problem formulation**: The paper identifies and addresses a genuine limitation in HOI generation research—the grasp-centric bias—and formulates the Free-Form HOI generation task. This is a meaningful extension of the problem space with clear practical relevance to AR/VR and robotics.
- **Significant dataset contribution**: WildO2 is the first large-scale 3D dataset covering non-grasping daily interactions, built through an automated O2HOI frame pairing strategy. The multi-level annotation system (SSCs, DSCs, 17-part hand segmentation, contact maps) is comprehensive and well-designed, providing over 44k annotations. The scale (4.4k interactions, 92 intents, 610 object categories) represents a meaningful resource for the community.
- **Strong empirical results**: The method consistently outperforms adapted baselines (ContactGen, Text2HOI) across all metrics in Table 1 (e.g., P-IoU 0.776 vs. 0.711/0.620, MPVPE 2.97 vs. 4.69/5.46). The ablation study is thorough and the discussion of why penetration metrics can be misleading without established contact is insightful.
- **Out-of-domain generalization demonstrated**: The evaluation on Objaverse CAD models (Fig. 7) convincingly shows that the method generalizes beyond the training distribution, including to verbs outside the primary annotated intents.

## Weaknesses
### Fatal
None.

### Major
- **Limited evaluation against concurrent work on semantic HOI generation**: While the authors note that existing methods focus on grasps, there are relevant recent approaches for semantic/action-conditioned HOI generation (e.g., Yang et al. 2024a;b; Yu et al. 2025 cited in related work). The paper does not compare against these methods that explore task/intent-level constraints, which weakens the claim of being the first to move beyond grasping. Either these should be adapted as baselines, or a clearer justification for why they cannot be compared should be provided.
- **The multi-level diffusion architecture is insufficiently novel**: The coarse-to-fine conditioning in a transformer-based DDPM (Eq. 4-5) is a straightforward application of existing techniques (FiLM, cross-attention, hierarchical conditioning) that have been well-explored in image and motion generation. The paper does not demonstrate that this specific design is superior to simpler alternatives (e.g., a single-level diffusion with the same conditioning), beyond the ablation in Table 2 which removes multiple components simultaneously.
- **Contact map prediction evaluation is missing**: The paper evaluates the final HOI generation but does not separately evaluate the quality of the predicted contact maps (Section 4.1). Since contact prediction is claimed to be a key enabler for free-form generation, the ablation in Table 2 ("w/o hoc.") confounds removal of both hand and object contact map guidance. A direct evaluation of contact prediction accuracy (against ground-truth contact maps in WildO2) is needed.

### Minor
- **The physical constraints refinement (Section 4.3) uses test-time optimization (TTA)**, which introduces computational overhead at inference. The paper does not report runtime or discuss the practical implications of this design choice.
- **The VLM-based evaluation (VLM score in Table 1) is not clearly described**: Which VLM was used? What was the prompt? How were scores normalized? Without this information, the semantic consistency metric is difficult to interpret.
- **The dataset is derived from a single source (Something-Something V2)**: While this provides rich action annotations, the diversity of objects and interactions is inherited from this dataset's biases. The paper would benefit from discussing potential coverage gaps.
- **The text encoder ablation (Table 2) shows Qwen-7B outperforms CLIP/BERT/MPNet, but the differences are small** (e.g., P-IoU 0.728 vs 0.713/0.705/0.704). The claim of "better performance in capturing fine-grained semantic details" is overstated given these margins.

### Trivial
None.

## Nice-to-Haves
- A video or animation-based evaluation showing the progression through the three-stage pipeline for a few examples would help intuition.
- An analysis of failure cases (the 45% of reconstruction outcomes that were not "Success" in Fig. 3a) and how they might affect the generation model.
- Discussion of whether 4.4k samples is sufficient for the 92 intents × 610 object categories space (the intentional sparsity is a challenge).

## Novel Insights
The paper's most interesting insight is that explicit contact modeling (contact maps on both hand and object surfaces) serves as a more effective spatial prior than implicit grasping priors for free-form HOI. This is a principled shift: rather than constraining the hand to a predefined grasp taxonomy or force-closure conditions, contact maps leave the interaction space open while providing sufficient geometric guidance. The observation that "force-related semantics" (firm vs. gentle) can be learned purely from contact geometry without explicit force modeling is also genuinely interesting, suggesting that language encoders capture affordance-relevant features that translate well to interaction generation.

## Suggestions
- Add a direct evaluation of the contact map prediction module (Section 4.1) against ground-truth contact maps from WildO2, separate from the full generation pipeline. Report IoU/F1 for contact prediction alone.
- Compare against the most relevant task/intent-conditioned baselines (e.g., Yang et al. 2024a;b) or provide a clear justification for exclusion. If these methods are fundamentally grasp-centered, demonstrate this limitation empirically.
- Report the TTA inference time and discuss whether the refinement module could be trained to match TTA quality without at-test optimization.

## Score and Decision
The paper addresses a genuine gap in HOI generation, provides a substantial new dataset, and demonstrates strong empirical results. The weaknesses (limited baseline comparisons, insufficient ablation of the prediction module, limited architectural novelty) are major but not fatal—they can be addressed in revision. The contribution to the community is clear.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>