## Summary

This paper proposes **HiSo**, a Hessian-informed zeroth-order federated optimization method. Its core contribution is a clever mechanism that repurposes the scalar ZO gradient update vectors (Δx) — which are already communicated — to estimate a diagonal Hessian preconditioner, accelerating convergence while strictly preserving dimension-free (scalar-only) communication. The paper also presents a generalized scalar-only communication FL framework that decouples the approach from vanilla ZO-SGD. Empirically, HiSo achieves 1.4–5.4× round-speedup over DeComFL across LLM fine-tuning tasks (SST-2, QQP, SQuAD) with up to 94M× communication savings versus first-order methods. Theoretical analysis attempts to establish dimension-independent convergence under a well-approximated Hessian condition.

## Strengths

1. **Genuinely clever core idea (Section 4.2).** The insight that the ZO gradient update vectors Δx — already communicated as scalars — can be repurposed to estimate a diagonal Hessian preconditioner without any extra communication is both novel and non-trivial. This cleanly resolves the tension between curvature-aware optimization and dimension-free communication.

2. **Generalized framework is a real contribution (Section 3.3, Algorithm 1).** Decoupling scalar-only communication from vanilla ZO-SGD is architecturally significant. It opens the door for future methods beyond both ZO-SGD and HiSo.

3. **Clean empirical results (Tables 2 and 3).** The communication speedups (1.4–5.4× over DeComFL) are meaningful, and HiSo consistently achieves higher test accuracy than all ZO baselines across all tasks. The communication savings relative to first-order methods (KB vs TB) are genuinely impressive.

4. **Honest treatment of theoretical limitations (line 285).** The paper explicitly acknowledges that it is "hard to determine if this [well-approximated] condition holds" for LLMs and notes that at worst HiSo degenerates into DeComFL. This candor is appreciated, even if the theoretical framing in the abstract is stronger than what is established.

## Weaknesses

### Fatal
None.

### Major

1. **The "dimension-free" convergence rate depends on a condition whose satisfaction by the update rule is unverified (Definition Eq. 17, Corollary 1).** The paper defines H as a well-approximate matrix of Σ if ζ = Tr(H^{-1/2} Σ H^{-1/2}) ≤ ζ (where ζ is independent of d), and then Corollary 1 gives an O(√(ζ/mR)) convergence rate — independent of d — under this condition. The issue is that ζ is *defined* as the trace quantity that the corollary then claims is small. The paper provides no independent argument that its specific Hessian update rule (Eq. 12) produces an H satisfying ζ ≪ d for LLM Hessians. The numerical experiment in Fig. 4 uses a synthetic log-normal eigenvalue distribution rather than a learned H from Eq. 12, so it does not fill this gap. The paper acknowledges this limitation in prose (line 285), but the abstract and introduction still claim a convergence rate "independent of... model dimension d" (line 27) without caveat commensurate with the evidence.

2. **The Hessian update rule's relationship to the actual Hessian is not established (Eq. 12).** The paper updates H via H_{r+1} = (1-ν)H_r + ν·Diag([Δx_{r,0}]² + εI), where Δx is a ZO gradient estimate, and justifies it as "Adam-style." However, Adam squares *first-order* stochastic gradients, whose second-moment expectation relates to the Fisher information. For ZO estimates, the expected squared value E[Δx Δxᵀ] involves a mixture of gradient outer-product terms and Hessian terms through a more complex relationship. The paper never derives what quantity E[Diag(|Δx|²)] actually estimates, nor does it establish conditions under which gradient contamination of the Hessian signal is negligible. Without this, the claim that Eq. 12 "learns global curvature" (Section 4.2) lacks grounding.

### Minor

3. **Tension between the whitening argument and the Hessian approximation goal.** The theory's "low whitening rank" ζ = Tr(H^{-1/2} Σ H^{-1/2}) is small when H *does not* closely approximate Σ (since H ≈ Σ gives ζ ≈ d, the worst case). The paper acknowledges this (line 224: "If H is the perfect approximation of Σ, then ζ = d") and pivots to a Wiener filtering analogy. However, the update rule (Eq. 12) tries to approximate the diagonal of Σ, which would push ζ toward d. The paper does not fully reconcile this tension or characterize what kind of H the update rule actually produces and whether it satisfies the condition needed for the theory.

4. **Limited experimental scale.** The LLM experiments use only 6 clients with 2 sampled per round — a very small FL system. Models are limited to OPT-2.7B (modest by 2026 standards). The paper does not study how performance scales with client count or model size, which limits confidence in the method's practicality for real FL deployments.

5. **Missing analysis of failure cases.** The paper does not examine when HiSo might underperform. For instance, on OPT-1.3B+QQP, HiSo's communication cost (96.67 KB) more than doubles DeComFL's (43.95 KB), but the paper only mentions this in passing. Understanding when the Hessian preconditioner hurts would strengthen the paper's practical guidance.

### Trivial
None.

## Nice-to-Haves

- An ablation comparing HiSo against a variant that uses a fixed (non-adaptive) diagonal preconditioner, or against HiSo with H=I throughout (recovering DeComFL), would isolate the benefit of the Hessian adaptation.
- Clarification of whether the clipping step mentioned in Assumption 4 was used in experiments.
- A clearer explanation of the stopping criterion for DeComFL's "fully converged" state used in Table 2.

## Removed Points

- **"90 million times claim not traceable"**: The critic questioned traceability of the 90M× savings figure, but Table 3 directly shows FedZO on OPT-1.3B+SST-2 costs 4.73 TB vs HiSo's 49.18 KB, yielding ~94M× savings. The figure is traceable.
- **"Evaluation metric favors HiSo"**: The critic argued the speedup metric in Table 2 is asymmetric. However, Table 3 shows HiSo's final accuracy *exceeds* DeComFL's in every case, so matching DeComFL's best is a conservative comparison. The asymmetry, if anything, favors DeComFL.
- **"Factor of 2 in Table 1 unexplained"**: The paper explicitly states (line 249) that the factor 2 is "just a safety factor to tolerate the imperfect inverse." This is acknowledged and intentional.
- **"Repeated figure captions"**: Parser artifact from PDF extraction; not present in the original submission.
- **"Missing clipping details"**: The paper mentions clipping as a design option (line 265); whether it was used is an implementation detail more appropriate as a nice-to-have than a weakness.
- **Missing larger-scale experiments / more clients**: These are scope limitations that do not undermine what was done.
- **Missing ablation of Hessian update**: A reasonable request but a nice-to-have, not a core weakness.

## Novel Insights

The most penetrating observation from the reviews is the fundamental tension between the paper's theoretical framework and its practical update rule. The theory requires ζ ≪ d, which occurs when H *differs substantially* from Σ in a specific way (over-emphasizing low-curvature directions like a Wiener filter). But the update rule (Eq. 12) accumulates the squared ZO gradient, which one would expect to approximate Σ's diagonal — the exact opposite of what the theory needs. The paper's acknowledgment of this (line 224) shows awareness but does not resolve it. This tension suggests that if HiSo works well in practice, the mechanism may be closer to RMSProp-style variance adaptation (where the squared gradient adaptively normalizes each coordinate) rather than genuine Hessian approximation. The paper would benefit from clarifying this distinction explicitly rather than presenting the Hessian framing as the primary justification.

## Suggestions

1. Either derive what Diag(|Δx|²) estimates for ZO gradients and under what conditions it reflects Hessian rather than gradient information, or reframe the Hessian update as a variance-adaptive preconditioner (analogous to RMSProp for ZO) rather than claiming it learns Hessian structure.

2. Calibrate the theoretical claims in the abstract and introduction to match what is actually established: Theorem 1's convergence bound (which does not require the well-approximated condition) should be the headline result; the dimension-free corollary should be presented as a conditional explanation, not a proven guarantee.

## Score and Decision

The paper makes a genuinely clever practical contribution with solid empirical support. The core ideas — repurposing Δx for preconditioning and generalizing scalar-only communication — are novel and useful. However, two structural issues weaken the presentation: (1) the theory's headline result (dimension-free convergence) depends on an unverified condition that is not shown to be satisfiable by the proposed update rule, and (2) the Hessian update's relationship to the actual Hessian is not formally established. These are addressable with clearer framing and additional analysis. The empirical case for the method stands on its own merits.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>