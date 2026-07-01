## Summary

This paper analyzes gradient descent (GD) from a continuous-time dynamical systems perspective, reformulating gradient flow as a second-order ODE. The authors show that GD's stability depends on the curvature of the loss landscape, proving that GD can be unstable even in convex settings when the Hessian is not strictly positive definite. They propose a control-theoretic modification (Controlled Gradient Descent, CGD) that adds a gradient guidance term to guarantee local asymptotic stability regardless of curvature, and validate their approach on synthetic numerical examples.

## Strengths

- **Novel theoretical framing**: The paper provides a clean connection between control theory and optimization by reformulating GD as a second-order dynamical system and analyzing stability via eigenvalue analysis of the Jacobian. This perspective is underexplored in the optimization literature.
- **Clear theoretical contribution**: Theorem 2 and Theorem 3 provide rigorous stability characterizations under different curvature regimes, and the proof that the controlled system achieves local asymptotic stability regardless of curvature is mathematically sound.
- **Well-motivated problem**: The paper correctly identifies that existing stability analyses rely on strong convexity or smoothness assumptions that often fail in practice, and the observation that GD can diverge even in simple convex settings is a genuine concern.

## Weaknesses

### Fatal
None.

### Major
- **The continuous-to-discrete gap is not addressed**: The paper's entire theoretical analysis is in continuous time (ODE), but the proposed algorithm (Algorithm 1) is a discrete update rule. The derivation from Equation 5 to the discrete update is mathematically questionable. Specifically, the integration in Equation 5 yields $\frac{d\theta'}{dt} = \frac{d\theta}{dt} - \frac{1}{2}K_1\theta^2 - K_2\theta$, but this is not a valid integration of the controller term $\mathbf{u} = -K_1\theta - K_2\frac{d\theta}{dt}$ — the integration of $-K_1\theta$ with respect to $t$ is not $-\frac{1}{2}K_1\theta^2$ unless $\theta$ is linear in $t$, which is not generally true. This invalidates the connection between the theoretical controller and the proposed algorithm.
- **The proposed algorithm is essentially a heuristic with no discrete-time stability guarantee**: Even if the continuous-time system is asymptotically stable, the discrete Euler discretization (which is what Algorithm 1 implements) may not preserve stability, especially for large learning rates. The paper acknowledges this as a limitation but does not provide any analysis or mitigation.
- **Experiments are limited to trivial 2D toy problems**: All experiments use 2-parameter quadratic or quartic objectives. There is no evaluation on any realistic machine learning task (e.g., neural network training on CIFAR, MNIST, or even a simple logistic regression on real data). This severely limits the empirical contribution.
- **The "convex but not strongly convex" example is actually strongly convex**: The sphere loss $L(\theta) = \theta_1^2 + \theta_2^2$ has Hessian $2I$, which is positive definite (eigenvalues = 2). This is strongly convex, not "convex but not strongly convex" as claimed. This undermines the experimental validation of the theoretical claims in Section 4.2.2.

### Minor
- **The paper claims GD is "unstable" for convex but not strongly convex losses, but this is a continuous-time analysis**: In practice, discrete GD on a convex quadratic with a zero eigenvalue (e.g., $L(\theta) = \theta_1^2$) converges to the minimum along the non-zero eigenvalue direction and stays constant along the zero eigenvalue direction — it does not diverge. The "instability" is a linear growth in continuous time that may not manifest in discrete GD.
- **The ablation study on hyperparameters is superficial**: Only three values of $k_1=k_2$ are tested (0.05, 0.1, 0.2), and all on the same 2D problems. No analysis of how to choose these parameters or their effect on convergence rate is provided.
- **The paper does not compare against any existing stabilization methods**: No comparison with momentum, Adam, gradient clipping, or other standard techniques that also stabilize training.

### Trivial
- The notation $\theta^2$ for element-wise square is non-standard and could be confused with $\theta$ squared in matrix sense.
- Figure 2(b) and (e) are described as "convex but not strongly convex sphere" but the loss is $L(\theta) = \theta_1^2 + \theta_2^2$, which is strongly convex.

## Nice-to-Haves

- A discrete-time stability analysis (e.g., using Lyapunov theory for difference equations) would significantly strengthen the paper.
- Experiments on at least one standard deep learning benchmark (e.g., training a small CNN on CIFAR-10) would greatly improve empirical validation.
- Comparison with momentum-based methods (which also modify the gradient dynamics) would help contextualize the contribution.
- Analysis of how the controller hyperparameters $K_1, K_2$ affect convergence rate, not just stability.

## Novel Insights

The key insight — that GD's continuous-time dynamics can be analyzed as a second-order ODE whose stability depends on the Hessian's eigenvalue structure, and that a PD controller can guarantee asymptotic stability — is genuinely novel and potentially useful. However, the paper does not fully exploit this insight because the connection to practical discrete algorithms is not rigorously established. The observation that zero eigenvalues in the Hessian (from non-strong convexity) cause Jordan blocks that lead to instability in continuous time is a nice theoretical point that is rarely discussed in the optimization literature.

## Suggestions

1. **Fix the derivation of the discrete update**: The integration in Equation 5 is mathematically incorrect. Either provide a correct derivation (e.g., using a different controller formulation that integrates cleanly) or acknowledge that the discrete algorithm is a heuristic inspired by the continuous analysis and analyze its properties separately.
2. **Correct the experimental setup**: The "convex but not strongly convex" example should use a genuinely non-strongly convex function (e.g., $L(\theta) = \theta_1^2$ with a zero eigenvalue direction, or $L(\theta) = \theta_1^4$ which has zero Hessian at the minimum).
3. **Add realistic experiments**: Even a simple logistic regression on a real dataset would significantly strengthen the paper.
4. **Provide guidance on choosing $K_1$ and $K_2$**: The paper says they can be chosen as $\mu I$ with $\mu > 0$ and $K_2 \succ -H(\theta)$, but in practice the Hessian is unknown. How should practitioners set these parameters?

## Score and Decision

The paper presents a novel theoretical perspective on GD stability using control theory, and the core theoretical results (Theorem 2 and Theorem 3) are sound within the continuous-time framework. However, the paper has two critical flaws: (1) the derivation connecting the continuous-time controller to the discrete algorithm is mathematically invalid, and (2) the experiments are limited to trivial 2D problems and contain a factual error (mislabeling a strongly convex function as non-strongly convex). These issues prevent the paper from making a convincing case that the proposed method is practically useful or that the theoretical insights translate to actual algorithms. The paper would need substantial revision to address these concerns.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>