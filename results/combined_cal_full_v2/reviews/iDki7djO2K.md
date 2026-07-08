## Summary

This paper proposes a novel conceptual framework for defining and measuring forgetting in learning systems. The core idea is to define forgetting as a violation of *predictive self-consistency*: if a learner updates on data drawn from its own predictive distribution and its beliefs change, that change must represent a loss of information rather than acquisition. The paper formalizes this through a general stochastic interaction process between learner and environment, defines a consistency condition (Definition 4.5), and derives an operational measure Γ_k(t) (Definition 4.6). Experiments on regression, classification, generative modeling, CL, and RL (CartPole) illustrate the framework.

## Strengths

- **A genuinely novel and well-motivated conceptual framework (§4.2).** The idea of grounding forgetting in predictive self-consistency is clean, original, and addresses real limitations in prior work. The core intuition — that updating on data the learner already expects cannot represent information gain — is simple and compelling. This is the paper's primary contribution and is genuinely novel. [weight=10.10]

- **Well-constructed desiderata (§4.1).** The four desiderata (loss of learned information, not conflating forgetting with belief change, encompassing loss of general capabilities, being a property of the learner) are carefully justified and serve as a useful framework for evaluating any definition of forgetting. The paper's own definition demonstrably satisfies them better than the alternatives it critiques. [weight=10.26]

- **Elegant theoretical anchor: exact Bayesian learners are unforgetful (§5.1, Equation 10).** The demonstration that exact Bayesian updates satisfy the self-consistency condition (marginalizing over a hypothetical future observation recovers the current posterior) provides a clean sanity check. The contrast with diagonal variational posteriors and point estimates in Figure 2 effectively illustrates how the formalism separates parameter change from forgetting. [weight=10.19]

- **Clean separation of forgetting from backward transfer.** This is a genuine advance over continual-learning metrics (Chaudhry et al., 2018a) that conflate these two phenomena. The formalism's construction — performing updates on targets drawn from the learner's own predictive distribution rather than on new external data — cleanly isolates forgetting from constructive backward transfer. [weight=9.05]

## Weaknesses

### Fatal
None.

### Major

1. **Structural gap between the formalism and practical instantiation.** The operational measure Γ_k(t) (Definition 4.6) and the consistency condition (Definition 4.5) both rely on the hybrid distribution q_e / q_c — the environment's response to the learner's outputs. An external observer monitoring a learning system generally does **not** have access to this distribution, because it encodes the environment's unknown transition dynamics (e.g., the true labeling function in supervised learning, the transition and reward functions in RL). The paper defines q_e as "borrowing components from the environment as needed" (§3.2) but never specifies how an observer could acquire these components. This creates a genuine gap between the formal definition and what can actually be computed in practice. While the paper references supplementary files for experimental implementation details, the conceptual concern about general computability remains unaddressed. [weight=3.79]

2. **Empirical evidence does not support the sweeping title and claims.** The title "Forgetting is Everywhere" and the abstract's claim of "validating the theory" are not supported by the evidence provided. The experiments use small-scale models (shallow/single-layer neural networks) on simple tasks (two-moons classification, CartPole, basic regression). No modern architectures (deep convnets, transformers, LLMs) or realistic benchmarks (Split CIFAR, Atari, MuJoCo) are evaluated. The paper explicitly states (§5.2) that these experiments motivate the title, but the gap between "shallow neural networks on two-moons" and "everywhere in deep learning" is substantial. The experiments are useful illustrations of the framework but do not constitute validation at the level of generality claimed. [weight=-0.49]

3. **The claimed "fundamental trade-off between forgetting and training efficiency" (Takeaway 3, Figure 4) is supported by thin evidence.** This claim rests on two hyperparameter sweeps (momentum, number of parameters) on a **single** regression task. The paper interprets correlational patterns causally ("a moderate amount of forgetting improves learning efficiency"), but what is shown is that certain hyperparameter choices co-vary with both Γ and efficiency on one task. No controls for confounding factors, no replication across multiple tasks or architectures, and no direct manipulation of Γ independent of other factors are provided. A "fundamental trade-off" cannot be established from this evidence. [weight=0.98]

