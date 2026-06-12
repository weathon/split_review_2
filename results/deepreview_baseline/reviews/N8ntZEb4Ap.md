## Summary
The paper proposes AutoNFS, a neural feature selection method that uses Gumbel-Sigmoid relaxation to learn a binary mask over features and a sparsity penalty to automatically determine how many features to select. The masking and task networks are trained end-to-end. Experiments on OpenML benchmarks (with corrupted feature scenarios) and metagenomic datasets show that AutoNFS selects far fewer features than baselines while maintaining or improving predictive performance, and the authors claim nearly constant computational overhead regardless of input dimensionality.

## Strengths
- **Automatic feature count discovery** – Unlike many methods that require the user to specify the number of features, AutoNFS learns the appropriate cardinality during training, which is a practical advantage.
- **Strong empirical performance on real-world data** – On 24 metagenomic datasets, AutoNFS reduces dimensionality to ~7.7% of the original while often improving accuracy for both MLP and Random Forest downstream classifiers.
- **Efficient end-to-end training** – The differentiable Gumbel-Sigmoid mechanism allows joint optimization of selection and prediction without iterative retraining.

## Weaknesses
### Major
1. **Unfair comparison with baselines in the main benchmark.** The benchmark design forces all baseline methods to select exactly the original number of features (before corruption), while AutoNFS is allowed to select fewer. Since many corrupted features are irrelevant, selecting more features can hurt performance. This biases the comparison in favor of AutoNFS and undermines the claim that AutoNFS “consistently outperforms all competitive methods.” The paper should compare against baselines that also automatically determine feature count (e.g., Lasso with cross-validation, STG, L0-regularized nets) or at least allow baselines to choose their number of features via validation.

2. **Overclaimed computational scalability.** The paper claims “nearly constant computational overhead regardless of input dimensionality” and reports an empirical complexity exponent of 0.08. However, the masking network outputs D logits and the Gumbel-Sigmoid operation is applied per feature, both of which scale linearly with D. The equally important task network also has a first layer whose weight matrix is of size D × H. The near-constant empirical behavior is likely an artifact of the tested feature range (10²–10⁵) where fixed overheads dominate. For higher dimensions the method must become linear in D. The claim should be tempered with a theoretical complexity analysis and a discussion of the practical regime where the method remains efficient.

### Minor
3. **Novelty relative to existing differentiable FS methods** – Methods like STG (Yamada et al. 2020b) and L0 regularization (Louizos et al. 2017) already use continuous relaxations and sparsity penalties to automatically select features. The paper should more clearly differentiate AutoNFS (e.g., the separate masking network design, the specific use of a fixed seed embedding) and discuss what additional value it brings.

4. **Sensitivity to the sparsity parameter λ** – The paper fixes λ=1 across all datasets, but the optimal sparsity level likely varies. Without an ablation study (Appendix F is mentioned but not included in the provided material), it is unclear how robust the automatic count discovery is to this hyperparameter.

### Trivial
5. None.

## Nice-to-Haves
- Include baselines that automatically determine feature count (e.g., STG, Lasso with cross-validation) to enable an apples-to-apples comparison.
- Provide a theoretical complexity analysis showing O(D) scaling and discuss the range of D where empirical scaling appears sublinear.
- Add an ablation study on the effect of λ on both the number of selected features and downstream performance.

## Novel Insights
The paper shows that a simple Gumbel-Sigmoid gating module combined with a cardinality penalty can produce competitive feature selection with automatic count determination, and that the selected features transfer well across different classifiers (MLP and Random Forest). The core idea, however, closely follows existing differentiable FS work (STG, L0 regularization), and the primary novelty lies in the specific architectural instantiation rather than a fundamentally new principle.

## Suggestions
1. Rerun the main benchmark comparison allowing baselines to select their optimal number of features (e.g., by tuning the number of selected features on a validation set). Without this, the “outperforming” claim is not convincingly supported.
2. Discuss the theoretical time complexity (at least O(D) for the mask computation and task network) and explain why the empirical exponent is so low. Acknowledge that for sufficiently large D the scaling will become linear.

## Score and Decision
MY FINAL SCORE: 4</score>
MY FINAL DECISION: Reject</decision>