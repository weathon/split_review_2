Here is the final consolidated review.

---

## Summary

The paper proposes ConciseHint, a framework that injects conciseness hints (either manually designed text or learned embeddings) **during** the reasoning process of large reasoning models (LRMs), rather than before it (as in prompting, SFT, or RL-based approaches). The hints are injected adaptively: the injection interval grows with the current reasoning length (Eq. 1), so easy queries receive more frequent hints than complex ones, and the injection position moves progressively from head to tail (Eq. 3) to balance accuracy and prefilling cost. Evaluated on Qwen3-1.7B/4B/8B and DeepSeek-R1-14B across GSM8K, AIME24, and GPQA-Diamond, ConciseHint reduces token usage by 10–49% when applied alone and achieves further reductions when stacked on top of existing methods like BeConcise, Prompt, Deer, and NoWait.

---

## Strengths

- **A genuinely orthogonal approach to an active problem.** ConciseHint intervenes during the reasoning process (between generation segments) rather than before reasoning begins (prompting, SFT, RL). This opens a new design axis, clearly distinguished in Figure 1 and the related work section. The paper's framing that prior work operates "before reasoning" while this operates "during reasoning" is accurate and well-supported.

- **The adaptive injection mechanism (Eq. 1) is well-motivated and empirically validated.** Table 3 cleanly demonstrates that a fixed short interval (64) catastrophically degrades AIME24 accuracy (67% → 45% on Qwen3-4B) while barely affecting GSM8K; the adaptive strategy recovers this loss. This is convincing evidence that naive application would fail and that the complexity-adaptive design is necessary.

- **Impressive compatibility with existing methods.** Table 1 consistently shows ConciseHint stacks on top of BeConcise, Prompt, Deer, and NoWait, yielding token reductions *beyond* what any baseline achieves alone. For example, on Qwen3-4B GSM8K, Ours(Prompt) achieves 839 tokens vs. Prompt's 1263 — a 34% further reduction. This is the strongest evidence that the method contributes something genuinely complementary rather than rediscovering an existing effect.

- **Clean and practical implementation.** The base method (ConciseHint) is training-free with a simple algorithmic description (Algorithm 1). The trained variant (ConciseHint-T) uses lightweight prompt-tuning-style embedding learning. This simplicity is a practical virtue.

---

## Weaknesses

### Major

- **Wall-clock time and latency are not measured.** The paper's central claim is efficiency, yet the only metric reported is token count. ConciseHint makes multiple API calls per query (one per injection interval), each sending the full accumulated context. Without latency measurements, it is unknown whether token savings translate to real speedups given the multi-call overhead. The paper references an appendix analysis of prefilling costs, but the main text of an efficiency paper should report wall-clock time or end-to-end latency. *(Note: the appendix was stripped by the parser; the analysis referenced there may exist, but the main-text gap remains.)*

### Minor

- **No variance or uncertainty reported despite multiple runs.** The paper runs GSM8K 5 times and other benchmarks 10 times, but reports only point estimates (no standard deviations, confidence intervals, or error bars). This is especially problematic for AIME24 (30 problems), where sampling variability is high — small accuracy differences (e.g., 64.67% vs. 67.00%) could be within noise. This is a low-cost fix (the data exists).

- **No empirical comparison against token-budget or length-control methods.** The paper cites Token-Budget-Aware Reasoning (Han et al., 2024) and related work but does not include such methods as baselines, nor explains why comparison is infeasible. Adding this or providing a justification would strengthen the evaluation.

- **The abstract's "will not undermine model performance" claim is overstated.** Table 1 shows cases with modest accuracy drops — e.g., DeepSeek-R1-14B on AIME24 (63.00% → 61.00%) and on GPQA-Diamond (56.06% → 54.65%). These are small but indicate a trade-off that should be acknowledged honestly rather than claimed away.

- **ConciseHint-T is only evaluated on the smallest model (Qwen3-1.7B).** Table 2 shows the trained-embedding variant solely on the 1.7B model. Evaluating it on larger models (Qwen3-8B or DeepSeek-R1-14B) would substantiate claims about generalization and scalability of the learned embeddings.

### Trivial

None.

---

## Nice-to-Haves

- A small ablation on hint text variants (e.g., "Be brief," "Keep it concise") to test robustness to phrasing.
- A deeper analysis of the transition-word statistics (Table 5) — the observation that the interval between transition words stays roughly constant while the count drops is interesting but underexplored.
- Training details for ConciseHint-T (dataset size, training steps, learning rate) — these are likely in the (stripped) appendix but worth reiterating.

---

## Removed Points

The following points from the input review were removed:

- **"During generation" framing as overstated.** The paper transparently describes the mechanism (Algorithm 1: generate τ_k tokens, stop, inject hint, continue). Calling this "in-reasoning intervention" or "during generation" is accurate — the reasoning process spans the entire multi-segment generation. The framing is not misleading.
- **Figure 1 teaser discrepancy.** Teaser figures commonly use illustrative numbers; the actual experimental numbers are reported in Table 1. This is standard practice.
- **Circularity concern about complexity-adaptive mechanism.** The concern that successful compression could fool the adaptive mechanism is speculative and not supported by the empirical evidence, which shows the method works correctly across benchmarks.
- **Training details underspecified.** Standard prompt-tuning details are likely in the (stripped) appendix. This is a parser artifact, not an author omission.
- **Pure formatting/style nitpicks.** These are parser artifacts, not author errors.

---

## Novel Insights

None beyond the paper's own contributions. The review confirms that the core insight — repeatedly injecting conciseness cues during the reasoning process via adaptive prompt editing — is genuinely novel and orthogonal to existing methods.

---

## Suggestions

1. **Add wall-clock time or end-to-end latency measurements** to the main results. Even a simple average-time-per-query measurement would resolve whether token savings translate to real speedups given multi-call overhead.
2. **Report standard deviations or confidence intervals** for both accuracy and token usage, especially for AIME24 (30 problems, high variance).
3. **Extend ConciseHint-T evaluation** to at least one larger model (e.g., Qwen3-8B) to substantiate the scalability claim.
4. **Qualify the "will not undermine" claim** to acknowledge the small observed accuracy drops (e.g., DeepSeek-R1-14B on AIME24 and GPQA-Diamond).
5. **Include token-budget methods** as baselines, or explain why comparison is infeasible.

---

## Score and Decision

This is a solid paper with a genuinely novel contribution, well-supported by clean ablations and consistent results across models and benchmarks. The weaknesses are real but all fixable without changing the core claims: the missing latency data is the most substantive gap, and the absence of variance reporting is the most impactful methodological oversight. Neither undermines the validity of the core contribution — orthogonal in-reasoning intervention validated by strong empirical evidence.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>