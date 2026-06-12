## Summary
The paper introduces Ano, a stochastic optimizer that decouples update direction (from momentum sign) and step-size magnitude (from instantaneous gradient norm), combined with a modified Yogi-style second-moment estimate with an explicit decay factor. The authors also propose Anolog, which uses a logarithmic momentum schedule to reduce hyperparameter sensitivity. Non-convex convergence guarantees of Õ(K^{-1/4}) are established, and experiments across CV, NLP, and reinforcement learning demonstrate strong performance particularly in noisy and non-stationary regimes.

## Strengths
- **Well-motivated design with clear decoupling principle**: The paper provides a clean decomposition of the update into direction (sign of momentum) and magnitude (instantaneous gradient norm), directly addressing the observation from Balles & Hennig (2018) that momentum sign captures most directional information. The comparison to Adam's decomposition (Equations 1-2) makes the design choice transparent.
- **Strong RL results across multiple algorithms and environments**: Ano achieves first-place ranking in 4/5 MuJoCo tasks under SAC (default settings) with +10% normalized improvement, and ranks first overall on Atari-5 under PPO. The convergence curves (Figures 2 and 4) show faster learning and often higher final performance. The hyperparameter robustness heatmaps (Figure 3) convincingly show Ano is less sensitive than Adam to learning rate and beta choices.
- **Thorough ablation study (Table 6)**: The ablation isolates the contribution of each component — second-moment rule, gradient normalization, gradient magnitude, momentum direction, and momentum schedule — providing clear evidence that the design choices are complementary and necessary.
- **Honest experimental positioning**: The authors transparently frame CV and NLP experiments as "diagnostic checks" rather than claiming superiority in all domains, and clearly delineate the intended target regime (noisy, non-stationary) versus standard supervised learning. This intellectual honesty strengthens confidence in the RL results.
- **Practical extension via Anolog**: The logarithmic momentum schedule eliminates the need to tune β₁, with the ablation showing it outperforms theoretically-motivated √k schedules in DRL — a useful practical finding.

## Weaknesses
### Fatal
None.

### Major
- **Convergence rate is worse than Adam's**: The Õ(K^{-1/4}) rate is worse than Adam's O(K^{-1/2}), and while the authors acknowledge this stems from the sign-based design requiring decaying step sizes, they don't deeply discuss practical implications. A more detailed discussion of when this theoretical gap matters versus when the empirical noise-robustness advantage compensates would strengthen the paper.
- **Limited experimental scale**: The CV experiments are only CIFAR-100 with ResNet-34, and NLP experiments are BERT-base fine-tuning. While the authors acknowledge this, the lack of any large-scale experiment (e.g., ImageNet training, large language model pre-training, or even larger RL benchmarks) makes it difficult to assess whether the benefits scale or whether the hyperparameter defaults (β₁=0.92, β₂=0.99) remain appropriate.
- **Statistical rigor concerns**: Many comparisons have overlapping confidence intervals (e.g., CIFAR-100 Table 2: Ano 70.31±0.50 vs. Adan 69.87±0.09; several GLUE tasks). No formal statistical tests (e.g., bootstrap hypothesis tests) are reported. For RL, 10 seeds is good, but for CV/NLP with only 5 seeds, the margins are often within noise.

### Minor
- **Second-moment modification novelty**: The Yogi+β₂-decay modification (adding a β₂ multiplier to v_{k-1}) is relatively incremental. The paper would benefit from a deeper analysis of why this specific modification helps — e.g., does it effectively change the effective memory horizon, and by how much?
- **Default hyperparameter fairness**: Ano uses β₁=0.92 and β₂=0.99 by default, while Adam uses β₁=0.9 and β₂=0.999. In the "Default" comparison settings, these differences could contribute to performance differences, and the paper doesn't disentangle this.
- **Grams anomaly in Table 1**: Grams achieves 71.34% at σ=0 but jumps to 77.90% at σ=0.01, which the authors hypothesize is due to noise-induced step-size reduction. While an interesting observation, this could also indicate an issue with the Grams implementation or hyperparameter configuration, warranting further investigation.
- **Anolog performance gap**: Anolog shows notably lower performance than Ano in several settings (e.g., CIFAR-100: 64.84 vs. 70.31; HalfCheetah SAC: 94.50 vs. 99.48 normalized). While positioned as a convenience variant, the gap is sometimes substantial enough to question its practical value.

### Trivial
None.

## Nice-to-Haves
- A comparison of wall-clock time / computational overhead per step across optimizers, since the update rule involves both sign operations and element-wise division.
- An analysis of the effective memory horizon introduced by the β₂-decay in the second-moment rule, potentially showing how it changes the bias-variance tradeoff in the variance estimate.
- Experiments on a slightly larger RL benchmark (e.g., DMControl or full Atari-26) to demonstrate scalability of the gains.

## Novel Insights
The key insight is that in noisy, non-stationary optimization landscapes (particularly RL), using instantaneous gradient magnitudes for step-size scaling while relying on smoothed momentum for direction provides a better bias-variance tradeoff than Adam's coupled scheme, where momentum-based magnitudes can be overly conservative due to noise-induced cancellations. The paper's noise robustness analysis (Table 1) provides concrete evidence that the performance gap widens systematically with noise level, supporting this decoupling thesis. The observation that logarithmic scheduling of β₁ outperforms the theoretically-motivated √k schedule is also noteworthy — it suggests that in non-stationary settings, the momentum window should expand very slowly to maintain responsiveness to recent gradient information.

## Suggestions
- Add formal statistical tests (e.g., stratified bootstrap comparison) for key comparisons, especially where confidence intervals overlap.
- Provide a brief analysis of computational cost per step relative to Adam, since practitioners need to know the overhead.
- Consider running at least one larger-scale experiment (e.g., Atari-26 full suite or a larger CV task) to demonstrate scalability beyond toy/small-scale settings.

## Score and Decision
The paper presents a well-motivated optimizer with clear design principles, solid theoretical grounding, and genuinely strong results in its target domain (RL). The ablation study is thorough and the honest positioning across domains builds credibility. However, the incremental novelty of some components (Yogi modification), limited experimental scale, and convergence rate inferior to Adam's temper enthusiasm. The paper occupies the space between a solid incremental contribution and a clear advance — it would be a reasonable accept at ICLR but falls slightly short of a clear one.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept