Good, I've verified all key claims against the paper. Let me now produce the final consolidated review.

---

## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency for LLMs. It introduces a continuous (KL-based) measure of watermark strength (Def. 3.1), formalizes the trade-off as a Pareto optimization problem (Section 3.2), derives explicit trade-off curves for existing watermarking schemes, and proposes Algorithm 1 — a pseudorandom draft-token acceptance mechanism. Theorem 4.1 proves that, under the assumption of degenerate (deterministic) watermarks, Algorithm 1 simultaneously achieves maximal watermark strength and maximal sampling efficiency. Experiments with Gumbel-max and SynthID watermarks show improved detectability at fixed false-positive rates without sacrificing efficiency.

## Strengths

1. **Quantitative watermark-strength measure (Def. 3.1).** The paper replaces the binary all-or-nothing definition from Hu & Huang (2024) with a continuous KL-based measure. Theorem 3.1 connects this measure to the p-value decay rate of the UMP test, establishing sample-complexity implications. Theorem 3.2 bounds it by the entropy of the original distribution, with equality iff the watermark is degenerate. This reframing is principled and is a genuine step forward for analyzing the trade-off.

2. **Theorem 4.1 — theoretical guarantee for pseudorandom acceptance.** The paper proves that Algorithm 1 simultaneously achieves unbiasedness (a), maximal sampling efficiency 1−TV(Q,P) (b), and maximal watermark strength Ent(P) (c) when the watermark decoder is degenerate. Within this regime, the result cleanly breaks the prior impossibility result by Hu & Huang (2024) by identifying their binary definition of watermark strength, rather than a fundamental barrier, as the limiting factor.

3. **Empirical improvement in detectability (Figure 2).** Both Ars-τ (for Gumbel-max) and Bayes-MLP (for SynthID) achieve higher TPR@FPR=1% with fewer tokens than the prior-based baselines, while the left panel confirms that AATPS (efficiency) is preserved. The gap to the oracle detector is relatively small, providing concrete evidence that the pseudorandom acceptance signal (ζ^R) can be exploited in practice.

4. **Explicit Pareto-curve derivation (Section 3.2, Figure 1).** The paper formulates the trade-off as a constrained convex optimization problem (Eq. 10) and derives explicit curves for linearly watermarked classes, Hu's class, and Google's class. Figure 1 provides a visualization that was absent from prior work, showing that Google's class outperforms Hu's class at matched efficiency and that neither reaches the theoretical optimum.

## Weaknesses

### Fatal
None.

### Major

1. **Scope gap between Theorem 4.1 and the experimental setting.** Theorem 4.1's guarantee of simultaneous maximal watermark strength and maximal sampling efficiency depends critically on the assumption that the watermark decoder 𝒮 is **degenerate** (point-mass output per ζ). Gumbel-max qualifies, but SynthID with the practically used m=30 is *not* degenerate — the paper's own line 172 states its strength drops below the maximum, and this is consistent with Theorem 3.3. The experiments (Section 5) operate in this non-degenerate regime yet are presented as validating the theory. While the conclusion (line 275) acknowledges this as an open direction, the abstract and contributions (lines 28-31) do not clearly delimit the scope, creating a mismatch between the strongest claim in the paper and what the experiments actually demonstrate. The paper would be stronger if it either: (a) restricted its high-level claims to the degenerate regime, or (b) provided theoretical analysis or empirical evidence explicitly addressing the non-degenerate case.

### Minor

2. **Limited experimental scope.** Experiments use only two model pairs (Llama-68M/7B and Gemma-2B/7B) and two datasets (ELI5 and C4), with one of each deferred to the appendix. Temperatures are set low (0.5 for Gumbel-max, 0.7 for SynthID) "to make the results more pronounced," which suggests the advantage may shrink at standard temperatures (~1.0). The paper does not explore this, weakening the claim about "practical deployment."

3. **Baseline comparison is informative but incomplete.** Ars-τ (with ζ^R) is compared against Ars-Prior (without ζ^R), and Bayes-MLP against Bayes-Prior. This is a clean ablation of ζ^R's benefit, which is the paper's contribution. However, the paper never provides an end-to-end comparison against the original full algorithms from Hu & Huang (2024) and Dathathri et al. (2024) under their original formulations. Such a comparison would strengthen the claim of practical superiority over prior systems, not just over stripped-down detectors.

4. **Independence assumption not addressed in practice.** Theorem 4.1 assumes ζ^D, ζ^T, and ζ^R are independent. In implementation, all three are derived from the same random seed, and the paper does not discuss how independence is ensured or whether violations affect the guarantees.

