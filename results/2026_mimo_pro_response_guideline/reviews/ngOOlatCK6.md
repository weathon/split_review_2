Now I have enough data for calibration. Let me synthesize everything into the final review.

**Calibration summary:**
- IPayPEGwdE.md (5.00, Reject): Causal contextual bandits — weaker theory, limited experiments. Paper under review is substantially stronger.
- oVVLBxVmbZ.md (5.25, Reject): Conditional intervention for recourse — less theoretical depth. Paper under review is stronger.
- YcW8i9VCf5.md (6.00, Accept): Adversarial causal BO — comparable quality, different focus.
- u63OVngeSp.md (7.00, Accept): Causal order from interventions — very comparable: strong theory + clean algorithm + experiments. Best anchor.
- M0xK8nPGvt.md (7.50, Accept): Causal graph priors for RL — novel + regret analysis + experiments. Slightly above.
- xByvdb3DCm.md (8.00, Accept): All 8s, very strong. Paper under review is below this level.

**Bracket: 6.5–7.5. Final score: 7.0.** The paper's theoretical contribution (complete characterization + surprising equivalence + optimal algorithm) is clean and self-contained, comparable to u63OVngeSp. The experiments are adequate proof-of-concept for a primarily theoretical paper. The missing random-pruning baseline is a gap in empirical demonstration but not in the core contribution.

## Summary
This paper introduces conditional causal bandits, where arms correspond to conditional interventions do(X = g(Z_X)), and provides a complete graphical characterization of the minimal set of nodes guaranteed to contain the optimal intervention target — the mGISS, shown to equal the LSCA closure of Pa(Y). The C4 algorithm computes this set in O(|V|+|E|) time, and Proposition 4 establishes a surprising equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority.

## Strengths
- **Surprising equivalence between conditional and deterministic atomic superiority (Proposition 4, Section 3):** The proof that these two superiority relations coincide is non-trivial: conditional interventions are strictly more expressive than atomic interventions, so one would naively expect the orderings to differ. This equivalence is the key bridge enabling the entire graphical characterization via the simpler deterministic setting, and means the mGISS characterization applies simultaneously to two intervention paradigms.
- **Elegant graphical characterization via Λ-structures (Theorems 12, 13, Section 4):** The recursive LSCA closure (Definition 9) is collapsed into a single structural condition: a node belongs to the closure iff it forms a Λ-structure over (Pa(Y), Pa(Y)). Theorem 13 proves this closure equals the mGISS, completing the characterization.
- **Optimal-time C4 algorithm (Algorithm 1, Definition 14, Lemma 15, Theorem 16, Section 5):** The connector abstraction translates the recursive closure computation into a single reverse-topological-order pass achieving O(|V|+|E|) time — asymptotically optimal since the graph itself has that size.
- **Substantial search-space reduction on real-world graphs (Section 6):** For random graphs with 500 nodes and expected degree 2, mGISS retains only 17% of ancestors on average. For real-world bnlearn graphs, reductions exceed 90% for the largest models.
- **Demonstrated impact on cumulative regret (Section 6, Figure 3):** The CondIntUCB algorithm with mGISS pruning shows strictly lower cumulative regret on four bnlearn datasets, averaging over 300–500 runs, with the effect most pronounced for the larger pathfinder graph (109 nodes).

## Weaknesses

### Fatal
None

### Major
- **Bandit experiment conflates "fewer arms" with "correctly pruned arms" (Section 6, Figure 3):** The bandit experiment compares UCB convergence with mGISS pruning vs. brute-force (all ancestors of Y). This comparison conflates two effects: (a) having fewer arms leads to faster convergence for any MAB algorithm, and (b) the specific arms retained by mGISS include the optimal one. No baseline of random pruning to the same number of arms as mGISS is included. While the theory guarantees correctness (point b), the experiment is supposed to demonstrate *practical value*, and a random-pruning baseline would cleanly establish that the specific pruning matters. This is a methodological gap in the empirical demonstration, not in the theory itself.

### Minor
- **Limited bandit experiment scope (Section 6):** The bandit experiments use only 4 bnlearn datasets (asia, sachs, child, pathfinder), while the search space reduction experiments cover many more graphs. Standard deviations are plotted in Figure 3 (line 281: "plot the two average cumulative regret curves along with their standard deviations") but are not discussed or accompanied by statistical tests.
- **Choice of Y biases toward large ancestor sets (Section 6):** Setting Y to be the node with most ancestors (footnote 8) biases toward nodes with large An(Y) sets, potentially making pruning appear more effective than typical cases.

### Trivial
None

## Nice-to-Haves
- The experiments would benefit from more diverse graph topologies beyond Erdős-Rényi (e.g., scale-free, small-world).
- A brief discussion of how graph uncertainty affects pruning tightness (beyond the mention of applying C4 to candidate graphs and taking unions) would connect to practical deployment.
- A complexity comparison of mGISS size relative to |An(Y)| as a function of graph properties (beyond expected degree) would deepen understanding of when the method is most useful.

