## Summary

This paper establishes the first theoretical framework for certified unlearning in a continual learning setting. It adapts two existing certified unlearning approaches (gradient-based "natural forgetting" and Hessian-based) to work under sequential task arrival with deletion requests, providing theoretical guarantees on both excess risk and unlearning loss. The key formal contribution is the decomposition of post-unlearning excess risk into continual-learning excess risk plus unlearning loss, and the characterization of how the forgetting rate ρ controls unlearning error.

## Strengths

1. **Novel problem formulation (Section 2).** The decomposition of post-unlearning excess risk into continual-learning excess risk (Eq. 7) plus unlearning loss (Eq. 6) is clean and enables structured analysis. The two-stage diagram (Figure 1) clarifies the temporal flow. This is genuinely the first formal treatment of certified unlearning inside a continual learning process with this decomposition.

2. **Explicit connection between forgetting rate ρ and unlearning error (Theorem 4.1, Eq. 9).** The bound γ_t(S_{1:t}) = (L/λ) ∑_i ∑_s ρ^{t−s−n_{t_i,s+1}^i} makes a concrete, testable prediction: earlier tasks (larger t−s) contribute less to unlearning loss because ρ<1. This is a structurally meaningful theoretical result.

## Weaknesses

### Major

1. **Central comparative claim contradicted by the paper's own data.** The paper repeatedly claims that the Hessian-based algorithm achieves "lower unlearning loss" than the gradient-based (natural forgetting) algorithm (lines 37, 318: "the Hessian-based method achieves lower unlearning loss"). However, Figure 2(b) shows the exact opposite: the natural forgetting algorithm has unlearning loss ≈0.08–0.10 across all λ, while the Hessian-based algorithm has ≈0.20–0.24 — a 2–3× difference in the wrong direction. The claim about lower "post-unlearning excess risk" (line 264) is also untested: Table 1 reports only Hessian-based vs. retraining, with no comparison column for the gradient-based algorithm on the same combined metric. Thus the paper's headline comparative claim is either contradicted by or unsupported by its own experimental evidence.

2. **Theorem 3.1 (Eq. 8) contains degenerate terms as printed.** The foundation theorem for all subsequent excess risk guarantees contains two terms that vanish identically: (i) $\rho^{\tau_j - \tau_j} \|w_{\tau_j}^* - w_{\tau_j}^*\| = \rho^0 \cdot 0 = 0$ in the double-sum, and (ii) $L \rho^{\tau_k} \sum_{i=2}^k \|w_{\tau_i}^* - w_{\tau_i}^*\| = 0$ in the third line. These appear to be LaTeX typos where the authors intended distinct indices (e.g., $\|w_{\tau_i}^* - w_{\tau_{i-1}}^*\|$). Since Theorem 3.1 is used by Theorem 4.1, Corollary 5.3, and the entire post-unlearning excess risk analysis, the correctness of the theoretical chain cannot be verified from the main paper as currently typeset.

3. **Assumption 2.1 (μ-strong convexity) is violated in the experiments** (line 288: "we relax its assumption of μ-strong convexity here"). The experiments use cross-entropy loss with a softmax output, which is not strongly convex. The paper claims this shows "more general results under a non-strongly convex setting" but provides no theoretical bridge. With μ = 0, ρ = λ/(μ+λ) → 1, and the bounds in Theorem 4.1 and Corollary 5.3 degenerate. The experiments therefore do not test the theory in the regime where the guarantees apply.

### Minor

4. **Limited experimental scope.** The empirical validation uses a single dataset (MNIST) with a linear model, while the paper motivates its work with large-scale systems like "ChatGPT" and "large language models" (line 17). This does not invalidate the theoretical contribution, but the empirical validation is far narrower than the motivation suggests.

5. **No confidence intervals or variance reporting.** With T = 30 tasks and small per-task datasets (each with "at most three labels"), variance could be substantial. The reported two-decimal-place accuracy numbers (Table 1) cannot be assessed for statistical significance.

