All key claims verified against the paper. Now writing the final consolidated review.

## Summary

This paper empirically compares the optimization dynamics of SSMs (Mamba, Hyena) and Transformers on synthetic associative recall (MQAR) and copying benchmarks. The central finding is that SSMs exhibit a much narrower window of effective learning rates than Transformers, meaning their reported performance is extremely sensitive to hyperparameter tuning — a factor the authors argue has confounded prior expressivity comparisons. Additional findings include contrasting width-vs-depth scaling preferences, a clean ablation showing the 1D convolution is essential for Mamba's single-layer performance, and an analysis of single-layer training dynamics.

## Strengths

- **The learning rate sensitivity finding (Figure 1, Section 3) is clearly demonstrated and practically important.** The contrast between the wide LR plateau for Attention and the narrow spike for Mamba/Hyena is visually decisive and serves as a genuine caution for practitioners comparing these model classes. The paper shows that prior work (Arora et al., 2023) could have drawn different conclusions with a coarser grid, which is a concrete and useful observation.

- **The convolution ablation (Section 7, Table 2) is a clean mechanistic finding.** Removing the 1D convolution from 1-layer Mamba collapses accuracy to 2% (the same as 1-layer Transformer), while adding a convolution to the 1-layer Transformer raises accuracy to 99%. This pinpoints a specific architectural component that explains part of the expressivity gap and is exactly the kind of falsifiable analysis that distinguishes this paper from a purely observational study.

- **The scaling analysis (Figure 4, Table 1) — width vs depth — is a useful corrective.** The demonstration that a deeper-but-narrower Mamba (24 layers, 1024 width) fails at copying while a shallower-but-wider Mamba (12 layers, 1408 width, same 150M params) succeeds provides concrete evidence that matched-parameter-count comparisons can be misleading.

## Weaknesses

### Fatal
None.

### Major

- **The central thesis on line 39 is internally inconsistent with the paper's own evidence.** The paper states: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics"* (line 39). However, the paper itself acknowledges contradictory evidence:
  - *"while fundamental expressivity issues exist between such model classes, the main driver of poor performance can be an unsuccessful optimization"* (lines 31–32)
  - *"a sizable gap with Transformers can still be observed at low widths (e.g. Hyena)"* (line 140)
  - In Section 7, Mamba without its 1D convolution collapses to 2% accuracy — the same as the Transformer — showing that the convolution (not the SSM recurrence alone) is a key expressivity enabler. This is an architectural/expressivity limitation, not an optimization issue.

  The abstract uses a more defensible formulation: *"not just in their expressivity but in their fundamental learnability properties."* The paper would be substantially stronger if it consistently adopted this nuanced framing — presenting optimization instability as an important *confounder* that can *exaggerate* expressivity differences, rather than claiming expressivity is not a differentiator at all. **This is a structural framing problem, not a minor wording issue.**

### Minor

- **The quantitative characterization of the LR window width rests on only 5 seeds with min-max ranges.** For a paper whose central claim is that the window is *so narrow* that prior work missed it, 5 seeds is thin for precise statements about window boundaries. Standard deviations or confidence intervals would be more informative than min-max error bars. The qualitative pattern (wide vs narrow) is likely robust, but the quantitative precision claimed implicitly about window width is weaker than it could be.

- **The DeltaNet "Transformer-level robustness" claim (Section 7) is based on only two model dimensions (64 and 256)** — the latter being the maximum supported by the implementation. Claiming DeltaNet achieves "Transformer-level robustness" (line 221) from this limited evidence is overconfident; we do not know whether this holds at larger dimensions or on the copying task.

- **The copying task comparison (Table 1) does not report whether training budget (steps, data) was held constant** across the deep-narrow vs shallow-wide Mamba models. Since these models have different depths (24 vs 12 layers), their training dynamics (e.g., gradient propagation) differ, and this confound is not discussed.

- **The framing regarding language modeling correlation is slightly inflated.** The abstract and introduction describe the benchmarks as "highly correlated with language modeling performance" (line 9, 23), attributing this to prior work. The limitations paragraph (line 235) appropriately calls for downstream validation, but the earlier framing gives a stronger impression of practical relevance than the paper's own evidence supports.

### Trivial
None.

## Nice-to-Haves

- Test whether the narrow LR window persists with cosine LR scheduling (standard in Mamba training), AdamW, or warmup strategies — this would substantially strengthen the claim that the instability matters for large-scale training.
- Analyze whether the optimal LR for SSMs scales systematically with model size or sequence length, which would inform practical recommendations.
- Provide mechanistic evidence (attention map visualizations) to support the induction head hypothesis in Section 6, rather than relying on loss-curve resemblance alone. (The paper does present this as a hypothesis, so this is a desirable addition rather than a correction.)

## Removed Points

These points from the input review were removed with brief justification:

1. **"The paper does not discuss how the LR grid was constructed"** — The paper states experimental details are in Appendix A.2 (line 105), which was stripped by the parser. Per the review rules, this is a parser artifact, not an author omission.
2. **"No analysis with LR schedulers, warmup, or adaptive strategies" / "No comparison with different optimizers" / "No analysis of whether optimal LR scales with model size"** — These are reasonable extensions but go beyond the paper's stated scope. The paper already conducts over 3,000 runs; demanding additional experiment dimensions is not a core weakness.
3. **"The induction head claim (Section 6) needs mechanistic evidence or should be softened"** — The paper already uses conditional language: "resembles," "we hypothesize that during this phase transition, the Attention mechanism *attempts* to form induction heads." It is presented as a hypothesis, not a definitive finding, so this criticism overstates the problem.

## Novel Insights

The most interesting observation from reviewing this paper critically is the internal tension between its strong central thesis ("not in terms of expressive power") and its own evidence. This tension is not a sign of flawed science — the empirical results are solid — but it reveals something about how optimization-focused papers are framed. The authors appear to have two competing goals: (1) establishing optimization as an *overlooked* factor (which requires a strong counterpoint to the expressivity-focused narrative), and (2) being honest that expressivity gaps also exist. These goals collide on line 39. The paper's actual contribution is more interesting than either extreme position: it shows that optimization and expressivity *interact* in ways that simple theoretical comparisons miss, and that the right question is not "which one matters?" but "how do they trade off?" This interactive perspective is never explicitly stated but is implicit in the paper's best findings (e.g., the convolution ablation simultaneously reveals an expressivity dependency and an optimization dependency).

## Suggestions

1. **Reframe the central thesis** to match the paper's actual evidence: replace the strong claim on line 39 with the more nuanced version already present in the abstract and conclusion ("lies not just in their expressivity but in their fundamental learnability properties"). Acknowledge upfront that expressivity differences exist alongside optimization differences, and position the paper's contribution as showing that optimization is a *confounding factor* that can exaggerate or mask expressivity gaps.
2. **Increase seed count** for the LR grid characterization (Figure 1) and report confidence intervals rather than just min-max ranges, to strengthen the quantitative claim about window narrowness.
3. **Add a training-budget control statement** to Table 1, or acknowledge the confound explicitly.
4. **Qualify the DeltaNet claim** by noting the dimension limitation in the main text (not just the figure caption), and avoid asserting "Transformer-level robustness" without evidence at larger scales.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>