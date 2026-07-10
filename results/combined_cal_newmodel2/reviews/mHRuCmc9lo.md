Now I have all the evidence I need. Let me produce the final consolidated review.

## Summary

This paper studies robust decision making under ℋ-calibration, a flexible family of partial calibration guarantees. The authors characterize the minimax-optimal decision policy via a duality argument (Theorem 3.1), then show a sharp transition: once ℋ contains the decision-calibration indicators (size |𝒜|), the optimal robust policy collapses to the plug-in best response (Theorems 4.1–4.2). They also study practical cases where ℋ is induced structurally by standard training (self-orthogonality under squared loss, bin-wise calibration), and provide experiments on two regression datasets in the self-orthogonality setting.

## Strengths

- **Clean theoretical framing of a timely problem.** The paper formalizes a natural and important question: how should a decision maker act when the only guarantee about a forecaster is that it satisfies a specific weak calibration condition? The ℋ-calibration framework elegantly captures a spectrum from "no information" (ℋ = ∅) to full calibration (ℋ = all functions), and the robust optimization lens (Equation 5) is the right technical tool. The interpolation property (Section 2, Figure 1) cleanly situates the contribution relative to the two classical extremes.

- **The sharp transition at decision calibration is a genuine and non-obvious insight.** Theorems 4.1–4.2 show that the robust policy collapses to plug-in best response *as soon as* ℋ contains the |𝒜| decision-calibration indicators, rather than gradually as ℋ is enriched. This is not just a technical corollary — it meaningfully strengthens what was known about decision calibration. Prior work (Zhao et al., 2021; Noarov et al., 2023) showed that decision calibration implies no swap regret, which only precludes improvement via action-remapping policies. Theorem 4.1 precludes improvement via *any* forecast-to-action policy in the minimax sense, which is a strictly stronger guarantee (lines 175–177).

- **Practical bridge via training-pipeline structure.** Proposition 4.4 (self-orthogonality from squared-loss training) and Proposition 4.5 (bin-wise calibration) show the framework is not purely theoretical — it can be instantiated using constraints that arise naturally from standard training or common post-hoc procedures. This demonstrates awareness of deployment realities.

- **Computational tractability.** Theorem 3.1 reduces the infinite-dimensional minimax problem to a finite-dimensional dual optimization plus pointwise convex programs, enabling practical computation. The "two-step procedure" (lines 135–139) provides a clear interpretation.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Thin experimental evaluation.** Table 1 reports only point estimates with no error bars, confidence intervals, or significance tests. The reported differences are 0.01–0.02 on absolute scales (e.g., 0.410 vs. 0.402 for Bike Sharing under the worst-case-for-robust condition), making it impossible to assess whether these differences are meaningful or simply noise. There are no comparison baselines beyond the plug-in policy itself — for instance, simply recalibrating the forecaster via isotonic regression and then best-responding would be a natural and relevant baseline. The scope is limited to 2 tabular regression datasets, 1 model architecture (two-layer MLP), and 1 ℋ class. This limits the support for the paper's claims about practical applicability of the framework.

2. **The adversarial evaluation is circular in design.** The "adversarial" test distributions are derived from the dual of the same optimization problem that defines the robust policy (line 269: "a worst case induced by the robust dual, tailored to the robust policy"). The robust policy is designed to be optimal against this exact adversary; outperforming the plug-in rule against it is a consistency check of the saddle-point optimization rather than an empirical finding about real-world robustness. The paper would be strengthened by evaluating under realistic distribution shifts (e.g., time-based splits, domain shifts) not constructed from the dual.

3. **Gap between exact theory and approximate practice.** The self-orthogonality guarantee (Proposition 4.4) requires the model to reach a first-order stationary point of the *population* squared loss. The paper acknowledges (line 293) that the learned forecaster only "approximately satisfies" ℋ-calibration due to finite samples and approximate stationarity. While the paper notes that Appendix B discusses approximate ℋ-calibration (line 85), the main text does not sketch how approximation errors propagate to the robust policy's guarantees. For a paper that emphasizes practical relevance alongside theory, this gap deserves at least a brief quantitative discussion.

4. **Task-specificity of the decision calibration result is underdiscussed.** The paper establishes that decision calibration recovers plug-in optimality, framing this as comparable to full calibration's "trustworthiness" semantics. However, decision calibration is inherently task-specific: it requires |𝒜| indicator functions defined by a particular downstream utility and action set. The contrast with full calibration — which is task-agnostic and provides guarantees for *any* downstream decision maker — is therefore less dramatic than the framing sometimes suggests. While Corollary 4.3 addresses the case of multiple decision problems, the sample complexity of achieving joint decision calibration across many problems is not discussed.

5. **No discussion of sample complexity.** The paper does not address how much calibration data is needed to estimate the dual multipliers λ* (Theorem 3.1) from finite data to a given precision. For practitioners considering this framework, understanding the data requirements matters. Similarly, the claim about efficient computation (lines 140–142) is somewhat vague ("standard, fast methods").

