Now I have all the data I need. Let me construct the final review.

## Summary

This paper introduces Distributed Neural Architectures (DNA), a generalization of conditional computing that unifies Mixture-of-Experts, Mixture-of-Depths, early exit, and weight sharing into a single trainable proto-architecture. Tokens/paths are routed through computational modules with learned routing decisions, and the model can learn to skip modules for compute efficiency. The paper validates the approach in vision (ViT-Small scale on ImageNet) and language (GPT-2 Medium scale on FineWeb-Edu), showing competitiveness with dense baselines, and provides extensive qualitative analysis of emergent routing specialization.

## Strengths

- **The DNA framework genuinely generalizes multiple lines of conditional computing work.** Mixture-of-Experts, Mixture-of-Depths, early exit, and weight sharing all emerge as special cases of the same proto-architecture (Sec. 2.1–2.2). End-to-end training of both module parameters and routing decisions with no fixed notion of depth or width is a meaningful step beyond existing approaches that typically route only along one axis.

- **Two-domain validation at non-trivial scale.** The Top-2 DNA language model (433M active params) outperforms GPT-2 Medium (406M) on 6 of 8 benchmarks, including validation loss (2.674 vs 2.720) (Table 3). This suggests the architecture is not just viable but potentially advantageous in the language domain even without load-balancing or efficiency-oriented training.

- **Unusually thorough qualitative interpretability analysis.** Figures 3, 4, 5, and 8 provide rich visualization of path distributions and routing specialization — some paths focus on object boundaries, others on background, others on specific semantic categories (brass instruments, puzzle pieces). The deep-dream-style routing visualization (Fig. 4) is creative and reinforces the interpretability narrative.

- **Intellectual honesty about scope.** The paper explicitly states it is "not focused on beating SOTA models" but on demonstrating feasibility and analyzing emergent structure (Footnote 3). It candidly acknowledges when findings are weaker than they appear — e.g., random models also produce power-law path distributions (Fig. 1 caption), and language model parameter sharing "is most likely random" (Sec. 4.3).

- **The efficiency-by-skip mechanism** with identity modules and bias-based control (Sec. 2.2, Eqs. 2–3) provides a clean framework for learning per-token compute budgets without auxiliary losses beyond the routing signal.

## Weaknesses

### Major

- **No actual runtime or FLOPs measurement despite efficiency motivation.** The paper's efficiency analysis (Sec. 3.3) measures "compute" as a count of non-identity module activations per token — a proxy that ignores routing overhead, dispatch/recombination costs, and sparse attention gather/scatter operations. The introduction motivates DNAs by arguing that "developing methods that save inference compute is critical" (Sec. 1), and the abstract/conclusion highlight compute efficiency. Yet no FLOPs, wall-clock time, or throughput measurements are provided. The paper acknowledges that infrastructure co-design is needed (Sec. 2.1) but delegates this to future work, leaving a gap between the stated motivation and what is actually measured. This does not invalidate the architecture contribution but means the efficiency claims are only about a *capability* (the model can learn to modulate compute) rather than a demonstrated practical benefit.

- **No ablation isolating the effect of learned routing.** The paper compares DNAs against dense baselines but never against the same architecture with random or uniform routing at inference time. Without this, it is unclear whether the routing mechanism itself drives the competitive results or whether the architectural flexibility (more modules, different connectivity patterns) is responsible. The paper shows that random *weight* initialization produces power-law path distributions (Fig. 1), but this does not substitute for an inference-time random-routing ablation. A minimal test — fixing routing decisions to random assignments on the trained architecture and measuring accuracy — would directly validate whether learned routing contributes meaningfully.

- **No multi-seed or variance reporting.** Results are reported as "the best run of each model" after hyperparameter grid search (Sec. 3.1, 4.1), with no standard deviations or indication of run-to-run variance. The vision accuracy gaps are small (0.7% for Top-1 DNA vs ViT), and the language loss difference (0.046) is modest. Without variance estimates, the reader cannot assess whether these differences are significant or within noise, especially given the complexity of routing-based training which could have higher variance than standard architectures.

### Minor

- **The vision Top-2 DNA comparison is confounded.** From Table 1, Top-2 DNA (25% skip) uses d_embed=256, N_head=4, and 18M active params vs. ViT's 384/6/22M. The 1.0% accuracy gap (79.8% vs 78.8%) could partially reflect this reduced per-module capacity. The Top-1 DNA comparison (matched d_embed=384, N_head=6) is cleaner, but the compute-efficiency analysis in Sec. 3.3 is conducted on the confounded Top-2 model.

- **No discussion of the attention sparsity constraint.** When tokens are routed to different modules, they cannot attend to each other (Sec. 2.2). This is a strong architectural choice that could limit performance on tasks requiring long-range cross-token interactions. The paper does not discuss when this constraint might be harmful or how it compares to full attention.

- **No analysis of training stability.** Routing architectures are known to be difficult to train (load balancing collapse, router saturation). The paper mentions hard top-k sampling (Sec. 2.2) but does not discuss whether training was stable, whether any configurations collapsed, or whether the grid search was driven by stability concerns.

