Now I have the calibrated favorability scores. Let me compose the final review.

The three major weaknesses have very low favorability (0.00–0.24), confirming they are genuine concerns that drag the score down. The strengths are solid (0.81–1.00). The paper has a real technical contribution but is undermined by overclaimed results and a confounded comparison for one configuration.

## Summary

The paper proposes RoPE++, an extension of Rotary Position Embedding that computes an additional attention score by rotating query vectors by −π/2 before applying standard RoPE, yielding a "sine-integral" characteristic curve that decays more slowly than the standard cosine-based curve. Two configurations are introduced: EH (equal heads, half KV cache) and EC (equal cache, doubled heads). The method is evaluated via pre-training from scratch at 376M and 776M scales on 50B tokens plus 10B tokens of long-context continual pre-training.

## Strengths

- **Clean mathematical derivation (Section 3.1, Equations 3–4).** The paper correctly derives that the negative imaginary part of the complex RoPE attention product is equivalent to applying a −π/2 rotation to the query vector before the standard RoPE computation. This is the paper's cleanest result: it provides a simple, drop-in mechanism without modifying keys or values.
- **Well-designed noise-ablation experiment (Section 5.2, Figure 5).** Adding Gaussian noise separately to the real and imaginary attention components and measuring the impact on RULER-4k provides genuine causal evidence. The finding that corrupting the imaginary component degrades long-context performance more than corrupting the real component (by 5–8 points at σ=1.0) is stronger evidence than correlation-based attention-pattern inspection.
- **Two well-motivated configurations (EH and EC).** The paper correctly identifies two sensible instantiations trading off KV cache against attention head count. EH's ability to halve KV cache with broadly comparable performance is a practical contribution for long-context deployment.
- **Substantial experimental investment.** Pre-training from scratch at two model sizes (376M, 776M) on 50B tokens plus 10B tokens of long-context continual pre-training, with consistent comparison across multiple baselines, represents a significant evaluation effort.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed results for the EH variant on long-context.** Of four long-context comparisons (Table 2), EH loses to vanilla RoPE on two (376M RULER: 18.2 vs 18.8; 776M BABILong: 19.4 vs 22.8) and ties or marginally wins on the other two. The paper's abstract and conclusion state that "both RoPE++_EH and RoPE++_EC outperform vanilla RoPE," which is not supported for EH on long-context. The paper's own more careful language from Section 4.3 ("comparable performance with half the KV-cache and QKV parameters") is accurate and should be used throughout. Given that EH's primary value is an efficiency gain (half the cache), this should be the main claim.

- **The EC configuration's gains are confounded with increased model capacity.** RoPE++_EC doubles the number of attention heads and doubles the output projection W_o (Section 3.3, lines 99–102), adding parameters beyond the vanilla RoPE baseline. The improvements on long-context benchmarks (Table 2: EC 25.0 vs RoPE 18.8 on RULER at 376M) may be partly or entirely attributable to this increased capacity. A controlled comparison — e.g., EC against a vanilla RoPE model with the *same number of attention heads* (same W_o size, larger KV cache) — is needed to isolate whether the imaginary mechanism itself, rather than the added capacity, drives the gains.

- **No variance or statistical information for any result.** Every cell in Tables 1–3 is a single number with no standard deviation, confidence interval, or number of independent seeds. Given that many reported differences are very small (EH vs RoPE on short-context averages: 0.2–0.7 points), readers cannot distinguish genuine improvements from random seed variation. This is a standard expectation for pre-training experiments at these scales.

### Minor

- **The "discarded information" framing is rhetorically inflated.** The paper repeatedly states that standard RoPE "discards the imaginary component" (Abstract, Introduction, Section 3). However, standard RoPE operates with real-valued vectors and real rotation matrices; the imaginary component of the complex product is never computed. The paper proposes *additional* computation (a −π/2 query rotation), not recovery of lost information. The mathematical derivation is valid, but this framing overstates the novelty. The paper would be stronger by stating directly: "We propose computing an additional attention score by rotating queries by −π/2 before RoPE, which yields complementary positional sensitivity."

- **The "Avg." column in Table 1 averages heterogeneous metrics.** The column aggregates perplexity (Wiki, LAMBADA) where lower is better with accuracy metrics where higher is better, on different numerical scales (ranges 15–70). This average is not well-defined and conflates incompatible measurement types. Per-task reporting or properly normalized aggregation would be more informative.

### Trivial

- **Minor notation inconsistency.** The Figure 1 caption shows the exponent as \(10^{-d}\) while Equation 5 correctly uses \(10^{-n/d}\). The paper should ensure consistency between figures and equations.

## Nice-to-Haves

- A controlled comparison for EC against a vanilla RoPE model with the same number of attention heads to disentangle the imaginary mechanism from capacity effects.
- The Section 3.4 length-extrapulation argument (that RoPE++ dimensions observe both positive and negative embeddings, improving extrapolation) could be strengthened with OOD perplexity curves at extended lengths.
- Reporting results from multiple seeds and including variance measures.
- A clearer explanation of how the "Avg." column in Table 1 is computed.

## Removed Points

The following criticisms from the source reviews were removed after verification:
- "Missing PI/YaRN baselines in main tables" — Table 3 explicitly includes these comparisons; the criticism is factually incorrect.
- "Needs larger-scale validation" — The paper states Appendix C covers larger scales; the appendix is stripped by the parser and cannot be verified from the extracted text.
- "Lines 103–104 admission undermines the contribution" — This is the paper transparently explaining a constraint of its design, which is good scientific practice, not a flaw.
- "Section 3.4 argument needs stronger empirical backing" — Moved to Nice-to-Haves; the paper provides an analytical argument and Figure 3.
- Pure formatting and speculation about missing appendix content removed per filtering guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Tone down the claims for EH consistently.** Replace "outperform" with "comparable" for EH on long-context, consistent with the paper's own more accurate language in Section 4.3.
2. **Add a controlled comparison for EC.** Run a vanilla RoPE model with the same number of attention heads (matching EC's W_o size) to isolate the imaginary mechanism's effect from capacity gains.
3. **Report variance.** Run at least 3 seeds and report standard deviations or confidence intervals for main results.
4. **Fix the "Avg." column.** Either remove it and report per-task results, or use a principled normalization scheme.
5. **Reframe the contribution honestly** without the "recovering discarded information" rhetoric — the derived equivalence (Eq. 3–4) is interesting enough on its own merits.

## Score and Decision

The paper makes a genuine technical contribution — the equivalence between negative imaginary attention and −π/2 query rotation is clean, and the noise-ablation experiment provides compelling causal evidence. However, the experimental evaluation has three significant flaws: the EH variant is overclaimed (it does not consistently outperform on long-context), the EC comparison is confounded by increased capacity, and no variance information is provided. These issues are addressable in revision but in their current form weaken the paper's central quantitative claims. The score reflects a paper that is above the rejection threshold but needs substantial revision to the claims and experimental methodology.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>