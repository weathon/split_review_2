Now I have all the information I need. Let me write the final consolidated review.

**Round 1 bracket**: The paper's weighted items show strong theoretical contributions (weights 8.58–9.30) but two significantly negative weaknesses: missing baselines (−3.65) and theory-experiment mismatch (−1.80). The most relevant anchors in the 4–6 range include CGfWyU28Pd (4.50, theory-practice gap), dYTjB86pcT (5.50, theoretical unlearning paper with evaluation gaps), and C3TrHWanh5 (6.00, strong theory+experiments). After comparison, the paper falls between CGfWyU28Pd (4.50) and dYTjB86pcT (5.50), closer to the latter given the stronger theoretical novelty. **Round 1 bracket: 4.0–6.0.**

**Round 2 narrowing**: Compared to CGfWyU28Pd (4.50, -2.48 missing baselines, -0.63 theory mismatch) and dYTjB86pcT (5.50, -0.86 missing comparisons, -0.62 lack of evaluation), this paper has stronger theory weights (8.58–9.30 vs ~7–10 in those anchors) but also more negative weights on missing baselines (−3.65 vs −2.48 and −0.86). The Hessian-based certified unlearning anchor C3TrHWanh5 (6.00, Accept) had milder weaknesses (−2.19 convexity assumptions) with comparable strength weights, confirming that this paper's evaluation gaps are more severe than a 6-level paper would exhibit.

**Final placement**: 5.0 — the theoretical contributions are genuinely novel and represent a non-trivial advance, but the evaluation issues (missing baselines, theory-experiment mismatch) are substantial enough to prevent acceptance at the borderline-accept threshold.

---

## Summary

This paper establishes a theoretical framework that connects ℓ₂-regularized continual learning with certified machine unlearning. It decomposes post-unlearning excess risk into continual-learning excess risk and unlearning loss (Section 2.3), extends excess-risk bounds from linear to μ-strongly convex nonlinear models (Theorem 3.1), and adapts gradient-based and Hessian-based certified unlearning algorithms to the continual learning setting, including handling arbitrary unlearning sequences (Algorithms 1–2).

## Strengths

- **Clean decomposition of the post-unlearning excess risk (Section 2.3, eqs 5–7).** Separating the objective into interpretable components — continual-learning excess risk and unlearning loss — and identifying their inherent tradeoff is a genuinely novel conceptual contribution relative to prior certified unlearning work. [weight: 8.76]

- **Extension of excess-risk bounds from linear to μ-strongly convex nonlinear models (Theorem 3.1).** This is a non-trivial generalization of prior work (Lin et al. 2023) that could be useful for future theoretical analyses. The observation that the bound does not vanish even with large sample sizes (line 125) is a meaningful point about the irreducible cost of task heterogeneity. [weight: 9.27]

- **Hessian-based algorithm design for arbitrary unlearning sequences (Section 5.1, Algorithm 2).** The derivation of the correction term (13) that handles interference between unlearning requests arriving in arbitrary order is the most technically substantive part of the paper. The analysis of how unlearning sequence order affects approximation error (Proposition 5.1) goes beyond what prior work has considered. [weight: 9.30]

- **Clear characterization of the storage-accuracy tradeoff** across the two algorithms (Alg. 1 requires zero storage but has looser bounds; Alg. 2 has tighter bounds but O(td²+2td) storage), with a principled forgetting-enhanced variant (Section 5.3) to interpolate between extremes. [weight: 8.58]

## Weaknesses

### Major

- **Theory-experiment mismatch.** The entire theoretical framework rests on Assumption 2.1: the loss must be L-Lipschitz, μ-strongly convex, and M-smooth. The parameter ρ = λ/(μ+λ) appears in every bound, and the decay of the forgetting effect depends critically on μ > 0. The experiments (Section 6) use cross-entropy loss with softmax, which is not strongly convex. The paper acknowledges this at line 288 ("we relax its assumption of μ-strong convexity here") but provides no theoretical justification for why the bounds would still hold in a non-strongly convex setting. The claim that experiments "validate these theoretical findings" (Abstract, line 9) is therefore unsupported by the evidence provided. [weight: −1.80]

- **Missing baselines.** The experiments compare only the paper's two algorithms (Alg. 1 and Alg. 2) against each other and against perfect retraining. No comparisons are made against existing certified unlearning methods (even applied naively), simple baselines (e.g., using the most recent model without unlearning, fine-tuning on recent tasks only), or heuristic unlearning methods from the cited continual learning-unlearning systems papers (Liu et al. 2022; Chatterjee et al. 2024; Cha et al. 2024; Huang et al. 2025). Without baselines, it is difficult to assess whether the proposed methods offer practical advantages. [weight: −3.65]

### Minor

- **Limited experimental scope.** Only one dataset (MNIST) is used. No error bars, standard deviations, or confidence intervals are reported for any experimental result, making it impossible to assess the reliability of the observed trends. [weight: −0.01]

