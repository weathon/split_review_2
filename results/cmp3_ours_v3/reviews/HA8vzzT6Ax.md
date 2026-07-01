Now let me write the final consolidated review.

## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency for LLMs. It introduces a quantitative measure of watermark strength (expected KL divergence) that moves beyond prior binary definitions, characterizes the trade-off as a Pareto frontier, and proposes a pseudorandom acceptance mechanism (Algorithm 1) that theoretically achieves maximal watermark strength while preserving sampling efficiency for degenerate watermarks. Experiments on Gumbel-max and SynthID watermarks demonstrate improved detectability at maintained efficiency.

## Strengths

- **A genuine theoretical advance over a binary impossibility result.** The paper correctly identifies that Hu & Huang (2024)'s binary definition of watermark strength precludes intermediate characterization. The proposed quantitative measure (Definition 3.1) — expected KL divergence between watermarked and original distributions — connects to statistical detectability via the p-value decay rate (Theorem 3.1) and has a clean upper bound in terms of the original distribution's entropy (Theorem 3.2). This shifts the problem from binary to continuous optimization, enabling a more nuanced analysis.

- **The pseudorandom acceptance mechanism (Algorithm 1) is conceptually clean and principled.** The insight that residual randomness in the acceptance coin flip is a source of watermark degradation is simple but advances the line of work. Theorem 4.1's guarantee of simultaneous maximum watermark strength and maximum sampling efficiency (under the degenerate watermark assumption) is a genuine advance over the prior state of knowledge.

- **Theorem 3.3 and the characterization of which schemes achieve maximal strength.** Showing that both Gumbel-max and SynthID (in the m→∞ limit) attain maximum watermark strength is informative, and the paper is honest about SynthID's finite-m degradation. The trade-off curves in Figure 1 usefully visualize the continuous landscape that was previously only described at two endpoints.

## Weaknesses

### Fatal
None.

### Major

- **Theorem 4.1's guarantee requires degenerate watermarks, which the practical SynthID experiments do not satisfy.** Theorem 4.1 requires the watermarked distribution to be degenerate (point masses, achieving Ent(P_ζ)=0 a.s., per Theorem 3.2), which holds for Gumbel-max and SynthID only in the m→∞ limit. The experiments use SynthID with m=30 (line 251), which the paper acknowledges does not achieve maximum strength (line 172: "the maximal watermark strength is attained only in the limit m → ∞"). The paper is transparent about this condition, but the overall narrative — the abstract's "we prove it achieves maximal watermark strength while preserving speculative sampling efficiency" and the title — implicitly suggests a unified theoretical treatment that the SynthID-m=30 experiments do not fully realize. The empirical improvements for SynthID are real but are heuristic extensions not formally explained by Theorem 4.1. This means the rigorous theoretical contribution is narrower than the framing suggests: it applies rigorously to Gumbel-max and SynthID-m→∞, while the practical experiments operate in a regime where the theoretical guarantees do not directly apply.

### Minor

- **Missing ablation isolates the mechanism's contribution for SynthID.** The Bayes-MLP detector is trained on (y_t^P, y_t^T, u_t) and compared against Bayes-Prior (a weighted average). The improvement could come from (a) the u_t signal from pseudorandom acceptance, (b) the increased capacity of an MLP over a weighted average, or (c) both. Without an ablation training an MLP on (y_t^P, y_t^T) *without* u_t, the specific contribution of pseudorandom acceptance to the SynthID gain is not identified. This matters because the paper's core claim is about the mechanism (pseudorandom acceptance), not about using MLPs for detection.

- **The proposed watermark strength metric (Eq. 7) is not measured experimentally.** The paper introduces a novel quantitative measure (expected KL divergence), proves it governs asymptotic detectability, and then evaluates TPR@FPR=1% instead. While Remark 3.1 and Section 4.2 acknowledge that strength and detectability differ, measuring the actual KL divergence would bridge theory and experiments — revealing how far the m=30 SynthID case operates from the theoretical maximum and whether the mechanism improves strength even when it does not achieve the maximum.

