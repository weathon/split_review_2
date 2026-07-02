## Summary
This paper investigates the integration of dynamic sparse training (specifically Cannistraci-Hebb Training, CHT) into ANN-to-SNN conversion pipelines. The authors demonstrate that sparse SNNs obtained through this approach can achieve accuracy comparable to or exceeding dense SNNs while reducing theoretical energy consumption by up to 99%. Additionally, they uncover a novel phenomenon where firing rate saturation precedes accuracy saturation in converted SNNs, with sparse networks exhibiting significantly larger time lags than dense networks.

## Strengths
- **First systematic investigation of dynamic sparse training in ANN-to-SNN conversion**: The paper addresses a clear gap in the literature by combining two previously separate research directions—dynamic sparse training and ANN-to-SNN conversion. This intersection is well-motivated and practically relevant.
- **Comprehensive experimental coverage**: The evaluation spans three network architectures (MLP, VGG-16, ViT-B), three datasets (CIFAR-10, CIFAR-100, ImageNet), and four conversion methods, providing convincing evidence for the generality of the findings.
- **Novel analysis of firing-rate/accuracy saturation dynamics**: The identification of a consistent positive time lag between MASFR saturation and accuracy saturation, along with the significant difference between sparse and dense networks, offers genuine insight into SNN temporal dynamics that extends beyond the paper's primary contribution.

## Weaknesses

### Major
- **Theoretical energy calculation is insufficiently justified as a primary contribution**: The claimed "up to 99% energy reduction" is theoretically expected given 99% connection sparsity on MLPs. Since the paper explicitly acknowledges the lack of hardware supporting both sparse and event-driven computation, the practical significance of these theoretical savings is unclear. The analysis would be substantially stronger with either actual hardware measurements or a more nuanced discussion of when and how these theoretical savings translate to practice.
- **Limited comparison with existing sparse SNN approaches**: The paper compares against pruned ANNs and STBP sparse training only in appendices (C and D), but these comparisons are not discussed in the main text. Given that directly trained sparse SNNs exist in the literature, the paper would benefit from a more prominent comparison showing whether the conversion-based approach offers advantages over direct sparse SNN training.
- **The saturation time analysis methodology is somewhat arbitrary**: The 1% relative improvement threshold over 10 time steps is presented without justification or analysis of sensitivity to these hyperparameters. A more rigorous approach or ablation study would strengthen the claims about time lag differences.

### Minor
- **The MLP results on CIFAR-10/100 show unusually low accuracy (63-66% for dense ANNs)**: These results are far below what modern architectures achieve on these benchmarks. While the relative comparison between sparse and dense is still valid, the practical significance of findings on such low-performing models is questionable.
- **The paper claims "accuracy improvement" in cases where the differences are within noise levels**: Several reported improvements under 1% (e.g., +0.51%, -0.05%) are likely not statistically significant, yet they are presented as positive results.
- **Missing details about the grid search for Vision Transformer**: The paper mentions grid-search for all experiments except ViT, but no justification is provided for why ViT was excluded.

### Trivial
- The definition of energy reduction in Table 1 appears to have an error: the formula uses E_sparse in the denominator but the text describes it as reduction from dense to sparse.

## Nice-to-Haves
- Analysis of how different sparsity levels affect the accuracy-energy trade-off curve would strengthen the practical guidance
- Discussion of which layers benefit most from sparsification in terms of energy savings
- Investigation of whether the time lag phenomenon holds for other SNN training paradigms beyond conversion

## Novel Insights
Beyond the paper's own contributions, the most interesting insight is the discovered asymmetry in how structural sparsity affects temporal dynamics in SNNs. The finding that sparse networks exhibit longer time lags between firing rate and accuracy saturation suggests that sparse connectivity may be processing information in a fundamentally different temporal regime, where individual neurons must integrate over longer periods to achieve stable representations. This raises interesting questions about whether there exists an optimal sparsity level that balances energy efficiency against inference latency, and whether different tasks would benefit from different sparsity-adaptation strategies.

## Suggestions
1. **Provide energy analysis at multiple sparsity levels**: Instead of only reporting results at fixed sparsity levels (99%, 70%, 50%), include curves showing how the accuracy-energy trade-off varies with sparsity. This would make the practical guidance much stronger.
2. **Acknowledge the limitations of theoretical energy more prominently**: The paper should discuss what hardware assumptions are needed for the theoretical savings to materialize and which layers or operations dominate energy in practice.
3. **Include statistical significance tests for accuracy comparisons**: Report confidence intervals or statistical tests for the accuracy improvements claimed in Table 1, especially for small differences.

## Score and Decision
This paper makes a meaningful contribution by systematically exploring an underexplored intersection of two active research areas. The experimental breadth is commendable, and the discovery of the time lag phenomenon provides genuine insight. However, the practical significance of the theoretical energy calculations is overstated, and the weaknesses in comparison methodology temper the overall impact.

**Score**: 6

**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>