## Summary

ESS-Flow proposes a gradient-free method for controlled generation with pretrained flow-based generative models. The key insight is to perform Bayesian inference in the source (latent) space of flow models using Elliptical Slice Sampling (ESS), which leverages the typically Gaussian source distribution. The Jacobian of the transport map cancels out via change of variables, so only forward passes through the generative model and potential function are needed — no gradients through either. The method is demonstrated on materials property targeting (where it substantially outperforms baselines) and protein structure prediction from sparse distance measurements.

## Strengths

1.  **Genuinely gradient-free on a non-differentiable task**: The space-group symmetry task (Table 3) uses a binary indicator computed via the non-differentiable external program `spglib`. ESS-Flow achieves 81.9% target rate and 25.5% S.U.N.T. rate. Gradient-based methods (D-Flow, PnP-Flow) cannot run on this task at all because the potential is non-differentiable — this directly validates the paper's central claim.

2.  **Large quantitative improvements on materials property targeting**: Table 2 shows ESS-Flow achieves MAEs of 8.99 (bulk modulus), 10.53 (shear modulus), and 1.85 (band gap), versus the next-best method (DAPS) at 39.14, 84.33, and 3.90 — improvements of roughly 4–8×. Figure 3 confirms the samples concentrate near the target values while baselines remain diffuse. These are not marginal gains.

3.  **Geometric convergence guarantee**: Proposition 1 (citing Natarovskii et al., 2021) states the ESS-Flow Markov chain converges geometrically fast in total variation distance. This is a stronger theoretical guarantee than any of the optimization-based alternatives (D-Flow, PnP-Flow) or even the sampling-based DAPS offer.

4.  **Gradient-based methods demonstrably fail on disconnected manifolds**: Figure 2 provides a toy illustration where D-Flow samples remain trapped in a disconnected manifold component while ESS-Flow samples are well-distributed across the target. This clearly motivates why a gradient-free MCMC approach can overcome topological obstacles that gradient flows cannot escape.

5.  **Transparent discussion of limitations**: The paper explicitly discusses when ESS-Flow struggles (potentials constraining to lower-dimensional manifolds, line 99; sharp target distributions causing importance-weight collapse in multi-fidelity, lines 203–204) and acknowledges the protein prediction task "remains challenging for all methods we consider" (line 256).

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1.  **Abstract oversells the protein results**: The contributions list claims "improved structural realism in proteins" (line 41). Table 4 shows ESS-Flow indeed produces better ELBO (8.89 vs. −5.68 for ADP-3D) and far fewer atomic clashes (24.8 vs. 731.3), but at the cost of substantially worse data fidelity (d_y = 37.02 vs. 3.43) and RMSD to ground truth (13.55 vs. 11.45). The paper honestly discusses this trade-off in the text (lines 254–257), but the unqualified phrase "improved structural realism" bundles two different claims — prior faithfulness and prediction accuracy — as if both were unambiguously better. Softening this framing would better match the evidence.

2.  **No MCMC convergence diagnostics in the main text**: For an MCMC-based method, readers need trace plots, effective sample sizes, R-hat statistics, or autocorrelation analysis to assess whether the reported samples are at stationarity. The paper mentions numerical scaling evaluations in the appendix (line 101) but provides no convergence diagnostics for the actual experimental runs. This is especially relevant given that only 10 protein structures are generated per method (line 244), which is a small number for MCMC inference — the large standard deviations in Table 4 are consistent with undersampling.

3.  **Computational cost mentioned only in the appendix**: Line 183 states "Hyperparameter details and the runtime costs of the methods are provided in the Appendix." For an MCMC method, the number of function evaluations, acceptance rates, and wall-clock time are important context for practical adoption. The conclusion mentions "moderate numbers of function evaluations" (line 271) but gives no specific numbers. Even a brief summary in the main text (e.g., "ESS-Flow required roughly X NFEs per sample, compared to Y for DAPS") would significantly aid the reader.

4.  **Multi-fidelity proof of concept has limited demonstrated utility**: The importance-weighting approach achieves good effective sample sizes for bulk modulus (65.3%) and shear modulus (33.9%) but collapses to 0.1% and 1.0% for band gap and stability tasks (lines 193–203). The paper honestly reports this, but the method as presented is only usable for about half the tested settings with no diagnostic for when it will or won't work. As a "proof of concept" this is fine, but its placement as a numbered contribution (line 40) is somewhat overstated relative to the empirical results.

### Trivial

None.

## Nice-to-Haves

