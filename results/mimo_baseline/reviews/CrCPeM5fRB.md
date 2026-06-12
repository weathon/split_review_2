## Summary

This paper proposes the Signal Dice Similarity Coefficient (SDSC), a structure-aware reconstruction loss for time-series self-supervised learning that extends the Dice Similarity Coefficient from segmentation to continuous signals. SDSC is integrated into the reconstruction branch of SimMTM while keeping its contrastive objective fixed, enabling controlled comparison with MSE and other losses. Experiments on forecasting and classification benchmarks show mixed results, with SDSC achieving modest gains mainly in frozen in-domain classification settings.

## Strengths

- **Well-motivated problem**: The paper clearly articulates why MSE is inadequate for capturing structural fidelity in time-series signals, supported by concrete examples (Table 1, Figure 1) showing MSE's insensitivity to polarity reversal, scale distortion, and zero-baseline signals. This is a legitimate concern for physiological signals like EEG/ECG.

- **Controlled experimental design**: By replacing only the reconstruction loss in SimMTM while keeping the contrastive objective (InfoNCE) identical, the paper isolates the contribution of the reconstruction objective cleanly. This is a sound methodological choice that avoids confounding factors.

- **Hybrid loss formulation**: The combination of SDSC with MSE using uncertainty-based weighting (Kendall et al., 2018) is a practical and well-motivated design choice that addresses SDSC's amplitude blindness. The hybrid consistently performs well across settings.

- **Comprehensive baselines**: The paper compares against MSE, SoftDTW, PCC, and SI-SNR, providing a thorough landscape of alternative objectives rather than just the vanilla MSE baseline.

## Weaknesses

### Fatal

None.

### Major

- **Inconsistent and marginal experimental improvements**: The evidence for SDSC's effectiveness is weak across settings. Forecasting gains (Table 4) are negligible—SDSC achieves 0.294 vs. MSE's 0.295 MSE on average, essentially noise. For frozen classification (Table 5), SDSC improves in-domain (+1.2% accuracy) but loses in cross-domain (-0.55% accuracy). For fine-tuned classification (Table 6), PCC outperforms both MSE and SDSC in in-domain, and MSE dominates in cross-domain. The paper's abstract claims "comparable or improved performance," which technically holds but is misleading—the improvements are fragile and setting-dependent.

- **Cherry-picked presentation**: Table 4 shows only Electricity (a single favorable dataset) alongside averages, while the paper refers to full results in the appendix. The pre-training table (Table 2) shows SDSC achieving higher reconstruction errors than MSE on distance-based metrics for forecasting, and for classification, SoftDTW achieves the best pre-training MSE while SDSC scores high on SDSC. The paper does not convincingly argue why this translates to downstream value.

- **Limited backbone generalizability**: All experiments use only SimMTM. The paper provides no evidence that SDSC benefits transfer to other pre-training frameworks (TI-MAE, TS2Vec, TimesNet, etc.), making it impossible to assess whether SDSC's value is architecture-dependent or general.

- **Questionable structure-awareness for sign-sensitive signals**: SDSC uses H(S(t)) to require sign agreement, meaning a signal with a 1-sample phase offset that flips polarity at even a few points receives severe penalties. For signals like EEG or ECG (the paper's stated motivation), where phase varies across channels and subjects, this aggressive sign sensitivity could be counterproductive. The paper acknowledges SDSC is "not tolerant to global shifts" but does not analyze when this property harms rather than helps.

### Minor

- **Missing computational cost analysis**: The paper claims SDSC's "linear complexity" is a selling point over SoftDTW's quadratic complexity, but provides no actual runtime or memory comparisons despite running on 2× 3090 GPUs.

- **Sensitivity analysis incomplete**: α=10 for the sigmoid approximation is stated as chosen "based on analysis in Appendix A.3," but the main paper provides no indication of how sensitive results are to this parameter. The paper mentions "excessively large values of α can lead to sharp transitions that result in unstable gradients" without empirical evidence.

- **Weak correlation argument**: The Pearson correlation of -0.324 between MSE and SDSC (Figure 3a) is presented as evidence that "MSE-based SSL captures structural features to some extent but lacks reliability," but a weak negative correlation simply means the metrics are not strongly coupled—not that one is unreliable.

- **Missing ablation of hybrid weighting strategy**: The uncertainty-based weighting is adopted from Kendall et al. (2018) without comparison to simpler alternatives (equal weighting, grid search). The paper mentions "controlled evaluation using frozen λ=0.5" in the appendix but the main paper should discuss this comparison.

### Trivial

None.

## Nice-to-Haves

- Experiments on at least one additional backbone to support generalizability claims.
- Runtime/memory comparison table for SDSC vs. SoftDTW vs. MSE during pre-training.
- Analysis of what types of signals or domains benefit most from SDSC versus MSE, going beyond "depends on dataset characteristics."
- Sensitivity curves for α across a range of values.

## Novel Insights

The paper's core observation—that MSE and SDSC are weakly correlated in learned representations, and that models pre-trained with SDSC achieve tighter SDSC distributions at matched MSE levels—is genuinely interesting and suggests that reconstruction losses shape representations in partially orthogonal ways. However, this insight remains underdeveloped: the paper does not explain mechanistically why structural alignment aids downstream tasks or identify which signal characteristics determine when SDSC is preferable to MSE.

## Suggestions

- Provide a practical decision framework backed by empirical signal characteristics (e.g., waveform complexity, sign variability, amplitude sensitivity) rather than the vague guideline mentioned in Appendix A.14.
- Include at least one experiment with a different backbone (e.g., replacing MSE with SDSC in TI-MAE or a contrastive-only framework) to demonstrate generalizability.
- Add a computational cost comparison table as a main-text result, since efficiency is a stated advantage over SoftDTW.
- Analyze the failure mode where SDSC's sign-agreement requirement hurts performance (e.g., on signals with high phase variability) with concrete examples.

## Score and Decision

The paper addresses a legitimate concern about MSE's limitations for time-series representation learning, but the experimental evidence is insufficient to support strong claims. The improvements are marginal in forecasting, inconsistent across classification settings (with SDSC losing in cross-domain and after fine-tuning), and demonstrated on only a single backbone. The methodological contributions—extending DSC to continuous signals and adding a sigmoid approximation—are incremental rather than transformative. The paper reads more as an exploratory study than a definitive contribution.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>