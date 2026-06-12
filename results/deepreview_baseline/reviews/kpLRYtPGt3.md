## Summary

This paper introduces Neon, a remarkably simple post-processing method that improves generative models by first fine-tuning them on their own synthetic data (which degrades performance) and then reversing the resulting parameter update via negative extrapolation: θ_Neon = (1+w)θ_r - wθ_s. The authors prove that mode-seeking inference samplers (e.g., low temperature, CFG) create a predictable anti-alignment between synthetic and real-data gradients, making this reversal effective. Neon is demonstrated across diffusion, flow matching, autoregressive, and few-step models on ImageNet, CIFAR-10, and FFHQ, achieving a new state-of-the-art FID of 1.02 on ImageNet-256 with xAR-L using only 0.36% additional compute.

## Strengths

- **Simplicity and elegance**: The method is a single parameter merge requiring no auxiliary models, no inference modifications, no likelihood computations, and no additional real data. This stands in stark contrast to existing approaches that add significant complexity.
- **Strong theoretical foundation**: The paper provides rigorous analysis (Theorems 1 and 2) showing why mode-seeking samplers induce anti-alignment and why negative extrapolation reduces the true data risk. The theory is connected to concrete instances (autoregressive temperature/top-k, diffusion CFG).
- **Extensive empirical validation**: Experiments span four model families (diffusion, flow matching, autoregressive, few-step) and three datasets, with consistent improvements. The ablation studies (transferability, sensitivity to synthetic data quality, robustness to base model quality) are thorough and informative.
- **Practical impact**: Neon achieves state-of-the-art FID 1.02 on ImageNet-256 with negligible compute overhead (0.36%). It works with as few as 1k synthetic samples and compensates for a 40% reduction in real training data, which is highly relevant for data-scarce applications.
- **Clear exposition**: The paper is well-structured, with intuitive figures (toy Gaussian example, precision-recall trade-offs) that effectively communicate the core ideas.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical assumptions may not always hold in practice**: The anti-alignment guarantee relies on small model error ‖ε‖_H_d, local convexity, and for diffusion/flow models a specific curvature-density coupling condition (A-MONO). While the experiments suggest these conditions are often satisfied, the paper does not discuss cases where they might fail or provide diagnostics to check them.
- **Hyperparameter sensitivity is not fully characterized**: The method requires tuning the extrapolation strength w and, for autoregressive models, joint tuning with CFG scale γ. Although the paper shows robustness to synthetic data quality, the sensitivity to w and the interaction with γ (Figure 6) suggests that optimal performance may require careful grid search, which could be a practical barrier.

### Minor
- **No uncertainty quantification**: FID improvements are reported as point estimates without error bars or confidence intervals. Given that FID can be noisy, some measure of statistical significance would strengthen the claims.
- **Limited discussion of failure modes**: The paper does not explore scenarios where Neon might hurt performance (e.g., if the base model is already near-optimal, or if the synthetic data is generated with a diversity-seeking sampler). The theory predicts interpolation (w<0) would help in such cases, but this is not empirically demonstrated.
- **Comparison to related methods could be more direct**: While the paper mentions DDO, SIMS, and Discriminator Guidance, it does not provide a direct FID comparison on the same benchmarks (e.g., applying DDO to xAR-L). The state-of-the-art claim relies on Table A.1 in the appendix, which is not available in the main text.

### Trivial
None.

## Nice-to-Haves
- A practical guideline for choosing w (e.g., based on the angle between gradients or validation FID) would increase usability.
- An experiment with a diversity-seeking sampler (e.g., high temperature) to empirically validate the interpolation regime predicted by the theory.
- Error bars or multiple seeds for the main FID results.

## Novel Insights

Beyond the paper's own contributions, the key insight is that model degradation from self-training is not random noise but a structured signal that is anti-aligned with the true data gradient. This reframes a known failure mode (model collapse) as a diagnostic tool: the direction of degradation reveals where the model is overconfident, and reversing it corrects the bias. The connection between inference samplers and gradient alignment is a novel perspective that could inspire other self-correction methods.

## Suggestions
- Add a practical heuristic for selecting w, such as a small validation set or a simple rule based on the norm of the degradation vector.
- Include error bars or multiple runs for the main FID results to quantify variability.
- Provide a direct comparison to DDO or SIMS on at least one benchmark (e.g., ImageNet-256 with a diffusion model) to contextualize the improvements.

## Score and Decision

Score: 9.0

Decision: Accept

MY FINAL SCORE: <score>9.0</score>
MY FINAL DECISION: <decision>Accept</decision>