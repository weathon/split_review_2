## Summary

This paper identifies a theoretical limitation of HiResCAM (non-uniqueness due to softmax invariance to a spurious shift matrix M), proposes ContrastiveCAMs that are invariant to this shift while providing class-versus-class explanations, and introduces Core-Focused Cross-Entropy (CFCE) that leverages core-region masks to suppress non-core feature contributions during training. Experiments on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC demonstrate substantially improved feature alignment (IoU) with modest accuracy trade-offs.

## Strengths

- **Rigorous theoretical framework connecting HiResCAM ambiguity to softmax invariance.** Theorem 3.2 formalizes the observation that HiResCAMs admit spurious shifts by any matrix M∈ℝ^{d₁×d₂}, and the construction of ContrastiveCAMs via pairwise differences cleanly removes this redundancy while yielding M-invariant explanations (Theorem 3.5). Proposition 4.1 further shows that softmax probabilities are precisely recoverable from ContrastiveCAMs, enabling the subsequent loss decomposition.

- **Strong empirical improvements in feature alignment.** On Hard-ImageNet, CFCE+KL improves GradCAM IoU from 16.25% to 51.52%, RFS from -0.23 to +0.236, and ContrastiveCAM IoU to 93.39%—transforming a model that actively relies on non-core regions into one that primarily uses core features. On Oxford-IIIT Pets, IoU improves from ~78% to ~93%. These are substantial and consistent improvements across datasets and classification settings (binary, multiclass, multilabel).

- **Practical considerations for real-world deployment.** The paper demonstrates that approximate masks from SAM and even coarse bounding boxes achieve competitive alignment (Table 3), addressing the practical concern that ground-truth core-region masks may be unavailable. The downstream segmentation improvements (Figure 4) further validate that core-focused backbones learn more transferable representations.

- **Clear theoretical motivation for the problem.** Proposition 4.2 provides a clean decomposition of cross-entropy into core and non-core contributions, showing that standard CE has no inherent preference for either, thus theoretically motivating the need for a modified loss.

## Weaknesses

### Fatal
None.

### Major

- **Significant accuracy trade-offs on Hard-ImageNet.** CFCE drops un-ablated accuracy from 94.25% to 90.53%, and even CE w/Arch drops to 93.69%. This ~4% absolute drop is substantial, particularly for a dataset that already represents a challenging subset of ImageNet. The paper should discuss whether this accuracy degradation is uniform across classes or concentrated in certain categories, and whether there exists a regularization regime that better trades off accuracy and alignment.

- **Evaluation metric inconsistency limits direct comparison.** The paper reports GradCAM IoU for all models (for consistency with prior work) but also ContrastiveCAM IoU only for core-focused models. Since ContrastiveCAMs are proposed in the same paper and their IoU is much higher (89-93% vs 51% GradCAM IoU), presenting only ContrastiveCAM IoU for the proposed method risks conflating the contribution of a better explanation method with better alignment. A fairer evaluation would compute ContrastiveCAM IoU for baseline models as well.

### Minor

- **Mask dependency.** The method fundamentally requires core-region annotations H, which creates a chicken-and-egg problem: if we already know where the target is, why not use that information directly in a segmentation or region-based approach? The paper partially addresses this with SAM and bounding box alternatives, but the sensitivity of performance to mask quality is not systematically studied (e.g., how does IoU degrade as mask noise increases?).

- **Limited baseline comparisons.** The baselines are restricted to CORM, DFR, and their combination. More recent feature alignment methods (e.g., those discussed in Gao et al. 2024 or Weber et al. 2023 surveys) would strengthen the comparison.

- **Hyperparameter sensitivity of KL regularization.** Definition 4.7 introduces three hyperparameters (λ₁, λ₂, λ₃) whose effects on the accuracy-alignment trade-off are not explored. A sensitivity analysis would be valuable.

### Trivial
None.

## Nice-to-Haves

- A Pareto frontier analysis plotting accuracy vs. IoU across different hyperparameter settings would make the accuracy-alignment trade-off more transparent.
- Analysis of whether ContrastiveCAM class-versus-class explanations reveal systematic patterns (e.g., which class pairs are most confounded and why).
- Extension discussion or preliminary experiments on vision transformers, since the single-layer classifier assumption (Eq. 1) applies broadly to modern architectures beyond ConvNets.

## Novel Insights

The paper's core novel insight—that cross-entropy loss decomposes into core and non-core contributions without inherent preference between them (Proposition 4.2)—provides a clean theoretical explanation for why convolutional networks learn shortcuts, particularly when targets are small relative to the image. This connects interpretability theory to the alignment problem in a principled way. The further observation (Section 4.1) that small targets lead models to preferentially learn non-core surrogates because they provide stronger gradients is a useful and practically relevant characterization of scale-sensitive shortcut learning.

## Suggestions

- Compute ContrastiveCAM IoU for all baseline models in Table 2 to enable a fully fair alignment comparison using the proposed explanation method.
- Add a table or figure showing the accuracy-IoU Pareto frontier by varying the λ₁ parameter in RCFCE.
- Discuss the practical scenario where core masks are noisy or partially incorrect—does the model gracefully degrade, or does incorrect masking cause significant harm?

## Score and Decision
The paper makes genuine contributions: the HiResCAM non-uniqueness result is clean if modest, ContrastiveCAMs are a useful interpretability tool, and Core-Focused CE achieves striking alignment improvements with theoretical grounding. The major concerns are the accuracy trade-off on Hard-ImageNet (not fully addressed) and the self-referential evaluation aspect. These prevent a higher score but do not invalidate the contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>