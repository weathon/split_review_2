## Summary

This paper proposes Aligned Scoring Rules (ASR), which optimizes proper scoring rules for textual information elicitation to align with an exogenous reference score (human or LLM-judge scores). Building on Wu & Hartline (2024)'s reduction from textual to numerical elicitation, the paper formulates a convex optimization problem over separate scoring rules with properness constraints, minimizing MSE with a reference score. Experiments on peer grading datasets show correlation improvements over non-aligned baselines.

## Strengths

1. **Well-motivated and timely problem.** The paper correctly identifies the tension between provable truthfulness (properness) and alignment with human preferences in LLM-mediated scoring. Non-proper methods (direct LLM scoring) lack incentive guarantees, while existing proper methods (V-shaped rules) do not prioritize alignment. This gap is genuine and practically relevant for peer grading and other LLM-based evaluation settings.

2. **Clean convex optimization formulation.** Reducing to a convex optimization problem over separate scoring rules (Program 2) — with 6 variables per dimension, linear properness constraints, and a quadratic (MSE) objective — is a clean instantiation of automated mechanism design for this setting. The convexity guarantee (Corollary 3.4) is meaningful because it makes global optimality computationally tractable, differentiating this from non-convex alternatives like max-over-separate rules.

3. **Large improvement on correlation metrics.** ASR achieves Pearson correlations of 0.717 (Instructor) and 0.705 (LLM-Judge), versus 0.294 and 0.328 for the best non-aligned baseline (EGPT(AV)). Even accounting for the evaluation concerns below, the correlation improvement is sizable and suggests the approach has genuine potential.

## Weaknesses

### Fatal
None.

### Major

1. **No held-out evaluation — the central empirical claim is unsubstantiated.** The paper never describes a train/test split, cross-validation, or any form of out-of-sample evaluation. The phrase "training data D" appears once (line 358) in defining the constant baseline, but the results in Table 1 are never stated to be on held-out data. Since ASR is *explicitly optimized* to minimize MSE with the reference score, comparing its training-set performance against non-optimized baselines (fixed V-shaped rules, constant) tells us nothing about whether ASR has learned a genuinely better scoring rule or has simply memorized the training data. The sample sizes compound this concern: per assignment there are roughly 36–64 peer reviews, and each optimization has 6*m* variables (where *m* is the number of summary points). With such small samples, overfitting is a realistic possibility, yet no regularization, held-out results, or confidence intervals are reported anywhere. **Without out-of-sample evaluation, the paper's central claim that ASR "outperforms baseline methods" lacks evidential support.** This is the single most consequential flaw.

