Since the calibration search is unavailable, I'll proceed with my expert judgment based on careful reading of the paper, verification of all claims, and the ICLR scoring guidelines. Let me finalize my review.

---

## Summary

This paper studies language model pre-training under fixed data and unlimited compute — motivated by the fact that compute grows ~4×/year while web text grows ~1.03×/year. It shows that standard data-constrained recipes (epoching + parameter scaling) overfit, and improves upon them by tuning weight decay to be ~30× larger than standard practice, enabling monotone power-law scaling. The paper proposes evaluation by the *asymptote* of scaling laws rather than at fixed compute budgets, shows that ensembling multiple models achieves a lower asymptote than scaling a single model, and demonstrates that distillation preserves most of these gains in smaller models.

## Strengths

- **Optimal weight decay discovery (30× larger than standard practice):** Section 3 and Figure 3 show that the regularized recipe requires weight decay values of 0.8–3.2 (models 150M–1.4B) compared to the standard 0.1 from Brown et al. (2020). This is a concrete, reproducible finding backed by an extensive coordinate-descent hyperparameter search, and it directly enables the paper's central claim of monotone power-law scaling under data constraints.

- **Ensembling beats parameter scaling at matched total parameter count:** Section 4.2 and Figure 4 show that a K=3 ensemble of 300M models (900M total params, asymptote 3.34) outperforms the regularized recipe's infinite-parameter asymptote of 3.43. This contradicts the prior expectation that parameter scaling dominates ensembling and is the basis for the best combined recipe.

- **Asymptote-based evaluation framework:** Sections 1 and 3 propose evaluating recipes by computing $\lim_{N\to\infty} \hat{\mathcal{L}}_{D,N}$ (the scaling law asymptote) rather than at fixed compute budgets. This differs from prior scaling-law work focused on compute-optimal points and directly addresses the paper's motivating scenario of unlimited compute with fixed data.

- **Ensemble distillation retains 83% of gains in an 8× smaller model:** Section 6.1 shows that distilling an 8-ensemble teacher (300M members) into a 300M student achieves loss 3.36, preserving 83% of the ensembling improvement over the regularized 300M baseline (loss 3.57). This demonstrates that the asymptotic gains can be realized at practical inference costs.

- **Self-distillation improves over the teacher despite literature on model collapse:** Section 6.2 shows that self-distilling a 300M model into a same-size student (mixing real and synthetic tokens) matches the regularized recipe's asymptote of 3.43, contrary to recent results (Shumailov et al., 2024) finding collapse from training on self-generated data.

- **Downstream benchmark validation with held-out evaluations:** Section 7 reports that the best ensemble outperforms the best unregularized model by 9% on average over PIQA, SciQ, and ARC Easy. Since evaluations were held out until after recipe selection (lines 230–233), this provides strong evidence that validation-loss improvements are not artifacts.

## Weaknesses

### Fatal
None.

### Major

- **The joint scaling recipe's headline result rests on an unvalidated heuristic (Section 4.3).** The paper's strongest quantitative claim — 5.17× data efficiency and asymptote loss 3.17 for the joint scaling recipe (ensembling + parameter scaling combined) — depends on a double limit ($K \to \infty$, then $N \to \infty$). For the inner limit, the paper states explicitly (line 143): *"we cannot fully find locally optimal hyperparameters due to experimental constraints. Instead, we use the heuristic of taking the optimal regularized hyperparameters with 2× epochs and 0.5× weight decay."* The entire regularized recipe's success in Section 3 is predicated on the finding that hyperparameters must be jointly and carefully tuned at each scale — yet the joint scaling regime uses an untested heuristic. Without evidence that this heuristic is close to optimal (or even monotonic in the right direction), the 5.17× figure and 3.17 asymptote have significant unquantified uncertainty.

- **Data scaling laws are fitted from 4 data points with 3 free parameters (Section 5).** The data scaling laws in Section 5 (Figures 6, 7) are fitted across four token budgets (200M, 400M, 800M, 1.6B) using the form $\hat{\mathcal{L}}_D = A/D^\alpha + E$. With 4 data points and 3 parameters, the fit has one degree of freedom, making it impossible to assess goodness of fit or validate against held-out data. The paper's claim that *"improvements persist at higher token budgets"* relies on these fits. No confidence intervals, leave-one-out analysis, or other robustness checks are provided for these specific fits (the sensitivity analysis in Appendix I.1 concerns a different set of fits — the parameter scaling law asymptotes). The paper acknowledges these laws are "expected to be noisy" (line 195), but the evidence is thinner than the confidence of the claim suggests.

