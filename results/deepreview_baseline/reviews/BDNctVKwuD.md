## Summary
This paper identifies a theoretical limitation of HiResCAM interpretability: HiResCAM explanations are not uniquely determined due to softmax invariance, allowing arbitrary spurious shifts by a common matrix M. The authors propose ContrastiveCAMs, which are invariant to this shift and provide class-versus-class explanations. Using ContrastiveCAMs, they observe that networks often rely on non-core regions, motivating Core-Focused Cross-Entropy (CFCE), a modified loss that penalizes contributions from non-core regions while encouraging focus on core regions. Experiments on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC demonstrate improved feature alignment and interpretability metrics.

## Strengths
- **Theoretical contribution identifying a genuine limitation of HiResCAM**: Theorem 3.2 formally proves that HiResCAM explanations are not uniquely determined due to softmax invariance, which is a non-trivial and previously unrecognized flaw in a widely-used interpretability method. This is a clean, well-motivated theoretical result.
- **Principled connection between interpretability and training**: The paper does not merely propose a new interpretability method; it leverages the theoretical properties of ContrastiveCAMs (Proposition 4.1) to derive a training loss (CFCE) that directly addresses feature misalignment. This creates a tight coupling between the explanation method and the training objective.
- **Strong empirical results on feature alignment**: The IoU improvements on Hard-ImageNet (from ~18% GradCAM IoU to ~89-93% ContrastiveCAM IoU) and Oxford-IIIT Pets (from ~78% to ~93% IoU with KL regularization) are substantial and demonstrate that the method genuinely changes what the model attends to, not just the explanation method.
- **Demonstration of practical applicability with approximate masks**: The experiments showing competitive performance with SAM-generated masks and bounding boxes (Section 5.2) address a key practical concern—that ground-truth core masks may not always be available.

## Weaknesses
### Fatal
None.

### Major
- **The paper does not adequately address the circularity concern**: The primary evaluation metric (IoU) measures alignment between ContrastiveCAM explanations and core-region masks. However, the CFCE loss is explicitly designed to make ContrastiveCAMs match these masks. The high IoU scores may largely reflect that the training objective directly optimizes for this metric, rather than indicating that the model has learned genuinely better features. The paper would benefit from evaluation on independent metrics that are not directly optimized by the loss, such as out-of-distribution generalization or robustness to spurious correlations beyond the provided masks.
- **Limited comparison to existing feature alignment methods**: The paper compares only against CORM and DFR on Hard-ImageNet, but there is a broader literature on feature alignment, including methods based on saliency regularization (Ismail et al., 2021), masking strategies (Aniraj et al., 2023), and invariant risk minimization (Arjovsky et al., 2020). The paper would be stronger with comparisons to a wider set of baselines, particularly those that also use region masks during training.
- **The accuracy drop on Hard-ImageNet is not sufficiently discussed**: CFCE reduces un-ablated accuracy from 94.25% to 90.53%, and CFCE+KL to 90.35%. While the paper frames this as a trade-off, the magnitude of the drop (~4 percentage points) is significant and the paper does not provide a thorough analysis of whether this is acceptable or how it might be mitigated. The claim that the method "primarily extracts predictive performance from core image regions" is weakened by the fact that overall performance also drops substantially.

### Minor
- **The paper's notation and presentation are sometimes overly complex**: For example, Proposition 4.2 and Remark 4.3 essentially restate the same decomposition in different forms, which adds redundancy without clarity. The derivation from Proposition 4.2 to Definition 4.5 could be more streamlined.
- **The KL regularization term (Definition 4.7) introduces three hyperparameters (λ₁, λ₂, λ₃) without systematic ablation**: The paper reports results with specific values but does not analyze sensitivity to these choices, which is important for practical adoption.
- **The PASCAL VOC segmentation results are presented as a bar chart without numerical values or error bars**: This makes it difficult to assess the statistical significance of the improvements claimed.

### Trivial
- The paper uses "ContrastiveCAMs" and "ContrastiveCAM" interchangeably; consistency would improve readability.

## Nice-to-Haves
- An analysis of what types of spurious correlations are most effectively suppressed by CFCE versus what remains challenging (e.g., background textures vs. object co-occurrence).
- A discussion of the computational overhead of computing ContrastiveCAMs during training, since this requires computing HiResCAMs for all classes at each training step.
- An investigation of whether the benefits of CFCE transfer to transformer-based architectures, given that the paper focuses on ConvNets.

## Novel Insights
The key insight is that the softmax function's invariance to constant shifts creates a fundamental ambiguity in HiResCAM explanations, and that this ambiguity can be resolved by considering pairwise differences between class explanations (ContrastiveCAMs). This is a genuinely novel theoretical observation about a widely-used interpretability method. The further insight—that this corrected explanation can be directly integrated into the training loss to enforce feature alignment—is a natural but non-trivial extension that bridges interpretability and representation learning in a principled way. The paper demonstrates that interpretability methods are not just diagnostic tools but can serve as differentiable training signals.

## Suggestions
1. Add an evaluation on an independent metric that is not directly optimized by CFCE, such as accuracy on a test set with novel spurious correlations, or performance on a downstream task where core-region masks are not available.
2. Compare against a broader set of feature alignment baselines, particularly those that use masking or saliency regularization during training.
3. Provide a more thorough analysis of the accuracy-IoU trade-off, including experiments that vary the strength of the CFCE term to characterize the Pareto frontier.
4. Include a sensitivity analysis for the KL regularization hyperparameters (λ₁, λ₂, λ₃).

## Score and Decision
The paper makes a clear theoretical contribution (identifying and fixing a flaw in HiResCAM) and demonstrates a novel, principled approach to feature alignment. The empirical results are strong on the metrics that are directly targeted. However, the circularity concern in evaluation and the limited comparison to existing methods prevent this from being a top-tier paper. The work is solid and should be accepted, but with room for improvement.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>