Now let me read more details about the theoretical sections and experiments to verify additional claims:Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me proceed with Round 1 calibration — bracketing across score bands:Let me read the most relevant anchor papers to calibrate properly:Now I have enough context to form my bracket and finalize the review. Let me analyze the calibration anchors:

**Round 1 Bracket:**
- **Strong reject band (< 1.5):** Unrelated papers (GFlowNets, jailbreaking). HiSo is clearly far above these.
- **Reject band (1.5-3.5):** FedADM (3.0), compressed decentralized learning (1.67), bidirectional FL (2.75). HiSo is significantly stronger — genuine novelty, solid theory, consistent empirical results.
- **Borderline reject band (3.5-5.5):** FZooS (3.67), FeedSign (5.25), FedCO (4.67). HiSo has a more novel core contribution and better execution than these papers. HiSo is above this band.
- **Borderline accept band (5.5-7.5):** **DeComFL (6.25, Accepted)** — the direct predecessor, and **ZO stability analysis (7.0, Accepted)**. HiSo is a direct extension of DeComFL with a clever zero-cost curvature integration, but introduces a new theory-practice gap (well-approximated condition). HiSo sits in this band.
- **Accept band (7.5-8.5):** Papers with very strong and complete contributions (8.0 scores). HiSo's theory-practice gap prevents it from reaching this tier.

**Initial bracket: 5.5 – 7.0**

HiSo is comparable to its predecessor DeComFL (6.25) — it extends the framework meaningfully but the unresolved gap between the algorithm's second-moment estimator and the theory's Hessian assumption, plus the unverified well-approximated condition on actual LLM experiments, makes the contribution less than fully established.

Now let me write the final review:Now I have all the information needed. Let me write the final consolidated review.

## Summary
HiSo proposes a Hessian-informed zeroth-order federated optimization method that integrates diagonal Hessian preconditioning into the scalar-only communication FL framework at zero additional communication cost. The key insight is that the diagonal Hessian approximation can be reconstructed from already-communicated gradient scalars and shared random seeds, exploiting the algebraic structure of ZO updates (Δx = g·H^{-1/2}u). The paper provides convergence theory showing dimension-free and Lipschitz-free rates under a "well-approximated" Hessian condition, generalizes the DeComFL framework, extends convergence guarantees to multiple local updates (τ > 1), and demonstrates 1.4–5.4× speedup over DeComFL on OPT-family LLM fine-tuning benchmarks.

## Strengths

- **Zero-cost curvature integration via algebraic structure (Section 4.2, Eq. 12):** The central insight—that the diagonal Hessian approximation H can be reconstructed from the already-communicated Δx scalars and shared seeds during the model reconstruction step—is genuinely clever. This exploits the algebraic structure of the ZO update to piggyback curvature learning onto existing communication, adding *zero* communication overhead. This is the paper's most distinctive and non-trivial contribution.

- **Generalized scalar-only communication framework (Section 3.3, Algorithm 1):** Decoupling the dimension-free communication paradigm from the specific choice of ZO-SGD is a useful abstraction. The paper cleanly shows that DeComFL is a special case (H_r ≡ I), opening the door for future methods. This is concrete and verified in Corollary 2.

- **Extension to multiple local updates (Corollary 3, Section 5.2):** The paper resolves an acknowledged open question from DeComFL: providing convergence rates under the low-effective rank assumption when τ > 1. The client drift term analysis in Theorem 1 is a meaningful addition for practical FL where multiple local updates are standard.

- **Intellectual honesty about assumptions (Section 5.2, remarks after Corollary 3):** The paper explicitly states (line 285): "it is hard to determine if this approximation holds in the context of LLMs" and that "HiSo, at worst case, degenerates into DeComFL." This candor about the limits of the theoretical claims raises credibility.

## Weaknesses

### Fatal
None

### Major

- **Gap between algorithm's second-moment estimator and theory's Hessian assumption (Section 4.2 Eq. 12 vs. Section 5.1 Eq. 17):** The H update rule (Eq. 12) computes Diag(|Δx_{r,0}|² + εI), which is a second-moment estimator of the ZO update—the paper itself acknowledges this in footnote 2: "our method resembles RMSProp." However, the theoretical corollaries assume H is a "well-approximate matrix of Hessian Σ" satisfying Eq. 17 (Tr(H^{-1/2}ΣH^{-1/2}) ≤ ζ). The paper does not prove or empirically demonstrate that the algorithm's Adam-style H satisfies this condition. This creates a disconnect: the theory assumes a property of H that the algorithm is not shown to guarantee.

- **Well-approximated condition unverified on actual LLM experiments (Section 5.1, Section 6):** All headline claims of dimension-free and Lipschitz-free convergence (Corollaries 1–3) rest on Eq. 17. The only supporting evidence is a synthetic simulation with log-normal eigenvalues (Fig. 4, d=200) and a distribution plot of H entries on CNN/MNIST (Fig. 5 right). Neither demonstrates that Tr(H^{-1/2}ΣH^{-1/2}) is small on the OPT models (125M–2.7B parameters) used in the main experiments. While the paper's honesty about this gap is commendable, the gap remains the central evidential weakness—the theoretical acceleration story is plausible but unsubstantiated on the paper's own experiments.

