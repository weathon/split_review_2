## Summary
This paper proposes Multi-Grade Deep Learning (MGDL), which trains a sequence of shallow networks on the residuals of previously trained grades, and provides theoretical and empirical arguments for why it outperforms standard end-to-end training (SGDL). The authors establish convergence guarantees for gradient descent on MGDL, show convexity when each grade is a single ReLU layer, and analyze the eigenvalue distributions of Jacobian matrices to explain stability. Experiments on image regression, denoising, deblurring, CIFAR-10/100, and time-series transformers are presented to demonstrate MGDL’s advantages.

## Strengths
- **Attempt at theoretical justification**: The paper provides convergence theorems for GD applied to MGDL, and a convex reformulation for single-layer ReLU grades (Theorem 3, building on Pilanci & Ergen 2020). The eigenvalue analysis offers an intuitive explanation of why shallow grades can avoid oscillatory training.
- **Broad experimental scope**: Experiments span multiple tasks (regression, denoising, deblurring, classification, time series) and architectures (fully connected, CNN, transformer), showing consistent improvements of MGDL over SGDL.
- **Learning-rate robustness study**: Section 6 systematically demonstrates that MGDL maintains good performance over a wider range of learning rates than SGDL, which is a practically relevant finding.

## Weaknesses
### Fatal
None.

### Major
1. **Unfair experimental comparison**: The architectures used for SGDL and MGDL are not matched in depth, capacity, or parameter count. For image tasks, SGDL is a deep fully connected network (e.g., 8 hidden layers) while MGDL uses 4 grades each with 2 hidden layers – the total depth differs, and the deeper SGDL naturally suffers more from training instability. Similarly for transformers, SGT uses a deep stack of blocks while MGT trains single-block transformers sequentially. This confounds the effect of the multi-grade strategy with the effect of network depth. A proper comparison would control for total model depth or capacity.

2. **Weak theoretical novelty and rigor**:
   - The convergence theorems (Theorems 1 and 2) are standard GD convergence results for smooth nonconvex functions, but they assume the activation is twice continuously differentiable, whereas ReLU (used throughout experiments) is not. The mismatch is not addressed.
   - The convexity result (Theorem 3) is a direct application of Pilanci & Ergen (2020) to each shallow grade; the claimed “extension from shallow to deep architectures” is simply the multi-grade decomposition itself, which is already defined in Section 3.
   - The eigenvalue analysis (Theorem 4 and Section 7) is heuristic: it linearizes the gradient and argues that eigenvalue location determines stability, but does not rigorously prove that MGDL’s eigenvalues are always within (-1,1) while SGDL’s are not. The empirical eigenvalue plots are for very small networks (e.g., 48 hidden units) and may not generalize.

3. **Incomplete evaluation on classification**: For CIFAR-100 the paper only reports training loss (Figure 3) and no test accuracy. For CIFAR-10 eigenvalue analysis, only training loss is shown, and the setting (fully connected network, 10,000 samples, full-batch GD, MSE loss) is far from standard practice. Without test accuracy, the practical benefit for classification is unsubstantiated.

4. **Missing comparison to related iterative refinement methods**: MGDL trains shallow networks on residuals, which is conceptually very close to boosting, gradient boosting, and residual learning (ResNets). The paper does not discuss or compare against these well-established approaches, leaving the novelty of MGDL unclear.

5. **Scalability claims not supported**: The paper uses small networks (e.g., 128 hidden units, 4 grades) and limited datasets. The claim that MGDL is a “scalable framework” is not backed by experiments on modern large-scale architectures or datasets (e.g., ImageNet, large transformers).

### Minor
- The paper often writes equations without fully specifying dimensions, and some notation (e.g., the recursive definition in Eq. (3)) is hard to follow.
- The “single-grade” vs. “multi-grade” terminology is non-standard and could cause confusion with existing literature on curriculum learning or stagewise training.

### Trivial
None.

## Nice-to-Haves
- A more rigorous connection between the eigenvalue analysis and the actual nonlinear training dynamics, perhaps using the theory of the Edge of Stability (Cohen et al., 2021).
- Controlled experiments where the total number of parameters and training budget are matched between SGDL and MGDL.
- Comparison on standard classification benchmarks with cross-entropy loss and test accuracy.

## Novel Insights
None beyond the paper’s own contributions. The combination of convex reformulation (per grade) and eigenvalue stability analysis is a plausible explanation for why training shallow subproblems sequentially can be more stable than training a deep network end-to-end. However, the same insights could largely be obtained from known results on shallow networks and the difficulty of deep optimization.

## Suggestions
1. **Match model capacity and depth** in SGDL vs. MGDL experiments. For example, take a deep SGDL network of total depth D, and decompose it into L shallow grades that together have the same total depth D+L-1 as defined in the paper, and compare end-to-end training of the full deep network vs. sequential training of the grades.
2. **Provide test accuracy** for CIFAR-10 and CIFAR-100, and use cross-entropy loss for classification as is standard. Evaluate on larger networks and datasets to substantiate scalability claims.
3. **Compare MGDL to gradient boosting** (e.g., XGBoost, LightGBM) and to deep residual networks with skip connections, which also address training stability.
4. **Fix the activation assumption** in the convergence theorems to cover ReLU (e.g., by treating it as piecewise twice differentiable and analyzing subgradients).
5. **Tighten the eigenvalue analysis**: derive a bound on the Hessian spectral norm for shallow grades vs. deep networks, and show theoretically why MGDL’s eigenvalues stay within (-1,1) for a larger set of learning rates.

## Score and Decision
The paper addresses an interesting practical question and contains a breadth of experiments, but the theoretical contributions are incremental and the experimental comparisons are fundamentally flawed because architectures are not matched. The case for MGDL’s practical advantage over standard deep learning is not convincingly made. I recommend rejection.

**MY FINAL SCORE:** <score>3</score>  
**MY FINAL DECISION:** <decision>Reject</decision>