## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs), which generate intermediate reasoning traces before final answers. The correct marginal objective (summing over all traces) is intractable, and the standard single-trace surrogate suffers from high gradient variance. The authors propose **BVPO**, which mixes the high-variance trace-based gradient with a low-variance "empty-trace" gradient (obtained by suppressing reasoning) via convex combination, and optimizes the mixing weight to minimize mean squared error (MSE) relative to the true marginal gradient. Theoretically, they prove variance reduction, MSE-optimality, and tighter SGD convergence bounds. Empirically, BVPO improves alignment by up to 7.8 points on AlpacaEval 2 and 6.8 points on Arena-Hard over strong baselines, while also improving math reasoning performance by up to 4.0 points on average across six benchmarks.

## Strengths

- **Timely and well-motivated problem**: Aligning LRMs with human preferences is a critical, largely unexplored area. The paper clearly identifies trace-induced gradient variance as a key bottleneck.
- **Principled and simple method**: BVPO is a drop-in, convex combination of two gradient estimators with a clean bias–variance justification, compatible with any preference optimization algorithm (here DPO).
- **Strong theoretical guarantees**: Theorems 1–4 connect variance reduction, MSE-optimal mixing, and SGD convergence, establishing a principled link between statistical optimality and algorithmic performance.
- **Consistent and substantial empirical gains**: Across three LRMs (7B, 1.5B, 8B) and two alignment benchmarks, BVPO outperforms DPO and SimPO, sometimes by several points. The additional result that alignment with general data can improve math reasoning is noteworthy.
- **Reproducible evaluation setup**: The use of standard benchmarks (AlpacaEval 2, Arena-Hard, six math reasoning sets) and clear model variants (Thinking/NoThinking) facilitates comparison.

## Weaknesses

### Fatal
*None.*

### Major
1. **Practical selection of the mixing coefficient α is not described.** The paper derives a closed-form MSE-optimal α (Theorem 2) but does not explain how α is chosen in experiments. This formula requires quantities (biases, covariances) that are not readily available in practice. If α was tuned as a hyperparameter or set to a fixed value, that should be stated; if it was estimated from data, the estimation procedure should be detailed. Without this, the experimental results cannot be faithfully reproduced, and the claim of "MSE-optimal" mixing is disconnected from the actual implementation.

2. **The empty-trace estimator's definition and validity are underspecified.** The paper conditions on an empty trace `r = ∅` by appending `