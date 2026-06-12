## Summary

This paper introduces HG-DCM, a framework that addresses the "cold-start" problem in pandemic forecasting by transferring knowledge from historical pandemics (Ebola, SARS, Dengue, seasonal influenza) to a novel outbreak. The approach uses a ResNet backbone with metadata to predict parameters of the DELPHI compartmental model, which then generates forecasts via an ODE solver. Experiments on early-stage COVID-19 forecasting across 258 locations demonstrate improvements over standalone DELPHI and a pure CNN baseline, with particularly notable reductions in overshooting behavior.

## Strengths

- **Genuine novelty in cross-disease transfer**: The core idea of learning universal temporal patterns across biologically distinct pandemics and transferring them to a new outbreak is well-motivated and, to my knowledge, underexplored. The paper correctly identifies that human social behavior and intervention responses create shared macroscopic dynamics across outbreaks, providing a principled basis for this transfer.

- **Interpretable parameter predictions**: Unlike black-box deep learning, HG-DCM extracts compartmental model parameters that can be inspected individually. The parameter analysis in Section 3.2.3 (with statistical testing via Wilcoxon signed-rank tests) demonstrates that HG-DCM produces more conservative, realistic parameter estimates compared to DELPHI, which is a meaningful practical advantage for epidemiologists.

- **Well-designed ablation study on 258 locations**: The ablation against DELPHI, CNN, and T-DCM provides a clear decomposition of the contributions of historical guidance, compartmental structure, and deep learning. The T-DCM ablation (no historical data or metadata) is particularly valuable for isolating the effect of the historical transfer mechanism.

- **Thoughtful data augmentation**: The window-shift augmentation with carefully defined LDoA (to prevent information leakage) and the block-masking strategy for the current pandemic demonstrate careful design for the data-scarce setting.

## Weaknesses

### Fatal

None.

### Major

- **Inconsistent and mixed results across metrics and horizons**: The ablation results (Table 2) are more mixed than the paper's narrative suggests. For mean MAE, HG-DCM loses to CNN at 4 weeks by nearly 10× (110,452 vs 11,238) and to T-DCM at 2 weeks. For median MAE, HG-DCM loses to CNN at 6 weeks and DELPHI at 8 weeks. The 4-week mean MAE discrepancy is particularly striking and unexplained — it suggests HG-DCM produces catastrophically poor predictions for certain locations, inflating the mean while the median looks competitive. The paper does not discuss these failures or characterize which locations produce poor results.

- **Very limited external benchmark comparison**: The comparison against GradABM and EiNNs (Table 1) is restricted to only US and Massachusetts due to data/code availability constraints. This severely limits the paper's claim of outperforming "state-of-the-art methods." Moreover, on Massachusetts, EiNNs outperforms HG-DCM at 4-week and 6-week horizons, a result that receives minimal discussion. The paper acknowledges that most COVID-19 Forecast Hub models lack reproducible code, but this does not diminish the weakness of having external validation on only 2 out of 258 locations.

- **Insufficient details on training and hyperparameter selection**: The paper does not describe how β (weight between past and current pandemic losses) was selected, what cross-validation strategy was used, or how hyperparameters were tuned. For a method that trains on heterogeneous historical data and transfers to a new disease, the choice of β is critical and could significantly affect results. This makes reproducibility difficult and raises concerns about potential overfitting of experimental settings.

### Minor

- **Single target disease evaluation**: HG-DCM is only evaluated by transferring from historical diseases to COVID-19. While this is a reasonable proof of concept, the paper makes broad claims about the "new paradigm" without demonstrating the approach works when transferring to other novel pathogens (e.g., a future novel influenza strain or coronavirus).

- **No confidence intervals or statistical testing on forecasting results**: Statistical significance testing is applied to the parameter comparison (Section 3.2.3) but not to the primary forecasting results in Tables 1 and 2. Given the variability across 258 locations, confidence intervals or paired statistical tests on MAE would strengthen the claims considerably.

- **BatchNorm removal justification lacks empirical evidence**: The removal of BatchNorm layers is motivated by distribution shift between historical and current batches, which is reasonable, but no ablation is provided to confirm this design choice contributes to performance.

### Trivial

None.

## Nice-to-Haves

- A visualization or analysis of which historical diseases contribute most to the transfer (e.g., are SARS features more useful than Dengue features for COVID-19 forecasting?)
- Sensitivity analysis on β to show how the balance between historical and current data affects performance
- Error analysis identifying which locations/situations where HG-DCM fails catastrophically (explaining the 4-week mean MAE gap)

## Novel Insights

The paper's key insight — that macroscopic epidemic dynamics driven by human behavior are transferable across biologically distinct pathogens — is genuinely novel and potentially impactful beyond this specific implementation. The empirical finding that historical guidance acts as a form of implicit regularization, preventing the parameter overshooting that plagues standalone compartmental models, is a valuable contribution to the epidemiological modeling community. However, the mixed nature of the results (particularly the 4-week mean MAE collapse and the inconsistent wins across horizons/metrics) somewhat undermines the strength of the conclusion that this approach broadly improves forecasting.

## Suggestions

- Provide a thorough error analysis of the 4-week mean MAE result to understand why HG-DCM produces some catastrophic outliers. Characterize the locations where the model fails and investigate whether certain metadata features or historical disease combinations are responsible.
- Add paired statistical tests (e.g., Wilcoxon signed-rank test across locations) for the primary forecasting MAE comparisons in Tables 1 and 2, mirroring the parameter analysis in Section 3.2.3.
- Report hyperparameter selection details including how β was chosen and what validation protocol was used, as this is critical for reproducibility and for understanding the sensitivity of the method.
- Expand the discussion of Table 1 to honestly address where HG-DCM does not win (EiNNs at 4-week and 6-week Massachusetts).

## Score and Decision

The paper proposes a genuinely novel and well-motivated approach to the important problem of early-stage pandemic forecasting. The cross-disease transfer concept is a valuable contribution that could influence future work in this space. However, the evaluation has significant issues: the external comparison is extremely limited (2 locations), the ablation results are mixed (with an unexplained 10× worse mean MAE at 4 weeks), and key methodological details about training are missing. These issues prevent full confidence in the claims made.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject