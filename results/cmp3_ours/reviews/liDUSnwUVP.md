## Summary

This paper proposes HG-DCM, a framework that uses a deep neural network to predict parameters of a compartmental model (DELPHI) for early-stage pandemic forecasting. The key idea is to train the network on historical pandemic data (Ebola, SARS, Dengue, influenza) alongside early COVID-19 data, enabling "cross-disease temporal transfer" to stabilize forecasts when data for a new pathogen is scarce. The method is evaluated on early-stage COVID-19 forecasting.

## Strengths

1. **Problem framing is well-motivated and important.** Early-pandemic forecasting under data scarcity is a genuine challenge. The analogy to an epidemiologist's mental library of historical curves (lines 19–20) provides a clear intuition for why cross-pandemic knowledge transfer should help.

2. **Method design is internally coherent.** Using a neural network to predict DELPHI compartmental model parameters from time-series and metadata is a natural way to operationalize the stated goal. The removal of BatchNorm (line 75) is a thoughtful modification motivated by the specific challenge of training across heterogeneous pandemics. The data augmentation strategies (window-shift for historical data, masking for current data) are sensible and avoid look-ahead bias.

3. **New multi-pandemic dataset.** The paper constructs and uses a curated dataset of Ebola, SARS, Dengue, and seasonal influenza case data alongside COVID-19 (lines 31–32, 122–124), which is a useful resource for the community.

## Weaknesses

### Major

1. **The evaluation does not isolate cross-disease temporal transfer, which is the paper's central claim.** HG-DCM is trained on a composite dataset that *includes COVID-19 data* alongside historical pandemics: "HG-DCM is trained on a composite dataset of past pandemics, specifically Ebola, SARS, Dengue, and Seasonal Influenza, *alongside the available early-stage data (2–8 weeks) from the current pandemic (COVID-19)*" (line 128). The model is then evaluated on COVID-19. Because COVID-19 data from other locations/time periods appears in training, the improvement over DELPHI could reflect spatial transfer within the same disease rather than cross-disease temporal transfer. A leave-one-pandemic-out evaluation (train on all past pandemics *except* COVID-19, then test on COVID-19) is the standard way to test the core claim and is absent. Without this, the paper cannot substantiate its central thesis.

2. **External benchmarking is conducted on only 2 locations.** Table 1 compares HG-DCM against GradABM and EiNNs on just the United States and Massachusetts (line 138: "These locations were selected because they were the only locations in which there was available data and code for the comparison methods"). The abstract and introduction claim evaluation across "258 global locations" (line 33), but the head-to-head comparison against external methods rests on two data points. No standard time-series baselines (ARIMA, Prophet, simple exponential smoothing) are included, making it difficult to assess whether the advantage is over strong baselines.

3. **Key ablation results contradict the paper's narrative and go unacknowledged.** In Table 2, at 2-week Mean MAE: CNN = 15,600.4, T-DCM = 15,049.2, **HG-DCM = 18,602.6** — HG-DCM is the worst. At 4-week Mean MAE: CNN = 11,238.1, T-DCM = 17,691.2, **HG-DCM = 110,452.4** — HG-DCM is catastrophically worst. The paper claims "CNN generally underperforms HG-DCM across all training horizons" (line 188) and selectively reports the 38.2% *median* MAE reduction while ignoring that HG-DCM is *worse* than a plain CNN in *mean* error at the same horizons. The 4-week Mean MAE of 110,452.4 (vs. CNN's 11,238.1) suggests severe instability — likely a few extreme failures that the median masks. For a public-health forecasting method, this reliability concern needs explanation and is not discussed.

4. **The T-DCM ablation does not isolate the effect of cross-disease transfer.** T-DCM removes *both* historical pandemic data and metadata simultaneously (line 190). Its underperformance relative to HG-DCM could be due to either factor or their combination. A proper ablation would include variants trained on historical pandemics *without* metadata (and vice versa) to identify the source of improvement.

### Minor

1. **MAPE loss is undefined for zero-case days.** The loss function (Eq. 3, 4) uses MAPE with C_ij in the denominator, which is undefined when C_ij = 0 — a common occurrence in early-stage data before an outbreak takes off. The paper does not discuss how zero-case days are handled in the loss computation.

2. **Seasonal influenza data (2009–2023) overlaps temporally with COVID-19 (2020–2023).** Influenza dynamics during 2020–2023 were heavily affected by pandemic-era public health measures (lockdowns, masking). This creates potential confounding: the "historical" data may encode pandemic-era behavioral patterns that are then "transferred" to COVID-19, diluting the biological cross-disease claim.

3. **No statistical significance for forecasting accuracy comparisons.** The parameter analysis uses Wilcoxon tests (Section 3.2.3), but the key forecasting comparisons (Tables 1, 2) lack error bars or significance testing. Given the large mean vs. median discrepancies, this is a notable omission.

