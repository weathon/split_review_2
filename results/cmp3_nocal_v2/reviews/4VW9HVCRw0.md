## Summary

This paper introduces the new task of Free-Form HOI Generation — producing hand-object interactions beyond stable grasps (e.g., pushing, poking, tipping, pressing). The authors contribute (1) **WildO2**, a 4.4k-sample 3D HOI dataset reconstructed from internet videos using a clever O2HOI frame-pairing strategy, and (2) **TOUCH**, a three-stage framework combining contact-map prediction (CVAEs), multi-level conditioned diffusion (coarse-to-fine text+geometry injection), and physical constraint refinement (cycle-consistency + TTA). Experiments on WildO2 show substantial gains over adapted baselines (ContactGen, Text2HOI) across contact accuracy, physical plausibility, diversity, and semantic consistency.

## Strengths

1. **Problem framing is specific and well-motivated (Sec. 1).** The paper precisely identifies that existing HOI generation is constrained by grasp-centric inductive biases (force-closure priors, palm-dominant contact models) and correctly argues that these biases suppress non-grasping interactions. The proposed shift to "free-form HOI" is a meaningful expansion of scope anchored in a concrete limitation.

2. **O2HOI frame-pairing strategy is clever and practical (Sec. 3.1).** Using a pre-interaction object-only frame to obtain clean object masks via SAM2 segmentation + dense matching, then transferring these masks to the interaction frame, avoids the geometric inconsistencies of diffusion-based inpainting while being scalable. This is a simple, well-executed idea that directly enables the automated pipeline.

3. **Multi-level annotation scheme (SSCs + DSCs + 17-part hand segmentation) is well-designed (Sec. 3.3).** The division into template-based coarse labels (from Something-Something V2) and VLM-generated detailed descriptions specifying hand contact parts, object contact parts, and physical actions is thoughtful. The 17-part hand segmentation including dorsal-side parts, absent from most grasp-centric datasets, is a genuine enabler for the task.

4. **Quantitative result gap over baselines is substantial (Table 1).** TOUCH outperforms both baselines on every metric: P-IoU 0.776 vs. 0.711/0.620, MPVPE 2.97 vs. 4.69/5.46, VLM score 7.1 vs. 6.5/4.8, user perceptual score 8.8 vs. 7.5/6.3. These are not marginal improvements, and the ablation study (Table 2) confirms that both the contact prediction module and the refiner contribute meaningfully (P-IoU drops from 0.728 to 0.492 and 0.513 when removed).

## Weaknesses

### Fatal

None.

### Major

1. **Evaluation is conducted exclusively on the authors' own dataset (WildO2), with no cross-dataset validation (Sec. 5.1).** Every quantitative result in Tables 1 and 2 is on the WildO2 test set, which was reconstructed and annotated through the authors' own pipeline — the same pipeline the generation model is trained on. The paper would be substantially strengthened by at least one of: (a) evaluation on an existing grasp-centric benchmark (GRAB, OakInk) to show TOUCH does not regress on standard grasping, or (b) a controlled human study comparing generated outputs against the original internet video frames ($I_{hoi}$). Without this, it is difficult to assess how well the method generalizes beyond the distribution of the authors' reconstruction pipeline. The paper's limitations section (Sec. 6) acknowledges the static-snapshot and dataset-scale limitations but does not address this single-dataset evaluation concern.

### Minor

2. **VLM evaluation protocol is unspecified (Sec. 5.1).** The paper reports a "VLM assisted evaluation" score (7.1 vs. 6.5 vs. 4.8) but does not specify which VLM was used, what prompt template was employed, whether the evaluation was pairwise or absolute, or how many samples were evaluated. Without this information, these scores are uninterpretable and cannot be reproduced or compared against.

3. **User study uses only 10 users (Sec. 5.1).** The perceptual score is reported as an average from 10 users. For a subjective evaluation that claims significance, a sample of 10 is too small to draw reliable conclusions, and no measure of inter-rater agreement or statistical significance is reported.

4. **Baseline post-processing is underspecified (Sec. 5.2).** The paper states that both baselines (ContactGen, Text2HOI) were augmented with "an optimization-based post-processing module to correct hand poses" described in a single sentence. The loss functions, hyperparameters, and whether the same post-processing was applied to the authors' method are not stated. This makes it difficult to assess whether the comparison is fair — the post-processing could be tuned to the authors' setting and applied to baselines without similar tuning.

