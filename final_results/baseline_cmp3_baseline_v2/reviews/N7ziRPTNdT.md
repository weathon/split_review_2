## Summary

This paper investigates whether generative (decoder-based) or non-generative (encoder-based) approaches are necessary for achieving compositional generalization in visual perception, a key component of data-efficient human-like learning. The authors provide theoretical analysis showing that enforcing the inductive biases required for compositional generalization on encoders is generally infeasible due to dependence on unknown out-of-domain data manifold geometry, while such constraints can be straightforwardly applied to decoders. Empirically, they demonstrate that non-generative methods often fail at compositional generalization on photorealistic PUG datasets unless pretrained at massive scale, whereas generative methods leveraging decoder inversion via gradient-based search and generative replay achieve significant improvements without additional data.

## Strengths

- **Strong theoretical contribution**: The paper provides a rigorous formalization of compositional generalization in terms of identifiability of generators and their inverses, and proves a key result (Theorem 3.2) showing that when the ambient dimension is much larger than the latent dimension, the derivatives of inverse generators can be arbitrary, making practical constraints on encoders infeasible. This is a novel and non-trivial theoretical insight.

- **Clear conceptual framing**: The paper clearly distinguishes generative and non-generative approaches not by whether an encoder/decoder is used, but by whether perception is achieved through inverting a learned decoder or learning an encoder directly. This clarifies a common source of confusion in the literature.

- **Well-designed experiments**: The use of PUG datasets with controlled in-domain/out-of-domain splits allows rigorous evaluation of compositional generalization. The experiments systematically compare multiple pretrained encoders (DINOv1/v2, CLIP, SigLIP2, I-JEPA) and show that generative methods with search and replay consistently improve OOD performance across all base encoders.

- **Practical relevance**: The paper demonstrates that even with massive pretraining (SigLIP2), non-generative methods still show suboptimal OOD performance on some splits, while generative methods with search/replay achieve near-perfect performance, suggesting fundamental advantages rather than just scaling issues.

## Weaknesses

### Major

- **Limited empirical scope**: The experiments are confined to PUG datasets with simple concepts (animals, backgrounds, textures) in controlled settings. While the authors acknowledge this limitation, the gap between these toy-like datasets and real-world visual complexity is substantial. The claim that generative approaches are "required for data-efficient perception" is not convincingly supported by experiments on such simplified data.

- **Theoretical assumptions may not hold in practice**: The theory assumes the ground-truth generator belongs to the specific function class $\mathcal{F}_{\text{int}}$ (polynomial interactions between slots). While this is the largest class known to enable OOD identifiability, it is unclear whether real visual data actually conforms to this structure. If real generators fall outside $\mathcal{F}_{\text{int}}$, the theoretical guarantees for generative methods also break down.

- **The decoder architecture used is not truly constrained to $\mathcal{F}_{\text{int}}$**: The paper uses a regularized cross-attention Transformer as an approximation to $\mathcal{F}_{\text{int}}$, but does not provide evidence that this architecture actually satisfies the required constraints (e.g., block-diagonal higher-order derivatives). The regularization encourages pixel-slot specialization but does not provably enforce the polynomial structure of Eq. (2.7). This weakens the connection between theory and experiments.

### Minor

- **The comparison between generative and non-generative methods is somewhat unfair**: Generative methods leverage search and replay which require additional computation at test time (gradient-based optimization) or additional training (replay). Non-generative methods are evaluated as a single forward pass. A fairer comparison would measure performance under similar computational budgets.

- **The paper does not ablate the importance of the decoder being constrained to $\mathcal{F}_{\text{int}}$**: Results in Appendix C mention unstructured decoders but the main paper does not show whether the regularized decoder is actually necessary for the benefits of search/replay, or whether any decoder would work.

### Trivial

- Figure 1 is confusing and the caption is overly long and repetitive.

## Nice-to-Haves

- An ablation study showing whether search/replay benefits persist when using an unconstrained decoder (not regularized toward $\mathcal{F}_{\text{int}}$) would strengthen the claim that the decoder constraints are what enable the improvements.
- Experiments on more complex datasets (e.g., CLEVR, or procedurally generated scenes with more objects and interactions) would increase confidence in the generality of the findings.
- A discussion of computational cost trade-offs between search/replay and simply scaling up pretraining data for non-generative methods would be valuable for practitioners.

## Novel Insights

The paper's key insight is that the asymmetry between generators and their inverses in high-dimensional spaces makes it fundamentally harder to constrain encoders than decoders for compositional generalization. This provides a theoretical justification for the long-standing intuition in cognitive science that generative models are necessary for human-like generalization. The result that inverse generators lose their structured derivatives when the ambient dimension exceeds the latent dimension cubed is a genuinely novel mathematical observation that explains why encoder-only methods struggle with OOD generalization even when they work perfectly in-domain.

## Suggestions

- Add an experiment where the decoder is intentionally not constrained toward $\mathcal{F}_{\text{int}}$ (e.g., a standard MLP decoder) to test whether the benefits of search/replay depend on the decoder having the right inductive biases.
- Include a comparison where non-generative methods are given additional computational budget (e.g., test-time adaptation or fine-tuning on OOD examples) to make the comparison more equitable.
- Clarify in the main text whether the decoder regularization actually enforces the block-diagonal derivative structure or merely encourages it, and discuss the implications for the theoretical guarantees.

## Score and Decision

The paper makes a solid theoretical contribution and provides clean experiments on controlled data. However, the gap between the simplified experimental setting and the strong claim that "generation is required for data-efficient perception" is too large. The theory is elegant but rests on assumptions about the generator class that may not hold in practice, and the experiments do not demonstrate that the approach scales to realistic visual complexity. The paper is a valuable contribution to the discussion but does not conclusively settle the question.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>