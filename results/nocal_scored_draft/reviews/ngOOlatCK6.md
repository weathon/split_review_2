Now I have the full paper text and the favorability scores from the draft tool. Let me finalize the review.

The favorability scores are informative:
- All four strengths score 1.00 — genuinely strong
- The two major weaknesses score 0.00 — genuinely damaging to the experimental claims
- The pruning-fractions-relative-only item scores 0.71 — the model reads this as not really a weakness (and rightly so, since fraction of ancestors is the relevant metric and absolute numbers appear in the figure captions)

I'll remove the pruning-fractions item and the Erdos-Renyi item (the latter is already partially addressed by the real-graph experiments and not a core concern).

---

## Summary

This paper introduces the conditional causal bandit problem (single-node conditional interventions, known causal graph, unknown SCM parameters) and provides a complete graphical characterization of the minimal set of nodes guaranteed to contain the optimal intervention node (the mGISS). The mGISS is shown to be the LSCA (Lowest Strict Common Ancestor) closure of the parents of the target node Y, equivalently characterized via Λ-structures. The paper also contributes the C4 algorithm, which computes this closure in O(|V|+|E|) time. The theoretical core is novel, well-constructed, and represents a genuine advance in the causal bandits literature.

## Strengths

- **Novel theoretical characterization.** Theorem 13 (LSCA closure = mGISS) together with the Λ-structure characterization (Theorem 12) provides a clean, non-trivial graphical criterion for the minimal node set guaranteed to contain the optimal conditional intervention. The uniqueness of the mGISS (Proposition 6) ensures the framework is well-defined. This is a genuine theoretical advance in the causal bandits literature.

- **Elegant reduction.** Proposition 4 shows equivalence between conditional-intervention superiority in probabilistic SCMs and atomic-intervention superiority in deterministic SCMs. This is non-obvious and provides real analytical traction throughout the proofs.

- **Linear-time algorithm.** The C4 algorithm runs in O(|V|+|E|) and the connector mechanism is a clever way to compute the LSCA closure without explicit iterative construction. The correctness argument via Lemma 15 is intuitive.

- **Clear problem framing.** The paper properly defines the conditional causal bandit problem, distinguishes it from contextual bandits and from prior causal bandit formulations, and is honest about its scope (single-node interventions, no latent confounders).

## Weaknesses

### Major

- **Regret measured against estimated (not ground-truth) best arm.** Footnote 11 states that regret uses "the arm that most runs concluded to be the best at the end of training." Since the true optimal arm is not determined from the SCM but estimated from the same experimental data used to evaluate regret, this introduces optimism bias. The mGISS setting has strictly fewer arms, making its best-arm estimate potentially more reliable than the brute-force setting, which structurally favors the pruned method. The regret curves therefore cannot be interpreted as unbiased comparisons. Since the bnlearn datasets have known conditional probability tables, the ground-truth optimal intervention could have been computed, making this an avoidable methodological flaw.

- **Systematic selection bias in target node choice.** In all experiments (random graphs, real-world graphs, and bandit regret), the target Y is always chosen as the node with the most ancestors. This maximizes the pool of ancestors available for pruning and thus the apparent benefit of the method. The paper does not vary the target node per graph or report a distribution of pruning fractions across different target nodes, making it unclear whether typical (rather than best-case) performance matches the reported results. Footnote 8 excludes the trivial one-parent case but does not justify always picking the maximally favorable node.

### Minor

- **Single-algorithm evidence for regret benefits.** The regret experiments only test one bandit algorithm (CondIntUCB, a UCB-per-context construction). The abstract claims that pruning "accelerates convergence rates when integrated into standard multi-armed bandit algorithms" — a plural claim that is not fully evidenced without testing at least one additional base algorithm (e.g., Thompson sampling). The paired comparison (same algorithm, pruned vs. unpruned nodes) is valid as a proof of concept, but the broader claim is not fully supported.

## Nice-to-Haves

- The observable conditioning set monotonicity assumption (W∈An(X) ⇒ Z_W⊆Z_X) could be discussed further: how would violation affect the theoretical guarantees?
- The worst-case nature of the mGISS guarantee (it must hold for *all* SCMs consistent with G, making it conservative for any specific SCM) could be discussed more explicitly — noting that for a given SCM, more aggressive pruning may be possible.
- Repeating the regret experiments with another base algorithm (e.g., Thompson sampling for node selection) would strengthen the claim about accelerating "standard MAB algorithms."
- Reporting absolute (not just relative) node counts for all datasets in the main text would improve practical interpretability.

## Removed Points

- The claim that "the paper does not explicitly state the C4(G, Pa(Y)) step in the experiments" — **removed as factually wrong**: line 263 explicitly states "used C4 to compute L^∞(Pa(Y)) = mGISS_Y(G)."
- Presentation preferences about definition walkthrough — **removed** as style nitpicks.
- Terminology concerns about "conditional causal bandit" — **removed** as speculative; the paper clearly defines its terms.
- Request to report pruning fractions relative to full node set — **removed** because the fraction of the ancestor set is the relevant metric (nodes outside An(Y) cannot affect Y), and absolute counts appear in Figure 3 captions.
- The Erdos-Renyi graph concern — **removed** because the paper already partially addresses this with real-world graph experiments, and the concern is about the generality of an illustrative experiment, not a core flaw.

## Novel Insights

Beyond the paper's own contributions, the main insight surfaced by the review process is the interaction between the estimated-best-arm regret computation and the asymmetric arm counts of the two conditions being compared. This is an experimental design critique rather than a novel scientific insight about the paper's subject matter.

## Suggestions

1. **Fix the regret evaluation.** Construct synthetic SCMs with known structural equations and noise distributions (e.g., linear Gaussian or discrete Bayesian networks with known CPDs) so the ground-truth optimal intervention can be computed by exhaustive enumeration over the known model, and regret can be measured against this ground truth.
2. **Vary the target node.** For each graph, repeat the search space reduction experiment for every node Y with at least two parents and report the distribution (not just the maximum) of pruning fractions.
3. **Test at least one additional base algorithm** (e.g., Thompson sampling for node selection) to support the claim that pruning benefits "standard multi-armed bandit algorithms" more generally.

## Score and Decision

The theoretical contribution — the graphical characterization of the mGISS, the equivalence in Proposition 4, and the C4 algorithm — is genuine, well-constructed, and independently valuable. These results are the paper's primary contribution and they are sound. The experimental evaluation has methodological flaws (estimated-best-arm regret, systematic target-node selection bias) that undermine the empirical claims in their current form, but these do not invalidate the theory, and they are fixable. On balance, the paper merits acceptance on the strength of its theoretical contributions, with the expectation that the experimental issues will be corrected in the final version.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>