- **The power-law finding is presented as a main result** (abstract, conclusion) but both trained and random models produce power-law path distributions (exponent ~-1 for random, ~-1.2 for trained language). The paper acknowledges this but does not analyze what the exponent difference signifies, making the finding less informative than its prominence suggests.

### Trivial

None.

## Nice-to-Haves

- Quantify the interpretability claims (e.g., clustering purity of patches/tokens assigned to the same path, mutual information between path rank and token label) to complement the qualitative visualizations.
- Provide a FLOPs breakdown (routing, each module type, dispatch/recombination overhead) to either validate the compute-savings claims or properly constrain them.
- Add a random-routing ablation at inference time to directly test whether the learned routing mechanism contributes beyond architectural flexibility.

## Removed Points

These points are flagged to be removed, treat them with caution:

- The harsh critic's statement that "the entire efficiency motivation is evaluated with no runtime measurement" was retained as a Major weakness but reframed from "structural — undermines the paper's stated motivation" to "no actual runtime measurement despite efficiency motivation." The paper's primary contribution is the architecture and feasibility framing; the weakness is a gap between motivation and measurement, not a fatal flaw.
- The harsh critic's claim about "GPU utilization drives quality (line 14) is slightly off" — this is a minor framing quibble about a citation reference, not a substantive weakness.
- The harsh critic's "the power-law finding is less informative than claimed" observation was retained as a Minor weakness but contextualized since the paper already acknowledges the random-baseline finding.
- Generic section-by-section notes and "strengthening the paper on its own terms" suggestions have been absorbed into Nice-to-Haves or Minor weaknesses where concrete.
- The harsh critic's criticism about "missing parts" (no discussion of attention sparsity, no analysis of training stability) were kept but downgraded to Minor since these are addressable without invalidating results.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one of: (a) actual FLOPs/throughput measurements, (b) a random-routing inference ablation — preferably both. These directly address the two most significant empirical gaps.
2. Report multi-seed results (mean and std) for all main comparisons. Three seeds per configuration would suffice to address variance concerns.
3. Explicitly discuss the attention sparsity constraint — when it might be beneficial vs. harmful, and what architectural alternatives exist.
4. Either provide deeper analysis of the power-law exponent difference between trained and random models, or de-emphasize the finding.

## Score and Decision

**Calibration summary (all anchors retrieved across rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| Tight Clusters Make Specialized Experts (Pu3c0209cx) | 7.00 | 1 | Yes | Cleaner execution with theoretical proofs, but narrower in scope. DNA paper is more ambitious. |
| Soft Merging of Experts (QHzzAU7Qf9) | 6.00 | 1 | Yes | Rejected for limited novelty and small scale. DNA paper has broader validation and more novel architecture. |
| γ-MoD (q44uq3tc2D) | 6.67 | 2 | Yes | Similar quality level — both have architectural contributions and practical gaps. |
| MoE++ (t7P5BUKcYv) | 8.00 | 1 | Yes | Superior empirical validation with actual throughput measurements. DNA paper lacks this rigor. |
| ViMoE (KaYXsoCxV7) | 3.00 | 2 | Yes | Much weaker — only CIFAR experiments, marginal improvements. DNA paper is clearly stronger. |
| COMET (1qq1QJKM5q) | 5.67 | 2 | Yes | Similar novelty level but DNA paper has stronger two-domain validation and richer interpretability. |
| More Experts Than Galaxies (1qq1QJKM5q) | 5.67 | 1 | No | Also about fixed routing; DNA paper's learned routing is a different approach. |
| NeurFlow (GdbQyFOUlJ) | 6.50 | 3 | No | Interpretability-focused; different sub-area. |
| Circuit Component Reuse (fpoAYV6Wsk) | 6.50 | 3 | No | Mechanistic interpretability; different sub-area. |

**Bracket determination (Round 1):** The paper clearly sits above the 3.00–5.67 range (ViMoE, COMET) and below the 8.00 level (MoE++). The closest matches are in the 6.00–7.00 band. **Initial bracket: [6.0, 7.0].**

**Narrowing (Round 2–3):** Comparing favorability-rated items: the DNA paper's top strengths (11–12 favorability) match those of Tight Clusters (7.00) and γ-MoD (6.67), but its lowest weakness (routing ablation at -1.19) is more severe than Tight Clusters' weakest items (which bottom out around 1.66). The routing ablation gap and missing FLOPs measurement are concrete omissions that Tight Clusters and γ-MoD do not share. This places the paper slightly below Tight Clusters (7.00) but above SMEAR (6.00/reject) and COMET (5.67/accept). **Final score: 6.5.**

The paper makes a genuine contribution as a feasibility study proposing a new architecture class. The limitations (no FLOPs measurement, no routing ablation, no variance reporting) are real but fixable and do not invalidate the core contribution. The strong interpretability analysis and two-domain validation demonstrate that the architecture is viable and produces interesting emergent behavior.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>