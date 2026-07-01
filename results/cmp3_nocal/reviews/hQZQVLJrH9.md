## Summary

This paper proves a first-order equivalence between activation steering (adding vectors to intermediate layers) and influence functions (tracing output changes to training data re-weighting). It develops the Influence-Aligned Steering (IAS) construction, an alignment diagnostic γ(x) that certifies when steering can match influence, a no-free-lunch bound for when it cannot, and a spectral optimality result. The paper is predominantly a theoretical contribution with illustrative experiments on GPT-2 Medium (detoxification) and ResNet-50 (spectral direction).

## Strengths

1. **The core theoretical duality is novel and cleanly formalized.** The primal–dual formulation (Section 3) connecting activation-space and parameter-space sensitivities, and the proof that steering vectors and influence functions are first-order projections of the same geometric structure, is a genuine contribution. The exposition from the primal program (P) through the chain-rule factorization to the equivalence theorem (Thm. 4.2) is mathematically sound and well-motivated.

2. **The alignment diagnostic γ(x) and the no-free-lunch theorem (Thm. 6.2) yield crisp, actionable geometry.** The cosine of the smallest principal angle between two Jacobian subspaces provides a single scalar that certifies feasibility, and the bound √(1−γ²) on irreducible error is the kind of result that could inform practitioners' decisions. Computing γ costs "two small SVDs" (line 154), which is plausible and cheap.

3. **The spectral optimality result (Thm. 5.3) offers a principled alternative to hand-crafted steering directions.** Maximizing expected first-order logit change under an ℓ₂ budget via the leading eigenvector of Σ is theoretically well-grounded and provides a clear recipe (lines 174–178) that goes beyond minimum-norm heuristics.

## Weaknesses

### Major

1. **The headline data-attribution claim (Corollary 1) has zero empirical validation.** The abstract promises "a constructive algorithm for mapping undesired behaviors back to causal training examples." Corollary 1 provides the theoretical construction — the ℓ₁-minimal signed measure ρ_s that connects a steering vector to training examples — and the text directs readers to "Section 7" (line 130) for validation. However, Section 7 contains no data-attribution experiments whatsoever: no human evaluation, no ground-truth comparison (e.g., training with known spurious correlations and checking whether ρ_s identifies corrupted examples), no ablation, no case study. For a contribution marketed as a primary deliverable in the abstract and introduction, this absence is a structural gap that severs the paper's practical promise from its evidence.

2. **The linearity experiment reveals a systematic 50% deviation that the paper does not explain.** Figure 1 reports a cosine of 0.978 (strong linear correlation) but a slope of 1.50, meaning the actual logit shift is consistently 50% larger than the first-order prediction. The paper's characterization that this is "consistent with the expected linear regime" (line 239) is misleading — a slope of 1.50 indicates that second-order terms are large and directional, not noise around the identity line. If the first-order approximation systematically under-predicts by 50%, every downstream claim relying on its accuracy (the IAS construction, the influence equivalence, the alignment bounds) operates in a regime where approximation error is systematic and nontrivial. The paper should analyze the sources of this discrepancy (Hessian-Jacobian interactions, nonlinear activation functions, numerical error in the pseudoinverse) or at minimum acknowledge that the theory captures direction but not magnitude.

3. **The proposed method (IAS) underperforms the existing baseline (CAA) on every metric without discussion.** Table 1 shows IAS achieving higher toxicity (0.0164 vs 0.0150) and higher perplexity (13701 vs 13291) than CAA — strictly worse on both objectives. For a paper whose contributions include a "constructive algorithm" and a "practical workflow," this underperformance demands explanation. The paper does not analyze whether CAA operates in a regime where the linear approximation is more favorable, whether the Hessian damping λ was tuned differently, or whether IAS's minimum-norm property is actually suboptimal for detoxification. This omission leaves readers uncertain about when IAS should be preferred over existing methods.

### Minor

