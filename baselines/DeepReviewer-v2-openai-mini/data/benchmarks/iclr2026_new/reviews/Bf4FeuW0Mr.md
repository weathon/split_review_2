## Summary
This paper presents DemoGrasp, a reinforcement learning framework for universal dexterous grasping that uses a single demonstration trajectory to guide exploration. The core idea is to reformulate grasping as a single-step MDP where the policy outputs editing parameters (an SE(3) transformation for wrist motion and delta joint angles for hand pose) that modify a pre-recorded demonstration before replay. This compact action space eliminates the need for complex reward shaping. A vision-based policy is then trained via flow-matching imitation learning on successful RL rollouts for sim-to-real transfer.

DemoGrasp achieves strong simulation results: 95.2% success on DexGraspNet with the Shadow Hand (state-based), outperforming prior methods by 4-5%. It generalizes to six unseen object datasets with 84.6% average success across diverse hand embodiments. Real-world experiments on 110 objects achieve 86.5% overall success, including 71.1% on flat/thin objects—a challenging regime for prior work. The method extends to cluttered scenes and language-conditioned grasping.

The paper is well-structured, clearly motivated, and the core methodological insight (demonstration editing as single-step MDP) is creative and effectively communicated. The experiments are extensive, covering multiple datasets, embodiments, and real-world scenarios. However, several concerns limit the current assessment: (1) no statistical variance is reported for any experiment, making significance unclear; (2) novelty claims cannot be verified without external literature (deferred in this run); (3) the core method operates open-loop, which limits robustness; (4) several comparisons are confounded by different training sets; and (5) key reproducibility details for the vision-based policy are missing. These issues are fixable and should be addressed in revision.

## Strengths
**1. Creative and well-motivated methodological contribution.** The demonstration editing formulation is a genuinely clever insight. By decomposing grasping into "where to grasp" (SE(3) wrist transformation) and "how to grasp" (delta hand pose), the method reduces the effective action space from the full joint-space dimensionality (~24 DoF for Shadow Hand + wrist) to ~9 parameters. This design choice is directly motivated by the exploration challenges in dexterous grasping and is clearly explained with intuitive examples.

**2. Impressive empirical scope and generalization.** The paper evaluates on an unusually broad set of conditions: multiple datasets (DexGraspNet, YCB, DGA, EGAD, Omni6DPose, ModelNet40, Visual Dexterity), multiple hand embodiments (Shadow, Allegro, Inspire, Schunk, DClaw, Panda gripper), and real-world objects (110 items). The cross-dataset zero-shot evaluation (84.6% average across six datasets) and the cross-embodiment results (all multi-fingered hands > 90% on training objects) convincingly demonstrate that the method does not overfit to a specific hand or dataset.

**3. Real-world validation on challenging objects.** The real-world experiments go beyond standard benchmarks by including 110 objects with diverse geometries, including flat/thin items (<1.5 cm thickness) that prior work struggles with. Achieving 71.1% on flat/thin objects is a practically meaningful advance, as these items (e.g., tools, cards, phone cases) are common in real-world manipulation.

**4. Simple reward design that works.** The binary reward combining success and collision indicators, together with the 50% collision-disabling trick for thin objects, is elegant. The ablation (Table 8) systematically validates the contribution of each editing parameter, showing that wrist rotation (+13%) and translation (+6%) are the primary drivers of improvement, while hand DoF editing (+2%) provides additional robustness. This analysis strengthens the paper's scientific rigor.

**5. Clean writing and presentation.** The paper is well-organized with a logical flow from problem formulation to method to experiments. The "where/how to grasp" framing makes the core idea accessible. Figures 1 and 2 effectively communicate the pipeline. The experiments section clearly states objectives and covers the most important ablations (necessity of RL, action space components, camera configurations, demonstration quality).

## Weaknesses
### W1: Missing statistical variance across all experiments (Major)
Every simulation result — Tables 1, 2, 5, 6, 7, 8 — reports single-point success rates without standard deviations, confidence intervals, or significance tests. Since RL training involves stochasticity (random seeds, object initialization, environment randomization), single-point estimates are insufficient to establish reliable rankings. For example, DemoGrasp reports 95.2% vs UniGraspTransformer's 91.2% on state-based training (Table 1), but without variance, the reader cannot determine whether this 4% gap is statistically significant or within noise. This is a fundamental reproducibility concern that affects all performance claims.

