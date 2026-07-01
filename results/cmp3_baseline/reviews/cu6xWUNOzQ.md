## Summary

This paper introduces a nonlinear multimodal encoding model for predicting fMRI brain responses to naturalistic speech. The model combines semantic features from LLaMA and audio features from Whisper via a single-hidden-layer MLP applied to PCA-reduced voxel responses. The authors report relative improvements of 17.2% in r² and 17.9% in normalized correlation over a unimodal linear baseline, and 7.7%/14.4% over prior linear ensemble methods. Additional analyses using variance partitioning and a novel RED-based clustering method aim to reveal distributed multimodal processing patterns across the cortex.

## Strengths

- **Systematic comparison of architectures and modalities.** The paper evaluates multiple encoder types (Linear, MLLinear, DIMLP, MLP) and modality combinations (text-only, audio-only, multimodal), providing a clear picture of where gains come from.
- **Introduction of RED-based spatiotemporal clustering.** The Relative Error Difference metric preserves temporal dynamics and enables joint spatial-temporal analysis of prediction errors, offering a potentially useful tool for studying brain organization.
- **Variance partitioning analysis.** The decomposition of explained variance into unique semantic, unique audio, and joint contributions provides interpretable insights into how different brain regions integrate multimodal information.
- **Consistent improvements across layers and regions.** The nonlinear MLP outperforms linear models across all layers of both language and audio models, and the gains are widespread across cortical regions, suggesting the effect is robust.

## Weaknesses

### Fatal
None.

### Major

1. **Low absolute prediction performance and modest absolute gains.** The best model achieves only 4.29% average r². The absolute improvement over the linear baseline is 0.19 percentage points in r² and 2.96 percentage points in normalized correlation. While relative percentages sound large, the practical significance of such small absolute gains for downstream applications (e.g., decoding, in-silico testing) is unclear and not discussed.

2. **Unfair comparison with prior state-of-the-art.** The baseline (Antonello et al., 2024) uses multiple Whisper layers and linear stacked regression, while the proposed method uses only the final layer and direct concatenation. The paper attributes the improvement to nonlinearity and multimodality, but differences in feature extraction and fusion strategy are confounded. A controlled ablation (e.g., using the same feature pipeline with and without nonlinearity) is missing.

3. **Lack of statistical rigor.** With only three subjects, the paper does not report subject-level performance or statistical tests for the overall model comparisons. The ROI analyses use FDR correction, but the main claims about model superiority are not supported by significance tests (e.g., paired permutation tests across voxels or subjects). The modularity differences in RED clustering (0.155 vs. 0.145 vs. 0.068) are reported without any measure of uncertainty or significance.

4. **PCA on the response variable is a critical design choice with insufficient justification.** The model predicts 512 PCA components rather than raw voxels, then inverse-projects to voxel space. This introduces potential information loss and makes voxel-wise comparisons indirect. The paper does not show that results are robust to the number of PCA components, nor does it compare with alternative dimensionality reduction methods or full-voxel models with appropriate regularization.

5. **Neuroscientific interpretations are speculative and not strongly supported.** The paper claims alignment with Motor Theory of Speech Perception, Convergence-Divergence Zone model, and embodied semantics based on correlational patterns in variance partitioning and prediction improvements. Alternative explanations (e.g., quasi-semantic factors, articulatory demands) are acknowledged but not tested. The evidence is insufficient to support strong theoretical claims.

6. **RED-based clustering lacks validation.** The clustering analysis is presented as a key contribution, but there is no quantitative validation (e.g., comparison to known functional networks, stability analysis, permutation tests). The modularity values are low, and it is unclear whether the observed groupings are meaningful or driven by noise.

### Minor

- The paper claims "first time" for nonlinear multimodal encoding in naturalistic speech, but prior nonlinear work in language encoding exists (e.g., Moussa et al., 2024; Vatikonda et al., 2025). The novelty is more in the specific combination for speech fMRI, which is incremental.
- The model uses a single-hidden-layer MLP with 256 units; the contribution is primarily empirical rather than methodological. The paper does not explore more sophisticated nonlinear architectures that might be feasible with larger datasets.
- The paper does not discuss the computational cost of the nonlinear models relative to linear baselines, which is relevant for practical adoption.

### Trivial
None.

## Nice-to-Haves

- Report subject-level performance and statistical significance (e.g., bootstrap or permutation tests) for all main comparisons.
- Provide a controlled comparison with Antonello et al. using the same feature extraction pipeline (same layers, same fusion method) to isolate the effect of nonlinearity.
- Validate RED clustering with permutation tests or comparison to established functional network atlases.
- Show robustness of results to the number of PCA components and consider alternative dimensionality reduction methods.
- Discuss the practical implications of the absolute prediction performance for applications like decoding and in-silico testing.

## Novel Insights

None beyond the paper's own contributions. The paper demonstrates that a simple nonlinear multimodal model can improve fMRI speech encoding over linear unimodal baselines, and introduces RED-based clustering as a spatiotemporal analysis tool. However, the insights about brain organization are preliminary and largely consistent with existing theories; the paper does not provide strong new evidence that would change our understanding of neural speech processing.

## Suggestions

- Perform a controlled ablation where the only difference between models is the presence/absence of nonlinearity, keeping all other factors (features, fusion method, response representation) identical.
- Report subject-level results and perform a statistical test (e.g., paired t-test or permutation test across voxels) to assess whether the improvement of the multimodal MLP over the linear baseline is significant.
- Validate the RED clustering by comparing cluster assignments to known functional networks (e.g., language network, dorsal stream) using metrics like adjusted Rand index or normalized mutual information.
- Add a discussion of the absolute prediction performance and its implications for the claimed "unusually large improvements."

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>