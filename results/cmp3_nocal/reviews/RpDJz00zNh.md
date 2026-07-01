Now I have all the evidence I need. Let me produce the final consolidated review.

## Summary

This paper proposes ConciseHint, a framework for improving the token efficiency of large reasoning models (LRMs) by injecting conciseness hints (either manually designed text or learned embeddings) *during* token generation, rather than before generation (as in prompting or fine-tuning). An adaptive interval mechanism controls hint intensity based on the growing reasoning length, and a dynamic position strategy determines where to inject the hint to balance accuracy and prefilling cost. Experiments on Qwen3 (1.7B/4B/8B) and DeepSeek-R1-14B across GSM8K, AIME24, and GPQA-Diamond show substantial token reductions (often 30–65%) with minimal accuracy change, and the approach is demonstrated to combine with existing efficiency methods (Prompt, Deer, NoWait, BeConcise) for further gains.

## Strengths

1. **Genuine paradigm novelty.** The paper cleanly identifies and fills a gap: existing efficient-reasoning methods operate *before* generation (prompting, SFT, RL), whereas ConciseHint intervenes *during* generation by injecting hints into the ongoing token stream. The "before-reasoning" vs. "in-reasoning" framing is the paper's strongest conceptual contribution.

2. **Substantial and consistent token reductions across multiple models and benchmarks.** Table 1 shows large, often dramatic token savings — e.g., Qwen3-4B on GSM8K drops from 2381→839 tokens (65% reduction, combined with Prompt) while accuracy stays within 0.3 points of the original. The reductions are consistent across model scales (1.7B to 14B) and difficulty levels (GSM8K, AIME24, GPQA-Diamond).

3. **Well-designed adaptive interval control, convincingly ablated.** Table 3 cleanly demonstrates why the adaptive mechanism is necessary: fixed high-intensity injection (interval=64) on the hard AIME24 benchmark crashes Qwen3-4B accuracy from 67.00%→45.33%, while on easy GSM8K the same interval barely hurts. The linear adaptive formula (τ_k = α + β·l_k) is simple, principled, and empirically validated.

4. **Clean ablation on injection position.** Table 4 shows that injecting at the tail destroys accuracy (42.93% vs. 55.56%), injecting at the head preserves accuracy but incurs 100% prefilling overhead, and the dynamic strategy navigates this trade-off. This is a thorough, well-motivated ablation.

5. **Plugin compatibility demonstrated, not just claimed.** The paper evaluates ConciseHint combined with four different baselines (Prompt, Deer, NoWait, BeConcise) and shows that in every case, the combination reduces tokens further than either method alone. This strengthens the practical utility claim.

## Weaknesses

### Fatal
None.

### Major

- **The integration mechanism with baselines is underspecified, harming reproducibility.** The paper claims "seamless integration" (lines 69, 214, 300) but never explains *how* ConciseHint combines with each baseline. What does "Ours (Deer)" mean algorithmically? Deer terminates generation early based on confidence; ConciseHint injects hints during generation. Does Deer's confidence check run after each chunk, or only at the end? For NoWait (which prohibits transition tokens like "wait"), how does the injected hint text interact with the token prohibition? Without specifying the integration mechanism, the combined results (Table 1) cannot be reproduced or interpreted. This is a core reproducibility gap that should be addressed in a rebuttal.

### Minor

- **No variance or confidence intervals reported, despite multiple runs.** The paper states that each experiment is run 5 times (GSM8K) or 10 times (AIME24, GPQA-Diamond) but only reports means (line 168–169). For AIME24 (30 problems), a difference of 2–3 percentage points corresponds to less than 1 problem. Without variance, the reader cannot assess whether accuracy differences like 64.33% vs. 66.67% (Ori vs. Ours(Ori) on AIME24, Qwen3-4B) are meaningful or noise. Adding standard deviations or confidence intervals would substantially strengthen the evidence, especially on the small-n benchmarks.

