Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper studies the conditional causal bandit problem, where arms are single-node conditional interventions (rather than hard multi-node interventions). The main contributions are: (1) a graphical characterization showing that the minimal set of nodes guaranteed to contain the optimal conditional intervention equals the LSCA (lowest strict common ancestor) closure of the parents of the target variable Y; (2) a characterization of this closure in terms of Λ-structures; (3) the C4 algorithm, which computes this set in linear O(|V|+|E|) time; and (4) empirical validation of search-space reduction on synthetic and real-world graphs.

## Strengths

- **Clean conceptual framing.** The paper identifies a genuine gap: existing work on search-space reduction for causal bandits (Lee & Bareinboim, 2018) handles multi-node hard interventions; the single-node conditional-intervention case is both practically relevant and theoretically distinct. The core claim — that the mGISS equals the LSCA closure of Pa(Y) — is non-trivial and well-motivated through worked examples.

- **Proposition 4 (equivalence of conditional-intervention superiority and deterministic atomic-intervention superiority) is a clever theoretical maneuver** that connects a probabilistic, policy-based problem to a deterministic, value-based one, making the subsequent graphical characterization tractable.

- **The Λ-structure characterization (Theorem 12) is elegant.** Reducing the LSCA closure to the set of nodes that form Λ-structures over (U, U) provides clean visual intuition that matches the algorithmic implementation (connectors with multiple children).

- **The C4 algorithm is genuinely simple and linear-time** O(|V|+|E|), which is optimal in the sense that the input must be read. The connector mechanism provides intuitive explanation for why certain nodes are retained or pruned.

- **The empirical evaluation of search-space reduction is honest and appropriately scoped.** The paper reports what fraction of ancestor nodes are retained, and shows that sparser graphs benefit more. Real-world graphs from bnlearn showing over 90% reduction for large models are genuinely impressive.

## Weaknesses

### Fatal
None.

### Major

1. **The bandit regret experiment has methodological gaps that weaken the empirical support for the central claim.** The regret is computed against an "estimated best arm" (the arm that most runs concluded to be best at end of training) rather than a ground-truth optimal node. This introduces potential circularity: if the mGISS-restricted and brute-force runs converge to different nodes, the consensus-based estimate could be biased. Additionally, the experiments compare mGISS only against brute-force (all nodes). Since any reduction in arms reduces regret as long as the optimal arm is preserved, the comparison primarily validates that mGISS pruning doesn't destroy performance — not that the specific mGISS pruning is better than alternative strategies (e.g., pruning to Pa(Y) only, or a random subset of the same cardinality). The paper would be strengthened by verifying whether the truly optimal node (which could be approximated via the known CPDs of bnlearn models) lies within the mGISS for the datasets used.

2. **The LSCA definition and the motivation for the recursive closure need sharper justification in the main text.** The paper introduces the LSCA because the standard LCA fails for Figure 1d, but the heuristic argument for why the *recursive* closure (rather than a single-pass LSCA computation) is needed is thin — it is presented as an observation ("the reasoning for testing the lowest strict common ancestors of the parents can be repeated") rather than a fully justified claim. While the formal proof is in the appendix, the main text's intuition gap leaves a disconnect between the heuristic examples and Theorem 13.

### Minor

3. **The algorithm's linear-time claim is not fully discussed.** The algorithm requires computing Ch(V) ∩ An(U) for each node. Checking whether a child is in An(U) requires either precomputed ancestor information or repeated traversal. The paper claims O(|V|+|E|) time but does not discuss how An(U) is represented or computed. This is a minor implementation-level omission.

4. **Bandit experiment details are sparse.** The paper does not report the number of rounds per run, the range of values each node can take, or how reward distributions are simulated from the bnlearn models. These details are needed to assess reproducibility of the regret experiments.

### Trivial
None.

## Nice-to-Haves

