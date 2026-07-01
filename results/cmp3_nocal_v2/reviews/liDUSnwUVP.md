Here is my final consolidated review:

---

## Summary

This paper introduces HG-DCM, which uses a neural network to predict parameters of a compartmental model (DELPHI) by learning from historical pandemic data (Ebola, SARS, Dengue, seasonal influenza) to enable cross-pandemic knowledge transfer for early-stage COVID-19 forecasting. The core idea—that human-driven macroscopic dynamics (transmission decay under interventions, mobility constraints) generalize across biologically distinct pandemics—is well-motivated and plausible.

## Strengths

- **Well-motivated problem with clear intuition.** The paper correctly identifies the cold-start problem in pandemic forecasting and provides a genuine rationale for cross-disease transfer that goes beyond "more data is better" (Section 1). The distinction between biological specificity of pathogens versus universality of human-driven spread dynamics is a sound basis for the method.

- **Novel multi-pandemic dataset.** Compiling time-series data across COVID-19, Ebola, SARS, Dengue, and seasonal influenza with country-level metadata (Section 3.1.1) is a non-trivial contribution that enables further research into cross-pandemic forecasting.

- **Interpretable parameter analysis.** Section 3.2.3 shows that HG-DCM produces more stable DELPHI parameters than fitting DELPHI independently per location, with statistical testing (Wilcoxon signed-rank test, p < 0.05). The overshooting analysis (Figure 4) provides a meaningful evaluation beyond simple error metrics.

- **Sound architectural design choices.** The removal of BatchNorm for cross-pandemic generalization (Section 2.1) and the window-shift/masking augmentation strategies (Section 2.2) are well-reasoned and address genuine challenges in this setting.

## Weaknesses

### Major

- **Claims are overstated relative to the evidence.** The abstract and introduction claim HG-DCM "consistently and significantly outperforms state-of-the-art methods" and the ablation section (line 188) states CNN "generally underperforms HG-DCM across all training horizons." However, the ablation results (Table 2) tell a mixed story:
  - By **mean MAE**: CNN beats HG-DCM at 2 weeks (15,600 vs 18,603) and 4 weeks (11,238 vs 110,452—a ~10× failure). The 4-week result is particularly problematic and unreported in the narrative.
  - By **median MAE**: CNN beats HG-DCM at 6 weeks (1,188 vs 1,276); DELPHI beats HG-DCM at 8 weeks (538 vs 796).
  - The statement "the performance gap is largest in the early stage (2–4 weeks)" (line 188) is directly contradicted by the mean MAE data, where CNN massively outperforms HG-DCM at 4 weeks.
  - The paper relies on median MAE when it favors HG-DCM (against T-DCM, DELPHI) while ignoring mean MAE when it does not (against CNN at 2/4 weeks). This is selective reporting.

- **The anomalous 4-week mean MAE for HG-DCM is unexplained and undermines confidence.** In Table 2, HG-DCM's mean MAE jumps from 18,602.6 (2 weeks) to 110,452.4 (4 weeks), then drops to 7,112.5 (6 weeks). This U-shaped pattern is not physically plausible for a model that should benefit from more data. The paper does not acknowledge or discuss this result—no variance, no distributional analysis, no failure count. The gap between mean and median MAE at 4 weeks (110,452 vs 1,771) signals that outliers are driving the narrative, but the paper does not investigate this.

- **External validation is limited to only two locations (US and Massachusetts).** The abstract mentions evaluation "across 258 global locations," but the comparison against methods outside the DELPHI/CNN/T-DCM family (GradABM, EiNNs) is conducted on only two locations from the same country (Section 3.2.1). The paper acknowledges this limitation but it remains severe: a pandemic forecasting method must demonstrate robustness across diverse geographies with different healthcare systems and epidemic trajectories. The 258-locations claim is accurate only for the ablation study against variants of the same model family.

- **No evaluation on a held-out target pandemic.** The paper's central claim is about cross-pandemic transfer generalization, yet every experiment uses COVID-19 as the sole target. Training on COVID-19 + other pandemics and testing on a held-out pandemic (e.g., withholding SARS) would directly test whether cross-disease transfer generalizes, rather than only testing whether historical data helps predict COVID-19. This is a critical gap for the paper's core thesis.

- **No simple or naive baselines.** Every baseline is either a complex deep learning method or a variant of the proposed model. Standard time-series baselines (ARIMA, exponential growth extrapolation, persistence/naive model) are missing entirely. Without these, the reader cannot assess whether improvements over DELPHI reflect meaningful gains from cross-pandemic transfer or merely DELPHI's documented instability on small data.

### Minor

