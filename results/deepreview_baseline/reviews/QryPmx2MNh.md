## Summary

The paper proposes a method for systematically discovering a learning-friendly order of decoder output tokens for Transformers learning arithmetic tasks. It uses *loss profiling*—short training on a mixture of candidate orders—to identify orders that yield fast early loss drops, and combines this with a two-stage hierarchical search to handle the factorial permutation space. Experiments on three synthetic order-sensitive tasks (ReLU, SQUARE-19, INDEX) and the PROD (multiplication) task show that the method recovers the known optimal forward or reverse order out of billions of candidates and raises success rates from near 0% to near 100%.

## Strengths

- **Novel problem formulation.** While prior work manually designed output orders (e.g., reverse digits for multiplication), the paper is the first to treat output-order optimization as a search problem and propose a systematic, automated solution.
- **Clever use of learning dynamics.** The loss-profiling idea—exploiting the easy-to-hard feature of neural net training to rank permutations—is a well-motivated and intuitive proxy faster than full training.
- **Hierarchical search makes the factorial space tractable.** The global–local decomposition is a sensible way to prune the search space, and the empirical demonstration of handling up to 13! ≈ 6×10⁹ permutations with random initialization (and L=40 with structured initialization) is convincing.
- **Rediscovery of known results.** The method recovers the reverse-digit order for multiplication (Shen et al., 2023), serving as a strong sanity check on real-world arithmetic.

## Weaknesses

### Fatal
None.

### Major

1. **Scalability and practicality are limited.** The method is demonstrated only for target lengths up to L=13 (random) and L=40 (structured). For longer or variable-length sequences—common in real-world reasoning—the computational cost of the hierarchical search would grow prohibitively. The paper acknowledges this as future work, but it severely restricts the immediate applicability of the method.
2. **Lack of competitive baselines.** The paper compares only to forward and reverse orders. Without comparisons to a simple random search with the same compute budget, or to heuristic strategies (e.g., sorting by dependency analysis), it is unclear whether the hierarchical loss-profiling pipeline is actually more efficient than naive alternatives. The contribution would be stronger if the method outperformed a reasonable random-sampling baseline.
3. **Transfer from small to large model is not validated.** The exploration uses a small transformer (1 layer, 1 head), while final evaluation uses a 6-layer model. The paper assumes the ordering is universal, but no experiment checks whether the order ranked best by the small model is also best for the large model. If rankings disagree, the method could misguide the final training.
4. **Tasks are designed such that forward order is obviously optimal.** The three synthetic tasks (ReLU, SQUARE-19, INDEX) are explicitly constructed so the forward order is the natural causal order. Demonstrating that the method recovers forward order is a validation, but it does not show that the method can discover *non-obvious* learning-friendly orders that differ from the human-intuitive order. A more compelling experiment would involve a task where the optimal order is counter-intuitive and unknown a priori.

### Minor

- **Missing experimental details.** The number of candidates T in the global stage, the number of epochs E in loss profiling, and the exact hyperparameters for the depth K are not clearly stated. This makes reproduction harder.
- **Sensitivity analysis is absent.** There is no study of how performance changes with the depth K, the block size l, or the number of candidates retained after each stage. The method might be brittle to these choices.
- **The “unraveling the chain of thought” framing is somewhat overclaimed.** The paper only reorders the existing output tokens; it does not generate new intermediate reasoning steps as in chain-of-thought prompting. The title is catchy but might mislead readers about the actual scope.

### Trivial
None.

## Nice-to-Haves
- An experiment that explicitly validates the correlation between small-model loss profiling rank and large-model final accuracy (e.g., scatter plot).
- A comparison to a simple baseline that searches over block-level swaps only (without the full hierarchical pipeline) to isolate the benefit of each component.
- Application to a non-arithmetic sequential reasoning task (e.g., program execution output) to demonstrate broader applicability.

## Novel Insights
None beyond the paper’s own contributions. The core insight—that early-stage loss can serve as a cheap proxy for ordering difficulty—is an incremental application of known easy-to-hard learning dynamics, though its use for output-order search is new.

## Suggestions
1. Provide the missing experimental hyperparameters (e.g., T, E, K) either in the main text or appendix.
2. Add a baseline that performs random permutation search with the same compute budget (same number of trained models) and compare success rates.
3. Include a transferability experiment: train the small exploration model and the large final model on the same set of candidate orders and measure the rank correlation of their losses/accuracies.
4. Apply the method to at least one task where the optimal order is not the forward order (e.g., a task where the naturally recursive dependency runs backward or has no obvious causal direction), to demonstrate genuine discovery of a non-trivial order.

## Score and Decision

**Score:** 6  
**Decision:** Accept (Borderline)

The paper addresses a novel and relevant problem with a reasonable method and positive experimental results on synthetic tasks. However, the limited scalability, lack of strong baselines, and unvalidated model transfer keep it from being a strong acceptance. The contribution is solid but incremental, and the audience at ICLR will find the problem and the loss-profiling idea interesting. The issues are addressable and do not invalidate the core claims.

MY FINAL SCORE: 6</score>  
MY FINAL DECISION: Accept</decision>