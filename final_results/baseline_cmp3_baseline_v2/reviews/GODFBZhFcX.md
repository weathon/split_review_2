## Summary

This paper introduces PCE (Planner-Composer-Evaluator), a framework that converts implicit assumptions in LLM reasoning traces into structured decision trees for uncertainty-aware planning in decentralized multi-agent embodied environments. Instead of relying on heavy inter-agent communication to mitigate partial observability, PCE extracts assumptions from LLM reasoning, organizes them into a scenario tree, and scores each path by likelihood, goal-directed gain, and execution cost to select actions rationally. Experiments across two benchmarks (C-WAH and TDW-MAT) and three LLM backbones show consistent improvements over communication-centric baselines in success rate and task efficiency with comparable token usage.

## Strengths

- **Novel and principled approach to uncertainty handling**: The core idea of extracting implicit assumptions from LLM reasoning traces and structuring them into a decision tree is genuinely novel. Unlike prior work that treats communication as the primary uncertainty mitigation mechanism, PCE treats environmental assumptions as first-class decision variables, shifting the paradigm from communication-centric coordination to structured reasoning over uncertainty. This is a conceptually clean and well-motivated contribution.

- **Strong empirical validation across diverse settings**: The paper evaluates PCE on two challenging benchmarks (C-WAH and TDW-MAT) with three diverse LLM backbones (GPT-4o mini, GPT-OSS:20B, Gemma3:4B), demonstrating consistent improvements. The ablation studies (LLM scaling, component analysis) are thorough and convincingly show that PCE's gains are additive to and distinct from scaling model capacity or reasoning depth. The user study adds valuable human-centric validation.

- **Well-designed evaluation framework**: The metrics are thoughtfully chosen—Total Steps and success rates for task performance, Usages for total computational cost (including internal LLM tokens), and Comm as a descriptive diagnostic measure rather than a success metric. This avoids conflating communication frequency with quality and provides a complete picture of system behavior.

- **Clear writing and effective figures**: The paper is well-structured and clearly explains the motivation, method, and results. Figures 1 and 2 effectively communicate the architecture and the flow from reasoning trace to action selection.

## Weaknesses

### Major

- **Limited evaluation of the Composer's reliability**: The Composer is a critical component that must extract meaningful assumptions from reasoning traces and construct coherent decision trees. While the paper mentions human-expert correlation studies in the appendix (A.10, A.11), the main text provides no quantitative assessment of how often the Composer generates valid, non-redundant, or logically consistent assumptions. If the Composer frequently produces irrelevant or contradictory assumptions, the entire framework degrades. A simple metric like "fraction of generated assumptions that are semantically valid" or "human agreement rate on assumption relevance" would strengthen the evaluation.

- **The cost model is simplistic for real-world deployment**: The execution cost function uses only movement distance and message length with fixed weights (α=1, β=1, λ=1). In practice, the relative costs of movement vs. communication depend heavily on the environment (e.g., communication might be nearly free in some settings but extremely costly in others). The paper does not analyze sensitivity to these hyperparameters in the main text (only mentioned in appendix A.5), and the fixed default values raise questions about how well the framework would generalize to domains with different cost structures.

- **Limited analysis of failure modes**: The paper reports aggregate performance improvements but does not systematically analyze when PCE fails or underperforms baselines. For instance, in Table 1, PCE's Usages for GPT-4o mini on C-WAH (44353.56) is higher than CaPo (41702.00) and CoTS (44628.12). Understanding the conditions under which PCE's structured approach incurs higher computational cost would help practitioners decide when to use it. Similarly, the paper could discuss scenarios where the assumption extraction fails (e.g., when LLM reasoning traces are too vague or contradictory).

### Minor

- **The user study is relatively small (12 participants)**: While the results are consistent and statistically suggestive, a larger sample would increase confidence. The paper could acknowledge this limitation more explicitly.

- **The comparison with MCTS-based planning is relegated to the appendix**: Given that CoTS uses MCTS and PCE is positioned as an alternative to tree search, a more prominent comparison in the main text would strengthen the paper's claims about PCE's efficiency advantages.

### Trivial

- The paper uses "Usages" as a metric name, which is slightly awkward; "Token Usage" or "Total Tokens" would be clearer.

## Nice-to-Haves

- A discussion of how PCE handles cases where the LLM's reasoning trace contains no explicit assumptions (e.g., when the model is uncertain and produces hedging language like "I'm not sure").
- An analysis of the computational overhead of the Composer and Evaluator modules relative to the Planner, to help practitioners understand the trade-offs.
- A comparison with a simple baseline that uses random action selection or heuristic exploration, to establish the lower bound of performance.

## Novel Insights

The paper's key insight is that LLM reasoning traces already contain implicit assumptions about uncertain aspects of the environment, but these assumptions are fragmented and locally referenced, preventing systematic reconciliation. By extracting and structuring these assumptions into a decision tree with explicit likelihood, gain, and cost evaluation, PCE demonstrates that uncertainty-aware planning can be achieved without heavy communication or model scaling. This suggests that the bottleneck in LLM-based embodied planning is not reasoning capability per se, but the lack of a structured mechanism to aggregate and weigh competing hypotheses about the environment. The finding that PCE's benefits are additive to scaling (both model capacity and reasoning depth) is particularly valuable, as it implies that structured uncertainty handling is a complementary axis of improvement that does not require larger models or more inference compute.

## Suggestions

- Add a quantitative evaluation of the Composer's output quality (e.g., human agreement on assumption relevance, fraction of valid assumptions) in the main text or a prominent appendix section.
- Include a sensitivity analysis of the cost model hyperparameters (α, β, λ) in the main text, or at least provide guidance on how to set them for new domains.
- Discuss failure cases or limitations more explicitly—for example, scenarios where the LLM's reasoning trace is too vague to extract meaningful assumptions, or where the decision tree becomes too large to evaluate efficiently.

## Score and Decision

The paper presents a novel, well-motivated, and empirically validated framework for uncertainty-aware planning in embodied multi-agent systems. The core idea is principled and the experiments are thorough, covering multiple benchmarks, backbones, ablations, and a user study. The weaknesses are relatively minor and do not invalidate the contribution. The paper is a strong candidate for acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>