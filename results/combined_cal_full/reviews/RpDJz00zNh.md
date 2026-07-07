Now I have enough calibration data. Let me write the final review.

## Final Review

**Bracket from Round 1:** Based on the calibration anchors, the paper sits plausibly between 5.0 and 6.0. Rational Metareasoning (5.00, rejected) had severe concerns about incremental contribution (-9.27, -6.03) that ConciseHint does not share — ConciseHint's paradigm is genuinely novel. LazyLLM (5.00, rejected) suffered from missing baselines (-7.29). Hint Marginalization (5.75, rejected) had a -9.11 item questioning its scientific advance. ConciseHint's heaviest weaknesses (-3.75 for a selective claim, -1.88 for no CIs) are significantly milder. CoTFormer (5.75, accepted) and How Many Tokens (5.75, accepted) demonstrate that papers in this score band can be accepted with proper strengths.

**Narrowing rationale:** ConciseHint shares with the 5.0–5.75 anchors the pattern of "novel approach with evaluation gaps." But where those papers had fatal-level weight weaknesses (incremental contribution, missing baselines, insufficient novelty), ConciseHint's weaknesses are moderate and addressable. Its strongest positive weight (+5.04 for the adaptive interval mechanism) is higher than most strengths in the 5.0-range anchors. The paper is a clear borderline case leaning toward acceptance.

---

## Summary

This paper proposes ConciseHint, a framework that injects learnable hints (manually designed text or trained embeddings) *during* a reasoning model's token-by-token generation to encourage conciseness — an "in-reasoning intervention" paradigm distinct from prior work that operates before reasoning (prompting, SFT, RL). The method adaptively controls hint injection intensity based on reasoning length (shorter = easier queries receive stronger hints) and dynamically selects injection positions to balance accuracy and prefilling costs. Experiments on Qwen3 and DeepSeek-R1 models across GSM8K, AIME24, and GPQA-Diamond show token count reductions while maintaining accuracy.

## Strengths

1. **Genuinely novel paradigm.** The paper correctly identifies a gap: prior efficiency methods operate *before* reasoning (prompting at input, fine-tuning before inference). ConciseHint's idea of intervening *during* token-by-token generation is orthogonal and well-articulated in Section 1 and Figure 1. This is the paper's clearest contribution.

2. **Adaptive interval mechanism is well-motivated and ablation-validated.** Table 3 convincingly demonstrates that a fixed aggressive injection interval (64 tokens) destroys accuracy on AIME24 (Qwen3-4B drops from 67.00% to 45.33%) while barely affecting GSM8K. This empirically justifies the need for complexity-adaptive control, and the linear schedule τ_k = α + β·l_k is a simple, reasonable solution. The ablation is done on the right pair of datasets (high vs. low complexity).

3. **Practical simplicity.** The training-free version (ConciseHint with manually designed hints) requires no model modification and can be applied to any LRM via API. This is a meaningful practical advantage over SFT/RL-based methods.

## Weaknesses

### Major

- **Efficiency measured solely by output token count, which is incomplete for a method with iterative overhead.** Algorithm 1 reveals that ConciseHint operates via sequential API calls: generate τ_k tokens, inject hint, recompute prefix, repeat. Each cycle involves a new API call with the full accumulated context and KV-cache recomputation for text after the injection point. The paper's own position control (Equation 3) explicitly acknowledges prefilling costs — injecting earlier means more text must be reprocessed. Yet the main evaluation (Section 4.1) measures only "average token usage... to measure the efficiency," without reporting wall-clock time, latency, or FLOPs. While the paper defers cost analysis to Appendix A.2 (which exists in the original submission) and claims overhead is negligible, the main text would be substantially strengthened by including actual efficiency measurements. Token count is a standard metric in this literature, but for a method whose cost profile differs qualitatively from single-pass baselines, it is insufficient as the sole efficiency measure.

### Minor

- **The claim that ConciseHint alone is "comparable to strong baselines" is not uniformly supported.** Looking across Table 1: for Qwen3-8B on GSM8K, Ours(Ori) at 1489 tokens is *higher* than Prompt (1353), Deer (1223), and NoWait (1406). For DeepSeek-R1-14B on GSM8K, Ours(Ori) at 713 tokens is higher than Prompt (627). For Qwen3-8B on AIME24, Ours(Ori) at 11,228 tokens is the highest among all methods. The paper selects favorable examples (Qwen3-4B on GSM8K) and generalizes beyond what the data fully supports. The claim is best described as "sometimes better, sometimes comparable, sometimes worse."

