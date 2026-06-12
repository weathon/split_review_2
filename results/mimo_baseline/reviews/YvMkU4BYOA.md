## Summary

The paper proposes XBIC, a score-based causal discovery method for discrete Bayesian networks that augments the standard BIC complexity penalty with edge-specific Shapley values computed from per-node XGBoost classifiers. When a candidate parent contributes strongly (via SHAP attribution) to predicting its child, the BIC penalty is reduced proportionally, helping orient edges within Markov equivalence classes. The method is evaluated on 10 benchmark discrete BNs across 7 sample-size regimes (700 total runs), reporting ~5.6% relative F₁ improvement over hill-climbing BIC.

## Strengths

- **Creative cross-domain idea.** The paper brings a genuinely novel perspective by using explainability tools (Shapley values) to improve structure learning itself, rather than the more common direction of using causal knowledge to improve explanations. This is a worthwhile research direction.

- **Extensive empirical evaluation.** The evaluation covers 10 networks (6–76 nodes), 7 sample-size regimes, and 700 total runs with proper statistical testing (adjusted Friedman + Wilcoxon signed-rank). This is more thorough than many causal discovery papers.

- **Practical drop-in design.** XBIC reduces exactly to BIC when w=0 or when attribution signal is absent, preserving familiarity and backward compatibility. This makes adoption straightforward within existing score-based pipelines.

- **Reproducibility.** Code, data splits, and evaluation scripts are publicly released.

## Weaknesses

### Fatal

None.

### Major

- **Core mechanism lacks theoretical or conceptual justification.** The entire method rests on the assumption that Shapley values from predictive models (XGBoost classifying X_i from X_{\setminus i}) provide reliable *directional* evidence for causal edges—i.e., that |φ_{j→i}| ≫ |φ_{i→j}| reliably indicates the causal direction j→i. The paper offers no theoretical argument or conceptual analysis for why this asymmetry should hold in general. For symmetric binary relationships or in the presence of confounders, the predictive asymmetry may not track causal direction. The method works empirically (on average), but without understanding *when and why* the signal is reliable, the contribution is less impactful. A failure-mode analysis or characterization of when the Shapley asymmetry correctly vs. incorrectly indicates direction would have substantially strengthened the paper.

- **Ad hoc scoring formula.** The XBIC score (Eq. 2) divides the complexity penalty by exp(w·SHAP(G)). Why exponential? Why divide rather than subtract or use another modulation? No alternative formulations are explored or compared, and no principled derivation connects the functional form to the desiderata. The "consistency remark" argues the penalty still grows as O(log N), but this is insufficient: BIC consistency under standard regularity conditions requires that the penalty term scales correctly relative to the log-likelihood, and multiplying by a data-dependent, graph-dependent factor c(G) ∈ (0,1] can violate these conditions in non-trivial ways, particularly as SHAP(G) itself varies with N.

- **Significant computational overhead with limited discussion.** Table 5 shows XBIC is 50–200× slower than BIC-HC (e.g., 1904s vs. 36s on Hailfinder). While the paper mentions parallelization, no actual parallelized runtime is reported. For the largest networks, XBIC takes ~2000 seconds, which is practical for offline analysis but raises questions about scalability to larger problems. The overhead is front-loaded (classifier training + SHAP computation), making repeated evaluation with different w expensive.

- **Missing baselines.** MMHC is mentioned but explicitly excluded ("not the focus here"), despite being arguably the most relevant hybrid baseline for discrete BNs. No comparison with recent methods like NOTEARS-based approaches adapted to discrete data, SCORE, or other order-based methods is provided. PC and GES are reasonable baselines, but the choice not to include MMHC or more recent competitors weakens the comparative claims.

### Minor

- **Modest and inconsistent gains.** The overall relative improvement over BIC is 5.6%, with absolute F₁ gains of 0.03–0.04. Several network/sample-size combinations show zero or negative deltas (e.g., Asia at most sample sizes, Win95pts at large samples, Water at small samples). The paper acknowledges this occurs when classifiers fail to surpass the confidence threshold, but this means XBIC's benefit is non-uniform and unpredictable without diagnostics.

- **Comparison methodology for GES.** GES exceeded the 7-day timeout on many settings, so comparison is only on runs where GES completed. While the paper frames this as "favorable filtering for GES," it introduces selection bias: the excluded settings are precisely the harder ones where the comparison might look different. The analysis would be stronger with a per-network breakdown showing which settings were excluded.

- **Insensitivity of confidence threshold is under-analyzed.** Varying τ between 0.7 and 0.95 changed F₁ by <1%. If the filter is truly this insensitive, its primary role is computational (reducing SHAP evaluations), which should be stated explicitly. If it does affect results on some networks, a per-network analysis would be informative.

### Trivial

- Table 2 uses many dashes for missing GES runs without clearly indicating which network/sample-size combinations were excluded due to timeout.

## Nice-to-Haves

- A diagnostic showing the correlation between Shapley asymmetry (|φ_{j→i}| vs |φ_{i→j}|) and true edge orientation on benchmark networks. This would directly validate the core mechanism.
- An ablation comparing the exponential modulation to alternative functional forms (e.g., linear, sigmoid) for the SHAP weight.
- Runtime comparison with parallelized XBIC to give a practical sense of the achievable speedup.

## Novel Insights

The paper's genuinely novel insight is that predictive feature importance (Shapley values from per-node classifiers) can be repurposed as a directional signal to break ties within Markov equivalence classes in score-based causal discovery. This bridges XAI and causal structure learning in an underexplored direction: using explanations to inform discovery rather than vice versa. However, the paper stops short of providing a deeper understanding of *when and why* this cross-domain transfer works—for instance, under what data-generating conditions the Shapley asymmetry reliably mirrors causal direction. Without such analysis, the insight remains empirical rather than principled.

## Suggestions

1. Add an analysis characterizing when Shapley asymmetry correctly identifies edge direction vs. when it fails (e.g., as a function of the functional relationship, variable cardinality, or presence of confounders). This would transform the method from an empirical trick into a principled approach.
2. Compare at least one alternative functional form for the SHAP weight modulation and provide justification for the exponential choice.
3. Include MMHC as a baseline and discuss why it was excluded.
4. Provide an ablation on whether the Shapley signal helps specifically with orientation (the claimed benefit) vs. skeleton recovery. Separate skeleton and orientation F₁ would clarify the mechanism.
5. Report actual parallelized runtimes to give a practical sense of computational feasibility.

## Score and Decision

The paper presents a creative idea at the intersection of XAI and causal discovery, with extensive evaluation. However, the core mechanism (Shapley asymmetry as directional evidence) lacks theoretical justification, the scoring formula is ad hoc, the gains are modest (5.6% relative over BIC), and important baselines are missing. The computational overhead is also substantial. These issues collectively place the paper below the acceptance threshold for ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>