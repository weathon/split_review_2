## Summary
# Final Review Report

## Summary

This paper proposes DIPOLE (Dichotomous Diffusion Policy Improvement), a reinforcement learning algorithm for fine-tuning diffusion-based policies. The core technical contribution is a reformulation of the KL-regularized RL objective that replaces the standard exponential weighting (which can cause training instability) with a sigmoid-weighted dichotomous decomposition. The optimal policy is expressed as a ratio of a "positive" policy (reward-maximizing) and a "negative" policy (reward-minimizing), both trained with bounded sigmoid weights. During inference, the score estimates of these two policies are linearly combined, structurally similar to classifier-free guidance, providing controllable greediness via a hyperparameter ω.

The method is evaluated in offline and offline-to-online RL settings on 39 tasks across ExORL and OGBench benchmarks, showing competitive or superior performance against baselines including IQL, ReBRAC, IFQL, FQL, and CFGRL. Additionally, DIPOLE is scaled to a 1-billion parameter vision-language-action (VLA) model for autonomous driving, achieving improved closed-loop simulation scores on the NAVSIM benchmark over an imitation-learning pre-trained baseline.

**Key strengths:** Clean theoretical derivation connecting KL-regularized RL, sigmoid-weighted dichotomous decomposition, and classifier-free guidance; strong empirical results across multiple benchmarks; impressive scaling to a large VLA driving model.

**Key weaknesses:** (1) The method requires two separately trained diffusion models (~2x parameters vs single-model approaches), and the performance contribution from increased model capacity versus the algorithmic innovation is not disentangled; (2) Several reproducibility-critical training details are omitted from the main text; (3) NAVSIM evaluation lacks statistical significance reporting and has an unexplained performance gap between data splits; (4) The connection to classifier-free guidance is structurally correct but operationally different (separately trained models vs. conditional/unconditional dropout) and this distinction is not acknowledged; (5) The abstract and conclusion overclaim "real-world" applicability based solely on closed-loop simulation results.

**Note:** External literature verification was unavailable in this run (Retrieval-Disabled Mode); novelty and comparison conclusions are intentionally deferred to manual verification.

## Strengths
1. **Novel theoretical connection.** The paper establishes a clean derivation linking KL-regularized RL, sigmoid-weighted dichotomous decomposition, and classifier-free guidance in diffusion models. The insight that the optimal policy under a greedified KL objective naturally factorizes into positive and negative components, and that these can be combined via a CFG-like score combination, is mathematically elegant and provides a principled framework for controllable greediness.

2. **Strong empirical breadth.** DIPOLE is evaluated on 39 tasks across diverse benchmarks (ExORL, OGBench) covering locomotion, manipulation, maze navigation, and object interaction. The results are consistent across settings, with DIPOLE achieving best or near-best performance in most task categories — particularly notable on challenging long-horizon tasks (cube-double-play: 44 vs next-best 29; scene-play: 60 vs next-best 56).

3. **Scaling to large VLA models.** The demonstration of DIPOLE on a 1-billion parameter vision-language-action model for end-to-end autonomous driving is a significant engineering achievement. The NAVSIM closed-loop results (PDMS 94.8 on navtest) show that the method can scale to realistic, high-dimensional control tasks far beyond the standard RL benchmarks.

4. **Algorithmic stability.** The core motivation — replacing unstable exponential weighting with bounded sigmoid-based dichotomous weights — directly addresses a well-known limitation of weighted regression approaches. The claim that this stabilizes training is supported by the mathematical structure (sigmoid outputs in [0,1] vs exponential values that can grow arbitrarily large) and the consistent performance across tasks.

5. **Controllable inference.** The ω hyperparameter provides an intuitive interface for adjusting the greediness of action generation without retraining, which is a practical advantage for deployment scenarios where risk tolerance may vary.

## Weaknesses
### W1. Model capacity confound in comparisons (Major)
DIPOLE uses two separately trained diffusion models ($\epsilon_{\theta_1}^+$ and $\epsilon_{\theta_2}^-$) — effectively doubling the parameter count compared to single-model baselines like CFGRL, IFQL, and FQL. The paper does not control for this capacity difference. Some performance gains attributed to the algorithmic design may instead come from increased model capacity. This is a significant confound because weighted regression baselines (e.g., the exp-weighted approach in Eq. 4) with double capacity might also show improved performance.

**Evidence:** Table 1 shows DIPOLE w/o rs outperforms CFGRL across most tasks, but both the algorithmic decomposition AND the extra model capacity contribute to this gap. The paper does not include a capacity-matched ablation.

**Action required:** Add an ablation comparing DIPOLE against a single-model baseline with matched total parameter count (e.g., a single diffusion model with 2x width/depth), or compare against an ensembled version of baselines.

### W2. Rejection sampling contribution not disentangled (Major)
The paper reports "DIPOLE" (with rejection sampling during inference) separately from "DIPOLE w/o rs" (without rejection sampling). The gap between these two variants is substantial — e.g., on Walker-stand: 953 vs 793 (+20%), Walker-walk: 910 vs 679 (+34%), Walker-run: 442 vs 256 (+73%). This indicates that rejection sampling, which is an inference-time compute strategy rather than part of the core algorithmic contribution, accounts for a large fraction of the reported gains.

**Action required:** Clearly separate the contribution of rejection sampling from the algorithmic innovation. Add analysis showing how much of the improvement over baselines remains when all methods use comparable inference-time compute.

