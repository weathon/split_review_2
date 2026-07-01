## Summary

This paper introduces the *conditional causal bandit* problem, where arms are single-node conditional interventions on a known causal graph and the goal is to maximize an expected reward variable. The authors provide a rigorous graphical characterization of the *minimal globally interventionally superior set* (mGISS)—the smallest set of nodes guaranteed to contain the optimal intervention node—proving it equals the LSCA (lowest strict common ancestor) closure of the parents of the reward variable. They also propose C4, an \(O(|V|+|E|)\) algorithm to compute this set, and experimentally demonstrate significant search-space pruning and improved convergence in bandit regret.

## Strengths

- **Solid theoretical contribution**: The paper proves the uniqueness of mGISS, the equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4), and the graphical characterization via LSCA closure (Theorem 13). The proofs appear correct and well-structured.
- **Practical linear-time algorithm**: C4 is simple, runs in linear time in the size of the graph, and directly outputs the mGISS. This makes the theoretical insight actionable.
- **Well-motivated problem**: Conditional interventions are more realistic than hard interventions in many real-world decision-making scenarios (e.g., medical treatment, traffic control), and the single-node assumption is a natural first step before tackling the harder multi-node setting.
- **Empirical validation**: Experiments on random and real-world graphs show that mGISS can prune the search space substantially (e.g., >90% reduction in some real graphs). The regret experiments with a UCB-based conditional bandit demonstrate that using the mGISS leads to faster convergence.

## Weaknesses

### Major
1. **Strong assumption on conditioning sets \(\mathbf{Z}_X\)**. The paper assumes that \(\text{An}(X)\setminus\{X\}\subseteq \mathbf{Z}_X\) and that conditioning sets are nested (if \(W\in\text{An}(X)\) then \(\mathbf{Z}_W\subseteq\mathbf{Z}_X\)). In practice, some ancestors may be unobserved or unavailable at decision time. The paper does not discuss how robust the mGISS characterization is when these assumptions are violated, which limits practical applicability.
2. **Limited baseline comparison in bandit experiments**. The CondIntUCB algorithm is a simple context-UCB that does not leverage the causal graph beyond node selection. No comparison is made against other causal bandit methods (e.g., those using structural knowledge for policy learning). The improvement shown is only against a brute-force search over all nodes with the same algorithm. Showing relative improvement over a stronger causal baseline would strengthen the claim.
3. **Single target node per graph**. In the experiments on real graphs, \(Y\) is always chosen as the node with the most ancestors. Results may be sensitive to this choice. The paper would benefit from evaluating multiple choices of \(Y\) per graph to show consistency of the pruning benefit.

### Minor
- The paper states that the mGISS is “minimal with respect to set inclusion” and claims uniqueness (Proposition 6), but the argument for uniqueness relies on the definition of superiority (if two nodes are mutually superior, they must both be in any GISS, so the minimal set is unique). This is correct but could be explained more clearly.
- The regret plots (Figure 3) show overlapping standard deviations for some datasets (e.g., asia, sachs), making the advantage less visually compelling. A statistical test (e.g., confidence intervals on the difference) would be helpful.

### Trivial
- None.

## Nice-to-Haves
- Provide a theoretical regret bound that quantifies the benefit of pruning to the mGISS.
- Extend the empirical study to cases where some ancestors are missing from conditioning sets, to examine robustness.
- Include a comparison with the approach of Lee & Bareinboim (2018) adapted to the single-node conditional setting (if possible).

## Novel Insights

The paper’s key insight is that for single-node conditional interventions, the search space can be reduced to the LSCA closure of the parents of the reward variable—a purely graph-theoretic object. The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority is elegant and simplifies the proof. The characterization via \(\Lambda\)-structures and the linear-time algorithm provide a clean, practical tool for any causal bandit problem with conditional interventions.

## Suggestions
- Discuss the robustness of the mGISS characterization when some ancestors are not in the conditioning set, or at least clarify the scope of the assumptions.
- For the regret experiments, report the average regret difference with 95% confidence intervals instead of just standard deviations.
- Consider evaluating the search-space reduction for multiple target nodes per graph to show that the benefit is not an artifact of choosing the node with the most ancestors.

## Score and Decision

I assess the paper as a strong contribution to the causal bandits literature. The theoretical characterization is novel and complete, the algorithm is efficient, and empirical results support the practical value. The weaknesses are minor and do not invalidate the core claims.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>