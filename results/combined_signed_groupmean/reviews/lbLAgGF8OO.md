Now I have sufficient calibration data. Let me produce the final review.

## Summary

The paper introduces Dig-DEC, a new model-free Decision-Estimation Coefficient that replaces optimism with information gain (via an extra KL regularization term), and provides a general algorithmic framework for decision-making with structured observations. It obtains regret bounds in both stochastic MDPs and hybrid MDPs (stochastic transitions + adversarial rewards with bandit feedback), resolving an open problem from [LWZ25]. The paper also refines online function estimation procedures, achieving improved estimation error bounds.

## Strengths

- **Conceptual contribution: removing optimism from DEC.** The paper identifies that the optimistic DEC of [FGQ+23] relies on an optimism principle that limits it to stochastic environments. Replacing this with an information-gain-driven mechanism (via an extra KL regularization term) is conceptually clean, principled, and constitutes a genuine advance, not an incremental tweak.

- **Handling the hybrid setting with bandit feedback.** The removal of optimism avoids the need for an explicit reward estimator, which is why optimistic approaches could not handle the bandit-feedback hybrid setting. If the technical results hold, this resolves the main open problem from [LWZ25] — model-free learning in hybrid MDPs with bandit feedback is a natural and important setting.

- **Improved online function estimation.** The unbiased estimator using sample splitting (Section 4.2.1) and the two-timescale procedure yielding a log²|Φ| Est bound (Theorem 11) are substantial improvements over the T^{1/2} bound of prior work, assuming the proofs hold.

- **Theorem 14 (3-armed bandit construction).** Provides a concrete example where optimistic DEC suffers Ω(√T) regret while Dig-DEC achieves constant regret, demonstrating strict improvement that can be arbitrarily large.

- **More flexible analysis framework.** The connection to Bregman divergences and mirror descent (lines 153–171) genuinely generalizes the earlier AIR framework of [XZ23, LWZ25], which relied on a "constructive minimax theorem" restricted to strictly convex divergences.

## Weaknesses

### Major

- **Numerical inconsistencies between abstract and introduction.** The abstract (line 13) claims improvement from T^{3/4} to T^{3/5} (on-policy) and from T^{5/6} to T^{7/8} (off-policy). The introduction (line 33) gives different numbers: improving T^{3/2}/T^{5/8} to T^{3/2}/T^{5/6}. Worse, two of the four claimed pairs are actually regressions (exponent increases): T^{5/6}→T^{7/8} (0.833→0.875) and T^{5/8}→T^{5/6} (0.625→0.833). The abstract and introduction also disagree on the baseline values. This makes it impossible to determine which rates are actually being claimed, and it is unclear whether the paper's own advertised improvements are correct as written.

- **Table 2 (hybrid settings) shows mostly superlinear regret exponents contradicting the headline claim of "first sublinear regret" (line 32).** Of the 5 entries, 4 have T^{3/2}=T^{1.5} or T^{13/8}=T^{1.625}, which are superlinear (worse than linear). Only the bilinear★ off-policy entry achieves T^{1/2} (sublinear). For the coverable MDP entry (which the claim explicitly includes), the exponent is T^{3/2} — directly contradicting the claim of sublinear regret. The paper's central advertised claim is materially misleading relative to its own results.

### Minor

- **Line 213 states "improves their rate of Est from sqrt(T) to T^{1/2}".** Since sqrt(T) and T^{1/2} are identical, this is self-contradictory. Likely a typo, but it indicates sloppy presentation of quantitative claims in a paper whose numerical results are already hard to verify.

- **Abstract's "always no larger" claim omits additive slack.** Theorem 13 shows dig-dec ≤ o-dec + η, where η is a parameter that can be non-negligible. The abstract's phrasing "Dig-DEC is always no larger than optimistic DEC" (line 11) is imprecise; Theorem 13 gives the correct statement. This is a minor presentation issue since the paper does discuss the relationship in Section 6.

### Trivial

None.

## Nice-to-Haves

- The "model-free" definition (line 37: regret bound independent of |M|) is honestly caveated but readers expecting computationally tractable algorithms may be misled. A brief paragraph discussing the computational requirements of solving the minimax optimization (Eq. 3) for the settings considered would strengthen the paper.

- A concrete example for the hybrid setting analogous to Theorem 14 (which is for the stochastic case) would strengthen the claim that optimism removal enables handling adversarial rewards with bandit feedback.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Model-free definition is weak"** (Removed: the paper explicitly defines "model-free" on line 37 and caveats it honestly. This is a standard definition in this subfield; the criticism reflects expectations outside the paper's stated framing.)

