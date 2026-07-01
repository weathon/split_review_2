My verification confirms all the key claims. Let me now produce the final review.

## Summary

This paper proposes "Controlled Gradient Descent" (CGD), which adds control-theoretic correction terms to the gradient update. The authors analyze gradient flow through a second-order ODE reformulation, propose a controller to stabilize the continuous-time dynamics, and attempt to translate this into a discrete update rule that adds $-\frac{1}{2}K_1\theta^2 - K_2\theta$ to the gradient. Experiments are conducted on three 2D synthetic optimization problems.

## Strengths

- **Control-theoretic framing of optimization dynamics.** Analyzing gradient flow through a second-order ODE lens and leveraging quadratic eigenvalue problems (Lemma 4, Tisseur & Meerbergen) to establish stability conditions is a conceptually novel angle. The use of full-state feedback for eigenvalue regulation is an interesting idea for the continuous-time setting.

- **The Jacobian analysis at equilibrium (Section 4.2) is mathematically careful.** The block structure computation, the characteristic polynomial $\det(\lambda^2 I + \lambda H)$, and the analysis of Jordan block sizes for the zero eigenvalue in the convex-but-not-strongly-convex case are correctly argued within the paper's chosen framework.

## Weaknesses

### Fatal

- **Mathematical error in Equation 5 breaks the connection between the continuous theory and the discrete algorithm.** The derivation attempts to recover the first-order update by integrating the controlled second-order ODE: $\frac{d\theta'}{dt} = \int \frac{d^2\theta'}{dt^2} dt = \int \frac{d^2\theta}{dt^2} dt + \int \mathbf{u}\, dt$. With $\mathbf{u} = -K_1\theta - K_2\frac{d\theta}{dt}$, the term $\int\mathbf{u}\,dt = -K_1\int\theta(t)\,dt - K_2\int\frac{d\theta}{dt}dt$. While $\int\frac{d\theta}{dt}dt = \theta + C$ is correct, the paper evaluates $\int\theta(t)\,dt$ as $\frac{1}{2}\theta^2$. This is the antiderivative of $\theta$ with respect to $\theta$, not with respect to time $t$: the identity $\int\theta\,d\theta = \frac{1}{2}\theta^2$ does **not** apply to $\int\theta(t)\,dt$ unless $\frac{d\theta}{dt}=1$, which does not hold during optimization. This is not a typo or formatting artifact — it is the sole step that translates the continuous controller into Algorithm 1. Without a correct derivation, the discrete update rule ($g_t = \nabla L(\theta_t) - K_1\theta_t^2 - K_2\theta_t$) is not theoretically grounded in the stability analysis of Sections 4–5. The algorithm may or may not work, but the paper does not provide a valid theoretical basis for it.

### Major

- **Insufficient experimental validation for the claims made.** The paper evaluates CGD exclusively on three 2D synthetic objectives ($2\theta_1^2+0.5\theta_2^2$, $\theta_1^2+\theta_2^2$, $\theta_1^4+\theta_2^4$). There are: (i) no experiments on any neural network, despite Algorithm 1 being titled "Controlled Gradient Descent for Neural Network Training"; (ii) no comparisons with standard optimizers beyond vanilla GD (no SGD with momentum, Adam, etc.); (iii) no demonstration of scaling beyond $d=2$; (iv) no analysis of computational overhead. The abstract and conclusion make broad claims about "stabilizing optimization across diverse curvature structures" and "improving tolerance to larger learning rates," but the evidence is far too narrow to support these claims.

- **Mismatch between the continuous controller and the discrete algorithm.** The continuous controller is $\mathbf{u} = -K_1\theta - K_2\frac{d\theta}{dt}$ (Definition 4), which is linear in $\theta$ and $\dot\theta$. Theorem 3 guarantees asymptotic stability of the linearized ODE system with Jacobian $J = \begin{bmatrix}0 & I \\ -K_1 & -(H+K_2)\end{bmatrix}$, where $K_1$ multiplies $\theta$ linearly. However, Algorithm 1 introduces a quadratic term $-\frac{1}{2}K_1\theta_t^2$ (element-wise square) that has no counterpart in the continuous analysis. The stability analysis in Section 5 does not apply to this quadratic modification, and the paper provides no analysis of how the $\theta^2$ term affects stability in the discrete setting. Even setting aside the integration error in Equation 5, the discrete algorithm does not match the continuous system that was analyzed.

