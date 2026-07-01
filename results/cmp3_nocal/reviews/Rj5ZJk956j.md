## Summary

This paper introduces a weight-based method for analyzing gated neurons in transformers (SwiGLU/GEGLU) by computing cosine similarities between their input, gate, and output weight vectors. This yields a taxonomy of "read-write" functionalities. The central empirical discovery is a class of **weakening neurons** (where w_out points roughly opposite to w_in) that appears consistently across 12 LLMs, is concentrated in late layers, activates very frequently despite being numerically few, and has outsized influence on model behavior (attribute rate, output entropy). The paper further shows that part of this influence comes from the *negative gate value* regime, where Swish(x_gate) < 0, demonstrating that these negative values play a functionally meaningful role.

## Strengths

- **Timely and targeted contribution.** Gated activation functions (SwiGLU/GEGLU) are the dominant MLP activation in modern LLMs (Llama, Gemma, OLMo, Mistral, Qwen, Yi) but have received far less interpretability attention than ReLU or GELU-based models. The paper identifies a genuine gap and addresses it directly.

- **Cross-model weight analysis is thorough and striking.** The paper computes cosine similarities across 12 LLMs spanning multiple families and scales (0.5B–9B). Figure 1(a), showing median cos(w_in, w_out) per layer, reveals a strikingly consistent pattern across all models: positive in early layers, crossing to negative in later layers. This is a clean, reproducible empirical result.

- **The method is simple and decoupled from activations.** Computing cosine similarities between weight vectors requires no data, no activation runs, and no trained probes. This makes the core findings readily verifiable and extensible — a genuine virtue in mechanistic interpretability.

- **The negative gate value finding is empirically novel.** The paper demonstrates that the x_gate < 0 regime of weakening neurons is functionally relevant, providing evidence that the Swish nonlinearity matters for model function beyond training dynamics. This is a meaningful observation for the interpretability community, even if the geometric mechanism is straightforward.

## Weaknesses

### Fatal

None.

### Major

- **Functional validation is conducted on a single model (OLMo-7B), but the paper's claims are framed as universal.** The weight-based cosine analysis (Section 5) spans 12 models and is the paper's strongest result. However, all functional validation — the ablation experiments (Section 6), conditional ablation analysis (Section 6.2), the case study of entropy reduction (Section 6.3), the activation frequency analysis (Section 7), and the neuron case studies (Section 8) — is performed on OLMo-7B alone. The paper acknowledges this as a resource constraint (line 188), but the title (referring to "Transformers" generally) and abstract (claiming that weakening neurons "activate extremely often and have a large influence on model behavior") implicitly claim universality. Without functional replication on at least one additional model family (e.g., a Llama variant), the reader cannot distinguish between a genuine universal mechanism and a property specific to OLMo-7B's training. This is the single most consequential gap.

### Minor

- **The headline entropy effect ("about 10 nats") lacks basic summary statistics.** The paper states "in ≈ 10^6 next-token predictions, weakening neurons decrease the entropy by about 10 nats" (line 209, caption of Figure 3b). However, the histogram's alt text (line 203) reports it is "centered around 0." If the distribution is centered at zero, "10 nats" must refer to a tail event (e.g., the maximum), not the typical effect. The paper does not report the mean, median, standard deviation, or any quantile for the entropy change. The ablation results similarly lack confidence intervals or effect sizes. Given the 20M-token dataset, even negligible effects could be statistically significant; the reader cannot judge practical meaningfulness.

- **The "conditional ablation" method (contribution iv) is presented as a methodological contribution but is a straightforward extension of standard ablation.** Conditional ablation (Section 6.2) is zero-ablation restricted by a sign condition on x_gate and x_in. While it is a useful analytical technique, listing it as a contribution in the introduction (line 19) overstates its novelty relative to the paper's other contributions.

- **The framing of the negative gate value "mechanism" inflates a geometrically necessary consequence into a surprising finding.** The paper states that the finding "solves the mystery" (line 221) and that "for the first time, we observe a mechanism involving negative gate values" (abstract, line 9, and conclusion, line 281). In reality, for a weakening neuron (w_out ≈ -w_in), when x_gate < 0 and x_in < 0, Swish(x_gate) is negative, the product becomes positive, and the neuron acts as a strengthener — this is a direct mathematical consequence of equations (1–2) plus the definition of weakening. The genuinely novel empirical contribution is simply *that* this regime occurs and matters in practice. The framing could be more measured.

