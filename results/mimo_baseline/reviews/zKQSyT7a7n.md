## Summary

This paper introduces Visuo-Tactile World Models (VT-WM), the first multi-task world model that fuses exocentric vision (via Cosmos tokenizer) with fingertip tactile sensing (via Sparsh-X on Digit 360 sensors) in a transformer-based predictor for action-conditioned future state prediction. The key thesis is that tactile feedback provides contact grounding that vision-only world models lack, reducing hallucinations such as object disappearance under occlusion, teleportation, and physically implausible dynamics. The paper demonstrates improvements in imagination quality (33% better object permanence, 29% better causal compliance), zero-shot real-robot planning (up to 35% higher success rates on contact-rich tasks), and data efficiency (3.5× over behavioral cloning with 20 demonstrations).

## Strengths

- **Well-motivated and clearly articulated problem.** The paper convincingly argues that vision-only world models fail in contact-rich manipulation due to occlusion and visual aliasing, and that tactile sensing provides the missing local contact signal. The qualitative examples (e.g., cloth wiping without contact, cube stacking with occlusion) make the problem tangible and compelling.

- **Comprehensive multi-faceted evaluation.** The paper evaluates across three distinct dimensions—imagination quality (object permanence and causal compliance via CoTracker-based Fréchet distance), zero-shot planning success on real hardware across 5 tasks of increasing difficulty, and data efficiency against a BC baseline. This breadth strengthens the paper's claims considerably.

- **Statistical rigor in perception evaluation.** The paper reports paired t-tests with p-values for the Fréchet distance comparisons across tasks, and reports 95% confidence intervals. The results are significant at p < 0.05 for the majority of tasks, lending credibility to the 33% and 29% headline improvements.

- **Compelling real-robot planning results.** The zero-shot open-loop transfer to a real robot is a strong experimental validation. The task-dependent gains (0% for reach, 35% for reach & push, 31% for wipe) directly support the hypothesis that tactile grounding matters specifically for contact-rich, multi-step tasks, not just for kinematic fidelity.

- **Data efficiency result is practically meaningful.** The plate-insertion experiment (77% vs. 22% success with only 20 demonstrations) demonstrates that multi-task visuo-tactile pretraining yields transferable contact priors, which is a valuable practical finding for real-world deployment.

## Weaknesses

### Fatal
None.

### Major

- **Limited number of planning trials.** The planning evaluation uses only 5 trials per task from distinct initial conditions. With binary success/failure outcomes, this provides very low statistical power to detect differences between conditions. For instance, the 10% gap on push fruits (83% vs. 92%) and 11% gap on stack cubes (75% vs. 83%) are not distinguishable from noise at n=5. The paper would benefit substantially from more trials or at minimum reporting confidence intervals / Wilson score intervals for the success rates.

- **Open-loop planning limits practical conclusions.** All plans are executed open-loop on the real robot, meaning the world model's advantages are only tested in a single-shot setting without error correction. While this is a standard evaluation protocol for world models, it means the reported success rates may not reflect performance in a closed-loop planning regime where the model would be most useful. The paper should discuss this limitation more explicitly and ideally include at least a qualitative analysis of how errors accumulate.

### Minor

- **Inconsistent results on scribble with marker.** VT-WM shows *worse* causal compliance than V-WM on this task (Fréchet distance ~0.50 vs. ~0.35 in Figure 6). The paper acknowledges this but provides no explanation. This inconsistency weakens the generality of the causal compliance claim and deserves analysis—is the tactile signal uninformative or misleading for this task?

- **No ablation on architectural choices.** The paper uses a specific combination of Cosmos + Sparsh-X + 12-layer transformer but does not ablate key design decisions: the effect of tactile context length (currently only 2 frames / 0.16s), the number of tactile sensors, or the fusion strategy (concatenation vs. cross-attention). Understanding which design choices matter would strengthen the contribution.

- **Single robot platform.** All experiments use an Allegro Hand with Digit 360 sensors on a Franka Panda. While this is a reasonable platform, the paper does not discuss how the approach would generalize to other tactile sensors or hand designs, which limits the broader applicability of the findings.

### Trivial
None.

## Nice-to-Haves

- A comparison with a third baseline that uses tactile sensing in a simpler way (e.g., tactile-conditioned reward shaping or tactile features concatenated with visual features in a non-world-model policy) would help isolate whether the gains come from the world model formulation specifically or from tactile information generally.
- Including the number of CEM iterations and planning time would help practitioners assess the computational feasibility of the approach.

## Novel Insights

The paper's central insight—that tactile sensing resolves the contact-ambiguity problem in visual world models—is well-supported and practically important. Beyond this, the paper makes the interesting observation that tactile grounding improves planning *indirectly*: the tactile modality is not used in the planning cost function (which remains vision-based), yet it substantially improves plan quality by making the world model's rollouts more physically faithful. This suggests that the value of tactile sensing for planning lies not in providing a better goal specification but in reducing compounding errors in imagined futures—a distinction that has implications for how multi-modal world models should be designed.

## Suggestions

- Increase the number of planning trials to at least 15-20 per task to enable meaningful statistical comparisons of success rates, and report confidence intervals.
- Provide analysis of the scribble-with-marker failure case: is the tactile signal uninformative for this task, or does the model fail to leverage it?
- Add an ablation on tactile context length to justify the 2-frame / 0.16s design choice and to understand the sensitivity of the approach to this hyperparameter.

## Score and Decision

The paper presents a clear, well-motivated contribution with a novel multi-task visuo-tactile world model architecture. The evaluation is comprehensive, spanning imagination quality, real-robot planning, and data efficiency, with appropriate statistical testing for the perception metrics. The real-robot results are convincing, particularly the task-dependent gains that validate the contact-grounding hypothesis. However, the planning evaluation is weakened by very few trials (n=5), and the inconsistent results on one task and lack of architectural ablations prevent a stronger score. Overall, this is a solid paper that advances the important topic of contact-aware world models for manipulation.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>