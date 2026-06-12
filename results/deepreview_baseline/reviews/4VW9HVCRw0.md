## Summary
This paper introduces the task of Free-Form Hand-Object Interaction (HOI) generation, moving beyond traditional grasp-centric approaches to enable diverse interactions like pushing, poking, and rotating. The authors construct WildO2, a large-scale in-the-wild 3D HOI dataset with 4.4k interactions across 92 intents and 610 object categories, built from internet videos via an automated reconstruction pipeline. They propose TOUCH, a three-stage framework combining contact map prediction, multi-level conditioned diffusion, and physical constraints refinement to generate controllable, diverse, and physically plausible hand poses from fine-grained text prompts and object meshes.

## Strengths
- **Novel and well-motivated task formulation**: The paper convincingly identifies and addresses a genuine limitation in existing HOI generation research—the over-reliance on grasp-centric paradigms. The shift toward free-form interactions (non-grasping actions) is a meaningful and timely contribution that expands the scope of the field.
- **Substantial dataset contribution**: WildO2 is a significant resource, being the first large-scale in-the-wild 3D HOI dataset covering non-grasping interactions. The automated O2HOI frame pairing and reconstruction pipeline is clever and addresses the critical bottleneck of 3D data scarcity for diverse daily interactions. The multi-level annotation system (SSCs, DSCs, 17-part hand segmentation, contact maps) is thorough and well-designed.
- **Strong empirical results**: The method consistently outperforms adapted baselines (ContactGen, Text2HOI) across all four evaluation categories (contact accuracy, physical plausibility, diversity, semantic consistency) with substantial margins. The ablation study is comprehensive and clearly demonstrates the contribution of each component, with a particularly insightful discussion about why penetration metrics can be misleading without established contact.
- **Demonstrated generalization and controllability**: The out-of-domain experiments on Objaverse and the semantic controllability results (force-related semantics, diverse poses for the same object) provide compelling evidence that the method learns meaningful representations beyond memorization. The analysis of "firm" vs. "gentle" prompts showing 22-25% contact area differences is a particularly nice validation of semantic understanding.

## Weaknesses
### Fatal
None.

### Major
- **Limited evaluation of temporal dynamics despite framing**: The paper motivates the task using video-based interactions and constructs the dataset from video clips, yet the generation task is fundamentally static (single-frame HOI). While the authors acknowledge this as a limitation, the disconnect between the motivating examples (pushing, tipping, rotating—inherently dynamic actions) and the static output is significant. The evaluation metrics and comparisons are all for static poses, which raises questions about whether the generated poses would actually produce the described dynamic actions if animated.
- **Baseline adaptation concerns**: The baselines (ContactGen, Text2HOI) were designed for fundamentally different tasks (grasp generation with coarse control). While the authors attempt fair comparison by adding post-processing, the adapted baselines may be operating far outside their intended design space. The paper would benefit from a more detailed discussion of what modifications were made and whether the baselines' poor performance reflects genuine superiority of TOUCH or simply better task alignment.

### Minor
- **Dataset quality concerns**: The reconstruction pipeline shows only 55% success rate (Figure 3a), with 31% "Pore Estimation Failure" (likely a typo for "Pose Estimation Failure"). This means nearly half the attempted reconstructions failed, and the final 4,414 samples underwent manual inspection. The paper should discuss potential biases introduced by this filtering process—are certain types of interactions or objects systematically excluded?
- **Limited comparison to grasp-based methods**: While the paper correctly argues that grasp-based methods cannot handle free-form interactions, a quantitative comparison showing how TOUCH performs on traditional grasp tasks (e.g., on GRAB or OakInk datasets) would strengthen the claim that the method doesn't sacrifice grasp quality while gaining free-form capability.

### Trivial
- The paper uses "Pore Estimation Failure" in Figure 3a which appears to be a typo for "Pose Estimation Failure."

## Nice-to-Haves
- A user study with more participants (currently 10) and statistical significance testing would strengthen the perceptual score results.
- Analysis of failure cases in the generation model (not just the reconstruction pipeline) would provide useful insights for future work.
- The paper could benefit from a discussion of computational cost and inference time, particularly for the TTA refinement stage.

## Novel Insights
The paper's most novel insight is that contact relationships can serve as a powerful spatial prior to constrain the high-dimensional space of free-form HOI, breaking the reliance on restrictive grasping priors. The observation that penetration metrics can be misleading in free-form settings (since a hand that drifts away from the object achieves low penetration but fails at the task) is a valuable methodological point that should inform evaluation design in this emerging subfield. Additionally, the finding that a diffusion model can learn to associate force-related language ("firmly" vs. "gently") with contact geometry without explicit force supervision is an interesting emergent property worth further investigation.

## Suggestions
- Consider adding a small-scale experiment on a traditional grasp dataset (e.g., GRAB) to demonstrate that TOUCH maintains competitive performance on standard tasks while enabling new capabilities.
- Provide more detail on the manual inspection and refinement stage of the dataset construction—what criteria were used, how many samples were rejected, and what types of interactions were most commonly filtered out.

## Score and Decision
This paper makes a strong, well-executed contribution to an important and underexplored problem. The task formulation is novel and well-motivated, the dataset is a significant resource, the method is technically sound with thorough ablation, and the results convincingly demonstrate the approach's effectiveness. The main limitation (static generation for inherently dynamic actions) is acknowledged and does not invalidate the core contribution. The paper is clearly written and the experiments are comprehensive.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>