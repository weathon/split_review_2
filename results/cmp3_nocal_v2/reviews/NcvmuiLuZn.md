## Summary

The paper introduces the Noise-to-Process (N2P) paradigm for modeling stochastic processes from a single trajectory without strong structural priors. The key idea is to push a shared base-noise process through a learnable generator to produce the full trajectory in one pass, making projective consistency automatic. The Deconvolution-Based Process Transformation (DBPT) is proposed as a concrete instantiation using deconvolution layers. Experiments are conducted on synthetic data, financial time series, image completion, and black-box optimization.

## Strengths

- **Strong image completion results (Table 2, Figure 3).** On MNIST, DBPT achieves PSNR 21.65 (vs. CNP 16.58, next best) and SSIM 0.94 (vs. CNP 0.62). On CIFAR, PSNR 24.04 (vs. CNP 18.56) and SSIM 0.90 (vs. CNP 0.61). These are large, unambiguous improvements that suggest the architecture captures spatial structure effectively in this setting. The visual results in Figure 3 corroborate the quantitative advantage.

- **Clear problem framing.** The paper articulates a genuine tension between prior-driven methods (data-efficient but rigid) and data-driven meta-learning approaches (flexible but requiring multi-trajectory supervision), and targets a worthwhile gap: learning from a single trajectory with weak priors while obtaining useful uncertainty.

## Weaknesses

### Major

- **The projective consistency "contribution" is mathematically automatic and not a distinguishing property.** Proposition 3 states that if the process law is a pushforward $\mu_\theta = \nu \circ G_\theta^{-1}$, then the finite-dimensional marginals are consistent. This follows directly from the functoriality of pushforwards and holds for *any* joint generator $G_\theta$, regardless of architecture. The paper presents this as a key design innovation ("making projective consistency intrinsic by design," Remark 4) and as a distinguishing advantage over Neural Processes (Section 3, line 119). But Neural Processes also define a stochastic process via a latent-variable pushforward (Garnelo et al., 2018b), and any method that produces all coordinates jointly from a shared noise source has this property automatically. The paper's central theoretical novelty does not distinguish it from existing approaches. This does not invalidate the empirical contributions (DBPT's architecture could still be effective), but the framing significantly overstates the theoretical contribution.

- **No evidence supporting the headline claim of "calibrated uncertainty."** The abstract (line 9) and contribution list (line 27) claim "calibrated uncertainty," and the paper states that DBPT delivers "flexible uncertainty modeling" and "reliable uncertainty quantification." However, the paper reports **zero calibration metrics**: no coverage curves, no interval scores, no reliability diagrams, no calibration plots, no assessment of whether predictive intervals at stated confidence levels are accurate. The only probabilistic metric is NLL (Table 1), and even there DBPT's NLL has very high variance (std 135.30 vs. WGP's 55.42 on BIA) and DBPT trails WGP on average rank (2.50 vs. 1.75). The training objective is masked MSE (Eq. 1), not a proper scoring rule that would directly optimize probabilistic calibration. The model is an implicit generative model where uncertainty comes from resampling $Z$, but without calibration checks there is no evidence that predictive dispersion corresponds to genuine uncertainty. This is a significant evidential gap for a paper whose central claim is about uncertainty quantification.

### Minor

- **Missing key baseline: ConvCNP.** The Related Work section discusses Convolutional Conditional Neural Processes (Gordon et al., 2019) as an NP variant that "integrate[s] a broad class of group equivariances into NP architectures" (line 119). Yet ConvCNP is not included as a baseline in the image completion experiments, where its equivariance properties are most relevant. Since the paper claims DBPT beats "Neural Processes" broadly, excluding the most appropriate NP variant for spatial data weakens this claim.

- **Unsupported claim about data efficiency.** The conclusion states DBPT "retains the data efficiency of prior-driven methods" (line 218), but no experiment compares performance as a function of observation count or trajectory length. This claim is asserted without evidence.

- **Synthetic experiment is too limited.** The visualization (Section 4.1, Figure 2) uses only 2 observation points (positions [10, 20]). With only two data points, most methods unsurprisingly struggle, and this does not convincingly demonstrate DBPT's flexibility or advantages in the claimed low-data regime. A more informative experiment would vary the number of observations.

- **"Single-trajectory" framing is stretched for image completion.** A 32×32 CIFAR image has 1024 pixels, and with random masking the model sees hundreds of observed pixels. Calling this "single-trajectory" is technically correct but diverges substantially from the motivating regime (e.g., CFD simulations with few noisy measurements, Introduction lines 13-14). The strong image results may reflect DBPT's ability to leverage many observed pixels rather than its claimed ability to learn from extreme data scarcity.

## Nice-to-Haves

- **Add proper uncertainty calibration metrics.** Report coverage of 50%, 80%, 90%, 95% predictive intervals and calibration curves for at least the time series and synthetic experiments. This would directly support (or refute) the paper's central claim about calibrated uncertainty.
- **Include ConvCNP as a baseline** for the image completion experiments, as it is the most relevant NP variant for spatial data.
- **Add a data-efficiency experiment** showing performance as a function of the number of observed points, to test the claimed advantage in single-trajectory, few-shot regimes.

## Removed Points

These points from the input review were excluded per the filtering rules, and should be treated with caution:

- *Architecture underspecification* (Critical Issue 3 in input): The paper states "Detailed descriptions of the experimental configurations and results are provided in the Appendix F" (line 125). Criticizing details missing from the main text when the appendix exists is removed per the hard rule about missing appendix content.
- *No deep learning time series baselines* (DeepAR, Transformers): This constitutes scope creep — the paper compares against stochastic process methods, not general time series forecasting models.
- *SDE Matching performs dramatically worse*: The reviewer speculates about "poor configuration," which is not verifiable from the paper. The paper notes SDE Matching is a multi-trajectory method adapted via episodic segmentation and was excluded from image experiments due to cost, which is transparent.
- *Statistical significance testing*: A nice-to-have, not a core flaw.
- *NGGP results not documented*: Discussed only as a qualitative observation; documenting failed attempts in detail is not a standard expectation for the main text.
- *Notation typo in Proposition 3*: Removed per the hard rule on typos/formatting.
- *Related Work claims about generative models*: The statement about generative models not capturing process-level joint distributions is debatable but not central to the paper's contribution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Tone down the projective consistency claim. Reframe as: "joint generation from a shared noise source yields consistent finite-dimensional marginals automatically, and we show this design choice is practically effective for single-trajectory learning."
2. Add coverage and calibration metrics to support the uncertainty claims.
3. Include ConvCNP as a baseline for image completion.
4. Add a data-efficiency experiment varying the number of observed points to substantiate the "data efficiency" claim.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>