### Trivial
None.

## Nice-to-Haves

- Compare the robust policy against simpler alternatives: e.g., recalibrate the forecaster via isotonic regression or Platt scaling, then best-respond. This would help isolate whether the robust framework's value comes from accounting for calibration uncertainty or from some other aspect of the procedure.
- Evaluate under realistic covariate shifts (e.g., temporal splits) alongside the dual-derived adversaries, to demonstrate protection beyond the worst-case optimization that defines the method.
- Add a brief paragraph distilling the key takeaway from the (stripped) Appendix B discussion of approximate ℋ-calibration into the main text, so readers can assess the practical reliability gap.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Experiments do not test the paper's headline contribution (decision calibration)"* — REMOVED because Theorem 4.1 is a mathematical theorem, not an empirical claim. The paper's abstract explicitly scopes the experiments to the self-orthogonality case: "we provide an empirical evaluation of a natural one that applies to any regression model solved to optimize squared error." The experimental section (lines 265–296) is honest about testing ℋ = {h(v)=v}. The decision calibration result does not require experimental validation; it is proven.
- *"No code mentioned; reproducibility concerns"* — REMOVED per the hard rule: the parser strips appendix sections where code/data links may reside, and the rule forbids criticizing missing appendix content.
- *"The 'any strictly stronger notion' framing elides task-specificity"* — WEAKENED and merged into the minor weakness about task-specificity above. The abstract is a summary; the body discusses task-specificity (Corollary 4.3).
- *"The paper would benefit from discussing non-linear utility extensions more"* — MOVED to nice-to-have; the paper already discusses this limitation (lines 105–107, 301) and notes potential linearization strategies, which is reasonable.

## Novel Insights

None beyond the paper's own contributions. The reviewers converge on the paper's own framing: the sharp transition at decision calibration (Theorems 4.1–4.2) is the key insight, cleanly distinguishing this work from prior swap-regret guarantees and establishing a crisp target for forecaster design.

## Suggestions

1. Add bootstrapped confidence intervals or error bars to Table 1, and report effect sizes with uncertainty measures.
2. Include at least one baseline: e.g., recalibrate the forecaster via isotonic regression and then best-respond, or compare against conformal-prediction-based decision rules.
3. Test under a realistic covariate shift (e.g., temporal split) alongside the dual-derived adversaries to demonstrate robustness beyond the definitional worst-case.
4. Add a brief paragraph in Section 4.2 or Section 5 that discusses how approximate ℋ-calibration (finite samples, approximate stationarity) impacts the robust policy's guarantees, even if only to bound the gap.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/X0epAjg0hd.md` | 5.67 | R1, R2 | Yes | "Reassessing Calibration" — similar experimental thinness (1 dataset), weaker theoretical contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uuPkll6i7m.md` | 6.75 | R1 | Yes | "Certified Calibration" — stronger experiments, comparable theory |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dIkpHooa2D.md` | 6.75 | R2 | Yes | "MixMax" — strong theory AND comprehensive experiments; novelty concerns (-1.76, -2.32) |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iOMnn1hSBO.md` | 6.80 | R2 | Yes | "Decision-Focused UQ" — strong theory, good empirical validation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XM7INBbvwT.md` | 4.67 | R1 | Yes | "Does Calibration Affect Human Actions" — weaker theoretical contribution, HCI study |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/g6fYDGKeyB.md` | 6.00 | R1 | No | "Addressing Misspecification in SBI" — similar score band, different topic |

**Round 1 bracket:** 5.5–7.5, based on the paper's solid theoretical contribution and limited experimental breadth.

**Round 2 narrowing:** Comparing itemized favorability ratings against anchors:
- My paper's strengths (favorability 11.44–15.43) are stronger than the 5.67 anchor's strengths (4.02–10.88) and competitive with the 6.75–6.80 anchors.
- My paper's main negative weaknesses (experimental thinness at -1.74 to -0.27) are comparable to the 5.67 anchor's only negative weakness (-0.55) and less severe than the 6.75–6.80 anchors' worst weaknesses (-1.75 to -2.32).
- However, the 6.75–6.80 anchors have FAR more comprehensive experiments (multiple datasets, ablations, baselines), which offsets their moderate novelty concerns. My paper lacks this empirical support.

The paper's theoretical contribution is strong enough to rise above the 5.67 anchor, but the weak experiments prevent it from reaching the 6.75–6.80 level. The final score reflects a solid theoretical paper whose experimental rigor does not match its theoretical ambition.

**Final score: 6.0** — borderline accept. The theoretical contributions (Theorem 3.1's duality characterization, the sharp transition in Theorems 4.1–4.2) are genuine and well-presented. The experiments, however, are too thin to convincingly demonstrate practical applicability for a venue like ICLR. The paper would be strengthened by addressing the minor weaknesses (error bars, baselines, realistic distribution shifts) and providing a quantitative discussion of the approximation gap.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>