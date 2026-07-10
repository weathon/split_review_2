Now I have everything I need. Here is my final consolidated review.

---

## Summary

This paper introduces the problem of conditional causal bandits (single-node conditional interventions) and provides a graphical characterization of the minimal set of nodes guaranteed to contain the optimal intervention node. The key results are: (1) the LSCA (Lowest Strict Common Ancestor) closure characterization of the minimal globally interventionally superior set (mGISS), (2) a Proposition equating conditional-intervention superiority with deterministic atomic-intervention superiority, and (3) the C4 algorithm that computes the mGISS in O(|V|+|E|) time. The paper demonstrates strong pruning on real-world graphs (>90% reduction) and presents bandit regret experiments.

## Strengths

- **Elegant theoretical framing via the LSCA closure (Section 4).** The paper identifies a genuine difficulty: when only single-node interventions are allowed, the optimal node to intervene on is not simply a parent of Y, nor a lowest common ancestor of parents — it requires a recursive strict common ancestor (LSCA) closure. The Λ-structure characterization (Theorem 12) is visually intuitive and connects cleanly to the C4 algorithm. This is a real insight, not a trivial extension of existing work. [favorability=16.31]

- **The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4).** This is a clever simplification that lets the paper reason about deterministic atomic interventions while making claims about conditional interventions in probabilistic models. This theoretical bridge makes the subsequent graphical characterization genuinely usable rather than decorative. [favorability=11.83]

- **The C4 algorithm (Section 5) is clean and genuinely linear-time O(|V|+|E|).** The connector idea is well-motivated, and the reasoning about why multiple distinct child connectors imply that V belongs in the closure is sound. This is directly usable by practitioners. [favorability=14.00]

- **The paper correctly identifies its role as a pre-processing step.** Rather than proposing yet another MAB algorithm with its own regret bounds, it provides a graph-theoretic pre-processing step that can be combined with any existing or future conditional bandit algorithm. This modularity is a genuine strength. [favorability=10.16]

- **Empirical pruning results on real-world graphs are compelling.** The finding that some bnlearn models see >90% search space reduction (Section 6) is genuinely impressive and suggests practical utility. [favorability=16.01]

## Weaknesses

### Major

- **Regret computation uses an estimated best arm rather than the true optimal arm (footnote 11).** The paper defines the estimated best arm as "the arm that most runs concluded to be the best at the end of training." In a synthetic experiment where the ground-truth SCM is known to the experimenters, the true optimal arm could be computed directly. Using an estimate derived from the algorithm's own convergence conflates convergence speed with identification of the truly optimal arm — if most runs converge to the same suboptimal arm (which is plausible when pruning helps convergence but the underlying bandit algorithm is imperfect), the regret will appear near zero even when the algorithm is suboptimal. This weakens the specific claim in the abstract that mGISS "substantially accelerates convergence rates when integrated into standard multi-armed bandit algorithms." The core theoretical contribution is unaffected, but this is a real methodological flaw in the regret experiments. [favorability=5.60]

### Minor

- **The bandit regret experiments lack alternative baseline comparisons.** The paper compares brute-force (all ancestor nodes) vs. mGISS-pruned nodes, but no comparison with simpler heuristic pruning strategies (e.g., parents-only, parents + LSCA without the full closure). While mGISS is theoretically minimal, the empirical question of how much smaller it is than reasonable heuristic alternatives would strengthen the evaluation. Without such baselines, the regret experiments primarily confirm that reducing arm count helps — which is expected from first principles. [favorability=1.06]

- **The paper does not explain how bnlearn Bayesian networks were converted to SCMs for the regret experiments.** bnlearn models are typically Bayesian networks (graph + CPTs), but the causal bandit framework assumes structural assignments with noise distributions. For the pruning experiments only the graph structure is needed. But the regret experiments require simulating an SCM, and the conversion process is not described, making these experiments difficult to reproduce or interpret. [favorability=4.62]

- **The random-graph experiments select Y as "the node with the most ancestors" (Section 6), which is a favorable heuristic.** This choice maximizes the potential pruning fraction. A more robust evaluation would average over multiple target nodes per graph, or report variance across different choices of Y. [favorability=5.96]

- **The regret experiments are conducted on only 4 datasets where both An(Y) and mGISS are "sufficiently small to allow experimentation."** This selection bias limits the generality of the regret findings — the graphs where pruning matters most (large ones) are excluded from the bandit evaluation. [favorability=4.25]

### Trivial

- **Proposition 4 is stated without a proof sketch in the main text.** The proof is deferred to the appendix; a brief sketch of why the equivalence holds would help readers assess its plausibility without consulting the appendix. [favorability=6.08]

- **The C4 algorithm's O(|V|+|E|) claim is stated without explaining how ancestor computation (An(U)) is achieved within that bound.** This is standard practice but worth a brief note. [favorability=4.85]

## Nice-to-Haves

