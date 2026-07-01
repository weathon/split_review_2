Now let me write the final consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses

### Fatal
None

### Major
- weakness 1
- weakness 2

### Minor
- weakness 1

### Trivial
- weakness 1

## Nice-to-Haves
- suggestion

## Removed Points
...

## Novel Insights
...

## Suggestions
...

## Score and Decision

Let me produce the final output.

# Final Review

## Summary

This paper proposes HiSo, a federated zeroth-order optimization algorithm that combines a generalized scalar-only communication framework with Hessian-informed preconditioning. The key idea is maintaining dimension-free communication (scalar-only) while using a learned diagonal matrix H to precondition ZO gradient estimates, achieving 1.4–5.4× speedup over the state-of-the-art ZO-FL baseline DeComFL across OPT models (125M–2.7B) on SST-2, QQP, and SQuAD. Theoretical analysis provides convergence bounds conditional on a Hessian approximation assumption.

## Strengths

1. **Generalized scalar-only communication framework (Section 3.3, Algorithm 1).** The insight that scalar-only communication can be decoupled from ZO-SGD into a general framework is a genuine architectural contribution. It cleanly separates the communication protocol from the optimization algorithm, opening the door to integrating techniques beyond vanilla ZO-SGD.

2. **Consistent and well-structured empirical gains.** HiSo consistently outperforms DeComFL (the only scalar-only ZO-FL baseline) across three model scales (OPT-125M/350M/1.3B/2.7B) and three NLP tasks, with 1.4–5.4× speedup in communication rounds (Table 2) and higher test accuracy (Table 3). Standard deviations are reported and HiSo's accuracy advantage over DeComFL is clear in nearly every setting.

3. **Theoretical analysis covering multiple local updates (τ > 1).** The convergence analysis extends to τ > 1 local updates per round, which DeComFL's theory did not support. Corollary 3 provides the first dimension-free convergence rate for ZO-FL with multiple local updates under the low-effective rank assumption.

## Weaknesses

### Fatal
None.

### Major

1. **The "Hessian-informed" claim is not supported by the algorithm.** The paper frames HiSo as capturing "curvature information through diagonal Hessian approximation" (abstract, line 23, Section 4.2). However, the H matrix is updated via H_{r+1} = (1−ν)H_r + ν·Diag(|Δx|² + εI) (Eq. 12), where Δx is the ZO gradient estimate. Squaring the gradient estimate yields **gradient second-moment information**, not Hessian or curvature information — this is RMSProp-style gradient-magnitude preconditioning. The paper tacitly acknowledges this in footnote 2 ("our method resembles RMSProp") but the main text, title, abstract, and theoretical analysis (Definition 17, Corollaries 1–3) all rely on the assumption that H approximates the Hessian Σ in a specific spectral sense. The paper's own remarks concede "it is hard to determine if this approximation holds" (line 285). This creates a gap between what the algorithm computes and what the theory assumes: the convergence rates in Corollaries 1–3 are conditional on an unverified (and likely unverified) condition. The empirical evidence (Fig. 5) shows a long-tail distribution of H entries, which is a property of gradient statistics, not evidence of Hessian approximation.

2. **Limited ZO-FL baseline comparisons.** The only scalar-only ZO-FL baseline is DeComFL. The paper does not compare against (a) ZO methods with momentum applied within the scalar-only framework (which the paper notes would be straightforward), or (b) simple adaptive ZO methods with per-coordinate scaling via accumulated gradient magnitudes. Without these ablations, it is unclear whether HiSo's gains come from the specific Hessian-informed mechanism or simply from any form of adaptive scaling.

### Minor

1. **Derivation gap in Section 4.1.** The paper absorbs the scalar (u^T H^{-1} u)^{-1} into the learning rate, stating it is "independent of iterates." While independent of x, it depends on the random direction u and the current H matrix, both of which vary per iteration. Absorbing a per-sample random scalar into a fixed global learning rate is not a standard operation without further justification.

2. **Table 1's numerical entries lack rigor.** Under L-smoothness, with H=I and Σ=LI, E‖z‖_Σ² = Tr(H^{-1/2}ΣH^{-1/2}) = L·Tr(I) = Ld, not 2d. The factor 2 is attributed to a "safety factor," which is non-standard and makes the table misleading without a more prominent caveat.

3. **Several experimental details are missing.** (a) The hyperparameter P (line 301, "We set P = 5 for all ZO methods") is never defined. (b) The initialization of H₀ is not specified. (c) Learning rates and tuning procedures are not reported — only that both methods "were tuned using their optimal learning rates." (d) No statistical significance tests are provided for the accuracy comparisons.

4. **Speedup metric is non-standard.** Table 2 reports rounds for HiSo to match DeComFL's best accuracy, which conflates convergence speed with a variable accuracy threshold. While Table 3 partially addresses this with final accuracy comparisons, the primary speedup claim would be stronger with a standard metric like rounds to reach a fixed target accuracy jointly specified for both methods.

### Trivial

