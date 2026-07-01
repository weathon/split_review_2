## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence by leveraging global diagonal Hessian approximations while preserving scalar-only (dimension-free) communication. The method extends the DeComFL framework by incorporating curvature information without transmitting any second-order data. The authors provide convergence analysis showing the rate can be independent of model dimension and Lipschitz constant under a "well-approximated Hessian" condition, and demonstrate 1–5× speedups over DeComFL across LLM fine-tuning benchmarks.

## Strengths

- **Novel and practical idea**: Using gradient scalars that are already communicated to reconstruct a global diagonal Hessian approximation without any additional communication overhead is clever and well-motivated. This directly addresses the tension between curvature-aware optimization and dimension-free communication.
- **Generalized framework**: The paper first presents a generalized scalar-only communication FL framework that decouples the approach from vanilla ZO-SGD, enabling integration of more sophisticated optimizers. This is a valuable conceptual contribution beyond the specific HiSo algorithm.
- **Convergence analysis with multiple local updates**: The theory extends to the τ > 1 (multiple local updates) setting, which DeComFL did not support in its convergence analysis. This is a nontrivial theoretical contribution that addresses a genuine gap in the literature.
- **Consistent empirical gains**: Across three LLM families (OPT-125M, 350M, 1.3B) and three tasks (SST-2, QQP, SQuAD), HiSo consistently outperforms DeComFL and other ZO baselines in both convergence speed and final accuracy while maintaining the same per-round communication cost.

## Weaknesses

### Fatal
None.

### Major
- **Conditional theoretical guarantees**: The core theoretical claim of dimension-independent convergence (Corollary 1) relies on the "well-approximated condition" (Definition in Eq. 17), which is not guaranteed by the algorithm and cannot be verified in practice. The paper acknowledges this but then uses it as the basis for the main theoretical selling point ("first such result for ZO methods in FL"). Without a provable guarantee that HiSo actually satisfies this condition during training, the theoretical advancement over DeComFL's O(√(Ld/mR)) rate is conditional and limited in impact.
- **Limited empirical scale and setup**: The FL system uses only 6 total clients with 2 sampled per round, which is very small. Experiments are restricted to OPT models up to 2.7B. While computational constraints are understandable, the lack of larger-scale validation (more clients, larger models, cross-device settings) weakens the practical claims, especially given that communication efficiency is most critical at truly large scales.
- **No comparison with other Hessian-aware FL methods**: The paper compares primarily with DeComFL and standard first-order FL baselines. However, methods like FedAdam with per-coordinate scaling also leverage curvature-like information (via gradient variance). A direct comparison showing that HiSo achieves similar or better per-round progress than FedAdam while using orders of magnitude less communication would strengthen the paper, but is absent.

### Minor
- The "well-approximated condition" (17) includes a somewhat arbitrary factor of 2 ("safety factor") without clear justification. The definition mixes two cases (L-smoothness and low effective rank) with different upper bounds, making it less clean.
- The theoretical result includes an O(ημ) term from the ZO smoothing parameter, which is standard but means the rate is not strictly dimension-free even under the ideal assumptions.
- Figure captions and some figure content appear duplicated or garbled, making certain illustrations hard to interpret.

### Trivial
- The notation H_r is used for the Hessian approximation but its relationship to the actual Hessian Σ_r,k could be made clearer (H_r approximates the inverse of the diagonal Hessian, but the paper sometimes writes as if H_r ≈ ∇²f).

## Nice-to-Haves
- An ablation study showing how the quality of the learned Hessian H evolves over training (e.g., correlation with true diagonal Hessian on a small model) would strengthen the empirical support for the "well-approximated" assumption.
- Discussion of how to handle the case when the low-effective rank assumption fails (e.g., in non-overparameterized regimes) would improve practical guidance.

## Novel Insights

Beyond the paper's own contributions, one genuinely novel observation is that the diagonal of the ZO update vectors Δx (which are available for free as part of the communication protocol) can serve as a surrogate for the diagonal Hessian. This insight connects the scalar-only communication framework with adaptive preconditioning in a way that is both theoretically grounded and practically efficient. The analysis relating the whitening rank ζ to the effective rank κ provides a plausible explanation for why Hessian-informed ZO can be much faster than the worst-case O(d) bound, and this explanation is supported by the long-tail distribution of learned Hessian values shown in Figure 5.

## Suggestions

- Provide a clearer discussion of when the "well-approximated condition" is likely to hold or fail, and add experiments that measure the whitening rank ζ during training (even approximately) to validate the theoretical story.
- Include a comparison with FedAdam (which also uses per-coordinate scaling) in terms of convergence *rounds* (not just communication cost) to decouple the effect of curvature adaptation from the communication savings.

## Score and Decision

Score: 6

Decision: Accept

The paper proposes a clever method with a clean theoretical framework and consistent empirical improvements. The main limitations are the conditional nature of the theoretical guarantees and the modest scale of experiments. However, the core idea is novel, the generalized framework is valuable, and the empirical results convincingly demonstrate practical acceleration. These contributions outweigh the weaknesses, making the paper worthy of acceptance at ICLR.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>