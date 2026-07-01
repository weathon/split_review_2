## Summary

The paper introduces TD-JEPA, a novel zero-shot unsupervised RL method that learns latent-predictive representations via temporal difference (TD) learning. It trains separate state and task encoders, a policy-conditioned multi-step predictor, and parameterized policies entirely in latent space from offline, reward-free transitions. The method is theoretically connected to successor measures, and empirically demonstrates state-of-the-art or competitive performance across 65 tasks on 13 datasets from ExoRL and OGBench, particularly excelling in pixel-based settings.

## Strengths

- **Novel technical contribution:** The paper proposes a principled combination of TD learning with latent-predictive representations for multi-policy, off-policy, zero-shot RL. The TD-based latent-predictive loss (Eq. 9) is a clean and effective way to learn long-term dynamics from offline data without rewards.
- **Strong theoretical grounding:** The paper provides rigorous theoretical analysis (Theorems 1–4) showing that TD-JEPA learns a low-rank factorization of successor measures, avoids collapse via covariance preservation, and minimizes an upper bound on policy evaluation error. The gradient matching argument generalizes prior theory for latent-predictive methods.
- **Extensive empirical evaluation:** The method is evaluated on 65 tasks across 13 datasets covering locomotion, navigation, and manipulation with both proprioceptive and pixel-based observations. Comparisons include multiple state-of-the-art zero-shot baselines (FB, HILP, RLDP, BYOL, etc.) with proper tuning and consistent architecture. Results are presented with confidence intervals and a rigorous probability-of-improvement analysis.
- **Practical significance:** TD-JEPA matches or outperforms strong baselines across diverse settings, and its learned representations enable fast downstream adaptation (offline/online fine-tuning), which is a valuable property for real-world deployment.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Strong theoretical assumptions:** The theoretical analysis (Theorems 1–3) relies on linear predictors, symmetric transition matrices, uniform state distribution, and orthogonal representations. While the authors acknowledge these and note they can be relaxed, the practical method uses nonlinear neural networks and does not guarantee these conditions, leaving a gap between theory and practice.
2. **Limited ablation on design choices:** The paper compares TD-JEPA against a symmetric variant (shared encoder) and MC-based variants, but does not provide a systematic ablation studying the impact of key components such as the orthonormality regularization weight \(\lambda\), the predictor architecture, or the target network update frequency. This would help understand which aspects are most critical to performance.
3. **Adapted baselines:** Several baselines (BYOL*, BYOL-\(\gamma\)*, ICVF*) are not originally zero-shot methods and are adapted for this setting. While this is reasonable and done fairly with shared architecture, the comparison may not reflect the full strengths of those methods as originally intended, and the novelty of these adaptations could be considered part of TD-JEPA’s contribution.

### Trivial
- The paper does not include explicit discussion of limitations or failure cases of TD-JEPA, which would be helpful for practitioners.

## Nice-to-Haves

- An analysis of the learned representations (e.g., visualization of latent space, successor feature predictions) to provide intuitive understanding of what TD-JEPA captures.
- Sensitivity analysis of the orthonormality regularization coefficient and the dimension of latent spaces.
- Evaluation on larger-scale real-world robotic datasets (as suggested in the conclusion) to further validate the approach.

## Novel Insights

Beyond the paper’s own contributions, the key novel insight is that temporal difference learning can be integrated into latent-predictive frameworks to enable off-policy, multi-policy learning of successor measures in a way that directly supports zero-shot reward optimization. The paper shows that the predictor in TD-JEPA approximates an oblique projection of the successor measure, which is a deeper characterization than previous one-step latent-predictive analyses. The theoretical connection between TD latent prediction and forward/backward TD losses for successor measures (Theorem 3) is also a new synthesis that generalizes existing results.

## Suggestions

- Include a brief discussion of failure cases or settings where TD-JEPA might underperform (e.g., highly stochastic environments, low-coverage data) to guide practitioners.
- Provide an ablation on the dimensionality of \(\phi\) and \(\psi\) to show the impact on approximation quality and zero-shot performance.
- Consider comparing to a variant of TD-JEPA that uses a single shared encoder but with separate predictors to isolate the benefit of dual encoders.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>