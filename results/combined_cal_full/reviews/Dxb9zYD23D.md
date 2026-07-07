## Summary

This paper proposes ST-Diff, a framework for unconditional multivariate time series generation that reframes the problem as video generation. The key idea is to apply the Short-Time Fourier Transform (STFT) to convert a multivariate time series into a spectro-temporal video tensor (frames = STFT time steps; spatial dimensions = frequency bins × covariates), then train a custom video diffusion model on this representation and invert back via iSTFT. A specialized architecture with anisotropic patching, tri-axial factorized attention, and empirically-initialized attention biases is designed to exploit the structure of this domain.

## Strengths

- **Genuinely novel conceptual paradigm (Sec. 4.1).** The idea of treating time series generation as video generation via the STFT is a clean synthesis of signal processing and generative modeling that is well-motivated and, to my knowledge, not proposed in this form before. Prior work either diffuses in the time domain (Diffusion-TS, CSDI), the frequency domain (Crabbé et al., 2024), or collapses time into a single static image (ImagenTime). The observation that a spectro-temporal video tensor preserves *both* spectral resolution and an explicit temporal axis, thereby enabling spatiotemporal architectures, is a genuinely new perspective.

- **Domain-specific architectural design (Sec. 4.3).** The anisotropic patching (aggregating along frequency while preserving unit granularity along covariates), tri-axial factorized attention with separate RoPE for temporal and frequency axes, and attention bias matrices initialized from empirical cross-correlation statistics are each justified with respect to the structure of the data. This is not a generic "throw a transformer at it" approach.

- **Strong empirical signal where comparisons exist (Table 1, Table 2).** On Discriminative and Predictive metrics where competitor values are available, ST-Diff often wins by a wide margin. The qualitative plots (Figures 3, 4) show close alignment of distributions, ACF, and PSD.

## Weaknesses

### Fatal
None.

### Major

- **Missing baseline results on Context-FID and Correlational scores (Table 1).** ImagenTime and Diffusion-TS — the paper's primary competitors, around which the introduction and related work are organized — are listed as "—" for Context-FID and Correlational scores across *all six datasets*. This means that on the two metrics that most directly measure distributional fidelity, ST-Diff is compared only against TimeGAN and TimeVAE, two much weaker pre-diffusion baselines. The claim "ST-Diff establishes a new state of the art" (line 150) and the count "superior performance on 21 out of 24 metric-dataset combinations" cannot be verified on 12 of those 24 combinations because the relevant competitors have no reported values. On Context-FID, the SOTA claim rests entirely on comparisons with methods that are not the paper's main rivals.

- **No ablation studies for any design component (Sec. 5).** The paper introduces several non-trivial design choices — (a) trend-residual decomposition before the STFT, (b) anisotropic patching, (c) attention bias matrices initialized from empirical statistics, (d) the cross-covariance loss on STFT magnitudes — and isolates none of them. Without ablations, it is impossible to tell which components drive the performance or whether the core video-representation paradigm is the main contributor versus specific architectural or loss choices. This is particularly concerning because the cross-covariance loss (line 140) is introduced only in the implementation details and not formally defined, making it unclear whether the impressive results come from the paradigm or from an auxiliary objective.

- **Cross-covariance loss buried in implementation details (line 140).** This auxiliary training objective is described only in the implementation paragraph, not in the method section (Sec. 4), and is not formally defined as a mathematical objective. The method section frames the framework as using only the standard DDPM noise-prediction loss, which is inconsistent with the actual implementation. Its contribution to the reported results is never isolated.

### Minor

- **Context-FID undefined in evaluation metrics (Sec. 5).** Despite being used as a primary metric in Table 1 and listed among "four established metrics" (line 148), Context-FID is never defined in the evaluation metrics section (lines 109–110). The reader must consult an external paper to understand a metric central to the paper's central empirical claims.

- **Cross-publication comparison concerns (line 111).** The paper states it reports "performance from the original publications to ensure fair comparison." Different papers may use different random seeds, data splits, preprocessing, and evaluation protocols. Given the very large reported improvements (e.g., Context-FID of 0.031 vs. 0.631 for Diffusion-TS at length 64 — a 20× improvement), evaluation differences cannot be ruled out as contributors. At minimum, the leading baselines should be re-run under the same evaluation pipeline.

- **Long-sequence evaluation limited to one dataset (Sec. 5.1.2).** The scalability experiments are conducted only on ETTh. The paper's motivation discusses general "long-range dependencies" and "multi-scale periodicities," but does not show whether the approach scales on other datasets (MuJoCo, Energy, fMRI) at longer lengths.

- **Trend broadcasting across frequency not clearly justified (Sec. 4.1).** The trend component is broadcast across all frequency bins and stored as a separate channel. Since the trend is a time-domain concept with no natural frequency structure, this creates an artificial spatial pattern in the frequency-covariate frame that the video diffusion model may learn spurious correlations from. This design choice deserves justification or an ablation.

### Trivial

- Number of experimental runs not stated (standard deviations are reported but the number of runs is unspecified).
- No runtime, parameter count, or inference speed comparison is provided despite the paper acknowledging "higher computational and memory costs" (line 203).

## Nice-to-Haves

- A formal mathematical statement of the cross-covariance loss in the method section.
- Comparison against Crabbé et al. (2024), a frequency-domain diffusion model cited in the related work but not included in experiments.
- Results on at least one additional dataset (e.g., Energy or MuJoCo) at longer sequence lengths.

## Removed Points

