## Summary

This paper addresses the training-inference misalignment in tree-based speculative decoding (SpD) for LLM acceleration. The authors propose two contributions: (1) TALF (Tree-Aware Loss Function), a training objective that explicitly incorporates tree structure into draft model training by computing cross-entropy loss over dynamically constructed trees from the target LLM, and (2) SALF (Stopping at Low Further Gains), a dynamic tree construction algorithm with a conditional stopping criterion that balances draft quality against computational overhead. Combined, SALF & TALF achieve 15.6-39.4% and 6.5-24.4% end-to-end speedups over EAGLE-2 and HASS respectively across multiple model architectures and benchmarks.

## Strengths

- **Clear problem identification and motivation**: The paper convincingly demonstrates (Figure 2) that existing training methods (EAGLE, HASS) underperform on lower-ranked tokens that constitute a non-negligible portion of draft trees, providing strong empirical justification for the tree-aware training approach.

- **Well-designed ablation studies**: Table 2 systematically isolates the individual contributions of TALF and SALF by testing all combinations of loss functions and tree construction methods, showing that each component provides meaningful improvements and that they are complementary.

- **Comprehensive evaluation across diverse settings**: The paper tests 3 model families (Llama-2, Llama-3.1, DeepSeek-R1-Distill), 5 benchmarks, and both greedy and non-greedy sampling, with consistent improvements across all configurations.

- **Practical contribution with theoretical grounding**: SALF includes a provable monotonicity guarantee (Theorem 1) for the probability sum, and the method addresses a real practical concern (drafting overhead) that prior work on optimal tree search (SpecExec) acknowledged but did not fully resolve.

## Weaknesses

### Major

- **Limited novelty of TALF relative to HASS**: The core idea of TALF—computing loss over multiple branches rather than a single sequence—is a natural extension of HASS's approach of feeding back draft model features during training. The paper acknowledges that TALF with k=1 is "almost the same as HASS" (Section 4.4), and the main difference is expanding to multiple branches. While this is a reasonable contribution, the incremental nature should be more explicitly acknowledged.

- **Training cost and fairness concerns**: The training procedure for TALF requires precomputing trees with the target LLM, which adds preprocessing cost. For DeepSeek-R1-Distill-Llama-8B, the paper trains each method for the same wall-clock time (24 hours) rather than the same number of epochs, which could disadvantage EAGLE and HASS if they converge faster. The paper should report training FLOPs or total compute cost to enable fair comparison.

- **SALF threshold sensitivity**: Table 4 shows that the optimal threshold varies (th=0.5 gives best mean speedup for DeepSeek, but th=0.6 is chosen as default for "more consistent performance"). The paper acknowledges this as future work but does not provide guidance on how practitioners should select this threshold for new models, which limits practical applicability.

### Minor

- **The paper claims "without altering the draft model architecture"** in the abstract, but this is somewhat misleading since TALF changes the training procedure significantly (tree-based loss computation, no regression loss), which could affect convergence properties even if the forward pass architecture is identical.

- **Missing comparison with SpecExec**: The paper mentions SpecExec's optimal tree search as a baseline for tree construction but does not include SpecExec in the end-to-end speedup comparisons (Table 1). Given that SALF is positioned as an improvement over optimal tree search, a direct comparison would strengthen the evaluation.

### Trivial

- The paper uses "SALF & TALF" as the combined method name but the acronyms are introduced in reverse order (SALF first in the title, TALF first in the abstract).

## Nice-to-Haves

- Analysis of how the SALF threshold could be dynamically adapted during inference based on observed acceptance rates or drafting overhead
- Investigation of whether TALF's benefits extend to other draft model architectures beyond the EAGLE-style single-decoder-layer design
- Discussion of the memory overhead of storing precomputed trees during TALF training

## Novel Insights

The key insight is that tree-based SpD creates a fundamental distribution mismatch: training objectives focus on the most probable token sequence, but inference relies on exploring multiple branches. The paper's demonstration that draft models are poorly calibrated on lower-ranked tokens (Figure 2b) provides a clear diagnostic for why prior methods underperform. The SALF stopping criterion insight—that the probability sum of nodes being expanded monotonically decreases, enabling principled early stopping—is a practical contribution that bridges the gap between theoretically optimal tree search and computationally feasible inference.

## Suggestions

- Report training FLOPs or total compute (including target LLM preprocessing for TALF) alongside wall-clock time to enable fair comparison of training costs
- Include SpecExec as a baseline in the main speedup table (Table 1) to directly validate the SALF improvement claim
- Provide a heuristic or rule-of-thumb for selecting the SALF threshold based on model characteristics or inference budget

## Score and Decision

The paper makes a solid, well-executed contribution to an active area (speculative decoding). The problem is well-motivated, the experiments are thorough, and the results are consistently positive. However, the novelty is incremental—TALF is a natural extension of HASS to tree structures, and SALF is a practical optimization of existing tree search methods. The paper does not introduce fundamentally new architectures or paradigms. Given the ICLR 2026 score distribution where the median is 4.0 and the mean is 4.21, this paper's quality and contribution warrant a score above the median but not at the top of the scale.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>