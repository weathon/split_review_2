Good — the favorability scores confirm the weight of each item. The two Major weaknesses are rated at 0.00 (strongly negative), while the three strengths all score ≥0.93 (strongly positive). This tells me the paper has genuinely strong contributions but the evaluation gap is severe enough to prevent acceptance in its current form.

Let me finalize the review accordingly.

---

## Summary

This paper proposes a streaming framework for designing high-dimensional neural stimulations that target low-dimensional latent dynamics under realistic experimental constraints (non-negativity, limited targets, bounded power). The framework integrates streaming latent space construction, dynamical modeling, a nonparametric kernel-regression stimulus-response mapper, and a constrained optimization procedure. Experiments use a toy model (circular LDS) and two real neural datasets (calcium imaging, electrophysiology).

## Strengths

- **Well-motivated problem.** The paper identifies a genuine gap: no existing streaming method addresses the full problem of designing high-dimensional stimulations to drive low-dimensional latent dynamics under realistic constraints. The combinatorial argument (30 out of 400 neurons → ~10⁴⁵ combinations) effectively motivates the need for an algorithmic approach.

- **Coherent framework design.** The four-component pipeline — streaming latent space construction, dynamical modeling, nonparametric stimulus-response mapping, and constrained optimization — is logically structured and addresses the right sub-problems. Algorithm 1 provides a clear picture of how the components interact in real time.

- **Runtime feasibility.** The reported end-to-end runtimes (<10 ms average, <100 ms worst-case) are concretely documented and are genuinely fast enough for real-time applications at typical neural data acquisition rates (15–30 Hz).

## Weaknesses

### Fatal
None.

### Major

1. **Real data experiments use simulated AR(1) stimulations, not real stimulation-response data.** The paper states (Section 4.1): "For each of the real datasets, we simulated stimulations using an autoregressive function…" with a known additive process `y_t = r_t + a_t`, `a_t = 0.8·a_{t-1} + u_t` overlaid onto real neural recordings. The paper never tests whether its framework can learn a genuine (non-synthetic) stimulus-response map or successfully design stimuli that produce desired effects on real neural dynamics. The central claim — providing "a novel streaming method for stimulation-response modeling… and an optimization framework for selecting high-dimensional stimulation patterns to drive low-dimensional dynamics" — is only validated on the toy model for the optimization component and on a known additive process for the real-data response modeling. This gap between what is claimed and what is validated undermines the core empirical contribution. The paper acknowledges this as a limitation (Discussion), but the gap remains too large for the claims to be considered substantiated.

2. **The optimization framework is only evaluated on the toy model; real data experiments do not test the optimization loop.** On real data, stimulations are pre-determined (14 of 592 neurons at particular timepoints), not the output of the optimization procedure. The paper tests whether the kernel regression can *predict* the effect of a *known* stimulation, but never tests whether the optimization (Eq. 8) can successfully *design* stimuli to produce a *desired* latent effect on real neural data. The closed-loop results (Fig. 5) also use the toy model with a known S function. Since stimulus design is half of the paper's stated contribution, this is a significant evidential gap.

### Minor

3. **Ambiguous sparsity regularization in Eq. (8).** The term `λ₁(||u||₀^max − ||u||₁)` with u ∈ [0,1]^N is problematic: if λ₁ > 0, minimizing the term maximizes ||u||₁ (spreading energy across more neurons) — the opposite of sparsity. If λ₁ < 0, the formulation works but the sign is never clarified. The describing text also uses inconsistent notation ("offset by N" vs. `||u||₀^max`).

4. **Weak baselines.** The stimulus-response model is compared only against a "blind" model that ignores stimulation entirely — showing that a model accounting for a known perturbation outperforms one that ignores it. The optimization baselines (random single-neuron, random multi-neuron, shuffled stimuli) show the method works better than random, but no comparison is made against even simple principled alternatives (e.g., greedy selection, linear least-squares estimation).

5. **sjPCA and parallel selection are disconnected from the stimulation pipeline.** The sjPCA method is presented as a novel streaming contribution but is never used in any stimulation experiment (real data uses proSVD). The parallel model selection capability (Fig. 1c) is demonstrated for predictive accuracy but its utility for the stimulation task is not validated. These components are described but their role in the main pipeline goes untested.

### Trivial
None.

## Nice-to-Haves

- Replace the AR(1) overlay with a more realistic forward model (e.g., a biophysical model of opsin-mediated effects that has genuine state-dependence and nonlinearity), and test the full optimization loop against it.
- Compare against at least one non-random baseline for optimization (greedy selection, linear regression-based approach, or Bayesian optimization over a limited candidate set).
- Clarify the sign convention for λ₁ in Eq. (8) and resolve the notational inconsistency.

## Removed Points

These points were considered but removed with justification:
- **Algorithm 1 inconsistency (x_t vs x_{t-d}):** The critic claimed using x_t for prediction is inconsistent with using x_{t-d} for training. This misunderstands the algorithm — when designing a stimulus at time t to be delivered *now*, the current state x_t *is* the state at stimulation time. The training stores (x_{t-d},·) because the stimulus was delivered at time t−d; for a new stimulus at time t, x_t is correct.
- **O'Shea et al. discussion depth:** A suggestion to discuss already-cited prior work more directly — a presentation preference, not an evidential weakness.
- **Toy model binary stimulations:** The critic noted the toy model S function only checks u ∈ {0,1}. The optimization itself operates over u ∈ [0,1]^N; the toy model's threshold-based response is a modeling choice, not a flaw in the optimization's evaluation.

## Novel Insights

The synthetic-data evaluation reveals an interesting property not emphasized by the paper: the relationship between feasibility manifolds and stimulation design. The observation that some latent directions (e.g., blanket inhibition) are inherently infeasible under non-negativity and sparsity constraints (Fig. 4b) identifies a fundamental constraint on what kinds of neural perturbations are achievable — a finding with implications for experimental design independent of the optimization method used. Additionally, the use of a temporal kernel in the regression to detect and recover from non-stationarities (flips and rotations in the stimulus-response map, Fig. 2d–e) is a practically valuable mechanism.

## Suggestions

- The single most impactful improvement would be to test the full closed-loop optimization pipeline on data where the stimulus-response mapping must be learned from actual (non-AR(1)) observations — either real stimulation-response data or a biophysically realistic forward model with genuine state-dependence and nonlinearity.
- Compare against at least one principled non-random baseline for optimization.
- Clarify the regularization sign convention in Eq. (8) and fix the notation.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>