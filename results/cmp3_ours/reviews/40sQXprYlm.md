## Summary

This paper introduces Distributed Neural Architectures (DNAs), where each token follows a learned path through a collection of computational modules, with connectivity, compute allocation, and parameter sharing emerging from end-to-end training. DNAs generalize MoE, MoD, parameter sharing, and layer skipping under a single framework. The authors train DNA models in both vision (ImageNet, ~ViT-Small scale) and language (FineWeb-Edu, ~GPT-2 Medium scale), demonstrating feasibility and analyzing emergent structure including power-law path distributions, module specialization, and interpretable routing patterns.

## Strengths

1. **Genuinely novel core idea.** DNAs generalize MoE, MoD, parameter sharing, early exit, and layer skipping under a single framework where connectivity and specialization emerge from training. The framing (Section 2.1, Minsky 1986 inspiration) is coherent and the direction is well-motivated.

2. **Insightful interpretability analysis.** Figures 3 and 8 provide compelling evidence of emergent specialization: frequently-used paths aggregate patches sharing high-level features (edges, flat color) while rare paths correspond to specific visual concepts (brass instruments, puzzle pieces). The language analysis showing early routers group semantically similar tokens (Section 4.2) is similarly substantive. These analyses go well beyond typical "routing works" demonstrations.

3. **Intellectual honesty throughout.** The paper explicitly acknowledges: models are underparametrized for language (Section 4), the work is not about beating SOTA (footnote 3), parameter sharing in language is "most likely random" (Section 4.3), and the power-law behavior is partially shared with random models (Figure 1 caption). This candor is valuable.

4. **Two-domain demonstration** (vision + language) with broadly consistent findings strengthens the generality of the approach.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The "competitive" framing in the abstract is slightly stronger than the cleanest interpretation of the evidence.** The top-1 DNA (vision) has 34M total params vs ViT's 22M total but achieves 79.1% vs 79.8% — at the same active param count (22M), it underperforms by 0.7%. The top-1 DNA (language) has 583M total params vs GPT-2's 406M and achieves worse loss (2.754 vs 2.720). The top-2 DNA outperforms GPT-2 on several benchmarks but with 27M more active params (433M vs 406M) and 197M more total params. Footnote 3 clarifies the feasibility framing, so this is a presentation issue rather than a substantive flaw, but pairing "competitive" in the abstract with comparisons that sometimes favor the DNA models by larger parameter budgets creates a slightly misleading impression.

2. **Compute efficiency evaluation lacks baselines against standard methods.** The paper demonstrates that DNAs can learn to skip compute with graceful degradation, but does not compare against simpler alternatives: training a smaller ViT at the same compute budget, stochastic depth, or pruning. Without such calibration, the reader cannot evaluate whether the learned compute allocation is more efficient than standard approaches. (The language section partially addresses this by including a shallower GPT-2 baseline in Table 3, but the vision section has no comparable baseline.)

3. **Ablations of key design choices are absent.** The paper does not systematically vary the number of modules (N_m), backbone layers (N_b) beyond the 0/1/2 range used across experiments, top-k values beyond 1 and 2, or the importance of the identity-module bias trick for encouraging skipping. For a feasibility study introducing a new architecture with several free design parameters, these ablations would be more informative than additional benchmarks.

4. **The attention sparsity mechanism is noted but not analyzed.** The paper states (Figure 1 caption) that when a module with attention acts on a subset of tokens, attention is computed only between those tokens, making attention a dynamic sparse operation. This is a potentially significant design feature that affects effective receptive field, training dynamics, and actual compute savings, but receives no dedicated analysis.

5. **No variance or multi-seed reporting.** All results are reported as single best-run numbers from hyperparameter searches. While single-seed reporting is common at this scale, multi-seed results would strengthen the comparative claims.

