## Summary

This paper investigates whether generative (decoder-based) approaches are fundamentally necessary for compositional generalization in visual perception, compared to non-generative (encoder-based) approaches. The authors prove theoretically that constraining an encoder to the class of inverse generators is generally infeasible when the image dimension exceeds the latent dimension, because the required structural constraints depend on the geometry of the (unobserved) data manifold. In contrast, constraining a decoder is data-independent and straightforward. Empirically, they show on photorealistic PUG datasets that non-generative methods often fail at compositional generalization without large-scale pretraining, while generative methods leveraging decoder inversion via search and replay achieve significant OOD improvements.

## Strengths

- **Novel theoretical asymmetry result.** Theorem 3.2 is the paper's centerpiece: when d_x ≥ d_z³, the Jacobian and Hessian of inverse generators can be essentially arbitrary at any point, meaning there is no exploitable structural constraint on encoders. This cleanly establishes that the constraints for G_int are manifold-dependent (Eq. 3.4) while those for F_int are not (Eq. 3.1), creating a fundamental asymmetry. This is a genuinely insightful result that goes beyond prior work.

- **Well-designed experimental evaluation.** The PUG dataset splits (Background, Texture, Object) provide controlled, interpretable tests of compositional generalization. The PUG-Object result (n=0 case, near-perfect OOD accuracy for all methods) serves as a useful sanity check that validates the theoretical framework—the more constrained G_int for n=0 makes the problem tractable even for non-generative methods.

- **Practical generative methods with clear gains.** The search and replay approaches (Sec. 4) are well-motivated by the theory and yield consistent empirical improvements. On PUG-Background, replay alone substantially boosts OOD accuracy across all base encoders, and search provides additional gains. This demonstrates that the theoretical insights translate into practical methods.

- **Clear and coherent presentation.** The paper builds its argument systematically: formalize the problem (Sec. 2), establish the theoretical asymmetry (Sec. 3), propose practical inversion methods (Sec. 4), and validate empirically (Sec. 5). The connection to causal/anti-causal learning (Kilbertus et al., 2018) provides useful broader context.

## Weaknesses

### Fatal
None.

### Major

- **Limited scope of non-generative baselines.** The non-generative methods tested are pretrained encoders with simple slot encoders (Transformer or Slot Attention). The paper does not compare against non-generative methods specifically designed for compositional generalization (e.g., object-centric architectures with strong slot-disentanglement inductive biases, or methods using structured prediction heads). While the theory suggests such methods would still face fundamental limitations, the empirical case would be stronger with these comparisons, especially since the paper's title makes the strong claim that "generation is required."

- **Gap between theoretical claim and empirical evidence.** The theory guarantees compositional generalization only for exact identification within F_int, but the experiments use approximate methods (regularized cross-attention decoders, finite gradient steps for search). The paper does not quantify how well the decoder actually identifies f or how close the search solutions are to the true inverses. This makes it difficult to assess whether the empirical gains come from the theoretical mechanism or from other factors.

- **Simple experimental domain.** The PUG datasets involve animals and backgrounds with limited diversity (~20K images, 10 backgrounds, 32 animals). While controlled experiments are valuable, the paper's strong conclusion about human-level visual perception requires more convincing evidence on more complex, realistic data. The authors acknowledge this limitation but it remains significant given the strength of their claims.

### Minor

- **Replay cannot handle PUG-Texture.** The paper notes that generative replay cannot be applied to PUG-Texture because slots capture objects and backgrounds, not textures. This limits the generative approach's generality—the method requires knowing which concept dimensions can be recomposed, which may not always be available.

- **The d_x ≥ d_z³ condition.** Theorem 3.2 requires d_x ≥ d_z³. While this is easily satisfied for images (e.g., 224×224×3 >> 64³), the paper does not discuss what happens for intermediate regimes or why this specific bound is needed.

### Trivial
None.

## Nice-to-Haves

- A quantitative analysis of how well the regularized decoder approximates F_int, and how this approximation quality affects OOD generalization.
- Experiments on more complex datasets or with more diverse concept types to strengthen the generality of the claims.
- Analysis of the computational cost of gradient-based search at test time, which could be a practical bottleneck.

## Novel Insights

The paper's most novel insight is the formal demonstration of a fundamental asymmetry between the structure of generators and their inverses in the overcomplete setting (d_x >> d_z). While it is intuitive that the "causal direction" (generating images from latents) might be simpler than the "anti-causal direction" (inferring latents from images), the paper provides a precise mathematical characterization: the constraints defining F_int are coordinate-aligned and data-independent, while those defining G_int depend on the tangent space of the data manifold—including in unobserved OOD regions. This connects the abstract causal learning principle (Janzing & Schölkopf, 2010) to concrete architectural and regularization implications for representation learning, providing a principled explanation for why non-generative methods require massive pretraining data to achieve compositional generalization.

## Suggestions

- Include comparisons with non-generative baselines that have explicit compositional inductive biases (e.g., slot-based models with strong separation losses) to strengthen the empirical argument.
- Provide a quantitative measure of decoder identification quality (e.g., reconstruction error on held-out OOD images) to connect the theoretical guarantees to empirical performance.
- Discuss the computational trade-offs of gradient-based search more explicitly, as this is a practical concern for deploying the generative approach.

## Score and Decision

The paper presents a clean theoretical result (Theorem 3.2) establishing a fundamental asymmetry between constraining decoders and encoders for compositional generalization, supported by well-designed experiments on controlled photorealistic data. The theoretical contribution is genuinely novel and likely has implications beyond the specific F_int function class studied. The experiments, while limited in scale, consistently support the theoretical predictions. The main weaknesses are the limited experimental scope and the gap between the strong title claim and the evidence provided, but these do not invalidate the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: Accept