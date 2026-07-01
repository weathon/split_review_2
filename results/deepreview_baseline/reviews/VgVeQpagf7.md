## Summary

This paper proposes SPS (Summarize-Privatize-Synthesize) and its enhanced variant SPS+, a differentially private dataset distillation method that generates synthetic versions of sensitive datasets. The approach adapts the D3S dataset distillation framework to work with public pretrained models while privatizing intermediate activation statistics via the Gaussian mechanism. The authors claim this is the first generation-based method to match or exceed DP-SGD accuracy on image classification tasks, achieving 96.2% on CIFAR-10 and 76.6% on CIFAR-100 at ε=1, outperforming state-of-the-art DP-SGD results. The method also demonstrates practical advantages including support for model ensembling, federated learning, and continual learning without additional privacy cost.

## Strengths

- **Strong empirical results**: The paper demonstrates that SPS+ achieves higher accuracy than DP-SGD on both CIFAR-10 and CIFAR-100 across multiple privacy budgets, with particularly notable improvements on CIFAR-100 (76.6% vs 70.3% at ε=1). This is a significant achievement for a generation-based approach.

- **Novel technical contributions**: The multitask clipping and grouped pseudo-classes techniques (SPS+) are well-motivated and address real challenges in the high-privacy regime. The noise redistribution strategy (Section 3.2.4) is a clever adaptation that improves the signal-to-noise ratio for per-class statistics.

- **Practical advantages clearly demonstrated**: The paper convincingly shows the flexibility benefits of data-based privacy through federated learning and continual learning experiments, which are genuinely difficult or impossible with DP-SGD. The ability to use SAM optimization and ensembles without additional privacy cost is a meaningful practical advantage.

- **Well-structured presentation**: The paper clearly explains the challenges of adapting D3S to the private setting, the modifications needed, and the reasoning behind each design choice. The connection between dataset distillation and privacy is well-motivated.

## Weaknesses

### Major

- **Unfair comparison to DP-SGD baselines**: The paper compares SPS+ (which uses a public pretrained model) against DP-SGD results from De et al. (2022), which also uses public pretraining. However, the comparison is not apples-to-apples. The DP-SGD baseline uses a WRN-22-8 model, while SPS+ evaluations use WRN-28-10 and WRN-34-10 models for fine-tuning. Since SPS+ benefits from post-processing, it can use larger models without additional privacy cost, while DP-SGD cannot. The paper should include DP-SGD results with the same model architectures (WRN-28-10, WRN-34-10) for fair comparison, or at minimum acknowledge this asymmetry more prominently.

- **Missing computational cost analysis**: The paper mentions generation cost is "relatively heavy" but provides no quantitative comparison. Given that SPS requires generating 50,000 synthetic images (same size as original dataset), the computational cost is likely orders of magnitude higher than DP-SGD training. Without reporting wall-clock time, GPU hours, or convergence iterations, it's impossible to assess the practical trade-off. This is particularly important because the method's main selling point is flexibility, but if generation is prohibitively expensive, the practical value is diminished.

- **Limited evaluation scope**: The paper only evaluates on CIFAR-10/100 and CAMELYON17. For a method claiming to be a general alternative to DP-SGD, experiments on larger-scale datasets (e.g., ImageNet subsets, medical imaging at higher resolution) are needed. The CAMELYON17 experiment uses only ε=8, missing the high-privacy regime where the method claims particular strength.

- **The grouped pseudo-classes technique lacks theoretical justification**: Section 4.2 claims the technique "only works due to dynamics of optimizing the loss function" and "does not offer benefits for direct mean estimation," but provides no analysis of why or under what conditions this holds. This is a core component of SPS+ and deserves more rigorous treatment.

### Minor

- **Privacy accounting details are sparse**: Theorem 4.1 states ε = Mα/(2δ²) for RDP, but this appears to be a simplified expression. The actual RDP guarantee for the Gaussian mechanism is ε = α/(2σ²), and composition would give Mα/(2σ²). The paper should clarify the relationship between b₀, σ, and the privacy parameters more carefully.

- **The "first to match DP-SGD" claim needs qualification**: While the paper achieves higher accuracy than the specific DP-SGD baseline cited (De et al., 2022), there are other DP-SGD works with different architectures and training recipes that may achieve different results. The claim should be more precisely scoped.

- **Ablation studies are limited**: The paper introduces several design choices (smooth activations, SAM optimization, noise redistribution, multistage clipping, grouped pseudo-classes) but does not systematically ablate them to show which components contribute most to the performance gain.

### Trivial

- Figure 3's axis labels appear to be swapped or mislabeled: the text describes CIFAR-100 accuracy as "consistently higher than CIFAR-10 accuracy," which contradicts the actual results in Table 1 where CIFAR-10 accuracy is much higher.

## Nice-to-Haves

- A comparison with DP-SGD using the same model architecture for fine-tuning would strengthen the claims significantly.
- Reporting the computational cost (GPU hours, wall-clock time) for generating the synthetic datasets would help practitioners assess the trade-off.
- An analysis of how the synthetic dataset size affects privacy-utility trade-offs beyond the compression ratio experiments would be valuable.
- Experiments on higher-resolution datasets (e.g., Tiny ImageNet, CelebA) would demonstrate scalability.

## Novel Insights

The key insight is that dataset distillation's statistic-matching paradigm is particularly well-suited for differential privacy because it requires only a single privatization step (aggregating statistics) rather than per-iteration privatization as in DP-SGD. This allows the method to bypass the composition limitations that constrain DP-SGD. The paper also shows that by carefully designing the dimensionality of released statistics (much smaller than gradient dimensionality in DP-SGD), the signal-to-noise ratio can be improved. The grouped pseudo-classes technique, while lacking full theoretical justification, is an interesting empirical observation that noise in covariance estimation can be leveraged to improve class-conditional matching.

## Suggestions

1. Add a direct comparison with DP-SGD using the same model architecture (WRN-28-10 or WRN-34-10) for fine-tuning, even if this requires re-running DP-SGD with those architectures.
2. Report the computational cost of SPS generation (GPU hours, number of optimization steps) and compare it to DP-SGD training cost.
3. Provide a more detailed privacy accounting derivation, clarifying the relationship between the clipping parameters, noise scale, and final (ε, δ) guarantees.
4. Add ablation studies showing the contribution of each component (smooth activations, SAM, noise redistribution, multistage clipping, grouped pseudo-classes) to the final performance.

## Score and Decision

The paper presents a genuinely novel approach that achieves impressive empirical results, outperforming DP-SGD on standard benchmarks for the first time with a generation-based method. The practical advantages (ensembling, federated learning, continual learning) are well-demonstrated and meaningful. However, the unfair comparison to DP-SGD (using different model architectures) and the lack of computational cost analysis are significant concerns that prevent full acceptance without revision. The paper is clearly above the rejection threshold but needs to address these issues to be considered for acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>