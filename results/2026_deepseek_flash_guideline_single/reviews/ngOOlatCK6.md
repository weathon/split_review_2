Now let me finalize the review based on all the calibration and paper reading.

## Final Review

## Summary
This paper studies the problem of identifying the minimal set of nodes that are guaranteed to contain the optimal single-node conditional intervention in a causal bandit. The authors introduce the LSCA (Lowest Strict Common Ancestor) closure, prove it equals the minimal globally interventionally superior set (mGISS), and present the C4 algorithm that computes this set in O(|V|+|E|) time. Empirical results on random and real-world graphs show substantial search space reduction (e.g., 17% of ancestors retained for sparse 500-node graphs, >90% reduction for large real models).

## Strengths

1. **Novel and well-motivated theoretical contribution.** The LSCA closure characterization (Theorem 12, Theorem 13) is genuinely new — this is the first complete graphical characterization of the minimal search space for conditional-intervention causal bandits. The problem is clearly motivated with concrete examples (doctor selecting treatments based on symptoms, traffic control).

2. **Clean, efficient algorithm.** The C4 algorithm (Algorithm 1) is presented clearly via the connector mechanism (Definition 14, Lemma 15), runs in optimal O(|V|+|E|) time, and is proved correct (Theorem 16). The connector formulation gives intuitive insight into why certain nodes can be pruned.

3. **Substantial and well-documented search space reduction.** The experiments on random graphs (1000 graphs per setting, 4 sizes, 4 densities) and real-world graphs from the `bnlearn` repository systematically demonstrate pruning efficacy. The results are striking: e.g., 17% retention for 500-node sparse graphs, and over 90% reduction for the largest real-world graphs.

4. **Proposition 4 is a clever theoretical simplification.** The equivalence between conditional-intervention superiority (Definition 1, expectation-based) and deterministic atomic-intervention superiority (Definition 2, pointwise) is non-trivial and dramatically simplifies the analysis, reducing a stochastic policy problem to a deterministic comparison.

## Weaknesses

### Fatal
None.

### Major

1. **The bandit regret experiment (Figure 3) does not properly validate the claimed benefit of C4.** The experiment compares regret of a UCB bandit using all nodes vs. only mGISS nodes. Since mGISS has fewer "meta-arms" by construction, any reduction in arm count would reduce regret — the experiment cannot distinguish whether C4's *specific* node selection matters or whether any subset would produce the same effect. The experiment also lacks baseline comparisons against other principled node-reduction methods (e.g., parents-of-Y only, ordinary LCA set, random subset of same size). Furthermore, Footnote 11 defines regret using an "estimated best arm" (majority vote across runs) rather than ground-truth optimal rewards, which is a circularity — the best arm is determined by the same class of algorithms whose performance is being measured. This experiment does not invalidate the paper's core theoretical contribution, but it should be either redesigned with proper baselines and ground-truth regret, or (preferably) removed in favor of more direct comparisons between mGISS and simpler node-selection baselines on the search space reduction metrics.

### Minor

1. **Proposition 4 proof is fully deferred to the appendix.** The equivalence between an expectation-based definition (Definition 1) and a pointwise deterministic definition (Definition 2) is non-trivial and central to the theory. A brief proof sketch in the main text (even 3–4 lines explaining how the expectation/noise gap is bridged) would greatly improve reader trust and accessibility.

2. **Missing baseline comparisons in search space experiments.** The paper reports the mGISS size as a fraction of the ancestor set, but does not compare against simpler alternatives such as (a) just the parents of Y, (b) the ordinary LCA set (which the paper shows is insufficient), or (c) the set of all ancestors. These comparisons would directly quantify the value added by the recursive LSCA closure refinement.

3. **No discussion of how the Z_X assumption affects the characterization.** The theory assumes all ancestors of X can be included in the conditioning set Z_X (Footnote 3). A practitioner who cannot observe some ancestors would benefit from a discussion of whether and how the mGISS characterization degrades when this assumption is violated.

4. **Minimality/uniqueness proof (Proposition 6) is deferred.** Since "minimal" is in the title, a brief intuition for why the mGISS is unique and why no proper subset works would help the reader.

### Trivial
None.

