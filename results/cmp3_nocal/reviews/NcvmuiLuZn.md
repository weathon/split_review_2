Now let me write the final review.

## Summary

This paper proposes Noise-to-Process (N2P), a weak-prior paradigm for stochastic process modeling from a single observed trajectory. The core idea is to learn a single measurable generator \(G_\theta\) that maps a shared base-noise process \(Z\) to an entire trajectory \(X = G_\theta(Z)\) in one pass, making projective consistency intrinsic by design. The authors instantiate this with Deconvolution-Based Process Transformation (DBPT), a deconvolution-based architecture designed to capture inter-temporal dependencies. Experiments on synthetic data, financial time series, image completion, and black-box optimization show competitive performance against prior-driven (GP, WGP, Markov) and data-driven (CNP, SDE matching) baselines.

## Strengths

- **Clean theoretical framing of projective consistency (Sections 2.1–2.2).** The idea that a single-generator + shared-noise structure makes all finite-index marginals projections of one joint sample, thereby internalizing projective consistency, is mathematically well-articulated. Propositions 2 and 3 are correct, and the compatibility discussion with Kolmogorov extension is sound. This packaging of the "shared noise + single generator" design principle for single-trajectory settings is genuinely novel.

- **The synthetic experiment (Section 4.1, Figure 2) is the paper's most compelling empirical evidence.** Showing GP failing on Markov data and vice versa while DBPT handles both cleanly illustrates the argument against prior sensitivity. This figure directly supports the paper's motivation.

## Weaknesses

### Fatal
None.

### Major

- **The training objective (masked MSE) does not explicitly enforce meaningful use of the noise path for uncertainty quantification.** The loss is \(\mathcal{L}(\theta) = \mathbb{E}_Z[\frac{1}{|\tau_o|}\|R_{\tau_o}\hat{X}(\mathcal{T}) - O\|_F^2]\) (Section 2.3.2). A generator that ignores \(Z\) and predicts a deterministic function can achieve equally low MSE. The paper claims "repeated draws provide uncertainty" (line 103) and that DBPT "places a stronger emphasis on modeling the uncertainty" (line 145), but the training signal contains no mechanism — no KL divergence, no adversarial loss, no likelihood objective — that compels the generator to distribute probability mass across trajectories rather than collapse to the conditional mean. The paper references Appendix C (mean-calibration guarantees) and Appendix D (identifiability), but the main text does not establish why the masked MSE alone would incentivize meaningful noise usage. Given that uncertainty quantification is a central claim, this is a significant gap.

- **The "single-trajectory" claim is ambiguous for the image completion experiments, which are the paper's most visually impressive results.** The paper states "all experiments in this section are conducted within a single-trajectory data" (line 125) and for image completion says "During training, we randomly mask a portion of the pixels, treating it as a single-trajectory image completion problem" (line 178). MNIST has 60,000 training images and CIFAR-10 has 50,000. The paper does not clarify whether DBPT is trained on (a) a single image, (b) each image treated as an independent trajectory (i.e., multi-trajectory training), or (c) a single contiguous sequence formed by concatenating all images. The quantitative results (PSNR 21.65 on MNIST vs. GP's 6.33) are striking, but without clarifying the training protocol it is impossible to assess whether the comparison to per-image baselines is commensurate. If DBPT trains on the full dataset while CNP is restricted to episodic segmentation of a single trajectory (as stated for other experiments), the comparison is asymmetric.

- **NGGP is discussed in the synthetic experiment results (line 139) but not listed among the baselines in the experiment setup (line 125).** The setup enumerates GP, WGP, Markov, DKL, SDE matching, and CNP. NGGP appears only in Related Work (line 117). Its convergence behavior is commented on, but the paper never states how it was set up or what data it saw. This is a minor presentational inconsistency but raises questions about whether other unreported baselines were attempted.

### Minor

- **The image completion evaluation reports only PSNR and SSIM (Table 2).** These are deterministic reconstruction metrics. For a method whose advertised strength is uncertainty quantification, the lack of any uncertainty-aware metric (e.g., NLL, CRPS, empirical coverage curves) for this experiment weakens the claim that DBPT provides "reliable uncertainty quantification" on images.

