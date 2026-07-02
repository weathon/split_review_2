## Summary

This paper unifies four diverse problem domains—robust optimization, global optimization, polynomial root-finding, and sampling—under the homotopy paradigm, revealing their common predictor-corrector (PC) structure. It then proposes Neural Predictor-Corrector (NPC), a reinforcement learning framework that replaces hand-crafted heuristics for step sizes and termination criteria with learned adaptive policies. NPC is trained offline on a distribution of problem instances and deployed without per-instance fine-tuning. Experiments on four representative tasks show that NPC consistently reduces iterations and runtime while maintaining solution quality compared to classical and specialized baselines.

## Strengths

- **Unified perspective**: The paper clearly articulates how four seemingly distinct problems share a common homotopy-based PC structure, enabling a single algorithmic framework rather than separate per-domain solvers.
- **Novel RL formulation**: Treating predictor step size and corrector termination as sequential decisions and learning them via RL is a natural and well-motivated approach that addresses a genuine limitation of existing heuristics.
- **Amortized training**: The one-time offline training over a distribution of instances, followed by zero-shot deployment on unseen instances, is practically appealing and demonstrated across all four tasks.
- **Comprehensive experimental evaluation**: The method is tested on four different homotopy problems with multiple baselines per task, including both classical and learning-based competitors, and the results consistently show substantial efficiency gains (70–90% reduction in iterations/runtime) with comparable accuracy.
- **Ablation study**: The ablation of RL state components (Table 6) provides clear evidence that each component contributes meaningfully to the learned policy.

## Weaknesses

### Fatal
None.

### Major
- **Limited problem scale**: All experiments are on relatively small-scale problems (2D optimization benchmarks, small polynomial systems, low-dimensional sampling). The paper does not demonstrate scalability to higher-dimensional or more complex instances, which is critical for a general-purpose solver claim.
- **State computation overhead**: The state includes “convergence velocity,” which requires computing the objective value or KSD at each step. The paper does not account for this overhead in runtime comparisons, potentially overstating efficiency gains. For sampling, KSD computation can be expensive.
- **Reward design sensitivity**: The reward balances accuracy (based on convergence velocity) and efficiency (corrector iterations). No analysis is provided on how the coefficients λ₁, λ₂ affect the learned policy or whether the reward signal is robust across different problem classes.
- **Incomparable baselines**: For polynomial root-finding (Simulator HC in C++) and sampling (iDEM on a more powerful GPU), runtime comparisons are explicitly marked as not directly comparable, weakening the efficiency claims against these methods. The paper still uses these comparisons to support its conclusions.

### Minor
- **Neural network capacity**: The policy network is a small MLP (2 layers, 16 units each). While sufficient for the tested problems, it is unclear whether this capacity generalizes to more complex homotopy landscapes.
- **Generalization scope**: Training is done on a single instance (GNC point cloud registration) or a narrow distribution (Ackley with randomized parameters, 4-view triangulation). The paper does not test generalization to substantially different problem distributions within the same class.
- **No failure case analysis**: The paper reports success rates of 100% for polynomial root-finding but does not discuss scenarios where NPC might fail (e.g., highly ill-conditioned trajectories) or compare failure modes with classical methods.
- **Hyperparameter reporting**: The reward coefficients λ₁, λ₂ are referenced to Appendix A but not given in the main text, making it harder to assess the reward design at a glance.

### Trivial
- The term “Homotopy” is capitalized inconsistently in the title and body.

## Nice-to-Haves

- Analysis of the learned policy behavior: e.g., how does the step size Δt vary along the homotopy path for different problem instances? Does the policy learn to take larger steps in smooth regions and smaller steps near sharp transitions?
- Comparison with an oracle that knows the optimal step-size schedule (e.g., derived from the curvature of the solution trajectory) to quantify the gap between learned and optimal policies.
- Application to a higher-dimensional problem (e.g., 10D optimization or larger polynomial systems) to demonstrate scalability.

## Novel Insights

The paper’s core insight is that the predictor-corrector structure common to many homotopy solvers can be cast as a sequential decision-making problem amenable to RL. While the unification of these four domains under the homotopy paradigm is more of a conceptual reframing than a technical novelty, the demonstration that a single RL policy can replace domain-specific heuristics and generalize across instances within each domain is a valuable empirical finding. The ablation study further confirms that the chosen state variables (homotopy level, corrector statistics, convergence velocity) are all informative for efficient control.

## Suggestions

- Provide a detailed analysis of the computational cost of computing the state (especially convergence velocity) and include it in the runtime comparisons.
- Perform a sensitivity analysis on the reward coefficients λ₁, λ₂ to show how they affect the efficiency-precision trade-off.
- Test NPC on at least one higher-dimensional problem (e.g., 10D Ackley or a larger polynomial system) to give evidence of scalability.
- Include a discussion of failure cases or conditions under which the learned policy might underperform classical heuristics.

## Score and Decision

The paper presents a novel and well-motivated framework that unifies several homotopy problems and applies RL to learn adaptive solver policies. The experiments are thorough across four tasks and demonstrate clear efficiency gains. However, the limited problem scale, unaccounted state computation overhead, and sensitivity of the reward design are notable concerns that prevent the paper from being a strong accept. The contribution is solid but incremental, and the evidence supports acceptance with minor reservations.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>