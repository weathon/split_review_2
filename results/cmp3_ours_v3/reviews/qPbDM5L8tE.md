Now I'll produce the final review.

## Summary

CoRAL proposes a modular neuro-symbolic framework for contact-rich robotic manipulation that separates VLM-based perception (pose tracking, physical parameter estimation) from LLM-based reasoning (cost function design, contact strategy, online adaptation). The LLM generates the structure of an MPPI cost function and biases contact-point sampling, while an outer loop allows the LLM to diagnose failures and correct its world model mid-execution. The architecture is evaluated on 6 simulated manipulation tasks (2 from LIBERO, 4 custom) against VLA baselines and expert-designed cost functions.

## Strengths

- **Principled modular architecture with strong ablation evidence.** The paper's central design choice — separating VLM for perception from LLM for reasoning — is convincingly validated by the Unified VLM ablation, which collapses to near-zero success on almost all tasks. This is the paper's strongest empirical result (Table 1: Unified VLM gets 0/10 on T1, T3, T5, T6).
- **Novel use of LLM for cost function structure and contact strategy.** Having the LLM generate the *form* of an MPPI cost function (Equation 2) and bias contact-point sampling (Equation 3), rather than producing waypoints or text plans, is a distinctive way to ground LLM reasoning in a low-level controller. The contact strategy ablation on T6 (83.9% faster, 63.9% shorter path) isolates this contribution.
- **Online adaptation loop is well-motivated.** The outer loop (Section 3.4), where the LLM diagnoses persistent failures and corrects its own world model (mass, friction), is a natural and potentially powerful capability. The demonstration of mass converging from 2.0 kg toward 0.1 kg (Figure 4) illustrates the mechanism clearly.

## Weaknesses

### Fatal
None.

### Major

1. **Statistically uninformative evaluation.** Every result in Table 1 is based on 10 trials with binary success/failure. No confidence intervals, standard deviations, or variance measures are reported. A change of 1 trial shifts a result by 10 percentage points. Several core claims rest on differences that could easily be noise: the memory benefit on T1 (4/10 vs. 2/10, i.e., 2 more successes), memory benefit on T3 (10/10 vs. 9/10, effectively ceiling), refinement benefit on T3 (10/10 vs. 3/10 — a larger gap but still within a 10-trial design). Research questions RQ1–RQ3 cannot be answered reliably from these data. The paper's central quantitative claims are built on an insufficient experimental foundation.

2. **Core method mechanism is underspecified.** The paper states the LLM "is free to introduce any cost terms constructible from the available state, pose, and action variables" and that Equation 2 "is only an illustrative example" (Section 3.2). But it does not specify: (a) how the LLM is prompted, (b) the output format (JSON? Python code? structured text?), (c) how the system communicates which state/pose/action variables are available for the LLM to reference, or (d) what the LLM-generated cost functions actually look like for any of the 6 evaluated tasks. Since LLM-generated cost functions are the paper's methodological centerpiece, this makes the method difficult to reproduce or assess.

3. **The comparison against end-to-end VLA models is structurally mismatched and overclaimed.** The paper claims CoRAL "significantly outperforms both state-of-the-art baselines" (Section 4.1.1), but CoRAL uses MPPI with 200 parallel MuJoCo rollouts per step, known 3D object models via FoundationPose, and GPT-4o for cost design — while OpenVLA-OFT and π_0.5 are feedforward policies mapping images directly to action tokens. The VLA models predictably fail on force-control tasks (T1, T4–T6) because they lack access to a simulator, known geometry, or an optimizer. This is a known limitation of feedforward imitation-learned policies. The valid comparison would be against other model-based approaches (VLMPC, IMPACT, or MPPI with learned cost functions), which are discussed in Related Work but never empirically compared.

4. **Modest absolute performance on the signature task.** On T1 (Push and Pick Cutting Board), the marquee multi-stage task, full CoRAL succeeds only 4/10 times — a 60% failure rate. The expert FSM baseline achieves 8/10. The paper frames this as "narrows the gap" (Section 4.1.2), but the headline claims about robustness and effectiveness should be read against this baseline: the proposed system fails more often than it succeeds on its own most challenging demonstration, and is outperformed 2:1 by a hand-designed FSM.

### Minor

5. **Mostly custom-designed tasks with limited standardized benchmark coverage.** The paper states it evaluates on "standardized benchmarks from the LIBERO suite" (Section 1), but only 2 of 6 tasks (T2, T3) are from LIBERO. The remaining 4 tasks are custom-designed. The tasks where CoRAL shows its largest advantage over VLA baselines (T4–T6) are precisely these custom tasks, and no argument is given for why they are more diagnostic than existing benchmarks.

6. **"Zero-shot" framing is overstated.** The paper defines zero-shot as "without task-specific training data," which is defensible, but the framing obscures substantial pre-requisites: known 3D geometric models of all interactable objects (for FoundationPose), a MuJoCo physics simulator for MPPI rollouts, hand-specified action spaces, and two pre-trained foundation models (GPT-4o and FoundationPose). This is a legitimate approach, but the "zero-shot" label obscures the engineering cost.

