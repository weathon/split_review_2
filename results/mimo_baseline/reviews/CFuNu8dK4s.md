## Summary

Vidar proposes a three-stage pipeline for data-efficient bimanual robotic manipulation: (1) continuous pre-training of a video diffusion model on ~750K multi-view robotic episodes from three platforms using a unified observation space, (2) fine-tuning on as few as 20 minutes of target-domain demonstrations, and (3) a masked inverse dynamics model (MIDM) that learns to attend to action-relevant regions without dense supervision to decode actions from generated videos. The system outperforms video-based baselines (UniPi, VPP) and Pi0.5 on both simulation benchmarks and real-world tasks, including generalization to unseen tasks and backgrounds.

## Strengths

- **Effective cross-embodiment transfer with minimal data**: The core claim is well-supported—Vidar achieves 68.2% success on seen tasks and 55.6% on unseen backgrounds with only ~232 episodes (20 minutes) of demonstrations, massively outperforming UniPi (36.4%/22.2%) and VPP (4.5%/0.0%). This is a practically significant result for real robot deployment.

- **Well-motivated architectural design**: The factorization of the policy through video space ($\pi = I \circ G$) cleanly separates the representation burden (handled by large-scale video pretraining) from the lightweight action adapter. The unified observation space (Eq. 3) that encodes robot, camera, and task context is a principled approach to handling heterogeneous embodiments without coupling actions to the generative model.

- **MIDM demonstrates clear generalization gains**: Table 4 shows MIDM achieves 49.0% test accuracy vs. 24.3% for the ResNet baseline despite identical 99.9% training accuracy, validating that learned sparsity masks (Figure 3) provide genuine background robustness. The ablation (Table 5) further confirms MIDM's contribution across all three evaluation scenarios.

- **Comprehensive evaluation**: The paper evaluates on both simulation (RoboTwin 2.0, multi-task setting) and real-world platforms, tests three distinct generalization axes (seen, unseen tasks, unseen backgrounds), and provides ablations for both TTS and MIDM components.

## Weaknesses

### Fatal

None.

### Major

- **Open-loop control and limited task complexity**: All real-world experiments use open-loop control with no replanning, and the demonstrated tasks (pick-and-place, flipping a dice, lifting a basket) are relatively simple single-step or short-horizon manipulation. The paper claims contributions for "bimanual manipulation for everyday activities" but the real-world tasks don't convincingly demonstrate the tight temporal coordination and contact dynamics that make bimanual manipulation genuinely hard. The gap between the claim's ambition and the evaluation scope weakens the contribution.

- **Test-time scaling reliance on proprietary models**: TTS uses GPT-4o for video ranking, introducing cost ($K=3$ means 3× inference plus GPT-4o API calls) and a dependency on a closed-source model. The paper provides no analysis of TTS contribution decomposition, no cheaper alternative evaluator, and no cost-performance tradeoff analysis. The ablation shows TTS matters (Table 5: 45.5%→68.2% on seen tasks), making the dependency on a proprietary evaluator a notable limitation for reproducibility and practical deployment.

- **Table 4 reveals significant overfitting**: Both models reach 99.9% training accuracy but MIDM only achieves 49.0% test accuracy (and ResNet 24.3%). While MIDM improves over the baseline, 49% action prediction accuracy still means the model fails on roughly half of test cases. This raises questions about the robustness of the action decoding pipeline, especially under distribution shift.

### Minor

- **Simulation and real-world use different backbone models**: Simulation uses Wan2.2 while real-world uses Vidu 2.0, making it hard to isolate whether performance differences across settings stem from the method or the backbone. The additional real-world experiments with Wan2.2 and HunyuanVideo (mentioned but deferred to Appendix D) would benefit from in-paper discussion.

- **Limited pre-training data diversity**: The 750K episodes come from only 3 robot platforms. The paper's "one prior, many embodiments" framing would be stronger with evidence that the prior transfers to embodiments substantially different from the training distribution (e.g., different gripper types, mobile manipulators, or single arms).

- **Lack of closed-loop comparison**: VPP uses closed-loop control while Vidar uses open-loop, making the comparison in Table 2 confounded by control strategy. The paper acknowledges this difference but doesn't disentangle its effect.

### Trivial

None.

## Nice-to-Haves

- An analysis of how performance scales with the number of fine-tuning episodes (e.g., 10, 50, 100, 200) would strengthen the low-shot claims and help practitioners decide data budgets.
- A comparison of TTS using cheaper evaluators (e.g., CLIP score vs. GPT-4o) would make the approach more practical.
- Closed-loop experiments with iterative video replanning would demonstrate the full potential of the video diffusion prior.

## Novel Insights

The paper's genuinely novel insight is that decoupling video generation from action prediction—combined with a unified observation space that strips action information from the video diffusion model—enables effective cross-embodiment transfer without requiring embodiment-specific action labels during pretraining. This is a meaningful departure from end-to-end VLA approaches and from coupled video-action methods like VPP. The MIDM's implicit mask learning from action supervision alone (without segmentation labels) provides an elegant solution to the distractor problem that is well-validated empirically.

## Suggestions

- Provide a cost-performance analysis for test-time scaling with different numbers of candidates K and different evaluators (CLIP, smaller VLMs vs. GPT-4o).
- Add closed-loop replanning experiments to demonstrate the approach beyond open-loop single-shot generation.
- Report per-task results in Table 2 to show whether the high average success rates are driven by easy tasks.
- Investigate whether MIDM's 49% test accuracy is a bottleneck by analyzing whether the 51% action prediction failures correlate with task failures in the end-to-end system.

## Score and Decision

This paper presents a well-motivated framework with strong empirical results for data-efficient cross-embodiment manipulation. The unified observation space for video pretraining and MIDM are genuine contributions. However, the open-loop control limitation, reliance on proprietary models for TTS, and the gap between claimed and demonstrated task complexity (particularly for "bimanual manipulation") prevent a higher score. The results are compelling but the evaluation is somewhat narrow.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>