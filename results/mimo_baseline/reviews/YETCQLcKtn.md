## Summary

PolicyFlow is an on-policy reinforcement learning algorithm that replaces Gaussian policy parameterizations with continuous normalizing flows (CNFs) within a PPO-style framework. Its two main technical contributions are: (1) an importance ratio approximation that evaluates velocity field variations along a linear interpolation path instead of simulating full ODE trajectories during training, and (2) a Brownian-inspired entropy regularizer that encourages the learned velocity field to follow entropy-increasing dynamics without requiring expensive log-likelihood computation. Experiments across MultiGoal, MuJoCo Playground, and IsaacLab benchmarks demonstrate competitive or superior performance relative to PPO, FPO, and DPPO.

## Strengths

- **Novel and efficient importance ratio approximation.** The key insight that Gaussian likelihood ratios are shift-invariant (Eq. 8), combined with approximating the terminal shift via velocity field variations along a linear interpolation path (Eq. 10), provides a computationally practical way to integrate CNFs into PPO-style updates. This avoids full ODE simulation and path-wise backpropagation during training, which is the primary barrier to using expressive flow policies in on-policy RL. The approach is well-motivated and the resulting algorithm (Algorithm 1) is clean.

- **Principled entropy regularizer for flow-based policies.** The Brownian regularizer (Eq. 15-16) addresses a genuine gap in the literature—entropy regularization for flow-based policies where log-likelihoods are intractable. By leveraging the relationship between velocity fields and score functions (Eq. 14), the regularizer enforces entropy-increasing dynamics without expensive divergence computation. The MultiGoal experiment (Fig. 2) convincingly demonstrates that this regularizer produces substantially more diverse, multimodal behavior compared to alternatives (uniform noise injection, Gaussian entropy alone, DPPO, and FPO).

- **Comprehensive experimental evaluation.** The paper evaluates PolicyFlow across three distinct benchmark suites (MultiGoal for multimodality, MuJoCo Playground for continuous control, IsaacLab for robotics), includes ablation studies on clipping range, initialization strategy, time sampling, and interpolation paths, and provides per-iteration training time comparisons. The use of 5 random seeds with standard error and p-values in Table 1 strengthens the empirical claims.

## Weaknesses

### Fatal
None.

### Major

- **Approximation quality is environment-dependent and potentially fragile.** The linear interpolation path (Eq. 9) between the latent variable z and the terminal point φ₁ replaces the actual ODE trajectory. When the learned velocity field is complex or highly nonlinear, this linear path can diverge significantly from the true flow trajectory, making the velocity field variation along it a poor proxy for the actual terminal shift δφ₁. The paper provides an error bound claim (Eq. 11) but states the details are in an inaccessible appendix; without being able to verify the assumptions (e.g., smoothness conditions on the velocity field, Lipschitz constants), it is difficult to assess how tight this bound is in practice. Some empirical evidence on when the approximation degrades (e.g., on harder tasks or with larger policy updates) would strengthen the paper.

- **Incomplete baseline comparison on IsaacLab.** The comparison on IsaacLab omits FPO and DPPO, justified by framework differences (JAX vs PyTorch). While this is a practical concern, it substantially limits the paper's ability to claim that PolicyFlow outperforms these SOTA methods across all benchmarks. The MuJoCo Playground results show PolicyFlow and FPO are often close in performance, so the IsaacLab comparison with only PPO cannot substantiate the stronger claims in the abstract ("competitive or superior performance compared to... FPO and DPPO").

### Minor

- **The Brownian regularizer's theoretical justification is acknowledged to be inexact.** The authors themselves note (Remark, Section 4.1) that the velocity field is not obtained via flow matching gradients, so it does not strictly correspond to rectified flow dynamics. This self-awareness is commendable, but it means the connection between Eq. 14 and the actual policy velocity field is heuristic. The empirical results clearly show the regularizer works, but a more rigorous characterization of when and why this approximation is valid would strengthen the contribution.

- **Statistical significance on MuJoCo Playground is not reported.** Table 1 provides p-values for IsaacLab comparisons, but the MuJoCo Playground results (Fig. 3) show only means with standard errors. Given that some curves appear to overlap substantially (e.g., PolicyFlow vs. PPO on BallInCup, CheetahRun), reporting statistical significance or at least final performance numbers with confidence intervals would make the claims more rigorous.

- **Training time overhead could be more thoroughly characterized.** Table 2 shows per-iteration times on an RTX 5090, but the comparison would benefit from breaking down where the overhead comes from (interpolation computation, extra forward passes, etc.) and whether total wall-clock time to convergence (not just per-iteration) is favorable.

### Trivial
- Minor notation inconsistencies between the paper body and algorithm pseudocode (e.g., φ̂_k vs φ₁ notation).

## Nice-to-Haves

- A failure case analysis or discussion of when PolicyFlow underperforms would be valuable for practitioners deciding when to use this approach versus standard PPO or other baselines.
- Evaluating on harder locomotion or manipulation tasks where the expressiveness of CNF policies would provide a more decisive advantage over Gaussian policies.

## Novel Insights

The paper's most novel insight is that the shift-invariance of Gaussian log-likelihood ratios can be exploited to avoid simulating full ODE trajectories during PPO-style training—only the velocity field at interpolated points along a simple linear path is needed. This transforms the computational complexity of using CNF policies in on-policy RL from ODE-simulation-heavy to nearly lightweight, which is a practically important observation for the flow-based RL community. The connection between Brownian motion dynamics and entropy regularization for flow policies, while approximate, offers a conceptually clean alternative to existing approaches.

## Suggestions

- Provide a more detailed theoretical analysis of the approximation quality, possibly including conditions under which the interpolation-based approximation is tight or loose, and empirical diagnostics (e.g., measuring the actual approximation error during training).
- Include FPO and DPPO baselines on IsaacLab by reimplementing the core algorithmic components in PyTorch, or at minimum discuss the expected relative performance based on the MuJoCo Playground trends.
- Report final converged performance with confidence intervals and significance tests for MuJoCo Playground, consistent with the IsaacLab analysis.

## Score and Decision

The paper presents a well-motivated and practically useful algorithm for integrating CNF policies into PPO-style on-policy RL. The core technical ideas (importance ratio approximation via velocity field variations and the Brownian regularizer) are novel and address real challenges. The experimental evaluation is broad and generally convincing, though incomplete baseline comparisons on IsaacLab and unverifiable theoretical claims (due to the removed appendix) temper the strength of the contribution. Overall, this is a solid methodological contribution that advances the state of expressive policy optimization in online RL.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>