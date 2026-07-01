Based on my calibration analysis, let me finalize the review.

The paper's theoretical contribution is genuine and the core idea is insightful. The main calibration anchors are:
- "Watermarking using Semantic-aware Speculative Sampling" (6.0, rejected) — similar topic but had proof errors and missing baselines; our paper is stronger in both theory quality and experimental execution.
- "Black-Box Detection of Language Model Watermarks" (7.0, accepted) — practical contribution, accepted; our paper has a stronger theoretical component but narrower experimental scope.
- "Can Watermarked LLMs be Identified by Users via Crafted Prompts?" (7.5, accepted) — well-received empirical paper; our paper trades some experimental breadth for theory depth.
- "A Watermark for Black-Box Language Models" (4.6, rejected) — weaker contribution and execution.

Round 1 bracket: **6.5–8.0**. The paper is clearly above the 4.6 (weak watermark paper) and 6.0 (flawed theory paper) anchors, and broadly comparable to the 7.0–7.5 accepted watermark papers.

Final score: **7.0**, Decision: **Accept**.

---

## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a continuous (KL divergence-based) measure of watermark strength, formulates the trade-off as a Pareto optimization problem, and proposes a mechanism — pseudorandom draft-token acceptance — that theoretically achieves both maximal watermark strength and maximal sampling efficiency for degenerate decoders. Experiments on Gumbel-max and SynthID watermarks show improved detectability at matching efficiency.

## Strengths

1. **Genuinely insightful core idea (Section 4.1, Algorithm 1).** The observation that the residual randomness of standard speculative acceptance (the random coin flip) is what weakens watermark strength, and that making acceptance pseudorandom removes this weak link, is both simple and non-obvious. It is the kind of idea that seems obvious only in retrospect. The proof in Theorem 4.1 that this construction simultaneously achieves unbiasedness, maximal sampling efficiency, and maximal watermark strength (for degenerate decoders) is clean and appears sound.

2. **Clear advance over the binary framework of Hu & Huang (2024).** The paper correctly identifies that prior work's binary definition of watermark strength (preserved vs. not preserved) was a limiting lens, and that moving to a continuous measure (Definition 3.1) is necessary to analyze the trade-off properly. The specific choice — expected KL divergence between watermarked and original distributions — is well-motivated by the connection to p-value decay rates (Theorem 3.1) and has a clean information-theoretic interpretation as mutual information I(w;ζ) under unbiasedness.

3. **Pareto frontier formulation (Definition 3.2) provides a principled language for the trade-off.** Framing the problem as maximizing watermark strength subject to an efficiency constraint is a natural and useful formalism. Lemma 3.1 (speculative sampler is optimal for any fixed P_ζ) is a helpful simplification that connects the abstract optimization to known mechanisms.

## Weaknesses

### Major

- **Theory-experiment gap for SynthID (m=30).** Theorem 4.1(c) proves maximal watermark strength under the assumption that the decoder S is degenerate (i.e., "achieves the largest watermark strength, hence it is degenerate by Thm. 3.2"). Gumbel-max satisfies this condition. SynthID only satisfies it in the m→∞ limit. The experiments (Section 5) explicitly use SynthID with m=30, which the paper itself acknowledges is not degenerate (Figure 1 caption: "when we set m=30 — a practical choice for SynthID — the watermark strength drops below that of Gumbel-max...maximal watermark strength is attained only in the limit m→∞"). This means the headline theoretical guarantee of Theorem 4.1(c) does not apply to the SynthID experimental setting. The improvement shown for SynthID is in detectability (via the ζ^R variable and Bayes-MLP), which is a real practical contribution, but the abstract's claim — "ensuring maximal watermark strength while maintaining speculative sampling efficiency" — is stated without the necessary qualification that it applies only when the decoder is degenerate. The paper should more clearly separate which claims are proven theoretically (and for which watermark schemes) and which are demonstrated empirically, and for what settings each applies.

### Minor