2. **Scale mismatch inflates MSE comparisons against EGPT baselines.** The V-shaped scoring rule (Definition 2.4) outputs scores in [0, 1/2]. ASR is constrained to [0, 1] (Program 2, boundedness constraint) and reference scores are normalized to [0, 1] (Section 3.2, line 227). MSE is not scale-invariant: ASR MSE of 1.730 vs. EGPT(AV) MSE of 9.541 — a ~5.5× gap — is partially an artifact of different scales. The paper acknowledges this indirectly for Spearman correlation (footnote 3, line 366: "because the ElicitationGPT scores are not in the same scale as reference scores") but still reports MSE as if the comparison were apples-to-apples. Pearson correlation is scale-invariant and shows a real advantage, but even that comparison is compromised if results are in-sample (Issue #1).

### Minor

3. **The "nearly-identity" claim is unquantified.** The paper states (lines 40–41, 344) that linear regression of reference scores on ASR scores is "nearly the identity function" but does not report the regression coefficients, intercepts, or confidence intervals. Without these numbers, the claim is visually suggestive but not quantitatively substantiated.

4. **Baselines do not include any other *aligned* proper scoring rule.** The paper compares ASR against a constant score and non-aligned V-shaped rules (EGPT(AV/MV)). Neither baseline is optimized for alignment. Showing that optimizing for alignment (ASR) outperforms not optimizing is unsurprising. To establish that ASR's specific form is valuable, the paper should compare against other ways of producing an aligned proper scoring rule — e.g., optimizing the V-shaped rule's parameters (steepness, threshold) to minimize MSE, or a simple post-hoc affine transformation of the EGPT score (which would be weakly truthful if monotonic).

5. **Know-it-or-not assumption (Assumption 2.2) is under-discussed.** Restricting agent beliefs to {0, 1, prior} is a significant restriction shaped by the specific dataset. The paper does not discuss how this limits applicability to settings where agents have more nuanced posterior beliefs (e.g., "70% confident"), and how the ternary representation constrains the method's generality.

6. **No analysis of per-assignment summary point count (m) or its effect on optimization.** The number of variables scales linearly with m, and overfitting risk grows with larger m, but m is never reported across the 22 assignments.

### Trivial
- The notation switch from θ ∈ [0,1]^n (Section 2.1, numerical elicitation) to θ ∈ {0,1}^m (Section 2.2, textual elicitation) without explicit explanation of whether n = m or these are distinct spaces could confuse readers.

## Nice-to-Haves
- Report out-of-sample results using per-assignment cross-validation with mean and variance of MSE and correlations across folds.
- Normalize EGPT baselines to [0,1] scale before MSE comparison, or report scale-invariant metrics (e.g., R²) consistently.
- Add at least one baseline that is also optimized for alignment (e.g., optimized V-shaped rule parameters, learned affine transformation of EGPT).
- Report regression coefficients with confidence intervals for the "nearly-identity" fit.

## Removed Points

These points were considered but removed from the main weakness list with justification:

- **"Section 3 theorems are inherited from Wu & Hartline (2024) — should be clearer about what is novel."** — The paper explicitly attributes Theorems 3.2 and 3.3 to Wu & Hartline (2024) (lines 217, 221). The novelty is the optimization framework, not the properness theorems themselves, and this is clearly stated.

- **"How is the expectation in Program 1/2 estimated?"** — This is standard practice: empirical MSE over the dataset, as implied by "gradient descent over samples" (line 256).

- **"Exponentially many constraints in Program 2."** — The boundedness constraint Σ_i S_i(r_i, θ_i) ∈ [0,1] is over all r,θ combinations, giving 3^m × 2^m constraints in principle. However, these are linear constraints on the 6m variables, and m is small in practice (the paper never reports m, but given 6–8 submissions per assignment, m is likely small). This is a practical implementation detail rather than a fundamental flaw.

- **"LLM-Judge correlation of 0.55 is noisy."** — The paper acknowledges this and uses LLM-Judge as a *second* reference score; it does not claim the LLM-Judge is perfect. The main results also use the Instructor Score as reference.

- **"Spearman comparison differs from prior work."** — The paper transparently notes this difference in footnote 3. This is appropriate disclosure, not a weakness.

- **"No runtime or convergence analysis."** — Minor implementation detail; the convexity guarantee (Corollary 3.4) ensures global optimality, making runtime details secondary for a methodology paper.

- **"Interpretability claim deferred to appendix."** — The appendix was stripped by the parser; this is not a weakness of the submitted paper.

- **"Cost of LLM oracle calls."** — Out of scope; all methods using LLMs have comparable costs, and this paper uses the same ElicitationGPT framework as the baselines.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a critical experimental gap (held-out evaluation) that the paper itself does not address, but this is a flaw to be fixed rather than a novel observation.

## Suggestions

1. **Add out-of-sample evaluation.** Use per-assignment cross-validation: for each assignment, hold out some submissions, train ASR on the remainder, and evaluate on held-out data. Report mean and variance of MSE and correlations across folds. This is the single most important improvement needed.

2. **Normalize EGPT baselines to [0,1] scale** before computing MSE, or report scale-invariant metrics (R², Pearson correlation) as the primary comparison.

3. **Report regression coefficients** for the "nearly-identity" fit (Figure 4), including confidence intervals.

4. **Add aligned baselines** — e.g., optimize V-shaped rule parameters for MSE, or apply a learned affine transformation to EGPT scores.

5. **Report summary point statistics** (m per assignment, distribution) to help assess overfitting risk.

---

## Score Calibration

**Anchor papers used for calibration** (from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR.md (KL Divergence GFlowNets) | 1.00 | Bracket | Fundamentally flawed method; this paper is substantially stronger |
| ga4LyaucKr.md (PFM-Net) | 2.50 | Bracket | Trivial extension of prior work with missing baselines; this paper has a genuine contribution |
| dxJKLozjQl.md (Data Distribution Valuation) | 3.00 | Bracket | Definitional error in key concept; this paper's theory is sound |
| EW62GvCzP9.md (Truthfulness w/ Peer Prediction) | 4.67 | Bracket+Narrow | Interesting idea with broader experiments but stronger assumptions; comparable quality |
| yCEf1cJDGh.md (Truthful Aggregation of LLMs) | 5.25 | Bracket | Cleaner experiments but limited novelty; this paper is slightly weaker empirically |
| XM7INBbvwT.md (Calibration & Human Actions) | 4.67 | Narrow | Insufficient experimentation similar to this paper, but different domain |
| VGLU5N1AD2.md (Incentivized Black-Box Model Sharing) | 6.00 | Bracket | Solid theory and experiments; this paper's evaluation is notably weaker |

**Round 1 bracket:** 3.5–5.5 (the paper has a real theoretical contribution but the evaluation is insufficient to properly assess the central empirical claims).

**Final score determination:** The paper is clearly above the 2.5–3.0 level of papers with trivial or definitionally flawed contributions. However, it falls below the 5.0–5.5 level of papers with adequate experimental validation. The held-out evaluation gap is the deciding factor — without it, the paper's main empirical claim cannot be evaluated. Compared to the Truthfulness w/ Peer Prediction paper (4.67), which had broader experiments but stronger assumptions, this paper has cleaner theory but weaker experiments, placing it at a similar level. Score of 4.0 reflects a borderline-reject paper with a real contribution that needs significant experimental rework.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>