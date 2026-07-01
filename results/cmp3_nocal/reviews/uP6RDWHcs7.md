## Summary

Marginal Flow proposes a density estimation framework where latent parameters **w** are marginalized out by resampling them from a learnable distribution \(q_\theta(\mathbf{w})\) rather than optimized directly. This avoids the expressiveness ceiling of finite mixture models (where capacity is capped by the number of components) while enabling efficient evaluation (no Jacobian determinants or ODE solves) and single-pass sampling. The paper demonstrates computational advantages (1–3 orders of magnitude faster than normalizing flows, flow matching, and free-form flows) and flexibility (lower-dimensional manifold learning, multi-modal targets, tunable parametric family \(q(\mathbf{x}|\mathbf{w})\)).

## Strengths

1. **Novel and conceptually clean core idea (Section 2.1).** The mechanism of marginalizing over latent parameters by resampling them from a learnable distribution, rather than optimizing a fixed set, is genuinely interesting. The contrast with a finite GMM (where expressiveness is capped by the number of components) is well motivated, and Figure 1 illustrates the difference convincingly. This is the paper's main intellectual contribution.

2. **Clear computational efficiency advantage (Section 2.2, Figure 3).** The runtime measurements show that Marginal Flow's evaluation and sampling costs scale favorably with dimension compared to Normalizing Flows (Jacobians), Flow Matching (ODE solves), and Free-form Flows. The observed 1–3 orders of magnitude speedup is structurally baked into the method: evaluating \(q_\theta(\mathbf{x})\) is just \(N_c\) evaluations of a closed-form density, and sampling is single-pass.

3. **Flexible framework (Section 2.3, Section 4.3).** The ability to swap the parametric family \(q(\mathbf{x}|\mathbf{w})\) (Gaussian, Wishart, Dirichlet) without changing the model structure is cleanly demonstrated. The Wishart mixture experiment (Section 4.3) handles positive-definite matrices by changing only the output distribution, not the architecture.

4. **Lower-dimensional manifold learning (Section 2.3, Figure 4, Section 4.4).** The ability to set \(m < d\) and learn densities on lower-dimensional manifolds is a genuine advantage over Normalizing Flows and Flow Matching, which preserve dimensionality. The synthetic spiral example (Figure 4) and the image latent-space experiments showcase this capability.

## Weaknesses

### Fatal

None.

### Major

1. **Inconsistent "exact density evaluation" claim.** The paper states repeatedly that Marginal Flow provides "exact density evaluation" — in the abstract (line 9), Table 1 (line 25), Section 2.2 ("only Marginal Flow and Normalizing Flow provide exact density by construction," line 145), Section 2.3 (line 155), and the conclusions (line 323). However, the model in Eq. 2 is a Monte Carlo average over \(N_c\) resampled latent parameters. The paper itself acknowledges this at line 64: "The resampling *induces an approximation* to the marginal distribution in Eq. 1." Evaluating Eq. 2 twice at the same \(\mathbf{x}\) with different draws of \(\{w_i\}\) produces different numbers, which is not what "exact density" means in the normalizing flows literature (where the density is a deterministic function of \(\mathbf{x}\)). This inconsistency is not a minor terminological quibble — the "exact likelihood" checkmark in Table 1 is how the paper distinguishes itself from GANs, VAEs, Flow Matching, and Free-form Flows. The paper should honestly characterize the density estimate as a stochastic (but unbiased) Monte Carlo approximation, analyze its variance as a function of \(N_c\), and adjust Table 1 accordingly.

2. **Density estimation quality is only demonstrated on low-dimensional problems.** The quantitative density estimation results are limited to 2D synthetic datasets (Two Moons, Pinwheel, Swiss Roll, Checkerboard, Mixture of Gaussians; Section 4.1, Figures 6–7). The Wishart experiment (Section 4.3, \(d=55\)) provides a quantitative KL divergence comparison against NF in one specialized setting, but there are no results on standard tabular density estimation benchmarks (e.g., UCI datasets with \(d=10\)–\(100\)) to establish that the method produces accurate density estimates in moderate dimensions. The runtime plots (Figure 3) scale to \(10^5\) dimensions, but these measure only speed — not whether the estimated density is accurate at those dimensions. Without moderate-dimensional density quality benchmarks, the paper's claim of being a "framework for density estimation" is only partially supported.

3. **Missing analysis of the critical hyperparameter \(N_c\).** The number of samples \(N_c\) used to evaluate \(q_\theta(\mathbf{x})\) directly controls the trade-off between Monte Carlo variance and computational cost. The paper states that \(N_c\) "is not required to be fixed" (line 58) but provides no analysis of how the density estimate's variance scales with \(N_c\) or dimension \(d\), no guidance on how a practitioner should choose \(N_c\), and no ablation study showing the effect of different \(N_c\) values on density quality or training behavior. This gap is essential for anyone who wants to use the method seriously.

### Minor

