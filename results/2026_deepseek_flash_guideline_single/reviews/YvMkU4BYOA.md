Now let me produce the final review.

## Summary

This paper proposes XBIC, a score-based causal discovery method for discrete Bayesian networks that augments the BIC score with Shapley-value-based directional evidence. The method: (1) trains per-node XGBoost classifiers to predict each variable from all others, (2) aggregates TreeExplainer Shapley values over confidently predicted instances to obtain directional signals, and (3) incorporates these signals by dividing BIC's complexity penalty by exp(w·SHAP(G)), where SHAP(G) sums the absolute Shapley values over edges in the candidate graph. XBIC degrades gracefully to standard BIC when the attribution signal is weak. Evaluated on 10 benchmark discrete networks (6–76 nodes) across 7 sample-size regimes (700 runs), the method reportedly improves oriented-edge F₁ by 5.6% over hill-climbing BIC, 9.6% over GES, and 20.9% over PC.

## Strengths

1. **Novel conceptual bridge.** The idea of using feature attributions (Shapley values) from predictive classifiers as soft weights on BIC's complexity penalty is genuinely novel and well-motivated (Section 3). The paper clearly distinguishes this from prior work that injects causal knowledge into explanations rather than using explanations to improve structure learning. This is the right kind of cross-pollination between explainability and causal discovery.

2. **Clean degradation to BIC.** When the confidence filter yields few instances or w=0, XBIC reduces exactly to standard BIC (Eq. 2, line 113: "if w=0 or SHAP(G)=0, then XBIC_w = BIC"). This graceful fallback means the method cannot be worse than BIC in expectation — a practical safety property that makes it a plausible drop-in replacement.

3. **Broad and transparent evaluation.** The experiments cover 10 networks, 7 sample-size regimes, and 700 total runs with appropriate statistical testing (adjusted Friedman + Wilcoxon). Code and data splits are released. The paper honestly reports the substantial runtime overhead (Table 5: e.g., 74.78s vs 0.39s for Asia, 1904s vs 36s for Hailfinder) and explicitly notes settings where XBIC provides little benefit (small samples, small networks). Section 4.5's treatment of GES — using only completed runs — is transparent about the filtering.

## Weaknesses

### Major

1. **The core directional signal lacks a principled connection to causal direction.** The paper asserts (line 127) that |φ̄_{i→j}| ≫ |φ̄_{j→i}| indicates "stronger directional support" for X_i → X_j, but provides only intuition, not theoretical justification. Predictive models capture statistical dependence, not causal asymmetry. In common structures (e.g., mediator chain X₁→X₂→X₃), the Shapley signal may be near-symmetric between directions for reasons unrelated to the true causal structure. The paper acknowledges the need for theoretical analysis only as future work (line 313: "formal analysis of the weighting mechanism... is an important direction"). This makes XBIC a heuristic whose behavior on any given dataset is opaque. While the empirical evaluation partially compensates, the method's core mechanism is not grounded in a theory of when or why the Shapley asymmetry should align with causal direction.

2. **The evaluation against PC (and to a lesser extent GES) uses a non-standard comparison that inflates the reported gains.** The paper states (line 190): "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." This is not standard practice in causal discovery evaluation. PC's design is to correctly identify edges whose direction is not identifiable from data, leaving them undirected. Randomly orienting these edges converts ~50% of such correctly-identified ambiguities into orientation errors, deflating PC's scores. The headline 20.9% improvement over PC (Table 4) is likely inflated by this choice. The comparison against BIC-HC (which also returns a DAG, so the comparison is fair) shows a more modest 5.6% relative (0.04 absolute) F₁ improvement at a 50–200× computational cost.

### Minor

3. **The exponential penalty weighting (Eq. 2) is not ablated or justified against alternatives.** The penalty is divided by exp(w·SHAP(G)). For moderate Shapley values (e.g., SHAP(G)=5, w=2), the denominator is exp(10)≈22,000, making the penalty near-zero and the score dominated by pure log-likelihood. A linear or sigmoid weighting (e.g., penalty × (1−α·SHAP(G))) would be more controlled. The paper sweeps w but does not compare functional forms, and does not report the typical range of SHAP(G) values across networks.