## Removed Points
These points are flagged to be removed, treat them with caution.
- The harsh critic's claim that the paper "lacks quantified error bars in the text" is partially incorrect: the paper explicitly states standard deviations are plotted in Figure 3 (line 281). The concern about limited scope and lack of statistical tests is valid.
- The Strength Finder's claims about "honest and precise positioning relative to prior work" and "clear and well-motivated problem formulation" are generic and lack specific citation grounding — they describe good practice rather than concrete contributions.

## Novel Insights
The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4) is a genuinely novel insight. Since conditional interventions are strictly more expressive than atomic interventions, one would expect the superiority orderings to potentially differ. The fact that they coincide means the entire graphical characterization applies simultaneously to two different intervention paradigms, and allows the simpler deterministic setting to serve as a proving ground for results in the more general conditional setting. This is a non-obvious structural result that simplifies the entire development and has independent theoretical interest.

## Suggestions
- **Add a random-pruning baseline to the bandit experiment:** Prune random subsets of An(Y)\{Y} down to |mGISS| nodes and show this leads to worse regret. This cleanly separates the "fewer arms" effect from the "correctly pruned" effect and would make the practical contribution much more compelling.
- **Report the fraction of runs where the best node is included in the pruned set** for both random pruning and mGISS, directly validating the theoretical guarantee empirically.
- **Briefly discuss practical implications of conditioning set size** — how mGISS interacts with the difficulty of the contextual bandit problem per node.

## Reporting

**Anchors retrieved across all rounds:**

Round 1:
| Path | Avg Score | Band |
|------|-----------|------|
| Uj0h13lVrR.md | 1.00 | <1.5 |
| bEgDEyy2Yk.md | 1.00 | <1.5 |
| nSDOkm0SKo.md | 1.00 | <1.5 |
| 5kMwiMnUip.md | 1.40 | <1.5 |
| MVpvyeVeyI.md | 3.40 | 1.5–3.5 |
| fSxiromxAq.md | 3.00 | 1.5–3.5 |
| AvXrppAS2o.md | 3.00 | 1.5–3.5 |
| JzFLBOFMZ2.md | 3.20 | 1.5–3.5 |
| IPayPEGwdE.md | 5.00 | 3.5–5.5 |
| oVVLBxVmbZ.md | 5.25 | 3.5–5.5 |
| fcl6WeMARK.md | 4.33 | 3.5–5.5 |
| xA8WW2dlTX.md | 4.40 | 3.5–5.5 |
| YcW8i9VCf5.md | 6.00 | 5.5–7.5 |
| u63OVngeSp.md | 7.00 | 5.5–7.5 |
| pOoKI3ouv1.md | 5.75 | 5.5–7.5 |
| nmvmPIi185.md | 6.25 | 5.5–7.5 |
| xByvdb3DCm.md | 8.00 | 7.5–8.5 |
| 3cuJwmPxXj.md | 8.00 | 7.5–8.5 |
| A3YUPeJTNR.md | 8.00 | 7.5–8.5 |
| DzGe40glxs.md | 8.00 | 7.5–8.5 |

Round 2:
| Path | Avg Score | Band |
|------|-----------|------|
| u63OVngeSp.md | 7.00 | 5.5–7.5 |
| BZYIEw4mcY.md | 6.00 | 5.5–7.5 |
| fGhr39bqZa.md | 6.00 | 5.5–7.5 |
| qac43AwuL9.md | 6.00 | 5.5–7.5 |
| u63OVngeSp.md | 7.00 | 6.0–8.0 |
| mGmx41FTTy.md | 6.33 | 6.0–8.0 |
| qlzxeNESWI.md | 6.50 | 6.0–8.0 |
| M0xK8nPGvt.md | 7.50 | 6.0–8.0 |

**Bracket (Round 1):** 6.0–7.5. The paper under review has stronger theory than the causal bandits papers at 5.0–5.25, comparable to u63OVngeSp (7.00), and slightly below xByvdb3DCm (8.00).

**Narrowing (Round 2):** The most comparable paper is u63OVngeSp (7.00), which also has a strong theoretical contribution (interventional faithfulness + Intersort algorithm) with empirical validation. The paper under review's theory is arguably cleaner (complete characterization + surprising equivalence + optimal algorithm), but its experiments are more limited. M0xK8nPGvt (7.50) has more comprehensive experiments and a regret analysis, placing it slightly above.

**Final score: 7.0.** Matches u63OVngeSp: strong, clean theoretical contribution with adequate empirical proof-of-concept. The core theory (Proposition 4, Theorems 12/13, C4) is a complete and novel contribution to the causal bandits literature. The main weakness (missing random-pruning baseline) is a gap in empirical demonstration that could be addressed but does not undermine the theoretical results.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>