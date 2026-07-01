## Summary

This paper introduces a nonlinear multimodal encoding model for predicting fMRI brain responses to naturalistic speech, combining audio features from Whisper and semantic features from LLaMA via a single-hidden-layer MLP with PCA preprocessing. The authors report relative improvements of 17.2% (r²) and 17.9% (normalized correlation) over a unimodal linear baseline, and 7.7% and 14.4% over a prior state-of-the-art linear ensemble. They further analyze brain organization using variance partitioning and a novel RED-based clustering metric, interpreting results in light of neurolinguistic theories.

## Strengths

- **Addresses an important gap**: Speech encoding fMRI has predominantly used linear unimodal models, while vision encoding has moved to nonlinear approaches. The paper systematically demonstrates that nonlinear multimodal encoding is feasible and beneficial for naturalistic speech.
- **Systematic ablation design**: The comparison of Linear, MLLinear, DIMLP, and MLP architectures cleanly isolates the effects of nonlinearity, dimensionality reduction, and cross-modal interactions.
- **Rich analysis beyond prediction**: Variance partitioning, RED-based clustering, and ROI-wise interpretation provide a multi-faceted view of how multimodal information is organized in the brain, connecting to established neurolinguistic theories.
- **Uses a large public dataset** (LeBel et al., 2023) with 20 hours of data per subject, enabling more complex modeling than typical smaller fMRI language datasets.

## Weaknesses

### Fatal
None.

### Major

1. **Overstated improvement claims relative to the strongest baseline**: The paper emphasizes a 17.2% improvement over the unimodal linear baseline, but the best linear multimodal model (all voxels) achieves 4.10% r², while the proposed MLP achieves 4.29%—a relative improvement of only ~4.6%. The 17.2% figure is against a weaker baseline, not the state-of-the-art linear model. The abstract and introduction should clearly distinguish these comparisons.

2. **Variance partitioning method is not described in the main text**: The critical analysis of unique vs. joint contributions (Figure 3, Section 3.3) relies on a variance partitioning method that is only referenced to Appendix M.2. Without an explanation of how nonlinear variance is decomposed (e.g., Shapley values, sequential R², or other approaches), the results are uninterpretable. This is a core methodological gap.

3. **Lack of statistical significance for main results**: Table 1 reports average r² and CC_norm without confidence intervals, error bars, or significance tests. The paper refers to Appendix C for statistical analysis, but the main text should include at least basic uncertainty quantification (e.g., bootstrap intervals or subject-wise variability) to support the claimed improvements.

4. **RED-based clustering improvements are marginal and unvalidated**: The modularity Q values (nonlinear 0.155 vs. linear 0.145 vs. FC 0.068) show small differences, and no statistical test or error bar is provided. The claim of "clearer functional groupings" is not convincingly supported, especially given the visual similarity of the dendrograms in Figure 1.

5. **Single nonlinear architecture tested**: Only a one-hidden-layer MLP is evaluated. The paper argues that deeper models overfit, but does not explore other nonlinear approaches (e.g., kernel methods, random forests, or regularized deeper networks). The conclusion that "nonlinearity is the key driver" rests on a single architecture.

### Minor

- **Only three subjects**: While common in fMRI speech encoding, the small N limits generalizability. The paper acknowledges this but does not discuss potential subject-specific biases or the stability of the observed patterns.
- **Comparison with prior SOTA is not fully controlled**: The baseline from Antonello et al. (2024) uses full voxel linear regression, while the proposed method uses PCA + MLP. The paper includes a multimodal linear model on all voxels (4.10% r²) which is a fairer comparison, but the narrative still emphasizes the unimodal baseline.
- **DIMLP architecture is a specific choice**: The conclusion that cross-modal nonlinear interactions are important relies on the comparison between MLP and DIMLP. The improvement is small (4.29% vs. 4.18% r²), and other fusion methods (e.g., cross-attention) are not tested.

### Trivial

- Figure 1 caption appears duplicated in the text.
- Some ROI abbreviations are not defined in the main text (though Appendix A is referenced).

## Nice-to-Haves

- Include confidence intervals or bootstrap error bars for all main performance metrics (Table 1).
- Provide a clear description of the variance partitioning method in the main text, or at minimum a summary of the approach.
- Test additional nonlinear architectures (e.g., kernel ridge regression, deeper MLPs with dropout) to strengthen the claim that nonlinearity is beneficial.
- Validate the RED metric against other temporal analysis methods (e.g., temporal receptive fields, dynamic RSA).

## Novel Insights

The paper demonstrates that nonlinear multimodal encoding is feasible for speech fMRI and can reveal distributed multimodal processing patterns that are less apparent with linear models. The RED-based clustering approach is a novel way to capture spatiotemporal dynamics of modality-specific processing. However, the core insight—that nonlinearity and multimodality improve encoding—is not surprising given analogous findings in vision, and the modest effect sizes limit the novelty of the specific results.

## Suggestions

- Reframe the main claims to honestly reflect the improvement over the best linear multimodal model (~4.6% relative in r²) rather than only the unimodal baseline.
- Add statistical significance tests (e.g., subject-wise paired t-tests or bootstrap) for all key comparisons in Table 1 and Figure 1.
- Explain the variance partitioning method in the main text or ensure the appendix description is self-contained and accessible.
- Consider a cross-validation scheme that accounts for the hierarchical structure of the data (sessions, stories) to better estimate generalization.

## Score and Decision

**Score**: 4.0  
**Decision**: Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>