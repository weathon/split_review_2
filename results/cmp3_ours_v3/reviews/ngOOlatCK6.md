## Summary

This paper studies conditional-intervention causal bandits with single-node interventions, and provides a complete graphical characterization of the minimal set of nodes (mGISS) guaranteed to contain the optimal intervention node. The authors prove equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Proposition 4), characterize mGISS as the LSCA closure of the parents of Y with an elegant Λ-structure formulation (Theorems 12–13), and propose the linear-time C4 algorithm (Algorithm 1) to compute it. Experiments on random and real-world graphs demonstrate search space reduction, and bandit experiments illustrate improved convergence.

## Strengths

1. **A clean theoretical framework.** The equivalence between conditional-intervention superiority and deterministic atomic-intervention superiority (Definitions 1–2, Proposition 4) is the right formal architecture. It lets the authors reason about the simpler deterministic atomic case while making claims about the conditional case — a genuinely useful reduction.

2. **An elegant graphical characterization.** The LSCA closure (Definition 9) and its equivalent Λ-structure characterization (Theorem 12) are novel and well-motivated. The paper traces intuition clearly from the simple "parents of Y" case through increasingly complex examples (Figure 1a–d). The fact that the mGISS is unique (Proposition 6) and equals the LSCA closure of Pa(Y) (Theorem 13) is a compact, verifiable result.

3. **A simple, correct, linear-time algorithm.** Algorithm 1 (C4) uses a single reverse-topological pass with a connector bookkeeping scheme. The connector definition (Definition 14) and Lemma 15 cleanly tie the algorithm's behavior to the LSCA closure. O(|V|+|E|) is optimal for a preprocessing step, and the pseudocode is clear enough to reimplement without ambiguity.

4. **Clear placement within the literature.** The paper consistently distinguishes itself from multi-node hard-intervention work (Lee & Bareinboim, 2018), contextual bandits, and work on selecting policies for a pre-specified node. Limitations (no latent confounders, single-node only) are acknowledged.

## Weaknesses

### Fatal
None.

### Major

1. **Bandit experiment lacks meaningful baselines.** The bandit experiment (Figure 3) compares mGISS-pruned search only against brute-force (all ancestors of Y). Because mGISS is always a subset of the ancestors, this comparison only shows that fewer arms helps — not that mGISS is the *right* set of fewer arms. A parents-only (Pa(Y)) baseline would reveal whether the extra LSCA nodes beyond Pa(Y) actually contribute to convergence, or whether gains come entirely from arm-count reduction. A random-subset-of-ancestors baseline (size |mGISS|) would test whether the specific set matters. Without such controls, the paper's claim that pruning to the mGISS "substantially accelerates convergence rates" (abstract, Section 1) is not convincingly supported by the bandit evidence presented. The search-space-reduction experiments (random graphs and bnlearn graphs) are fine for demonstrating pruning, but the convergence claim depends on this bandit experiment.

### Minor

2. **Bandit experiment uses only 4 hand-picked datasets.** The paper states these were "selected because their graphical structures are non-trivial and both An(Y) and mGISS_Y(G) are sufficiently small to allow experimentation." This introduces selection bias — datasets where mGISS is large (and pruning less substantial) were excluded. While the search-space-reduction results in Appendix H cover many more graphs, the bandit results would be more convincing on a broader or random sample.

3. **Regret oracle is an estimate, not ground truth.** Footnote 11 defines the best arm as "the arm that most runs concluded to be the best at the end of training." This is a reasonable heuristic but not a true oracle. Both methods are evaluated against the same estimate, so the comparison is not biased, but the paper should acknowledge this limitation more prominently.

4. **Conditioning-set assumption may limit practical applicability.** The paper assumes An(X)\{X} ⊆ Z_X for each X, meaning all ancestors of the intervened node must be observed. For nodes deep in a large graph, this conditioning set could be high-dimensional, potentially making the per-context bandit problem intractable. Footnote 3 notes this is not strictly necessary for the results to hold, but the claim that the method is useful "especially when [graphs] are large" (Section 6) is exactly where this assumption becomes most onerous. The experiments use small graphs with the smallest conditioning set Z_X = An(X)\{X\}, sidestepping the issue.

5. **No discussion of total arm-space reduction.** The mGISS prunes the node search space, but each surviving node X has a conditioning set Z_X including all its ancestors. The total "arm space" (node × policy space) may not shrink proportionally to the node count. The paper does not bound or empirically report the actual reduction in (node, context) pairs.

6. **Worst-case guarantee is inherently conservative.** Definition 1 quantifies over all SCMs consistent with G, so mGISS includes nodes relevant only for pathological SCMs. In practice, the true SCM may allow much more aggressive pruning. This is a property of the theoretical framework (not a flaw), but the paper should acknowledge this gap between worst-case guarantee and average-case behavior — the conclusion does not currently mention it.

