## Summary

This paper introduces HG-DCM, a framework that uses a neural network to predict compartmental model (DELPHI) parameters by learning from historical pandemic data (Ebola, SARS, Dengue, seasonal influenza) and transferring that knowledge to early-stage forecasting of a novel pathogen (COVID-19). The core idea — using cross-disease temporal transfer to regularize forecasts when current data is scarce — is well-motivated and practically relevant. The authors constructed a new multi-pandemic dataset and propose several thoughtful design choices (removing BatchNorm for cross-disease robustness, window-shift augmentation with look-ahead prevention).

## Strengths

1. **Well-motivated problem and framing.** The "cold-start" problem in pandemic forecasting is genuinely important and underexplored. The analogy to human epidemiologists drawing on mental libraries of past outbreak curves is compelling (Section 1), and the paper correctly identifies that the bottleneck in early-stage forecasting is data, not architecture.

2. **Multi-pandemic dataset is a logistical contribution.** Assembling time-series data from COVID-19, Ebola, SARS, Dengue, and seasonal influenza with country-level metadata into a unified format is a nontrivial effort (Section 3.1.1). This dataset could be useful to the community.

3. **Principled architectural modification (removing BatchNorm).** The observation that BatchNorm statistics differ across biologically distinct pandemics, and that removing BN layers improves cross-disease generalization (Section 2.1), is a specific, well-motivated design choice grounded in the problem structure.

4. **Thoughtful data augmentation design.** The window-shift augmentation for historical pandemics with the LDoA constraint (preventing look-ahead) and the block-masking strategy for the current pandemic are clearly explained and show careful attention to information leakage (Section 2.2).

## Weaknesses

### Major

1. **Ablation results contradict central claims, and one metric reveals a critical failure mode.** Table 2 shows that HG-DCM's performance is mixed relative to its ablations:

   - **4-week mean MAE anomaly:** HG-DCM scores **110,452** — approximately **10× worse** than the CNN ablation (11,238). The paper offers no explanation for this catastrophic failure.
   - **Claim "CNN generally underperforms HG-DCM across all training horizons" (Section 3.2.2, line 188) is factually incorrect** for mean MAE at 2 weeks (CNN 15,600 vs HG-DCM 18,603) and 4 weeks (CNN 11,238 vs HG-DCM 110,452).
   - **Claim "HG-DCM consistently outperforms DELPHI across forecasting horizons" (Section 3.2.2, line 170) is overstated.** While true for mean MAE at all horizons, for median MAE at 8 weeks DELPHI (538) beats HG-DCM (796). The paper acknowledges 6-week median is "comparable" but omits the 8-week reversal.
   - On the full 8-cell ablation table (4 metrics × 2 aggregation methods), HG-DCM wins only 4 cells; CNN wins 2, DELPHI wins 1, T-DCM wins 1.

   The 4-week mean MAE outlier (110,452) is especially concerning — it suggests either a systematic instability (e.g., certain locations trigger catastrophic failures) or a pipeline issue. Since this not discussed, confidence in the method's reliability is undermined.

2. **The baseline comparison is limited to two locations, reducing benchmarking to a case study.** The main comparison against GradABM and EiNNs (Table 1) covers only the United States and Massachusetts. The paper acknowledges this constraint ("These locations were selected because they were the only locations in which there was available data and code for the comparison methods," Section 3.2.1) but does not compensate by including even simple baselines that could be run across all 258 locations (e.g., ARIMA, exponential curve fits, naive persistence). The reader cannot assess how HG-DCM performs in general relative to any reasonable alternative.

3. **The evaluation is limited to a single pandemic (COVID-19).** The paper's core thesis is that historical pandemics improve forecasting of *novel* pathogens — yet the method is validated only on COVID-19, the very pandemic that dominates the training data. A retrospective evaluation (e.g., training on pre-2009 data and testing on 2009 H1N1) would have substantially strengthened the claim. The paper acknowledges this only implicitly and does not treat it as the fundamental limitation it is.

4. **The contribution of cross-disease transfer is not cleanly isolated from cross-location sharing and neural network capacity.** HG-DCM trains one neural network across all 258 COVID-19 locations plus historical pandemics, while DELPHI fits parameters per location independently. The T-DCM ablation removes historical data *and* metadata simultaneously, and still uses cross-location sharing. Thus, the apparent advantage of HG-DCM over DELPHI could arise from (a) cross-location parameter sharing, (b) greater model capacity, or (c) the metadata — not necessarily from cross-disease transfer. A cleaner control would hold metadata and cross-location sharing fixed while only toggling historical pandemic data.

5. **The loss function uses MAPE (|(C_{ij} - \hat{C}_{ij})/C_{ij}|) which is undefined when C_{ij}=0** (Equations 3–4, Section 2.2). This occurs during very early pandemic phases, and the paper does not explain how zero actual cases are handled (e.g., epsilon smoothing, sample exclusion, or domain masking).

