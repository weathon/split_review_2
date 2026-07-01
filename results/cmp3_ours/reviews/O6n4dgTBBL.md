Now let me write the final, complete review.

## Summary

This paper proposes a control-theoretic framework for analyzing gradient descent (GD) stability. It reformulates GD as a second-order ODE, analyzes stability under different curvature regimes (strongly convex, convex-but-not-strongly, concave), and introduces a controller that provably stabilizes the continuous-time dynamics. The paper then attempts to map this continuous controller to a discrete algorithm (Controlled Gradient Descent, CGD) and validates it on 2D synthetic objectives.

## Strengths

1. **The control-theoretic framing is genuinely novel.** Treating GD as a second-order ODE and applying quadratic eigenvalue problem results (Lemma 4 from Tisseur & Meerbergen) to prove asymptotic stability of the continuous controlled system is a creative conceptual bridge between control theory and optimization that I have not seen before in this context.

2. **The continuous-time stability analysis (Theorems 2 and 3) is technically coherent on its own terms.** The eigenvalue analysis of the Jacobian block matrix at equilibrium, the handling of Jordan block sizes for the zero eigenvalue, and the application of Lyapunov's linearization method are executed without algebraic mistakes for the strongly convex and concave cases.

## Weaknesses

### Fatal

1. **The derivation linking the continuous controller to the discrete algorithm (Algorithm 1) contains a fundamental mathematical error that invalidates the paper's central claimed contribution.** Equation (5) states:

   $$\frac{d\theta'}{dt} = \int \frac{d^2\theta'}{dt^2} dt = \int \frac{d^2\theta}{dt^2} dt + \int u dt = \frac{d\theta}{dt} - \frac{1}{2}K_1\theta^2 - K_2\theta$$

   where $u = -K_1\theta - K_2\frac{d\theta}{dt}$. The term $\int K_1\theta(t) dt$ is evaluated as $\frac{1}{2}K_1\theta(t)^2$ (element-wise square). This is mathematically incorrect: $\frac{d}{dt}(\frac{1}{2}\theta^2) = \theta \cdot \frac{d\theta}{dt} \neq \theta$ in general. The integral $\int \theta(t) dt$ cannot be evaluated without knowing the function $\theta(t)$. Consequently, **Algorithm 1 does not implement the controller whose stability is proven in Theorem 3.** The paper's core claim — that it has "stabilized gradient descent" via this controller — rests on an unjustified algebraic step. This is not the continuous/discrete discretization gap that the limitations section acknowledges; it is an error in the derivation itself. Without a correct derivation, the theoretical results (which analyze a different mathematical object) do not support the proposed algorithm.

### Major

2. **A key experimental example is factually mislabeled.** The loss $L(\boldsymbol{\theta}) = \theta_1^2 + \theta_2^2$ is labeled "convex but not strongly convex sphere training loss" in Figure 2's caption (Section 7.1, line 269). Its Hessian is $\nabla^2 L = 2I$, which is positive definite with minimum eigenvalue 2; by Lemma 1 of the paper itself, this is **strongly convex**. The paper claims CGD stabilizes the "convex but not strongly convex" case, but the example does not actually instantiate that regime. (The inconsistency is compounded by Section 7.2's Figure 3 caption, which correctly labels the same function "strongly convex training loss.") This error undermines the connection between the experiments and Theorem 2's analysis of the non-strongly-convex regime.

3. **The experimental validation is far too narrow to support the paper's broad claims.** The entire empirical evaluation consists of three 2D synthetic objectives with scalar multiples of the identity for $K_1, K_2$. There are no experiments on higher-dimensional problems, no comparisons with any established optimization method beyond vanilla GD (not even SGD with momentum or Adam, which are standard baselines for any optimization paper), no stochastic gradient experiments, and no evaluations beyond quadratic and quartic toy cases. The paper claims CGD "stabilizes gradient descent" and demonstrates "higher tolerance on learning rate" — claims with broad practical implications — yet the evidence is limited to three carefully chosen 2D functions. Even a small-scale neural network experiment (e.g., an MLP on MNIST) would substantially strengthen the empirical case.

### Minor

4. **The continuous/discrete gap is acknowledged but systematically under-addressed.** The paper proves Theorem 3 about the continuous ODE but consistently frames the contribution in terms of the discrete GD algorithm (title, abstract, introduction, contribution list). The "higher tolerance on learning rate" claim (contribution 3) is an empirical observation from the discrete algorithm with no theoretical backing from the paper's own analysis — there is no theorem bounding the allowable learning rate for the discrete CGD update. While the limitations section mentions this gap, the structural disconnect between what is proven (continuous ODE stability) and what is claimed (discrete GD stabilization) warrants more substantive treatment than a single paragraph.

