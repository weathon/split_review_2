Now let me finalize and format the review properly.

## Summary

This paper presents XBIC, a method that augments the BIC score for discrete causal discovery by incorporating Shapley values from per-node XGBoost classifiers. The Shapley values provide asymmetric directional signal about predictive relationships between variables, which is used to soft-weight the BIC complexity penalty during hill-climbing search. The method is evaluated on 10 benchmark discrete Bayesian networks across 7 sample-size regimes (700 runs), reporting improvements in oriented-edge F₁ over BIC-HC (5.6%), PC (20.9%), and a GES variant (9.6%).

## Strengths

1. **Novel and well-motivated conceptual bridge.** The idea of using local feature attributions (Shapley values) from predictive classifiers to inject directional signal into score-based structure learning is genuinely novel. The paper inverts the typical direction of causality-XAI work (using known causal structure to improve explanations) and instead uses explanations to improve discovery. The three-stage pipeline (train classifiers → compute attributions → search with weighted BIC) is clearly laid out and easy to follow.

2. **Principled design with BIC as a limiting case.** Equations (2)–(3) ensure that XBIC defaults to standard BIC when directional evidence is absent (w=0, or SHAP(G)=0, or no instances pass the confidence filter). The penalty still grows as O(log N), preserving BIC's large-sample consistency in the limit. This limits the downside risk of the modification.

3. **Reproducibility commitment.** The paper states that code, data splits, and scripts are released, which is important given the method's several design choices (XGBoost hyperparameter search space, confidence threshold, weight w) that merit independent testing.

## Weaknesses

### Fatal
None.

### Major

**1. Missing ablation: the source of improvement is confounded with classifier expressiveness.**

The Shapley values in XBIC come from XGBoost classifiers trained with extensive hyperparameter search (50 Optuna trials, 5-fold CV across the search space in Table 3). The BIC-HC baseline uses standard conditional-probability-table-based likelihood (a saturated multinomial model). XGBoost can capture non-linear and high-order predictive relationships that the simple multinomial model cannot.

This means the improvement attributed to the Shapley-weighting mechanism could instead come largely from XGBoost extracting richer predictive information — and any reasonable asymmetric score derived from XGBoost's outputs might yield similar gains even without the BIC penalty modulation. The paper needs an ablation that controls for classifier expressiveness: for instance, using a simple logistic regression or shallow decision tree as the base learner to see if the Shapley signal from a weaker model still helps. Without this, the reader cannot determine whether the core contribution is the Shapley-weighting idea or the application of XGBoost to the data.

**2. PDAG→DAG completion procedure systematically disadvantages PC and GES.**

Section 4.1 (line 190) states: "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." PC and GES return PDAGs/CPDAGs encoding Markov equivalence classes — edges that the data cannot orient remain undirected. XBIC outputs a DAG directly and never suffers from this random orientation step. Randomly guessing directions for undirected edges adds noise to the baselines' precision and recall, inflating XBIC's apparent advantage, especially on networks with large Markov equivalence classes. The reported 20.9% improvement over PC and 9.6% over GES should be interpreted with this caveat. A fairer evaluation would report PDAG/CPDAG-level metrics or apply the same random-completion procedure to XBIC's output (by first reducing it to its Markov equivalence class).

Note: This issue does not affect the BIC-HC comparison, since BIC-HC also outputs a DAG directly.

### Minor

**3. "Consistent gains" over BIC overstated by the disaggregated results.**

The abstract and contribution list claim "consistent gains" and "consistent improvements" over BIC-HC. However, Table 2 shows that XBIC (w=2) achieves ≤0.01 F₁ delta against BIC-HC on Asia (5 of 7 sample sizes), Survey (4 of 7), Water (2 of 7), Win95pts (4 of 7), Hepar2 (6 of 7), and Child (3 of 5). Several entries are negative. The aggregate 5.6% relative improvement is driven primarily by gains on Sachs, Insurance, and Hailfinder. The paper partially acknowledges this (line 206: "XBIC sometimes does not improve on BIC") but the central framing of "consistent gains" is not supported by the per-network breakdown.

**4. Raw F₁ values not reported.**

Table 2 reports only F₁ deltas (XBIC minus baseline), not the raw F₁ values. An absolute delta of 0.04 could mean going from 0.50 to 0.54 or from 0.80 to 0.84 — very different scenarios. Without raw values, it is difficult to assess the practical significance of the reported improvements. This is especially relevant since the paper emphasizes the discrete-data setting where baselines may already perform well.

**5. Global penalty modulation mechanism vs. "edge-specific" framing.**

