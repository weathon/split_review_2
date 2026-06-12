## Summary

This paper introduces ST-Diff, a framework that reframes multivariate time series generation as a video generation task by using the Short-Time Fourier Transform (STFT) to convert time series into spectro-temporal video tensors—where frequency and covariate axes form spatial dimensions and the temporal evolution of the spectrum is preserved along the video time axis. A custom video diffusion model with tri-axial factorized attention and domain-specific inductive biases (learned covariate correlation and spectral covariance biases) is designed to operate on this representation. Extensive experiments on six benchmarks demonstrate state-of-the-art performance for unconditional time series generation, with particularly strong gains on high-dimensional datasets.

## Strengths

- **Novel and well-motivated paradigm**: The core insight of treating time series as videos via STFT is creative and bridges classical signal processing with modern video generative models in a principled way. The paper clearly articulates the limitations of both time-domain and static-image approaches and positions the video representation as a natural middle ground that preserves temporal dynamics while exposing spectral structure.

- **Tailored architecture with meaningful inductive biases**: The tri-axial factorized attention (temporal/frequency/covariate) is well-designed for this data representation. Key design choices—such as anisotropic patching to avoid imposing spatial locality on covariates, the symmetric covariate bias matrix initialized from empirical cross-correlations, and the frequency bias from STFT magnitude covariance—demonstrate careful domain-specific thinking rather than naively importing a video backbone.

- **Strong and comprehensive empirical evidence**: ST-Diff achieves superior performance on 21 of 24 metric-dataset combinations for L=24 and consistently dominates across all metrics and sequence lengths (64, 128, 256) on ETTh. The long-term generation results are especially compelling: the Discriminative Score remains remarkably stable (0.030→0.032→0.029) while competitors degrade substantially, and the Context-FID improvement at L=64 is over an order of magnitude better than the next-best method. Qualitative analyses (t-SNE, KDE, ACF, PSD) provide strong complementary evidence of distributional and temporal fidelity.

## Weaknesses

### Fatal
None.

### Major

- **Incomplete baseline comparisons**: A significant number of cells for ImagenTime and DiffusionTs in Table 1 are marked with '—' (not reported). While the paper attributes this to the original publications, it weakens the comparison. For Context-FID and Correlational scores—arguably the most informative metrics—no numbers are available for the two strongest diffusion baselines. This makes it difficult to fully assess ST-Diff's advantage over the most relevant competitors. The paper should at least attempt to reproduce these baselines under a unified evaluation protocol.

- **Primary evaluation limited to L=24**: The main comparison (Table 1) uses sequences of only 24 time steps, which is unusually short for many practical time series applications. While the extended results (L=64–256) partially address this, not all baselines are compared at these lengths (only DiffusionTs, TimeGAN, TimeVAE—ImagenTime is absent from Table 2). Given the paper's emphasis on preserving temporal structure and the inherent advantage of video models for sequential data, demonstrating this benefit more convincingly at longer horizons would strengthen the contribution.

### Minor

- **No computational cost analysis**: The paper acknowledges higher computational and memory costs but provides no empirical quantification. Given that video diffusion transformers are substantially more expensive than time-domain models, reporting training time, inference time, parameter counts, and memory usage relative to baselines would be important for practitioners evaluating this approach.

- **Limited ablation of STFT hyperparameters**: The STFT configuration (nfft = seq.len/2 − 1, hop = nfft/4) is set with little justification or sensitivity analysis. The window length and hop size fundamentally control the time-frequency resolution trade-off, and understanding how these choices affect generation quality would be valuable, especially since different datasets may benefit from different spectral resolutions.

- **Simple trend decomposition**: Using EMA for trend extraction is pragmatic but somewhat underexplored. More sophisticated decomposition methods (e.g., seasonal-trend decomposition, learned decomposition modules) might better isolate non-stationary components, particularly for datasets with complex seasonal patterns.

## Nice-to-Haves

- A comparison of ST-Diff's wall-clock training/inference costs against baselines would make the results more actionable.
- Experiments on conditional tasks (forecasting, imputation) would substantiate the claim that the paradigm generalizes beyond unconditional generation.
- An analysis of how the learned bias matrices (B_C, B_F) evolve during training and whether they capture interpretable structures would provide deeper insight.

## Novel Insights

The paper's central contribution—the time-series-as-video paradigm—is genuinely novel and represents a productive intersection of signal processing and video generation that neither community has systematically explored for general multivariate time series. The observation that STFT produces a natural video tensor whose "spatial" dimensions (frequency × covariate) have very different statistical structure from natural images, motivating anisotropic patching and domain-specific attention biases, is an insightful design lesson. The strong empirical finding that preserving temporal evolution of spectral content is more valuable than either raw time-domain modeling or static image representations constitutes meaningful evidence for the community.

## Suggestions

- Run ImagenTime and DiffusionTs through a unified evaluation pipeline to fill the missing cells in Table 1, or clearly justify why direct comparison is infeasible.
- Add a computational cost table comparing training time, inference time, GPU memory, and parameter counts across methods.
- Include an ablation study on STFT hyperparameters (window size, hop length) and trend extraction method to quantify their impact on generation quality.
- Extend evaluation to longer sequences (L=512+) and at least one conditional task to support the generalizability claims made in the conclusion.

## Score and Decision

The paper presents a well-motivated, novel paradigm (time series as videos via STFT) with a carefully designed architecture and strong empirical results across diverse benchmarks. The main weaknesses—incomplete baseline comparisons and limited evaluation at short sequence lengths—are notable but do not invalidate the core contribution, and the extended results up to L=256 provide reasonable evidence of scalability. The work opens a productive research direction at the intersection of signal processing and video generation.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: Accept