5. **No analysis of the $\theta^2$ term's effect on optimization behavior.** The $K_1\theta^2$ term (element-wise square) in the gradient is unusual. It is always non-negative and grows quadratically with parameter magnitude, which could have unintended consequences far from the optimum (e.g., dominating the gradient signal, creating spurious sign biases). The paper does not analyze how this term affects dynamics away from equilibrium or whether it could introduce artifacts.

6. **No practical guidance for selecting $K_1$ and $K_2$.** Remark 2 states $K_2$ should satisfy $K_2 \succ -H(\theta)$ for all $\theta$, but in any realistic setting the Hessian is not computable or trackable. The ablation (varying $k_1 = k_2$ jointly across three values on 2D problems) does not constitute meaningful sensitivity analysis — $K_1$ and $K_2$ are never varied independently, and no guidance is given for choosing them in practice.

## Nice-to-Haves

- Comparing CGD with standard optimizers (SGD with momentum, Adam) on the same toy problems would help contextualize the method's empirical behavior.
- If the derivation error is fixable, a discrete-time control analysis or a proper numerical integration scheme that provably inherits the continuous stability properties would substantially strengthen the theory-to-algorithm connection.
- Adding a genuinely non-strongly-convex function (e.g., $L(\theta_1, \theta_2) = \theta_1^2$, or $L(\theta_1, \theta_2) = \theta_1^4$) to test the regime that Theorem 2 predicts instability in.

## Removed Points

These points are flagged to be removed; treat them with caution:
- "The second-order ODE does not add information" (Section 3): This is an opinion about information content, not a factual error. The reformulation is mathematically valid and conceptually enables the control analysis.
- "No neural network experiments": Weakened and merged into point 3 (Major) rather than treated as a separate fatal issue, since the paper primarily targets theoretical analysis.
- "Section 4.2.2 instability is polynomial, not exponential, and about the extended state": This is a correct observation but it is a nuance the paper already partially covers (the Jordan block analysis correctly identifies linear growth). It does not invalidate the theoretical claim.
- Various presentation and formatting nitpicks: removed per filtering policy.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the derivation error in Equation (5).** The integral $\int \theta(t) dt$ cannot be evaluated as $\frac{1}{2}\theta^2$. Either (a) keep the continuous analysis as a self-contained theoretical contribution and explicitly label the discrete algorithm as a heuristic inspired by the continuous theory, or (b) replace the derivation with a correct discrete-time control argument (e.g., via a valid numerical integrator like symplectic Euler, or a provably stable discretization scheme).
2. **Correct the mislabeled example** — relabel $\theta_1^2 + \theta_2^2$ as strongly convex and add a genuinely non-strongly-convex function.
3. **Broaden the experimental validation** to include at least one higher-dimensional problem and comparison with a standard optimizer beyond vanilla GD.
4. **Analyze the $\theta^2$ term's effect** and provide practical guidance on choosing $K_1$ and $K_2$.

---

### Calibration Report

**Calibration anchors retrieved (all rounds):**

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|------------------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md` (GFlowNets) | 1.00 | 1 | Completely different topic; score reflects papers with irredeemable flaws |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nSDOkm0SKo.md` (Financial News) | 1.00 | 1 | Very different topic; poor quality |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/W98SiAk2ni.md` (Ensemble Systems) | 3.00 | 1, 2 | Similar framing (ODEs for learning algorithms); rejected for significant gaps between claims and validation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/naEeJTlRsr.md` (HR-ODEs) | 3.75 | 1, 2 | Most topic-similar; rejected for incremental contributions and limited scope. The current paper has a fatal error (incorrect derivation), which is qualitatively worse than incrementalism |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JZdd7EUefP.md` (Continuous Approx. of Momentum) | 4.75 | 2 | Topic-similar (ODE approximations of optimizers); rejected for presentation issues and limited novelty. Again, the current paper has a fatal mathematical error, which is more severe |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SXopqmHJO1.md` (Linear Convergence) | 5.00 | 1 | Strong optimization theory paper; mixed reviews. This paper has no comparable theoretical errors |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AfhNyr73Ma.md` (ZO Stability) | 7.00 | 1 | Strong accepted paper with clear theory and consistent experiments. This paper's flaws are far more severe |

**Round 1 bracket:** 2.0 – 4.0 (the paper has a fatal mathematical error, which places it below incremental-contribution papers at ~3.75, but some conceptual novelty prevents it from being a 1)

**Final score determination:** The derivation error in Equation (5) is a genuine mathematical mistake ($\int \theta(t) dt \neq \frac{1}{2}\theta^2$). This breaks the central claimed contribution linking theory to algorithm. The paper also contains a factual error in experimental labeling and extremely thin validation. However, the continuous-time analysis is technically sound and the control-theoretic framing has genuine conceptual novelty. Compared to topic-similar papers like the HR-ODEs paper (3.75, rejected for incrementalism) and the Ensemble Systems paper (3.00, rejected for claims/validation gaps), a score of 3.0 reflects that the paper has a more fundamental flaw than those works, but is not a complete non-starter.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>