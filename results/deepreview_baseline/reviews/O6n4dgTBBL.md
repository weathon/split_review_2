## Summary
The paper attempts to connect the stability of gradient descent (GD) to the curvature of the loss landscape using a continuous-time, second-order dynamical system perspective. It analyzes the local stability of the second-order ODE derived from gradient flow under various curvature assumptions, designs a controller that guarantees asymptotic stability, and proposes a discrete algorithm (Controlled Gradient Descent, CGD) by integrating the controller back into the gradient update. Synthetic experiments on low-dimensional convex objectives are provided to illustrate the method.

## Strengths
- The paper identifies an interesting connection between stability of optimization dynamics and the eigenstructure of the Hessian, and it attempts to bring control-theoretic tools to the analysis of GD.
- The mathematical derivation of the eigenvalues of the Jacobian for the second-order reformulation at equilibrium is clearly presented and technically correct within that narrow setting.
- The synthetic experiments do show that the proposed CGD can outperform standard GD on the simple test problems studied.

## Weaknesses
### Fatal
- **Derivation of the discrete update from the controller is mathematically invalid.**  
  The paper integrates the controller term \(\mathbf{u} = -K_1\boldsymbol{\theta} - K_2\frac{d\boldsymbol{\theta}}{dt}\) with respect to time to obtain a modification of \(\frac{d\boldsymbol{\theta}}{dt}\). The claimed result \(\frac{d\boldsymbol{\theta}'}{dt} = \frac{d\boldsymbol{\theta}}{dt} - \frac{1}{2}K_1\boldsymbol{\theta}^2 - K_2\boldsymbol{\theta}\) (Equation 5) treats \(\int \boldsymbol{\theta}\,dt\) as \(\frac{1}{2}\boldsymbol{\theta}^2\), which is incorrect (the integral of a vector function over time is not the elementwise square of the function). This error invalidates the core algorithmic contribution and the entire transition from continuous control back to discrete gradient updates.
- **The dynamical system analyzed is not standard gradient descent.**  
  The paper studies the second-order ODE \(\frac{d^2\boldsymbol{\theta}}{dt^2} = -H(\boldsymbol{\theta})\frac{d\boldsymbol{\theta}}{dt}\) derived from gradient flow. However, gradient flow is a first-order system with state \(\boldsymbol{\theta}\) only. The second-order reformulation introduces an auxiliary variable \(\mathbf{x} = \frac{d\boldsymbol{\theta}}{dt}\) and analyzes the stability of the pair \((\boldsymbol{\theta}, \mathbf{x})\). This is a different dynamical system from original GD / gradient flow; its stability properties do not directly translate to the stability of discrete GD iterations. The paper does not justify why controlling this second-order system is relevant for the actual algorithm practitioners use.
- **The continuous-time stability results do not address discrete GD.**  
  The paper acknowledges a gap between continuous and discrete dynamics in the conclusion but never bridges it. Theorems 2 and 3 concern a continuous second-order ODE, yet Algorithm 1 is claimed to inherit asymptotic stability. No discrete-time stability analysis is provided, and the experimental validation is limited to synthetic problems. This disconnect undermines the main claims of the paper.

### Major
- **Insufficient experimental validation.**  
  Experiments are restricted to three low-dimensional quadratic or quartic functions. No experiments on neural networks, real datasets, or any non-convex deep learning benchmarks are presented. A method paper that proposes a new optimizer should demonstrate its effectiveness on realistic tasks (e.g., image classification, language modeling) with standard architectures.
- **Unsupported claim about GD instability under bounded learning rates.**  
  The paper claims that GD can diverge even when \(\eta < 2/\lambda\) in convex settings, citing Figure 1. However, Figure 1 shows GD eventually converging (oscillating but reaching the optimum) for the strongly convex ellipse with \(\eta = 0.5\) (which equals \(2/\lambda\) and thus is at the threshold, not below). The claim is not demonstrated by the provided evidence.
- **Lack of theoretical connection to the Edge of Stability (EoS) literature.**  
  The paper mentions EoS but does not provide any analysis or comparison of how its controller relates to the well-studied EoS phenomenon. The statement that CGD increases the \(2/\text{sharpness}\) threshold is not theoretically derived in the discrete setting.

### Minor
- The integration from the controller to the gradient modification is presented without justification of the integration constant or the indefinite integral interpretation.
- The algorithm uses \(\boldsymbol{\theta}^2\) (element-wise square), which is unusual and not motivated by the controller that depends linearly on \(\boldsymbol{\theta}\).
- The paper sometimes uses notation inconsistently (e.g., \(\lambda\) for both eigenvalues of the Hessian and the eigenvalue of the Jacobian).

### Trivial
- There are minor points about figure numbering and caption formatting, but these are not consequential.

## Nice-to-Haves
- A discrete-time stability analysis (e.g., spectral radius of the update matrix for quadratic objectives) would strengthen the paper substantially.
- Experiments on standard deep learning benchmarks (CIFAR, ImageNet with a small CNN/ResNet) would help validate the practical utility of CGD.
- A connection to existing stabilisation techniques (e.g., Polyak heavy ball, Nesterov acceleration, or gradient clipping) could contextualise the contributions.

## Novel Insights
None beyond the paper’s own contributions. The insight that a proportional-derivative controller of the form \(-K_1\boldsymbol{\theta} - K_2\dot{\boldsymbol{\theta}}\) can asymptotically stabilize the second-order ODE of gradient flow is a straightforward control-design exercise and not novel in the control literature. The claimed novelty lies in applying it to optimization, but the flawed derivation and lack of discrete analysis prevent any genuine insight from emerging.

## Suggestions
- Re-evaluate the derivation from continuous control to discrete gradient update; a proper discretisation would involve interpreting the controlled second-order ODE as a damped mass-spring system and then applying a numerical integrator (e.g., Verlet or Runge-Kutta) rather than the ad hoc integration used.
- Provide a discrete-time Lyapunov analysis or eigenvalue spectrum analysis for the proposed update to show stability in the discrete regime.
- Conduct experiments on neural network training at least on a problem like logistic regression on MNIST or a small two-layer network to move beyond synthetic, convex examples.

## Score and Decision
The paper contains a fatal flaw that invalidates the core algorithmic derivation and a major disconnect between the analyzed dynamics and the actual algorithm. The experimental validation is insufficient to support the method’s claims. Therefore, the paper should be strongly rejected.

MY FINAL SCORE: 1.0<score>
MY FINAL DECISION: Reject<decision>