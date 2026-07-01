## Summary

The paper introduces AutoNFS, an end-to-end differentiable neural network for automatic feature selection. It uses a Gumbel-Sigmoid mechanism to learn a binary mask that selects features, and a cardinality penalty in the loss function to automatically determine how many features to retain, removing the need to pre-specify the number of features. The method is evaluated on OpenML benchmark datasets and metagenomic data, showing that it selects far fewer features than competing methods while maintaining or improving predictive performance.

## Strengths

- **Addresses a practical pain point**: Automatically determining the number of relevant features is a genuine challenge in high-dimensional tabular data, and the paper proposes a clean end-to-end differentiable solution.
- **Strong empirical results on benchmarks**: In the three corruption scenarios, AutoNFS consistently achieves the best average rank among 11 methods, and it selects significantly fewer features than baselines while preserving predictive accuracy.
- **Demonstrated utility on real-world biological data**: On 24 metagenomic datasets, AutoNFS reduces the feature set to about 7.7% of the original while maintaining or improving downstream classifier accuracy across two different model types (MLP and Random Forest).
- **Computational complexity analysis**: The paper provides an empirical scaling analysis showing that the wall-clock time of AutoNFS grows very slowly with the number of features, which is a desirable property for high-dimensional settings.

## Weaknesses

### Major

1. **Unfair comparison with baselines**: All baseline methods are forced to select exactly the same number of features as the original (pre-corruption) dimensionality. In contrast, AutoNFS is allowed to automatically select a much smaller subset. This gives AutoNFS a substantial advantage in both the feature selection quality metric (misselection error) and predictive performance, because selecting fewer features is itself beneficial for reducing overfitting. A fairer evaluation would also compare with baselines that automatically determine the number of features (e.g., L1-regularized methods with cross-validated lambda, or hold-out validation to choose the number of top-k features).

2. **Overstated claim of near-constant computational overhead**: The paper claims that AutoNFS “achieves a nearly constant computational overhead regardless of input dimensionality.” However, the masking network must output a D-dimensional vector, so its forward pass (and backward pass) scale at least linearly with D. The task network also takes D inputs, so its cost also scales with D. The empirical plot (Figure 4a) shows AutoNFS time remaining flat around 10 seconds, but this is only shown up to 10^5 features and lacks sufficient detail (e.g., what component of time is measured? Are the task network, data loading, and pre-processing included?). Such a flat curve contradicts the basic scaling of the architecture and requires much stronger evidence and a clearer explanation.

3. **Limited novelty over existing differentiable feature selection methods**: The core technique—using a continuous relaxation of binary gates with a penalty on the number of selected features—is already established in methods such as Hard-Concrete (Louizos et al., 2017) and Stochastic Gates (Yamada et al., 2020). The paper’s use of Gumbel-Sigmoid and a separate masking network is a minor architectural variant. The claim that existing methods “involve user intervention... with different feature budgets” is misleading because Hard-Concrete and STG also automatically induce sparsity through regularization. The novelty over this prior work is not clearly articulated.

4. **No ablation or sensitivity analysis for the key hyperparameter λ**: The cardinality penalty weight λ is set to a constant 1 for all experiments, which is a strong assumption. There is no study of how the number of selected features and predictive performance vary with λ, nor any justification that λ=1 is universally appropriate. The paper references Appendix F for this analysis, but the appendix is stripped, so the reader cannot evaluate this.

### Minor

- **Inconsistent naming in figures**: The method is labeled “GFS-NetWork” in Figure 2 tables and the bar chart, while the paper calls it “AutoNFS”. This inconsistency confuses the reader.
- **Lack of details on the masking network architecture**: The paper only states that the masking network maps an embedding of size D_e to D dimensions. It does not specify the architecture (e.g., number of layers, activation functions, whether it is a linear layer or an MLP), which makes reproducibility harder.
- **No justification for the seed embedding**: The role of the seed embedding e and why the mask is conditioned on it rather than on the data is not explained. The embedding could be collapsed into the parameters of the masking network, so the design seems unnecessary.

## Nice-to-Haves

- Compare with baselines that also automatically select the number of features (e.g., Lasso with cross-validated lambda, or Hard-Concrete/STG with similar sparsity penalties) to make the comparison fair and to highlight what AutoNFS adds.
- Include a sensitivity analysis for the λ parameter and for the temperature annealing schedule to help practitioners set these hyperparameters.
- Provide a theoretical or intuitive explanation for why the method should be able to automatically discover the minimal sufficient subset, beyond saying the penalty encourages it.

## Novel Insights

None beyond the paper’s own contributions. The paper repackages existing differentiable gating and penalized selection techniques into a specific architecture and demonstrates strong empirical results, but does not introduce a new learning principle or theoretical understanding.

## Suggestions

1. In a revised version, allow baseline methods to also select the number of features automatically (e.g., by cross-validation on a validation set or by using L1 regularization with a tuned lambda). Report results for both the original feature budget and the automatically chosen budget.
2. Clarify what “computational overhead” means in the complexity analysis: include the time of the task network, data batching, and gradient computation. Provide a theoretical complexity analysis and show scaling for a wider range of feature dimensions, including the cost of the masking network separately.
3. Differentiate the work more clearly from Hard-Concrete and STG in the text, and include them as baselines in the experiments.
4. Make the naming consistent throughout the paper (choose either AutoNFS or GFS-NetWork).

## Score and Decision

**Score**: 4  

**Decision**: Reject  

The paper tackles a relevant problem and reports strong empirical results, but the core technical novelty is limited given prior differentiable feature selection methods, the empirical comparison is unfairly skewed in favor of the proposed method, and the central claim of near-constant computational overhead is not convincingly supported. These issues are serious enough that the paper in its current form does not meet the bar for acceptance at ICLR.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>