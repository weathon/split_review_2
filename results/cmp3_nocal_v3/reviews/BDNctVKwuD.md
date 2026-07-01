Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper makes two primary contributions: (1) **ContrastiveCAM**, which identifies and removes a softmax-induced non-uniqueness in HiResCAM explanations by taking pairwise differences of class-level HiResCAMs, and (2) **Core-Focused Cross-Entropy (CFCE)**, a loss function that leverages ContrastiveCAMs to penalize the model's use of non-core image regions during training. The paper provides theoretical results (Theorems 3.2, 3.5, Proposition 4.1, Theorem 4.6) and empirical evaluations on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC showing that CFCE-trained models rely substantially more on core (target-relevant) regions.

## Strengths

1. **Clean theoretical identification of a genuine limitation in HiResCAM (Theorem 3.2).** The observation that adding the same matrix M to all class-level HiResCAMs preserves the softmax probability prediction is mathematically sound and, to my knowledge, novel in the CAM literature. ContrastiveCAM (pairwise differences) is a natural and correct resolution (Theorem 3.5).

2. **Proposition 4.1 provides a non-trivial bridge between ContrastiveCAMs and softmax probabilities.** Showing (Eq. 11) that class probabilities can be expressed as a direct function of ContrastiveCAMs is a stronger connection than standard CAM-family methods offer, and it provides the theoretical foundation for using ContrastiveCAMs as a training signal.

3. **The core-region ablation results on Hard-ImageNet are impressive and indicative of real behavioral change.** In Table 2, CFCE reduces accuracy under gray-mask core-region ablation from 75.94% (CE) to 41.78%, and RFS improves from -0.18 to +0.224. ContrastiveCAM IoU jumps from 30.27% (CE w/ Arch) to 89.22% (CFCE). These are large, consistent differences across multiple metrics, suggesting the method genuinely alters what the model attends to.

## Weaknesses

### Fatal
None.

### Major

1. **Underspecified gradient computation for the CFCE loss.** The CFCE loss (Definition 4.5, Eq. 15) is defined in terms of ContrastiveCAMs, which are built from HiResCAMs. HiResCAM (Eq. 2) requires computing gradients of logits *with respect to the feature maps* A. During training, the loss must be backpropagated through model parameters, which — depending on implementation — would require differentiating through this gradient computation, yielding second-order gradients (or requiring the HiResCAM to be detached from the computation graph). The paper is completely silent on how this is handled. There is no discussion of whether HiResCAM is detached (treated as a constant during backprop), whether higher-order gradients are explicitly computed (e.g., using `create_graph=True`), or what the resulting computational overhead is. Since the method demonstrably works (the models are successfully trained), the issue is not that the method is impossible, but that the paper omits a critical implementation detail that determines reproducibility and practical feasibility. This should be addressed in the main text (not deferred to an appendix, which in any case is stripped by the parser).

2. **Primary alignment metric (ContrastiveCAM IoU) is partially circular with the training objective.** CFCE explicitly trains to suppress non-core ContrastiveCAM contributions and encourage core-region ContrastiveCAM contributions. Measuring ContrastiveCAM IoU against ground-truth masks therefore primarily confirms that the optimization works — it does not independently validate that the learned features are of higher quality. This is most visible in Table 2, where ContrastiveCAM IoU jumps from 30.27% to 89.22% under CFCE, while GradCAM IoU (a less circular metric) only moves from 16.25% to 18.88%. The core-region ablation metrics (Gray Mask, Gray BBOX, Tile) and RFS are genuinely independent and provide the strongest evidence, but their validity would be strengthened by also reporting the downstream segmentation results (which are independent) with proper numerical values — currently only presented as a bar chart (Section 5.3) without means, standard deviations, or significance tests.

### Minor