4. **No variance or uncertainty estimates are reported.** Table 1 reports single numbers for toxicity and perplexity with no indication of variability across seeds, train/test splits, or prompt sampling. Given the evaluation set is only 500 prompts, standard deviations or confidence intervals are essential for interpreting the CAA vs. IAS comparison.

5. **Experimental scope is narrow for the breadth of claims.** All language experiments use one model (GPT-2 Medium), one layer (ℓ=8) for the main steering comparison, one task (detoxification), and one steering construction dataset (50 toxic + 50 neutral prompts). The spectral direction (Theorem 5.3) is evaluated only on ImageNet as a significance test (Fig. 3), never on an actual steering task like detoxification, so its practical utility relative to simpler baselines (CAA, PCA-based directions) remains unknown.

6. **The cost model slightly understates computational requirements.** Line 56 claims "all results rely on" two Jacobian-vector products and a rank-d pseudoinverse. However, the spectral optimality construction (Theorem 5.3) and the influence-function computation require access to (H+λI)⁻¹, which for billion-parameter models typically needs conjugate-gradient or Neumann-series approximation. The conclusion acknowledges this (line 277), but the caveat appears too late and is absent from the cost model where it would be most relevant.

### Trivial

7. Corollary 2's Lipschitz constant κ on the map θ ↦ (J_(θ→y), J_(θ→h)) is never estimated or bounded in experiments. This does not affect the theory's correctness but limits the practical applicability of the second-order radius guarantee.

## Nice-to-Haves
- An ablation of the Hessian damping parameter λ showing sensitivity of the spectral direction and IAS to this hyperparameter.
- Validation of the composability result (Lemma 5.4) through a multi-layer steering experiment.
- A comparison of the spectral direction against CAA on the same detoxification task used in Section 7.1.
- A discussion of where the first-order (infinitesimal) regime ends and the finite-edit regime begins, situating IAS relative to ROME/MEMIT-style parameter editing.

## Removed Points
These points are flagged to be removed; treat them with caution:
- *"The citation on line 92 is disconnected and misplaced"* — Factually incorrect: Section 4 is titled "Steering–Influence Duality at the Data Level," so a citation about data-attribution methods is in-scope.
- *"Minimum-norm may not be the right objective for steering"* — Speculative; the paper makes a principled theoretical choice, and the question of task-specific optimality is partially addressed through the spectral construction (Thm. 5.3). The spectral direction was designed for exactly this concern.
- *"Lemma 5.4 composability has no experimental validation"* — This is a theoretical inequality derived from the geometry; requesting experimental validation of every lemma goes beyond standard expectation.
- *Several generic strength statements* (e.g., "addressed an important problem") removed as lacking specific evidence.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Validate the data-attribution claim** with at least one experiment. A straightforward setup: train on a dataset with known spurious correlations, steer to suppress the spurious behavior, and check whether ρ_s identifies the corrupted training examples.
2. **Investigate and explain the slope of 1.50** in Figure 1. If the first-order theory systematically under-predicts by 50%, characterize when this occurs and whether it affects the practical utility of IAS. At minimum, acknowledge the discrepancy honestly.
3. **Add standard deviations or confidence intervals** to all reported metrics in Table 1.
4. **Consider reframing** the paper as primarily a theoretical contribution with illustrative experiments, or substantially expand the experimental validation to support the practical workflow claims.

## Score and Decision

The paper's core theoretical contribution — the first-order unification of activation steering and influence functions, the alignment diagnostic γ, and the no-free-lunch result — is genuinely novel, well-formalized, and clearly presented. This alone constitutes a meaningful addition to the interpretability literature.

However, the experimental evaluation falls short of supporting the paper's broader practical claims. The proposed method (IAS) underperforms the existing baseline (CAA) without explanation. The headline data-attribution claim is never empirically validated. The linearity experiment reveals a systematic 50% magnitude discrepancy that the paper does not address. These gaps prevent the paper from being a clear accept, but they do not invalidate the theory.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept (borderline)</decision>