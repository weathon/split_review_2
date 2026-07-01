## Summary

This paper introduces the History-Guided Deep Compartmental Model (HG-DCM), a framework for early-stage pandemic forecasting that combines a neural network parameter predictor with a compartmental epidemiological model (DELPHI). The key innovation is training the neural network on data from multiple historical pandemics (Ebola, SARS, Dengue, seasonal influenza) to learn universal patterns of disease spread, which then regularizes and stabilizes predictions for a novel pandemic (COVID-19) when only 2-8 weeks of data are available. Experiments on early COVID-19 forecasting across 258 global locations show that HG-DCM reduces overfitting and improves forecasting accuracy compared to standard compartmental models and data-isolated deep learning approaches.

## Strengths

- **Novel and well-motivated problem formulation**: The paper identifies a genuine and important gap—the "cold-start" problem in pandemic forecasting—and proposes a principled solution: cross-disease temporal transfer learning. The argument that macroscopic spread dynamics are constrained by human behavior rather than pathogen biology is compelling and well-articulated.

- **Clean architectural design**: The two-stage pipeline (neural network predicts compartmental model parameters, then ODE solver generates forecasts) is elegant and preserves interpretability. The removal of Batch Normalization layers to avoid cross-pandemic batch statistics instability is a thoughtful, principled design choice.

- **Comprehensive ablation study**: The paper systematically isolates the contributions of historical guidance (T-DCM vs. HG-DCM), mechanistic constraints (CNN vs. HG-DCM), and the compartmental backbone (DELPHI vs. HG-DCM). The results clearly demonstrate that each component contributes meaningfully to overall performance.

- **Parameter inference analysis**: The paper goes beyond forecasting accuracy to analyze the inferred epidemiological parameters, showing that HG-DCM produces more stable and realistic parameter estimates than DELPHI alone. This provides mechanistic insight into *why* the model works, not just that it works.

## Weaknesses

### Fatal
None.

### Major

- **Limited baseline comparison**: The paper compares against only two baselines (GradABM and EiNNs) on only two locations (US and Massachusetts). The authors acknowledge that most COVID-19 Forecast Hub models lack reproducible code, but this severely limits the strength of the empirical claims. The ablation study is more comprehensive (258 locations), but the main benchmarking table (Table 1) is too narrow to convincingly demonstrate state-of-the-art performance.

- **Potential data leakage concern**: The model is trained on historical pandemics (Ebola, SARS, Dengue, influenza) and evaluated on COVID-19. However, the "past pandemic" dataset includes seasonal influenza data from 2009-2023, which overlaps with the COVID-19 evaluation period (2020). While influenza is biologically distinct from COVID-19, the temporal overlap means the model could learn patterns from the COVID-19 era (e.g., behavioral changes, testing practices) that are encoded in influenza data from 2020-2023. The paper does not address this potential leakage.

- **Unclear generalization to truly novel pathogens**: The paper evaluates only on COVID-19, which is a respiratory virus with transmission dynamics similar to influenza. The claim that the framework generalizes to "any" novel pathogen is unsupported. A truly novel pathogen with fundamentally different transmission modes (e.g., vector-borne, sexually transmitted) might not share the "universal patterns" the model learns from respiratory and vector-borne historical diseases.

### Minor

- **The window-shift augmentation for past pandemics uses the "first wave" peak (LDoA) identified retrospectively from the full time series**. While the authors correctly note this is not used during inference, the augmentation strategy means the model is trained on input windows that are guaranteed to contain the rising phase of an outbreak. During inference on a novel pandemic, the model receives windows that may or may not be in the rising phase. This training-inference mismatch could affect performance.

- **The loss function (Eq. 3-5) uses MAPE, which is undefined when true cases are zero**. The paper mentions setting negative daily cases to zero but does not discuss how zero-valued cumulative cases are handled in the MAPE term.

- **The paper claims HG-DCM is evaluated on 258 global locations (Section 3.1) but the main benchmarking table (Table 1) only shows results for 2 locations**. The ablation study (Table 2) appears to use more locations, but the exact number and which locations are not clearly stated.

### Trivial
- The paper uses "geological" metadata when it likely means "geographical" or "demographic" metadata.

## Nice-to-Haves

- Evaluate on a held-out historical pandemic (e.g., train on all historical data except SARS, then test on SARS) to demonstrate generalization to a truly unseen pathogen within the historical dataset.
- Include uncertainty quantification in the forecasts, which is critical for public health decision-making.
- Provide an analysis of which historical pandemics contribute most to the transfer learning signal (e.g., does influenza help more than Dengue?).

## Novel Insights

The paper's core insight—that cross-disease temporal transfer learning can regularize compartmental models in data-scarce settings—is genuinely novel and practically important. The observation that removing Batch Normalization improves cross-pandemic generalization is a non-obvious architectural insight that could benefit other transfer learning settings with heterogeneous source domains. The demonstration that historical data acts as a regularizer rather than just additional training data (i.e., it stabilizes parameter estimates rather than just improving point predictions) provides a useful conceptual framework for thinking about knowledge transfer in epidemiological modeling.

## Suggestions

1. **Address the temporal overlap concern**: Either exclude influenza data from 2020-2023, or explicitly test whether the model's performance degrades when trained only on pre-2020 influenza data. This would strengthen the claim that the model learns universal patterns rather than COVID-era artifacts.

2. **Expand baseline comparison**: Even if code is unavailable, compare against published results from the COVID-19 Forecast Hub for the same locations and time periods. Many models reported weekly forecasts that could be used for approximate comparison.

3. **Clarify the evaluation setup**: State explicitly how many locations are used in the ablation study (Table 2), which locations they are, and whether the same 258 locations are used across all experiments.

4. **Test on a non-respiratory pathogen**: If possible, evaluate on a held-out historical pandemic with different transmission characteristics (e.g., train on respiratory diseases and test on vector-borne, or vice versa) to probe the limits of the "universal patterns" assumption.

## Score and Decision

This paper addresses a genuine and important problem with a well-motivated, cleanly designed solution. The core idea—cross-disease temporal transfer learning for compartmental model regularization—is novel and practically significant. The ablation study is thorough and convincingly demonstrates the contribution of each component. However, the limited baseline comparison (only 2 locations for the main benchmark) and the potential data leakage from overlapping influenza/COVID-19 time periods weaken the empirical claims. The paper would benefit from addressing these concerns, but the contribution is solid and the methodology is sound.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>