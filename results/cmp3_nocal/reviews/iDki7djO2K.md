## Summary

This paper proposes a new formal definition of forgetting in learning systems, grounded in the concept of *predictive self-consistency*. The central idea is that a learner forgets when its predictive distribution over future experience changes after updating on targets that the learner itself already expected. From this principle, the authors derive the consistency condition (Definition 4.5) and a divergence-based propensity measure $\Gamma_k(t)$ (Definition 4.6). The formalism is designed to be algorithm- and task-agnostic, and the paper illustrates it with small-scale experiments spanning regression, classification, generative modeling, continual learning, and reinforcement learning. The core conceptual contribution — separating forgetting from backward transfer and from parameter change — is genuinely novel and well-motivated.

## Strengths

- **The self-consistency principle is a sharp and well-motivated insight.** The core idea — that updating on learner-consistent targets and checking whether the predictive distribution changes isolates forgetting from justified belief revision — is elegant and addresses a real gap in prior work. The formal separation of forgetting from backward transfer (Desideratum 4.2, lines 203–207) is a clear advance over accuracy-based CL metrics.

- **The formalism is genuinely algorithm-agnostic.** Section 3 frames supervised learning, RL, generative modeling, and CL as instances of a single interaction process. The paper explicitly shows how each paradigm maps onto the abstract variables $(X_t, Y_t, Z_t)$ (§3.3, lines 147–151). This breadth is a real advance over prior definitions that are tied to continual learning or specific model classes.

- **The exact Bayesian learner is a clean sanity check.** The demonstration that exact Bayesian posteriors satisfy self-consistency and thus have zero propensity to forget (§5.1, Figure 2) is tight and convincing. It directly supports Takeaway 2 ("Parameter changes alone do not imply forgetting") and validates the internal logic of the framework.

- **The desiderata (4.1–4.4) are well-reasoned and motivate the formalism effectively.** The thought experiments they reference (§C) ground the conceptual choices in concrete scenarios, even though the appendix text is not available in the extraction.

## Weaknesses

### Major

1. **The forgetting-efficiency trade-off (Takeaway 3) is not convincingly established and appears confounded.** The claim that "optimal training efficiency occurs at a non-zero level of forgetting" (Figure 4) is supported by two experiments: varying SGD momentum and varying model size. In the momentum experiment, higher momentum is known to amplify gradient update magnitudes, which correlates with both faster convergence and greater predictive change. The paper does not disentangle whether $\Gamma_{40}(t)$ is measuring a meaningful forgetting phenomenon or merely tracking update magnitude — a confound that weakens the causal interpretation that forgetting is a "mechanism for adaptive and efficient learning" (line 277). The 20-parameter optimum in the model-size experiment (Figure 4 right) is presented as a general principle but is clearly a property of the specific regression task. No argument is given for why this should generalize. This weakness directly undermines one of the paper's four stated takeaways.

2. **The empirical validation is thin relative to the breadth of the claims.** The paper's title ("Forgetting is Everywhere") and abstract ("we empirically demonstrate how forgetting is present across all learning settings") suggest broad empirical support, but the experiments use: a shallow neural network on unnamed datasets (Figure 3 left), a single-layer network on two-moons (Figure 3 right), a 20-parameter model (Figure 4 right), and DQN on Cartpole (Figure 5). These are toy-scale settings that do not support the claimed generality about "deep learning." The paper's own qualifier (line 17: "CL, RL, and neural networks are not our focus") is more modest, but it conflicts with the title and the language used throughout Section 5 (e.g., "Forgetting in Deep Learning" in §5.2 using a shallow network). The gap between claim and evidence is substantial.

3. **The paper conflates correlation with causation in interpreting the RL experiment.** The observation that the forgetting curve tracks TD loss in DQN (Figure 5, Takeaway 4: "forgetting is an integral component of learning") is presented as an empirical discovery. However, both quantities *measure predictive change* — TD loss is driven by changes in Q-value predictions, and $\Gamma_k(t)$ measures divergence between predictive distributions. Their correlation is expected rather than informative. The paper interprets this as evidence that forgetting is a "deliberate mechanism" (Figure 5 caption), but the data only show that two measures of prediction dynamics covary.

