## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence while strictly preserving scalar-only (dimension-free) communication. The key insight is to use the global update vectors Δx (which must be tracked anyway for model reconstruction) as a free source of diagonal Hessian information via Diag(|Δx|²), avoiding any additional communication or computation overhead for curvature information. The paper also contributes a generalized scalar-only communication FL framework (Algorithm 1) that decouples the communication format from vanilla ZO-SGD. Empirically, HiSo achieves 1.4–5.4× speedup over DeComFL across OPT-125M to OPT-2.7B on SST-2, QQP, and SQuAD.

## Strengths

- **A genuinely clever zero-cost Hessian estimation trick.** The core insight — using the global update vectors Δx (which must be tracked anyway for model reconstruction in the scalar-only framework) to estimate a diagonal Hessian via Diag(|Δx|²) smoothed by EMA — is elegant. The curvature approximation comes at no extra communication cost. This is a simple-yet-effective idea that makes a clear contribution.

- **Generalized scalar-only communication framework (Algorithm 1).** Separating the scalar-only communication property from vanilla ZO-SGD is a useful contribution that extends beyond HiSo itself. The framework cleanly decouples communication format from optimization algorithm, enabling future work to plug in other methods while maintaining dimension-free communication.

- **Theoretical analysis that generalizes DeComFL and handles τ > 1.** The convergence analysis extends prior work by handling multiple local updates (τ > 1), which DeComFL could not analyze under the low-effective-rank assumption. The recovery of DeComFL's rate as a special case (Corollary 2) provides a useful sanity check.

- **Consistent empirical improvement across multiple model scales and tasks.** HiSo delivers 1.4–5.4× speedup in communication rounds (Table 2) and marginally higher accuracy than DeComFL (Table 3) across OPT-125M, 350M, 1.3B, and 2.7B on SST-2, QQP, and SQuAD. The communication savings are practically meaningful (KB-level vs. TB-level for first-order methods).

## Weaknesses

### Fatal
None.

### Major

- **The accelerated convergence rates are conditional on an unverified assumption.** The headline theoretical results (Corollaries 1–3) depend on the "well-approximated condition" (Definition, Eq. 17), which requires that the learned diagonal Hessian H_r satisfies Tr(H_r^{-1/2} Σ H_r^{-1/2}) ≤ ζ (dimension-independent). The paper's Hessian estimation method (Eq. 12, Diag(|Δx|²) smoothed by EMA) has no established theoretical connection to this condition — there is no proof or sketch that the procedure yields a matrix satisfying it. The paper candidly states "it is hard to determine if this approximation holds in the context of LLMs" (line 285), yet the abstract and introduction present the dimension-independent rate as a headline contribution ("can achieve an accelerated convergence rate that is independent of the Lipschitz constant L and model dimension d") without clearly foregrounding this conditionality. Theorem 1 (unconditional) still holds, but its bound involves ρ̄ which could be as large as O(Ld) in the worst case, matching standard ZO rates. The paper claims performance "at worst case, degenerates into DeComFL" — this is plausible from the unconditional bound but the case where a poor Hessian estimate amplifies noise is not formally analyzed. The MNIST "simulation" (Fig. 4) uses a synthetic log-normal eigenvalue distribution, not the actual Hessian of the trained models, so it does not substitute for verifying that the learned H_r satisfies the condition.

### Minor

- **The LLM experiments use a very small FL system.** The setup involves only 6 clients with 2 sampled per round. Real-world federated fine-tuning often involves 10–100× more clients with higher heterogeneity. There is no study of how HiSo's performance scales with client count or data heterogeneity. Since the Hessian is estimated by averaging over sampled clients' Δx values, its quality likely depends on representative participation — a concern that grows with client count and non-IID partitioning.

- **The metric in Table 2 is unconventional.** Table 2 reports rounds needed for HiSo to *match DeComFL's best test accuracy*, rather than rounds-to-convergence for each method to its own peak. Since HiSo achieves modestly higher accuracy (Table 3), this metric may understate HiSo's advantage. Additionally, the paper does not specify how DeComFL's "best test accuracy" is determined (e.g., early stopping vs. final accuracy), making the speedup hard to interpret precisely.

- **The hyperparameter P is undefined.** The paper states "We set P = 5 for all ZO methods" (line 301) without defining what P represents. If P is the number of perturbations per gradient estimate, this is an important hyperparameter affecting both convergence and computation cost.

- **Minor notational inconsistency in the Hessian update rule.** Equation (12) (the τ=1 simplified case) uses Δx_{r,0} (the global update at round start) for the Hessian estimate, while line 140 (the general formulation) uses |Δx_{r,τ}^{(i)}|² (the client's total update after τ steps). For τ > 1 these differ, and the relationship between the two formulations is not clarified.

### Trivial
None.

## Nice-to-Haves

- Sensitivity analysis for the smoothing parameter ν on LLM-scale experiments (currently only tested on MNIST with three values).
- Discussion of how the model-reset mechanism at the end of each round interacts with any local (client-side) Hessian information that might be accumulated during local steps.
- Quantification of the O(d) memory cost of storing the diagonal Hessian on the server (belongs in main text, though the paper notes Appendix E covers this).

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Missing ablation isolating the Hessian component"** — Removed because DeComFL IS HiSo with H_r≡I (explicitly stated in Corollary 2). The comparison against DeComFL already serves as this ablation. The concern about "other implementation differences" is addressed by the paper's mathematical equivalence statement.

- **"Algorithm 1 is too abstract"** — Removed because the paper explicitly refers to Appendix D (stripped by parser) for the full detailed algorithm with all features.

- **"No wall-clock time reported"** — Removed because the paper states that computation time analysis is in Appendix E (stripped by parser).

- **"Theorem 1's learning rate depends on unknown Hessian (ρ_k)"** — Removed because this is standard in optimization theory; most convergence bounds depend on quantities (L, σ², etc.) that are unknown in practice.

- **"The 90 million times communication savings claim is misleading"** — Removed because it is a technically accurate comparison between ZO and first-order frameworks; it is not specific to HiSo but is clearly contextualized alongside ZO-specific comparisons in Tables 2 and 3.

- **"Model-reset mechanism's interaction with Hessian"** — Removed because HiSo's Hessian is global (server-side), not client-local, so the reset does not discard accumulated curvature information.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the theoretical claims** in the abstract and introduction to match their conditional nature. The current framing ("can achieve an accelerated convergence rate that is independent of L and d") would be more accurate as "can achieve such a rate under the well-approximated condition, which we empirically observe to hold in practice."

2. **Provide empirical evidence** that the learned H_r approximately satisfies the well-approximated condition, even for small models. For example, estimate Tr(H_r^{-1/2} Σ H_r^{-1/2}) via Hessian-vector products for the MNIST CNN or OPT-125M and report the measured ζ vs. d. This would directly bridge the gap between theory and practice.

3. **Clarify the Table 2 metric**: specify how DeComFL's "best test accuracy" is determined (peak of validation curve? final accuracy?) and consider also reporting rounds-to-convergence for each method to its own peak.

4. **Define P** explicitly and discuss the effect of the number of perturbations on convergence quality and computation cost.

5. **Resolve the notational inconsistency** between Eq. (12) and line 140 for the Hessian update rule with τ > 1.

6. **Add a larger-scale FL experiment** or at minimum a discussion of expected scalability behavior as the number of clients grows.

---

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>