4. **The confidence threshold τ used in the main experiments is not reported.** Line 194 says "Varying this threshold between 0.7 and 0.95 changed downstream F₁ by < 1% on average" but never states the specific value used for the results in Tables 2 and 4.

5. **No ablation of the classifier choice.** All experiments use XGBoost with TreeExplainer. The entire directional signal is mediated by this choice. An ablation with a simpler model (e.g., logistic regression or random forest) would strengthen confidence that the signal is robust to the predictor.

6. **High heterogeneity across networks.** XBIC shows negative F₁ deltas on Win95pts at 8M² (−0.09 vs BIC, −0.15 vs PC) and essentially no improvement on Hepar2 at any sample size (Table 2). The aggregated 5.6% average masks this variability, and the paper does not analyze when/why XBIC hurts.

### Trivial

None.

## Nice-to-Haves

- Report CPDAG-level metrics (adjacency F₁, orientation F₁ on oriented edges only) for PC to enable a fairer comparison.
- Report the typical range of SHAP(G) values across networks to assess whether the exponential weighting enters a degenerate regime.
- Report variance/confidence intervals for F₁ scores in Tables 2 and 4 (currently only means are given for aggregated numbers).
- Ablate the exponential weighting against a linear or sigmoid alternative.

## Removed Points

- "Unstable formatting of Table 2" — this is a parser artifact during PDF extraction, not a paper problem; the original submission's table is properly formatted.
- "GES filtering as a fatal flaw" — the paper is transparent about this (Section 4.5: "We retained only repetitions where GES completed and computed GES statistics on that subset"). The filtering favors GES by dropping its hardest runs, so the comparison is conservative against XBIC, not the reverse.
- "SHAP(G) conflates density with directional evidence" — edges with zero Shapley value contribute nothing to the sum, so the concern is about the exponential functional form (retained as Minor #3) rather than a fundamental confound.
- "Selection bias from ignoring low-confidence instances" — the paper provides a τ sensitivity analysis showing <1% F₁ impact, which partially addresses this.
- Generic scope-creep criticisms (demanding continuous-data experiments, larger-scale networks beyond the stated scope).

## Novel Insights

The harsh review usefully identifies that the random-orientation evaluation of PC/GES is non-standard and that the headline 20.9% improvement is almost certainly inflated by this choice. This is a genuinely insightful methodological criticism that would benefit the authors in revising their evaluation. The concern about the Shapley-causality connection is also well-taken, though the paper already acknowledges this gap as future work in its limitations section.

## Suggestions

1. Either (a) provide an intuitive theoretical account of when |φ̄_{i→j}| ≠ |φ̄_{j→i}| should align with causal direction, or (b) reframe the contribution more modestly as a heuristic directional bias for BIC rather than a principled resolution of Markov-equivalence ambiguity.

2. Fix the PC/GES evaluation: report CPDAG-level metrics (adjacency F₁, orientation F₁ on oriented edges) so that the comparison does not penalize methods for correctly identifying equivalence-class ambiguity.

3. State the confidence threshold τ used in the main experiments.

4. Ablate the exponential weighting against a linear alternative (e.g., penalty × (1 − α·SHAP(G)) clamped to [0,1]).

5. Report the typical range of SHAP(G) values encountered across networks.

## Score and Decision

### Calibration Anchors

**Round 1 (Bracketing):** I retrieved 24 anchor papers across six score bands using the query "score-based causal discovery discrete Bayesian networks BIC".

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR.md (KL Divergence GFlowNets) | 1.00 | 1 | Far weaker — unclear methodology, no empirical rigor |
| nSDOkm0SKo.md (Financial Markets NN) | 1.00 | 1 | Far weaker — speculative, no actual contribution |
| bEgDEyy2Yk.md (Minimax Path) | 1.00 | 1 | Far weaker — code implementation paper |
| u1cQYxRI1H.md (IC-Light) | 10.00 | 1 | Far stronger — mature, well-evaluated method |
| fSxiromxAq.md (Sparse Causal Model) | 3.00 | 1 | Weaker — vague problem definition, unclear contribution |
| TRHyAnInUC.md (D³PM Diffusion CD) | 3.25 | 1 | Somewhat weaker — identifiability concerns but good idea |
| JzFLBOFMZ2.md (LLM Supervised CSL) | 3.20 | 1 | Somewhat weaker — LLM reliability concerns |
| MVpvyeVeyI.md (Causal BO unknown graphs) | 3.40 | 1 | Comparable approach but higher variance (scores 3–10) |
| eqQFBnjjPP.md (ExDBN) | 4.00 | 1 | Comparable — reasonable contribution, mixed reviews |
| orD5t7blqV.md (PIT Algorithm) | 4.25 | 1 | Comparable — incremental contribution to PC |
| i5JfdnCob7.md (Optimal Kernel Choice) | 4.40 | 1 | Comparable — solid but incremental |
| G19piTjVYA.md (Efficient Differentiable Causal Order) | 4.00 | 1 | Comparable — reasonable but some concerns |
| 8muemqlnG3.md (DrBO) | 6.50 | 1 | Stronger — novel method, cleaner evaluation, minor weaknesses |
| eeJz7eDWKO.md (Meta-Learning Bayesian CD) | 6.00 | 1 | Stronger — solid theoretical framing, clean experiments |
| qac43AwuL9.md (Causal Information Bottleneck) | 6.00 | 1 | Stronger — well-grounded theory, clear contribution |
| 3n6DYH3cIP.md (Extendable Iterative SL) | 5.60 | 1 | Somewhat stronger — practical contribution, cleaner eval |
| xByvdb3DCm.md (Selection meets Intervention) | 8.00 | 1 | Far stronger — deep theoretical contribution |
| k38Th3x4d9.md (Root Cause Analysis AERCA) | 8.00 | 1 | Far stronger — well-executed, practical + theoretical |
| 3cuJwmPxXj.md (Representations for Intervention Extrapolation) | 8.00 | 1 | Far stronger — strong theory + experiments |
| NSVtmmzeRB.md (GeoBFN) | 8.00 | 1 | Far stronger — mature, full pipeline |

**Round 1 bracket:** 3.5–5.5 (the paper is clearly stronger than the 1–3 range papers and weaker than the 5.5–8 range papers).

**Round 2 (Narrowing):** Additional retrieval in the 3.0–5.5 band.

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| ljZFM2mhbR.md (DAG-SHAP) | 5.00 | 2 | Slightly stronger — similar lack of theory but cleaner evaluation |
| lnMQGBHYRt.md (Scalable do-Shapley) | 5.33 | 2 | Stronger — clear methodology |
| lLzeKG6t52.md (Shapley Value Approximation) | 4.00 | 2 | Comparable — incremental contribution |
| 2pEqXce0um.md (Root Cause Analysis) | 4.50 | 2 | Comparable — reasonable but some gaps |

The paper under review sits at the lower end of the 4–5 range. Its idea is more novel than the typical 4-range incremental paper, but the two major weaknesses (lack of principled grounding for the core mechanism, and a flawed evaluation that inflates headline numbers) prevent it from reaching the 5+ range.

**Final Score: 4.0** — This is a borderline reject. The paper introduces a genuinely novel idea (Shapley-weighted BIC for discrete causal discovery), and the implementation is clean with broad evaluation. However, (a) the core mechanism is presented as a heuristic without theoretical justification for why Shapley asymmetry should indicate causal direction, (b) the evaluation against PC/GES uses a non-standard random-orientation procedure that inflates the reported improvements, and (c) the fair-baseline comparison (BIC-HC) shows only 0.04 absolute F₁ gain at 50–200× computational cost. The paper has merit and could be strengthened with a revised evaluation and clearer framing, but in its current form the evidence does not fully support the claims.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>