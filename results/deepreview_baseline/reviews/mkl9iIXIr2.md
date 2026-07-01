## Summary
This paper studies online inventory optimization (OIO) under non-stationary demands, a variant of online convex optimization with carryover stock constraints. The authors propose an algorithm based on a two-stage projection strategy that connects OIO to smoothed online convex optimization (SOCO), achieving near-optimal dynamic regret \(\tilde{\mathcal{O}}(\sqrt{L_{\max}(1+P_T)T})\) without prior knowledge of the sell-out period \(L_{\max}\) or the comparator path length \(P_T\). They also tighten the static regret bound to \(\mathcal{O}(\sqrt{L_{\max}T})\) and provide a matching \(\Omega(\sqrt{L_{\max}T})\) lower bound, resolving an open question from prior work.

## Strengths
- **Novel and technically sound approach**: The connection between OIO and SOCO via a two-stage projection is elegant and not obvious. The analysis carefully handles the carryover stock constraint by bounding the regret in terms of the base learner’s switching costs, which is a key technical insight.
- **Near-optimal dynamic regret**: The algorithm’s dynamic regret guarantee matches the lower bound up to logarithmic factors, and the static regret bound improves upon existing results by a \(\sqrt{L_{\max}}\) factor. This is a significant theoretical advance for inventory optimization in adversarial environments.
- **Lower bound**: The paper provides the first \(\Omega(\sqrt{L_{\max}T})\) lower bound for the OIO setting, confirming the near-optimality of the proposed algorithm and also establishing a lower bound for SOCO as a corollary.
- **Clear exposition**: The problem setting, the algorithm design, and the main proof ideas are presented in a well-structured and understandable manner. The use of examples to motivate dynamic regret is effective.

## Weaknesses
### Fatal
None.

### Major
- **No empirical evaluation**: The paper is purely theoretical and provides no experiments, not even on synthetic data. While this is acceptable for a theory paper, empirical validation would significantly strengthen the practical relevance and help assess the tightness of the bounds in realistic scenarios. The paper would benefit from at least small-scale simulations illustrating the algorithm’s behavior under various demand patterns.

### Minor
- **Restricted capacity constraint**: The analysis assumes a linear-sum capacity constraint \(\sum_i y_t^i \leq D\). As the authors note, general convex constraints are left for future work. This limits the applicability of the current results compared to the more general convex setting of Hihat et al. (2023). The paper could discuss whether the linear constraint is essential or whether the proof techniques extend to convex sets with additional structure.
- **Dependence on \(L_{\max}\) and \(P_T\)**: The algorithm requires a doubling trick to handle the unknown \(L_{\max}\), which adds overhead. While the theoretical guarantee is preserved, the practical efficiency could be affected by restarts. A brief discussion of this overhead would be helpful.

### Trivial
- None.

## Nice-to-Haves
- A simple numerical experiment (e.g., synthetic demands with known \(L_{\max}\) and \(P_T\)) to demonstrate the algorithm’s regret behavior and validate the theoretical bounds.
- Discussion on how to estimate \(L_{\max}\) online without the doubling trick, perhaps using a confidence-based method.

## Novel Insights
The paper’s key insight is that online inventory optimization with carryover stocks can be reduced to smoothed online convex optimization by projecting the base learner’s decisions onto the feasible region. This reduction reveals that the dynamic regret in OIO is governed by a switching cost proportional to the cycle length (bounded by \(L_{\max}\)), which is a non-trivial consequence of the inventory dynamics. The connection between OIO and SOCO is interesting in its own right and may inspire further cross-fertilization between these two areas.

## Suggestions
- Add a small experimental section (or in the appendix) with synthetic data to illustrate the algorithm’s regret and show that the theoretical bounds are not overly pessimistic.
- Discuss more explicitly the difficulty of generalizing to convex constraints and whether the linear constraint is truly needed in the proofs.

## Score and Decision
- **Score**: 8 (accept)
- **Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>