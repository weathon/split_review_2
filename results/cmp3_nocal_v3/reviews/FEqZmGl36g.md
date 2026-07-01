## Summary

This paper proposes ESS-Flow, a gradient-free method for controlled generation with pretrained flow-based generative models. The key insight is to reformulate Bayesian inference in the source space (where the prior is Gaussian) rather than data space, which cancels the Jacobian determinant and enables the use of Elliptical Slice Sampling (ESS). ESS-Flow requires only forward passes through the generative model and potential function, avoiding gradients entirely. The method is demonstrated on materials design (targeting bulk modulus, shear modulus, band gap, stability, and space-group symmetry) and protein structure prediction from sparse inter-residue distance measurements, showing strong results particularly in the materials domain.

## Strengths

1. **Clean and elegant methodological insight (Section 4.1, Equation 3).** The derivation showing that the Jacobian determinant cancels when both prior and posterior are expressed in source space is simple but important, enabling gradient-free MCMC without backpropagating through the ODE. This correctly identifies a structural advantage over gradient-based source-space methods (D-Flow, source-space HMC/Langevin) which still require the Jacobian for gradient computations.

2. **The gradient-free property solves a genuine and under-served problem.** The space-group targeting experiment (Section 5.1, Table 3) is a clean demonstration: the potential is a binary indicator from a non-differentiable external program (Togo et al., 2024), where no gradient-based method can be applied. ESS-Flow achieves 81.9% target rate vs. 2.3% unconditional — this is not a synthetic toy but a naturally occurring scientific constraint.

3. **Materials generation results are strong and consistent (Tables 2 and 3).** ESS-Flow achieves MAEs of 8.99 (bulk modulus), 10.53 (shear modulus), and 1.85 (band gap) — dramatically lower than the best baseline DAPS (39.14, 84.33, 3.90). The S.U.N.T. rates (Table 3) show ESS-Flow achieving the highest combined rate across all four property tasks. These improvements are large in magnitude and consistent across tasks.

4. **The protein experiment design is more realistic than prior work.** The authors improve on Levy et al. (2024) by adding a 6Å cutoff and Gaussian noise to the distance observations, making the inverse problem properly underdetermined. The ELBO and clash-count analysis (Table 4) correctly identifies that ADP-3D and DAPS sacrifice structural realism for data fidelity — an important observation that validates the case for Bayesian sampling approaches.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Numeric inconsistency in space-group results.** The text (Section 5.1, line 185) states ESS-Flow generates "92.3% of samples with the target P6₃/mmc space group, compared to only 2.5% when sampling unconditionally." However, Table 3 reports a target rate (Tᵣ) of 81.9% for ESS-Flow and 2.3% unconditional. These discrepancies — roughly 10 percentage points for ESS-Flow and 0.2 points for unconditional — need clarification. If different denominators are used (e.g., all generated samples vs. valid samples only), this should be explicitly stated. This is a presentation error in a non-core quantitative claim, not a threat to the paper's main results.

2. **The main paper lacks a summary of computational cost.** The paper notes that "Hyperparameter details and the runtime costs of the methods are provided in the Appendix" (line 183), but the main paper gives no wall-clock time or NFE comparison across methods. Given that ESS-Flow is an MCMC method requiring many sequential ODE solves, a practitioner evaluating the method needs a sense of the computational budget. A one-line summary table in the main paper (even brief) would resolve this.

3. **Framing of protein results is slightly lopsided.** The abstract claims "improved structural realism in proteins." This is supported by ELBO (ESS-Flow: 8.89 vs. ADP-3D: -5.68 vs. DAPS: -8.07) and clash counts (24.8 vs. 731.3 vs. 483.3), which are stark differences. However, ESS-Flow's data fidelity (d_y = 37.02) is substantially worse than ADP-3D (3.43) and DAPS (11.79). The paper does acknowledge this trade-off honestly in the discussion (Section 5.2, lines 256-257), but the abstract and contributions list present the protein result as a clean win. The framing would be more accurate as "improved structural realism at the cost of data fidelity."

4. **Equation (4) contains a notational/derivation issue.** In the multi-fidelity section (Section 4.2), the fraction g(T_δ^Δ(z))/g(T_δ^Δ(z)) cancels to 1, making the derivation appear circular as written. The notation T_δ^Δ (with δ as subscript and Δ as superscript) is also confusing given the text says δ ≪ Δ. The intent is clear — importance-weighting coarse samples with fine evaluations — but the equation as stated does not communicate it correctly. Since this section is presented as a "proof of concept" with acknowledged poor results on sharp targets (0.1% ESS for band gap), this does not affect the core contribution.