- **Theorem 3.1 regularity conditions not verified for the specific schemes.** Theorem 3.1 assumes the log-likelihood ratios Z_t are "independent, uniformly bounded, and admit a common neighborhood around zero where their moment generating functions are finite." These are nontrivial conditions, and the paper does not discuss whether Gumbel-max and SynthID satisfy them. This leaves a gap between the general theory and its application to the two watermarking schemes analyzed throughout.

- **Limited experimental scope.** Experiments use only two model pairs (both with small draft models), one dataset in the main text (EL15; C4 deferred to appendix), and lower temperatures (0.5 for Gumbel-max, 0.7 for SynthID) that make results "more pronounced." The paper does not discuss behavior at higher temperatures (more common in open-ended generation) or how results vary across different levels of Q-P similarity. An explicit statistical test comparing TPR between methods at specific token lengths would strengthen the detection claims beyond the ROC curves with confidence intervals.

- **Detection methods require calibration/training data.** Ars-τ requires grid-searching τ on a held-out validation set, and Bayes-MLP trains on 1,000 examples. The paper does not discuss sensitivity to validation set size or performance when training data is scarce, which is a realistic deployment concern.

### Trivial

None.

## Nice-to-Haves

- **Ablation to isolate detection improvement from extra information.** Training Ars-Prior on data from Alg. 1 but withholding u_t would help quantify how much of the improvement comes from the availability of u_t for detection versus from the mechanism itself.
- **Efficiency comparison against prior watermark+speculative sampling methods** (e.g., from Hu & Huang, 2024) to quantify how much efficiency prior approaches sacrificed.
- **Analysis across different levels of Q-P similarity** (draft and target models very close vs. very far apart).
- **Discussion of practical deployment considerations** for pseudorandom acceptance (e.g., synchronization of ζ^R between watermarking server and detector).

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"No efficiency comparison against prior watermark+speculative sampling"** — REMOVED. The paper's claim is that Alg. 1 achieves the theoretical maximum SSE (1-TV(Q,P)), which equals unwatermarked speculative sampling. Comparing against unwatermarked sampling is the correct baseline for this claim. Showing that prior methods sacrificed efficiency would be a nice addition but is not required to substantiate the claim as stated.
- **"Fully characterize claim is overstated"** — REMOVED. The abstract says "we fully characterize the trade-off as a constrained optimization problem," which refers to the general formulation (Definition 3.2), not a complete analytical solution. The paper also derives explicit Pareto curves for specific classes. This characterization is accurate.
- **"Detection improvement is structurally unsurprising"** — DEMOTED to Nice-to-Have. The paper explicitly acknowledges that ζ^R provides extra information (Section 4.2: "the extra information encoded in ζ^R reduces uncertainty about the token generation process and can therefore improve detectability"). The mechanism's contribution is making this information available; the paper does not claim the improvement is surprising.
- **Section-by-section notes on presentation density** — REMOVED. Subjective presentation preferences.
- **Non-convexity of feasible set** — REMOVED. The paper explicitly acknowledges this limitation (Section 3.2: "entropy is concave, so the feasible set is not convex in general").

## Novel Insights

The key insight — that the random coin flip in standard speculative acceptance is the specific mechanism preventing maximal watermark strength, and that replacing it with a pseudorandom decision restores determinism and thus maximal strength — is elegantly simple and non-obvious. The connection between watermark strength (as mutual information I(w;ζ)) and the Pareto frontier with sampling efficiency provides a unified language for thinking about the trade-off. The reframing of existing watermark+speculative sampling approaches as specific points on this Pareto surface is a useful conceptual contribution.

## Suggestions

1. Explicitly qualify the abstract's "maximal watermark strength" claim to note it applies to degenerate decoders (Gumbel-max, SynthID with m→∞), and separately state the SynthID (m=30) finding as improved detectability.
2. Verify (or at minimum discuss) whether the regularity conditions of Theorem 3.1 hold for Gumbel-max and SynthID.
3. Add explicit statistical significance tests for the detection comparisons.
4. Broaden experimental scope to include higher temperatures and more diverse Q-P similarity levels.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>