4. **The gap between the formal definition of $\Gamma_k(t)$ and its practical computation is not addressed in the main text.** Definition 4.6 involves a divergence between distributions over *infinite future sequences* $H^{t+k:\infty}$, but the experiments compute KL divergence (classification/regression) and MMD (generative tasks), which operate on finite-dimensional marginals. The step from infinite-dimensional distributions to computable finite approximations is never explained in the main body. The paper mentions "See [SF] for details" (Figure 3 caption), but the core empirical section should at least sketch the approximation strategy. A reader cannot tell whether the reported values primarily reflect the formalism or the specific approximation choices.

### Minor

1. **The scope/boundary section (lines 227–228) creates a tension with the DQN experiment.** The paper states that forgetting is "undefined" during periods of "target-network lag" (when the predictive distribution is decoupled from the learner state). DQN (used in §5.4) is the canonical example of an algorithm that uses a target network. While the target network in DQN is used for TD targets rather than action predictions, the paper does not acknowledge this subtlety or explain why its own experiment does not trigger the scope exception. This is a gap the authors should address.

2. **The divergence $D$ in Definition 4.6 is left unspecified, and different divergences (KL, MMD) are used for different tasks without justification.** The paper does not discuss whether the choice of divergence affects the qualitative results or whether the measure is robust to this choice. For high-dimensional predictive distributions, KL and MMD can give very different readings.

3. **The causal framing of "forgetting as a mechanism" (line 277) overinterprets correlational evidence.** The paper states that "effective approximate learners utilise forgetting as a mechanism for adaptive and efficient learning," which implies deliberate use of forgetting. The evidence supports only that forgetting (as measured by $\Gamma_k$) correlates with training efficiency. The paper does not distinguish between "forgetting-as-mechanism" and "forgetting-as-epiphenomenon" (a byproduct of faster learning).

### Trivial

None.

## Nice-to-Haves

- A comparison experiment between $\Gamma_k(t)$ and standard backward-transfer metrics on the same data would strengthen the argument that the proposed measure reveals something backward transfer misses.
- A discussion of how many samples are needed in the rollout for $\Gamma_k(t)$, how $q_e$ is approximated in practice, and how sensitive the measure is to these choices would substantially improve the paper's transparency.
- The paper could be strengthened by showing that $\Gamma_k(t) predicts a failure mode that standard metrics miss, or that it can be used to tune hyperparameters more effectively than loss-based metrics.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **"The paper never explains how predictive distributions over infinite futures are approximated"** — The paper references supplementary material ("See [SF]"), and the appendix is stripped by the PDF parser. Per the rules, weaknesses about missing appendix content are removed. The remaining concern (the infinite-to-finite approximation gap in the main text) is kept as a Major weakness above.
- **"Missing related works (Fisher information, influence functions)"** — Per rules: "DO NOT mention missing related works, as you do not have external sources to confirm their existence."
- **"The paper does not explain how $q_e$ is constructed in practice"** — This may be detailed in the stripped appendix. The kept version of this concern focuses on the main text's insufficient operational detail.
- **Speculative statements about what the appendix "may" or "may not" contain** — Removed per rules about stripped appendices.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the empirical section explicitly as illustrative of the formalism rather than as evidence for sweeping claims about deep learning. Change the title and abstract language to match the paper's own more modest scope (line 17).
- For the forgetting-efficiency trade-off, add an experiment that controls for confounds (e.g., compare learners that differ in forgetting but not in update magnitude, or use the same optimizer with different regularization that affects forgetting).
- Address the DQN/scope-boundary tension directly: explain why the target network in DQN does not trigger the scope exception, or measure forgetting only during periods when the scope condition holds.
- Add a short paragraph in the main text explaining how the infinite-dimensional predictive distributions in Definition 4.6 are approximated in practice.

## Score and Decision

<score>6.0</score>
<decision>Accept</decision>