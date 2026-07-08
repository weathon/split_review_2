Now I have a clear picture of the calibration landscape. Let me compile my final review.

## Summary

The paper presents ESS-Flow, a training-free method for controlled generation with pretrained flow-based generative models. The key insight is that writing the posterior in the source space cancels the Jacobian determinant of the transport map (Equation 3), reducing the problem to sampling from a Gaussian prior times a potential — a setting perfectly suited for Elliptical Slice Sampling (ESS). This yields a gradient-free method requiring only forward passes through the ODE and potential. The paper demonstrates ESS-Flow on materials design (bulk modulus, shear modulus, band gap, space group) and protein structure prediction from sparse inter-residue distances.

## Strengths

- **Clean mathematical insight (Equation 3).** The observation that expressing both prior and posterior in the source space cancels the Jacobian determinant, reducing controlled generation with flow models to sampling from a Gaussian prior times a potential, is genuinely elegant. This makes the connection to elliptical slice sampling immediate and natural — a nontrivial synthesis of two existing ideas.

- **Genuinely gradient-free.** The method requires only forward passes through the ODE and the potential, with no backpropagation through the ODE solver. The space-group experiment (Section 5.1) uses a binary indicator from a non-differentiable external program (Togo et al., 2024), providing a concrete demonstration of a setting where gradient-based methods cannot be applied. This is a real and clean advantage over D-Flow, Purohit et al. (2025), and Wang et al. (2025).

- **Strong materials results on the core metric.** In Table 2, ESS-Flow achieves dramatically lower absolute errors — e.g., 8.99 GPa for bulk modulus vs. 39.14 for the next best DAPS, and 10.53 GPa for shear modulus vs. 75.48 for PnP-Flow. The property histograms in Figure 3 visually confirm that ESS-Flow concentrates mass near the target while other methods remain diffuse.

## Weaknesses

### Major

1. **Protein results weaken the paper's narrative.** ESS-Flow achieves substantially worse data fidelity (d_y = 37.02 vs. ADP-3D's 3.43 and DAPS's 11.79) and worse RMSD_gt (13.55 vs. 11.45 and 11.41) on the protein structure prediction task (Table 4). The ELBO improvement over unconditional sampling is marginal (8.89 vs. 8.70). The paper's framing as a "better trade-off" is charitable — ESS-Flow sacrifices data fidelity while achieving only modest improvements in realism over the unconditional prior. Furthermore, only 10 structures are generated per method (line 244), making statistical comparisons unreliable given the reported standard deviations (e.g., RMSD_gt stds of 1.17–1.52 across methods with means differing by ~2 Å). This experiment does not demonstrate success; it reveals that for highly underdetermined inverse problems where the posterior differs substantially from the prior, the gradient-free MCMC approach is not competitive on the primary objective.

2. **Missing MCMC diagnostics.** ESS-Flow is an MCMC method, yet the paper provides no trace plots, effective sample size (ESS is reported only for the multi-fidelity ablation, not the main experiments), autocorrelation analysis, burn-in discussion, or chain-length details. Proposition 1's geometric convergence guarantee requires the pullback potential to be "bounded away from 0 and ∞ on compact sets" (line 103), which may not hold for the binary indicator potential used in the space-group task (which is 0 almost everywhere, and thus not bounded away from 0). Without empirical diagnostics, readers cannot assess whether the chains have converged to the target distribution.

### Minor

3. **Multi-fidelity contribution overclaimed.** The importance-weighting approach yields effective sample sizes of only 0.1% and 1.0% for the band gap and stability tasks (line 203), where sharper targets make it most needed. While the paper honestly acknowledges this shortcoming and calls the approach a "proof of concept" (line 193), listing it as a contribution (line 40: "We propose a multi-fidelity extension of ESS-Flow...") overstates what has been demonstrated.

4. **Chroma modification unvalidated.** The paper modifies Chroma's random protein graph construction to use k-nearest neighbors and generates samples with the probability flow ODE (line 207), but does not validate that this modified version still produces realistic unconditional samples. This could affect prior quality in the protein experiments.

5. **Figure 2 compares against an optimization method on a sampling task.** The toy example compares ESS-Flow against D-Flow (a MAP optimization method, not a sampler). A comparison against source-space Langevin Monte Carlo (Purohit et al., 2025) or HMC (Wang et al., 2025) would be more informative for evaluating ESS-Flow's sampling behavior.

