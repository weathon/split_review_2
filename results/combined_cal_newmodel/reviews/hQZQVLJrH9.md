Here is the final consolidated review.

## Summary

This paper establishes a formal first-order equivalence between activation steering and influence functions — two previously disconnected strands of interpretability research. It introduces the Influence-Aligned Steering (IAS) vector, an alignment diagnostic γ (smallest principal-angle cosine between Jacobian subspaces), and a no-free-lunch bound when alignment is poor. The theoretical framework (primal-dual formulation, steering-influence duality, spectral optimality, generalization bounds) is genuinely novel and clearly presented.

---

## Strengths

- **A genuinely novel theoretical connection between activation steering and influence functions**, formalized through a primal-dual lens (Section 3). The observation that a steering vector can be mapped to a signed data weighting (Theorem 4.2) and vice versa is clean, nontrivial, and worth stating in print.

- **The γ diagnostic (Theorem 5.1) and the no-free-lunch bound (Theorem 6.2) provide a crisp, interpretable answer** to a practical question: when can steering, in principle, replicate a given weight-space effect at a given layer? The bound sharpens the alignment intuition into a definitive limitation rather than a heuristic. This is the kind of tool practitioners could in principle adopt.

---

## Weaknesses

### Fatal
None.

### Major

- **The central validation experiment (Figure 1, Section 7.2) shows a slope of 1.50 — meaning the actual steering effect is 50% larger than the first-order prediction — yet the paper describes this as "consistent with the expected linear regime" without acknowledging or explaining the systematic magnitude error.** The cosine of 0.978 confirms directional alignment, but the 50% magnitude error means the quantitative first-order equivalence claim is not validated as stated. For a paper whose core deliverable is a claimed equivalence, this unexplained discrepancy undermines confidence in the quantitative claims. The paper must either explain the source of this error (calibration of the IAS vector norm? second-order effects?) or acknowledge it as a limitation.

- **The data-provenance workflow — mapping steering vectors back to causal training examples — is presented as a primary contribution (Abstract: "constructive algorithm for mapping undesired behaviors back to causal training examples"; Section 4.1: "points straight to the most causal training documents") but receives zero experimental validation.** No examples are shown, no comparison to existing influence-based attribution methods (TracIn, RelatIF, etc.) is provided, and no precision/recall is measured. The reverse direction (steering → data) is arguably the more novel and impactful of the two, yet it is left entirely at the mathematical level.

- **The detoxification experiment (Table 1) shows the principled IAS method is outperformed by the heuristic CAA baseline on both toxicity (0.0164 vs 0.0150) and perplexity (13701 vs 13291).** This is presented without any discussion or analysis. If the "principled" method derived from the theory is worse on both metrics on the paper's own chosen task, the paper must address whether (a) the theory is missing something relevant, (b) the setup is unfavorable to IAS, or (c) the practical value of the equivalence is limited.

- **The spectral optimality experiment (Figure 3, Section 7.4) does not actually steer: it only computes a p-value against random directions (p=0.00498, z=3.55).** It does not apply the spectral direction to measure logit change, compare against any baseline steering vector (CAA-style difference-in-means, PCA, or random), or measure side effects on non-target classes. The comparison against random directions is the weakest possible baseline.

### Minor

- **Only one model (GPT-2 Medium, ~355M parameters) is used for the LM experiments**, despite the Introduction claiming the tools "scale to billion-parameter models." Only one task (detoxification) is evaluated; no fact-editing, sentiment control, or reasoning experiments are included.

- **The γ vs. layer depth experiment (Figure 2) is purely descriptive**: it shows γ increases with depth but does not test whether the γ diagnostic actually predicts steering success on any downstream task.

- **No confidence intervals, standard deviations, or significance tests are reported** for any experimental results (Table 1 reports only means). The one exception is the permutation test in Figure 3.

- **The Rademacher generalization bound (Theorem 6.1) adds a term αL√(2k/(dn)) that is very small** (≈0.04αL for the experimental setting) and is not tested empirically. The bound essentially restates known results from the LoRA literature and does not yield actionable predictions.

- **The "two backward passes per input" cost model (Introduction, Section 2) is accurate for the basic IAS construction but misleading for the spectral direction (Theorem 5.3)**, which requires a power iteration over a matrix Σ involving H⁻¹ — the main computational bottleneck of influence functions. The gap between the stated cost model and the actual cost of the spectral construction is not bridged.

- **Corollary 1's ℓ₁-minimality proof sketch is non-rigorous**: it does not properly handle the possibility that alternative measures might induce different effective steering magnitudes, and the argument from contradiction is incomplete.

- **Corollary 2 assumes κ-Lipschitz Jacobians but no estimate of κ is provided** for any model studied, so the second-order radius bound is not actionable.

### Trivial
None.

---

## Nice-to-Haves

- Investigate and explain the slope discrepancy in Figure 1 — this single fix would most improve the paper's credibility.
- Run the data-provenance experiment (show top-weighted training examples for a detoxification steering vector) or temper the claims accordingly.
- Add more models (e.g., Llama-7B) and tasks to strengthen empirical breadth.
- Report confidence intervals for all experimental results.
- For the spectral direction, compare actual steering performance against baselines rather than only a permutation test against random directions.

---

## Removed Points

These points were identified in the input review but removed per filtering rules:

1. "Theorem 4.2 proof is deferred to the appendix (which we cannot verify)" — removed per hard rule: the appendix is stripped by the PDF parser; it exists in the original submission.
2. "Lemma 4.1 is a standard application of the chain rule and does not warrant being stated as a lemma" — removed as a stylistic preference, not a substantive weakness.
3. "Strengths: Computationally honest framing" — removed because the cost model claim is incomplete for the spectral direction (verified weakness conflicts with this claimed strength).
4. "Claim about scaling to billion-parameter models vs. outdated models" — the billion-parameter claim is retained as a minor weakness; the "outdated models" phrasing was removed per the rules on model availability.
5. Various speculative framing (e.g., "could the metric be measuring a proxy?", area-of-concern sweep items without specific paper anchors) — removed as unfounded speculation.

---

## Novel Insights

The input review surfaces a pattern: the paper's theoretical contribution is genuinely strong, but there is a systematic gap between what the theory promises and what the experiments deliver. The three major empirical weaknesses (unexplained 50% slope error, zero validation of the data-provenance direction, and the principled method losing to the heuristic) form a consistent pattern of overclaim relative to evidence. This is not a case of a fundamentally flawed theory — the theory is sound — but of a paper that commits the error of presenting an otherwise solid theoretical contribution with empirical support that is too weak to carry the weight placed on it. An interesting meta-point is that the slope of 1.50 in Figure 1, if taken at face value, might actually be fixable (e.g., by re-calibrating the norm of the IAS vector), which would salvage the quantitative claim.

---

## Suggestions

1. **Most critical:** Investigate why the slope in Figure 1 is 1.50 rather than 1.0. If this is a calibration issue with the IAS vector norm or a known second-order correction, provide the explanation. If it cannot be explained, the quantitative equivalence claim should be downgraded to a directional equivalence.
2. Either run the data-provenance experiment or clearly scope the paper as a theory paper with illustrative experiments, removing the unsubstantiated data-provenance claims from the abstract and introduction.
3. Add a candid discussion of why IAS underperforms CAA on detoxification and what this implies for the practical value of the framework.
4. Add confidence intervals to all experimental results and test at least one additional model scale.

---

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| 2XBPdPIcFK.md (CAA/ActAdd) | 5.00 | R1 | Yes | Stronger experiments, comparable theory depth; the current paper's theory is more novel but empirical support is weaker |
| 9wjGUN65tY.md (Conceptors) | 5.00 | R1 | Yes | Similar theoretical ambition, better experiments but less clean theory; comparable overall quality |
| WT2bL7sCM1.md (Hessian-free IF) | 3.00 | R1 | Yes | Much weaker contribution; mostly incremental changes to existing methods |
| qJkCEcd50n.md (Influence manipulation) | 3.00 | R1 | Yes | Interesting question but unrealistic threat model; less novel theory |
| uHLgDEgiS5.md (Temporal influence) | 8.00 | R1 | Yes | Strong theory + thorough experiments; gold standard for influence papers |
| I4e82CIDxv.md (Sparse Feature Circuits) | 8.00 | R1 | Yes | Exceptional empirical validation; very different paper type |
| EwAGztBkJ6.md (Gradient generalization) | 4.00 | R2 | Yes | Theory-heavy with limited experiments; comparable structure but less novel theory |
| 89nUKXMt8E.md (World model definition) | 4.75 | R2 | Yes | Pure theory with no experiments; wider reviewer disagreement |

**Bracket reasoning:** Round 1 bracketing placed the paper between 4.0 and 6.0 — above pure-incremental influence function papers (3.00) but below fully-validated interpretability papers (8.00). Round 2 narrowed to 4.0–5.0 by comparing against the theory-heavy gradient generalization paper (4.00) and conceptors paper (5.00). The paper's strengths (favorability 12.44–12.54) are competitive with 5.00+ anchors, but its three most damaging weaknesses (−3.08, −2.35, −2.03) are more negative than any weakness in the 5.00 anchors, placing it below them. The final score of 5.0 reflects a genuinely novel theoretical contribution that is undercut by empirical validation too weak to support the paper's central claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>