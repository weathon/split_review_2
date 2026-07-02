Now I'll produce the final consolidated review.

## Summary

This paper develops a theoretical framework for data curation (pruning) in high-dimensional binary classification with Gaussian features, ridge regression, and squared L2 loss. The key result (Theorem 2) shows that the optimal pruning strategy flips based on generator quality: "keep hard" is optimal for strong generators (ρ→1), while "keep easy" is optimal for weak generators (ρ<1). The theory is validated with synthetic experiments matching the theoretical predictions and with ImageNet experiments, and is qualitatively connected to recent LLM reasoning results (LIMO, s1).

## Strengths

1. **Clean, well-posed theoretical setup (Section 2).** The paper defines a mathematically precise framework with Gaussian isotropic features, ridge-regularized squared L2 loss, and a proportional asymptotic limit. The key geometric quantities — generator quality (ρ), oracle quality (ρ₊), and their alignment (ρ_g) — are clearly defined as cosines of angles between linear classifiers, enabling exact analysis. This meaningfully extends prior work (Feng et al. 2025; Firdoussi et al. 2024) which only considered label-verification oracles without difficulty-based pruning.

2. **Theorem 2 is genuinely interesting and interpretable.** The result that "keep hard" is optimal for strong generators and "keep easy" is optimal for weak generators is precisely stated, non-obvious, and provides a clear theoretical anchor for understanding when aggressive pruning can outperform training on all data. This is the paper's strongest contribution.

3. **Synthetic experiments (Figure 1) show good match between theory and simulation.** The solid (theoretical) and dashed (empirical) lines agree across all four regimes of the 2×2 grid (varying ρ and n). The crossover where "less is more" appears only in the large-n, ρ=1 quadrant is consistent with Theorem 2 and demonstrates the theory works within its stated assumptions.

4. **Honest limitations section.** The paper explicitly acknowledges its core assumptions (Gaussian features, binary classification, linear predictors, isotropic covariance) and identifies specific avenues where the theory does not apply (non-linear predictors, multi-epoch optimization, active learning).

## Weaknesses

### Fatal
None.

### Major

1. **Overclaimed LLM connection.** The paper claims to provide a "principled explanation" (abstract), "rigorous justification for why methods like LIMO and s1 succeed" (line 27), and states that LIMO and s1 "are not coincidences but follow from fundamental properties of learning with pruned data" (line 281). However, the theoretical framework studies binary classification with Gaussian isotropic features, squared L2 loss, and linear ridge regression — while LLM reasoning involves autoregressive next-token prediction on natural language with cross-entropy loss and transformers. Section 4.2's "explanation" assigns generator quality ρ entirely post-hoc (the base LLM is called "strong" for average AIME problems despite 16.5% Pass@1, and "weak" for hard problems at 1.0%), meaning the "prediction" is a re-description of the observed data rather than an independent test. The theory is valuable on its own terms; these framing claims significantly overstate the strength of the connection and should be softened to "qualitative consistency" or removed.

2. **Key prediction of Theorem 2(B) — "keep easy" for weak generators — is not tested in the controlled synthetic setting.** Theorem 2 predicts that keep-easy is optimal when ρ<1, but the synthetic experiments (Section 4.1, Figure 1) only compare "keep hard" vs. "random" pruning. Keep-easy is never evaluated in the synthetic experiments. It is tested in the ImageNet experiments (Figure 2) but only in a less-controlled setting where confounds (architecture, training protocol, difficulty operationalization) are not fully specified in the main text. Since the synthetic setting is the only environment where the theory's assumptions hold exactly, the absence of a keep-easy condition means half of the paper's central theoretical prediction lacks direct controlled validation.

3. **Pruner quality not independently varied.** In the synthetic experiments, the pruner's quality is coupled to the generator's quality (ρ₊ = ρ, footnote line 183). Theorem 2's predictions assume an excellent pruner (ρ₊→1). The effect of varying pruner quality independently from generator quality is not explored, so the empirical support does not fully cover the claim's scope.

### Minor

4. **ImageNet and model collapse experiments are underspecified in the main text.** The main text (Section 4.3) does not state: the architecture used (ResNet? ViT?), whether the pre-trained model is fine-tuned or linearly probed on pseudo-labels, how "difficulty" is operationalized for images, the exact source of the 160K and 1.2M datasets, or how error bars are constructed. The model collapse experiment (Figure 3) similarly omits the base model, pseudo-labeling procedure, and dataset. While details may reside in the appendix, the main text should provide enough information to evaluate these empirical claims.

5. **Model collapse experiment lacks a proper control.** The experiment (Figure 3) compares "keep hard" curation against "training on all data from previous round," but not against random pruning at the same retention rate. This makes it unclear whether the observed stabilization is due to strategic hardness-based selection or simply to the reduced effective dataset size.

6. **No experimental comparison to Sorscher et al. (2022).** The paper builds directly on Sorscher et al.'s margin-based pruning results and uses a similar ImageNet setup, but does not quantitatively compare its empirical results to this closely related prior work.

### Trivial

7. **Finite-size analysis not discussed.** Theorem 2 is derived in the data-rich, unregularized limit (φ→0, λ→0), but the empirical crossover in Figure 1 occurs at finite n=5000 with implied φ = d/n. The paper does not discuss how the optimal strategy varies with φ or whether finite-size corrections affect the conclusions.

## Nice-to-Haves

- **Test keep-easy in the synthetic setting.** Adding a keep-easy condition to the synthetic experiments would directly validate Theorem 2(B) under the exact assumptions of the theory.
- **Vary pruner quality independently.** Decoupling ρ₊ from ρ in synthetic experiments would test whether excellent pruner quality (ρ₊→1) is necessary for the predicted effects, as Theorem 2 requires.
- **Include a random-pruning baseline in the model collapse experiment** to distinguish the effect of strategic selection from reduced dataset size.
- **Provide closed-form expressions** for at least the keep-hard and keep-easy cases if the appendix contains them — making Theorem 1 more concrete.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- *"Theorem 1 is opaque; the actual forms of m, m̃, r are deferred to the appendix"* — removed per hard rule: weaknesses about content deferred to the appendix (which is stripped by the parser) are not valid criticisms of the paper as submitted.
- *"Proof sketch for Theorem 1 does not show how the pruning indicator p_i interacts with the resolvent"* — same rationale: the full proof is in the appendix.
- *"The model collapse experiment uses only 6 rounds, which is short"* — this is a speculative judgment; 6 rounds show clear degradation, and the literature demonstrates collapse within comparable or fewer generations.
- *"The claim about 'exact scaling law curves' is technically true but the curves are expressed in terms of Stieltjes transforms deferred to the appendix"* — this is about appendix content being deferred, removed per hard rule.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the LLM connection.** Replace "principled explanation" and "rigorous justification" with "qualitative consistency" or "suggestive alignment." The theoretical result (Theorem 2) and synthetic validation are independently publishable contributions that do not need overstated LLM framing.
2. **Add keep-easy to the synthetic experiments** and independently vary ρ₊ to test the full scope of Theorem 2.
3. **Expand the main-text experimental description** for the ImageNet and model collapse experiments to include architecture, training protocol, difficulty operationalization, and dataset sources.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>