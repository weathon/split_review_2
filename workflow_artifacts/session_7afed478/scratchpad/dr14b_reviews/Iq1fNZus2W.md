### Summary

This paper addresses the computational inefficiency in multi-condition Diffusion Transformers (DiTs) by introducing Patch-wise and Keyword-Aware Attention (PKA). PKA consists of two modules: Position-Aligned Attention (PAA) and Keyword-Scoped Attention (KSA). PAA confines spatial control to aligned patches, while KSA restricts subject-driven control to keyword-activated regions. The authors also propose an early-timestep sampling strategy to accelerate training. The method achieves up to a 10× inference speedup and a 5.12× reduction in attention module VRAM usage, while maintaining or improving generative quality.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a thorough analysis of the computational redundancy in the standard full-attention mechanism of DiTs, which is a valuable contribution in itself.
2. The proposed PKA framework, with its two specialized modules (PAA and KSA), is a well-thought-out solution to the identified problem. The design of each module is motivated by empirical observations of attention patterns.
3. The early-timestep sampling strategy is a novel contribution that accelerates training without compromising performance.
4. The paper is well-written and easy to follow. The figures are clear and effectively illustrate the proposed method and its advantages.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on spatial and subject-driven conditions. It would be beneficial to explore the applicability of PKA to other types of conditions, such as style or texture.
2. The paper does not provide a detailed analysis of the impact of different hyperparameters on the performance of PKA. For example, the size of the patches in PAA or the threshold for keyword activation in KSA could significantly affect the results.
3. While the paper demonstrates impressive efficiency gains, it would be useful to have a more detailed comparison with other efficient attention mechanisms, such as linear attention or low-rank approximations. Specifically, a comparison with methods that explicitly target efficient attention in diffusion models would be more relevant.
4. The paper lacks a thorough discussion of the limitations of the proposed method. For example, how does PKA perform when dealing with complex scenes or multiple interacting objects? Does the method have any failure cases? The paper should also discuss the potential for error propagation due to the early timestep sampling strategy.

### Suggestions

The paper would benefit from a more comprehensive exploration of the hyperparameter space, particularly concerning the patch size in Position-Aligned Attention (PAA) and the keyword activation threshold in Keyword-Scope Attention (KSA). A detailed ablation study should be conducted to understand how these parameters affect both the quality of generated images and the computational efficiency. For instance, varying the patch size in PAA could reveal a trade-off between spatial control and computational cost, while different thresholds in KSA might impact the accuracy of keyword-specific attention. The study should also investigate the sensitivity of the method to these parameters across different datasets and condition types. Furthermore, the paper should include a more detailed analysis of the impact of the early timestep sampling strategy on the final image quality, especially in scenarios with complex conditions. It would be beneficial to show how the sampling strategy affects the convergence of the training process and the stability of the generated images. 

To strengthen the paper's contribution, a more thorough comparison with other efficient attention mechanisms is needed. Instead of comparing with general efficient attention methods, the paper should focus on comparing with methods that are specifically designed for efficient attention in diffusion models. This would provide a more relevant benchmark for the proposed method. The comparison should include not only computational efficiency but also the quality of generated images. It would be useful to analyze the trade-offs between different methods in terms of both speed and image quality. The paper should also discuss the specific advantages and disadvantages of PKA compared to these methods, highlighting the unique contributions of the proposed approach. This would help to better position the paper within the existing literature and demonstrate its practical value.

Finally, the paper should include a more detailed discussion of the limitations of the proposed method. This should include an analysis of how PKA performs in challenging scenarios, such as complex scenes with multiple interacting objects or scenes with significant occlusions. The paper should also discuss the potential failure cases of the method and the reasons behind these failures. Furthermore, the paper should address the potential for error propagation due to the early timestep sampling strategy. A more thorough analysis of these limitations would provide a more balanced view of the proposed method and help to identify areas for future research.

### Questions

1. How does the performance of PKA scale with the number of conditions? Are there any limitations in terms of the number of conditions that can be effectively handled?
2. Can the proposed method be extended to video generation tasks? If so, what modifications would be necessary?
3. How does the choice of the base DiT model affect the performance of PKA? Have you experimented with different DiT architectures?
4. The paper mentions that the attention computation scales as O(c^2n^2). Can you provide a more detailed breakdown of this complexity and how PKA reduces it?
5. How does the early-timestep sampling strategy affect the training dynamics? Are there any potential drawbacks to this approach?

### Rating

6

### Confidence

4

**********