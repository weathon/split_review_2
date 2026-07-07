## Summary

This paper introduces Distributed Neural Architectures (DNAs), a framework where each token/patch can follow an arbitrary path through a collection of computational modules (transformer blocks, MLPs, attention, etc.), with routing decisions learned end-to-end. DNAs are positioned as a conceptual generalization of MoE, MoD, weight sharing, and early exit. The paper trains DNA models in vision (ImageNet classification at ViT-Small scale) and language (language modeling at GPT-2 Medium scale), showing they are competitive with dense baselines. It further provides creative interpretability analyses (path distribution power-laws, deep-dream-style routing reconstructions, path specialization visualizations) and demonstrates that compute efficiency can be learned from data.

---

## Strengths

- **Conceptual unification of conditional computing approaches.** The paper correctly identifies that DNAs subsume MoE, MoD, early exit, and weight sharing under a single framework (Section 1). The fact that a trained DNA can exhibit a "mixture-of-all-of-these-methods" is a genuinely interesting property that a standard fixed-architecture transformer cannot match. This conceptual contribution is the paper's strongest asset. *(Weight: +4.49)*

- **Interpretability analysis is genuinely creative and goes beyond what is standard.** The deep-dream-style reconstruction of images from routing decisions (Fig. 4), the visualization of path specialization by rank (Fig. 3, Fig. 8), and the finding that boundary patches consume more compute (Fig. 5) are clever analyses that generate interesting hypotheses about how the model organizes its computation. *(Weight: +6.04)*

- **Cross-domain validation at non-trivial scales.** Demonstrating the approach in both vision (ImageNet classification with ViT-Small) and language (language modeling with GPT-2 Medium + downstream tasks) strengthens the claim of generality. The top-2 DNA model's competitive performance across multiple benchmarks (Table 3) is notable given the framework's additional flexibility. *(Weight: +5.05)*

- **Honest reporting of mixed results.** The paper does not hide results that go against its narrative: module reuse in language is "most likely random" (Section 4.3), reconstruction-based classification yields low confidence (44–55%, Fig. 4), and language models are acknowledged as "way too small" and "vastly underparametrized" (Section 4 opening). This candor is rare and should be credited. *(Weight: +2.91)*

---

## Weaknesses

### Major

- **Missing comparisons against the methods DNA claims to generalize (MoE, MoD).** The paper positions DNA as a "natural generalization" of MoE, MoD, and weight sharing (Abstract, Section 1), yet compares *only* against dense baselines (ViT-small, GPT-2 medium). Without MoE/MoD baselines of comparable size and total parameter count, we cannot determine whether the additional flexibility of arbitrary routing between all modules provides any benefit over structured routing. If a standard MoE transformer matches or exceeds DNA, the main claim reduces to "a more complex architecture can match a simpler one." If DNA outperforms MoE, that would be a strong result. The paper provides neither. *(Weight: -3.92)*

- **The restricted attention mechanism is a fundamental architectural property whose implications are not analyzed.** As stated in the Fig. 1 caption, tokens only attend to other tokens routed to the *same* module. This means long-range dependencies can only be captured if two tokens consistently co-occur in the same attention module, and the model cannot perform all-pairs attention within the context window. The paper frames this as "dynamic sparsity" but does not analyze whether this creates a bottleneck for tasks requiring long-range cross-token interaction (e.g., coreference resolution in language, object-part reasoning in vision). Given that the models are competitive but not better than dense baselines, this restricted attention is a plausible bottleneck — but the paper does not investigate this hypothesis. *(Weight: -2.25)*

### Minor

- **The power-law path distribution finding is over-interpreted.** The paper acknowledges that *random* routing through the DNA architecture also produces a power-law (Fig. 1 caption), meaning the heavy-tailed distribution is primarily a consequence of the architecture (number of modules, steps, branching factor), not of learning. The claimed shift in exponent from -1 to -1.2 is presented as a key finding (abstract, Fig. 1) without error bars or statistical tests, and there is no comparison to a null model controlling for architectural parameters. *(Weight: -4.16)*

- **Interpretability claims rely on qualitative examples without systematic quantification.** The path specialization analysis (Sections 3.2, 4.2) depends on visual inspection of selected patches/tokens. While the paper compares against a random baseline — which is good practice — the comparison itself is qualitative ("very different similarity measure... superficial features" without measurement). The paper does not provide quantification metrics such as clustering quality scores, inter-path distance measures, or precision/recall of hypothesized specializations on held-out data. *(Weight: -6.97)*

- **No training cost analysis.** The paper motivates DNAs by citing rising inference costs (Section 1), yet provides zero analysis of training cost. DNAs introduce routers, dynamic token-module assignment, hard top-k sampling with straight-through gradients, and sparse attention that may be hard to batch efficiently. Without training throughput, GPU-hour comparisons, or hardware utilization analysis, the practical overhead of training DNAs versus dense baselines is unknown. *(Weight: -1.08)*

### Trivial

- The backbone design choice (first N_b layers are not routed) is described as necessary for convergence but is not ablated (e.g., N_b=0 is not tested).
- The mapping from the bias-control hyperparameter *r* (Eq. 3) to achieved skip rates (25%, 30%) is not explained.
- It is not stated whether the ViT-small baseline (79.8%) was tuned with the same grid search as the DNA models or taken from prior work.

