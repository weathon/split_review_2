## Summary

This paper argues that diffusion models in high-dimensional settings do not actually learn the statistical quantities (posterior, score, velocity field) that theory assumes they learn. The authors identify a "weighted sum degradation" phenomenon where, due to data sparsity in high dimensions, the fitting target of the diffusion model's objective function degrades from a weighted sum of multiple samples to a single sample. They then propose a "Natural Inference" framework that unifies most existing inference methods (DDPM, DDIM, Euler, DPM-Solver, etc.) without relying on statistical concepts, instead framing the process as predicting x₀ from noisy inputs.

## Strengths

- **Provocative and important research question**: The paper challenges a fundamental assumption in diffusion model theory—whether these models actually learn the statistical quantities they claim to learn. This is a genuinely interesting and timely question given the widespread success of diffusion models.
- **Clear empirical demonstration of degradation**: Tables 1 and 2 provide concrete statistics showing that weighted sum degradation occurs at high rates (often 100%) for early timesteps in ImageNet-256 and ImageNet-512, with the effect being more pronounced for flow matching than VP schedules.
- **Unification of diverse inference methods**: The Natural Inference framework successfully shows that many seemingly different sampling methods (DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, DEIS) can be expressed within a common structure, which is a useful conceptual contribution.

## Weaknesses

### Fatal

**The core argument that degradation prevents learning is not supported by evidence.** The paper claims that when weighted sum degradation occurs, the model "cannot effectively learn the essential statistical quantities." However, this is a logical leap not backed by experiments. The authors show that the fitting target becomes a single sample rather than a weighted sum, but they do not demonstrate that this actually prevents learning or degrades performance. In fact, diffusion models achieve state-of-the-art results on ImageNet, which directly contradicts the paper's central thesis. The paper needs to either (a) show that models trained under conditions where degradation is severe perform worse than those where it is not, or (b) provide theoretical proof that single-sample targets are insufficient for learning the desired quantities. Without this, the argument is speculative.

**The "Natural Inference" framework is presented as a novel contribution but is essentially a reparameterization of existing methods.** The framework expresses inference as linear combinations of predicted x₀ values and noise terms. While this is a valid mathematical reformulation, it does not provide new algorithmic insights, improved performance, or testable predictions that differ from existing methods. The paper acknowledges that existing methods "are merely specific parameter configurations within the Natural Inference framework" but does not demonstrate any advantage of this perspective beyond "visual and interpretable" benefits. A framework that merely repackages existing methods without enabling new capabilities or insights is not a significant contribution.

**The paper makes strong claims without sufficient empirical validation.** The abstract states "diffusion models do not learn these statistical quantities; instead, they operate via a different mechanism," yet no experiments are conducted to directly test whether models learn posterior/score/velocity fields. The paper could have trained models and compared their learned quantities to ground-truth statistical quantities (e.g., via Monte Carlo estimation on simple distributions), but no such experiments are performed. The entire argument rests on the degradation phenomenon, which is a property of the training data, not a test of what the model actually learns.

### Major

**The degradation analysis conflates "cannot learn" with "the target is a single sample."** Even if the fitting target for a particular (x_t, x_0) pair is a single sample, the model sees many such pairs across training. The model could still learn the underlying distribution by aggregating information across many training examples. The paper's analysis focuses on individual posterior distributions p(x₀|x_t) but does not consider how the model might learn from the ensemble of training examples. This is a critical oversight.

**The frequency-domain interpretation (Section 3.3) is not novel.** The observation that diffusion models progressively generate low-to-high frequencies is well-known in the literature (e.g., Dieleman 2023, 2024, which the paper cites). The paper presents this as part of its "new perspective" but does not add new analysis or insights beyond what is already known.

**The Self Guidance concept is a trivial extension of Classifier-Free Guidance.** Defining Self Guidance as applying CFG between two outputs of the same model at different timesteps is a straightforward idea that does not constitute a significant contribution. The paper does not demonstrate any practical benefit of this formulation.

### Minor

- The paper claims to provide "the first rigorous analysis" of the diffusion model objective in high-dimensional sparse scenarios, but similar observations about data sparsity and posterior concentration have been made in prior work (e.g., Karras et al. 2022, which the paper cites).
- The experimental setup for measuring degradation uses a threshold of p > 0.9, but the sensitivity of results to this threshold is not explored.
- The paper does not discuss how the degradation phenomenon might be mitigated or whether it actually harms performance in practice.

### Trivial

- The paper uses "Ancestral Sampling" when it likely means "Ancestral Sampling" (typo in the original).
- Figure 5 is difficult to read due to small text and complex layout.

## Nice-to-Haves

- Experiments directly testing whether models learn the posterior/score/velocity field (e.g., by comparing model predictions to Monte Carlo estimates on simple distributions like mixtures of Gaussians).
- Ablation studies showing that models trained under conditions with less degradation (e.g., lower-dimensional data, more training data) perform better, supporting the causal claim.
- A demonstration that the Natural Inference framework enables new sampling methods or improved performance over existing methods.

## Novel Insights

None beyond the paper's own contributions. The degradation phenomenon is an interesting observation, but the paper does not convincingly connect it to model behavior or provide a framework that yields new capabilities.

## Suggestions

1. **Conduct experiments that directly test whether models learn statistical quantities.** Train a diffusion model on a simple high-dimensional distribution (e.g., a mixture of Gaussians) where ground-truth posteriors/scores can be computed analytically. Compare the model's learned quantities to ground truth under varying levels of data sparsity. This would directly test the paper's central claim.

2. **Demonstrate that the Natural Inference framework enables something new.** Either show that it leads to better sampling methods (e.g., by optimizing the coefficient matrices), or show that it provides testable predictions that differ from existing theory (e.g., predicting failure modes that standard theory would not).

3. **Address the ensemble learning counterargument.** Explain why the model cannot learn the distribution by aggregating information across many training examples, even if individual targets are single samples.

4. **Provide evidence that degradation correlates with performance degradation.** Compare model performance on datasets/timesteps where degradation is severe versus mild, controlling for other factors.

## Score and Decision

The paper asks an interesting question and identifies a genuine phenomenon (weighted sum degradation), but it fails to connect this observation to its central claim that diffusion models do not learn statistical quantities. The Natural Inference framework is a reparameterization of existing methods without demonstrated advantages. The paper makes strong claims without sufficient empirical support, and its core argument contains a logical gap (degradation of individual targets ≠ inability to learn from the ensemble). While the paper has some value in raising questions about diffusion model theory, it does not provide convincing evidence for its conclusions or offer practically useful new insights.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>