- The convergence bound in Theorem 1 uses the H^{-1}-weighted gradient norm rather than the standard unweighted norm. This is common in adaptive methods but makes the "dimension-free" claim less directly comparable to standard ZO convergence results.

## Nice-to-Haves

- Experiments on additional model families beyond OPT (e.g., LLaMA) would strengthen generality.
- An ablation comparing HiSo against a version with H frozen to a fixed diagonal matrix would isolate the benefit of online H learning from the choice of preconditioner.
- A comparison with ZO-SGD + explicit RMSProp-style gradient second-moment accumulation would test whether the Hessian framing adds anything over simpler adaptive methods.

## Removed Points

These points from the harsh critic were filtered out with brief justification:

1. **"Up to 90 million times communication savings" comparison against first-order methods** — This is a comparison against FedAvg/FedAdam and primarily reflects the ZO scalar-only framework inherited from DeComFL, not HiSo-specific. The paper frames this transparently ("compared to first-order baselines"), so it is not a weakness of HiSo per se.
2. **Criticism that the learning rate condition depends on d** — The reviewer correctly notes Theorem 1 requires η ≤ √(1/(L(d+2))), but then acknowledges "this is fine technically." This is standard practice and does not undermine the contribution.
3. **Request for more model families (LLaMA)** — Moved to Nice-to-Haves as a scope-extending suggestion rather than a weakness.
4. **"The convergence measure is non-standard"** — Partially retained under Trivial. The weighted norm is standard in adaptive optimization theory.
5. **Statistical significance tests** — Retained in Minor (item 3d above) as a genuine concern.

## Novel Insights

None beyond the paper's own contributions. The core tension identified — that a method claiming to be "Hessian-informed" actually computes gradient second moments — is a significant framing issue but is visible from reading the paper, not a novel discovery from the reviewer discussion.

## Suggestions

1. **Reframe the method honestly.** Drop the "Hessian-informed" terminology in favor of "adaptive gradient-magnitude preconditioning" or similar. The practical contribution — a ZO adaptive optimization method with scalar-only communication — is interesting without needing to claim Hessian estimation. The paper already has a footnote comparing to RMSProp; this should be elevated to the main framing.

2. **Connect theory to algorithm.** Either (a) prove (even under idealized conditions) that the H update in Eq. (12) can satisfy the well-approximated condition, or (b) present the convergence results as bounds conditional on the quality of H_r without claiming dimension-free rates as a *proven* property of HiSo specifically. The current framing implies more than is supported.

3. **Add meaningful ablations.** The most informative experiments would be: (a) HiSo vs. HiSo with H frozen to a fixed diagonal matrix (precomputed from gradient statistics), to isolate the benefit of online H learning; (b) HiSo vs. ZO-SGD with an explicit RMSProp-style gradient second-moment accumulator, to test whether the Hessian framing adds anything over simpler adaptive methods.

4. **Specify P, H₀ initialization, and learning rate schedules** in the main paper, and consider adding statistical significance tests to strengthen the empirical claims.

## Score and Decision

**Calibration procedure.** I searched the 13k human-review corpus for topically similar papers. The closest anchors are:

| Paper | Avg Score | Decision | Comparison to HiSo |
|-------|-----------|----------|-------------------|
| DeComFL (Li et al., 2025b) | 6.25 | Accept | Direct predecessor. HiSo adds generalized framework + Hessian-informed component, but DeComFL had cleaner theory (H=I, no Hessian assumption needed). |
| HiZOO (Zhao et al., 2025) | 5.67 | Accept | Single-node Hessian-informed ZO. Had similar concern about Hessian estimator not being true Hessian (Reviewer 2), yet was accepted — but is single-node, not FL. |
| FeedSign | 5.25 | Reject | ZO-based communication-efficient FL. Rejected due to novelty concerns and flawed convergence proof. |
| ZOO Trajectory-Informed (FZooS) | 3.67 | Reject | Another ZO FL method. Had more severe issues with computation cost and assumptions. |

**Round 1 bracket:** I placed this paper in the 4.0–6.0 range. Below DeComFL (6.25, accepted) because the Hessian framing issue creates a theory-practice gap that DeComFL did not have. Above FZooS (3.67, rejected) because the empirical results are stronger and the core contribution is cleaner.

**Round 2 narrowing:** Compared to HiZOO (5.67, accepted), which had similar Hessian concerns but a clearer link between theory (actual second-order difference estimator) and algorithm. HiSo's H update is even further from actual Hessian estimation, making the gap larger. Compared to FeedSign (5.25, rejected), HiSo has stronger empirical results and novelty but similar concerns about the gap between theory and algorithm.

**Final score: 5.0.** The paper has real contributions — the generalized scalar-only framework is clean, the empirical results consistently improve over DeComFL, and the τ > 1 theory fills a gap. However, the central framing issue (calling gradient second-moment accumulation "Hessian-informed") creates a mismatch between what the paper promises and what it delivers. The theoretical claims of dimension-free convergence depend on an unverified condition with no evidence connecting the actual algorithm to that condition. The paper needs major revisions in framing and a clearer articulation of what is proven vs. assumed before it meets the bar for acceptance. 

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>