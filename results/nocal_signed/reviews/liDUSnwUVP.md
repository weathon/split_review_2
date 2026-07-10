Now let me finalize the review based on all the evidence and impact scores.

## Summary

This paper introduces HG-DCM, a framework for early-stage pandemic forecasting that leverages cross-disease temporal transfer — training a deep learning backbone on historical pandemics (Ebola, SARS, Dengue, seasonal influenza) alongside early data from a current outbreak to predict compartmental model parameters. The core idea is genuinely novel and addresses an important real-world problem.

## Strengths

- **Novelty of the approach (Section 2).** Cross-disease temporal transfer — training a deep compartmental model on biologically distinct historical pandemics to initialize forecasts for a novel pathogen — is a genuinely new formulation. Prior work either transfers parameters between close epidemics or does spatial transfer; assembling a diverse multi-pandemic training set to learn universal spread dynamics is a novel contribution. [impact: +9.8]

- **Dataset construction (Section 3.1.1).** Compiling time-series case data from COVID-19, Ebola, SARS, Dengue, and seasonal influenza into a single usable dataset is non-trivial and constitutes a real contribution. [impact: +9.0]

- **Architectural design (Section 2.1).** The two-stage pipeline (neural parameter predictor → DELPHI compartmental solver) is clearly described. The specific design choice of removing Batch Normalization because cross-pandemic batch statistics introduce bias is a concrete, sensible fix motivated by the problem structure. [impact: +8.6]

- **Problem framing (Section 1).** The cold-start problem in pandemic forecasting — where a novel pathogen has emerged but only 2–8 weeks of data exist — is genuinely important and under-addressed. The analogy to an epidemiologist drawing on a mental library of past outbreak trajectories is effective. [impact: +4.8]

## Weaknesses

### Major

- **Claim-evidence mismatch for CNN comparison (Table 2, Section 3.2.2).** The paper states that "CNN generally underperforms HG-DCM across all training horizons" and that "the performance gap is largest in the early stage (2–4 weeks)." On mean MAE, CNN wins at 2 weeks (15,600 vs. 18,603) and at 4 weeks (11,238 vs. 110,452 — roughly an order of magnitude). On median MAE, HG-DCM wins at 2 and 4 weeks but CNN wins at 6 weeks (1,188 vs. 1,276). The paper does not specify which metric supports its claim, does not acknowledge the contradictory evidence from mean MAE, and makes the strongest claim about the exact horizons where mean MAE contradicts it. [impact: -7.8]

- **Catastrophic 4-week mean MAE anomaly (Table 2).** HG-DCM's mean MAE at 4 weeks (110,452) is roughly 6× worse than its own 2-week mean (18,603) and 15× worse than its 6-week mean (7,113). The median at 4 weeks (1,771) is better than at 2 weeks (2,231), revealing an extreme mean/median gap indicating catastrophic failures on a subset of locations. The paper neither diagnoses this failure mode nor discusses it. For a model proposed for public health decision-making, understanding when and why it catastrophically fails is critical. [impact: -8.1]

- **External baseline comparison on only 2 locations (Table 1, Section 3.2.1).** The headline comparison against GradABM and EiNNs covers only Massachusetts and the United States (2 out of 258 locations the paper evaluates on). The authors note this is due to data/code availability constraints, which is understandable, but it means the full 258-location evaluation (Table 2) compares only against ablations of the authors' own framework (DELPHI, CNN, T-DCM). No external baseline is evaluated on the full set. [impact: -9.3]

### Minor

- **Evaluation on only one target pandemic (COVID-19) limits the cross-pandemic transfer claim (Section 3).** The paper's central thesis is that historical pandemics provide useful inductive bias for *novel* pathogens, but the evaluation tests only on COVID-19. The model is trained on historical data PLUS early COVID-19 data simultaneously, then evaluated on later COVID-19 data — this tests whether historical data helps as a regularizer within the same pandemic, not whether the model can forecast a genuinely novel pathogen before seeing any data from it. A leave-one-pandemic-out evaluation would more directly test the stronger claim. [impact: -9.6 — treating as Minor because it's scope-constrained but the scorer suggests near-fatal impact]

