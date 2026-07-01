Now I have sufficient calibration context. Let me produce the final review.

**Calibration anchors for reference:**

| Paper | Avg Score | Round | Comparison to AutoNFS |
|-------|-----------|-------|----------------------|
| RelChaNet (neural FS, pruning+regrowth) | 5.25 | R1 | Similar domain and contribution level, but RelChaNet's method is more novel and it has fairer comparisons; AutoNFS is slightly weaker due to evaluation asymmetry |
| Feature selection w/ neural MI estimation | 2.33 | R1 | Much weaker — only 2 synthetic datasets; AutoNFS has far more extensive evaluation |
| Gumbel-Softmax MRI optimization | 3.00 | R2 | Direct Gumbel-Softmax application to a specific domain; AutoNFS has a more general method and broader experiments |
| Mambular (tabular DL) | 4.25 | R2 | Similar score range for tabular DL papers with evaluation concerns |

**Round 1 bracket:** 3.5 – 5.5 (plausible range based on comparison to RelChaNet at 5.25 and the Gumbel-Softmax MRI paper at 3.00)

**Narrowing:** AutoNFS is weaker than RelChaNet (5.25) because its evaluation has a structural asymmetry issue that RelChaNet does not, and it omits the most relevant baselines (STG, L0-reg). It is clearly stronger than the Gumbel-Softmax MRI paper (3.00) because its method is more principled and its experiments are far more extensive. The final score of **4.5** reflects a borderline-reject paper with a sound method but insufficiently supported empirical claims.

---

## Summary

AutoNFS proposes a neural feature selection method using Gumbel-Sigmoid relaxation with two trainable components: a masking network (generating a feature mask from a learned embedding) and a task network (making predictions on masked features). The method is trained end-to-end with a combined task loss and sparsity penalty that automatically determines how many features to retain. Its architecture achieves near-constant scaling with input dimensionality because the masking network's internal computation depends only on a fixed-size embedding. Experiments follow the Cherepanova et al. (2023) benchmark (11 datasets, three corruption scenarios, 10 baselines) plus 24 metagenomic datasets.

## Strengths

- **Automatic feature-count discovery via principled regularization.** The L_select sparsity penalty combined with Gumbel-Sigmoid temperature annealing lets the model learn how many features to retain without manual specification or iterative search over k. This is a genuine practical convenience relative to methods that require tuning a sparsity threshold or retraining with different budgets.

- **Near-constant computational scaling w.r.t. dimensionality.** The empirical complexity exponent α ≈ 0.08 (Figure 4) is architecturally grounded — the masking network maps from a fixed-size embedding, so its forward pass does not scale with D. This property, if robust across broader dimensional ranges, is a meaningful practical advantage over methods whose cost grows with D.

- **Standardized evaluation setting.** Following the Cherepanova et al. (2023) benchmark provides a fixed experimental framework with 11 datasets and three corruption scenarios, enabling direct comparison with the 10 baselines included in that benchmark. The supplementary metagenomic analysis on 24 real-world datasets adds practical relevance.

## Weaknesses

### Major

- **Asymmetric comparison undermines the headline performance claims.** The paper states (line 204): "all baseline methods select the same number of features as were in the initial representation (before corruption)." This means baselines are required to retain D features (the original count) even after 50% corrupted features are added, while AutoNFS is free to select a much smaller subset (e.g., 65 out of 128+64=192 features on AL). The claim "consistently outperforms while selecting significantly fewer features" therefore compares performance at fundamentally different sparsity levels — baselines cannot discard features even when doing so would help. The misselection analysis (Figure 3a) is informative and not affected by this asymmetry, but the central performance comparison is weakened. A proper evaluation would let each method determine its own sparsity (e.g., Lasso with cross-validated λ, STG with its own penalty) and compare performance at comparable feature counts.

- **Missing comparisons against the most directly relevant differentiable FS methods.** The Related Work discusses STG (Yamada et al., 2020), Hard-Concrete / L0 regularization (Louizos et al., 2017), Concrete Autoencoders (Balin et al., 2019), and INVASE (Yoon et al., 2018) — all differentiable FS methods that also learn masks with sparsity penalties and automatically determine feature count. None appear in the experiments. The 10 baselines used (No FS, Univariate, Lasso, L1 Lasso, ACL, LassoNet, AM, RF, XGBoost, Deep Lasso) are from the Cherepanova benchmark and are either classical or tree-based methods. Since AutoNFS is methodologically closest to STG and L0-regularization (continuous mask relaxation + sparsity penalty + end-to-end SGD), their absence makes it impossible to assess whether AutoNFS improves over the state of the art in its own methodological category. This is the most impactful omission in the paper.

### Minor

