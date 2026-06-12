Now I have everything I need. Let me produce the final calibrated review.

**Round 1 bracket:** Based on comparisons with calibration anchors, I narrow the plausible range to **6.5–7.5**. The paper is significantly stronger in theory than the 5.0 causal-bandits anchor (which has a simple chain-graph assumption), comparable to the 7.0 causal-order paper (both are theory+algorithm contributions with supporting experiments), and weaker in experimental breadth than the 8.0 anchors but on par theoretically.

**Final score: 7.0** (between borderline accept and accept, tilted upward because the theory contribution is complete and the algorithm is provably optimal).

---

## Summary

This paper studies conditional-intervention causal bandits (single-node conditional interventions with known causal graph but unknown mechanisms/noise). It provides the first complete graphical characterization of the minimal set of nodes (mGISS) guaranteed to contain the optimal intervention node, proving it equals the LSCA closure of Pa(Y) (Theorem 13). It also contributes the C4 algorithm that computes this set in optimal O(|V|+|E|) time (Theorem 16) and an elegant Λ-structure characterization (Theorem 12). Empirical results on random and real-world graphs (bnlearn) show substantial search-space reduction (over 90% in large models) and improved regret when mGISS is used as a pre-processing step.

## Strengths

- **Complete theoretical characterization of the minimal intervention set (Theorem 13).** The paper proves that the LSCA closure of Pa(Y) is the minimal node set guaranteed to contain the optimal conditional-intervention node. This is the first full characterization for non-hard (conditional) interventions in causal bandits, going substantially beyond prior work (Lee & Bareinboim, 2018) which addressed multi-node hard interventions in a different setting. The proof structure is clearly laid out in the main text with accessible examples.

- **Proposition 4 — equivalence between conditional-intervention and deterministic atomic-intervention superiority.** This is a non-trivial bridge that reduces a probabilistic conditional-intervention problem to a simpler deterministic setting, enabling clean graphical reasoning. The equivalence is stated and motivated in Section 3; the paper then exploits it throughout to derive the mGISS characterization.

- **Elegant Λ-structure characterization (Theorem 12).** The theorem gives a clean graphical criterion: a node is in the LSCA closure iff it forms a Λ-structure over (U, U) — two node-disjoint directed paths to distinct nodes in U, intersecting only at the top. This aids both proof construction and intuitive understanding of why certain nodes must be included.

- **Linear-time C4 algorithm (Theorem 16).** The algorithm computes the mGISS in O(|V|+|E|) time using an elegant "connector" concept (Definition 14, Lemma 15). This is optimal since the input is a graph, and the connector-based reasoning is both correct and clearly explained.

- **Empirical validation of practical utility.** Testing on graphs from the bnlearn repository, the paper demonstrates that mGISS retains fewer than 10% of ancestor nodes for some of the largest models (e.g., pathfinder with 109 nodes). Bandit experiments further show that pruning to mGISS reduces cumulative regret across four real-world causal graphs.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The bandit regret evaluation would benefit from methodological clarification and stronger baselines.** The regret computation uses "the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training" (line 291). While this is a reasonable heuristic when the true optimal arm is unknown (the SCM mechanisms are not given to the algorithm), the paper does not clarify whether this estimate is computed jointly across all runs or separately per method. Additionally, the experiments compare only brute-force (all ancestors) vs. mGISS. Adding comparisons against smaller candidate sets (e.g., parents-only, or parents+LCA without closure) would strengthen the empirical connection to the theoretical minimality claim by demonstrating that removing nodes from mGISS does lose optimality in practice.

2. **The random-graph experiments measure search-space reduction but do not test whether mGISS contains the optimal intervention node.** The paper reports how much the search space shrinks (e.g., 17% of ancestors retained at degree 2) but does not specify SCMs for these random graphs to verify that the optimal node lies within mGISS. The theoretical guarantee (Theorem 13) covers correctness, but explicitly constructing counterexample SCMs where removing a node from mGISS loses the optimal intervention would strengthen the empirical story.

3. **Scope limitation: no latent confounders and full-ancestor conditioning sets.** The paper assumes no latent confounding and that An(X)\{X} ⊆ Z_X (the conditioning set includes all ancestors of X). These are clearly stated assumptions (Section 2, footnote 3), and the paper acknowledges them as limitations with latent confounding left to future work (Section 7). However, practitioners should be aware that the guarantees apply only when these assumptions hold.

