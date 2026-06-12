## Summary

CoRAL proposes a modular neuro-symbolic framework for contact-rich robotic manipulation. It uses a VLM (GPT-4o) for perception and physical parameter estimation, an LLM (GPT-4o) to generate the *symbolic structure* of an MPPI cost function and contact strategies, and an outer-loop LLM for online diagnosis and parameter adaptation after failures. The system is evaluated in simulation (Robosuite/MuJoCo) on 6 tasks against OpenVLA, π0.5, human-expert-designed cost functions, and ablations.

## Strengths

1. **Well-motivated architectural separation of vision and language roles.** The Unified VLM ablation shows that giving a single VLM both perception and planning responsibilities causes collapse from 9/10 to 1/10 on T4. This concretely demonstrates that modular role separation matters for performance, not just the individual components.

2. **Novel use of LLM to generate MPPI cost function structure.** Prior work (IMPACT, VLMPC) uses VLMs to produce cost *maps* or identify sub-goals within an MPC loop. CoRAL elevates the LLM to formulate the *symbolic structure* of the cost function itself — including contact-aware terms like `w_c * I{no contact at t}` — and to propose contact surface regions. This is a genuinely different idea from existing "VLM-as-perceptual-guide" approaches.

3. **Thorough ablation suite.** The four ablations (w/o Memory, w/o Refinement, Unified VLM, w/o Pose Tracking) systematically isolate different design choices. The results are consistent with the story the paper tells about each component's role. The w/o Refinement variant dropping from 4/10 to 0/10 on T1 and the Unified VLM collapsing on all complex tasks are particularly informative.

## Weaknesses

### Major

1. **The headline comparison against end-to-end VLAs does not validate CoRAL's specific contribution and is framed misleadingly.** The paper leads with the OpenVLA/π0.5 comparison as its primary result (Section 4.1.1: "CoRAL significantly outperforms both state-of-the-art baselines… This is a critical finding"). However, CoRAL has access to (a) a known MuJoCo dynamics model for MPPI rollouts, (b) FoundationPose for continuous 6-DoF pose tracking, and (c) force/torque feedback for reactive control augmentation. OpenVLA and π0.5 receive only pixels and must predict joint-level actions with no dynamics model, no pose tracker, no trajectory optimization, and no force feedback. The comparison tests model-based-vs-model-free paradigms, not CoRAL's specific novelty — that an LLM can generate the cost function structure. Every competent MPPI system with a reasonable cost function would outperform imitation-learned policies on these out-of-distribution contact-rich tasks. The informative comparisons for CoRAL's contribution are the human-expert and ablation baselines, which the paper de-emphasizes.

2. **The Planning World dynamics model is not specified, which is the most consequential gap for assessing claims of robustness.** MPPI rollouts happen "in the 'Planning World'" (line 118), which is "constructed" from estimated parameters θ (line 69). The paper never states what this Planning World is. The natural reading is that it is the same MuJoCo-based Robosuite environment used for evaluation, configured with estimated parameters. If correct, the "robustness" demonstrated (Section 4.1.4, Figure 4: correcting mass from 2.0 kg → 0.85 kg against a ground truth of 0.1 kg) is robustness to *parameter mismatch within a known simulator*, not to the actual sim-to-real gap where the dynamics model itself is approximate and contacts are stochastic. The paper invokes "sim-to-real gap" as motivation (Eq. 7, line 126; line 220) but provides no evidence outside simulation, making it impossible to assess whether this architecture would transfer to real hardware.

3. **Performance on the hardest tasks is modest and the evidence lacks statistical rigor.** On the flagship multi-stage task T1 (Push + Pick Board), CoRAL achieves 4/10 success — a task it was specifically designed for. The memory module adds only 2/10 on T1 (from 2/10 to 4/10) and 2/10 on T6 (from 5/10 to 7/10). With binary outcomes and only 10 trials per condition, the 95% Clopper-Pearson confidence interval for 4/10 spans approximately 12%–74%. No confidence intervals or statistical tests are reported anywhere. Against the Expert (FSM) baseline, CoRAL achieves 4/10 vs. 8/10 on T1 — a 2× gap — while the paper states the LLM "can recover much of the structure of expert-designed costs automatically" (Section 4.1.2), which overstates performance on the hardest tasks.

### Minor

1. **The LLM-based cost function generation and outer-loop adaptation are underspecified for reproducibility.** The paper does not describe: the prompt format or any constraints preventing the LLM from generating syntactically invalid cost functions; how numerical weight outputs (w_d, w_c, w_u) are parsed and validated; whether physical parameter updates from the LLM are numerical estimates or textual refinements; the exact format of logged episode data E_t fed to the outer loop; or any guard against the LLM producing increasingly extreme parameters over multiple adaptation cycles.

2. **No quantitative evaluation of the VLM's physical parameter estimation.** The VLM estimates mass and friction from appearance and task description (Section 3.1), but no accuracy metrics, ablation of this step, or analysis of estimation error is provided. This is the first step in the pipeline and its quality directly affects all downstream components.

3. **The memory unit is evaluated only on the same task distribution, not on cross-task generalization.** The paper frames memory as enabling "generalization across diverse manipulation scenarios" (Contributions, line 31), but the evaluation tests only within the same 6 tasks. The 2/10 improvement on T1 reflects within-task adaptation, not the cross-task generalization claimed.

4. **No analysis of LLM output reliability or variance.** The paper does not report how often the LLM generates a valid cost function on the first try, how often the outer loop's diagnosis actually improves the estimated parameters, or the variance across different LLM calls/inference seeds. This makes it difficult to assess whether the LLM is a reliable component or a source of variance.

5. **Key implementation details missing from the main text.** The values of K_f (feedback gain matrix in Eq. 7) are not given. How "contact" is detected for the indicator term `I{no contact at t}` is not specified (through MuJoCo contact forces?). The exact failure criterion triggering the outer loop beyond "persistent failures" (N_retry=15) is vague. Randomization ranges for object masses, friction coefficients, and dimensions are not reported.

6. **No breakdown of wall-clock time between components.** The paper reports average completion time but does not separate time spent on LLM inference vs. MPPI computation vs. perception, which matters for assessing real-time feasibility.

### Trivial

None beyond the minor points above.

## Nice-to-Haves

- Reporting confidence intervals or increasing the number of trials per condition would substantially strengthen the statistical claims.
- A real-robot validation on at least one task would transform the paper's credibility for claims about contact-rich adaptive control.
- Providing the LLM prompt template, a representative generated cost function, and an example of the outer-loop's natural language diagnosis in the main text (rather than deferred to a stripped appendix) would make the claimed explainability benefit verifiable.
- A comparison against a simpler LLM baseline (e.g., LLM outputs a goal position for a PD controller) would help isolate the value of LLM-as-cost-formulator specifically.

## Removed Points

- *Critique about "the paper claims to address manipulation in the real world but provides only simulated evidence":* The paper does not explicitly claim real-robot experiments; it mentions sim-to-real gap as a motivation but evaluates in simulation. Removed as overstatement.
- *Speculation about Appendix ?? content:* The parser strips appendices from all papers. Not a valid weakness.
- *"The single-stage expert underperformance suggests the human expert was not particularly skilled":* Speculative and not grounded in the paper. Removed.
- *Requesting comparison to Inner Monologue, ThinkAct, ECoT:* These are methodologically different (decoupled reasoning for learned policies, not MPPI cost formulation). Scope creep.
- *Critique about the VLM baseline comparison being "unfair":* The rule states to remove claims of unfair comparison if the asymmetry favors the baseline, not the author's method. Here the asymmetry (model-based advantages) favors CoRAL, but the core issue is about whether the comparison is *informative* for validating the specific contribution, not about fairness. Retained with adjusted framing.

## Novel Insights

The harsh critic's review surfaces a recurring pattern at the intersection of LLMs and robotics: papers that compare hybrid model-based+LLM systems against pure model-free learned policies without controlling for the structural advantages (known dynamics models, pose trackers, force feedback) that the model-based component provides. The critical validation for CoRAL's contribution lies in the human-expert cost-function comparison and the ablation study — not in outperforming VLAs that operate without any of these architectural supports.

## Suggestions

- Reframe the narrative to lead with the human-expert cost-function comparison and ablation study — these directly test CoRAL's contribution. Demote the VLA comparison to a supplementary finding.
- Explicitly specify the Planning World dynamics model: its relationship to the evaluation MuJoCo model, what approximations are made, and how it differs from the evaluation world.
- Report confidence intervals (or Bayesian credible intervals) for all success-rate results.
- Provide the LLM prompt template, a representative generated cost function, and an example outer-loop diagnosis in the main text.
- Include a quantitative evaluation of VLM parameter estimation accuracy (mass, friction) against ground truth.
- Increase trial counts or report measures of variance across random seeds.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Generating Robot Policy Code (WtHKqtHVXo) | 4.00 | R1 | Similar LLM+contact-rich topic, simulation-only, called "ad-hoc" by reviewers. CoRAL has a more principled architecture and better ablations but similar evaluation limitations. |
| Intelligent Control Embodied Robotics (70kYH6InYU) | 3.50 | R1 | LLM-integrated control, weak evaluation. CoRAL is more novel and better evaluated. |
| Make a Donut (iTsHStJKcm) | 5.25 | R1 | LLM-guided hierarchical planning, has real-world experiments, still rejected. CoRAL lacks real-world validation. |
| HAMSTER (h7aQxzKbq6) | 6.00 | R1 | Hierarchical VLA, real-world and simulation, accepted. CoRAL's evaluation is substantially weaker. |
| Plan-Seq-Learn (hQVCCxQrYN) | 6.67 | R2 | LLM+RL+MP for long-horizon tasks, >85% on 25 tasks, accepted. CoRAL's evaluation much less thorough. |
| ManiBox (VEdeDd13gx) | 5.25 | R2 | Simulation-to-real grasping, has real-robot experiments, rejected. CoRAL is simulation-only. |
| NaVILA (gkDRrvqeWF) | 5.50 | R1 | VLA for legged navigation, real-world deployment, rejected. CoRAL's simulation evaluation is weaker. |
| Predictive Inverse Dynamics (meRCKuUpmc) | 7.50 | R1 | Large-scale learned policy, thorough eval, accepted. Far beyond CoRAL's evaluation scope. |

**Round 1 bracket:** 3.5 – 6.0

**Round 2 narrowing:** After comparing against Plan-Seq-Learn (6.67, full real+sim evaluation, 25+ tasks), Make a Donut (5.25, real+sim, rejected), and ManiBox (5.25, real+sim, rejected), CoRAL's simulation-only evaluation with n=10 trials, no confidence intervals, and modest success rates places it clearly below the 5.25 anchors. The genuinely novel cost-function-formulation idea and thorough ablation prevent it from falling as low as the 3.5–4.0 anchors.

**Final score:** 4.5 — a borderline reject reflecting a novel architectural contribution undermined by an evaluation that does not provide sufficient evidence to support the strength of the paper's claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>