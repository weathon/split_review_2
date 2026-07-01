## Summary

Count Bridges introduces a stochastic bridge process on the integers using Poisson birth-death dynamics that yields closed-form conditionals for exact training and sampling (Proposition 3.1). The paper extends this framework to deconvolution via an EM algorithm that treats unit-level counts as latent variables, and demonstrates the method on synthetic benchmarks and two biological applications: nucleotide-resolution bulk RNA-seq deconvolution and reference-free spatial transcriptomic deconvolution.

## Strengths

- **Novel bridge construction on integers (Sec. 3.1, Proposition 3.1).** The slack-variable decomposition (Eq. 7)—separating displacement $d_t$ from slack $M_t$—is the key insight that makes the bridge tractable. Sampling reduces to a Bessel draw for $M_t \mid d_t$, followed by Binomial thinning of $N_t$ and a Hypergeometric draw for $B_s$. The fact that this family satisfies bridge consistency (Eqs. 1–2) is non-trivial. This is a genuinely new object, not an incremental modification of an existing discrete diffusion.

- **Connection to Schrödinger bridges and entropy-regularized OT (Sec. 3.1, lines 121–135).** Showing that $\kappa = \sqrt{\lambda_+ \lambda_-}$ plays the same role as $\sigma$ in the Gaussian case, with $\kappa \to 0$ recovering discrete OT with cost $|x_1 - x_0|$, places Count Bridges in a well-understood theoretical landscape and clarifies what the model is doing probabilistically.

- **Scaling to higher dimensions (Fig. 3).** On the low-rank Gaussian mixture transport task, CB's Wasserstein-1 stays near zero as $d$ increases from 4 to 512, while CFM and DFM degrade sharply. This gap is large enough to suggest a meaningful practical advantage for high-dimensional count data, even accounting for comparison caveats.

## Weaknesses

### Major
None.

### Minor

1. **The Enformer comparison (Table 1) does not isolate CB's contribution.** The paper obtains "a local genomic context $z$ ... with Enformer" (line 327), meaning CB receives Enformer features *plus* cell-type embeddings, diffusion time, and noisy counts. The baseline is a fine-tuned Enformer with only the DNA sequence. This is a valid system-level comparison, but it does not test whether the Count Bridge *architecture itself* drives the improvement, since CB receives strictly more information. A controlled ablation (CB with vs. without Enformer features, or Enformer with the same auxiliary inputs) would clarify the source of the gains.

2. **Synthetic CFM/DFM comparisons (Sec. 6.1, Figs. 2–3) compare across data types, not methods.** The data is "a scaled and rounded variant" (Fig. 2 caption) of continuous tasks. CFM operates on continuous data and DFM on categorical tokens; rounding introduces quantization error CFM was not designed for, and converting integer counts to tokens discards ordinal structure. The large W1 gap in Fig. 3 likely reflects data-type mismatch rather than relative method quality. A comparison against a count-native method (e.g., Blackout Diffusion, which the paper discusses but does not benchmark) would be more informative. The paper acknowledges the comparison framing but should either include a matching-method comparison or more carefully qualify the conclusions.

3. **Parametric form of the denoiser $q_\theta$ is underspecified (line 327).** The paper states a "final softplus head that parameterizes the conditional count distribution $X_0 \mid X_t, t, z$" without specifying what family of distributions is parameterized (Poisson? Negative binomial with dispersion? Product of independent marginals?). This is needed for reproducibility and for interpreting the biological results (e.g., whether overdispersion is modeled).

4. **The deconvolution EM uses an approximate E-step whose behavior is not characterized.** The E-step (Algorithm 3) replaces exact sampling from the aggregate-conditional $Q_\theta$ with projection-guided diffusion. The paper acknowledges this "lacks serious theoretical support" (line 368, limitations). The synthetic deconvolution experiment (Fig. 4) provides no baseline comparison, so we cannot assess whether the approximation is adequate or how much error it introduces. A comparison against a simpler Monte Carlo E-step on a small-scale task would help validate the approach.

