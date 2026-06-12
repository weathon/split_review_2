## Summary

This paper introduces the problem of conditional causal bandits, where arms are single-node conditional interventions on a causal graph, and provides a graphical characterization of the minimal set of nodes (mGISS) guaranteed to contain the optimal intervention node. The authors define the LSCA closure of the parents of the target variable Y, prove it equals the mGISS, and present the C4 algorithm that computes it in O(|V|+|E|) time. Empirical results demonstrate significant search space reduction in real-world graphs and improved convergence when integrated with a UCB-based bandit algorithm.

## Strengths

- **Novel and well-motivated problem setting.** The paper convincingly argues that conditional interventions are more realistic than hard interventions in many real-world scenarios (medical treatment, traffic control), and that single-node interventions make the search space problem fundamentally more challenging than the multi-node case studied by Lee & Bareinboim (2018). This is a genuine gap in the literature.

- **Clean theoretical contribution.** The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4) is a surprising and elegant result that simplifies the analysis considerably. The graphical characterization via Λ-structures (Theorem 12) and the proof that the LSCA closure equals the mGISS (Theorem 13) are technically sound and well-presented.

- **Efficient algorithm with provable guarantees.** The C4 algorithm is simple, runs in linear time, and is provably correct. The connector-based approach is intuitive and well-motivated by Lemma 15.

- **Practical validation.** The experiments on real-world Bayesian networks from `bnlearn` show search space reductions of over 90% for large models, and the bandit experiments demonstrate meaningful improvements in cumulative regret (Figure 3), particularly for the larger `pathfinder` dataset.

## Weaknesses

### Fatal
None.

### Major

- **Limited experimental evaluation of the bandit impact.** Only 4 datasets are used for the bandit experiment, and only a single UCB-based algorithm (`CondIntUCB`) is tested. The paper would be substantially stronger with more datasets, more bandit algorithms (e.g., Thompson Sampling variants), and analysis of how the benefit scales with graph size and structure. The current experiments demonstrate the concept but don't fully establish practical significance.

- **No latent confounders.** The assumption of no unobserved confounding is a significant limitation that restricts applicability. While the authors acknowledge this, even a partial result or discussion of how the characterization might change (or fail) with latent variables would strengthen the paper. The claim that "this study is a necessary step toward the general case" needs more support.

- **The conditioning set Z_X is exogenous to the analysis.** The paper assumes Z_X is pre-determined by the practitioner, with only the minimal constraint An(X)\{X} ⊆ Z_X ⊆ V\De(X). The choice of Z_X can significantly affect the reward distribution, and the paper does not address how different choices of Z_X interact with the mGISS. This is a notable gap since the mGISS characterization is independent of Z_X, which could be seen as either a strength (generality) or a weakness (ignoring an important degree of freedom).

### Minor

- **Sensitivity to graph specification.** The paper briefly mentions that if a family of candidate graphs is available, C4 can be applied to each and results combined via union. However, no analysis is provided of how sensitive the mGISS is to graph misspecification, which is important for practical deployment.

- **Random graph experiments could be richer.** Only the Erdős-Rényi DAG model is used. Other graph families (e.g., scale-free, small-world) that better model real-world causal structures would provide additional insight.

- **The connection to contextual bandits could be made more precise.** The paper states that "conditional causal bandits are not simply particular cases of contextual bandits" but the formal relationship could be stated more precisely to help readers from the bandits community.

### Trivial
None.

## Nice-to-Haves

- A discussion of how the mGISS changes when the target Y has no parents (trivial case) or exactly one parent (the paper handles this but could be more explicit about the degenerate case).
- Analysis of the average size of the mGISS as a function of graph properties beyond just expected degree.
- A brief discussion of how C4 could be integrated into existing causal bandit pipelines beyond the simple UCB example.

## Novel Insights

The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4) is a genuinely novel and surprising insight. It reveals that the complexity of reasoning about conditional interventions (which involve arbitrary policies over conditioning sets) can be entirely reduced to reasoning about simple atomic interventions in a deterministic setting. This is non-obvious and elegant. The concept of Λ-structures as a complete graphical characterization of the LSCA closure is also novel and provides an intuitive geometric interpretation of which nodes are worth testing.

## Suggestions

- Expand the bandit experiments to at least 8-10 datasets and include at least one additional bandit algorithm (e.g., Thompson Sampling) to strengthen the practical claims.
- Add a brief discussion or preliminary analysis of how the framework might extend to settings with latent confounders, even if only identifying the key obstacles.
- Consider adding an experiment that varies the conditioning set Z_X to show how the mGISS interacts with different context choices.

## Score and Decision

The paper presents a clean, novel theoretical contribution with an efficient algorithm and adequate empirical validation. The problem is well-motivated, the technical results are sound, and the graphical characterization is elegant. The main limitations are the restricted experimental evaluation and the assumption of no latent confounders, but these are reasonable for a first paper on this topic. The contribution is above the median for the venue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept