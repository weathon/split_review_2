Now I have enough information to calibrate. Let me produce the final review.

## Summary

This paper studies conditional-intervention causal bandits, where arms are conditional interventions $do(X = g(\mathbf{Z}_X))$ and the goal is to maximize expected reward of a target variable $Y$. The main contribution is a graphical characterization of the minimal set of nodes (mGISS) guaranteed to contain the optimal intervention node, computable in linear time via the C4 algorithm. The characterization uses the LSCA (lowest strict common ancestor) closure of $\text{Pa}(Y)$ and a $\Lambda$-structure condition (a node has two disjoint directed paths into $\text{Pa}(Y)$). A key enabling insight (Proposition 4) shows that conditional-intervention superiority is equivalent to deterministic atomic-intervention superiority, allowing the analysis to be carried out in a simpler deterministic setting.

## Strengths

- **Well-motivated problem with practical relevance.** The paper clearly motivates conditional interventions over hard/soft interventions with concrete real-world examples (traffic control, kidney function management in Section 2) and properly distinguishes from prior work (Lee & Bareinboim 2018 on multi-node hard interventions under latent confounders). The argument that restricting to single-node interventions makes the problem more challenging (lines 36–38) is genuinely insightful.

- **Proposition 4 is an elegant theoretical simplification.** The equivalence between conditional-intervention superiority (Definition 1) and deterministic atomic-intervention superiority (Definition 2) turns a probabilistic, policy-dependent problem into a much more tractable deterministic one. This is the key enabler for the entire graphical analysis and is a genuine insight.

- **The $\Lambda$-structure characterization (Theorem 12) is intuitive and checkable.** The LSCA-closure definition (Definitions 7–9) is technical, but Theorem 12 gives a crisp graphical condition: a node belongs to the mGISS iff it has two disjoint paths to the parents of $Y$. This is trivial to verify manually for small graphs.

- **The C4 algorithm is clean and efficient.** Linear-time ($O(|V|+|E|)$) with a simple topological-sort pass and connector propagation (Definition 14, Lemma 15, Algorithm 1). The connector concept is intuitively clear: a node whose children have multiple distinct connectors can independently influence multiple branches toward $Y$'s parents. This is the kind of algorithm that is trivially implementable.

## Weaknesses

### Major

- **No comparison against simpler baseline pruning methods.** The regret experiments (Figure 3) compare mGISS only against brute-force (all nodes). There is no comparison against simpler alternatives such as $\text{Pa}(Y)$ alone, $\text{Pa}(Y) \cup \text{LCA}(\text{Pa}(Y))$, or heuristic pruning. Without such baselines, the experiments cannot demonstrate that the full LSCA-closure machinery yields practically meaningful benefits over simpler approximations, especially for small graphs (asia: 8 nodes, sachs: 11 nodes) where the mGISS may not differ substantially from these simpler sets. This limits what the experiments can tell us about the method's practical value.

- **The regret experiments do not directly test the core theoretical claim.** The paper's headline theoretical result (Theorem 13) is that the mGISS provably contains the optimal intervention node. The regret experiments (Figure 3) only show that pruning to mGISS yields lower cumulative regret than using all nodes. However, this is a predictable consequence of reducing the number of arms — any pruning (even random elimination) would produce the same pattern. The experiments would show the same result even if the mGISS did not contain the optimal node and both methods converged to suboptimal nodes (the mGISS version just converges faster to its suboptimal node). To validate the theoretical guarantee, the experiments would need to verify directly that the optimal intervention falls within the mGISS, e.g., by constructing SCMs with known optimal interventions on the same graphs.

### Minor

- **The regret computation uses an estimated rather than ground-truth optimal arm.** Footnote 11 states: "For the computation of regret, we use the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." This is common practice in bandit experiments when the true SCM is unknown, but it means the regret comparison is not interpretable as independent validation of the mGISS's correctness — if both methods converge to the wrong node (but mGISS converges faster), the curves would still favor mGISS.

- **The worst-case nature of the guarantee is not discussed.** Definition 1 requires the same policy $g$ to work for *all* SCMs in $\mathcal{C}(G)$ simultaneously. This means the mGISS might include nodes that are only "superior" in this worst-case graph-only sense but are never actually optimal in any realistic SCM. This is an inherent property of the graph-only guarantee, but it merits explicit discussion as a limitation rather than being left implicit.