5. **The aggregate-level M-step loss loses unit-level structure.** For a sum aggregate, $\rho(A(\mathbf{X}), A(\mathbf{X}')) = |\sum_g X_g - \sum_g X_g'|$, a single scalar that is insensitive to how counts are distributed across units. While the E-step provides unit-level latent samples, the M-step gradient contains no information about unit-level configuration, making it unclear how the model learns to distinguish between unit-level patterns.

6. **Proposition 4.1 projection outputs real numbers, not integers.** The projection $\Pi(\mathbf{x}_0)_g = a_0 x_{g0} / (\sum_{g'} x_{g'0})$ produces real-valued outputs, but the data are integer counts. The paper does not specify how the projection output is discretized. The "learned projection" attention module (Sec. 6.2) may handle this implicitly, but the mechanism is not described.

7. **The synthetic deconvolution experiment (Fig. 4) lacks baselines.** Without any comparator, the figure only shows that deconvolution gets harder as groups grow—which is expected—and provides no reference point for whether CB's performance is acceptable.

8. **Number of samples $m$ for the energy score plugin estimator is not reported** (line 183). The variance and computational cost of the training loss depend directly on $m$. This should be stated.

### Trivial

- The paper does not specify the distance metric used for assigning "closest cell type" when converting CB's count profiles to cell-type proportions for comparison with CIBERSORTx/MuSiC (line 333) and STDeconvolve (line 345).
- The cross-entropy versus energy-score ablation is deferred to a missing appendix section (D.1), making the discussion in Sec. 3.2 feel incomplete.
- Several entries in Tables 1 and 5 report $\pm 0.000$ standard errors, which appears to reflect rounding or near-deterministic sampling rather than genuine zero variance.

## Nice-to-Haves

- Benchmark against Blackout Diffusion on the synthetic tasks, since it is the only other count-specific generative method. The paper notes that CB generalizes Blackout Diffusion (line 262) but does not compare empirically.
- Add convergence diagnostics for the EM procedure on synthetic data (does the loss decrease monotonically? Does it converge from different initializations?).
- Include confidence intervals or standard errors for baseline methods in Tables 2–4; currently only CB has error bars.
- Show results on real Visium data where ground truth is unavailable but qualitative validation (alignment with known tissue architecture) is possible.
- Discuss the computational cost of the Bessel sampler relative to Gaussian sampling, since it is the bottleneck.

## Removed Points

These points were identified but not included in the main review for the reasons stated:

- *"The paper does not clearly argue whether the consistency properties are necessary conditions or desirable properties"* — This is a presentation preference; the paper states them as requirements and shows CB satisfies them. Not a substantive weakness.
- *"CFM/DFM comparisons are structurally invalid / 'not a real comparison'"* — The paper is transparent about the data conversion. The comparison is informative about what happens when continuous/categorical methods are applied to counts, even if it is not apples-to-apples. Demoted to Minor #2 with adjusted framing.
- *"The EM lacks convergence guarantees"* — The paper already acknowledges this as a limitation (line 368). Kept as Minor #4 but without the "fatal" framing the reviewer assigned.
- *"Table 1 vs. Table 2 discrepancy (nucleotide vs. gene level)"* — The paper explains this conversion (line 333). The different levels serve different evaluation purposes.
- *"Standard errors over 3 inference seeds not 3 training runs"* — The paper states this clearly (line 282). The ±0.000 entries are noted as a trivial observation but are not a structural flaw.

## Novel Insights

The harsh reviewer correctly identified a pattern across the evaluation: the headline performance claims rely on comparisons that systematically favor the proposed method (CB receives more features than the Enformer baseline; CFM/DFM must operate on data outside their native type). This suggests a gap between the paper's claimed evidential strength and what the experiments actually isolate. At the same time, the core theoretical contribution—the Poisson birth-death bridge with closed-form conditionals—is genuinely novel and stands independently of the evaluation issues. The practical message is that the paper would be stronger if it reframed its empirical claims to match what the evidence supports, or added controlled comparisons that isolate the bridge architecture itself.

## Suggestions

1. Ablate the Enformer features in the nucleotide-resolution experiment: compare CB with and without Enformer embeddings, and give the fine-tuned Enformer the same auxiliary inputs (cell-type labels, etc.) that CB receives.
2. Replace or supplement the CFM/DFM synthetic comparisons with a count-native baseline (Blackout Diffusion or a Poisson-based method).
3. Specify the parametric family of $q_\theta$ (distribution type, factorized or joint) and report the number of samples $m$ used in the energy score estimator.
4. Validate the approximate E-step by comparing against a Monte Carlo E-step on a small-scale deconvolution task.
5. Add baselines to Fig. 4 and include convergence curves for the EM procedure.

## Score and Decision

The Poisson birth-death bridge with closed-form conditionals is a genuine theoretical contribution that fills a real gap in generative modeling of integer-valued data. The deconvolution framework is a natural and useful extension. The empirical evaluation, however, contains several comparisons that do not cleanly isolate the proposed method's contribution, and a few implementation details are underspecified. These issues are addressable and do not undermine the core method, but they weaken the reported performance claims as currently presented.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>