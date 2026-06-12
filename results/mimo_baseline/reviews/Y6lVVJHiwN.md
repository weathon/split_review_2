## Summary

The paper introduces FEDSGM, a unified framework for federated constrained optimization that simultaneously handles functional constraints (via the switching gradient method), bidirectional compression with error feedback, multiple local update steps, and partial client participation. The framework provides projection-free, primal-only updates and derives convergence guarantees showing O(1/√T) rates for the averaged iterate, with high-probability bounds that decouple optimization progress from sampling noise under partial participation. A soft switching variant is also introduced to stabilize updates near the feasibility boundary.

## Strengths

- **Genuine theoretical unification.** FEDSGM is the first framework to simultaneously address all four challenges—functional constraints, bidirectional compression with EF, multi-step local updates (E>1), and partial participation—with clean convergence guarantees. Prior work (Islamov et al., 2025) required full participation, E=1, and hard switching only. The Γ factor in Theorem 1 cleanly isolates the interaction between compression and drift, and the high-probability bounds in the partial participation case elegantly separate optimization error from estimation error.

- **Consistent recovery of known results.** The convergence rates correctly reduce to known results in all special cases: centralized SGM (O(DG/√T) matching Nesterov et al., 2018; Lan & Zhou, 2020), FedSGM without compression (O(DG√E/√T) capturing client drift), full participation with compression (matching Islamov et al., 2025), and EF-14 in the unconstrained case (matching Karimireddy et al., 2019). This consistency across special cases is convincing evidence of correctness.

- **Insightful geometric analysis of soft switching.** The characterization of oscillatory behavior via the skew-symmetric matrices K_glob and K_loc, and the observation that client heterogeneity alone (K_glob=0 but K_loc≠0) can induce rotational drift, provides genuinely useful intuition for constrained federated optimization. The soft switching mechanism β acts as a geometric stabilizer, which is a principled motivation beyond mere algorithmic convenience.

- **High-probability partial participation bounds.** The sub-Gaussian concentration framework (Assumption 4) with explicit probability tolerance δ provides practical guarantees that go beyond expectation-based bounds, cleanly decoupling the optimization rate from the sampling noise floor.

## Weaknesses

### Fatal

None.

### Major

- **No comparison with alternative constrained FL methods.** The paper claims FEDSGM's advantages over AL/ADMM-type methods, projection-based constrained FedAvg (He et al., 2024), and penalty-based approaches, yet provides zero empirical comparisons. Without this, the practical significance of the unification remains unsubstantiated. Even showing that FEDSGM outperforms methods handling subsets of the four challenges would significantly strengthen the contribution.

- **Extremely limited experimental scope.** The NP classification experiments use only the breast cancer dataset (~570 samples), and the CMDP experiments use only the CartPole environment—one of the simplest RL benchmarks. For a paper establishing a "theoretically grounded foundation for constrained FL at scale," this is insufficient to demonstrate scalability or broad applicability.

### Minor

- **Soft switching parameter sensitivity underexplored.** Theorem 2 requires β ≥ 2/ε, and the experiments use β=100 without systematic exploration. Given that the practical behavior of soft switching likely depends on β in ways not captured by the worst-case theory (e.g., the stabilization benefit at moderate β vs. convergence rate), a sensitivity analysis would be valuable.

- **Practical parameter guidance is limited.** The threshold ε depends on problem constants (D, G, T) and compression parameters that may be unknown in practice. While the theoretical setting of ε is necessary for the proofs, the paper provides little guidance on how practitioners should choose these parameters, especially in the non-convex RL setting where the convex theory doesn't directly apply.

- **The partial participation ε is significantly inflated.** In Theorem 1's partial participation case, ε includes terms scaling with n/m, √(log(T/δ)/m), and compression factors, potentially making it much larger than the full participation ε. While this is theoretically inevitable, the practical implications for large-scale systems with low participation rates could be discussed more carefully.

## Nice-to-Haves

- Empirical comparison against at least constrained FedAvg and AL-based federated methods across the NP classification and CMDP tasks.
- Additional datasets (e.g., Adult/Census for NP classification, Mujoco environments for CMDP) to demonstrate broader applicability.
- Ablation study on β for soft switching to show the stabilization effect quantitatively.
- Discussion of computational overhead per round relative to simpler alternatives.

## Novel Insights

The observation that even when global gradients are perfectly aligned (K_glob = 0), client-level heterogeneity creates a non-trivial skew-symmetric matrix K_loc with Frobenius norm bounded by √(2V_f·V_g), which induces rotational drift in federated switching dynamics, is a genuinely novel geometric insight. This means that the standard source of instability in SGM—misalignment between objective and constraint gradients—is compounded in federated settings by a heterogeneity-driven component that persists even in benign geometric configurations. This insight goes beyond the paper's algorithmic contributions and could inform the design of future federated constrained methods.

## Suggestions

- Add empirical comparisons with at least 2-3 baseline methods (e.g., constrained FedAvg, federated AL/ADMM) on both NP classification and CMDP tasks to validate practical advantages.
- Expand experiments to larger datasets and more complex environments to demonstrate scalability.
- Include a sensitivity analysis of the soft switching parameter β.
- Provide more concrete practical guidance on setting ε and β in real applications.

## Score and Decision

The theoretical contribution is genuinely novel and non-trivial—the first convergence analysis unifying all four challenges with clean rates that recover known results in special cases. The geometric analysis of soft switching provides useful new insights. However, the experimental validation is significantly underdeveloped: only two tasks (one simple dataset, one simple RL environment) with no comparison against alternative constrained FL methods. This gap between strong theory and weak experiments places the paper at the borderline.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject