## Summary
# Final Review Report

## Summary

This paper proposes XBIC, a modification of the Bayesian Information Criterion (BIC) for score-based causal discovery in discrete Bayesian networks. The core idea is to soft-weight BIC's complexity penalty using edge-specific Shapley values: when a candidate parent variable contributes strongly to predicting its child (measured by average absolute Shapley value), the penalty for adding that edge is reduced proportionally, while edges with weak directional support retain standard BIC penalization. The motivation is to help resolve edge orientations within Markov-equivalence classes, which standard BIC and constraint-based methods struggle with.

The method operates in three stages: (1) train a per-node XGBoost classifier to predict each variable from all others, (2) compute and aggregate TreeSHAP values over confidently predicted instances to obtain mean directional attributions φ̄_{j→i}, and (3) perform hill-climbing search over DAGs using the modified score XBIC_w = log P(D|G) - (log N/2) × dim(G)/exp(w·SHAP(G)).

Experiments on 10 benchmark discrete BNs (6-76 nodes) across 7 sample-size regimes (700 runs) show consistent F1 improvements: +5.6% vs hill-climbing BIC, +20.9% vs PC, and +9.6% vs GES (relative) at w=2, with the largest gains on medium-to-large networks. The method defaults to standard BIC when Shapley evidence is weak (small samples, low-confidence predictions).

The paper is clearly written, the pipeline is well-structured, and the empirical evaluation is broad. However, several methodological gaps require attention: the exponential penalty weighting can in principle vanish (removing all regularization), the consistency argument assumes an unproven boundedness of SHAP(G), the baseline comparison via random PDAG-to-DAG completion systematically disadvantages competitors, and the critical assumption that Shapley asymmetry reflects causal direction rather than mere predictive asymmetry is not adequately justified. Novelty claims cannot be externally verified in this run due to retrieval limitations.

## Strengths
1. **Clean, principled idea with practical value.** The core concept — using Shapley-based predictive asymmetry to modulate BIC's penalty and help resolve Markov-equivalence orientations — is well-motivated and intuitive. It connects explainable AI (feature attribution) to structure learning in a novel way that is distinct from prior work (which typically uses causal knowledge to improve explanations, not the reverse).

2. **Drop-in compatibility.** XBIC retains the BIC score structure and requires only a pre-computation phase (classifier training + SHAP aggregation) that is separable from the search loop. This means existing BIC-based hill-climbing implementations can adopt XBIC with minimal code changes, which is a practical advantage for adoption.

3. **Extensive and systematic evaluation.** The benchmark setup covers 10 networks (6-76 nodes) with 7 sample-size regimes and 10 repetitions each (700 total runs). This is more comprehensive than many causal discovery papers that test on 3-5 networks. The use of multiple sample sizes (0.125M² to 8M²) helps characterize the data regime where XBIC helps versus defaults to BIC.

4. **Transparent failure-mode analysis.** The paper honestly reports when XBIC does not help (small samples, small networks, low classifier confidence) and explains the mechanism (SHAP(G) near zero → reverts to BIC). This candor increases confidence that the positive results are not cherry-picked.

5. **Statistical rigor.** The use of adjusted Friedman test with post-hoc Wilcoxon signed-rank tests (p < 0.05) across the full 700-run set provides reasonable statistical support for the main claims about w=1 and w=2.

6. **Reproducibility commitment.** Code, data splits, and evaluation scripts are released, which is essential given the complexity of the pipeline (XGBoost training, SHAP computation, search).

## Weaknesses
### W1. Exponential penalty scaling lacks normalization and may eliminate regularization [Major]

The XBIC score (Eq. 2) divides the penalty term `dim(G)` by `exp(w · SHAP(G))`. Since `SHAP(G)` sums absolute Shapley values across all edges in G, and per-edge attributions can be substantial (log-odds scale magnitudes of 0.5–2.0), for networks with 50+ edges `exp(w · SHAP(G))` can reach astronomically large values (e.g., `exp(50) ≈ 5×10²¹`), effectively eliminating the penalty term entirely. This would reduce XBIC to pure likelihood maximization, risking severe overfitting.

The "consistency remark" (Page 4, line 93–95) argues that the penalty still grows as `O(log N)` because `1/exp(w·SHAP(G))` is a constant factor in G, but this assumes SHAP(G) is bounded as N→∞. This assumption is neither proved nor empirically verified. In fact, SHAP(G) likely grows with N because larger samples yield more confident classifiers and larger attributions. If SHAP(G) grows with N, the effective penalty becomes sub-logarithmic, breaking the standard BIC consistency guarantees.

**Required fix:** Normalize SHAP(G) so the exponent is bounded, e.g., `SHAP_norm(G) = (1/|E(G)|) Σ |φ̄_{j→i}| / max_{k≠l} |φ̄_{k→l}|`, ensuring `exp(w·SHAP_norm(G)) ∈ [1, exp(w)]`. Alternatively, report empirical SHAP(G) distributions across networks and sample sizes to demonstrate boundedness.

### W2. Baseline comparison via random PDAG-to-DAG completion creates systematic bias [Major]

In Section 4.1 (Page 5, line 116), the authors state that for PC and other baselines returning a PDAG, they "complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." This random completion systematically disadvantages baselines: an undirected edge that was correctly left unoriented (reflecting genuine Markov-equivalence ambiguity) gets a random direction that is correct only ~50% of the time. 

XBIC's advantage then partly reflects that it "decides" those edges using Shapley evidence, compared against random guessing. The reported +20.9% F1 improvement over PC and +5.6% over BIC-HC may substantially overstate the true structural learning advantage, because the baselines are evaluated on a task (forced orientation of equivalence-ambiguous edges) that they were designed to avoid.

**Required fix:** Report two sets of metrics: (a) skeleton-level precision/recall (ignoring orientation of undirected PDAG edges), and (b) orientation accuracy only on edges where baselines do produce a direction. Alternatively, use a more informed PDAG completion (e.g., orienting by likelihood within the equivalence class) rather than random assignment. At minimum, the fraction of undirected edges in each baseline's PDAG should be reported alongside the completed metrics.

### W3. Shapley asymmetry as a causal signal lacks principled justification [Major]

The paper's core premise is that asymmetric Shapley values (|φ̄_{1→2}| >> |φ̄_{2→1}|) provide directional evidence for causal orientation. However, Shapley values measure predictive relevance, not causal influence. Asymmetry can arise from:
- Confounding (a common cause produces asymmetric predictivity without directional causation),
- Imbalanced functional dependence (one variable is a more informative predictor of another even when both are mutually dependent),
- Classifier capacity differences (XGBoost may fit P(X₁|X₂) better than P(X₂|X₁) due to different marginal complexities).

The paper acknowledges this only indirectly (Section 3.2: "Intuitively, if |φ̄_{1→2}| >> |φ̄_{2→1}|, the edge X₁→X₂ has stronger directional support") but provides no formal argument, synthetic validation (e.g., on a known non-causal asymmetric relationship to test false positive rate), or theoretical justification for why predictive asymmetry implies causal direction. Without this, the method's validity rests on an unverified assumption.

**Required fix:** Add a subsection explicitly discussing when predictive asymmetry coincides with and diverges from causal direction. Include a controlled experiment on data with known confounders to measure the false discovery rate for orientations. Alternatively, provide a theoretical argument linking Shapley asymmetry to causal direction under well-specified assumptions (e.g., causal Markov condition, faithfulness, no hidden confounders).

### W4. Confidence threshold τ may introduce selection bias [Major]

Stage 1 (Section 3.1, page 3, line 68) filters instances for SHAP computation using a confidence threshold τ, retaining only samples where max_c P(X_i=c | X_{\i}) ≥ τ. This systematically excludes low-confidence regions where causal relationships may be genuinely ambiguous. The resulting attributions may over-estimate directional asymmetry, biasing XBIC toward confident (but potentially incorrect) orientations.

The sensitivity analysis (Section 4.3) reports that varying τ between 0.7 and 0.95 changes F1 by <1%, but this narrow range does not test whether τ itself is necessary. A comparison with τ=0 (no filtering) or τ=0.5 would reveal whether the filter helps or hurts.

**Required fix:** Include an ablation comparing τ ∈ {0, 0.5, 0.7, 0.9} and report the fraction of retained instances per node. If low τ does not degrade performance, remove the filter to simplify the method.

### W5. Missing variance, effect size, and SHD reporting for main comparisons [Major]

Table 2 reports only mean F1 deltas (differences) without standard deviations or confidence intervals, despite 10 repetitions per setting. Key information is missing:
- **Absolute F1 values** are not shown for any baseline, making it impossible to assess whether an absolute delta of 0.03 (the average improvement over BIC) matters in practice.
- **SHD** (structural Hamming distance) is defined as a metric in Section 4.2 but only reported for the GES sub-comparison (Section 4.5), not for the main BIC/PC comparisons.
- **Negative deltas** (e.g., Asia at 2M²: -0.12 vs BIC) are not individually discussed or explained.

