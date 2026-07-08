## Summary

This paper proposes Marginal Flow, a density estimation framework where the model is defined through a parametric conditional $q(x|w)$ with latent parameters $w$ that are marginalized out via sampling from a learnable implicit distribution $q_\theta(w)$. The key idea is that the method never needs to evaluate $q_\theta(w)$ — only to sample from it — which removes architectural constraints (no bijectivity, no Jacobian computation, no ODE solvers). This enables flexible adaptation to different data types, training with forward or reverse KL, learning on lower-dimensional manifolds, and efficient simultaneous sampling and density evaluation.

## Strengths

- **Genuinely flexible framework architecture (Sections 2.1–2.3):** The core idea — defining a model through a parametric conditional $q(x|w)$ with a learnable implicit distribution over $w$ — is simple and modular. No bijectivity constraints, no Jacobian computation, no ODE solvers needed. This allows easy adaptation to different data types by swapping $q(x|w)$ (Gaussian, Wishart, Dirichlet) and different training objectives (forward and reverse KL). This is a genuine architectural advantage over Normalizing Flows and Flow Matching / Diffusion models.

- **Strong empirical demonstration on Wishart mixture distributions (Section 4.3, Figure 9):** For $10\times10$ Wishart mixtures, Marginal Flow achieves test KL divergences of $\approx 0.0088$ across forward, reverse, and symmetric KL, versus $\approx 0.82$ for Normalizing Flow — roughly two orders of magnitude better. The model also scales to $100\times100$ matrices ($d=5050$) where NF cannot train, and correctly recovers the 1D manifold. This is a clean, quantitative demonstration of the framework's effectiveness in a nontrivial setting.

- **Ability to learn on lower-dimensional manifolds (Section 2.3, Figure 4):** By simply setting the base distribution dimension $m < d$, Marginal Flow handles a setting that Normalizing Flows and Flow Matching cannot address by design. The spiral example shows this working, and Marginal Flow appears to learn the correct manifold where Free-form Flow does not.

- **Favorable efficiency profile (Section 2.2, Figure 3):** The method is orders of magnitude faster than NF and FM for both sampling and density evaluation across dimensions $10^2$ to $10^5$, and competitive with Free-form Flows. This efficiency profile — fast sampling AND fast density evaluation — is rare among deep generative models.

## Weaknesses

### Fatal
None.

### Major

- **The "exact density evaluation" claim is unqualified and conflates Monte Carlo estimation with deterministic exactness.** The model in Eq. 2 defines $q_\theta(x) := \frac{1}{N_c} \sum_{i=1}^{N_c} q(x|w_{\theta,i})$ where $w_{\theta,i} \sim q_\theta(w)$. For any finite $N_c$, this is a stochastic quantity — two evaluations with different random seeds give different values — whereas Normalizing Flows provide a deterministic density that is a function of $x$ alone. The paper repeatedly asserts "exact density evaluation" (abstract, Table 1, Section 2.2, conclusion) in the same category as NF without ever discussing the Monte Carlo variance, how $N_c$ controls the stochasticity, or how this affects downstream tasks. The paper should (a) clearly distinguish the finite-$N_c$ Monte Carlo estimate from the ideal marginal $\int q(x|w)q_\theta(w)dw$, (b) characterize the approximation error, and (c) qualify the checkmark in Table 1. This is not a terminological nitpick — for practical use of the density (test log-likelihood, downstream inference), the stochasticity matters.

### Minor

- **The multi-modal experiment (Figure 5) compares structurally different model classes without the most natural baseline.** Marginal Flow with $q(x|w) = \mathcal{N}(x|\mu=w, \Sigma=\sigma^2)$ is functionally a mixture of Gaussians with learnable means — a model class that trivially handles multimodality. The baselines (NF, FM, FFF) learn bijections from a unimodal base distribution, so the comparison is structurally slanted. The paper would benefit from including a standard Gaussian Mixture Model (with a learned number of components) as a baseline to demonstrate whether the resampling mechanism adds value over fixed-component mixtures, especially since the paper argues MF "is not a mixture model" while simultaneously depending on mixture-like behavior.

