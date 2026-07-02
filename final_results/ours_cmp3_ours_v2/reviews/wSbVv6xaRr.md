## Summary

This paper introduces FedMPDD, a federated learning algorithm that compresses client gradients via multi-projected directional derivatives. Instead of transmitting full *d*-dimensional gradients, each client computes *m* random directional derivatives (*m* ≪ *d*), sends the resulting scalars plus a random seed, and the server reconstructs the gradient estimate. The paper claims O(1/√*K*) convergence (matching FedSGD), inherent privacy against gradient inversion attacks from the rank-deficient projection, and a tunable privacy-communication-accuracy trade-off via the parameter *m*. Experiments on MNIST and CIFAR-10 demonstrate communication savings and low SSIM scores under gradient inversion attacks.

## Strengths

1. **Well-motivated and clean algorithmic idea.** The multi-projection approach is a principled fix for the dimension-dependent variance of a single projected directional derivative (which the paper correctly identifies as O(*d*/√*K*) for the single-projection baseline). Averaging *m* projections produces an unbiased estimator with a closed-form variance expression (Lemma 1: relative MSE = (*d*−1)/*m*). The protocol's use of client-specific random seeds to avoid transmitting the projection vectors is a practical design choice.

2. **Consistent empirical privacy evaluation.** FedMPDD achieves SSIM < 0.22 across two attack methods and two datasets, while competing compression methods (lp-proj, Top-k, QSGD, SA-FedLora) all yield SSIM > 0.74 under the same attacks (Tables 1–2). This gap is large enough to be practically meaningful and is the paper's strongest empirical result.

3. **Transparent three-way trade-off.** The parameter *m* directly controls communication per round (O(*m*)), gradient reconstruction error ((*d*−1)/*m*), and the multi-round privacy bound (*T* × *m* < *d*). This is laid out more explicitly than in most compression or privacy papers.

## Weaknesses

### Major

1. **Abstract convergence rate contradicts Theorem 2.** The abstract states "FedMPDD converges at a rate of O(1/*K*), matching the performance of FedSGD" (line 9), but Theorem 2 and the contributions list (lines 114 and 32) both state O(1/√*K*). For non-convex smooth SGD, O(1/√*K*) is the standard rate, so the abstract is wrong on two counts: the rate is overstated by a factor of √*K*, and it does not match FedSGD (which converges at O(1/√*K*), not O(1/*K*)). This is the most visible part of the paper and must be corrected.

2. **Unresolved tension between the exact variance and the convergence analysis.** Lemma 1 gives the per-client relative MSE as (*d*−1)/*m*. For the CIFAR-10 experiment (*d* ≈ 300K, *m* = 600), this is roughly 500×‖*g*‖² — a very large noise level (standard deviation ≈ 22‖*g*‖ per client). Averaging over 10 participating clients reduces this to ≈ 7‖*g*‖, still substantial.

   The convergence guarantee (Theorem 2) instead relies on a Johnson–Lindenstrauss bound (Eq. 4) that controls the *norm* of the reconstructed gradient, bounding ‖ĝ‖ ≤ (1+*ε*)‖*g*‖ with *m* = O(log(*d*)/*ε*²). However, controlling ‖ĝ‖ is not the same as controlling the estimation error ‖ĝ − *g*‖ — a vector can have its norm approximately preserved while being nearly orthogonal to *g*, yielding a large estimation error. The convergence bound (5) contains an O(*εG*²/√*K*) term where *ε* = O(√(log *d*/*m*)), but the relationship between this JL-*ε* and the exact variance (*d*−1)/*m* is not analyzed. The two quantities scale very differently: the JL argument suggests *m* = O(log *d*) suffices for bounded distortion, while the variance expression implies *m* = O(*d*) is needed to keep relative error below 1. Without seeing the full proof (the appendix is stripped), this gap is a significant theoretical concern that undermines confidence in the claimed dimension-insensitive convergence.

### Minor

3. **Strength of the privacy guarantee is overstated.** The paper presents Lemmas 1–2 as a formal privacy guarantee, but two issues limit their practical force:

   (a) The transition from gradient-level uncertainty (Lemma 1) to data-level protection (Lemma 2) depends on *Lᵥ*(*x*), the Lipschitz constant of the gradient with respect to the input. This constant is not estimated or bounded for any of the tested models. For deep networks, *Lᵥ*(*x*) can be large enough to make the lower bound vacuous.

   (b) The multi-round composition bound (Remark 2: *T* × *m* < *d*) is restrictive: for the CIFAR-10 experiments (*d* ≈ 300K, *m* = 600), this gives *T* < 500 rounds, while training from scratch typically requires many more iterations. The paper acknowledges this but offers only an empirical claim about "natural evolution of gradients" without supporting evidence.

4. **Communication savings are modest when compared against actual compression methods.** The paper prominently advertises a "356× reduction" compared to FedSGD, but FedSGD transmits uncompressed gradients and is not a compression baseline. Against methods designed for communication efficiency (lp-proj, Top-k, SA-FedLora), FedMPDD achieves a 1.4–1.8× reduction (1.32 GB vs 1.84–2.30 GB in Table 2). This is a modest improvement that should be contextualized rather than contrasted with the 356× headline number. The paper's genuine advantage over compression baselines is the *joint* communication + privacy benefit, which is a legitimate contribution better served by de-emphasizing the FedSGD comparison.

### Trivial

None beyond the issues captured above.

## Nice-to-Haves

- Reporting results with multiple random seeds (confidence intervals) would strengthen the empirical evaluation, especially given the stochastic nature of the projections.
- Wall-clock time or computational overhead analysis would help practitioners assess the O(*dm*) per-client computation cost.
- Estimating *Lᵥ*(*x*) for the tested models would help readers assess the practical strength of the data-level privacy bound.

## Removed Points

These points from the input review were removed:

- "The JL argument goes beyond standard JL" — The paper's application of JL to the composed mapping (1/*m*)*UU*^T applied to a single gradient vector is a standard use of distributional JL; this specific sub-claim is incorrect.
- "Assumption 1 is not stated in the main paper" — Assumptions may reside in the appendix (which is stripped by the parser); per instructions, weaknesses about missing appendix content are removed.
- "Garbled figure caption from parser" — This is a PDF-parser artifact, not an author error.
- Various unsupported speculations (e.g., "the bound [from JL] is not an immediate consequence") — removed as factually incorrect or unverifiable.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the abstract to state O(1/√*K*) convergence, consistent with Theorem 2.
2. Reconcile the exact variance expression (*d*−1)/*m* with the JL-based convergence analysis — either by showing how the two relate, or by clarifying why the JL norm-preservation argument suffices for the proof despite not bounding the estimation error directly.
3. Present the communication savings primarily against compression baselines (where the improvement is 1.4–1.8×) and qualify the privacy guarantees more carefully, particularly the dependence on *Lᵥ*(*x*) and the restrictiveness of the *T* × *m* < *d* bound.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| bEgDEyy2Yk.md (minimax paths) | 1.00 | R1 | Unrelated topic; score 1 indicates broken/nonsense paper — not comparable |
| 0jmFRA64Vw.md (FedComLoc) | 3.00 | R1 | FL compression with local training; accepted-level experiments but limited novelty |
| zqXANcFO9T.md (DEFD-PSGD) | 1.67 | R1 | Decentralized compression with error-feedback; rejected for poor presentation |
| Jl0aEFrp11.md (FedBNLACA) | 2.75 | R1 | Bidirectional compression FL; mixed reviews, rejected |
| IsHWcsk4Fz.md (FedADM) | 3.00 | R1 | Adaptive FL with dissimilarity; rejected for limited contribution |
| 9TSv6ZVhvN.md (Improving Accel FL) | 4.67 | R1 | FL + compression + importance sampling; solid theory but only logistic regression experiments |
| J7hIz9GXKq.md (Collaborative Compressors) | 5.25 | R1 | DME compressors with theoretical gap (non-decaying term); rejected |
| L9eEfwwUwU.md (SAFL) | 4.50 | R1 | Sketched adaptive FL; theoretical novelty, limited experiments, rejected |
| CMMpcs9prj.md (MoTEF) | 6.60 | R1 | Decentralized compression with momentum tracking; strong theory, accepted |
| W0nydevOlG.md (DP-FL Time-Adaptive) | 7.00 | R1 | DP-FL with adaptive privacy spending; strong paper, accepted |
| ZU42Wrcqfm.md (FedSMU) | 5.75 | R1 | Sign-based FL compression; good experiments, rejected due to novelty concerns |
| Pv6fwGPgrA.md (Prune at Clients) | 4.20 | R1 | FL sparse training; mixed reviews |

**Round 1 bracket:** The paper's closest topical matches are in the 3.0–5.75 range. The core idea (projected directional derivatives in FL) has more novelty than FedADM (3.00) or FedComLoc (3.00), and the experimental evaluation is more complete than Improving Accelerated FL (4.67, logistic regression only). However, the abstract error and the unresolved variance-vs-JL gap are more serious flaws than what the 5.0+ anchors (Collaborative Compressors at 5.25, SAFL at 4.50) contend with, placing this paper below those. The final score of **4.0** reflects: a genuinely novel algorithmic idea that is clearly explained and empirically validated on real tasks, weighed against a factual error in the abstract, a significant theoretical concern about the convergence proof that is not resolved in the main text, and overstated privacy claims.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>