5. **Out-of-domain generalization on Objaverse is only qualitative (Sec. 5.4.2, Fig. 7).** The paper claims "strong generalization capability" based on visual examples alone. No contact accuracy, penetration, or any quantitative metric is reported for these novel-object generations. At minimum, the contact and penetration metrics used in the main evaluation should be reported here.

6. **Force-related semantic analysis lacks experimental control (Sec. 5.4.3).** The finding that "firm" prompts yield 22–25% larger contact area than "gentle" prompts is interesting, but the paper does not specify the sample size, how samples were selected, whether the object was held constant, or whether the comparison was controlled for other confounding factors. This finding deserves proper statistical treatment to be convincing.

7. **Dataset reconstruction pipeline failures may introduce selection bias (Fig. 3a).** Only 55% of reconstruction attempts succeed; 31% fail due to pose estimation failure, 9% to other causes. The paper does not analyze what types of interactions fail. If failures concentrate in the most interesting non-grasping categories (delicate fingertip actions, heavy occlusions, small/thin objects), WildO2 may systematically underrepresent the very diversity the paper targets. While this does not invalidate the existing results, it would strengthen the paper to report a breakdown of failures by interaction type.

### Trivial

None.

## Nice-to-Haves

- A cross-dataset evaluation on grasp benchmarks (even a small subset) would substantially strengthen generalization claims.
- A diagnostic analysis of the 45% reconstruction failure cases, showing the distribution of failures across object categories and action types, would address selection-bias concerns.
- The VLM evaluation protocol should be fully specified (model, prompt template, rating scale, number of samples) in any revision.

## Removed Points

- **Code/dataset release status.** Removed per Hard Rules: the paper cites a project page; questioning release status of cited entities is not permitted.
- **Notation confusion ("✗ hoc." / "✗ mul.").** Removed: these are defined in the Table 2 caption ("absence of $\mathcal{M}_O$ and $\mathcal{M}_H$ (hoc.)" and "multi-level network structure (mul.)").
- **PD/PV metric tension in main results.** Removed: the paper addresses the primacy of contact metrics in the ablation section, and in Table 1 the ranking is unambiguous (TOUCH wins on every metric including contact, so PD/PV interpretation does not create ambiguity).
- **Missing baselines (Yang et al. 2024a,b; Yu et al. 2025; Zhang et al. 2025).** Removed: the paper correctly notes existing methods focus on grasping, and the authors scope their comparison to methods adaptable to their non-grasping setting. Exhaustive comparison against grasp-dedicated methods would not test the paper's core claim.
- **Minor presentation/style notes and formatting nitpicks.** Removed per instructions: parser artifacts are not author errors.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one genuinely novel observation: the paper's own argument about PD/PV metric interpretation in the ablation (that penetration metrics are misleading without established contact) exposes a broader issue in HOI evaluation — that standard HOI metrics developed for grasp-centric settings may not transfer cleanly to free-form interactions. This tension, while not explored by the paper itself (it defaults to reporting all metrics), points to a need for the community to develop evaluation standards for non-grasping HOI that do not conflate "no contact" with "good contact." This is an insight the paper enables by virtue of tackling a new task, even though it does not resolve it.

## Suggestions

1. In a revision or camera-ready, add a cross-dataset evaluation on a grasp benchmark (even a single held-out split of GRAB or OakInk) to demonstrate that TOUCH does not regress on standard grasping performance. This directly addresses the single-dataset evaluation concern.
2. Fully specify the VLM evaluation protocol — model name, prompt template, rating scale, number of samples — in a supplementary section or footnote in the main paper.
3. Append a failure-mode analysis table to the dataset description (Appendix), showing the distribution of reconstruction failures across object categories and interaction types, to address the selection-bias concern.

## Score and Decision

**Score rationale.** The paper makes genuine contributions: a well-motivated new task, a cleverly constructed dataset, and a method with substantial quantitative gains over adapted baselines. The multi-level conditioning design and the O2HOI pairing strategy are architecturally sound. However, the evaluation is limited to the authors' own dataset without cross-dataset validation, and several evaluation details (VLM protocol, user study size, baseline post-processing specification) are insufficiently documented. These are addressable concerns that weaken but do not invalidate the core claims. The paper's contributions are clear enough and the method strong enough to warrant acceptance despite these gaps.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>