The paper describes the penalty modulation as "edge-specific" throughout (abstract, contributions, conclusion). However, Equation (2) divides dim(G) by exp(w·SHAP(G)), where SHAP(G) is the sum over all edges. This is a global factor: adding one high-SHAP edge reduces the effective penalty on *every other edge* in the graph, not just the newly added one. While the Shapley evidence itself is per-edge, the penalty modulation is graph-level. The paper's language ("when a candidate parent contributes strongly to its child's likelihood, XBIC reduces the penalty proportionally") suggests a per-edge mechanism that does not match the math. This is a framing issue rather than a methodological flaw, but it should be corrected.

**6. GES comparison on a systematically selected subset.**

Section 4.5 acknowledges that GES exceeded the 7-day limit on many settings and that the comparison is restricted to the subset where GES completed. The paper notes this is "favorable filtering for GES" and that XBIC still wins on this subset. However, the headline "9.6% improvement over GES" in the abstract is presented without this caveat. The paper should at minimum report which (network, sample-size) pairs are excluded and characterize how the subset differs from the full set.

**7. Cost-benefit ratio is severe and underexamined.**

Table 5 shows XBIC is 28×–217× slower than BIC-HC in wall-clock time (e.g., 75s → 2,139s on Win95pts; 36s → 1,904s on Hailfinder). The paper mentions parallelization as a mitigation but provides no multi-core speedup measurements despite stating that runs used 4 CPUs. The limitations paragraph (lines 313–317) mentions faster base learners as future work but does not adequately contextualize whether a 0.04 absolute F₁ gain justifies a 100×+ slowdown for offline discovery.

### Trivial
None.

## Nice-to-Haves
- **Run XBIC with a simple base learner** (e.g., logistic regression) to isolate whether the gains come from the Shapley-weighting mechanism or from XGBoost's predictive power. This is the single highest-leverage ablation.
- **Report PDAG-level metrics** (e.g., SHD on CPDAGs, or skeleton F₁ alongside orientation F₁ conditioned on edges the method oriented) to enable fair comparison with PC/GES.
- **Report raw F₁ values** alongside the deltas so readers can calibrate practical significance.
- **Provide per-network, per-sample-size statistical tests** rather than only the aggregate adjusted Friedman test.
- **Show a concrete case study** (e.g., on the Asia network) confirming that Shapley asymmetry aligns with known ground-truth directions and does not systematically favor arbitrary directions for symmetric relationships.

## Removed Points
These points were raised in the input review but are removed after verification against the paper:
- "The penalty modulation is graph-level, not edge-specific — the paper's central framing is inconsistent with the actual mechanism." **Demoted to Minor (#5 above).** The Shapley values are genuinely edge-specific (computed per edge); the modulation aggregates them into a global factor, which the paper's math (Equations 2–3) makes explicitly clear. The "edge-specific" language refers to the evidence, not the weighting. The abstract's "when a candidate parent contributes strongly…XBIC reduces the penalty proportionally" is imprecise but not a fatal misrepresentation.
- "The GES baseline choice is not explained." **Removed.** The paper cites Huang et al. (2018) for the generalized score variant, which is a legitimate choice.
- "Confidence threshold τ is an unnecessary hyperparameter." **Removed.** The paper shows F₁ varies <1% with τ. The stated purpose is reducing SHAP computation cost, which is a practical benefit even if results are insensitive.
- "Shapley evidence phrasing in abstract could mislead about causal interpretation." **Removed.** The paper explicitly distinguishes its setup from causal-Shapley work in Section 2.2.
- Various pure formatting nitpicks and speculative reproducibility concerns about the release status of cited tools.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add an ablation with a weaker base classifier (e.g., logistic regression) to isolate the contribution of the Shapley-weighting mechanism from XGBoost's predictive power. This is the most important fix.
2. Evaluate on PDAG/CPDAG-level metrics (or apply the same random-completion procedure to XBIC's output) for fair comparison with PC and GES.
3. Report raw F₁ values in addition to deltas.
4. Tone down the "consistent gains" language in the abstract to match the per-network results.
5. Clarify the global nature of the penalty modulation in the abstract and introduction.
6. Provide multi-core runtime benchmarks to substantiate the parallelization claims.
7. Characterize the GES-completion subset to contextualize the 9.6% figure.

## Score and Decision

This paper presents a genuinely novel idea at the intersection of explainability and causal discovery. The pipeline is clearly described, the evaluation is extensive (10 networks, 7 sample sizes, 700 runs), and the design is principled (BIC as limiting case). However, two major concerns significantly weaken the contribution: (1) the missing ablation leaves the source of improvement confounded with the base classifier's expressiveness, and (2) the PDAG→DAG evaluation procedure systematically disadvantages PC and GES, inflating the reported advantages. Several additional issues (overstated "consistent gains" claim, missing raw F₁ values, imprecise framing, GES subset characterization, severe cost-benefit ratio) also need attention. The paper would benefit substantially from controlled ablations and fairer evaluation before its claims can be fully supported.

MY FINAL SCORE: 5.0
MY FINAL DECISION: Reject