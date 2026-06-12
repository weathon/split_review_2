## Summary
The paper introduces Marginal Flow, a density estimation framework that defines a model as the average of a parametric distribution \(q(\mathbf{x}|\mathbf{w})\) over latent parameters \(\mathbf{w}\) sampled from a learnable distribution \(q_\theta(\mathbf{w})\). By resampling \(\mathbf{w}\) from \(q_\theta(\mathbf{w})\) (implemented via an unconstrained neural network \(f_\theta(z)\)), the method avoids the trade-offs of existing models: it supports exact density evaluation, efficient single-step sampling, flexible neural architectures, lower-dimensional base distributions, and multiple training objectives. Experiments on synthetic data, simulation-based inference, Wishart distributions on positive-definite matrices, and latent spaces of MNIST/JAFFE images demonstrate the framework’s flexibility and computational speed.

## Strengths
- **Novel and elegant framework**: The idea of marginalizing over a learnable distribution of latent parameters (rather than optimizing fixed mixture components) is simple yet powerful, and it cleanly decouples model capacity from the number of mixture components.
- **Unprecedented flexibility**: Marginal Flow simultaneously offers exact likelihood evaluation, efficient sampling, unconstrained network architectures, the ability to learn lower-dimensional manifolds, and straightforward support for multi-modal targets and various training objectives—a combination not achieved by any single prior method.
- **Strong empirical efficiency**: Runtime experiments (Figure 3) show that both density evaluation and sampling are orders of magnitude faster than Normalizing Flows, Flow Matching, and Free-form Flows. Training convergence (Figure 7) is also much faster on the tested synthetic datasets.
- **Comprehensive and well-designed experiments**: The paper tests the method on a diverse set of tasks (synthetic, SBI, Wishart matrices, latent space manifold learning) and includes both forward and reverse KL training, demonstrating robustness across different settings.

## Weaknesses
### Fatal
None.

### Major
- **Claim of “exact density evaluation” is ambiguous**: The model density is evaluated as a finite-sample average (Eq. 2), which is exact for the model *as defined*, but the model itself is a Monte Carlo approximation to the true marginal distribution (Eq. 1). This may confuse readers who expect point-wise exactness comparable to Normalizing Flows. The paper should clearly distinguish between the model’s definition and its approximation quality.
- **Empirical validation is limited in scope**: The method is not tested on standard density estimation benchmarks (e.g., UCI datasets, raw image likelihoods on CIFAR-10/MNIST pixels). The paper’s main comparison on synthetic data (≤1000 points) and on latent spaces (where the VAE encoder already reduces dimensionality) leaves open whether the framework scales to high-dimensional, high-structure data without a pre-trained encoder. The claim of being “orders of magnitude faster” is supported only by small-scale runtime tests (100 points) and may not generalize to full-scale training.
- **State-of-the-art claim on SBI is unsubstantiated in the main text**: The paper states “Marginal Flow achieves state-of-the-art results” for simulation-based inference, but the actual results are only in the appendix. The main text should present at least the key quantitative comparisons for this claim to be credible.

### Minor
- **Influence of the number of components \(N_c\)**: The paper does not analyze how the number of sampled parameters \(N_c\) affects the density estimate’s variance, accuracy, or training behavior. This is an important practical aspect for users.
- **Missing comparisons to simpler baselines**: The paper compares only to deep generative models (NF, FM, FFF). Comparisons with simpler methods such as KDE with learned bandwidth, Gaussian mixtures, or radial-basis-function networks would help position the framework’s practical advantage.
- **Conditional manifold experiments**: The visual quality of the MNIST and JAFFE interpolations (Figures 10–11) is modest and does not surpass prior work. While this is not a core weakness given the low-data regime, the paper could benefit from a more thorough quantitative evaluation (e.g., FID or density estimates in the latent space).

### Trivial
None.

## Nice-to-Haves
- An ablation study on the effect of \(N_c\) (both during training and inference) would be very informative.
- A discussion of the variance of the log-likelihood estimate and potential strategies to reduce it (e.g., importance weighting or using more samples).
- Application to a standard density estimation benchmark like the UCI “Power” or “Gas” datasets would strengthen the scalability claims.

## Novel Insights
Beyond the paper’s own contributions, the key insight is that a neural-network‑driven sampling of mixture parameters, when combined with resampling, transforms what would otherwise be a finite mixture into a flexible density approximator that separates model capacity from the number of components. This perspective connects generative modeling with ideas from Monte Carlo marginalization and kernel methods, and it opens a new design space where the parametric form of \(q(\mathbf{x}|\mathbf{w})\) can be tailored to the data’s geometric structure (e.g., Wishart for positive-definite matrices) without altering the learning algorithm.

## Suggestions
1. Clarify in the abstract and introduction that “exact density evaluation” refers to the model’s own density (not an upper/lower bound) and acknowledge that the marginal integral is approximated via finite samples.
2. Include at least one experiment on a standard high-dimensional density estimation task (e.g., MNIST pixels or a UCI dataset) to demonstrate scalability beyond synthetic and latent-space settings.
3. Provide a discussion and ablation on the trade-off between \(N_c\) and density estimation quality, including a practical guideline for choosing \(N_c\).
4. Move the SBI quantitative results (C2ST scores) from the appendix to the main text to support the state-of-the-art claim, or weaken the claim if the results are only slightly better.
5. Add a comparison against a simple baseline such as a learned kernel density estimator or a GMM with neural-network-parametrized components to show the added value of the marginalization.

## Score and Decision
MY FINAL SCORE: <score>6.0</score>  
MY FINAL DECISION: <decision>Accept</decision>