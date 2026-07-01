## Summary

This paper provides theoretical and empirical analysis of Multi-Grade Deep Learning (MGDL), which decomposes end-to-end neural network training into sequential shallow subproblems trained on residuals. The authors establish convergence guarantees for gradient descent in MGDL, prove that single-layer ReLU grades reduce to convex optimization subproblems, and analyze eigenvalue distributions of Jacobian matrices to explain MGDL's stability advantages. Experiments on image regression, denoising, deblurring, CIFAR-10/100 classification, and transformer-based time series forecasting demonstrate MGDL's empirical benefits over standard end-to-end training (SGDL).

## Strengths

- **Novel theoretical contribution**: The convexification result (Theorem 3) showing that MGDL with single-layer ReLU grades decomposes a nonconvex deep learning problem into a sequence of convex subproblems is a significant theoretical insight, extending prior convexification results from shallow to deep architectures.
- **Comprehensive empirical evaluation**: The paper evaluates MGDL across diverse tasks (image regression, denoising, deblurring, CIFAR classification, time series) and architectures (FCNs, CNNs, transformers), providing strong evidence of practical benefits.
- **Eigenvalue analysis provides mechanistic understanding**: The analysis linking MGDL's stable convergence to eigenvalues staying within (-1,1) versus SGDL's eigenvalues falling outside this range offers a clear, testable explanation for observed training dynamics.
- **Learning rate robustness demonstration**: The systematic study showing MGDL maintains performance over a wider range of learning rates than SGDL is practically valuable.

## Weaknesses

### Major

- **Theoretical results rely on unrealistic assumptions**: Theorem 1 and Theorem 2 assume the loss function is twice continuously differentiable, but ReLU activations are not twice differentiable (they are not even once differentiable at zero). This is a fundamental mismatch between the theory and the experiments, which all use ReLU. The paper acknowledges this assumption but does not address how the results extend to non-smooth activations.
- **Convexity result is limited in scope**: Theorem 3 requires each grade to be a single hidden-layer ReLU network with at least as many neurons as the number of activation regions (P_l), which grows exponentially with input dimension. This severely limits practical applicability—the condition m_l ≥ P_l is essentially impossible for high-dimensional inputs like images.
- **Missing comparison to standard baselines**: The image reconstruction experiments compare MGDL only to SGDL with the same total depth, but do not compare to standard methods like BM3D (for denoising), non-blind deconvolution methods (for deblurring), or modern architectures. The CIFAR experiments use MSE loss with fully connected networks, which is far from standard practice—modern CNNs with cross-entropy loss would be more meaningful baselines.
- **No statistical significance or error bars**: All reported results are single runs without error bars, confidence intervals, or multiple random seeds. Given the known variance in deep learning training, this makes it impossible to assess whether the reported improvements are statistically significant.

### Minor

- **The eigenvalue analysis (Section 7) is heuristic**: The linearization argument that neglects the remainder term r^{k-1} is not rigorously justified, and the claim that convergence of the linearized iteration implies convergence of the original GD is only stated under conditions (τ < 1) that are not verified to hold in practice.
- **Transformer experiments lack architectural details**: The MGT and SGT architectures are described only at a high level; the number of heads, embedding dimensions, and training hyperparameters are deferred to the appendix (which is stripped), making the results difficult to reproduce or assess.
- **The paper claims MGDL "outperforms" SGDL but does not control for total compute**: MGDL trains multiple shallow networks sequentially, which may use different total compute than SGDL. A fair comparison would account for total training time or FLOPs.

### Trivial

- Figure captions are duplicated in the text (e.g., "Figure 1: MGDL at grade 3" appears twice).

## Nice-to-Haves

- Adding error bars or confidence intervals across multiple random seeds would substantially strengthen the empirical claims.
- Comparing MGDL to other iterative refinement or boosting approaches (e.g., AdaBoost, gradient boosting machines) would help contextualize the contribution.
- A discussion of when MGDL might fail or underperform SGDL would improve the paper's balance.

## Novel Insights

The key insight is that MGDL's sequential training of shallow networks on residuals naturally constrains the Hessian spectrum, keeping eigenvalues of the GD iteration matrix within the stable range (-1,1). This provides a mechanistic explanation for why decomposing deep learning into shallower subproblems improves training stability—the spectral properties of shallow networks are fundamentally more favorable than those of deep networks trained end-to-end. The convexification result for single-layer ReLU grades, while limited in scope, provides a clean theoretical justification for why MGDL can avoid the nonconvex optimization difficulties that plague standard deep learning.

## Suggestions

- Address the ReLU non-differentiability issue by either (a) using smooth activations (e.g., GELU, SiLU) in the theoretical analysis while keeping ReLU for experiments, or (b) providing a rigorous treatment of subgradient methods for non-smooth losses.
- Add experiments with standard baselines (e.g., BM3D for denoising, modern CNNs with cross-entropy for CIFAR) to demonstrate that MGDL's advantages are not simply due to weak SGDL baselines.
- Report results with multiple random seeds (at least 5) with mean and standard deviation.
- Clarify the practical feasibility of the convexity result—how large can P_l be before the condition m_l ≥ P_l becomes impractical?

## Score and Decision

The paper presents a novel theoretical perspective on multi-grade training and provides extensive empirical evidence. However, the fundamental mismatch between the theoretical assumptions (twice differentiable loss) and the experimental setup (ReLU activations) undermines the core theoretical claims. The convexity result, while interesting, has limited practical applicability. The empirical evaluation, while broad, lacks statistical rigor and comparison to standard baselines. These issues are major but not fatal—the paper still offers valuable insights and a promising framework.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>