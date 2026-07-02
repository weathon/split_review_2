---
job_id: f22320b1-caa9-432d-9c41-5ccac37c8d93
agent_id: ICLR_main_2026_2
status: COMPLETED
filename: vPSiCA3CkD.pdf
paper: Nesterov Finds GRAAL: Optimal and Adaptive Gradient Method for Convex Optimization
main_score_norm: 0.6
desk_reject: false
---
# Desk Rejection Assessment:
## Paper Length
Pass ✅.

## Topic Compatibility
Pass ✅. The paper is clearly within ICLR scope, specifically optimization and learning theory, with a focus on adaptive accelerated first-order methods for convex optimization.

## Minimum Quality
Pass ✅. This is a theory-heavy optimization paper with a complete scientific structure for that genre: abstract, introduction/related work, method, formal results, and proofs; although it lacks empirical experiments, it provides substantial theoretical results and quantitative comparison in **Table 1**, which is sufficient to avoid desk rejection for a purely theoretical submission.

## Prompt Injection and Hidden Manipulation Detection
Pass ✅. I found no evidence in the paper text of hidden prompts, manipulative instructions to automated reviewers, or suspicious embedded content aimed at influencing the review process.

# Expected Review Outcome:
## Summary
This paper proposes Accelerated GRAAL, an adaptive first-order method for minimizing convex differentiable objectives that combines GRAAL-style local-curvature-based stepsizes with Nesterov-type acceleration. The main technical claims are a general Lyapunov descent result for the method, an accelerated complexity bound for $L$-smooth convex optimization up to additive logarithmic factors, and a near-optimal complexity guarantee under the broader $(L_0,L_1)$-smoothness assumption.

## Strengths
The paper tackles a meaningful and fairly sharp question, namely whether one can get genuine GRAAL-style adaptivity together with Nesterov acceleration, without line search and without tuning the stepsize from global smoothness constants. That is a technically interesting gap to address, and the paper gives a nontrivial algorithmic construction rather than just a cosmetic variant of existing accelerated methods.

The central idea in **Section 2.1**, especially the additional coupling step in **Equation (15)** and the identity in **Equation (16)**, is clever. It addresses the implementability issue around the desired relation in **Equation (14)** in a way that appears genuinely tailored to the adaptive accelerated setting. This is the part of the paper where the contribution feels most substantive.

The theoretical development is fairly ambitious. The paper does not stop at the standard $L$-smooth case in **Section 3**, but also analyzes the more general $(L_0,L_1)$-smooth regime in **Section 4**. The latter is important because the paper’s claimed advantage over AC-FGM/AdaNAG is precisely about stronger adaptivity when local curvature can change rapidly.

I also appreciate that the method is spelled out algorithmically in **Algorithm 1**, not only as an abstract estimate-sequence argument. For a theory paper, the update structure is concrete enough that one can see how the pieces fit together: gradient step, coupling, extrapolation, acceleration mixing, local curvature estimate, and adaptive stepsize update.

The complexity comparison in **Table 1** is useful. It makes the positioning under $(L_0,L_1)$-smoothness much easier to parse than the surrounding prose alone. In particular, the table clarifies that the claimed advantage is not “best additive constant” but rather “near-optimal and adaptive,” which is a more defensible framing.

The descent relation in **Theorem 1**, via the potential $\Psi_k(x)$ in **Equation (21)** and the decrease inequality in **Equation (20)**, is a solid backbone for the rest of the analysis. Even though many details are deferred to the appendix, the overall proof strategy is coherent: prove a generic potential decrease, then lower-bound the cumulative stepsize mass $H_k$, then convert that into complexity.

## Weaknesses
1. **There is no empirical evaluation at all, despite repeated practical framing and comparative claims.**  
   The introduction repeatedly motivates the method through practical adaptivity and contrasts with line search, AdaGrad-type methods, AC-FGM, and AdaNAG in terms of how well they can adapt to local curvature, see **Pages 2 to 3**, especially the discussion around **Equations (5) to (7)** and the claims in **Section 1.3**. However, the paper contains no experiments, no runtime comparison, no synthetic stress test, and no even minimal numerical validation. This matters because a central selling point is not just asymptotic rate, but the ability of the stepsize to adapt “at a geometric rate” and recover quickly from poor initialization. Without plots or even a small table, the reader has no evidence that the theoretical mechanism translates into behavior one would care about in practice. For a method paper at ICLR, that is a real omission.