- **No confidence intervals or standard deviations reported despite multiple runs.** Section 4.1 states experiments are run 5 times (GSM8K) or 10 times (AIME24, GPQA), but only means are reported. Many accuracy differences in Table 1 are very small (e.g., 94.81 vs. 94.74 vs. 94.60) — well within typical LLM variance at temperature 0.6. Given AIME24 has only 30 problems, a single-answer swing changes accuracy by ~3.3 points, so 1–2 point differences may be noise.

- **The trained variant ConciseHint-T is evaluated exclusively on the smallest model (Qwen3-1.7B, Table 2).** No evidence is provided that learned hint embeddings work on Qwen3-4B, Qwen3-8B, or DeepSeek-R1-14B. Since the training data (MixChain-Z-GSM8K) is domain-specific (GSM8K math), the scalability and generality of learned embeddings are unclear. The accuracy degradation at γ=1.0 (GSM8K: 90.87→88.01, GPQA: 39.39→35.05) is also non-trivial and under-discussed.

- **The exact text of the manually designed hint used in experiments is not precisely specified.** The paper only gives "make answer concise!" as an example ("injecting the hint like 'make answer concise!'"). This affects reproducibility, as the hint text likely influences effectiveness.

- **The framing of the plugin results (Ours(baseline)) is inflated.** Claim (ii) states ConciseHint "substantially raises the upper bound of efficiency" when combined with baselines. Since Ours(baseline) applies two length-reduction mechanisms simultaneously, additive token reduction is largely expected. The more informative result for standalone value is Ours(Ori) vs. baselines. Showing compatibility without accuracy collapse is useful, but the "substantial" framing overstates the significance.

### Trivial

None.

## Nice-to-Haves

- The paper could benefit from a limitations section acknowledging: (a) the iterative API calling pattern and its potential overhead; (b) that ConciseHint-T requires curated concise data and has only been validated on a 1.7B model; (c) the sensitivity of α and β hyperparameters (currently deferred to the appendix).
- The controllability via γ interpolation (Figure 3) is interesting but only shown on Qwen3-1.7B — showing it on a larger model would strengthen the claim.

## Removed Points

These points were considered and removed as they either misinterpret the paper, were addressed by the paper, or are speculative:

1. **"Complexity proxy circularity"** (from the harsh critic's section notes): The concern that using reasoning length as complexity proxy creates circularity is partially addressed by Table 3, which empirically validates the adaptive strategy over fixed intervals. This is a reasonable theoretical concern but the paper provides supporting ablation evidence, making it a discussion point rather than a weakness.
2. **"Hyperparameter sensitivity not in main text"**: The paper states α=128, β=0.2 "always work well" and defers sensitivity analysis to Appendix A.1 (which exists in the original submission). This is standard practice.
3. **"No limitations section"**: A nice-to-have, not a weakness.
4. **"Constants in Equation 3 not derived"**: The constants 1024 and 0.8 are engineering heuristics, which is acceptable for a methods paper of this type.
5. **"Missing related works"**: Removed per protocol — no external sources to confirm their existence.
6. **Related papers found by the human finder**: If the human finder surfaced papers that are not topically similar, they are not included here.
7. **Formatting/style nitpicks and typos**: Removed per protocol — these are parser artifacts, not author errors.

## Novel Insights

Beyond the paper's own contributions, the review surfaces a key tension: ConciseHint's core novelty is its *in-reasoning intervention* paradigm, but the evaluation validates it using metrics (token count, comparisons to single-pass baselines) that are inherited from the *before-reasoning* paradigm it seeks to supersede. A proper evaluation of in-reasoning methods would ideally measure end-to-end latency or cost, accounting for the iterative calling pattern. This gap does not invalidate the approach but means the paper's evidence for its central claim ("improved efficiency") is weaker than the evidence for its secondary claims (reduced token count, maintained accuracy). The adaptive interval ablation (Table 3) is the paper's strongest empirical contribution — it cleanly validates the design choice of complexity-adaptive control independently of the efficiency metric question.

## Suggestions

1. Add wall-clock time or latency measurements to the main evaluation (even on a subset of configurations) to demonstrate that token count reduction translates to real efficiency gains despite iterative API calls.
2. Add confidence intervals or standard deviations to Table 1, particularly for AIME24 where the small problem set creates high variance.
3. Evaluate ConciseHint-T on at least one larger model (Qwen3-8B or DeepSeek-R1-14B) to establish scalability of learned embeddings.
4. Provide the exact hint text used in experiments.
5. Tone down the framing of results where the data is mixed — acknowledge configurations where baselines outperform Ours(Ori).

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>