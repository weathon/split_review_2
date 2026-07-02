## Summary

This paper introduces the History-Guided Deep Compartmental Model (HG-DCM), a framework that combines deep learning with compartmental epidemiological models to forecast pandemics during their early stages when data is extremely scarce. The key innovation is a cross-disease knowledge transfer mechanism: a neural network learns to map early outbreak signals and metadata to compartmental model parameters by training on a curated dataset of historical pandemics (Ebola, SARS, Dengue, seasonal influenza), then applies this learned mapping to forecast a novel pathogen like COVID-19. Experiments on early COVID-19 forecasting across 258 global locations show that HG-DCM reduces overfitting and improves stability compared to standard compartmental models and data-isolated deep learning approaches.

## Strengths

- **Novel and well-motivated problem formulation**: The paper identifies a genuine and important gap—early-stage pandemic forecasting when data is too sparse to calibrate standard models. The idea of transferring knowledge across biologically distinct pandemics by learning universal human-driven dynamics of spread is creative and grounded in epidemiological intuition.

- **Clean architectural design**: The two-stage pipeline (deep learning parameter predictor + compartmental ODE solver) is elegant and preserves interpretability. The removal of Batch Normalization to avoid cross-pandemic distribution shift is a thoughtful, principled design choice. The use of DELPHI as the compartmental backbone leverages a well-established, high-performing model.

- **Comprehensive ablation study**: The paper systematically isolates the contributions of historical guidance (T-DCM vs HG-DCM), mechanistic constraints (CNN vs HG-DCM), and the full framework (DELPHI vs HG-DCM). The results clearly demonstrate that each component contributes meaningfully, with the full HG-DCM outperforming all ablations.

- **Practical significance**: The 38.2% reduction in median MAE with 2 weeks of training data and the dramatic reduction in overshooting events (Figure 4a) represent practically meaningful improvements for public health decision-making during the critical early window of a pandemic.

## Weaknesses

### Major

- **Limited baseline comparison scope**: The main benchmarking (Table 1) is conducted on only two locations (United States and Massachusetts) due to "limited data accessibility to run the comparison models." This is a significant limitation—258 locations are used for the ablation study, but the head-to-head comparison against state-of-the-art methods is restricted to just 2 locations. The paper acknowledges this but does not adequately address why broader comparison was infeasible or provide alternative evidence that the results generalize.

- **The "past pandemic" dataset is dominated by seasonal influenza**: The training set includes Ebola, SARS, Dengue, and seasonal influenza. Seasonal influenza is fundamentally different from COVID-19 in transmission dynamics, severity, and public health response. The paper's central claim that "macroscopic dynamics of spread are universally constrained by human social behavior" is plausible but requires stronger evidence that influenza patterns actually transfer to COVID-19. The ablation study shows HG-DCM outperforms T-DCM (no historical data), but does not isolate which historical pandemics contribute most to the transfer.

- **Evaluation metric choice**: The paper uses MAE on cumulative cases, which is a reasonable metric but has known limitations. Cumulative MAE can be dominated by the final time point and does not capture trajectory shape. The paper would benefit from additional metrics (e.g., symmetric MAPE, pinball loss for quantile evaluation, or metrics that penalize timing errors differently from magnitude errors). The overshooting analysis (Figure 4a) is a good step but is not formalized as a primary evaluation metric.

### Minor

- **The masking augmentation for the current pandemic** (randomly zeroing 7-day segments) is described but its impact is not ablated. It is unclear whether this augmentation meaningfully improves performance or is a minor detail.

- **The parameter inference analysis (Figure 5)** shows statistically significant differences between DELPHI and HG-DCM parameters, but the interpretation is somewhat circular: HG-DCM predicts "more conservative and realistic estimates" because it was trained to match historical patterns. The paper does not validate whether these inferred parameters are actually more biologically plausible or just different.

- **The loss function** combines MAE and MAPE with a weighting parameter α, and past/current losses with a weighting parameter β. The values of α and β are not reported, and no sensitivity analysis is provided. This makes reproducibility harder and leaves open questions about how sensitive results are to these hyperparameters.

### Trivial

- The paper states "To our knowledge, this is the first study to develop a forecasting framework that systematically leverages data from multiple prior pandemics to predict the trajectory of a newly emerging one." This is a strong claim that would benefit from a more thorough literature search, but given the paper's own related work section, it appears to be a reasonable claim.

## Nice-to-Haves

- A per-pandemic ablation showing which historical datasets contribute most to COVID-19 forecasting performance (e.g., train on influenza only, SARS only, all but influenza, etc.)
- Uncertainty quantification for the forecasts (e.g., prediction intervals) would significantly increase practical utility for decision-makers
- A sensitivity analysis on the loss weighting parameters α and β
- Evaluation on a held-out pandemic (not COVID-19) to demonstrate generalizability of the approach

## Novel Insights

The paper's core insight—that the macroscopic dynamics of disease spread are driven more by universal human behavioral patterns than by pathogen-specific biology, and that this can be exploited for cross-disease transfer learning—is genuinely novel and well-articulated. The idea of using a neural network to map early signals to compartmental model parameters, with the network trained across multiple historical pandemics, is a creative synthesis of mechanistic modeling and data-driven learning. The paper convincingly demonstrates that in data-scarce regimes, the diversity of training signal (across pandemics) matters more than architectural complexity, which is a valuable lesson for the broader ML community working on time-series forecasting with limited data.

## Suggestions

1. Expand the baseline comparison to more locations, even if it requires simplifying the baseline implementations or using a subset of locations where all methods can run. At minimum, provide a clear explanation of why broader comparison was infeasible and what steps were taken to ensure the 2-location results are representative.

2. Add trajectory-shape metrics (e.g., dynamic time warping distance, or pinball loss at multiple quantiles) to complement cumulative MAE, and report results separately for the peak timing and peak magnitude.

3. Conduct a per-pandemic ablation to identify which historical datasets drive the transfer learning benefit, and discuss whether the approach would work for a pandemic that is truly novel (e.g., no similar historical analog).

4. Report the values of α and β in the loss function and include a sensitivity analysis showing how performance varies with these hyperparameters.

## Score and Decision

The paper addresses a genuinely important problem with a creative, well-motivated solution. The experimental design is thoughtful, the ablation study is comprehensive, and the results are convincing within the scope presented. The main limitations are the narrow baseline comparison (2 locations) and the lack of per-pandemic ablation to validate the cross-disease transfer hypothesis. These are significant but not fatal—the paper's core contribution is novel and the evidence, while not exhaustive, is sufficient to support the claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>