6. **The implemented architecture is less flexible than the aspirational framing suggests.** The actual implementation uses a fixed sequence of routers (one per token-processing step) rather than arbitrary connectivity between any pair of modules (Section 2.2). The paper should more precisely describe what "distributed" means in the implemented architecture vs. the general vision.

### Trivial
None.

## Nice-to-Haves

- Adding stochastic depth, pruned ViT, or smaller ViT baselines for the compute efficiency experiments in vision
- Multi-seed reporting for key experiments
- Ablating the backbone (N_b) to test whether a "dense foundation" is a necessary design choice or an emergent property
- Analyzing how the dynamic sparse attention affects effective receptive field and training dynamics

## Removed Points

These points from the harsh critic were removed with justification:

1. **"The power-law finding is partially an artifact that the paper acknowledges but does not reckon with"** — This criticism is undercut by the paper's own explicit discussion. The paper reports (Figure 1 caption) that random models also show power-law distributions, and Section 3.2 acknowledges that random models can cluster images. The interpretability analysis focuses on what specific paths route (content, concepts), not on the power-law distribution itself. The issue is already addressed by the paper.

2. **Criticism about "matching ViT-small in active parameters" for top-2 DNA** — Factually incorrect: top-2 DNA has 18M active params, ViT-small has 22M active params. This specific sub-claim is removed; the broader point about comparison confounds is retained in Weakness #1.

3. **Criticism that the paper doesn't explain what "reused" means in parameter sharing** — In context (Section 3.3: "weight-sharing distribution is roughly gaussian with 25% and 15% of parameters reused"), the meaning is sufficiently clear: across the dataset, a fraction of module parameters are activated through shared routing.

4. **Criticism that the lack of "statistical significance or variance" is a fatal issue** — Demoted to Minor weakness #5. Single best-run reporting is common practice at this scale; its absence is a limitation but not a fundamental flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Recalibrate the abstract's "competitive" claim** to match the feasibility framing, e.g., "trained DNAs achieve performance within 1% of dense baselines while enabling emergent specialization and interpretable routing."

2. **Add one controlled comparison** for each domain: e.g., a ViT with the same total parameter count as the top-1 DNA (34M), and a GPT-2 with matching total parameters. This would clarify whether any performance gaps are due to the DNA architecture or simply parameter inefficiency.

3. **Benchmark compute efficiency against at least one standard baseline** in vision (e.g., a smaller ViT, or ViT with stochastic depth) to calibrate whether the learned allocation is more efficient than naive alternatives.

4. **Add ablations of backbone depth (N_b) and number of modules (N_m)** to help readers understand which design choices are critical.

## Score and Decision

All anchors retrieved across calibration rounds:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| KaYXsoCxV7 (ViMoE) | 3.00 | R1 | Much weaker novelty, marginal improvements, limited experiments. DNA paper is clearly stronger. |
| hJDTuVQcQp (Adaptive Inference) | 4.20 | R1 | Interesting theory but flawed execution. DNA paper has stronger empirical contribution. |
| irorVob9Eq (CapsNet analysis) | 5.67 | R1 | Analysis-only paper with limited scope. DNA paper proposes new architecture plus analysis across two domains. |
| 2J18i8T0oI (Towards Universality) | 6.50 | R1 | Well-executed analysis with minor novelty concerns. Comparable quality to DNA paper. |
| 52UtL8uA35 (DLGN) | 6.75 | R1 | Novel architecture + analysis, more focused experiments. DNA paper has broader scope but weaker experimental rigor. |

**Round 1 bracket**: 5.5 – 7.0  
**Final calibration**: The DNA paper's core contribution (a genuinely new architecture paradigm spanning two domains) is novel enough to place it above the CapsNet analysis paper (5.67). Its weaker experimental rigor (no ablations, single seeds, missing compute baselines) places it slightly below the Towards Universality paper (6.50) and DLGN paper (6.75). A score of **6.0** reflects a borderline-accept paper with real intellectual contributions that would benefit from addressing the experimental gaps — appropriate for a conference interested in architectural exploration.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>