### Minor

- **Factual error in classifying the "convex sphere" loss.** Section 7.1 labels $L(\theta) = \theta_1^2 + \theta_2^2$ as "convex but not strongly convex." However, its Hessian is $2I$, which is positive definite with minimum eigenvalue 2, making it **strongly convex** by the paper's own definition (Lemma 1: $H \succeq mI$ with $m>0$). This misclassification undermines the paper's claim of testing across distinct curvature regimes.

- **Theorem 2 contains a non-standard classification.** The third bullet states the system is "unstable if the loss function $L$ is convex but not strongly concave" (line 124). This is not a standard curvature classification, and Section 4.2.3 analyzes the concave case. The phrasing appears to be a misstatement for "concave."

- **Table 1 conflates the second-order reformulation with the original gradient flow.** The table claims GD is only Lyapunov stable (not asymptotically stable) even for strongly convex losses. However, the original first-order gradient flow $\frac{d\theta}{dt} = -\nabla L(\theta)$ at a strongly convex minimum has Jacobian $-H(\theta^*)$ with all eigenvalues strictly negative, making the equilibrium asymptotically stable. The paper's weaker stability result follows from the second-order reformulation, which introduces $n$ zero eigenvalues as an artifact of the derivation. The paper does not acknowledge this distinction and presents the table as a comparison of "Original Gradient Descent."

### Trivial

None.

## Nice-to-Haves

- **Quantify the learning rate tolerance.** The paper claims CGD "tolerates larger learning rates" but does not systematically measure the maximum stable $\eta$ as a function of $K_1, K_2$.
- **Analyze the $\theta^2$ regularization effect.** The element-wise quadratic penalty is unusual; its connection to known techniques (L2 regularization, weight decay) is not discussed.
- **Explore independent settings of $K_1$ and $K_2$.** The ablation varies $k_1=k_2$ jointly but does not explore $K_1 \neq K_2$ or different relative magnitudes.

## Removed Points

These points were considered but removed after verification against the paper:

- *"The second-order ODE is a mathematical identity, not a controllable dynamical system"* — Removed. Adding a control term to a derived ODE is a legitimate control-theoretic framing for proposing a modified optimization algorithm. The real issue is the erroneous integration step (Fatal weakness), not the act of constructing a controlled system from a derived relationship.
- *"Abstract overclaims the unsolved nature of GD instability"* — Removed. Subjective assessment about scope; the evidential gap is covered under the Major weakness on experiments.
- *"No analysis of the $K_1\theta^2$ term"* — Moved to Nice-to-Haves; it is a reasonable suggestion but not a flaw in the paper's core argument.
- *"No analysis of hyperparameter sensitivity"* — Moved to Nice-to-Haves; the paper does provide some ablation.
- *"No discussion of computational cost"* — Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The key observation from the review — that the integration in Equation 5 is mathematically invalid — is the single most important point.

## Suggestions

1. **Either correct the derivation or abandon the continuity claim.** If the continuous framework is to justify the algorithm, the integration step in Equation 5 must be fixed — or replaced by a proper discretization of the controlled ODE that preserves the stability guarantees. Alternatively, present CGD as an independently motivated regularizer and drop the claim that it is derived from the control-theoretic analysis.
2. **Add experiments on actual neural networks.** Even a minimal setup (two-layer MLP on MNIST) comparing CGD to GD, SGD with momentum, and Adam would substantially strengthen the empirical case.
3. **Correct the misclassification of $L(\theta) = \theta_1^2 + \theta_2^2$** as "convex but not strongly convex" throughout Section 7.1 and Figure 2.
4. **Acknowledge the framing gap** between the second-order reformulation and the original first-order gradient flow, particularly regarding Table 1.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>