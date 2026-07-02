## Summary
AutoNFS proposes a fully differentiable neural feature selection method that uses a Gumbel-Sigmoid masking network and a task predictor trained end-to-end. The key innovation is that the number of selected features emerges automatically from a sparsity penalty (mean mask) rather than requiring manual specification. Experiments on OpenML benchmarks (with three corruption scenarios) and 24 real-world metagenomic datasets show that AutoNFS selects far fewer features than strong baselines while maintaining or improving predictive accuracy, and its runtime scales nearly constant with dimensionality.

## Strengths
- **Automatic feature count discovery is practically useful.** Most existing FS methods require the user to pre-specify the number of features, which often necessitates expensive retraining. AutoNFS learns the cardinality directly from the task loss plus a simple sparsity penalty, a clean and important simplification.
- **Convincing empirical results across diverse settings.** On the Cherepanova et al. (2023) benchmark, AutoNFS achieves the best average rank in all three corruption scenarios (e.g., rank 2.1 vs. next best 3.8 on Corrupted features). It selects significantly fewer features than all baselines while maintaining or improving performance. The metagenomic experiments further validate that the method works on real high-dimensional biological data, reducing dimensionality by over 90% on average and often improving downstream accuracy.
- **Near-constant computational overhead.** The complexity analysis (Figure 4) shows that AutoNFS’s runtime is essentially independent of the number of input features (α ≈ 0.08), a striking contrast to classical methods that scale linearly or superlinearly. This makes the approach particularly attractive for high-dimensional tabular data.
- **Thorough quantitative analysis of selected features.** The paper goes beyond just accuracy: it measures misselection rate (features chosen that are not in the ground-truth original set) and the predictive power of selected features (drop in performance when removing one of them). Both analyses confirm that AutoNFS is precise and non-redundant.

## Weaknesses
### Fatal
None.

### Major
- **The claim of fully automatic feature count is weakened by a fixed λ=1.** The sparsity loss weight λ is the main lever controlling how many features are retained. The paper asserts that λ=1 “gives satisfactory results across datasets,” but the main text provides no ablation or sensitivity study over λ. Without showing that the method is robust to λ or that λ=1 is nearly optimal across different datasets, the “automatic” claim is overstated—the user still must choose λ, even if only once. (If the appendix provides such analysis, it should be referenced more prominently.)

- **Missing architectural details for the masking network and task network.** The paper describes the training procedure in Algorithm 1 but does not specify the architecture of f (masking network) or g (task network) beyond “MLP” for g and no detail for f. For example: how many layers, what activation functions, what hidden sizes? The learning rates η₁, η₂ are also not reported. While these are common choices, their absence makes reproduction non-trivial.

### Minor
- **Comparison of computational complexity is limited to classical methods.** The time-scaling analysis only compares AutoNFS with ANOVA F-value, Mutual Information, Random Forest, and RFE. It does not include any other neural FS methods (e.g., STG, Deep Lasso, LassoNet), which are the most relevant competitors and might also benefit from GPU parallelization. The claim of “near-constant time” could be put in better perspective by showing that differentiable neural methods in general scale efficiently.

- **Inconsistency in method naming.** In Figure 2 the method is labeled “GFS-NetWork,” while the text and table use “AutoNFS.” This is confusing and should be unified.

### Trivial
- The MNIST interpretability study (Figure 7, 8) is referenced but not included in the main paper; its value cannot be assessed from the limited description.

## Nice-to-Haves
- Investigate whether the same λ value generalizes to datasets of very different dimensionality, or whether a simple heuristic (e.g., λ ∝ D) could make the method truly hyperparameter-free.
- Include runtime comparisons with other neural FS methods (e.g., STG, LassoNet) on a subset of the benchmark datasets to strengthen the complexity claim.
- Provide a brief sensitivity study of the temperature annealing schedule (initial τ, decay rate) to show that the method is not brittle to these settings.

## Novel Insights
Beyond the paper’s own contributions, the empirical observation that a single λ=1 works well across 11 diverse benchmark datasets (with feature counts ranging from 8 to 136) is interesting: it suggests that the scale of the task loss and the sparsity loss are naturally balanced in many common settings, so practitioners may not need extensive hyperparameter tuning for the sparsity weight. The near-constant time scaling results also suggest a broader design principle: if a FS method can be expressed as a feed-forward pass on a small learned embedding (independent of the data dimensionality), it can achieve O(1) complexity in the number of features, which is a valuable insight for scalable FS algorithm design.

## Suggestions
- Add a brief description of the masking network and task network architectures (layers, activations, widths) to the main paper or Algorithm 1 caption.
- Include a simple sensitivity analysis over λ (e.g., at three values) on a subset of benchmark datasets to demonstrate that the method’s performance is not highly sensitive to λ.
- Rename the legend in Figure 2 from “GFS-NetWork” to “AutoNFS” to match the paper.

## Score and Decision
**Score:** 7  
**Decision:** Accept  

Justification: The paper presents a clean, well-motivated, and empirically strong neural feature selection method. The automatic feature count and near-constant runtime are valuable contributions that address genuine limitations of existing approaches. The weaknesses (lack of architectural details, limited complexity comparison, and the degree of “automatic” nature) are addressable and do not invalidate the core results. I recommend acceptance.

MY FINAL SCORE: <score>7</score>  
MY FINAL DECISION: <decision>Accept</decision>