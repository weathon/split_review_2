## Summary

This paper introduces a new perspective on class-wise machine unlearning by decoupling the class label from the target concept. It identifies three novel unlearning scenarios beyond the conventional all-matched setting—target mismatch, model mismatch, and data mismatch—where the label domains of the forgetting data, model output, and target concept do not coincide. The authors provide a theoretical analysis of forgetting dynamics (representation gravity) and propose a general framework, TARF, that combines annealed gradient ascent on forgetting data with target-aware gradient descent on selected retaining data. Experiments on CIFAR-10/100, ImageNet-1k, and real-world applications demonstrate that TARF consistently outperforms existing methods in the new mismatch settings while remaining competitive in the conventional setting.

## Strengths

- **Novel and practically motivated problem formulation.** Decoupling the class label from the target concept is a meaningful extension of machine unlearning that addresses realistic scenarios (e.g., unlearning a semantic concept that spans multiple classes or is a subset of a class). The paper clearly defines four distinct tasks and provides concrete examples (Figure 1).
- **Theoretical insight into forgetting dynamics.** Theorem 3.2 and the concept of representation gravity offer a principled explanation for why mismatched label domains cause existing methods to fail, and they motivate the design of TARF. The analysis connects representation similarity to the co-movement of losses during gradient ascent, which is both intuitive and useful.
- **Comprehensive and well-designed experiments.** The evaluation covers multiple benchmarks (CIFAR-10/100, Tiny-ImageNet, ImageNet-1k), multiple architectures (ResNet-18, VGG-16bn, WideResNet-50), and all four mismatch settings. The paper also includes case studies on concept removal in stable diffusion and information removal in LLMs (TOFU), demonstrating real-world applicability. Ablation studies (Figure 7) systematically examine the effect of key components (annealing, hyperparameters, model capacity, gradient operations).
- **Effective and general framework.** TARF is simple, computationally efficient (comparable to fine-tuning), and consistently achieves the lowest gap to the retrained reference across all mismatch settings. The three-phase interpretation (target identification, target separation, retraining approximation) provides a clear conceptual understanding of how the method works.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Theoretical analysis is heuristic.** Theorem 3.2 provides a bound that depends on the largest eigenvalue of the Jacobian and the Lipschitz constant, which may be loose in practice. The proof is relegated to the appendix, and the main text relies on intuitive reasoning. While the insight is valuable, the theoretical contribution is not rigorous enough to be considered a core strength.
- **Hyperparameter sensitivity is not fully explored.** TARF introduces several hyperparameters (k, t0, t1, β). The paper provides some guidance and an ablation on k, but the sensitivity to t0, t1, and the threshold β (especially the quantile choice) is not thoroughly studied. The method may require careful tuning for new datasets or tasks.
- **Limited evaluation beyond image classification.** The case studies on stable diffusion and TOFU are promising but brief. The paper does not demonstrate TARF on other modalities (e.g., text classification, graph data) or on more complex multi-label/multi-attribute scenarios. The claim of generality is somewhat under-supported.
- **Performance in model mismatch is still far from the retrained reference.** While TARF achieves the lowest gap, the absolute UA and RA values in model mismatch (e.g., CIFAR-10: UA 91.11 vs. Retrained 87.76) indicate that the method does not fully recover the retrained behavior. This is acknowledged but not deeply discussed.

### Trivial
- The notation in Table 1 and the description of data partitions could be slightly clearer, especially for the model mismatch case where affected retaining data is defined.

## Nice-to-Haves
- A more detailed analysis of the target identification phase (Phase I) would be helpful, particularly how the threshold β is set in practice and how robust the method is to misidentification.
- An extension to multi-label or multi-attribute unlearning would strengthen the generality claim.
- A discussion of the limitations of representation gravity when the target concept is inherently ambiguous or when the representation space is poorly structured (e.g., long-tailed data) is already present in the conclusion and is appreciated.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the success of unlearning is fundamentally tied to the structure of the learned representation space. The concept of representation gravity—where the effect of gradient ascent on one subset propagates to nearby subsets in the latent space—provides a unified explanation for why existing methods fail in mismatch scenarios and why TARF succeeds by explicitly leveraging this gravity to identify and separate target concepts. This perspective reframes unlearning not merely as an optimization problem but as a representation-level intervention, which could inspire future work on concept-level forgetting in other domains.

## Suggestions
- Provide a more thorough ablation on the threshold β and the quantile choice for target identification, as this is a critical component of the method.
- Include a discussion of the computational overhead of Phase I (target identification) in the main text, as it adds an extra forward/backward pass on the remaining data.
- Consider evaluating TARF on a more challenging multi-concept unlearning scenario (e.g., forgetting two disjoint target concepts simultaneously) to further demonstrate its flexibility.

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>