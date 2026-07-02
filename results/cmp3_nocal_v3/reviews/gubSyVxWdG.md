Now let me produce the final consolidated review.

## Summary

This paper proposes a robust evaluation framework for heterogeneous treatment effect (HTE) estimators, building on the relative error framework of Gao (2025). The key contribution is a relative error estimator that remains √n-consistent and asymptotically normal even when the outcome regression model is misspecified, as long as the propensity score model is correctly specified at a rate faster than n^{-1/4}. This is achieved by deriving orthogonality conditions (Eq. 4), designing a weighted least squares loss (L_wls) and a balance regularizer (L_const) that enforce these conditions, and embedding them in a Dragonnet-inspired neural architecture. The paper also presents an HTE learning extension that averages outcome regression models over pairs of candidate estimators.

## Strengths

- **Well-motivated theoretical contribution targeting a genuine limitation of prior work.** The paper identifies that Gao (2025)'s relative error estimator requires both propensity score and outcome models to be consistent at better than n^{-1/4} (Condition 2), and correctly argues that outcome regression models are especially prone to misspecification because they are trained within one treatment arm and must extrapolate to the other arm, while propensity score models are trained on the full dataset. This asymmetry is a real, well-articulated weakness of the existing approach.

- **Principled derivation of robustness conditions (Section 4.1–4.2).** The paper derives the conditions (Eq. 4) under which the relative error estimator remains √n-consistent even with a misspecified outcome model. The weighted least squares loss L_wls is designed so that its population-level gradient directly satisfies the first condition in Eq. (4). Theorem 1 formalizes the guarantee, and Proposition 2 provides valid confidence intervals under the relaxed conditions. The theoretical development is clean and grounded.

- **Consistent and substantial empirical gains on the evaluation metrics.** On both IHDP and Twins, the proposed method achieves coverage rates close to the nominal 90% level (Figure 1) and substantially higher selection accuracy than the baselines (Table 2: 0.80 vs. 0.44/0.48 on IHDP, 0.94 vs. 0.88/0.86 on Twins). The ablation study (Table 5) confirms that the constraint loss L_const is essential: removing it causes selection accuracy to drop from 0.80 to 0.14 on IHDP.

- **Sensitivity analysis on propensity score misspecification (Table 6).** The paper explicitly tests robustness to perturbed propensity scores, showing that while performance degrades with increasing noise, the degradation is gradual rather than catastrophic. This strengthens confidence that the method's reliance on propensity score correctness is practically manageable.

## Weaknesses

### Major

- **The HTE learning extension (Section 5) lacks theoretical grounding, and its empirical evaluation does not fully isolate the source of improvement.** The paper states that the aggregation estimator "performs exceptionally well, even surpassing the performance of any single candidate estimator" and describes this as "Surprisingly" (line 228). There is no theoretical analysis of why averaging pairwise outcome regression models should produce a strong HTE estimator — if all candidate estimators are poor, it is unclear why averaging them would help. Moreover, the ablation study (Table 5) varies only the loss components (L_wls, L_ce, L_const) while keeping the aggregation strategy fixed. It does not test whether the aggregation strategy *alone* (applied with standard losses, e.g., standard Dragonnet or TARNet) improves HTE estimation. As a result, the empirical comparison in Table 1 conflates the effect of the novel loss functions with the effect of the aggregation strategy. The paper acknowledges this limitation in the conclusion ("A remaining limitation is our use of a simple uniform averaging scheme"), but this acknowledgment does not resolve the lack of isolation in the experimental design.

### Minor

- **The asymptotic theory assumes Φ(X) is fixed, but it is learned adaptively from data.** The working models (Eqs. 1–2) posit logistic regression on Φ(X) for the propensity score and linear regression on Φ(X) for outcomes. Theorem 1 requires the propensity score model to be correctly specified, meaning the logistic model on Φ(X) equals the true e(X). However, Φ(X) is "a representation of X adaptively learned from data" (line 110). The theoretical analysis does not incorporate the uncertainty or bias from representation learning — it treats Φ as known/fixed. The paper partially addresses this by noting that a flexible neural network can approximate the true propensity score and by providing sensitivity analyses (Table 6, Appendix F.3), but this is a gap between the formal guarantees and the implemented algorithm. Readers attentive to this gap will reasonably question whether Theorem 1's conditions apply to the actual procedure run.

- **No discussion of the trade-offs of avoiding sample splitting.** The paper emphasizes that unlike Gao (2025), the proposed method "does not require sample splitting" (lines 28, 214), framing this as an advantage. However, cross-fitting exists precisely to break the dependence between nuisance estimation and the evaluation statistic, enabling valid inference under weaker conditions. The paper does not discuss whether using the full dataset creates any risk of overfitting bias that sample splitting would mitigate, nor does it justify why the theoretical framework avoids this concern. This is a missing nuance in an otherwise carefully motivated paper.

- **Large standard deviations relative to reported differences (Table 1).** For instance, on IHDP, the proposed method's √e_PEHE_in is 0.638 ± 0.138 vs. DCFR at 0.741 ± 0.068. The standard deviations are large enough that a paired significance test would help establish whether improvements are statistically reliable, especially given the modest sample size (747 for IHDP).

### Trivial

- None.

## Nice-to-Haves

- Include the Jobs dataset results in the main paper rather than the appendix to broaden the empirical scope.
- Provide more algebraic detail showing how the first-order condition of L_wls yields the first term in Eq. (4) (currently one sentence at line 156).
- Report paired significance tests or confidence intervals for the HTE estimation results in Table 1.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper, per the filtering rules specified:

- **"The relative error evaluation baselines (Table 2) are not properly matched"** — Removed. The paper's primary comparison (Table 2) is against the standard implementation of Gao (2025) using off-the-shelf nuisance estimators (linear regression, gradient boosting), which is the correct baseline. The ablation study (Table 5, "L_wls & L_ce" row) provides the matched neural-network comparison. This particular row shows *worse* performance (coverage 0.88, selection 0.14) than the off-the-shelf baselines (coverage 0.94, selection 0.44–0.48), so the comparison in Table 2 is actually conservative, not unfair. The paper's narrative already covers this by saying "the method (L_wls & L_ce) can be seen as a method of (Gao, 2025)" and noting that the gap is large.

- **"Section 3 formula appears to have a typo (line 78)"** — Removed. This is a parser formatting artifact where τ(Xᵢ) was rendered as τ̂(Xᵢ); the original PDF does not have this issue.

- **"Section 4.2, line 156 deserves more explanation"** — Removed. This is a minor presentation preference, not a substantive weakness.

- **"Section 4.2, lines 158–180: relaxation means Eq. (3) only approximately satisfied"** — Removed. The paper acknowledges this ("effective in practice") and Appendix F.4 addresses it empirically. The concern is noted but does not rise to the level of a weakness given the empirical validation.

- **"Table 1 / 3 / 5 / 6 column formatting"** — Removed. These are parser-induced formatting artifacts.

- **"Jobs dataset in appendix"** — Removed. This is a presentation preference, not a weakness.

- **"Section 5 computational cost clarification needed"** — Removed. This is a request for clarification, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Provide theoretical analysis or a clear rationale for the HTE aggregation strategy**, or reframe it explicitly as a heuristic extension (which the conclusion already partially does). Add an ablation that applies the aggregation strategy to standard Dragonnet/TARNet (without the proposed losses) to isolate the effect of aggregation from the effect of the novel loss functions.
2. **Acknowledge the Φ-learning gap more explicitly in the theory section.** Either state that Theorem 1 assumes Φ is fixed/known and that additional analysis is needed for the adaptive case, or provide a sketch showing why the convergence rate of representation learning does not affect the asymptotic guarantees.
3. **Add a brief discussion of why sample splitting is unnecessary under the proposed framework,** addressing the potential overfitting risk that cross-fitting guards against. Even a paragraph acknowledging the trade-off would sharpen the paper.
4. **Report paired statistical tests** (e.g., paired t-tests or bootstrap confidence intervals) for the main HTE estimation results where standard deviations are large relative to differences.

## Score and Decision

This paper makes a genuine theoretical contribution — a relative error estimator robust to outcome model misspecification — that is well-motivated, rigorously derived, and convincingly validated on the evaluation metrics (coverage and selection accuracy). The core evaluation framework is a solid piece of work.

The primary weakness is that the HTE learning extension in Section 5 is presented with no theoretical justification, and its empirical evaluation does not fully separate the effect of the novel loss functions from the effect of the aggregation strategy. However, this extension is secondary to the paper's main contribution (robust evaluation). The Φ-learning gap in the theory is real but partially addressed through sensitivity analysis. Neither weakness invalidates the core claims.

With the above improvements (particularly isolating the aggregation effect empirically and being more precise about the scope of the theory), this paper would be a clear accept. In its current form, the core evaluation contribution is strong enough to warrant acceptance, provided the authors clarify the scope of the HTE learning claim and address the aggregation isolation.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>