- **The masking network design is not ablated.** The core architectural difference from prior differentiable FS is the learned embedding e plus network f(e) to produce mask logits, rather than learning logits directly. The paper does not compare against simpler variants (directly learned logits, logits without embedding, etc.). Without this ablation, it is unclear whether the added complexity of f(e) provides any benefit.

- **No variance or significance reported for ranking results.** Figure 2 and the rankings show AutoNFS ahead by 0.7–0.9 rank points, but no error bars, standard deviations, or significance tests are reported. With only 11 datasets, a single outlier could shift rankings meaningfully.

- **Metagenomic experiment lacks FS baselines.** Table 2 compares AutoNFS only against "full data" (no feature selection). No other FS methods (Lasso, STG, etc.) are evaluated on these 24 datasets, so the experiment only shows that AutoNFS can compress features without catastrophically degrading average performance — not that it is better than alternatives.

- **Individual dataset failures in the metagenomic experiment are not discussed.** On several datasets, AutoNFS substantially degrades performance (e.g., ThomasAM_2018a: MLP drops from 0.733 to 0.567; YuJ_2015: MLP drops from 0.653 to 0.417). The paper reports only averages and does not discuss these cases, which is important for understanding when the method can be trusted.

- **Overclaim in the motivation.** The abstract states existing methods "often cannot automatically detect the number of attributes required to solve a given task," but the Related Work discusses STG, L0-regularization, and Concrete Autoencoders — all of which determine sparsity automatically. The claim should be qualified.

- **Computational complexity comparison is partially apples-to-oranges.** Figure 4 compares AutoNFS (which requires full neural training) against filter methods (ANOVA, Mutual Information) that are one-shot scoring procedures. While the scaling exponent α for AutoNFS is a genuine architectural property, the choice of comparators is questionable — comparing against other neural FS methods (STG, L0-regularization) would be more informative.

### Trivial

- **Method name inconsistency.** The method is called "AutoNFS" throughout the paper but appears as "GFS-NetWork" in Figure 2 and its table. The caption identifies them as the same, but this is confusing.

## Nice-to-Haves

- Include STG and L0-regularization / Hard-Concrete as experimental baselines, or provide a clear justification for their omission.
- Run baselines with their own sparsity mechanisms enabled (e.g., Lasso with cross-validated λ) so the "automatic feature count" claim is evaluated fairly.
- Add an ablation comparing learned embedding + f(e) vs. directly learned logits vs. no embedding to justify the masking network design.
- Report standard deviations or confidence intervals for the ranking results.
- Add at least one FS baseline to the metagenomic experiment.
- Discuss individual datasets where performance drops substantially.

## Removed Points

These points from the input reviews are removed per the filtering rules:

- **Missing architecture details for f and g networks.** These are in Appendix C (removed by the parser). Per guidelines, weaknesses about content in the parser-stripped appendix are removed.
- **Sensitivity to λ in the removed appendix.** The paper references Appendix F for λ analysis. Removed per guidelines.
- **Reproducibility details (E, B, η1, η2, D_e).** These are in the anonymous repository. Removed per guidelines about reproducibility nitpicks.
- **"Methodologically AutoNFS is essentially the same class as Hard-Concrete."** This is an interpretive opinion rather than a verifiable weakness. The architectural distinction (learned embedding + network vs. direct logits) is real, even if its importance is not demonstrated. The missing comparison against STG/Hard-Concrete is retained as a Major weakness above.
- **Criticism about the scaling exponent being measured with too few data points.** The paper states confidence intervals over 5 runs (Figure 4b) and the specific range tested (10² to 10⁵ features). Without more detail, this is a speculation about robustness rather than an identified flaw.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one genuinely novel observation: the asymmetry in the evaluation — baselines forced to select exactly the original number of features while AutoNFS can select fewer — is not a minor design choice but a structural confound. The paper interprets its results as showing that AutoNFS outperforms baselines while selecting fewer features, but the evaluation conflates the method's ability to select *good* features with its ability to select *fewer* features (which baselines are not permitted to do). This reframes the main empirical claim and suggests that a controlled comparison at matched sparsity levels would be more informative.

## Suggestions

1. Include STG and L0-regularization / Hard-Concrete as experimental baselines. These are the natural comparators for any new differentiable FS method.
2. Run the main benchmark with baselines configured to select their own sparsity level (e.g., Lasso with cross-validated λ) to enable a fair comparison of automatic feature count methods.
3. Add an ablation study: compare (a) learned embedding + f(e), (b) directly learned logits, (c) directly learned logits without embedding, to establish whether the masking network architecture is beneficial.
4. Report standard deviations or confidence intervals for the ranking results in Figure 2.
5. Add at least one FS baseline (e.g., Lasso) to the metagenomic experiment.
6. Discuss individual datasets where AutoNFS degrades performance, and explain potential reasons.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>