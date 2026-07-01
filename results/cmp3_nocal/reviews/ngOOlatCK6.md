## Summary

This paper studies conditional causal bandits, where arms are conditional interventions on single nodes. It provides a graphical characterization of the minimal set of nodes guaranteed to contain the optimal intervention (the mGISS). The characterization uses the LSCA (Lowest Strict Common Ancestors) closure of the parents of the target variable, proved equivalent to a clean Λ-structure condition. The paper also proposes the C4 algorithm that computes this set in O(|V|+|E|) time, and presents experiments on random and real-world graphs.

## Strengths

- **Clean theoretical characterization (Theorems 12, 13).** The LSCA closure and its equivalence to the Λ-structure condition is an elegant characterization of the minimal search space. The refinement of standard LCA to "strict" common ancestors (which excludes paths passing through the target nodes themselves) is nontrivial and necessary, as demonstrated in Figure 1d vs. 1a. This is the paper's core intellectual contribution.

- **Clever reduction (Proposition 4).** The equivalence between conditional-intervention superiority in probabilistic SCMs and deterministic atomic-intervention superiority lets the authors reason about the simpler deterministic-atomic case while results still apply to the full conditional-intervention bandit problem. This makes the proofs tractable and is a nice theoretical bridge.

- **Linear-time algorithm (Theorem 16).** The C4 algorithm and its connector concept (Definition 14) are simple, intuitive, and achieve O(|V|+|E|) complexity — essentially optimal. The connector intuition ("if all children of V have the same connector, V is redundant") directly maps to the theoretical characterization.

- **Honest scope.** The paper is upfront about its limitations: no latent confounders, single-node interventions only, and the conditioning-set assumptions. It distinguishes itself clearly from Lee & Bareinboim (2018) (multi-node hard interventions) without overclaiming.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Bandit experiments lack discriminative controls (Section 6, Figure 3).** The bandit experiments only compare mGISS-pruned arms against the full set of nodes (brute-force). This conflates two effects: (a) a smaller arm set leads to faster convergence for any bandit algorithm, and (b) the mGISS is specifically the *right* small set. The experiment only demonstrates (a). To validate that the *specific* structure of the mGISS matters, the experiments should compare against other comparably-sized subsets (e.g., a random subset of the same size, or the set of parents Pa(Y) only, or the standard LCA set). Without such controls, the bandit results are consistent with the theory but do not empirically discriminate it from simpler pruning strategies.

- **Regret computation uses an estimated best arm (Footnote 11).** The regret is computed relative to "the arm that most runs concluded to be the best at the end of training," not the true optimal arm. If the algorithm converges to a suboptimal node, regret is underestimated. Since the bnlearn models used are Bayesian networks with known CPDs, the ground-truth optimal arm could in principle be computed; using an estimate weakens the empirical demonstration.

- **Selection of Y systematically biases pruning results toward the method's favor (Section 6).** The target Y is always chosen as "the node with the most ancestors" (with >1 parent). This maximizes the number of ancestors available for pruning and thus the apparent benefit of the method. The paper does not report results for random choices of Y or for Y chosen as a specific meaningful target variable. The reported "over 90% reduction" in some graphs is likely an upper bound; typical reductions for arbitrary Y would be lower.

- **Raw mGISS sizes not reported for real-world graphs (Section 6).** The paper states "over 90% reduction" for some graphs but does not give the actual numbers (e.g., "pathfinder: 109 ancestors, mGISS size: X"). These numbers would help readers calibrate expectations for different graphs.

### Trivial

- The paper would benefit from a small step-by-step worked example of the mGISS computation on a non-trivial graph, to bridge the formal definitions and the algorithm. This is a readability suggestion, not a substantive flaw.

## Nice-to-Haves

- Add ablation experiments comparing mGISS against (a) a random subset of nodes of the same size, (b) the set of parents Pa(Y) only, and (c) the set of standard LCAs of Pa(Y) (without the strictness condition). This would close the logical gap between the theory (which is about the *minimal* set) and the experiments (which only compare one set against the full set).
- Compute regret relative to the true optimal arm for at least one small synthetic SCM where ground truth is known, to address the estimated-best-arm concern.
- Report pruning results for multiple choices of Y (not just the node with the most ancestors) to give a more representative picture.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Criticism about the Z_X assumption being strong and not adequately contextualized.* The paper clearly states the assumption (An(X)\{X} ⊆ Z_X), explains why it is reasonable under the no-latent-confounders setting, provides examples, and notes in Footnote 3 that the results do not require all ancestors to actually be in Z_X. The limitation is adequately addressed for the paper's scope.
- *Criticism about lack of statistical significance tests.* This is a generic concern common to many empirical ML papers and does not specifically harm the paper's claims; the error bars shown in Figure 3 are standard practice.
- *Section-by-section observations that are not concrete weaknesses* (e.g., "the paper could be more precise" about the complexity comparison, "the C4 pseudocode uses An(U) without formal definition for sets"). These are either not substantive or clear from context.
- *Strength about "addressing an important problem."* This is generic and lacks specific anchoring to the paper's concrete contributions.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's core claims: the LSCA closure characterization is novel and well-motivated, the reduction via Proposition 4 is elegant, and the C4 algorithm is simple and efficient. The weaknesses lie primarily in the experimental design, which is less rigorous than the theoretical portion but does not undermine the theory.

## Suggestions

- Add ablation experiments comparing mGISS against other comparably-sized subsets in the bandit setting to empirically validate that the *specific* structure of the mGISS drives improvement, not just the reduction in arm count.
- Replace the estimated best arm with ground-truth optimal arm (or at least report the discrepancy between estimated and true optimal arm) for the regret computation.
- Report pruning results for multiple choices of Y (not just the node with the most ancestors) to give a more representative picture of expected pruning in practice.
- Include raw mGISS sizes alongside percentage reductions for the real-world graphs.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>