5. **Trade-off curves and Algorithm 1 are not fully integrated.** The Pareto curves in Figure 1 are computed under standard (random) acceptance mechanisms, while Algorithm 1 uses pseudorandom acceptance — a fundamentally different mechanism that the Section 3 formalization does not constrain. The paper does not verify that Algorithm 1 achieves a point beyond these specific frontiers or characterize the gap, making the two sections feel somewhat disconnected despite the narrative suggesting they form a unified story.

### Trivial

- The paper defines watermark strength WS (Def. 3.1) as a quantitative measure but never reports measured WS values in the experiments, only TPR@FPR=1%. Reporting WS would directly connect the theoretical framework to the empirical results.

## Nice-to-Haves

- Experiments at standard temperature (~1.0) to demonstrate generalizability.
- Reporting measured WS (Eq. 7) alongside TPR in the experiments.
- Explicit discussion of how independence of ζ^D, ζ^T, ζ^R is ensured in practice.

## Removed Points

*These points were raised in the reviews but removed after verification against the paper; they are listed here for completeness but should be treated with caution.*

- **"Baseline comparison is staged to inflate gains"**: The harsh critic characterized the Ars-τ vs Ars-Prior comparison as unfair because Ars-τ has access to ζ^R. However, ζ^R is precisely the paper's contribution; comparing a detector *with* ζ^R against one *without* it is a clean and appropriate ablation. The critic's suggestion to compare against prior systems that also have ζ^R is impossible by definition. The point is retained in softened form as Weakness #3 above (desire for additional end-to-end comparisons), but the "staged/inflated" characterization is removed as inaccurate.

- **"Theorems 3.1 and 3.2 are shallow / basic information-theoretic facts"**: This is a subjective judgment about novelty depth, not an actionable weakness. The theorems are correctly stated and appropriately applied within the paper's framing.

- **"Proof is in the appendix" / "construction deferred to the appendix"**: Several criticisms pointed to content deferred to the appendix. Per the hard rules, appendices were stripped by the parser and exist in the original submission.

- **Missing related works**: Not raised by reviewers; included here as a rule reminder.

## Novel Insights

The key insight that emerges from synthesizing the reviews is that the paper's architecture — separating the theoretical achievement (simultaneous maximal WS and SE for degenerate decoders) from the empirical validation (improved detection for non-degenerate SynthID m=30) — creates a subtle but important scope mismatch. The paper implicitly relies on readers accepting two independent claims: (1) Algorithm 1 is theoretically optimal in the degenerate regime, and (2) it improves detection in practice even outside that regime. These are both interesting, but the paper does not foreground the boundary between them, and the abstract's phrasing ("ensuring maximal watermark strength while maintaining speculative sampling efficiency") reads as applying to the experimental setting when Theorem 4.1's guarantee does not directly cover it. The paper would benefit from explicitly stating this as a two-part contribution with different scopes.

## Suggestions

1. In the abstract and contributions, explicitly note that Theorem 4.1's guarantee of *maximal* watermark strength applies to degenerate watermarks (Gumbel-max; SynthID only in the m→∞ limit), while SynthID with finite m achieves improved but not maximal strength.
2. Add an end-to-end comparison against the original algorithms from Hu & Huang (2024) and Dathathri et al. (2024) to show overall system-level superiority, not just the benefit of ζ^R.
3. Report measured WS values (Eq. 7) alongside TPR to bridge theory and experiments.
4. Add experiments at temperature ~1.0 to demonstrate that the advantage is not limited to low-temperature settings.
5. Discuss how independence of ζ^D, ζ^T, ζ^R is ensured from a single random seed in practice.

## Score and Decision

**Score rationale:** The paper makes genuine contributions — a principled quantitative measure of watermark strength, a clean theoretical result (Theorem 4.1), a clever algorithmic idea, and positive empirical evidence. No fatal flaws exist: the theory is sound within its stated assumptions, and the experiments show real improvement. However, the scope gap between the strongest theoretical claim and the experimental regime, the limited experimental breadth (2 model pairs, 2 datasets, low temperatures only), and the lack of end-to-end comparison against prior full algorithms prevent this from being a strong accept. The paper is solidly in the borderline-to-accept range: the contributions are real and the idea is interesting, but the paper's presentation overreaches slightly and the empirical support is thinner than would be ideal. A score of 6.5 reflects a paper that makes a meaningful contribution with room for improvement in scope precision and empirical coverage.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>