### Trivial

None.

## Nice-to-Haves

- A dedicated experiment varying task "staleness" (how many tasks intervene between training and a deletion request) would directly test the ρ^{t−s} decay predicted by Eq. 9 and could more cleanly validate the theory than the current λ-sweep.
- A discussion of how the per-time-step (ε,δ) guarantees compose over multiple deletion requests across the full timeline would strengthen the privacy analysis.

## Removed Points

- **Retrained model outperformed (Table 1 at λ=30):** Removed. The paper describes the retraining accuracy as a "loose accuracy upper bound." The ℓ2-CL retraining model is itself an approximate solver and can plausibly be surpassed.
- **Internal state problem (line 170):** Removed. The paper acknowledges the concern and directs readers to Appendix C.2. Standard practice for space constraints.
- **No composition over time discussion:** Removed. Per-time-step guarantee is standard for a first theoretical treatment.
- **No baseline methods (Neel et al./Sekhari et al. directly):** Removed. The paper's premise is that existing certified unlearning methods do not work in continual learning without modification.
- **Hessian storage cost critique:** Removed. The paper explicitly acknowledges the O(td² + 2td) storage trade-off and proposes a forgetting-enhanced variant to address it.
- **No systematic λ-selection method:** Removed. Exploring the trade-off experimentally is appropriate for a first theoretical paper.
- **Various formatting/style nitpicks and appendix speculation:** Removed per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the degenerate indices in Theorem 3.1 (Eq. 8) so the bound is interpretable from the main text.
2. Either revise the claims about Hessian-based unlearning loss to match Figure 2(b), or explicitly explain why the theoretical predictions differ from the empirical results.
3. Add a direct experimental comparison of both algorithms on post-unlearning test accuracy (the full combined metric, not just unlearning loss).
4. Add confidence intervals and consider at least one additional dataset or a simple nonlinear model to strengthen the empirical validation.
5. Clarify whether the claim "Hessian-based achieves lower unlearning loss" refers to theoretical upper bounds or empirical measurements — if the former, qualify it as such throughout the paper.

---

**Calibration Anchors Consulted:**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| UnCLe (continual learning + unlearning) | 5.75 | 1 | Yes | Similar topic, stronger experiments, no contradictory evidence |
| Privacy-Aware Lifelong Learning | 6.25 | 1 | Yes | Stronger empirical validation, clearer contributions |
| Why Fine-Tuning Struggles (unlearning theory) | 4.50 | 1,2 | Yes | Similar theory-heavy profile, comparable weakness severity |
| Efficient Second-Order Certified Unlearning | 6.00 | 1 | Yes | Cleaner theoretical presentation, better experiments |
| Deep Unlearning | 5.25 | 1,2 | No | More empirical contributions, less theory |
| Blind Unlearning | 3.60 | 1,2 | No | Weaker theory and limited evaluation |
| Replay can provably increase forgetting | 3.00 | 1 | No | Continual learning theory, well-executed but narrow |
| Unified Framework for CL | 5.25 | 1,2 | No | Framework paper, different contribution type |
| (11 others below 3.5 or tangentially related) | 1.0–3.25 | 1 | No | Lower quality or different focus |

**Bracketing:** Round 1 placed this paper in the 3.5–5.5 range based on comparison to certified unlearning and continual learning theory anchors. Round 2 narrowed it: the paper has stronger theoretical novelty than "Fine-Tuning Struggles" (4.50) but more severe empirical contradictions; it has weaker experimental rigor than "UnCLe" (5.75). The impact-score comparison confirms that this paper's decisive weaknesses (-10.00 on contradictory evidence, -10.00 on theorem typos, -10.00 on assumption violation) pull it substantially below the 5.75–6.00 anchors despite its strong theoretical novelty (+10.00 on both the formulation and the ρ-unlearning connection).

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>