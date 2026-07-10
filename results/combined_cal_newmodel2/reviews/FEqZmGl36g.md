Now let me compile my final review.

## Summary

This paper introduces ESS-Flow, a training-free method that uses Elliptical Slice Sampling (ESS) in the source space of pretrained flow-based generative models for conditional generation. The key insight is that the Jacobian terms cancel when expressing the posterior in source space, reducing the target to the Gaussian prior times the pullback potential, enabling gradient-free posterior sampling. The method is demonstrated on materials design (bulk modulus, shear modulus, band gap, stability, space-group targeting) and protein structure prediction.

## Strengths

- **Elegant and well-motivated core idea (Section 4, Eq. 3).** The observation that the Jacobian terms cancel when expressing the posterior in source space — reducing the target to the Gaussian prior times the pullback potential — is mathematically clean and sidesteps backpropagating through an ODE solver that gradient-based source-space methods require.

- **Material generation results are genuinely strong (Table 2, Table 3).** On bulk modulus, ESS-Flow achieves a mean absolute error of 8.99 vs. 39.14 for the next-best method (DAPS), and for shear modulus 10.53 vs. 84.33. The histograms in Figure 3 show ESS-Flow concentrating samples near the target in a way no baseline does.

- **The space-group experiment (Section 5.1, Table 3) convincingly demonstrates a setting where gradient methods cannot operate.** The binary indicator potential from a non-differentiable external program is a concrete illustration of the paper's central motivation. ESS-Flow achieves 92.3% target space-group rate vs. 2.5% unconditional — and no gradient-based baseline is even attempted.

- **Clear theoretical grounding.** Proposition 1 (geometric convergence) is adapted from established results, and the paper states the assumptions under which it holds.

## Weaknesses

### Major

- **The protein experiment framing overstates the contribution (Section 5.2, Table 4).** ESS-Flow's `d_y` (37.02) is an order of magnitude worse than ADP-3D (3.43) and 3× worse than DAPS (11.79). Its RMSD to ground truth (13.55) is the worst of any conditional method, and its ELBO (8.89) is essentially identical to unconditional Chroma sampling (8.70). The paper claims a "better trade-off between data fidelity and sample realism" (Figure 4 caption), but with these numbers the method has largely failed to condition on the data. ADP-3D and DAPS produce unrealistic structures (clash counts 731.3 and 483.3 vs. 24.8), so neither camp is satisfactory — but framing this as a favorable trade-off rather than a clear limitation of ESS-Flow misrepresents the evidence. The paper acknowledges "this problem remains challenging for all methods," but the conclusion and Figure 4 caption go beyond what the evidence supports.

### Minor

- **The multi-fidelity contribution (Section 4.2) has severely limited practical value.** Effective sample sizes of 0.1% and 1.0% (reported for band gap and stability tasks in Section 5.1.1) mean importance weighting is essentially collapsing — one or two samples dominate the entire weighted estimate. While the paper acknowledges this as a "shortcoming" and calls it a "proof of concept," it is listed as one of four bulleted contributions in the introduction. A contribution that demonstrably fails on half the tasks tested should either be substantively improved or removed from the contribution list.

- **Low U.N. (uniqueness + novelty) rates reveal a diversity cost not adequately discussed (Table 3).** ESS-Flow's U.N. rates for bulk modulus (46.1) and shear modulus (30.5) are substantially lower than DAPS (80.8 and 74.6). This is a natural consequence of MCMC producing correlated samples, but the paper does not discuss diversity or effective sample size in the material generation experiments. The S.U.N.T. metric masks this because the T (target rate) term dominates.

- **Scalability to high-dimensional source spaces is not discussed in the main text.** ESS's acceptance rate degrades as dimensionality grows. The paper references a scaling analysis in Appendix A.1, but the main text provides no summary or caveat about practical limits for readers evaluating ESS-Flow for high-dimensional problems (e.g., images with source dimensions in the tens or hundreds of thousands).

### Trivial

- None.

## Nice-to-Haves

- A brief qualitative statement in the main text about how ESS-Flow's acceptance rate scales with source dimension.
- A sentence or two discussing the diversity (U.N.) limitation in the material experiments and how it relates to the MCMC nature of the method.

## Removed Points

These points from the input review were removed with justification:

- **DAPS adaptation fairness concern**: Removed because the paper states the adaptation details are in the appendix (stripped by parser). This criticism cannot be evaluated without access to content that exists in the original submission.
- **Missing comparison against Wang et al. (2025)**: The paper correctly acknowledges this as concurrent work; requiring a comparison against a method discovered after submission is not standard.
- **Missing MCMC diagnostics (R-hat, ESS, trace plots)**: Scope creep for the main text. The paper reports means and standard deviations, which is appropriate for a methods paper.
- **Toy example uses D-Flow as only comparator**: D-Flow is the most relevant gradient-based source-space baseline; the comparison serves its purpose.
- **Runtime/NFE not in main text**: The paper states these are in the appendix (stripped by parser).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the protein experiment honestly**: Acknowledge that ESS-Flow largely fails to condition effectively on this task and use it to delineate the regime where the method is appropriate (when the potential is diffuse relative to the prior spread) versus where it is not (concentrated potentials).
2. **Either remove or substantively improve the multi-fidelity contribution**: If it remains, it should not be listed as a main contribution. If it is kept, explore more principled multi-fidelity approaches (e.g., delayed acceptance ESS).
3. **Add a brief discussion of the diversity limitation** in the material generation experiments, explaining the MCMC correlation effect and its implications for scientific discovery.
4. **Include a scaling caveat in the main text** — even a single sentence noting that ESS acceptance rates degrade with source dimension.

## Score and Decision

**Round-1 bracket:** [6.0, 7.5] — the paper is clearly above the 4–5 level of papers with weak experiments or unclear theory (e.g., AC1QLOJK7l at 4.00, 0QJPszYxpo at 5.00) and below the 8.0 level of papers with uniformly strong evaluations and no overclaiming (e.g., 6EUtjXAvmj at 8.00).

**Narrowing:** Comparing against anchors inside the bracket:
- **GK5ni7tIHp** (avg 6.25, Accept): TFG-Flow for multimodal molecular design. ESS-Flow has stronger quantitative improvements (factor-of-several vs. marginal gains) and a cleaner core idea. ESS-Flow is above this anchor.
- **61ss5RA1MM** (avg 6.50, Accept): OC-Flow for guided flow matching. Comparable in quality: OC-Flow has stronger theory, ESS-Flow has stronger empirical results. Similar level.
- **kIPEyMSdFV** (avg 7.00, Accept): rdMC for reverse diffusion sampling. rdMC had weaker experimental support (2D toy example). ESS-Flow has more comprehensive experiments. Comparable level.

**Final score:** 6.5

The paper's top favorability items (material results at 15.48, space-group experiment at 14.85) are as strong as the top items in the 6.5–7.0 anchors (OC-Flow top item at 15.26, rdMC top item at 12.49). The damaging items (multi-fidelity at -2.64, "better trade-off" claim at -2.11) are moderate but addressable. No anchor in this range is free of comparable issues.

**Decision:** Accept

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>