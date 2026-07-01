## Summary

This paper presents a hybrid neural-MPM framework for fluid simulation that combines a GNN-based neural physics model (trained at low spatiotemporal resolution) with a fallback mechanism to the Material Point Method (MPM) when the learned model's predictions become unreliable. It also introduces a diffusion-based generative controller trained via a reverse simulation strategy to enable sketch-based fluid control. The system is evaluated across seven 2D/3D scenarios covering water, sand, and multi-material interactions.

## Strengths

1. **The reverse simulation strategy for control data generation (Section 3.2.2, Equation 3) is technically interesting and original.** Solving for the external force field required to reverse a forward trajectory provides a principled, automated way to generate paired data (sketch, force field) for training the diffusion controller, without requiring expensive real-world data or manual annotation. This is the paper's most distinctive idea.

2. **Broad scenario coverage and consistent empirical pattern.** The dataset (Table 2) spans 7 domains across 2D/3D, water and sand, with and without rigid obstacles (ramps), each with 1k trajectories. Across all scenarios, the hybrid solver consistently occupies an intermediate position on the error-latency Pareto front between pure neural physics and pure MPM (Figure 10), which supports the paper's central claim about improving the trade-off.

3. **The fallback design is computationally lightweight.** Using a cosine similarity of acceleration histories as a complexity metric (Section 3.1.2) is simple to compute at each step, unlike velocity divergence which would require expensive finite-difference operations. This design choice is well-motivated by the real-time constraint.

## Weaknesses

### Fatal

None.

### Major

1. **The "real-time" framing is overstated relative to the evidence.** The paper's central pitch is "achieving real-time simulations at high frame rates" (abstract). However, the numbers tell a more nuanced story:
   - For the Water-Sand 2D case, MPM runs at 0.114s per frame (~8.8 fps) and the hybrid method at 0.08s per frame (~12.5 fps). Neither reaches standard real-time thresholds (30–60 fps). The claim that this constitutes "high frame rates" is misleading.
   - For the 3D cases (e.g., Sand 3D: 1.02ms per step with dt=2.5ms), MPM is already running faster than real-time. The 11.8% reduction to 0.90ms is an incremental improvement to an already real-time solver, not an enabler of real-time performance where it was previously impossible.
   
   The paper should be upfront about these absolute numbers and frame the contribution as improving the error-latency trade-off (which it does) rather than as "enabling real-time."

2. **The fluid control evaluation is fundamentally insufficient to support the claimed contribution.** The paper's second major contribution — a diffusion-based generative controller — is validated against a single baseline: a spatiotemporal constant force field (Section 4.3, line 273). The issues are:
   - **No comparison to prior fluid control methods.** The paper cites Chu et al. (2021), Yan et al. (2020), and Schoentgen et al. (2020) as related work on learned fluid control but provides no quantitative comparison against any of them. A contribution claiming to advance fluid control must benchmark against the state of the art, not against a constant-force heuristic.
   - **Only the final time step is evaluated** (line 282). The paper's own framing is about whether the fluid "follows the user's sketch" — this is inherently about the trajectory, not just the endpoint. Per-frame trajectory error is needed.
   - **No user study.** The paper claims "user-friendly freehand sketches" (abstract) and "interactive fluid control" (title, Section 3.2), yet there is no human evaluation of usability, responsiveness, or intuitiveness. These claims remain unsupported.
   - **Weak absolute performance.** The RMSE values for the 2D cases (0.0802 for Water 2D, 0.0924 for Sand 2D) indicate substantial residual deviation from ground truth, and the relative improvement over the constant-force baseline is modest (11.7–19.7%).

### Minor

3. **No statistical confidence or variance reported for any result.** All tables (Table 1, Table 3) and figures (Figure 6, Figure 10) report single-point measurements with no error bars, standard deviations, or variance estimates. This includes inherently noisy measurements such as GPU latency. While this is common practice in parts of the simulation literature, it prevents the reader from assessing whether reported differences (e.g., RMSE 0.0169 vs. 0.0144 at different thresholds in Table 1) are meaningful or within noise.

4. **The fallback threshold is tuned on a single scenario and applied without cross-validation.** The threshold \( r_c = 0.8 \) is selected based on the Water 2D ablation study (Section 3.1.2, Figure 6d) and used across all six other scenarios involving different materials (sand), dimensions (3D), and obstacle configurations. Different materials have different acceleration profiles, and the optimal threshold likely varies. The paper does not report how often the fallback triggers per scenario, so it is unclear whether the hybrid system is primarily running neural physics with occasional MPM correction, or mostly falling back to MPM.

