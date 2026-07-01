## Summary

This paper introduces **Free-Form HOI generation**, a task that moves beyond grasp-centric hand-object interaction synthesis to include diverse non-grasping actions (e.g., pushing, poking, rotating). To support this task, the authors construct **WildO2**, the first large-scale in-the-wild 3D HOI dataset (4.4k samples, 92 intents, 610 object categories) built from internet videos via an automated reconstruction pipeline. They further propose **TOUCH**, a three-stage framework combining contact map prediction (CVAEs), a multi-level conditioned diffusion model with coarse-to-fine text/geometry injection, and a self-supervised physical refinement module. Experiments show TOUCH outperforms adapted baselines on contact accuracy, physical plausibility, diversity, and semantic consistency.

## Strengths

- **New task and dataset of genuine significance.** The paper identifies and formalizes a clear gap in HOI generation—the dominance of grasping priors—and provides both a principled problem formulation and a large-scale, annotated 3D dataset (WildO2) that includes non-grasping interactions. This is a valuable resource for the community.
- **Technically sound and well-motivated framework.** TOUCH’s three-stage design (contact prediction → multi-level diffusion → physical refinement) is logically structured. The use of contact maps as an explicit spatial prior to break grasping biases is justified, and the coarse-to-fine injection of semantic/geometric conditions is a clean solution for balancing global intent and local detail.
- **Comprehensive experimental validation.** Evaluation covers four key aspects (contact accuracy, physical plausibility, diversity, semantic consistency) with multiple metrics. Ablation studies systematically isolate the contribution of each component, and out-of-domain generalization tests on Objaverse demonstrate robustness. The analysis of force-related semantics (firm vs. gentle) adds an insightful qualitative dimension.
- **Strong empirical results.** TOUCH achieves substantial improvements over adapted baselines: ~9% absolute gain in contact IoU, ~50% reduction in penetration depth, and clear superiority in semantic consistency metrics (P-FID, VLM, user study). The ablations confirm that each module is necessary.

## Weaknesses

### Fatal
None identified.

### Major
1. **Limited dataset size and potential reconstruction bias.** With only 4.4k successful samples (55% success rate from 8k clips), the dataset is modest compared to typical 3D HOI datasets. The high failure rate (especially “Pose Estimation Failure” at 31%) may introduce systematic bias toward easier, less occluded interactions. The paper does not analyze how such filtering affects the diversity or representativeness of the final dataset.

2. **Baseline adaptation is not fully convincing.** The two baselines (ContactGen, Text2HOI) were originally designed for grasp-centric settings. While the authors add an optimization-based post-processing module to correct global drift, the large performance gap could partly stem from suboptimal adaptation (e.g., architectural mismatches, different training recipes) rather than TOUCH’s inherent superiority. A stronger comparison might involve retraining the baselines with more careful hyperparameter tuning on WildO2.

3. **Semantic consistency evaluation relies on small-scale human judgment.** The perceptual score (PS) is based on only 10 users, which limits statistical reliability. The VLM-assisted evaluation is reasonable but lacks details on the prompting strategy and potential biases of the chosen VLM. More rigorous semantic evaluation (e.g., human rating on a larger scale, or agreement metrics) would strengthen the claims.

### Minor
1. **Contact prediction accuracy is not directly evaluated.** The paper evaluates the full pipeline’s contact performance but does not report how accurate the intermediate contact map prediction (CVAE) is on its own. Since this stage is critical, an isolated evaluation (e.g., contact map IoU vs. ground truth) would help assess error propagation.

2. **The physical refinement module adds complexity without clear analysis of its computational cost.** The test-time adaptation (TTA) step involves iterative optimization, but the paper does not report inference time or the number of iterations used in practice. This matters for practical deployment.

### Trivial
- Figure 3(a) labels “Pore Estimation Failure” – likely a typo/parser artifact for “Pose Estimation Failure”. Not a paper flaw.
- Some figure captions are dense and small (e.g., Figure 3, Figure 4), making details hard to read.

## Nice-to-Haves
- Provide an isolated evaluation of the contact map prediction stage (e.g., CVAE reconstruction accuracy on a held-out set).
- Include ablation on the number of TTA iterations to show the trade-off between quality and speed.
- Release the pre-trained models and reconstructed dataset publicly to facilitate community use and reproducibility.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions
- **Strengthen baseline comparison:** Retrain ContactGen and Text2HOI from scratch on WildO2 with a systematic hyperparameter search, and report whether the gap narrows. Alternatively, include a variant of TOUCH without contact prediction to isolate the benefit of that module.
- **Analyze dataset bias:** Provide statistics comparing the distribution of successful vs. failed reconstruction samples (e.g., object category, action type, occlusion level) to inform users about potential biases.
- **Scale up human evaluation:** Collect PS from at least 30–50 participants, or use a validated perceptual quality metric (e.g., LPIPS on rendered images) to complement the small user study.

## Score and Decision
The paper makes a novel, well-motivated contribution to an underexplored problem, with a new dataset and a carefully designed framework that shows clear empirical gains. Minor limitations in baseline adaptation and evaluation depth do not invalidate the core contributions.

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>