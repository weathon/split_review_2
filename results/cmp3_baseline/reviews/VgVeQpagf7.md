## Summary

This paper introduces SPS (Summarize-Privatize-Synthesize) and its enhanced variant SPS+, a family of differentially private dataset distillation algorithms. The methods use a public pretrained model to extract privatized activation statistics from a sensitive dataset, then synthesize a private synthetic dataset by matching those statistics via KL divergence. For the first time, a generation-based DP approach matches or exceeds the accuracy of DP-SGD on CIFAR-10/100 classification (e.g., 96.2% vs. 94.8% on CIFAR-10 at ε=1) while offering additional flexibility such as unlimited model reuse, ensembling, federated learning, and continual learning without extra privacy cost.

## Strengths

- **Novel and impactful contribution**: The paper convincingly demonstrates the first generation-based DP method that achieves higher accuracy than state-of-the-art DP-SGD on standard image classification benchmarks. This is a long-standing open challenge, and the result is significant for the privacy community.
- **Well-motivated and clear presentation**: The paper clearly articulates the limitations of DP-SGD (bounded iterations, incompatibility with ensembling/BatchNorm, composition costs) and shows how a data-based privacy approach overcomes them. The method is explained with sufficient detail (statistic extraction, privatization, multi-stage clipping, grouped pseudo-classes).
- **Thorough experimental validation**: The evaluation covers multiple datasets (CIFAR-10/100, CAMELYON17), multiple architectures (WRN28-10, WRN34-10, ensembles), various privacy budgets (ε=1,2,4,8), and diverse settings (federated learning, continual learning, compression ratios, oversized distillation). Results consistently show SPS+ outperforming DP-SGD baselines, especially in high-privacy regimes.
- **Practical advantages demonstrated**: The paper showcases concrete benefits of data-based privacy: ensembling without composition cost, asynchronous federated learning, and class-incremental continual learning. These scenarios are impractical under standard DP-SGD, and the results convincingly show that SPS+ enables them effectively.
- **Sound privacy analysis**: The privacy guarantee (Theorem 4.1) follows directly from RDP composition of Gaussian mechanisms, and the conversion to (ε,δ)-DP is standard. The use of δ=10⁻⁵ (or 3·10⁻⁶) is reasonable for the dataset sizes considered.

## Weaknesses

### Fatal

None.

### Major

- **Computational cost not quantified**: The paper acknowledges that generation is "relatively heavy" but provides no runtime, FLOPs, or wall-clock comparison to DP-SGD training. Given that the method synthesizes 50k images (potentially with multiple M stages), the cost could be prohibitive for practitioners. A quantitative comparison would help assess practical deployability.
- **Reliance on a specific public pretrained model**: The method uses a WRN-22-8 with SiLU activations trained on 32×32 ImageNet. While domain shift is tested with CAMELYON17, the sensitivity to the choice of public model architecture, pretraining data, or activation function is not studied. The method may underperform if a suitable public feature extractor is unavailable.
- **Limited justification for grouped pseudo-classes**: The authors state that this technique “only works due to dynamics of optimizing the loss function” and does not help for direct mean estimation, but the explanation is brief and somewhat heuristic. The empirical gains are clear, but a deeper theoretical or intuitive understanding would strengthen the paper.
- **Comparison to alternative generation methods at comparable ε**: The paper cites Private Evolution (89.13% at ε=10) and DP-Diffusion, but does not compare SPS+ to these methods at the same privacy budgets (e.g., ε=1,2,4,8). While SPS+ clearly outperforms at low ε, direct comparisons would further substantiate the claim of being the first generation method to beat DP-SGD.

### Minor

- **No error bars for ensemble results**: Table 1 reports standard deviations for single models but only point estimates for ensembles. While ensembles are deterministic given the models, reporting variation across runs would be informative.
- **Continual learning experiment limited scope**: The class-incremental setting (10 subsets of 10 classes) is tested only for one partitioning strategy. Additional ablations (e.g., different ordering, more steps) would strengthen the conclusion.
- **Only small image resolutions**: All experiments are on 32×32 or 64×64 images. Scaling to higher resolutions (e.g., 224×224) may increase statistic dimensionality and noise, potentially diminishing performance. This limitation is not discussed.

### Trivial

None.

## Nice-to-Haves

- Could discuss amortizing generation (e.g., using a public generator with an SPS-style loss, similar to GLaD for dataset distillation).
- Could study the effect of class imbalance on SPS performance.
- Could extend the method to discrete modalities (text) as a future direction.
- Could provide a computational cost comparison (e.g., GPU-hours) and memory footprint relative to DP-SGD.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that **privatizing summary statistics (first and second moments) of intermediate activations from a public pretrained model can produce synthetic data of surprisingly high quality—competitive with direct DP training**. This reframes the problem: instead of privatizing the training process (DP-SGD), one can privatize a compact set of features derived from the data and then synthesize a dataset. The multi-stage clipping and grouped pseudo-class techniques further show that iterative refinement and judicious grouping of weak signals can substantially improve the signal-to-noise ratio in high-privacy settings. This opens a new axis for DP deep learning: invest computation in high-quality privatized data that can be reused arbitrarily.

## Suggestions

- Quantify the generation cost (GPU-hours, number of optimization steps) and compare to DP-SGD training time for a fair practical assessment.
- Include a study of sensitivity to the public pretrained model: vary architecture (e.g., ResNet, ViT), pretraining dataset (e.g., ImageNet, Places), and activation function (e.g., ReLU vs. SiLU).
- Provide a more intuitive explanation for why grouped pseudo-classes work, perhaps showing that the KL divergence’s inverse-covariance term amplifies certain noise patterns that help the optimization.
- Add comparisons to more recent DP-SGD baselines (e.g., DP-SGD with adaptive clipping, large batch training) or additional generation methods (e.g., DP-Diffusion) at matching epsilon values.

## Score and Decision

The paper presents a novel, well-executed method that achieves state-of-the-art results for generation-based DP and matches/exceeds DP-SGD, a long-standing goal. The experiments are thorough and the advantages for practical scenarios are convincingly demonstrated. The weaknesses (computational cost, reliance on public model, limited scale) are real but do not invalidate the core contribution. The paper makes a significant contribution to the field of differentially private machine learning.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>