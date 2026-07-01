## Summary

This paper proposes MoRE (Mixture of Remapping Experts), a training-free framework for feature-level machine unlearning. The method relaxes erasure of forget-class prototypes by (i) first projecting features into a prototype-orthogonal (PO) space to prevent collateral damage to remain-class representations, (ii) remapping forget prototypes onto remain prototypes (instead of merely erasing them), and (iii) using a mixture of experts with a stochastic router to scatter forget features across multiple remain prototypes, thereby breaking residual cohesive structure. Extensive experiments on image classification (CIFAR, Tiny-ImageNet, ImageNet) and concept unlearning in Stable Diffusion show that MoRE preserves utility, achieves near-zero forget accuracy under knowledge retention probing, and does so with orders-of-magnitude lower cost than training-based baselines.

## Strengths

- **Addresses an important limitation of prior work**: The paper clearly identifies that existing feature-level unlearning methods (e.g., ESC) leave forget features cohesive and separable in latent space, making them recoverable via linear probing. The remapping strategy directly tackles this residual structure.
- **Novel and well-motivated technical design**: The combination of prototype-orthogonal projection (to decouple forget/remain subspaces) and remapping (to disperse forget features) is original and founded on a clear observation (high cosine similarity between class prototypes). The use of concept-wise activation means as prototypes yields a practical, training-free procedure.
- **Strong empirical performance on the KD task**: Under the KR evaluation (linear probing), MoRE achieves forget accuracy near random-guess levels while maintaining remain accuracy close to the original model. It consistently outperforms training-based baselines across CIFAR-10/100 and Tiny-ImageNet, often with negligible variance.
- **Efficiency and scalability**: The method requires only a single forward pass for prototype collection, involves only lightweight linear algebra for the unlearning operation, and has O(dk) memory cost (independent of dataset size). Figure 5 confirms that MoRE completes unlearning in <10 seconds with <600 MB GPU memory, far cheaper than retraining or existing training-free alternatives with SVD on full forget matrices.

## Weaknesses

### Fatal
None.

### Major
- **Limited evidence for the benefit of multiple experts**: The core motivation of MoRE is that multiple remapping experts outperform a single remapping expert. Yet in Table 1, the difference between **Remap** (single expert) and **MoRE** (multiple experts) is marginal—HM changes from 95.38→95.23 (CIFAR-10), 95.39→95.03 (CIFAR-100), and 95.05→94.74 (Tiny-ImageNet) under the KR setting. These differences are within one standard deviation (where reported) and do not convincingly demonstrate that the MoRE routing is crucial. Figure 7 appears to show a large gap only when the number of experts is changed from 1 to 2, but that figure uses a different metric (HM defined differently?) and contradicts the Table 1 results for CIFAR-10. The paper should reconcile this inconsistency and provide stronger ablation evidence that MoRE scattering is significantly better than a single well-chosen remapping target.

- **Insufficient characterization of “irreversibility”**: The paper claims that MoRE makes unlearning “irreversible at the feature level,” but the only attacks tested are linear probes with a single learning rate (lr=0.1) and a limited set of learning rates in the appendix. To earn the “irreversible” claim, the evaluation should include stronger recovery attacks (e.g., adversarial fine-tuning, non-linear probes, or model inversion). Without such experiments, the irreversibility claim is supported only for a weak adversary. The authors should either soften the claim or provide more thorough probing/fine-tuning experiments.

- **Sensitivity to target remapping class**: Table 5 shows that the HM (KR setting) varies from 66.75 to 69.78 (excluding class 9) depending on which remain class is chosen as the remapping target for the forget class. This indicates that the method is somewhat sensitive to the choice of target, but the paper does not discuss how to select targets reliably. A practitioner would need guidance on target selection, and the potential failure cases (e.g., class 9 in CIFAR-10) should be explained.

### Minor
- **Clarity of the mathematical exposition**: The derivation from Eq. (3) to Eq. (5) is dense and the role of the complement-space projection is not fully motivated. While the paper mentions a “skip connection,” the notation \( (\mathbf{I} - \mathbf{P}\mathbf{D})\mathbf{z} \) is not justified as resulting in a full-rank transformation. A short intuitive explanation or a diagram of the linear operators would help readability.

- **Diffusion model evaluation is preliminary**: The diffusion experiments demonstrate that MoRE can be applied out-of-the-box, but the quantitative results (Table 2) are not uniformly better than existing training-free methods (e.g., LPIPS_f for Van Gogh is 0.33 vs. ESD’s 0.4, but ESD requires training). The qualitative example in Figure 4 is compelling, but the paper should report results on more than two forget styles and include additional metrics (e.g., FID, CLIP score) to fully assess utility.

- **Metric definition reconciliation**: The paper defines HM as Harmonic Mean in §B.3, yet Figure 7 labels HM as “Hit Rate” and shows a different scale. This mismatch confuses the ablation analysis. The authors should ensure that all HM references use the same definition.

### Trivial
None significant.

## Nice-to-Haves

- A theoretical justification for why prototype-orthogonal projection preserves utility, perhaps showing that the condition number of the feature covariance is reduced.
- Ablation experiments with non-linear probes (e.g., a two-layer MLP) to further substantiate the irreversibility claim.
- Demonstration on instance-wise unlearning (already included in Table 4 for CIFAR-10), but the paper could include results on larger datasets (e.g., Tiny-ImageNet instance-wise) and compare more MIA baselines.

## Novel Insights

The paper’s key insight is that **remapping** (redirecting forget prototypes to remain prototypes) is superior to **erasing** (zeroing out directions) for feature-level unlearning. Erasing leaves a hole in the feature space that linear probes can exploit; remapping instead fills that hole by aligning forget features with remain distributions. The prototype-orthogonal projection ensures that this remapping does not distort remain prototypes, a problem that plagued earlier subspace-erasure methods. The additional MoE-inspired scattering is a natural extension to further spread forget features, though the empirical benefit over a single remapping target is modest in the current evaluation.

## Suggestions

1. Provide a direct ablation comparing MoRE (stochastic router) with a single-expert version on the same KR metric used in Table 1. Clarify the discrepancy between Figure 7 and Table 1.
2. Evaluate against a stronger recovery adversary: fine-tune the full classification head or the last few layers of the feature extractor, not just a linear probe, and measure forget accuracy recovery.
3. For the diffusion experiments, include a wider range of forget concepts and report a user study or a more comprehensive set of generative metrics (e.g., FID on remain classes, CLIP alignment).
4. Discuss guidelines for selecting remapping targets, especially when remain classes are correlated with the forget class.

## Score and Decision

I recommend **Borderline Accept**. The paper tackles a well-motivated problem, proposes a clever training-free method, and shows clear advantages over ESC and training-based baselines on standard benchmarks. However, the central claim of “irreversibility” is only partially supported, and the improvement from the MoRE routing component remains unconvincing given the small gains over a single remapping expert. The paper would benefit from stronger recovery attacks and a reconciliation of the ablation inconsistencies before acceptance. Nevertheless, the core idea (remapping + orthogonalization) is novel, efficient, and likely to be impactful.

**Score**: 6

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>