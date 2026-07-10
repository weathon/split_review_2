Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper studies single-node conditional-intervention causal bandits, where the agent must choose both which node to intervene on and the policy (value assignment conditioned on observed context) to maximize expected reward of a target variable Y. The paper's core theoretical contribution is a graphical characterization of the minimal globally interventionally superior set (mGISS) — the minimal set of nodes guaranteed to contain the optimal conditional intervention — defined as the LSCA (Lowest Strict Common Ancestor) closure of the parents of Y. The paper proves this set equals the mGISS (Theorem 13), provides an equivalent Λ-structure characterization (Theorem 12), and proposes a linear-time algorithm C4 (Algorithm 1) to compute it. Experiments on random and real-world graphs show search space reduction, and bandit experiments demonstrate faster convergence with mGISS-pruned arm sets.

## Strengths

- **The problem framing is well-motivated and timely.** The paper convincingly argues that conditional interventions (where the intervention value depends on observed context) are significantly more realistic than hard interventions for real-world decision-making, and draws clear connections to and distinctions from existing work in causal bandits and contextual bandits (Section 7). [favorability=9.84]

- **The LSCA closure characterization and Λ-structure equivalence (Theorem 12) are theoretically elegant.** The paper defines lowest strict common ancestors (Definition 7) and proves that the LSCA closure of a set equals the set of nodes forming Λ-structures over that set. This is a clean graph-theoretic characterization that admits a linear-time algorithm. Theorem 13, equating the mGISS to the LSCA closure of the parents of Y, is the paper's core result and is structurally sound given the definitions. [favorability=9.25]

- **The C4 algorithm (Algorithm 1) is simple, intuitive, and efficient.** Running in O(|V|+|E|) time, the connector-based approach — a node is added to the mGISS precisely when its children have multiple distinct connectors — is a clean, optimal (linear in input size) solution. [favorability=8.66]

- **The paper is clearly written and well-structured.** The progression from definitions → superiority relations → graphical characterization → algorithm → experiments is logical, and the notation is consistent throughout. [favorability=10.24]

## Weaknesses

### Fatal
None.

### Major

- **The bandit experiments do not validate the paper's core claim that the mGISS contains the optimal node.** The cumulative regret comparison (Figure 3) shows that mGISS-pruned node selection converges faster than brute-force selection when both use the same CondIntUCB algorithm. However, this primarily demonstrates that a UCB algorithm with fewer arms converges faster — a foregone conclusion that holds regardless of whether the pruned set contains the true optimal arm. The paper provides no check that the node selected by brute-force search actually belongs to the mGISS. A proper validation would verify, for each dataset, whether the empirically best node lies within the mGISS. (Verified: Figure 3 and surrounding text, lines 271–297)

- **The regret computation is circular.** The "estimated best arm" is defined as "the arm that most runs concluded to be the best at the end of training" (footnote 11, line 291). Since the "best arm" is determined by the algorithm's own convergence behavior rather than a ground-truth comparison, the regret measure conflates convergence speed with optimality. The regret curves do not reliably indicate whether the mGISS-pruned algorithm approaches a genuinely better intervention. (Verified: line 291)

### Minor

- **The random graph experiments report only the fraction of nodes retained by mGISS relative to An(Y)\{Y}, with no comparison to simpler baselines** (e.g., just taking the parents of Y, or nodes at distance ≤ k from Y). Without such baselines, it is difficult to quantify how much additional pruning the LSCA closure provides beyond straightforward heuristics. (Verified: lines 263–279)

- **The experimental evaluation uses only 4 real-world datasets from bnlearn and no synthetic SCM experiments** where ground-truth optimal nodes can be verified through exhaustive computation. The paper would be substantially strengthened by synthetic SCMs with known structural assignments to directly confirm that the mGISS contains the optimal node. Additionally, the choice of target Y as "the node with the most ancestors" (line 279) may bias results toward cases where pruning is most impactful. (Verified: lines 271–297, 279–280)

- **The assumption that Z_X must contain all ancestors of X** (An(X)\{X} ⊆ Z_X, line 86) is stated as an assumption but its practical implications for settings with partial observability are not discussed as a limitation. While footnote 3 clarifies that this is not claimed to be necessary for the results, the paper would benefit from discussing how the mGISS characterization behaves when only a subset of ancestors is available. (Verified: lines 86–87, footnote 3)