- **"Algorithm 1 is underspecified without the appendix"** (Removed: deferring implementation details to the appendix is standard for theory papers at this venue. The main text provides the conceptual structure.)

- **"No discussion of computational cost"** (Removed: papers that define "model-free" in the narrow sense used here routinely do not discuss computational complexity. This is a scope-appropriate choice.)

- **Various formatting/style complaints** (Removed per instructions: these are parser artifacts or out of scope.)

## Novel Insights

The reviews surface a clear pattern: the conceptual contribution (information-gain-driven DEC replacing optimism) is genuinely novel and well-motivated, and the theoretical framework connecting to Bregman divergences and mirror descent is a meaningful generalization. However, the presentation of quantitative results — particularly the inconsistency between abstract and introduction, some regressions being presented as improvements, and Table 2's mostly superlinear exponents contradicting the "first sublinear regret" claim — is severe enough that the core numerical claims cannot be verified from the main text alone. This is unusual: typically a strong conceptual paper presents clean numerical results, but here the numbers themselves are at odds with the paper's narrative.

## Suggestions

1. **Reconcile the abstract and introduction** to give the same numerical claims. Verify each claimed improvement is actually an improvement (exponent decreases, not increases).

2. **Clarify the "first sublinear regret" claim.** If only the Bellman-complete off-policy setting achieves sublinear regret in the hybrid case, state this explicitly. The coverable entry shows T^{3/2}, which is superlinear — this directly contradicts the claim as written in line 32.

3. **Fix the sqrt(T)=T^{1/2} typo** at line 213.

4. **Present the additive η in Theorem 13** alongside the abstract's "no larger" claim to avoid misleading readers.

## Score and Decision

**Calibration anchors used:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Value-Biased MLE for Model-based RL (rej) | 2h3m61LFWL.md | 4.25 | R1 | Yes | Weaker conceptual novelty, cleaner presentation. Current paper has stronger ideas but worse numerical presentation. |
| Model-Free BPI in CMDPs (rej) | w8Zo7jACq7.md | 5.20 | R1 | Yes | Different setting (CMDPs). Similar quality of theory but cleaner claims. |
| Nearly Optimal Low-Switching RL (rej) | G1DoOVM3xZ.md | 5.25 | R1 | Yes | Similar type of theory paper with presentation issues. Current paper has stronger conceptual novelty. |
| Model-based RL Minimalist (acc) | txD9llAYn9.md | 7.00 | R1 | Yes | Cleaner presentation, stronger empirical grounding. Higher quality tier. |
| No-regret Adversarial MDP Revealed Trans. (rej) | i3KSorBQxF.md | 4.00 | R2 | No | Similar subfield, weaker novelty. Accepted for comparison. |
| MaxInfoRL (acc) | R4q3cY3kQf.md | 6.75 | R2 | Yes | Different approach (empirical + theory). Cleaner quantitative presentation. |
| RL as Info-State Policies in BAMDP (rej) | ByW9j60mvV.md | 5.25 | R2 | Yes | Conceptual paper with mixed reviews, some presentation concerns. Current paper has more rigorous technical framework. |
| Bits and Bandits (acc) | 0oWGVvC6oq.md | 6.50 | R2 | Yes | Clean theory paper with clear claims. Higher quality tier. |

**Round 1 bracket:** 3.5–5.5

**Narrowing:** Compared to anchors at the 4.0–5.25 level (i3KSorBQxF, 2h3m61LFWL, w8Zo7jACq7, G1DoOVM3xZ, ByW9j60mvV), the current paper has stronger conceptual novelty (the Dig-DEC idea is genuinely new) but worse numerical presentation issues (inconsistent claims, regression-as-improvement, superlinear-exponent-vs-sublinear-claim mismatch). The anchor at 4.00 (i3KSorBQxF) had incremental novelty concerns — the current paper's novelty is substantially stronger. However, the numerical presentation issues here are more damaging than those of any anchor in the 4–5.25 range. The anchors in the 5.5+ range all have substantially cleaner quantitative claims.

**Final placement:** The conceptual novelty pushes this above a straight 3 (strong reject), but the numerical inconsistencies and mismatched claims pull it down from a 5 (low accept). The paper sits at the borderline: the core technical ideas are solid and interesting, but the presentation of quantitative results is too problematic for acceptance as-is. A revised version with clean, internally consistent numbers and a corrected "first sublinear regret" claim could be a strong paper.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>