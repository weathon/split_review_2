## Summary

This paper demonstrates that incorporating geometric structure-preserving inductive biases into machine learning models for dynamical systems allows for smaller, more robust models compared to larger structure-naive approaches. The authors investigate two use-cases: a dissipative 2D heat transfer system learned via Riemannian optimization on the symmetric positive definite manifold, and a conservative 18D Fermi-Pasta-Ulam-Tsingou system learned via symplectic Hamiltonian neural networks. The key finding is that structure-aware models achieve superior long-horizon rollout stability and generalization to unseen conditions with significantly fewer parameters.

## Strengths

- **Clear and compelling core message**: The paper makes a strong, well-motivated argument that geometric inductive biases are not just nice additions but can fundamentally change the scaling behavior of models for dynamical systems, reducing the need for massive models. This is a timely and important message for the community.

- **Well-designed comparative study**: The authors carefully benchmark structure-preserving methods against multiple structure-naive baselines (RF, XGBoost, LSTM, NeuralODE) across varying model sizes. The inclusion of both one-step and rollout metrics, plus energy drift, provides a nuanced evaluation that goes beyond simple MSE.

- **Effective use-case selection**: The two use-cases (dissipative heat transfer and conservative FPUT) are well-chosen to represent fundamentally different classes of dynamical systems, strengthening the generality of the paper's claims.

- **Insightful visualization of energy drift**: Figure 4 is particularly effective at showing *why* structure-naive LSTMs fail on long rollouts—they drift across energy levels, while SHNNs stay on the correct energy surface. This provides intuitive understanding of the failure mode.

- **Strong empirical evidence for the central claim**: The results clearly show that small SHNNs (1,441 params) outperform massive LSTMs (97,074 params) on rollout and drift metrics, directly supporting the "smaller models" thesis.

## Weaknesses

### Fatal
None.

### Major
- **Limited scope of the dissipative use-case (2D system)**: The heat transfer system is only 2-dimensional, which severely limits the strength of the claims about "smaller models." A 2D linear state-space model is already extremely simple, and it's not surprising that structure-aware optimization helps. Scaling this to significantly higher-dimensional dissipative systems (e.g., 10+ states) would dramatically strengthen the paper's claims.

- **Unclear novelty of the heat transfer approach**: The use of Riemannian optimization to enforce SPD constraints in LSSMs is presented as a contribution, but this is a relatively standard application of known techniques. The paper does not clearly articulate what is novel beyond applying established Riemannian optimization (RAdam from Bécligneul & Ganea, 2019) to a specific heat transfer identification problem.

- **Missing crucial implementation details for the SPD optimization**: The paper mentions using Cholesky decomposition as an alternative but does not report results for it. More importantly, the Riemannian gradient computation and the retraction used in the optimization are not specified beyond equation (9). How exactly is the exponential map computed on the SPD manifold? What metric (e.g., affine-invariant, Log-Euclidean) is used? These details are essential for reproducibility.

- **Questionable fairness in baseline comparisons for the dissipative case**: The structure-naive baselines (RF, XGBoost, LSTM) are "model-free" time-series approaches. A more fair comparison would include a standard LSSM learned with Euclidean optimization on the Cholesky factor (to enforce SPD), which is mentioned but not compared directly. The EucOpt baseline is not constrained to be SPD, so it's not a fair comparison for whether structure helps within the same model class.

- **The "smaller models" claim is not rigorously quantified**: The paper shows that structure-aware models are smaller than the *best* structure-naive baselines, but the scaling trends in Figure 3 show that for SHNN, test and rollout MSE continue to improve with size (though drift does not worsen). The paper should discuss whether a saturation point exists and whether the structure-aware models have fundamentally better scaling exponents.

### Minor
- **Potential data leakage in the FPUT experiment**: The training and test sets are split chronologically from a *single trajectory*. This tests temporal extrapolation but not generalization to different initial conditions or dynamical regimes. The unseen initial condition test (Figures 4b, 4c) only shows one such condition. Testing on a distribution of unseen conditions would be more convincing.

- **Missing error bars/statistical significance**: Results in Tables 1 and 2 show single values without standard deviations or confidence intervals. Given the stochastic nature of neural network training, repeated runs with different seeds would strengthen the conclusions.

- **The heat transfer results are mixed**: While RieOpt has the best MSE on London data, it is not uniformly better than XGBoost (which has better MSE on T_est2 for London). The paper should discuss this nuance rather than focusing only on the best-case comparison.

### Trivial
- The paper occasionally uses "off-piste" language (e.g., "nudging" for Riemannian optimization) that, while engaging, could be clarified for precision.

## Nice-to-Haves

- Include results for the Cholesky-parameterized SPD optimization as a baseline to isolate the effect of Riemannian optimization vs. reparameterization.
- Show learning curves for all models to support the claim about slower training convergence for structure-naive methods.
- Add a more challenging dissipative example (e.g., heat transfer in 2D or 3D spatial domain) to demonstrate scaling.

## Novel Insights

Beyond the paper's own results, the key insight is that the relationship between model size and generalization is fundamentally different for structure-preserving models vs. structure-naive ones. For structure-naive models, larger size primarily improves one-step accuracy but does not reliably improve long-horizon stability or energy drift. For structure-preserving models, even modest sizes achieve excellent long-horizon behavior because the inductive bias directly controls the qualitative properties of the dynamics (energy conservation, phase-space volume preservation). This suggests that rather than simply scaling up neural networks, the community should invest more in identifying and encoding the right inductive biases for each problem class. The paper also implicitly highlights that standard metrics (one-step MSE) are poor proxies for model quality in dynamical systems, and that energy drift or phase-space metrics should be standard for evaluation.

## Suggestions

- Add a paragraph explaining the specific Riemannian metric and exponential map used for the SPD manifold optimization.
- Report results with multiple random seeds and error bars.
- Test the FPUT models on several different unseen initial conditions drawn from a distribution.
- Add a direct comparison of Cholesky-parameterized LSSM vs. Riemannian-optimized LSSM to isolate the effect of the optimization scheme.
- Consider adding experiments on a higher-dimensional dissipative system (even synthetic) to strengthen the generality of the claims.

## Score and Decision

MY FINAL SCORE: 6.0score
MY FINAL DECISION: Accept