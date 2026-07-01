Now I will produce the final consolidated review.

---

## Summary

AutoNFS proposes a differentiable neural architecture for feature selection that combines Gumbel-Sigmoid relaxation with an automatic sparsity penalty, trained end-to-end with a downstream predictor, to determine both which features to select and how many to retain. It is evaluated on tabular benchmarks with corrupted-feature scenarios and 24 real-world metagenomic datasets, and includes a complexity analysis showing near-constant time scaling with dimensionality.

## Strengths

- **Complexity analysis (Figure 4) is informative and well-executed.** The empirical demonstration that AutoNFS's wall-clock time scales with α ≈ 0.08 (near-constant) from 10² to 10⁵ features, while filter methods scale linearly or worse, is a concrete, measurable advantage. Confidence intervals over 5 runs strengthen the claim.

- **Real-world validation on 24 metagenomic datasets (Table 2) is a genuine strength.** Most FS papers stop at synthetic benchmarks; showing results on high-dimensional biological data with both MLP and RF downstream classifiers adds practical credibility, even though individual results are mixed.

- **Misselection error analysis (Figure 3a) is a clean, interpretable diagnostic.** Showing that AutoNFS perfectly recovers original features in two of three corruption scenarios, combined with the predictive power analysis (Figure 3b), goes beyond reporting only accuracy and provides direct evidence about selection quality.

## Weaknesses

### Fatal

None.

### Major

- **Missing comparison against the most directly relevant differentiable FS baselines.** The Related Work (line 36) cites Louizos et al. (2017, L₀ Hard-Concrete), Yamada et al. (2020, STG), Balin et al. (2019, Concrete Autoencoders), and Yoon et al. (2018, INVASE). None appear in the experimental comparison (Figure 2). The only neural baseline included is Deep Lasso. Because the method's core recipe — learn a per-feature mask via continuous relaxation, apply a sparsity penalty, jointly train with a predictor — closely resembles these prior works (especially STG, which uses Gaussian-based stochastic gates with a sparsity penalty), omitting them from the evaluation means a reader cannot assess whether AutoNFS improves over existing differentiable FS or is a variant with minor changes. The abstract's claim that AutoNFS "consistently outperforms both the classical and neural FS methods" is only partially evaluable from the presented evidence.

- **Unequal comparison conditions confound the results.** As stated on line 204: "all baseline methods select the same number of features as were in the initial representation (before corruption), whereas our method automatically chooses a much smaller subset." This means baselines were forced to select the original feature count (e.g., 128 for AL, 27 for HE) while AutoNFS selected far fewer (e.g., 65 and 14 respectively). Most baselines (Lasso, LassoNet, RF, XGBoost) have mechanisms to control sparsity. Fixing them at the original dimensionality rather than tuning each to its own optimal sparsity means the comparison confounds selection quality with sparsity budget. The central claim would be better supported if baselines were either (a) tuned to their own accuracy-sparsity Pareto frontier or (b) constrained to the same feature budget as AutoNFS, so the comparison isolates selection quality.

- **Method novelty relative to existing differentiable FS is untested.** The core pipeline — learn logits, apply continuous relaxation (Gumbel-Sigmoid here, Gaussian-based gates in STG), mask inputs, train jointly with a predictor and sparsity penalty — closely follows the STG framework. The claimed differentiators (a masking network $f_\phi$ mapping a learned embedding to logits, and Gumbel-Sigmoid relaxation) are neither ablated nor compared against alternatives. The paper does not show that the masking network adds value over learning per-feature logits directly, nor that Gumbel-Sigmoid yields better masks than alternative relaxations (e.g., Concrete distribution, straight-through estimator). Without such analysis, the method's incremental contribution over prior differentiable FS is not empirically established.

### Minor

- **Internal inconsistency in the loss formulation.** The main text (line 83) defines $\mathcal{L}_{select} = \frac{1}{D} \sum_{j=1}^D m_j$ (normalizing by feature count $D$), while Algorithm 1 (line 14) uses $\mathcal{L}_{select} = \frac{1}{B} \sum_{j=1}^D m_j$ (normalizing by batch size $B$). These give different penalty magnitudes, and the effective λ would scale with batch size in one formulation but not the other. The authors should clarify which was actually used.

