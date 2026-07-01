##Summary

This paper introduces SPS and SPS+, algorithms that generate differentially private synthetic datasets by privatizing intermediate activation statistics from a public pretrained model and then synthesizing images via KL-divergence matching. The method is the first generation-based approach to match or exceed DP-SGD accuracy on CIFAR-10/100 (e.g., 96.2% vs. 94.8% on CIFAR-10 at ε=1) while enabling flexible downstream uses such as ensembling, federated learning, and continual learning without additional privacy cost.

## Strengths

- **State-of-the-art empirical results**: SPS+ achieves higher accuracy than DP-SGD on both CIFAR-10 and CIFAR-100 across multiple privacy budgets, a milestone for generation-based private learning. The gains are substantial (e.g., +6.3% on CIFAR-100 at ε=1).
- **Novel technical contributions**: Multistage clipping and grouped pseudo-classes are clever adaptations that address the high-privacy regime and the noise scaling problem for per-class statistics. The use of random projections to control dimensionality is well-motivated.
- **Practical advantages over DP-SGD**: The synthetic-data paradigm naturally supports model ensembling, asynchronous federated learning, and continual learning without extra privacy cost—capabilities that are difficult or impossible under DP-SGD. The paper demonstrates these benefits with solid experiments.
- **Clear exposition and thorough evaluation**: The paper is well-structured, the method is explained in sufficient detail, and the experiments cover multiple settings (different architectures, ensembles, domain shift, compression, federated, continual). Code is provided.

## Weaknesses

### Fatal
None.

### Major
- **Privacy accounting error in Theorem 4.1**: The theorem states that the RDP parameter ε = Mα/(2δ²), but δ is the DP parameter, not the noise scale. The correct expression should involve the noise multiplier b₀ (or σ). This appears to be a typo, but it is a critical part of the paper’s core guarantee. The authors must clarify the correct formula and confirm that the actual accounting used in experiments is correct. If the accounting is flawed, the entire privacy claim is invalid.

### Minor
- **Computational cost not quantified**: The paper acknowledges that generation is “relatively heavy” but provides no runtime or resource comparison with DP-SGD. Given that the synthetic dataset is the same size as the original (50k images), the cost could be a practical barrier. A brief comparison (e.g., GPU-hours) would help readers assess trade-offs.
- **Heuristic justification for grouped pseudo-classes**: The claim that this technique “only works due to dynamics of optimizing the loss function” is interesting but lacks theoretical analysis. While the empirical results are strong, a more rigorous explanation would strengthen the paper.
- **Federated learning privacy accounting**: The paper states that each party runs SPS+ independently, but it does not clarify whether the overall privacy guarantee is per-party or global. Since the synthetic datasets are released independently, the total privacy loss is the composition of the individual releases. This should be explicitly discussed.

### Trivial
None.

## Nice-to-Haves

- A comparison of the computational cost (time/memory) between SPS generation and DP-SGD training would be useful for practitioners.
- An ablation study isolating the effect of SiLU activations in the pretrained model (vs. standard ReLU) would clarify the necessity of this design choice.
- Extending the evaluation to a larger-scale dataset (e.g., Tiny ImageNet or a subset of ImageNet) would further demonstrate scalability.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that dataset distillation’s statistic-matching framework can be naturally adapted to differential privacy by privatizing only the summary statistics (means and covariances) rather than per-iteration gradients. This reduces the effective dimensionality of the privatized object (from ~10⁷ to ~10⁵) and enables post-processing flexibility. The paper also shows that the synthetic data can be reused across multiple tasks (federated, continual) without additional privacy cost, which is a fundamental advantage over iterative gradient-based methods.

## Suggestions

1. Correct the privacy accounting formula in Theorem 4.1 and provide a brief derivation in the appendix.
2. Add a table or paragraph comparing the computational cost of SPS generation (e.g., GPU-hours for CIFAR-10/100) with DP-SGD training.
3. Clarify the privacy guarantee in the federated learning setting: is each party’s ε independent, and what is the total privacy loss when combining synthetic datasets?

## Score and Decision

**Score**: 8  
**Decision**: Accept

The paper presents a novel and effective method that achieves a significant milestone in private deep learning—matching and exceeding DP-SGD accuracy with a generation-based approach. The practical advantages (ensembling, federated, continual learning) are convincingly demonstrated. The main weakness is the apparent typo in the privacy accounting theorem, which must be corrected, but it does not invalidate the overall contribution. I recommend acceptance.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>