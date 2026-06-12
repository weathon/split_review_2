## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order (ZO) federated optimization method that accelerates convergence while preserving scalar-only communication in federated learning. The method uses a diagonal Hessian approximation as a preconditioner for ZO gradient estimates, achieving this without transmitting any Hessian-related information between clients and server. The authors provide theoretical convergence guarantees showing rates independent of model dimension and Lipschitz constant under certain Hessian approximation assumptions, and demonstrate 1-5× speedup over existing ZO-FL baselines in LLM fine-tuning benchmarks.

## Strengths

- **Addresses a practically important problem**: Communication efficiency in federated LLM fine-tuning is a critical bottleneck, and the idea of accelerating ZO methods with curvature information while preserving dimension-free communication is well-motivated.
- **Clean integration of Hessian information without communication overhead**: The key technical contribution—reusing the scalar representation of ZO updates to approximate the diagonal Hessian—is clever and practically valuable. The method extracts Hessian approximations from the same scalar values already being communicated.
- **Novel theoretical analysis with dimension-independent rates**: The theoretical analysis provides the first convergence result for ZO-FL methods where the rate can be independent of model dimension under Hessian approximation assumptions, offering a plausible explanation for empirically observed faster convergence.
- **Strong empirical results across multiple LLMs and tasks**: HiSo demonstrates consistent speedups (1.4-5.4×) and communication savings (29%-80%) over DeComFL on SST-2, QQP, and SQuAD with OPT models of varying sizes (125M to 2.7B).

## Weaknesses

### Fatal

- **The analysis falls short for the practical τ>1 setting**: The corollary for τ>1 (Corollary 3) shows convergence rate O(√(ζ/τmR) + O(√(τ κ/mR)). The term O(√(τ κ/mR)) still depends on κ, which in prior work Li et al. (2025b) already showed can be bounded by O(Lκ) in the dimension-dependent regime. More critically, the authors claim DeComFL "cannot provide the convergence rate with a low-effective rank assumption when τ>1," but this does not actually demonstrate that HiSo avoids dimension dependence in practical settings. The second term still depends on L and the effective rank through κ = Tr(Σ)/L. The separation claimed between HiSo and DeComFL in the τ>1 setting is overstated and not convincingly demonstrated as dimension-free.

### Major

- **The well-approximated Hessian condition is insufficiently justified**: The paper's core theoretical claim of dimension-free convergence depends critically on the assumption that the diagonal Hessian approximation H_r satisfies Eq. (17) with ζ ≪ d. However, the only empirical evidence for this is a synthetic simulation (Fig. 4) with 200 eigenvalues from a log-normal distribution. No actual Hessian eigenvalue distributions are computed for the LLMs being fine-tuned. Given that H_r is only a diagonal approximation and the method uses the squared update norm as a proxy, whether this condition holds in practice is an open empirical question that the paper does not adequately address.

- **Missing comparison with natural baselines**: The paper compares against first-order FL methods (FedAvg, FedAdam, etc.) only in the final performance table but does not compare against the natural baseline of using first-order methods with communication compression (e.g., gradient quantization/sparsification) that also aim to reduce communication costs. The 90-million-times communication savings claim relative to first-order methods is misleading because it compares apples to oranges—first-order methods with standard compression techniques (e.g., 1-bit SGD, QSGD) would have much lower communication costs than the uncompressed TB-level figures reported.

- **Incomplete communication cost accounting**: The paper reports communication costs in KB for ZO methods, but this appears to only count the scalar gradient values and random seeds. The computation overhead in terms of additional function evaluations per step is mentioned but not integrated into the comparison. Since ZO methods require 2 function evaluations per step (forward passes through the model) versus 1 backward pass for first-order methods, the wall-clock time comparison would differ from the round-based comparison.

- **No analysis of the Hessian update frequency or staleness**: The global Hessian is updated once per communication round, but the analysis does not address how the staleness of Hessian information (especially when clients are inactive for multiple rounds) affects convergence. The reconstruction process for inactive clients uses outdated Hessians, but this effect is not analyzed theoretically or empirically studied.

### Minor

- The mathematical notation is inconsistent in places (e.g., both x_{r,τ} and x_{r,τ}^{(i)}, sometimes dropping the client index i in update equations).
- The paper uses "Hessian-informed" but the actual update is better described as "diagonal preconditioner" since it uses a diagonal approximation.
- The ablation study on ν (smoothing parameter) is only shown for a small CNN on MNIST, not for the LLM tasks.

### Trivial

- Figure 2 and Figure 3 captions contain duplicated text from parsing artifacts.
- The term "ascent direction" is used but the optimization is minimizing loss.

## Nice-to-Haves

- An empirical comparison or analysis of how well the learned diagonal H approximates the true diagonal of the Hessian for LLM tasks would strengthen the paper significantly.
- A wall-clock time comparison or at least a discussion of the computational overhead of ZO methods relative to first-order methods with compression would improve practical relevance.
- Convergence plots for the main LLM experiments (Table 2-3) showing the full training curves rather than just final numbers would be valuable.

## Novel Insights

The paper's core insight—that the scalar-only communication framework for ZO-FL can be generalized to support Hessian-informed preconditioning by reusing the same scalar values already being communicated—is genuinely novel and practically important. The theoretical analysis offering a plausible mechanism for why ZO methods can converge faster than their worst-case dimension-dependent bounds is a valuable contribution to understanding ZO optimization. However, the novelty is somewhat tempered by the fact that Hessian-informed ZO methods already exist in single-node settings, and the key innovation is the FL communication-free integration rather than a fundamentally new optimization algorithm.

## Suggestions

1. Provide a more thorough empirical evaluation of the well-approximated Hessian condition. At minimum, compute the true diagonal Hessian (via Hutchinson's method) for a small model on a simple task and compare with the learned H.

2. Add a benchmark comparing against first-order methods with standard gradient compression (e.g., QSGD, 1-bit SGD at similar effective communication budgets) to provide a fairer comparison.

3. Clarify in the main text that the "TB-level" communication for first-order methods does not account for compression, and provide compressed communication costs for fairer comparison.

4. Include wall-clock time comparisons or at least analyze the computational overhead trade-offs.

5. Provide convergence curves for the LLM experiments to complement the tabular results.

## Score and Decision

The paper addresses an important problem and makes a clever contribution in integrating Hessian information into ZO-FL without communication overhead. The idea is clean, and the empirical results show meaningful improvements over existing ZO-FL baselines. However, the theoretical claims of dimension-free convergence are not convincingly supported—they depend on an assumption that is neither theoretically established nor empirically validated for the practical settings considered. The comparison against first-order methods is misleading due to the lack of compression-aware baselines. These are significant issues that would need to be resolved for acceptance.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>