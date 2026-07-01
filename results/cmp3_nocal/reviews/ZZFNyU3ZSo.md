## Summary

This paper analyzes token redundancy patterns across tasks and layers in unified multimodal transformers (Show-o, Emu3, JanusFlow, Lumina-mgpt), then proposes UniMoD — a task-aware token pruning method that assigns separate routers for generation and understanding tasks. Applied to Show-o and Emu3, it reports 15% and 40% FLOPs reductions respectively while maintaining broadly comparable benchmark performance.

## Strengths

- **Thorough empirical analysis (Section 3).** The investigation of attention weight patterns, ARank-based token redundancy, and task interactions across four unified transformer families (Figures 2, 3) is careful and yields a genuine insight: token redundancy varies systematically by task and by layer within a task. This provides concrete motivation for why a single-router MoD would underperform in unified models — stronger motivation than most efficiency papers provide.

- **Clean ablation study (Table 5).** Comparing Basic MoD (single router, interleaved layers), "w/o layer switch" (separate routers at interleaved layers), "w/o task-aware router" (single router at ARank-selected layers), and full UniMoD cleanly isolates the contribution of each component. The collapse on GenEval (0.61→0.15 for Basic MoD) is a convincing demonstration that both task-specific routing and ARank-based layer selection are necessary.

- **Meaningful efficiency gain on Emu3.** The 40% FLOPs reduction (89.0→53.5 TFLOPs) on an 8.5B-parameter unified model represents the kind of savings that justifies the added complexity of task-specific routing.

## Weaknesses

### Major

- **Emu3 headline result is on a re-implementation, not the published model.** The paper states (line 242): "Our full Emu3 results differ from the original paper because we use alternative training datasets, as the official code and data are not publicly available." The "Emu3" baseline in Table 3 is therefore the authors' own training run (using LLaVA-v1.5-mix-665K and different T2I data), not the published Emu3. Whether the 40% FLOPs reduction and accuracy trade-offs transfer to the actual Emu3 model with its original training setup is unverified. The paper is transparent about this, but the headline efficiency claim rests on evidence that cannot be validated against the published model.

- **Main results table (Table 3) omits the most relevant baseline.** The table compares UniMoD against only Full Computation, Interleaved Layer Skipping (removes all tokens from every other layer — an extreme strategy), and Early Exit at layer 12 (also extreme). The proper comparison — vanilla MoD with a single router — appears only in the ablation study (Table 5). Since Table 3 and Table 5 use different metric sets, a direct side-by-side comparison of UniMoD against its most natural prior-art baseline is not available in the main results. This presentation choice weakens the evidentiary force of the paper's central empirical claim.

- **Performance regressions on understanding benchmarks are understated.** The abstract claims "maintaining or improving performance on several benchmarks." However, comparing UniMoD to the full-computation baseline (Table 3) shows:

  Show-o: GQA 56.3→54.5 (−1.8), VQAv2 68.3→66.2 (−2.1)
  Emu3: GQA 46.0→45.2 (−0.8), POPE 76.0→74.7 (−1.3), VQAv2 54.8→53.9 (−0.9)

  These drops are not trivial and receive no discussion. A more accurate framing would be "modest regression on several understanding benchmarks in exchange for FLOPs savings."

### Minor

- **Marginal wall-clock gains on Show-o.** The 15% FLOPs reduction yields training speed of 1.27×/iter vs. 1.30×/iter (≈2.3% improvement) and memory reduction of 67→64G (≈4.5%) — practically negligible for most setups. The method's practical efficiency argument rests heavily on the Emu3 results.

- **No statistical variance reported.** All benchmark numbers are single values with no error bars, multiple seeds, or standard deviations. For metrics like MME, GQA, and POPE, this makes it impossible to distinguish signal from noise.

- **Layer switch module sensitivity not analyzed.** The ARank-based layer selection uses 50 samples per task and selects "half of layers with the lowest values." No analysis is provided of how sensitive the final performance is to (a) the number of samples, (b) the "half" threshold, or (c) ranking stability across data subsets.

- **"Last 12 layers" (Section 5.1) vs. ARank-based selection (Section 4.1) needs clarification.** Section 4.1 describes layer selection via ARank values, while Section 5.1 states "we transform the last 12 layers into MoD layers for both tasks." These may be consistent if the bottom half of ARank values corresponds to the last 12 layers, but the paper does not explain this correspondence, creating confusion about whether ARank analysis drives the design or post-hoc justifies it.

- **Observation 5 could be confounded by loss scaling.** The competitive pruning experiment (Figure 4) shows generation tokens are retained more than understanding tokens, interpreted as them being "more important." If the two task losses are not equally weighted in the Gumbel-Softmax training, the asymmetry could reflect loss-scale imbalance rather than inherent token importance. Loss weighting is not reported.

- **Table 1 anomaly: GQA=0.0 when layer 3 is skipped.** Skipping layer 3 causes complete failure — a far more dramatic effect than any other layer. This striking data point receives no discussion.

### Trivial

- The paper does not analyze what fraction of image vs. text tokens are pruned by each task-specific router, which would directly validate whether the task-aware design works as intended.

## Nice-to-Haves

- Reporting results over 3 random seeds with standard deviations would substantially strengthen evidential confidence.
- Separately ablating the "which layers to convert" decision from the "what pruning ratio to use" decision would clarify the source of benefit.
- Breaking down pruned tokens by modality (image vs. text) per task would validate whether the routers learn sensible patterns.

## Removed Points

These points are flagged per filtering rules; treat with caution:

- **γ-MoD / MoMa comparison request.** Asking for empirical comparison against methods designed for different architectures (γ-MoD uses MLLMs; MoMa uses Chameleon) constitutes scope creep. The paper cites both in related work.
- **"Line chart suggests visual inspection" characterization.** The ARank procedure is numerically well-defined (compute ARank per layer, select bottom half); "line chart" refers to how values are presented, not how they are computed.
- **Appendix-deferred claims (Pareto frontier, scaling, diffusion adaptation).** These sections exist in the original submission appendix, which the review setup strips.

## Novel Insights

Beyond the paper's own contributions, the input reviews surface two genuine issues: (1) the strategic placement of the vanilla MoD comparison in the ablation table rather than the main results table makes the paper's evidence look stronger than it is, and (2) the paper's framing of "maintaining or improving performance" papers over non-trivial accuracy regressions on understanding benchmarks. Both are presentation/evidence issues, not flaws in the method itself.

## Suggestions

1. **Move the Basic MoD (vanilla single-router MoD) comparison from the ablation table into the main results table** (Table 3), so readers can directly evaluate UniMoD against its most relevant prior-art baseline alongside the FLOPs and accuracy numbers.

2. **Either validate the Emu3 results on the original model/data when available, or explicitly reframe the Emu3 experiment as a proof-of-concept** on a re-implementation with appropriate caveats about transferability.

3. **Acknowledge and discuss the performance regressions** on GQA, VQAv2, and POPE explicitly, rather than using the blanket phrase "maintaining or improving performance."

4. **Clarify the relationship between "last 12 layers" (Section 5.1) and ARank-based selection (Section 4.1)** — specifically whether the ARank analysis selects these same layers and how the correspondence was verified.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>