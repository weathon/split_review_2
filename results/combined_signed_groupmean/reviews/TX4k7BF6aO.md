Now I have all the calibration data. Let me finalize my analysis and produce the review.

Let me now write the final review with the score calibration fully reasoned.

**Round 1 Bracket:** Based on the calibration search, the most relevant anchors are:
- StepTool (5.50) — very similar topic (step-grained RL for tool learning), rejected mainly for limited novelty
- LAM Simulator (6.00) — similar (online exploration for agent RL)
- ARMAP (6.67) — similar (LLM agent RL with reward modeling)
- CRAFT (6.67) — similar (tool creation/retrieval for LLMs)

The paper has a stronger novelty signal than StepTool (5.50) but shares the missing-baseline weakness. It has broader evaluation than LAM Simulator (6.00) but has the no-variance gap. I'd place the initial bracket at (5.5, 6.5).

**Final Score:** 6.0 — The paper has a genuinely novel core idea (entropy-guided adaptive rollout) with strong empirical motivation and broad evaluation. However, the missing Tool-Star baseline (the paper inherits both the reward design and test splits from Tool-Star) and lack of variance reporting are meaningful gaps that prevent a stronger score. The GPG Theorem overclaim is a minor concern.

Let me write the final review now.## Summary

This paper proposes Agentic Reinforced Policy Optimization (ARPO), an RL algorithm for multi-turn LLM-based agents that use tools. The core idea is to measure token-level entropy during tool interactions and adaptively branch sampling at high-entropy steps (following tool-call feedback), rather than treating the entire trajectory as a single rollout. ARPO combines an entropy-based adaptive rollout mechanism with advantage attribution estimation (hard and soft variants) and is evaluated across 13 benchmarks spanning mathematical reasoning, knowledge-intensive reasoning, and deep search, using Llama3.1-8B, Qwen2.5-7B, and Qwen3-8B/14B backbones.

## Strengths

- **Empirically grounded motivation.** The preliminary experiment (Section 2, Figures 1–2) directly measures token-level entropy during multi-turn tool use and demonstrates that entropy spikes following tool-call feedback. The three observations — that entropy spikes after tool calls, that search feedback causes larger spikes than Python feedback, and that early reasoning has lower entropy — are specific, falsifiable, and provide a clear rationale for why trajectory-level RL may be suboptimal for tool-use agents.

- **The core algorithmic idea is creative and coherent.** The entropy-based adaptive rollout mechanism (Section 3.1) follows directly from the empirical observation: if entropy spikes at certain steps, branch there. The design — global sampling for coverage, partial sampling at decision points, and termination with compute budgets — is internally consistent. The advantage attribution estimation (Section 3.2), particularly the soft variant that falls out naturally from GRPO's importance sampling ratio (Equation 4), handles branched trajectories without introducing a separate value function.

- **Consistent empirical advantage across model families and task types.** Table 1 shows ARPO outperforming GRPO, DAPO, and REINFORCE++ across 10 datasets using two backbone families (Llama3.1-8B and Qwen2.5-7B). On deep search benchmarks (Table 2), ARPO improves over GRPO on both Qwen3-8B and Qwen3-14B. The Pass@K analysis (Figure 6) shows the advantage holds at higher sampling budgets. This breadth of evaluation is a genuine strength.

- **Tool-call efficiency finding has practical value.** Figure 7a shows ARPO using roughly 250–350 tool calls during training compared to GRPO's 400–480 while achieving higher accuracy. Tool-call costs are a significant practical bottleneck in agentic RL, making this finding meaningful for deployment.

## Weaknesses

### Major

- **Missing the most directly relevant baseline (Tool-Star).** The paper's reward function (Equation 5) and test splits for math and knowledge reasoning benchmarks are directly adopted from Tool-Star (Dong et al., 2025). Tool-Star is itself an agentic RL method designed for multi-tool agents, making it the most natural competitor. Without this comparison, it is impossible to attribute whether ARPO's gains come from the entropy-guided adaptive rollout or from the shared training pipeline (reward design, data selection, etc.) that both methods use. The paper compares against GRPO, DAPO, and REINFORCE++ — general-purpose RLVR algorithms — but the comparison that would isolate ARPO's core contribution is absent. This is a structural gap that weakens the central claim.

- **No statistical significance or variance reported.** None of the results in Table 1 or Table 2 include standard deviations, confidence intervals, or any measure of variance. This is especially concerning on small-problem-count datasets: on AIME2024 (30 problems), ARPO's 23.3% vs GRPO's 13.3% is a difference of 3 problems out of 30; on AIME2025 (30 problems), the difference is 16.7% vs 13.3% — 1 problem. Given that LLM evaluation and RL training are inherently stochastic, the reader cannot assess whether the reported improvements are reliable or within noise of the evaluation. The consistent pattern across 13 datasets partially mitigates this concern, but variance reporting is standard practice in RL research and should be included.

- **The GPG Theorem does not carry the theoretical weight it is asked to bear.** Section 3.3 presents the Generalized Policy Gradient Theorem as providing "a robust theoretical foundation" for ARPO. The theorem essentially states that if you group tokens into macro-actions (segments), the policy gradient theorem applies at the segment level. This is a standard property of the policy gradient — it holds at any temporal abstraction level — and does not justify why tool-call boundaries specifically or high-entropy branching is optimal. The actual justification for the branching criterion remains empirical (the entropy observation in Section 2). The GPG framing adds formal language but no substantive constraint or new insight.

### Minor