- An ablation study showing how the number of ESS iterations (MCMC chain length) affects sample quality on the materials tasks would help practitioners understand the cost-quality trade-off.
- A discussion of the assumptions in Proposition 1 (boundedness conditions on \(g \circ T_\theta\)) and whether they are verifiable for the specific potentials used in the experiments would strengthen the theoretical framing.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Harsh critic claim that D-Flow is "arguably a stronger prior-preserving baseline" than ESS-Flow on the protein task**: Factually incorrect. Table 4 shows ESS-Flow outperforms D-Flow on d_y (37.02 vs. 46.54), RMSD_gt (13.55 vs. 14.44), min RMSD_gt (10.63 vs. 11.54), and ELBO (8.89 vs. 8.64). D-Flow only has a slight advantage in clash count (14.8 vs. 24.8). The critic's claim that D-Flow has "better" d_y and RMSD_gt misreads the direction of these metrics (lower is better).

- **Harsh critic claim that "only gradient-free method in this category" (line 65) is misleading**: The paper explicitly qualifies this as "in this category" (source-space methods), which is accurate. Data-space methods like DAPS and PnP-Flow are in a different category and the paper's taxonomy in Section 3 is clear about this distinction.

- **Harsh critic claim that Proposition 1 is a known result and should be more clearly cited**: The paper already cites Natarovskii et al. (2021) and states "For completeness we state one of the main results here" (lines 101–103). This is transparent and appropriate.

- **Strength Finder claim about "structural realism in protein prediction" as a strength**: The protein results are mixed (good ELBO/clashes but poor d_y/RMSD), making this a nuanced finding rather than an unqualified strength. It has been integrated into the minor weaknesses as an overclaim issue.

- **Generic strengths about problem importance**: Removed as they lack specific evidence anchoring.

## Novel Insights

None beyond the paper's own contributions. The core insight — canceling the Jacobian via change-of-variables and applying ESS in the Gaussian source space of flow-based models — is the paper's own novel contribution and is well articulated.

## Suggestions

1.  **Reframe the protein claim**: In the abstract and contributions list, replace "improved structural realism in proteins" with language that acknowledges the trade-off, e.g., "producing more physically realistic protein structures (fewer clashes, better ELBO) while exhibiting higher data-fidelity error than likelihood-focused methods."
2.  **Add a computational cost summary to the main text**: Report the number of MCMC iterations, acceptance rate, NFE per sample, and wall-clock time for the materials experiments. A single sentence or small table would suffice.
3.  **Include MCMC diagnostics**: Add effective sample sizes, trace plots, or R-hat statistics for the main experimental runs (either in the main text or with a clear pointer to the appendix, if space is tight).
4.  **Increase protein sample sizes**: 10 structures per method is very small for MCMC-based inference. Increasing to 50–100 would provide more reliable statistics.
5.  **Provide a diagnostic for when multi-fidelity importance weighting will work**: The paper identifies that "sharper target distributions" cause collapse but does not operationalize this into a usable diagnostic.

## Score and Decision

**Bracket determination (Round 1)**: Based on comparison with calibration anchors, ESS-Flow sits above the accepted 6.0–6.2 papers (which had weaker experiments or less clean methods) but below the 8.0-level papers (which had flawless, thorough evaluations with extensive ablations and no overclaiming issues). The plausible range is **6.5–7.5**.

**Calibration anchors considered**:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Jyh0DR4fFE.md` (Injective flows for star-like manifolds) | 6.0 | R1 | Accepted. Solid theory but limited experimental scope. ESS-Flow has stronger empirical results. |
| `bNVbOS3lrl.md` (Bridging VI and SG-MCMC) | 6.2 | R1 | Accepted. Method more complex, practical impact questioned. ESS-Flow is cleaner and more directly applicable. |
| `0QJPszYxpo.md` (Extended Flow Matching) | 5.0 | R1 | Rejected. Limited experiments (32 dims max), theoretical concerns. ESS-Flow is clearly stronger. |
| `AC1QLOJK7l.md` (Training-free guidance for inpainting) | 4.0 | R1 | Rejected. Fundamental theoretical issues (biased sampling). ESS-Flow's theory is sound. |
| `zMoNrajk2X.md` (CADS) | 8.0 | R1 | Accepted. Flawless evaluation with ImageNet SOTA and extensive ablations. ESS-Flow's protein experiment and missing diagnostics prevent reaching this level. |
| `xoXn62FzD0.md` (SMC for LLM control) | 8.0 | R1 | Accepted. Strong results across four domains, clear advantages demonstrated. ESS-Flow is comparable in method quality but less thoroughly evaluated. |

**Final score**: 7.0. The method is sound and clean, the materials results are strong, and the paper is well-written. The main shortcomings — an overclaimed protein result, absent MCMC diagnostics and computational cost in the main text, and a partial multi-fidelity proof-of-concept — are addressable and do not undermine the core contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>