- **Reporting only MAE on cumulative cases.** The loss function uses both MAE and MAPE, but results report only MAE on cumulative cases. A model that stays near the last observed value can achieve reasonable cumulative MAE. Metrics like growth-rate error, log-score, or percentage error would provide a more informative picture, especially for early-stage forecasting where growth rates matter more than absolute levels.

- **No confidence intervals or uncertainty quantification.** The paper provides only point estimates (mean/median MAE). For public health decision-making, the range of plausible outcomes is at least as important as the point forecast. Figure 3 shows density plots but these are qualitative.

- **DELPHI baseline's unusual pattern is not discussed.** In Table 2, DELPHI's mean MAE goes 342,686 → 813,808 → 29,746 → 45,141 across training windows. The 4-week mean being the highest when more data should help is unusual and suggests either instability (a known DELPHI issue) or a fitting problem. Since HG-DCM uses DELPHI as its compartmental backbone, understanding DELPHI's baseline behavior matters for contextualizing HG-DCM's improvements.

- **No characterization of the compiled dataset.** The paper constructs a novel multi-pandemic dataset but does not analyze it: how many locations per pandemic, what is the data distribution, how variable are trajectories, how much overlap exists between pandemics? This would help assess whether the transfer learning premise is plausible.

- **No discussion of computational cost or inference time.** For a tool aimed at real-time public health decision-making, this information is relevant.

### Trivial

None.

## Nice-to-Haves

- Acknowledge and analyze the failure cases (especially what drives the 4-week mean MAE spike). Understanding failure modes would strengthen the paper more than additional cherry-picked wins.
- Test on a held-out target pandemic (e.g., train on COVID-19 + others, test on SARS) to directly test the generalization claim.
- Report distributional metrics (error quantiles, fraction of catastrophic failures) alongside point estimates.
- Include simple baselines (ARIMA, persistence model) to calibrate the reader's sense of effect size.

## Removed Points

These points were flagged during filtering; treat them with caution:

- The critic's claim of "5 wins, 2 losses, and 1 draw" in Table 1 (correct count: HG-DCM wins 6 of 8 comparisons; EiNNs wins 2). The Massachusetts 4-week comparison (39,194 vs 46,097) is a clear win for HG-DCM, not a draw. The overall point about mixed results still stands but the count was off.
- The critic's claim that metadata details are missing from the main paper (referenced to Appendix A.1, which was stripped by the parser—the original submission contains this information).
- The critic's suggestion that the paper omits discussion of related work on pre-training on epidemiological time series (per rules on missing related work).
- The critic's speculation about the specific causes of the 4-week anomaly (ODE solver non-convergence, catastrophic failures) is not verifiable from the paper and is removed as speculative; the observation that the anomaly exists and is unexplained is retained as a Major weakness.
- The critic's claim that the ABM comparison is a "straw man"—the paper acknowledges the different paradigms and ABMs are part of the SOTA landscape, so this is not a weakness of the paper itself.
- Various presentation nitpicks and formatting observations that are either parser artifacts or trivial.

## Novel Insights

The reviews surface one genuinely novel observation beyond what the paper itself contributes: the paper's rhetorical strategy of selectively reporting mean vs. median MAE depending on which favors HG-DCM. The ablation results (Table 2) reveal a pattern where HG-DCM's mean MAE is worse than CNN's at 2 and 4 weeks (including a catastrophic 10× failure at 4 weeks), but the paper's narrative focuses on median MAE when discussing these comparisons. Conversely, the comparison against DELPHI uses median MAE where HG-DCM wins, but mean MAE would also show wins there. This asymmetry in reporting suggests the narrative was constructed to minimize the appearance of failure cases. The 4-week mean MAE spike—an order of magnitude above both the 2-week and 6-week values—is the single most informative data point in the paper and its absence from the discussion is a notable omission.

## Suggestions

1. **Calibrate claims to evidence.** Replace "consistently and significantly outperforms" with a more measured characterization that acknowledges the method's strengths (strong against DELPHI, GradABM; competitive against EiNNs) but also its failure cases (CNN at early horizons by mean MAE, the anomalous 4-week result).

2. **Investigate and report the 4-week failure.** The 110,452 mean MAE at 4 weeks needs explanation: is it a few catastrophic outliers? A systematic failure mode? Report the fraction of locations where HG-DCM fails, the distribution of errors, and what characterizes those failures.

3. **Add at least two simple baselines** (e.g., ARIMA, exponential growth extrapolation, last-observation persistence) to calibrate the reader's sense of effect size.

4. **Perform a held-out pandemic experiment** to directly test the cross-disease generalization claim that is the paper's central thesis.

5. **Include at least one additional non-MA metric** (e.g., MAPE, growth-rate error) and explicitly report both mean and median throughout without selective omission.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>