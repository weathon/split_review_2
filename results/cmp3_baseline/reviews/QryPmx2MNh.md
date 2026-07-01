## Summary

This paper introduces a method for automatically discovering learning-friendly token orderings for the decoder input in Transformer-based arithmetic reasoning. The key idea is to train a small Transformer on a mixture of sequences in different orders and identify orders that yield faster loss drops in early training (loss profiling). To handle the factorial search space, the authors propose a two-stage hierarchical approach: a global stage that permutes blocks of tokens and a local stage that refines within-block order. Experiments on three synthetic order-sensitive tasks (ReLU, SQUARE-19, INDEX) show the method recovers the known forward order, and on multiplication (PROD) it rediscovers the reverse-digit order reported in prior work.

## Strengths

- **Novel problem formulation.** The paper is the first to systematically address the optimization of decoder token order for learning arithmetic tasks, moving beyond heuristic choices.
- **Practical and efficient search strategy.** The loss profiling technique leverages early training dynamics to rank orders without full training, and the hierarchical decomposition makes the search tractable for up to ~6 billion permutations (L=13) with random initialization and longer sequences with structured initialization.
- **Clear empirical validation.** The designed tasks (ReLU, SQUARE-19, INDEX) convincingly demonstrate that order matters and that the proposed method can identify the optimal forward order, improving success rates from ~10% to near 100%.
- **Reproduction of known result.** The method successfully rediscovers the reverse-digit order for multiplication, confirming its ability to find non-trivial learning-friendly orders.

## Weaknesses

### Major

- **Limited novelty of discovered orders.** On the three designed tasks, the optimal order is the trivial forward order, which is obvious from the task construction. The only non-obvious discovery is the reverse-digit order for multiplication, which was already known from prior work. The paper would be significantly stronger if it demonstrated a genuinely new, non-obvious order that improves learning on a more complex or realistic task.
- **No comparison to alternative search methods.** The paper dismisses soft-permutation optimization due to information leakage but does not compare the proposed method to other discrete optimization approaches (e.g., evolutionary algorithms, Bayesian optimization over permutations, or reinforcement learning). Without such baselines, it is unclear whether the hierarchical loss profiling is the most effective or efficient approach.
- **Potential for suboptimality due to greedy pruning.** The hierarchical method greedily prunes candidates at each stage, which may discard promising permutations that would only perform well after further refinement. The paper does not analyze the risk of missing the global optimum or provide any theoretical guarantees.

### Minor

- **Limited sequence length.** With random initialization, the method only works up to L=13. While the factorial space is large, many practical reasoning tasks involve longer sequences. The structured initialization extends to L=40, but this requires prior knowledge to design block-level candidates.
- **Computational cost not fully characterized.** The paper reports 1–7 hours on a single GPU for the longest exploration, but the cost scales with the number of candidate permutations and the number of hierarchical stages. A more detailed analysis of how the cost grows with L and the number of candidates would be helpful.
- **Connection to chain-of-thought is overstated.** The tasks are simple arithmetic recurrences, not multi-step reasoning chains typical of CoT. The paper's title and framing suggest a broader applicability that is not yet demonstrated.

### Trivial

- The INDEX task definition in Equation (5.4) uses a sum of previous outputs modulo L, but the window size d is not clearly defined in the equation (it appears as a fixed parameter in the text). Minor clarification needed.

## Nice-to-Haves

- Apply the method to a task where the optimal order is genuinely unknown and non-trivial, such as multi-step symbolic integration or theorem proving.
- Compare against a simple baseline like random search with early stopping to show the advantage of loss profiling.
- Provide theoretical analysis of why loss profiling works (e.g., connection to easy-to-hard learning dynamics or spectral bias).

## Novel Insights

None beyond the paper's own contributions. The observation that loss drops in early training correlate with learning-friendly orders is empirically demonstrated but not theoretically novel; similar ideas are used in curriculum learning and data-quality control. The hierarchical search strategy is a practical engineering contribution rather than a conceptual breakthrough.

## Suggestions

- Add a baseline comparison with random search over permutations (with early stopping) to quantify the benefit of loss profiling.
- Include an experiment on a task where the optimal order is not known a priori, e.g., a multi-step arithmetic problem with carries or a symbolic reasoning task.
- Discuss the risk of greedy pruning and consider adding a small number of random restarts or a beam-search variant to mitigate suboptimality.

## Score and Decision

**Score:** 6.5  
**Decision:** Accept (borderline)

The paper addresses a novel and well-motivated problem, proposes a practical solution, and provides solid empirical validation on synthetic tasks. However, the contributions are incremental: the method recovers known optimal orders rather than discovering genuinely new ones, and the evaluation lacks comparisons to alternative search strategies. The paper is technically sound and clearly written, making it a borderline accept for ICLR.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>