## Summary

This paper introduces DemoGrasp, a framework for universal dexterous grasping that reformulates multi-task grasping as a single-step demonstration-editing MDP. Starting from one successful grasping demonstration, an RL policy learns to edit the demonstration along two axes (wrist SE(3) transform → *where* to grasp; delta joint angles → *how* to grasp), dramatically simplifying exploration and eliminating complex reward shaping. The policy is distilled into a vision-based policy via flow-matching imitation learning for zero-shot sim-to-real deployment. Results on DexGraspNet (95.2% state-based, 92.2% vision-based), six unseen object datasets across multiple embodiments (84.6% average), and real-world tests on 110 objects (86.5% overall, 71.1% on small/thin objects) demonstrate strong performance.

## Strengths

1. **The single-step MDP formulation via demonstration editing is genuinely novel and well-motivated.** Sections 2.2–2.3 articulate a clean idea: instead of exploring in the raw action space over a long horizon, the policy edits one demonstration along two axes. The fact that open-loop replay of the unedited demo already achieves 75% on the training set (Table 8) confirms the inductive bias is real.

2. **Strong and clean simulation results on DexGraspNet (Table 1).** DemoGrasp achieves 95.2% vs. 91.2% for UniGraspTransformer in the state-based setting, and 92.2% vs. 88.9% in the vision-based setting. The generalization gap between training and unseen categories (~1%) is materially smaller than the baselines (~3–5%).

3. **Real-world validation is unusually thorough.** 110 objects across varied categories with 5 trials each, including small (sub-3.5 cm diameter) and thin (sub-1.5 cm) objects. The 71.1% success rate on small/thin objects (Table 3) is a genuine empirical advance over prior work that struggles in this regime.

4. **Cross-embodiment results are informative.** Training one method on six different hand-arm systems (five-fingered, four-fingered, three-fingered, parallel gripper) without hyperparameter tuning and reporting results per dataset (Figure 3) is a strong demonstration of generality. The parallel gripper's expected failure on wide EGAD objects is acknowledged rather than hidden.

5. **Ablation studies are well-designed.** The action space ablation (Table 8) cleanly decomposes contributions: wrist rotation +13%, hand DoFs +2%, and all three components needed for best results. The demonstration-quality study (Table 9) convincingly shows robustness to which specific demonstration is used.

## Weaknesses

### Fatal

None.

### Major

1. **The DexGraspNet comparison with baselines is not apples-to-apples (Section 3.2).** The paper states: "the baseline methods do not randomize object initial positions, whereas our method is trained and tested with a large reset region of 50 cm × 50 cm" (line 131). This means evaluation protocols differ on a variable that directly affects task difficulty. The baselines are evaluated at a fixed object position; DemoGrasp is evaluated with position randomization. The paper frames this as "posing a challenge for spatial generalization" that DemoGrasp overcomes, but the more parsimonious reading is that the comparison conflates method quality with evaluation protocol differences. Without a controlled experiment — e.g., evaluating DemoGrasp *without* position randomization — the reported 4–5% margin in Table 1 cannot be cleanly attributed to the method. This does not invalidate the paper (the cross-dataset and real-world results independently support the method's strength), but it weakens the headline comparison.

2. **The RobustDexGrasp comparison (Table 2) is uncontrolled.** The paper acknowledges that RobustDexGrasp was "trained on different object datasets" (line 148). This means the comparison tests both method quality *and* training data quality simultaneously. Given that training data composition strongly affects generalization, the reported advantage on 4 of 5 datasets could partly reflect training data differences rather than method superiority. The paper's justification — "since both aim at universal grasping over arbitrary objects" — does not make the comparison controlled. This comparison is informative but should be caveated more strongly.

### Minor

1. **The "closed-loop" vision-based policy is somewhat underspecified relative to the single-step MDP formulation (Sections 2.3–2.4).** The paper describes the vision-based policy as "closed-loop" and claims it exhibits "regrasp behaviors to recover from failures" (line 173). However, the transition from the single-step RL teacher (which outputs editing parameters once per episode) to a per-timestep vision policy is not fully explained. The paper states it records "robot proprioception... robot actions, and rendered RGB or depth images from successful rollouts" (line 101) — which *does* provide per-timestep supervision from the full trajectory replay — so the mechanism is standard, but the main text could better clarify the vision policy's architecture and how it produces sequential actions. This is a clarity issue, not a technical gap.

2. **Equation (2) has an unaddressed edge case.** The hand pose interpolation uses elementwise division: (q_Tlift + Δq^G − q_0) / (q_Tlift − q_0). If any joint angle is at the same value at timesteps 0 and T_lift (denominator zero), the interpolation is undefined. The paper does not address this edge case or describe how joint limits are handled after the scaling of the delta.

3. **Motion planning dependency is not discussed.** The first step of demonstration replay requires "moving the end effector to p_0^\{*ee-obj\} under the new initial object frame via motion planning" (line 73). The paper does not discuss what happens when motion planning fails (e.g., due to kinematic constraints or collisions), how often this occurs, or how it is handled. For a method aimed at practical deployment, this is a relevant detail.

4. **Joint limits are not addressed.** The hand pose interpolation in Equation (2) can produce joint angles outside the feasible range. The paper contains no mention of clamping or projecting onto joint limits.

### Trivial

None.

## Nice-to-Haves

- A controlled experiment on DexGraspNet: evaluate DemoGrasp *without* position randomization (or with minimal randomization) and report those numbers alongside the baselines to make the headline comparison ironclad.
- Additional clarity on the vision policy architecture: specify whether the flow-matching policy predicts single-step editing parameters or per-timestep actions, and how the action chunking is structured.
- Discussion of motion planning failure rate and handling strategy.
- Discussion of how joint limit violations after interpolation are resolved.

## Removed Points

The following points from the input review were removed per filtering rules:

- *"Success criterion could conflate grasp stability with post-grasp hand positioning"* — Not framed as a flaw by the reviewer ("Not a flaw, but worth noting"). Removed as it is a neutral observation, not a weakness.
- *"Figure 3 / Table 10 identical numbers — cross-embodiment results not verifiable"* — The identical numbers are a tokenization/parser artifact (the actual data was in the radar chart image). Per hard rules, formatting artifacts from PDF extraction are removed.
- *"Sampling vs. RL ablation (Table 5) is stacked in RL's favor"* — The paper already acknowledges the multimodality issue and provides it as the motivation for using RL. Requesting additional baselines (dataset filtering, learned reward models) is beyond standard ablation practice. This is not a genuine weakness.
- *"Real-world trial count for cluttered scenes is small"* — The reviewer raised this as a caution, not a weakness. The 10-scene sample is small but consistent with simulation results. Not a substantive criticism.
- *"The gap between single-step teacher and per-timestep vision policy is a material gap"* — Downgraded from "material gap" to Minor after verifying that the paper records full trajectory data (per-timestep observations and actions) from rollouts, which provides standard per-timestep supervision for imitation learning. The reviewer's concern about *how* per-timestep supervision is obtained is answered by line 101 of the paper.

## Novel Insights

None beyond the paper's own contributions. The reviews affirm the paper's core claims without adding genuinely new analytical perspectives.

## Suggestions

1. **Run a controlled experiment on DexGraspNet:** Evaluate DemoGrasp under the same evaluation protocol as the baselines (fixed object position) and report the result alongside the existing numbers. This would either strengthen or honestly bound the headline claim.
2. **Clarify the vision policy architecture in 2–3 sentences:** Explain whether the vision policy produces per-timestep actions or single-step editing parameters, how it achieves closed-loop behavior, and what exactly "action chunking" means in this context.
3. **Address the Equation (2) edge case and joint limit handling:** Add a brief note on numerical stability and clamping behavior.
4. **Discuss motion planning in the main paper:** Even a sentence acknowledging that failures are rare and how they are handled would suffice.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>