## Summary

This paper proposes ARPO (Agentic Reinforced Policy Optimization), an RL algorithm for training multi-turn LLM-based tool-use agents. The key insight is that token entropy increases sharply after tool-call steps, revealing underexplored behavioral uncertainty. ARPO introduces an entropy-based adaptive rollout mechanism that branches sampling at high-entropy tool-call steps, combined with advantage attribution estimation, to improve step-level tool-use exploration while halving the tool-call budget. Experiments across 13 benchmarks show consistent improvements over trajectory-level RL baselines.

## Strengths

- **Well-motivated empirical observation.** The paper provides a clear pilot study (Figures 1, 2) demonstrating that token entropy spikes after tool-call steps, which is a genuine and practically useful signal. This observation is quantified across multiple tools (search engine, Python interpreter) and tasks, lending it credibility.

- **Comprehensive and diverse evaluation.** The paper evaluates across 13 benchmarks spanning mathematical reasoning, knowledge-intensive reasoning, and deep search domains, using multiple backbone models (Qwen2.5-7B, Llama3.1-8B, Qwen3-8B, Qwen3-14B). Results in Tables 1 and 2 show consistent improvements. For instance, on Llama3.1-8B, ARPO achieves 55.3% average accuracy versus 51.1% for the best baseline, a 4+ point improvement.

- **Genuine efficiency gains.** Figure 7a demonstrates that ARPO uses roughly half the tool calls of GRPO during training while achieving better final performance. This is a practically significant advantage given the high cost of tool interactions in agentic RL training.

- **Multiple complementary analyses.** The paper provides useful secondary evidence including Pass@K scaling analysis (Figure 6), rollout diversity clustering (Figure 7b), and hard vs. soft advantage comparison (Figure 5), which together paint a coherent picture of why ARPO works.

- **Theoretical grounding.** The Generalized Policy Gradient (GPG) theorem in Section 3.3 provides a formal justification for optimizing over macro-actions (partial rollout segments), connecting the practical algorithm to policy gradient theory.

## Weaknesses

### Fatal
None.

### Major

- **The novelty of advantage attribution is diminished by the soft variant.** The paper proposes hard and soft advantage estimation, but Figure 5 shows soft is consistently better, and Section 3.2 explicitly states that the soft setting's effect is already implicit in standard GRPO via the importance sampling ratio (Equation 4). This means the primary algorithmic novelty reduces to the adaptive rollout mechanism, while the advantage attribution component (presented as a second core contribution) is largely a no-op in practice. This weakens the paper's claim of two distinct contributions.

- **Incremental gains on standard benchmarks.** On Qwen2.5-7B (Table 1), several individual benchmark scores are tied with or even slightly below baselines (GSM8K: 92.2 vs. GRPO's 92.8; MATH500: 78.8 vs. DAPO's 80.4). The average improvement over the best baseline is only ~1.8 points on Qwen2.5-7B. While consistent, these gains are modest for a method paper proposing a new algorithm.

- **Insufficient ablation of key hyperparameters in the main text.** The branching decision depends critically on α, β, and τ (Equation 2), yet the paper does not present sensitivity analysis for these in the main body. The method's robustness to these choices is unclear, which matters given that they directly control the exploration-exploitation tradeoff.

### Minor

- **Theoretical analysis notation is loose.** Macro states are defined twice with the same symbol MS_i (Section 3.3), and the connection between the GPG theorem and the actual ARPO algorithm is not made explicit. The theorem is general enough that it would justify almost any macro-action RL method, so its specific value to ARPO is unclear.

- **Unfair comparison elements in deep search.** Table 2 includes workflow-driven agents (ReAct, Vanilla RAG, WebThinker) that are not RL-trained, mixing comparison categories. The RL-based comparisons (GRPO vs. ARPO) are the most informative, but the table conflates different paradigms.

- **The "pioneeringly" claim overstates novelty.** The paper claims to "pioneeringly quantify the token entropy variation" of LLMs during agentic reasoning, but entropy-based analysis of LLM reasoning has been extensively studied (as acknowledged in the paper's own citations of Wang et al., 2025b,c; Zheng et al., 2025b).

### Trivial
None.

## Nice-to-Haves

- A convergence analysis or at least empirical convergence curves comparing ARPO and GRPO over more training steps would strengthen the efficiency narrative.
- Analysis of failure cases—when does ARPO's branching fail to help or even hurt performance?
- Comparison with other exploration strategies in RL beyond entropy-based branching (e.g., curiosity-driven exploration, count-based exploration).

## Novel Insights

The most novel insight is the empirical finding that entropy spikes at tool-call boundaries provide a reliable signal for directing RL exploration, and that selectively branching at these high-entropy points yields a more efficient exploration strategy than full trajectory-level sampling. The PCA/DBSCAN clustering analysis (Figure 7b) further suggests that this entropy-guided branching produces more structured and diverse rollout distributions, which is a non-obvious finding. However, the core idea—branching where the model is most uncertain—is conceptually straightforward within the existing entropy-regularized RL literature.

## Suggestions

- Move the key ablation studies (entropy threshold sensitivity, effect of α and β, number of branches) from the appendix into the main paper, as these are essential for understanding the method's robustness.
- Add a clearer explanation of why the soft advantage estimation (which reduces to GRPO) works better, possibly connecting it to variance reduction or implicit regularization arguments.
- Provide a more direct comparison of ARPO's computational overhead (wall-clock time, not just tool calls) versus trajectory-level methods.

## Score and Decision

The paper presents a well-motivated and empirically validated method for improving RL training of tool-use agents. The entropy-based adaptive branching mechanism is sound and consistently effective, and the efficiency gains (half the tool-call budget) are practically valuable. However, the core algorithmic novelty is limited—the advantage attribution component is shown to be largely redundant with GRPO—and the improvements on standard benchmarks are modest. The deep search results are more impressive, and the multi-backbone evaluation is thorough. Overall, this is a solid contribution that would benefit the community but falls short of a strong accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>