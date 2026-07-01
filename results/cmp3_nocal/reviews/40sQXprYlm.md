## Summary

This paper introduces Distributed Neural Architectures (DNAs), a flexible proto-architecture where tokens dynamically route through a collection of (transformer, MLP, attention, etc.) modules with learned connectivity. DNAs generalize MoE, MoD, parameter sharing, and early-exit into a single framework. The paper trains DNA models at non-trivial scale in both vision (ImageNet, ViT-Small scale) and language (FineWeb-Edu, GPT-2 Medium scale), and analyzes emergent structure. The core contribution is demonstrating feasibility and providing interpretability analysis, not achieving SOTA.

## Strengths

1. **Genuinely novel architectural framework.** The proto-architecture where tokens route through modules with learned connectivity (Section 2.1) is a clean, well-motivated generalization of multiple conditional computing approaches. This is not an incremental tweak.

2. **Cross-domain feasibility demonstration at non-trivial scale.** Training DNAs in both vision (ImageNet, 300 epochs, line 116) and language (FineWeb-Edu, 21B tokens, line 160) and showing they reach within ~1% of dense baselines (Tables 1, 3) is a genuine empirical contribution. The fact that these models are trainable at all with dynamic routing is nontrivial.

3. **Rich interpretability analysis that goes beyond typical architecture papers.** The path-specialization analysis (Figs. 3, 8), routing-decision visualization via deep-dream (Fig. 4), and compute-allocation analysis (Fig. 5) reveal real emergent structure—low-rank paths capturing broad features (edges, colors) and high-rank paths capturing specific concepts (brass instruments, puzzle pieces). Section 3.2 is particularly strong.

4. **Honest reporting of negative or ambiguous results.** The paper acknowledges that (i) parameter sharing in language appears "most likely random" (Section 4.3), (ii) the random-initialization baseline also exhibits power-law path distributions with exponent −1 (Fig. 1 caption), and (iii) the compute-efficient language model degrades substantially (Table 3). This honesty makes the positive results more credible.

## Weaknesses

### Major

1. **"Competitive" claim is not fully controlled on total parameters.** The central claim that DNAs are "competitive with dense baselines" (abstract, line 32, line 205) is supported by comparisons with mismatched total parameter counts. In vision (Table 1), top-1 DNA (34M total params, 79.1%) trails ViT-small (22M, 79.8%) with 55% more total parameters. In language (Table 2), top-1 DNA (583M total) and top-2 DNA (603M total) exceed GPT-2 Medium (406M) by 43–48% in total parameters. While active parameters *are* matched (22M/22M in vision, 406M/406M in language for top-1), and the paper's explicit framing ("not focused on beating SOTA," line 38) mitigates this, the "competitive" claim as stated is only partially supported. A controlled comparison matching total parameters or a clear statement that the overhead is inherent to the routing framework would strengthen the paper.

### Minor

2. **Training cost is unreported.** The paper reports no information about training FLOPs, GPU hours, memory usage, or throughput. Since DNA's dynamic routing, per-step forward passes, and attention sparsity likely introduce overhead, whether training is practically feasible is an unanswered question relevant to evaluating the contribution.

3. **Compute-efficiency results show substantial degradation without adequate contextualization.** The top-2 (30% skip) language model (Table 3) drops from 2.674 to 2.784 loss (4.1% relative increase) and sees large drops on downstream tasks (e.g., ARC-E: 59.2→52.5, HellaSwag: 41.8→35.5, LAMBADA: 34.0→23.8). It also underperforms GPT-2 (30% shallower) on nearly every metric. The paper presents these results but does not discuss how this trade-off compares with alternative efficiency methods or whether it represents a favorable operating point.

4. **The power-law path distribution is partially a property of the random architecture, and the difference training makes is not analyzed.** The paper acknowledges (Fig. 1 caption, lines 26–27) that random DNA models also exhibit power-law path distributions with exponent −1. The trained vision model has exponent −1 (same as random), while the language model has −1.2. This difference is noted but not analyzed for significance, reproducibility, or mechanism. This weakens the power-law finding as a claim about learned structure.

5. **The dynamic attention sparsity mechanism is underspecified.** The paper states (Fig. 1 caption) that "when a module that contains attention operation acts on several tokens simultaneously the attention pattern is computed *only* between these tokens." How tokens are grouped for attention computation, minimum group sizes, and handling of near-empty attention modules are not described.

6. **Number of identity modules is not specified.** The paper introduces "several *identity* modules" (line 82) for compute efficiency but never states how many exist in the routing search space.

### Trivial

7. **No error bars or multiple seeds reported.** Given that routing involves sampling with hard top-k, seed variance is relevant. The main results (Tables 1, 3) report single runs.

## Nice-to-Haves

- A Pareto curve of accuracy/loss vs. compute for multiple skip rates (0%, 10%, 20%, 30%, 50%), including a "train a smaller dense model with equivalent inference FLOPs" baseline, would strengthen the compute-efficiency analysis.
- Reporting training FLOPs and wall-clock time would support the feasibility thesis.
- An analysis of whether the exponent difference (−1 vs −1.2) between random and trained language models is statistically significant.

## Removed Points

The following points from the input review were removed under the filtering rules:
- Comments about the "laundry list of efficiency techniques" in the introduction — this is a standard related-work overview, not a weakness.
- The backbone layers being a "significant constraint" — the paper explicitly states this as a design choice (line 80–81).
- Load-balancing concerns — the paper states it does not use load balancing (line 102); speculation about training instability is not grounded in the reported results.
- "Figure references are inconsistent" — paper references appendices that were stripped by the parser; this is an artifact, not a paper flaw.
- The per-step single-router design being "less general than Section 2.1 framing" — Section 2.1 describes routers as separate components (line 52–54), and Section 2.2 clarifies the single-router-per-step choice (line 80); no contradiction exists.

## Novel Insights

The input review's most valuable insight beyond the paper's own contributions is the observation that the power-law path distribution needs a deeper "what does training actually change?" analysis beyond the paper's reporting of exponent values. The review also correctly identifies that the comparison framing could be strengthened by additional controlled experiments, and that the compute-efficiency results would benefit from a complete Pareto frontier rather than a single operating point. These are constructive directions that the paper's own framing ("not focused on beating SOTA") partially addresses but does not fully resolve.

## Suggestions

1. Add a controlled comparison matching total parameters for at least one configuration in each domain, or explicitly state the total-parameter overhead as a limitation.
2. Report training FLOPs and wall-clock time for the main models.
3. Provide a fuller Pareto analysis of the compute-efficiency trade-off (accuracy vs. inference FLOPs across multiple skip rates), including a shallower dense baseline at each compute budget.
4. Clarify the attention grouping mechanism and identity module count in the main text.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>