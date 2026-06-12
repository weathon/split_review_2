## Summary
CoRAL proposes a modular framework for zero-shot contact-rich manipulation that separates VLM-based perception (pose estimation via FoundationPose, physical parameter estimation via GPT-4o) from LLM-based strategy generation (MPPI cost function formulation and symbolic contact strategies), augmented by an online refinement loop and a RAG-based memory unit. Experiments in MuJoCo simulation on six contact-rich tasks demonstrate CoRAL outperforms end-to-end VLA baselines (OpenVLA-OFT, π₀.₅) and that each architectural component is necessary via comprehensive ablations.

## Strengths
- **Comprehensive ablation study isolating component contributions:** Table 1 demonstrates that collapsing VLM and LLM into a single unified model causes catastrophic failure (0/10 on 5 of 6 tasks), and removing pose tracking causes failure on all complex tasks. The w/o Refinement ablation shows T1 drops from 4/10 to 0/10, and memory consistently boosts performance (e.g., T3: 9/10→10/10). These ablations go beyond typical system papers in rigorously isolating each component's contribution with controls that cleanly distinguish the roles of perception, strategy, refinement, and memory.
- **Inclusion of expert-designed cost baselines as upper bound:** The paper compares against both single-stage hand-designed costs and FSM-based expert costs (Table 1, lines 176–177), a comparison most LLM-for-robotics papers omit. The Expert FSM achieves the strongest overall performance, and CoRAL approaches it on several challenging tasks (T4: 9/10 vs. 10/10, T5: 9/10 vs. 10/10) while being fully automated — demonstrating that LLM-generated costs can recover much of the structure of carefully engineered objectives.
- **Quantified LLM contact strategy contribution:** The targeted ablation on T6 (Section 4.1.4) shows the guided approach is 83.9% faster (32 vs. 199 steps) with 63.9% shorter end-effector path (1.33 m vs. 3.69 m), providing concrete evidence that the LLM's symbolic contact strategy meaningfully prunes the MPPI search space.
- **Diverse task suite covering distinct contact-rich challenges:** Six tasks span multi-stage sequential reasoning (T1), force-controlled pushing (T4), environment-as-tool multi-contact reasoning (T5, T6), and clutter manipulation (T3).

## Weaknesses

### Fatal
None

### Major
- **Asymmetric baseline comparison with information-hungry VLAs:** CoRAL has access to known 3D object models *M* (line 65: "the known 3D geometric models of the objects, M, as input"), perfect force/torque feedback from MuJoCo (line 147–148: "force/torque data provided by the physics engine"), and a physics simulation "Planning World" for MPPI rollouts. The VLA baselines receive only RGB-D images and were trained on LIBERO pick-and-place demonstrations. The tasks are explicitly "designed to be difficult for purely vision-based, collision-avoidant planners" (line 155). This information asymmetry is not discussed in the results section, making the headline comparison somewhat uninformative about architectural superiority. The comparison shows VLAs fail on contact-rich tasks (expected given the asymmetry), but the performance gap may be largely explained by privileged physics access rather than LLM-based cost generation specifically. The Expert-Designed Cost baselines partially mitigate this by providing a model-based reference, but the paper should prominently acknowledge the asymmetry.

- **Figure 4 mass correction narrative contradicts its own evidence:** The text (line 220) states initialization with "a severely overestimated mass (2.0 kg vs. a ground truth of 0.1 kg)" and claims convergence "remarkably close to their true values" (line 222). However, the figure (lines 244–246) shows initial mass at 1.0 kg (not 2.0 kg) with corrected mass converging to ~0.85 kg — 8.5× the stated ground truth of 0.1 kg. The y-axis range (0.75–1.00) would not even display a 0.1 kg ground truth. Either the figure was not updated to match the text, or convergence to 0.85 kg is being mischaracterized as "remarkably close" to 0.1 kg. This undermines the robustness claim central to Section 4.1.4.

- **Simulation-only evaluation despite real-world deployment framing:** All experiments are in MuJoCo simulation. The paper claims CoRAL is "a cornerstone for deploying robots in unknown environments" (line 226) and designs a reactive control augmentation for "robustness against the inherent sim-to-real gap" (line 126), but provides no real-world experiments or sim-to-real transfer results. For a system relying on perfect force/torque readings from the physics engine, real-world performance could differ significantly.

### Minor
- **10 trials with no statistical testing:** All results use 10 trials per condition with no confidence intervals or significance tests. The memory ablation differences on T1 (2/10→4/10) and T6 (5/10→7/10) are within the noise of 10 binary trials. The claim that memory "consistently achieved the highest success rates" (line 210) cannot be statistically validated at this sample size.

- **LLM interaction protocol is underspecified:** The paper describes the LLM generating cost functions (Eq. 2) and contact strategies (Eq. 3) but provides no details on prompt format, output format, or how LLM outputs are parsed into executable code. This reproducibility-critical detail is absent.

- **FoundationPose requires known 3D models, limiting "zero-shot" claims:** FoundationPose takes "known 3D geometric models of the objects, M" as input (line 65). For truly novel objects, obtaining accurate 3D models is a significant prerequisite that limits practical applicability.

- **Expert FSM substantially outperforms CoRAL on hardest tasks:** On T1 (8/10 vs. 4/10) and T6 (9/10 vs. 7/10), the expert-designed FSM significantly outperforms CoRAL. While the paper frames this as "narrowing the gap" (line 197), the LLM-generated costs are meaningfully inferior to expert-designed ones on the tasks most central to the paper's thesis.

