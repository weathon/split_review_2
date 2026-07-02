## Summary
# Final Review Report

## Summary

This paper proposes a control-theoretic approach to stabilizing gradient descent (GD) by formulating it as a second-order dynamical system. The authors derive a second-order ODE from the gradient flow dynamics, analyze local stability under different curvature regimes (strongly convex, convex but not strongly convex, concave), and introduce a controller term $\mathbf{u} = -K_1\boldsymbol{\theta} - K_2\frac{d\boldsymbol{\theta}}{dt}$ that guarantees local asymptotic stability regardless of loss curvature (Theorem 3). The controller is then converted into a discrete algorithm (Controlled Gradient Descent, CGD) by integrating the controlled second-order ODE to obtain a modified gradient update. Empirical validation is conducted on synthetic 2D objective functions.

The paper has a clear theoretical motivation and a novel framing of GD stability through second-order control dynamics. The Lyapunov stability analysis in Section 4 is technically sound for the continuous-time setting. However, the paper has several critical issues: (1) the integration in Equation (5) that bridges the continuous-time theory to the discrete algorithm contains a fundamental mathematical error; (2) no neural network experiments are conducted despite the method being styled for "Neural Network Training"; (3) the experimental examples are misclassified (the "convex but not strongly convex" sphere is actually strongly convex); (4) the "variational interpretation" claimed in the Abstract is never developed; and (5) several overclaims about generality and guarantees are not supported by the evidence. The core theoretical contribution is interesting and worth pursuing, but the paper in its current form requires major revisions before it can be accepted.

## Strengths
1. **Novel theoretical framing.** The formulation of gradient descent as a second-order dynamical system and the subsequent stability analysis through linearization are mathematically clean and provide a fresh perspective on GD stability that does not rely on discrete-time analysis artifacts. The connection between the Hessian eigenvalues of the loss and the stability of the continuous-time dynamics via the characteristic polynomial $\det(\lambda^2 I + \lambda H) = 0$ is elegantly derived.