### Minor

6. **Overshooting reduction is attributed to historical data, but the CNN ablation also shows few overshoots without historical data.** Figure 4a shows both HG-DCM and CNN have drastically fewer overshoots than DELPHI. The paper states "HG-DCM, by leveraging historical pandemic information, reduced overfitting" (Section 3.2.2), but the CNN result suggests the low overshooting may come from cross-location sharing or neural network regularization rather than historical data specifically.

7. **Parameter inference analysis (Section 3.2.3) shows statistical significance but does not demonstrate that HG-DCM's parameters are "more conservative and realistic."** The Wilcoxon test confirms distributions differ (p < 0.05), but labeling lower infection rates as "more realistic" conflates statistical difference with correctness. Without independent ground truth for the "correct" parameters, this analysis is suggestive but not evidential.

8. **The masking augmentation for the current pandemic is not ablated.** The paper describes the block-masking strategy (Section 2.2) but never measures its contribution to performance relative to the window-shift augmentation for historical data.

### Trivial

None.

## Nice-to-Haves

- The paper does not report confidence intervals or variance measures for the main results (Tables 1, 2). Reporting variability across random seeds or bootstrapped samples would strengthen conclusions.
- Computational cost (training time, inference time, hardware) is not reported. For a method targeting rapid deployment during an emerging crisis, practical feasibility matters.
- The window-shift augmentation creates training samples with substantial temporal overlap. Discussing the effective number of independent samples would aid interpretation.

## Removed Points

These points from the input review were removed with justifications:

- **"Methods section underspecified (depth, filters, kernel sizes)"** — The paper references Appendix A.2 for baseline setups and Section A.1 for metadata. The appendix was stripped by the parser; this is not an author omission.
- **"Training procedure details not in main text"** — Also deferred to the stripped appendix.
- **"No confidence intervals or measures of variance"** — Moved to Nice-to-Haves (not standard in all pandemic forecasting work, but would strengthen the paper).
- **"Hyperparameters and training details"** — Appendix stripped.
- **"Window-shift augmentation overlap reduces effective sample size"** — Speculative; the reviewer does not quantify the effect, and temporal overlap in augmentation is standard practice.
- **"Computational cost not reported"** — Moved to Nice-to-Haves.
- Criticism about missing related works — not included as per rules (cannot confirm existence of works not mentioned in the paper).
- Formatting nitpicks, typos, parser artifacts — removed per rules.
- The strength about "this paper addressed an important problem" — generic, surface-level. Removed.
- The strength about the paper "establishing a new paradigm" — while the paper makes this claim, as a strength it is too closely tied to the reviewer's opinion rather than concrete evidence in the paper. Removed.

## Novel Insights

The most interesting finding from cross-referencing the reviews is the tension between the paper's conceptual contribution and its empirical support. The idea of cross-disease temporal transfer for pandemic forecasting is genuinely novel and well-motivated by the analogy to human epidemiologists' reasoning. However, the ablation results reveal that the value of the specific instantiation (ResNet + DELPHI) is inconsistent: the method outperforms its ablations on some metrics and horizons but is dramatically worse on others (the 4-week mean MAE anomaly). This pattern suggests that the contribution may be real but fragile, and that the paper's claims of "consistent" outperformance are not matched by the data. The failure to cleanly disentangle cross-disease transfer from cross-location sharing further muddies what the actual source of improvement is. None of this invalidates the core idea, but it means the paper's evidence is substantially weaker than its rhetoric suggests.

## Suggestions

1. **Explain the 4-week mean MAE anomaly.** If this is driven by a small number of outlier locations, identify and analyze them. If it reflects a systematic instability (e.g., the model fails when given exactly 4 weeks of data), this is critical for users to know.
2. **Add simple baselines across all 258 locations.** Even a naive persistence forecast, exponential curve fit, or ARIMA model would allow the reader to gauge HG-DCM's general performance level.
3. **Conduct a cleaner ablation that isolates cross-disease transfer by keeping metadata and cross-location sharing but removing only historical pandemic data.** The current T-DCM removes both, introducing a confound.
4. **Tone down claims that are contradicted by the reported data.** "CNN generally underperforms HG-DCM across all training horizons" is not supported by Table 2.
5. **Address the MAPE undefined-at-zero issue** in the loss function (Equations 3–4).

## Score and Decision

HG-DCM addresses a genuinely important underexplored problem and the core idea is compelling. The multi-pandemic dataset and several design choices are worthwhile contributions. However, the paper's evidence does not match the strength of its claims. The ablation results are mixed, including one dramatic failure mode (4-week mean MAE 10× worse than the CNN ablation) that is not discussed. The baseline comparison is limited to two locations, and the method is only validated on COVID-19. The central contribution — cross-disease transfer — is not cleanly isolated from alternative explanations (cross-location sharing, model capacity, metadata). In its current form, the conclusions overreach the evidence by a wide margin.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>