## Summary

This paper studies sparse recovery under mixed-quality data, where some samples have low noise (high-quality) and others have higher noise (low-quality). It establishes sufficient conditions for information-theoretic support recovery in both agnostic (unknown noise variances) and informed (known variances) settings, quantifying the trade-off between high- and low-quality samples via the “Price of Quality.” On the algorithmic side, it extends LASSO recovery guarantees to the heterogeneous-noise agnostic setting, showing the threshold depends only on total sample size and average noise level, not on the individual noise levels — revealing a fundamental difference in how information-theoretic and algorithmic thresholds adapt to data heterogeneity.

## Strengths

- **Novel and timely problem.** Mixing high-quality and low-quality data (e.g., human labels combined with LLM/weak labels) is of growing practical importance. This paper is the first to formalize this setting in the context of sparse recovery with rigorous theoretical guarantees.
- **Conceptually clean quantity: Price of Quality.** The paper introduces an intuitive measure — how many low-quality samples are needed to replace one high-quality sample under a sufficient condition — and characterizes it in both agnostic and informed settings. The result that the price is at most 2 in the agnostic setting and can be arbitrarily large in the informed setting is insightful and actionable.
- **Technically sound extension of LASSO threshold.** Theorem 3 generalizes Wainwright’s classic LASSO phase transition to heterogeneous noise in the agnostic setting, using a QR-decomposition and Haar-measure arguments to handle the non-scalar noise covariance. The finding that the LASSO threshold depends only on total sample size and average noise is striking and demonstrates robustness of algorithmic recovery.
- **Well-structured exposition.** The paper clearly separates information-theoretic and algorithmic analyses, distinguishes agnostic vs. informed settings, and acknowledges limitations (sufficient not tight conditions, lack of informed LASSO result) without overclaiming.

## Weaknesses

### Fatal

None.

### Major

1.  **Price of Quality rests on a sufficient condition that is not tight.** The information-theoretic sufficient condition (9) is acknowledged to be potentially loose (Remark 3.2), but the paper’s central conceptual contribution — the boundedness of the Price of Quality and the “at most 2” conclusion — is derived directly from this condition. The actual information-theoretic threshold might have a very different trade-off. Without necessity results or matching lower bounds, the quantitative claims about the Price of Quality (e.g., “never worth more than two low-quality samples”) should be interpreted cautiously as properties of the sufficient condition, not of the fundamental limit.

2.  **No algorithmic result for the informed setting.** The paper compares information-theoretic thresholds in agnostic vs. informed settings, but the algorithmic analysis is only for the agnostic case (Remark 4.2 discusses why the proof does not easily extend). This makes the claimed “fundamental difference between how the information-theoretic and algorithmic thresholds adapt to data quality” less clean — one cannot compare the algorithmic thresholds across agnostic/informed because the informed algorithmic threshold is absent. The informed LASSO remains an open problem, which limits completeness.

3.  **Dependence on the free parameter  δ .** The Price of Quality expressions (12, 18) depend on the error tolerance  δ , which is a free parameter. The paper does not discuss how  δ  should be chosen or how the Price of Quality varies with  δ . For different  δ , the price could change, making the conclusions less robust.

### Minor

1.  **The binary-signal assumption for information-theoretic results** ( β^* ∈ {0,1}^p ) is standard but restrictive. The justification in Remark 3.1 that detecting a signal in  C_{p,s}(1)  reduces to the binary case is not fully detailed — scaling by  ρ  would also scale the noise variances, so the reduction is not immediate. This does not invalidate the results, but the interpretation as applying to all signals with lower-bounded entries needs more nuance.

2.  **The Price of Quality interpretation** as “one high-quality sample is worth  γ  low-quality samples” assumes the sufficient condition (9) is linear and the trade-off is exact at the boundary. Since the condition is only sufficient and derived via relaxation, this interpretation may be quantitatively imprecise. The paper could be more careful in distinguishing properties of the analysis from properties of the true threshold.

### Trivial

- The “extension to arbitrary noise structures” Remark 3.4 claims the agnostic condition extends to (22) with  σ_max(Σ)^4  in the denominator. This expression seems dimensionally inconsistent (a variance squared in the denominator of a log argument) and should be verified; however, since this is a minor point and the appendix is omitted, it does not affect the core review.

## Nice-to-Haves

- Simulations illustrating the phase transitions and the Price of Quality would strengthen the paper and help validate the theoretical predictions in finite samples.
- A discussion on how practitioners could estimate the per-sample noise variances in the informed setting (or at least a reference to relevant methods) would enhance practical impact.

## Novel Insights

The paper reveals an unexpected asymmetry: at the information-theoretic level, knowing which samples are high- vs. low-quality dramatically changes the value of data (Price of Quality unbounded), while at the algorithmic level (agnostic LASSO), the threshold is completely insensitive to heterogeneity and depends only on total sample size and average noise. This suggests that the computational constraints “flatten” the quality information that is otherwise crucial for optimal decoding. The contrast between the two thresholds and how they each react to heterogeneity is the paper’s most novel conceptual contribution.

## Suggestions

- Clearly restate that the “Price of Quality” conclusions (boundedness, at most 2) are derived from a *sufficient* condition and may not hold for the true information-theoretic threshold. Consider adding a sentence explicitly noting this caveat in the abstract or introduction to avoid potential misinterpretation.
- Consider adding a simple numerical example or table showing how the Price of Quality behaves for concrete values of  σ_1^2, σ_2^2, s, δ  to give readers intuition.

## Score and Decision

The paper addresses a timely problem with rigorous theory, introduces a clean conceptual quantity, and extends classical LASSO results to a practically relevant heterogeneous-noise setting. The main weaknesses are that the core Price-of-Quality results are only for a sufficient condition (not tight) and the missing algorithmic result for the informed setting limits the comparison. These are not fatal but prevent the paper from being a strong accept. The work is clearly above the ICLR average in novelty and technical quality.

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>