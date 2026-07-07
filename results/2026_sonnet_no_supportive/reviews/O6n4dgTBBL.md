Now I have enough to write the draft review. Let me compose it and then calibrate.**Round 1 bracket**: Based on the topical anchors, the paper sits in the **1–3 range**. Both fatal flaws are unambiguously verifiable from the text as written. The NbbsRnPBoS anchor (score 2.33) rejected a paper with correct but narrow results; the paper under review has *incorrect* mathematics at two critical junctures plus mislabeled experiments — placing it below that anchor, closer to 1–2.

**Round 2 narrowing**: No round 2 needed; the fatal flaws are verifiable and the bracket is already tight.

---

## Summary
The paper proposes "Controlled Gradient Descent" (CGD), which reformulates gradient flow as a second-order ODE, lifts it to a 2n-dimensional first-order state space, proves (Theorem 3) that a controller u = -K₁θ - K₂(dθ/dt) renders the *augmented* system locally asymptotically stable, and then derives a gradient-update algorithm by integrating the second-order controller term. Experiments on three 2D synthetic functions show improved convergence over standard GD.

## Strengths
- The reduction to a quadratic eigenvalue problem (Lemma 4, Tisseur & Meerbergen 2001) is a clean and legitimate use of existing theory, and Theorem 3's proof is internally valid within the 2n-dimensional augmented system.
- The three-case curvature breakdown (strongly convex / convex-not-strongly-convex / concave) in Section 4 is clearly organized, and the characteristic polynomial derivation det(λ²I + λH) = ∏λ(λ+λᵢ) is correct.

## Weaknesses

### Fatal

- **The second-order reformulation introduces spurious zero eigenvalues, causing the paper to mischaracterize GD's actual stability.** The paper lifts the first-order gradient flow (Eq. 1) to the 2n-dimensional system (Eq. 3) and then presents the stability of Eq. 3 as "the stability of gradient descent." However, the original first-order gradient flow's Jacobian at a minimum under strong convexity is −H(θ*), whose eigenvalues are all strictly negative — making the actual gradient flow *locally asymptotically stable* (not merely Lyapunov stable, as claimed in Table 1). The n zero eigenvalues found in Section 4.2.1 arise solely from the auxiliary velocity direction in the 2n-dimensional embedding: the paper's own computation shows "the nullspace has dimension n … geometric multiplicity of the zero eigenvalue is n." These zeros are an artifact of the second-order lift. Consequently, the "gap" between Lyapunov and asymptotic stability that motivates the entire controller does not exist in the actual gradient flow; it is an artifact of the chosen representation. The stability claims in Table 1, Section 4.2.2 ("unstable" for convex-not-strongly-convex), and all of Theorem 2 describe the augmented system — not GD itself.

- **Equation 5 contains a calculus error that severs the connection between Theorem 3 and Algorithm 1.** The paper integrates the controller back to a gradient update: ∫(−K₁θ)dt is claimed to equal −½K₁θ². This is wrong. Because θ = θ(t) is a time-varying function, ∫K₁θ(t)dt ≠ ½K₁θ²(t); the latter holds only if θ is the variable of integration. As a consequence, the algorithm in Algorithm 1 (g_t = ∇L(θ_t) − K₁θ_t² − K₂θ_t) is not derived from the theoretical controller in Definition 4, and Theorem 3 provides no guarantee about the behavior of Algorithm 1.

### Major

- **Algorithm 1 implicitly introduces L2 regularization without acknowledgment.** The −K₂θ_t term added to the gradient corresponds to the gradient of ½‖K₂^(1/2)θ‖², i.e., standard L2 weight decay. CGD therefore minimizes a *different* objective than L(θ) and converges to a different parameter value. The empirically observed improvements in Figure 2–3 may wholly or partly reflect this regularization effect rather than any dynamic stabilization. The paper does not acknowledge this, analyze it, or compare final solution quality.

- **All experiments are on 2D synthetic functions; no neural network results are provided.** The abstract, Introduction, and Algorithm 1 explicitly frame CGD for "neural network training," but Section 7 reports only results on L(θ) = 2θ₁²+0.5θ₂², θ₁²+θ₂², and θ₁⁴+θ₂⁴. There are no comparisons against Adam, SGD with momentum, or SAM, and no tests on any neural network.

### Minor

- **The "convex but not strongly convex" experiment in Section 7.1 uses L(θ) = θ₁²+θ₂², which is strongly convex.** This function has Hessian 2I ≻ 0, so it does not illustrate the theoretical setting it is labeled as. The label "Convex but not strongly convex sphere" is incorrect.

