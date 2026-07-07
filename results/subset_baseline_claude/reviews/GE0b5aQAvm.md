## Summary
The paper argues that neural network (nonlinear) policy ensembles are provably sub-optimal compared to linear policy ensembles. It provides three theorems (suboptimality, stability violation, mixing suboptimality) and validates these claims experimentally on linear dynamical systems and simple nonlinear systems. The central claim is that the nonlinearity of neural policies breaks the ensemble-averaging properties that work for linear controllers, and that this has implications for RL and MoE architectures.

---

## Strengths

- **Clean identification of the convexity argument:** The key insight—that a weighted average of linear policies is itself a valid linear policy (closed under convex combination), while weighted averages of nonlinear policies are not—is mathematically correct and cleanly expressed in Definitions 6–8.
- **Theorem 3 / Corollary 1 is the strongest contribution:** For LQR systems, Theorem 3 and Corollary 1 cleanly establish that convex mixing weights equal the cost weights $\lambda$ at the optimum. This is a principled, closed-form result.
- **Broad empirical coverage within scope:** The paper tests multiple switching patterns, diversity levels, and both linear and simple nonlinear systems, providing a reasonably thorough experimental validation within the LQR/near-LQR domain.

---

## Weaknesses

### Fatal

**The entire theoretical and empirical framework presupposes that the optimal policy is linear (LQR setting), making the conclusions largely tautological.**

Theorem 1 compares a neural ensemble $\Pi^N$ against a linear ensemble constructed from "corresponding optimal linear policies $\{K_i^* x\}$." For a linear system with quadratic cost, these optimal linear policies are *exactly* the LQR solution. The paper then shows that a neural network approximating each $K_i^*$ is worse than using $K_i^*$ exactly. This is essentially saying "approximating the exact solution with a neural network introduces error"—a statement that is true by definition, not a structural limitation of neural ensembles. The suboptimality gap $\epsilon(\kappa_0, \delta, L_f)$ in Theorem 1 is driven by the nonlinearity measure $\kappa(\pi^{\theta_i}, D) > 0$, which is just a measure of how far the neural network is from its linear target. If the neural network perfectly approximated the LQR (achievable in principle), $\kappa \to 0$ and the gap vanishes—so the result does not show a structural impossibility for neural ensembles, only a deviation from the known-linear-optimal.

**The paper does not analyze the setting where neural policy ensembles are actually used or have an advantage.** Neural policy ensembles appear in RL precisely when: (a) the optimal policy is not known to be linear, (b) the system is highly nonlinear, and (c) policies must be learned from data. In such settings, there may be no linear policy that competes with a trained neural policy, let alone an exactly solvable LQR. The paper's framework is entirely silent on whether neural ensembles are sub-optimal to *individual neural policies* or to *the best achievable controller* in genuinely nonlinear problems. The "2 orders of magnitude" headline claim is measured against an exact LQR oracle—not a fair neural single-policy baseline.

### Major

**Theorem 2's stability result applies equally to time-varying linear ensembles, but the paper does not acknowledge this.**

The instability condition requires $\|\dot{w}(t)\| \geq \beta > 0$ (time-varying ensemble weights). In switched systems theory, switching between stable linear controllers can also produce an unstable system (Liberzon, 2003)—this is a classical result. The paper's claim that "linear policy ensembles are stable" tacitly relies on weights being *fixed*, in which case the ensemble collapses to a single linear controller $K_\text{ens}$, and stability is trivially guaranteed by LQR. With time-varying weights, the comparison is not fair: a time-varying linear ensemble faces the same switched-system instability risks. The paper does not compare neural ensembles to *time-varying* linear ensembles under equivalent switching conditions.

**Figure 5 contains an internal inconsistency.** Table (a) shows Mean Episode Cost ≈ 0 for both Oracle and Linear Convex Mixing on Linear\_Systems and Mid\_Nonlinear\_Oscillator, while Table (c) shows 166.1% and 138.3% relative performance loss for those same systems. A 166% loss relative to a baseline cost of ~0 is undefined/uninformative and contradicts the visual in (a). This undermines the empirical credibility of the policy mixing section.

### Minor

- Condition 3 of Theorem 1 ($L_f \kappa_0 \delta > \rho$) depends on $L_f$, the Lipschitz constant of the *system dynamics*. In the LQR setting, $L_f = \|A\|$. The paper does not discuss whether this condition is generically satisfied or requires adversarial choices of problem parameters.
- The neural ensemble in experiments is trained to minimize cumulative cost, but the paper does not report whether the trained neural policy (as a single policy, not ensemble) achieves performance close to the LQR. Without this, it is impossible to distinguish "neural ensemble is bad" from "neural training is bad in this setting."
- Theorem 2 requires $\|V_i\|_\infty < \infty$ implicitly (the condition $\beta > \frac{\min_i \alpha_i}{2 \max_i \|V_i\|_\infty}$), but for global Lyapunov functions on unbounded domains the sup-norm is infinite, making the condition vacuous. The domain restriction is not stated.

### Trivial

- The abstract claims "2 orders of magnitude" underperformance, but Figure 1 shows approximately a 2× gap (432 vs 234), which is less than one order of magnitude.

---

## Nice-to-Haves

- Include a single-neural-policy baseline (no ensemble) in all figures to establish whether the neural ensemble underperforms a single neural network, not just the LQR oracle.
- Test on a control problem where linear policies are genuinely suboptimal (e.g., a nonlinear system without valid linearization) to assess whether the conclusion changes in neural policies' natural habitat.
- Clarify the stability theorem's domain assumptions and compare against time-varying linear ensembles.

---

## Novel Insights

The paper cleanly formalizes why linear policy ensembles are closed under convex combination (Theorem 3 / Corollary 1), making them structurally superior to neural ensembles in the LQR setting—a result that is well-grounded. However, the key limitation is that this insight is largely a restatement of "LQR is optimal for linear-quadratic problems and neural networks introduce approximation error," rather than a discovery about the structural limitations of neural ensembles in settings where they are actually employed. The observation that nonlinearity of individual policies propagates adversely through ensemble averaging is insightful but remains unvalidated outside the LQR regime.

---

## Suggestions

- Provide experiments where no closed-form linear optimal policy exists (e.g., a truly nonlinear system without LQR applicability) and compare neural ensemble vs. single best neural policy. This would directly address whether the sub-optimality is structural or just an artifact of the LQR comparison.
- Prove or disprove the stability claim for time-varying *linear* ensembles under identical switching conditions as the neural case, to isolate the effect of nonlinearity from the effect of weight switching.
- Reconcile Figure 5 tables (a) and (c): clarify how a baseline cost of ~0 yields a 166% relative loss.

---

## Score and Decision

The paper addresses a conceptually interesting question but the theoretical framework is essentially restricted to the LQR setting, where the conclusions are largely expected (neural approximations of linear optima are worse than the exact linear optima). The most important potential use cases for neural ensembles—genuinely nonlinear, high-dimensional systems—are not addressed. Theorem 2's stability result does not properly account for the instability of switched linear systems. The empirical validation, while systematic, compares neural approximations against exact closed-form solutions, making the gap unsurprising. The headline claims overreach the actual demonstrated scope. The contribution is not sufficient for acceptance in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>