Now I have verified the pseudocode-text discrepancy. The critic's point about the algorithm mismatch is valid but the severity is overblown. Let me produce the final consolidated review.

## Summary

This paper formalizes critical KV cache identification for LLM inference from an output perturbation perspective. It derives an upper bound on attention output perturbation (Theorem 3.3) that jointly considers attention weights and projected value states (VW^O), going beyond prior attention-weight-only heuristics. It proposes a two-stage greedy selection algorithm (Algorithm 1) to minimize this upper bound, which integrates as a plug-and-play replacement for the selection step in SnapKV, AdaKV, and HeadKV. Experiments on 29 datasets across three LLMs (Llama-3.1-8B, Mistral-7B, Qwen2.5-32B) show consistent improvements, reducing compression loss by more than half on average.

## Strengths

- **Formal derivation of an output-perturbation upper bound (Theorem 3.3).** The bound θ = C − (2 − 1/∑𝒩ᵢAᵢ) ∑𝒩ᵢAᵢ‖𝐕ᵢ,∶‖₁ (where **V** = VW^O) reveals that both attention weights and value states projected through the pretrained output matrix W^O influence worst-case perturbation. This provides formal justification absent from prior heuristics that rely solely on accumulated attention scores. The derivation is correctly traced through Theorem 3.2's renormalization and the triangle inequality.

- **Consistent and substantial empirical gains across a large evaluation suite.** On Ruler (Table 1), integrating with HeadKV on Qwen2.5-32B reduces loss from 13.7% → 3.4% at 40% cache. On LongBench (Table 2), improvements appear in 88/90 test cases (97.8% success rate) across three models, three base methods, and two cache sizes. On SCBench multi-turn QA (Table 3), gains are especially pronounced at low budgets (e.g., EN.QA at 40%: 15.71 → 22.14). Results hold across three model families and parameter scales (8B–32B).

- **Empirical validation that the theoretical bound translates to real perturbation reduction (Section 4.7).** Head-wise analysis shows lower perturbation in 92% of Llama-3.1-8B attention heads; layer-wise analysis shows reduction accumulates across layers, reaching near-zero in the final layer; budget-wise analysis shows consistent reduction from 2.5% to 40% cache sizes.

- **Minimal computational overhead (Section 4.6).** Additional TTFT is only 0.06s (1.7%) at 32K context with batch size 1 (3.54 → 3.60s). Decoding latency is unchanged since selection happens during prefill. A 2.49× decoding speedup over full cache is preserved.

- **Systematic hyperparameter analysis confirming the practical necessity of the two-stage design (Section 4.5, Table 4).** On Mistral-7B, removing the attention-weight safeguard (α=0.0) causes a catastrophic drop from 42.85 → 31.94, while α=0.5 is stable. This validates that the two-stage design is empirically essential for certain models.

## Weaknesses

### Minor

- **Algorithm pseudocode notation is ambiguous (Algorithm 1, line 5 vs. 8).** The text (line 126) and Assumption 3.4 (line 170) both state that Stage 1 selects by attention weights and Stage 2 by the composite score. However, the pseudocode writes Stage 1 as "A_i ∈ Top_k(𝒜, b')" where 𝒜 is the composite score (attention × value norms). This notation is dimensionally confusing and conflicts with the text description. The theoretical analysis (Assumption 3.4 uses "Top_k(A, b')") confirms the intended Stage 1 uses attention weights A. This is a presentational fix — the intended algorithm is clear from the text and theory — but the pseudocode must be corrected to avoid ambiguity.

- **Single-query theory vs. multi-query practice gap.** The perturbation analysis in Section 3 considers a single known query state q at a single decoding step. In practice, cache eviction compresses the context once and serves many future queries whose attention patterns are unknown at compression time. The evaluation protocol (Section 4.1) correctly compresses "independently before the question is introduced," which is the standard realistic setting. However, the paper does not acknowledge that the theoretical framing (optimizing for a specific query) is narrower than the practical setting (optimizing over a distribution of future queries). The empirical results stand on their own, but the gap should be explicitly noted.

- **α=0.0 outperforms α=0.5 on Llama-3.1-8B (Table 4).** On Llama-3.1-8B at 20% cache, α=0.0 (pure composite-score selection, no attention-weight safeguard) achieves 44.35 vs α=0.5's 43.77. The paper's theoretical argument (Assumption 3.4) predicts α=0.0 should be suboptimal because it violates the cumulative-attention > 0.5 condition. While the Mistral failure case (31.94 vs 42.85) clearly demonstrates the safeguard's importance for some models, the α=0.0 outperformance on Llama is not reconciled with the theory. This does not invalidate the overall contribution but represents an unaddressed tension between the theoretical motivation and empirical observations.

