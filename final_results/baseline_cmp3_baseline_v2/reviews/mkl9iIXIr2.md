## Summary

This paper studies online inventory optimization (OIO) with carryover stock and warehouse capacity constraints under non-stationary demand. The authors propose an algorithm that achieves near-optimal dynamic regret \(\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})\) by connecting OIO to smoothed online convex optimization (SOCO) via a two-stage projection strategy and a doubling trick for the unknown sell-out period \(L_{\max}\). They also provide a matching \(\Omega(\sqrt{L_{\max}T})\) lower bound for static regret, resolving an open question from prior work.

## Strengths

- **Novel connection between OIO and SOCO.** The paper shows that under the proposed two-stage projection, the dynamic regret of OIO can be bounded by the regret of a SOCO problem with switching costs proportional to \(L_{\max}\). This insight is elegant and enables the use of existing SOCO algorithms for inventory management.
- **Near-optimal dynamic regret guarantee.** The algorithm achieves \(\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})\) dynamic regret without prior knowledge of \(L_{\max}\) or the path-length \(P_T\), improving over prior static regret bounds by a factor of \(\sqrt{L_{\max}}\).
- **First lower bound for OIO.** The paper establishes a \(\Omega(\sqrt{L_{\max}T})\) lower bound, showing that the \(\sqrt{L_{\max}}\) factor is unavoidable and that the static regret bound is nearly optimal.
- **Clear and well-structured exposition.** The problem setting, algorithmic ideas, and theoretical results are presented in a logical and accessible manner.

## Weaknesses

### Fatal
None.

### Major
- **Assumption of known time horizon \(T\).** The base learner (Algorithm 5) requires \(T\) as an input to set the number of experts \(K\) and the block sizes \(n^k\). In many online settings, \(T\) is not known in advance. The paper does not discuss how to handle an unknown horizon, which limits the practical applicability of the algorithm. A doubling trick for \(T\) could be employed, but this is not addressed.

### Minor
- **Linear capacity constraint.** The paper assumes a linear-sum capacity constraint \(\sum_i y_t^i \leq D\), which is a special case of the general convex constraint considered in Hihat et al. (2023). The authors acknowledge this limitation and leave extension to future work.
- **Computational overhead.** The meta-algorithm (SOGD) incurs \(\mathcal{O}(T\log T)\) cost, which is higher than simple OGD. This is common for non-stationary environments but may be a concern for large-scale systems.
- **No empirical validation.** The paper is purely theoretical. While not required, experiments on synthetic or real inventory data would strengthen the practical relevance.

### Trivial
None.

## Nice-to-Haves

- Provide a variant of the algorithm that works with an unknown horizon \(T\) (e.g., using a doubling trick for \(T\)).
- Discuss the case where \(L_{\max} = \Omega(T)\) and the regret becomes linear, clarifying the boundary of sublinear regret.
- Include a brief numerical illustration to demonstrate the algorithm’s behavior under non-stationary demand.

## Novel Insights

The key insight is that the carryover stock constraint in OIO can be transformed into a switching cost in a SOCO problem through a two-stage projection. This connection is non-trivial because the feasible region of the decision \(y_t\) depends on the previous carryover stock, while the comparator \(u_t\) is not subject to this constraint. By analyzing cycles during which the projected decision differs from the base learner’s output, the paper shows that the regret decomposes into the base learner’s regret plus a switching cost proportional to \(L_{\max}\). This perspective opens the door to applying rich SOCO theory to inventory management.

## Suggestions

- Address the known-horizon assumption by either noting that \(T\) is typically known in periodic-review inventory settings or by sketching a doubling-trick extension for unknown \(T\).
- Clarify in the main text how the subgradient \(g_t\) can be obtained without full demand information (e.g., for Newsvendor loss), as this is crucial for practical applicability.

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>