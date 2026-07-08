Now let me produce the final consolidated review.

## Summary

This paper presents a streaming algorithmic framework for designing neural stimulations to drive latent neural dynamics in desired directions. The method integrates streaming dimensionality reduction (including a novel streaming jPCA variant), dynamical modeling via Kalman filtering, nonparametric kernel regression for learning stimulus-response mappings, and constrained optimization to select high-dimensional stimulation patterns under realistic experimental constraints (non-negativity, sparsity, magnitude limits). The paper tests this pipeline on simulated data and two real neural datasets (calcium imaging from mouse visual cortex, electrophysiology from nonhuman primate sensorimotor cortex), with synthetic stimulation effects added to the real background activity.

## Strengths

- **The framework accounts for realistic experimental constraints.** The optimization in Eq. (8) incorporates non-negativity constraints (excitation-only opsins), a sparsity constraint (limited simultaneous targets), and box constraints on stimulation magnitudes. The temporal kernel in Eq. (7) handles non-stationarity by discounting old observations. These reflect genuine experimental constraints that prior work often abstracts away.

- **Tests across multiple data modalities.** The paper uses both calcium imaging (15 Hz, mouse) and electrophysiology (30 Hz, nonhuman primate) data, demonstrating some breadth, and runtime benchmarks (<10 ms average) are relevant for real-time applications.

- **Well-motivated, difficult problem.** The paper correctly identifies that the combinatorial explosion of possible stimulation targets (which neurons, at what magnitudes) makes exhaustive search infeasible, and that the state-dependence of stimulation effects adds complexity. Sections 1 and 2.3 articulate these challenges clearly.

## Weaknesses

### Major

- **The method is validated on synthetic stimulation effects only, not on real biological stimulus-response mappings.** The "real data" experiments (Section 4.1, line 178) add a synthetic AR(1) stimulation effect (a_t = 0.8·a_{t-1} + u_t) on top of real background activity. This means the method is tested on a known, simple generative process rather than on genuine biological responses to optogenetic or electrical stimulation. The abstract states "demonstrate our approach on both simulated and real neural data" without clarifying that stimulations on real data were also simulated — this could mislead readers. The Discussion (lines 255–260) acknowledges offline experiments but does not highlight the synthetic nature of the stimulation effects as a core limitation. The comparison against the "blind" model that ignores stimulation is a reasonable sanity check but does not validate the method on real biological responses.

- **No comparison against existing stimulation design methods despite citing them as prior work.** The paper cites Bayesian optimization (Minai et al., 2024), active learning (Wagenmaker et al., 2024), and Bayesian variational inference (Draelos & Pearson, 2020) as addressing the same problem, yet the experimental comparisons are only against random stimulation (single neurons, groups, shuffled) and a "blind" dynamical model. Beating these weak baselines demonstrates the pipeline's internal consistency but does not establish an advance over prior methods. The paper does not discuss why comparison against existing methods is infeasible.

### Minor

- **sjPCA is an incremental engineering adaptation, not a fundamentally novel method.** The streaming jPCA implementation (Section 2.1) combines proSVD (existing), Sherman-Morrison (standard), and Orthogonal Procrustes (standard for aligning streaming subspaces). The paper frames it as a "novel streaming latent space construction method" (line 68), but it is a reasonable engineering contribution without fundamental methodological novelty.

- **The adaptive representation selection is motivated but never validated in the stimulation pipeline.** The abstract describes "a novel streaming estimator to determine which representation is most predictive of ongoing neural dynamics at any timepoint" and claims this "allows for direct comparison between different latent representations and the opportunity for adaptive selection of stimulations." Figure 1c shows a heatmap of predictive performance, but no experiment demonstrates the system switching between representations during stimulation or shows that adaptive selection improves stimulation targeting.

- **No hyperparameter sensitivity analysis.** The method has several free parameters (latent dimensionality k, sparsity penalty λ₁, max targets ‖u‖₀^max, kernel length scales, delay d) with no analysis of how performance depends on these choices. For an experimentally-oriented method, parameter robustness is important.

- **Runtime scaling with observation count is not addressed.** The kernel regression in Eq. (7) is O(N) per evaluation where N is the number of past stimulations. The paper reports <10 ms average runtime but does not analyze how this scales as N grows, which is critical for real-time viability over long experiments.

- **Eigenvalue crossing not addressed in sjPCA.** The Orthogonal Procrustes stabilization (Eq. 2) independently aligns rotation planes without discussing how the ordering of eigenpairs is maintained when eigenvalues cross, a known problem for streaming eigendecompositions.

- **Open-loop baseline is a weak comparator.** The comparison in Section 4.2 between open-loop (S(u)=Q^T u, an identity mapping) and closed-loop (learned Ŝ) uses an unrealistically simple null model. Outperforming this baseline is expected.

### Trivial

None.

## Nice-to-Haves