- **The K₁θ_t² term in Algorithm 1 (element-wise square, as defined in Eq. 5) is the gradient of ⅓Σᵢθᵢ³, not of any standard regularizer.** Its geometric or regularization meaning is left unexplained.

### Trivial
- None beyond the above.

## Nice-to-Haves
- A first-order formulation of the controller — modifying dθ/dt = −∇L(θ) + u(θ) directly — would eliminate the spurious eigenvalue problem and yield a valid theory-to-algorithm derivation. The Hessian-shifting mechanism remains potentially interesting in that setting.
- Even a small-scale neural network experiment (MLP on MNIST, logistic regression) would better support the stated scope.
- A clear statement that CGD adds implicit L2 regularization, with an analysis separating regularization benefits from stabilization benefits.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Strength: "contributes to understanding of gradient descent dynamics for general non-convex loss"** — removed because the core stability analysis is performed on the wrong (augmented) system and the claimed contribution does not hold for the actual gradient flow.
- **Strength: "Algorithm 1 is a principled control-theoretic optimizer"** — removed because the derivation of Algorithm 1 from Theorem 3 is broken by the integration error in Eq. 5.
- **Reviewer suggestion that Section 4.2.2's Jordan block argument about GD being "unstable" is wrong** — kept as a consequence of the spurious-eigenvalue fatal flaw, not separately listed.

## Novel Insights
The reduction of gradient descent stability to a quadratic eigenvalue problem (QEP) structure (Lemma 4) is a genuinely interesting connection; certifying negative real parts of eigenvalues via Tisseur & Meerbergen's conditions is non-trivial. However, this insight is built on a flawed foundation (the 2n-dimensional augmented system). Were the paper reformulated in the first-order setting — designing u(θ) such that dθ/dt = −∇L(θ) + u(θ) is asymptotically stable — the QEP approach could yield legitimate and novel guarantees.

## Suggestions
1. Reformulate entirely in the first-order ODE framework: treat u(θ) as a modification to the right-hand side of dθ/dt = −∇L(θ), analyze the Jacobian of the resulting system at equilibrium, and derive the algorithm directly from u(θ). This avoids the spurious zero eigenvalue problem.
2. If the second-order framing is retained, do not claim it characterizes the stability of the original gradient flow — be explicit that it analyzes the lifted system, which is a strictly different dynamical object.
3. Correct or remove Eq. 5; the algorithm should be stated directly without claiming it follows from integration of the controller.
4. Acknowledge and analyze the L2 regularization implicit in the −K₂θ term; compare CGD to GD+L2 to isolate the stabilization effect.
5. Add neural network experiments to match the paper's stated scope.

## Score and Decision

### Anchor Papers Retrieved

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| NbbsRnPBoS.md | 2.33 | R1 | GD convergence paper with correct but narrow/uninteresting results — paper under review has both narrower scope *and* mathematical errors, placing it below this anchor |
| 1NYhrZynvC.md | 2.50 | R1 | Adaptive stepsize paper, mostly correct but questioned on novelty — paper under review has fundamental soundness failures, placing it below |
| xpmDc76RN2.md | 2.33 | R1 | Operator network optimization paper rejected for insufficient novelty; paper under review has two fatal mathematical errors |
| 2NwHLAffZZ.md | 2.33 | R1 | Linearization of gradient-based learning, rejected on novelty grounds; paper under review additionally has math errors |
| OZZYqfplS3.md | 4.00 | R1 | Stability/convergence paper with correct proofs and experiments; far above paper under review |
| UMOlFJzLfL.md | 5.75 | R1 | Rigorous SGD stability analysis; paper under review not comparable |
| bI3fcTsKW4.md | 6.25 | R1 | Hessian-informed optimizer with real experiments; clearly above paper under review |
| J4Dvxv7WnG.md | 7.00 | R1 | Edge-of-stability analysis in deep matrix factorization; well above |
| sbG8qhMjkZ.md | 8.00 | R1 | Strong SVGD convergence paper; well above |

**Round 1 bracket**: 1–2.5.

The two fatal flaws — (1) the augmented-system stability does not characterize actual GD stability, and (2) the integration error in Eq. 5 severs the theory-to-algorithm connection — are both unambiguously verifiable from the paper as written. They invalidate the paper's two main contributions: the theoretical characterization of GD stability and the claimed derivation of CGD. The experiments are limited to mislabeled 2D synthetic cases with no neural networks. Compared to rejected papers at 2.33 that at least had correct mathematics, this paper's compounded mathematical errors place it at approximately **1.5**.

MY FINAL SCORE: <score>1.5</score>
MY FINAL DECISION: <decision>Reject</decision>