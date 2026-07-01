Now let me produce the final review.

## Summary

This paper demonstrates that normalized training loss curves (TLCs) from LLMs of different sizes collapse onto a universal trajectory when the AdamW timescale τ, the tokens-per-parameter ratio (TPP), and the learning-rate schedule are matched across scales. The authors identify these controls experimentally (Section 3), introduce the Celerity model family trained with fixed TPP and optimal τ (Section 4), and show two practical applications: using collapse residuals as an early diagnostic of training pathologies, and enabling early stopping in hyperparameter tuning by extrapolating final loss from partial runs via a parametric surrogate (Section 5).

## Strengths

1. **Clean empirical demonstration of the three controls governing TLC shape (Section 3, Figures 3–4).** The systematic isolation of τ, TPP, and LR schedule — showing that sweeping η, λ, or B independently produces different raw curves but curves with matching τ align — is an informative experiment that goes beyond prior work (Qiu et al. 2025 did not study AdamW's weight decay timescale).

2. **Practical diagnostic application with a concrete, documented case study (Section 4, Figures 1 right, 6 right).** The 1.8B case study — where a numerical instability was detected via collapse residuals at ~60% of training rather than via raw loss divergence at ~90% — is compelling and well-documented. The authors describe how the collapse reference pinpointed the onset timing, ruled out data-side causes, and guided a targeted fix.

3. **Early stopping procedure for HPO (Section 5, Figure 9).** The approach of fitting a parametric surrogate for normalized TLCs at 111M scale and extrapolating final loss from 10–30% of large-scale training is clever. The gap vs. "current best" selection is substantial (near 0% loss gap for "predicted best" vs. up to ~1.4% for "current best" at early stopping points).

## Weaknesses

### Fatal
None.

### Major
None. The core empirical claims (conditions for collapse, diagnostic value, early stopping utility) are supported by the evidence presented. The weaknesses below are framing, documentation, and scope issues that do not invalidate the main contributions.

### Minor

1. **The "signature of compute-efficient training" claim is imprecisely supported.** The paper states that collapse is a "signature of compute-efficient training" (Abstract, line 31, line 38). The evidence clearly shows that collapse follows from *fixed τ and fixed TPP* across model sizes. However, Section 3 (Figure 3) shows that **any** fixed τ (not only the optimal one) yields matched TLC shapes when TPP is held fixed. The paper does not test whether suboptimal τ would *break* collapse at fixed TPP, or whether optimal τ produces systematically tighter collapse. The connection to compute-efficiency is imported from Bergsma et al. (2025a) and demonstrated via Celerity's position on the Pareto frontier, but claiming collapse as a *signature* of optimality specifically (rather than of consistent scaling) conflates two different claims. This is a framing issue — the core findings are unaffected, but the headline should be calibrated to say "collapse is a signature of consistent τ-and-TPP scaling; when combined with optimal-τ-in-TPP scaling laws, it coincides with compute-efficient training."

2. **Llama-2 τ values in Figure 1 are presented without derivation.** Figure 1 (left) shows Llama-2 curves with specific τ values (0.07, 0.13) and attributes the lack of collapse to varying τ and TPP. The paper never explains how τ was computed from Llama-2's published hyperparameters (η, λ, B, D). While the varying-TPP observation is verifiable from public data (D/N ratios), the τ claims and the "before/after" narrative would benefit from a documented derivation or hyperparameter table. Without this, the comparison is not fully reproducible.

3. **The Pareto frontier comparison (Figure 2) mixes heterogeneous training recipes.** Celerity is claimed to be on the accuracy/compute Pareto frontier, but the comparison set includes models from different years with different data mixtures, annealing protocols, and evaluation setups. The paper acknowledges this obliquely but does not quantify confounds. The power-law formula in the caption ("100 - 5 / (tau * 154e38)^-0.097") is never explained in the text, making the extrapolation claim uninterpretable.

4. **The parametric surrogate (Eq. 4–5) is under-documented.** The functional form was selected through experimentation on 111M-scale data without explicit reporting of the candidate set, the number of curves used for fitting, or hold-out validation. The alternating fitting procedure for b and q parameters is described without convergence diagnostics. The empirical validation at 3.3B scale mitigates overfitting concerns, but the construction would be difficult to reproduce for new regimes.

5. **The "early-align" diagnostic normalization is blind during the first 25% of training.** For diagnostic use, the paper normalizes by aligning to a reference curve over 25–50% of training (line 194). This means any training issue that begins before 25% would not be detected by this method. This limitation is not discussed.

### Trivial
- The paper uses "LLM scale" and "full-scale LLM families" for models up to 3.9B parameters. By 2025–2026 standards this is modest. The paper should describe the tested range as "up to 3.9B parameters (a ~35× range from 111M)" rather than "full-scale."

## Nice-to-Haves

- Add variance/confidence estimates for collapse measurements to calibrate what counts as a meaningful "deviation from collapse" given inter-run noise.
- Document the sensitivity of the early stopping procedure to the fixed hyperparameters m=0.05, ε₁=0.001, ε₂=0.2.
- The parametric surrogate could be strengthened with cross-validation results or a discussion of functional form selection.
- Explicitly discuss the early-align normalization's 25% blind window.

## Removed Points

- **Celerity competitiveness "caused by collapse" (strawman).** The reviewer claimed the abstract implies collapse *causes* Celerity's competitiveness. The paper states "collapse emerges naturally as a consequence of good training" (line 139) and attributes competitiveness to "effective parameterization, including tuning and transferring τ" (line 33). This is not a causal claim from collapse to competitiveness; removed as a misreading.

- **Reliance on Appendix C.1 for compute-vs-parameter trade-off (missing appendix).** The reviewer criticized the derivation being in Appendix C.1, which was stripped by the parser. The main text reports the key result (62% parameter reduction for 67% FLOPs increase) and Figure 5 visualizes the trade-off. Removed per rule against penalizing appendix-deferred content.

- **No statistical significance / variance estimates (scope creep).** This is standard practice for empirical scaling-law papers with single-run evaluations at these compute budgets. Moved to nice-to-have.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface unanticipated interpretations beyond what the paper already articulates.

## Suggestions

1. Reframe "signature of compute-efficient training" to the more precise formulation: collapse is a signature of consistent τ-and-TPP scaling; when combined with the known dependence of optimal τ on TPP, it coincides with compute-efficient training.
2. Document the derivation of Llama-2 τ values, or remove the specific τ labels and rely on the observable TPP variation alone.
3. Explain the Figure 2 power-law formula in the text and discuss confounds in the Pareto frontier comparison.
4. Acknowledge the 25% blind window of the early-align normalization.
5. Add brief convergence diagnostics for the alternating fitting procedure.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>