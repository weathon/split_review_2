## Summary

The paper introduces Ano, a stochastic optimizer that decouples update direction (momentum sign) from magnitude (instantaneous gradient norm) to improve robustness in noisy and non-stationary optimization landscapes. Anolog extends this with a logarithmic momentum schedule that reduces hyperparameter sensitivity. The authors provide non-convex convergence guarantees (O(K^{-1/4})) and evaluate extensively on CV, NLP, and deep RL benchmarks, demonstrating clear gains in RL and smaller noisy tasks while remaining competitive on standard supervised benchmarks.

## Strengths

- **Clear problem motivation and simple, intuitive design.** The paper correctly identifies that momentum-coupled magnitude estimation in Adam can degrade under noise, and proposes a straightforward decoupling that is easy to implement and understand.
- **Strong and comprehensive empirical evaluation.** The paper covers multiple domains (CIFAR, ImageNet proxy? Actually CIFAR-10/100, GLUE, MuJoCo SAC, Atari PPO), with ablations, hyperparameter sensitivity studies, and noise injection experiments. The RL results show consistent improvements over strong baselines (Adam, RMSprop, Adan, Lion, Grams) with 10+ seeds.
- **Ablation study convincingly justifies design choices.** The ablation in Table 6 systematically isolates the effect of each component (second-moment rule, gradient/momentum norm, direction, scheduling) and shows that the full Ano design yields the best performance in the intended noisy regime.

## Weaknesses

### Major

- **Novelty is incremental relative to existing sign-based and direction-magnitude decoupling methods.** The core idea – using momentum sign for direction and raw gradient for magnitude – is a specific combination of ideas from Signum/Lion (sign direction) and Grams (momentum norm scaling). The Yogi-like variance update is also a known technique. While the specific recipe may be new, the paper’s contribution is more an engineering combination than a conceptual leap.
- **Theoretical result is not stronger than existing analyses.** The O(K^{-1/4}) convergence rate matches that of Signum and Lion, and is slower than Adam’s O(K^{-1/2}). The proof relies on standard assumptions and a sign-mismatch lemma. The theory does not provide new insight beyond confirming that Ano behaves like other sign-based methods in the worst case.
- **Limited evidence of superiority in the low-noise supervised regime.** The paper explicitly states that Ano is not designed for CV/NLP dominance, but the title “Faster Is Better in Noisy Landscapes” and the claimed “competitive” performance are weakly supported: improvements on CIFAR-100 and GLUE are within 1–2 percentage points and often within confidence intervals. This is not a fatal flaw but reduces the generality of the contribution.

### Minor

- **Missing comparison to Yogi in RL experiments.** Since the method uses a Yogi-like variance update, comparing directly to Yogi (or a Yogi variant) would help isolate the benefit of the decoupling.
- **The proxy tuning for RL (100k steps on HalfCheetah) may bias hyperparameters towards faster initial learning.** The authors acknowledge this and take the better of default/tuned, but the tuned results could still be suboptimal for longer horizons. The paper reports consistent trends, so this is not critical.
- **The paper does not report training wall-clock times or memory usage.** While both are likely similar to Adam, showing this explicitly would strengthen the claim of “same memory cost as Adam” and practical efficiency.

## Nice-to-Haves

- A comparison to a variant that uses gradient sign (like SignSGD) with instantaneous magnitude would further isolate the effect of momentum direction.
- Reporting results on a larger-scale CV task (e.g., ImageNet-1k with a ResNet-50) would better support the claim of being “competitive” in low-noise settings, even if not expected to outperform.

## Novel Insights

The paper’s main insight is empirical: decoupling the momentum sign from momentum magnitude (replacing it with raw gradient norm) is particularly effective in reinforcement learning, which is characterized by high gradient noise and non-stationarity. While the individual components are known, the specific combination and the thorough RL validation constitute a useful contribution. The ablation confirms that both components (gradient magnitude and momentum sign) are necessary and complementary.

## Suggestions

- Add a direct comparison to Yogi in the main RL tables.
- Include a brief analysis of why momentum sign + raw gradient norm yields larger effective steps in noisy settings, potentially linking to Figure 3’s robustness results.

## Score and Decision

Score: 6  
Decision: Borderline Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>