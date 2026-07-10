Now let me compose the final review based on all verified information.

## Summary

This paper proposes CoRAL, a modular framework for contact-rich robotic manipulation that integrates a VLM (for perception and physical parameter estimation), an LLM (for generating cost functions and contact strategies for an MPPI controller), and a reactive control loop. The key architectural innovation is having the LLM formulate the structure and weights of the MPPI optimization problem itself — not just identify sub-goals — alongside a memory unit for experience reuse and an outer-loop adaptation mechanism for online refinement.

## Strengths

- **Well-motivated neuro-symbolic architecture.** Separating VLM (perception) from LLM (strategy) and feeding the LLM's output directly into an MPPI cost function is a clean design that advances beyond prior work (IMPACT, VLMPC) where foundation models played more limited roles. The two-loop architecture (inner reactive loop at high frequency, outer adaptation loop at low frequency) is clearly described and well-motivated.

- **Informative Unified VLM ablation.** The ablation showing that using a single model for both perception and planning fails catastrophically (0/10 on most tasks, Table 1) provides clear, direct evidence that the role separation between VLM and LLM is critical to performance.

- **Concrete contact-strategy analysis on T6.** The guided-contact-strategy analysis (Section 4.1.4) — showing 83.9% fewer steps and 63.9% shorter end-effector path — provides quantitative evidence for why the LLM's contact-strategy output helps, beyond what raw success rates alone capture.

## Weaknesses

### Fatal
None.

### Major

- **Factual error in the mass-adaptation claim.** The paper states that after online adaptation the estimated mass converged "remarkably close to their true values" (line 222), but the ground truth mass is stated as 0.1 kg (line 220) while Figure 4 shows the corrected mass plateauing at ~0.85 kg — a value 8.5× the ground truth and barely different from the initial estimate of 1.0 kg. There is also an internal inconsistency: the text says the initial evaluation-world mass was 2.0 kg while the figure clearly shows 1.0 kg. This error directly undermines one of the paper's central claims about the LLM's ability to correct physical parameters online.

- **Insufficient sample size for claimed "significant" improvements.** With N=10 trials per condition, the 95% confidence interval for a 4/10 success rate spans approximately 12%–74%. Key ablation comparisons (Memory vs. w/o Memory on T1: 4/10 vs. 2/10; on T6: 7/10 vs. 5/10; on T5: 9/10 vs. 7/10) are all well within chance variation. The paper uses "significantly" (line 234) to describe the 2/10→4/10 memory improvement without any statistical test.

- **LLM cost function generation is critically underspecified for reproducibility.** The paper states the LLM "is free to introduce any cost terms constructible from the available state, pose, and action variables" (line 91) without specifying the prompts used, how outputs are parsed, the space of permitted cost terms, or how the LLM is constrained to generate syntactically valid cost functions. The contact strategy generation (Eq. 3) similarly lacks detail on how the LLM identifies surface regions from object geometry.

### Minor

- **Asymmetric VLA comparison.** The primary comparison against OpenVLA and π0.5 is structurally unfair: CoRAL has access to known 3D object models, FoundationPose for 6-DoF tracking, a MuJoCo simulator for 200 parallel MPPI rollouts per step, force/torque sensor data, and human-designed controller components. The VLA baselines receive only pixels and output actions directly, and were fine-tuned on LIBERO (a pick-and-place benchmark, not contact-rich tasks). Their poor performance on contact-rich tasks is expected and does not serve as strong validation. The paper's more relevant comparison — against human-designed cost functions — should have been the primary framing.

- **Simulation-only evaluation limits robustness claims.** All experiments are conducted in MuJoCo simulation with no real-robot validation. The paper invokes the sim-to-real gap (line 126) as motivation for the reactive control term and as evidence of adaptation robustness (Section 4.1.4), yet never validates the system on a physical robot. Claims about "robustness" and "adaptive manipulation" are broader than the simulation-only evidence supports.

- **Overstated "expert-level" characterization.** On the hardest task (T1), CoRAL achieves 4/10 vs. the human-expert FSM baseline's 8/10 — a 50% success-rate gap. The paper's framing of "approaching expert-level performance" (line 197) overstates the results.

- **Uninformative "w/o Pose Tracking" ablation.** Removing FoundationPose and relying on the VLM for 6-DoF pose estimation sets up a straw-man comparison. VLMs are not designed for millimeter-precision pose tracking; their inevitable failure does not meaningfully inform the architecture design beyond confirming that a task-appropriate tool is needed.

### Trivial
None.

## Nice-to-Haves

- Run 50+ trials per condition (or report bootstrapped confidence intervals) for key ablation comparisons to make claims about improvement statistically meaningful.
- Add at least one real-robot demonstration on a simple task to substantiate claims about sim-to-real robustness.
- Provide the LLM prompt templates, output parsing code, and the space of permitted cost terms as supplementary material.
- Reframe the primary contribution around the LLM-generated cost/strategy comparison against human-designed costs, demoting the VLA comparison to a secondary motivating experiment.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **LIBERO tasks missing from Table 1**: The reviewer noted that "two benchmark tasks from the LIBERO suite" were mentioned but not explicitly identified in Table 1. However, T2 and T3 are standard pick-and-place tasks consistent with LIBERO-style benchmarks, and the VLA baselines use LIBERO checkpoints. This is not a real discrepancy.
- **Completion time comparison**: The reviewer noted CoRAL is slower than VLA baselines on simple tasks without discussion. This is secondary; the paper's focus is on contact-rich tasks where VLAs fail.
- **Missing related work**: Per policy, missing related works cannot be raised.
- **VLM mass estimation from appearance**: The reviewer noted mass is not visually inferable on real objects. This is a known limitation the paper partially acknowledges.
- **RAG implementation details**: Covered under the broader underspecification point.
- **Outer-loop LLM diagnosis capability**: A reasonable research question but not a flaw in the paper, which provides simulation evidence that the mechanism works.

## Novel Insights

None beyond the paper's own contributions. The reviews surfaced no insight that the paper itself does not already present about its architecture or findings.

## Suggestions

1. Correct the mass adaptation results: either provide a figure whose y-axis ranges down to the ground truth (0.1 kg) and shows actual convergence, or revise the text to honestly describe the magnitude of residual error.
2. Run at least 50 trials per condition for key ablation comparisons and report confidence intervals.
3. Add at least one real-robot demonstration on a contact-rich task to support claims about robustness to the sim-to-real gap.
4. Provide LLM prompt templates, parsing code, and the full space of permitted cost terms as supplementary material.
5. Reframe the primary contribution as "LLM-generated cost functions and contact strategies for MPPI" with human-designed cost as the main baseline, to more honestly reflect what the paper demonstrates.

## Score and Decision

The paper proposes a genuinely interesting architecture with clean design rationale. However, the experimental evaluation has several significant problems that prevent its claims from being well-supported. The factual error in the mass-adaptation analysis is particularly concerning, and the small sample size leaves most ablation comparisons statistically ungrounded. The method's underspecification affects reproducibility, and the simulation-only scope limits the practical claims. While the strengths are real, the evidential issues are substantial enough that the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>