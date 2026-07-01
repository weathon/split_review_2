## Summary

This paper proposes a general, algorithm- and task-agnostic theory of forgetting in learning systems. Forgetting is defined as a violation of self-consistency in a learner’s predictive distribution: after updating on targets consistent with the learner’s own expectations, the predictive distribution should be recoverable in expectation from the pre-update distribution. The paper introduces a formal framework based on an interaction process between learner and environment, formulates consistency conditions, and derives a propensity-to-forget measure. Empirical studies across classification, regression, generative modelling, continual learning, and reinforcement learning show that forgetting is ubiquitous in deep learning and that a moderate amount of forgetting can improve training efficiency.

## Strengths

- **Novel conceptual foundation**: The paper provides a principled, predictive-distribution-based definition of forgetting that disentangles forgetting from performance degradation, parameter change, and backward transfer. This is a significant conceptual advance over existing task- or algorithm-specific measures.
- **Clear desiderata**: The motivations and thought experiments in §4.1 and Appendix §C (as referenced) establish well-justified criteria that any notion of forgetting should satisfy, and the proposed formalism directly addresses each one.
- **Broad applicability**: The framework is expressed in a general interaction-process formalism that subsumes supervised learning, RL, generative modelling, and continual learning, demonstrating genuine algorithm- and task-agnosticism.
- **Theoretical grounding in Bayesian consistency**: The paper shows that exact Bayesian learners satisfy the consistency condition (and thus do not forget), while common approximate learners (diagonal Gaussian variational inference, gradient-based point estimates) violate it. This provides a crisp theoretical benchmark.

## Weaknesses

### Fatal
None.

### Major
- **Insufficient experimental validation of the core measure**: The paper relies on a specific divergence (KL or MMD) to compute the propensity-to-forget Γₖ(t), but provides no principled justification for choosing one divergence over another, nor does it discuss sensitivity to the choice. The experiments use small-scale problems (shallow networks, cartpole) and the reported forgetting values are not linked to any ground-truth notion of forgetting—the empirical evaluation is largely demonstrative rather than confirmatory.
- **Lack of rigorous support for the “training efficiency” trade-off claim**: The claim that moderate forgetting improves efficiency (Figure 4) is based on a single regression task with an ad-hoc efficiency proxy (inverse normalized area under the training loss curve). This does not convincingly establish a general trade-off; the observed “elbow” could be an artifact of the particular setting. Without multiple independent tasks and a validated efficiency metric, the claim remains speculative.
- **Missing crucial operational details in the main text**: The paper does not explain how the predictive distributions \(q(H^{t+1:\infty} \mid Z_t, H_{0:t})\) are actually obtained from deep neural networks in the experiments—e.g., how future trajectories are simulated, what hybrid distribution \(q_e\) is used, and how the k-step expectation in Definition 4.6 is approximated. These omissions make it difficult to assess the validity and reproducibility of the empirical results.

### Minor
- **Overstated claim of being “the first” generalized definition**: Several prior works (e.g., Kim et al., 2025; Lee et al., 2021; Raghavan & Balaprakash, 2021) propose task-agnostic or representation-based definitions of forgetting. The paper does not clearly demonstrate that these prior notions are subsumed or that no previous formulation could be extended to the same degree of generality.
- **The trade-off observation in RL (Figure 5) is purely correlational**: The authors note that forgetting follows TD loss, but do not establish a causal relationship or rule out alternative explanations (e.g., both are driven by the same update dynamics). The interpretation that forgetting is an “active mechanism” for managing information retention is not directly supported by the data.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis of the propensity-to-forget measure to the choice of divergence (KL vs. MMD vs. Wasserstein) and to the number of steps \(k\).
- A concrete example where the proposed forgetting measure reveals a failure mode that existing CL metrics (e.g., backward transfer) miss.
- A discussion of how the framework could guide the design of new algorithms (e.g., regularizers that enforce approximate self-consistency).

## Novel Insights

The central insight—that forgetting can be characterized as a failure of predictive self-consistency, and that this characterization is independent of the learner’s architecture or the environment—is genuinely novel and valuable. The paper convincingly argues that forgetting is not merely a nuisance in continual learning but a fundamental consequence of how approximate learners update beliefs. The connection between self-consistency and the need for replay mechanisms (Appendix B.3) is also an elegant theoretical justification for a widely used practical technique. These insights shift the perspective from “how to avoid forgetting” to “how to manage the inevitable forgetting in a principled way,” which could influence future research on stable and efficient learning algorithms.

## Suggestions

- **Strengthen empirical support for the trade-off claim**: Include multiple tasks (e.g., classification, RL, generative) and multiple hyperparameter families (learning rate, network width, replay buffer size) to demonstrate that the forgetting-efficiency trade-off generalizes beyond the specific regression setting shown in Figure 4.
- **Provide detailed operationalization of the measure**: In the main text, briefly describe how predictive distributions are approximated for neural networks (e.g., using ensemble or dropout for uncertainty, or assuming a simple parametric form) and how the expectation over k-step updates is computed in practice. This would significantly improve reproducibility and transparency.
- **Clarify the scope of validity**: The paper acknowledges edge cases where the predictive distribution does not reflect the state (buffer reinitialization, target network lags). It would strengthen the paper to discuss how one can detect such intervals or what alternative definitions might handle them.

## Score and Decision

**Score**: 4.0  
**Decision**: Reject  

The paper presents a conceptually clean and general theory of forgetting that addresses a genuine gap in the literature. However, the empirical validation is too limited and insufficiently detailed to confirm that the proposed measure behaves as claimed, and the key trade-off result rests on a single, weakly justified experiment. The theoretical contribution alone is interesting but not yet impactful enough to warrant acceptance at ICLR; a revised version with substantially stronger empirical support could be a strong submission.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>