## Nice-to-Haves

- Add comparisons against parents-of-Y and ordinary LCA baselines in the search space experiments.
- Replace or remove the regret experiment in favor of a direct node-selection baseline comparison.
- Include a short proof sketch of Proposition 4 in the main text.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"The bandit regret experiment is uninformative as designed and does not support the claims made from it"* — Kept as Major Weakness 1 (see above). The criticism about estimated best arm and lack of baselines is substantive; the "tautology" framing is slightly overstated since the experiment does show mGISS doesn't discard the optimal node (regret converges despite fewer arms), but the core concern stands.
- *"Proposition 4 requires more scrutiny"* — Demoted to Minor Weakness 1. The concern is valid but the proof exists in the appendix; a main-text sketch would help but the paper does provide the proof.
- *"No comparison against simpler baselines in search space experiments"* — Kept as Minor Weakness 2.
- *"No discussion of Z_X assumption"* — Kept as Minor Weakness 3.
- *"Minimality claim would benefit from sketch"* — Kept as Minor Weakness 4.
- *"Random graph generation not ideal"* — Removed (standard methodology, the paper already supplements with real graphs).
- *"Missing related works"* — Removed (cannot verify).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Replace the regret experiment with a direct mGISS vs. baseline comparison.** Specifically, compare the size of mGISS against: (a) parents of Y alone, (b) the ordinary LCA set, (c) the full ancestor set. This would directly quantify the incremental value of the recursive LSCA computation over simpler alternatives, and would be far more convincing than the current bandit experiment.

2. **Add a 3–5 line proof sketch of Proposition 4 in Section 3.** Explain how the gap between "expectation over noise" (Definition 1) and "pointwise for every noise realization" (Definition 2) is bridged — even a high-level argument that the policy in Definition 1 can be chosen to select the optimal x from Definition 2 would dramatically improve readability.

3. **Briefly address the Z_X assumption's robustness.** A paragraph noting that the characterization holds as long as the conditioning sets include all ancestors (which can always be assumed under the paper's observability assumptions), and discussing what happens when some ancestors are unobserved, would improve practical applicability.

4. **Consider renaming or repositioning** the "Impact on conditional intervention bandits" subsection if keeping it, to clarify that it is a sanity check (C4 pruning does not hurt) rather than a comparative validation.

## Score and Decision

**Bracketing:** Round 1 retrieval across 6 score bands identified anchors from strong reject (avg 0.5–1.0) through accept (avg 6–8). The paper's core contribution (novel theoretical characterization + efficient algorithm) rules out the strong reject band (avg <2) and the reject band (avg 2–4). The most topically similar anchors are:

| Anchor Paper | Avg Score | Comparison to Our Paper |
|---|---|---|
| "Learning Good Interventions in Causal Contextual Bandits" | 5.0 | Weaker theory (binary interventions, simple graphs); our paper stronger |
| "Adversarial Causal Bayesian Optimization" | 6.0 | Comparable theoretical depth; our experiments more focused |
| "Causal Bayesian Optimization with Unknown Causal Graphs" | 6.5 (accepted avg) | Strong disagreement (scores 5,8,3,10); our paper has cleaner theory |
| "Deriving Causal Order from Single-Variable Interventions" | 7.0 | Strong theory + experiments; our paper comparable but experiments weaker |
| "Robust agents learn causal world models" | 5.75 | Purely theoretical with no experiments; our paper more applied |

**Round 1 bracket:** 5.5–7.5 (confirmed by similarity to ACBO at 6.0 and Deriving Causal Order at 7.0).

**Narrowing:** Comparing against "Adversarial Causal Bayesian Optimization" (6.0, accepted) — our paper has cleaner theoretical framing and better-focused experiments, but its regret experiment is weaker. Comparing against "Deriving Causal Order" (7.0, accepted) — similar theoretical depth, but our experimental validation is less complete (missing baselines). The estimated best arm issue and missing baselines pull the score down from the 7.0 anchor.

**Final score: 6.5.** This reflects a genuine, novel theoretical contribution with solid search space validation, tempered by the flawed regret experiment design and missing baseline comparisons which prevent it from reaching the 7+ level.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>