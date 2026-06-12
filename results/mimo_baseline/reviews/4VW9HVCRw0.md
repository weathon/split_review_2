## Summary
This paper introduces the task of Free-Form HOI Generation, which extends hand-object interaction synthesis beyond grasp-centric paradigms to include diverse non-grasping interactions (pushing, poking, rotating, etc.). The authors construct WildO2, an in-the-wild 3D HOI dataset with 4.4k samples across 92 intents and 610 object categories via an automated pipeline from internet videos, and propose TOUCH, a three-stage framework combining contact map prediction, multi-level conditioned diffusion, and physical constraint refinement.

## Strengths
- **Well-motivated new task definition**: The paper convincingly argues that existing HOI generation methods are confined to grasp-centric paradigms with strong inductive biases toward force-closure grasps. The Free-Form HOI Generation task is clearly defined and addresses a genuine gap in the literature. The example interactions (pushing, poking, tipping, rotating) are compelling and practically relevant for AR/VR and robotics.

- **Clever data pipeline with O2HOI frame pairing**: The strategy of pairing object-only frames (unoccluded) with interaction frames from SS-V2 is innovative, enabling mask transfer via dense matching to avoid the geometric inconsistencies of diffusion-based inpainting. This is more scalable than manual completion and produces reasonable 3D reconstructions with a semi-automated approach.

- **Multi-level coarse-to-fine conditioning design**: The hierarchical injection strategy—global context (SSC + global geometry) in early diffusion stages and local details (DSC + contact features) in later stages—is well-motivated by the observation that interaction generation benefits from establishing overall pose before refining contact details. The ablation (Tab. 2) confirms that removing multi-level conditioning ("✗ mul.") causes substantial degradation across all metrics.

- **Thorough ablation study**: The ablations systematically validate each component's contribution (contact maps, refiner, cycle-consistency loss, multi-level structure, text levels, text encoders). The authors make a particularly insightful observation that penetration metrics (PD, PV) are misleading without contact—exemplified by the "✗ refiner" variant having low PD/PV simply because the hand drifts away from the object entirely.

- **Multi-level annotation system**: The combination of template-based SSCs, VLM-generated DSCs, fine-grained 17-part hand segmentation, and dense contact maps provides rich supervision signals. The force semantics analysis (Fig. 9) showing that "firm" prompts yield 22-25% larger contact areas is a nice emergent finding.

## Weaknesses
### Fatal
None.

### Major
- **Limited and potentially unfair baseline comparisons**: Only two baselines are compared—ContactGen (designed for grasp generation with coarse hand parts) and Text2HOI (adapted by removing its temporal axis). Both are fundamentally designed for different tasks and augmented with post-processing to handle pose drift. This makes the comparison somewhat apples-to-oranges. Ideally, the authors should compare against more recent methods like Zhang et al. (2025a;b) mentioned in the introduction, or other diffusion-based grasp generation methods adapted to this setting.

- **Small human evaluation**: The perceptual score (PS) uses only 10 users, which is too few to draw reliable conclusions about semantic consistency. The VLM-assisted evaluation protocol is also not fully described, making it difficult to assess its reliability.

- **Modest dataset scale relative to claims**: While 4.4k samples across 92 intents and 610 categories demonstrates impressive diversity in *types* of interactions, the absolute scale is small for training generative models. The pipeline's 55% success rate (with 31% failing due to pose estimation) further highlights scalability concerns. The paper calls it "large-scale" but 4.4k samples is quite limited compared to modern 3D datasets.

### Minor
- **Static snapshots only**: The framework generates single-pose snapshots rather than interaction sequences, which limits its applicability for dynamic tasks. The authors acknowledge this but it remains a significant limitation for robotics and embodied AI applications.

- **Contact map quality dependence on text parsing**: The hand branch generates a canonical point cloud with a hand-part mask initialized from fine-grained text (T_DSC), which requires reliable parsing of hand part mentions. The robustness of this parsing is not analyzed.

- **Physical plausibility constraints are lightweight**: Despite the paper's emphasis on physical plausibility, the constraints rely on penetration depth/volume and ICP losses rather than physics simulation. The authors justify not using stability simulation because interactions extend beyond grasps, but some form of physics validation (e.g., checking if pushing actually displaces an object) would strengthen claims of physical realism.

### Trivial
None.

## Nice-to-Haves
- A comparison with more diverse baselines, including recent methods that use LLM-based semantic guidance for HOI
- Larger-scale human evaluation (e.g., 50+ participants) with inter-annotator agreement statistics
- Analysis of failure modes—what types of interactions does the method struggle with?
- Quantitative analysis of diversity beyond entropy and cluster size, e.g., coverage of the 92 intent categories

## Novel Insights
The paper's most novel insight is the observation that contact relationships, rather than grasping priors, provide the right abstraction for constraining the high-dimensional free-form interaction space. By decoupling contact prediction from pose generation, the framework can explore diverse interaction modalities (dorsal contact, fingertip pressing, knuckle tipping) that are inaccessible to grasp-centric approaches. The cycle-consistency regularization between hand and object contact surfaces is also a genuinely novel contribution for enforcing bidirectional mapping consistency in HOI generation, reducing ambiguity in the contact space.

## Suggestions
- Expand the comparison with additional baselines, particularly recent text-conditioned generation methods
- Report results with larger-scale human evaluation and establish reliability metrics
- Provide per-intent-category analysis to understand which interaction types are well-captured and which remain challenging
- Consider adding a physics-based validation step (even if not used as a training signal) to verify that generated interactions are physically meaningful (e.g., a "push" should involve correct force direction)

## Score and Decision
The paper makes a valuable contribution by defining a new task, building a dataset with a clever automated pipeline, and developing a complete framework with well-designed components. The multi-level conditioning, contact-guided generation, and cycle-consistency refinement are technically sound and well-ablated. However, the limited baseline comparisons, small human evaluation, and modest dataset scale (relative to claims) prevent a stronger recommendation. The work is a solid foundation for the free-form HOI generation direction but would benefit from stronger experimental validation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>