### Trivial

- In the discussion of Figure 1d, the text explains why X needs to be tested but does not explicitly state the resulting mGISS for that example; the reader must infer it from the gray highlighting in the figure. A brief worked example would help.

## Nice-to-Haves

- Adding a random-subset-of-ancestors baseline (of size |mGISS|) to the bandit experiment would directly test whether the specific mGISS set matters or just the arm-count reduction.
- A theoretical characterization of graph structures where mGISS is significantly smaller than the ancestor set would strengthen the paper beyond the current empirical observation that sparse graphs benefit more.
- The paper could discuss how the universal quantification over Z_X/Z_W in Definition 1 contributes to the conservatism of the mGISS, and whether relaxing it is viable future work.

## Removed Points

These points were raised in the input review but are not included as weaknesses in the final assessment:

- **Claim that "more challenging" is unsupported:** The critic argued this claim on p.1 (lines 37–38) is stated without support. However, the paper explicitly supports it on p.3 (line 98): "if one allows for interventions on arbitrary sets, one simply needs to intervene on all the parents Pa(Y) of Y... Since in our case the agent cannot do this whenever |Pa(Y)| > 1, the minimal search space will, as we will see, be complex." The support is present.
- **Criticism about observability not following from "no latent variables":** In the Pearlian framework with no latent confounders, all variables in the DAG are assumed measured. This is standard and clearly stated.
- **Comparison to Lee & Bareinboim (2018/2020) on a shared metric:** The problem settings differ fundamentally (multi-node hard interventions vs. single-node conditional interventions), making direct comparisons non-straightforward; this is scope creep.
- **Regret measure being "circular" in a biased way:** The estimated best arm is computed across all runs (both methods), not per-method, so it does not inherently favor the pruned method. The lack of a true oracle is retained as a Minor weakness.
- **Formatting/presentation nitpicks:** Parser artifacts; the original submission does not have these issues.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one meaningful baseline to the bandit experiment: parents-only (Pa(Y)) to test whether extra LSCA nodes contribute, and a random subset of ancestors of size |mGISS| to test whether the specific set composition matters.
2. Discuss the conditioning-set assumption's practical implications for large graphs more explicitly, and ideally bound or estimate total arm-space (node × context) reduction.
3. Add a paragraph to the conclusion acknowledging the gap between the worst-case guarantee (over all SCMs) and the average-case behavior practitioners encounter.

---

**Calibration report:**
All retrieved anchors, with avg human score, round, and comparison to paper under review:

| Paper | Score | Round | How it compares |
|-------|-------|-------|----------------|
| Learning Good Interventions in Causal Contextual Bandits | 5.00 | R1 | Weaker theory (restrictive binary assumptions), similarly weak experiments — our theory is substantially stronger |
| Causal Bayesian Optimization with Unknown Causal Graphs | 3.40 | R1 | Lower quality overall; high variance (scores 3–10) — our paper is more consistent and complete |
| Sparse Causal Model | 3.00 | R1 | Problems with novelty and methodology — our paper is cleaner and more rigorous |
| Adversarial Causal Bayesian Optimization | 6.00 | R1/R2 | Comparable: theory-focused causal bandit paper, accepted, but with some framing concerns |
| Deriving Causal Order from Single-Variable Interventions | 7.00 | R1/R2 | Strong theory with solid experiments — our theory is comparably strong but experiments weaker |
| Optimal Causal Representations and the Causal Information Bottleneck | 6.00 | R2 | Split reviews (8,5,5,6), rejected — our paper has cleaner theory and fewer internal conflicts |
| Exploiting Causal Graph Priors with Posterior Sampling for RL | 7.50 | R2 | Strong theory + solid experiments — our experiments are notably weaker |
| When Selection meets Intervention | 8.00 | R2 | Principled theory with thorough experiments — our paper's experiments are not at this level |
| Robust agents learn causal world models | 5.75 | R2 | Controversial (scores 8,1,6,8) — our paper has more consistent evaluation appeal |
| Identifying Representations for Intervention Extrapolation | 8.00 | R2 | Strong theory + thorough experiments — our experiments are not comparable |

**Round-1 bracket**: 6.0–7.0 (based on the observation that the theory is as strong as 7.00+ papers but experiments are more like 5.00–6.00 papers; the theory genuinely stands on its own as the primary contribution).

**Narrowing**: Compared to the 6.00 anchor (Adversarial CBO), this paper has less controversy about its framing and cleaner theory. Compared to the 7.00 anchor (Deriving Causal Order), the experiments are weaker. The midpoint of the bracket (6.5) best reflects a paper with a strong, well-structured theoretical contribution that is held back by insufficiently rigorous experimental validation.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>