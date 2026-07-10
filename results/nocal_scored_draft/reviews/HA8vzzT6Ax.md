## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a continuous watermark strength measure (expected KL divergence) that governs statistical detectability (Theorem 3.1) and is maximized when tokens are deterministic functions of pseudorandom numbers (Theorem 3.2). Using this measure, the paper formalizes the trade-off as a Pareto optimization problem (Definition 3.2). The key algorithmic contribution (Alg. 1) injects pseudorandomness into draft-token acceptance, achieving maximal watermark strength while preserving speculative sampling efficiency (Theorem 4.1). Experiments on Gumbel-max and SynthID watermarks with Llama/Gemma model pairs show improved detectability at maintained efficiency.

---

## Strengths

- **The continuous watermark strength measure (Def. 3.1, expected KL divergence) is well-motivated and connects cleanly to statistical theory.** Theorem 3.1 shows the average KL divergence governs the p-value decay rate of the UMP test, giving this measure genuine operational meaning. The connection to mutual information under unbiasedness further anchors it information-theoretically. This is a clear improvement over the binary notion in prior work, which could not distinguish between schemes with different levels of pseudorandom coupling.

- **The algorithmic insight — making rejection/acceptance pseudorandom — is genuinely clever.** The fact that this can be done while preserving unbiasedness and maximal SSE (Theorem 4.1) is a non-trivial result. The proof structure connecting degenerate decoders → maximal WS → deterministic acceptance is logically tight.

- **The trade-off curve formulation (Def. 3.2, Eq. 8) is general and reusable.** By framing the problem as optimizing WS subject to SSE constraints, and showing the speculative sampler is optimal among all kernels realizing a given P_ζ (Lemma 3.1), the paper provides a template applicable to future watermarking schemes beyond Gumbel-max and SynthID. This is a genuine structural contribution.

---

## Weaknesses

### Fatal
None.

### Major

- **Experiments conflate improvements from the generation method with improvements from the detection method.** The comparison is (Alg. 1 + Ars-T/Bayes-MLP) vs. (prior approach + Ars-Prior/Bayes-Prior), which differ on *both* the generation side and the detection side simultaneously. Ars-T uses the pseudorandom acceptance variable u_t = G(ζ^R_t) as a selector (Eq. 11), which is only available under Alg. 1. Ars-Prior uses an estimated acceptance rate (Eq. 12). Without an ablation that isolates whether the improved detectability comes from (a) the changed generation process making the watermark signal fundamentally stronger, (b) the detector having access to a cleaner selection signal (u_t), or (c) both, the source of the gain is ambiguous. This does not invalidate the theoretical results, but it weakens the empirical attribution in Section 5.

### Minor

- **The "breaking the trade-off" framing (abstract, Section 4.1) slightly overstates what is achieved.** Hu & Huang (2024) defined watermark strength in binary terms; the paper replaces this with a continuous measure (Def. 3.1) and shows maximal WS is achievable under that measure. Under the prior binary definition, Alg. 1 does *not* preserve the watermarked distribution exactly. The paper acknowledges the definitional change in Section 2 but does not connect it back to the "breaking" narrative (e.g., in the abstract), so a reader could infer the original impossibility result is contradicted when in fact a different quantity is being optimized. The abstract should more precisely state: *under a continuous measure of watermark strength, the trade-off can be circumvented, whereas under the prior binary definition it remains.*

- **Theorem 4.1 assumes the decoder is degenerate (achieves maximal WS), but the SynthID experiments use m=30 which is not degenerate.** The paper acknowledges in Section 3.2 that m=30 yields WS below the maximum, yet Section 5 does not explicitly note that Theorem 4.1's guarantees do not apply to these experiments. The SynthID results are encouraging but empirical only, without theoretical backing for this setting.

- **Lower temperatures (0.5 for Gumbel-max, 0.7 for SynthID) are used "to make the results more pronounced" (Section 5).** At temperature 1.0 (the default generation temperature), the effects may be smaller. The paper should include results at temperature 1.0 or justify why lower temperatures are the appropriate testbed.

- **No quantitative analysis of bonus-step frequency.** Footnote 3 claims "the sampling process rarely enters a bonus step" for K not very small, but provides no empirical validation. Reporting the fraction of steps resulting in bonus tokens across the K values tested would substantiate this claim.

### Trivial
None.

---

## Nice-to-Haves

- An ablation study disentangling generation and detection effects (e.g., applying standard truly-random acceptance with the Ars-T detector, or applying the MLP detector to the prior generation method).
- Discussion of how the pseudorandom components (ζ^D, ζ^T, ζ^R) are seeded and synchronized between generation and detection in deployment.
- Temperature 1.0 results.

---

## Removed Points

These points are flagged to be removed, treat them with caution:
- "Section 2 description of Eq. (6) is dense" — presentation nitpick; does not affect validity.
- "Theorem 3.1's practical relevance is limited" — the paper's Remark 3.1 already addresses the gap between WS governing ideal detection and practical detection.
- "Linearly watermarked classes' practical relevance unclear; Figure 1 lacks error bars" — Figure 1 is a theoretical illustration, and the critic acknowledges it is acceptable for that purpose.
- "Per Token Time and Log Perplexity should be in main text" — these are standard in the appendix; presentation preference.
- "Oracle gap analysis needed" — the paper already discusses this gap in Section 5.
- "Wall-clock time overhead of G(ζ^R) calls not discussed" — PTT is reported in appendix tables, partially addressing this.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Ablation study (highest priority):** Add an experiment that applies the Ars-T detector to outputs generated with standard (truly random) acceptance, or applies the MLP detector architecture to the prior generation method. This would directly address the major weakness by isolating whether the improvement comes from the generation method (Alg. 1) or the detection method.
2. **Explicit acknowledgment:** In Section 5, explicitly state that the SynthID (m=30) results are empirical and do not fall under Theorem 4.1's guarantees.
3. **Quantitative support:** Report the fraction of steps that result in bonus tokens for K ∈ {2,3,4} to validate the claim in footnote 3.
4. **Temperature sensitivity:** Include results at temperature 1.0, or provide a clear justification for why the chosen lower temperatures are the appropriate testbed.

---

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>