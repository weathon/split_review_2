## Summary

This paper proposes Agentic Reinforced Policy Optimization (ARPO), a reinforcement learning algorithm designed for training multi-turn LLM-based agents that interact with external tools. ARPO introduces an entropy-based adaptive rollout mechanism that branches sampling at high-entropy tool-call steps, enabling step-level exploration of tool-use behaviors, combined with advantage attribution estimation for better credit assignment. Experiments across 13 benchmarks in mathematical reasoning, knowledge-intensive reasoning, and deep search domains show ARPO consistently outperforms trajectory-level RL algorithms (GRPO, DAPO, REINFORCE++) while using approximately half the tool-call budget.

## Strengths

- **Novel and well-motivated approach**: The paper identifies a genuine limitation of trajectory-level RL for agentic tasks—that LLMs exhibit high entropy after tool-call feedback, which trajectory-level methods ignore. The entropy-based adaptive rollout mechanism directly addresses this observation, providing a principled motivation for step-level exploration.

- **Strong empirical results**: ARPO consistently outperforms GRPO, DAPO, and REINFORCE++ across 10 reasoning benchmarks (Table 1) and 4 deep search benchmarks (Table 2), with average gains of ~4% on reasoning tasks and substantial improvements on GAIA (43.7% vs 36.9% for GRPO with Qwen3-14B). The tool-call efficiency result (Figure 7a) is particularly compelling—achieving better performance with half the tool calls.

- **Theoretical grounding**: The paper provides a Generalized Policy Gradient Theorem (Equation 6) that justifies the macro-action (partial rollout) perspective, showing that traditional token-level policy gradient is a special case of their framework. This adds rigor beyond purely empirical contributions.

- **Comprehensive evaluation**: The paper evaluates across 13 diverse benchmarks spanning three task categories, uses multiple backbone models (Llama3.1-8B, Qwen2.5-7B, Qwen3-8B/14B), and compares against strong baselines including both prompting methods and RL algorithms.

## Weaknesses

### Fatal
None.

### Major

- **Limited analysis of the entropy threshold hyperparameters**: The adaptive beaming mechanism (Equation 2) depends critically on parameters α (base sampling probability), β (stability entropy), and τ (threshold). The paper does not provide ablation studies on these hyperparameters, making it unclear how sensitive ARPO is to their choice or how to set them in practice. This is a significant gap for a method whose core innovation is entropy-based branching.

- **Missing comparison with other step-level RL methods**: The paper compares ARPO against trajectory-level methods (GRPO, DAPO, REINFORCE++) but does not compare against other step-level or segment-level RL approaches for LLMs, such as those cited in the related work (Guo et al., 2025; Li et al., 2025g; Zheng et al., 2025a). Without this comparison, it's unclear whether ARPO's gains come from step-level credit assignment generally or from the specific entropy-based mechanism.

- **Computational cost analysis is incomplete**: The paper claims ARPO reduces complexity from O(n²) to between O(n log n) and O(n²), but this analysis neglects the overhead of entropy computation, branching decisions, and the fact that partial sampling may create more total tokens than trajectory-level sampling (since branches are additional tokens). A more rigorous comparison of wall-clock time or FLOPs between ARPO and GRPO would strengthen the efficiency claims.

### Minor

- **The hard vs. soft advantage comparison (Figure 5) is limited**: Only one model (Qwen2.5-7B) is shown, and the training curves appear to have different starting points. It would be more convincing to see this comparison across multiple seeds and model sizes.

- **The theoretical contribution, while appreciated, is somewhat disconnected from the algorithm**: The GPG Theorem (Equation 6) shows that macro-action policy gradients are valid, but it doesn't specifically justify why entropy-based branching is optimal or why the specific form of Equation 2 is chosen over other branching criteria.

### Trivial
- The paper uses "Agentic Reinforced Policy Optimization" in the title but "Agentic Reinforce Policy Optimization" in the abstract (Section 3 heading). This inconsistency should be resolved.

## Nice-to-Haves

- An ablation study on the entropy threshold parameters (α, β, τ) would significantly strengthen the paper.
- Comparison with a simpler baseline that does random branching (rather than entropy-based) at tool-call steps would isolate the benefit of the entropy signal.
- Analysis of how the optimal branching budget (M-N) scales with task difficulty or model size would be practically useful.

## Novel Insights

Beyond the paper's own contributions, the key insight is that tool-call feedback creates a distributional shift in LLM token distributions that manifests as elevated entropy, and this entropy signal can be exploited as a natural exploration signal for RL training. This connects the uncertainty quantification literature with agentic RL in a way that is both intuitive and empirically validated. The finding that search engine feedback induces higher entropy than code interpreter feedback (Ob.3) is also interesting, suggesting that different tool types may require different exploration strategies.

## Suggestions

1. Add ablation studies on the entropy threshold parameters (α, β, τ) to demonstrate robustness and provide practical guidance.
2. Compare against at least one step-level or segment-level RL baseline (e.g., from the cited works) to isolate the benefit of the entropy-based mechanism versus step-level credit assignment in general.
3. Provide wall-clock time or FLOPs comparison between ARPO and GRPO to substantiate the efficiency claims beyond tool-call counts.
4. Consider adding a random-branching baseline to show that entropy-based branching is better than arbitrary branching.

## Score and Decision

The paper presents a novel, well-motivated algorithm with strong empirical results across diverse benchmarks. The entropy-based adaptive rollout mechanism is a creative solution to a genuine limitation of trajectory-level RL for agentic tasks. The main weaknesses are the lack of hyperparameter sensitivity analysis and missing comparisons with step-level baselines, but these do not invalidate the core contribution. The paper is clearly written, the experiments are thorough, and the results are convincing.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>