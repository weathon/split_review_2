## Summary

This paper studies causal bandits with conditional interventions (single-node interventions where the intervened value can depend on observed variables). The authors provide a graphical characterization of the minimal set of nodes guaranteed to contain the optimal intervention node (mGISS), proving it is exactly the LSCA (Lowest Strict Common Ancestor) closure of the parents of the reward variable. They propose the C4 algorithm that computes this set in linear time O(|V|+|E|), and demonstrate empirically that pruning the search space using this method significantly reduces regret in bandit algorithms.

## Strengths

- **Novel and well-motivated problem formulation**: The paper introduces conditional interventions to causal bandits, which is a natural and important extension that better models real-world decision-making scenarios where actions depend on observed context. The motivation using the doctor/treatment example and the train delay example is clear and compelling.

- **Clean theoretical contribution**: The graphical characterization of mGISS via LSCA closure and Λ-structures is elegant and non-trivial. The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4) is a clever reduction that simplifies the analysis.

- **Linear-time algorithm**: The C4 algorithm is simple yet efficient with O(|V|+|E|) complexity, making it practical for large graphs. The connector concept provides an intuitive explanation for why certain nodes can be pruned.

- **Empirical validation on real-world graphs**: The experiments on bnlearn datasets (asia, sachs, child, pathfinder) demonstrate meaningful regret reduction, with pruning being especially effective for larger, sparser graphs typical of real-world causal models.

## Weaknesses

### Major

- **Strong assumption about observable conditioning sets**: The assumption that An(X)\{X} ⊆ Z_X (all ancestors are observable and can be used for the conditional intervention) is quite strong. In many real-world applications, some ancestors may not be observed or may not be available at decision time. While the authors acknowledge this is a minimal assumption, it significantly limits applicability and the paper does not discuss how violations would affect the results.

- **No comparison with baselines**: The experiments only compare "brute-force" (all ancestors) vs. mGISS pruning. There is no comparison with alternative node selection strategies or state-of-the-art causal bandit algorithms that also leverage graph structure. This makes it difficult to assess how much of the improvement is due to the specific mGISS characterization vs. simply reducing the search space in any reasonable way.

- **Limited empirical scope for regret evaluation**: Only 4 datasets are used, all from bnlearn, and all relatively small (8-109 nodes). The regret curves show improvement, but it's unclear how the method scales to graphs with hundreds of nodes or complex dependencies. The random graph experiments only measure search space reduction, not regret.

### Minor

- **The assumption that Z_X must be observable for X is not fully formalized**: The paper states "we assume that An(X)\{X} ⊆ Z_X" and also requires that "W ∈ An(X) ⇒ Z_W ⊆ Z_X" for observable conditioning sets. These constraints are motivated but their necessity for the theoretical results is not entirely clear. Would the mGISS characterization change if practitioners chose smaller conditioning sets?

- **The relationship to Lee & Bareinboim (2020) could be more precise**: The paper mentions connection to optimal scopes but does not fully explain how the single-node conditional intervention setting relates to or differs from that work's scope-based characterization.

### Trivial

- The caption of Figure 1 is somewhat redundant with the figure description in the text.

## Nice-to-Haves

- An ablation study comparing C4 pruning against random pruning of the same number of nodes would strengthen the claim that the specific mGISS set is important.
- Extending experiments to include synthetic graphs with controlled confounding or partial observability would help understand robustness.
- Discussion of how the C4 algorithm could be adapted when the graph is partially unknown or when there is uncertainty about edges.

## Novel Insights

Beyond the paper's own contributions, the key insight is that for single-node conditional interventions, the optimal intervention node can be characterized purely through the graph's Λ-structures over the parents of the reward variable. This is surprising because one might expect that the optimal node depends on the specific functional relationships or noise distributions. The equivalence result (Proposition 4) showing that conditional-intervention superiority reduces to deterministic atomic-intervention superiority is particularly insightful, as it connects a probabilistic sequential decision problem to a simpler deterministic optimization. This suggests that the complexity of conditional interventions does not come from the conditioning per se, but from the need to coordinate multiple parents through a single intervention.

## Suggestions

- Discuss the practical implications of the strong observability assumption (An(X)\{X} ⊆ Z_X) and how practitioners might verify whether their application satisfies it.
- Add a baseline comparison with a standard bandit algorithm that randomly selects among all ancestors (not just mGISS) to isolate the benefit of the specific characterization versus any reduction.
- Consider including a small theorem or remark about the expected size of mGISS as a function of graph sparsity, based on the random graph results.

## Score and Decision

The paper makes a genuine theoretical contribution to the causal bandits literature by characterizing the minimal search space for conditional interventions. The problem is well-motivated, the theoretical development is rigorous, and the algorithm is practical. However, the strong assumptions about observability and the lack of comparison with alternative approaches temper the overall impact. The empirical evaluation, while positive, is somewhat narrow.

Score: 7

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>