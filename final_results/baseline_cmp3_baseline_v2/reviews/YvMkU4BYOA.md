## Summary

The paper proposes XBIC, a score-based causal discovery method for discrete data that augments the Bayesian Information Criterion (BIC) with edge-specific Shapley values. By training per-node classifiers, computing mean Shapley attributions for confident predictions, and using these to softly reduce BIC’s complexity penalty, XBIC provides directional information that helps orient edges within Markov equivalence classes. The method is evaluated on ten benchmark Bayesian networks (6–76 nodes) across seven sample-size regimes (700 runs), showing consistent improvements in oriented-edge \(F_1\) (e.g., +5.6% vs. BIC) and structural Hamming distance over BIC, PC, and a GES variant.

## Strengths

- **Novel and well-motivated approach.** The idea of using local feature attributions (Shapley values) to inject directional evidence into a score-based causal discovery objective is creative and naturally connects explainability with structure learning. The method reverts to standard BIC when attribution signals are weak, preserving a familiar baseline.
- **Clean formulation and implementation.** The XBIC score is a simple modification of BIC, making it a drop-in replacement in existing search procedures. The pipeline (classifier training → attribution aggregation → score-based search) is clearly described with algorithms and a figure, aiding reproducibility.
- **Extensive empirical evaluation.** The experiments cover 10 diverse discrete networks, 7 sample sizes, 10 repetitions per setting, and three strong baselines. Improvements are reported with multiple metrics (precision, recall, \(F_1\), SHD) and statistical significance tests. The results are consistent and favor XBIC.
- **Open-source release.** Code, data splits, and evaluation scripts are provided, supporting reproducibility and further research.

## Weaknesses

### Fatal

None.

### Major

1. **High computational cost.** XBIC is orders of magnitude slower than standard BIC (e.g., ~200× on small networks, ~28× on Win95pts) due to per-node XGBoost training, hyperparameter tuning (Optuna + 5-fold CV), and TreeSHAP aggregation. The paper acknowledges this but does not demonstrate practical mitigation (e.g., parallelization benchmarks, simpler classifiers, or approximate SHAP). The claim of a “drop-in upgrade” is undermined by this overhead.
2. **Heuristic weighting scheme without theoretical grounding.** The penalty modulation \( \exp(w \cdot \text{SHAP}(G)) \) is ad-hoc. The paper’s “consistency remark” only shows that the penalty order is unchanged, but the constant factor is data-dependent and no formal convergence or identifiability guarantee is provided. The choice of weight \(w\) (swept over \(\{1,2,3\}\)) is a free hyperparameter with no principled selection method.
3. **Potential selection bias in GES comparison.** GES failed to complete within 7 days on many settings, so head-to-head comparison is limited to a subset where GES succeeded. This could favor GES, yet XBIC still outperforms. Nevertheless, the baseline evaluation is incomplete.
4. **Evaluation focuses only on directed-edge metrics.** While orientation is the paper’s target, metrics like Structural Hamming Distance (SHD) and Structural Intervention Distance (SID) would provide a fuller picture. The paper reports SHD but not adjacency-level accuracy or SID, and the comparison of directed-edge \(F_1\) alone may overstate orientation improvements relative to overall graph quality.

### Minor

- The confidence threshold \(\tau\) is varied only briefly (0.7–0.95, <1% \(F_1\) change). A more detailed sensitivity analysis (e.g., on networks with low confidence predictions) would strengthen the method.
- The paper does not compare against other score-based methods that use asymmetric or data-dependent penalties (e.g., fNML, Bayesian Dirichlet scores, or the generalized score from Huang et al. directly within different searches).
- The phrase “generalized-score GES variant” is slightly imprecise; GES is a search algorithm, not a score. Clarifying the exact GES implementation used would help.

### Trivial

None.

## Nice-to-Haves

- A theoretical analysis (even informal) of when and why Shapley-based weighting improves orientation beyond chance, or a consistency proof under standard regularity conditions.
- An ablation study isolating the role of each component: classifier choice, confidence filter, aggregation method, weighting function. This would clarify what drives the gains.
- Exploration of faster base learners (LightGBM, logistic regression) or approximate SHAP to reduce runtime without sacrificing much signal.
- Guidance for setting \(w\) in practice (e.g., cross-validation on a held-out set or adaptive schemes based on confidence).

## Novel Insights

The paper demonstrates that local feature attributions from predictive models can yield asymmetric directional signals that are useful for orienting edges in score-based causal discovery, even when the true causal graph is unknown. This bridges explainability and structure learning in a concrete way, showing that the asymmetry in Shapley values—normally used for feature importance—can be exploited to break ties within Markov equivalence classes for discrete data.

## Suggestions

- Provide runtime experiments with parallel execution across nodes to show how wall-clock time can be reduced in practice.
- Include results with a simpler classifier (e.g., a single decision tree or logistic regression) to separate the effect of the classifier’s predictive power from the Shapley signal itself.
- Add a small-scale experiment on synthetic DAGs where the true orientation signal is known, to validate that the Shapley-based gradient correlates with correct orientation.
- Discuss the choice of \(w\) more explicitly; consider a cross-validation scheme or an automatic selection based on the magnitude of \(\text{SHAP}(G)\) across candidate graphs.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>