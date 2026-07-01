Now I have all the verification I need. Let me produce the final consolidated review.

## Summary

CoRAL is a modular neuro-symbolic framework for contact-rich robotic manipulation that decouples perception (VLM → physical parameter estimation + FoundationPose for tracking) from planning/reasoning (LLM → MPPI cost functions and contact strategies). The system adds an outer-loop LLM-driven refinement mechanism that corrects both world model parameters and planning strategy based on execution failures, plus a RAG-based memory unit for experience reuse. Evaluated on 6 simulated Robosuite tasks.

## Strengths

1. **The decoupling hypothesis is well-motivated and tested.** The paper makes a clear argument (lines 37–45) for why threading everything through a single end-to-end policy is suboptimal for contact-rich tasks requiring explicit physical reasoning. The "Unified VLM" ablation (which collapses perception and planning into one model) catastrophically fails (0/10 on most tasks), providing concrete evidence that the architectural separation matters.

2. **The online adaptation loop (outer loop) is a genuine architectural contribution.** The LLM-driven refinement mechanism (Section 3.4), where the LLM diagnoses failures from logged episode data and corrects both world model parameters and cost/contact strategy, is a concretely implemented capability. The w/o Refinement ablation showing a drop from 4/10 to 0/10 on T1 and 9/10 to 3/10 on T3 demonstrates real value.

3. **The LLM-guided contact strategy ablation on T6 is clean and well-executed.** Isolating the contribution of the contact strategy (C₀) vs. just the cost function (J₀) on the "Flip with Wall" task (Section 4.1.4) shows an 83.9% reduction in steps and 63.9% shorter path. This concretely demonstrates that biasing MPPI sampling toward semantically meaningful contact regions prunes an otherwise intractable search space.

4. **The human expert cost baselines provide a meaningful upper bound.** The Expert (FSM) baseline (hand-designed finite-state machine with phase-specific costs) and single-stage variant give a calibrated anchor for interpreting CoRAL's performance. CoRAL approaches but does not match the FSM expert, which is an honest positioning of the method's capability.

## Weaknesses

### Major

1. **The comparison against OpenVLA and π₀.5 is fundamentally asymmetric and does not support the claims drawn from it.** The "state-of-the-art baselines" are tested using their **LIBERO-OBJECT** and **LIBERO-GOAL** checkpoints (line 163) — weights fine-tuned for a specific distribution of 10 LIBERO tasks. The CoRAL tasks (T1–T6) are custom Robosuite tasks that are *not* in the LIBERO training set. Meanwhile, CoRAL has: (a) known 3D object models (M) provided as input, (b) a GPT-4o LLM with prompt engineering for cost functions on *these specific tasks*, (c) an MPPI planner with explicitly tuned hyperparameters, and (d) a dedicated pose tracker requiring known object geometry. The paper claims this tests "CoRAL's zero-shot capabilities against powerful policies" (line 163) and concludes that "VLA models fail at contact-rich reasoning" (line 193), but the experiment only shows that *pre-trained LIBERO checkpoints* applied zero-shot to a *different task distribution* perform poorly — which is expected and does not support broad conclusions about the VLA paradigm. The paper would need either (a) a VLA model fine-tuned on these same tasks, or (b) a comparison on LIBERO tasks where the VLA baselines have relevant training data, to support its claims. The human expert baselines are informative, but the VLA comparison as presented is misleading. *(Verified: lines 163, 193)*

2. **The figure-text inconsistency in the parameter adaptation evidence undermines the quantitative claim.** In the "Robustness of Online Parameter Adaptation" section (line 220), the text states the *Evaluation World* was initialized with a mass of **2.0 kg** vs. a ground truth of **0.1 kg**. However, Figure 4 (line 244) shows a y-axis ranging **0.75–1.00 kg**, an "Initial Mass" dashed line constant at **1.0 kg**, and a "Corrected Mass" solid line that starts at 1.0 kg and drops only to **~0.85 kg**. The initial estimate, ground truth, and corrected value in the figure do not match the text. The corrected value (0.85 kg) is nowhere close to the text's claimed ground truth (0.1 kg), so the claim that "the agent's belief about both mass and friction converged remarkably close to their true values" (line 222) is unsupported by the figure presented. This is not a formatting artifact — the figure and text describe clearly inconsistent experiments. *(Verified: lines 220–222 vs. 244–248)*

### Minor

3. **Low statistical power with no variance reporting.** Every reported result uses N=10 trials with binary success/failure outcomes. At N=10, the difference between CoRAL (4/10) and CoRAL w/o Memory (2/10) on T1, or between CoRAL (4/10) and Expert FSM (8/10), is not statistically distinguishable from noise. Completion times are reported as means without standard deviations, confidence intervals, or any measure of variance (Table 1). While N=10 is common in robotics manipulation evaluations, the paper should either report uncertainty intervals or explicitly acknowledge the limited precision of the comparisons. *(Verified: line 155, Table 1)*