**Required action:** Report mean ± std over at least 3 independent training seeds for all main simulation results. Add a significance test (e.g., bootstrap or paired permutation) for the primary comparison against UniGraspTransformer. Report the number of evaluation trials per condition.

### W2: Novelty and "first" claims are unverifiable without external literature (Major, Deferred)
The paper makes several strong novelty claims: "to our knowledge, the first to grasp previously unseen small, thin objects in tabletop settings without severe collisions" and "a novel formulation of demonstration editing and single-step RL." Due to Retrieval-Disabled Mode in this run, external literature verification could not be performed. The authors should review whether prior tabletop dexterous grasping methods (e.g., AnyGrasp, GraspGPT, DexDiffuser, or other learned grasping frameworks) have addressed flat/thin objects, and whether demonstration-conditioned policies have been explored in other robotic domains.

**Required action:** Add a dedicated novelty analysis section that explicitly compares against the strongest prior methods on small/thin objects, reporting their performance on comparable benchmarks. Replace the "first" claim with precise evidence-bounded wording, e.g., "Prior work [X] achieves Y% on thin objects; DemoGrasp improves this to Z% on a comparable set of 24 flat items."

### W3: The core method operates open-loop, limiting robustness (Major)
The edited demonstration is replayed without online feedback correction. If the SE(3) transformation is slightly misestimated, if the object shifts during approach, or if unexpected contacts occur, the pre-computed trajectory cannot adapt. The vision-based policy partially mitigates this by operating in a closed-loop manner with action chunking, but it is trained to imitate open-loop RL rollouts, not to perform reactive control. This design choice fundamentally limits the method's ability to recover from errors during execution.

**Required action:** (a) Explicitly acknowledge the open-loop nature and discuss its implications in Section 2.2. (b) Provide a failure analysis showing how many real-world failures are attributable to open-loop execution vs. other factors. (c) Add a discussion section on how to extend to closed-loop editing (e.g., periodic re-estimation of editing parameters using visual feedback).

### W4: The RobustDexGrasp comparison (Table 2) is confounded by different training sets (Major)
DemoGrasp is compared against RobustDexGrasp on five unseen datasets, but both methods were trained on different object sets. While the authors claim this comparison is "fair since both aim at universal grasping," training distribution differences can significantly affect generalization — a method trained on objects geometrically similar to the test set has an inherent advantage. Without controlling for training data, the claim that DemoGrasp "surpasses RobustDexGrasp on four of five datasets" conflates algorithmic superiority with training set effects.

