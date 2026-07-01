All theorems, definitions, and claims referenced in my review are verified in the paper. Here is the final consolidated review:

---

## Summary
This paper studies single-node conditional-intervention causal bandits, where the arm is an intervention `do(X = g(Z_X))` with a policy `g` over observed context `Z_X`. The main contribution is a graphical characterization of the minimal set of nodes (mGISS) guaranteed to contain the node with the optimal conditional intervention. The authors prove that conditional-intervention superiority is equivalent to deterministic atomic-intervention superiority (Proposition 4), characterize the mGISS as the LSCA closure of Pa(Y) (Theorem 13), and provide a linear-time algorithm (C4) to compute it. Experiments on random and real-world graphs show substantial search-space reduction.

## Strengths
- **Clean theoretical bridge from conditional to deterministic-atomic superiority (Proposition 4).** The equivalence reduces a problem with rich functional degrees of freedom (conditional policies) to a structural/graphical problem about which node can exert the finest-grained control over Y in the worst-case SCM. Without this result, the graphical machinery would not connect to the conditional-intervention setting.
- **Elegant and non-trivial mGISS characterization via LSCA closure (Theorem 13).** The concept of lowest strict common ancestors, the Λ-structure reformulation (Theorem 12), and the proof that the LSCA closure of Pa(Y) equals the unique minimal globally interventionally superior set form a coherent theoretical package. The failure example in Figure 1d correctly motivates why naive LCA-based reasoning is insufficient.
- **Clean, efficient C4 algorithm.** Computing the mGISS in O(|V|+|E|) time using the connector notion (Definition 14, Lemma 15) is a solid algorithmic contribution. The connector idea captures a clear "bottleneck" intuition.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **Bandit experiment regret definition weakens the empirical evidence.** Footnote 11 defines regret relative to "the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." This is not a ground-truth benchmark — it is an artifact of the algorithm's own convergence behavior within each condition. If the mGISS condition converges to a suboptimal node (because the truly optimal node was pruned, though Theorem 13 guarantees it is not), this regret definition would still report convergence. The regret curves therefore primarily demonstrate convergence speed, not correctness of node selection. A synthetic SCM experiment with known ground truth (where the true optimal intervention can be identified by exhaustive search) would directly validate Theorem 13 and strengthen the empirical case.

2. **No control for subset size in the bandit experiment.** The experiment compares mGISS against the full ancestor set, but any smaller subset of nodes would produce lower cumulative regret under UCB due to reduced exploration overhead. Without a comparison against random subsets of the same size, the experiment cannot distinguish whether mGISS confers an advantage beyond simply having fewer arms. The search-space-reduction experiments (which quantify pruning magnitude) are valid on their own, but the bandit experiment does not specifically validate the mGISS over other pruning strategies.

### Trivial
- **No variance reported for random-graph experiments.** The paper reports averaged fractions (17%, 29%, etc. for 500 nodes) over 1000 random graphs but provides no standard deviations or error bars. The variance across graphs could be substantial and would help readers gauge the reliability of the trends.

## Nice-to-Haves
- A synthetic SCM experiment where ground-truth optimal nodes are known by construction, allowing direct verification that the mGISS always contains them.
- Reporting which nodes are selected at convergence in the bandit experiment (not just regret curves).
- Error bars / standard deviations for the random-graph search-space-reduction results.

## Removed Points
These points are flagged to be removed; treat them with caution.
- **Issue 2 (experiment does not instantiate conditional interventions):** The reviewer claimed CondIntUCB does not learn policies g. However, maintaining per-context UCB bandits (one per realization of Z_X) and selecting argmax_a UCB_z(a) for each context implicitly defines a valid policy g(z). This is standard for discrete-context contextual bandits, and the paper transparently cites Lattimore & Szepesvári (2020, §18.1). This criticism stems from a misunderstanding.
- **Proposition 4 proof concern:** The reviewer speculated about whether the proof handles a subtle case. The proof is in the appendix, which was stripped by the PDF parser. Speculative criticisms about appendix content that cannot be verified are removed per guidelines.
- **Missing comparison to Lee & Bareinboim (2018):** The paper explicitly states the problems are "fundamentally different and non-comparable" (line 39). A quantitative comparison of search-space size would not be meaningful.
- **Ancestor conditioning set limitation (Section 2):** The paper addresses this in footnote 3, noting that the assumption that all ancestors are included in Z_X is not necessary for the results to hold.
- **Various section-by-section observations** that are descriptive or speculative rather than verified weaknesses.
- **"Strengthening the Paper on Its Own Terms" suggestions** that are nice-to-haves, not critiques.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a synthetic SCM experiment: generate random SCMs consistent with a given graph G, exhaustively evaluate all single-node conditional interventions to identify the true optimal node, and verify it always falls in mGISS_Y(G). This directly validates Theorem 13.
2. In the bandit experiment, include a random-subset-of-same-size control and report the final node selected at convergence (not just regret curves).
3. Add standard deviations or confidence intervals to the random-graph pruning results.

## Score and Decision
MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>