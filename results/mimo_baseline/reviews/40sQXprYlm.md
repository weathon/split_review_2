## Summary
The paper introduces Distributed Neural Architectures (DNAs), where tokens/patches can traverse any series of computational modules in any order via learned routing decisions, generalizing MoE, MoD, parameter sharing, and early exit into a unified framework. The authors train DNAs in vision (ImageNet, ViT-small scale) and language (FineWeb-Edu, GPT-2 medium scale), finding they are competitive with dense baselines and exhibit emergent interpretable structure including power-law path distributions, module specialization, and context-dependent compute allocation.

## Strengths
- **Rich interpretability analysis.** The paper provides extensive, compelling visualizations of emergent structures: path specialization in vision (edges vs. objects vs. boundaries, Fig. 3), token grouping in language (semantically similar words routed to the same modules, Fig. 8), and deep-dream reconstruction showing interpretable features emerging at intermediate routing steps (Fig. 4). This is genuinely interesting and goes well beyond typical efficiency papers.

- **Principled unification of conditional computing approaches.** The DNA framework cleanly subsumes MoE, MoD, parameter sharing, and early exit as special cases that can emerge from optimization, providing a useful conceptual lens. The observation that "a mixture-of-all-of-these-methods emerges from end-to-end training" is a valuable finding.

- **Interesting empirical observations.** The power-law distribution of paths (both in random and trained models), the correlation between visual complexity and compute allocation (Fig. 5), and the finding that compute savings and parameter savings are not correlated are all noteworthy findings that advance understanding of conditional computation.

## Weaknesses
### Fatal
None.

### Major
- **Incomplete comparative evaluation.** The paper claims DNAs are "a natural generalization" of MoE and MoD but provides no comparison against these methods. This is a significant gap: without knowing whether a well-tuned MoE or MoD baseline at the same scale achieves similar performance and interpretability, it is impossible to assess what DNA uniquely contributes beyond novelty of framing. This is especially problematic since the architecture introduces substantial additional complexity (multiple routers, backbone layers, identity modules, bias tricks, step scheduling).

- **The top-2 language DNA outperforms GPT-2 medium but has ~7% more parameters (433M vs 406M).** The paper does not provide a controlled ablation showing whether a dense model with matched parameters would also improve. The claim that "trained DNAs are competitive with the dense baselines" obscures this asymmetry. In vision, the DNA models are actually worse (79.1% vs. 79.8%). The paper's framing overstates the empirical case.

- **No concrete efficiency measurements.** Despite "compute efficiency" being a central motivation and result, the paper reports no wall-clock latency, throughput, or FLOPS comparisons. The skip mechanisms (25% skip in vision, 30% skip in language) come with non-trivial accuracy drops (Table 3: top-2 with 30% skip drops from 59.2 to 52.5 on ARC-E), and the paper does not rigorously evaluate the Pareto frontier of efficiency vs. performance.

- **Numerous hyperparameters with limited ablation.** The architecture introduces many design choices: number of routers, modules, backbone size, identity modules, bias update speed ($u$), skip ratio ($r$), maximum steps ($s_{\max}$), and top-$k$ selection. The paper acknowledges limited search over these but provides no systematic ablation showing which choices matter most, making it difficult to assess whether the results are robust or sensitive to specific tuning.

### Minor
- **Random models also show power-law paths (Fig. 1 caption).** This raises the question of whether the power-law distribution is a structural property of the routing architecture itself rather than an emergent learned property. The paper notes this but does not investigate its implications for the interpretability claims.

- **The non-standard GPT-2 baseline.** The GPT-2 medium baseline uses no weight-tying ("GPT-2 medium (no weight-tying)" in Table 2), which is non-standard and likely hurts the baseline. This makes the language comparisons less convincing.

- **The language models are heavily under-parameterized** for the FineWeb-Edu dataset (21B tokens on 100B subset). The paper acknowledges this but the benchmarks in Table 3 are noisy—e.g., the shallower GPT-2 baseline has very different behavior on BoolQ (54.9 vs. 60.5) suggesting the comparisons are fragile at this scale.

- **No investigation of training cost.** DNAs likely require significantly more training compute than dense baselines due to the routing overhead, multiple forward passes through non-uniform paths, and inability to fully leverage hardware-level parallelism. This is not discussed.

### Trivial
- Table 3 references "Table 1" and "Appendix A" for hyperparameter details that are mentioned as being available in the paper.
- The Wiki perplexity column header could be clearer about whether it is word-level or token-level.

## Nice-to-Haves
- A comparison against MoE and MoD baselines at matched scale would substantially strengthen the paper.
- Wall-clock efficiency measurements (latency, FLOPS per token) for the skip models.
- Ablation on the number of modules, routers, and backbone depth.
- Scaling experiments at larger model sizes to assess whether DNA benefits grow with scale.

## Novel Insights
The observation that path distributions through both random and trained DNAs follow power-law distributions with exponent ~-1 is genuinely novel and intriguing—it suggests a structural universality in how tokens distribute through router-based architectures regardless of training. The finding that compute savings and parameter savings are uncorrelated (Section 3.3) is also non-obvious and suggests these are orthogonal efficiency dimensions that could be independently optimized. Finally, the visualization showing that boundary patches tend to follow distinct computational paths and that high-compute images are those with intricate boundaries (Fig. 5) connects conditional computation to perceptual salience in a compelling way.

## Suggestions
- Add comparison against MoE and MoD baselines with matched parameter budgets and compute.
- Report FLOPS or wall-clock latency for the skip models to ground the efficiency claims.
- Provide ablation studies on key hyperparameters (number of modules, backbone depth, top-$k$).
- Investigate whether the power-law path distribution is a property of the architecture design (e.g., softmax routing with finite steps) rather than a learned phenomenon—this would clarify the nature of the emergent structure.

## Score and Decision
The paper presents an interesting conceptual framework and produces compelling interpretability analyses. However, the empirical evaluation has significant gaps: no comparison against the conditional computing methods it claims to generalize, inflated efficiency claims without wall-clock measurements, and confounded parameter counts in the language comparison. The models are small-scale, and the results are competitive rather than clearly superior to baselines. The interpretability findings are the strongest contribution but are not rigorous enough (e.g., no causal testing of routing decisions) to carry the paper alone. This is a solid exploratory paper with valuable observations, but the experimental rigor does not yet match the ambition of the claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject