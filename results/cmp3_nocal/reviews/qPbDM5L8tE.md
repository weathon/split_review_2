## Summary

CoRAL proposes a modular neuro-symbolic framework that uses an LLM to generate the structure and weights of an MPPI cost function, along with symbolic contact strategies, for contact-rich robotic manipulation. The system features a two-loop design: an inner high-frequency MPPI control loop and an outer low-frequency LLM-driven adaptation loop that refines the world model and plan upon persistent failure. The framework also includes a memory unit for experience reuse and uses FoundationPose for 6-DoF pose tracking. The core idea—using an LLM to formulate the optimization objective itself rather than just identify subgoals—is a meaningful architectural contribution.

## Strengths

1. **Novel architectural contribution.** Having the LLM generate the *structure and weights of an MPPI cost function* (Eq. 2) rather than merely identifying subgoals or objects (as in VLMPC) is a genuine step forward in bridging high-level symbolic reasoning with trajectory optimization. The two-loop design—inner MPPI loop for reactive control and outer LLM loop for reparameterization upon failure—gives the system a clean mechanism for correcting its own world model mid-task (Sec. 3.4).

2. **Ablation study is structured to test the paper's own claims.** The ablations (w/o Memory, w/o Refinement, Unified VLM, w/o Pose Tracking, Table 1) target each claimed contribution individually. The finding that disabling online refinement drops T1 success from 4/10 to 0/10 and disabling pose tracking collapses *all* tasks to 0/10 is informative and shows the components interact meaningfully.

3. **Contact strategy analysis on "Flip with Wall" (T6) provides concrete evidence of search-space pruning.** The comparison of guided vs. unguided MPPI on cost profiles and path lengths (Sec. 4.1.4) shows an 83.9% reduction in planning steps and 63.9% shorter end-effector path, giving direct evidence that the LLM's contact strategy actually prunes the search space rather than being epiphenomenal.

## Weaknesses

### Fatal
None.

### Major

1. **The VLA baseline comparison compares systems with fundamentally different information access, not different manipulation ability.** CoRAL uses (a) known 3D object models (required by FoundationPose, Sec. 3.1), (b) a physics engine (MuJoCo) for MPPI rollouts, (c) force/torque feedback from the simulator, and (d) GPT-4o for open-ended reasoning. The VLA baselines (OpenVLA-OFT, π₀.₅) receive only RGB images and are evaluated using LIBERO checkpoints fine-tuned on substantially different tasks (Sec. 4, Baselines). They lack object models, physics rollouts, force feedback, and the LLM. The paper frames this as showing "even fine-tuning an end-to-end policy is insufficient" for contact-rich tasks (Sec. 4.1.1), but this conflates a method comparison with an information-access comparison. The more informative comparison—CoRAL vs. expert-designed MPPI baselines that share CoRAL's planning infrastructure but lack the LLM—shows more modest gains (Table 1: expert FSM outperforms CoRAL on T1, T4, T5, T6). Calling the VLA comparison a "state-of-the-art comparison" rather than an *oracle-vs.-restricted-agent* comparison overstates what it demonstrates.

2. **The statistical basis for the headline results is extremely weak.** Every condition is evaluated on 10 trials with binary success/failure outcomes. No confidence intervals, error bars, or significance tests are reported anywhere in the paper (Table 1). With N=10, a 4/10 success rate has a 95% Clopper-Pearson CI of roughly [12%, 74%]—the true rate could be barely above zero or three-quarters. The paper's granular comparative claims (e.g., "memory boosted the success rate from 2/10 to 4/10," Sec. 4.1.3) rest on differences of 2 successful trials, which are not statistically distinguishable from noise under any standard test. This undermines the quantitative backing for the component-importance analysis.

### Minor

3. **The "zero-shot" claim requires qualification.** The term "zero-shot" appears throughout the paper (abstract, intro, contributions, methodology, experiments), but the system requires known 3D object models (input `M` to FoundationPose), a physics simulator for MPPI rollouts, force/torque feedback from the environment, and a Memory Unit that retrieves past successful episodes (Sec. 3.2). Running physics rollouts encodes prior knowledge about contact dynamics, and memory-based retrieval is, by definition, not zero-shot. The paper's intended meaning—"requires no task-specific teleoperated demonstration data"—is a reasonable contribution, but the unqualified "zero-shot" framing is likely to mislead readers about what the system presupposes.

4. **The core LLM interface mechanism is underspecified for reproducibility.** The paper's key claim is that the LLM generates cost functions (Eq. 2) and contact strategies (Eq. 3). However: (i) Eq. (2) is presented as "only an illustrative example" with the LLM "free to introduce any cost terms constructible from the available state"—no prompt format, output parsing mechanism, or error-handling for malformed outputs is described; (ii) Eq. (3) specifies contact regions via centers, radii, and tangent vectors, but how the LLM produces these spatial coordinates from its knowledge of the scene (pixel-space projection, coordinate regression, etc.) is not explained; (iii) the "State Metrics" fed to the outer loop (Sec. 3.4) are described only as a log of "states, actions, the contact strategies and cost functions that were used"—the exact structure and serialization format are absent. Without these details, the pipeline cannot be independently implemented or assessed for robustness.

