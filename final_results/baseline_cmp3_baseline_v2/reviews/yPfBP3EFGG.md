## Summary

This paper proposes STNAdam, a stochastic optimizer for “nonconvex + weakly-convex” composite problems. STNAdam maintains two coupled iteration trajectories: an extrapolation track and a regular update track, combining Nesterov momentum with Adam-style adaptive learning rates. The algorithm supports arbitrary variance-reduced gradient estimators (SVRG, SAGA, SARAH) and dynamically schedules hyper-parameters within iterate-dependent intervals. The authors provide a convergence analysis under the Kurdyka-Łojasiewicz (KL) property and demonstrate strong empirical performance on low-light image enhancement (LIE) tasks.

## Strengths

- **Novel two-track framework:** The idea of maintaining two intertwined trajectories (extrapolation and regular update) to simultaneously leverage Nesterov acceleration and adaptive conditioning is a genuine algorithmic innovation over single-track variants like Adam, NAdam, and SNAdam.
- **General convergence theory:** The analysis covers a broad class of problems (nonconvex + weakly-convex), allows arbitrary variance-reduced stochastic gradient estimators, and establishes almost-sure convergence under the KL property with explicit rates. This is a significant theoretical contribution.
- **Strong empirical results on LIE:** STNAdam, especially with SARAH variance reduction, substantially outperforms both standard optimizers (SGD, Adam, SNAdam) and specialized LIE methods (NPE, DeHz, LIME, LR3M, Retinex-Net) on the LOL dataset across PSNR, SSIM, and LPIPS metrics.

## Weaknesses

### Fatal
None.

### Major

1. **Impractical hyper-parameter scheduling:** The adaptive intervals for \(\gamma_{k+1}\), \(\lambda_{k+1}\), and \(\alpha_{k+1}\) depend on problem-dependent constants (e.g., \(V_1, V_2, V_\Upsilon, \rho, L, \tau, M, s\)) that are typically unknown in practice. The paper provides no concrete guidelines for estimating these constants; saying parameters are “randomly selected within some updated intervals” is insufficient. This severely limits the practical applicability of the algorithm.

2. **Unclear and likely flawed runtime reporting:** The reported times in Tables 2 and 3 are on the order of \(10^{-5}\) seconds (e.g., 2.64e-05 s for STNAdam-SARAH). These are implausibly fast for processing entire images on the LOL dataset. Without a clear statement of what these times represent (e.g., per‑iteration time, wall‑clock time for the whole optimization), the speed claims are unreliable and may mislead readers.

3. **Limited empirical validation:** The experiments are confined to a single application (low-light image enhancement) on one dataset (LOL). No experiments on standard machine learning benchmarks (e.g., image classification, language modeling, or synthetic nonconvex problems) are provided. The paper therefore does not demonstrate that STNAdam generalizes beyond this specific task. Comparison with only three generic optimizers (SGD, Adam, SNAdam) omits many relevant modern variants (e.g., AdamW, AMSGrad, AdaBelief, RAdam, AdamP).

4. **Lack of ablation studies:** The design has several components (two‑track structure, two momentum corrections, dynamic scheduling, variance reduction). Without controlled experiments isolating each component, it is impossible to attribute the observed improvement to any specific mechanism. The improvement could come primarily from the variance‑reduced estimator (SARAH) rather than from the two‑track framework.

5. **Strong assumptions in theory:** The convergence results rely on the KL property, the validity of which is not verified for the LIE problem (14) or any other problem in the experiments. The rates depend on the KL exponent \(\vartheta\), which is generally unknown. This limits the practical usefulness of the theoretical guarantees.

### Minor

- The notation is heavy and many constants (e.g., \(A_1,\dots,A_8\), \(M, H, Z, D\)) are introduced without being explicitly defined in the main text, making Section 3 hard to follow.
- Figure 1 captions are extremely long and nearly identical; they could be condensed to improve readability.
- The convergence analysis jumps from “Step 3” to “Step 5” (no Step 4), likely a numbering error.

### Trivial

- The title uses “STNADAM” but the paper consistently uses “STNAdam”. Minor inconsistency.

## Nice-to-Haves

- Provide default values or a practical recipe for setting \(\underline{\gamma}, \underline{\lambda}, \underline{\alpha}\) without needing unknown constants.
- Conduct ablation experiments to separate the contributions of the two‑track mechanism, Nesterov momentum, adaptive learning rates, and variance reduction.
- Test STNAdam on standard deep learning tasks (e.g., CIFAR-10 classification with ResNet, language modeling) to demonstrate generalizability.
- Clarify what the reported “Time(s)” represents and verify it is meaningful (e.g., total wall‑clock time for optimization).

## Novel Insights

Beyond the paper’s own contributions, the most novel insight is that maintaining two coupled update trajectories—one using a standard gradient estimate and another using a Nesterov‑accelerated estimate—can provide a larger effective update neighborhood while continuously exploring better descent directions. This idea could inspire further work on multi‑trajectory optimization methods. However, the practical value of this insight is diminished by the complexity of the resulting parameter scheduling and the lack of evidence that the two‑track structure itself is responsible for the empirical gains.

## Suggestions

- Provide an implementation-friendly version of the algorithm with default hyper‑parameter choices (e.g., fixed \(\gamma, \lambda, \alpha\) or simple annealing rules) that still provides competitive performance.
- Report wall‑clock times meaningfully (e.g., “total time in seconds”) and double‑check the numbers for consistency.
- Include experiments on at least one standard benchmark (e.g., training a small convnet on CIFAR-10) to show the method works beyond LIE.
- Add an ablation study where STNAdam is compared with a variant that removes the two‑track coupling (i.e., one fixed trajectory) while keeping the same adaptive mechanics.

## Score and Decision

The paper introduces a genuinely novel algorithmic idea and provides a thorough theoretical analysis. However, the practical applicability is severely limited by the complex and problem‑dependent hyper‑parameter intervals, the questionable runtime reporting, and the narrow empirical evaluation. Until these issues are addressed, the contribution is not sufficiently compelling for acceptance at ICLR.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>