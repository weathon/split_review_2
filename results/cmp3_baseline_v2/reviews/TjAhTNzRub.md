## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning. The method introduces three key innovations: (1) prototype-orthogonal projection to decorrelate forget and remain prototypes before erasure, preserving utility; (2) remapping forget prototypes into remain prototypes via mixture-of-experts to break the cohesive-separable structure of forget features, making unlearning irreversible; and (3) efficient activation-mean prototypes that achieve linear computational complexity and constant memory. Experiments across CIFAR-10, CIFAR-100, Tiny-ImageNet, and ImageNet demonstrate state-of-the-art performance in both standard unlearning metrics and the Knowledge Retention (KR) metric, while also showing applicability to concept unlearning in diffusion models.

## Strengths

- **Novel and well-motivated approach to irreversibility**: The paper identifies a critical limitation of existing feature-level unlearning methods—that forget features remain cohesive and separable in latent space, making them recoverable via fine-tuning. The remapping strategy that scatters forget features across multiple remain prototypes is a principled solution to this problem, and the t-SNE visualizations (Figure 1) convincingly demonstrate the effect.

- **Strong empirical results across multiple settings**: MoRE consistently achieves the best or near-best performance across all datasets and metrics, often surpassing training-based methods that require orders of magnitude more compute. The results on the KR metric are particularly striking—MoRE keeps forget accuracy at random-guess levels while existing baselines show substantial recovery.

- **Elegant theoretical formulation**: The prototype-orthogonal projection (Section 3.1) is mathematically sound and well-justified. The derivation from the observation that forget and remain prototypes are highly correlated (Figure 3) to the pseudoinverse construction is clear. The extension from erasing to remapping (Equation 6) is a natural and clever generalization.

- **Computational efficiency**: The method requires only a single forward pass and lightweight linear algebra, achieving unlearning in under 10 seconds with less than 200 MB GPU memory on CIFAR-10/100. This is a significant practical advantage over training-based methods.

- **Broad applicability**: The paper demonstrates effectiveness on class-wise unlearning, random data forgetting, and concept unlearning in diffusion models, suggesting the framework generalizes beyond the primary image classification setting.

## Weaknesses

### Major

- **Limited evaluation of irreversibility claims**: The paper's central claim is "irreversible feature-level unlearning," yet the only evidence for irreversibility is the KR metric (which measures forget accuracy after linear probing) and the t-SNE visualization. A more thorough evaluation would include: (1) fine-tuning attacks that go beyond linear probing (e.g., full model fine-tuning on forget data), (2) membership inference attacks specifically designed to detect residual knowledge, and (3) quantitative measures of feature-space separability (e.g., centroid distance, Fisher discriminant ratio). Without these, the claim of "irreversibility" is not fully substantiated.

- **Missing details on the diffusion model experiments**: The diffusion model results (Table 2, Figure 4) are presented as a significant contribution, but the methodology is described in only one paragraph. Critical details are missing: How exactly are prototypes constructed from tokenized prompts? How is the remapping applied to cross-attention layers? What is the exact architecture modification? The paper states it is applied "entirely out of the box" but this is unclear given the need to modify cross-attention layers. The appendix is stripped, so these details are unavailable for evaluation.

- **The "mixture of experts" terminology is misleading**: The paper uses MoE terminology, but the actual mechanism is fundamentally different from standard MoE. The "experts" are not learned sub-networks but rather fixed linear remapping operators. The "router" is either stochastic (random assignment) or a simple linear layer. This is more accurately described as "multiple remapping heads" or "ensemble remapping." The connection to MoE is superficial and may confuse readers.

- **Incomplete ablation of the remapping mechanism**: The ablation study (Table 3) compares "Erase" vs "Remap" with and without PO projection, but does not isolate the effect of the remapping itself. The "Erase" baseline without PO is essentially ESC, but the "Erase with PO" is a new method that is not compared to any existing baseline. The paper would benefit from a more systematic ablation that isolates: (1) PO projection alone, (2) erasing alone, (3) remapping alone, and (4) the full MoRE.

### Minor

- **The KR metric definition is unclear**: The paper mentions KR as a "feature-level unlearning performance" metric but does not clearly define it in the main text (referring to Appendix B.3, which is stripped). The results tables show "KR setting: lr = 0.1" but it's not clear what this means or how it relates to the standard evaluation.

- **Sensitivity to target remapping class is not adequately explained**: Table 5 shows that different target classes yield different HM values (ranging from 15.24 to 66.89 in the KR setting), but the paper only notes "mild preference" without analysis of why certain targets work better. This is a significant variance that deserves investigation.

- **The stochastic router vs. conditional router comparison is incomplete**: Table 6 shows that trained routers (MoRE-P-T-B) can outperform the stochastic router, but the paper adopts the stochastic router as default without a clear justification beyond "compute efficiency." Given that the trained router achieves better HM on CIFAR-10, the trade-off should be discussed more thoroughly.

### Trivial

- Figure 7's x-axis is labeled "Number of experts" but the values range from 0.2 to 0.8, which is inconsistent. This appears to be a plotting error.

## Nice-to-Haves

- A theoretical analysis of why remapping prevents recovery via fine-tuning would strengthen the paper. Currently, the argument is empirical (t-SNE visualization and KR metric).
- An analysis of the method's behavior under different forget set sizes (e.g., 1%, 5%, 20% of classes) would be useful for practitioners.
- A discussion of potential failure cases or limitations (e.g., when prototypes are not well-separated, or when the number of forget classes is large relative to remain classes).

## Novel Insights

The key insight is that existing feature-level unlearning methods (like ESC) only erase the subspace associated with forget data but leave the forget features still forming a cohesive cluster in the remaining subspace. This residual structure makes unlearning reversible. The paper's novel contribution is recognizing that active remapping—redirecting forget features into the distribution of remain features—breaks this cohesive structure and makes recovery fundamentally harder. The use of multiple remapping experts to scatter forget features across different remain prototypes is a clever extension that further disrupts any residual structure. This insight about the importance of destroying feature-level structure (not just removing information) is a meaningful conceptual advance for the unlearning field.

## Suggestions

1. Provide a more rigorous evaluation of irreversibility, including fine-tuning attacks with varying amounts of forget data and quantitative measures of feature-space separability (e.g., silhouette score, Davies-Bouldin index) before and after unlearning.

2. Clarify the diffusion model adaptation with full methodological details, including how prototypes are constructed from text prompts and how the remapping is applied to cross-attention layers.

3. Rename the "mixture of experts" terminology to something more accurate, such as "multi-head remapping" or "ensemble remapping," to avoid confusion with standard MoE architectures.

4. Add a systematic ablation study that isolates each component (PO projection, erasing, remapping, multiple experts) and reports their individual contributions to both utility and irreversibility.

5. Investigate and explain why certain target remapping classes perform significantly worse than others (Table 5), as this could reveal important limitations of the method.

## Score and Decision

The paper presents a novel, well-motivated, and empirically strong approach to feature-level unlearning. The core ideas (prototype-orthogonal projection and remapping) are elegant and effective. The empirical results are convincing across multiple datasets and architectures, and the computational efficiency is a significant practical advantage. However, the central claim of "irreversibility" is not fully substantiated with sufficient evaluation, and the diffusion model experiments lack methodological detail. These issues are addressable but currently weaken the paper's contribution.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>