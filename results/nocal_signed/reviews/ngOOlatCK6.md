Now I have all the information needed. Let me compile the final consolidated review.

---

## Summary

This paper studies conditional-intervention causal bandits (single-node interventions with policies conditioned on observed variables). It characterizes the minimal globally interventionally superior set (mGISS) as the LSCA (lowest strict common ancestor) closure of the parents of the target variable Y (Theorem 13), proves equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4), and proposes the linear-time C4 algorithm to compute this set. The theoretical contributions are clean, non-obvious, and well-motivated.

## Strengths

- **Clean theoretical result (Theorem 13).** The characterization that the mGISS equals the LSCA closure of Pa(Y) is elegant and well-motivated. The paper builds intuition progressively through examples showing why simpler proposals (just Pa(Y); Pa(Y) ∪ LCA(Pa(Y))) fail and why recursive closure is needed. The Λ-structure re-characterization (Theorem 12) provides a simple graphical membership test.

- **Proposition 4 is a nontrivial insight.** The equivalence between conditional-intervention superiority in probabilistic SCMs and atomic-intervention superiority in deterministic SCMs bridges two settings that look very different on the surface, enabling reasoning about the simpler deterministic atomic case while claiming results for the more complex conditional case. This is the enabling idea of the whole paper.

- **Linear-time C4 algorithm (Theorem 16, O(|V|+|E|)).** The connector mechanism is a clean graph-theoretic idea that computes the LSCA closure without explicitly constructing LSCA sets via pairwise comparisons. The algorithm is practically relevant as a pre-processing step for any downstream causal bandit algorithm.

- **Honest and clear scope.** The paper transparently states its assumptions (no latent confounders, specific inclusion relations for Z<sub>X</sub>), acknowledges limitations, and clearly distinguishes its setting from related work (Lee & Bareinboim 2018, 2020).

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison against simpler pruning baselines.** The experiments compare mGISS only against brute-force (all ancestors of Y). The theoretical motivation (Figures 1a–1d) explicitly shows that Pa(Y) alone, and Pa(Y) ∪ LCA(Pa(Y)), can fail to contain the optimal node. However, the experiments never quantify the sizes of these simpler candidate sets on the same random and real graphs. The reader cannot assess how much the recursive LSCA closure adds beyond what a simpler rule would achieve, especially in random graphs where Λ-structures may be rare. An ablation comparing Pa(Y), Pa(Y) ∪ LCA(Pa(Y)), Pa(Y) ∪ LSCA(Pa(Y)), and the full LSCA closure would directly validate what the theoretical complexity buys in practice.

- **Regret computation uses an empirically estimated oracle (footnote 11).** Cumulative regret is computed with respect to "the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." This is not the standard regret definition (which uses the *true* best arm). The models are Bayesian networks with known CPDs, so the true optimal expected reward could be computed for small models. The relative comparison (mGISS vs. brute-force under the same definition) is still informative, but the claim that "better nodes are selected earlier for applying conditional interventions" is not fully supported — what is shown is faster convergence to the empirical consensus, which may not be the true optimum. This does not invalidate the theoretical contributions but weakens the strength of the empirical claims.

### Minor

- **Potential selection bias in bandit experiments.** Datasets were selected because their mGISS is "sufficiently small to allow experimentation with our setup" (lines 281–282). Datasets with larger mGISS (where pruning matters most) are excluded for computational reasons. The pathfinder dataset (109 nodes) partially addresses this, but the concern remains. The paper acknowledges this, which is good, but it limits the generality of the empirical conclusions.

- **CondIntUCB assumes finite/small domain sizes.** The algorithm maintains one UCB per context value per node, which does not scale to variables with large or continuous domains. This is a limitation of the experimental baseline rather than the core contribution, but it constrains the scope of the empirical validation.

### Trivial
None.

## Nice-to-Haves

- Ablation comparing mGISS against its natural subsets (Pa(Y), Pa(Y) ∪ LCA(Pa(Y)), Pa(Y) ∪ LSCA(Pa(Y))) on the same random and real graphs used in Figures 5 and 6.
- For the bandit experiments, recompute regret against the true model-based optimal arm (from known bnlearn CPDs) for small datasets where exact computation is tractable.
- Report wall-clock time, number of arms before/after pruning, and per-round cost of CondIntUCB.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- *"Single-node makes it harder claim is not demonstrated"* — REMOVED. The paper provides explicit reasoning (lines 98–99) that the multi-node case reduces to Pa(Y) (trivial) while the single-node case requires the more complex LSCA closure (non-trivial). The claim is sufficiently supported by the paper's own results.
- *"Definition 1 equation has a parser artifact in rendering"* — REMOVED as a formatting issue from PDF extraction, not an author error.
- *"The 'for all SCMs' quantifier is very strong"* — REMOVED. The paper is transparent about this being a worst-case guarantee. It is a feature of the definition, not a flaw.
- *"Z<sub>X</sub> includes all ancestors may not always hold in practice"* — REMOVED. The paper already addresses this in footnote 3 and explicitly states it as an assumption of the problem setting.
- *Pure formatting nitpicks and section-by-section observations that are not weaknesses* — REMOVED per filtering guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. For the bandit experiments, recompute regret against the true optimal arm derived from the known CPDs of the bnlearn models (at least for the smaller datasets: asia, sachs, child). This would replace the current self-referential oracle with an absolute ground truth.

2. Add a table or figure comparing the sizes of Pa(Y), Pa(Y) ∪ LCA(Pa(Y)), Pa(Y) ∪ LSCA(Pa(Y)), and the full LSCA closure on the same real-world and random graphs. This directly isolates what the recursive closure adds.

## Score and Decision

The paper makes a solid theoretical contribution: a clean, non-obvious graphical characterization of the minimal search space for single-node conditional interventions, and a linear-time algorithm to compute it. The main weaknesses are in the empirical evaluation (missing simpler baselines and a non-standard regret oracle), but these are fixable in revision and do not undermine the core theory. The theory stands on its own as a useful advance in the causal bandits literature.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>