2. **Notation is inconsistent in a way that materially hurts verifiability of the proofs.**  
   The main algorithm in **Algorithm 1** uses $\hat{x}_k$ and $\bar{x}_k$, but **Lemma 2**, **Theorem 1**, **Equation (20)**, **Equation (21)**, and large parts of the appendix switch to $\tilde{x}_k$ without the paper clearly defining in the main text how $\tilde{x}_k$ relates to $\hat{x}_k$. In **Equation (18)**, for example, the quantities are written as $f(\bar{x}_k)-f(\tilde{x}_k)$ and $D_f(\bar{x}_k;\tilde{x}_{k-1})$, yet the algorithm never introduced $\tilde{x}_k$. The appendix then mixes $\hat{x}_k$ and $\tilde{x}_k$ in derivations. I can infer that these symbols are intended to denote the accelerated/extrapolated point after line 9, but inference is not enough here. In a proof-heavy paper, this kind of inconsistency is not a cosmetic issue, it directly raises the cost of checking whether the Lyapunov algebra is correct.

3. **The presentation of the core parameter conditions is too hand-wavy for a method that is supposed to be “hyperparameter-free.”**  
   In **Theorem 1**, the algorithm requires universal constants $\theta,\gamma,\nu>0$ satisfying **Equation (19)**. The paper says “it is easy to verify that such parameters exist” on **Page 6**, but it does not provide a concrete admissible triplet in the main text. For a theorem-centric paper, that is a strange omission. The method is advertised as not requiring tuning, yet the reader is not told what actual fixed constants to use. At minimum, the paper should give one explicit feasible choice, and ideally explain the sensitivity of the analysis to that choice.

4. **The main “optimality” claim needs more careful framing, especially in the generalized-smoothness setting.**  
   In the abstract and **Section 1.3**, the paper emphasizes near-optimality under both $L$-smoothness and $(L_0,L_1)$-smoothness. But **Table 1** makes clear that under $(L_0,L_1)$-smoothness, the additive term in **Corollary 3** is $(L_1\mathcal D)^3$, while the table itself shows a better additive dependence for Vankov et al. (2024), namely $(L_1\mathcal D)^{5/3}$, and for Tyurin (2025), $(L_1\mathcal D)^2$. So the real contribution is not best-known complexity, but adaptivity with near-optimal dependence on $\epsilon$. That is still interesting, but the paper sometimes slides from “adaptive and near-optimal” into wording that sounds closer to “state of the art overall.” The distinction matters.

5. **Several comparison claims against prior accelerated adaptive methods are argued mostly by asymptotic intuition, without a sufficiently balanced discussion of tradeoffs.**  
   **Section 3.2** argues that AC-FGM and AdaNAG are limited because their stepsize growth is only sublinear, citing **Equations (27) to (29)**. The high-level point is reasonable, but the section is quite one-sided. For instance, the paper emphasizes sensitivity to a bad $\eta_0$ for these baselines, yet does not discuss whether the proposed method may pay in constants, stability, or estimator noise when the local curvature estimate $\lambda_k$ is inaccurate. Similarly, **Section 4.2** argues that geometric growth is crucial under $(L_0,L_1)$-smoothness, but this is presented mostly as a theoretical necessity argument rather than a demonstrated algorithmic advantage. Some of these claims would be more convincing with either a simple illustrative example or numerical evidence.

6. **The local curvature estimator and stepsize rule are theoretically motivated, but the operational implications are underexplained.**  
   The estimator $\Lambda(x;z)$ in **Equation (11)** uses
   \[
   \Lambda(x;z)=\frac{2D_f(x;z)}{\|\nabla f(x)-\nabla f(z)\|^2},
   \]
   and line 10 of **Algorithm 1** takes the minimum of two such quantities. Then line 11 sets
   \[
   \eta_{k+1}=\min\left\{(1+\gamma)\eta_k,\frac{\nu H_{k-1}\lambda_{k+1}}{\eta_{k-1}}\right\}.
   \]
   This is mathematically defined, but the paper does not spend enough time explaining what this means computationally. In particular, compared with plain GD or AGD, the method requires gradients at mixed points and evaluation of Bregman divergences. For general ML readers, it would help to state explicitly the per-iteration oracle cost and whether any quantities can be cached. Since the paper criticizes line search for extra evaluations on **Page 2**, the computational budget of the proposed alternative should be equally transparent.

7. **The proof pipeline is very dense and leaves too much essential reasoning outside the main text.**  
   The paper’s validity depends heavily on the machinery in Appendices A to C, especially the proof of **Theorem 1** across **Pages 13 to 16** and the set-partition argument in **Equations (36) to (40)** for **Theorem 3**. The main text gives only the statements, not even a proof sketch for the most delicate steps. For a result of this complexity, a shorter “why the potential works” explanation in the main paper would significantly improve trust. Right now the paper is in a somewhat awkward place: too technical to take on faith, but too compressed in the main body to audit comfortably.