- **The taxonomy threshold (τ = ±0.5) is arbitrary and unaccompanied by a sensitivity analysis.** The paper acknowledges the threshold (line 129) and partially mitigates this by providing scatter plots and marginal distributions. However, the central categorical claims (number of weakening neurons, distribution patterns, etc.) depend on this choice. A sensitivity analysis showing how results change at τ = 0.3, 0.7 would strengthen confidence.

- **The breakdown of the activation-frequency correlation in the final two layers is noted but not discussed.** The paper reports that the correlation between cos(w_in, w_out) and activation frequency drops to −0.29 and +0.29 in the last two layers (line 245), whereas earlier layers have correlations of at least −0.71. Since weakening neurons are most prevalent in late layers, this pattern breakdown deserves analysis rather than just a mention.

- **The weight preprocessing step (flipping signs of w_in and w_out based on cos(w_gate, w_in), line 85) changes which neurons are classified as weakening vs. strengthening.** The paper argues this preserves model behavior (Appendix C, not available), but it means the taxonomy is relative to the preprocessed basis, not an absolute classification. This should be stated more explicitly.

- **The two qualitative case studies (Section 8) are both "prediction neurons" (Gurnee et al., 2024), which are known to be unusually monosemantic.** This selection bias means the case studies may not be representative of weakening neurons generally, and the paper does not acknowledge this limitation.

### Trivial

- The median cos(w_in, w_out) values in late layers are described as "slightly below zero" (line 172) but are not reported numerically in the text or a table. Given that Figure 1(a) is a key result, tabulating these values would be helpful.

## Nice-to-Haves

- Replicate the ablation and conditional ablation experiments on at least one additional model family (e.g., Llama-3.2-3B or Gemma-2-2B) to ground the universality claims.
- Add a sensitivity analysis for the cosine threshold τ, showing how the number of weakening neurons and ablation results change at τ = 0.3, 0.5, 0.7.
- Report the mean ± std entropy change for each ablation condition, not just a tail value.
- For cross-class ablation comparisons, clarify whether the same number of neurons is ablated from each class and discuss how different class sizes affect the comparison.

## Removed Points

- **"Other classes show no effect" is unverifiable from main text** — Removed because the appendix figures (14–16) were stripped by the PDF parser; the results exist in the original submission.
- **Taxonomy has 8+ categories reducing interpretability** — Removed as a subjective preference that the paper's three-level granularity (threshold + marginals + scatter plots) already addresses.
- **"Weakening neuron is largely a geometric redescription" framed as a critical/fatal issue** — Removed as overblown. The paper's "surprising behavior" claim refers to empirical properties (activation frequency, outsized influence despite few neurons), not to the definition itself. The reviewer's characterization that the paper "treats the existence of weakening neurons as a surprise" misreads the text.
- **The entropy effect criticism framed as if the "10 nats" refers to the mean** — Reframed as a reporting gap (no summary statistics), not as an error. The paper is ambiguous about whether 10 nats is the max or a typical value.
- **Conditional ablation is "not novel" as a harsh criticism** — Demoted from a critical issue to a minor overclaim, since the technique is presented as part of a broader analytical toolkit.
- **Concurrent work (Kong et al., 2025) undercuts novelty of negative gate finding** — The paper already acknowledges this concurrent work (line 226), so the criticism does not add new information.

## Novel Insights

None beyond the paper's own contributions. The cross-model weight-based analysis of gated neurons is the paper's genuine contribution, and the review does not surface a novel insight that the paper itself missed.

## Suggestions

1. Add at least one more model to the ablation experiments. The cross-model weight analysis is the paper's strongest result; extending one functional experiment to a second family (e.g., Llama-3.2-3B) would substantially strengthen the universality claims.
2. Report mean ± std entropy change for each ablation condition in a table, not just a histogram and a qualitative description of a tail value.
3. Re-frame the negative gate value finding as an *empirical demonstration* that this regime is functionally relevant, rather than a surprising "mechanism" — this is still a genuine contribution.
4. Add a brief sensitivity discussion for the cosine threshold, and tabulate the median cos(w_in, w_out) values shown in Figure 1(a).

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>