## Summary

This paper introduces Distributed Neural Architectures (DNAs), a class of models where each token is routed through a collection of modules (transformer blocks, MLPs, attention) via learned routers, generalizing MoE, MoD, weight sharing, and early exit into a single end-to-end trainable framework. The paper validates DNAs on ImageNet classification (~79% accuracy vs ViT-Small's 79.8%) and language modeling on FineWeb-Edu, demonstrating feasibility and providing a rich qualitative analysis of emergent structure: path specialization by semantic category, power-law path distributions, and data-dependent compute allocation. The core contribution is the architecture class itself and the interpretability analysis, not SOTA performance.

## Strengths

- **Genuinely novel architecture class.** DNAs synthesize MoE, MoD, weight sharing, early exit, and layer skipping into a unified framework where connectivity is learned end-to-end. This is a clean, well-motivated generalization that reframes how routing in neural networks can be conceptualized. The proto-architecture (modules + routers, with identity modules for compute control) is a sensible design that enables diverse computational patterns to emerge from a single optimization process.

- **Two-domain validation with consistent qualitative findings.** Demonstrating DNAs on ImageNet (vision) and FineWeb-Edu (language) is substantially stronger than a single-domain proof-of-concept. The qualitative consistency across domains—path specialization, power-law distributions, interpretable routing decisions—lends credibility to the approach.

- **Rich interpretability analysis that goes beyond typical method papers.** The path-specialization visualizations (Fig. 3 for vision, Fig. 8 for language) showing that high-rank paths correspond to specific semantic categories (brass instruments, puzzle pieces, sentence-level attention for "." tokens) are genuinely compelling. The deep-dream-style routing reconstruction (Fig. 4) is methodologically creative and reveals interpretable features developing layer by layer. The compute-allocation analysis (Fig. 5) showing that boundary-rich images require more compute is an interesting behavioral finding. This interpretability work is the paper's strongest contribution.

- **Intellectual honesty about limitations.** The paper explicitly acknowledges that power-law distributions also appear in random models (exponent -1), that language models are "way too small" for the data, that parameter sharing in language appears random rather than structured, and that many improvements are "left on the table." This candor is rare and valuable.

## Weaknesses

### Fatal

None.

### Major

- **No compute-cost measurements despite efficiency motivation.** The paper motivates DNAs by stating "the task of developing methods that save inference compute is critical" (Introduction) and claims models "allocate compute intelligently." Yet it never reports FLOPs, wall-clock time, or throughput for any model. The "active parameters" metric does not account for routing overhead, sparse-attention bookkeeping, or non-contiguous memory access—all well-known to add cost in routed architectures. Without compute measurements, the efficiency framing is untestable. The paper would be stronger if it either (a) reported FLOPs/throughput or (b) de-emphasized efficiency and framed the contribution purely around feasibility and analysis.

### Minor

- **"Competitive with dense baselines" claim modestly overstates the evidence.** The vision Top-1 DNA trails ViT-Small by 0.7% (79.1 vs 79.8%) with no cost accounting; the language Top-1 DNA (matching GPT-2's 406M active params) is worse on 6/8 benchmarks; the Top-2 DNA (433M active params, 27M more) is better on 6/8. This is better described as "approaching baseline performance." Given the paper's stated goal is feasibility (footnote 3), this is a framing issue rather than a fatal flaw, but it matters for first impressions.

- **Power-law finding lacks needed caveats in abstract/conclusion.** The paper correctly discloses in Figure 1's caption that random models also exhibit power-law path distributions (exponent -1). However, the abstract and conclusion present the power-law as a signature of DNAs' emergent structure without this caveat. The interesting question—what the exponent difference (-1 for random vs -1.2 for trained) tells us about learned structure—is never analyzed.

- **No error bars or multiple seeds.** For a paper reporting small performance gaps (0.7% on ImageNet, tenths-of-a-point on perplexity), single-run evaluations make it impossible to assess whether these gaps are meaningful noise.

- **Language experiments at severely undertrained scale.** The ~50:1 token-to-parameter ratio (far below the ~2000:1 suggested by scaling laws) means observed patterns (random parameter sharing, mixed benchmark results) may be artifacts of undertraining rather than intrinsic properties of DNAs. While the paper acknowledges this, the abstract and conclusion do not distinguish the strength of evidence across domains.

- **"GPT-2 (30% shallover)" baseline undefined in main text.** This term appears only in Table 3 with a reference to Appendix A, leaving readers to infer its meaning.

- **Vision Top-2 DNA uses substantially different model dimensions** (d_embed=256 vs 384, d_MLP=1024 vs 1536, 4 heads vs 6) from the ViT baseline, complicating attribution of performance differences.

### Trivial

- The conclusion is a single paragraph that restates claims without synthesizing the paper's own limitations or the contrast between vision and language findings.

## Nice-to-Haves

- An ablation comparing learned routing vs. frozen random routing would directly test whether the learned structure contributes to performance beyond what random routing provides. This is the most impactful ablation the paper could add.
- Analysis of what the power-law exponent difference (trained vs. random) actually measures—does a steeper exponent imply more path specialization or something else?
- Analysis of why the Top-2 (30% skip) language model collapses (Table 3: LAMBADA drops from 33.8→23.8, Wiki perplexity from 33.7→52.6).

## Removed Points

- **"Competitive claim not supported" framed as fatal by harsh critic.** Demoted to minor because (a) the paper's stated goal is feasibility (footnote 3), not benchmark dominance, (b) 0.7% on ImageNet does show the approach is in the same performance neighborhood, and (c) the real substantive issue is the missing compute-cost accounting, not the performance gap per se.
- **Power-law "undermines the paper's claims" framing.** Removed the structural/methodological gap framing since the paper does disclose the random-model finding in the body. Retained as a minor framing issue in the abstract.
- **Section-by-section granular notes** (Eq. 1 notation clarity, compute measurement methodology details, conclusion brevity being "brief"). These are observations rather than distinct actionable weaknesses and are mostly absorbed into the weaknesses above or too granular for a final review.
- **Missing error bars described as "evidential issue."** Kept as minor—it's a real concern but doesn't invalidate the core qualitative findings.
- **"No FLOPs" treated as separate from efficiency gap.** Merged into the single "no compute-cost measurements" major weakness.

## Novel Insights

None beyond the paper's own contributions. The interpretability findings—path specialization by semantic category, compute allocation by image boundary complexity, the structured-vs-random parameter sharing contrast between vision and language—are themselves the paper's most novel and valuable outcomes.

## Suggestions

1. **Report FLOPs or throughput for all models.** This is the single most impactful revision. Even a simple estimate (FLOPs per forward pass accounting for routing overhead) would transform the efficiency claims from speculative to substantive.
2. **Reframe "competitive" to "approach baseline performance"** or add the necessary cost accounting to support the stronger claim.
3. **Add the random-model power-law caveat to the abstract** so readers get an accurate first impression.
4. **Add at least one controlled ablation** (learned routing vs. frozen random routing) to measure whether the emergent structure contributes beyond chance.
5. **Report results from multiple seeds** (at least 3) with standard deviations for the main comparisons.

---

### Calibration Anchors

All anchors from `deepreview_13k_calibration`. Round 1 bracketing placed the paper between 5.5 and 7.5.

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `1qq1QJKM5q` (More Experts Than Galaxies) | 5.67 | R1 | Similar modular-routing paper, accepted. Weaker novelty (fixed random routing vs. learned routing), similar missing-cost-analysis weakness. The paper under review has stronger novelty and better interpretability analysis. |
| `QHzzAU7Qf9` (Soft Merging of Experts) | 6.00 | R1 | Rejected despite 6.0. Differentiated by stronger novelty of current paper (DNAs are more architecturally novel than SMEAR's weight-averaging approach) and richer qualitative analysis. |
| `z1mLNhWFyY` (Gradient Routing) | 5.25 | R1 | Rejected. Current paper is more novel architecturally and has stronger two-domain validation. |
| `cNmu0hZ4CL` (Comparing Noisy Neural Dynamics) | 8.00 | R1 | Different subfield (neuroscience) — less directly comparable. Anchor for the 7.5-8.5 band. |
| `t7P5BUKcYv` (MoE++) | 8.00 | R1 | Efficiency-focused MoE paper with thorough benchmarking. Current paper has stronger architectural novelty but weaker efficiency evidence. |
| `ar9tcnD4e9` (Automatic Organization of Neural Modules) | 4.75 | R1 | Similar theme (modular NNs) but weaker execution. Current paper is clearly stronger. |
| `XVHXVdoV11` (Collective Model Intelligence) | 3.40 | R1 | Model merging paper. Less related. Confirms lower band. |

**Round 1 bracket**: 5.5–7.5. The paper is clearly above rejected papers in the 3.0–5.5 range due to genuine architectural novelty and strong interpretability analysis. It is below the 8.0 band due to missing compute-cost measurements and some evidential gaps.

**Final score determination**: Anchored against "More Experts Than Galaxies" (5.67, accepted) — the paper under review has stronger architectural novelty and richer analysis but shares the missing-cost-measurement weakness. Against "Soft Merging of Experts" (6.00, rejected) — the paper under review has stronger novelty. The final score of **6.0** reflects a borderline-accept paper with a solid core contribution that would benefit from addressing the compute-cost gap.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>