- **Convergence measured in preconditioned norm obscures comparison with DeComFL (Theorem 1):** The convergence bound in Theorem 1 is stated as ‖∇F(x̄)‖²_{H_r^{-1}} rather than the standard ‖∇F(x̄)‖². Converting to the standard norm requires multiplying by β_ℓ^{-1} (via Assumption 4), but the paper does not perform this conversion, discuss its magnitude, or quantify β_ℓ empirically. This means the headline rate improvement over DeComFL (removing L and d dependence) may be partially offset by this factor. Corollary 2 recovers DeComFL's rate as a special case with β_ℓ = β_u = 1, but for HiSo with a non-identity H, the comparison is opaque.

### Minor

- **No main-text experiments for τ > 1 despite Corollary 3 being a headline contribution:** Corollary 3 resolves an open question about convergence with multiple local updates, yet the main-text LLM experiments appear to use τ = 1. The paper mentions appendix results but the lack of main-text empirical support for this theoretical claim weakens its visibility and impact.

- **Learning rate retains d dependence (Theorem 1):** The step size condition η ≤ ... · √(1/(L(d+2))) still requires the learning rate to shrink with dimension. The "dimension-free" rate comes from the bound on ρ̄ via the well-approximated condition, not from removing d from the step size constraint. This subtlety is not discussed and may confuse readers about what "dimension-free" means in this context.

- **Narrow experimental scope:** Only the OPT model family (125M–2.7B) is tested with 6 clients and 2 sampled per round—a minimal FL setup. The absolute accuracy gap between HiSo and first-order methods remains substantial (e.g., HiSo 90.34% vs. FedAdam 92.86% on SST-2, OPT-1.3B in Table 3). The speedup over DeComFL varies from 1.4× to 5.4× across tasks (Table 2) with no discussion of what task/model properties predict larger vs. smaller speedups.

- **Random scalar absorbed into learning rate (Eq. 7):** The term (u^T H^{-1} u)^{-1} varies across iterations depending on the realization of u but is absorbed into a deterministic η. While this scalar concentrates around its expectation as d grows, the paper states only that it is "independent of iterates" (line 118), which is true but sidesteps the randomness concern. This is a minor formal gap.

### Trivial
None

## Nice-to-Haves

- Empirically verify the well-approximated condition on OPT models by computing Tr(H^{-1/2}Σ_{diag}H^{-1/2}) at selected checkpoints using Hutchinson's estimator on a parameter subset—even an approximate measurement would significantly strengthen the theory-experiment connection.
- Provide a corollary restating convergence in the standard gradient norm ‖∇F(x)‖² to make the comparison with DeComFL's rate transparent.
- Add main-text experiments with τ > 1 to empirically support Corollary 3.
- Discuss formally why the Adam-style second-moment estimator serves as a reasonable proxy for the diagonal Hessian in the ZO setting, connecting the update rule to the theoretical assumption.
- Test on architectures beyond OPT (e.g., LLaMA) and with larger client pools to demonstrate generality.
- Analyze which task/model characteristics predict larger speedups to help practitioners assess applicability.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Abstract should foreground the conditionality of claims more clearly":** The abstract already states "under some Hessian approximation assumptions," which adequately signals the conditionality. Removed as a nitpick about framing.
- **"Missing comparison with PEFT methods in main text":** The paper explicitly states (line 347): "comparisons and analyses of memory cost, communication cost, computation time, and other FL+PEFT baselines" are provided in Appendix E. Removed as addressed in appendix (which was stripped by the parser).
- **"H updated only from first local update step (k=0)":** This is a design choice, not a flaw. Using only Δx_{r,0} for the Hessian update is a reasonable simplification that avoids additional complexity. Removed as a design decision rather than a weakness.
- **"Speedup of 1.4–5.4× is only moderate":** Consistent speedup across all tasks with zero additional communication cost is a real practical improvement. Removed as applying an unreasonable standard.

## Novel Insights
The paper's central insight—that the algebraic structure of ZO updates allows curvature information to be piggybacked onto already-communicated scalars at zero additional cost—is genuinely novel and may have implications beyond federated learning for any setting where ZO optimization is used under communication constraints. The generalization of scalar-only FL frameworks beyond ZO-SGD provides a useful abstraction that could enable future methods (e.g., momentum-based or variance-reduced variants). The formal connection between the whitening rank ζ and convergence acceleration offers a new lens for understanding when and why Hessian-informed ZO methods outperform vanilla ZO methods.

