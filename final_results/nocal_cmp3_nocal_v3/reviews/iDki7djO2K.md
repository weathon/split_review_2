## Summary

This paper proposes a conceptual framework for defining and measuring forgetting in learning systems, grounded in the idea of *predictive self-consistency*. The core insight is that a learner forgets when its predictive distribution changes after being updated on targets it already expects — a violation of what the authors call the "consistency condition." From this, they derive a measure Γ_k(t) (propensity to forget) and demonstrate it empirically across regression, classification, generative modeling, continual learning, and reinforcement learning settings.

---

## Strengths

1. **The core conceptual move is well-motivated and addresses a real gap.** Existing definitions of forgetting are fragmented across continual learning, RL, and neural network training, and often conflate forgetting with backward transfer or parameter change. The paper correctly identifies that parameter changes alone do not imply forgetting (the Bayesian learner example in §5.1 cleanly demonstrates this), and provides a unified formalism that resolves this confusion.

2. **The consistency condition (Definition 4.5) provides a clean mathematical anchor.** The idea that a non-forgetting learner should have its predictive distribution invariant (in expectation) to updates on self-generated targets is conceptually elegant. It formalizes the paper's central insight in a domain-independent way, and the fact that exact Bayesian inference satisfies it while approximate methods do not gives the definition a clear theoretical reference point.

3. **The four desiderata (§4.1) are well-reasoned.** They establish a principled standard: forgetting should be distinguished from task performance, from parameter change, and from the retention of specific observations, and should be a property of the learner rather than the environment. These provide a useful foundation for evaluating definitions of forgetting.

4. **The formalism is genuinely domain-independent.** The paper shows how the same abstract framework (interface, environment, learner with dual update functions) can be instantiated across supervised learning, RL, and generative modeling, making the contribution genuinely general rather than tied to one subfield.

---

## Weaknesses

### Fatal
None.

### Major

1. **The hybrid distribution q_e/q_c is underspecified, which weakens the formalism.** The entire definition of forgetting — the consistency condition and Γ_k(t) — depends on sampling the next observation X from q_e (or q_c in Definition 4.5). The only description is that q_e is a "hybrid distribution that treats the learner's predictions as targets while borrowing components from the environment as needed" (§3.2). This is not a formal definition. In supervised learning, does X represent an input-target pair, and if so, where does the input come from — the empirical data distribution or the learner's generative model? In RL, does q_e require an explicit environment model (transition dynamics, reward function)? Because q_e is the distribution over which the expectation in the consistency condition is taken, its underspecification means a reader cannot determine how to instantiate or compute Γ without filling in substantial gaps. This is not a missing-implementation-detail; it is a gap in the formal definition.

2. **The paper claims its definition "disentangles forgetting from backward transfer" but never tests this against existing measures.** The experiments show that (a) Bayesian learners have Γ≈0, (b) deep learners have Γ>0, and (c) Γ spikes at task boundaries. These are consequences of the definition, not validations that Γ captures something existing measures miss. A head-to-head comparison with conventional CL forgetting metrics (e.g., backward transfer, average accuracy drop) in a setting where they diverge would substantiate a central claim of the paper. Without this, the claim that the new definition "disentangles" forgetting from backward transfer remains asserted but undemonstrated.

3. **The RL experiment is too thin to support the paper's general claims.** A single DQN agent on Cartpole with 10 seeds (§5.4, Figure 5) cannot support the sweeping interpretation that "forgetting is the mechanism by which the agent manages this process" and that "forgetting is an essential component of RL." The discussion in §5.4 goes well beyond what a single environment and algorithm can support.

### Minor

1. **Gap between the theoretical definition and the empirical computation.** Definition 4.6 defines Γ_k(t) as a divergence between distributions over *infinite future sequences* (H^{t+k:∞}). The experiments compute KL divergence and MMD on what appear to be distributions over single predicted outputs. The paper does not explain how the infinite-dimensional distributions are marginalized, summarized, or approximated to yield computable quantities. The note "See [SF] for details on the experimental implementation" suggests details exist elsewhere, but the main text should at least outline the bridge.

2. **The forgetting–efficiency trade-off analysis (§5.3) is correlational with confounders.** Varying SGD momentum or model size changes multiple aspects of learning dynamics (effective step size, convergence rate, generalization, optimization landscape). The observed correlation between Γ and training efficiency is compatible with forgetting being causal, but also with both being separately caused by the manipulated variable. The interpretation ("effective approximate learners utilise forgetting as a mechanism for adaptive and efficient learning") overstates what the experimental design can support.

3. **Notation inconsistency.** Definition 4.5 uses q_c (line 215) while the surrounding text (§3.2, §4.2) uses q_e. The paper never explains whether these refer to the same distribution or different ones. This confuses an already underspecified part of the formalism.

