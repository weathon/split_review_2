## Summary

This paper extends the recently discovered phenomenon of *loss curve collapse* — where normalized training loss curves for different model sizes align onto a universal trajectory — from small-scale settings with vanilla Adam to full-scale LLM families trained under practical recipes (co-scaling width, depth, batch size, weight decay with AdamW and μP). The authors identify three controls that govern collapse: the AdamW timescale τ, tokens-per-parameter (TPP) ratio, and LR schedule. They introduce the Celerity model family (300M–3.9B) trained at fixed TPP with optimal τ, demonstrating collapse and two applications: (i) using collapse residuals as an early diagnostic of training issues, and (ii) leveraging a parametric surrogate of normalized curves to enable early stopping (10–30% of training) for hyperparameter tuning.

## Strengths

- **Practical diagnostic utility.** The demonstration that collapse residuals detect training anomalies (e.g., numerical issues near 60% of training) well before raw loss shows a visible blip is compelling and directly useful for practitioners running large-scale LLM training.
- **Clear identification of scale-invariant controls.** The paper convincingly shows that τ, TPP, and LR schedule jointly determine TLC shape, and that matching these across model sizes produces collapse. The experiments sweeping η, λ, B while holding τ fixed (Figure 3) cleanly isolate the effect.
- **Actionable early-stopping procedure.** The proposed method — fitting a parametric normalized TLC on small-scale runs, then aligning partial large-scale curves to predict final loss — is principled, leverages collapse directly, and shows strong results (near-zero loss gap after 10–30% of training). This offers a concrete way to reduce tuning cost.
- **Compute-efficient Celerity models.** The 234-TPP band lies on the accuracy/compute frontier among open models (Figure 2), and the analysis of the compute vs. compression trade-off (Figure 5) provides a grounded rationale for choosing TPP.

## Weaknesses

### Fatal
None.

### Major
- **Modest model scale for a "full-scale LLM" claim.** The largest Celerity model is 3.9B parameters. While the paper convincingly shows collapse up to this size, many LLM families now train beyond 70B parameters. The claim that collapse "persists for LLM families" is supported only up to a relatively modest scale. The paper would benefit from demonstrating collapse at least at the 7B–13B scale (which is common in open families) or acknowledging this limitation more prominently.
- **Collapse is approximate, not exact, and the deviations are not fully explained.** At 20 TPP, Figure 6 shows clear early deviations attributed to differing warmup proportions, and at 234 TPP the middle plot shows late-training divergences that the authors admit reflect disproportionate improvement on training vs. held-out data. These deviations undermine the claim that collapse is a *signature* of compute-efficient training — they suggest collapse may depend on details of data distribution or warmup in ways not captured by τ, TPP, and schedule alone. The paper should more carefully characterize when collapse degrades and whether the diagnostic use is robust to mild violations.
- **The parametric surrogate model (Eq. 4–5) is heuristic and lightly validated.** The functional form is proposed without strong theoretical justification, and the alternating fitting procedure, while pragmatic, risks being brittle. Validation is limited to 111M-scale data and two larger scales (1.7B, 3.3B). The paper does not test whether the surrogate generalizes to unseen combinations of τ and TPP, or whether the power-law fits for b and q extrapolate reliably beyond the training grid. The claim that predictions "improve with scale" is based on only two target scales and could be coincidental.

### Minor
- **Celerity's evaluation is limited to 7 downstream tasks.** While the paper selects common benchmarks, modern LLM evaluation typically covers a much broader suite. The compute-efficiency frontier claim (Figure 2) would be strengthened by more tasks and by controlling for data composition differences across models.
- **The early-stopping procedure requires knowing TLC controls for large-scale sweeps.** Step 1 of the procedure says "identify the corresponding TLC controls" for each large-scale setting, but these controls include τ, which itself depends on the hyperparameter being swept (e.g., λ). If the sweep varies λ, τ changes, and one must train small-scale runs for each λ value anyway — reducing the practical advantage. The paper could clarify how often the small-scale step is genuinely avoided.

### Trivial
- The figures are dense and sometimes difficult to parse in grayscale (e.g., Figure 4 right, many overlapping curves).

## Nice-to-Haves

- Provide a simple recipe for practitioners: given a target model size and compute budget, how should one choose TPP and τ to *guarantee* collapse? The current paper gives heuristics but no closed-form guidance.
- Include an ablation where the parametric surrogate is replaced by a more principled form (e.g., derived from the noisy quadratic model in Appendix B.3) to test whether the heuristic form is essential.
- Validate the early-stopping procedure on a real-world large-scale sweep where the "true best" is known only after full training (e.g., a held-out λ sweep at 7B+).

## Novel Insights

The paper's core insight is that the AdamW timescale τ — not just learning rate or weight decay individually — acts as a *scale-invariant control* that shapes training loss curves. Combined with TPP, this offers a unified explanation of why curves from different model sizes can collapse. The practical deduction is that monitoring deviations from a collapsed reference provides an interpretable, quantitative diagnostic that is sensitive earlier than raw loss. The parametric surrogate, though heuristic, demonstrates that normalized TLCs can be predicted *across* hyperparameter settings, not just matched when settings are identical. None beyond the paper's own contributions.

## Suggestions

1. Acknowledge more explicitly the scale limitation (up to 3.9B) and discuss whether collapse is expected to hold at 70B+ given known challenges (e.g., loss spikes, hardware heterogeneity). If possible, include a small validation at 7B scale using existing open models with controlled TPP and τ.
2. Characterize when collapse fails: under what conditions (e.g., very high TPP, unusual LR schedules, data distribution shifts) do deviations become large enough to degrade the diagnostic utility? This would strengthen the practical guidance.
3. For the parametric model, report cross-validation results where the power-law fits for b and q are trained on a subset of (τ, TPP) pairs and tested on held-out pairs, to assess generalization more rigorously.
4. Clarify in the early-stopping procedure how one obtains the "TLC controls" for large-scale runs without pre-training small-scale equivalents. If small-scale runs are required for each unique combination, the procedure may be less impactful than presented.

## Score and Decision

**Score:** 6.0

**Decision:** Accept

The paper presents a well-motivated empirical study with clear practical applications. The core claims — that collapse persists at LLM scale under appropriate scaling recipes and has diagnostic value — are supported by the experiments, though the scale of validation and occasional deviations from perfect collapse temper the strength of the conclusions. The early-stopping application is particularly interesting and novel. The paper is clearly written and will likely influence how practitioners think about training curve predictability. While the contribution is incremental over Qiu et al. (2025) in the sense that it extends from small-scale μP to practical LLM settings, the added analysis of τ as a control and the two applications (diagnostics, early stopping) provide sufficient novelty and practical value to merit acceptance at a top venue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>