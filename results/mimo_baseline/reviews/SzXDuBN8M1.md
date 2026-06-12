## Summary

The paper introduces TD-JEPA, a zero-shot unsupervised RL method that combines temporal-difference learning with latent-predictive (JEPA-style) representations to learn policy-conditioned, multi-step dynamics from offline, reward-free data. The method trains separate state and task encoders, a policy-conditioned multi-step predictor, and parameterized policies end-to-end, enabling zero-shot policy optimization for any downstream reward entirely in latent space. Theoretical analysis connects latent-predictive TD learning to successor measure factorization, and experiments across 65 tasks on 13 datasets demonstrate competitive or superior performance compared to strong baselines.

## Strengths

- **Novel technical formulation**: The paper introduces a genuinely new combination of TD learning with latent-predictive objectives for multi-policy, multi-step dynamics modeling. This advances beyond existing approaches limited to one-step prediction (BYOL), single-policy training, or on-policy data requirements. The policy-conditioned TD loss (Eq. 9) is a clean and well-motivated objective.

- **Rigorous theoretical contributions**: The paper provides four theorems with meaningful insights. Theorem 1 establishes a "gradient matching" result showing that gradients of the latent-predictive MC loss exactly match those of a successor measure approximation loss—this is elegant and novel. Theorem 2 provides a non-collapse guarantee under a continuous-time relaxation. Theorem 3 connects the TD variant to forward/backward TD losses with oblique projections. Theorem 4 bounds policy evaluation error, providing soundness guarantees for zero-shot RL. The authors note these results generalize all prior guarantees for latent-predictive representations.

- **Comprehensive and fair empirical evaluation**: The paper evaluates on 65 tasks across 13 datasets spanning locomotion, navigation, and manipulation with both proprioceptive and pixel observations. The use of probability-of-improvement (Agarwal et al., 2021) in Figure 2 provides a statistically rigorous comparison beyond simple point estimates. Crucially, the paper augments existing representation learning methods (BYOL, BYOL-γ, ICVF) with successor features to create fair baselines, which is methodologically sound and improves the literature's understanding of what representations work for zero-shot RL.

- **Distinct state and task encoders**: The asymmetric design (Section 3.2) where different encoders capture low-level dynamics vs. higher-level task features is well-motivated by intuition (e.g., joint positions vs. building topology) and empirically validated in Figure 3 (right).

- **Fast adaptation demonstrations**: The fine-tuning experiments (Figure 4) show that pre-trained representations—particularly when frozen—enable sample-efficient downstream learning, demonstrating practical utility beyond zero-shot performance.

## Weaknesses

### Fatal
None.

### Major

- **Restrictive theoretical assumptions**: Theorems 1–3 require (A1) orthonormal encoders, (A2) uniform state distribution, and (A3) symmetric transition matrices $P^{\pi_z}$. Assumption A3 is particularly strong—policy-induced transition matrices are generally not symmetric. While the authors acknowledge these assumptions are standard and can be relaxed (Appendix C), the practical gap between the symmetric assumption and the real-world asymmetry of successor measures is not fully addressed. The regularization in Algorithm 1 encourages but does not enforce orthonormality, and no empirical evidence is provided about how well these assumptions approximately hold.

- **Computational cost not discussed**: TD-JEPA trains four networks (two encoders, two predictors) plus policies with target networks for each. The cost relative to simpler baselines like FB (which learns one task encoder) or HILP is unclear. Given that improvements are sometimes modest (e.g., 37.98 vs 39.04 on OGBench proprioception vs FB), a cost-performance analysis would help practitioners make informed choices.

- **Mixed results on certain benchmarks**: On OGBench proprioception, TD-JEPA (37.98) trails FB (39.04) and is comparable to HILP (37.98). On several individual OGBench tasks (antmaze-mm proprioception, cube-single proprioception), FB or other baselines significantly outperform. While the paper's aggregate claim of "matches or outperforms" holds in spirit, the inconsistency across domains deserves more discussion about when the method's assumptions may or may not hold.

### Minor

- **Limited ablation breadth**: While the paper ablates on prediction targets and symmetric vs. asymmetric encoders, there is no analysis of sensitivity to the regularization coefficient λ, encoder dimensions $d_\phi$ and $d_\psi$, or the number/parameterization of policies $\{π_z\}$. These could significantly affect practical performance.

- **Actor training stability**: The actor loss (Algorithm 1) maximizes $T_φ(φ(s), \hat{a}, z)^\top z$ while the predictor is simultaneously being updated. No analysis of training stability (e.g., gradient norms, oscillation) is provided, which is important given that the actor and predictor are jointly optimized.

### Trivial

None.

## Nice-to-Haves

- Wall-clock training time comparison between TD-JEPA and baselines
- Analysis of how learned representations vary across different policy parameters z
- Visualization or quantitative analysis of whether the learned encoders approximately satisfy the orthonormality and symmetry assumptions

## Novel Insights

The key novel insight is that temporal-difference learning within a latent-predictive framework can learn representations capturing multi-step, policy-conditional dynamics from off-policy data—something prior methods could not achieve. The theoretical "gradient matching" result (Theorem 1, Part 2) showing that gradients of the latent-predictive loss exactly match those of a successor measure approximation loss is genuinely novel and generalizes all previous guarantees for latent-predictive representations in RL. Theorem 3 further reveals that TD-JEPA's optimal predictor solves a least-squares TD problem yielding oblique projections of successor measures, connecting latent-predictive TD learning to the classical LSTD literature in a new way. These results collectively establish that latent-predictive TD learning is not just a heuristic but a principled approach to successor measure factorization for multiple policies.

## Suggestions

- Include a table comparing wall-clock training times across methods
- Add an ablation study on the orthonormality regularization coefficient λ
- Discuss the computational implications of training four networks vs. simpler alternatives
- Provide quantitative metrics on how well the learned encoders satisfy assumptions (A1) and (A3)

## Score and Decision

This paper makes a substantial contribution by introducing a principled combination of TD learning with latent-predictive representations for multi-policy RL, supported by novel theoretical analysis that generalizes prior results. The empirical evaluation is comprehensive and the method performs well across diverse settings, particularly in the challenging pixel-based domain. The main theoretical limitations (restrictive assumptions) are acknowledged, and the practical algorithm includes appropriate regularization. The mixed results on some benchmarks and the lack of computational cost analysis are notable but do not invalidate the contribution.

MY FINAL SCORE: 7.0
MY FINAL DECISION: Accept