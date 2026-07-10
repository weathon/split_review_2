## Summary

ESS-Flow reformulates controlled generation with flow-based models as Bayesian inference in the source space, using Elliptical Slice Sampling (ESS) to exploit the Gaussian prior. The key insight — Jacobian cancellation in Equation (3) — eliminates the main computational bottleneck of source-space methods and enables gradient-free posterior sampling. The method is demonstrated on material generation (FlowMM) and protein structure prediction (Chroma), with a particularly clean proof-of-concept on a non-differentiable space-group targeting task.

## Strengths

- **The core idea is principled and elegantly leverages the Gaussian source prior.** The Jacobian cancellation in Equation (3) is correct and turns the otherwise expensive source-space Bayesian inference problem into a setting perfectly suited for ESS. This insight is non-obvious, cleanly derived, and directly addresses a real limitation of existing work — gradient dependence — that matters for scientific applications where simulators or quantization break differentiability. **[impact=+9.99]**

- **The space-group experiment is a genuine and clean demonstration of the gradient-free advantage.** Targeting a specific space group using a non-differentiable external program (Togo et al., 2024) is a task where gradient-based methods simply cannot operate. ESS-Flow achieves 81.9% target rate vs. 2.3% unconditional (Table 3) — a convincing proof of concept for the method's stated purpose. **[impact=+10.00]**

- **The method is honest about its limitations.** The paper explicitly states (line 43) that ESS-Flow "limits the applicability of the method in situations when the prior poorly informs the target distribution" and is unsuitable for targets constrained to a lower-dimensional manifold. This candor is stated upfront in the introduction, not buried in a limitations section. **[impact=+9.00]**

- **ESS-Flow achieves numerically strong absolute performance on material generation tasks.** In Table 2, ESS-Flow attains 8.99 MAE on bulk modulus and 10.53 on shear modulus — substantially better than unconditional sampling (209.39, 168.41) and the next-best method DAPS (39.14, 84.33). **[impact=+9.97]**

## Weaknesses

### Fatal
None.

### Major

- **The material generation comparison is asymmetric in a way that inflates ESS-Flow's margin.** D-Flow and PnP-Flow are forced to use a continuous approximation for atomic numbers (softmax with τ=0.1 in Equation 5) to maintain differentiability, while DAPS uses exact discrete atomic numbers via a Metropolis-Hastings correction and ESS-Flow handles them natively through its gradient-free mechanism. The paper acknowledges this (line 185: "Even with the continuous approximation for a, D-Flow fails to explore atomic compositions far from initialization"), yet the headline that "ESS-Flow outperforms all other methods significantly" (line 185) is stated as a general claim about controlled generation rather than being explicitly qualified by the asymmetric evaluation setup. A controlled comparison on a fully differentiable task where all methods operate on equal footing would substantiate the claim more convincingly. **[impact=-8.29]**

- **The protein structure results show a trade-off, not clear superiority.** In Table 4, ESS-Flow has worse RMSD to ground truth (13.55) than ADP-3D (11.45) and DAPS (11.41), and a much larger distance to observed data d_y (37.02) versus ADP-3D (3.43) and DAPS (11.79). Meanwhile, ADP-3D and DAPS produce severely unnatural structures (731 and 483 clashes respectively). The paper's claim of achieving "a better trade-off" (line 267) is subjective — the methods differ along two axes and ESS-Flow dominates neither. With only n=10 samples per method, the standard deviations are large enough that rankings on RMSD_gt may not be statistically significant. **[impact=-4.28]** [impact=-3.97 merged with -5.78]

### Minor

- **No ESS acceptance rates are reported for any experiment.** For an MCMC method, acceptance rate is the primary diagnostic of chain mixing. Without it, the reader cannot assess whether ESS is exploring effectively or getting stuck. This is particularly relevant because Proposition 1's geometric convergence guarantee requires the pullback potential to be bounded away from 0 and ∞ on compact sets, which may not hold for the sharp Gaussian likelihoods used (σ_y = 0.1 eV for band gap). **[impact=-8.26]**

- **The D-Flow baseline performs at near-unconditional levels across all four material properties** (bulk modulus: 205.88 vs. unconditional 209.39; shear modulus: 165.93 vs. 168.41; band gap: 9.24 vs. 9.28; energy above hull: 1.92 vs. 1.96). While the paper acknowledges this (line 185), D-Flow's inclusion makes the comparison more lopsided than informative. Either D-Flow is fundamentally unsuitable for this domain, or the adaptation was not adequately tuned. **[impact=-8.69]**

- **Low S.U.N.T. uniqueness rates suggest possible over-concentration.** ESS-Flow's U.N. rates for bulk modulus (46.1%) and shear modulus (30.5%) are substantially lower than DAPS (80.8%, 74.6%). The paper attributes this to targeting extreme values (line 189), but the possibility of the chain exploring only a narrow region of the prior's support — generating similar plausible materials repeatedly — deserves deeper investigation. **[impact=-0.00]**

### Trivial
None.

## Nice-to-Haves

