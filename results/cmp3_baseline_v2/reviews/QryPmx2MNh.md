## Summary
This paper addresses the problem of automatically discovering a learning-friendly order of output tokens for Transformers learning arithmetic tasks. The authors propose a pipeline that trains a Transformer on a mixture of sequences in different orders, then selects orders that yield fast early loss drops (loss profiling). To handle the factorial search space, they introduce a two-stage hierarchical search: a global stage that finds a coarse block-level permutation and a local stage that refines within-block and between-block orders. Experiments on three synthetic order-sensitive tasks (ReLU, SQUARE-19, INDEX) and a multiplication task show that the method can recover the optimal (forward) order in most cases and rediscover the known reverse-digit order for multiplication, improving success rates from around 10 % to near 100 %.

## Strengths
- **Novel problem formulation.** Optimizing the output token order for learning is an underexplored direction. The paper formalizes the problem and provides a practical search framework, which is a meaningful contribution.
- **Clever use of training dynamics.** Leveraging the observation that learning-friendly orders exhibit faster early loss drops is an elegant way to rank permutations without full training. The loss profiling procedure is computationally efficient (can process thousands of candidates in a single short training run).
- **Hierarchical search to manage combinatorial explosion.** The two-stage global–local approach is a sensible way to tackle the factorial search space. The experiments demonstrate it can find good orders from billions of candidates.
- **Reproduction of known result.** The method correctly rediscovers the reverse-digit order for multiplication reported in prior work (Shen et al., 2023), which lends credibility to the approach.

## Weaknesses

### Fatal
None.

### Major
- **No comparison with alternative order-search methods.** The paper only compares its discovered orders with the forward and reverse baselines. It does not compare against other plausible search strategies (e.g., random sampling with full training, evolutionary optimization, Gumbel-softmax-based permutation learning). Without such baselines, it is difficult to gauge whether the proposed method is truly effective or simply adequate for the chosen tasks.
- **Validation on synthetic tasks where the optimal order is known by construction.** The three order-sensitive tasks (ReLU, SQUARE-19, INDEX) are designed so that forward is the only causally consistent order. Recovering forward order is a necessary sanity check but does not demonstrate the ability to discover *non-obvious* good orders. Only the multiplication task provides a non-trivial target (reverse-digit), and that order was already known. A stronger validation would be a task where the optimal order is unknown and the discovered order leads to measurably better performance than any manually defined candidate.
- **Limited task difficulty and length.** For the INDEX task (the hardest one), the method often fails to find the forward order, and success rates after retraining are not reported. The experiments with random initialization only go up to length 13. With structured initialization the method works up to length 40, but scaling to longer sequences typical of real arithmetic (e.g., 100+ digits) is left open and may be challenging.

### Minor
- **The local stage search over block sizes is heuristic and may not guarantee a good result.** The method iterates over block lengths from 2 to L/2, but the order of exploration (intra-block then inter-block) may miss better permutations that require simultaneous changes across multiple block sizes. No analysis of the quality of the local search is provided.
- **The assumption that learning-friendly orders always show faster early loss drop is plausible but not rigorously justified.** The paper does not discuss failure cases or counterexamples where an order is hard to learn initially but eventually achieves high performance. The experiments only demonstrate that forward order has fast drop; other orders that are eventually good but slow to start would be missed.
- **The computational cost, though reasonable, is not compared to a simple alternative.** The exploration takes 1–7 hours. A naive approach of training a full model on dozens of random orders for the same total compute might yield competitive results. The paper does not provide such a cost–benefit comparison.

## Nice-to-Haves
- Compare the method with a random search baseline that trains full models on a small set of random permutations, to show that loss profiling provides a clear efficiency advantage.
- Apply the method to a task where the optimal order is not obvious, e.g., learning to execute a simple program or perform symbolic integration, and demonstrate improved generalization.
- Analyze the discovered orders to extract principles (e.g., dependency length, myopia of causal structure) that explain why certain orders are easier to learn, beyond the trivial "forward is causal" case.

## Novel Insights
The core insight—that training dynamics can be used as a cheap proxy for ordering quality, combined with a hierarchical decomposition to handle factorial search—is genuinely novel within the context of output token order optimization. While the easy-to-hard learning phenomenon itself is well known, its application to ranking permutations of the target sequence (rather than ranking instances) is a creative extension. The hierarchical search strategy, though heuristically motivated, provides a practical way to narrow the search space shown to work in both random and structured settings.

## Suggestions
- Add a baseline of random order search with full training (even if computationally expensive) to demonstrate that loss profiling achieves better or comparable results with far less compute.
- For the INDEX task, report success rates after retraining on the discovered orders; if they are still low, analyze why the method fails and whether modifications (e.g., more epochs of loss profiling, larger exploration model) can improve.
- Include an experiment on a task longer than length 13 with random initialization, even if it requires more computational budget, to show the method’s scaling behavior.
- Provide an ablation of the hierarchical search: compare the final performance when only the global stage is used, only the local stage (starting from identity), or with different block sizes in the global stage.

## Score and Decision
**Score:** 6  
**Decision:** Accept  

The paper introduces a genuinely novel problem and a practical method for solving it. The experiments are sufficient to demonstrate the viability of the approach, though they are limited by the synthetic nature of the tasks and the lack of comparisons to other search methods. The missing baselines and the restriction to short sequences prevent a stronger score, but the overall contribution is positive and well within the acceptance threshold for ICLR.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>