- **Experiments use lower temperatures without characterizing the temperature dependence.** The paper uses temperature 0.5 for Gumbel-max and 0.7 for SynthID, described only as "to make the results more pronounced" (line 259). No results at temperature 1.0 (the standard setting in most LLM inference) are reported in the main text. The paper should either provide temperature-1.0 results or explicitly delimit claims to lower-temperature regimes.

### Trivial
None.

## Nice-to-Haves

- The claim that the trade-off formulation "can be applied in a plug-and-play manner to any watermarking schemes" (line 29) is somewhat optimistic: the paper provides closed-form solutions only for specific decoder classes, and solving the optimization for arbitrary families may be nontrivial.

## Removed Points

- "Theory (KL) vs experiments (TPR) gap bridged by untested argument" — The paper explicitly acknowledges this gap in Remark 3.1 ("watermark strength is conceptually distinct from detection efficiency") and Section 4.2. The paper does not claim the theory predicts TPR magnitudes; it separately proves strength maximization and empirically demonstrates detectability improvement.
- "Hu & Huang baseline not compared" — Hu & Huang (2024) provide a theoretical impossibility result, not a specific watermarking method. The paper compares against the prior approaches that achieve the trade-off endpoints, which is appropriate.
- "TPR at a single FPR is restrictive" — The paper notes that ROC curves are provided in the appendix (Fig. 4 and 7), addressing this concern.
- "No statistical significance tests beyond confidence intervals" — Confidence intervals are reported; this aligns with common practice for this type of evaluation.
- "Bayes-MLP description is vague" — Implementation details are deferred to the appendix, which exists in the original submission.
- Framing criticism about "unites speculative sampling and watermarking" — Subjective phrasing preference.
- "SE maintained" and "WS maintained" points — These are baseline conditions, not missing comparisons.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include an ablation for the SynthID detector that trains an MLP on (y_t^P, y_t^T) without u_t, to isolate the contribution of pseudorandom acceptance.
2. Measure watermark strength (Eq. 7) directly in experiments to bridge the theory-experiment gap.
3. Provide results at temperature 1.0 or explicitly scope claims to low-temperature settings.
4. Clarify in the abstract and introduction that Theorem 4.1 applies strictly to degenerate (maximally strong) watermarks, while practical experiments include heuristic extensions.

## Calibration Anchors

All anchors retrieved from the human-review corpus:

| Anchor | Path | Avg Score | Round | Comparison with Reviewed Paper |
|--------|------|-----------|-------|-------------------------------|
| Watermarking using Semantic-aware Speculative Sampling | LdIlnsePNt | 6.00 (Reject) | R1 | Similar topic (watermark + speculative sampling); that paper had serious proof issues and missing error bars. Our paper is cleaner and more rigorous. |
| A Watermark for Black-Box Language Models | 0koPj0cJV6 | 4.60 (Reject) | R1 | Different topic (black-box watermark); lower quality. |
| I Know You Did Not Write That! | eKGEsFdpin | 3.67 (Reject) | R1 | Simple watermarking; less contribution. |
| Black-Box Detection of Language Model Watermarks | E4LAVLXAHW | 7.00 (Accept) | R1 | Strong empirical detection paper with thorough evaluation; our paper has stronger theory but weaker experimental coverage. |
| DistillSpec | rsY6J3ZaTF | 6.00 (Accept) | R2 | About speculative decoding + distillation, not watermarking. |
| Optimized Multi-Token Joint Decoding | ZHhBawo3k5 | 6.00 (Accept) | R2 | About speculative decoding, not watermarking. |

**Round-1 bracket:** 6.0–7.5. The SEAL paper at 6.0 (rejected) is a reasonable lower bound — our paper is more coherent and has no proof errors. The Black-Box Detection paper at 7.0 (accepted) is an upper bound — our paper has stronger theory but less experimental breadth. **Final score is calibrated between these anchors.**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>