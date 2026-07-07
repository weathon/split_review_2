Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

This paper introduces Dig-DEC, a model-free decision-estimation coefficient that removes the optimism principle from prior work (FGQ+23) and drives exploration purely through information gain (KL regularization plus an information-gain term). The framework generalizes prior AIR-based approaches under a flexible divergence measure D, connects to mirror descent analysis, and is applied to stochastic and hybrid MDPs with bandit feedback. The paper claims improved regret exponents over prior DEC-based methods and the first model-free regret bounds for hybrid MDPs with bandit feedback.

## Strengths

1. **Conceptual advance: optimism-free DEC.** The paper introduces Dig-DEC, a model-free DEC that removes the optimism principle, driving exploration purely through information gain. The general framework (Algorithm 1, Eq. 2) unifies prior AIR-based approaches (XZ23, LWZ25) under a flexible divergence measure D with an analysis connecting to mirror descent rather than relying on the restrictive "constructive minimax theorem" of prior work. This is a genuine conceptual advance.

2. **Improved estimation procedure (squared error case).** The two-timescale posterior update (Section 4.2.2) that bounds Est by a constant (independent of T), improving over FGQ+23's O(T^{1/2}) bound, and achieving √T regret for Bellman-complete MDPs, is a clean technical improvement. This is the first time a DEC-based method matches the rate of optimism-based approaches in Bellman-complete MDPs.

3. **Addressing an open problem.** The paper claims to resolve the main open question of LWZ25 — model-free learning in hybrid MDPs with bandit feedback — by leveraging the removal of optimism to avoid explicit reward estimators. If the theoretical results are sound, this is a significant contribution to the RL theory literature.

## Weaknesses

### Fatal

None. The core ideas (Dig-DEC, optimism-free exploration, general divergence framework) appear conceptually sound, and no verified error invalidates the framework itself. However, the paper has serious presentation and consistency issues that undermine confidence in the specific quantitative claims.

### Major

1. **Pervasive exponent inconsistencies between the abstract, introduction, and Table 1.** The paper's central quantitative claims — the regret exponents — are reported inconsistently across sections:

   - **Abstract (line 13):** For average estimation error, the improvement is *from* T^{3/4} *to* T^{3/5} (on-policy) and *from* T^{5/6} *to* T^{7/8} (off-policy).
   - **Introduction (line 33):** For the same average estimation error case, the improvement is described as *from* T^{3/2}/T^{5/8} *to* T^{3/2}/T^{5/6}.
   - **Table 1 (lines 262–265):** All non-completeness stochastic entries show **T^{2/3}**.

   These are three different sets of numbers that cannot all be correct for the same quantity. The abstract's T^{3/5} (0.6) and T^{7/8} (0.875), the introduction's T^{3/2} (1.5, superlinear) and T^{5/6} (0.833), and Table 1's T^{2/3} (0.667) are numerically incompatible. For a theory paper whose primary contribution is quantified by regret exponents, a reader cannot determine what rate the paper actually claims. This is a structural presentation error that must be fixed.

2. **Hybrid setting regret bounds in Table 2 are superlinear for 5 of 6 entries, directly contradicting the paper's claim of "sublinear regret."** The paper states (line 32) it obtains "the first sublinear regret for model-free learning in hybrid bilinear classes and Bellman-complete coverable MDPs." However, Table 2 (lines 291–295) reports the following regret exponents:

   | Entry | Exponent | Sublinear? |
   |-------|----------|------------|
   | bilinear, on-policy | T^{3/2} = T^{1.5} | No |
   | bilinear, off-policy | T^{13/8} = T^{1.625} | No |
   | bilinear\*, on-policy (complete) | T^{3/2} = T^{1.5} | No |
   | bilinear\*, off-policy (complete) | T^{1/2} = T^{0.5} | Yes |
   | coverable (complete) | T^{3/2} = T^{1.5} | No |

   Five of six entries have superlinear exponents, meaning regret grows faster than the number of rounds. The table caption states these are the final regret bounds after optimizing η. Without an explanation that resolves the apparent contradiction between the superlinear table entries and the "sublinear regret" claim, the paper's central advertised result is unsupported by its own data. A simple algebraic check using the stated dig-dec and Est formulas for the bilinear on-policy case (dig-dec = (H⁵d³η)^{1/2}, Est = d log|Φ| T^{1/2}) yields Reg = O(T^{5/6}) after η-optimization, *not* T^{3/2} — which suggests either the table, the formulas, or the optimization is incorrectly communicated.

3. **Claimed "improvement" for the off-policy case is actually a degradation in the abstract.** The abstract (line 13) claims to improve the off-policy regret bound from T^{5/6} (≈0.833) to T^{7/8} (≈0.875). Since larger exponents mean worse regret scaling, this is an arithmetic degradation, not an improvement. Whether this is a typo (the actual result is T^{2/3} as in Table 1) or a genuine error, it erodes confidence in the paper's self-reported results.

