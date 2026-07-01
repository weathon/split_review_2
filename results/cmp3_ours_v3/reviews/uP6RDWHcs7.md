Now I have sufficient calibration context. Let me produce the final review.

**Round 1 bracket:** Based on the calibration anchors, this paper sits most naturally between 5.5 and 7.5. Papers at 3.0-3.5 (e.g., "Flow Matching for One-Step Sampling") had theoretical flaws or unclear contributions. Papers at 6.0-6.5 (e.g., "Injective flows for star-like manifolds" at 6.0, "Lifting Architectural Constraints of Injective Flows" at 6.5) had clean ideas with some experimental limitations but were accepted. Marginal Flow has a cleaner core idea than the injective flow papers but thinner quantitative validation and a missing baseline.

**Final score: 6.0** — borderline accept. The idea is genuinely novel and well-motivated, the flexibility demonstrations are compelling, and the computational advantages are clear. However, the missing GMM baseline and undisclosed N_c are meaningful gaps that should be addressed.

Here is my final review:

## Summary

This paper proposes Marginal Flow, a density estimation framework that defines the model through a parametric distribution q(x|w) with latent parameters w. Instead of optimizing w directly (as in GMMs), the method samples w from a learnable distribution q_θ(w) — implemented by feeding noise through an unconstrained neural network — and computes the density as a mixture of the resulting components. This avoids Jacobian determinants (NF), ODE solvers (flow matching), and multi-step sampling (diffusion), while supporting exact computation of the defined mixture density, lower-dimensional manifolds, and flexible training objectives.

## Strengths

- **Simple and elegant core idea (Section 2.1).** The insight of marginalizing over learnable parameters rather than optimizing them directly is clean and well-motivated. The method sidesteps the Jacobian-determinant bottleneck of normalizing flows and the ODE-solving cost of flow matching / diffusion models.
- **Demonstrated flexibility (Sections 2.3, 4.3).** The Wishart mixture experiment (Section 4.3) is compelling: switching the parametric family q(x|w) from Gaussian to Wishart for positive-definite matrix data is straightforward and works well. The ability to simultaneously learn a lower-dimensional manifold and the density (Figures 4, 9) is a genuine advantage over NF and flow matching, which cannot change dimensionality.
- **Clear computational advantage (Section 2.2, Figure 3).** The method genuinely avoids expensive operations — no Jacobian determinants, no ODE solvers, no multi-step sampling. A small MLP feeding into Gaussian evaluations is undeniably cheaper per iteration. The runtime comparison in Figure 3 is clean and shows orders-of-magnitude speedups.

## Weaknesses

### Fatal
None.

### Major
- **Missing GMM baseline (Section 4.1, 4.2, vs. Section 2.1).** The paper motivates Marginal Flow by explicitly contrasting it with a fixed-component GMM (Figure 1, line 64: "Without marginalization, the model reduces to a simple mixture model... The expressiveness and scalability of the model are then fundamentally limited by the number of mixtures N_c"). Yet no experiment includes a GMM baseline. The comparisons are exclusively against more complex models (NF, FM, FFF). The core claim — that marginalization over learnable parameters improves over directly optimizing mixture parameters — is never directly tested against a GMM with the same N_c trained via EM. Without this baseline, the main argument for marginalization lacks direct empirical support.
- **Undisclosed N_c (Sections 2.1, 4).** The hyperparameter N_c (number of sampled components) governs the trade-off between density quality and computational cost. Its value is never reported for any experiment in the main text (the only mention is an illustrative "e.g. 10" in Section 2.1). Since the runtime advantage (Figure 3) and density fidelity both depend on N_c, the reader cannot assess whether the reported speedups persist at N_c values that yield density quality competitive with NF/FM/FFF.

### Minor
- **"Exact density evaluation" needs qualification (Sections 2.1, Abstract, Table 1).** The paper claims "exact density evaluation" throughout. For the model as defined in Eq. 2 — q_θ(x) = (1/N_c) Σ q(x|w_i) — computing the mixture density given a fixed set of w_i IS exact. However, the w_i are resampled for each evaluation, so q_θ(x) is a random variable whose value changes between evaluations at the same x. This differs from normalizing flows, where the density is a deterministic function of the learned parameters. The paper should clarify this distinction rather than placing itself in the same cell as NF in Table 1 without comment.
- **Quantitative evidence is thinner than the claims warrant (Section 4).** Test log-likelihoods are shown as curves (Figure 7) without final numerical values in the main text. The SBI results are cited only to the appendix ("results in the Appendix in Figure 14") with no numerical values in the main body. Image manifold experiments (Section 4.4) are entirely qualitative. For a paper claiming to "overcome limitations altogether" and achieve "state-of-the-art results," the quantitative evidence in the main text is sparse.
- **"Converges orders of magnitude quicker" conflates speed and efficiency (Section 4.1, Figure 7).** Figure 7 uses runtime (seconds) on the x-axis, so the claim reflects per-second progress, which conflates the method's per-iteration speed with its statistical efficiency. A method that is fast per-iteration but requires more iterations to converge may still converge faster in wall time; this should be explicitly disentangled.
- **No discussion of limitations or failure modes (Section 5).** The paper does not acknowledge that the density estimate's variance depends on N_c, that the density is stochastic rather than deterministic, or how these issues might affect high-dimensional scaling.

### Trivial
- **Mixture-model language inconsistency (Figure 5 caption, line 216).** The paper says "Note that Marginal Flow is not a mixture model" but then defines it in Eq. 2 as (1/N_c) Σ q(x|w_i) — which is formally a mixture model, just with resampled (rather than fixed) components.

## Nice-to-Haves
- An analysis of how the variance of the density estimate scales with N_c and dimensionality, with empirical validation.
- A comparison against a standard KDE with learned bandwidth, to further contextualize the method.
- Numerical log-likelihood values on standard density estimation benchmarks (e.g., UCI tabular datasets).

## Removed Points
*These points from the harsh critic input were removed, but retained here for reference:*

1. **"Exact density evaluation is a structural issue that invalidates core claims"** — Removed because this overstates the problem. The model is defined in Eq. 2; evaluating Eq. 2 IS exact for a given draw of w_i. The stochasticity from resampling is by design and the paper acknowledges it ("resampling induces an approximation to the marginal distribution in Eq. 1"). This is a presentation clarification, not a fatal flaw. Moved to Minor.

2. **"SBI results relegated to appendix is a major weakness"** — Removed as a major weakness because the parser strips appendices from all papers; they exist in the original submission. The criticism that no numerical values appear in the main text is kept as a Minor weakness.

3. **"Comparison with Free-form Flows in Figure 4 may be unfair"** — Removed because it is speculative and depends on claims about FFF's design not established in the paper under review.

4. **"Insufficient discussion of relationship to mixture models and KDE"** — Removed because the paper does discuss this relationship (Section 2.1, Figure 1). The discussion could be expanded but is not absent.

5. **"Disentanglement claims overstated"** — Removed because the paper makes a modest claim ("We observe disentanglement") rather than a strong one. The conditioning variable is provided, so the separation by label is expected.

6. **"No limitations section"** — Removed as a standalone point; folded into the Minor point about acknowledging limitations.

7. **"Universality claim stated without proof"** — Removed because the paper cites Micchelli et al. (2006) for the claim, which is standard practice for citing known results. A proof sketch would be nice but is not required.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a GMM baseline (same N_c, EM-trained) to the synthetic experiments to directly validate the core claim about marginalization vs. parameter optimization.
2. Report N_c for every experiment, and include an ablation study showing how density quality and variance change with N_c.
3. Clarify the "exact density" terminology: state explicitly that the density given the sampled parameters is exact but the overall density estimate is stochastic because parameters are resampled.
4. Include final numerical log-likelihood values in the main text (or a table) alongside the curves in Figure 7.
5. Add a brief limitations paragraph acknowledging the Monte Carlo variance of the density estimate and the dependence on N_c.

## Score and Decision

**Calibration anchors consulted (all rounds):**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `kBNIx4Biq4.md` (Lifting Architectural Constraints of Injective Flows) | 6.50 | 1 | Similar topic (flow-based density estimation on manifolds), stronger quantitative validation. |
| `Jyh0DR4fFE.md` (Injective flows for star-like manifolds) | 6.00 | 1 | Similar topic (density estimation on manifolds), comparable quality and scope of experiments. |
| `spDUv05cEq.md` (Flow-based Variational Mutual Information) | 6.00 | 1 | Similar methodology (flows for density estimation), comparable weaknesses (limited real-world validation). |
| `6Z8rZlKpNT.md` (NF for OOD detection) | 3.40 | 1 | Lower quality — methodological concerns about normalizing flows for OOD. |
| `46tjvA75h6.md` (No MCMC Teaching for EBMs) | 3.00 | 1 | Lower quality — unclear novelty in energy-based model training. |
| `mbo4YnWCHd.md` (Non-negative Tensor Mixture Learning) | 4.25 | 1 | Different topic (discrete density estimation with tensor mixtures). |

**Round 1 bracket:** 5.5 – 7.5. The paper has a genuinely novel core idea and clear computational advantages, placing it clearly above the 3–4 range. However, the missing GMM baseline and undisclosed N_c prevent it from reaching the 7.5+ tier. Within this bracket, the paper is most comparable to the 6.0–6.5 injective flow papers.

**Final score: 6.0.** The core idea is novel, simple, and practically motivated. The flexibility demonstrations (Wishart, manifold learning, SBI) are convincing. However, the missing GMM baseline (which the paper itself motivates as the key comparison) and the lack of N_c disclosure are meaningful gaps that keep this at the borderline-accept level rather than stronger acceptance.

**Decision: Accept**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>