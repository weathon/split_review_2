## Summary

This paper formalizes the all-day multi-scenes lifelong vision-and-language navigation (AML-VLN) problem, where an agent must continually learn across diverse scenes and illumination environments (normal, low-light, overexposed, scattering) without catastrophic forgetting. To address this, the authors propose Tucker Adaptation (TuKA), which represents multi-hierarchical navigation knowledge as a high-order tensor and uses Tucker decomposition to decouple shared subspaces from scene-specific and environment-specific experts. They introduce a decoupled knowledge incremental learning (DKIL) strategy for lifelong learning, build the AllDayWalker agent, extend Habitat with degraded imaging models, and demonstrate consistent improvements over a wide range of baselines on 24+ hierarchical tasks.

## Strengths

- **Well-motivated problem formulation**: The AML-VLN setting is a natural and practically important extension of existing VLN research. The two-dimensional problem structure (scenes × environments) is clearly defined with non-overlapping scenario pairs, and the paper provides a concrete illustration of catastrophic forgetting in this setting.

- **Novel technical approach with sound mathematical foundation**: Using Tucker decomposition to separately model shared core knowledge, scene-specific factors, and environment-specific factors is a clever and principled way to handle multi-hierarchical knowledge. The tensor-to-matrix alignment (Equation 3) that reduces the high-order tensor to a 2D weight matrix compatible with LLM backbones is a key technical contribution.

- **Strong and consistent empirical results**: AllDayWalker outperforms all 12 compared baselines (including advanced LoRA variants like BranchLoRA, HydraLoRA, SD-LoRA) across SR, SPL, OSR, and their forgetting-rate counterparts. On the 24-task benchmark, AllDayWalker achieves 65% average SR versus the best baseline at 52%, a clear 13% absolute improvement. Forgetting rates are also substantially lower (11% vs. 18–87% for other methods).

- **Comprehensive evaluation**: The paper includes ablation studies on tensor order (3rd vs. 4th), shared component analysis, scaling to more tasks (30 total), and generalization to six unseen scenarios including real-world scenes. The results support the design choices and demonstrate robustness.

## Weaknesses

### Major

1. **Overstated novelty of "high-order tensor representation"**: The paper repeatedly claims to overcome limitations of "2D matrix form" by using high-order tensors. However, the final adaptation update \(\Delta W_t\) applied to the LLM backbone is still a 2D matrix (Equation 3). The tensor is an internal representation that is contracted to a matrix before integration. While the decomposition structure is valuable, the rhetoric about fundamentally breaking free of 2D representations is misleading. The actual dimensionality of the adaptation parameters applied to the backbone remains the same.

2. **Incremental combination of existing techniques**: The DKIL strategy combines elastic weight consolidation (EWC), consistency constraints, and orthogonal regularization—all well-established continual learning techniques. The orthogonal constraint for expert separation parallels O-LoRA. While applying these to the Tucker-decomposed structure is new, the individual components are not novel. The paper would benefit from more explicit discussion of what is genuinely new beyond the architectural choice of Tucker decomposition.

### Minor

1. **Retrieval-based expert selection has unscalable assumptions**: During inference, expert selection relies on storing CLIP vision features for each scene/environment and performing cosine similarity matching. This assumes that the agent's first observation in an unseen scenario is sufficient to identify both the scene and environment correctly. The paper does not analyze retrieval accuracy or failure cases, nor does it discuss what happens when the similarity scores are ambiguous.

2. **Limited analysis of computational overhead**: The paper compares trainable parameter counts but does not provide inference time, memory usage, or training FLOPs comparisons. Given that TuKA involves a core tensor and multiple factor matrices, understanding the practical cost relative to standard LoRA is important for deployment.

3. **Real-world results are referenced only to appendix**: The paper claims "additional real-world deployments also validate the superiority" but only shows simulation-based results in the main paper. Without seeing those results, the claim about real-world validation is unsubstantiated in the main text.

### Trivial

- Figure 3 and Figure 4 have redundant/long captions that are parser artifacts.
- The color-coding in Figure 6 is difficult to interpret without the appendix details.

## Nice-to-Haves

- An ablation study showing the contribution of each loss term (\(\mathcal{L}_{sk}\), \(\mathcal{L}_{co}\), \(\mathcal{L}_{es}\)) individually would strengthen the claims about DKIL.
- Analysis of how the choice of low-rank dimensions \(r_1, r_2, r_3, r_4\) affects the trade-off between performance and parameter efficiency.
- A discussion of limitations: does the approach assume a fixed number of scenes \(M\) and environments \(N\)? How would the method handle an unbounded stream of new scenes/environments?

## Novel Insights

The key insight is that multi-hierarchical knowledge in VLN (shared navigation skills, scene-specific knowledge, environment-specific knowledge) can be naturally captured by a tensor structure where each mode of the tensor corresponds to a distinct knowledge hierarchy. Tucker decomposition then provides a clean factorization: a shared core tensor captures interactions across all hierarchies, while factor matrices along each mode serve as specialized expert pools. This is more expressive than the two-level shared-specific decomposition in MoE-LoRA variants. The paper also demonstrates that a 4th-order tensor (separating scene and environment) outperforms a 3rd-order tensor (bundling scene-environment pairs), validating that explicit decoupling of hierarchies improves lifelong learning.

## Suggestions

- Add a paragraph clarifying that while the internal representation is high-order, the final adaptation update applied to the LLM backbone is a standard low-rank matrix. This would make the contribution more precise and less prone to misinterpretation.
- Include an analysis of expert retrieval accuracy or a sensitivity study showing how performance degrades when the CLIP-based matching is imperfect.
- Provide inference time measurements for AllDayWalker versus standard LoRA to help practitioners assess the deployability trade-off.

## Score and Decision

Score: 8

Decision: Accept

The paper addresses a well-motivated and practically important problem, proposes a technically sound solution that goes beyond incremental extensions of LoRA, and provides strong empirical evidence across multiple metrics and settings. The weaknesses are not fatal—the overstatement about high-order representation is minor in practice, and the incremental nature of the learning strategy does not diminish the value of the overall contribution. This work advances the state of the art in lifelong VLN and introduces a principled tensor-based framework that could influence future parameter-efficient adaptation research.

MY FINAL SCORE: 8<score>8</score>
MY FINAL DECISION: Accept<decision>Accept</decision>