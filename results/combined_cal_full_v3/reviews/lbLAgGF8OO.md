Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces Dig-DEC (dual information-gain decision-estimation coefficient), a new model-free DEC framework that replaces the optimism principle of prior work [FGQ+23] with information-gain-driven exploration. This reframing allows the framework to handle adversarial/hybrid environments without explicit reward estimators, yielding the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and general transition structures — resolving an open problem from [LWZ25]. The paper also refines online function-estimation procedures to obtain improved regret rates in the stochastic setting and provides a concrete separation result (Theorem 14) showing Dig-DEC can be arbitrarily better than optimistic DEC.

## Strengths

- **A clean conceptual generalization (Section 4, Eqs. 7-8).** Dig-DEC replaces optimism with a KL information-gain term and a flexible divergence measure \(D\), unifying stochastic and hybrid/hybrid settings under one framework. This is a genuinely insightful reframing of the AIR/DEC methodology.

- **Concrete separation from optimistic DEC (Theorem 14, Section 6).** A 3-armed bandit example where optimistic DEC suffers \(\Omega(\sqrt{T})\) regret while Dig-DEC achieves \(O(1)\) regret. This demonstrates the additional KL information-gain term can yield arbitrarily large improvements, not just a technical modification.

- **Resolves an open problem (Section 5.2).** Obtaining the first model-free regret bounds for hybrid MDPs with bandit feedback under linear reward and general transition structures is a genuine advance over [LWZ25], which required full-information feedback. The paper correctly motivates why this was challenging (line 81: optimistic updates require explicit reward estimators that bandit feedback cannot provide).

- **Clear limitations acknowledged.** The paper explicitly identifies where Assumptions 3-4 break down (line 115: low-rank MDPs with unknown reward features) and states this as future work. The non-standard definition of "model-free" (independence from \(|\mathcal{M}|\), not absence of model access) is clarified in line 37.

## Weaknesses

### Minor

- **Fraction rendering errors create inconsistencies in quantitative claims.** Several places in the paper show internally inconsistent or contradictory exponents:

  - **Abstract (line 13):** Claims improvement from \(T^{5/6}\) to \(T^{7/8}\) (off-policy), but \(7/8 > 5/6\), so this would be a worse rate, not an improvement.
  - **Introduction (line 33):** Gives different starting numbers (\(T^{3/2}/T^{5/8}\)) than the abstract (\(T^{3/4}/T^{5/6}\)) for the same claimed improvements.
  - **Table 2 (lines 291-295):** The regret column shows superlinear exponents \(T^{3/2}\) and \(T^{13/8}\) for the hybrid setting, which directly contradicts the paper's claim of "first sublinear regret" for model-free hybrid learning. Computing the regret formula \(T\cdot\text{dig-dec} + \text{Est}/\eta\) with optimal \(\eta\) yields sublinear rates (approximately \(T^{5/6}\) for the average-estimation case), confirming these are formatting/rendering errors rather than mathematical errors.

  These issues are very likely artifacts of fraction mis-rendering during PDF generation, and the conceptual contribution of the paper does not depend on the exact exponent values. Nevertheless, the printed text as-is prevents a reader from verifying the paper's quantitative claims. The authors must correct these before publication.

### Trivial

- The term "model-free" has a non-standard meaning here (independence from \(|\mathcal{M}|\)), which is clarified on line 37 but the abstract uses the term without this qualification. A brief clarification in the abstract would prevent misinterpretation.

## Nice-to-Haves

- A brief remark on when the saddle-point optimization in Eq. (3) is computationally feasible would be useful, though this is outside the paper's stated scope of regret bounds.
- Including a worked example in the main text (e.g., computing the Dig-DEC bound for the 3-armed bandit of Theorem 14) would help readers verify the mechanics without diving into appendices.

## Removed Points

These points from the input review were removed:

- "All verification deferred to appendices" — standard for ICLR papers; not a genuine weakness.
- "Computational complexity of Algorithm 1 not discussed" — outside the paper's scope.
- "Model-free caveat should be stated early" — the paper does state it in Section 1 (line 37); adding to the abstract is a nice-to-have, not a weakness.
- Speculative concerns about assumptions being "strong" — the paper acknowledges these limitations itself.
- "Strengthening the Paper on Its Own Terms" suggestions — these are suggestions for improvement, not weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the fraction rendering in the abstract, introduction, and Table 2 so that regret exponents are internally consistent and match the stated claims (e.g., verify whether \(T^{3/2}\) in Table 2 should be \(T^{2/3}\) or \(T^{5/6}\) after optimizing \(\eta\)).
2. Reconcile the abstract's rate claims with the introduction's — they should reference the same quantities.
3. Add a brief clarification in the abstract that "model-free" means the regret bound is independent of \(|\mathcal{M}|\).

## Score and Decision

**Calibration:** I compared this paper against six anchors from the review corpus. 

| Anchor | Score | Decision | Comparison |
|--------|-------|----------|------------|
| txD9llAYn9 (Model-based RL, horizon-free) | 7.00 | Accept | Stronger theory but also more extreme weakness items; our paper has fewer fundamental issues |
| aPNwsJgnZJ (Horizon-free adversarial RL) | 6.00 | Accept | Similar genre; our paper has stronger strength-item ratings and a less severe novelty concern |
| 0oWGVvC6oq (Bits and Bandits) | 6.50 | Accept | Similar level of contribution; comparable strength ratings |
| GvsCOOPxoI (DEC-POMDPs) | 6.17 | Reject | Rejected despite score due to presentation issues; our paper has clearer novelty |
| 2h3m61LFWL (VBMLE) | 4.25 | Reject | Our paper does not share its fatal flaw (limited novelty vs. prior work) |
| G1DoOVM3xZ (Low-switching RL) | 5.25 | Reject | Our paper has clearer technical novelty and a separation result |

The paper under review has all strengths rated \(\ge 8.86\) (high, comparable to 6-7 range accept-level papers) and its weakest item at 3.36 (no sub-1.0 or negative items that characterize lower-scored papers). Its conceptual novelty is genuine, and the fraction-rendering issue is fixable without affecting the core contribution.

**Round-1 bracket**: [6.0, 7.0]. The paper sits comfortably above the 4-5 range papers that lacked novelty, and somewhat below the very strongest 7+ papers that had higher-impact theoretical advances. Final score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>