Now I have sufficient calibration data. Let me produce the final review.

## Summary

This paper empirically compares Transformer and SSM (Mamba, Hyena, Mamba2, DeltaNet) learning dynamics on multi-query associative recall (MQAR) and copying tasks across ~3,000 runs. The central finding is that SSMs have an extremely narrow learning rate window for successful training, while Transformers are robust across ~2 orders of magnitude of LR values — a critical confound that can exaggerate expressivity gaps in prior work. The paper also documents opposing scaling behaviors (SSMs benefit from width, Transformers from depth), identifies the 1D convolution as mechanistically critical for single-layer SSM expressivity, and shows that DeltaNet achieves Transformer-level LR robustness.

## Strengths

- **Figure 1 is a compelling diagnostic.** The side-by-side comparison of Attention, Mamba, and Hyena accuracy across a log-scale LR sweep at two model dimensions cleanly demonstrates that SSM success is confined to a narrow LR peak while Attention is robust across ~2 orders of magnitude. The overlay of the Arora et al. (2023) LR grid as vertical dashed lines makes the "confounded evaluation" point visually and concretely. [favorability=14.24]

- **The scale of the empirical study is impressive.** With 3,000+ runs (~20,000 GPU hours), systematic LR sweeps across multiple architectures (Mamba, Mamba2, Hyena, DeltaNet, Attention), sequence lengths, and model dimensions, the findings are built on a strong evidential foundation. [favorability=13.33]

- **The width-vs-depth scaling analysis provides clear practical guidance.** Table 1 is particularly effective: a 12-layer Mamba (1024 width, 80M params) gets 0% on copying, a 24-layer Mamba (1024 width, 150M params) gets 16%, while a 12-layer Mamba (1408 width, 150M params) gets 100% — concretely demonstrating that SSMs should be scaled in width, not depth. [favorability=12.67]

- **Section 7's convolution ablation is crisp and informative.** Showing that Mamba without conv1d drops to 2% (matching the 1-layer Transformer baseline) and that adding a convolution to 1-layer Attention raises it to 99% isolates the convolution as mechanistically critical for single-layer expressivity. [favorability=11.35]

- **The DeltaNet result is a constructive finding.** It shows that Transformer-level LR robustness is achievable in a recurrent model, grounding the paper's thesis that optimization stability is a tractable challenge rather than a fatal limitation of recurrent architectures. [favorability=11.67]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The central thesis at line 39 is somewhat overstated.** The claim "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics" is stronger than what the evidence fully supports. The paper itself shows genuine expressivity differences (1-layer SSMs can solve MQAR while 1-layer Transformers cannot; residual gaps at low widths persist even with optimal LR tuning). The more precise framing in the abstract — "a crucial differentiator lies not just in their expressivity but in their fundamental learnability properties" — is better supported. The paper should soften line 39 to acknowledge that both expressivity and optimization contribute to observed gaps. [favorability=5.89]

- **The mechanistic explanation for LR instability is hypothesized but not directly measured.** The paper attributes the narrow LR window to vanishing/exploding gradients in the SSM's recurrent structure (lines 23, 221) but provides no gradient norm diagnostics, Hessian analysis, or loss landscape measurements. Without these, it is impossible to distinguish the proposed explanation from alternatives (sharp minima, poor conditioning, etc.). This is the single most impactful missing piece of evidence. [favorability=0.33]

- **The induction head analysis in Section 6 is speculative.** The paper observes a loss bump and hypothesizes it "resembles the formation of an induction head circuit" without any mechanistic verification (attention pattern analysis, head-by-head inspection, or causal intervention). The analysis would be strengthened by showing attention maps or explicitly acknowledging alternative explanations for the loss bump. [favorability=3.77]

### Trivial

- **The paper uses "relative max-min errors" across 5 seeds for variance reporting**, which is non-standard and outlier-sensitive. Standard deviation or per-seed visualizations would be more informative, especially given that LR sensitivity is central to the paper's claims. [favorability=-1.65]

