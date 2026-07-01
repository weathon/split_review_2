Now let me produce the final consolidated review.

## Summary

DIPOLE proposes a novel RL algorithm for fine-tuning diffusion/flow-matching policies. The core contribution is a greedified KL-regularized objective that decomposes the optimal policy into two dichotomous policies (positive/reward-maximizing and negative/reward-minimizing), each trained with bounded sigmoid-weighted regression losses that avoid the instability of exponential weighting. The final policy is recovered as a linear combination of the score functions of these two policies, enabling controllable greediness during inference. Experiments on ExORL, OGBench, and NAVSIM (with a 1B-parameter VLA model) show consistent improvements over baselines.

## Strengths

1. **Well-motivated problem framing (Sections 1, 3.1).** The paper clearly identifies three failure modes for diffusion policy RL—gradient-through-denoiser instability, Gaussian approximation bias in policy-gradient methods, and loss explosion/domination in exponential-weighted regression—and diagnoses each concretely. This sets up the technical contribution cleanly.

2. **Elegant theoretical derivation (Section 3.2).** The decomposition of the optimal policy from Eq. (5) → Eq. (6) → Eq. (7)–(10) is genuinely clever. Using the identity σ/(1-σ) = exp(βG) to transform an unstable exponential weighting into bounded sigmoid-weighted dichotomous policies, while preserving the same optimal policy, is mathematically sound and practically useful. The connection to classifier-free guidance (Eq. 10) is both theoretically satisfying and algorithmically convenient.

3. **Strong empirical results on RL benchmarks (Tables 1–3).** On ExORL, DIPOLE substantially outperforms all baselines across most tasks (e.g., Walker stand: 953 vs. 873 for IFQL; Quadruped run: 657 vs. 595). The "w/o rejection sampling" variant already surpasses CFGRL, showing the core method drives performance. On OGBench, DIPOLE achieves best or near-best on 4 out of 6 task categories. Offline-to-online results (Table 3) show large improvements (e.g., humanoidmaze-m: 61→97 vs. 56→82 for IFQL). Results use 8 seeds with standard deviations.

4. **Scalability demonstration (Table 4, Section 4.2).** Training a 1B-parameter VLA model with DIPOLE on NAVSIM and obtaining a 6.5-point PDMS improvement (navtest: 88.3→94.8) over the imitation baseline, and 5.8 points over DPPO (89.0), demonstrates the method works at scale and in a challenging real-world domain. The navtrain improvement (+1.4 PDMS) provides a standard offline-to-online comparison.

## Weaknesses

### Major
None.

### Minor