## Suggestions
- At selected training checkpoints, compute the diagonal Hessian via Hutchinson's estimator on a parameter subset and measure Tr(H^{-1/2}Σ_{diag}H^{-1/2}) to empirically ground the well-approximated condition on the actual LLM experiments.
- Add a corollary converting Theorem 1's bound to the standard ‖∇F(x)‖² norm, explicitly showing the β_ℓ^{-1} factor and discussing its practical magnitude.
- Include τ > 1 experiments in the main text to validate Corollary 3.
- Provide a formal or semi-formal argument connecting the Adam-style second-moment update to the well-approximated condition, even if only under simplifying assumptions (e.g., stationary iterates or separable loss landscapes).

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to HiSo |
|-------|------|-----------|-------|---------------------|
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Fundamentally flawed; HiSo is far stronger |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Not a research paper by ICLR standards; irrelevant |
| Lifelong Person ReID | 5lUdTogEL3 | 1.00 | R1 | Completely different domain; far weaker |
| All Pairs Minimax | bEgDEyy2Yk | 1.00 | R1 | Code implementation paper; irrelevant |
| Bidirectional FL | Jl0aEFrp11 | 2.75 | R1 | FL optimization paper with multiple weaknesses; HiSo substantially stronger |
| Compressed Decentralized Learning | zqXANcFO9T | 1.67 | R1 | Decentralized learning with major theoretical issues; HiSo much stronger |
| Faster Adaptive Federated CO | Og7ZZd7hDm | 3.25 | R1 | Fed composition optimization; HiSo has a more novel contribution and stronger execution |
| FedADM | IsHWcsk4Fz | 3.00 | R1 | Adaptive FL without novelty; HiSo is clearly stronger |
| Fed ZO Trajectory-Informed (FZooS) | ZAMoxm86KV | 3.67 | R1 | **Fed ZO paper rejected for computation/theory issues; HiSo has a more practical and novel zero-cost curvature approach** |
| FeedSign | DJRd4IQHGQ | 5.25 | R1 | **1-bit FL fine-tuning; rejected for novelty and theoretical concerns; HiSo has a more novel core contribution** |
| Federated Compositional Opt | Ob0UafH2YI | 4.67 | R1 | Rejected FL optimization paper; HiSo stronger overall |
| Efficient Adaptive Fed Opt (FedAda²) | AbJWZp4THG | 5.00 | R1 | Efficient adaptive FL; rejected; HiSo has comparable or stronger contribution |
| **DeComFL** | omrLHFzC37 | **6.25** | R1 | **Direct predecessor; accepted. HiSo extends it meaningfully but introduces new theory-practice gaps. Comparable quality.** |
| ZO Stability Analysis | AfhNyr73Ma | 7.00 | R1 | General ZO theory paper; accepted. More complete theory-experiment alignment; HiSo is slightly weaker due to unverified assumptions. |
| FedSMU | ZU42Wrcqfm | 5.75 | R1 | Rejected comm-efficient FL; HiSo has a more distinctive contribution |
| Error Feedback Sparse Features | B5Tp4WwZl8 | 6.25 | R1 | Theoretical FL paper with novel proof; accepted. Comparable quality to HiSo. |
| Learning to Relax | 5t57omGVMw | 8.00 | R1 | Much stronger theoretical contribution with complete validation; HiSo below this tier |
| Tight Lower Bounds | fMTPkDEhLQ | 8.00 | R1 | Pure theory with tight results; above HiSo's tier |
| SVGD Convergence | sbG8qhMjkZ | 8.00 | R1 | Strong theory paper; above HiSo |
| DRO Bias/Variance Reduction | TTrzgEZt9s | 8.00 | R1 | Complete theory+experiments; above HiSo |

### Scoring Rationale

**Round 1 bracket: 5.5 – 7.0**

HiSo sits in the borderline accept range. Its most direct comparator is DeComFL (6.25, accepted), which it extends with a clever zero-cost curvature integration. However:

- **For a higher score (toward 7.0):** The zero-cost curvature insight is genuinely novel, the framework generalization is useful, the τ > 1 extension resolves an open question, and empirical speedups are consistent across all tasks.
- **Against a higher score:** The three major weaknesses—the gap between the algorithm's second-moment estimator and theory's Hessian assumption, the unverified well-approximated condition on LLM experiments, and the preconditioned norm obscuring comparison—collectively mean the paper's central theoretical claims are plausible but not fully substantiated. The experimental scope is also narrow.

Compared to DeComFL (6.25), HiSo provides meaningful algorithmic and theoretical extensions, but the gap between what the algorithm computes and what the theory assumes is arguably larger than in DeComFL (where the low effective rank is a property of the landscape, not of a learned estimator). The contribution is somewhat incremental relative to the foundational DeComFL framework.

The paper is above the rejected papers in the 3.5–5.5 range (FZooS, FeedSign, FedAda²) by a clear margin, and comparable to accepted papers in the 6.0–6.5 range. The theory-practice gap prevents it from reaching the 7.0+ tier.

**Final score: 6.0**

The paper has a strong and novel core idea with competent execution. The zero-cost curvature integration is the kind of insight that advances the field. However, the central theoretical claims rest on assumptions that are neither proven to hold for the algorithm's actual estimator nor empirically verified on the main experiments. This gap is fixable (as the suggestions above indicate) but currently prevents the contribution from being fully established. At this stage, the paper sits at borderline accept—a worthwhile contribution that would benefit from targeted strengthening of the theory-experiment connection.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>