- **Crabbé et al. not used as a baseline**: The paper cites this work in Related Work but does not include it in experiments. While a natural comparison point, the paper's scope is centered on the video representation paradigm, not exhaustive frequency-domain method comparison. Repositioned as a nice-to-have.
- **"Context-FID not defined" severity downgraded**: Originally presented as a critical oversight. It is a genuine omission but a minor one — the metric is from a published NeurIPS paper (Naiman et al., 2024) that readers can consult. Moved to Minor.
- **"Standard deviations without number of runs" and "No runtime comparison"**: These are genuine but trivial issues. Moved to Trivial.

## Novel Insights

None beyond the paper's own contributions. The key takeaway from the review process is that the paper's strongest claim (a new SOTA paradigm) requires two concrete additions the paper currently lacks: (1) ablation isolating the video representation from the architectural and loss components, and (2) re-running the main competitors on the two metrics where they are absent. These are evaluative gaps, not unrecognized findings about the paper.

## Suggestions

1. Re-run ImagenTime and Diffusion-TS under the same evaluation protocol and report Context-FID and Correlational scores for them. Without this, the central SOTA claim is unverifiable on those metrics.
2. Add ablation studies isolating: (i) the STFT video representation vs. raw time series reshaped as video, (ii) a 2D diffusion model on static spectrograms (as in ImagenTime), (iii) the anisotropic patching, (iv) the attention bias initialization from empirical statistics, (v) the cross-covariance loss. This would directly test whether the *video representation* is additive over existing approaches.
3. Formally define Context-FID and the cross-covariance loss in the main text.
4. Include at least one additional dataset in the long-sequence experiments.

## Score and Decision

**Calibration Anchors (all retrieved across rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| u1cQYxRI1H.md (lighting diffusion) | 0.50 | R1 (0–1.5) | No | Unrelated topic, extreme low outlier |
| Uj0h13lVrR.md (GFlowNets) | 1.00 | R1 (0–1.5) | No | Unrelated topic |
| nSDOkm0SKo.md (financial news) | 1.00 | R1 (0–1.5) | No | Unrelated topic |
| P49gSPmrvN.md (UMAP embeddings) | 1.00 | R1 (0–1.5) | No | Unrelated topic |
| RDLvnUJ5JZ.md (TF-score, diffusion forecasting) | 3.00 | R1 (1.5–3.5) | No | Similar topic, lower novelty, accepted-level score 3 |
| zB6uMznFuZ.md (TimeAutoDiff) | 3.00 | R1 (1.5–3.5) | Yes | Criticized as lacking novelty ("assembly"), writing issues. ST-Diff has stronger novelty and clarity → above |
| 2whSvqwemU.md (FM-TS, flow matching) | 3.00 | R1 (1.5–3.5) | No | Similar topic, reject-level score |
| 2orBSi7pvi.md (STDM, spatiotemporal diffusion) | 3.00 | R1 (1.5–3.5) | No | Similar topic, reject-level score |
| etUJR2xBYa.md (TimeDiT, DiT for TS) | 4.20 | R1 (3.5–5.5) | Yes | Missing implementation details, no baselines for some tasks. ST-Diff is better structured and written → above |
| 4f4HDfbwY5.md (CPDD, patch compression) | 4.75 | R2 (4.5–6.5) | Yes | Severe writing (-8.00) and evaluation gaps (-7.72). ST-Diff has better novelty and clarity → above |
| Y8KK9kjgIK.md (SigDiffusions) | 4.33 | R1 (3.5–5.5) | Yes | Strong theory but dragged by an outlier 1/10; ST-Diff's contribution is more accessible |
| GkeTXeujW0.md (CausalDiffusion) | 4.25 | R1 (3.5–5.5) | No | Similar space, lower score |
| 4h1apFjO99.md (Diffusion-TS) | 6.33 | R1 (5.5–7.5), R2 | Yes | Closest topical anchor. Stronger evaluation (ablations present) but weaker novelty. ST-Diff below due to missing ablations and incomplete baseline comparison |
| lcmd2Qdrsv.md (MoD, mixture of diffusers) | 5.60 | R1 (5.5–7.5) | No | Similar score range |
| CZiY6OLktd.md (MG-TSD, multi-granularity) | 6.00 | R1 (5.5–7.5) | No | Forecasting task, less directly comparable |
| qae04YACHs.md (TMDM, transformer-modulated) | 6.33 | R1 (5.5–7.5) | No | Forecasting task |
| uKZdlihDDn.md (fluid simulation diffusion) | 7.60 | R1 (7.5–8.5) | No | Unrelated domain |
| tyEyYT267x.md (interpolating AR + diffusion LM) | 8.00 | R1 (7.5–8.5) | No | Unrelated domain |
| I5lcjmFmlc.md (robust classification via diffusion) | 8.00 | R1 (7.5–8.5) | No | Unrelated domain |
| EO8xpnW7aX.md (permutation discrete diffusion) | 8.00 | R1 (7.5–8.5) | No | Unrelated domain |

**Round 1 bracket:** 5.0 – 6.5. **Narrowing:** The comparison against Diffusion-TS (6.33, closest topical anchor) and CPDD (4.75) places the paper between them. This paper shares the positive-weight items "novel paradigm" and "strong empirical signal" with Diffusion-TS, but lacks its ablation studies and reports more incomplete baseline comparisons. The missing-baseline weakness (-6.18 in model weight) is heavier than any single weakness Diffusion-TS faced. Conversely, the paper avoids the severe clarity/novelty penalties that pulled CPDD down to 4.75.

**Final score: 5.5**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>