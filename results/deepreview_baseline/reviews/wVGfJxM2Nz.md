## Summary

This paper argues that geometry-informed inductive biases (SPD manifold constraints for dissipative systems, symplectic structure for conservative systems) enable machine learning models to be much smaller than structure-naive baselines while achieving superior long-horizon generalization. Two case studies support the claim: system identification of a 2D heat transfer system via Riemannian optimization on the SPD manifold, and modeling the 18-dimensional FPUT chain using symplectic Hamiltonian neural networks (SHNNs). The key empirical finding is that compact structure-preserving models (e.g., 1,441-parameter SHNN) outperform much larger baselines (e.g., 97,074-parameter LSTM) on rollout accuracy and energy drift.

## Strengths

- **Compelling central message**: The paper clearly articulates and empirically supports the idea that geometric structure preservation is a more efficient path to generalization than simply scaling up model size – an important lesson for the community.
- **Well-designed comparative experiments**: Both use cases include systematic sweeps over model size (parameters) and multiple baseline methods (LSTM, NeuralODE, RF, XGBoost, Euclidean optimization), allowing direct comparison of structure-aware vs. naive models under controlled conditions.
- **Diverse coverage**: By addressing both dissipative and conservative systems, the paper demonstrates breadth and suggests the principle applies across different classes of physical dynamics.
- **Clear visualization of stability**: Figures 2 and 4 provide intuitive visual evidence of energy drift vs. preservation, making the failure mode of naive models tangible.

## Weaknesses

### Fatal

None.

### Major

- **Dissipative use-case is too simple to strongly support the general claim**: The system is a 2D linear model where the correct dynamics are exactly linear. That a linear model with a stability constraint outperforms large nonlinear baselines is expected and does not demonstrate that structure preservation enables *smaller* models in challenging nonlinear settings. A higher-dimensional or nonlinear dissipative example would be needed to validate the paper's thesis in that regime.
- **Limited novelty relative to existing methods**: Both techniques (Riemannian optimization on SPD for linear state-space models; symplectic Hamiltonian neural networks) are already established. The paper's contribution is primarily empirical — a comparative demonstration — rather than a new method or theoretical insight.
- **Conservative-case baselines exclude other structure-preserving approaches**: The paper compares SHNN against naive LSTM and NeuralODE but not against other structure-preserving baselines (e.g., standard HNN without symplectic integrator, SympNets). This makes it difficult to isolate what aspect of the inductive bias (Hamiltonian parameterization vs. symplectic integrator) drives the improvement.
- **No analysis of failure modes or limitations**: The paper does not discuss scenarios where the assumed geometric structure is misspecified (e.g., nearly-Hamiltonian with weak dissipation, or systems whose dynamics do not exactly live on an SPD/symplectic manifold). This would strengthen the practical guidance for practitioners.

### Minor

- **Rollout length is modest**: The conservative system uses 1,000-step rollouts; for Hamiltonian dynamics, long-time energy behavior over many more periods would be a stronger test. The paper claims "long roll-out generalization" but does not demonstrate stability over, e.g., 10,000+ steps.
- **Some unclear writing in geometry exposition**: For example, the description of the s-plane to z-plane mapping in Section 2.1.1 is garbled ("within the unit circle in the s-plane where Re(λ_i) > 0") and could mislead readers.
- **Discrepancy in notation**: In Section 2.1, the input matrix U is described as ℝ^{1×1} but earlier it is ℝ^{2×1} (and the B matrix is 2×1). Minor but sloppy.

### Trivial

None significant.

## Nice-to-Haves

- Include an additional dissipative benchmark that is nonlinear (e.g., a forced Duffing oscillator or Van der Pol system) to strengthen the generalizability claim.
- Compare SHNN against standard HNN (without symplectic integrator) to separate the effect of Hamiltonian parameterization from the symplectic discretization.
- Provide longer rollouts (e.g., 10,000 steps) to demonstrate energy drift stability over extended horizons.
- Add a discussion about the computational cost of Riemannian optimization vs. Euclidean optimization in the dissipative case.

## Novel Insights

None beyond the paper's own contributions. The empirical result that a 1,441-parameter SHNN dramatically outperforms a 97,074-parameter LSTM on energy drift is a concrete and useful data point, but the underlying principle (structure preservation reduces model complexity) is already well-understood in the scientific ML community. The paper's value lies in a clean, controlled demonstration rather than a new insight.

## Suggestions

- **Strengthen the dissipative case**: Either replace it with a nonlinear dissipative system (e.g., a heat equation with temperature-dependent conductivity or a simple chaotic attractor) or explicitly clarify that the LSSM example is intended only as a proof-of-concept for stable linear systems, and note that the true test of the "smaller models" claim would require nonlinear dissipative dynamics.
- **Add a structure-preserving baseline for the conservative case**: Include standard HNN or SympNet in the comparison to isolate the contribution of the symplectic integrator.
- **Quantify "smaller" more rigorously**: Report the number of trainable parameters for the heat transfer physics-grounded initial model (which implicitly has structure) vs. the RieOpt learned model, and relate this to the number of parameters in the naive baselines.
- **Repair the confusing mapping description in Section 2.1.1** for clarity.

## Score and Decision

Score: 6.0 — Borderline accept. The paper presents a clean, well-executed empirical study that supports an important and timely point about structure-preserving ML. However, the limited novelty and the weakness of the dissipative example prevent it from being a stronger accept. The work is likely to be useful as a tutorial/reference for practitioners adopting geometric priors, but it does not introduce a new method or deep theoretical advance.

MY FINAL SCORE: 6.0</score>  
MY FINAL DECISION: Accept (borderline)</decision>