---

## Nice-to-Haves

- Analyzing the attention bottleneck directly by measuring pairwise attention coverage: what fraction of token pairs attend to each other at least once during the forward pass, and how does this compare to a standard transformer?
- Quantifying the path specialization claims with metrics such as silhouette scores of path-based clustering or precision/recall of hypothesized specializations.
- Reporting training throughput and GPU-hour comparisons between DNA models and dense baselines.
- Testing the necessity of the backbone (N_b = 0) to understand whether the fixed early layers are truly required.

---

## Removed Points

These points were flagged by the harsh critic but removed from the main review for the following reasons:

- *Missing related works* — Removed per instructions (cannot verify literature completeness without external sources).
- *Formatting/style nitpicks and appendix references* — Removed per instructions (parser strips formatting and appendices; these are parser artifacts, not author errors).
- *Criticism that "Section 2.2 Eq. 1" is awkward* — The paper already acknowledges this ("somewhat awkward form," footnote 4). This is transparent reporting, not a weakness.
- *Language models being "underparametrized"* — The paper acknowledges this explicitly (Section 4 opening). The reviewer's concern is already addressed by the paper's own candor.
- *Different configs between vision and language models (Table 1 vs Table 2)* — Different domains naturally require different configurations; this is not a meaningful criticism.
- *Module reuse in language contradicts vision findings* — The paper explicitly and honestly discusses this discrepancy (Section 4.3), making it a strength of the paper's reporting rather than a weakness.
- *Claim that interpretability findings are "cherry-picked"* — Retained in weakened form as "qualitative without systematic quantification" (Minor tier). The paper does include a random baseline comparison, which partially mitigates the concern, but the analysis remains qualitative.

---

## Novel Insights

The harsh critic's most insightful observation is that the restricted attention mechanism (tokens only attending to co-located tokens in the same module) is not merely "dynamic sparsity" but a fundamentally different computational primitive whose implications for long-range dependencies are not analyzed. This is a genuinely useful framing that goes beyond what the paper itself provides. The critic also correctly identifies that the power-law finding's significance is limited by the fact that random architectures also produce power-laws — the interesting question is whether the exponent shift is meaningful, which the paper does not establish.

---

## Suggestions

1. **Add MoE baselines of comparable size.** This single addition would transform the paper. If DNA outperforms MoE, the contribution is significantly strengthened. If it matches, the narrative shifts to "a more general framework matches a special case." This is the single most important missing experiment given the paper's own framing.

2. **Analyze the attention bottleneck directly.** Measure pairwise attention coverage — what fraction of token pairs attend to each other at least once during a forward pass? How does this compare to a standard transformer? This would clarify whether the restricted attention is a bottleneck or a feature.

3. **Quantify the interpretability claims with metrics.** Compute silhouette scores of path-based clustering compared to baselines, or measure precision/recall of hypothesized path specializations on held-out data.

---

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| KaYXsoCxV7.md (ViMoE) | 3.00 | R1 | Yes | Significantly weaker — had marginal performance gains, unfair comparisons, no theory. My paper has genuine conceptual novelty. |
| 762u1p9dgg.md (MOEfication) | 3.40 | R1 | No | Similar theme but different contribution type. |
| XVHXVdoV11.md (Collective Model Intelligence) | 3.40 | R1 | No | Different approach (model merging), less relevant. |
| uWvKBCYh4S.md (Mixture of LoRA Experts) | 5.00 | R1 | No | Applied MoE for LoRA fusion, different technical focus. |
| 1qq1QJKM5q.md (More Experts Than Galaxies) | 5.67 | R1 | Yes | Most similar in profile — new architecture with interesting properties but missing analyses. My paper has slightly stronger negative weights on interpretability and power-law. |
| Pu3c0209cx.md (Tight Clusters) | 7.00 | R1 | Yes | Strong theory + thorough experiments. My paper lacks this level of rigor. |
| t7P5BUKcYv.md (MoE++) | 8.00 | R1 | Yes | Clear practical improvements with thorough experiments. My paper is not at this level. |
| fmWVPbRGC4.md (Local vs Distributed) | 5.67 | R2 | Yes | Analysis-heavy paper with moderate empirical scope. Similar profile but different domain. |

**Weighted-item comparison grounding:** The paper's strongest positive items (interpretability analysis +6.04, cross-domain +5.05) are comparable to the "More Experts Than Galaxies" anchor's top items (+6.27 for clarity/methodology, +4.20 for novelty). However, the paper's strongest negative items (interpretability qualitative at -6.97, power-law at -4.16, missing baselines at -3.92) are more severe than that anchor's negatives (strongest: -4.63 for unrealistic expert counts, -3.30 for no code). This places the paper slightly below the 5.67 anchor. The paper is clearly above ViMoE (3.00) which had fatal flaws. **Round 1 bracket: 4.0–6.0. Final score: 5.0** — the paper has genuine conceptual contributions and creative analysis that justify a borderline score, but the missing key baselines and qualitative-only evidence prevent a higher rating.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>