### Trivial

None.

## Nice-to-Haves

- Add a dedicated MCMC diagnostics figure showing trace plots, autocorrelation, and running ESS estimates for the main experiments.
- Increase the protein experiment sample size (substantially beyond n=10) to enable statistically meaningful comparisons, or reframe the claims more modestly.
- Validate the modified Chroma model by comparing unconditional sample quality against the original.
- Report wall-clock time or NFE per sample for all methods on all tasks, even if these are deferred to the appendix, to help readers calibrate the computational trade-offs.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Computational budget accounting.** The harsh critic argued that without runtime reporting the Table 2 comparison is uninterpretable. However, the paper states on line 183 that "Hyperparameter details and the runtime costs of the methods are provided in the Appendix." Per hard rules, the appendix is stripped by the parser but exists in the original submission. REMOVED per rule: "REMOVE criticisms about missing appendix, missing proofs in appendix."

2. **Introduction overstated about 'point estimates'.** The critic claimed the paper says DAPS provides only point estimates. In fact, the introduction (line 17) says "optimization-based methods...only provide point estimates." DAPS is correctly classified as a sampling method in Related Work (line 63). The critic misread this passage. REMOVED — factually incorrect.

3. **Algorithm 1 notation ambiguity.** The critic flagged the acceptance criterion's use of log g(x') as notationally ambiguous. The criterion is standard: x' = T_θ(z'), so log g(x') = log g(T_θ(z')) is correct. This is a formatting/notation nitpick. REMOVED.

4. **Table 3 lower U.N. rates not discussed.** The critic claimed the paper does not discuss reduced diversity in S.U.N.T. rates. The paper explicitly addresses this on line 189: "The S.U.N. rates are naturally low compared to unconditional generation, but they should be viewed in light of the fact that we are (successfully) targeting extreme values." REMOVED — paper already addresses this.

5. **No standard image benchmarks.** The critic faulted the paper for not including image inpainting/super-resolution benchmarks. The paper explicitly scopes itself to scientific domains where the prior well-informs the target (line 43): "The primary use-case for ESS-Flow is thus applications, e.g. in scientific domains, where the target distribution is not overly-collapsed." REMOVED — outside stated scope.

## Novel Insights

None beyond the paper's own contributions. The key observation (source-space inference with ESS cancels the Jacobian) is the paper's own contribution, and the reviews do not surface any unclaimed insight.

## Suggestions

- Reframe the protein experiment more modestly: acknowledge that ESS-Flow trades data fidelity for structural realism, and that the problem remains challenging for all methods. Consider increasing the sample size substantially or running additional chains to improve statistical reliability.
- Add a dedicated MCMC diagnostics figure to the main paper or appendix showing trace plots, running ESS estimates, and autocorrelation for the materials experiments.
- Remove the multi-fidelity approach from the contributions list or reframe it as a negative result with analysis of failure modes.
- Validate the modified Chroma model by presenting unconditional sample quality metrics against the original Chroma.
- In the toy example (Figure 2), consider also including a comparison against a gradient-based source-space sampling method (e.g., Purohit et al., 2025) to make the illustration more informative.

## Score and Decision

**Round 1 bracket:** 5.5–7.5 (anchored by OC-Flow at 6.50 and other flow-based controlled generation papers).

**Round 2 narrowing:** Compared item weights between the paper under review and the most topically similar anchors. The paper's strengths (8.93–9.93) are comparable to OC-Flow's peak strengths (8.48–12.44, avg 6.50, Accept), and substantially stronger than Controlled Denoising (avg 4.60, Reject) and Flow Matching for Posterior Inference (avg 4.20, Reject). The paper's worst negative-weighted weakness (−1.14 for protein results) is milder than OC-Flow's worst (−3.80 for reproducibility), but OC-Flow has more extensive theoretical grounding and a broader experiment suite. The missing MCMC diagnostics weakness receives a slightly positive weight (0.52) from the scoring model, suggesting it is not a major concern in the corpus. The protein results weakness and the overclaimed multi-fidelity contribution are the primary drags.

**Final score:** 6.0. The paper has a genuinely novel and elegant idea with strong empirical results on materials; the protein results are weak and the presentation overclaims on multi-fidelity. At this score the paper is a borderline accept — the core contribution is solid and the method fills a genuine gap, but the evidence as presented needs strengthening.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>