## Nice-to-Haves
- Compare against other model-based or MPPI-based approaches from the literature rather than only against end-to-end VLAs and internal expert baselines.
- Report closed-loop control frequency given K=200 rollouts over H=50 steps plus LLM API calls.
- Include failure mode analysis for tasks with high failure rates (T1: 6/10 failures) to diagnose whether failures stem from LLM reasoning, perception, or control.
- Increase trial count to 30+ and report confidence intervals for the ablation study.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **Harsh critic's "missing comparison with right baselines" (point 2):** Partially kept above, but weakened — the Expert FSM baseline does serve as a strong model-based reference. Missing external model-based comparisons is a nice-to-have, not a fatal gap.
- **Harsh critic's claim the comparison is "essentially a foregone conclusion":** Overstated. The comparison is informative and the paper's ablation study isolates CoRAL's specific contributions beyond just having physics models. The weakness is real but the framing is too strong.
- **Strength Finder's "explainability advantage" claim:** The paper only provides a single example of LLM failure diagnosis in an appendix. This is asserted rather than systematically demonstrated.
- **Strength Finder's "online parameter recovery" as a full strength:** The Figure 4 discrepancy significantly undermines this claimed strength. The concept is sound but the evidence is compromised.

## Novel Insights
The paper's key insight — that separating VLM perception from LLM strategy generation is critical rather than using a single multimodal model — is convincingly demonstrated by the Unified VLM ablation showing catastrophic failure (0/10 on 5 of 6 tasks). This finding that a single VLM cannot simultaneously handle precise 6-DoF pose estimation and strategic cost function generation is a genuinely useful contribution for the community designing modular robotic systems.

## Suggestions
- Address the Figure 4 discrepancy: either update the figure to match the 2.0 kg → 0.1 kg experiment, or update the text to match what the figure shows. If convergence to 0.85 kg is the actual result, honestly discuss the residual error.
- Add a paragraph explicitly acknowledging the information asymmetry between CoRAL and the VLA baselines (3D models, force feedback, physics simulation access).
- Include prompt templates and output parsing details, at minimum in an appendix.
- Increase trial count to enable statistical significance testing, particularly for memory unit claims.

## Reporting

**All anchor papers retrieved across rounds:**

Round 1:
- gwZ90hFSL2 (1.0) — off-topic NLP paper, not comparable
- Uj0h13lVrR (1.0) — GFlowNet theory paper, not comparable
- 8QTpYC4smR (1.0) — LLM survey paper, not comparable
- 5kMwiMnUip (1.4) — LLM jailbreaking, not comparable
- oyXoGJQlUf (3.0) — GRAIL: LLM for PDDL planning, rejected for weak evaluation in single domain
- Q6HYM1EMu8 (3.0) — LARG2: LLM for reward generation, rejected for weak evaluation
- EODzbQ2Gy4 (3.4) — Diff-Transfer: differentiable simulation skill transfer, rejected
- I0To0G5J7g (3.2/6.25) — Online Self-Improvement for Embodied Models, mixed scores
- WtHKqtHVXo (4.0) — Generating Robot Policy Code: LLM contact-rich manipulation, rejected for limited tasks and missing baselines
- iTsHStJKcm (5.25) — Make a Donut: language-guided deformable manipulation, rejected
- qGL6fE1lqd (4.4) — LLMPhy: physical reasoning with LLMs, rejected
- uaKBM9sGEm (4.0) — Off-Road Driving with MPPI, rejected
- c0chJTSbci (6.25) — SuSIE: zero-shot manipulation with diffusion models, accepted with real-world experiments
- MWHIIWrWWu (6.25) — MPC²: hierarchical model-based planning, accepted
- h7aQxzKbq6 (6.0) — HAMSTER: hierarchical VLA, accepted with real-world experiments
- lFYj0oibGR (6.5) — Vision-Language Foundation Models as Robot Imitators, accepted
- OI3RoHoWAN (8.0) — GenSim: generating robotic tasks via LLMs, accepted
- 7BLXhmWvwF (8.0) — Geometry-aware RL for Manipulation, accepted
- KsUh8MMFKQ (8.0) — Thin-Shell Object Manipulations, accepted
- pISLZG7ktL (8.0) — Data Scaling Laws in Imitation Learning, accepted

Round 2:
- gisAooH2TG (4.25) — RePLan: robotic replanning with LLMs/VLMs, very similar theme but rejected for weak evaluation (4 tasks, 3 trials) — CoRAL is clearly stronger
- JWrl5pJCnl (5.0) — Instruct2Act: multi-modal instructions to robotic actions, rejected
- Afjf6izLvJ (5.33) — Grounding Robot Policies, rejected
- u6imHU4Ebu (5.75) — LLaRP: LLM as generalizable embodied policy, accepted — most comparable to CoRAL
- 9pKtcJcMP3 (7.0) — Video Language Planning, accepted
- hQVCCxQrYN (6.67) — Plan-Seq-Learn: LLM-guided RL, accepted
- JVkdSi7Ekg (6.25) — AHA: VLM for failure detection, accepted
- KTtEICH4TO (4.75) — CORN: contact-based object representation, accepted but weak

**Round 1 bracket:** 5.0–6.5 (CoRAL is clearly above rejected papers at 3–5 range but below accepted papers at 6–7 range that have real-world experiments)

**Round 2 narrowing:** 5.0–6.0 (CoRAL is clearly above RePLan [4.25] which has very similar themes but weaker evaluation, and comparable to LLaRP [5.75] which was a weak accept)

**Final calibration:** CoRAL's ablation study is stronger than most papers in the 5–6 range, but the Figure 4 discrepancy and simulation-only evaluation hold it back from the 6–7 range where accepted papers typically have real-world experiments. The score sits at 5.5 — a borderline score reflecting solid architectural contributions held back by empirical concerns.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>