Now I have sufficient calibration context. Let me finalize the review.

## Summary

ESS-Flow proposes a training-free method for controlled generation with flow-based generative models by applying elliptical slice sampling (ESS) directly in the Gaussian source space. The key insight is that the Jacobian determinant cancels out through a change of variables (Equation 3), enabling gradient-free MCMC that only requires forward passes through the transport map and potential. The method is demonstrated on material design with target properties and protein structure prediction from sparse distance measurements.

## Strengths

- **Clean mathematical insight (Equation 3).** The cancellation of the Jacobian determinant when expressing both prior and posterior in source space is correctly derived and forms the backbone of the method. This insight cleanly sidesteps the Jacobian computation problem that plagues both data-space and source-space gradient methods. This is the paper's central intellectual contribution and it is sound.

- **Strong empirical results on material generation (Tables 2, 3).** ESS-Flow dramatically outperforms all baselines on four material property tasks (bulk modulus: 8.99 vs DAPS 39.14; shear modulus: 10.53 vs DAPS 84.33; band gap: 1.85 vs PnP-Flow 5.63). These margins are large enough that they cannot be dismissed as noise.

- **The space-group symmetry task (Table 3) is a clean demonstration of unique value.** This is a genuinely non-differentiable problem where the potential is a binary indicator computed by an external program. Gradient-based methods cannot be applied here, and ESS-Flow's 81.9% target rate (vs 2.3% unconditional) is a compelling showcase of the method's unique applicability.

- **Honest framing of limitations.** The paper acknowledges early (line 43) and reiterates in the conclusion (line 271) that ESS-Flow struggles when the prior does not inform the target well (e.g., constrained submanifolds). This specificity about scope makes the claims that are made more credible.

- **Theoretical convergence guarantee (Proposition 1).** A geometric convergence rate is provided for the ESS Markov chain under regularity conditions, adapted from Natarovskii et al. (2021).

## Weaknesses

### Fatal

None.

### Major

- **Missing MCMC diagnostics for primary experiments.** ESS-Flow is an MCMC method, yet the main material generation experiments (1000 samples, Table 3) report no effective sample sizes, no autocorrelation times, no convergence diagnostics (trace plots, Gelman-Rubin R̂), and no burn-in discussion. The protein experiment uses only 10 samples per method, making mixing assessment impossible. For a method whose central selling point is asymptotically exact sampling, the reader cannot verify whether chains have converged or assess the effective independence of samples. The lower Uniqueness rates (e.g., Bulk: 46.1 vs DAPS 80.8; Shear: 30.5 vs DAPS 74.6) could be partially explained by chain autocorrelation, but without ESS estimates the interpretation is ambiguous. The multi-fidelity section (5.1.1) does report ESS for importance weights, and scaling analysis is in Appendix A.1, but neither covers the primary experiments. This is the single biggest evidential gap.

### Minor

- **Protein experiment framing overstates the "better trade-off" claim.** The paper claims ESS-Flow "achieves a better trade-off between data fidelity and sample realism" (line 267), but ESS-Flow has worse data fidelity (d_y=37.02 vs ADP-3D 3.43) and worse ground-truth accuracy (RMSD_gt=13.55 vs ADP-3D 11.45). While ADP-3D/DAPS clearly produce unrealistic structures (731 and 483 clashes, negative ELBO), ESS-Flow's RMSD_gt of 13.55 Å is also poor for structure prediction. The paper partially acknowledges this ("this problem remains challenging for all methods"), but the framing of "better trade-off" is a value judgment rather than a demonstrated fact. The real conclusion is that all methods struggle and ESS-Flow exhibits a different failure mode.

- **D-Flow comparison provides limited signal.** D-Flow's results in Table 2 (Bulk: 205.88, Shear: 165.93, Band gap: 9.24) are barely distinguishable from the unconditional baseline (209.39, 168.41, 9.28), indicating D-Flow fails to explore under the continuous atomic-number approximation. The paper explains this, but the comparison mainly shows that a specific approximation hurts D-Flow rather than revealing the relative merits of the methods. The space-group task comparison is cleaner and more informative.

- **Proposition 1 conditions do not hold for a core demonstration task.** The geometric convergence guarantee requires the pullback potential to be "bounded away from 0 and ∞ on compact sets." For the space-group task, the binary indicator potential g(c)=𝟙[P_c=y] is zero almost everywhere, violating this condition. The method works empirically, but the scope of the theory should be stated more precisely.

- **Claim about manifold extension is unvalidated.** The paper states ESS-Flow "extends naturally to flows on manifolds" (line 34) but provides no experimental demonstration on any manifold-structured data.

- **No experimental comparison to the most similar methods.** The paper cites concurrent work by Wang et al. (2025) on source-space HMC and Purohit et al. (2025) on source-space Langevin Monte Carlo but does not compare to them. A comparison would directly isolate the value of gradient-free vs. gradient-based MCMC in source space.

