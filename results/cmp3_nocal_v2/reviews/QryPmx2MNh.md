## Summary

This paper addresses a novel task: automatically discovering learning-friendly output orderings (permutations) for autoregressive Transformers learning arithmetic tasks. The core idea — "loss profiling" — trains a single Transformer on a mixture of different orders and identifies benign orders by their faster early-training loss drops. To handle the factorial search space, the authors propose a two-stage hierarchical approach (global block-level search + local intra-block refinement). Experiments on four arithmetic tasks show the method can identify good orders among billions of candidates, rediscovering the known reverse-digit order for multiplication (Shen et al., 2023).

## Strengths

1. **Well-motivated and clearly scoped new problem.** The paper identifies a genuine gap: prior work (Shen et al., 2023) showed output ordering matters for arithmetic but relied on heuristic choices. Automating the discovery of learning-friendly orders is a sensible and novel direction. The formulation in Section 3 (Eqs. 3.1–3.2) cleanly captures the problem.

2. **Elegant core idea empirically validated.** Training a single model on a mixture of permutations and identifying the best order from validation loss (Section 4, P1–P2) is clever and avoids the prohibitive cost of training a separate model per permutation. The proof-of-concept in Section 5.4 (Figure 5) convincingly shows that the forward order is separable from random orders in the loss profile across all three tasks — this is the paper's strongest experiment.

3. **Successful rediscovery of a known result on multiplication.** The method recovers the least-significant-digit-first order for PROD (Table 2, L=10), matching Shen et al. (2023). This provides valuable external validity that the method is finding genuinely meaningful orders.

4. **Observation that non-forward orders can also be learning-friendly.** For RELU L=10 and L=12, the method finds orders that are *not* the exact forward order but still achieve 100% success (Figure 6a). This suggests the method can discover alternative good orders beyond the trivial identity permutation.

## Weaknesses

### Fatal
None.

### Major

1. **Incomplete evidence for INDEX (d=4, d=8) undermines the headline "10% to 100%" claim.** The abstract states "increasing the success rate of arithmetic computation from approximately 10% to 100%" and the conclusion echoes this across all three tasks. However:
   - For INDEX (L=13, d=4) and (L=13, d=8), Table 2 shows the discovered orders *differ* from the forward order (`[0,1,7,6,4,2,5,8,3,9,10,11,12]` and `[1,2,3,4,5,6,7,8,10,9,12,0,11]`).
   - **No success rates are reported** for training on these discovered orders. Figure 6 (success rate curves) covers only RELU and SQUARE-19. The paper acknowledges INDEX "proves harder" (Section 5.5) — the forward order itself achieves only 62.3% (d=4) and 81.8% (d=8) — but never tells the reader whether the discovered orders outperform even the ~10% reverse-order baseline, let alone approach 100%.
   
   The "10% to 100%" claim is supported for RELU, SQUARE-19, and INDEX d=2 (forward order recovered, 100% achieved), but not for INDEX d=4 and d=8. This is an evidential gap that directly affects the paper's central quantitative claim.

2. **No comparison against any alternative search method.** The paper evaluates against two fixed orders (forward and reverse) — neither is a *search* method. The relevant comparison is against alternative strategies that could also find good permutations, such as random search (sample N permutations, train briefly, pick the best) or greedy/evolutionary search. Without such a baseline, the reader cannot assess whether the hierarchical loss profiling is genuinely efficient relative to simpler alternatives. The paper's claim that the method "efficiently determines learning-friendly orders" (contribution 2) needs a reference point.

### Minor

3. **Structured initialization experiments do not isolate the method's contribution.** When initialized with $\mathcal{P}_b$ (block-restricted permutations with block size 5), the method scales to L=30–40. But $\mathcal{P}_b$ dramatically restricts the search space (block-wise shuffles of size-5 blocks instead of $L!$ full permutations). The paper attributes the scaling to the hierarchical search (Section 5.5: "once implausible candidates are pruned, the proposed method can explore the remaining space far more effectively"), but the dominant factor is likely the initialization restriction. No ablation is provided: what does the hierarchical search achieve starting from $\mathcal{P}_b$ that a simple greedy search over $\mathcal{P}_b$ alone would not? Without this control, the L=30–40 results are less convincing as evidence for the method's scalability.

4. **Method description is underspecified in key places.** The global stage (Section 4) says "conceptually split each target sequence into $k$ blocks" and generates block-level permutations $Q_i$, but it is not specified how these $Q_i$ are constructed — are they all $k!$ block permutations, a random subset, or something else? The local stage says $R_1^i,\dots,R_l^i$ are "all the permutations inside the $i$-th block" — for a block of size $l$, enumerating all $l!$ internal permutations could be expensive. The paper states a single training handles up to 5,040 permutations, which provides an upper bound, but the description of how candidate sets are constructed within this budget is unclear, affecting reproducibility.

5. **Results appear to come from single runs with no variance estimates.** Figure 5 (loss profiling) and Figure 6 (success rates) show no error bars or confidence intervals. Given that the method involves training Transformers with random initialization and data shuffling, the ranking of permutations by validation loss (where differences can be as small as ~0.05 nats in Figure 5a) could exhibit non-trivial variance across seeds. Multiple seeds would substantially increase confidence in the reliability of the ranking.

### Trivial
None.

## Nice-to-Haves

- **Soft-permutation exploration:** The paper dismisses the soft-permutation approach (Section 3, Figure 2) due to information leakage, but does not explore whether adding sparsity or entropy regularization could mitigate the issue. A fuller treatment would strengthen the motivation.
- **Efficiency breakdown:** The paper reports 1–7 hours total runtime but does not break this down by stage (global vs. local) or by number of training runs.
- **Ablation of candidate set size $T$:** The choice $T = (K+1)!$ is not empirically justified. Showing how performance varies with $T$ would be informative.
- **Out-of-distribution evaluation:** Contribution 1 mentions generalization to out-of-distribution samples, but all experiments only measure in-distribution success rate. An OOD experiment would strengthen the claims.

## Removed Points

These points were flagged for removal from the input review. Treat them with caution:

- **"Duplicate 1 in Table 2 RELU L=10 order"**: The extracted text shows `[4,5,6,7,8,9,0,1,1,2,3]` with a duplicate "1" — this is a parser artifact from PDF extraction, not an error in the original submission.
- **"Motivating example about non-injective maps is over-explained"**: This is a presentation preference, not a substantive weakness.
- **"Loss profiling on out-of-distribution generalization should be tested"**: Moved to Nice-to-Haves; the paper scopes in-distribution success as its primary evaluation.
- **"The method's soft-permutation dismissal is too quick"**: Moved to Nice-to-Haves; this is a constructive suggestion, not a flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report the missing INDEX success rates.** Train the large model on the discovered orders for INDEX (L=13, d=4 and d=8) and report whether they improve over the reverse-order baseline. If they do not, honestly characterize this limitation. If they do, the paper's main claim becomes properly supported.
2. **Add a random-search baseline.** Sample the same number of permutations as used in loss profiling, train each briefly, and pick the best. Compare against the hierarchical method's result so the reader can assess the efficiency claim.
3. **For the structured initialization experiments, include an ablation** that applies a simpler search (e.g., greedy refinement without the global-local hierarchy) on $\mathcal{P}_b$ to isolate the hierarchy's contribution from the restricted search space.
4. **Report multiple seeds** (at least 3) for the loss profiling step (Figure 5a) and the final success rates (Figure 6).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>