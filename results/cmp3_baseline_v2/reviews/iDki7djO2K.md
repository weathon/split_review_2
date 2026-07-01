## Summary

This paper proposes a general, algorithm- and task-agnostic theory of forgetting in learning systems. The authors define forgetting as a violation of self-consistency in a learner's predictive distribution over future experiences, formalized through a probabilistic interaction framework between a learner and environment. They introduce a measurable "propensity to forget" (Γ_k(t)) and empirically demonstrate that forgetting is pervasive across classification, regression, generative modeling, and reinforcement learning, while also revealing a non-trivial trade-off where moderate forgetting can improve training efficiency.

## Strengths

- **Principled and general formalism**: The paper provides a rigorous mathematical framework (Definitions 3.1-3.6, 4.5-4.6) that unifies forgetting across diverse learning paradigms (supervised, unsupervised, RL, generative) under a single predictive-consistency perspective. This is a genuine conceptual advance over fragmented, task-specific definitions in the literature.

- **Clear separation of forgetting from related phenomena**: The consistency condition (Definition 4.5) cleanly disentangles forgetting from backward transfer, parameter drift, and performance degradation—a long-standing confusion in continual learning. The demonstration that exact Bayesian learners satisfy self-consistency while approximate learners do not (Section 5.1, Figure 2) provides compelling validation.

- **Empirical breadth and insight**: The experiments span regression, classification, generative modeling, continual learning, and RL (Figures 3-5), convincingly showing that forgetting is "everywhere" in deep learning. The finding that optimal training efficiency occurs at non-zero forgetting (Figure 4) is a non-trivial and practically relevant observation.

## Weaknesses

### Major

- **Operationalization gap between theory and practice**: The theoretical definition of Γ_k(t) (Definition 4.6) requires computing divergences between predictive distributions over infinite future sequences, which is intractable. The empirical implementation uses finite-horizon approximations (k=1 to 40) and specific divergence choices (KL, MMD), but the paper does not provide a rigorous analysis of how these approximations affect the measure's validity, nor does it establish convergence guarantees or sensitivity to the choice of k and divergence.

- **Limited validation of the measure's properties**: While the paper shows that Γ_k(t) behaves intuitively (e.g., spikes at task boundaries), it does not systematically validate that the measure satisfies the desiderata (4.1-4.4) beyond qualitative examples. For instance, there is no ablation study showing that Γ_k(t) is invariant to parameter-preserving updates (Desideratum 4.2) or that it captures generalization forgetting (Desideratum 4.3) in a controlled setting.

- **The "forgetting-efficiency trade-off" claim is weakly supported**: Figure 4 shows correlation between Γ_k(t) and training efficiency for two hyperparameters (momentum, model size) in one regression task. This is insufficient to establish a general trade-off. The paper does not control for confounding factors (e.g., optimization dynamics, capacity) that could explain the observed relationship without invoking forgetting as a causal mechanism.

### Minor

- **The interaction formalism (Section 3) is overly complex for the paper's core contribution**: The detailed agent-environment framework (Definitions 3.1-3.6) with separate learning/inference modes (u, u') and hybrid distributions (q_e) adds substantial notation that is never fully leveraged in the empirical analysis. A simpler predictive-Bayesian framing might have been more accessible without losing the core insight.

- **Scope and boundary conditions are acknowledged but not explored**: The paper notes that forgetting is undefined during transitory phases (buffer reinitialization, target-network lag) and that some algorithms may fall outside the formalism. However, it does not characterize how common or problematic these edge cases are in practice, nor does it provide guidance for handling them.

### Trivial

- The title "Forgetting is Everywhere" is somewhat overstated given that the empirical evidence is limited to specific neural network architectures and tasks, though the theoretical claim is well-supported.

## Nice-to-Haves

- A systematic comparison of Γ_k(t) against existing forgetting metrics (e.g., backward transfer, forgetting in CL benchmarks) on the same tasks would strengthen the claim that the new measure captures distinct information.
- Theoretical analysis of how Γ_k(t) behaves under common mitigation strategies (replay, regularization, parameter isolation) would increase practical utility.
- Discussion of computational cost: estimating predictive distributions via rollouts is expensive; guidance on efficient approximation would aid adoption.

## Novel Insights

Beyond the paper's own contributions, the key insight is that forgetting is not merely a failure mode but a necessary feature of efficient approximate learning. The consistency condition reveals that exact Bayesian learners never forget, but they are computationally intractable; approximate learners must forget to adapt, and the optimal forgetting rate is non-zero. This reframes the continual learning problem from "how to prevent forgetting" to "how to control forgetting at the right level." The connection between the consistency condition and the mathematical justification for replay (Section B.3) is also a novel perspective that bridges theory and practice.

## Suggestions

- Strengthen the empirical validation of the forgetting-efficiency trade-off by testing across multiple tasks (classification, RL), multiple hyperparameters (learning rate, batch size, regularization strength), and with causal interventions (e.g., explicitly controlling forgetting via replay ratio).
- Provide a more rigorous analysis of the approximation errors in Γ_k(t) estimation, including how the choice of k and divergence affects the measure's reliability and whether there are principled ways to select these hyperparameters.

## Score and Decision

The paper makes a genuine conceptual contribution by providing the first unified, principled definition of forgetting that generalizes across learning paradigms. The formalism is mathematically sound and addresses long-standing confusions in the literature. However, the empirical validation is preliminary—the key claims about the forgetting-efficiency trade-off and the measure's properties are not yet convincingly supported. The paper would benefit from more systematic experiments before acceptance at a top venue.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>