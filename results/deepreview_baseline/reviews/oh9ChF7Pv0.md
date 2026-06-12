## Summary

This paper introduces EGG-SR, a unified framework that integrates symbolic equivalence into symbolic regression (SR) via equality graphs (e-graphs). It extends three classes of SR algorithms—Monte Carlo Tree Search (MCTS), Deep Reinforcement Learning (DRL), and Large Language Models (LLMs)—by using e-graphs to compactly represent equivalent expressions, prune redundant exploration, aggregate rewards, and enrich feedback prompts. The authors provide theoretical justification that EGG-MCTS tightens the regret bound and EGG-DRL reduces gradient variance, and present empirical results showing improved normalized MSE across several benchmarks.

## Strengths

- **Novel problem framing and unified approach:** The paper identifies an underexplored and computationally important issue—symbolic equivalence in SR—and proposes a single data structure (e-graph) that can be plugged into multiple modern SR paradigms. This unification is conceptually clean and practically valuable.

- **Theoretical analysis:** The paper provides formal regret analysis for EGG-MCTS (building on existing transposition table work) and proves unbiasedness and variance reduction for the EGG-DRL gradient estimator. These theoretical guarantees support the claim that equivalence awareness accelerates learning.

- **Empirical gains in multiple settings:** Across MCTS, DRL, and LLM-based SR, EGG brings noticeable improvements in prediction accuracy (lower NMSE) on several datasets, especially under the noiseless setting. The memory and time efficiency plots convincingly demonstrate that EGG adds negligible overhead.

- **Clear presentation and good visualization:** The figures illustrating e-graph construction and the integration pipelines are well-designed and help the reader understand the mechanics.

## Weaknesses

### Fatal
None.

### Major

1. **Inconsistent empirical gains.** The claim that EGG “consistently enhances” SR is not fully supported by the data. In Table 1, several entries show EGG performing worse than the baseline (e.g., noisy DRL on (4,4,6) where DRL achieves 2.46 vs EGG-DRL 5.09; noisy MCTS on (3,2,2) where MCTS is better). The paper does not discuss these failure cases or provide an explanation, weakening the overall message.

2. **Overhead in MCTS and LLM not evaluated.** The time efficiency analysis is performed only for DRL (Fig. 5). For MCTS, the cost of repeatedly constructing e-graphs for many nodes could be substantial, yet only search tree size is reported. For LLM, the cost of parsing generated code and building e-graphs is not measured. The claim of efficiency is therefore only partially supported.

3. **Rewrite rule sensitivity not studied.** The method’s effectiveness depends on the set of rewrite rules. The paper lists rules only in the appendix and never analyzes how performance changes with rule coverage, whether missing rules hurt, or whether rules ever introduce unsound equivalences. This is a critical missing analysis for a method whose core is equivalence detection.

### Minor

1. **Limited LLM evaluation.** The LLM experiments cover only four problems and two base models. The improvements are often small and occasionally reversed (e.g., Bacterial growth with Mistral). The generalizability of EGG-LLM to a broader range of SR tasks is unproven.

2. **No comparison to alternative equivalence-aware methods.** The paper does not compare against simpler equivalence-handling baselines, e.g., expression simplification before reward computation, or hashing-based deduplication. This makes it hard to judge whether the e-graph machinery is strictly necessary or merely sufficient.

3. **Theoretical sketch is dense.** While full proofs are in the appendix, the main-text sketch of the regret and variance theorems is terse and would be difficult for a non-specialist to follow. The connection between the effective branching factor and the specific MCTS variant used here could be clarified.

### Trivial
None.

## Nice-to-Haves

- An ablation study showing which rewrite rules provide the most benefit.
- Evaluation on non-trigonometric datasets (e.g., rational, exponential) to test generality.
- A direct runtime comparison of EGG-MCTS versus standard MCTS over the full training duration.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that equality graphs—originally designed for program optimization—can serve as a single abstraction to inject mathematical equivalence awareness into fundamentally different SR search strategies (tree search, policy gradient, and language model prompting). This suggests a broader principle: many combinatorial search problems in science may benefit from a shared, compact representation of equivalence classes, even when the underlying search mechanisms are heterogeneous.

## Suggestions

1. Discuss or analyze the cases where EGG fails to improve (e.g., noisy DRL on (4,4,6)), and hypothesize why. This would strengthen the paper’s credibility.
2. Provide an overhead analysis (time and memory) for EGG-MCTS comparable to the DRL analysis, or at least a qualitative discussion of expected cost.
3. Add a sensitivity experiment where rewrite rules are removed one at a time to measure their impact.
4. Consider comparing against a simple baseline that directly simplifies expressions (e.g., via SymPy) before computing rewards, to isolate the benefit of e-graph-based equivalence.

## Score and Decision

- **Score:** 6.0  
- **Decision:** Accept  
The paper presents a novel, theoretically grounded framework that addresses a meaningful problem in symbolic regression. The core idea is sound, and the empirical evidence, though not uniformly strong, is sufficient to support the contribution. The identified weaknesses (inconsistent gains missing on some metrics, insufficient overhead evaluation, and lack of rewrite-rule analysis) prevent a higher score but do not invalidate the overall contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>