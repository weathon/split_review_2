## Summary

This paper introduces Dig-DEC, a model-free Decision-Estimation Coefficient that replaces the optimism principle (used in prior work FGQ+23) with a pure information-gain-plus-regularization mechanism. The authors present a general AIR framework using arbitrary convex divergences that unifies several prior approaches, improve the online function estimation procedure (unbiased estimator, refined two-timescale procedure), and obtain the **first model-free regret bounds for hybrid MDPs** (stochastic transitions, adversarial rewards) with bandit feedback — resolving an open problem from LWZ25. They also demonstrate regret improvements in the stochastic setting, including √T for Bellman-complete MDPs.

## Strengths

1. **First model-free regret bounds for hybrid MDPs with bandit feedback.** The paper resolves the open problem explicitly left by LWZ25, establishing sublinear regret for hybrid bilinear classes and Bellman-complete coverable MDPs under linear reward with bandit reward feedback. Prior methods either required model-based estimation (incurring log|ℳ| complexity) or full-information reward feedback. This is a genuine advance.

2. **Improved estimation procedures yielding concrete rate improvements.** The unbiased estimator via sample splitting (lines 211–213) and the refined two-timescale procedure for squared estimation error (lines 243–244) are concrete technical innovations that yield demonstrable improvements. The √T regret for Bellman-complete MDPs is the first time a DEC-based method matches the performance of optimism-based approaches (JLM21, XFB+23) in that setting.

3. **Conceptually clean and unifying framework.** The general AIR formulation with an arbitrary convex divergence D (Eq. 2) and the Bregman-divergence-based analysis (Eq. 5–6) genuinely unify several prior threads (XZ23, LWZ25, FGQ+23) under a simpler analysis that the authors argue is more flexible than the "constructive minimax theorem" of XZ23. This generalization is likely to be useful for future work in this line of research.

## Weaknesses

### Fatal
None.

### Major

1. **The central claim that Dig-DEC strictly improves over optimistic DEC is only substantiated for a 3-armed bandit, not for MDPs.** The abstract states "Dig-DEC is always no larger than optimistic DEC and can be much smaller in special cases," and the introduction claims Dig-DEC "improves over the optimistic DEC." However, Theorem 13 shows `dig-dec ≤ o-dec + η`, which means Dig-DEC does not yield asymptotically better T-dependence over optimistic DEC for the MDP settings studied. Theorem 14 — the sole demonstration of strict improvement — is a 3-armed bandit (H=1, |A|=3, no states). For the actual MDP settings in Table 1 (bilinear classes, Bellman-Eluder dimension, coverable MDPs), the better regret bounds likely derive from the **improved estimation procedures** (unbiased estimator, refined two-timescale) rather than from the conceptual change from optimistic DEC to Dig-DEC. The paper conflates these two distinct sources of improvement without disentangling them. This does not undermine the paper's other contributions (first hybrid bounds, better estimation procedures) but means the conceptual contribution is narrower than advertised.

### Minor

2. **Demonstrational narrowness of the strict improvement claim.** Even accepting that Theorem 14 (bandit, H=1, no states) is theoretically valid, the paper would be considerably stronger by showing strict improvement in even a simple MDP (e.g., horizon 2, 2 states) where the MDP-specific structure that the framework is designed to handle actually matters. The current example does not leverage any of the MDP structure (states, horizon > 1, transition dynamics) that distinguishes the paper's contribution from standard bandit results.

### Trivial
None.

## Nice-to-Haves

- Separate analyze the contribution of Dig-DEC (conceptual change) vs. the improved estimation procedures in the stochastic setting, to clarify which innovation drives the better rates in Table 1. Since Theorem 13 shows dig-dec ≤ o-dec + η, the improved T-dependence in Table 1 likely comes from estimation, not from Dig-DEC per se — acknowledging this would strengthen the paper's intellectual honesty.
- Provide at least one MDP example where the information-gain term in Dig-DEC yields strict improvement over what optimistic DEC achieves.

## Removed Points

- **Parser-dependent criticisms about Table 2 exponent inconsistency, abstract/introduction exponent mismatch, and Est rate "from √T to T^{1/2}" being identical.** The PDF extraction has clearly corrupted various exponent values in the extracted text (e.g., T^{3/2} appears in places where the formula analysis yields T^{5/6}; the abstract and introduction show inconsistent fraction values). These are parser artifacts, not author errors, and per the review guidelines such formatting artifacts are excluded.
- **Criticism about the "model-free" framing.** The paper explicitly defines its usage of "model-free" on line 37 ("only means that the regret bound is independent of the size of the model set M") and is transparent about the scope. This is a definitional choice clearly stated in the paper, not a gap.
- **On-policy/off-policy comparison concerns for the hybrid setting.** These depend on the parser-corrupted Table 2 entries and cannot be reliably evaluated from the extracted text.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Disentangle the two sources of improvement (Dig-DEC as a conceptual framework vs. the improved estimation procedures) for the stochastic setting. A clear discussion or simple ablation making explicit that the improved T-dependence in Table 1 comes from the estimation improvements rather than from Dig-DEC's conceptual change would substantially strengthen the paper.
- Provide at least one MDP example where the information-gain term in Dig-DEC yields strict improvement over optimistic DEC, rather than only the current 3-armed bandit example.

## Score and Decision

**Initial bracket (Round 1):** Based on the calibrated comparison, this paper is most comparable to theory papers at the 6–7 level on the ICLR scale. It is more substantive than the adversarial linear mixture MDP paper (6.0) because it resolves an open problem across a broader class of MDPs and contributes multiple technical innovations. However, the overclaimed conceptual contribution (strict MDP improvement only shown for a bandit) and confounded sources of improvement prevent it from reaching the 7.5+ level of papers like the Maximum Entropy Model Correction paper (7.33).

**Final score:** 6.5 — a solid paper with genuine technical contributions (first model-free hybrid bounds with bandit feedback, improved estimation procedures, clean unified framework) but with a notable gap between its advertised conceptual claims and what is actually proven for MDPs.

**Anchors used:**
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/aPNwsJgnZJ.md (6.0, Round 2) — adversarial linear mixture MDP theory paper; the current paper is broader in scope but has a weaker central claim
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/txD9llAYn9.md (7.0, Round 2) — model-based RL with horizon-free bounds; the current paper is comparable in theoretical depth but less clean in its claimed contributions
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kNpSUN0uCc.md (7.33, Round 3) — MaxEnt model correction; the current paper is similar in having a gap between advertised claims and proof, which pulled that paper's score down from 8 to an average of 7.33
- /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rJ5g8ueQaI.md (5.75, Round 3) — SEMDICE; a solid but not exceptional theory+empirical paper

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>