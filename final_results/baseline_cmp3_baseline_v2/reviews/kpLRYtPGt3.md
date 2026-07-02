## Summary

This paper introduces Neon (Negative Extrapolation from self-traiNing), a remarkably simple post-hoc method that improves generative models by first fine-tuning them on their own synthetic data (which degrades performance) and then reversing the resulting parameter updates via negative extrapolation. The authors provide theoretical analysis showing that mode-seeking inference samplers create anti-alignment between synthetic and real data gradients, making this reversal effective. Neon is demonstrated across diffusion, flow matching, autoregressive, and few-step models on ImageNet, CIFAR-10, and FFHQ, achieving state-of-the-art FID of 1.02 on ImageNet-256 with xAR-L using only 0.36% additional compute.

## Strengths

- **Exceptional simplicity and universality**: Neon is a single-line parameter merge (θ_Neon = (1+w)θ_r - wθ_s) that works across fundamentally different architectures (diffusion, flow matching, autoregressive, few-step) without requiring auxiliary models, inference modifications, or access to original training data. This is a genuinely elegant contribution.

- **Strong theoretical grounding**: The paper provides rigorous analysis (Theorems 1 and 2) explaining why mode-seeking samplers induce anti-alignment between synthetic and real gradients, and why negative extrapolation reduces true data risk. The theory connects concrete inference practices (temperature < 1, top-k, CFG) to the method's success.

- **Compelling empirical results**: Neon achieves state-of-the-art FID of 1.02 on ImageNet-256 with xAR-L, surpassing UCGM's 1.06. Improvements are consistent across all tested architectures and datasets, with minimal compute overhead (<1% additional training). The ablation studies (cross-architecture transfer, sensitivity to synthetic data quality, robustness to base model quality) are thorough and informative.

- **Novel perspective on model collapse**: Rather than treating self-training degradation as a problem to avoid, the paper reframes it as a structured signal for improvement. This conceptual contribution could influence future work on self-improving generative models.

## Weaknesses

### Major

- **Limited comparison to related methods**: The paper mentions Discriminator Guidance, SIMS, DDO, and Self-Play Fine-Tuning in the related work but does not provide direct empirical comparisons on the same benchmarks. For instance, how does Neon compare to DDO on autoregressive models where both apply? The paper claims Neon is simpler and more universal, but quantitative comparisons would strengthen this claim. Given that DDO reports FID improvements on similar models, the absence of direct comparison is a notable gap.

- **Practical tuning complexity**: While the method itself is simple, the paper reveals that optimal performance requires joint tuning of (w, γ) for autoregressive models, and that optimal w depends on the fine-tuning budget B and synthetic dataset size |S|. The sensitivity analysis shows a U-shaped relationship with |S| and non-trivial interactions between w and γ. The paper does not provide clear practical guidance on how to select these hyperparameters without a validation set, which limits deployability.

- **Theoretical assumptions may not hold for all practical configurations**: Theorem 2's guarantee for diffusion/flow models requires "curvature-density coupling (A-MONO)" which is acknowledged as an assumption. The practical scope of this assumption is not empirically validated. Additionally, the theory assumes the base model is near-optimal (small ||ε||), and while Figure 9 shows robustness, the theoretical guarantees may not cover all practical regimes explored.

### Minor

- **The "state-of-the-art" claim for xAR-L (FID 1.02) should be contextualized**: The paper compares against UCGM's 1.06, but there are many recent generative models on ImageNet-256. A more comprehensive comparison table (beyond what's in the appendix) would help situate this result. The claim is impressive but would benefit from broader context.

- **The cross-architecture transfer results (Figure 8) show improvement but are weaker than self-transfer**: The paper frames this as a strength, but the practical utility is unclear—if you have access to a flow matching model's synthetic data, why not just apply Neon to that model directly? The theoretical explanation (Appendix B.8) is appreciated but the practical motivation could be stronger.

### Trivial

- The paper uses "MAD" and "model collapse" terminology but does not clearly distinguish between the two concepts or cite the most recent work on the topic.

## Nice-to-Haves

- A practical hyperparameter selection heuristic (e.g., using a small validation set or early stopping rule) would significantly improve the method's usability.
- Analysis of Neon's effect on other metrics beyond FID (e.g., IS, CLIP score, human evaluation) would strengthen the claims about improved "sharpness and realism."
- Discussion of whether Neon could be applied iteratively (multiple rounds of self-training and reversal) and whether this leads to further improvement or diminishing returns.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the failure mode of self-training (model collapse) is not random degradation but a structured, predictable bias that can be inverted. This suggests a broader principle: for any process that introduces a known, systematic bias into a model, the bias direction can be identified and reversed to improve performance. The paper's framing of inference samplers as "diagnostic tools" for uncovering distributional flaws is a genuinely novel perspective that could inspire new methods for model analysis and correction.

## Suggestions

- Add direct empirical comparisons to DDO, Discriminator Guidance, and SIMS on at least one shared benchmark (e.g., ImageNet-256 with a diffusion model) to quantitatively demonstrate Neon's advantages.
- Provide a practical guideline for hyperparameter selection, such as: "For most models, w ≈ 1.0 and |S| ≈ 10k-100k samples with B ≈ 1-2Mi works well; tune w on a small validation set of 1k real samples."

## Score and Decision

The paper presents a genuinely simple, theoretically grounded, and empirically effective method that works across diverse architectures with minimal overhead. The main weakness is the lack of direct empirical comparison to related methods, which would strengthen the claims of superiority. However, the method's elegance, universality, and strong results (including a new state-of-the-art FID) make this a valuable contribution to the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>