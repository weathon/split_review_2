## Summary

This paper addresses online inventory optimization (OIO) under non-stationary demand, proposing the first algorithm with near-optimal dynamic regret guarantees. The key technical contribution is a two-stage projection strategy that transforms the OIO problem into a smoothed online convex optimization (SOCO) problem, enabling the use of existing SOCO algorithms. The algorithm achieves \(\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})\) dynamic regret and improves the static regret bound from \(\mathcal{O}(L_{\max}\sqrt{T})\) to \(\mathcal{O}(\sqrt{L_{\max}T})\), matching a new \(\Omega(\sqrt{L_{\max}T})\) lower bound the authors establish.

## Strengths

- **Novel dynamic regret analysis for OIO.** This is the first work to provide dynamic regret guarantees for online inventory optimization with carryover stock constraints, advancing beyond previous static regret results.
- **Elegant reduction to smoothed OCO.** The two-stage projection strategy and cycle-based analysis cleanly connect OIO to SOCO, making the problem amenable to existing SOCO algorithms and their regret bounds.
- **Improved static regret and matching lower bound.** The \(\sqrt{L_{\max}}\) improvement over prior work is significant, and the new lower bound resolves an open question about the optimality of existing OIO algorithms.
- **Adaptivity to unknown environment difficulty.** The algorithm uses a doubling trick to avoid prior knowledge of \(L_{\max}\), and the base learner (SOGD) adapts to the path-length \(P_T\) without needing it in advance.
- **Clear presentation and positioning.** The paper is well-structured, with a formal problem definition, clear explanation of the algorithm, and detailed comparison to related work in Table 1.

## Weaknesses

### Fatal
None.

### Major
- **No experimental evaluation.** The paper is purely theoretical. While theory papers are acceptable for ICLR, the practical nature of inventory management would benefit from even simple simulations to illustrate the behavior of the algorithm and validate the regret bounds.
- **The \(L_{\max}\) assumption may be restrictive.** The definition of \(L_{\max}\) requires that within every interval of length \(L_{\max}\) the cumulative demand for each item reaches at least \(D\). This can be a strong condition in practice, and the paper provides limited discussion of how realistic this is or how the algorithm degrades when \(L_{\max}\) is large.

### Minor
- **The dynamic regret bound includes a logarithmic factor.** The bound \(\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})\) is not strictly matching the \(\Omega(\sqrt{(1+P_T)T})\) lower bound from OCO (without \(L_{\max}\)). The paper claims “near-optimal,” but a dynamic regret lower bound that includes \(L_{\max}\) is not provided, so the tightness in \(L_{\max}\) is only justified for static regret.
- **The algorithm assumes knowledge of the horizon \(T\).** The base learner parameters (e.g., learning rates, number of combiners \(K\)) depend on \(T\). A standard extension to unknown \(T\) using a doubling trick is not discussed, though it would likely be straightforward.
- **The projection step requires solving a linear constraint with lower bounds.** While this is efficient, the paper does not discuss the computational cost per round beyond stating \(\mathcal{O}(T\log T)\) overhead from the meta-algorithm; details on the cost of projection itself could be clarified.

### Trivial
None.

## Nice-to-Haves

- Empirical validation using synthetic or real-world demand sequences to demonstrate regret behavior and compare against baselines.
- Extension to more general convex capacity constraints beyond the linear sum constraint, as the paper acknowledges this limitation.
- Discussion of handling unknown \(T\) via a meta-doubling trick.

## Novel Insights

The central insight is that the carryover stock constraint in OIO induces a switching cost proportional to the sell-out period \(L_{\max}\) when the base learner’s decisions are projected onto the feasible region. This allows the OIO regret to be bounded by the SOCO regret of the base learner, elegantly bridging two previously separate problem classes. Additionally, the lower bound shows that the \(\sqrt{L_{\max}}\) factor is inherent, and the connection implies a new lower bound for SOCO itself, illustrating a nice cross-fertilization.

## Suggestions

- Include simulation results for a simple single-item or multi-item setting with non-stationary demands to illustrate the empirical regret and the effect of \(L_{\max}\) and \(P_T\).
- Add a remark on how the algorithm can be adapted to unknown \(T\) (e.g., a standard doubling trick on the horizon).
- Clarify whether the dynamic regret lower bound can be extended to incorporate \(L_{\max}\) (e.g., \(\Omega(\sqrt{L_{\max}(1+P_T)T})\)) or discuss why such a bound is challenging.

## Score and Decision

**Score:** 8 – Accept  
**Decision:** Accept  

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>