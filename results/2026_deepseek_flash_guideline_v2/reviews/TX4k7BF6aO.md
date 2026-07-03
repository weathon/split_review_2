The calibration tool is unavailable. I'll proceed with my own judgment calibrated against the ICLR scoring guidelines.

Let me now produce the final consolidated review.

## Summary

ARPO proposes an RL algorithm for training multi-turn LLM agents that use tools. The key idea is an entropy-based adaptive rollout mechanism: since LLM token entropy spikes after tool-call steps (shown in a pilot study), ARPO branches sampling at these high-entropy points to encourage step-level exploration, combined with advantage attribution estimation for the resulting branched trajectories. Experiments across 13 benchmarks (math reasoning, knowledge QA, deep search) compare ARPO against GRPO, DAPO, and REINFORCE++, reporting consistent improvements.

## Strengths

- **Empirically-motivated branching mechanism**: Section 2 directly measures token entropy after tool calls, showing sharp rises in the first 10–50 tokens following each tool invocation (observations Ob.1–3). This provides a concrete, data-driven motivation for branching at tool-call steps — the method is grounded in a measured phenomenon rather than chosen arbitrarily.

- **Consistent directional improvements across 13 benchmarks**: Table 1 shows ARPO outperforming GRPO/DAPO/REINFORCE++ on average across 10 reasoning tasks for both Llama3.1-8B (55.3% vs. 51.1% best baseline) and Qwen2.5-7B (58.3% vs. 56.5%). Table 2 extends this to deep search tasks (e.g., GAIA: ARPO 43.7% vs. GRPO 36.9% with Qwen3-14B). The improvement is directionally consistent across backbones and task families.

- **Tool-use efficiency finding**: Figure 7a shows ARPO using approximately 250–350 tool calls during training vs. GRPO's 400–450 on Qwen2.5-7B, demonstrating that the entropy-guided branching does not come at the cost of excessive tool use — a practically relevant result.

- **Generalization across model families and scales**: Results are reported on Llama3.1-8B, Qwen2.5-7B, Qwen3-8B, and Qwen3-14B, showing the method is not tied to a single architecture.

## Weaknesses

### Major

- **No variance or statistical significance reporting**. All results are point estimates without confidence intervals, error bars, standard deviations, or multiple seeds. Given that many individual-task gains are small (e.g., Qwen2.5-7B MATH500: ARPO 78.8 vs. DAPO 80.4; Llama3.1-8B AIME25: ARPO ties REINFORCE++ at 16.7), it is impossible to determine which differences reflect genuine improvement vs. sampling noise. The paper's strong claim of "firmly establishing its superiority" (line 184) is undermined by this omission. This is the most significant weakness because it directly affects the primary empirical contribution.

- **Overclaimed theoretical contribution**. Section 3.3 presents a "Generalized Policy Gradient Theorem" (Equation 6) which is the standard policy gradient theorem restated at the macro-action (segmented token) level. This is a well-understood property of temporal abstraction (options framework, Sutton et al., 1999) and does not specifically justify ARPO's entropy-based branching — any method that segments trajectories would satisfy it equally. Framing this as a novel theorem that provides a "robust theoretical foundation" for ARPO is a significant overreach. Removing or honestly reframing this section would strengthen the paper.

### Minor

- **"Half the tool-call budget" claim is only validated on one setting**. The tool-efficiency analysis (Figure 7a) compares ARPO vs. GRPO only on Qwen2.5-7B, not on other backbone sizes (Llama3.1-8B, Qwen3-8B/14B) or against DAPO/REINFORCE++. The abstract and conclusion generalize this claim broadly, but the evidence is limited to one comparison. The mechanism behind the efficiency gain (shorter trajectories vs. better exploration) is also not disentangled.

- **"Soft advantage estimation" is standard GRPO with no new loss**. Section 3.2 acknowledges that the soft setting "retain[s] the original GRPO loss formulation" (line 142). For the default configuration, the advantage contribution therefore reduces to applying GRPO to the adaptive rollout's output structure, not a new loss or advantage estimator. The paper presents this as a co-equal contribution alongside the rollout mechanism, which is a framing issue.

- **Pass@K analysis lacks baselines**. Figure 6 shows Pass@1/3/5 scaling for ARPO but does not include GRPO or DAPO at the same Pass@K levels. Without baselines, the scaling trend cannot be attributed to ARPO's method specifically rather than to properties of the model or tasks.

- **Rollout diversity evidence is thin**. The DBSCAN clustering analysis (54 vs. 48 clusters) depends critically on the eps parameter and embedding model choice (BGEM3). No parameter sensitivity or cluster quality metrics are reported, making this evidence suggestive but not conclusive.

### Trivial

- **Evaluation metric not indicated per-dataset in Table 1**. The paper states F1 is used for four knowledge-intensive QA tasks and LLM-as-Judge for others, but Table 1 does not indicate which metric applies to which dataset.
- **No limitations discussion**. The paper does not discuss when ARPO might fail (e.g., noisy entropy estimates, wasteful exploration from excessive branching).

## Nice-to-Haves

- Compare against segment-level or step-level RL methods cited in related work (Guo et al., 2025; Li et al., 2025g; Zheng et al., 2025a) rather than only trajectory-level baselines.
- Include GRPO/DAPO baselines in the Pass@K analysis (Figure 6).
- Disentangle the cause of tool-use efficiency (shorter trajectories vs. better exploration) by reporting average trajectory length.

## Removed Points

*These points were flagged for removal but are retained here for reference; treat them with caution.*

- "Deepsearch-R1-47B and WebWalker-3B are not standard model names" — These appear in Figure 1 description only (a parser artifact from image extraction), not in the paper's main text or results tables. **Removed** per parser-artifact rule.
- "Hyperparameters (α, β, τ, Z, M, N, k) not specified in main text" — The paper states implementation details are in Appendix E (line 178), which is stripped by the parser. **Removed** per appendix-stripping rule.
- "Unfair comparison due to hierarchical reward design" — The reward design (Equation 5) follows Tool-Star and applies to all RL methods, not just ARPO. The concern is a misunderstanding of the experimental setup. **Removed**.
- "Missing comparison against segment-level RL methods" — The paper clearly defines its comparison scope as trajectory-level RL algorithms. This is a nice-to-have, not a valid weakness. **Moved** to Nice-to-Haves.
- "GPG Theorem is a strength" (from Strength Finder) — As noted in Major Weaknesses, this is overclaimed and not a genuine theoretical contribution. The claimed strength is invalid. **Removed**.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a novel interpretation or reframing that the paper itself does not already articulate.

## Suggestions

1. **Add statistical rigor**: Run main experiments with at least 3 random seeds and report means ± standard deviations, or provide bootstrap confidence intervals for Pass@1. This is the single most important fix.
2. **Reframe the theoretical section**: Either present the macro-action policy gradient as a straightforward observation (with proper citation to the options framework) or remove it entirely. The paper's empirical contribution stands without this framing.
3. **Broaden the tool-efficiency validation**: Validate the "half the tool-call budget" claim on at least one additional backbone and against at least one additional baseline.
4. **Add baselines to Pass@K analysis**: Include GRPO/DAPO at the same Pass@K levels to contextualize the scaling trend.
5. **Clarify contribution boundaries**: Make explicit in the contribution list that the advantage attribution for the default "soft" setting is the application of GRPO to the adaptive rollout structure, not a new loss function.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>