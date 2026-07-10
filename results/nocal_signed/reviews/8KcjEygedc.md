Now here is my final consolidated review.

---

## Summary

This paper develops a theoretical framework for data curation in high-dimensional binary classification, deriving exact scaling laws for test error under label-agnostic and label-aware pruning rules. The core result (Theorem 2) predicts a qualitative phase transition: when the generator is strong and data is abundant, "keep hard" is optimal (explaining LIMO/s1-style successes); when the generator is weak, "keep easy" is optimal (explaining classical "more is more" scaling). The framework extends prior theoretical work on synthetic data oracles to settings where the oracle also assesses example difficulty.

## Strengths

- **Clean theoretical setup with an interpretable qualitative prediction (Theorem 2).** The paper derives a crisp, memorable result showing when "keep hard" vs. "keep easy" is optimal, grounded in a tractable high-dimensional Gaussian model. The qualitative rule directly engages with the motivating LIMO/s1 observations and gives practitioners a concrete lens. (Impact: +9.2)

- **Timely and well-motivated framing.** The paper correctly identifies a genuine tension between classical scaling laws ("more is more") and recent aggressive pruning successes ("less is more"), and offers a concrete theoretical lens for resolving it. The connection to model collapse as a second application adds breadth. (Impact: +9.8)

- **Meaningful extension of prior theoretical work.** The framework generalizes Feng et al. (2025) and Firdoussi et al. (2024) from oracles that only filter for label correctness to oracles that also assess example difficulty, clearly stating this relationship and providing a unified treatment. (Impact: +7.2)

## Weaknesses

### Fatal
None.

### Major

- **Theorem 2 covers a limited regime that does not include the practically relevant case.** Both parts of Theorem 2 assume the pruner is excellent (ρ* → 1) AND the data-rich, unregularized limit (φ → 0, λ → 0). In the LIMO/s1 settings that motivate the paper, the pruner is typically a model closely related to the generator — its quality is not independently excellent. The theory does not address the regime where both generator and pruner are imperfect (ρ < 1, ρ* < 1), nor does it discuss how the optimal strategy changes for finite φ and λ. This significantly limits the applicability of the paper's main qualitative claim to realistic settings. (Impact: -7.4)

- **The ImageNet experiments are described at a level that prevents proper evaluation.** Section 4.3 claims empirical validation on ImageNet but omits critical details: the model architecture used (ViT? ResNet?); how "difficulty" is operationalized for multi-class ImageNet images in a way corresponding to |x^T w_o| in the theory; how pseudo-labels were generated and validated; the number of random seeds/trials; and statistical significance of the claimed crossover between "keep easy" and "keep hard" at different data scales. The error rate range reported (0–50%) does not clearly correspond to standard ImageNet top-1 or top-5 metrics. Without these details the results cannot be interpreted as validation of the theory. (Impact: -7.1)

- **The LLM reconciliation (Section 4.2) is post-hoc narrative rather than evidence.** Tables 1 and 2 are direct citations from prior work, and the paper labels the generator as "strong" for average AIME performance and "weak" for hard AIME questions based purely on the outcomes being explained. There is no independent measurement of ρ (or a proxy) for an LLM on these problem sets, no quantitative prediction verified, and no comparison between the theory's predictions and the observed numbers. The abstract's claim that the paper "provides a principled explanation for the contradictory curation strategies recently observed in LLM mathematical reasoning" overstates what this section supports — the section provides a plausible post-hoc interpretation, not a principled explanation derived from the theory. (Impact: -9.3)

### Minor

- **The synthetic validation conflates generator and oracle quality.** Section 4.1 sets ρ_* = ρ for the "keep hard" strategy, tying oracle quality to generator quality. While this is a natural choice for self-training scenarios, it conflates two effects that the theory assigns distinct roles to, making it impossible to isolate the unique contribution of each. (Impact: -2.8)

- **The model collapse experiment (Figure 3) does not clarify the label source for selection.** It is unclear whether the "hard valid examples" are selected using ground-truth labels or pseudo-labels. If ground-truth labels are used for selection in the curated setting but pseudo-labels for the "all data" baseline, the comparison would be confounded. (Impact: -1.5)

- **The synthetic experiments omit the dimensionality d.** The caption of Figure 1 gives n = 100 or n = 5000 but does not report d (or equivalently φ = d/n), making the simulations unreproducible. (Impact: -4.0)

- **The role of the parameter τ is unexplained in the main text.** τ = ρ_g / √(1-ρ_*²) is defined in Eqn (7) and appears in the constants β and β̃ (Eqn 8) via φ(τG) and Φ(τG), but how τ affects the key results remains unclear without consulting the appendix. (Impact: -0.0)

## Nice-to-Haves

- Quantify an empirical proxy for ρ on actual LLM outputs (e.g., agreement rate with ground truth on a held-out set) and compare the observed crossover with the theory's prediction. Even a rough calibration would transform Section 4.2 from narrative to evidence.
- Extend Theorem 2 to characterize what happens when ρ* < 1 (finite pruner quality), even if the result is a bound or a conjecture rather than an exact formula.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Theorem 1 is a black box with proofs deferred to appendix.* Removed per policy: the parser strips appendix content from all papers; the original submission contains these proofs.
- *The "random" baseline (ρ_* = ρ_g = 0) is "actively misaligned" rather than properly random.* Removed as factually incorrect — an orthogonal pruner with ρ_* = 0 yields selection uncorrelated with the task, which is exactly a model of random selection.
- *Model collapse analysis lacks connection to one-shot theory.* Removed per appendix rule.
- Various formatting/style nitpicks and generic concerns. Removed.

## Novel Insights

None beyond the paper's own contributions. The most noteworthy observation arising from cross-review is that the paper's main limitation (Theorem 2 covers only ρ* → 1) mirrors a common pattern in theoretical ML: the cleanest results hold at the boundary cases, and the messy middle (both generator and pruner imperfect) is where the most practical value lies.

## Suggestions

1. Provide complete experimental details for ImageNet (architecture, difficulty operationalization, pseudo-label generation protocol, number of runs, standard deviations) so these results can be evaluated.
2. Add an independent measurement of ρ (or a proxy) for the LLM setting to move Section 4.2 from post-hoc narrative to evidence.
3. Report the dimensionality d (or φ) in the synthetic experiments.
4. Clarify the label source used for selection in the model collapse experiment.
5. Discuss how the optimal pruning strategy changes for finite φ, λ (away from the asymptotic limits assumed in Theorem 2).

---

## Score and Decision

The paper has a genuinely interesting core theoretical idea and compelling motivation. However, the empirical validation is substantially underspecified (ImageNet) or post-hoc (LLM), and the central qualitative result (Theorem 2) is proven only in a regime (ρ* → 1, φ → 0, λ → 0) that does not cover the realistic settings the paper claims to explain. The gap between what the paper claims (empirical validation, principled explanation) and what it demonstrates is too large for acceptance in its current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>