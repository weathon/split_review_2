## Summary

This paper introduces Automatic Complementary Separation Pruning (ACSP), a fully automated structured pruning method for CNNs. ACSP constructs a per-layer graph space encoding each component's separation capability across all class pairs (using Jeffries-Matusita distance), applies k-Medoids clustering to select complementary components from diverse graph-space regions, and uses the MSS index with the Kneedle algorithm to automatically determine the optimal pruning extent. Experiments on CIFAR-10/100 and ImageNet across VGG, ResNet, DenseNet, and MobileNet architectures demonstrate 1.5–2.5× FLOP reductions with competitive accuracy retention and real-world inference speed-ups.

## Strengths

- **Fully automated pruning volume selection.** Unlike most baselines that require a user-specified pruning ratio, ACSP determines layer-wise pruning extent automatically via knee-finding on MSS scores. This is a genuine practical advantage, eliminating expensive trial-and-error tuning.
- **Well-motivated complementary selection principle.** The idea that retained components should cover diverse regions of a separability graph space, rather than simply having the highest individual scores, is conceptually sound and connects to established work in feature selection and clustering.
- **Comprehensive experimental coverage.** The paper evaluates ACSP on 6 architectures (VGG-16/19, ResNet-50/56, DenseNet-40, MobileNet-V2) across 3 datasets (CIFAR-10, CIFAR-100, ImageNet-1K), and reports both FLOP-based speed-ups and wall-clock inference latency (Table 2), lending practical credibility to the claims.
- **Consistent accuracy preservation.** Across most settings, ACSP maintains or slightly improves accuracy post-pruning, often outperforming or matching baselines (e.g., best accuracy on CIFAR-10 MobileNet-V2 at 94.98%, best speed-up on ImageNet ResNet-50 at 2.25×).

## Weaknesses

### Fatal
None.

### Major

- **Infeasible graph-space construction for large C.** For ImageNet (C=1000), the separation matrix dimensions are N_i × (p × p × 499,500). For a typical ResNet-50 layer (256 channels, 7×7 spatial), this yields billions of entries. The paper provides no explanation of how this is handled computationally (class-pair sampling, approximation, aggregation). Since this is a core part of the method, the omission undermines reproducibility and raises questions about whether the ImageNet results were obtained via the described methodology or a modified version.

- **Lack of ablation studies on key design choices.** Several important design decisions are not ablated: (1) weight-based vs. medoid-based component selection within clusters (Section 3.4.2), (2) different separability metrics (JM vs. Hellinger vs. Wasserstein are mentioned but no comparison table is provided), (3) sensitivity to fine-tuning duration and data fraction, and (4) polynomial degree in the Kneedle algorithm. Without these, it is unclear which components of ACSP are driving the improvements.

### Minor

- **Layer-by-layer sequential pruning without cross-layer awareness.** Each layer is pruned independently with a short fine-tuning step (2 epochs on 25% data for CIFAR). This sequential approach means pruning decisions in early layers constrain later layers, potentially leading to suboptimal global solutions. The paper does not discuss this limitation or compare against an end-to-end alternative.

- **Results are competitive but not consistently dominant.** On several benchmarks, ACSP achieves best speed-up but not best accuracy (e.g., CIFAR-10 ResNet-56 where DepGraph achieves +0.24% vs. +0.13% at similar speed-ups), or best accuracy but not best speed-up. The method does not convincingly dominate any single baseline across all metrics simultaneously.

- **Wall-clock speed-ups modest relative to FLOP reductions.** Table 2 shows real-world latency improvements of 2–20%, which are considerably smaller than the 1.5–2.5× FLOP reductions. While the paper honestly acknowledges this gap, the practical impact is less impressive than the headline FLOP numbers suggest.

### Trivial

None.

## Nice-to-Haves

- A comparison with recent automatic pruning methods (e.g., those using learnable pruning ratios or neural architecture search) to better contextualize the automatic component.
- Visualization or analysis of the separation matrices across layers to provide intuition about what the graph space captures at different depths.
- Discussion of how the method handles residual connections in detail—Algorithm 1 seems to treat each layer independently, but ResNet skip connections impose structural constraints that may not be fully addressed.

## Novel Insights

The complementary selection principle—choosing components that cover diverse regions of a class-separability graph space rather than simply the most individually discriminative ones—is a genuinely useful framing for structured pruning. The connection to k-Medoids clustering and MSS evaluation provides a principled mechanism for implementing this principle, and the automatic knee-finding for determining pruning extent removes a practical barrier that plagues many existing methods. While individual building blocks (JM distance, k-Medoids, MSS, Kneedle) are established, their integration into a pruning pipeline with the specific goal of ensuring complementary diversity among retained components is a novel and reasonable contribution.

## Suggestions

- Add a detailed discussion of how the O(C²) class-pair scaling is handled in practice, especially for ImageNet. If approximations are used, describe them formally.
- Include ablation tables comparing: (a) weight-based vs. medoid-based selection within clusters, (b) JM vs. alternative separability metrics, and (c) automatic vs. oracle (best) pruning ratios to quantify the cost of automation.
- Provide computational overhead analysis (total pruning time including graph construction, clustering sweeps, and fine-tuning) alongside the inference speed-ups.

## Score and Decision

The paper presents a coherent and well-motivated method with broad experimental evaluation and competitive results. The automatic pruning volume determination and complementary selection principle are genuine contributions. However, the unexplained handling of infeasible graph-space dimensions for large-class datasets (affecting the method's core scalability claim) and the complete absence of ablation studies on critical design choices significantly limit my confidence in the method's robustness and the authors' understanding of what drives performance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: Reject