## Summary

This paper identifies and theoretically motivates an inherent label dependency in semi-supervised learning (SSL), where the utility of unlabeled data is bounded by the quantity and quality of labeled samples. To mitigate this, the authors propose CaPT, a co-training framework that asymmetrically pairs a unimodal vision network (fully fine-tuned) with a multimodal CLIP model (parameter-efficiently fine-tuned) via entropy-weighted co-pseudo labels. CaPT consistently achieves state-of-the-art results across multiple SSL benchmarks, with particularly large gains in extremely low-label regimes (e.g., 21.38% improvement on CIFAR-100 with one label per class).

## Strengths

- **Novel problem diagnosis and theoretical grounding.** The paper provides a clear empirical demonstration that SSL performance degrades sharply when labeled data is extremely scarce or of low quality, and supports this with a theoretical bound (Theorem 1.1) linking pseudo label error to labeled sample size and prototype bias. This formalizes a previously underappreciated limitation.
- **Effective framework design.** CaPT’s asymmetric-modalities co-training with entropy-based weighting is well motivated. Using PEFT for CLIP while fully fine-tuning the vision network strikes a good balance between leveraging CLIP’s prior and maintaining learning capacity. The ablation studies validate each design choice (e.g., bidirectional flow, feature-augmented consistency regularization, entropy weighting).
- **Strong and consistent empirical results.** CaPT outperforms 12 prior SSL methods across all 6 USB benchmark settings, with particularly large margins in low-label regimes (e.g., +4.09% on CIFAR-100 with 2 labels/class, +6.18% on STL-10 with 4 labels/class). The one-label-per-class results (e.g., 82.51% vs. 61.13% on CIFAR-100) are striking. Gains also hold on ImageNet and multiple fine-grained datasets.
- **Efficiency considerations.** The paper reports that CaPT adds only 8% memory and 11% training time over FreeMatch, while outperforming the heavier RegMixMatch in both accuracy and resource consumption.
- **Thorough ablations.** The ablation study disentangles contributions of each module (UPM, MPM, co-training direction, weighting scheme, feature augmentation), giving confidence that the full design is needed.

## Weaknesses

### Fatal
None.

### Major
- **The theoretical analysis (Theorem 1.1) uses a simplified prototype-based Gaussian-mixture model with a nearest-prototype classifier, which is far removed from the actual SSL algorithms (neural networks with thresholding, augmentation, etc.).** The bound is used to motivate SSL’s label dependency, but the connection to modern SSL methods is not rigorously established. The gap between the prototypical model and deep SSL limits the theorem’s direct applicability as a justification for the method.
- **The paper’s reliance on CLIP’s zero-shot prior raises concerns about fair comparison.** Many standard SSL benchmarks (CIFAR-100, STL-10, EuroSAT) likely overlap with CLIP’s training data. Although the authors partially address this by testing on fine-grained datasets (where CLIP zero-shot is weaker) and by ablating the CLIP-only baseline, the magnitude of improvement on standard benchmarks may partly reflect CLIP’s pre-existing knowledge of those datasets. A more explicit discussion of this confound and its potential impact on the reported margins is warranted.

### Minor
- **The co-pseudo label generation mechanism is not fully described in the main text.** In particular, the handling of low-confidence samples (replacing the pseudo label by an all-zero vector when confidence is below threshold) is only mentioned in passing. This detail is important for reproducibility and should be integrated into the core methods section.
- **The claim of “breaking” label dependency is somewhat over-stated.** CaPT significantly reduces dependency, but performance still drops when going from 2 to 1 label per class (e.g., CIFAR-100: 84.83% → 82.51%). The paper does not eliminate the effect, it mitigates it.
- **Portability of the framework is claimed but not demonstrated.** The authors note that future VLMs can be plugged into CaPT, but no experiments with alternative VLMs (e.g., SigLIP, OpenCLIP) are provided. This limits support for the portability claim to a forward-looking statement.

### Trivial
None.

## Nice-to-Haves

- An experiment replacing CLIP with a different VLM (e.g., SigLIP) would strengthen the portability claim.
- A more direct connection between the theoretical bound and the actual co-training dynamics (e.g., analyzing how the bound changes when CLIP prior is added) would be illuminating.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that SSL’s label dependency can be viewed as a failure of the pseudo label generator when labeled data is poor, and that a pretrained VLM with broad world knowledge can serve as a complementary source of supervision that is *not* coupled to the limited labels. The asymmetric-modalities co-training idea—using a vision-language model alongside a pure vision model—is a natural way to increase view independence (a classic co-training requirement) and yields richer representation exchange than homogeneous co-training. The entropy-based weighting scheme is also a practical way to dynamically balance two teachers with very different learning trajectories.

## Suggestions

- Clarify the co-pseudo label generation procedure in Section 3.3 by explicitly stating the confidence thresholding step and how all-zero vectors affect the final loss.
- Add a discussion of the potential overlap between CLIP’s training data and the evaluation benchmarks, and explain how the fine-grained experiments partially mitigate this concern.
- Consider adding a small experiment with an alternative VLM (e.g., OpenCLIP ViT-B/32) to support the portability claim.

## Score and Decision

Score: 8

Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>