- **The paper focuses on LR sensitivity but sometimes generalizes to "optimization instability" more broadly.** Only LR is systematically varied; other optimization dimensions (Adam betas, weight decay, gradient clipping, warmup schedule) are not explored. Acknowledging this scope limitation would improve precision. [favorability=0.22]

## Nice-to-Haves

- Adding gradient norm diagnostics across the LR sweep for each model would substantiate the proposed vanishing/exploding gradient mechanism and significantly strengthen the paper.
- Extending a subset of findings to a small-scale language modeling task (e.g., Wikitext-103 with small models) would broaden the paper's impact beyond synthetic benchmarks.
- The induction head section could be dropped or significantly compressed if mechanistic verification is not feasible, as it does not carry its weight in its current form.

## Removed Points

These points are flagged to be removed; treat them with caution:
- "The central claim is contradicted by the paper's own evidence" — On verification, the paper's evidence largely supports optimization as a critical differentiator; the claimed contradiction is not present when reading the qualified claim carefully.
- Tone complaint about the Arora et al. comparison — This is a style preference, not a substantive weakness.
- Novelty complaint about 1-layer Attention failure — The paper cites prior work establishing this result (Sanford et al. 2024).
- Missing LR grid specifics — The details were in the appendix, which was stripped by the parser.
- Request for more architectures/methods — The scope (MQAR + copying, multiple SSM variants) is already appropriate for the claims made.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add gradient norm measurements across the LR sweep to substantiate the claimed mechanism.
2. Soften line 39's central claim to match the more measured framing in the abstract.
3. Either add mechanistic evidence for the induction head claim in Section 6 or remove/clearly frame it as speculation.
4. Replace max-min error bars with standard deviation or show individual seed results.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iVy7aRMb0K.md` | 4.50 | R1 | Yes | "Mimetic Init" — similar thesis (SSM recall gaps due to training difficulties). Current paper has stronger empirical scope and more definitive findings. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/BwG8hwohU4.md` | 5.33 | R1 | Yes | "StableSSM" — SSM memory limitations. Current paper is empirically broader. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QFgbJOYJSE.md` | 5.75 | R1/R2 | Yes | "SSMs Provably Comparable" — theory paper with limited experiments. Current paper is empirically richer. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pymXpl4qvi.md` | 6.00 | R1/R2 | Yes | "SSM Bottlenecks" — similar quality empirical analysis of SSM limitations. Comparable contribution. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AL1fq05o7H.md` | 6.25 | R2 | Yes | "Mamba" — landmark architecture paper with broader impact. Current paper is more focused but less impactful. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/d8w0pmvXbZ.md` | 8.00 | R1 | Yes | "Small-scale proxies" — higher quality empirical study of training instabilities with broader scope and thoroughness. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PdaPky8MUn.md` | 8.00 | R1 | Yes | "Never Train from Scratch" — broader methodological critique with similar ethos. Higher thoroughness and scope. |

**Round 1 bracket:** 5.5–7.5

**Narrowing:** After comparing item-level favorability ratings, the paper's strengths (all 11–14) exceed those of the 4.50–5.33 anchors (strengths 8–10) and match those of the 5.75–6.25 anchors. Its weakness ratings (0.33, 3.77, 5.89 for the substantive ones) are comparable to the 5.75–6.25 anchors' weakness ranges, but lack the extremely negative items (below -3) that drag lower-scored papers down. However, the paper lacks the very high favorability on core claims (items >15) and the minimal weakness drag that characterize the 7.5+ papers. The missing gradient diagnostics and slight overclaiming are real but non-fatal limitations that place the paper below the 7+ tier.

**Final score: 6.0.** The paper makes a genuine, well-supported empirical contribution that advances understanding of SSM vs Transformer differences. The core finding (LR sensitivity as a critical confound) is important and clearly demonstrated. The weaknesses — absent mechanistic evidence, slight overclaiming, and a speculative section — are addressable and do not invalidate the core claims but prevent the paper from reaching the top tier.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>