7. **Simulation-only evaluation.** Section 3.3 explicitly augments the controller to address the sim-to-real gap (Equation 7: reactive control with real-time force feedback), yet the system is never tested on hardware. A single real-world validation would substantially strengthen the claims about robustness.

8. **Completion time / computational cost tradeoff is not discussed.** CoRAL is 5–10× slower than VLA baselines on tasks all systems solve (T2: 45s vs. 5s; T3: 49s vs. 7–13s), and slower than expert single-stage cost baselines on several tasks (e.g., T4: 52s vs. 32s). This practical limitation of the MPPI-based approach is not acknowledged.

### Trivial
None.

## Nice-to-Haves

- Run at least 30–50 trials per condition and report confidence intervals or Bayesian credible intervals to support the core claims.
- Provide the exact LLM prompt templates, output format specification, and examples of LLM-generated cost functions for each task.
- Compare against VLMPC and/or IMPACT as more architecturally matched baselines.
- Include a real-world validation on at least one task.

## Removed Points

*These points were flagged during the review process but are not included in the final assessment for the reasons stated below.*

- **Criticisms about appendix content being unavailable.** The critic noted that "the appendix reference (A.3.2) is stripped by the parser" and that certain details could not be evaluated. The parser strips appendices from all submissions; the original paper contains this content. Removed per policy.
- **"Known property" claim about VLA limitations.** The critic characterizes the finding that VLA models fail on contact-rich tasks as "not a discovery." This is a judgment about significance rather than a verifiable flaw. The structural mismatch of the comparison is addressed in Weakness #3 above.
- **Formatting/style nitpicks.** Removed per policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Increase statistical power** to at least 50 trials per condition with confidence intervals. With only 10 binary trials, the margin of error is too large to distinguish signal from noise for the paper's core comparisons.
2. **Specify the LLM cost function interface completely.** Provide the full prompt template, the output format specification (e.g., JSON schema, code structure, or symbolic grammar), and at least two concrete examples of LLM-generated cost functions from the evaluated tasks. This is essential for reproducibility and for assessing the reasoning complexity the LLM actually exhibits.
3. **Re-baseline against model-based approaches.** Replace or supplement the feedforward VLA comparison with methods that share CoRAL's architectural affordances: MPPI with learned/designed cost functions, or the closest prior works (VLMPC, IMPACT) discussed in the Related Work.
4. **Acknowledge the infrastructure cost.** Replace or qualify the "zero-shot" framing with a description that honestly conveys the pre-requisites and engineering investment (known 3D models, simulator, pre-trained foundation models, hand-specified action spaces).
5. **Validate on real hardware** for at least one task, given that the paper explicitly addresses the sim-to-real gap.

## Score and Decision

### Calibration Details

**Retrieved anchors (all rounds):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks | 4.00 | R1 | Very similar topic (LLM + contact-rich manipulation). Rejected (1,5,5,5). CoRAL has better ablation evidence but similar evaluation weaknesses. |
| RePLan: Robotic Replanning with Perception and Language Models | 4.25 | R1 | Similar architecture (LLM+VLM+MPC/replanning). Rejected (6,3,3,5). Comparable weaknesses in trial count and task breadth. |
| LLMPhy: Complex Physical Reasoning Using LLMs and World Models | 4.40 | R1 | Similar approach (LLM+simulator for physical reasoning). Rejected (6,3,5,3,5). Comparable experimental limitations. |
| Wonderful Team: Solving Robotics Problems in Zero-Shot with VLLMs | 3.67 | R1 | Closest in framing (zero-shot robotics with foundation models). Rejected (5,3,3). Similar overclaim concerns. |
| Plan-Seq-Learn: Language Model Guided RL | 6.67 | R1 | Much stronger evaluation (25+ tasks, 85%+ success). Accepted (6,8,6). CoRAL is below this level. |
| On the Surprising Efficacy of Online Self-Improvement for Embodied Foundation Models | 6.25 | R2 | Real-world + simulated validation, stronger experiments. Despite higher score, rejected (5,10,5,5). CoRAL has substantially weaker empirical validation. |

**Round 1 bracket:** [3.5, 5.0]

**Final score determination:** After inspecting the full reviews of the most comparable anchor papers (Generating Robot Policy Code at 4.0, RePLan at 4.25, LLMPhy at 4.40, Wonderful Team at 3.67) and comparing evaluation breadth, statistical rigor, and baseline appropriateness, CoRAL sits in the middle of this peer group. It has a stronger ablation story than most (the Unified VLM collapse is compelling evidence for the modular architecture claim) and a genuinely interesting core idea. However, it shares the same fundamental weaknesses: insufficient trials for the claims made, no real-robot validation, an underspecified core mechanism, and a structurally mismatched SOTA comparison. It is well below the accepted papers in this space (Plan-Seq-Learn at 6.67 covers 25+ tasks). The final score of 4.0 reflects a paper with a novel and worthwhile idea presented with insufficient evidence to support its central claims.

**Score:** 4.0 — Reject  
**Decision:** Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>