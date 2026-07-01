## Summary

This paper first identifies a theoretical limitation of HiResCAM: due to softmax invariance, HiResCAM explanations are not uniquely determined and admit an arbitrary additive shift \(M\) that leaves the predicted probability unchanged. To remove this redundancy, the authors propose ContrastiveCAMs (differences between HiResCAMs for different classes), which are invariant to the spurious shift and provide granular class-versus-class explanations. Using ContrastiveCAMs for analysis, they observe that networks often rely on non-core regions. To address this misalignment, they propose Core-Focused Cross-Entropy (CFCE), a modification of cross-entropy that penalizes contributions from non-core regions while retaining contrast in core regions. Experiments on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC show significant improvements in IoU between model attention and core masks, often with modest accuracy trade-offs, and demonstrate that the method works with approximate masks (e.g., from SAM or bounding boxes).

## Strengths

- **Clear theoretical identification of a fundamental flaw in HiResCAM.** Theorem 3.2 and its surrounding discussion rigorously show that HiResCAM explanations are not uniquely determined—they can be arbitrarily shifted by an additive matrix \(M\) without changing the predicted probability. This is a concise and original observation that improves understanding of CAM-based interpretability.

- **ContrastiveCAM is a principled fix.** By taking differences between class HiResCAMs, ContrastiveCAM removes the redundancy (\(M\)-invariance, Theorem 3.5) and provides class-versus-class granularity that reveals spurious contributions hidden by standard HiResCAM. The analysis of non-core contributions (Table 1, Figure 2) is convincing and motivates the subsequent training modification.

- **Core-Focused Cross-Entropy is a novel and well-motivated training objective.** The loss is derived from a rigorous decomposition of cross-entropy in terms of ContrastiveCAMs (Proposition 4.2) and is shown to be consistent with core-constrained risk minimization (Theorem 4.6). The KL regularization further encourages full coverage of core regions.

- **Strong experimental results across multiple datasets and settings.** The method achieves dramatic improvements in IoU scores on Hard-ImageNet (from 18.44 to 89.22), Oxford Pets (from 78.37 to 92.72), and PASCAL VOC (from 44.50 to 85.39). The authors also demonstrate robustness to mask quality (SAM, bounding boxes) and show beneficial downstream effects on segmentation tasks. The inclusion of confidence intervals adds rigor.

## Weaknesses

### Major

- **The core-focused loss is heuristic and its impact on optimization is not deeply analyzed.** The loss flips the sign of non-core ContrastiveCAM contributions and applies absolute value, which is a specific heuristic. While Theorem 4.6 shows consistency with core-constrained risk, it does not characterize the loss landscape, convergence properties, or potential detrimental effects (e.g., when a non-core region is genuinely useful or when masks are noisy). The paper could benefit from a more thorough empirical analysis of the regularization strength \(\lambda_1\) and the effect of mask quality on the loss.

### Minor

- **The theoretical redundancy in HiResCAM is partly a consequence of the softmax invariance, which is a well-known property.** The paper’s contribution lies in formalizing it for HiResCAM and proposing a fix, but the core insight (logits are not identifiable from probabilities) is not entirely new. The conceptual novelty is more in the application to CAMs and the concrete ContrastiveCAM construction.

- **Accuracy trade-offs are not deeply discussed.** On Hard-ImageNet, unablated accuracy drops from ~94% to ~90%. While the paper frames this as a necessary trade-off for alignment, the implications for deployment in high-stakes settings (where accuracy is paramount) are not addressed. The paper could include a Pareto analysis of accuracy vs. IoU.

- **The method requires externally provided core-region masks.** Although the authors show competitive performance with SAM-generated masks and bounding boxes, the reliance on such masks is a limitation. The paper does not discuss scenarios where core regions are ambiguous or multi-modal.

### Trivial

- Some figure captions (e.g., Figure 1, Figure 3) contain repeated text from the main body, which is a minor presentation issue.

## Nice-to-Haves

- An analysis of the effect of varying the KL regularization strength \(\lambda_1\) on the accuracy-IoU trade-off.
- A discussion of whether the method could be extended to other CAM variants (e.g., GradCAM) or to transformer-based architectures.
- A comparison with other loss-based alignment methods (e.g., saliency regularization) to contextualize the improvement.

## Novel Insights

Beyond the paper’s own contributions, a genuinely novel observation is that **the softmax invariance, typically viewed as a harmless property of the output layer, directly induces an arbitrary additive ambiguity in the spatial explanation maps of CAM-based methods**. This connects a standard architectural detail to a previously unappreciated weakness in interpretability, and the proposed solution (contrastive differencing) is a clean and principled way to recover invariance. The subsequent use of this invariant representation to design a training loss that directly penalizes non-core contributions is a natural and effective extension that bridges interpretability and feature alignment.

## Suggestions

- Provide a sensitivity analysis for the KL regularization coefficient \(\lambda_1\) and the scaling parameters \(\lambda_2, \lambda_3\). A plot showing IoU vs. accuracy for a sweep would help practitioners choose the appropriate trade-off.
- Include an ablation where the loss uses only core-region H contributions (ignoring non-core penalty) to isolate the effect of the non-core absolute-value term.

## Score and Decision

This paper presents a clear theoretical advance (identifying and resolving a non-uniqueness problem in HiResCAM) and a practically effective method for feature alignment supported by thorough experiments. The weaknesses (heuristic nature of the loss, reliance on masks) are not fatal and are offset by the novelty and experimental strength. The paper is well-written and makes a valuable contribution to both interpretability and representation learning.

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>