**Required fix:** Add standard deviations to Table 2 (or a supplementary table), report SHD alongside F1 for all baseline comparisons, and include a brief discussion of settings where XBIC underperforms.

### W6. GES comparison is incomplete due to selection bias [Major]

Section 4.5 (Page 7, line 175) compares XBIC to GES only on the subset of runs where GES completed within 7 days. The paper correctly notes this is "favorable filtering for GES," but the resulting comparison is on a non-representative subset (easier, smaller settings). The reported SHD improvements (6-32%) may not generalize to the full benchmark. Since the GES comparison is partial, the paper should not claim global superiority over GES — the claim should be scoped to the completed subset.

**Required fix:** Restate the GES finding as preliminary and adjust the abstract/conclusion claims accordingly. The main claims should be evaluated against BIC and PC, which completed across all settings.

### W7. Consistency claim needs stronger justification [Major]

The consistency remark (Page 4, line 93-95) states that XBIC preserves BIC's large-sample consistency "under standard regularity conditions" because the penalty grows as O(log N) with a bounded factor c(G). However, whether c(G) = 1/exp(w·SHAP(G)) remains bounded as N→∞ is an open question. As N increases, classifiers become more confident, SHAP values grow, and the penalty factor may approach 0. If it approaches 0 fast enough, the effective penalty could be o(log N), violating the conditions for BIC consistency.

**Required fix:** Either provide a proof that SHAP(G) converges to a finite limit under the confidence threshold τ, or downgrade the consistency remark to a conjecture with explicit conditions.

### W8. Missing real-data validation and domain-specific evaluation [Minor]

All experiments use synthetic data generated from benchmark BNs. While this is standard for causal discovery evaluation, the paper's practical relevance claims (healthcare, insurance, Page 8, line 179) would be more credible with at least one real-world discrete dataset. The absence of real data limits confidence in practical utility.

**Required fix:** Add one real-world discrete dataset (available in bnlearn or UCI repositories) or acknowledge this as a limitation more prominently.

### W9. Novelty verification deferred [Verification — Not Scored]

Due to retrieval unavailability in this run, external literature comparison cannot be performed. The paper's claim about being "the first to directly integrate local feature attributions as an edge-specific, directional modulation of a score-based objective for purely discrete data" (Section 2.3, line 31) requires manual verification against prior work on Shapley-guided structure learning, particularly ReX (Renero et al., 2025) and other methods that use feature attributions for edge scoring. This verification is deferred.

### W10. Minor writing and framing issues [Minor]

- The abstract uses "consistent gains" but Table 2 shows multiple negative entries (e.g., Asia at 2M²: -0.12 vs BIC, Water at 0.125M²: -0.01 vs BIC). The wording should be qualified.
- Contribution 2 ("extensive empirical study") is more of a methodology claim than a scientific contribution; consider merging it into the narrative.
- The "parallelizes naturally" claim in Section 3.3 and Conclusion lacks empirical backing — no multi-core or distributed results are shown.
- The Related Work section on MMHC mentions the method without including it in experiments or justifying its exclusion.
- Limitations should include interpretive scope (Shapley asymmetry ≠ causal direction) and synthetic-only evaluation.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper presents a well-motivated and intuitively appealing idea — using Shapley-based predictive asymmetry to help resolve Markov-equivalence orientations in discrete causal discovery. The empirical evaluation is broad (10 networks, 7 sample-size regimes, 700 runs) and the method's drop-in compatibility with existing BIC pipelines is a practical strength. The paper is clearly written and transparent about failure modes.

However, several major issues prevent a higher score:
- The exponential penalty formulation (Eq. 2) can theoretically eliminate all regularization, and the consistency argument assumes an unproven boundedness of SHAP(G) with sample size (W1, W7).
- The experimental comparison against baselines uses a random PDAG-to-DAG completion procedure that systematically disadvantages PC and GES, likely overstating XBIC's advantage (W2).
- The core assumption that Shapley asymmetry implies causal direction is not adequately justified, theoretically or empirically (W3).
- Reporting omits variance, absolute F1 values, and SHD for main comparisons, making effect sizes hard to assess (W5).

These gaps are addressable with additional experiments, normalization of the score formulation, and more careful baseline comparisons. The core idea has merit and the paper represents a worthwhile contribution to the discrete causal discovery literature, but the current evidence is insufficient to fully validate the claimed improvements or the method's theoretical properties.

**Decision:** Borderline reject / major revision. The paper requires substantial revisions to address the methodological concerns before being ready for publication at a competitive venue.