- **Metagenomic results are more mixed than the text suggests.** The paper reports only average gains (+0.7 pp for MLP, +1.2 pp for RF) and states AutoNFS "maintains predictive performance." However, Table 2 shows several datasets with substantial degradation (e.g., KeohaneDM_2020: 0.469→0.344; ThomasAM_2018a: 0.733→0.567; YuJ_2015: 0.653→0.417; ZhuF_2020: 0.657→0.559 for MLP; HanniganGD_2017: 0.817→0.533 for RF). Acknowledging these failure cases and discussing when AutoNFS underperforms would make the reporting more balanced.

- **The "nearly constant computational overhead" claim needs qualification.** The masking network $f: \mathbb{R}^{D_e} \to \mathbb{R}^D$ has an output dimension of $D$, so even a single linear layer incurs $O(D_e D)$ operations — linear in $D$. The paper does not specify $f$'s architecture (number of layers, hidden dimensions), making the theoretical complexity unclear. The empirical α ≈ 0.08 is striking and likely reflects that the task network dominates, but the claim would benefit from a formal complexity analysis and precise specification of the masking network.

- **No ablation of Gumbel-Sigmoid vs. alternative relaxations.** The paper does not compare against other differentiable relaxations (Concrete distribution, straight-through estimator, Gaussian-based gates) nor ablate the masking network to test whether per-feature logit parameters alone would suffice.

### Trivial

- **Naming inconsistency.** The method is called "GFS-NetWork" in Figure 2 (and "GFSNetwork" in Figure 4b) while the paper is titled AutoNFS. These should be harmonized.
- **Confidence intervals are absent from the main predictive performance results** (Table 2), though they appear in the complexity analysis. Given modest average gains, variance reporting would help assess significance.

## Nice-to-Haves

- Sensitivity analysis for the hard threshold (σ(w_i) > 0.5) used during inference.
- Analysis of the temperature annealing schedule's effect on final feature count and performance.
- Standard deviations for the rank-based results in Figure 2.

## Removed Points

The following points from the input review were removed with justification:

- **Criticism about missing appendix content** (λ sensitivity analysis in Appendix F, experimental setup in Appendix C, MNIST analysis in Appendix G). The parser strips these sections from all papers; they exist in the original submission.
- **"The problem is genuinely practical"** — generic praise not specific to this paper's execution.
- **Criticism that the paper's characterization of prior work is misleading** (claiming prior methods "cannot automatically detect the number of attributes"). While STG and L₀ regularization can also let sparsity emerge from a regularization penalty, this is a scope-of-claim issue that does not undermine the paper's technical contribution and would be addressed by toning down the language.
- **Missing related work** — not included per instructions.
- **Speculative claim about "whether experiments were carried out under the name AutoNFS or GFS-NetWork"** — this extrapolation beyond what the page shows is removed. The naming inconsistency itself is retained as a Trivial issue.

## Novel Insights

The most consequential finding across the reviews is that the paper's central claim — "consistently outperforms both classical and neural FS methods" — is unsubstantiated specifically because the most relevant differentiable baselines (STG, L₀ Hard-Concrete, Concrete Autoencoders) are cited in Related Work but never compared against. This, combined with the unequal feature-budget comparison design (baselines fixed at original dimensionality vs. AutoNFS selecting fewer), means the paper's headline results do not constitute a controlled evaluation against the methods it needs to distinguish itself from. A secondary insight is that the method's incremental novelty over STG (Gumbel-Sigmoid instead of Gaussian gates, a masking network instead of direct logits) is plausible but entirely untested through ablations.

## Suggestions

1. **Add STG, L₀ Hard-Concrete (or a reimplementation), and Concrete Autoencoders** to the experimental comparison, with each method's sparsity level tuned appropriately.
2. **Fix the baseline comparison** to either match feature budgets across methods or let each method optimize its own sparsity, then report both accuracy and sparsity jointly (e.g., via Pareto curves).
3. **Ablate the masking network**: compare full AutoNFS against a version learning per-feature logits directly, and compare Gumbel-Sigmoid against the Gaussian-based gates used in STG.
4. **Resolve the L_select inconsistency** ($\frac{1}{D}$ vs. $\frac{1}{B}$) and clarify which normalization was used in experiments.
5. **Specify the masking network architecture** and provide a formal complexity analysis to substantiate the near-constant scaling claim.
6. **Discuss the metagenomic failure cases** where performance degraded substantially, to give a more balanced assessment.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>