1. **Image experiments are purely qualitative (Section 4.4).** The MNIST and JAFFE experiments show interpolations along a learned 1D manifold, but there are no quantitative metrics — no reconstruction error, log-likelihood, or comparison against baselines. The JAFFE dataset has only 214 images, and the caption itself notes "inconsistencies." While these experiments serve as illustrative showcases, they do not provide evidence of practical utility.

2. **Figure 7 conflates architectural efficiency with statistical efficiency.** Test log-likelihood is plotted against wall-clock runtime, which conflates the fact that each Marginal Flow training step is cheaper (no Jacobians, no ODE solves) with whether the method requires fewer gradient steps to converge. Plotting test log-likelihood against training steps or epochs would disentangle these factors and strengthen the comparison.

3. **No quantitative comparison against a GMM baseline despite using GMMs as motivation.** The paper motivates its marginalization approach by contrasting with GMMs (Figure 1, line 64) but never compares Marginal Flow against a well-tuned GMM on any experimental task. For the 2D synthetic experiments especially, a GMM with a sufficient number of components is a natural and computationally cheap baseline that should be reported.

4. **Lower-dimensional manifold density normalization (Section 2.3).** When \(m < d\), the paper states the density can be evaluated "exactly" but does not discuss how the density is defined with respect to the Lebesgue measure on \(\mathbb{R}^d\) when the means \(w_i\) lie on an \(m\)-dimensional manifold. While the Gaussian \(q(\mathbf{x}|\mathbf{w})\) provides full support on \(\mathbb{R}^d\) and avoids degeneracy, the relationship between the manifold structure and the density's behavior is not discussed.

5. **Table 1 uses parenthetical qualifiers without explanation.** The "Efficient training" row marks FM as \((\checkmark)\) and FFF as \((\checkmark)\) without explaining what the parentheses signify.

### Trivial

None.

## Nice-to-Haves

- Provide a study of how \(N_c\) affects the variance of the density estimate and include practical guidance for choosing \(N_c\).
- Add a quantitative GMM baseline comparison for the 2D synthetic experiments.
- Report the SBI results (currently deferred to the appendix) with at least a summary table in the main text.
- Discuss training stability and sensitivity to optimizer/hyperparameter choices, particularly for reverse KL training.

## Removed Points

These points were raised in the input review but are removed per policy:

- **SBI results deferred to appendix:** The criticism that SBI results are "vacuous in the main text" is removed because the appendix exists in the original submission; the parser stripped it. The paper's main-text claim of "state-of-the-art results" without supporting numbers remains a presentation concern but is addressed in Nice-to-Haves.
- **Fragmentary sentence at line 17–18:** This is a parser artifact from a page break, not an author error.
- **FFF failure on multi-modal targets unexplained:** The paper is not required to explain why every baseline fails on every task; this is an observation, not a weakness.

## Novel Insights

The key insight that emerges from synthesizing the reviews — and that goes beyond the paper's own framing — is that Marginal Flow's central contribution is best understood as *architecture-level amortization* of mixture-model expressiveness. By learning a continuous distribution \(q_\theta(\mathbf{w})\) over mixture parameters and resampling at each evaluation, the model decouples its effective capacity from its parametric footprint in a way that finite mixture models cannot. Nearly all the criticism traces back to the same root: the paper overclaims the "exactness" of this stochastic evaluation while underdelivering on the empirical evidence needed to support the claim that the approximation is good enough in realistic settings. The paper would be substantially stronger if it leaned into the stochastic nature of its density estimate and provided the variance/\(N_c\) analysis that makes this framing honest and useful, rather than claiming parity with normalizing flows on a property (deterministic exactness) that the method structurally does not possess.

## Suggestions

1. **Reframe the density as a stochastic Monte Carlo estimate** (unbiased, variance controlled by \(N_c\)) rather than as "exact." Update Table 1, abstract, and all claims accordingly. Add a footnote or brief analysis of how \(N_c\) affects estimate variance.
2. **Add at least one moderate-dimensional density estimation benchmark** (e.g., UCI tabular data, \(d=10\)–\(100\)) with log-likelihood comparisons against NF, FM, and a GMM baseline. This would directly address the largest evidential gap.
3. **Include an ablation on \(N_c\)** showing how density quality (test log-likelihood or KL) changes with \(N_c\) on a representative problem.
4. **Add quantitative metrics to the image experiments** or reframe them as purely illustrative showcases without claiming practical utility.

## Score and Decision

**Score:** 5.5

**Decision:** Accept (with major revisions)

*Rationale:* The core idea is novel and the computational efficiency advantage is well-supported. The flexibility (manifold learning, choice of \(q(\mathbf{x}|\mathbf{w})\)) is convincingly demonstrated. However, the "exact density" framing is misleading and needs correction, the density estimation quality evidence is limited to very low dimensions, and the \(N_c\) hyperparameter is unanalyzed. These weaknesses are addressable through rewording and additional experiments; they do not invalidate the core contribution.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>