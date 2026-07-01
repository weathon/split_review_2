## Summary

ST-Diff proposes reframing multivariate time series generation as a video generation task: the Short-Time Fourier Transform (STFT) converts a time series into a 3D time-frequency-covariate tensor, and a custom video diffusion model with factorized attention and domain-specific bias matrices generates samples in this representation before inverting back to the time domain. The core idea is novel and the architecture is thoughtfully designed, but the evaluation has significant gaps that limit support for the central SOTA claims.

## Strengths

- **Novel and well-motivated data representation.** The STFT-based video tensor preserves both spectral content and temporal evolution, cleanly addressing the limitation of time-domain models (which lack spectral structure) and static-image models (which collapse the temporal axis). This synthesis of signal processing and generative modeling is the paper's strongest contribution.

- **Principled architecture with domain-specific inductive biases.** Anisotropic patching (preserving covariate granularity rather than imposing arbitrary spatial correlations), tri-axial factorized attention (temporal, frequency, covariate), and data-initialized bias matrices (empirical cross-correlation for covariates, spectral covariance for frequencies) each reflect genuine domain knowledge about multivariate time series. These are not off-the-shelf components.

- **Strong results on the metrics and baselines that are reported.** Where comparisons are available, ST-Diff often outperforms baselines by substantial margins (e.g., Discriminative Score on Energy: 0.009 vs. 0.040 for ImagenTime; Context-FID on ETTh at length 64: 0.031 vs. 0.631 for Diffusion-TS). The long-sequence experiments (Table 2, where Diffusion-TS is included on all four metrics) are particularly impressive.

## Weaknesses

### Major

- **Incomplete baseline comparison on Context-FID and Correlational (Table 1).** The two most relevant diffusion baselines—Diffusion-TS and ImagenTime—are entirely absent from Context-FID and Correlational scores across all six short-sequence datasets (L=24). On these two metrics, ST-Diff is only compared against TimeGAN (2019) and TimeVAE (2021). The paper's headline claim of "superior performance on 21 out of 24 metric-dataset combinations" includes wins on 12 combinations where the strongest competitors are missing. While Diffusion-TS *is* compared on all metrics in the long-sequence experiments (Table 2), the SOTA claim for Table 1 is not properly supported on half of the evaluation space. This gap stems from the paper's choice to rely entirely on numbers from original publications rather than running baselines under a unified protocol.

- **Context-FID is never defined.** The paper introduces Context-FID as one of four primary evaluation metrics (Section 5) and uses it to claim "more than an order-of-magnitude improvement" (Table 2), but never specifies what Context-FID is, how it is computed, or what "context" refers to. Discriminative, Predictive, and Correlational scores are each defined in the text; Context-FID is not. The reported values are uninterpretable without a definition.

- **No ablation studies.** The framework introduces multiple design choices: (a) STFT video representation vs. raw time-domain vs. static image, (b) trend-residual decomposition via EMA, (c) anisotropic patching, (d) tri-axial factorized attention, (e) data-initialized bias matrices, (f) cross-covariance loss on STFT magnitudes. None are ablated. It is impossible to determine which components drive the reported performance—whether the elaborate architecture matters, or the results could be obtained with a simpler model and the same STFT input.

### Minor

- **Crabbé et al. (2024) discussed but not compared.** The Related Works section (line 39) mentions frequency-domain diffusion as "complementary" work, but this directly relevant 2024 baseline—which also operates on spectral representations—is absent from the experiments. Its omission weakens the claim of comprehensive SOTA comparison.

- **Reliance on published baseline numbers constrains the comparison.** The paper states it uses numbers from original publications "to ensure fair comparison" (Section 5). This choice is the root cause of the missing baselines on Context-FID and Correlational—those papers simply did not report those metrics. Running baselines under a unified protocol would remove this limitation.

### Trivial

None.

## Nice-to-Haves

- Run ImagenTime and Diffusion-TS on Context-FID and Correlational for the short-sequence benchmarks (Table 1), or clearly scope the SOTA claim to only the metrics/datasets where all baselines are available.
- Add ablation experiments: (i) replace the custom architecture with an off-the-shelf video diffusion model (same STFT input), (ii) remove the cross-covariance loss, (iii) remove trend-residual decomposition, (iv) remove bias matrices.
- Include Crabbé et al. (2024) as a frequency-domain diffusion baseline.
- Report model size, training time, and inference speed to contextualize the acknowledged higher computational cost.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "Context-FID and Correlational scores are absent for both Diffusion-TS and ImagenTime across all datasets" — slightly overbroad: Diffusion-TS *does* have Context-FID and Correlational results in Table 2 (long-sequence experiments on ETTh), though it is absent from Table 1. The core concern (missing Table 1 comparisons) remains valid.
- Criticisms about the small video tensor size at L=24 being "barely more than an image" and whether the video framing adds value at this scale — this is an interesting observation but speculative as a weakness; the paper's results on L=24 are strong regardless.
- Criticisms about EMA vs. STL/HP filtering for trend-residual decomposition — this is a methodological preference, not a verified flaw.
- Generic or speculative concerns about dataset size, L=512 experiments, and missing compute benchmarks — these are nice-to-haves, not core weaknesses.

## Novel Insights

The reviews surface a central tension: the paper's thesis is that the time-series-as-video representation (plus custom architecture) is the key enabler of SOTA results, yet it never runs the controlled experiment that would substantiate this—comparing the same STFT input through the custom architecture versus through an off-the-shelf video diffusion model without domain-specific biases. The empirical claims also suffer from a systematic mismatch between the scope of the comparison (older GAN/VAE baselines on two of four metrics) and the scope of the SOTA assertion (which implicitly includes the strongest diffusion baselines on those metrics). The most constructive path forward would be to either complete the comparison or more carefully scope the claims.

## Suggestions

1. Define Context-FID explicitly in the main text.
2. Run the missing baselines on Context-FID and Correlational for Table 1, or restrict the SOTA claim to metrics where all baselines are available.
3. Add ablation experiments isolating the contribution of the custom architecture from the STFT representation itself.
4. Include Crabbé et al. (2024) in the experimental comparison.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>