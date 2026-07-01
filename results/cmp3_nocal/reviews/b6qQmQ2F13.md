Now let me write the final consolidated review.

## Summary

This paper presents an empirical study of memory-accuracy trade-offs for reasoning models (Qwen3 0.6B–32B, DeepSeek-R1-Distill, OpenReasoning-Nemotron) under the constraint that KV cache — not just weights — dominates memory. Through 1,700+ configurations spanning weight quantization (4/8/16-bit), token budgets (2k–30k), parallel scaling, and KV cache compression (eviction and quantization), it derives scale-dependent deployment principles. The core finding is that a model's effective size (parameters × bits per weight) determines whether memory is better spent on larger weights, longer generations, parallel samples, or KV cache compression.

## Strengths

1. **Timely and well-motivated problem.** The paper correctly identifies that prior memory-accuracy optimization literature was built on short-generation, non-reasoning models and that the dominance of KV cache memory in reasoning models invalidates those prescriptions. The motivating example (Qwen3-4B 4-bit: 2.49 GB weights vs. 4.42 GB KV cache at 32k tokens) is concrete and compelling.

2. **Systematic experimental coverage.** The study spans 1,700+ configurations across model size (0.6B–32B), weight precision (4/8/16-bit), token budgets (2k–30k), parallel scaling (group sizes up to 16), KV cache eviction, and KV cache quantization. The breadth alone is a useful reference for practitioners.

3. **Cross-family validation.** Central claims are tested on three model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron) across four benchmarks (AIME25, GPQA-Diamond, LiveCodeBench, MATH500), providing stronger generalization evidence than single-family studies.

4. **Task-dependent finding (Finding 2) is genuinely useful and non-obvious.** The discovery that knowledge tasks tolerate 4-bit weights while math/code require higher precision (8/16-bit) has direct practical implications and is supported by clear contrast across benchmarks (Figures 3 vs. 4).

## Weaknesses

### Fatal
None.

### Major
- **Internal inconsistency in Finding 5's threshold.** Finding 5 is stated as "effective size smaller than an **8-bit 4B** model" in the abstract and introduction (lines 41, 49), but as "effective size smaller than an **8-bit 8B** model" in the body text (line 211) and the formal Finding 5 box (line 221). The difference is a factor of 2× in effective size (~4.2 GB vs ~8.4 GB). This is a concrete error the authors must resolve — the paper currently contradicts itself on a headline numerical claim. It also raises the question of whether the two thresholds correspond to genuinely different transition points (for weight-vs-token allocation vs. eviction-vs-quantization) or whether one is simply a typo.

### Minor
- **No uncertainty quantification.** The paper reports accuracy values throughout but never provides standard deviations, confidence intervals, or error bars. With only 8 generations per instance in Section 5 and fine-grained comparative claims (e.g., "4-bit is broadly memory-optimal for knowledge tasks," "8-bit is memory-optimal for small models on AIME25"), the reader cannot assess whether observed gaps exceed measurement noise. While this is common in large-scale empirical studies, adding variance estimates — even bootstrapped confidence intervals on key pairwise comparisons — would substantially strengthen the evidential claims.

- **Threshold claims are more precise than the evidence supports.** The crisp "8-bit 4B" threshold is stated as a precise cutoff, but the available model sizes are 0.6B, 1.7B, 4B, 8B, 14B, 32B — the threshold falls between two adjacent configurations (4B/4-bit at ~2.5 GB and 4B/8-bit at ~4.2 GB). Framing this as a transitional region rather than a precise cutoff would better match the experimental granularity and avoid the appearance of false precision.

- **External verifier conclusion exceeds the evidence.** The paper concludes that "the external verifier is consistently memory-inefficient" (line 171) based on evaluating a single verifier (ActPRM-X, 7B, 13.28 GB). A smaller or distilled verifier could change the trade-off. The paper acknowledges this limitation in Section 7, but the main text claim is stated more broadly than the single-data-point experiment can support. The conclusion should be scoped to "large external verifiers" or downgraded to a preliminary observation.

### Trivial
None.

## Nice-to-Haves

- **Explicit guidance on how the scale-dependent and task-dependent axes interact.** The paper presents Findings 1–3 (scale-dependent) alongside Finding 2 (task-dependent) without discussing how they compose. For example: a small model on a math task — Finding 1 says prioritize weight capacity (consistent with Finding 2's "math needs higher precision"), but a large model on a knowledge task — Finding 1 says prioritize tokens while Finding 2 says 4-bit weights suffice. These are consistent, but the paper would benefit from explicitly stating how the guidance composes.

- **Note activation memory in the cost model.** The memory equation (line 71) excludes activation memory, which can be non-negligible for very long sequences. This is standard for inference-focused studies but worth noting for completeness.

## Removed Points

The following points from the source review were removed with justification:

- Criticisms about the Finding 1 discussion conflating "memory budget" and "effective size" — the paper's text at lines 111–113 uses the observable memory budget (~8 GB) to approximately ground the theoretical effective-size threshold (~4.2 GB). This is an explanatory bridge, not an inconsistency.
- Claims that the batching assumption should be discussed in the main text rather than Appendix C.3 — the paper flags the batched-inference assumption explicitly in the introduction (line 35) and references the appendix analysis. This is adequate disclosure.
- Speculation that the 8-bit 8B threshold might apply to Finding 1 or 3 — only Finding 5 has the inconsistency; Findings 1 and 3 use 8-bit 4B consistently throughout.
- Section-by-section presentation notes that are covered by the substantive weaknesses above or are not independently actionable.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface any finding that the paper itself does not already articulate.

## Suggestions

1. **Reconcile the Finding 5 threshold.** Decide whether the correct threshold is 8-bit 4B or 8-bit 8B, and ensure it is consistent across abstract, introduction, body discussion, and the formal Finding box. If the two thresholds (weight-vs-token vs. eviction-vs-quantization) are genuinely different, explain the mechanism.
2. **Add variance estimates** for at least the key pairwise comparisons (e.g., 4B 4-bit vs. 4B 8-bit on AIME25 at a given token budget). Bootstrapped confidence intervals on the Pareto frontier would be most informative.
3. **Replace crisp thresholds with transitional ranges** where appropriate (e.g., "models with effective size below approximately 4–5 GB, roughly equivalent to an 8-bit 4B model"), to match the granularity of the available model sizes.
4. **Scope the external verifier claim** to "large external verifiers" or downgrade it to a preliminary observation.

## Score and Decision

This is a solid and practically relevant empirical study. The core thesis — that memory-optimal deployment strategies for reasoning models depend on effective size and task type, and that received wisdom from non-reasoning models does not carry over — is well-motivated and supported by extensive experiments. The Finding 5 threshold inconsistency is a concrete error that must be fixed, and the precision of the threshold claims should be softened to match the experimental granularity. However, these issues are addressable and do not invalidate the central contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>