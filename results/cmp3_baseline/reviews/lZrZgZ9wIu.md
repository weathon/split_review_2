## Summary

This paper investigates the combination of dynamic sparse training (specifically Cannistraci-Hebb Training, CHT) with ANN-to-SNN conversion to produce sparse SNNs. It is the first study to explore this intersection. Experiments across MLP, VGG-16, and ViT-B on CIFAR-10/100 and ImageNet, using multiple conversion methods, show that sparse SNNs can match or exceed dense SNN accuracy while achieving up to 99% theoretical energy reduction. The paper also analyzes the time lag between firing rate saturation and accuracy saturation, finding a significant difference between sparse and dense networks.

## Strengths

- **Novel combination of two research directions**: The paper is the first to systematically study dynamic sparse training (CHT) for ANN-to-SNN conversion, bridging a gap between sparse ANN training and SNN conversion literature.
- **Comprehensive empirical evaluation**: Experiments cover three architectures (MLP, VGG-16, ViT-B), three datasets (CIFAR-10/100, ImageNet), and four conversion methods, providing robust evidence for the claims.
- **Interesting temporal dynamics analysis**: The discovery of a consistent positive time lag between firing rate saturation and accuracy saturation, and the significant difference between sparse and dense SNNs, offers new insight into how structural sparsity affects SNN information processing.
- **Large theoretical energy savings**: The paper demonstrates that sparse SNNs can reduce theoretical energy consumption by up to 99% compared to dense SNNs, which is a practically relevant result if sparse neuromorphic hardware becomes available.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical energy calculation relies on strong hardware assumptions**: The energy savings are computed assuming future hardware that simultaneously supports both structural sparsity and event-driven computation. The paper acknowledges this limitation, but it is a central claim. Without such hardware, the actual energy benefits may be significantly smaller or even negative due to overheads. This weakens the practical impact of the results.
- **Saturation detection algorithm is arbitrary**: The method for determining saturation time (1% relative improvement over 10 consecutive steps) is not justified or validated. The choice of threshold and window size can substantially affect the reported time lags and energy comparisons. A sensitivity analysis or a more principled approach (e.g., elbow detection) would strengthen the analysis.
- **Limited comparison to other sparsity methods in the main text**: The paper relegates comparisons to pruned ANNs and STBP-based sparse training to the appendix. Given that the core contribution is about sparse SNN conversion, a main-text comparison to at least one alternative sparsity approach (e.g., pruning before conversion) would better contextualize the benefits of CHT.

### Minor
- **Accuracy improvements are inconsistent**: While some configurations show clear accuracy gains (e.g., MLP on CIFAR-100 with AEC: +11.84%), others show small degradations (e.g., VGG-16 on CIFAR-100 with AEC: -0.52%). The claim "close or even superior" is accurate, but the paper could more clearly discuss when sparsity helps versus hurts.
- **Time lag explanation is speculative**: The qualitative explanation for why firing rate saturates before accuracy (last-layer stabilization) is plausible but not empirically supported. The paper does not analyze layer-wise firing rates to verify this mechanism.
- **No discussion of training cost**: The paper focuses on inference energy savings but does not mention the computational cost of CHT training itself, which may be higher than dense training due to topology evolution. This is relevant for a complete trade-off analysis.

### Trivial
- The legend in Figure 2 is partially duplicated in the caption and text; the figure is somewhat cluttered.

## Nice-to-Haves

- A sensitivity analysis of the saturation detection parameters (threshold, window size) would increase confidence in the time lag results.
- Layer-wise firing rate analysis to support the proposed mechanism for the time lag.
- A discussion of how the theoretical energy savings translate to realistic hardware (e.g., overheads of sparse computation, memory access costs).

## Novel Insights

Beyond the paper's own contributions, the key novel insight is that structural sparsity from dynamic sparse training not only reduces theoretical energy but also alters the temporal dynamics of converted SNNs, specifically by increasing the time lag between firing rate saturation and accuracy saturation. This suggests that sparse connectivity may require longer inference to stabilize output representations, which could be a fundamental property of rate-coded SNNs. The paper provides the first quantitative evidence of this effect across multiple architectures and conversion methods.

## Suggestions

- Include a main-text comparison to at least one alternative sparsity method (e.g., magnitude pruning before conversion) to better isolate the benefits of CHT.
- Validate the saturation detection algorithm with a sensitivity analysis or adopt a more standard method (e.g., change point detection).
- Discuss the practical feasibility of sparse neuromorphic hardware and the potential overheads that could reduce the theoretical energy savings.

## Score and Decision

**Score**: 6  
**Decision**: Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>