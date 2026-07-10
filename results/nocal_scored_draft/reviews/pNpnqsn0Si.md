Now I'll assemble the final consolidated review.

## Summary

This paper proposes Thoughtbubbles, a transformer variant that learns to dynamically fork and delete residual streams during pretraining using only language modeling loss. The key idea is a budget-bounded allocation problem: each residual stream accumulates a score, and the model decides whether to keep, fork, or delete it via a top-k mechanism. Forked streams are processed in parallel with score-attenuated attention and residual updates, then merged via weighted averaging at the output. The method is evaluated at 150M–772M scales on OpenWebText and peS2o, showing consistent perplexity improvements over standard transformers and non-adaptive parallel computation baselines (Copy-3/Copy-5).

## Strengths

- **Genuinely novel mechanism.** The forking/merging of residual streams during pretraining is a clean idea that differentiates this work from the pause-token line (fixed-position computation) and the CoT line (autoregressive generation). The formalization as a budget-bounded allocation problem (learned scores → top-k → score-attenuated processing → output averaging) is internally coherent.

- **Consistent perplexity improvement across all scales and settings.** In Table 1, Thoughtbubbles (κ=4L) achieves the lowest perplexity in every single row — all 6 model/dataset combinations. At 772M on OpenWebText, perplexity drops from 21.22 (baseline) to 19.74; on peS2o from 14.64 to 13.77. The direction is consistent across every setting, indicating a genuine architectural improvement.

- **Cross-scale outperformance.** The 319M Thoughtbubbles model (20.23 perplexity) beats the 772M baseline (21.22 perplexity) on OpenWebText. A 2.4× smaller model outperforming a larger one is a strong sanity check that the method provides meaningful value beyond simply adding parameters or compute.

- **Well-designed entropy-fork correlation diagnostic.** Figure 5 uses entropy measured from an independently trained baseline model (not just the forking model itself), ruling out the simplest confound that forking causes entropy rather than responding to it.

## Weaknesses

### Major

- **Motivation-experiment gap.** The paper motivates against pause-token methods (lines 17–20), arguing they insert computation at fixed positions and require manual placement, and positions Thoughtbubbles as addressing these limitations. However, no pause-token baselines (Goyal et al., 2024; Herel & Mikolov, 2024; Sun et al., 2025) are included in the experiments. While the Copy-3/Copy-5 baselines do test non-adaptive parallel computation, the paper's framing creates an expectation of comparison against the cited pause-token approaches that is not fulfilled. The scope of the empirical comparison is narrower than the motivation suggests.

### Minor

- **No variance estimates for zero-shot evaluations where results are close.** No confidence intervals or significance tests are reported. On several tasks the margins are small (e.g., HellaSwag at 319M on OpenWebText: Ours κ=2L=29.3, Ours κ=4L=29.0, Baseline=28.7 — both variants bracket the baseline within 0.6 points). The paper appropriately hedges its claims on BLiMP and PIQA (acknowledging mixed results), but variance estimates would strengthen confidence in the reported advantages on LAMBADA and HellaSwag.

- **The "roughly FLOPs-matched" claim is imprecise.** Line 212 states Ours (κ=4L) is "roughly FLOPs-matched against copy-5 baseline" without actual FLOP counts or analysis. Since forking occurs at only 3 layers while Copy-5 processes 5× sequence length at every layer, the FLOP profiles differ substantially. Actual counts are needed to assess this comparison.

- **The "parameter-matched" claim is underspecified.** The forking decision functions (3 layers × 2×d_model parameters) and learned fork embeddings (3 layers × d_model) add parameters beyond the base transformer. The paper states "Each setting is parameter-matched" without explaining whether base model dimensions were reduced to compensate. While the overhead is tiny (~0.005%), the claim should be explicit.

- **The gradient bottleneck through top-k is acknowledged but unmitigated.** The Limitations section (lines 320–321) notes that hard top-k decisions later in the model cut gradients to early forking layers. A frozen-score ablation (randomly initialized, frozen forking scores) would help separate gains from adaptivity from gains due to increased architectural capacity. Without this, it is unclear how much of the improvement comes from the adaptive mechanism itself.

- **Forking decision function architecture is unspecified.** The function f_θ^{(k)} : R^{d_model} → R^2 is described by its input/output dimensions but its architecture (linear? MLP? initialization?) is not stated. This affects understanding of the extra parameter count and the learned scoring quality.

### Trivial

- The RoPE "partial rotation" design for forked tokens is deferred entirely to Appendix D without a brief summary in the main text.

## Nice-to-Haves (not core flaws)

- Report actual FLOP counts for the computation-matched comparisons.
- Include a frozen-score ablation to directly test whether learned forking decisions drive the gains.
- Sweep κ values more finely (κ=1.5L, 3L, 6L, etc.) to understand hyperparameter sensitivity.
- Provide qualitative analysis of which tokens get forked (e.g., parts of speech, syntactic roles).
- Summarize the RoPE partial-rotation design briefly in the main text.

## Removed Points

These points from the input review are not included in the final assessment:
- Claim that the paper overstates BLiMP/PIQA results: the paper already acknowledges mixed results (lines 220–225: "our model only outperforms the parameter-matched, but not computation-matched baselines" for BLiMP; "performs similarly" for PIQA). The claims are appropriately hedged.
- Claim that the paper overstates pause-token limitations: this is a judgment call, not a factual error.
- "No analysis of what gets forked" beyond entropy: the entropy analysis is a meaningful first step; finer-grained analysis is a nice-to-have, not a weakness.
- Formatting/presentation nitpicks: these are parser artifacts, not author errors.
- The "Strengthening the Paper on Its Own Terms" and "Missing Parts" sections: subsumed into Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface issues about experimental scope and evidential precision but do not contribute novel analytical insights.

## Suggestions

- Expand the experimental scope to include pause-token comparisons, or alternatively re-frame the motivation to match the empirical scope.
- Add FLOP counts for all model variants and clarify the computation-matched comparison.
- Report confidence intervals or bootstrap estimates for zero-shot evaluations.
- Include a frozen-score ablation to isolate the contribution of adaptivity.
- Explicitly state how parameter-matching was achieved (or quantify the small overhead).

## Score and Decision

The paper introduces a genuinely novel mechanism with consistent perplexity improvements across all tested scales, and the cross-scale outperformance result is striking. However, the motivation frames the contribution against pause-token methods that are not compared against in experiments, creating a gap between framing and evidence. The remaining issues (imprecise FLOP-matching, missing variance, underspecified parameter-matching, unmitigated gradient bottleneck) are minor individually but collectively weaken the evidential basis. The contribution is real and the architecture is clearly novel; with stronger baselines and more precise reporting the paper would be substantially stronger.

**Score:** 6

**Decision:** Borderline Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>