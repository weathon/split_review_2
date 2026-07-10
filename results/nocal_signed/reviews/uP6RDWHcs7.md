## Summary

This paper proposes Marginal Flow, a density estimation framework where the density is defined by marginalizing over a learnable distribution over latent parameters via resampling. The core idea is simple: sample parameters $w_i \sim q_\theta(w)$ (implemented as $f_\theta(z_i)$ with $z_i \sim p_{\text{base}}(z)$) and define $q_\theta(x) = \frac{1}{N_c}\sum_i q(x|w_i)$. This sidesteps Jacobian computation (normalizing flows), ODE solving (flow matching), and multi-step sampling (diffusion). The framework enables exact density evaluation (conditioned on the drawn $w_i$), efficient single-step sampling, unrestricted neural architectures, the ability to learn lower-dimensional manifolds, and training with multiple objectives.

## Strengths

- **Clear advantage on lower-dimensional manifolds (Figure 4, Section 2.3):** Setting $m < d$ in the base distribution with no architectural restrictions on $f_\theta$ is a genuine and well-demonstrated advantage over normalizing flows and flow matching, which require dimensionality-preserving bijections. The spiral example is visually compelling and directly supports this core claim.

- **Flexibility across objective functions (Section 2.3, Figure 8):** Marginal Flow can be trained with both forward KL (log-likelihood) and reverse KL (unnormalized target density), which is practically useful for scientific applications where one may have access to energy functions without samples. The paper demonstrates this concretely with synthetic experiments.

- **Simple and elegant core idea (Section 2.1):** The method defines a density as a mixture with resampled parameters, cleanly avoiding the technical constraints (Jacobians, ODEs, multi-step sampling) that complicate competing frameworks. This simplicity is itself a contribution — it makes the framework transparent and easy to extend.

- **Simultaneous efficiency on both sampling and density evaluation (Figure 3, Table 1):** The paper correctly identifies that most density models trade off efficiency between these two operations. Marginal Flow is efficient at both, and the mechanism is clearly explained: no Jacobians, no ODEs, no multi-step sampling required.

## Weaknesses

### Fatal
None.

### Major

- **The central design parameter $N_c$ is entirely unexamined.** $N_c$ controls the fundamental trade-off in the model: higher $N_c$ gives lower-variance density estimates and smoother learned densities but increases computation; lower $N_c$ is faster but noisier. Beyond the illustrative "e.g. 10" in Figure 1, the paper never states what $N_c$ values are used in *any* experiment, never analyzes how $N_c$ affects training dynamics or final quality, and provides no guidance on how to choose $N_c$. This is consequential because the claimed runtime advantages (Figure 3) and density quality both depend on $N_c$, and the reader cannot assess whether they survive under a fair comparison. **Why it matters:** This is not a minor hyperparameter — $N_c$ is the knob that controls the approximation-vs-computation trade-off of the entire method. Leaving it unstated and unanalyzed makes the empirical claims (orders-of-magnitude speedups, density quality) difficult to evaluate rigorously.

- **The "exact density" claim conflates exactness with a Monte Carlo estimate.** The paper defines $q_\theta(x)$ in Eq. 2 as a mixture of $N_c$ components sampled from $q_\theta(w)$. Because $w_i$ are *resampled* at each evaluation, the density at a given $x$ is a random variable that changes with each evaluation. Table 1 puts Marginal Flow alongside normalizing flows with an unqualified checkmark for "Efficient exact likelihood," but normalizing flows give the *same deterministic* density at $x$ every time, whereas Marginal Flow does not. The paper partially acknowledges this (line 64: "The resampling induces an *approximation* to the marginal distribution in Eq. 1"), but the framing and Table 1 overstate the case. **Why it matters:** This is the paper's central theoretical claim. Readers evaluating Marginal Flow for applications requiring deterministic log-likelihoods (e.g., Bayesian inference diagnostics) need to understand this variance. The paper should either define the model as the expectation in Eq. 1 and treat Eq. 2 as a finite-sample estimator, or explicitly discuss the variance introduced by resampling and its dependence on $N_c$.

### Minor

- **The MNIST and JAFFE manifold experiments (Section 4.4, Figures 10–11) lack any quantitative metrics.** The paper shows qualitative traversals of learned 1D manifolds but reports no reconstruction error, FID, log-likelihood, or downstream task metric. While the paper frames these as "showcase" demonstrations, they are presented as one of the four main experimental domains and the claimed manifold-learning capability would be significantly strengthened by at least one quantitative measure.

- **The Wishart mixture experiments (Section 4.3, Figure 9) report test KL values of ≈0.0088 for all three KL variants (sym., forward, reverse) for Marginal Flow.** Forward KL and reverse KL are computed differently and typically yield meaningfully different values for the same model. The paper does not discuss this. (Note: Normalizing Flow also shows uniform values — all ≈0.82 — which may indicate a computation or rounding artifact rather than a Marginal Flow-specific problem, but the point warrants clarification.)

### Trivial
None.

## Nice-to-Haves

- An ablation varying $N_c$ (e.g., 1, 10, 100, 1000) on a synthetic task reporting both log-likelihood and wall-clock time would directly address whether the "orders of magnitude faster" claim holds for the $N_c$ needed for good density estimation.
- A comparison with VAEs on the manifold learning task would be informative, given the structural similarity when $q(x|w)$ is Gaussian.
- Sensitivity analysis for architecture choices (layers, hidden dimensions) and base distribution dimensionality.

## Removed Points

These points from the input review are flagged for removal — treat with caution:

- **SBI results deferred to appendix:** Removed per policy — the appendix exists in the original submission (stripped by the parser). Criticizing that results are in the appendix is not a valid weakness for review purposes.
- **Missing related work / VAE discussion:** Removed per policy — do not penalize for absent related-work discussions.
- **GMM comparison fairness:** Removed — this is a methodological discussion point, not a concrete verified weakness.
- **Hyperparameter sensitivity:** Removed as a generic/unspecific concern not tied to a concrete failure.
- **Runtime advantages being on small 2D problems:** Partially addressed by Figure 3, which shows runtime scaling to $10^5$ dimensions.
- **Speculative "fatal" framings in the original review:** Removed — none of the identified weaknesses invalidate the core contribution; they are addressable gaps in presentation and analysis.

## Novel Insights

Beyond the paper's own contributions, the most notable observation from the review process is that the core weakness — the unexamined $N_c$ trade-off — is structurally connected to the overclaimed "exact density" framing. Addressing these two issues together (defining the model as $\mathbb{E}_{w\sim q_\theta}[q(x|w)]$ with a finite-$N_c$ estimator, and analyzing how estimator variance scales with $N_c$) would resolve both problems simultaneously while strengthening the paper.

## Suggestions

1. Report $N_c$ values for all experiments and provide an ablation showing how density estimate variance and wall-clock time scale with $N_c$.
2. Reframe the "exact density" claim: acknowledge that Eq. 2 gives an exact normalized density *conditioned on a draw of $w_i$*, and discuss the estimator variance (or provide bounds) for the marginal $q_\theta(x) = \mathbb{E}_{w\sim q_\theta}[q(x|w)]$.
3. Add at least one quantitative metric (reconstruction error or FID) to the image manifold experiments.
4. Clarify the Wishart KL computation — explain why all three KL variants yield effectively the same value.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>