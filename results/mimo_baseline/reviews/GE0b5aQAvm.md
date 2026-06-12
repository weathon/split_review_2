## Summary

This paper claims to prove that neural (nonlinear) policy ensembles are inherently sub-optimal compared to linear policy ensembles in control settings. It presents three main theoretical results: (1) neural ensembles are sub-optimal on linear systems relative to linear ensembles, (2) neural ensembles can violate stability even when individual policies are stable, and (3) using neural networks to mix optimal linear policies is sub-optimal. These claims are supported by experiments on multi-regime linear dynamical systems and benchmark control tasks.

## Strengths

- **Well-posed research question.** The paper tackles an important and under-studied question about the fundamental limitations of neural policy ensembles versus linear ensembles, with implications for RL, Mixture-of-Experts, and agentic AI. The question is timely given the growing use of neural policy ensembles.

- **Mathematical formalism.** The paper presents a clean mathematical framework using optimal control formulations (HJB equations, CLFs, Riccati equations) and defines formal measures like the nonlinearity measure κ(π, D) (Eq. 8) and suboptimality gap Δ(π, x) (Eq. 7). This structure provides a foundation for formal reasoning about ensemble properties.

- **Theorem 3 (Convexity Advantage).** The result showing that convex mixing of linear policies is optimal with equality iff w = λ (Corollary 1) is a clean, well-motivated result with a tight characterization of the performance penalty. The proof structure appears sound for LQR systems.

- **Comprehensive empirical validation.** The experiments cover multiple dimensions: diversity levels, switching patterns (slow, fast, clustered, cyclic, random), multiple control tasks, and statistical significance testing with p-values and multiple seeds. The experimental design in Section 4.1 (three regimes with different control objectives: tracking, regulation, stabilization) is thoughtful.

## Weaknesses

### Fatal

- **Theorem 1 compares fundamentally different things, not ensemble approaches.** The theorem compares an ensemble of *learned neural policies* against an ensemble of *analytically optimal linear controllers* (K*_i). On a known linear system, optimal linear gains are trivially computable. The theorem does not show that if you train both neural and linear policies from identical data on the same task, the neural ensemble underperforms. Instead, it shows that a sub-optimal neural policy ensemble performs worse than a theoretically optimal linear ensemble—which is tautological for linear systems. The core claim of the paper (neural ensembles are inherently sub-optimal *as an ensemble method*) is not supported by this result.

- **Theorem 2 instability result applies to ANY ensemble under fast weight variation, not specifically neural ones.** The condition β > min_i α_i / (2 max_i ‖V_i‖∞) for time-varying weights w_i(t) would cause instability for linear ensembles under the same weight variation regime. The paper provides no linear ensemble stability result under comparable time-varying weights to demonstrate a meaningful contrast. This makes the "neural ensembles are unstable while linear ones are stable" claim unsubstantiated by the proof.

### Major

- **Sweeping claims backed by narrow results.** The paper's title ("NEURAL POLICY ENSEMBLES ARE SUB-OPTIMAL") and abstract make universal claims ("significant implications for all neural policy ensemble research"), but the theoretical results are restricted to (a) linear dynamical systems (Theorems 1, 3), (b) specific nonlinearity/diversity conditions (Theorem 1), and (c) time-varying weights with bounded variation rates (Theorem 2). The nonlinearity measure condition L_f κ₀ δ > ρ in Theorem 1 constrains when the result holds, but the paper frames the conclusion as universally applicable.

- **Empirical scope does not match theoretical claims.** Section 4 validates on linear systems only. Section 5 tests on Pendulum and CartPole but uses "Linearized LQR" as the baseline (Figure 4), not a proper nonlinear ensemble comparison. Section 6 tests neural mixing on a nonlinear oscillator and soft pendulum, but the results are inconsistent—the "Mid_Nonlinear_Oscillator" in Figure 5 shows minimal convexity violations, and the Neural Non-Convex Mixing performs comparably to Linear Convex Mixing in some cases. The paper never demonstrates sub-optimality on nonlinear systems where linear controllers genuinely cannot solve the task.

- **Theorem 3 conflates non-convex mixing with neural mixing.** The theorem proves that mixing weights outside the simplex (w ∈ ℝ^N \ Δ^{N-1}) are sub-optimal. This is about the weight space geometry, not about whether a neural network is used to produce the weights. A neural network could output convex weights (via softmax), and a linear combination could use non-convex weights. The claim "neural mixing is sub-optimal" does not follow from the theorem as stated.

### Minor

- **The "2 orders of magnitude" claim appears unsupported by the figures.** The abstract and text claim neural ensembles underperform by "2 orders of magnitude," but the empirical results (Figures 1, 2, 4) show cost ratios of roughly 1.8×–6.5×, not 100×.

- **Insufficient detail on neural controller training.** The paper states "Training is performed using gradient descent to minimize the cumulative cost over episodes" but does not specify learning rates, network architectures (depth, width), training episodes, or convergence criteria. Without this information, the neural ensembles may simply be poorly trained, rather than inherently sub-optimal.

- **Bayesian weight learning for ensemble weights is mentioned but not specified.** The paper states weights are "learned using Bayesian updates based on individual controller performance" but provides no formulation, prior, or update rule. This is a critical detail since ensemble weighting is central to the claims.

## Nice-to-Haves

- A direct comparison where both neural and linear policies are trained from the same data/budget on the same task, rather than comparing learned neural policies to analytically optimal linear ones.
- Experiments on genuinely nonlinear systems where linear controllers fail entirely, to test whether neural ensembles still underperform even when linear ensembles are infeasible.
- An analysis of whether neural ensemble sub-optimality persists when neural policies are well-optimized (e.g., via extensive hyperparameter tuning and sufficient training budget).

## Novel Insights

The observation in Theorem 3 / Corollary 1—that convex mixing of optimal linear policies dominates any other mixing weight vector for LQR systems, with the performance penalty expressible in closed form—is a useful contribution to the policy mixing literature. The characterization that the penalty equals E[x₀ᵀ(K_w - K_λ)ᵀR_λ(K_w - K_λ)x₀] provides actionable insight. Beyond this, the paper's broader claims about universal neural ensemble sub-optimality are not convincingly established by the theoretical or empirical evidence presented.

## Suggestions

1. **Reframe the claims more precisely.** Instead of "neural policy ensembles are sub-optimal" universally, state precisely under what conditions sub-optimality holds and acknowledge that Theorem 1 compares against an oracle linear baseline rather than an equivalently-trained linear ensemble.

2. **Add a fair comparison baseline.** Train linear ensembles under the same data/budget constraints as neural ensembles (rather than using analytically optimal LQR gains) to isolate whether the sub-optimality comes from the ensemble formulation or from optimization difficulty.

3. **Provide complete neural training details** including architecture specifications, hyperparameters, training curves, and convergence diagnostics to rule out the possibility that results reflect poor optimization rather than fundamental limitations.

4. **Test on nonlinear systems** where linear controllers fundamentally cannot work, to determine if neural ensembles are still sub-optimal when linear ensembles are inapplicable.

## Score and Decision

The paper addresses a genuinely important question and provides a structured mathematical framework. However, the core theoretical claims have significant logical gaps (Theorems 1 and 2 do not establish what the paper claims), the empirical validation is conducted primarily on linear systems with fair-comparison concerns, and the sweeping universal framing is not supported by the narrow conditions of the results. Theorem 3/Corollary 1 is the strongest contribution but is about weight space geometry rather than neural vs. linear ensembles per se.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>