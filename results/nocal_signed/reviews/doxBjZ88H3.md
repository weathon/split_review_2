Now I have all the signal I need. Let me write the final consolidated review.

## Summary

This paper proposes an information-theoretic framework for optimizing experimental designs to distinguish between two competing hypotheses about probabilistic neural codes: likelihood coding (probabilistic population codes) versus posterior coding (neural sampling codes). The key contribution is the *information gap* — derived analytic expressions (Eqs. 1–5) for the expected decoder performance difference under each hypothesis — which is validated through extensive simulations and used to produce actionable parameter landscapes (e.g., optimal prior separation d≈30° and width σ≈20° for low-contrast Gaussian priors). The Allen Institute null result (Δ≈0 under uniform priors) is cleanly framed as motivation rather than overclaimed validation.

## Strengths

- **Clean, non-trivial derivations.** The analytic expressions for Δ_L^info (Eqs. 1–2) and Δ_P^info (Eqs. 3–5) are genuinely derived. The insight that the optimal mismatched decoder converges to a task-marginalized Bayes-optimal estimator is sound, and the posterior-coding case involves a particularly non-trivial fixed-point condition (Eqs. 4–5) that identifies when a likelihood decoder is necessarily ambiguous.
- **Thorough simulation validation.** Figures 3 and 4 demonstrate convergence of empirical decoder performance differences to theoretical predictions across number of trials, number of neurons, and three contrast levels. The validation extends to a gain-modulated Poisson model (Goris et al. 2014) beyond the exact generative form assumed in the theory, showing robustness to model assumptions.
- **Actionable information gap landscapes.** Figures 5 and 6 provide concrete, visual guidance for experimental design (e.g., optimal separation d≈30° and prior width σ≈20° for low-contrast Gaussian priors; the finding that heavy-tailed priors are ineffective). These are directly usable by experimentalists.
- **Appropriate use of empirical null result.** The Allen Institute analysis (Fig. 7) shows Δ≈0 under uniform priors, confirming that single-context designs cannot distinguish the hypotheses. This is correctly framed as motivation for the framework rather than overclaimed validation.
- **Clear problem identification.** The paper correctly identifies that the debate between likelihood-coding and posterior-coding has been stalled partly because no one has quantified *how* to design an experiment that can tell them apart — the tradeoff between making contexts sufficiently different while maintaining overlap is real and unresolved.

## Weaknesses

### Fatal
None.

### Major
- **Discretization sensitivity of posterior-coding landscapes.** The posterior-coding information gap (Δ_P^info) depends on exact posterior equality across contexts (Eq. 4: ∀θ, p^A(θ|x_j) = p^B(θ|x_k)). Since the framework operates on discretized observations x∈{x_i}, the number of observation pairs satisfying this condition — and therefore the magnitude of Δ_P^info — could depend sensitively on discretization granularity. The paper does not examine this sensitivity. Without demonstrating that the Δ_P^info landscapes (Figs. 5 bottom row, 6) are stable across a range of bin sizes (e.g., 0.5°, 1°, 2°), the optimized parameter recommendations for posterior-coding rest on an unexamined methodological choice.

### Minor
- **Heuristic "sweet spot" selection.** The strategic task design selection (Section 4.1, lines 151–155) picks "sweet spots" using prose ("posterior-coding Δ approaches its maximum while likelihood-coding maintains sufficient discriminative signal") rather than a formal joint optimization criterion (e.g., maximize min(Δ_L, Δ_P) or Δ_L + λ·Δ_P). The title and framing emphasize principled optimization, yet the final selection rule is described qualitatively.
- **Parameter selection for validation underspecified.** The paper states "at least ten different sets of task parameters are selected" for Fig. 4 but does not describe whether these were randomly sampled, gridded, or manually chosen. The strong y=x agreement could partially reflect that the chosen points avoid regions where theory might break down.

### Trivial
None.

## Nice-to-Haves
- Formalize the joint optimization over both coding hypotheses with a concrete objective (e.g., maximize Δ_P subject to Δ_L ≥ ε).
- Quantify how much the optimized design improves over heuristic intuition (e.g., comparing against "maximally separated priors" or "equal-width overlapping Gaussians").
- A discretization sensitivity analysis for posterior-coding landscapes would strengthen confidence in the optimized designs.

## Removed Points
These points are flagged to be removed, treat them with caution:
1. "Continuous limit → Δ_P^info = 0" — The framework is explicitly defined on discretized observations; this criticism attacks a setting the paper never claims to address.
2. "Self-consistency validation not independent" — Validation against the same generative class is standard for theoretical papers; the paper additionally validates against gain-modulated Poisson.
3. "Notation sloppiness" — Typo-level issue, removed per hard rules on formatting artifacts.
4. "Appendix content missing" — Multiple points about appendix-deferred proofs/details; the appendix exists in the original submission.
5. "Statistical power for Allen dataset" — Speculative concern not supported by available data.
6. "Imperfect priors handling nontrivial" — The paper provides a procedure in Appendix A.4, which is a reasonable treatment.
7. "Heavy-tailed priors not quantified" — The paper refers to Appendix A.8 for details.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add a sensitivity analysis of Δ_P^info landscapes to discretization bin size and report whether the optimal (d, σ) recommendations shift meaningfully.
- Formalize the sweet-spot selection with a concrete objective function.
- Clarify how the ten+ parameter sets for Fig. 4 were selected (random, grid, or manual).

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>