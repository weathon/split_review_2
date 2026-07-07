Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper studies conditional causal bandits, where arms are single-node conditional interventions (the intervention value depends on observed context). The main contribution is a graphical characterization of the **minimal set of nodes** guaranteed to contain the optimal conditional intervention node. The authors prove that this minimal set (mGISS) equals the LSCA (Lowest Strict Common Ancestors) closure of the parents of the target variable Y (Theorem 13), provide an equivalent Λ-structure characterization (Theorem 12), and propose a linear-time O(|V|+|E|) algorithm (C4) to compute it. An elegant reduction (Proposition 4) connects conditional-intervention superiority to deterministic atomic-intervention superiority, simplifying the analysis.

## Strengths

- **Elegant theoretical reduction (Proposition 4).** The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority is a clever result that significantly simplifies the analysis, letting the authors reason about a simpler setting while making claims about a richer one. This result is well-proven and non-trivial.

- **Novel and non-trivial graphical characterization (Theorems 12, 13).** The mGISS as the LSCA closure of Pa(Y) is genuinely novel. The LSCA notion (Definition 7) is a natural refinement of standard LCA that correctly handles the single-node intervention constraint — the failure of LCA shown in Figure 1d demonstrates why this refinement is necessary, and the proof that the LSCA closure is the minimal set is convincing.

- **Clear problem framing and positioning.** The paper correctly identifies that conditional interventions are more realistic than hard interventions in many decision-making settings, and carefully distinguishes conditional causal bandits from both contextual bandits (Section 7) and prior multi-node hard-intervention causal bandits (Lee & Bareinboim, 2018).

- **Linear-time algorithm (C4).** Algorithm 1 is simple, intuitive (connector propagation in reverse topological order), and achieves O(|V|+|E|) complexity. This is a practical contribution — a practitioner can run this as a pre-processing step on any causal DAG.

- **Empirical pruning results on real-world graphs.** The reduction of over 90% of the search space on some large bnlearn graphs (Section 6) is striking and suggests genuine practical utility.

## Weaknesses

### Fatal
None.

### Major

**Missing baselines in experimental evaluation (Section 6).** The experiments compare mGISS only against brute-force (all ancestors of Y), providing no evidence that the *specific* LSCA characterization is more effective than simpler alternatives. Several natural baselines are absent:

1. **Just the parents Pa(Y):** In the multi-node hard-intervention setting (Lee & Bareinboim, 2018), Pa(Y) is the answer. Comparing Pa(Y) size vs mGISS size would reveal how much larger the mGISS actually is. If mGISS is essentially Pa(Y) plus a few nodes in most real graphs, the contribution is incremental; if substantially larger, that is an interesting finding — but the paper provides neither comparison.

2. **The LCA closure (without the "strict" condition):** The paper shows one counterexample (Figure 1d) where LCA fails and LSCA is needed, but never quantifies how often these two closures differ on real graphs. This makes it impossible to assess whether the LSCA refinement is a theoretical nicety or a practical necessity.

Without these comparisons, the experiments demonstrate that mGISS is smaller than *all ancestors*, but do not establish that the *specific theoretical characterization* yields practical benefits beyond what simpler heuristics would achieve. This is the most significant weakness in the paper.

### Minor

- **No empirical validation of the containment claim (Section 6).** The paper's core theoretical claim — that the mGISS is guaranteed to contain the optimal node — is never directly validated empirically. For the bnlearn models, which include full conditional probability distributions, one could enumerate interventions to compute the true optimal node and verify it falls within the mGISS. This would provide direct empirical support for the theoretical result. While the theory is proved in the appendix, direct empirical validation would substantially strengthen the paper.

- **Bandit regret uses estimated best arm rather than true optimal (footnote 11).** The regret computation uses "the arm that most runs concluded to be the best at the end of training" as the optimal reference. Both the mGISS and brute-force methods are evaluated against the *same* estimated standard (so the comparison is fair between methods), but the bnlearn models include full CPDs from which the true optimal intervention is computable. Using the true optimal would provide stronger, more absolute evidence for the convergence claims.

- **Only one bandit algorithm tested (CondIntUCB).** The paper uses only a simple per-context UCB algorithm. While the authors acknowledge this limitation and note that no existing causal bandit algorithm handles conditional interventions, the generality of the empirical convergence claims remains limited. A discussion of how different bandit algorithms might interact with mGISS pruning would strengthen the presentation.

- **No statistical significance testing for regret curves (Figure 3).** Given the overlapping standard deviation bars in the asia and sachs plots, it is unclear whether the observed differences between mGISS and brute-force are statistically significant.

- **Random graph experiments use only Erdős-Rényi DAGs.** This is a standard model but generates graphs with different structural properties from real causal graphs (e.g., different expected path lengths). Results on additional graph families (e.g., scale-free) would strengthen the generality claims.