4. **DELPHI 4-week Mean MAE anomaly.** In Table 2, DELPHI's 4-week Mean MAE (813,807.8) is roughly 25× larger than its 2-week value (342,686.3) and orders of magnitude above its median (2,619.7), suggesting extreme outliers. The paper does not discuss this.

### Trivial

None.

## Nice-to-Haves

- Reporting uncertainty quantification (prediction intervals) would strengthen the practical contribution.
- Evaluating on a truly novel held-out pathogen (e.g., Mpox/2022, or a later Ebola outbreak) would directly test the cross-disease transfer claim.
- Discussion of computational cost and inference time would be helpful for deployment considerations.

## Removed Points

These points from the input review were removed with justification:

- **"GradABM comparison is comparing fundamentally different tools"** — The asymmetry *favors* the baseline (GradABM uses more data: mobility, interaction). Per the hard rule, this criticism is removed.
- **"No uncertainty quantification"** — Moved to Nice-to-Haves; not standard for this type of compartmental-model hybrid work.
- **"Computational cost not discussed"** — Moved to Nice-to-Haves.
- **"Claim about diversity vs. depth being unsupported"** — This appears in the Discussion section (lines 212–214) as speculation/insight, not as a claimed experimental finding. Removed.
- **"Limitations section doesn't acknowledge fundamental limitations"** — The paper does acknowledge some limitations (weekly vs. daily data, death data exclusion). The criticism is too broad and partly factually incorrect.
- **"Novelty claim overstated"** — The paper qualifies with "To our knowledge" (line 29) and describes a specific combination. Not clearly overclaimed.
- **"Missing related works"** — Cannot verify without external sources per instructions.
- **Formatting and presentation nitpicks** — Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews raise important evaluation-design issues but do not surface novel observations about the method itself beyond what the paper presents.

## Suggestions

1. **Add a leave-one-pandemic-out evaluation.** Train on all pandemics *except* the test pandemic. For COVID-19, this means training on Ebola + SARS + Dengue + Flu only (no COVID-19 in training). This is the minimal experiment needed to substantiate the cross-disease transfer claim.

2. **Add proper ablations to isolate the source of improvement:** (a) HG-DCM without metadata, (b) HG-DCM without historical pandemics (trained on COVID-19 only), (c) HG-DCM without the compartmental constraint (direct end-to-end prediction).

3. **Acknowledge and analyze the failure cases in mean MAE.** The 4-week Mean MAE of 110,452.4 (Table 2) needs explanation. Report the fraction of locations where HG-DCM fails catastrophically and characterize them.

4. **Include standard time-series baselines** (ARIMA, Prophet) to calibrate whether the advantage is over meaningful baselines.

5. **Discuss handling of zero daily cases in the MAPE loss** (Eq. 3, 4).

## Calibration

Anchor papers retrieved (all rounds):

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| PEMs: Pre-trained Epidemic Time-Series Models | DL7JWbdGr3.md | 4.75 | R1 | Directly comparable: same goal (pre-training on multiple diseases for epidemic forecasting). PEMs tested zero-shot on unseen COVID-19; HG-DCM trains on COVID-19 data and tests on COVID-19, making its evaluation weaker. PEMs was rejected. |
| Mechanism-Empowered Multivariate Time Series... Tuberculosis | V83xzYnZ5q.md | 3.00 | R1 | Epidemiological forecasting: weak baselines, single dataset, limited methodology. HG-DCM has stronger motivation and architecture but similar evaluation gaps. |
| Integrated Multi-system Prediction via ESE | w2C7gJqaai.md | 2.33 | R1 | COVID-19 prediction with different methodology. Poorly written, unclear contributions. Not directly comparable. |
| Parameter Optimization for Epidemiological Model | CpiOUOaqh3.md | 2.00 | R1 | Basic SEIR variant with GA optimization. Much simpler method. |
| Overcoming Lookback Window Limitations | hVpAjJPfgZ.md | 3.25 | R1 | Time series forecasting, not disease-specific. |
| Feature-aligned N-BEATS | TS8HoIWAPQ.md | 6.67 | R1 | Time series domain generalization. Stronger evaluation, accepted. |

**Round 1 bracket:** Between 2.5 and 4.5. The most comparable anchor (PEMs, 4.75) has a cleaner evaluation design (zero-shot COVID-19) and was rejected. HG-DCM has a more interesting architectural contribution (neural network → compartmental model parameters) but a meaningfully weaker evaluation (trains on the same disease it tests on, contradictory ablation results unacknowledged). Scores below 3 correspond to papers with more severe problems (poor writing, no clear methodology), which don't apply here.

**Final score determination:** HG-DCM sits between the PEMs paper (4.75, rejected — stronger evaluation but less interesting architecture) and the TB paper (3.00 — weaker approach). The evaluation gap is decisive: the central claim cannot be evaluated from the presented evidence. The score of **3.5** reflects a paper with a genuinely interesting approach and strong motivation, but whose evaluation cannot support its core claims.

## Score and Decision

<score>3.5</score>
<decision>Reject</decision>