### Trivial
- Minor spelling inconsistency: "backward transfer" (line 15, 165, 307) vs. "backwards transfer" (line 41).

---

## Nice-to-Haves
- Specify q_e/q_e concretely for each setting (supervised learning, RL, generative modeling) so the formalism can be instantiated by other researchers.
- Add an explicit worked example (e.g., linear regression) showing how the theoretical Γ_k(t) maps to a computable quantity.
- Discuss the computational cost of computing Γ (requires rolling out the predictive distribution and computing divergences).
- Examine how Γ relates to generalization or test performance, since the paper motivates forgetting as a fundamental property of learning but never connects it to downstream capability.

---

## Removed Points

These points from the input review were removed with justification:

1. *"The paper oversimplifies — many CL papers do distinguish forgetting from backward transfer"* — The paper claims existing measures "often conflate" these phenomena, not "always." This is a reasonable characterization. Removed (rule: factually wrong / strawman).

2. *"Missing citations of Diaz-Rodriguez et al., 2018 and Lopez-Paz & Ranzato, 2017"* — References are stripped by the parser; I cannot verify what was cited. Removed (rule: missing references).

3. *"KL divergence is not well-defined between distributions over different spaces (classification vs. sequential futures)"* — Both arguments of the divergence in Γ_k(t) are distributions over the same space (H^{t+k:∞}). The critic appears confused about the formalism's spaces. Removed (rule: factually wrong).

4. *"The caption for Figure 3 conflates the horizon over which the consistency condition is tested with the horizon over which the predictive distribution is evaluated"* — The caption describes computing Γ_k(t) for k from 1 to 40, which is consistent with the definition (Γ_k(t) involves distributions over futures starting at t+k, compared before and after k updates). The critic misreads the definition. Removed (rule: factually wrong).

5. *"The empirical validation does not address the gap between the theoretical definition and the computed quantities"* — This criticism partially overlaps with Minor Weakness #1 above and is merged there. The stronger version (that the gap invalidates the experiments) is unsupported — many papers compute approximations of formally-defined quantities without this being fatal, and the appendix was stripped. Removed (rule: speculative-fatal claim).

6. *Generic strength about "addressing an important problem"* — This is too generic to keep as a standalone strength. Removed (rule: generic/superficial strength).

7. *"No analysis of how Γ relates to generalization"* — The paper does not scope itself to study generalization. This is scope creep. Moved to Nice-to-Haves.

---

## Novel Insights

Beyond the paper's own contributions, the review process surfaces one synthetic observation: the formalism's insistence that forgetting be measured via self-generated targets creates an inherent tension — the measure can only be computed when the learner has a well-defined predictive distribution, but many practical algorithms (those with target networks, replay buffer re-initialization, or decoupled state-prediction mappings) operate in regimes where this mapping is temporarily absent. The paper acknowledges this (§4, scope and boundary of validity), but the boundary condition may be more restrictive than acknowledged: it excludes precisely the kinds of mechanisms that many state-of-the-art methods use to manage forgetting.

---

## Suggestions

1. Specify q_e/q_c formally for at least the experimental settings (supervised learning, RL) so that the definition of Γ_k(t) is fully determined. A concrete construction (e.g., in supervised learning: inputs from the empirical marginal, targets from the learner's conditional predictive distribution) would make the formalism reproducible.

2. Add a single comparison experiment where Γ and a conventional CL forgetting metric (e.g., backward transfer) are computed on the same data and shown to disagree in an interpretable way. This would validate the paper's central claim about disentangling the two phenomena.

3. In §5.3, either soften the causal interpretation or add controls that isolate forgetting's role (e.g., by intervening on forgetting directly rather than through momentum/width).

4. Clarify how the infinite-future distributions in Definition 4.6 are reduced to the finite KL/MMD quantities in the experiments, even briefly.

5. Reconcile the q_e/q_c notation.

---

## Score and Decision

The paper makes a genuinely novel conceptual contribution — reframing forgetting as predictive self-consistency violation. The formalism is well-motivated, domain-independent, and addresses real limitations in existing definitions. However, the contribution is weakened by two significant issues: the central component of the formalism (the hybrid distribution q_e/q_c) is underspecified to the point where a reader cannot determine how to instantiate the measure, and the paper's claim that its definition "disentangles" forgetting from backward transfer is asserted but never empirically demonstrated against existing alternatives. These gaps are fixable but leave the paper in an incomplete state. The experiments illustrate the measure but do not validate it against alternatives or the paper's stronger claims.

**MY FINAL SCORE: <score>5.0</score>**
**MY FINAL DECISION: <decision>Reject</decision>**