- **No variance or statistical significance reported.** The Ruler evaluation samples 100 instances per task (line 204), but no standard errors, confidence intervals, or multiple-seed runs are reported anywhere. For large-magnitude improvements this is not a concern, but for LongBench gains of 1–2 points (e.g., Llama-3.1-8B Summarization at 40%: 26.11 → 27.15 for SnapKV), it is unclear whether the improvement is reliable. Given the overall consistency across 29 datasets, this does not undermine the main conclusions but is a reporting limitation.

### Trivial

- **H2O baseline simulation (line 200).** H2O is simulated using the last 256 tokens' attention weights due to FlashAttention-2 incompatibility. The paper mentions this but does not discuss how the simulation may affect H2O's relative performance. Since H2O is a minor reference baseline and the primary comparisons are against the three SOTA methods where H2O is not central, this is a minor clarity issue.

- **Efficiency evaluation scope.** Overhead measurement (Figure 3) uses only one model (Llama-3.1-8B) and one context length (32K). Since V·W^O is a linear operation scaling with n·d, results at longer sequences (e.g., 64K–128K) would strengthen the "negligible overhead" claim, but the current evidence is sufficient given the linear scaling argument.

## Nice-to-Haves

- Provide standard deviations or confidence intervals for main experimental results where practical.
- Extend efficiency evaluation to longer sequences to confirm linear-scaling overhead.
- Discuss bound tightness — the triangle-inequality bound could be loose, and acknowledging this caveat would strengthen the paper's rigor.

## Removed Points

- **Critic's "Critical Issue #1: Pseudocode mismatch."** Downgraded from Fatal to Minor because: (a) the text description is unambiguous, (b) Assumption 3.4 confirms the intended algorithm, (c) the pseudocode's meaning is inferable from context. This is a correctable presentational issue, not a structural flaw.
- **Bound tightness concern.** Generic to any triangle-inequality bound; the paper's empirical validation (Section 4.7) demonstrates practical effectiveness.
- **V·W^O scaling cost mentioned as a weakness.** The paper already quantifies overhead; the critic acknowledges it's modest.
- **"Missing variance/statistical significance" mentioned as a "Critical" or "Major" issue.** Moved to Minor because the results are consistent across 29 datasets; variance would be a nice addition but is not required given the scale of evidence.
- Generic strengths from Strength Finder (e.g., "important problem," "interesting question") removed. Only strengths with specific, verifiable evidence are retained.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the pseudocode notation issue and the α=0.0 paradox on Llama, both of which are genuine and actionable but do not constitute observations absent from the paper itself.

## Suggestions

1. **Fix Algorithm 1 pseudocode.** Make Stage 1 use "A_i ∈ Top_k(A, b')" (selection by attention weights) to match the text and Assumption 3.4. Change line 5 from "A_i ∈ Top_k(𝒜, b')" accordingly.
2. **Discuss the α=0.0 outperformance on Llama.** Either analyze why Llama's attention distribution makes the safeguard unnecessary, or add a boundary condition characterizing when the safeguard is critical vs. optional.
3. **Acknowledge the single-query vs. multi-query theoretical gap.** A brief paragraph noting that the bound is derived for a specific query while practical eviction handles future-unknown queries would improve intellectual honesty, even if the empirical results are not affected.
4. **Report variance measures** for at least the main Ruler results (where 100 samples per task are available) to allow readers to assess small-magnitude improvements.

## Score and Decision

**Score: 7.5**

**Decision: Accept**

**Rationale.** The paper makes a genuinely novel contribution: formalizing critical KV cache selection as output perturbation minimization and deriving a non-trivial upper bound that jointly incorporates attention weights and projected value states. The algorithm is clean, plug-and-play with three SOTA methods, and the empirical evaluation is unusually comprehensive (29 datasets, 3 LLMs, 3 base methods). The two-stage design is theoretically motivated and empirically validated — the Mistral α=0.0 failure case dramatically demonstrates its necessity. The weaknesses (pseudocode notation, single-query theory gap, α=0.0 Llama paradox, no variance reporting) are all addressable in revision and none threaten the core contribution. This is a well-above-average submission that advances the field's understanding of cache eviction from heuristic to principled optimization.

**Calibration note.** The calibration tool was unavailable due to a persistent file-system error. The score is based on direct assessment of the paper against ICLR standards: the contribution is novel and well-supported, the theory is sound, the experiments are extensive, and the limitations are minor and fixable. A score of 7.5 reflects a paper that is clearly above the acceptance bar without being a once-in-a-conference standout — appropriate for a strong submission with bounded, addressable weaknesses.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>