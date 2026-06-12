## Summary

The paper proposes CoRAL, a modular framework for zero-shot contact-rich robotic manipulation that integrates vision models (FoundationPose + VLM) for perception, an LLM for formulating MPPI cost functions and contact strategies, a reactive MPPI controller for execution, and a memory unit for experience retrieval. The key contribution is the explicit separation of perception and reasoning roles, along with an online adaptation loop where the LLM can diagnose execution failures and refine both world model parameters and control strategies.

## Strengths

- **Well-motivated architectural decomposition**: The explicit separation of VLM (perception/parameter estimation) from LLM (reasoning/strategy formulation) is a principled design choice, and the ablation study strongly validates it—the Unified VLM variant fails catastrophically (0/10 on 4 of 6 tasks), clearly demonstrating that role separation is not merely a convenience but a necessity.

- **LLM-formulated cost functions for MPPI is a genuinely novel idea**: Having the LLM directly specify the mathematical structure of the MPPI cost function (Eq. 2) and propose contact strategies that bias sampling (Eq. 3) creates a compelling bridge between high-level commonsense reasoning and low-level optimal control. This goes beyond using LLMs merely as planners or code generators.

- **Comprehensive and well-designed ablation studies**: The paper systematically removes each component (Memory, Refinement, Pose Tracking, Unified VLM) and clearly isolates each contribution. The results are internally consistent: removing refinement drops T1 from 4/10 to 0/10, removing pose tracking causes complete failure across all tasks, and removing memory degrades performance across the board. This is rigorous experimental design.

- **Comparison against expert-designed costs**: Including human-designed single-stage and FSM-based cost baselines provides a useful upper-bound reference, showing that CoRAL approaches expert-level performance on the hardest tasks while requiring no manual engineering.

- **Online parameter adaptation is convincing**: The demonstration that the LLM can diagnose physical parameter misestimation (mass, friction) from execution failures and converge toward true values (Section 4.1.4) demonstrates a meaningful form of closed-loop reasoning that goes beyond static planning.

## Weaknesses

### Fatal
None.

### Major

- **Simulation-only evaluation undermines key claims**: The paper repeatedly emphasizes handling the "sim-to-real gap" and "unknown environments," yet all experiments are conducted in MuJoCo simulation where the physics model is perfectly accessible to the controller. The reactive control augmentation (Eq. 7) and force/torque feedback are presented as sim-to-real solutions but are never validated on a real robot. This is a significant gap for a contact-rich manipulation paper, where real-world physics uncertainty is the primary challenge.

- **Unfair baseline comparisons**: The VLA baselines (OpenVLA-OFT, π₀.₅) are evaluated without force/torque feedback, reactive control augmentation, or the ability to reformulate objectives online—capabilities that CoRAL's architecture provides by design. This conflates the contribution of LLM-based reasoning with the benefit of having a full reactive control stack. A fairer comparison would either give VLAs access to similar low-level control capabilities or strip CoRAL down to open-loop execution.

- **Low sample size with no statistical analysis**: Only 10 trials per task condition with binary success/failure outcomes. The difference between 4/10 and 2/10 (T1 with/without memory) or 9/10 and 7/10 (T5) is not statistically distinguishable at any reasonable significance level. No confidence intervals, error bars, or significance tests are reported, making it difficult to assess whether observed differences are meaningful.

- **Critical implementation details are missing**: The paper does not explain how the LLM's textual output is parsed into executable MPPI cost functions and geometric contact parameters. How does a GPT-4o text response become the structured cost in Eq. 2 with specific weight values? How are tangent vectors and radii in Eq. 3 extracted from LLM output? This parsing/translation step is arguably the most technically challenging part of the system and is essentially a black box.

### Minor

- **Figure 4 narrative doesn't match the figure**: The text describes initializing mass at 2.0 kg (ground truth 0.1 kg) for a severe misestimation demonstration, but the figure shows mass going from 1.0 to ~0.85 kg with a y-axis range of 0.75–1.00. This discrepancy undermines a key result.

- **Heavy dependence on proprietary GPT-4o API**: All perception and reasoning relies on GPT-4o, raising concerns about reproducibility, cost, latency, and long-term availability. The paper does not report LLM inference latency, which could be substantial given the multiple LLM calls per task.

- **Memory retrieval mechanism is underspecified**: The RAG-based memory unit is described abstractly. What embedding space is used? How is similarity thresholded? How many experiences are stored/retrieved? The impact of memory is shown quantitatively, but the mechanism itself remains opaque.

- **Limited comparison with related LLM+robotics frameworks**: The paper does not compare against other LLM-based manipulation systems like SayCan, Code as Policies, or VoxPoser, which share the philosophy of using foundation models for robotic control.

### Trivial
None beyond parser artifacts.

## Nice-to-Haves

- A real robot demonstration, even on one or two tasks, would substantially strengthen the paper's claims about handling real-world contact dynamics and sim-to-real gaps.
- Adding error bars and statistical significance tests to Table 1 would make the results far more convincing.
- A comparison where VLAs are augmented with similar reactive control capabilities (or CoRAL is stripped of them) would cleanly isolate the contribution of LLM-based reasoning.

## Novel Insights

The paper's most novel observation is that an LLM can directly formulate the mathematical structure of a model predictive control cost function—not just select from predefined terms, but specify weights, add new terms, and propose geometric contact strategies that bias the planner's sampling. This creates a tight coupling between commonsense reasoning and optimal control that is qualitatively different from using LLMs as high-level planners that output symbolic actions. The ablation demonstrating that this formulation is critical (guided trajectories are 84% faster than unguided on the wall-flip task) provides concrete evidence that LLM reasoning can meaningfully reduce the search space in contact-rich planning problems.

## Suggestions

- Add a real robot experiment section, even limited, to validate the core claims about contact-rich manipulation in physical settings.
- Report per-task LLM/VLM inference latency separately from MPPI computation time to characterize the system's real-time capabilities.
- Provide detailed specification of how LLM outputs are parsed into executable cost functions—this is a critical and non-trivial system component.
- Include statistical tests (e.g., bootstrap confidence intervals or binomial tests) alongside the 10-trial success rates.
- Design a comparison where VLA baselines have access to force feedback and reactive control to isolate the LLM reasoning contribution.

## Score and Decision

The paper presents a genuinely novel architectural idea (LLM-formulated MPPI cost functions with separated VLM/LLM roles) supported by strong internal ablations. However, the evaluation is limited to simulation with unfair baseline comparisons, small sample sizes, and missing critical implementation details. The core contribution is promising but the evidence does not yet fully support the claims.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject