## Summary

This paper proposes Aligned Scoring Rules (ASR), a method that optimizes proper scoring rules — via MSE minimization — to align with human preference scores (e.g., instructor ratings) while maintaining the provable truthfulness (properness) guarantees of the Elicitation^GPT framework (Wu & Hartline, 2024). The optimization is a clean convex quadratic program over separate scoring rules, and experiments on a peer-grading dataset show substantial improvement in MSE and correlation over non-aligned baselines.

## Strengths

- **Well-motivated problem.** The paper correctly identifies the tension between properness (truthfulness) and human-preference alignment in textual scoring. LLM-as-Judge scores are not proper and hence vulnerable to strategic manipulation; naively applying non-proper scores as incentives lacks guarantees. Optimizing within the proper scoring rule space for alignment is a natural and worthwhile direction. (Section 1, lines 23–29)

- **Clean convex formulation.** The optimization in Program 2 is a quadratic program with linear constraints over only 6 variables per summary dimension, making it provably convex, tractable, and interpretable. The separate scoring rule structure also allows identifying the importance of individual rubric dimensions. (Section 3.2, Corollary 3.4, lines 252–256)

- **Significant empirical improvement over non-aligned baselines.** ASR achieves MSE 1.730 vs 9.541 (AV) and 18.360 (MV), and Pearson correlation 0.717 vs 0.294 and 0.213 when aligned to Instructor Scores. The improvement is substantial and consistent across both reference scores. (Table 1)

## Weaknesses

### Fatal
None.

### Major

- **No statistical reliability information.** The paper reports only point estimates for MSE and correlation (Table 1) without any confidence intervals, standard deviations, or per-assignment breakdown. With only 22 assignments (the natural independent units), these estimates could be noisy. More critically, the paper never specifies whether Table 1 reports training fit or held-out evaluation — the constant baseline mentions "training data D" (line 358) but no train/test split protocol or evaluation procedure is described anywhere. Without this information, the reader cannot assess whether the reported numbers reflect genuine predictive performance or in-sample overfitting. (Table 1, lines 304–305, 342–365)

- **MSE scale ambiguity.** Program 1 states "s normalized to [0,1]" and S(·,·) ∈ [0,1], but Table 1 reports SquaredLoss values > 1 (e.g., 1.730 for ASR, 3.741 for Constant baseline). Since the theoretical maximum MSE on [0,1] is 1, these values must be on the original [0,10] instructor score scale — but the paper never clarifies this transition. The headline numbers are difficult to interpret without knowing the scale on which they are reported. (Program 1 at lines 227–229, Table 1, line 304)

### Minor

- **Optimization per-assignment vs pooled is not clarified.** The paper states "the dataset is partitioned in advance into clusters" (line 194), each corresponding to one assignment with its own summary points and prior distribution, but never specifies whether Program 2 is solved independently per assignment or pooled across all assignments. This matters for understanding the experimental setup and for reproducibility. (lines 194, 227–256)

- **No human inter-rater reliability baseline.** The reported Pearson correlation of 0.717 with Instructor scores is compared only against non-aligned scoring rules. Knowing how well two human instructors agree on the same reviews would contextualize whether ASR is approaching the human ceiling (strengthening the result) or leaving substantial room for improvement (weakening it). (Table 1, Section 5)

- **Assumption 2.2 ("Know-it-or-not") restricts the report space to ternary {0,1,⊥}.** While justified from dataset observations, the paper does not discuss how this limits the achievable alignment ceiling or the generality of the approach to other textual elicitation domains where reports may express continuous uncertainty. (Section 2.2, lines 110–116)

### Trivial
None.

## Nice-to-Haves

- Comparing against an **unconstrained predictor** (same MSE objective without properness constraints) would illuminate whether the properness constraint imposes a meaningful alignment cost, providing additional insight into the trade-off.

- Testing whether the **non-inverting assumption** (Definition 3.1) holds empirically for the LLM used would further strengthen the truthfulness claim, though the paper's properness guarantee is mathematical, not empirical.

## Removed Points

These points from the input review were removed with justification:

1. **"Baselines do not test the hypothesis"** — Removed because the paper's central claim is that ASR improves alignment *over existing truthful methods*. The chosen baselines (AV, MV) are the standard truthful methods from prior work, making the comparison valid on the paper's own terms. The unconstrained-predictor comparison is informative but not required for this claim; it has been moved to Nice-to-Haves.

2. **"Truthfulness is asserted but never empirically verified"** — Removed because properness is a mathematical guarantee from the optimization constraints (Definition 2.5). If the constraints are satisfied at the QP solution — which they are by construction — the scoring rule is proper by definition. The paper does not claim to run human-subject experiments verifying truthful behavior, and this is standard practice in mechanism design.

3. **"Missing prompts / appendix content"** — Removed per policy: the parser strips appendices; they exist in the original submission.

4. **"Overselling 'converts the reference scores into a proper score'"** — Removed as a minor phrasing nitpick that does not affect technical correctness.

5. Several **generic or speculative concerns** from the input review (e.g., "could the metric be measuring a proxy?", "are confounders controlled?") lacked concrete anchors in the paper and were removed.

## Novel Insights

None beyond the paper's own contributions. The review process confirms that the paper's core framing (properness vs. alignment trade-off) and convex formulation are sound, but reveals that the empirical reporting lacks sufficient detail (no confidence intervals, no train/test split specification, MSE scale ambiguity) to fully assess the reliability of the claimed results.

## Suggestions

- Clarify the MSE scale: explicitly state whether Table 1 reports MSE on the original [0,10] scale or a normalized scale, and ensure consistency with Program 1.
- Add per-assignment error bars or cross-validation results to support the reliability of the empirical claims.
- Specify whether the optimization is per-assignment or pooled across assignments, and describe the train/test split protocol.
- If available, report human inter-rater reliability on the same reviews to contextualize the correlation numbers.
- Discuss how the "know-it-or-not" assumption (Assumption 2.2) might limit generality.

## Score and Decision

**Calibration anchors used (all rounds):**

| File | Avg Human Score | Round | Itemized? | Comparison to this paper |
|---|---|---|---|---|
| EW62GvCzP9 (Truthfulness Without Supervision) | 4.67 | 1, 2 | Yes | Most similar — uses mechanism design for LLM evaluation. Our strengths are comparable but our empirical gaps are larger. |
| CbmAtAmQla (PRD: Peer Rank and Discussion) | 4.25 | 2 | Yes | LLM evaluation with peer methods. Our theory is cleaner but empirical reporting is weaker. |
| ga4LyaucKr (Learning-based Mechanism Design) | 2.50 | 1 | Yes | Automated mechanism design. Less topically similar; our paper is substantially stronger. |
| dxJKLozjQl (Data Distribution Valuation) | 3.00 | 1 | Yes | Incentive-compatible valuation. Our paper is stronger in both theory and empirical results. |
| Uj0h13lVrR (KL Divergence for GFlowNets) | 1.00 | 1 | No | Not relevant; strong reject paper. |
| nSDOkm0SKo (Financial Markets NN) | 1.00 | 1 | No | Not relevant; strong reject paper. |
| JQQDePbfxh (Private Mechanism Design) | 6.50 | 1 | No | Higher-scored mechanism design paper; stronger empirical rigor. |
| VGLU5N1AD2 (Incentivized Black-Box Model Sharing) | 6.00 | 1 | No | Higher-scored; more thorough empirical evaluation. |
| X0epAjg0hd (Calibration Comparison) | 5.67 | 1 | No | Higher-scored; stronger empirical methodology. |

**Bracket:** Round 1 placed the paper between 3.0 and 5.5. Round 2 narrowed to 4.0–5.0 by comparing itemized weights against the two most similar anchors (EW62GvCzP9 at 4.67 and CbmAtAmQla at 4.25).

**Weighted-item comparison that determines placement:** The paper's strengths (weights 9.40–9.79) match or exceed the strongest items of the 4.67 anchor (weights 7.95–10.90). However, the paper's two most damaging weaknesses — "No statistical reliability" (weight 0.23) and "MSE scale ambiguity" (weight 1.72) — are more severe than the worst weaknesses of the 4.67 anchor (weights 1.24–2.46). These are fixable reporting gaps rather than conceptual flaws, but they substantially undermine the reader's ability to trust the headline empirical results. This places the paper slightly below the 4.67 anchor.

**Final Score: 4.5**

**Decision: Reject** — The paper addresses a genuine problem with a clean, theoretically grounded approach, and the direction of the empirical results is promising. However, the empirical evaluation is presented without essential reliability information (no confidence intervals, no train/test split specification, ambiguous MSE scale). These gaps prevent the contribution from being assessed as presented. The paper would benefit from a revision that addresses these reporting issues.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>