- **The assumption $\text{An}(X) \setminus \{X\} \subseteq \mathbf{Z}_X$ is practically strong.** While the paper acknowledges this in footnote 3, the practical implications are not discussed. In graphs with many ancestors, this could make the policy space enormous. It would be useful to discuss how the results might change with smaller or differently-structured $\mathbf{Z}_X$ sets.

### Trivial

None.

## Nice-to-Haves

- A correctness-validation experiment on synthetic SCMs where the true optimal intervention node is known by exhaustive search, directly verifying that the mGISS contains it.
- Comparison against simpler pruning strategies ($\text{Pa}(Y)$, $\text{Pa}(Y) \cup \text{LCA}(\text{Pa}(Y))$) to quantify the practical advantage of the full LSCA-closure machinery.
- A concrete SCM example where the optimal intervention is on a node that is an LSCA but not a standard LCA or parent, demonstrating why the extra complexity of LSCA closures is necessary.

## Removed Points

These points are flagged to be removed; treat them with caution.

- Weakness about Proposition 4 proof not being verifiable in the main text (appendix stripped by parser — the original submission contains the proof).
- Weakness about the CondIntUCB experimental algorithm being underspecified relative to theory (the theory places no restrictions on $g$ — line 96 — and the tabular approach is a reasonable experimental simplification that does not affect the mGISS guarantee).
- Formatting/style nitpicks and speculation from the Section-by-Section notes.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add baseline comparisons against simpler pruning strategies ($\text{Pa}(Y)$, $\text{Pa}(Y) \cup \text{LCA}(\text{Pa}(Y))$) in the regret experiments, and ideally also in the search-space-reduction experiments, to quantify the practical advantage of the full LSCA-closure machinery.
2. Design a correctness-validation experiment on synthetic SCMs (compatible with the causal graphs used) where the true optimal intervention node is known by exhaustive search, verifying directly that the mGISS contains it.
3. Explicitly discuss the worst-case nature of the graph-only guarantee (Definition 1 quantifies over all SCMs in $\mathcal{C}(G)$) as a limitation.
4. When possible, use ground-truth optimal arms (from known SCMs) for regret computation rather than empirically estimated best arms.

## Score and Decision

My round-1 bracket: **5.5–6.5**.

After comparing weighted items: The paper's strongest weaknesses (no baseline comparisons at -5.86, regret experiments not validating core claim at -6.80) are comparable to the most serious weaknesses in the anchor paper "Learning Good Interventions in Causal Contextual Bandits with Adaptive Context" (avg 5.00), which also had weak baselines and restrictive assumptions. However, the paper under review has substantially stronger theoretical contributions — the strength weights (+5.27, +5.03) are higher than that anchor's strongest strength (+3.96). Compared to "Adversarial Causal Bayesian Optimization" (avg 6.00), which had a -9.64 weighted novelty concern, the current paper has a cleaner, better-positioned theoretical contribution. The paper sits between these anchors: the theory is strong enough to support acceptance, but the experiments are too weak to confidently assess practical significance. I place the paper at **5.5**, reflecting that the theory is a genuine contribution but the experimental evaluation is insufficient to demonstrate practical value over simpler alternatives.

| Anchor Paper | Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|---|
| Learning Good Interventions in Causal Contextual Bandits with Adaptive Context | IPayPEGwdE.md | 5.00 | 1 | Yes | Similar experimental weaknesses (limited baselines), but weaker theory |
| Adversarial Causal Bayesian Optimization | YcW8i9VCf5.md | 6.00 | 1 | Yes | More serious novelty/positioning concerns; weaker theoretical contribution |
| Causal Bayesian Optimization with Unknown Causal Graphs | MVpvyeVeyI.md | 6.50 | 1 | Yes | Stronger overall paper with clear limitations stated |
| Fast Conditional Intervention in Algorithmic Recourse with RL | oVVLBxVmbZ.md | 5.25 | 1 | Yes | Different setting; weaker overall |
| Deriving Causal Order from Single-Variable Interventions | u63OVngeSp.md | 7.00 | 2 | Yes | Stronger experiments; comparable theoretical depth |

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>