## Summary
This paper studies conditional causal bandits, where arms are single-node conditional interventions (the value of the intervened variable can depend on observed context). The authors characterize the minimal set of nodes (mGISS) that is guaranteed to contain the best node for intervention, using the notion of Lowest Strict Common Ancestors (LSCA) and Λ-structures. They prove that the mGISS equals the LSCA closure of the parents of the reward variable, provide a linear-time algorithm (C4) to compute it, and empirically show that restricting the search space to the mGISS substantially reduces the number of nodes to consider and improves regret in standard bandit algorithms.

## Strengths
- **Novel problem formulation**: The paper studies conditional interventions in causal bandits, which are more realistic than hard or soft interventions for many applications. The setting with single-node conditional interventions under no latent confounders is unexplored and non-trivial.
- **Clean theoretical characterization**: The main result (Theorem 13) provides a rigorous graphical characterization of the minimal search space through LSCA closure, building on a clever equivalence (Proposition 4) between conditional-intervention superiority and deterministic atomic-intervention superiority. Theorem 12 gives an intuitive equivalent definition via Λ-structures.
- **Efficient algorithm**: The C4 algorithm computes the mGISS in O(|V|+|E|) time, which is optimal up to constants and makes the method scalable.
- **Empirical validation**: Experiments on random graphs and real-world Bayesian networks (bnlearn) show substantial pruning (often >90% reduction for larger, sparser graphs). Regret curves on four real causal graphs demonstrate that using the mGISS with a simple UCB-based bandit accelerates convergence.

## Weaknesses
### Fatal
None.

### Major
- **Limited experimental scope for bandit evaluation**: The bandit comparison uses only a single, custom algorithm (CondIntUCB) on 4 real graphs. The reward generation is not fully described (though likely from the true CPDs of the bnlearn models). The number of runs (300-500) is reasonable, but the evaluation would be stronger with more diverse causal graphs, comparison against other baseline strategies (e.g., random node selection or using all ancestors), and perhaps synthetic SCMs with known ground-truth.
- **The setting assumes known conditioning sets Z_X and no latent confounders**: While acknowledged, this restricts immediate applicability. The paper’s contributions are still significant, but the limitations should be more prominently discussed in the main text (not just in the conclusion). The claim that “restricting to single-node interventions in fact makes the problem more challenging” is somewhat argued but could be more clearly justified.

### Minor
- **Clarity of bandit regret baseline**: The paper compares “brute-force” (all nodes) vs. mGISS, but it is ambiguous whether the brute-force set is all ancestors of Y or all non-Y nodes. The random graph experiments use fraction of An(Y){Y} as denominator, which is natural, but the bandit experiments might use a different set. Clarifying this would help.
- **Definition of observable conditioning sets**: The assumption that An(X) ⊆ Z_X and Z_X ⊆ V \ De(X) is justified by examples, but the paper does not discuss cases where some ancestors are unobserved or not part of the conditioning set. The results likely still hold as long as Z_X contains all ancestors, but this could be stated more precisely.
- **The equivalence in Proposition 4** relies on deterministic atomic interventions, which is a clever reduction. The proof is in the appendix; the main paper could give a brief intuition.

### Trivial
- Some equation numbers and figure references appear in the main text (e.g., “Figure 2: (a) A diagram…”) that are likely artifacts of the PDF extraction but not errors.
- The paper repeatedly mentions “Section 2” and “Appendix” without providing page numbers; this is fine for the PDF but could be improved.

## Nice-to-Haves
- An ablation study on the effect of different conditioning set choices (beyond minimal ancestors) would be insightful.
- Combining C4 with more advanced causal bandit algorithms (e.g., those leveraging causal structure for faster learning) could demonstrate broader utility.
- A discussion on extending the results to settings with latent confounders, even if only speculative, would strengthen the outlook.

## Novel Insights
The paper’s key insight is that the minimal search space for conditional interventions on a single node is determined by the lowest strict common ancestors (LSCA) of the parents of the reward variable. This goes beyond the obvious candidates (parents and their common ancestors) and shows that the closure under LSCA is both necessary and sufficient. The equivalence between conditional interventions (with unknown policies) and deterministic atomic interventions (with a single fixed unit) is a clever trick that simplifies the analysis significantly. The Λ-structure characterization provides an intuitively appealing graphical criterion for whether a node can be eliminated.

## Suggestions
- In the experimental section, explicitly state the baseline set used for the regret comparison (e.g., “all nodes in V\{Y}” or “all ancestors of Y”). Report the fraction of ancestors retained for each dataset to connect with the earlier experiments.
- Provide a brief outline of the proof of Proposition 4 in the main paper (one paragraph of intuition) to help readers follow the reasoning.
- Consider adding a figure that illustrates the C4 algorithm’s connector propagation on an example graph, which would help readers unfamiliar with the algorithm.

## Score and Decision

**Score**: 8  
**Decision**: Accept

The paper presents a novel, theoretically sound characterization of the minimal search space for conditional causal bandits, supported by an efficient algorithm and informative experiments. It addresses an important gap in the causal bandits literature and provides a practical tool that can be used as a preprocessing step for any bandit algorithm. The weaknesses are minor and do not undermine the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>