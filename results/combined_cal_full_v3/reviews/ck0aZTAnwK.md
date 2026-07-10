I now have a thorough calibration. Let me write the final review.

## Summary

This paper studies pre-training under fixed data and no compute constraints — a timely problem given that compute grows ~4×/year while web text grows ~1.03×/year. The paper makes three main contributions: (1) an **asymptote evaluation framework** that evaluates scaling recipes by their limit loss as model size (or ensemble size) → ∞, rather than at a fixed compute budget; (2) a **regularized recipe** showing that optimal weight decay is up to 30× larger than standard practice (0.8–3.2 vs. GPT-3's 0.1), enabling monotone loss scaling with parameter count; (3) an **ensemble scaling** finding that independently trained models achieve a lower asymptotic loss than parameter scaling alone, and that the two compose. Experiments on 200M-token DCLM data show data efficiency gains of up to 5.17×, which data scaling laws suggest persist at higher token budgets.

## Strengths

- **The asymptote evaluation framework is a genuine methodological contribution** (Sections 3–4, Figure 1). Instead of comparing recipes at a fixed compute budget (Chinchilla-style), the paper proposes evaluating the limit of loss as model size (or ensemble size) → ∞ via the fitted asymptotic constant *E* in *A/N^α + E*. This cleanly reframes the right question for the data-constrained, compute-rich regime.

- **The regularized scaling law finding is concrete and actionable** (Section 3, Figure 3). The demonstration that optimal weight decay needs to be 30× larger (up to 3.2) than the GPT-3 default of 0.1, and that this enables monotone power-law scaling with exponent ~1.02 (vs. Chinchilla's 0.34), is a genuinely interesting observation about the data-constrained regime.

- **The ensemble-vs-parameter-scaling comparison is clean and non-obvious** (Section 4, Figure 4). Showing that *K* → ∞ with fixed-size members achieves a lower asymptotic loss than *N* → ∞ with a single model, and that *K*=3 already beats the regularized recipe's asymptote, is a crisp empirical result. The demonstration that the two limits compose (Figure 5) adds further depth.

- **The problem framing is timely and well-motivated** (Section 1). The concrete data on compute growth outstripping web text growth provides a compelling, data-driven argument for studying the data-constrained regime and distinguishes this work from the vast majority of scaling-law work that assumes unlimited data.

## Weaknesses

### Major

- **The paper's central quantitative claims (asymptotes 3.43, 3.34, 3.17; data efficiency ratios 2.29×, 5.17×) derive from 3-parameter power-law fits (*A/N^α + E*) from only 4 data points, leaving one degree of freedom per fit.** The paper only addresses variance from training stochasticity (footnote 2: ±0.02 across 3 seeds), not uncertainty from functional form, data point selection, or — most critically — compounding error through the nested fits for the joint-scaling recipe (*K*→∞ per *N*, then *N*→∞ per *D*, then *D*→∞). A 0.02 shift can substantially narrow the gap between asymptotes (e.g., 3.43→3.45 vs. 3.34→3.36). The paper should provide confidence intervals or at minimum a leave-one-out sensitivity analysis. Without this, the precision of the headline numbers is unknown. This does **not** invalidate the qualitative direction of the findings (higher weight decay helps, ensembles beat single models), but it means the exact ratios should be treated with caution.

### Minor

- **The joint scaling recipe's asymptote (3.17) — the paper's best result — relies on a heuristic rather than locally optimal hyperparameters** (Section 4.3): "we cannot fully find locally optimal hyperparameters due to experimental constraints. Instead, we use the heuristic of taking the optimal regularized hyperparameters with 2× epochs and 0.5× weight decay." If this heuristic is suboptimal, the estimate could shift meaningfully.

- **The standard recipe baseline fixes weight decay at 0.1 (the GPT-3 default) and only tunes epoch count and learning rate** (Section 2). The regularized recipe tunes weight decay as well, finding much larger optimal values (0.8–3.2). The resulting 2.29× data efficiency ratio therefore conflates two effects: (a) the value of tuning weight decay at all, and (b) the value of increasing it beyond 0.1. A comparison arm that tunes weight decay but constrains it to ≤0.1 would help isolate the paper's specific claim about high weight decay.

- **The downstream evaluation is narrow**: three multiple-choice QA benchmarks (PIQA, SciQ, ARC Easy; Section 7). The abstract claims "a 9% improvement for pre-training evals" based on these three tasks. While the paper notes these are "standard benchmarks for models at our scale," the absence of generative evaluation or non-QA tasks limits the generality of the claim that loss improvements transfer to downstream capabilities.

- **The i.i.d. validation loss is the paper's primary metric (Section 2), but models are trained on repeated data (up to 16 epochs)**. When training data is repeated, the held-out validation set is not drawn from the same distribution the model sees during training — the training distribution is degenerate over the fixed corpus. This does not invalidate relative comparisons, but it weakens the rationale for using validation loss as the basis for precise asymptote estimation.

- **The data scaling analysis (Section 5.3) extrapolates from only 4 token counts spanning less than one order of magnitude (200M–1.7B) to predict behavior at scales orders of magnitude larger.** The paper acknowledges the laws "are expected to be noisy" and the conclusions are "preliminary," but extrapolating to trillions of tokens requires assuming the same functional form holds over 3–4 orders of magnitude.

- **The self-distillation result (Section 6.2) — that a 300M student outperforms its 300M teacher — is presented as a single data point without ablation of the mixing ratio between real (*D*) and synthetic (*D'*) tokens.** Given the literature on model collapse from training on synthetic data, this finding deserves more thorough investigation before being presented as a general positive result.

### Trivial

None.

## Nice-to-Haves

- Add bootstrap confidence intervals (or leave-one-out sensitivity analysis) on all power-law asymptote fits, especially the nested cascade for the joint scaling recipe.
- Add a comparison arm that tunes weight decay but constrains it to ≤0.1 to isolate the effect of increased weight decay from the effect of tuning generally.
- Include at least one non-QA evaluation (e.g., perplexity on a different-domain corpus) to broaden the downstream validation.
- Report and ablate the mixing ratio (*D*:*D'*) used in the self-distillation experiment.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Coordinate descent detail missing**: REMOVED (per rule: do not penalize missing appendix content stripped by parser; paper cites Appendix C.1).
- **Compute/data growth rates are projections**: REMOVED (nitpick on motivation language; paper cites sources transparently).
- **Muennighoff contradiction framing**: REMOVED (critic notes this is accurate and fair; not a weakness).
- **"Standard recipe baseline too weak" fully**: REMOVED the framing that this is a fatal issue. WEAKENED to Minor because the paper's claim is specifically about weight decay being higher than standard practice, and the standard recipe represents actual practice. The suggestion to disentangle tuning from high values is a refinement, not a flaw in the comparison.
- **Section-by-section notes that were observations rather than weaknesses**: REMOVED (e.g., the critic's note about Section 1 introduction language).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add uncertainty quantification** (confidence intervals, bootstrap, or leave-one-out) to all power-law asymptote fits. This is the single highest-leverage improvement. The current paper only accounts for seed variance; the more significant sources of uncertainty (functional form, data point selection, compounding through nested fits) are unaddressed.

2. **Strengthen the baseline comparison** by adding a version of the standard recipe that tunes weight decay but restricts it to ≤0.1. This would sharpen the claim that the specific high weight decay values (not just tuning in general) drive the improvement.

3. **Broaden the downstream evaluation** modestly — even one non-QA task or a generative perplexity evaluation on a different-domain corpus would substantially strengthen the claim that loss improvements generalize.

---

### Calibration Report

**Anchors retrieved across all rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../u1cQYxRI1H.md | 0.50 | R1 | No | Strong reject; unrelated topic |
| /home/.../nSDOkm0SKo.md | 1.00 | R1 | No | Strong reject; unrelated |
| /home/.../7LZjuA4AB2.md | 3.00 | R1 | No | Distribution shift paper; lower quality |
| /home/.../ewZSzO6bts.md | 3.75 | R1 | Yes | Unified scaling laws; flawed theoretical model |
| /home/.../xGM5shdGJD.md | 5.20 | R1 | Yes | Scaling law estimation; similar domain, accepted with avg 5.20 despite a metric-favored concern (favorability -2.89) |
| /home/.../xI71dsS3o4.md | 5.75 | R3 | Yes | (Mis)Fitting scaling laws; survey paper, accepted with avg 5.75 despite severe novelty concern (-4.50) |
| /home/.../WYL4eFLcxG.md | 6.00 | R2 | Yes | Scaling Optimal LR; empirical scaling law paper, accepted. Weaknesses ~5.5-6.1 favorability range |
| /home/.../KnoS9XxIlK.md | 6.00 | R2 | Yes | Multi-Power Law; empirical law paper, accepted. Worst weakness favorability 0.32 (scope) |
| /home/.../I4YU0oECtK.md | 6.00 | R3 | No | Bayesian scaling laws; in-context learning |
| /home/.../vPOMTkmSiu.md | 6.60 | R1 | No | Scaling laws for MT; downstream task focus |
| /home/.../JCiF03qnmi.md | 6.80 | R1 | Yes | Critical Batch Size; careful empirical study, accepted. Strong methodology |
| /home/.../wg1PCg3CUP.md | 8.00 | R1 | Yes | Scaling Laws for Precision; strong paper, accepted. Thorough experiments (465+ runs) |

**Calibration path:** Round 1 bracketed the paper between 5.5 and 7.5. Round 2 narrowed by comparing against the most similar anchors (Scaling Optimal LR at 6.00, Multi-Power Law at 6.00, Critical Batch Size at 6.80). Round 3 added the (Mis)Fitting Scaling Laws anchor (5.75) for further resolution.

**Favorability comparison:** This paper's strongest items (10.93, 10.33, 8.58) are comparable to the 6.00-anchors' best items (10.18, 10.49). However, this paper's worst weakness (power-law fitting, favorability 0.94) is more severe than the worst weakness of Scaling Optimal LR (favorability ~5.5–6.1). It is, however, less severe than the most damaging weaknesses in the 5.20 and 5.75 anchors (favorability -2.89 and -4.50 respectively). The net assessment places this paper just below the 6.00-anchors due to unquantified uncertainty in all central quantitative claims, but clearly above the 5.20/5.75 anchors whose contributions were more limited in scope.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>