### Trivial

- **C4 algorithm complexity clarification (Algorithm 1).** Step 6 uses An(U) (ancestors of the input set U). The paper should explicitly state whether this precomputation is included in the O(|V|+|E|) complexity claim, though it can be using a reverse traversal.

- **Node reduction vs arm reduction.** The paper reports reduction in the number of nodes but not the reduction in the number of arms (each node has multiple possible value assignments). Reporting arm reduction would give a more complete picture of the pruning benefit.

## Nice-to-Haves

- Directly validate the containment claim on real SCMs by computing the true optimal intervention using known CPDs and verifying it falls within the mGISS.
- Include LCA closure (without strictness) as a comparison baseline in the real-world graph pruning experiments to quantify when LSCA provides additional pruning beyond LCA.
- Discuss how the choice of bandit algorithm might affect the benefits of mGISS pruning.

## Removed Points

These points from the input review are removed with justification:

- **"Regret computation is circular":** The harsh critic claimed the regret computation is circular because "each will compute regret against its own standard." However, footnote 11 defines the estimated best arm as "the arm that most runs concluded to be the best at the end of training" — this is a single estimated best determined across *all* runs (both mGISS and brute-force), so both methods are evaluated against the same standard. The concern about not using the true optimal is valid (preserved as a Minor weakness above), but the "circularity" claim is factually inaccurate.

- **"Section 1 claim about single-node being undersupported":** The paper provides the supporting argument in Section 2 (lines 97-98): multi-node interventions can directly target all parents of Y, while single-node interventions cannot. The claim is supported.

- **"Section 2 ancestors assumption is strong":** The paper explicitly addresses this in footnote 3, stating it is a permissive assumption ("we can always include them") rather than a requirement. Under no-latent-confounding, this is reasonable.

- **"Y with zero or one parent discussion":** The paper already scopes this out (footnote 8: "We also require Y to have more than one parent, to avoid the trivial case with |mGISS_Y(G)| = 1"). Not a gap.

- **"LSCA definition is dense"** and other presentation/style nitpicks: These are parser artifacts or presentation preferences, not technical weaknesses.

- **Various section-by-section "could benefit from..." suggestions:** These are either already addressed in the paper or reflect the reviewer's preferences rather than actual gaps.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add baselines:** Include Pa(Y) size and LCA closure (without strictness) size alongside mGISS size in the real-world graph pruning experiments (Figure 6). This is the single most impactful improvement — it directly addresses the most significant weakness.

2. **Validate containment empirically:** For each bnlearn model, compute the true optimal node (using the known CPDs) and verify it falls within the mGISS. This directly validates the core theoretical claim.

3. **Use true optimal for regret:** Replace or supplement the estimated-best-arm regret computation with regret computed against the true optimal intervention (computable from the bnlearn CPDs).

4. **Add statistical significance tests** for the regret curve comparisons, or at minimum discuss the overlapping confidence intervals for the asia and sachs datasets.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Learning Good Interventions in Causal Contextual Bandits with Adaptive Context | IPayPEGwdE.md | 5.00 | 1 | Yes | Similar topic (causal contextual bandits with interventions), but uses a much simpler chain-graph setup and binary interventions. Our paper's theoretical contribution (LSCA characterization) is substantially richer and more novel. |
| Adversarial Causal Bayesian Optimization | YcW8i9VCf5.md | 6.00 | 1 | Yes | Also a causal-bandits-adjacent paper with mixed reviews; some reviewers questioned its fundamental novelty (-9.64 weight). Our paper has cleaner, less controversial theoretical novelty. |
| Deriving Causal Order from Single-Variable Interventions | u63OVngeSp.md | 7.00 | 1 | Yes | Strong theoretical + empirical paper with solid contributions. Our paper's theory is comparably strong but experimental evaluation is substantially weaker. |
| Causal Discovery via Bayesian Optimization | 8muemqlnG3.md | 6.50 | 2 | Yes | Strong experimental validation with extensive baselines and outperforming SOTA. Our paper has stronger theoretical novelty but weaker experiments. |

**Bracket (Round 1):** 5.0–6.5

**Final calibration:** The paper is clearly above the 5.0 anchor (IPayPEGwdE), which had a simpler setup (chain graphs, binary vars) and weaker strengths (max strength weight +3.96 vs our +5.23). The paper falls below the 6.5 anchor (8muemqlnG3), which had extensive experimental validation with proper baselines. The decisive factor is the missing baselines weakness (-6.37 weight), which brings the paper below what would be expected for a strong accept. However, the core theoretical contribution (LSCA characterization, Proposition 4, C4 algorithm) is genuinely novel and well-proven, which places it above the reject threshold. The paper sits at the border where the theoretical contribution is sufficient for acceptance but the experimental evaluation needs strengthening.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>