5. **Control frequency is not reported.** The paper repeatedly describes the inner loop as operating at "high frequency" (Sec. 3.3, Fig. 2) but never reports the achieved control rate. Given that the system parallelizes K=200 MPPI rollouts and calls GPT-4o for the outer loop (which introduces API latency), the absence of timing information makes it impossible to assess real-time viability.

6. **No real-robot experiments.** The entire evaluation is conducted in simulation with clean force/torque sensing and idealized friction models. The sim-to-real gap for contact-rich tasks is well-known to be substantial. The paper acknowledges this as a limitation but does not include even a single real-robot validation, leaving the claims about "robust adaptive manipulation" ungrounded in physical hardware.

### Trivial
None.

## Nice-to-Haves

- **Increase trial count.** 10 trials per condition with binary outcomes is insufficient. 50+ trials or continuous metrics (e.g., completion progress) would substantially strengthen the quantitative claims.
- **Replace or redesign the "Unified VLM" ablation.** The current variant combines two changes (FoundationPose removal + role merging). A cleaner test would keep FoundationPose but merge the VLM (parameter estimation) and LLM (planning) roles into one model, isolating the effect of role separation from the effect of losing pose tracking.
- **Show an LLM-generated cost function verbatim** alongside the human expert's for at least one task. This would make the central technical contribution concrete and allow readers to understand where the gap in performance originates.

## Removed Points

These points from the input review were evaluated against the paper and removed with justification:

1. **"Unified VLM and w/o Pose Tracking ablations are straw-man comparisons"** — Partially factually incorrect. The critic claimed Unified VLM tasks GPT-4o with "estimating 6-DoF poses," but FoundationPose handles pose tracking in all variants; the ablation combines the VLM's *physical parameter estimation* with the LLM's *planning* into a single prompt, which is a legitimate test of the paper's modular separation claim (Sec. 4, Baselines). The "w/o Pose Tracking" ablation tests whether FoundationPose is necessary, which is a standard ablation for a system that claims it is critical.

2. **"Mass and friction cannot be visually estimated"** — The paper's outer-loop refinement mechanism (Sec. 4.1.4) explicitly addresses this limitation by correcting initial estimates online from physical outcomes. The criticism ignores the paper's own robustness analysis showing this correction in action.

3. **"No comparison to force-augmented VLA methods"** — The paper's scope is about LLM-driven cost generation, not force-based policy learning. The force-augmented methods cited in related work serve to contextualize the approach, and full empirical comparison is outside the stated scope.

4. **"The expert FSM still substantially outperforms CoRAL"** — The paper honestly presents this result (Sec. 4.1.2: "CoRAL narrows the gap to the expert... remaining below the FSM upper bound"). The contribution is automation of cost design, not surpassing human-engineered costs. No factual dispute.

## Novel Insights

The most insightful observation from the review process is that the paper's evaluation architecture conflates two distinct comparisons. The VLA baselines are information-starved relative to CoRAL (no object models, no physics rollouts, no force feedback), so their failure is overdetermined—it could stem from missing information, architectural differences, or both. The genuinely meaningful comparison is CoRAL vs. expert-designed MPPI, because both share the same planning infrastructure and differ only in whether the cost function is human-engineered or LLM-generated. This reframing clarifies that CoRAL's real contribution is automating cost-function design for MPPI controllers, not outperforming end-to-end VLAs on contact-rich tasks. The paper would benefit from leaning into this framing rather than leading with the VLA comparison.

## Suggestions

- Reframe the evaluation to lead with the human-expert MPPI comparison, which is the fair test of the LLM's contribution. Move the VLA comparison to a supplementary position with explicit caveats about asymmetric information access.
- Increase trial counts to at least 50 per condition for the main comparisons, and report confidence intervals or Bayesian credible intervals for binary success rates.
- Provide concrete details about the LLM interface: include the prompt template used for cost-function generation, the parsing/validation mechanism for LLM outputs, and the error rate for malformed responses.
- Report measured control frequency and outer-loop latency to substantiate the "high-frequency" claims.
- Show at least one LLM-generated cost function verbatim alongside the corresponding human-expert version to make the technical contribution concrete.

## Score and Decision

The core architectural idea (LLM-generated cost functions and contact strategies for MPPI) is genuinely novel and well-motivated. The two-loop design is clean, the ablation study is structured to test the paper's own claims, and the contact-strategy analysis on T6 provides credible evidence of search-space pruning. However, the evaluation has two significant weaknesses: (1) the headline VLA comparison is between systems with fundamentally asymmetric information access and therefore does not support the claimed "state-of-the-art" framing, and (2) the entire quantitative analysis rests on 10 binary trials per condition, which is insufficient to support the granular comparative claims about component importance. The paper's honest contribution—that LLM-generated cost functions can approach human-expert-designed MPPI controllers with no task-specific training—is valuable and plausible, but the evidence presented does not yet fully substantiate it.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>