Now let me finalize my calibration and produce the final review.

**Calibration Summary**

**Round 1 bracket:** 5.5–7.5 (the paper has a genuine theoretical contribution and strong empirical results, but the ablation pathology and framing issues prevent it from being a strong accept or a clear reject).

**Anchors examined:**

| Paper | Avg Score | Decision | Comparison |
|-------|-----------|----------|------------|
| Q2bJ2qgcP1 — CATE Benchmark (16 models, 43,200 datasets) | 6.00 | Accept | Less methodologically novel than the reviewed paper; had overclaiming concerns similar in severity to the ablation issue here |
| yuy6cGt3KL — Model Selection for CATE | 7.25 | Accept | More comprehensive empirical analysis (78 datasets, 34 metrics); the reviewed paper's theoretical contribution is stronger but the ablation pathology is a more significant weakness |
| QGGNvKaoIU — Meta-learners for HTE over time | 7.00 | Accept | Clean, well-received paper with minor weaknesses; the reviewed paper has a larger unresolved issue (ablation pathology) |
| TC9r8gsaoh — Nuisance-Robust Weighting Network | 6.00 | Reject | Most methodologically similar anchor; rejected due to missing related work and clarity issues. The reviewed paper is better written and has clearer contributions |
| S46Knicu56 — Variational Framework for Continuous Treatments | 7.33 | Accept | Well-written with clear motivation; the reviewed paper has comparable clarity but a more significant methodological concern |
| glgvpS1dD1 — Robust HTE under Covariate Perturbation | 4.50 | Reject | Seen as incremental; the reviewed paper is more novel theoretically |

**Final narrowing:** The ablation pathology (L_wls+L_ce producing √ePEHE=3.495 while TARNet gets 0.896, with the paper incorrectly claiming equivalence) is a real concern that prevents a score above 7. However, the core method works well, the theory is principled, and the contributions are genuine — this is above the 6.0 anchor papers in novelty and clarity. This places the paper at **6.5**.

---

## Summary

This paper proposes a robust evaluation framework for heterogeneous treatment effect (HTE) estimators using relative error. Building on Gao (2025), the authors design novel loss functions (weighted least squares + balance regularizer) embedded in a Dragonnet-inspired neural network so that the relative error estimator is √n-consistent and asymptotically normal *even when the outcome regression model is misspecified* — only requiring correct propensity score specification. The method is extended to HTE learning via aggregation over candidate estimator pairs. Experiments on IHDP and Twins demonstrate strong empirical performance.

## Strengths

1. **Well-motivated theoretical advance.** The paper identifies a genuine limitation of Gao (2025) — requiring Condition 2 (product of outcome regression and propensity score errors o_p(n^{-1/2})). It then shows that by carefully designing loss functions, one can relax this to only require correct propensity score specification while allowing outcome models to be misspecified (Theorem 1). The derivation via Taylor expansion (Eq. 3–4) is clean and principled.

2. **Clever loss function design.** The weighted least squares loss L_wls (Section 4.2) is elegantly constructed so that its first-order conditions correspond to the key condition in Eq. (4). The balance regularizer L_const that enforces the remaining constraints via a soft-margin formulation is novel and well-motivated by the over-constrained nature of the optimization problem.

3. **Strong empirical performance on HTE estimation.** In Table 1, the proposed method substantially outperforms all 11 baselines on both IHDP and Twins across all metrics (√ePEHE and ε_ATE, both in-sample and out-of-sample). Coverage rates are at or near the nominal 90% level (Figure 1), and selection accuracy is high (0.80–0.94 in Table 2).

4. **Extension to HTE learning is natural and useful.** The aggregation strategy over pairs of candidate estimators (Section 5) is simple but effective, producing an HTE estimator that outperforms individual candidates.

## Weaknesses

### Major

1. **The ablation study reveals unexplained pathological behavior and the paper mischaracterizes it.** Removing L_const (training with only L_wls + L_ce) yields √ePEHE = 3.495 on IHDP — more than 5× worse than the full model (0.638), and far worse than even the weakest baseline in Table 1 (LinDML at 1.053). The paper claims this variant "can be seen as a method of Gao (2025), where the proposed neural network degenerates to TARNet." This is factually incorrect: TARNet itself achieves √ePEHE = 0.896, and L_wls is a fundamentally different loss from standard MSE. The paper offers no explanation for why L_wls alone is so destructive. This suggests the method's success depends on a delicate interplay between loss terms that is not well understood.

2. **The "relaxation" framing is asymmetric and somewhat oversold.** Gao (2025) requires both propensity score and outcome regression to be consistent (at a product rate). The proposed method replaces this with: (i) correct specification of the propensity score model (logistic in Φ(X)), (ii) a parametric working model for outcome regression (linear in Φ(X)), and (iii) a shared representation Φ(X) learned from data. This is a *different* trade-off rather than a strict relaxation — Gao's approach allows any flexible outcome estimator as long as it converges fast enough, whereas the proposed method constrains the outcome regression to a specific parametric form. While the paper is transparent about its working models (Eq. 1–2), the title and framing should more carefully acknowledge this asymmetry.

