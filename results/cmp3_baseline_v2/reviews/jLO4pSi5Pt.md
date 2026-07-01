## Summary

This paper introduces Long-tailed Test-Time Adaptation (L-TTA), the first TTA method designed for Vision-Language Models under long-tailed test distributions. L-TTA comprises three co-designed components: Synergistic Prototypes (DPs and EPs) to enrich tail-class representations, learnable Rebalancing Shortcuts with a class re-allocation loss to dynamically balance prototypes, and Balanced Entropy Minimization (BEM) to mitigate head-class bias in entropy minimization. Extensive experiments on 15 datasets across three benchmarks (OOD, cross-domain, corruption) with varying imbalance ratios demonstrate that L-TTA consistently outperforms state-of-the-art TTA methods in both accuracy and macro-F1, while maintaining competitive efficiency.

## Strengths

- **Timely and well-motivated problem.** The paper correctly identifies that real-world test sets often exhibit long-tailed distributions, and existing TTA methods for VLMs (designed for balanced data) suffer from severe degradation. The two identified failure modes (Text-induced Tail Erosion and Modality-bias Amplification) are specific to VLM-based LT-TTA and provide a clear motivation for the proposed method.

- **Novel and principled methodology.** L-TTA’s three components (SyPs, RSs, BEM) are thoughtfully designed to address the unique challenges of LT-TTA for VLMs. The synergies between prototypes and shortcuts, the use of exclusionary prototypes to capture fine-grained inter-class information, and the theoretically motivated BEM loss represent a coherent and non-trivial integration of ideas.

- **Extensive and convincing experimental evaluation.** The paper evaluates on 15 datasets (OOD, cross-domain, corruption) with imbalance ratios of 10, 20, and 50, covering diverse distribution shifts. The consistent improvements over 12+ strong baselines (including SOTA methods like SCAP, DPE, TDA) across both accuracy and macro-F1 are compelling. Ablation studies isolate the contribution of each component, and additional analyses on backbones (ViT-L, ViT-H, SigLIP, MetaCLIP) demonstrate generalizability.

- **Efficiency is considered.** The paper reports time and memory costs, showing L-TTA is practical (1.45h, 1.89GB on ImageNet) while outperforming heavier methods. This strengthens the claim that the method can be deployed in realistic online settings.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Theoretical propositions in main text are incomplete.** Propositions 1 and 2 are central to motivating BEM, but the main text only states them and refers to Appendix A for proofs. While the appendix is not accessible, the main paper would benefit from a sketch of the proof or key intuition to make the theoretical claims self-contained. The current presentation relies heavily on the omitted proofs.

- **High hyperparameter sensitivity potential.** The method introduces several hyperparameters (λ₁, λ₂, η, β, K, θ) that require tuning. While ablation studies explore each individually, the combined sensitivity is not thoroughly investigated. The paper states default values but does not discuss how to set them in practice for new datasets without a validation set (a common challenge in TTA).

- **Construction of long-tailed test sets.** The long-tailed test sets are created by subsampling existing datasets to induce an exponential cardinality distribution. This is a standard approach, but it does not capture the full complexity of real-world long-tailed test streams (e.g., temporal correlations, evolving distributions). The paper would be strengthened by a discussion of this limitation or an experiment on a naturally long-tailed test set.

### Trivial
None.

## Nice-to-Haves

- A more detailed analysis of when and why the exclusionary prototypes (EPs) are most beneficial—e.g., in terms of class cardinality or domain shift severity.
- Visualization of the learned hyper-class vectors (experts) to provide intuitive insight into the rebalancing mechanism.

## Novel Insights

The key insight is that standard entropy minimization amplifies head-class bias in long-tailed TTA, and existing logit-adjustment strategies (from supervised LT learning) are incompatible with the unsupervised, online nature of TTA. The paper’s solution—introducing a penalty term weighted by prediction uncertainty to focus optimization on uncertain and tail classes—is a principled adaptation of EM to the LT setting. The use of exclusionary prototypes that store least-likely features for all classes (rather than just negative caches) and the load-balancing-inspired class re-allocation loss to distribute prototypes evenly across hyper-class experts are also novel and well-justified for the LT-TTA problem.

## Suggestions

1. Provide a brief proof sketch or intuitive explanation for Propositions 1 and 2 in the main text to make the theoretical contributions more accessible.
2. Consider including a small-scale experiment on a naturally long-tailed test stream (e.g., from iNaturalist or Places-LT) to complement the synthetic subsampling approach.
3. Discuss how to select hyperparameters in practice when no labeled validation set is available (e.g., by monitoring prototype statistics or adaptation stability).

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>