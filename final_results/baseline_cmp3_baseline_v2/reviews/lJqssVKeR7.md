## Summary

This paper proposes **HiSo**, a Hessian-informed zeroth-order (ZO) federated optimization method that accelerates convergence while preserving scalar-only communication (no Hessian-related information is transmitted). The key idea is to use a global diagonal Hessian approximation, learned from the gradient scalars themselves, to precondition ZO updates. Theoretically, under low-effective rank and whitening assumptions, HiSo achieves convergence rates independent of the model dimension \(d\) and Lipschitz constant \(L\). Empirically, on LLM fine-tuning benchmarks (OPT-350M to OPT-2.7B), HiSo delivers 1–5× speedup in communication rounds over the state-of-the-art ZO-FL baseline DeComFL, with up to 80% communication savings.

## Strengths

- **Novel and practical idea**: The paper identifies a clever way to incorporate curvature information into ZO-FL without any extra communication overhead—by reusing the gradient scalars that are already communicated to approximate a diagonal Hessian. This directly addresses a key limitation of existing ZO-FL methods (slow convergence) while preserving the dimension-free communication advantage.
- **Solid theoretical analysis**: The paper provides a convergence analysis for HiSo under standard FL assumptions, and introduces the concept of “low whitening rank” to obtain tighter variance bounds. The theory shows that, under the well-approximate Hessian condition, the convergence rate can be independent of \(d\) and \(L\), offering a plausible explanation for the empirically observed fast convergence of ZO methods.
- **Consistent empirical improvements**: Across multiple LLM sizes (OPT-350M, 1.3B, 2.7B) and three tasks (SST-2, QQP, SQuAD), HiSo consistently outperforms DeComFL in both convergence speed and final accuracy, while maintaining the same per-round communication cost. The ablation study on the smoothing parameter \(\nu\) shows robustness.
- **Generalized framework**: The paper proposes a generalized scalar-only communication FL framework that decouples the communication protocol from the specific choice of ZO-SGD, enabling integration of more advanced optimization techniques. This is a useful conceptual contribution that may inspire future work.

## Weaknesses

### Fatal
None.

### Major

1. **Strong theoretical assumptions**: The convergence rate improvements (independence of \(d\) and \(L\)) rely on the “well-approximate matrix of Hessian” condition (Definition 17) and the low-effective rank assumption. The paper acknowledges these are hard to verify, but does not provide direct empirical evidence that the learned diagonal Hessian \(H\) actually satisfies this condition for the models and tasks tested. The long-tail distribution of \(H\) (Fig. 5) is suggestive but not a rigorous verification. Without this condition, the theory degenerates to DeComFL’s rate, which limits the strength of the theoretical contribution.

2. **Limited empirical scope**: The FL setup uses only 6 clients with 2 sampled per round—a very small-scale setting. The paper does not test scalability to larger numbers of clients or more heterogeneous data partitions. The models are limited to OPT up to 2.7B; experiments on larger LLMs (e.g., 7B+) or different architectures (e.g., LLaMA) would strengthen the claims. The accuracy gap between HiSo and first-order methods (e.g., FedAvg, FedAdam) is significant (e.g., 90.34% vs 92.86% on OPT-1.3B SST-2), and the paper does not adequately discuss whether this gap is acceptable given the communication savings.

3. **Lack of clear pseudocode for HiSo**: Algorithm 1 is a generic framework, and the actual HiSo algorithm is described only in text and in the appendix. The main paper would benefit from a concise, self-contained pseudocode for HiSo (including the Hessian update rule and the reconstruction steps). This hurts reproducibility and clarity.

4. **Insufficient baseline comparisons**: The paper compares only against DeComFL and FedZO among ZO methods. There are other adaptive ZO methods (e.g., ZO-AdaMM, ZO-SGD with momentum) that could be adapted to the FL setting. The paper does not compare to any Hessian-aware ZO method in FL (if any exist), nor to simple adaptive learning rate schemes (e.g., per-coordinate scaling without Hessian approximation). This makes it harder to isolate the benefit of the Hessian-informed component.

### Minor

- The notation \(H_r^{-1/2}\) is used without explicitly defining the square root of a diagonal matrix; this is clear to most readers but could be stated.
- The paper claims “first such result for ZO methods in FL” regarding convergence independent of \(d\) and \(L\). While likely true, such claims should be carefully qualified given the strong assumptions.
- The communication cost comparison in Table 3 mixes TB (first-order) and KB (ZO) units, which is dramatic but the accuracy gap is not discussed. A more nuanced discussion of the accuracy-communication trade-off would be helpful.
- The theoretical analysis for \(\tau > 1\) is only briefly mentioned in a corollary; the main paper lacks details on how the client drift term is handled.

### Trivial

None.

## Nice-to-Haves

- Provide a clear, self-contained pseudocode for HiSo in the main paper.
- Include experiments with more clients (e.g., 50 or 100) and non-IID partitions to test scalability.
- Verify the low-effective rank and whitening assumptions empirically on the actual models used (e.g., by computing the eigenvalue distribution of the Hessian or its diagonal approximation).
- Compare against a version of HiSo without the Hessian update (i.e., using a fixed identity preconditioner) to isolate the benefit of the learned Hessian.
- Discuss the computational overhead of the Hessian update (O(d) per step) and confirm it is negligible compared to the forward passes.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the variance of ZO gradient estimates can be dramatically reduced by preconditioning with a diagonal Hessian approximation, and that this approximation can be obtained “for free” from the scalar updates already communicated in ZO-FL. The paper formalizes this through the concept of “low whitening rank” (\(\zeta\)), which can be much smaller than the effective rank (\(\kappa\)) and the dimension \(d\). This provides a principled explanation for why ZO methods can converge much faster than their worst-case \(\mathcal{O}(d)\) bounds in practice, and suggests that curvature-aware preconditioning is a promising direction for making ZO-FL practical.

## Suggestions

- Add a concise pseudocode for HiSo (including the Hessian update and model reconstruction) in the main paper, perhaps in Section 4.3.
- Include an experiment that measures the effective rank and whitening rank on the actual models (e.g., using a subset of parameters) to support the theoretical assumptions.
- Extend the empirical evaluation to at least one larger model (e.g., OPT-6.7B or LLaMA-7B) and a larger number of clients to demonstrate scalability.
- Discuss the accuracy gap to first-order methods more explicitly, and consider whether the communication savings justify the accuracy loss in practical scenarios.

## Score and Decision

**Score**: 6  
**Decision**: Accept

The paper presents a novel and well-motivated method that addresses an important problem (slow convergence of ZO-FL) with a clever solution (Hessian-informed preconditioning without extra communication). The theoretical analysis is a step forward, and the empirical results show consistent improvements over the state-of-the-art ZO-FL baseline. The major weaknesses (strong assumptions, limited empirical scope, lack of pseudocode) are significant but not fatal; they can be addressed in a revision. The paper brings sufficient value to the ICLR community by advancing the understanding and practicality of ZO optimization in federated learning.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>