## Summary

This paper introduces a weight-based method for analyzing gated neurons in transformers by computing cosine similarities between their input (reading) and output (writing) weight vectors. Through this lens, the authors discover a class of "weakening" neurons (where cos(w_in, w_out) < -0.5) that show a striking cross-model pattern: they appear mostly in late layers, activate very frequently, and ablation experiments on OLMo-7B suggest they have outsized influence on attribute rate and next-token entropy. The paper further introduces conditional ablation to investigate the role of negative gate values, finding that weakening neurons' entropy-sharpening effect is partly driven by cases where x_gate < 0 — a surprising result since negative Swish values are conventionally associated only with training dynamics.

## Strengths

- **Cross-model consistency of the strengthening-to-weakening pattern (Section 5, Figure 1a).** Across 9+ LLMs (OLMo, Llama-2/3, Gemma, Mistral, Qwen, Yi), the median cos(w_in, w_out) shifts from positive in early layers to negative in late layers. This is a robust descriptive finding, not a single-model artifact.

- **The taxonomy of read-write functionalities is well-grounded (Section 4.2, Table 1).** The six-category classification follows naturally from the three-weight-vector geometry of gated neurons, with careful handling of edge cases (atypical mismatches) and multiple granularity options.

- **The conditional ablation method (Section 6.2) is a clean methodological contribution.** Separating neuron effects by the sign conditions on x_gate and x_in allows the paper to isolate which activation regimes drive an observed effect, with value beyond this specific study.

- **The finding that negative gate values have functional relevance for weakening neurons (Section 6.2) is genuinely surprising** and challenges the conventional view that Swish's negative tail exists only for gradient dynamics during training, not for functional computation at inference.

## Weaknesses

### Major

1. **Single-model ablation evidence for universal causal claims.** Every causal claim — that weakening neurons have outsized influence on attribute rate and entropy, that negative gate values encode a mechanism, that case (iii) of conditional ablation explains the sharpening effect — rests on ablation experiments performed on one model (OLMo-7B) with one dataset (20M tokens from Dolma). The paper acknowledges this as a resource constraint (line 188), but the abstract and conclusions frame these as general discoveries about transformer LLMs ("weakening neurons have outsize influence," "for the first time, we observe a mechanism important for transformer functionality that involves negative gate values"). This creates a gap between the scope of the claims and the breadth of the evidence. The descriptive cross-model findings are solid, but the causal/mechanistic conclusions are not commensurately supported.

2. **The ablation design does not isolate the weakening property from correlated neuron attributes.** The experiment ablates all ~243 weakening neurons and compares against random neurons from the same layers, controlling only for layer position. If weakening neurons systematically have larger weight norms, higher activation magnitudes, or different firing statistics, the ablation effect could be driven by these confounds rather than by the weakening property (negative cos(w_in, w_out)). The causal claim conflates "the set of neurons with cos(w_in,w_out) < -0.5" with "the causal effect of the weakening property itself."

### Minor

3. **The conditional ablation evidence for the negative-gate-value mechanism is qualitative only.** The central mechanistic claim that case (iii) (x_gate < 0, x_in < 0) drives the entropy sharpening effect rests entirely on a visual comparison of histograms (Figure 3b) with no quantitative comparisons: no effect sizes, no distributional distance metrics, no statistical tests. The single text example studied (the "Omicron" case, line 233) was explicitly selected as the most extreme case, which does not constitute systematic evidence for a mechanism.

4. **The weight preprocessing step (Section 3.2) affects the taxonomy but its justification is deferred to Appendix C** (which is not present in the main body). The sign-flipping of w_in and w_out changes the values of cos(w_gate, w_in) and cos(w_gate, w_out), two of the three cosine similarities used to define the taxonomy. Without a self-contained justification in the main text, readers cannot evaluate whether this choice induces artifacts in the classification.

5. **Ablation results for other neuron classes are deferred to the appendix.** The paper states that other RW classes' effects are "indistinguishable from the clean line" (line 207) but defers this to Appendix figures 14-16. Given that this comparison supports the central claim about weakening neurons' unique influence, these results would strengthen the main text significantly.

6. **No threshold sensitivity analysis.** The taxonomy threshold of τ = ±0.5 (line 129) is acknowledged as a choice but no analysis shows how results change with different thresholds (e.g., ±0.3, ±0.7).

