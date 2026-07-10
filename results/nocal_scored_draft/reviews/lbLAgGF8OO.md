Now I have all the verification I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces Dig-DEC, a model-free decision-estimation coefficient that replaces the optimism principle of prior work with information-gain-driven exploration. It generalizes the AIR framework to arbitrary divergence measures with a clean Bregman-divergence analysis, provides improved estimation procedures (unbiased estimation for average error, constant-bound estimation for squared error), and applies the framework to obtain regret bounds for both stochastic and hybrid adversarial MDPs. The paper claims the first model-free regret bounds for hybrid MDPs with bandit feedback, resolving an open question from [LWZ25].

## Strengths

- **Conceptually cleaner complexity measure (Dig-DEC, Section 4.1).** The paper replaces the optimism principle of [FGQ+23] with an information-gain-driven approach. Removing optimism is necessary for the hybrid adversarial setting. Theorem 13 shows Dig-DEC ≤ optimistic DEC + η, so the new measure is never worse. (favorability: 0.94)
- **Theorem 14 (3-armed bandit example, Section 6).** This provides a concrete, verifiable instance where optimistic DEC suffers Ω(√T) regret while Dig-DEC achieves O(1), demonstrating that the improvement can be qualitative rather than a constant factor. (favorability: 1.00)
- **Improved estimation procedures (Section 4.2).** The unbiased estimator for average estimation error (splitting samples into two halves) is a genuine technical improvement over the biased estimator of [FGQ+23]. For Bellman-complete MDPs, achieving √T regret is substantial. The two-timescale posterior update that bounds Est by a constant is technically interesting. (favorability: 1.00)
- **Generalization to arbitrary divergence measures (Section 4).** The new Bregman-divergence-based analysis connects naturally to mirror descent and simplifies prior work while enhancing algorithmic flexibility. (favorability: 1.00)
- **Honest limitation discussion.** The paper explicitly acknowledges (lines 115-116) that Assumption 3 does not capture all learnable hybrid MDPs (e.g., low-rank MDPs with unknown reward features). (favorability: 0.79)

## Weaknesses

### Fatal
None.

### Major

- **Table 2 hybrid regret exponents are inconsistent with the paper's own dig-dec and Est bounds and the stated formula.** For the hybrid bilinear on-policy entry with Ḏ_av: dig-dec = (H⁵d³η)¹/², Est ≲ d log|Φ| T¹/² (Theorem 7 with N=d), and the paper's formula is Regret = T·dig-dec + Est/η (line 251). Applying this formula and optimizing η yields O(T⁵/⁶), but the table reports T³/². Four of the five hybrid entries have exponents > 1 (T³/², T¹³/⁸, T³/², T³/²), which would be worse than trivial regret. The dig-dec and Est bounds themselves are consistent with sublinear rates; the error lies in the computed final exponents in the table. Since the paper's core contribution includes the claim of "first sublinear regret for model-free learning in hybrid MDPs," this arithmetic inconsistency must be resolved. (favorability: 0.06)

- **Inconsistent improvement rate claims across abstract, introduction, and Table 1.** The abstract (line 13) claims improving T⁵/⁶ to T⁷/⁸ (off-policy, average error) — this is worse (0.833 → 0.875). The introduction (line 33) claims improving T⁵/⁸ to T⁵/⁶ — also worse. Table 1 reports T²/³ for these settings, matching neither the abstract nor the intro. Three locations report three incompatible sets of numbers on the paper's central quantitative claims, and two of the "improvements" actually increase the exponent. (favorability: 0.00)

### Minor

- **Line 213 claims a non-improvement.** The text states "our construction of the estimator improves their rate of Est from √T to T¹/²." Since √T = T¹/², this is not an improvement. The intended rate is unclear from the text. (favorability: 0.35)

### Trivial
None.

## Nice-to-Haves

- A brief discussion of when the minimax optimization in Eq. (3) is computationally tractable would strengthen the paper, though the paper acknowledges (line 37) that model-free here does not imply computational efficiency.
- Details on high-probability bounds for the hybrid setting (the paper mentions they are possible in the stochastic setting on line 272).

## Removed Points

These points were raised in the harsh review but are removed after verification against the paper:

- **Missing proof sketches / appendix derivations.** The criticism that no dig-dec bound derivations appear in the main body is removed because these derivations exist in the appendices (which are standard for a theory paper but stripped by the parser). Per the hard rules, weaknesses about missing appendix content in the extracted submission are not valid.
- **Speculative fatal classification of the Table 2 exponent issue.** The reviewer suggested the errors could be fatal. However, the underlying dig-dec and Est bounds are sublinear-consistent; the problem is in the final computed column. The core claim (sublinear rates exist) is not invalidated by an arithmetic mistake in the table.
- **Computational tractability as a weakness.** The paper explicitly scopes this out. Criticizing it for not addressing problems outside its stated scope is not a valid weakness.
- **Formatting/style nitpicks and requests for expanded exposition** (on-policy/off-policy terminology, high-probability bound exposition) are removed per the hard rules.

## Novel Insights

None beyond the paper's own contributions. The reviews surface numerical inconsistencies in the reported exponents, but these are error detections rather than new insights about the framework or methodology.

## Suggestions

1. **Correct the final regret exponents in Table 2** to be consistent with the formula Regret = T·dig-dec + Est/η and the stated dig-dec and Est bounds. Include explicit η-optimization algebra for at least one hybrid entry in the main body or appendix.
2. **Reconcile the improvement rate claims** across the abstract, introduction, and Table 1 so they report consistent numbers, and ensure every claimed improvement is actually a reduction in the exponent.
3. **Fix the √T = T¹/² non-claim** on line 213 by clarifying what improvement over [FGQ+23] is actually intended.

## Score and Decision

The paper introduces a conceptually clean complexity measure (Dig-DEC), a flexible generalized AIR framework with a simpler analysis, and improved estimation procedures. These are genuine contributions. However, the current version contains significant arithmetic and presentation errors in its flagship quantitative claims: Table 2's hybrid regret exponents are inconsistent with the paper's own formula and bounds, and the claimed improvement rates across the abstract, intro, and Table 1 are contradictory. These issues are fixable and do not invalidate the core technical framework, but they must be resolved before the paper can be accepted.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>