### Minor

1. **Vacuous claim about Est improvement (line 213).** The text states the estimator "improves their rate of Est from √T to T^{1/2}" — which are the same function. The surrounding context (unbiased vs. biased estimator) suggests the improvement may be in constants or log factors, but the statement as written is meaningless. This needs clarification.

### Trivial

None.

## Nice-to-Haves

- Including a worked derivation for one representative case (e.g., stochastic on-policy bilinear class) showing how dig-dec + Est + η-optimization yields the final regret exponent would substantially increase reader confidence.
- The notation T^{3/2}/T^{5/8} in the introduction (line 33) should be explicitly labeled as (on-policy/off-policy) rather than requiring the reader to infer this.

## Removed Points

The following points from the input review were removed. Treat them with caution:
- **Criticism about missing appendix/proofs in appendix:** The parser strips appendix sections from all papers; these exist in the original submission. The analysis connecting dig-dec to regret and the choice of η is in the appendix, which is standard for theory papers.
- **Criticism about scope limitation of Assumption 3 (low-rank MDPs with unknown reward features):** The paper explicitly acknowledges this limitation (line 115: "We remark that while Assumption 3 is a reasonable generalization... we leave it as future work"), so this is not a weakness the paper overlooks.
- **Criticism about missing comparison baselines / relation to other works:** These are either addressed in the paper or not verifiable (the reviewer may lack knowledge of the cited references).
- **Generic presentation and formatting concerns:** These are either parser artifacts or minor stylistic points.
- **Criticism about deriving regret bounds in main text:** It is standard for theoretical papers at this level to defer detailed derivations to the appendix.
- **Reproducibility concerns about hyperparameters and implementation details:** Appropriate for a theory paper whose contribution is analytical, not empirical.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reconcile all regret exponents.** The abstract, introduction, and Table 1 must report the same numbers. If Table 1's T^{2/3} is the correct rate for the average estimation error case under the stated setting, then both the abstract and introduction should say T^{2/3} — not T^{3/5}, T^{7/8}, or T^{3/2}. Verify and correct every number.
2. **Explain the hybrid Table 2 entries.** The preponderance of superlinear exponents (T^{3/2}, T^{13/8}) contradicts the paper's "sublinear regret" claim. Either show the algebra that reduces these to sublinear rates (e.g., T^{5/6} after properly substituting the optimal η), or clearly state which entries actually achieve sublinear regret and under what conditions. If some settings genuinely yield superlinear regret, this must be acknowledged rather than claiming sublinear regret for all hybrid settings.
3. **Fix the off-policy comparison.** If T^{7/8} in the abstract is a typo, correct it. If it is not, explain why a larger exponent constitutes an improvement.
4. **Correct the √T vs T^{1/2} statement** in Section 4.2.1 (line 213) to clearly state what is actually being improved.

## Score and Decision

**Calibration Analysis:** I compared this paper against anchors retrieved from the human-review corpus. The most relevant anchors for this type of theoretical RL contribution are:
- **Value-Biased MLE (2h3m61LFWL, avg 4.25):** A theory paper with a solid technical idea but notable weaknesses (strong assumptions, unclear novelty relative to prior work, missing analysis of computational cost). The current paper has stronger conceptual novelty (Dig-DEC vs. optimistic DEC) but more severe presentation issues (exponent inconsistencies affecting the headline claims).
- **Nearly Optimal RL (G1DoOVM3xZ, avg 5.25):** A solid theory contribution with near-optimal guarantees across multiple metrics. Its main weaknesses (strong assumptions, unclear novelty in parts) are comparable in severity to the current paper's exponent issues.
- **On Bits and Bandits (0oWGVvC6oq, avg 6.50):** A higher-scoring theory paper with a clean conceptual contribution and clear presentation despite some writing density. The current paper's presentation issues are more severe.
- **Model-based RL as Minimalist (txD9llAYn9, avg 7.00):** A strong theory paper with novel results and clean exposition. The current paper does not reach this level of presentation polish.

**Bracket:** After comparing weighted items, this paper sits between the 4.25 and 5.25 anchors — its conceptual contribution is stronger than the 4.25 paper, but its exponent inconsistencies and the Table 2 superlinear issue are more serious presentation problems than the 5.25 paper's issues (which were about assumptive strength and novelty shading, not self-contradictory numbers). The paper cannot be scored above 5 because the reader cannot currently verify which quantitative claims are correct.

**Final Score: 4.5/10** — Borderline reject. The core conceptual contribution (Dig-DEC as an optimism-free, information-gain-driven DEC) is interesting and potentially significant. However, the pervasive exponent inconsistencies between the abstract, introduction, and Table 1, combined with Table 2's unexplained superlinear hybrid entries that contradict the paper's advertised claim of sublinear regret, mean the paper's quantitative claims cannot be trusted in their current form. The paper requires a thorough rewrite that presents a single, consistent, correct set of numerical results before it can be evaluated on its scientific merit.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>