5. **The method's limitation when the prior poorly covers the target is acknowledged but not experimentally characterized.** The paper states (Section 1, Conclusion) that ESS-Flow struggles "when the prior does not well inform the target distribution" — but there is no experiment or diagnostic that quantifies or visualizes this failure mode. For a paper proposing an MCMC method for controlled generation, some empirical sense of when the method breaks down would strengthen the reader's understanding. This is a completeness gap, not a fatal one.

### Trivial
None.

## Nice-to-Haves

- **Convergence diagnostics for the MCMC chains.** ESS-Flow is a sampling method, but the main paper reports only means and standard deviations without effective sample size, Gelman-Rubin \hat{R}, or trace plots for the primary experiments. Such diagnostics would help readers assess whether chains have mixed, especially given the high-dimensional source space.
- **A controlled experiment isolating the gradient-free advantage.** The paper's strongest claim is that ESS-Flow is valuable when gradients are unreliable. A natural complement would be to compare ESS-Flow against source-space HMC/Langevin (Wang et al., 2025; Purohit et al., 2025) on a problem where gradients *are* well-behaved, quantifying the computational cost of being gradient-free. These methods are noted as concurrent work, so their absence from the experiments is understandable, but such a comparison would sharpen the contribution.

## Removed Points

These points from the input review were removed with justification:

- **"D-Flow comparison is systematically disadvantaged."** (REMOVED from Major category, downgraded to minor-adjacent observation.) The paper is transparent about the continuous relaxation (Eq. 5, τ=0.1) and explains why D-Flow struggles. The comparison is not "systematically disadvantaged" — it is a demonstration that gradient methods fail on problems with discrete variables, which is exactly the paper's thesis. DAPS (which handles discreteness via Metropolis-Hastings) also outperforms D-Flow but still performs far worse than ESS-Flow (MAE: 39.14 vs. 8.99 for bulk modulus), showing the advantage is not purely an artifact of the comparison design.

- **"Missing comparison against source-space HMC/Langevin."** (REMOVED.) The paper explicitly states these are concurrent works (line 65: "In work which is concurrent to ours, Wang et al. (2025) use Hamiltonian Monte Carlo in the source space"). Expecting experimental comparison with truly concurrent work is unreasonable. This is moved to a nice-to-have.

- **"Missing wall-clock time — critical omission."** (WEAKENED to Minor.) The paper states runtime details are in the Appendix (line 183). The parser stripped the appendix. The reasonable remaining point is that the main paper lacks a summary comparison.

- **"Protein results are mixed / claim is selective."** (WEAKENED to Minor.) The paper honestly reports all metrics and discusses the trade-off in the body. The criticism applies narrowly to the abstract's framing — the paper itself is transparent.

## Novel Insights

The most valuable insight emerging from the review is the tension between the paper's two domains of demonstration. The materials experiments show that when the target distribution is not overly sharp and the potential is non-differentiable, ESS-Flow dramatically outperforms all baselines — this is a clean win. The protein experiments reveal the method's boundary: when the posterior is concentrated (sharp target, underdetermined problem), ESS-Flow produces realistic but low-fidelity structures. This suggests the method's practical niche is applications where the potential is broad or the observation model is noisy — exactly the scientific inverse problems the paper targets. The review's implicit challenge is to make this boundary explicit through controlled experiments rather than leaving it as a post-hoc observation.

## Suggestions

1. Resolve the space-group percentage discrepancy (92.3% vs. 81.9%, 2.5% vs. 2.3%) — clarify the denominator or correct the numbers.
2. Add a brief computational cost summary to the main paper: approximate NFE per valid sample and relative wall-clock time per method.
3. Add a sentence clarifying that the abstract's "improved structural realism in proteins" comes with a data-fidelity trade-off.
4. Fix the notation in Equation (4) so the multi-fidelity derivation is mathematically sound as written.
5. Consider adding a simple diagnostic experiment (e.g., a 1D or 2D toy) that shows how ESS-Flow's performance degrades as the target becomes sharper relative to the prior, giving readers an empirical sense of the method's failure regime.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>