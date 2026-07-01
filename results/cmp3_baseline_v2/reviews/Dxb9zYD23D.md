## Summary

This paper proposes a new paradigm for unconditional multivariate time series generation: reframing time series as videos. It uses the Short-Time Fourier Transform (STFT) to convert a multivariate time series into a spectro-temporal video tensor, then applies a customized video diffusion model with factorized attention over time, frequency, and covariate axes. The resulting framework, ST-Diff, achieves state-of-the-art results on several benchmarks, especially for long sequence generation.

## Strengths

1. **Novel and well-motivated perspective** – The core idea of treating time series as videos via STFT is creative and addresses a clear limitation of prior work: time-domain models struggle with spectral dynamics, and image-based methods collapse the temporal axis. This is a unifying reframing that naturally bridges signal processing and modern video generation.

2. **Strong empirical results on long sequences** – Table 2 shows that ST-Diff dramatically outperforms Diffusion‑TS, TimeGAN, and TimeVAE on ETTh with lengths 64, 128, and 256. The improvements are large (e.g., Context‑FID drops from 0.63 to 0.03 at length 64) and the performance degrades gracefully, which is a genuine advance.

3. **Architectural design tailored to the representation** – The anisotropic patching (preserving covariate identity) and the tri‑axial factorized attention with learnable bias matrices (derived from empirical statistics) are well‑reasoned inductive biases for spectro‑temporal data. The paper explains why each design choice fits the structure of the video tensor.

## Weaknesses

### Major

1. **Missing or incomplete baseline comparisons** – In Table 1, many entries for ImagenTime and Diffusion‑TS are marked “—”. This makes it impossible to verify the claimed state‑of‑the‑art on several datasets and metrics (e.g., Context‑FID and Correlational score for Sines, ETTh, Energy, fMRI). The authors state they rely on original publications, but this leaves the evaluation incomplete; running these baselines or providing a clear justification for omissions would be necessary for a convincing claim.

2. **Context‑FID metric is not defined in the main text** – The paper introduces “Context‑FID” as a primary metric but never defines it. The reader cannot interpret what it measures, how it is computed, or whether it is an established score. This is a serious clarity gap that undermines the quantitative evaluation.

3. **No ablation studies** – The paper does not isolate the contributions of the STFT‑based video representation, the trend‑residual decomposition, the custom spectro‑temporal transformer, the bias matrices, or the cross‑covariance loss. Without such experiments, it is unclear which components are essential for the observed improvements. A baseline that applies a generic video diffusion model (e.g., a standard 3D‑UNet) to the STFT tensor would be particularly informative.

### Minor

4. **Bias matrix initialization** – The learnable bias matrices are initialized from “empirical statistics of the data.” It is not explicitly stated whether these statistics are computed only from training data, which could introduce test‑set leakage if not. The paper should clarify this.

5. **Computational cost mentioned but not quantified** – The conclusion notes higher memory/cost, but no runtime, parameter count, or FLOPs comparisons are given. This limits practical utility assessment.

## Nice-to-Haves

- Adding an ablation that removes the trend‑residual decomposition or the cross‑covariance loss would strengthen the contribution analysis.
- Including a comparison with a “vanilla” video diffusion model (e.g., a standard 3D‑UNet) on the STFT representation would clarify the value of the custom architecture.
- Defining Context‑FID explicitly and, ideally, comparing with more standard metrics (e.g., FID over time‑series features) would increase reproducibility.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that spectro‑temporal structure in time series closely resembles the spatiotemporal structure in videos: frequency and covariate axes act as spatial dimensions, while the temporal axis tracks evolution. This analogy opens up the entire video generation toolbox (e.g., 3D convolutions, factorized attention, temporal consistency losses) for sequence modeling. The paper convincingly shows that the inductive biases of video diffusion models are a natural fit for time‑frequency representations.

## Suggestions

- Clearly define Context‑FID in the main paper (or rename it to something standard).
- Provide the missing baseline numbers for ImagenTime and Diffusion‑TS on all datasets and metrics, or explain why they are unavailable.
- Add an ablation study that removes the custom spectro‑temporal attention (replacing it with a generic video diffusion backbone) to isolate the contribution of the architecture.

## Score and Decision

**Score:** 6  
**Decision:** Accept (borderline)

The paper introduces a genuinely novel and well‑motivated paradigm with strong empirical results on long‑sequence generation. However, the evaluation is weakened by missing baseline comparisons, an undefined metric, and the absence of ablation studies. These issues are major but not fatal; they can be addressed in a revision. On balance, the contribution to the community—especially the new perspective and the demonstrated scalability—merits acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>