- Add confidence intervals or error bars on the pruning fractions for random-graph experiments (1000 graphs per configuration).
- Include a brief pseudocode or formal description of CondIntUCB to aid reproducibility — the prose description referencing Lattimore & Szepesvári (2020, §18.1) is sufficient but a formal summary would help.
- Discuss how the mGISS characterization changes when Z_X is restricted to a proper subset of the ancestors (rather than containing all ancestors) — this would increase practical relevance for settings where only some ancestors are observable.

## Removed Points

These points were raised in the input review but removed after verification against the paper:

1. **"More challenging" claim is overstated**: The paper justifies why single-node interventions make the search-space characterization more complex than multi-node (where you can intervene on all parents at once) and explicitly states the problems are "fundamentally different and non-comparable." The claim is reasonable in context. REMOVED.

2. **Z_X assumption limits applicability**: The paper clearly states the assumption An(X)\{X\} ⊆ Z_X, defends it in footnote 3 ("we can always include them in Z_X under the assumptions of our problem"), and positions it as a scope choice. This is not a weakness but a deliberate problem framing. REMOVED.

3. **Condition Z_W ⊆ Z_X not formally justified**: The paper provides two real-world examples (train delays, doctor example) motivating this condition. Whether necessary or a convenience, it is an assumption of the framework. REMOVED.

4. **LSCA "strict" variant not sufficiently explained**: The paper explicitly explains why LCA fails for Figure 1d and motivates the need for the stricter LSCA definition. REMOVED.

5. **Missing discussion of C4 vs standard DAG algorithms**: The algorithmic contribution stands on its own; this comparison is not necessary. REMOVED.

6. **Paper does not address how practitioners determine Z_X in practice**: This is outside the paper's stated scope — the paper assumes Z_X is pre-specified. REMOVED.

7. **Statistical significance not reported**: For 1000 random graphs the trends are visually clear; confidence intervals would be a nice addition but are not necessary. DEMOTED to Nice-to-Have.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Fix the regret computation to use the true optimal arm derived from the ground-truth SCM parameters (which the experimenters control since they are simulating), rather than an estimated best arm based on the algorithm's own convergence.
- Add at least one simpler baseline pruning strategy (e.g., parents-only, or parents + LSCA without the recursive closure) to the pruning fraction and regret experiments to contextualize the additional reduction provided by the full LSCA closure.
- Explain how the bnlearn models were converted to SCMs for the regret experiments, or clarify that only the graph structures were used and the SCMs were constructed independently.
- Average over multiple choices of target node Y when reporting pruning fractions on random graphs.
- Include a brief proof sketch for Proposition 4 in the main text.

## Score and Decision

**Round 1 (Bracketing) Anchors:**
| Path | Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| /home/.../Uj0h13lVrR.md | 1.00 | R1 | No | Far weaker — fundamentally flawed GFlowNet paper |
| /home/.../5lUdTogEL3.md | 1.00 | R1 | No | Unrelated person re-id paper |
| /home/.../MVpvyeVeyI.md | 3.40 | R1 | No | Causal BO with unknown graphs — weaker theory, no algorithm |
| /home/.../fSxiromxAq.md | 3.00 | R1 | No | Causal discovery paper with thin theory |
| /home/.../IPayPEGwdE.md | 5.00 | R1 | Yes | Causal contextual bandits — restrictive assumptions, thinner theory |
| /home/.../YcW8i9VCf5.md | 6.00 | R1 | Yes | Adversarial CBO — regret bounds but questionable novelty relative to prior work |
| /home/.../qac43AwuL9.md | 6.00 | R1 | No | Causal information bottleneck — mixed reviews, rejected |
| /home/.../u63OVngeSp.md | 7.00 | R1 | Yes | Causal order from interventions — similar theoretical profile with stronger experiments |
| /home/.../Bp0HBaMNRl.md | 6.75 | R2 | No | Differentiable causal discovery — different methodology |
| /home/.../SKulT2VX9p.md | 6.67 | R2 | No | Interventional fairness — different subfield |
| /home/.../9vTAkJ9Tik.md | 7.00 | R2 | No | Doubly robust identification — different problem |

**Round-1 Bracket:** 5.5 – 7.0 (placed this paper above IPayPEGwdE/5.0 and slightly below u63OVngeSp/7.0)

**Narrowing Analysis:** The paper's strengths (favorability 10.16–16.31) are comparable to u63OVngeSp's strongest items (favorability 9.88–14.15), with the theoretical contribution actually cleaner since the mGISS characterization is exact rather than approximate. However, the paper's most damaging weakness — the estimated-best-arm flaw in regret computation (favorability 5.60) — is a real methodological problem absent from u63OVngeSp's weaknesses. The regret experiments in the current paper are less convincing than u63's empirical validation, which pulls the score below 7.0. Compared to YcW8i9VCf5 (6.00), the paper under review has clearer novelty but a more significant experimental flaw, landing at a similar overall level.

**Final Score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>