### Trivial
None.

## Nice-to-Haves

- A sketch of the backward direction of Proposition 4 in the main text would increase confidence in the theoretical framework, though the full proof is in the appendix.
- Comparing the mGISS against simple baselines (parents of Y, ancestors of Y, distance-based thresholds) would help quantify the value added by the LSCA closure.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. Concern about Proposition 4 proof being in the appendix — **REMOVED** per policy: the appendix exists in the original submission but was stripped by the parser. The reviewer could not verify the proof, and the criticism is speculative.
2. Concern that "restricting to single-node interventions in fact makes the problem more challenging" (line 37–38) is stated without justification — **REMOVED**: the paper provides justification at lines 97–98, explaining that with multi-node interventions one can simply intervene on all parents of Y, whereas with single-node interventions the search space characterization is more complex when |Pa(Y)| > 1.
3. Concern about uniqueness of mGISS (Proposition 6) proof being in the appendix — **REMOVED** per policy.
4. Various formatting/style nitpicks — **REMOVED** per policy as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add synthetic-verification experiments.** Construct small SCMs with known structural assignments where the optimal intervention node is known by exhaustive computation. Verify that the empirically optimal node belongs to the mGISS, and show that mGISS-pruned CondIntUCB converges to it. This directly validates the paper's central theoretical claim.
2. **Replace the circular regret computation.** Use a ground-truth optimal intervention (determined by exhaustive evaluation or known SCM structure) rather than the "estimated best arm" defined by the algorithm's own convergence.
3. **Include ablation comparisons against simpler baselines** (e.g., parents of Y, ancestors of Y) to quantify the additional pruning benefit of the LSCA closure.
4. **Discuss the Z_X ancestor-inclusion assumption** — address what happens when practitioners cannot observe all ancestors, and whether the mGISS characterization degrades gracefully.

## Score and Decision

**Calibration anchors consulted (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| IPayPEGwdE.md — "Learning Good Interventions in Causal Contextual Bandits…" | 5.00 | R1 | Yes | Less general setup (binary interventions only); weaker theory but similar experimental limitations. My paper has stronger theory and more general setting. |
| YcW8i9VCf5.md — "Adversarial Causal Bayesian Optimization" | 6.00 | R1 | Yes | More severe framing/novelty concerns (lowest weakness favorability -4.64) but accepted. My paper has cleaner framing and clearer novelty. |
| MVpvyeVeyI.md — "Causal Bayesian Optimization with Unknown Causal Graphs" | 6.50 | R2 | Yes | High score variance (3,5,8,10) leading to rejection despite high average. Very high strength favorabilities (up to 11.70) with mild weaknesses. My paper has more severe experimental weaknesses (-1.76 vs their mildest near 6.0). |
| ZXs3pkmrRG.md — "Test-Time Learning of Causal Structure…" | 5.50 | R1 | No | Causal structure learning, less topically similar. |
| 2pEqXce0um.md — "Root Cause Analysis of Failure…" | 4.50 | R1 | No | Different sub-area. |

**Round 1 bracket:** The most topically similar papers (causal bandits with intervention selection) sit between 5.0 and 6.0. My paper's theoretical contribution is stronger than the 5.0 anchor (IPayPEGwdE) but its experimental weaknesses are more severe than the 6.0 anchor's (YcW8i9VCf5).

**Narrowing:** Comparing favorability-rated items — the paper shares with the 5.0–6.0 anchors the pattern of high-strength favorabilities (8.66–10.24) paired with at least one notably negative weakness (-1.76 from the experiments not validating the core claim). This is comparable to the -0.55 and -0.20 items in IPayPEGwdE (5.0) and the -1.99, -4.64 items in YcW8i9VCf5 (6.0). However, those anchors' most negative weaknesses relate to framing/novelty/comparison issues that question the contribution itself, whereas my paper's most negative weakness concerns experimental design — the theoretical contribution stands independently. This tilts the score slightly higher.

**Final placement:** The paper's theoretical contribution (graphical characterization of mGISS, C4 algorithm) is genuine, novel, and cleanly presented — above the typical 5.0-level paper for this topic. The experimental flaws (circular regret computation, no direct validation of the core containment claim) are real but do not undermine the theory, which is proven independent of the experiments. The paper sits above the 5.0 anchor and is comparable to the 6.0 anchor, perhaps slightly stronger on theory but weaker on experiments.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>