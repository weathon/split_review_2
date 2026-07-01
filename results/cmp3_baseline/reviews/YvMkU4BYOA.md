## Summary

XBIC augments the standard Bayesian Information Criterion (BIC) for score-based causal discovery on discrete data by soft-weighting the complexity penalty with edge-specific Shapley values.  Directional evidence for each candidate edge is obtained by training per-node XGBoost classifiers and aggregating local TreeSHAP attributions; edges with strong attribution support incur a smaller penalty, guiding hill-climbing toward better orientations within Markov equivalence classes.  Evaluated on ten benchmark discrete networks across seven sample-size regimes (700 runs), the method reports 5.6% relative F₁ improvement over BIC, 9.6% over a generalized-score GES variant, and 20.9% over PC.

## Strengths

- **Novel integration of local feature attributions into a score-based objective.**  Using Shapley values from predictive models to inject directional information into the BIC penalty is a creative and underexplored direction, bridging explainability with structure learning.
- **Extensive empirical coverage.**  Ten networks (6–76 nodes), seven sample-size regimes, and 700 total runs provide a broad evaluation landscape.  The release of code, data splits, and scripts supports reproducibility.
- **Clear exposition of the pipeline.**  The three-stage process (train classifiers → aggregate Shapley → penalized search) is well illustrated and easy to follow.

## Weaknesses

### Major

1. **Unfair baseline comparison due to random orientation of undirected edges.**  PC and GES output partially directed graphs (CPDAGs).  The authors complete these to DAGs by *randomly* orienting undirected edges while preserving acyclicity.  This introduces uncontrolled noise and systematically underestimates the baselines’ ability to correctly orient edges, thereby inflating XBIC’s reported gains.  The standard practice is to compare at the CPDAG level (e.g., SHD on CPDAG) or to orient undirected edges via a principled secondary search (e.g., a few hill-climbing steps with BIC within the equivalence class).  Because the paper’s core claim rests on oriented-edge F₁, this flaw casts doubt on the validity of the experimental results.

2. **Incomplete and potentially biased GES comparison.**  GES timed out on many network/sample-size combinations; only runs where GES finished are retained.  This selection bias removes the hardest cases, making the head-to-head comparison less representative.  A fair comparison would either enforce a wall-clock budget for all methods or use a more efficient GES implementation.

3. **Lack of theoretical grounding for the score modification.**  The consistency remark (Section 3.3) is too superficial.  The weighting factor \(1/\exp(w\cdot\text{SHAP}(G))\) changes the penalty in a model-dependent way that could, in principle, distort the asymptotic ordering of models.  Without formal analysis—or at least a detailed discussion of when the weighting helps vs. harms—the method remains a heuristic whose behavior is not well understood.

### Minor

- **Modest absolute improvement.**  The average F₁ gain over BIC is only 0.04 (absolute).  While relative improvements are cited, the practical significance of such a small delta on realistic problems is unclear.
- **High computational overhead.**  XBIC is 8–15× slower than BIC and 2–10× slower than PC (Table 5).  The front-loaded classifier training and Shapley aggregation, combined with hyperparameter tuning via Optuna, make the method unattractive for time-constrained or large-scale applications.
- **Sensitivity analysis is limited.**  Only the Shapley weight \(w\) is varied (1,2,3).  The confidence threshold \(\tau\) is said to affect F₁ by <1% on average, but no results or ablations are shown.  The choice of classifier (XGBoost) and hyperparameter search are not ablated.

### Trivial

- The abstract’s claim of “5.6% … 9.6% … 20.9%” should be explicitly labeled as relative improvements (they are, but the table uses “relative” and “absolute” separately—this is fine).

## Nice-to-Haves

- Ablate the confidence threshold \(\tau\) and the choice of base learner (e.g., logistic regression, LightGBM) to understand when the Shapley signal is most useful.
- Analyze the method per edge type: how often does XBIC correctly orient previously ambiguous non-collider edges vs. introducing new errors?
- Compare with exact score-based solvers (e.g., GOBNILP) on small networks to calibrate the ceiling of improvement.

## Novel Insights

The core insight—that local feature attributions from predictive models can provide a directional signal for causal orientation, and can be integrated into a score-based objective as a soft complexity penalty—is genuinely novel.  It opens a new interface between explainability and causal discovery, with the potential to orient edges beyond what conditional-independence tests can resolve.  The paper demonstrates that even imperfect, correlation-based attribution signals can, on average, push the search toward better DAGs.

## Suggestions

1. **Fix the baseline evaluation.**  Compare all methods at the CPDAG/PDAG level using metrics such as Structural Hamming Distance on the completed PDAG, or orient undirected edges for the baselines using a few further hill-climbing iterations with the standard BIC (restricted to edge reversals that stay within the same equivalence class).  Re-evaluate all claims after this correction.
2. **Provide a more rigorous analysis of the score.**  At minimum, prove that, under standard regularity conditions and for any fixed \(w\), XBIC is consistent for the true graph when the true graph is identifiable (e.g., outside equivalence classes).  Show an example where the weighting could theoretically mislead.
3. **Include wall-clock limited runs for GES** to avoid selection bias, or drop GES comparisons where it does not finish.
4. **Report raw F₁, precision, and recall values** (not just deltas) in a supplementary table so readers can assess absolute performance levels.

## Score and Decision

The core experimental protocol (random orientation of undirected edges) invalidates the baseline comparisons on which the main quantitative claims rest.  Without this flaw, the paper would present a promising but preliminary heuristic with modest improvement and high overhead.  As submitted, the evidence is not sufficient to support the claimed gains.

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>