### Trivial
- Parser-garbled equation formatting (e.g., `\tilde{d}o` instead of `do`) appears throughout the extracted text but the conceptual definitions remain clear.

## Nice-to-Haves
- A brief (2–3 sentence) proof sketch of the non-trivial direction of Proposition 4 in the main text would help readers assess the claim without consulting the appendix.
- A discussion of how the guarantees degrade when Z_X is smaller than An(X)\{X} would be useful for practitioners, though the paper already scopes this assumption clearly.
- Combining C4 with a more sophisticated causal bandit algorithm (rather than the simple CondIntUCB) could further demonstrate practical value; the paper acknowledges that no such algorithm currently exists.

## Removed Points

These points were raised in one or more reviews but are not included as weaknesses in the final assessment, with justifications:

1. **"Circular regret evaluation is fatal"** — The paper defines the estimated best arm as "the arm that most runs concluded to be the best at the end of training." This is a standard heuristic in empirical bandit research when ground-truth means are unknown. The claim that this is a "circular" self-fulfilling prophecy (each method voting for its own best arm) reads more into the text than is warranted. At most, the paper should clarify whether this estimate is computed jointly or per method. Downgraded from the critic's "fatal" claim to Minor weakness #1 above.

2. **"Proposition 4 proof not visible in main text"** — Deferring proofs to the appendix is standard practice. The appendix exists in the original submission; the parser strips it. This is not a paper flaw.

3. **"Z_X assumption is a methodological gap"** — The paper explicitly states the assumption and provides a footnote (line 92–93) clarifying that the results hold under this scope. The paper clearly scopes its setting; this is a design choice, not a gap. Retained only as a scope note in Minor weakness #3.

4. **"Claim that single-node is more challenging is misleading"** — The paper provides justification (lines 98): multi-node hard interventions are combinatorial in a different way. The paper explicitly states the problems are "non-comparable" (lines 39–40). The critic misread this.

5. **"Missing baselines" overclaimed as fatal** — The critic claimed the lack of parents-only/parents+LCA baselines is a major evidential issue. While adding such baselines would strengthen the paper, the core minimality claim is proven theoretically. Downgraded to Minor weakness #1.

6. **Various presentation nitpicks** (LSCA definition clarity, C4 complexity detail, specific bnlearn graph listing) — These are either already clear in the paper, trivial implementation details, or artifacts of the parser stripping the appendix. All removed per the filtering rules.

## Novel Insights

None beyond the paper's own contributions. The reviews do not uncover a conceptual insight about the paper that the paper itself does not express.

## Suggestions

1. Clarify whether the "estimated best arm" for regret computation is computed jointly across all runs or separately per method, and ideally validate against a synthetic ground-truth optimal node.
2. Add bandit experiments comparing mGISS against parents-only and parents+LCA baselines to empirically demonstrate the necessity of the full LSCA closure.
3. Provide a 2–3 sentence proof sketch of the non-trivial direction of Proposition 4 in the main text.

## Score and Decision

**Calibration anchors used:**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| "Learning Good Interventions in Causal Contextual Bandits with Adaptive Context" | 5.0 | 1 | Narrower scope (chain graphs), weaker theory; our paper is stronger |
| "Causal Bayesian Optimization with Unknown Causal Graphs" | 3.4 (controversial) | 1 | Less directly related; graph learning setting |
| "Adversarial Causal Bayesian Optimization" | 6.0 | 1 | Comparable rigor; our theory is more complete |
| "Optimal Causal Representations and the Causal Information Bottleneck" | 6.0 | 1 | Mixed reviews; our contribution is more self-contained |
| **"Deriving Causal Order from Single-Variable Interventions"** | **7.0** | 2 | **Most comparable: theory+algorithm paper with experiments. Our theory contribution is at least as strong (complete characterization vs. score-based), experiments slightly less extensive** |
| "When Selection meets Intervention" | 8.0 | 2 | Stronger across the board (theory + extensive experiments); our paper is not at this level |

**Bracket progression:** Round 1 bracketing suggested 6.5–7.5. Round 2 narrowed by confirming the paper sits slightly below the 8.0 anchors but at or slightly above the 7.0 comparable anchor, which has similar structure but less complete theory.

**Final score: 7.0**

The paper makes a genuine theoretical contribution (first complete characterization of the minimal intervention set for conditional causal bandits, an optimal linear-time algorithm, and an elegant graphical criterion), presented clearly with supporting empirical evidence. The weaknesses are minor and do not threaten the core claims. The paper is clearly above the acceptance threshold.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>