7. **The paper lacks an explicit limitations section**, which would help clarify the scope of the claims given the single-model ablation experiments and the qualitative case study evidence.

### Trivial

None.

## Nice-to-Haves

- Replicate ablation experiments on at least 2–3 additional models from different families (e.g., one Llama, one Gemma) to bridge the gap between universal claims and single-model evidence.
- Add quantitative comparisons for the conditional ablation results (effect sizes, distributional distances between the histograms in Figure 3b, systematic analysis across many examples rather than the single extreme case).
- Add confound controls to the ablation: check whether weakening neurons have systematically different activation magnitudes or weight norms compared to the layer-matched random baseline, and if so, include a secondary baseline matched on those properties.
- Include the comparison of other RW classes' ablation effects in the main text.
- Add a limitations section.

## Removed Points

These points are flagged to be removed; treat them with caution:
- *Criticism about the taxonomy being "undercut" because 75% of neurons are orthogonal output but the paper then argues they manipulate input to some extent* — REMOVED. The paper transparently presents this as a sign that the threshold-based classification is conservative and provides multiple granularity options. This is appropriate scientific communication, not a weakness.
- *Criticism about the activation frequency definition (x_gate > 0) not being justified* — REMOVED. This is a standard definition consistent with prior work (Gurnee et al., 2024) and the paper's approach is reasonable.
- *Various formatting, presentation, and missing-related-work nitpicks* — REMOVED per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Replicate on more models.** The single most impactful improvement would be to run the ablation experiments on 2-3 additional models (e.g., one Llama variant, one Gemma variant) with the same protocol. If results hold, the causal claims become substantially more credible.
2. **Add quantitative rigor to the conditional ablation analysis.** Compute distributional distances (e.g., KL divergence, Earth Mover's Distance) between the histograms in Figure 3b to support the claim that case (iii) is more similar to the full weakening histogram than other cases.
3. **Control for confounds in the ablation.** Measure and report whether weakening neurons differ from random layer-matched neurons on other properties (activation frequency, weight norms), and if so, include a secondary matched baseline.
4. **Add threshold sensitivity.** Show how the taxonomy distribution and ablation results change with τ = ±0.3 and τ = ±0.7.
5. **Temper the universal framing of the causal/mechanistic claims** or add an explicit limitations section that clarifies the single-model scope of the ablation experiments.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Hierarchical Tracing | 89wVrywsIy.md | 3.40 | R1 | Yes | This paper has much stronger descriptive evidence (cross-model) but similar weakness severity in causal claims |
| Neuron to Graph | JBLHIR8kBZ.md | 4.00 | R1 | Yes | Both papers have solid methodology but limited evidence scope; the current paper's strengths are stronger |
| Neuron Path (ViT) | WQQyJbr5Lh.md | 6.00 | R1 | Yes | This paper's strengths are comparable, but it has more severe core evidential gaps (single model vs. multi-model experiments) |
| Circuit Discovery CD-T | 41HlN8XYM5.md | 6.33 | R1 | Yes | More methodologically rigorous; the current paper's qualitative evidence would not meet this bar |
| Retrieval Head | EytBpUGB1Z.md | 8.00 | R1 | Yes | Far more extensive multi-model experiments; this paper lacks that breadth for its causal claims |
| Selective Pruning | 8SPSIfR2e0.md | 5.75 | R2 | Yes | Similar strength-weakness profile: strong motivation and methodology, but evidence gaps in core claims |
| Function Vectors | AwyxtyMwaG.md | 6.00 | R2 | Yes | Stronger experimental breadth; the current paper's weakest items (favorability 0.89, 0.96, -0.25) are more severe than this anchor's lowest (1.45) |

**Bracket determination:** The paper's strengths (10.83-12.95 favorability) are competitive with 5.75-6.00 anchors, but its two Major weaknesses (favorability 0.89, 0.96) and the qualitative-only weakness (-0.25) are more severe than the lowest-rated items in the 6.0 anchors, while being less severe than the lowest items in the 3.5-4.0 anchors. The descriptive findings are genuinely strong, but the gap between universal causal claims and single-model evidential support is a real limitation. The final score of **5.0** reflects a paper with a solid descriptive contribution and interesting methodology that is held back by insufficiently supported causal/mechanistic claims — a borderline paper that could be strengthened substantially with multi-model replication.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>