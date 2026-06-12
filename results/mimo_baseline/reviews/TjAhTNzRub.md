## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for irreversible feature-level machine unlearning. MoRE introduces prototype-orthogonal projection to decorrelate forget and remain prototypes, remapping of forget prototypes into remain prototypes to break feature-level separability, and a mixture-of-experts mechanism to scatter forget features across multiple remain prototypes for stronger irreversibility. Experiments span classification (CIFAR-10/100, Tiny-ImageNet, ImageNet) and concept unlearning in Stable Diffusion.

## Strengths

- **Genuine novelty in the PO projection and remapping formulation.** The prototype-orthogonal projection (Eqs. 2–5) is a principled solution to the well-identified problem of prototype correlation between forget and remain data. The empirical evidence in Fig. 3 (cosine similarity dropping from 1.0 to 0.52 for remain prototypes after ESC erasure) convincingly motivates this design. The progression from erasure to remapping (Eq. 6) and then to mixture-of-experts is logically coherent and well-motivated.

- **Compelling irreversibility results under the KR evaluation.** MoRE keeps forget accuracy near random guessing even after aggressive fine-tuning (lr=0.1), decisively outperforming all baselines including the retrain-from-scratch model. For instance, on CIFAR-100 under KR, MoRE achieves HM_f = 0.07 vs. Retrain's 52.96, demonstrating unlearning guarantees that exceed the traditional gold standard.

- **Training-free efficiency with broad applicability.** MoRE completes unlearning in under 10 seconds on CIFAR-10/100 with <200 MB GPU memory (Fig. 5), while outperforming training-based methods requiring orders of magnitude more compute. The successful, out-of-the-box application to Stable Diffusion concept unlearning (Table 2, Fig. 4) without any architecture-specific adaptation demonstrates real-world versatility.

- **Thorough ablation.** Table 3 clearly isolates the contribution of PO projection, erasing, remapping, and the full MoRE framework, providing strong evidence that each component is necessary.

## Weaknesses

### Fatal
None.

### Major

- **KR evaluation validity is insufficiently scrutinized.** The retrain-from-scratch baseline achieves D_{ft} = 72.90% on CIFAR-10 forget test data under KR fine-tuning—a model that *never saw* forget data "recovers" substantial accuracy. This raises the fundamental question of what the KR metric actually measures: is it probing residual forget knowledge, or is aggressive fine-tuning on remain data sufficient to reconstruct forget-class decision boundaries from shared features? The paper uses KR as its primary evidence for irreversibility but does not address this confound. This needs explicit discussion, ideally with analysis of what the retrain model's features look like after KR fine-tuning and whether the recovered accuracy is genuine knowledge recovery or an artifact of the evaluation protocol.

- **Limited attack diversity for irreversibility claims.** The paper's central claim is "irreversibility," but the evaluation relies almost exclusively on a single fine-tuning attack at lr=0.1. Other relevant attacks—linear probing of intermediate features, model inversion attacks, gradient-based attribution, membership inference, and varying fine-tuning hyperparameters—are absent. A more comprehensive adversarial evaluation is needed to substantiate the irreversibility claim, which is the paper's primary differentiator from prior work.

### Minor

- **Random data forgetting evaluation gap.** Table 4 only reports results for the single-expert "Remap" variant, not the full MoRE framework. Moreover, MoRE/Remap's MIA score (79.31) is worse than ESC (73.43), and the paper omits accuracy metrics for the MoRE row entirely. For a method claiming broad applicability, the random forgetting evaluation should include MoRE with its full pipeline and more comprehensive metrics.

- **Prototype computation via class means is a limitation worth acknowledging.** Using activation means as prototypes implicitly assumes unimodal, roughly spherical class distributions. For datasets with multi-modal intra-class structure, mean prototypes may be poor representatives. The paper mentions alternatives (clustering, factorization) but doesn't explore them or discuss when the mean assumption breaks down.

- **Diffusion experiments are limited.** The artistic style erasure evaluation covers only 2 of 10 artists (Van Gogh and Kelly McKernan). While qualitative results are compelling, evaluating across all 10 artists and multiple prompts per artist would provide more robust evidence. Additionally, no quantitative comparison of the semantic fidelity of generated images (e.g., CLIP similarity to the original prompt) is provided—only LPIPS-based metrics.

### Trivial
The x-axis label in Fig. 7 appears to represent a fraction rather than absolute expert counts, but the axis label is ambiguous.

## Nice-to-Haves

- A discussion section or appendix exploring when MoRE's assumptions might fail (e.g., highly entangled class features, long-tailed distributions) would improve the paper's completeness.
- Analysis of MoRE's robustness to varying fractions of forget classes (e.g., 5%, 20%, 50%) beyond the fixed 10% setting.
- Information-theoretic or formal analysis characterizing conditions under which remapping provides irreversibility guarantees.

## Novel Insights

The paper's central insight—that existing feature-level unlearning methods leave a cohesive-and-separable residual structure in the latent space that enables recovery—is well-supported by the t-SNE visualizations and quantitative evidence. The proposal to actively *remap* forget features into the remain distribution rather than merely *erasing* them represents a meaningful conceptual shift in feature-level unlearning. The extension to mixture-of-experts for scattering remapped features is creative and well-motivated, even if the stochastic routing is simple. The observation that prototype correlation between forget and remain classes degrades naive erasure (Fig. 3) is a genuine empirical contribution that will be useful beyond this specific method.

## Suggestions

- Add discussion of the KR evaluation confound (retrain baseline high forget accuracy) and either justify why it doesn't undermine the metric or refine the protocol.
- Expand adversarial evaluation with diverse attack types to strengthen irreversibility claims.
- Report full MoRE results (not just Remap) for random data forgetting in Table 4.

## Score and Decision

The paper presents a novel and technically sound framework with three well-motivated components that collectively advance feature-level unlearning. The experimental results are extensive and compelling, particularly the KR evaluation and diffusion model extension. However, the central claim of "irreversibility" rests on a narrow attack evaluation and a KR metric whose validity is not sufficiently interrogated (as evidenced by high forget accuracy even for the retrain baseline). These gaps prevent the paper from fully substantiating its strongest claims. The contribution is above the ICLR median and warrants acceptance with the expectation that the authors address the evaluation concerns.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>