## Summary

This paper introduces the History-Guided Deep Compartmental Model (HG-DCM), a framework for early-stage pandemic forecasting that transfers knowledge from historical pandemics to a novel outbreak. The model uses a neural network to predict parameters of a compartmental model (DELPHI) from early time-series data and metadata, trained jointly on past pandemics (Ebola, SARS, Dengue, seasonal influenza) and limited current outbreak data. Experiments on early COVID-19 forecasting across 258 global locations show that HG-DCM reduces overfitting and improves stability compared to standard compartmental models and data-isolated deep learning approaches.

## Strengths

- **Novel and well-motivated problem formulation**: The paper identifies a genuine and important gap—early-stage pandemic forecasting under extreme data scarcity—and proposes a principled solution that mirrors how human epidemiologists reason (drawing on historical patterns). The cross-disease temporal transfer idea is original and clearly distinguished from prior spatial transfer or single-disease approaches.

- **Strong empirical results on the core claim**: The ablation study (Table 2) convincingly demonstrates that historical guidance provides substantial benefit. HG-DCM reduces median MAE by 38.2% (2-week) and 32.4% (4-week) over DELPHI, and the overshooting analysis (Figure 4) provides concrete evidence that historical data acts as a regularizer. The comparison against T-DCM (same architecture without historical data) directly isolates the contribution of cross-disease transfer.

- **Interpretability preserved**: Unlike black-box deep learning models, HG-DCM produces epidemiologically meaningful parameters (infection rate, action timing, etc.) that can be inspected and validated. The parameter inference analysis (Figure 5) shows that HG-DCM yields more stable and realistic parameter distributions than DELPHI, which is valuable for public health decision-makers.

- **Careful data construction and augmentation**: The authors built a new multi-pandemic dataset and designed thoughtful augmentation strategies (window-shift for past pandemics, masking for current pandemic) that respect temporal causality and avoid look-ahead bias.

## Weaknesses

### Fatal
None.

### Major

- **Limited baseline comparison scope**: The main benchmarking (Table 1) is conducted on only two locations (United States and Massachusetts) because "they were the only locations in which there was available data and code for the comparison methods." This is a significant limitation. The paper claims evaluation across 258 global locations for the ablation study, but the comparison against state-of-the-art methods (GradABM, EiNNs) is restricted to a tiny fraction of that set. Without broader benchmarking, it is unclear whether HG-DCM's advantage generalizes across diverse epidemiological settings.

- **The DELPHI baseline comparison is potentially unfair**: The paper compares HG-DCM (trained on historical pandemics + current data) against DELPHI (fit only on current data). This is the intended comparison to demonstrate the value of historical guidance, but the paper does not adequately address whether a simpler approach—such as fitting DELPHI with informative priors derived from historical data—would achieve similar gains. The comparison against T-DCM partially addresses this, but T-DCM uses the same neural architecture without historical data, not a simpler prior-based DELPHI. The contribution of the neural network versus the historical data is not fully disentangled.

- **Evaluation metric choice**: The paper uses MAE on cumulative cases, which is dominated by large-population locations. The median MAE results are more informative but receive less emphasis. Additionally, the paper does not report uncertainty quantification or prediction intervals, which are critical for public health decision-making. The comparison methods (GradABM, EiNNs) may produce probabilistic forecasts, making direct MAE comparison potentially misleading.

- **Data quality and temporal alignment concerns**: The paper acknowledges that older pandemics (Ebola, SARS) have weekly rather than daily data, requiring linear interpolation. This introduces artifacts, especially during the volatile early phase. The paper does not analyze how sensitive results are to this interpolation choice. Furthermore, the "start date" definition (first day cumulative cases exceed 100) may not be comparable across pandemics with vastly different reporting infrastructures.

### Minor

- **The paper overclaims novelty slightly**: While cross-disease temporal transfer is novel, the statement "to our knowledge, this is the first study to develop a forecasting framework that systematically leverages data from multiple prior pandemics" is strong. The related work section could more thoroughly discuss prior work on multi-epidemic learning, even if in different domains (e.g., influenza forecasting across seasons).

- **Limited analysis of which historical pandemics contribute most**: The paper treats all historical pandemics as equally useful, but intuitively, seasonal influenza may be more relevant to COVID-19 than Dengue. An analysis of per-pandemic contribution to the loss or parameter priors would strengthen the understanding of the transfer mechanism.

- **The parameter inference analysis (Figure 5) is descriptive rather than predictive**: Showing that HG-DCM produces different parameter distributions is interesting, but the paper does not validate whether these parameters are more "correct" in any ground-truth sense (e.g., by comparing to independently estimated epidemiological parameters for COVID-19).

### Trivial
None.

## Nice-to-Haves

- Evaluate on a held-out pandemic (not COVID-19) to test true generalization of cross-disease transfer.
- Include probabilistic evaluation metrics (e.g., CRPS, coverage of prediction intervals).
- Analyze sensitivity to the choice of historical pandemics included in training.
- Provide an ablation on the metadata components to identify which features are most informative.

## Novel Insights

The paper's core insight—that the macroscopic dynamics of disease spread are constrained by universal human behavioral patterns rather than pathogen-specific biology, and that this universality can be exploited through a learned mapping from early signals to compartmental model parameters—is genuinely novel and well-supported. This reframes the early-pandemic forecasting problem from "fit a model to sparse data" to "learn a prior over parameter dynamics from history," which is a conceptually important shift. The finding that historical data acts primarily as a regularizer (reducing overshooting) rather than as a source of precise parameter values is a nuanced and valuable observation.

## Suggestions

- Expand the baseline comparison to more locations, even if this requires implementing simpler versions of comparison methods or using the COVID-19 Forecast Hub data with appropriate filtering for early-stage results.
- Add a baseline that uses DELPHI with informative priors derived from historical data (e.g., fitting DELPHI to each historical pandemic and using the resulting parameter distributions as priors) to isolate the contribution of the neural network component.
- Report results stratified by population size or region to show that the improvement is not driven solely by large-population locations.
- Include an analysis of how the interpolation of weekly historical data affects results, perhaps by downsampling daily COVID-19 data to weekly and measuring performance degradation.

## Score and Decision

The paper addresses a genuinely important problem with a novel and well-motivated approach. The core empirical result—that historical guidance significantly improves early-stage forecasting—is convincingly demonstrated through careful ablation studies. However, the limited scope of baseline comparisons (only two locations for state-of-the-art methods) and the lack of a simpler prior-based DELPHI baseline weaken the strength of the claims. The paper is a solid contribution that would benefit from broader evaluation, but as presented, it falls short of the bar for a top venue acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>