3. **CFCE requires dense pixel-level mask supervision, which is a practical limitation the paper partially but incompletely addresses.** The CFCE loss (Eq. 15) requires binary masks H for every training image. The paper's SAM and bounding-box experiments (Section 5.2) show the method still works with weaker supervision, but IoU degrades substantially (e.g., Oxford Pets binary valid IoU drops from 92.72% with GT masks to 83.54% with SAM masks for CFCE+KL). The paper does not discuss regimes where even bounding boxes are unavailable (i.e., most real-world classification tasks), nor does it quantify how the method's benefits decay with mask quality.

4. **No comparison against the simplest mask-guided baseline: masking the input to core regions during training.** A natural baseline is to train with standard cross-entropy but crop or mask the input so that only core regions are visible. If CFCE outperforms this baseline, it would provide direct evidence that the ContrastiveCAM-based loss adds value beyond merely removing non-core information at the input level. The current comparison set (CORM, DFR, CE w/ Arch) does not include this simple control.

5. **The three hyperparameters in the KL-regularized variant (λ₁, λ₂, λ₃ in Eq. 18) are introduced without any ablation or sensitivity study.** Three tunable hyperparameters with no analysis of how they interact or how they were chosen makes it difficult to apply the method to new datasets.

6. **Computational cost is not reported.** Training with CFCE requires computing gradients of logits w.r.t. feature maps at each training step. The paper should report wall-clock time per epoch, memory usage, and number of training steps relative to standard CE training, so practitioners can assess the practical overhead.

### Trivial

- The redundancy metric γ (Table 1) is reported but never discussed in relation to the experimental results (e.g., whether datasets with higher γ benefit more from ContrastiveCAM).

## Nice-to-Haves

- Provide exact numerical values (means and standard deviations) for the downstream segmentation bar chart in Section 5.3, and include statistical significance tests.
- The "CE can motivate feature misalignment" framing (Section 4.1 title) is technically accurate (CE is indifferent to region provenance, which enables misalignment in the presence of spurious correlations), but could be slightly softened to avoid giving the impression that CE *actively* promotes misalignment rather than simply failing to prevent it.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"The theoretical 'limitation' of HiResCAM has limited practical bite."** — Removed because the paper correctly identifies a genuine mathematical non-uniqueness (Theorem 3.2), and the ContrastiveCAM fix is mathematically sound. The critic's observation that "the practitioner has access to model weights" is true, but the paper's theoretical contribution stands on its own. The practical significance of the non-uniqueness is a matter of interpretation, not a flaw in the paper's reasoning.

2. **"CFCE requires dense mask supervision is a severe practical limitation."** — Removed because "severe" overstates the case. The paper explicitly addresses this limitation in Section 5.2 with SAM and BBOX experiments showing competitive results even with weaker supervision. The limitation is real but the paper acknowledges and investigates it, so it belongs at Minor severity, not as a structural criticism.

3. **"The claim that cross-entropy 'motivates feature misalignment' is overstated."** — The substance (CE is indifferent to region provenance) is correct and the section title uses "can motivate," which is appropriate. This is a semantic framing preference rather than a substantive weakness. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the gradient-computation reproducibility concern and the circularity of the primary IoU metric, but these are practical issues with the paper's presentation rather than novel analytical insights about the method itself.

## Suggestions

1. **In the main text, specify how the CFCE loss is backpropagated.** State explicitly whether the HiResCAM computation is detached from the computation graph during training (treating it as a constant for the backbone gradients) or whether higher-order gradients are used. If detached, explain the optimization implications; if not, discuss the computational overhead of Hessian-vector products.

2. **Add a simple baseline**: train with cross-entropy on inputs masked to core regions only. This isolates whether the ContrastiveCAM-based loss adds value beyond simply removing non-core information from the input.

3. **Report exact numerical values (mean ± std) for the downstream segmentation results** in Section 5.3, and include at least one statistical significance test to establish that the improvements are reliable.

4. **Add a hyperparameter sensitivity study** for λ₁, λ₂, λ₃ (Eq. 18), or at minimum state the values used and justify their selection.

5. **Report training time and memory overhead** of CFCE relative to standard CE, so practitioners can assess the practical cost.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>