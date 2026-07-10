Here is my final consolidated review.

---

## Summary

This paper studies the problem of finding the minimal set of nodes that need to be considered for single-node conditional interventions in causal bandits (analogous to Lee & Bareinboim's 2018 characterization for multi-node hard interventions). The authors introduce the LSCA (Lowest Strict Common Ancestor) closure and a Λ-structure criterion to characterize the minimal globally interventionally superior set (mGISS), prove its optimality, and give a linear-time algorithm (C4) to compute it. Experiments on random and real-world graphs measure the size reduction achieved by mGISS, and a bandit experiment compares node selection with and without mGISS pruning.

---

## Strengths

- **Well-motivated problem and clear framing.** The paper identifies a genuine gap in the causal bandits literature: the search space for conditional (context-dependent) interventions has not been characterized, even though conditional interventions are the natural formalization of many real-world decision-making problems (doctor selecting treatment based on symptoms, traffic control, etc., Section 1). It correctly situates itself as the conditional-intervention analogue of Lee & Bareinboim (2018).

- **Elegant graphical characterization.** The LSCA concept (Definition 7) and its closure (Definition 9) naturally generalize the standard LCA idea to handle cases like Figure 1d where ordinary LCAs fail. The Λ-structure formulation (Definition 11, Theorem 12) provides a clean graphical criterion — a node belongs to the mGISS precisely when it sits atop a Λ-shaped substructure connecting two nodes in the parent set. This is visually interpretable and theoretically principled. [Model impact score: **+10.00**]

- **Linear-time algorithm (C4).** Algorithm 1 is simple, runs in O(|V|+|E|) time, and the connector notion (Definition 14) elegantly propagates information about which nodes have multiple distinct descendants in the target set. The intuition — a node whose children all funnel through the same connector can be dominated by that connector — is clean and well-explained. [Model impact score: **+9.99**]

- **Equivalence between conditional and deterministic superiority (Proposition 4).** This is a valuable reduction that simplifies analysis and provides a bridge between stochastic conditional interventions and deterministic atomic ones, enabling proofs to be carried out in the simpler deterministic setting. [Model impact score: **+9.97**]

---

## Weaknesses

### Fatal
None.

### Major

- **Regret computation uses an estimated best arm rather than the true optimal, undermining the bandit experiment.** The paper states (footnote 11): "For the computation of regret, we use the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training." Since the true optimal arm is unknown for the real-world bnlearn graphs (the SCMs are not fully specified), the benchmark is estimated from the algorithm's own behavior. This means: (a) the benchmark may differ between the brute-force and mGISS conditions if they converge to different nodes, making their regret curves incomparable; (b) the absolute regret values do not correspond to true regret against the optimal intervention. The paper's claim that "cumulative regret curves can be significantly improved — meaning that better nodes are selected earlier" (Section 6) is not reliably supported by the current experimental design. This is the paper's most significant weakness. [Model impact score: **-9.89 / -10.00**]

**Why this is Major, not Fatal:** The paper's core theoretical contribution (graphical characterization of mGISS, Theorem 13) is proven in the appendix and stands independently of the bandit experiment. The flawed experiment weakens the paper's empirical narrative but does not invalidate the theory.

### Minor

- **CondIntUCB is underspecified in the text.** The paper states that choice (ii) "utilizes a UCB instance specific to the conditioning set value" (Section 6), meaning for each realization of Z_X = An(X)\{X} there is a separate UCB. No hyperparameters (exploration constant), round counts, or implementation details for handling potentially many contexts are reported. While code is in the supplementary material, the text alone is insufficient for reproducibility. [Model impact score: **-9.42**]

- **Target node selection biases toward large-ancestor-set cases.** The paper consistently selects "the node with the most ancestors" as Y (footnote 8) to maximize potential search space reduction. This systematically biases the evaluation toward cases where the method works best; results for randomly selected Y or Y with small ancestor sets would provide a more complete picture. (The paper also runs random-graph experiments with varying parameters, which partially mitigates this concern.) [Model impact score: **-7.55**]

- **The brute-force baseline is ambiguously specified.** The bandit experiment compares "using all nodes (brute-force) and the mGISS nodes" (Section 6), but it is unclear whether "all nodes" means V\{Y} (all non-target nodes, potentially including non-ancestors that cannot affect Y) or An(Y)\{Y}. If non-ancestors are included, the comparison is trivially favorable to mGISS. Additionally, the paper does not compare against other principled subsets (e.g., parents-only, LCA set without the strict condition, random subsets of the same size), making it difficult to determine whether mGISS provides benefit beyond any reduction in arm count. [Model impact score: **-0.03**]

### Trivial
None.

---

## Nice-to-Haves

- **Validate mGISS correctness directly on synthetic SCMs**, where the true optimal intervention is analytically computable, to provide direct empirical support for Theorem 13 beyond the existing proofs.
- **Compare mGISS against other principled subsets** (parents-only, LCAs, random subsets of equal cardinality) to isolate whether mGISS provides specific benefit beyond arm-count reduction.
- **Fix the regret benchmark** by using synthetic SCMs with known optimal arms, or replace regret with alternative metrics (e.g., best reward found, proportion of runs selecting a node in the mGISS).
- **Discuss the computational cost** of the per-context UCB approach in CondIntUCB, especially for graphs with large ancestor sets.

---

## Removed Points

The following weaknesses from the input review were removed with justification:

1. **"Bandit experiments do not validate the core theoretical claim"** — REMOVED. The paper's theoretical result (Theorem 13) is proven. The experiments are intended to demonstrate practical utility, not to prove the theory. The reviewer's demand to verify correctness on synthetic SCMs is a nice-to-have, not a weakness.

2. **"More challenging claim is misleading"** — REMOVED. The paper (line 98) specifically states that *the minimal search space characterization* is more involved for single-node interventions (where mGISS = LSCA closure) than for multi-node interventions (where mGISS = Pa(Y) trivially). This is accurate within context.

3. **"Z_X assumption constrains applicability"** — REMOVED. The paper clearly states this as an assumption of its setting (footnote 3). Assumptions are legitimate in theoretical work.

4. **"LSCA definition uses confusing notation (X, Y)"** — REMOVED. Definition 7 uses X, Y as generic nodes in a pair-wise definition; the context makes the meaning clear. This is a trivial notational observation.

5. **"No comparison to existing causal bandit algorithms"** — REMOVED. The paper notes that no existing algorithm targets the conditional intervention setting (Section 7). Missing baselines that do not exist is not a valid weakness.

6. **"Computational cost of CondIntUCB per-context UCBs not discussed"** — MOVED to Nice-to-Haves. The paper notes datasets were selected so mGISS and ancestors are "sufficiently small," which partially addresses this.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Fix the bandit experiment by using synthetic SCMs with known optimal interventions, enabling proper regret computation against the true optimal arm.
2. Add comparisons against other principled subsets (parents-only, LCA set, random subsets) to demonstrate that mGISS provides benefit beyond simple arm-count reduction.
3. Report CondIntUCB hyperparameters, round counts, and implementation details in the main paper.

---

## Score and Decision

**Calibration process.** Round 1 bracketing queried the human-review corpus with six score bands (strong reject through strong accept) for "causal bandits graphical characterization minimal search space." The most relevant anchor papers retrieved were:

| Path | Avg score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `IPayPEGwdE` (Learning Good Interventions in Causal Contextual Bandits) | 5.00 | R1 | Yes | Similar topic (causal bandits + context), but weaker theoretical contribution (incremental extension from deterministic to stochastic contexts vs a new characterization). |
| `YcW8i9VCf5` (Adversarial Causal Bayesian Optimization) | 6.00 | R1 | Yes | Strong theory + mixed experiments; comparable overall balance of strengths and weaknesses. |
| `MVpvyeVeyI` (CBO with Unknown Causal Graphs) | 6.50 | R1 | Yes | Very divisive (scores 5,8,3,10); its top score was driven by exceptionally strong experiments. |

**Round-1 bracket:** 5.0–7.0. The paper's theory is stronger than IPayPEGwdE (score 5) but its experiments are weaker than MVpvyeVeyI (score 6.5).  

**Round-2 narrowing:** Compared itemized impact scores. My paper's strongest theoretical items (graphical characterization +10.00, C4 algorithm +9.99) match or exceed the anchors' strongest items, confirming the theory is accept-worthy. However, the regret-estimation weakness (-9.89/-10.00) is a major methodological flaw in the experiments that the anchors did not have at comparable severity. This pulls the score below the 6.5 anchor (whose experiments were strong) and toward the 6.0 anchor (which had balanced but not exceptional experiments).  

**Final score:** 6.0 — the theoretical contribution is solid and novel enough to warrant borderline acceptance, but the flawed bandit experiment prevents a higher score.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>