**Required action:** (a) Disclose the exact training set composition for both methods. (b) Perform a controlled comparison by training both methods on identical training sets (at minimum, the 175-object set used for DemoGrasp's cross-dataset experiments). (c) If this is infeasible, reframe the comparison as "under different training regimes" rather than claiming superiority.

### W5: Sim-to-real vision policy lacks reproducibility-critical details (Minor to Major)
The vision-based policy description (Section 2.4) lacks several details needed for reproduction: the flow-matching architecture (denoising network type, parameter count, inference steps, scheduler), data collection statistics (number of rollouts, filtering criteria), domain randomization parameter ranges, and ViT fine-tuning specifics. Without these, other researchers cannot reproduce or build upon the sim-to-real pipeline.

**Required action:** Add a supplementary table (Appendix E) specifying all architecture choices, hyperparameters, and domain randomization ranges. Provide data collection statistics (35K trajectories is mentioned in Figure 2 caption; confirm and add filtering/train-val split details).

### W6: The "175 objects enough?" analysis (Table 7) uses a biased comparison (Minor)
Row 2 of Table 7 trains directly on the test datasets, meaning there is no distribution shift between its training and test data. The 2.4% "marginal gain" is therefore not a fair measure of how close the 175-object training set is to optimal — it's comparing zero-shot generalization (Row 1) against in-distribution performance (Row 2). The strong absolute performance of Row 1 (65-99%) already supports data efficiency.

**Required action:** Remove Row 2 or add a clear caveat that it represents an in-distribution upper bound. Consider adding a training set size ablation (50, 100, 175, 350 objects) to show where performance saturates.

### W7: Missing compute cost and timing analysis (Minor)
The paper does not report training time, inference time, or compute budget for any component. This makes it difficult to assess practical deployability and the fairness of baseline comparisons (e.g., does DemoGrasp require more or less compute than UniGraspTransformer?).

**Required action:** Add a table reporting: RL training wall-clock time, vision-based policy training time, inference speed (Hz) on real hardware, and total GPU-hours compared against a representative baseline.

### W8: Conclusion lacks limitations and introduces unsupported claims (Minor)
The conclusion does not mention any limitations of the proposed method and includes unsupported claims (e.g., "establish a novel approach," "easy-to-implement"). Every paper should state its limitations explicitly.

**Required action:** Replace the current conclusion with a structured version: (1) validated findings, (2) bounded limitations, (3) prioritized future work. Remove "novel approach" and replace with precisely scoped contribution language.

### Summary of Severity Ranking
| Rank | ID | Severity | Impact on Acceptability | Fixable? |
|------|-----|----------|------------------------|----------|
| 1 | W1 | Major | Invalidates statistical conclusions | Yes — add variance |
| 2 | W2 | Major | Novelty unverifiable without lit review | Yes — bounded wording |
| 3 | W3 | Major | Fundamental robustness limit | Partially — acknowledge + analyze |
| 4 | W4 | Major | Weakens comparison claims | Yes — controlled experiment |
| 5 | W5 | Minor-Major | Harms reproducibility | Yes — add appendix |
| 6 | W6 | Minor | Misleading analysis | Yes — reframe or remove |
| 7 | W7 | Minor | Hinders practical assessment | Yes — add table |
| 8 | W8 | Minor | Weakens scientific framing | Yes — rewrite |

**Overall assessment:** The paper has a strong core contribution and impressive empirical scope, but the lack of statistical rigor (W1), unverifiable novelty claims (W2), open-loop limitation (W3), and confounded comparison (W4) are significant concerns that must be addressed before acceptance. All weaknesses are fixable with additional analysis, controlled experiments, and wording revisions.

## Score
**Final Score: 6.5/10**

**Scoring rationale:**

This score prioritizes research value and methodological novelty as primary dimensions, followed by empirical validity and reproducibility.

**Strengths supporting the score:**
- The demonstration editing + single-step MDP formulation is a creative and well-motivated methodological contribution that meaningfully reduces exploration complexity.
- The empirical scope is unusually broad (7 datasets, 6 embodiments, 110 real-world objects) and convincingly demonstrates generalization.
- Real-world results on flat/thin objects (71.1%) represent a practically relevant advance over prior work.
- The ablation analysis (Table 8) provides clear attribution of each editing component's contribution.

**Weaknesses constraining the score:**
- W1 (Missing variance): Fundamental statistical rigor issue that affects all performance claims. Without variance, the reported margins cannot be assessed for significance. This is the single most impactful weakness.
- W2 (Unverifiable novelty claims): The "first" claim on small/thin objects and the "novel formulation" language cannot be verified without external literature. The authors should adopt bounded, evidence-grounded wording.
- W3 (Open-loop execution): The method's open-loop nature is a meaningful practical limitation that is not adequately discussed or analyzed.
- W4 (Confounded comparison): The RobustDexGrasp comparison needs controlled training conditions to support the claimed superiority.

**Fixability assessment:** All major weaknesses are fixable with additional experiments (multi-seed runs, controlled comparisons, failure analysis) and wording revisions (bounded claims, explicit limitations). No fatal flaws were identified. The core methodological contribution is valid and the empirical results, once variance is reported, are likely to remain competitive.

**Without the statistical variance issue, the score would be approximately 7.5–8.0/10. The paper is on a strong trajectory and with a focused revision addressing the identified weaknesses, it has clear potential for acceptance at a top venue.**