4. **Causal interpretation of the RL experiment (Figure 5, §5.4) is unsupported.** The paper states that "forgetting old information is a deliberate mechanism for balancing knowledge acquisition with knowledge retention" and that "the forgetting curve follows the TD loss **because** forgetting information is the mechanism by which the agent manages this process." All that is shown is a correlation between Γ_k(t) and TD loss over the course of DQN training on CartPole. No causal evidence (e.g., comparisons between DQN with and without replay, or interventions that manipulate forgetting while controlling for other factors) is provided. Correlation between two metrics that both depend on training dynamics does not establish that one is a "mechanism" for the other. [weight=1.34]

### Minor

5. **Undefined notation in a key definition.** The consistency condition (Definition 4.5, Equation 8) uses the notation q_c (line 215), which is never introduced or defined in the paper. This appears to be related to the hybrid distribution q_e from §3.2, but the relationship is not explained. [weight=3.28]

6. **Connection between the Bayesian example and the formalism is not made explicit.** Equation (10) demonstrates self-consistency for the Bayesian *parameter posterior* p(θ | X_{1:t}), while the paper's formalism defines consistency in terms of the *predictive distribution* q(H^{t+1:∞} | Z_t, H_{0:t}). These are equivalent for Bayesian models (since the posterior predictive is the integral of the likelihood over the posterior), but this connection is left implicit. Making it explicit would strengthen the link between the Bayesian anchor example and the formal framework. [weight=7.01]

7. **DQN experiment does not address the "Scope and boundary of validity" limitation.** The paper notes (§4.2, line 227) that forgetting is "undefined" during periods of target-network lag, because the predictive distribution may not accurately represent the learner's state during these transitory phases. The DQN experiment uses target networks (which are periodically updated), but the paper does not discuss whether the reported Γ_k(t) values are computed during periods where the target network lags, and if so, what these values mean. [weight=4.26]

### Trivial
None.

## Nice-to-Haves

- **Comparison of Γ_k(t) to existing CL forgetting measures.** The paper critiques CL metrics (backward transfer) but never empirically demonstrates how Γ_k(t) differs from them on a common benchmark. A simple experiment showing a case where backward transfer and Γ_k(t) diverge would directly validate the paper's key conceptual claim.
- **Discussion of computational cost.** The k-step propensity requires sampling from the predictive distribution, rolling out k updates, and measuring divergence — this could be expensive for large models. A discussion of practical use cases and limitations would be helpful.
- **Clearer explanation of how q_e is approximated in experiments.** While implementation details are referenced to supplementary files, the main paper would benefit from a brief summary of how the hybrid distribution is instantiated for each task domain.

## Removed Points

These points are flagged to be removed; treat them with caution.
- Criticism that experimental implementation details are only in the supplementary (referenced as "[SF]"): removed per rule that parser-stripped appendix content should not be penalized. The paper does reference supplementary files for implementation details.
- Criticism about missing computational cost analysis: removed as a non-standard requirement for a conceptual/ theoretical paper.
- Generic criticism that the paper should compare to more methods/baselines: demoted to Nice-to-have. The paper's contribution is conceptual, not a new method.
- Weakness about the §3 formalism being too abstract to instantiate: this overlaps substantially with Major Issue #1 and is subsumed there.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify how q_e / q_c is approximated in practice — this is the single most important missing link between the formal definition and the empirical measure.
2. Either scale the experiments to support the title claim, or reframe the title and claims to honestly reflect the illustrative nature of the experiments (e.g., "Forgetting as Predictive Inconsistency: A Formal Framework and Illustrations").
3. Replace causal/mechanistic language ("deliberate mechanism," "fundamental trade-off") with descriptive language that matches the correlational evidence.
4. Add a discussion of when Γ_k(t) is computable vs. when it requires approximations, and what those approximations entail.
5. Define q_c and explain its relationship to q_e.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>