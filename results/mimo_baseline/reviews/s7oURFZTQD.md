## Summary

This paper provides theoretical and empirical analysis of Multi-Grade Deep Learning (MGDL), which decomposes deep network training into sequential shallow sub-problems, compared to standard single-grade deep learning (SGDL). The authors prove convergence guarantees for GD on MGDL, show that MGDL with single-layer ReLU grades decomposes into convex subproblems, and demonstrate via eigenvalue analysis that MGDL maintains iteration eigenvalues within (-1,1) for stable convergence while SGDL's eigenvalues frequently exceed this range. Comprehensive experiments on image regression, denoising, deblurring, CIFAR-10/CIFAR-100 classification, and transformer-based time series tasks consistently show MGDL advantages in stability and accuracy.

## Strengths

- **Novel convex reformulation (Theorem 3):** The extension of Pilanci & Ergen (2020) from shallow to deep architectures via the multi-grade decomposition is a genuine and elegant theoretical contribution. Showing that the nonconvex deep ReLU network optimization decomposes into a sequence of convex programs—provided the neuron count per grade meets the number of activation regions—provides structural insight into why MGDL is easier to train.

- **Insightful eigenvalue analysis framework:** The linearized GD analysis (Theorem 4) combined with empirical eigenvalue monitoring across multiple tasks (synthetic regression, image reconstruction, CIFAR-10) provides a clear and compelling mechanistic explanation for MGDL's stability advantage. Figures 4-6 consistently show SGDL eigenvalues dropping below -1 (correlating with loss oscillation) while MGDL's remain within (-1,1), offering a unifying narrative across tasks.

- **Comprehensive and consistent experimental evidence:** The paper benchmarks MGDL against SGDL across image regression, denoising, deblurring (Tables 1-3), CIFAR-100 classification (Figure 3), and transformer-based time series (Tables 4-5, Figures 7-8), covering fully connected networks, CNNs, and transformers. MGDL consistently shows gains of 0.16–4.23 dB in PSNR and significantly lower classification loss, with qualitatively different training dynamics (smooth vs. oscillatory).

- **Learning rate robustness analysis (Section 6):** The systematic study showing MGDL remains effective over a much wider learning rate range ([0.01, 0.3] vs. [0.03, 0.08] for SGDL in one setting) has practical value and directly supports the theoretical prediction that α_l ≪ α yields a wider admissible η interval.

## Weaknesses

### Fatal

None.

### Major

- **Smooth activation assumption vs. ReLU practice:** The convergence theorems (1, 2) require σ to be "twice continuously differentiable," yet all experiments use ReLU, which is not even once differentiable at zero. The paper never discusses this gap or how to bridge it (e.g., smooth ReLU approximations). This disconnect weakens the theoretical claims' applicability to the settings actually studied.

- **Weak baselines throughout:** All SGDL comparisons use vanilla architectures without modern training enhancements such as batch normalization, residual connections, learning rate scheduling, or data augmentation (for classification). This makes it difficult to attribute the gains specifically to the multi-grade decomposition rather than to comparing against an under-optimized baseline. For CIFAR-100 (Section 5), using MSE loss instead of cross-entropy is atypical and likely disadvantages SGDL relative to standard practice.

- **The key claim α_l ≪ α is asserted without proof:** The central theoretical argument that MGDL admits wider learning rates because each grade has a smaller Hessian spectral norm (α_l) than the full network (α) is stated as obvious from the shallower structure but never formally established. Without bounds relating α_l to α as a function of depth/width, this remains an intuition rather than a theorem.

- **No computational cost analysis at parity:** MGDL trains L networks sequentially, and the total parameter count across grades can exceed SGDL's. The paper does not provide wall-clock time or FLOP comparisons at matched compute budgets, making it impossible to assess whether MGDL's accuracy gains come "for free" or at significant additional cost.

### Minor

- **Convex reformulation's practical scope:** The condition m_l ≥ P_l (neurons ≥ number of activation pattern regions) can be exponentially large in input dimension. The paper does not discuss when this condition is met in practice or what happens when it is violated, limiting the practical impact of Theorem 3.

- **Transformer experiments are limited:** Tables 4-5 and Figures 7-8 show dramatic MGT advantages, but only on two time series tasks with architectures detailed in an appendix. The lack of standard transformer benchmarks (e.g., language modeling, standard time series benchmarks) limits the generalizability of the MGT claims.

- **Eigenvalue analysis is empirical, not predictive:** While the eigenvalue plots are compelling, they are computed post-hoc during training. The paper does not provide a way to predict a priori whether a given architecture/task will exhibit eigenvalues outside (-1,1) for SGDL, limiting the framework's predictive utility.

### Trivial

None.

## Nice-to-Haves

- A discussion of how the convergence theory extends to smooth approximations of ReLU (e.g., softplus or smoothed ReLU) to close the gap with experiments
- Comparison against SGDL with modern training techniques (batch norm, residual connections, cosine LR schedule) to isolate MGDL's specific contribution
- Wall-clock time and FLOP comparisons at matched total compute budgets
- Experiments on larger-scale benchmarks (e.g., ImageNet, standard NLP tasks) to demonstrate scalability

## Novel Insights

The eigenvalue analysis framework connecting MGDL's stability to the spectrum of I - ηH_F(W) is a genuinely useful conceptual contribution. The consistent empirical finding across diverse tasks that SGDL eigenvalues breach (-1,1) (causing oscillation) while MGDL's remain bounded provides a unifying mechanistic explanation that goes beyond task-specific arguments. Combined with the convex reformulation for single-layer ReLU grades, the paper builds a multi-level argument—convexity at the subproblem level, favorable spectral properties at the iteration level—for why the multi-grade decomposition aids optimization.

## Suggestions

- Address the smooth-activation assumption explicitly: either provide convergence results for ReLU (e.g., subgradient-based analysis) or show experiments with smooth ReLU approximations that satisfy the theory's assumptions.
- Include a comparison against SGDL with batch normalization, residual connections, and learning rate scheduling to demonstrate MGDL's advantage is not simply due to using an under-optimized baseline.
- Provide a formal bound on α_l relative to α as a function of network depth/width to substantiate the α_l ≪ α claim.
- Add computational cost comparisons (FLOPs, wall-clock time) at matched total compute budgets for the main experiments.

## Score and Decision

The paper presents a genuinely novel convex reformulation for deep networks via MGDL and an insightful eigenvalue analysis framework, supported by extensive experiments across multiple tasks and architectures. However, the disconnect between the smooth-activation theory and ReLU experiments, consistently weak baselines without modern training techniques, and the unsubstantiated key claim that α_l ≪ α prevent a strong recommendation. The contribution is above the median submission quality but falls short of the rigor expected for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject