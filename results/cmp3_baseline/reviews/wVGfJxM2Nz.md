## Summary

This paper argues that structure-preserving inductive biases in machine learning models for dynamical systems reduce the need for large models and large datasets while improving generalization. The authors demonstrate this through two case studies: (1) a dissipative 2D heat transfer system where a linear state-space model is learned with a symmetric positive definite (SPD) constraint via Riemannian optimization, and (2) a conservative 18D Fermi-Pasta-Ulam-Tsingou (FPUT) system where a symplectic Hamiltonian neural network (SHNN) is used. The results show that these geometry-aware models achieve better long-horizon rollout accuracy and energy conservation with far fewer parameters compared to structure-naive baselines like LSTMs, XGBoost, and NeuralODEs.

## Strengths

- **Clear and compelling central thesis**: The paper makes a well-motivated argument that geometric inductive biases can replace model scale, which is an important and timely message for the ML community.
- **Two complementary case studies**: Covering both dissipative (heat transfer) and conservative (FPUT) systems demonstrates the breadth of the claim across different dynamical regimes.
- **Strong empirical evidence for the conservative case**: The SHNN with only 1,441 parameters achieves significantly better rollout MSE and energy drift than an LSTM with 97,074 parameters, which is a striking and convincing result.
- **Rigorous experimental design**: The authors sweep over multiple model sizes, report one-step, rollout, and energy drift metrics, and test on both in-distribution and out-of-distribution conditions (Chicago weather for heat transfer, perturbed initial conditions for FPUT).

## Weaknesses

### Major

- **The dissipative case study is not a fair comparison**: The structure-naive baselines (RF, XGBoost, LSTM) are trained as pure time-series predictors, while the structure-preserving methods (RieOpt, EucOpt) are initialized from a physics-derived LSSM. The paper states that the initial matrix A is "derived from Physics but misspecified" (Section 2.1.2), meaning the structure-preserving methods start with a strong physics prior that the baselines do not have. This confounds the effect of structure preservation with the effect of having a good initialization. A fairer comparison would initialize the baselines with the same physics-informed prior or train the structure-preserving methods from scratch.
- **The dissipative results are not as clean as claimed**: In Table 1, for the London test set, XGBoost achieves lower MSE on T_ext2 (1.06e-01) than RieOpt (5.07e-01), and RF achieves lower MSE on T_ext1 (6.81e-01) than RieOpt (4.00e-01) only by a modest margin. The paper's claim that structure-naive models "demonstrate instability" on the Chicago out-of-distribution test is supported, but the in-distribution results are more mixed. The paper also does not report confidence intervals or standard deviations, making it hard to assess statistical significance.
- **Missing details on the heat transfer data generation and training**: The paper mentions synthetic data from EnergyPlus but does not specify the noise level, if any, added to the measurements. Real-world sensor data would have noise, and it is unclear how the methods perform under noisy conditions. Additionally, the training procedure for the structure-naive baselines (e.g., hyperparameter tuning, sequence length for LSTM) is not described, making reproducibility difficult.
- **The paper overclaims on "smaller models" without a rigorous definition**: The title and abstract emphasize "smaller models," but the comparison is not always apples-to-apples. For the heat transfer case, the LSSM has only 4 parameters (2x2 A matrix + 2x1 B matrix), while the LSTM likely has thousands. This is a valid point, but the paper should more explicitly discuss the trade-off: the LSSM is small because it is a linear model, not just because it is structure-preserving. The SHNN vs. LSTM comparison is cleaner in this regard.

### Minor

- **The paper's description of the SPD manifold and Riemannian optimization is somewhat imprecise**: The text states that the discrete-time matrix Φ_A belongs to the SPD manifold, but the condition for stability in discrete time is that eigenvalues lie inside the unit circle, not that the matrix is positive definite. A symmetric matrix with eigenvalues in (0,1) is indeed positive definite, but the paper's explanation of the mapping from the s-plane to the z-plane (Section 2.1.1) is confusing and contains errors (e.g., "Re(λ_i) > 0" in the z-plane is not the stability condition). This does not invalidate the method but weakens the theoretical exposition.
- **The paper does not discuss the computational cost of Riemannian optimization**: The RieOpt method requires computing exponential and logarithmic maps on the SPD manifold at each iteration, which is more expensive per step than Euclidean optimization. The paper should at least mention this trade-off.
- **The FPUT system is only tested with α=0.25**: It would be stronger to show results for multiple nonlinearity strengths (e.g., α=0.1, 0.5) to demonstrate robustness.

### Trivial

- Figure 1(b) is labeled with "T_ext3" on the z-axis, but the system only has two states (T_ext1, T_ext2). This appears to be a labeling error in the figure.
- Equation (7) has a typo: it should be Φ_B U_i, not Φ_B T_i.

## Nice-to-Haves

- Add confidence intervals or standard deviations to all reported metrics.
- Test the heat transfer case with noisy measurements to assess robustness.
- Include a baseline where the structure-naive models are also initialized with the physics-derived LSSM (e.g., by using the physics model as a feature or as a warm-start).
- For the FPUT case, show results for multiple values of α to demonstrate generality.

## Novel Insights

None beyond the paper's own contributions. The paper's main insight—that geometric inductive biases can dramatically reduce model size while improving generalization—is well-illustrated by the experiments, but the individual techniques (Riemannian optimization for SPD matrices, symplectic neural networks) are not novel. The value lies in the comparative study and the clear demonstration of the principle.

## Suggestions

- Reframe the dissipative case study to separate the effect of the physics-based initialization from the effect of the SPD constraint. One way is to train the structure-preserving method from a random initialization (e.g., a random symmetric matrix) and compare to baselines also trained from scratch.
- Correct the technical inaccuracies in the description of the SPD manifold and the z-plane mapping (Section 2.1.1).
- Report results with error bars or multiple random seeds to establish statistical significance.

## Score and Decision

The paper makes a valuable and well-communicated point about the benefits of geometric inductive biases, and the conservative case study provides strong evidence. However, the dissipative case study has a significant confound (physics-based initialization) that weakens the overall claim, and the paper overstates its conclusions slightly. The core idea is sound and the paper is clearly written, but the experimental design for the first case study needs improvement to fully support the title's promise.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>