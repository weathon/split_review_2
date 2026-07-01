## Summary

This paper proposes *DIPOLE* (Dichotomous diffusion Policy improvement), a novel RL algorithm for tuning diffusion policies. The key idea is to rewrite the KL-regularized RL objective with a greedified reference policy, leading to a closed-form optimal policy that naturally decomposes into a *positive* (reward-maximizing) and a *negative* (reward-minimizing) diffusion policy. Both policies are trained with bounded sigmoid-weighted regression losses, avoiding the instability of exponential weighting. During inference, actions are sampled via a linear combination of the scores of the two policies (similar to classifier-free guidance), enabling controllable greediness. The method is evaluated on offline and offline-to-online RL benchmarks (ExORL, OGBench) and scaled to a 1-billion parameter vision-language-action model for autonomous driving on NAVSIM, showing strong improvements.

## Strengths

- **Novel theoretical derivation.** The paper provides a clean, principled transformation from a greedified KL-regularized objective to a pair of dichotomous policies with bounded weighting functions. This elegantly addresses the instability and sample-dominance issues of standard exponential-weighted regression while preserving simplicity.
- **Strong empirical validation.** Extensive experiments across 39 tasks on two challenging RL benchmarks (ExORL and OGBench) show that DIPOLE consistently outperforms strong baselines including IQL, ReBRAC, IFQL, FQL, and CFGRL. The offline-to-online results further demonstrate the method's ability to improve with online fine-tuning.
- **Scalable to real-world applications.** The paper demonstrates scaling DIPOLE to a large VLA model (1B parameters) for end-to-end autonomous driving, achieving substantial improvements over the imitation-learned baseline on the NAVSIM benchmark (e.g., +6.5 PDMS on navtest). This highlights the practical relevance and robustness of the approach.
- **Clear connection to classifier-free guidance.** The formulation naturally recovers a CFG-like inference procedure, providing both a theoretical justification for a popular heuristic and a principled knob (ω) to control greediness. The paper also clearly differentiates from the prior CFGRL method.

## Weaknesses

### Fatal

None.

### Major

None. The paper is methodologically sound and well-supported by experiments.

### Minor

- **Computational overhead.** Training two separate diffusion models (positive and negative) doubles the compute and memory requirements compared to a single-policy method. The paper does not discuss this cost or suggest possible mitigations (e.g., shared backbone with separate heads).
- **Hyperparameter sensitivity of ω.** The greediness factor ω is a new hyperparameter introduced by the method. While the paper shows some ablation in the appendix (D.4), the analysis is limited. A clearer guideline for setting ω across different tasks would strengthen the practical utility.
- **Offline-to-online setting consistency.** In the offline-to-online experiments, the reference policy μ is set to the previous policy π_{k-1}. The derivation of the greedified objective (Eq. 5) assumes the reference policy is fixed; applying it iteratively may require additional justification or discussion of convergence, which is missing.

### Trivial

- The figure numbering in the text (Figure 1 referred to before it is placed) is slightly awkward but does not affect understanding.

## Nice-to-Haves

- Provide a comparison of training time and memory between DIPOLE and single-model baselines (e.g., FQL) to quantify the overhead.
- Include an ablation on the number of denoising steps during inference; the controllable generation may allow using fewer steps with appropriate ω.
- Discuss the impact of the sigmoid function's saturation on very large advantage values—does the bounded weight still allow sufficient differentiation between high-quality actions?

## Novel Insights

Beyond the paper's own contributions, the key insight is that the problematic exponential weighting in KL-regularized policy extraction can be “factored” into two bounded, symmetric components by introducing a greedified reference policy. This decomposition simultaneously resolves the instability-optimality trade-off and yields a control mechanism (ω) that maps cleanly to classifier-free guidance. The idea that reward-maximization and reward-minimization can be learned as separate, stable diffusion models and then combined linearly is both elegant and practical. This viewpoint may inspire other RL algorithms that need to handle extreme weights or require controllable exploitation.

## Suggestions

- Add a brief discussion or experimental result on the sensitivity of ω, perhaps showing a sweep on one or two tasks with different ω values and recommending a default range.
- Consider including a computational cost table (training time per iteration, model size, memory usage) for DIPOLE versus a single-model alternative to help practitioners assess the trade-off.
- Clarify in the offline-to-online setting whether the greedified reference policy objective is re-derived with μ = π_{k-1} and whether any additional constraints (e.g., trust region) are implicitly needed.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>