4. **Overbroad claim about VLAs in the Introduction.** The paper states "existing VLA frameworks struggle to effectively handle contact-rich manipulation tasks" (line 13) as a blanket claim, without acknowledging that works specifically targeting contact-rich VLA are cited in the Related Work (ForceVLA, TLA, VLA-Touch, RDP, FACTR — line 45). This framing sets up a straw version of VLAs. *(Verified: line 13, line 45)*

5. **The memory unit's demonstrated effect is modest.** The paper claims memory enables "generalization and efficient reuse of learned contact strategies and parameter adjustments across diverse manipulation scenarios" (line 31). The actual improvement from memory is 2/10 → 4/10 on T1 and 9/10 → 10/10 on T3 (Table 1). While positive, this is too narrow to support the claimed "generalization across diverse scenarios." *(Verified: line 31, Table 1)*

6. **The paper mentions two LIBERO benchmark tasks (line 151) but never identifies which of T1–T6 they are.** The task descriptions list six custom tasks (line 155) without labeling any as LIBERO tasks. This makes it impossible to assess the claim that LIBERO-standard tasks are part of the evaluation. *(Verified: lines 151, 155)*

### Trivial

7. The feedback gain matrix K_f in the reactive control term (Eq. 7) is not specified — it is unclear whether it is tuned, learned, or set to a constant.

## Nice-to-Haves

- A computational cost breakdown (time per MPPI cycle, LLM inference latency, outer-loop invocation frequency) would inform practitioners about real-time feasibility.
- Specifying the API constraints between the LLM and the MPPI parser would clarify what "any cost terms constructible from the available state" (line 91) actually means in practice.
- A real-world validation experiment, even on a single task, would significantly strengthen the sim-to-real robustness claims (line 126).

## Removed Points

- **"Ablation design stacks the deck" (from original review, Issue 4):** The reviewer claimed the w/o Pose Tracking and Unified VLM ablations test "extreme versions." However, these ablations test directly whether the paper's core design choices (dedicated pose estimator, role separation) are necessary — which is exactly the purpose of an ablation. Replacing FoundationPose with VLM-only pose estimation is a meaningful comparison (many systems attempt this), and testing a unified VLM for everything tests the paper's central decoupling hypothesis. This criticism is not valid. **Removed.**

- **"The memory unit's effect is visible" (from original review, Strength 4):** This strength was generic and superficial. The memory improvement is 2→4 on T1 — a modest effect that is better noted as a limitation (see Minor weakness 5). **Removed.**

- **Criticism about "missing appendix" or references to appendix content:** The parser strips appendix pages from all papers; references to missing appendix material (e.g., "Appendix A.3.2", "Appendix ??") reflect a known parsing artifact and do not indicate an author omission. **Removed.**

- **Criticism about undisclosed hyperparameters (beyond what is reasonable):** The paper specifies λ=0.1, H=50, K=200, N_retry=15, the API model (GPT-4o), and hardware. This level of detail is standard. **Removed.**

## Novel Insights

None beyond the paper's own contributions. The reviews surface the figure-text inconsistency and the structural asymmetry in the VLA comparison, but raise no fundamentally novel insight about the method itself or its theoretical underpinnings.

## Suggestions

1. **Redesign or remove the VLA comparison.** Either: (a) fine-tune a VLA model on these same tasks for a fair comparison, or (b) evaluate CoRAL on LIBERO tasks where the VLA baselines have relevant training, or (c) drop the VLA baselines entirely and focus on the human expert and ablation comparisons, which provide a more honest assessment of the method's value.

2. **Fix the Figure 4 inconsistency.** Clarify whether the figure depicts the same experiment described in the text. If the mass correction experiment achieved convergence to ~0.1 kg, present that data. If Figure 4 is from a different configuration, label it accordingly and provide the correct figure.

3. **Provide confidence intervals, standard deviations, or significance tests** for the main comparisons (at least for completion times). Acknowledge the limited precision of N=10 binary outcomes.

4. **Tone down the claims about VLAs** in the Introduction and Results sections to reflect what the evidence actually supports: that pre-trained LIBERO checkpoints fail zero-shot on novel contact-rich tasks, which is a weaker claim than "VLAs cannot handle contact-rich manipulation."

5. **Identify which tasks are the LIBERO benchmarks** in the task descriptions rather than mentioning them only in the environment setup paragraph.

## Score and Decision

<score>5.5</score>
<decision>Borderline (revise and resubmit)</decision>