### Trivial

- **"Asymptotically exact" should be clarified at point of use.** The claim (line 39) refers to exactness w.r.t. the learned model p_θ(x), not the true data distribution. This is standard but should be stated where the phrase appears.

## Nice-to-Haves

- A wall-clock time or number-of-function-evaluations (NFE) comparison in the main text would help practitioners assess computational trade-offs.
- A more extensive study of non-differentiable potentials beyond the single space-group task would strengthen the paper's core claim.
- The multi-fidelity contribution (Section 4.2) is honestly described as a proof-of-concept with very low ESS for two of four tasks (band gap 0.1%, stability 1.0%); more principled approaches (e.g., delayed acceptance) would strengthen this direction.

## Removed Points

These points from the input review were removed after cross-checking against the paper:

1. **Multi-fidelity limitations as a weakness.** The reviewer notes low ESS for band gap (0.1%) and stability (1.0%). However, the paper itself presents this as a "proof of concept" (line 137) and "preliminary evaluation" (line 191), and explicitly acknowledges the shortcomings. The paper is already appropriately measured about this contribution.

2. **Computational cost of ODE evaluation.** The reviewer notes that each evaluation of T_θ(z) requires solving an ODE. The paper acknowledges this is inherent to all source-space methods, and computational costs are reported in the appendix. Since the appendix is stripped by the parser, this cannot be verified but the paper notes its existence.

3. **Introduction claim about manifolds.** The reviewer suggests softening the claim (line 34) about extending to manifolds. The paper already qualifies this with "as long as the source distribution is Gaussian." This is a reasonable qualifier for a theoretical extension.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add MCMC diagnostics for primary experiments.** Report effective sample sizes, autocorrelation times, and convergence diagnostics (e.g., R̂ across multiple chains) for the 1000-sample material generation experiments. This directly addresses the most significant evidential gap.

2. **Reframe the protein results.** Characterize the observed trade-off more neutrally, acknowledging that all methods produce poor RMSD_gt values and that ESS-Flow offers a _different_ failure mode rather than claiming superiority.

3. **Clarify Proposition 1's scope.** Note explicitly that the geometric convergence guarantee requires the pullback potential to be bounded away from zero, and that this does not hold for binary indicator potentials used in the space-group task (though the method still works empirically).

4. **Add experimental comparison to source-space gradient MCMC** (Wang et al., 2025; Purohit et al., 2025) to directly isolate the value of gradient-free sampling.

5. **Include a computational cost summary** (wall-clock time or NFE) in the main text rather than deferring entirely to the appendix.

---

### Calibration Report

**Round 1 bracket:** 5.5–7.5 (papers in this range are accepted, make a genuine contribution, and have reasonable experimental validation, but may have some addressable gaps).

**Anchors retrieved (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| OC-Flow (61ss5RA1MM) | 6.50 | 1 | Training-free guided flow matching; stronger theory but similar scope. ESS-Flow has a cleaner gradient-free insight but weaker experimental validation. Comparable. |
| TFG-Flow (GK5ni7tIHp) | 6.25 | 1 | Training-free guidance for multimodal molecular flow; similar application domain. ESS-Flow has stronger material results but missing diagnostics. Comparable. |
| Discrete Space Guidance (XsgHl54yO7) | 6.50 | 2 | Guidance for discrete state-space models; more general method. ESS-Flow's contribution is more focused but well-executed. Comparable. |
| Universal Guidance (pzpWBbnwiJ) | 5.25 | 1 | Diffusion guidance for arbitrary modalities; less theoretical depth. ESS-Flow is stronger in theory and material experiments. ESS-Flow is stronger. |
| Conditional Prior (8ZJAdSVHS1) | 4.25 | 1 | Conditional flow matching with designed priors; novelty questioned. ESS-Flow has clearer novelty. ESS-Flow is stronger. |
| Controlled Denoising (MBDH5zyxHM) | 4.60 | 1 | Gradient-free guidance for diffusion; less ambitious evaluation. ESS-Flow has cleaner theory and stronger material results. ESS-Flow is stronger. |

**Narrowing:** The closest topical matches — OC-Flow (6.50) and TFG-Flow (6.25) — are accepted papers with similar scope. ESS-Flow's core idea is at least as novel as these, and its material results are stronger. However, its missing MCMC diagnostics and weaker protein experiment prevent it from reaching their level. The Sequential Controlled Langevin Diffusions paper (6.50) provides another MCMC-oriented anchor. Considering all evidence, ESS-Flow sits slightly below these anchors.

**Final score:** 6.0 — a solid paper with a genuine contribution and compelling results on its core application, held back from a higher score by the missing MCMC diagnostics (which weaken the interpretability of the primary experimental claims) and the uninformative protein experiment.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>