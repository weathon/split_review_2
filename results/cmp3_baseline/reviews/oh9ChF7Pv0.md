## Summary

This paper introduces EGG-SR, a unified framework that integrates symbolic equivalence into symbolic regression using equality graphs (e-graphs). The framework is applied to three classes of SR algorithms—Monte Carlo Tree Search (MCTS), Deep Reinforcement Learning (DRL), and Large Language Models (LLMs)—by compactly encoding equivalent expressions and using them to modify the learning procedure (e.g., sharing statistics across equivalent nodes in MCTS, aggregating probabilities in DRL, and enriching feedback in LLMs). Theoretical analysis provides regret bounds for EGG-MCTS and variance reduction for EGG-DRL, and experiments across several benchmarks show that incorporating EGG improves the accuracy of discovered expressions within the same time budget.

## Strengths

- **Novel unified framework**: The paper is the first to systematically integrate symbolic equivalence via e-graphs into multiple modern SR paradigms (MCTS, DRL, LLM) with a common module. This is a conceptually clean and practically useful