3. **The n^{-1/4} convergence condition for neural network nuisance estimators is asserted too casually.** Theorem 1 requires γ̂, β̂₀, β̂₁ to converge faster than n^{-1/4}. The paper states this is "readily satisfied" because parameters converge to their probability limits. However, convergence rates for neural networks are not automatically n^{-1/4} without additional regularity conditions (smoothness, network complexity control, etc.). The cited references (Chernozhukov et al., 2018; Semenova & Chernozhukov, 2021) typically rely on specific estimators with known rates. This claim needs more careful justification.

### Minor

4. **Relative error evaluation figures lack direct baselines.** Figures 1 and 2 show coverage and selection accuracy for the proposed method across estimator pairs, but include no comparison to alternative relative error estimators. Table 2 gives some comparison (linear regression, boosting) in tabular form, but the figures would be far more informative if they visualized these baselines. As presented, a reader can only see that the proposed method's coverage is near nominal, not how it compares to alternatives.

5. **The soft relaxation creates a theory-practice gap that should be stated more prominently.** The over-constrained system (2d constraints for d parameters) is solved via soft relaxation with slack variables. Theorem 1 and Proposition 2 assume Eq. (3) holds (i.e., the probability limits satisfy the constraints), but the soft relaxation only encourages, not guarantees, this. The paper points to Appendix F.4 for empirical validation, but the caveat should appear in the main text alongside the theorem.

6. **No direct implementation-level comparison with Gao (2025).** The "Comparison with Gao's Method" section uses linear regression and boosting as nuisance estimators plugged into the relative error formula, which the paper acknowledges is not Gao's full procedure. A reader cannot determine how the proposed method compares to a faithful implementation of Gao's method (with sample splitting and potentially better nuisance estimation).

### Trivial

7. **Table 3 formatting is ambiguous.** The row "TARNet / 2.0306" appears under the "# Candidate Est." column, making it unclear whether this is TARNet's runtime for comparison or a mislabeled entry. The text says "our method remains faster than the baseline TARNet" but the formatting is confusing.

## Nice-to-Haves

- Design an experiment where the outcome regression is deliberately misspecified (e.g., overly simple outcome heads) while the propensity score is correct, to directly test the paper's core claim that outcome model misspecification is tolerated.
- Include baseline methods in Figures 1–2 for a direct visual comparison of coverage and selection accuracy.
- Analyze the effect of random subset selection of estimator pairs when K is large (currently one sentence).
- Investigate the non-convexity of L_wls (the weighting by τ̂₁ − τ̂₂ can be negative) and its implications for optimization.

## Removed Points

- "Running time comparison issues with TARNet": Likely a parser formatting artifact; the original submission likely formatted this differently.
- "L_wls weighting when estimators agree is problematic": Speculative; the method compares estimators where differences are meaningful.
- "Sensitivity analysis characterization is too optimistic": Subjective judgment; the paper reports raw numbers transparently.
- "Jobs results deferred to appendix": Standard space management; not a weakness.
- "Missing related works": Cannot verify without external sources.

## Novel Insights

The harsh critic insightfully connects the ablation pathology (L_wls alone being catastrophic) with the core theoretical claim: this suggests that L_wls, as designed, is not independently a sensible loss for outcome regression — it only produces reasonable results when balanced by L_const. This implies the method's robustness does not cleanly decompose into "L_wls handles outcome misspecification + L_const handles propensity constraints" but rather these components interact in a way that is not explained by the current theoretical analysis. The fact that L_wls weights residuals by (τ̂₁ − τ̂₂), which can be negative, means the loss is not a conventional MSE and may have pathological stationary points that are only corrected by the balance regularizer. This observation goes beyond the paper's own narrative and points toward a deeper understanding that could strengthen the work.

## Suggestions

1. **Explain the catastrophic L_wls+L_ce result in detail.** Provide intuition for why this variant fails so badly, and correct the inaccurate claim that it "degenerates to TARNet."
2. **Reframe the contribution more precisely** as trading off outcome model flexibility (Gao's approach) for robustness to outcome model misspecification, rather than a strict "relaxation."
3. **Add baseline methods to Figures 1–2.** Include linear regression and boosting-based relative error estimates directly in the coverage/selection accuracy figures.
4. **Provide a more careful justification** for the n^{-1/4} convergence rate in the neural network setting, including any additional regularity conditions needed.
5. **Add a caveat in Section 4.2's main text** acknowledging the theory-practice gap from the soft relaxation.
6. **Investigate the optimization landscape of L_wls** — since the weighting by (τ̂₁ − τ̂₂) can be negative, the loss is not a conventional convex MSE and this may explain the pathological ablation behavior.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>