- **The paper does not explain how NLL is computed from DBPT samples (Table 1).** DBPT is an implicit model trained with MSE; computing a log-likelihood from its samples is non-trivial (e.g., kernel density estimation, Gaussian approximation, or simulation-based estimation). The NLL values (range ~500–2100) are not obviously implausible given the data scale implied by the MSE values, but without a description of the estimation procedure the metric cannot be interpreted or reproduced.

- **Ablation is limited to grid resolution (Section 4.5).** The paper varies \(N \in \{200, 400, 600, 800\}\) and notes an architecture ablation is in the appendix. However, there is no ablation in the main text examining whether the noise encoder is actually used (e.g., comparing output variance under different \(Z\) draws vs. a fixed noise baseline), nor an ablation of the loss function (e.g., comparing MSE against a proper scoring rule). These would directly inform the posterior collapse concern above.

### Trivial

- In the synthetic experiment discussion (line 139), the sentence "For WGP, when the number of observation points is limited, it struggles to construct an accurate distribution" is vague — the main experiment uses only 2 observation points (positions [10, 20] in Figure 2), but this is not stated in the main text.

## Nice-to-Haves

- An analysis showing that the empirical variance of DBPT samples correlates with predictive error (i.e., that the noise encoder is actually being used) would directly address the central uncertainty quantification concern.
- Comparing against a transformer-based or MLP decoder would clarify whether the deconvolution architecture is necessary for the claimed long-range dependency capture, or whether simpler alternatives suffice.
- Reporting uncertainty calibration metrics (coverage curves, CRPS) for the image completion task would strengthen the claim of reliable uncertainty quantification.

## Removed Points

- *"The theoretical apparatus (Kolmogorov extension) is decorative"* — The paper explicitly states that the Kolmogorov discussion "does not affect training" (line 55) and is a "compatibility statement." The paper is transparent about its scope; this is not a weakness.
- *"Architecture details deferred to appendix"* — Standard practice for main-text conciseness; not a weakness.
- *"Deconvolution cannot capture long-range dependencies"* — Stacked deconvolution layers with upsampling produce multi-scale receptive fields, as the paper states; this is an architectural speculation not grounded in a concrete analysis of the specific architecture.
- *"Evaluation of multi-trajectory baselines is adversarially uninformative"* — This criticism assumes the comparison is unfair, which depends on resolving the single-trajectory ambiguity (Issue 2 above). The paper's stated setting is single-trajectory; evaluating multi-trajectory methods in that setting and finding they struggle is informative about the gap the paper addresses. This concern is now folded into the ambiguity issue.
- *"The paper's discussion about MSE/uncertainty trade-off is post-hoc"* — The paper observes an empirical pattern (higher MSE, lower NLL) and offers an interpretation. This is standard scientific practice; not a weakness.

## Novel Insights

The harsh reviewer's most valuable observation is that the MSE training objective and the uncertainty quantification claim are in tension: the loss function used during training does not mathematically enforce the property that the paper later claims as a strength. This is a structural observation about the gap between the optimization objective and the desired behavior, and it applies regardless of the empirical results. The reviewer also correctly identifies that the "single-trajectory" framing in the image completion experiment is critically underspecified, which prevents proper evaluation of the paper's most impactful results. These two points together form a coherent diagnosis: the paper's theoretical framing is clean, but the empirical instantiation does not fully substantiate its central claims.

## Suggestions

1. For the image completion experiment, unambiguously state the training protocol: how many images are used, whether each image is a separate "trajectory," and what data each baseline sees.
2. Provide explicit evidence that different noise draws produce meaningfully different trajectories (e.g., variance of outputs across \(Z\) samples, correlation between predictive variance and error).
3. Describe how NLL is computed from DBPT samples in Table 1.
4. Add uncertainty-aware metrics (calibration curves, CRPS, or NLL) for the image completion task.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>