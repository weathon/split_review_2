## Summary

This paper introduces and analyzes multi-grade deep learning (MGDL), which trains a sequence of shallow networks on the residuals of previous grades, in contrast to standard end-to-end training (single-grade deep learning, SGDL). The authors provide convergence theorems for gradient descent applied to MGDL, prove that when each grade is a single-layer ReLU network the overall problem decomposes into convex subproblems, and present an eigenvalue analysis of the linearized GD dynamics to explain MGDL’s stability advantages. Extensive experiments on image regression, denoising, deblurring, CIFAR-10/100 classification, and transformer time-series forecasting demonstrate that MGDL consistently yields better accuracy and greater training stability than SGDL.

## Strengths

- **Important research question.** Understanding why sequential/residual training can outperform end-to-end learning is a timely and practically relevant problem. The paper clearly frames this question and provides a coherent framework (MGDL) and a suite of experiments to address it.
- **Extensive empirical evaluation.** The paper benchmarks MGDL against SGDL across multiple domains—image reconstruction, classification (CIFAR-10/100), and time-series regression with transformers—using fully connected networks, CNNs, and transformers. The consistent improvement of MGDL across these diverse settings is compelling evidence of its practical value.
- **Eigenvalue stability analysis.** The exposition linking GD dynamics to the spectrum of \(I - \eta H\) is intuitive and well-illustrated with figures. Showing that MGDL’s eigenvalues stay within \((-1,1)\) while SGDL’s often escape provides a plausible geometric explanation for the observed oscillations.
- **Learning-rate robustness study.** The paper demonstrates empirically that MGDL tolerates a much wider range of learning rates than SGDL, which is a practical strength for users who cannot afford extensive hyperparameter tuning.

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical contributions are weaker than claimed.**  
   Theorems 1 and 2 are standard gradient-descent convergence results under Lipschitz smoothness (assuming bounded Hessian and iterates in a compact set). The claim that MGDL enjoys “greater robustness to learning-rate choices” because \(\alpha_l \ll \alpha\) is plausible but not formally proven—the paper provides no bound linking \(\alpha_l\) to \(\alpha\), nor does it show that the admissible range is provably larger. The eigenvalue analysis (Section 7) relies on a linearized approximation whose error term is simply neglected, and convergence of the linearized iteration under \(\tau<1\) does not rigorously guarantee stability of the original GD dynamics. Overall, the theoretical justification for MGDL’s advantage remains heuristic rather than airtight.

2. **Convexity result is limited and disconnected from experiments.**  
   Theorem 3 shows that MGDL with single-layer ReLU grades reduces to a sequence of convex programs, but this result applies only to that very specific architecture. The paper’s own experiments use deeper grades (e.g., two hidden layers per grade in image regression, CNNs in classification, multi-head attention in transformers) for which the convexity property does not hold. Moreover, the convex program (8) requires \(m_l \ge P_l\), where \(P_l\) can be exponential in the data dimension, and the paper does not discuss how to solve it efficiently. Hence the convexity theorem, while theoretically interesting, has no bearing on the practical performance reported.

3. **Classification experiments lack accuracy metrics.**  
   On CIFAR-100 (and CIFAR-10 in Section 7) the paper reports only training loss, not test accuracy. For classification, accuracy is the standard performance measure, and lower loss does not always translate to higher accuracy. Without test accuracy, the claim that MGDL “outperforms SGDL” on classification tasks is incomplete and potentially misleading. The architecture descriptions (Eqs. 28, 29) are referenced but not given in the main text, making it hard to verify the experimental setup.

4. **Missing comparison with related sequential/boosting methods.**  
   MGDL is essentially a form of greedy sequential training with residual connections—closely related to gradient boosting, AdaBoost, and earlier greedy layer-wise pre-training (Bengio et al. 2006). The paper does not position itself against these well-known approaches, nor does it experimentally compare with them. Without such comparisons, it is unclear whether the benefits observed are unique to MGDL or shared by other sequential-residual frameworks. This oversight weakens the claim of novelty.

### Minor

- The image regression experiments use only 25% of pixels for training. While this is a valid regime, it is a low-data setting where sequential methods naturally excel; a full-data comparison would be informative.
- The eigenvalue analysis is performed only on very small networks (e.g., fully connected with 48 hidden units per layer). For larger models where Hessian computation is infeasible, the analysis does not directly apply, limiting its scope as an explanatory tool.
- The MGDL framework is presented as a single coherent algorithm, but the grade-depth partitioning ( \(\sum D_l = D+L-1\) ) seems arbitrary; no ablation studies are provided to show sensitivity to how depth is split across grades.

### Trivial

- None that affect the evaluation.

## Nice-to-Haves

- Include test accuracy for all classification experiments (CIFAR-10, CIFAR-100).
- Compare MGDL with other residual/boosting methods (e.g., gradient boosting, ResNets) on at least one benchmark.
- Provide parameter counts and total FLOPs for SGDL and MGDL to ensure fair computational comparisons.
- Discuss how to choose the number of grades and the depth per grade in practice.

## Novel Insights

Beyond the paper’s own contributions, the insight that sequential training of shallow subproblems can keep the GD iteration matrix’s eigenvalues strictly inside \((-1,1)\)—while deep end-to-end training pushes them outside—offers a fresh geometric perspective on training stability. Combined with the convexity observation for single-layer ReLU grades, this suggests that the difficulty of deep learning may be largely an artifact of joint optimization of many layers, and that a properly designed sequential scheme can circumvent non-convexity and spectral instability in a principled way.

## Suggestions

1. Add test accuracy (top-1 or top-5) to the CIFAR-100 and CIFAR-10 classification results.
2. Include a comparison with a standard gradient boosting or AdaBoost baseline on at least one task (e.g., image regression) to differentiate MGDL from existing sequential methods.
3. Strengthen the theoretical connection between \(\alpha_l\) and \(\alpha\): either derive a bound showing \(\alpha_l \leq \alpha / L\) under reasonable assumptions, or present empirical evidence that the Hessian norm per grade is indeed much smaller than that of the full deep network.
4. Clarify the novelty of MGDL relative to residual networks and greedy layer-wise training in the introduction.

## Score and Decision

**Score:** 4.0

**Decision:** Reject

The paper addresses an important problem and presents extensive experiments, but its theoretical contributions are oversold and not tightly coupled with the empirical results. The missing classification accuracy, the omission of comparisons with established sequential methods, and the disconnect between the convexity theorem and the actual experiments prevent the paper from providing a convincing, self-contained advance. While the empirical evidence for MGDL’s practical benefits is clear, the paper does not currently meet the bar for acceptance at ICLR given the stated claims of theoretical rigor and novelty.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>