### W3. Reproducibility gaps in experiment description (Major)
The main text omits several critical details needed to reproduce the results: (a) the number of training updates and training hyperparameters (batch size, learning rate, etc.); (b) how the value function $Q$ and $V$ are learned — the method uses advantage $A(s,a)$ in Eq. (9), but advantage estimation itself requires value learning, which is a separate challenge in offline RL; (c) the data collection protocol for ExORL datasets (described only as "collected by RND"). These details are deferred to appendices that are not available in the current excerpt.

**Action required:** Add a concise summary of key hyperparameters and the value learning procedure in the main text. At minimum, state the Q-learning method (e.g., "We use clipped double Q-learning with expectile regression as in IQL") and the number of gradient steps.

### W4. NAVSIM evaluation lacks statistical rigor (Major)
Table 4 reports NAVSIM scores as single numbers without variance or confidence intervals. Given that PDMS differences between methods can be small (Hydra-MDP: 86.5, DP-VLA: 88.3, DP-VLA w/ DIPOLE navtrain: 89.7), readers cannot assess whether the reported improvements are statistically significant. Additionally, the large gap between navtrain (+1.4 PDMS) and navtest (+6.5 PDMS) improvements is not explained.

**Action required:** Report results over at least 3 random seeds with standard deviations. Explain the navtrain/navtest performance discrepancy.

### W5. "Real-world" applicability overclaimed (Minor)
The abstract and conclusion claim "potential for complex real-world applications" based on NAVSIM results. However, NAVSIM is a closed-loop simulator, not a real-world driving test. While the use of real-world data is commendable, the evaluation does not address domain shift, sensor noise, or deployment constraints that characterize genuine real-world operation.

**Action required:** Replace "real-world applications" with "closed-loop simulation on real-world datasets" or similar bounded language throughout the paper.

### W6. CFG analogy overclaimed without operational distinction (Minor)
The paper states that the score combination in Eq. (10) is "remarkably similar to classifier-free guidance" and frames this as a theoretical contribution. While the functional form is identical, the operational mechanism is different: CFG uses a single model with conditioning dropout, while DIPOLE uses two separately trained models with different objectives. This distinction is important for reproducibility and for correctly positioning the contribution.

**Action required:** Add a sentence acknowledging that unlike standard CFG, DIPOLE's positive and negative policies are independently trained with different weighting schemes.

### W7. Greediness-stability trade-off not formally defined (Minor)
The paper repeatedly refers to a "greediness-stability trade-off" but never provides a formal definition of either term. "Greediness" could refer to the expected value of the policy distribution, the mode-seeking behavior, or the divergence from the reference policy. Without a precise definition, the claimed "perfect controllability over greediness" is difficult to verify.

**Action required:** Formally define greediness (e.g., as $\mathbb{E}_{a\sim\pi}[G(s,a)]$ relative to the reference policy) and stability (e.g., as the variance of the training loss or gradient norm) in Section 3.1 or 3.2.

### W8. Normalization factor Z(s) not discussed (Minor)
Equation (5) introduces a reference policy weighted by $\sigma(\beta G(s,a))/Z(s)$, where $Z(s)$ is described as "the normalization factor." The paper does not explain how $Z(s)$ is handled in practice. While it likely cancels out in the closed-form solution, the computational tractability of the greedified objective in Eq. (5) is not fully justified without discussing this.

**Action required:** Add a clarifying note that $Z(s)$ cancels in the derivation and never needs to be computed because the training losses in Eq. (9) use unnormalized weights.

### W9. Related Work lacks positioning clarity (Minor)
The Related Work section covers four method families in a single dense paragraph without explicit comparison axes. DIPOLE's position in the taxonomy is not clearly stated, making it hard for readers to understand what specific limitations it addresses.

**Action required:** Restructure as a brief table or clearly separated paragraphs organized by learning strategy, with an explicit statement of where DIPOLE fits and how it overcomes specific limitations of each family.

### External Literature Verification (Deferred)
Novelty and comparison conclusions are explicitly deferred to manual verification because external paper search was unavailable in this run (Retrieval-Disabled Mode). The paper's claims about outperforming "state-of-the-art" baselines should be independently verified against the most recent literature, particularly against concurrent or closely related works on diffusion policy optimization.

## Score
**Final Score: 7/10**

**Scoring rationale:**
- **Theoretical contribution and method design (7/10):** The core idea of dichotomous policy decomposition via sigmoid-weighted KL-regularized RL is mathematically sound and elegantly connects to classifier-free guidance. However, several missing formal definitions (greediness, stability) and an unaddressed normalization factor slightly reduce the theoretical completeness.
- **Empirical evidence (6/10):** The experimental breadth across 39 tasks is commendable, but the evidence is weakened by: (a) the model capacity confound not being addressed; (b) the large contribution of rejection sampling not being separated from the algorithmic contribution; (c) missing statistical significance in NAVSIM results; (d) key reproducibility details deferred to appendix. These issues reduce confidence in the exact magnitude of the reported improvements.
- **Novelty (deferred):** External literature verification was unavailable in this run. The paper's novelty positioning relative to concurrent diffusion policy optimization methods should be independently verified. The technical approach (dichotomous decomposition + CFG-style combination) appears novel within the KL-regularized diffusion policy literature, but a definitive assessment requires manual literature survey.
- **Writing and presentation (7/10):** The paper is generally well-structured with clear derivations. However, the abstract overclaims real-world applicability, the Related Work section lacks positioning clarity, and the conclusion omits necessary limitations discussion.

**Summary:** DIPOLE presents a theoretically grounded and practically demonstrated contribution to diffusion policy optimization. The main weaknesses are experimental confounds that should be addressed before publication, particularly regarding model capacity, rejection sampling, and statistical rigor. After addressing these issues (especially W1-W3), the paper would be suitable for a top-tier venue.