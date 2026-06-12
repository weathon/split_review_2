## Summary

This paper proposes a general, algorithm- and task-agnostic theory of forgetting in machine learning. It formalizes learning as a stochastic interaction process between a learner and environment, then defines forgetting as a violation of predictive self-consistency: if updating on data the learner already expects changes its predictive distribution over futures, that constitutes forgetting. This yields a tractable "propensity to forget" measure, which the authors validate empirically across regression, classification, generative modelling, continual learning, and reinforcement learning, revealing that forgetting is ubiquitous and that optimal training efficiency typically corresponds to non-zero forgetting.

## Strengths

- **Novel and well-motivated conceptual framework.** The core insight—that forgetting should be defined via predictive self-consistency rather than parameter drift or performance degradation—is genuinely useful. The desiderata in §4.1 are carefully reasoned (the thought experiments referenced in Appendix C are mentioned and appear to be well-considered), and the distinction between forgetting and backward transfer addresses a real shortcoming in CL metrics. The demonstration that exact Bayesian learners are unforgetful (§5.1) and that parameter changes alone do not imply forgetting is a clean theoretical result that clarifies prior confusion in the literature.

- **Broad empirical validation across paradigms.** The authors instantiate their forgetting measure (Definition 4.6) in regression, classification, generative modelling, class-incremental learning, and RL (DQN on CartPole). This breadth is unusual for a theory-leaning paper and serves to demonstrate generality. The finding that forgetting is non-zero even in i.i.d. settings (Figure 3, left) is counterintuitive and informative. The trade-off between forgetting and training efficiency (Figure 4) and the link between TD loss dynamics and forgetting in RL (Figure 5) offer genuinely novel observations.

- **Clean separation of concepts.** The formalism successfully disentangles forgetting from backward transfer (via learner-consistent target sampling in Eq. 7), from parameter changes (Takeaway 2), and from task performance (Desideratum 4.1). This is an advance over prior approaches that conflate these phenomena.

## Weaknesses

### Fatal

None.

### Major

- **Vague specification of the hybrid distribution q_e.** The predictive distribution rollout in Eq. 3 depends on a "hybrid distribution" q_e that "borrows components from the environment as needed." This object is central to the entire formalism—it appears in both the predictive distribution definition and the consistency condition—yet its construction is never precisely specified. For instance, in RL, does q_e use the true environment dynamics? If so, the predictive distribution couples back to the environment in a way that undermines the claimed isolation. If not, what exactly is borrowed? This ambiguity weakens the theoretical claims, as the consistency condition (Definition 4.5) and the propensity-to-forget measure (Definition 4.6) inherit this imprecision.

- **Limited experimental scale.** The deep learning experiments use shallow neural networks on simple tasks (shallow regression/classification, two-moons, CartPole). While sufficing to illustrate the framework, these are toy-scale settings. Given the paper's bold claims about generality and the ubiquity of forgetting, it is unclear whether the empirical patterns (e.g., the forgetting-efficiency elbow in Figure 4) persist with modern architectures, larger datasets, or more complex RL environments. The gap between the theoretical ambition and the experimental instantiation is notable.

- **The propensity-to-forget measure is hard to compute in practice.** The measure in Definition 4.6 requires rolling out the learner in inference mode to form q(H^{t+k:∞} | Z_t, H_{0:t}), which the authors approximate by sampling from the predictive distribution. The paper does not discuss the variance of this estimator, the sensitivity to the number of samples, or how the choice of divergence D (KL vs. MMD) affects the measure's reliability. For a proposed operational measure, this computational and estimation gap limits reproducibility and practical adoption.

### Minor

- **Scope limitation is acknowledged but underexplored.** The authors note that the formalism "applies whenever the learner's predictive distribution accurately represents the learner's state" and that algorithms lacking such a predictive mapping "fall outside the scope." This is a significant caveat for a paper claiming universality. A concrete example of such an algorithm or a clearer delineation of the boundary would strengthen the contribution.

- **The forgetting-efficiency trade-off deserves deeper analysis.** The "elbow" pattern in Figure 4 is interesting but the paper offers limited mechanistic explanation. Why does moderate forgetting improve efficiency in approximate learners? Is it related to implicit regularization, escaping bad local optima, or something else? Connecting this finding to existing optimization or generalization theory would add depth.

- **Comparison with existing forgetting measures is limited.** The paper criticizes prior metrics (§2) but does not quantitatively compare its propensity-to-forget measure against existing approaches (e.g., Chaudhry et al., 2018a) on the same tasks. Such a comparison would strengthen the claim that the new measure captures something distinct.

### Trivial

None.

## Nice-to-Haves

- A quantitative comparison of the propensity-to-forget measure against standard CL forgetting metrics on a shared benchmark.
- Experiments on larger-scale settings (e.g., ResNet on CIFAR, Atari with modern RL) to demonstrate generality.
- Analysis of how the choice of divergence D and rollout horizon k affect the measure's sensitivity and reliability.

## Novel Insights

The paper's most novel observation is that forgetting is present even in i.i.d. deep learning settings where it is typically ignored—hence "forgetting is everywhere." The empirical demonstration that optimal training efficiency corresponds to a non-zero level of forgetting (the forgetting-efficiency trade-off) is a genuinely new insight that challenges the implicit assumption that less forgetting is always better. The formal separation of forgetting from backward transfer via learner-consistent target sampling is also a meaningful conceptual advance, resolving a long-standing ambiguity in continual learning metrics.

## Suggestions

- Specify the hybrid distribution q_e precisely, ideally with a formal definition (e.g., as a specific mixture or conditional kernel) for at least the settings considered experimentally.
- Expand experiments to at least one modern-scale deep learning setting to demonstrate practical relevance beyond toy problems.
- Provide convergence/variance estimates for the Monte Carlo approximation of the propensity-to-forget measure, or release code enabling others to compute it reliably.

## Score and Decision

This paper makes a genuine conceptual contribution by providing a unified, principled definition of forgetting that cleanly separates it from related phenomena. The formalism is elegant and the desiderata are well-motivated. However, the ambiguity in specifying the hybrid distribution, the limited scale of experiments relative to the paper's ambitious claims, and the practical difficulties of the proposed measure temper enthusiasm. As a theory paper, the contribution is valuable but would benefit from sharper technical specification and broader empirical grounding.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept