## Summary

This paper introduces FEDSGM, a unified framework for federated constrained optimization that simultaneously addresses four major challenges: functional constraints, communication bottlenecks (via bidirectional compression with error feedback), multiple local updates, and partial client participation. The method extends the switching gradient method to the federated setting, providing projection-free, primal-only updates with convergence guarantees at the canonical $\mathcal{O}(1/\sqrt{T})$ rate, and introduces a soft switching variant to stabilize updates near the feasibility boundary. The authors validate their approach on Neyman-Pearson classification and constrained Markov decision process tasks.

## Strengths

- **Unified treatment of four major FL challenges**: The paper is the first to simultaneously address functional constraints, bidirectional compression with error feedback, multiple local updates, and partial client participation within a single framework. This is a genuinely novel contribution that addresses a significant gap in the literature.

- **Clean theoretical analysis with explicit dependence on key parameters**: The convergence bounds clearly isolate the effects of local steps ($E$), compression accuracies ($q, q_0$), and partial participation ($m/n$), making the theoretical contributions interpretable and practically meaningful.

- **Soft switching with geometric motivation**: The analysis of rotational dynamics via skew-symmetric matrices ($K_{\text{glob}}$ and $K_{\text{loc}}$) provides a principled explanation for oscillations near the feasibility boundary, and the soft switching mechanism offers a theoretically grounded remedy.

- **Strong empirical validation on challenging tasks**: The experiments on NP classification and CMDP (with TRPO) demonstrate the method works in practice, including in non-convex settings beyond the theoretical assumptions.

## Weaknesses

### Major

- **The theoretical analysis assumes convexity, but the main empirical validation is on a highly non-convex RL task (CMDP)**: While the authors acknowledge this limitation, the CMDP experiments constitute a significant portion of the empirical evaluation. The paper would benefit from either (a) a non-convex analysis (even with weaker guarantees) or (b) more extensive convex experiments to match the theory. The current presentation risks overclaiming empirical support for the theory.

- **The convergence rate for the constrained setting is not compared to known lower bounds**: The paper claims the $\mathcal{O}(1/\sqrt{T})$ rate is "canonical," but does not establish whether this rate is optimal for the constrained federated setting with all four challenges combined. A discussion of lower bounds (or their absence) would strengthen the theoretical contribution.

- **The soft switching convergence guarantee (Theorem 2) requires $\beta \geq 2/\epsilon$, which essentially recovers hard switching when $\epsilon$ is small**: This undermines the practical benefit of soft switching in the high-precision regime. The paper should clarify whether soft switching provides any theoretical advantage over hard switching, or if its benefits are purely empirical.

### Minor

- **The partial participation bound contains terms scaling with $n/m$ that are not fully explained**: The dependence on $n/m$ in the $\epsilon$ expression for partial participation (Theorem 1) appears to grow linearly with the total number of clients, which could be problematic in large-scale FL. A brief discussion of when this term dominates would be helpful.

- **The experimental setup for CMDP uses TRPO, which is not the simple gradient descent analyzed in the theory**: While the authors note this, the mismatch between the theoretical optimizer (gradient descent) and the practical one (TRPO with natural gradients) makes it difficult to attribute empirical success to the theoretical guarantees.

### Trivial

- The notation $\Gamma$ in Theorem 1 is defined differently for full and partial participation cases, which could cause confusion.

## Nice-to-Haves

- An ablation study isolating the effect of each component (compression, local steps, partial participation) on the convergence would strengthen the empirical validation.
- A comparison against a baseline that handles constraints via projection or penalty methods (e.g., constrained FedAvg) would help contextualize the practical benefits of the switching approach.
- Discussion of how the method might extend to stochastic gradients (SGD) rather than full gradients, which the authors mention as future work but could be partially addressed.

## Novel Insights

Beyond the paper's own contributions, the geometric analysis of rotational dynamics via $K_{\text{glob}}$ and $K_{\text{loc}}$ is a genuinely novel insight. The observation that even when global gradients are aligned ($K_{\text{glob}} = 0$), local heterogeneity can induce skewness ($K_{\text{loc}} \neq 0$) that causes oscillations in federated constrained optimization is a valuable conceptual contribution. This provides a principled explanation for why federated constrained optimization is fundamentally harder than its centralized counterpart, and why soft switching can help. The connection between the switching parameter $\beta$ and the amplification of heterogeneity-driven rotations offers a new perspective on algorithm design for constrained FL.

## Suggestions

- Add a discussion of known lower bounds for constrained convex optimization in the federated setting, or explicitly state that such bounds are not yet established.
- Clarify whether the soft switching guarantee (Theorem 2) can be improved to allow $\beta$ independent of $\epsilon$, or if the $\beta \geq 2/\epsilon$ condition is fundamental.
- Consider adding a simple convex experiment (e.g., constrained logistic regression on a standard benchmark) that directly validates the theoretical rates.

## Score and Decision

The paper makes a significant contribution by unifying four major challenges in federated constrained optimization within a single framework, with clean theoretical analysis and practical validation. The main weaknesses are the convexity assumption versus non-convex empirical validation, and the lack of lower bound comparison. However, these do not invalidate the core contribution. The paper is well-written, the theory is sound, and the empirical results support the claims within the stated limitations.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>