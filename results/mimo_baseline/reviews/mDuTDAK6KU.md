## Summary

The paper proposes KOALA, an adversarial detection method based on the disagreement between two complementary nearest-prototype classifiers—one using KL divergence (sensitive to dense, low-amplitude perturbations) and one using an L0-based metric (sensitive to sparse, high-impact perturbations). The authors provide a formal proof of correctness showing that under sufficient inter-class prototype separation, no single norm-bounded perturbation can simultaneously fool both metrics, guaranteeing detection. The method requires only lightweight fine-tuning on clean images and is evaluated on ResNet-18/CIFAR-10 and CLIP ViT-B/32/Tiny-ImageNet.

## Strengths

- **Genuine theoretical contribution with empirical validation.** The paper provides a formal proof (Theorem 1) that under stated assumptions, adversarial perturbations must cause disagreement between the two metrics. This is validated empirically: on theorem-compliant samples, recall is 1.0 across all settings (Table 1), which is compelling evidence that the theory holds in practice.

- **Well-motivated metric design with thorough ablation.** The choice of KL + L0 is motivated by the observation that energy-bounded attacks are either dense or sparse. Table 2 ablates four metric combinations, and KL+L0 achieves the best F1 on ResNet/CIFAR-10, supporting the complementary-metric hypothesis. Tables 3 and 4 further show that KL+L0 fine-tuning yields the strongest adversarial accuracy on ResNet.

- **Lightweight and practical.** The method requires no adversarial training, no architectural changes, and only clean-image fine-tuning. Clean accuracy degradation is minimal (95.16% → 94.78% on ResNet), and the adversarial accuracy under PGD improves substantially (45.5% → 57.32% at ε=2/255), suggesting the fine-tuning genuinely improves robustness beyond just detection.

## Weaknesses

### Fatal

None.

### Major

- **No comparison with existing adversarial detection methods.** The paper surveys a rich landscape of detection methods (MagNet, Mahalanobis, feature squeezing, NIC, LID, CADet, etc.) but does not compare KOALA against any of them. Without baseline comparisons, it is impossible to assess whether KOALA's precision of 0.94 / recall of 0.81 on ResNet/CIFAR-10 represents an improvement, a regression, or parity with existing work. This is a significant omission for a detection paper.

- **Limited experimental scope.** Only two model/dataset combinations are tested, both on relatively small-scale benchmarks (CIFAR-10 with 10 classes, Tiny-ImageNet with 200 classes). Only ℓ∞ attacks are evaluated. The paper claims the method is a "plug-and-play solution for existing models and various data modalities" but provides no evidence for modalities beyond images or for larger-scale settings (e.g., full ImageNet, NLP tasks).

- **Theoretical guarantee applies to a minority of samples, especially for CLIP.** On CLIP/Tiny-ImageNet, only ~10% of test samples are theorem-compliant (Table 1: 510/5000 and 556/5000). The paper does not adequately discuss what guarantees, if any, exist for the remaining ~90% of non-compliant samples, where performance degrades substantially (e.g., recall drops from 1.0 to 0.80-0.84 on CLIP). This significantly limits the practical impact of the theoretical contribution.

### Minor

- **Sensitivity to the L0 threshold τ is not analyzed.** The L0 metric (Eq. 2) depends on a threshold τ set to 0.75. No sensitivity analysis is provided, and it is unclear how robust the method is to this choice or how it should be selected in practice.

- **The "plug-and-play" characterization is slightly misleading.** The method requires fine-tuning the backbone encoder, which modifies the model's representations. This is lighter than adversarial training but is not truly plug-and-play (which would imply operating on a frozen, unmodified model).

- **CLIP results are inconsistent with the paper's narrative.** On CLIP/Tiny-ImageNet, KL+L0 does not clearly outperform other combinations: L0-only and KL-only achieve higher adversarial accuracy (Table 4), and KL+L0+Cosine achieves higher detection F1 (Table 2). The paper acknowledges this but the explanation (that high detection rate comes from broken classification rather than principled detection) somewhat undermines the claim that KL+L0 is the universally optimal combination.

### Trivial

None.

## Nice-to-Haves

- Comparison against at least 2-3 established detection baselines (e.g., Mahalanobis, MagNet, feature squeezing) on the same experimental setup.
- Experiments on at least one additional modality (e.g., text classification with a language model) to support the modality-agnostic claim.
- Analysis of the fraction of theorem-compliant samples as a function of embedding dimensionality, number of classes, or fine-tuning duration.

## Novel Insights

The paper's core novel insight is that the geometry of norm-bounded perturbation sets naturally decomposes into dense and sparse regimes, and that two complementary metrics (KL for dense, L0 for sparse) can be combined via disagreement to provably detect adversarial inputs. The formal proof that these two "stability bands" are mutually exclusive under energy constraints is a genuinely novel theoretical observation that, if the assumptions hold, provides a principled foundation for ensemble-based detection. The empirical finding that cosine similarity conflicts with KL/L0 objectives (Tables 3-4), degrading robustness, is also a useful practical insight about metric compatibility in embedding space design.

## Suggestions

- Add comparison experiments against at least 2-3 existing detection baselines (e.g., Mahalanobis distance detector, MagNet, feature squeezing) on the same ResNet/CIFAR-10 and CLIP/Tiny-ImageNet setups.
- Provide a sensitivity analysis for the L0 threshold τ and the smoothness parameter φ.
- Discuss more explicitly what practical guarantees (if any) exist for non-compliant samples, and whether the fraction of compliant samples can be increased through training or architectural choices.
- Consider adding experiments on a larger-scale dataset (e.g., ImageNet-1K) or a different modality to strengthen the generalizability claims.

## Score and Decision

The paper presents a genuinely novel theoretical framework for adversarial detection via metric disagreement, with a formal proof of correctness that is cleanly validated empirically. However, the complete absence of comparison with existing detection methods, the limited experimental scope (2 small datasets, 1 attack norm), and the fact that the theoretical guarantee covers only a small fraction of samples (especially for CLIP) significantly weaken the practical contribution. The theory is the paper's strongest asset, but the experimental evaluation is not yet sufficient to establish the method's value relative to the existing literature.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: Reject