- **Entropy computation overhead is acknowledged but not quantified.** Footnote 1 says "Neglecting the minor overhead from token-level entropy calculations." Computing the token-level entropy (Equation 1) requires the full softmax over the entire vocabulary at every token position, while standard LLM inference during rollout only computes logits for sampled tokens. The paper provides no wall-clock timing, no FLOP comparison, and no analysis of how this overhead trades off against the tool-call savings. Since the complexity analysis explicitly "neglects" this cost, the complexity claims are incomplete.

- **The "half the tool-call budget" claim is imprecise.** Figure 7a shows ARPO using approximately 250–350 tool calls versus GRPO's 400–480, which is roughly 37–48% fewer. While still a meaningful improvement, "half" overstates the savings. The claim should be scoped to the exact measured range.

- **Hard vs. soft advantage comparison lacks replication evidence.** Figure 5 compares hard vs. soft advantage estimation on Qwen2.5-7B alone, without multiple seeds or error bars. The conclusion that "the soft setting consistently yields more stable rewards" requires multiple independent runs to support the claim of consistency.

### Trivial

- **Equation (3) has a variable collision.** The outer sum uses index $t$ for trajectories while the inner sum also uses $t$ for token positions within a trajectory. This should be $\sum_{i=1}^G \sum_{t=1}^{|y_i|}$.

## Nice-to-Haves

- Report inference-time tool-call efficiency, which is what matters for deployment (the paper currently only reports training-time efficiency).
- Show whether ARPO provides differentially larger gains on search-heavy tasks vs. computation-heavy tasks, since Section 2 observes that search feedback causes larger entropy spikes.
- Provide sensitivity analysis for the branching threshold $\tau$ on at least one dataset to demonstrate robustness of the method to hyperparameter choices.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. **Missing hyperparameter values (α, β, τ, Z, M, N, k)** — The paper states implementation details are provided in Appendix E. Since the appendix is stripped by the parser per system constraints, this weakness cannot be verified against the actual submission per guidelines.
2. **Section 5.1 comparison to GPT-4o/DeepSeek-R1 is "misleading"** — The paper uses these as reference points for scale comparison (14B vs 671B), not as direct baselines; the actual RL comparison (ARPO vs GRPO on Qwen3-14B: 10.0% vs 8.6%) is clearly reported.
3. **Section 5.2 Chinese prompts as "confounding factor"** — Using Chinese prompts for Chinese queries is methodologically correct, not a confound; the paper explicitly explains this.
4. **Entropy analysis only shown for 1-2 tasks** — Preliminary experiments are illustrative by design; the evaluation span covers all 13 tasks.
5. **Conclusion claim too sweeping** — 13 benchmarks across 3 tool environments constitutes reasonable breadth.
6. **Normalization description vague** — The paper writes "summing all the values of ΔH and dividing by the vocab size V," which is adequately specific.
7. **Missing related works** — Cannot be verified without external sources.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include Tool-Star as a baseline to isolate whether gains come from the adaptive rollout or the shared training pipeline.
2. Report all main results with standard deviations across at least 3 random seeds.
3. Provide wall-clock timing or FLOP analysis comparing entropy-enabled rollout vs. standard rollout.
4. Scope the "half the tool-use budget" claim to the exact measured range.
5. Add multiple seeds for the hard vs. soft advantage ablation (Figure 5).

---

## Calibration Summary

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to this paper |
|--------|------|-----------|-------|-----------|--------------------------|
| StepTool | PNHjoWcQje | 5.50 | R2 | Yes | Very similar topic (step-level RL for tool learning); rejected mainly for limited novelty. ARPO is more novel (entropy-guided adaptive rollout vs. standard multi-step RL) and has broader evaluation. |
| LAM Simulator | Dpqw0namg3 | 6.00 | R1 | Yes | Similar topic (online exploration for agent RL); shares "no variance" weakness. ARPO has broader evaluation and stronger algorithmic novelty. |
| ARMAP | womU9cEwcO | 6.67 | R1 | Yes | Similar topic (LLM agent RL); lacks ARPO's baseline gap. ARPO has broader evaluation. |
| CRAFT | G0vdDSt9XM | 6.67 | R2 | Yes | Tool learning topic; shares missing-baseline concern. ARPO has comparable empirical strength. |
| RaDAgent | l1pNNQSzZv | 6.25 | R1 | Yes | Decision-making agents; ARPO has broader evaluation but also the baseline gap. |
| MetaTool | 6AUzsrsNUx | 5.00 | R1 | Yes | Tool learning; shares missing comparison weakness. ARPO has stronger novelty. |
| Efficient RL w/ LLM Priors | e2NRNQ0sZe | 6.25 | R2 | Yes | LLM+RL for sequential decision-making; accepted despite limited scope. ARPO has broader eval. |

**Round 1 bracket:** (5.5, 6.5) — established from the StepTool (5.50) and ARMAP/CRAFT (6.67) anchors.

**Narrowing:** StepTool (5.50) is the closest topical match and was rejected primarily for limited novelty — a weakness ARPO does not share (entropy-guided adaptive rollout is genuinely novel). However, ARPO shares StepTool's missing-baseline concern, and adds a no-variance gap that several anchors (LAM Simulator @ 6.00) also share. ARMAP (6.67) and CRAFT (6.67) are stronger papers or were accepted despite similar weaknesses, placing ARPO below them.

**Final placement:** 6.0. The paper's strengths (novel algorithm, broad evaluation, practical efficiency) outweigh its weaknesses, but the missing Tool-Star baseline and lack of variance reporting are meaningful gaps that prevent it from scoring above 6.5. The weaknesses are addressable in revision.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>