- In the regret experiments, verify whether the truly optimal node (obtainable from the bnlearn models' known CPDs, at least approximately) lies within the mGISS. This would directly substantiate the paper's central theoretical claim.
- Add at least one alternative pruning baseline to the bandit experiments, such as pruning to Pa(Y) only or a random subset of the same size as the mGISS.
- Provide more details about the bandit experimental setup (number of rounds, value ranges, reward simulation procedure) in the main text or appendix.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "The assumption that An(X)\{X} ⊆ Z_X is stronger than the paper's framing acknowledges." — The paper explicitly states this assumption and addresses it in Footnote 3. It is a clearly stated modeling assumption, not an oversight.
- "The nesting condition (W ∈ An(X) ⇒ Z_W ⊆ Z_X) is not used again." — This condition is part of the definition of "observable conditioning set" used in Definition 1.
- "No discussion of how to choose Y when the target variable is not pre-specified." — The paper assumes Y is given, which is standard in causal bandits.
- "The paper does not address what changes when Y has zero parents." — Proposition 6 explicitly requires Y to have "at least one parent"; the case is scoped out.
- "The claim that 'no such algorithm currently exists' seems overstated." — In context, the paper refers to causal bandit algorithms that additionally leverage causal structure beyond node-pruning, which is a reasonable statement about the literature.
- "The paper claims the setting is 'widely applicable' but does not return to examples." — Examples are given in Section 2 (traffic controller, doctor/kidney function).
- Various formatting/style nitpicks — These are parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- In the regret experiments, replace the "estimated best arm" with a verification step that checks whether the optimal node (approximated from known CPDs) falls within the mGISS.
- Compare mGISS against at least one alternative pruning strategy (e.g., pruning to Pa(Y) only) in the bandit experiments.
- Add a brief discussion in Section 5 of how An(U) is precomputed and represented to support the linear-time claim.
- Expand the intuition in Section 4 explaining why the *recursive* closure (not just a single LSCA pass) is needed.

## Score and Decision

**Calibration anchors used:**
| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Learning Good Interventions in Causal Contextual Bandits with Adaptive Context | IPayPEGwdE.md | 5.00 | R1 | Yes | Topically similar; paper under review has stronger strength weights (8-11 vs 7-9) and similar weakness profiles |
| Adversarial Causal Bayesian Optimization | YcW8i9VCf5.md | 6.00 | R1/R2 | Yes | Comparable strength weights; paper under review has fewer damaging weaknesses |
| Optimal Causal Representations / CIB | qac43AwuL9.md | 6.00 | R1 | Yes | Mixed reviews; paper under review is more consistent |
| Deriving Causal Order from Single-Variable Interventions | u63OVngeSp.md | 7.00 | R2 | Yes | Similar top strength weights (~10); paper under review has fewer and milder weaknesses |
| When Selection meets Intervention | xByvdb3DCm.md | 8.00 | R1 | Yes | Clearly above paper under review in both theoretical depth and experimental breadth |

**Bracket determination:**
- **Round 1 bracket:** 6.0 – 7.5. The paper's strength weights (8.14–10.88) substantially exceed those of the 5.0 anchor and match/lightly exceed the 6.0 and 7.0 anchors. The paper is clearly below the 8.0 anchor which has both stronger theory exposition and more comprehensive experiments.
- **Round 2 narrowing:** Compared against the 7.0 anchor ("Deriving Causal Order"), the paper under review has comparable strength-weight peaks (~10) but its empirical validation is less comprehensive (only search-space reduction + one bandit comparison vs. thorough benchmarking across multiple baselines). The most damaging weakness weight (6.79, a minor implementation detail) does not threaten the core contribution. Therefore the paper sits at the lower end of the bracket.

**Final score: 6.5.** The paper has a clean, non-trivial theoretical contribution (mGISS characterization, Λ-structures, C4 algorithm) with high-weighted strengths. Its weaknesses are addressable in revision — the regret experiment methodology can be improved and the intuition section can be expanded — without undermining the core theoretical results.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>