- Test the method with real optogenetic or electrical stimulation data (closed-loop or in collaboration with an experimental lab). This is the single highest-leverage improvement.
- Replace the simple AR(1) stimulation model with more realistic biophysical models (opsin kinetics, spatial spread, network-mediated effects) for more convincing simulation validation on real background data.
- Add hyperparameter sensitivity analysis (k, λ₁, ‖u‖₀^max, kernel length scales, delay d).
- Provide runtime scaling analysis as a function of the number of past stimulation observations.
- Compare against at least one existing stimulation design method (Bayesian optimization, active learning) on comparable simulation setups.
- Provide statistical confidence intervals for key results beyond the toy model's N=10 runs.

## Removed Points

1. **Criticism that the AR(1) validation is "circular"** — The harsh critic claimed this was "circular validation" because the method learns the same AR(1) model used to generate the data. However, the method does not have access to the true AR(1) parameters; it must learn them from observations. The real limitation (which is retained in the review) is that the validation uses a synthetic, simple stimulus-response function rather than a real biological one — this is a gap in evidence, not circularity.

2. **Criticism about missing Appendix C dynamical model comparison** — REMOVED per rule: weaknesses about missing appendix content are removed because the parser strips appendices from all papers; they exist in the original submission.

3. **Harsh critic's "Strengthening the Paper on Its Own Terms" section** — Absorbed into Nice-to-Haves above. The concrete suggestions are retained (real stimulation testing, better biophysical models, comparison against existing methods) but reframed as desirable extensions rather than required fixes.

4. **Abstract phrasing complaint** — The harsh critic's note about the abstract being "misleading" is partially retained in the Major weakness about synthetic validation, but the pure wording critique is subsumed.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the core gap between the paper's claims (real-time adaptive stimulation of latent neural dynamics) and its evidence (validation only on synthetic stimulation effects), but this gap is evident from reading the paper directly.

## Suggestions

1. **Reframe the paper's claims to match the evidence.** If real stimulation experiments are not feasible, the paper should be upfront about being a simulation study of a proposed pipeline. Drop phrases like "demonstrate on real neural data" without clarifying the synthetic nature of the stimulation effects.

2. **Strengthen the baselines.** Even without real stimulation data, the paper should compare against at least one existing method (Bayesian optimization, active learning) on the toy model or on the synthetic-stimulation real-background setup. This would establish an empirical baseline for the method's value.

3. **Validate the adaptive representation selection.** Run a simple experiment showing the system switching between latent representations and measure whether this improves stimulation targeting quality compared to using any single fixed representation.

## Score and Decision

**Calibration process:**

*Round 1 — Bracketing:* Six queries across score bands found the paper's most direct analog was "Identifying neural dynamics using interventional state space models" (FwW3jqchtY.md, avg 5.0, Reject), which addresses the same problem of causal neural dynamics modeling under perturbations but with real stimulation data and theoretical identifiability results. The paper under review is weaker on evidence quality and theoretical depth but stronger on pipeline completeness. On the lower end, "QuantFormer" (BBldjKEBlJ.md, avg 3.0) and "EEGTrans" (ydw2l8zgUB.md, avg 3.5) share the issue of claiming real-world applicability without real-world testing. Bracket: **3.0–5.0**.

*Round 2 — Narrowing:* Itemized comparison against the iSSM anchor (avg 5.0) showed the paper under review lacks the real perturbation data and theoretical results that anchor had. The iSSM anchor's strongest strengths had weights 10+ (e.g., "important open problem" weight=10.24), while this paper's strengths top out at 9.48. More importantly, the "no comparison to existing methods" weakness carries a negative weight (-3.77) in the scoring model — a stronger signal than any negative-weight item in the iSSM anchor. Together with the synthetic-only validation concern (weight 3.47), this places the paper clearly below the 5.0 anchor.

*Calibration against all retrieved anchors:*
- FwW3jqchtY.md (avg 5.0, Reject) — most similar topic; has real perturbation data and theory; our paper is weaker on both dimensions.
- BBldjKEBlJ.md (avg 3.0, Reject) — shares "claimed real-time applicability without testing" issue but has more fundamental architectural concerns.
- eR1119aUlL.md (avg 4.25, Reject) — real-time neural modeling with real data validation; our paper has broader pipeline but weaker validation.
- YIls9HEa52.md (avg 6.6, Accept) — higher-quality neural dynamics paper; our paper does not match this level.
- ydw2l8zgUB.md (avg 3.5, Reject) — synthetic-only validation with weak baselines; our paper is somewhat stronger but shares these issues.

Final placement: **3.5–4.5**. The paper has a coherent pipeline and addresses a genuine problem, but the two major weaknesses (synthetic-only validation, no comparison against existing methods) significantly limit what the evidence supports relative to the claims. The strengths are real but the gap between claims and evidence cannot be fully bridged by the current experiments.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>