- **Anomalous result in Table 1.** At λ=30, the Hessian-based unlearning model achieves 71.59% test accuracy while "perfect retraining" achieves only 71.05%. Since retraining is the gold standard that unlearning should approximate, this result is unexpected. The paper does not comment on it; it may be within noise (no error bars are reported), but the discrepancy should be acknowledged and explained. [weight: +2.25]

- **Coarse λ grid for post-unlearning excess risk.** Table 1 reports only three λ values (10, 20, 30), making it difficult to assess trends comprehensively. [weight: +4.01]

### Trivial

None.

## Nice-to-Haves

- Design experiments that satisfy the theory's assumptions (e.g., ℓ₂-regularized logistic regression, which is μ-strongly convex) to directly test whether the theoretical bounds hold, or provide new theory covering the non-strongly convex setting.
- Include at least 1–2 simple baselines (e.g., training on the most recent task only, or a naive application of an existing certified unlearning method) to contextualize the empirical results.
- Report error bars over multiple random seeds or task orderings.
- Investigate and explain the anomalous λ=30 result in Table 1.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Theorem 3.1 indexing errors.** The harsh critic identified apparent typos in equation (8) where terms contain τⱼ−τⱼ and ‖w*_{τⱼ}−w*_{τⱼ}‖, producing zero terms. Per the hard rule, all criticism about typos is treated as parser errors, not author errors. The original submission does not have these issues.
- **Missing Table 2 in appendix.** The critic noted that Table 2 is referenced but was in the (missing) appendix. Per the hard rule, appendix sections and tables are stripped by the parser but exist in the original submission.
- **Computational cost concerns about Hessian storage.** The critic noted that Hessian storage is prohibitive for large models — this is an acknowledged limitation that the paper explicitly discusses (storage-accuracy tradeoff, Section 5).
- **Combative general strengths/weaknesses.** Strength 2 about Theorem 3.1 was hedged with "If the proof is correct" — this is reasonable commentary given the appendix is stripped, not a weakness.
- **Section-by-section notes** that are general commentary without specific, falsifiable claims.

## Novel Insights

The reviews surface a genuine tension that the paper does not adequately resolve: the theoretical framework (strongly convex losses) operates in a different regime from the experiments (non-strongly convex softmax/cross-entropy), and the paper's claim of experimental validation is undermined by this disconnect. The missing-baselines concern is particularly significant because the paper frames its contribution as adapting existing certified unlearning methods to the continual setting, yet never benchmarks those very methods (or simple alternatives) to demonstrate whether the adaptations are necessary or effective. These are addressable issues in a revision.

## Suggestions

1. **Address the theory-experiment gap** by either (a) redesigning experiments to use a μ-strongly convex loss (e.g., ℓ₂-regularized logistic regression) so the theoretical bounds directly apply, or (b) providing new theoretical results that cover the non-strongly convex setting used in experiments. Qualify any claims of "validation" accordingly.
2. **Add baselines** — at minimum compare against a naive application of an existing certified unlearning method (even if it fails) and a simple fine-tuning-only baseline — to position the empirical contribution.
3. **Add error bars** to all experimental results.
4. **Comment on the anomalous λ=30 result** in Table 1 where Hessian unlearning exceeds perfect retraining.

## Score and Decision

The paper's theoretical contributions — the risk decomposition, extension to nonlinear models, and Hessian-based unlearning sequence analysis — are genuinely novel and technically substantive. However, the experimental evaluation has two significant gaps: (a) it operates outside the theory's core assumption (μ-strong convexity) without justification, so it cannot be said to validate the theory, and (b) it lacks baselines against any existing method, making it impossible to assess the practical value of the proposed algorithms. These issues are fixable but limit the paper's current impact.

**Calibration anchors used:**
| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| C3TrHWanh5 (Hessian-free certified unlearning) | 6.00 | R1 | Yes | Stronger experiments, milder weaknesses |
| CGfWyU28Pd (FT unlearning theory) | 4.50 | R1 | Yes | Similar theory-practice gap, weaker theory |
| HVFMooKrHX (In/OOD unlearning) | 6.60 | R1 | Yes | Stronger theoretical rigor, better evaluation |
| dYTjB86pcT (System aware unlearning) | 5.50 | R2 | Yes | Comparable theory weight, similar evaluation gaps |
| pFjzF7dIgg (UnCLe: CL+unlearning) | 5.75 | R2 | Yes | Similar topic, mixed reviews |
| Pin2kdWloe (Multitask in CL) | 5.75 | R2 | No | General CL theory, less relevant topic |
| BE5aK0ETbp (Unified CL framework) | 5.25 | R2 | No | Unrelated contribution type |
| ffuHn3Q6Hc (Plasticity in CL) | 5.33 | R2 | No | Unrelated topic |
| IhOeYKqnfp (Continual Memory) | 4.25 | R2 | No | Unrelated topic |

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>