8. **The assumptions behind the initialization story are understated.**  
   In **Corollary 2** and **Corollary 3**, the paper says one may simply choose $\eta_0$ to be “very small,” and that this only incurs a logarithmic additive factor, see **Pages 6 and 8**. Asymptotically that is true in the stated bounds, but this can still be quite pessimistic in practice, especially since the constants hidden in the $\mathcal O(\cdot)$ are not exposed and the logarithmic term in **Equation (41)** is multiplied by $(1+L_1^2\mathcal D^2)$. Since one of the paper’s main rhetorical points is robustness to poor initialization, this deserves a more honest discussion than “just pick $10^{-10}$.”

9. **The literature positioning is somewhat narrow relative to the broader adaptive acceleration landscape.**  
   The paper does a good job discussing GRAAL, AdGD, AC-FGM, and AdaNAG, but the framing in **Sections 1.2 to 1.4** risks giving the impression that these are the only meaningful reference points for adaptive accelerated convex optimization. There are other adaptive first-order and accelerated adaptive methods in the convex optimization literature that are close enough in spirit that a broader contextualization would help readers understand exactly what is unique here. This does not invalidate the contribution, but the positioning feels somewhat curated toward the most favorable comparison set.

10. **The paper is entirely theorem-driven, but some definitions and claims in the main body are not introduced with enough care for non-specialists.**  
   For example, the $(L_0,L_1)$-smoothness condition in **Equation (30)** is important, but the leap from that assumption to the need for geometric stepsize growth is only loosely motivated before the detailed proofs. Likewise, the role of choosing the minimum in line 10 of **Algorithm 1** is not explained intuitively. There is a technically interesting story here, but the exposition assumes substantial familiarity with the recent optimization literature. That narrows accessibility more than necessary for an ICLR audience.

## Questions
1. The biggest gap for me is the complete absence of experiments. Could the authors provide even a minimal empirical validation, for example on quadratic problems with badly mis-specified initial stepsizes, or on standard convex ML tasks, comparing Algorithm 1 to AGD with backtracking, AdGD/GRAAL, AC-FGM, and AdaNAG? What I would want to see is not just final objective value, but the trajectory of $\eta_k$ and whether the claimed geometric adaptation actually appears in practice.

2. Please clarify the notation around $\tilde{x}_k$ versus $\hat{x}_k$ versus $\bar{x}_k$ in the main paper. Is $\tilde{x}_k$ intended to be exactly the post-line-9 point in **Algorithm 1**? If so, this needs to be stated explicitly and used consistently everywhere, especially in **Lemma 2**, **Theorem 1**, and **Equations (20) to (21)**.

3. Can the authors give one explicit feasible choice of $(\theta,\gamma,\nu)$ satisfying **Equation (19)**? This would make the algorithm much easier to instantiate and would support the “no hyperparameter tuning” claim more concretely.

4. In **Table 1**, the proposed additive term under $(L_0,L_1)$-smoothness is worse than some non-adaptive alternatives. Could the authors sharpen the discussion and explain more explicitly when adaptivity is worth this tradeoff? A short informal example class where the adaptive method should be preferable would help.

5. The comparison in **Section 3.2** is based on sensitivity to initialization and stepsize growth restrictions. Can the authors provide either a toy construction or a proof sketch showing more directly why subgeometric growth is fundamentally insufficient in the $(L_0,L_1)$ setting? Right now the argument is plausible but still somewhat heuristic in the main text.

6. The proofs of **Theorem 2** and **Theorem 3** rely on somewhat intricate case analyses and index sets, especially **Equations (36) to (40)**. A short roadmap in the main text explaining what the sets $\mathcal T_1,\dots,\mathcal T_4$ mean algorithmically would materially improve confidence.

## Flag For Ethics Review
- No ethics review needed.

## Details Of Ethics Concerns
None.

## Soundness Rating
3: good. The technical claims appear largely well supported by the theorem statements and proof structure, but confidence is held back by notation inconsistencies in the core analysis and by the fact that the paper provides no empirical support for its practically framed claims.

## Presentation Rating
2: fair. The high-level motivation is understandable, but the exposition becomes hard to follow in the core method and proof sections, especially due to inconsistent notation and the lack of explicit parameter choices for **Equation (19)**.

## Contribution Rating
3: good. The paper makes a meaningful contribution in adaptive accelerated convex optimization, especially through the coupling construction and the generalized-smoothness guarantees, but the lack of experiments and somewhat overstated practical framing keep it from landing as a clearly stronger contribution.

## Overall Rating
6: Marginally above the acceptance threshold. But would not mind if paper is rejected.  
This is a technically interesting theory paper with a real contribution, and I do think the adaptive acceleration mechanism is more than incremental. That said, the absence of any experiments, the notation problems around the core proof objects, and the somewhat selective framing versus prior work stop me from being more enthusiastic.

## Reviewer Confidence
4: confident. I am confident in the assessment and checked the technical flow reasonably carefully, though the dense notation and appendix-heavy proofs make full line-by-line verification costly.