- **Mean vs. median MAE discrepancy not discussed (Section 3.2.2).** The paper reports both metrics in Table 2 but switches between them across comparisons without acknowledging disagreements. For the DELPHI comparison the paper quotes median reductions (38.2%, 32.4%). For the CNN comparison it makes a blanket claim without specifying the metric. For T-DCM it specifies "with respect to median MAE." The paper never discusses why mean and median diverge (e.g., the 4-week anomaly) or why one metric is preferred for a given comparison. [impact: -2.5]

- **Parameter interpretation overclaims (Section 3.2.3).** The paper states HG-DCM produces "more conservative and realistic estimates" based on Wilcoxon signed-rank tests showing different parameter distributions. There are no ground-truth parameter values for a real pandemic — the test only shows the distributions differ, not which is more accurate. "More conservative" is a normative interpretation that the evidence does not uniquely support. [impact: -6.6]

- **MAPE loss term has division-by-zero issue (Eqns. 3–4).** The loss function includes |(C_{ij} − Ĉ_{ij})/C_{ij}| which is undefined when C_{ij}=0. This occurs at the start of the time series for many locations. The paper mentions setting negative case counts to zero but does not address this division-by-zero in the loss. [impact: -1.3]

### Trivial

- **The sigmoid ranging function for parameter bounding is underspecified (Section 2.1).** The paper does not specify which parameters get which ranges or whether the ranges are learned or fixed from epidemiological first principles. [impact: -0.6]

- **The 258 locations used in the ablation are not characterized.** The paper does not describe how many countries these span, the range of outbreak sizes, or whether results are consistent across income levels. [impact: -5.4]

## Nice-to-Haves

- Uncertainty quantification (prediction intervals, CRPS) would strengthen the practical value for public health decisions.
- Simple baselines (exponential growth fit, seasonal ARIMA) would contextualize the improvement over reported methods.
- Run-time analysis would be useful for deployment during unfolding crises.
- The actual values of α and β (loss-balancing hyperparameters, Eqns. 3–5) should appear in the main text.

## Removed Points

These points are flagged to be removed; treat them with caution:

- Mention of hierarchical Bayesian models as missing related work → Removed per rule: do not mention missing related works.
- "The DELPHI model can produce uncertainty estimates; it is unclear why this is not included" → Demoted to Nice-to-Have; requesting UQ goes beyond standard practice for the paper's stated scope.
- "No runtime or computational cost discussion" → Demoted to Nice-to-Have.
- "Simple baselines like ARIMA/exponential extrapolation missing" → Demoted to Nice-to-Have.
- "α and β not reported in main text (possibly in the appendix)" → The appendix is stripped by the parser; these values exist in the original submission. However, reporting them in the main text is a valid suggestion; moved to Nice-to-Have.
- Formatting nitpick about [L, N, D] tensor notation → Trivial.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Diagnose the 4-week failure mode**: Identify which locations produce the catastrophic mean MAE, check whether metadata is complete for those locations, and report whether the failure is predictable from location characteristics. This is the most actionable critical finding from the paper's own data.
2. **Report both mean and median consistently**: For every comparison, report both metrics explicitly and discuss any discrepancies.
3. **Add a leave-one-pandemic-out evaluation**: E.g., train on all pandemics except SARS and test on SARS; train on everything except COVID-19 and test on COVID-19. This directly tests whether the model generalizes to genuinely novel pathogens, which is the paper's central claim.
4. **Provide α and β values in the main text**: These govern the balance between MAE/MAPE and between past/current pandemic loss.
5. **Characterize the 258 evaluation locations**: Report country breakdown, outbreak size range, and income-level analysis.
6. **Qualify the CNN comparison claim**: Acknowledge that on mean MAE, CNN outperforms HG-DCM at 2 and 4 weeks, and explain why this occurs.

## Score and Decision

The paper identifies a genuinely important problem and proposes a novel solution with thoughtful architectural design. The cross-disease temporal transfer idea and the compiled multi-pandemic dataset are valuable contributions.

However, the evaluation as presented does not adequately support the paper's claims. The central claim that HG-DCM outperforms baselines is contradicted by the paper's own ablation results on mean MAE (CNN wins at 2 and 4 weeks). A catastrophic failure mode at 4 weeks is neither diagnosed nor discussed. The headline external baseline comparison covers only 2 out of 258 locations. And the entire evaluation is on a single target pandemic, making it impossible to assess cross-pandemic generalization. These are structural evaluation issues that would need to be substantially addressed before the paper's contributions can be properly assessed.

Given the strength of the core idea balanced against the significant evaluation shortcomings, the paper falls below the acceptance bar in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>