2. **Rigorous application of control theory.** The paper correctly applies standard control-theoretic tools (local linearization, Lyapunov's indirect method, quadratic eigenvalue problems) to the optimization setting. Lemma 4 (Tisseur & Meerbergen) is appropriately cited and used to connect the definiteness of the controller-modified matrices to eigenvalue negativity. This interdisciplinary approach is potentially valuable for designing principled optimization algorithms.

3. **Clear taxonomy of stability by curvature.** The three-case analysis (strongly convex → Lyapunov stable; convex-but-not-strongly → unstable via Jordan blocks; concave → unstable via positive eigenvalues) provides a systematic classification that connects Hessian spectral properties to dynamical stability. Table 1 succinctly summarizes the comparison between GD and CGD.

4. **Ablation on controller hyperparameters.** The paper tests three values of $k_1=k_2 \in \{0.05, 0.1, 0.2\}$ and observes consistent behavior, providing preliminary evidence that CGD is not overly sensitive to these hyperparameters in the tested low-dimensional problems.

5. **Honest limitation discussion.** The Limitations paragraph acknowledges the gap between continuous-time analysis and discrete updates, as well as the need for extension to stochastic and adaptive methods. This self-awareness is commendable, though the main body claims contradict these limitations.

## Weaknesses
**W1 — Critical: Equation (5) contains a fundamental integration error that invalidates the bridge from continuous theory to discrete algorithm (Page 6).** The paper states $\int \mathbf{u}\ dt = \int (-K_1\boldsymbol{\theta} - K_2\frac{d\boldsymbol{\theta}}{dt})\ dt = -\frac{1}{2}K_1\boldsymbol{\theta}^2 - K_2\boldsymbol{\theta}$. This is only correct if $\boldsymbol{\theta}(t) = t$, i.e., a linear function with unit slope. For a general trajectory $\boldsymbol{\theta}(t)$ being optimized, $\int \boldsymbol{\theta}(t)\ dt \neq \frac{1}{2}\boldsymbol{\theta}(t)^2$. This error means Algorithm 1 does not actually implement the controlled dynamics derived in Section 5. The authors must either (a) use a proper discretization (e.g., symplectic/Verlet integration of the second-order ODE) or (b) derive the algorithm from the first-order controlled system directly without the erroneous integration step.

**W2 — Major: Experiments are limited to 2D synthetic quadratics; no neural network experiments despite claims (Page 7-8).** Algorithm 1 is titled "Controlled Gradient Descent for Neural Network Training," yet all three test objectives are 2D quadratics or quartics. There is no actual neural network training, no comparison to SGD/Momentum/Adam, no high-dimensional testing, no stochastic mini-batch setting, and no wall-clock timing. The claims about stabilizing "neural network training" and working for "general non-convex and non-smooth case" are unsubstantiated. A minimal acceptable addition would be an MLP on MNIST or a small CNN on CIFAR-10 with CGD compared to at least SGD and Adam.

**W3 — Major: The "convex but not strongly convex" sphere example is actually strongly convex (Page 7).** The function $L(\boldsymbol{\theta}) = \theta_1^2 + \theta_2^2$ has Hessian $H = 2I$, which is positive definite, satisfying $H \succeq 2I$. By the paper's own Lemma 1, this is strongly convex. This misclassification undermines the experimental validation of Theorem 2's convex-but-not-strongly-convex case, and the paper provides no genuinely non-strongly-convex example.

**W4 — Major: Theorem 2 contains a contradictory typo (Page 3).** The third bullet states "unstable if $L$ is convex but not strongly concave." A function cannot be simultaneously convex and concave unless affine. The intended condition is clearly "concave" (as in Section 4.2.3). This error in a central theoretical statement suggests insufficient proofreading.

**W5 — Major: Controller design requires Hessian knowledge that is impractical in deep learning (Page 5).** The condition $H(\boldsymbol{\theta}) + K_2 \succ 0$ from Definition 4 requires knowing the Hessian's minimum eigenvalue at every point. Remark 2 suggests choosing $K_2 \succ -H(\boldsymbol{\theta})$ for all $\boldsymbol{\theta}$, but this requires a global spectral bound that the paper explicitly avoids assuming. Without a practical selection strategy, the controller cannot be deployed as claimed.

**W6 — Major: The "variational interpretation" advertised in the Abstract is never developed (Page 1).** The Abstract claims the controller "admits a variational interpretation," but the term "variational" does not appear again in Sections 5-6 or the Appendix. No energy functional, Lagrangian, or action integral is derived. This claim should either be removed or substantiated.

**W7 — Major: Guarantee is local, but claims imply global/universal stabilization (Pages 1, 5, 8).** Theorem 3 proves *local* asymptotic stability (initial condition near equilibrium). The Introduction states the method "asymptotically stabilize gradient descent regardless of the curvature," which omits the local qualification. The Conclusion states the method "guarantees local asymptotic stability under general curvature settings," which is accurate, but the Abstract and contribution list use unqualified language.

**W8 — Major: Introduction claims "functional derivative" usage, which is incorrect (Page 2).** Section 3 derives the second-order ODE by taking a simple time derivative of the gradient flow equation — this is ordinary calculus, not functional differentiation. This technical inaccuracy may confuse mathematically sophisticated readers.

**W9 — Moderate: Section 4.2.2's algebraic multiplicity argument relies on a characteristic polynomial derived under the assumption $\lambda_i > 0$ (Page 4).** The characteristic polynomial $\prod_{i=1}^n \lambda(\lambda + \lambda_i)$ on line 63 is derived with the qualification "where $\lambda_i > 0$ are the eigenvalues of $H$." When analyzing the semidefinite case ($\lambda_i \geq 0$), this expression still holds but the derivation should be re-checked explicitly for zero eigenvalues, where factors become $\lambda(\lambda+0) = \lambda^2$, giving additional zero roots.

**W10 — Moderate: Related Work does not discuss momentum/adaptive methods (Page 2).** The paper claims "no existing method stabilizes GD for general curvature" but does not mention Polyak heavy-ball, Nesterov acceleration, or Adam — all of which modify GD dynamics. A brief discussion of why these methods do not solve the stability problem would strengthen the motivation.

**W11 — Minor: Abstract mentions "low-dimensional toy examples" but fails to mention that these are the *only* experiments.** A reader may expect at least one real-world benchmark from the Abstract's framing.

**W12 — Minor: Missing $C^2$ smoothness assumption for second-order ODE derivation (Page 3, Section 3).** The gradient flow definition assumes $C^1$, but taking the second derivative requires $C^2$. This should be stated explicitly.

## Score
**Final Score: 4/10**

**Scoring rationale:** The score is based on the following judgment, prioritizing research value and novelty as primary dimensions:

- **Novelty (fair):** The continuous-time second-order ODE formulation of GD stability and the control-theoretic modification are genuinely novel conceptual contributions. However, the novelty is substantially reduced by (a) the erroneous integration bridge (Eq. 5) that invalidates the claimed connection to the discrete algorithm, and (b) the paper not engaging with existing momentum methods that already modify GD dynamics.

- **Research value (moderate):** The core idea — using eigenvalue shifting via a PD controller to stabilize GD dynamics — is interesting and could inspire future work. However, the value is limited by the purely continuous-time analysis with no demonstrated improvement over practical methods, no neural network validation, and no guidance for hyperparameter selection in realistic settings.

- **Validity/soundness (major concerns):** The critical error in Equation (5) means the paper's central claim — that Algorithm 1 implements the controlled dynamics — is not justified. The misclassification of the sphere example further undermines confidence in the experimental validation. The theoretical analysis (Sections 2-5) is mathematically coherent for the continuous-time setting, but the gap to discrete algorithms is not credibly bridged.

- **Reproducibility (partial):** The synthetic experiments are reproducible from the description, but the lack of code, random seeds, variance reporting, and neural network benchmarks limits reproducibility of the broader claims.

- **Presentation (fair):** The paper is generally well-structured, but contains technical inaccuracies ("functional derivative," Theorem 2 typo), unsubstantiated claims ("variational interpretation"), and a mismatch between the Abstract's promises and the paper's deliverables.

The paper has a promising core idea and a clean theoretical framing, but the critical flaw in transitioning from continuous dynamics to a discrete algorithm (Eq. 5), combined with the absence of neural network validation and several factual errors, prevents it from being acceptable at a top-tier venue in its current form. A major revision is required, focusing on (a) fixing or replacing the erroneous derivation in Eq. (5), (b) adding meaningful empirical validation, and (c) calibrating the claims to what is actually proven and demonstrated.

**Post-Revision Target:** 6/10 — achievable if the core derivation is corrected, neural network experiments are added, and claims are appropriately bounded.