5. **The reverse simulation derivation (Equation 3) needs clarification.** The derivation solves for the acceleration required to reverse a trajectory by treating the particle as moving under the control force and gravity. However, MPM simulations include inter-particle forces (pressure, viscosity, collisions). The paper does not clearly explain whether the computed \( \mathbf{a}_t \) represents a pure external control force or the residual net acceleration after all forces. While the approach still generates useful training data in practice, this ambiguity should be resolved.

### Trivial

None.

## Nice-to-Haves

- Report per-frame trajectory error (not just final-frame RMSE) for the control evaluation, which is directly motivated by the paper's own framing of sketch-following.
- Include at least one prior learned fluid control method as a quantitative baseline to establish where the proposed approach stands relative to existing work.
- Add the missing factor of 2 in Equation 3 if the standard constant-acceleration kinematic equation is intended, or clarify the discretization scheme used.

## Removed Points (weaknesses filtered per guidelines)

1. **"MPN" typos in Section 3.1.2 (lines 127, 129, 131, 140, 142).** Removed per formatting/typo rule — these appear to be LaTeX→PDF parser artifacts where "MPM" was rendered as "MPN" in the extracted text; the original submission almost certainly uses "MPM" consistently.

2. **Equation 2 subscript error ("t-t-δt").** Removed per formatting artifact rule — this is a garbled LaTeX expression from PDF extraction, not a meaningful author error.

3. **Missing experimental comparison against Neural SPH/MPMNet.** Removed because the paper states "Additionally, we compare with other previous methods in Appendix E" (line 254). The appendix is stripped by the parser; we cannot verify what comparisons it contains.

4. **Novelty/modest significance criticism ("straightforward application of GNS," "simple rule-based hybrid").** Removed as a general opinion that does not identify a specific technical flaw in the paper. The paper's contribution is a working integration of components, and the question of whether this integration is "simple enough to be insufficient" is a judgment call rather than a verifiable weakness.

5. **Train-test loss mismatch (particle-level RMSE for training vs. grid-level RMSE for evaluation).** Removed because the paper explicitly acknowledges this trade-off and justifies it (lines 97–98): training uses the cheaper particle-level loss to avoid expensive p2g operations at each step. This is a reasonable engineering choice.

6. **Figure 10 caption "outperforming both."** Removed as a minor stylistic overstatement that does not materially affect the paper's validity. The data show the hybrid sits between neural and MPM on the error-latency Pareto front, which the caption elsewhere accurately describes as "balanced trade-off."

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the contribution honestly.** Drop the "real-time at high frame rates" phrasing for cases where the solver runs at 12.5 fps. Replace with precise language about improving the error-latency trade-off and report absolute frame rates alongside relative improvements. This would strengthen rather than weaken the paper by eliminating a vulnerability to scrutiny.

2. **Strengthen the control evaluation with one or more of:** (a) quantitative comparison against at least one prior learned control method, (b) per-frame trajectory RMSE, (c) a small user study (5–10 participants) with a simple task like "direct the fluid through a sketched path" to substantiate the interactivity claim, or (d) at minimum, report the baseline RMSE of an "uncontrolled" simulation (no force field) to contextualize the improvement.

3. **Report how often the fallback triggers** for each scenario (fraction of steps using MPM vs. neural physics) to allow readers to interpret what the hybrid system is actually doing.

4. **Add error bars** (at least from 3+ random seeds) for latency and RMSE measurements to establish that reported differences are meaningful.

5. **Clarify Equation 3** by explicitly stating what forces are included in the computed \(\mathbf{a}_t\) (pure external control vs. residual net acceleration) and whether the factor of \(1/2\) from the standard kinematic equation is accounted for.

## Score and Decision

The paper addresses a well-motivated problem and contains one genuinely interesting idea (reverse simulation for control data generation). However, the evaluation has significant gaps: the headline "real-time" claim does not hold up against the absolute numbers, and the control component — presented as a core contribution — is validated against only a trivial baseline with no comparison to prior work, no user study, and only final-frame metrics. The simulation acceleration results are solid but incremental. These issues are correctable, but as presented the paper does not meet the bar for acceptance at a top venue.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>