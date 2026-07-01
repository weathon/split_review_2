##Summary

The paper introduces Marginal Flow, a density estimation framework that defines the model as a mixture of parametric distributions \(q(\mathbf{x}|\mathbf{w})\) where the parameters \(\mathbf{w}\) are sampled from a learnable distribution \(q_\theta(\mathbf{w})\) via an unconstrained neural network. By resampling \(\mathbf{w}\) at each evaluation rather than optimizing fixed mixture components, the model approximates a marginal distribution and avoids collapse to a finite mixture. The framework provides exact density evaluation and efficient single-step sampling, supports lower-dimensional manifolds, multi-modal targets, and various training objectives, and is orders of magnitude faster than competing methods in runtime.

## Strengths

- **Novel and principled framework**: The idea of marginalizing over resampled latent parameters from a learnable distribution is a clean departure from both fixed mixture models and bijective flows. It simultaneously achieves efficient exact likelihood evaluation and efficient sampling, overcoming a fundamental trade-off in normalizing flows and diffusion models.
- **Exceptional flexibility**: The model imposes no bijective constraints on the neural network, can learn densities on lower-dimensional manifolds (by choosing a lower-dimensional base distribution), handles multi-modal targets naturally, and allows the parametric family \(q(\mathbf{x}|\mathbf{w})\) to be tailored to the data (e.g., Gaussian, Wishart, Dirichlet). This flexibility is demonstrated across diverse tasks.
- **Strong empirical efficiency**: Runtime comparisons (Figure 3) show that Marginal Flow is orders of magnitude faster than normalizing flows, flow matching, and free-form flows for both sampling and exact density evaluation, especially in high dimensions. Training convergence (Figure 7) is also substantially faster on synthetic benchmarks.
- **Clear exposition and motivation**: The paper clearly explains the marginalization idea, contrasts it with fixed mixture models (Figure 1), and provides intuitive diagrams (Figure 2). The motivation for why resampling prevents collapse is well illustrated.

## Weaknesses

### Major

- **Approximation error from finite \(N_c\) is not analyzed**: The model density in Eq. (2) is a Monte Carlo approximation of the true marginal in Eq. (1). The paper does not discuss the bias-variance trade-off, how to choose \(N_c\), or the effect of \(N_c\) on density quality. The claim of “exact density evaluation” (Table 1) is technically true for the mixture model, but the mixture itself is an approximation to the target marginal. This distinction should be clarified and analyzed.
- **Limited scalability to high-dimensional data**: All experiments are on relatively low-dimensional data (synthetic 2D, Wishart up to 5050 dimensions but with a structured manifold, MNIST latent 20D, JAFFE latent 10D). The paper does not demonstrate the framework on high-dimensional image generation (e.g., CIFAR-10, ImageNet) where competing models like diffusion models and normalizing flows are commonly evaluated. The capacity of a small MLP to generate complex high-dimensional distributions is questionable.
- **Incomplete comparison of final performance**: Figure 7 shows faster convergence in test log-likelihood versus runtime, but the final log-likelihood values after full training are not reported. It is unclear whether Marginal Flow ultimately matches or exceeds the performance of competitors given sufficient training time. The paper should provide final test metrics for all methods.
- **Lack of theoretical analysis**: The paper claims universality for certain families of \(q(\mathbf{x}|\mathbf{w})\) but provides no proof or rigorous discussion. The expressiveness of the model and the effect of the neural network architecture on the learned distribution are not theoretically characterized.

### Minor

- **Choice of \(N_c\) is not discussed**: The number of components \(N_c\) is a key hyperparameter, yet the paper does not provide guidance on how to set it or study its impact on density quality and computational cost.
- **Comparison to other mixture-based density estimators is missing**: The paper does not compare to mixture density networks, kernel density estimation, or other implicit mixture models that also offer efficient evaluation and sampling. The novelty relative to these baselines could be more clearly delineated.
- **Simulation-based inference results are relegated to the appendix**: The main text mentions state-of-the-art results on SBI but does not show the actual numbers or a summary figure. This weakens the impact of that experiment.
- **Runtime comparison (Figure 3) focuses on sampling and evaluation, not training**: The paper claims “orders of magnitude faster” overall, but the training time comparison (Figure 7) is only on synthetic data. A training runtime comparison on higher-dimensional tasks would strengthen the claim.

### Trivial

- The paper uses “exact density” to refer to the mixture model’s density, which is exact but not the true marginal. This could be clarified with a brief remark.

## Nice-to-Haves

- An ablation study on the effect of \(N_c\) on density quality and computational cost.
- A theoretical bound on the approximation error of the marginal in terms of \(N_c\) and the smoothness of \(q(\mathbf{x}|\mathbf{w})\).
- Demonstration on a higher-dimensional image dataset (e.g., CIFAR-10) using a convolutional architecture for \(f_\theta\).
- Comparison to other fast density estimators like neural spline flows or masked autoregressive flows in terms of both speed and quality.

## Novel Insights

The key insight is that by resampling the parameters of a parametric family from a learned distribution (rather than optimizing them as fixed points), the model avoids collapsing to a finite mixture while retaining the ability to evaluate the density exactly and sample efficiently. This marginalization perspective unifies the benefits of mixture models (fast evaluation/sampling) with the flexibility of deep generative models (learned latent representations, manifold learning). The observation that the neural network can be completely unconstrained (no bijectivity, no Jacobian) and still yield a valid density estimator is a significant departure from normalizing flows and opens the door to using arbitrary architectures for density estimation.

## Suggestions

- Provide a theoretical or empirical analysis of the bias introduced by finite \(N_c\) and suggest a practical rule for choosing \(N_c\).
- Report final test log-likelihood (or other metrics) for all methods after convergence, not just during training.
- Include a summary of the SBI results (e.g., C2ST scores) in the main text to strengthen that contribution.
- Consider demonstrating the framework on a moderately high-dimensional image dataset (e.g., downsampled CIFAR-10) to show scalability.

## Score and Decision

**Score**: 6  
**Decision**: Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>