- **Report ESS acceptance rates** for all experiments. This is a basic diagnostic for any MCMC-based method and directly relevant to assessing whether the chain is mixing well under the sharp likelihoods used.
- **Include wall-clock time or ODE evaluation count comparisons.** ESS-Flow evaluates the full ODE at each MCMC step; for complex flow models this could be orders of magnitude more expensive than single-pass methods. The paper states runtime costs are in the appendix (line 183), but this should be summarized in the main text.
- **The multi-fidelity approach (Section 4.2) has near-zero effective sample sizes for band gap (0.1%) and stability (1.0%).** The paper acknowledges this limitation, but the approach as presented is a negative result rather than a useful contribution. The delayed acceptance and parallel tempering variants hinted at as future work would be more promising directions.
- **Add a fully differentiable control experiment** (e.g., continuous property prediction or an image-domain task) where all methods operate on equal footing without discrete variables, to isolate ESS-Flow's gradient-free advantage from the confounding effect of the continuous approximation.
- **Make the toy experiment (Figure 2) quantitative** by reporting acceptance rates, RMS error to target, and the fraction of samples stuck in disconnected manifolds.

## Removed Points
These points were raised by the harsh critic but are removed with justification:
- **Proposition 1 convergence concerns for sharp potentials** — Removed as speculative. The paper correctly cites prior convergence results and references Appendix A.1 for scaling analysis; the critic's concern about finite-sample performance is a hypothesis without evidence from the paper.
- **Chroma conversion may degrade unconditional quality** — Removed as speculative. The critic hypothesizes degradation without any evidence; unconditional RMSD_gt of 16.98 is not obviously out of line.
- **Multi-fidelity should not be a contribution** — Downgraded to nice-to-have (see above). The paper is transparent about the limitation and presents it as a proof of concept.
- **Missing related works** — Removed per policy (the reviewer does not have external sources to confirm existence of missing citations).

## Novel Insights

The harsh critic makes one genuinely insightful observation that goes beyond what the paper itself provides: the paper's strongest experiments (space group, material generation with discrete atomic numbers) are precisely the settings where ESS-Flow's gradient-free nature is structurally advantageous, while the protein experiment — where results are mixed — is a setting where gradients *are* available. This suggests the paper would be significantly strengthened by restructuring its evaluation around non-differentiable tasks as the primary demonstrations and reframing the differentiable material tasks as secondary sanity checks with an explicit acknowledgment of the asymmetric setup.

## Suggestions

1. Restructure the experiments to foreground the non-differentiable tasks (space group as a main result, add another non-differentiable task if possible).
2. Add a fully differentiable control experiment to establish a fair baseline comparison.
3. Report ESS acceptance rates and wall-clock time for all experiments.
4. Qualify claims about material generation performance by explicitly noting the asymmetric evaluation setup.
5. Reframe the protein results more carefully — lean into the Bayesian framing (posterior uncertainty, diverse structures consistent with data) rather than claiming superiority.

## Score and Decision

### Calibration

**Round 1 bracket:** 4.5–6.5 (based on comparison to training-free guided flow matching papers)

**Anchors (all retrieved across calibration rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/.../61ss5RA1MM.md` (OC-Flow) | 6.50 | 1, 2 | Yes | Stronger theoretical framing but had fatal result-reproducibility issues; accepted. ESS-Flow has a cleaner core idea but weaker evaluation. |
| `/.../GK5ni7tIHp.md` (TFG-Flow) | 6.25 | 1, 2 | Yes | Similar problem setting (training-free guidance for molecular design); accepted. ESS-Flow's core contribution is more novel but evaluation is less thorough. |
| `/.../fs2Z2z3GRx.md` (FIG) | 6.00 | 2 | Yes | Linear inverse problems with flow matching; accepted. Stronger experiments on established benchmarks, less novel methodologically. |
| `/.../5AtHrq3B5R.md` (PnP-Flow) | 5.50 | 2 | Yes | Image restoration; accepted despite presentation weaknesses. ESS-Flow has a more novel core idea but messier evaluation. |
| `/.../DoDNJdDntB.md` (FM for Posterior Inference) | 4.20 | 1, 2 | Yes | Similar topic space (flow matching + posterior sampling for science); rejected. Weaker results. ESS-Flow is stronger. |
| `/.../F6SaYwJ3eV.md` (Posterior sampling via Langevin) | 3.60 | 1, 2 | Yes | Source-space MCMC for generative priors; rejected. Core idea not sufficiently novel. ESS-Flow's ESS + Jacobian cancellation is more novel. |
| `/.../XcAJ0qsMgh.md` (Annealing Flow) | 3.60 | 1 | Yes | Flow-based sampling; rejected. Limited novelty. Not directly comparable. |

**Narrowing:** ESS-Flow is stronger than the 3.6–4.2 papers (which were rejected for limited novelty or weak evaluation) and comparable to the 5.5–6.5 papers (which were accepted despite various weaknesses). The core contribution (+9.99 core-idea strength) is among the strongest seen across all anchors. However, the evaluation weaknesses (particularly the structurally asymmetric material comparison at -8.29 and the missing MCMC diagnostics at -8.26) are substantive enough to place this paper below the accepted training-free guidance papers (OC-Flow at 6.50, TFG-Flow at 6.25, FIG at 6.00), which had clearer or more standard evaluations. The paper is closest to PnP-Flow (5.50, accepted despite presentation issues) but with more substantive experimental concerns.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>