### Minor

- **Headline data efficiency number mixes asymptotic and finite-model quantities.** The 5.17× figure compares the joint scaling recipe's *asymptote* (as $N, K \to \infty$) against the standard recipe's *finite best-model curve*. The paper does hedge by also reporting the finite-model result of 3.75× at 1.4B with five members (line 185–186), and states "Without using asymptotes" alongside. However, the abstract and Figure 1 feature the asymptotic number more prominently, and readers may come away believing 5.17× is achievable at practical model scales.

- **Downstream evaluation is limited to 3 benchmarks.** Only PIQA, SciQ, and ARC Easy are evaluated (Section 7). While the paper justifies this by model scale and cites Thrush et al. (2025), evaluations on additional benchmarks (e.g., HellaSwag, WinoGrande) at the larger scales tested would strengthen the generalization claims.

### Trivial
None.

## Nice-to-Haves

1. Validate the joint scaling heuristic with a partial hyperparameter search at one representative $(N, K)$ point (e.g., N=600M, K=4) and characterize the gap from the heuristic.
2. Add leave-one-out or bootstrap analysis for the data scaling law fits in Section 5 to show their stability.
3. Clarify in the abstract and key figures that the 5.17× figure is an *asymptotic estimate* requiring $N, K \to \infty$, alongside the practical 3.75× figure.
4. Discuss the compute cost of the coordinate-descent hyperparameter search relative to the training runs themselves.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"No comparison with synthetic data methods"** (from Harsh Critic's "Missing Parts") — This is scope creep. The paper studies a different axis (regularization + ensembling vs. data augmentation). The Related Work section (Section 8) already cites these methods and situates the paper as distinct from them.
2. **"Standard recipe baseline could be stronger"** — The paper's core finding is that weight decay must be 30× higher than standard; using the de facto standard value (0.1, from Brown et al. 2020) as a baseline is the correct experimental design. The regularized recipe already explores the full tuning space, making the comparison internally consistent.
3. **"Compute cost of coordinate descent tuning not discussed"** (from Harsh Critic's "Missing Parts") — Moved to Nice-to-Haves. Under the paper's premise of "no compute constraints," this is a minor omission at most.
4. **"Only 4 parameter counts for the parameter scaling law"** — This is a complaint about a similar issue (4 points, 3 parameters) that is subsumed by the data scaling law analysis above; not a separate weakness.
5. **Various presentation/formatting nitpicks** (from both inputs) — Removed as parser artifacts or scope concerns per filtering rules.
6. **Generic strengths** from Strength Finder that were not anchored to specific content (e.g., "addressed an important problem", "well-motivated") — Removed as superficial. Only strengths with concrete evidence are retained.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run a targeted validation experiment for the joint scaling heuristic at one representative $(N, K)$ point to bound its suboptimality. Even a partial search would substantially increase confidence in the 5.17× claim.
2. Add leave-one-out cross-validation or bootstrap uncertainty estimates for the data scaling law fits in Section 5.
3. In the abstract and Figure 1, label the 5.17× more prominently as an *asymptotic* estimate (requiring $N, K \to \infty$) and juxtapose with the finite result (3.75× at 1.4B, five members).
4. Consider adding 1–2 additional downstream benchmarks at the largest model scale tested.

## Score and Decision

The paper has genuine contributions: the 30× weight decay finding is concrete and practically useful; the asymptote evaluation framework is a novel conceptual contribution; the ensembling-over-parameter-scaling result is surprising and well-demonstrated; the distillation results are robust and independent of the asymptotic extrapolations. The writing is clear, the motivation is compelling, and the experimental setup is well-controlled.

However, the paper's headline claim (5.17× data efficiency) rests on significantly weaker evidence than the rest of the paper — an unvalidated hyperparameter heuristic and data scaling laws fitted from essentially irreducible data (4 points, 3 parameters). These are real evidential gaps, but they are not fatal to the paper's core contributions (weight decay, asymptote framework, ensembling, distillation). The paper would benefit from addressing these gaps but is publishable as-is given the strength of its other contributions.

Based on the ICLR scoring scale, this paper sits in the borderline-accept to accept range. It has clear contributions that outweigh its weaknesses, but the most ambitious claim requires additional validation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>