- **The image manifold experiments (Section 4.4) are purely qualitative with no quantitative evaluation or baselines.** The results on MNIST and JAFFE are presented as anecdotal observations ("some sections look approximately bold, bold italic and normal font", "disentanglement of faces and emotions"). There are no likelihood or sampling quality metrics, no comparison to simpler alternatives (e.g., linear interpolation in VAE latent space, PCA-based manifold), and no assessment of whether the learned manifold is actually better than alternatives. The JAFFE dataset has only 214 images, making the "disentanglement" claim particularly tenuous without quantitative support.

- **No guidance on choosing the critical hyperparameter $N_c$.** $N_c$ controls both the quality of the density estimate (via Monte Carlo variance) and the computational cost, yet the paper never discusses how to set it, what values were used in experiments, or the trade-off involved.

- **No analysis of the Monte Carlo variance of the density estimate.** Given that the density estimate is stochastic (finite $N_c$), the paper should report the variance of $\hat{q}_\theta(x)$ across random seeds and show that training is not harmed by the gradient noise from finite $N_c$. Without this, it is unclear how reliable the reported log-likelihood values are or how to interpret comparisons where the baseline's density is deterministic.

### Trivial
None.

## Nice-to-Haves

- Including a standard GMM baseline (with an appropriate number of components via BIC or Dirichlet process) for the multi-modal and synthetic experiments would clarify whether the resampling mechanism adds value beyond a well-tuned finite mixture.
- Adding quantitative metrics and a simple baseline (e.g., linear interpolation in VAE latent space) to the image manifold experiments would strengthen Section 4.4.
- A brief discussion of how to choose $N_c$ as a function of dimension, kernel width, and desired precision would improve practical utility.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. "The GMM comparison in Figure 1 is set up to make MF look better than warranted" — REMOVED. The figure's purpose is pedagogical: it illustrates WHY marginalization helps, not a competitive benchmark. The paper compares MF (resampled components) against GMM (fixed components) with the same $N_c$ to demonstrate the conceptual benefit of marginalization. This is correctly framed as motivation, not a quantitative claim.
2. "SBI results claim SOTA but are in the appendix" — REMOVED per hard rule: the parser strips appendix sections from all papers. The results exist in the original submission.
3. "Runtime analysis missing details ($N_c$, NF architecture)" — REMOVED per hard rule on missing appendix. The paper references "Appendix Section A.3.1" for further details.
4. "Reverse KL results need error bars" — REMOVED. The Figure 8 caption explicitly states "95% confidence intervals error bars" are present.
5. "No comparison against a standard GMM with many components" — Merged into the multi-modal experiment weakness above.

## Novel Insights

The key observation that emerges from the review is that the paper's central claim of "exact density evaluation" conflates the Monte Carlo nature of the marginal estimate with the deterministic exactness provided by Normalizing Flows. The model in Eq. 2 defines a stochastic density estimate, but the paper systematically treats it as equivalent to NF's exactness without qualification. This is not a fatal flaw — the framework itself is valid and useful — but it is a meaningful overclaim that should be corrected. Beyond this point, the paper's limitations are primarily about experimental scope (missing baselines, qualitative-only evaluations) rather than fundamental methodological weaknesses.

## Suggestions

1. **Qualify the "exact density" claim throughout.** Distinguish between the finite-$N_c$ Monte Carlo estimate and the ideal marginal. Characterize the approximation error (Monte Carlo variance as a function of $N_c$, dimension $d$, and kernel width). Report variance of the density estimate across random evaluations.
2. **Add a standard GMM baseline** to the multi-modal experiment to clarify whether resampling adds value over fixed-component mixtures.
3. **Add quantitative metrics and a simple baseline** (e.g., linear interpolation in VAE space) to the image manifold experiments.
4. **Discuss how to choose $N_c$** and report the values used in each experiment.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>