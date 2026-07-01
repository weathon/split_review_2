## Summary

This paper argues that diffusion models in high-dimensional settings do not actually learn the statistical quantities (posterior, score, velocity field) that theory assumes they learn. The authors identify a "weighted sum degradation" phenomenon where, due to data sparsity in high dimensions, the fitting target of the diffusion model's objective function degrades from a weighted sum of multiple samples to a single sample. They then propose a "Natural Inference" framework that unifies most existing inference methods (DDPM, DDIM, Euler, DPM-Solver, etc.) without relying on statistical concepts, instead viewing the process as progressive information enhancement through predicting x₀.

## Strengths

- **Provocative and important research question**: The paper challenges a fundamental assumption in diffusion model theory—whether these models actually learn the statistical quantities they claim to learn. This is a genuinely interesting and timely question given the empirical success of diffusion models despite theoretical concerns about the curse of dimensionality.

- **Clear empirical demonstration of the degradation phenomenon**: Tables 1 and 2 provide concrete statistics showing that for ImageNet-256 and ImageNet-512, the weighted sum degradation is severe, especially at lower timesteps (t < 600). The degradation rates approaching 1.0 for many settings are striking and provide empirical grounding for the paper's central claim.

- **Unification of diverse inference methods**: The Natural Inference framework successfully shows that many seemingly different sampling methods (DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, DEIS) can be expressed within a common structure. This is a valuable conceptual contribution that could simplify understanding and comparison of inference methods.

## Weaknesses

### Fatal
None.

### Major

- **The core claim is overstated relative to the evidence provided**: The paper argues that diffusion models "do not learn these statistical quantities" and instead operate via a "different mechanism." However, the degradation phenomenon only shows that the *fitting target* for individual training examples may be a single sample rather than a weighted sum. This does not necessarily imply that the model cannot learn statistical quantities. A model trained on many such degraded examples across different noise levels and different x₀ samples could still learn meaningful statistical structure. The paper provides no experiments showing that models trained under these conditions actually fail to capture distributional information (e.g., by testing whether the learned model generalizes to out-of-distribution inputs or whether its internal representations correlate with statistical quantities).

- **The "Natural Inference" framework is primarily a reparameterization, not a new mechanism**: The framework expresses existing inference methods as linear combinations of predicted x₀ values and noise terms. While this is a useful unifying perspective, it does not constitute a fundamentally new mechanism for how diffusion models work. The paper claims this framework is "free from any statistical concepts," but the model is still trained to predict x₀, and the inference process still depends on the model's learned mapping from noisy inputs to clean predictions—which is itself a statistical quantity (the conditional expectation). The framework relabels rather than replaces the statistical foundation.

- **Lack of experimental validation for the proposed perspective**: The paper does not conduct any experiments to validate that the "information enhancement" interpretation leads to new insights or improved performance. There are no ablation studies, no comparisons showing that the Natural Inference framework enables better sampling, and no demonstrations that the framework predicts phenomena that the standard statistical interpretation cannot. The paper remains entirely theoretical/analytical.

- **The degradation analysis conflates "degradation of the fitting target" with "inability to learn"**: The paper shows that for individual (X₀, Xₜ) pairs, the posterior mean may be dominated by a single sample. However, the model is trained across many such pairs. Even if each individual target is "degraded," the model could still learn the underlying distribution by aggregating information across training examples. The paper does not address this crucial distinction.

### Minor

- **The analysis of the degradation phenomenon is limited to synthetic statistics**: Tables 1 and 2 show degradation rates computed from the training data itself, not from an actual trained model. It would be more convincing to show that a trained model's predictions deviate from the true posterior in ways predicted by the degradation analysis.

- **The frequency-domain interpretation (Section 3.3) is presented as novel but is well-known in the community**: The observation that diffusion models learn to predict low frequencies first and high frequencies later has been discussed extensively (e.g., Dieleman, 2024, which the paper cites). The paper does not add substantially to this understanding.

- **The connection between Classifier-Free Guidance and Unsharp Masking is interesting but not deeply explored**: The paper draws an analogy but does not leverage this connection to derive new guidance methods or improve understanding of guidance behavior.

### Trivial
None.

## Nice-to-Haves

- An experiment comparing a model trained on high-dimensional data with a model trained on low-dimensional data to directly test whether the degradation phenomenon affects learning quality.
- A demonstration that the Natural Inference framework enables a new sampling method that outperforms existing methods.
- Analysis of whether the degradation phenomenon is mitigated by techniques like data augmentation, larger batch sizes, or different noise schedules.

## Novel Insights

The paper's key insight—that in high-dimensional sparse settings, the posterior mean target for individual training examples may collapse to a single sample—is genuinely novel and thought-provoking. However, the paper does not fully develop the implications of this observation. The most interesting question raised is: if the model cannot learn the true posterior from individual examples, how does it still generate high-quality samples? The paper's answer (the "information enhancement" interpretation) is plausible but not rigorously supported. The paper would be stronger if it provided a concrete mechanism by which the model compensates for the degraded training signal, rather than simply reinterpreting the inference process.

## Suggestions

1. **Strengthen the core claim with experiments**: Train a diffusion model and directly test whether its predictions match the true posterior (computed via kernel density estimation or a simpler proxy) versus matching the "degraded" single-sample target. This would directly validate the claim that the model does not learn the statistical quantities.

2. **Provide a constructive use of the Natural Inference framework**: Show that the framework enables a new sampling method, or that it predicts which existing methods will perform better under specific conditions. Without this, the framework remains a post-hoc description rather than a useful tool.

3. **Address the aggregation argument**: Explain why training across many degraded examples does not allow the model to learn the true distribution. This is the most natural counterargument to the paper's thesis and should be addressed explicitly.

4. **Consider lower-dimensional baselines**: Show that the degradation phenomenon is less severe in lower dimensions (e.g., CIFAR-10) and that models trained on such data do learn statistical quantities, to establish the dimensionality link more convincingly.

## Score and Decision

The paper raises an important and interesting question, and the degradation analysis is empirically grounded. However, the core claim is overstated relative to the evidence, and the proposed alternative framework is primarily a reparameterization rather than a new mechanism. The paper would benefit from experimental validation of its central thesis. In its current form, the contribution is more provocative than conclusive.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>