- **Multi-call inference overhead is not measured or discussed.** Algorithm 1 shows that ConciseHint operates by repeatedly calling the model in chunks of τ_k tokens (6–8 calls for a typical output), while all baselines use a single generation call. The paper motivates its work by "high inference latency" (line 15) but reports only token counts, not wall-clock time, cost, or FLOPs. Per-call overhead (context re-encoding, API latency) could partially offset the token savings. Even if the net gain remains positive given the large token reductions (the paper's prefilling-cost analysis in the stripped appendix may address token-level compute), the efficiency claims are incomplete without acknowledging this measurement gap in the main text.

- **ConciseHint-T (learned hints) is only evaluated on the smallest model (Qwen3-1.7B) and shows non-trivial accuracy degradation at γ=1.0.** Table 2 shows that ConciseHint-T at γ=1.0 drops GSM8K accuracy from 90.87%→88.01% and GPQA-Diamond from 39.39%→35.05%. The paper does not report ConciseHint-T results on Qwen3-4B, Qwen3-8B, or DeepSeek-R1-14B — the models used for the main results in Table 1. The claim that learned hints "generalize well to out-of-domain data" is only weakly supported by evidence from one small model. While ConciseHint (manual hint) is the primary contribution and is well-validated, the learned variant's claimed advantages merit broader validation.

- **No control experiment with a neutral hint.** The paper does not isolate whether the improvement comes from the hint content itself ("make answer concise!") or from the effect of breaking generation into chunks and restarting. Running the same multi-call protocol with a neutral placeholder (e.g., "[continue]") at the same adaptive intervals would clarify the mechanism. If the neutral hint produces similar token reduction, the improvement is driven by the chunked generation protocol rather than the conciseness message. If it does not, the paper's mechanistic claim is cleanly supported.

- **Ours(Ori) on Qwen3-8B GSM8K (1489 tokens) is *worse* than Prompt (1353) and Deer (1223) alone.** Table 1 shows this directly. While the combination (Ours(Prompt), Ours(Deer)) wins, the standalone claim that ConciseHint is "comparable to strong baselines" is only partially accurate — it is comparable to some baselines and worse than others on this particular setting. This is a factual observation that slightly tempers the claim.

### Trivial

- The transition word analysis (Table 5) provides thin evidence for the claim of "promoting efficient self-reflections": the transition interval (tokens per transition word) barely changes (e.g., 113→119 for Qwen3-4B GSM8K). The paper would benefit from either stronger evidence or more measured language.

## Nice-to-Haves

- Report wall-clock time alongside token usage to directly address the efficiency framing around "high inference latency."
- Run ConciseHint-T on at least one larger model (Qwen3-8B or DeepSeek-R1-14B) on at least one benchmark to broaden validation of the learned variant.
- Provide a sensitivity analysis for α and β in the main text rather than deferring entirely to the appendix.

## Removed Points

These points appeared in the input review but were removed under the filtering rules:

1. **"Largely unexplored" claim is overstated.** — Removed as a minor phrasing nitpick that does not affect the paper's substance.
2. **Constants 1024 and 0.8 lack justification in main text.** — The paper explicitly references Appendix A.2 for theoretical and empirical analysis of the position formula. Since the appendix is stripped by the parser, this criticism cannot be verified against the submitted paper.
3. **DeepSeek-R1-14B is smaller than full DeepSeek-R1; whether findings scale.** — The paper explicitly names the model it uses (DeepSeek-R1-14B). Asking whether findings scale to a larger model the paper does not claim to evaluate is a generic scaling question, not a specific weakness.
4. **No discussion of failure modes.** — Removed as a generic expectation not standardly required for acceptance at ICLR; the ablations (Tables 3 and 4) effectively discuss when the method fails (high fixed intensity, tail injection).
5. **Hyperparameter sensitivity claim is anecdotal.** — The paper references Section A.1 for a detailed ablation study. Since the appendix is stripped, this criticism targets potentially addressed content. The main text statement ("we find it always works well") is informal but the approach of fixing α=128 and β=0.2 across all experiments is a deliberate methodological choice, not negligence.
6. **Missing baseline: a prompt that says "Be concise at each step."** — The paper already tests multiple prompting baselines (BeConcise, Prompt) and an adaptive "Prompt" that asks the model to control length based on complexity. This suggestion overlaps with existing evaluations.

## Novel Insights

None beyond the paper's own contribution. The input review provides a thorough critical analysis but does not surface a novel perspective on the problem or method that the paper itself does not articulate.

## Suggestions

1. **Specify the integration mechanism for each baseline.** Clarify algorithmically how ConciseHint is combined with Deer (does the early-exit confidence check run after each chunk or only at the end?) and NoWait (how does the hint text interact with token prohibitions?). A brief algorithmic description or pseudo-code extension would resolve this.
2. **Add variance bars or confidence intervals to Table 1**, leveraging the multiple runs already conducted. This would address the most straightforward evidential gap.
3. **Add a neutral-hint control** (e.g., "[continue]" injected at the same adaptive intervals) to Table 3 or similar, to isolate the effect of the hint content from the chunked-generation protocol.
4. **Acknowledge the multi-call overhead** explicitly in the paper and, ideally, report wall-clock time for at least one model/benchmark pair to confirm that token savings translate to latency reductions.

## Score and Decision

<score>6</score>
<decision>Accept</decision>