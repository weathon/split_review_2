## Summary

ESS-Flow proposes to use Elliptical Slice Sampling in the Gaussian source space of flow-based generative models for gradient-free controlled generation / Bayesian inference. The key insight is that expressing the posterior in source space cancels the Jacobian determinant (Eq. 3), enabling MCMC with only forward passes through the transport map. The method is demonstrated on materials design with target properties and protein structure prediction from sparse distance measurements.

## Strengths

- **Clean, principled core idea.** The observation that reparameterizing the posterior in source space cancels the Jacobian term (Eq. 3) is a simple but effective insight. It turns a problem that normally requires expensive Jacobian computations into one needing only forward passes through the transport map, and the Gaussian source distribution is exactly the setting ESS was designed for.

- **Gradient-free operation is genuinely well-motivated.** The space-group symmetry experiment (Section 5.1) is a clean demonstration of a setting where ESS-Flow works and gradient-based methods cannot be applied at all (binary indicator potential from a non-differentiable external program). This is not a toy problem — it reflects real constraints in scientific domains with simulation-based or quantized observation models.

- **Strong materials results across multiple metrics.** In Table 2, ESS-Flow achieves dramatically lower mean absolute errors than all baselines (e.g., bulk modulus MAE 8.99 vs. 39.14 for the next-best DAPS). Table 3 shows ESS-Flow achieves the best combined S.U.N.T. rates on all five tasks, including the space-group task where no gradient-based baseline can operate.

- **Honest treatment of limitations.** The paper explicitly discusses when ESS-Flow is expected to underperform (e.g., noiseless image inpainting where the prior poorly covers the target), and the protein experiment is candid about the challenge remaining for all methods. The multi-fidelity failure on sharp targets is acknowledged rather than concealed.

## Weaknesses

### Fatal
None.

### Major

- **No MCMC diagnostics reported for the main experiments.** The paper presents ESS-Flow as an asymptotically exact MCMC sampler (Proposition 1 guarantees geometric convergence) but provides no empirical evidence of convergence or mixing quality for the main results in Tables 2–3. Standard MCMC practice requires at minimum: effective sample sizes (ESS), burn-in discussion, and assessment of convergence (e.g., trace plots or diagnostics). The only ESS numbers reported are for the multi-fidelity importance-weighting procedure (Section 5.1.1), not the primary ESS-Flow chain. Without this information, a skeptical reader cannot determine whether the 1,000 samples per task in Table 3 are representative posterior draws or highly correlated samples clustered near a mode. The low Uniqueness+Novelty rates for ESS-Flow in Table 3 (e.g., 46.1 vs. 80.8 for DAPS on bulk modulus) could reflect genuine posterior concentration or limited mixing — the paper's attribution to "successfully targeting extreme values" would be more convincing with ESS diagnostics. This is the most significant evidential gap in the paper.

### Minor

- **Computational cost is discussed only vaguely in the main text.** The paper relegates runtime details to the appendix, but the main text does not report basic quantities needed to assess practical viability: number of MCMC steps per task, acceptance rate of ESS proposals, or number of ODE solves per accepted sample. The conclusion's statement ("moderate numbers of function evaluations in the ODE solver, fewer than what is typically used for unconditional generation") is too vague to be informative. If ESS-Flow requires an order of magnitude more ODE solves per sample than DAPS, that is important context for the results in Table 2.

- **The protein experiment rests on a single test case.** Only one protein (PDB:7r5b, 147 residues) is evaluated. ESS-Flow underperforms on data fidelity ($d_y=37.02$ vs. 3.43 for ADP-3D and 11.79 for DAPS), and all methods produce structures far from ground truth (RMSD$_{\text{gt}} \geq 11.4$ Å for all methods). While the paper is honest about the challenge, a single-protein evaluation is thin evidence for general applicability to protein structure prediction.

- **The multi-fidelity extension (Contribution 3) is premature.** The importance-weighting approach achieves near-zero effective sample sizes on two of four tasks (band gap 0.1%, stability 1.0%), which the paper acknowledges. However, listing this as a numbered contribution overstates what is essentially a failed proof of concept on sharp targets. It would be more appropriately framed as future work or a speculative direction.

- **The ODE solver and discretization for the main experiments are unspecified.** The multi-fidelity section gives $\Delta=1/50$ and $\delta=1/1000$, but the main ESS-Flow results in Tables 2–3 do not state what ODE solver or discretization was used. This is a basic reproducibility detail.

- **D-Flow is essentially inert on the materials tasks.** Its performance is nearly identical to the unconditional baseline across all metrics (e.g., 205.88 vs. 209.39 MAE for bulk modulus), meaning it provides a weak comparison. The paper acknowledges this, but it limits the strength of the empirical case.

### Trivial

- The notation $T_\delta^\Delta$ in Eq. (4) is ambiguous: it is unclear whether the superscript or subscript denotes coarse vs. fine discretization without reading the surrounding text carefully.

## Nice-to-Haves

- Include a brief cost summary in the main text (e.g., "ESS-Flow requires approximately X ODE solves per sample, compared to Y for DAPS").
- Expand the protein experiment to at least one additional protein of different size or difficulty.
- Consider framing the multi-fidelity section as a discussion of future work rather than a numbered contribution, or include a more robust approach (e.g., delayed acceptance ESS, which is mentioned but not implemented).

## Removed Points

These points from the input review were filtered out under the hard rules:

- **"Methods not compared on equal footing for discrete atomic numbers"** — The paper explicitly discusses the different strategies used for different methods and the reasons (maintaining differentiability vs. handling discreteness). This is acknowledged, not overlooked.
- **"Statistical significance not tested"** — The differences in Table 2 are large enough that this is not a pressing concern; requesting formal tests here would not change the conclusions.
- **"Need comparison on tasks where gradient methods work well"** — The paper explicitly scopes itself to settings where gradients are unavailable or unreliable; this request is outside the paper's stated scope.
- **D-Flow being a weak baseline** — This is a finding of the paper (D-Flow fails on the materials domain), not a weakness of the paper.
- **Criticisms that depend on appendix content being absent** — The rules require assuming the appendix (which was stripped by the parser) exists in the original submission; criticisms about missing content that is referenced as being in the appendix are not counted.

## Novel Insights

The input review does not surface insights beyond the paper's own contributions. The observation that the low Uniqueness+Novelty rates could reflect poor mixing (rather than genuine posterior concentration) is a useful interpretive caution that the paper itself does not fully engage with, but it is a critical reading, not a novel technical insight.

## Suggestions

1. **Report MCMC diagnostics for the main experiments.** Add effective sample sizes, a brief burn-in analysis, and at least one convergence trace to the main paper or prominently reference them if in the appendix. This would directly address the most significant evidential gap and strengthen the claim that ESS-Flow produces representative posterior samples.
2. **Include a computational cost summary in the main text.** Report the number of MCMC steps, ESS acceptance rate, and approximate ODE solves per sample alongside the results in Tables 2–3 so readers can calibrate the trade-off between cost and accuracy.
3. **Specify the ODE discretization used for the main ESS-Flow results** (solver type, number of steps / discretization granularity) for reproducibility.
4. **Either strengthen the protein experiment with additional proteins or temper the claims about broad applicability** to protein structure prediction.

## Score and Decision

The core method is sound, well-motivated, and the materials results are impressive. The paper makes a genuine contribution to controlled generation for scientific domains where gradient-based methods fail. However, the absence of MCMC diagnostics for the main experiments is a real evidential gap for a paper whose central contribution is an MCMC sampler, and the computational cost is not adequately quantified in the main text. These are fixable issues, but as presented they prevent full confidence in the results.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>