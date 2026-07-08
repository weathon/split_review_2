## Summary

The paper proposes RoPE++, an extension to Rotary Position Embeddings that re-introduces the imaginary part of the complex-valued attention computation as a complementary sine-based attention score. The authors show that this imaginary component can be computed by simply rotating the query by −π/2 before applying standard RoPE. They introduce two configurations: RoPE++_EH (equal heads, half KV cache) and RoPE++_EC (equal cache, doubled heads). Experiments at 376M and 776M model scales across 11 short-context and 2 long-context benchmarks show consistent improvements, especially for RoPE++_EC on long-context tasks.

## Strengths

- **Clean mathematical observation.** The paper correctly identifies that the imaginary component of the complex-valued RoPE product corresponds to a sine-based attention score, and derives that it can be computed by rotating the query by −π/2 before applying standard RoPE (Eq. 4). The derivation is sound and non-obvious. **[weight=11.22]**

- **Two pragmatically motivated configurations (EH and EC).** RoPE++_EH (same heads, half KV cache) and RoPE++_EC (same cache, doubled heads) address different deployment constraints, making the contribution actionable for practitioners with different resource profiles. **[weight=9.60]**

- **Noise-ablation experiment (Section 5.2, Figure 5).** Adding Gaussian noise to imaginary attention degrades long-context performance more severely (by up to 8 points) than the same perturbation to real attention. This is a genuinely informative diagnostic showing that the two components play different functional roles. **[weight=10.18]**

- **Thorough evaluation scope.** The paper evaluates on 11 short-context tasks and two long-context benchmarks (RULER, BABILong) at multiple lengths (2k–64k), at two model scales (376M, 776M), with three context-extension methods (NTK, Linear PI, YaRN). **[weight=9.79]**

## Weaknesses

### Fatal
None.

### Major

- **Missing head-count control experiment.** RoPE++_EC doubles the number of attention heads; the natural control is standard RoPE with twice as many heads (same parameter budget). RoPE++_EH halves QKV dimension per head; the control is standard RoPE with the same halved dimension. Without these controls, the claimed benefits of the imaginary-attention mechanism are confounded with architectural changes (more heads / different parameter allocation). The noise ablation shows imaginary heads are more *important* in the trained model, but not whether they carry information that couldn't be learned by additional standard RoPE heads. This is the single most important missing experiment and directly affects whether the paper's central claim is supported. **[weight=0.95]**

- **RoPE++_EH underperforms RoPE on BABILong at 776M.** Table 2 shows BABILong average 19.4 (RoPE++_EH) vs 22.8 (RoPE), a 3.4-point deficit. At 376M on BABILong, RoPE++_EH also trails at several individual lengths (e.g., 2k: 14.1 vs 17.7). The paper states RoPE++_EH achieves "comparable results with vanilla RoPE with half the cache"; at 776M on BABILong this claim is not accurate. **[weight=2.73]**

### Minor

- **Imprecise "discarded information" framing.** The paper repeatedly states that standard RoPE "discards the imaginary part outright," causing "irreversible information loss" (lines 9, 15, 45). In standard RoPE, the complex multiplication is a computational mechanism for realizing a real-valued rotation; the imaginary part of the intermediate product was never a signal present in the output. The paper is computing a complementary sine-based score — a genuine extension — but framing it as "recovering lost information" overstates the case. **[weight=5.01]**

- **No statistical significance or variance reporting.** All results in Tables 1–3 are single numbers with no confidence intervals or multiple seeds. Many short-context differences are small (e.g., 376M Short: RoPE avg 40.1 vs RoPE++_EH 40.3), and individual tasks show RoPE++_EH worse than RoPE (e.g., 776M GPQA 15.8 vs 25.8). Without variance estimates it is unclear whether the reported improvements are statistically meaningful. **[weight=0.86]**

- **ALiBi matches or exceeds RoPE++_EH on short-context average.** At 376M Short, ALiBi (40.5) outperforms RoPE++_EH (40.3); at 776M Short, ALiBi (42.6) again outperforms RoPE++_EH (42.5). The paper's framing of "best average performance" is accurate for RoPE++_EC but overstates for RoPE++_EH. **[weight=7.34]**

- **No direct extrapolation curves.** The paper claims improved length extrapolation (Section 3.4) but does not directly measure perplexity as a function of context length beyond the training window, which is the standard evaluation for extrapolation. The claim rests on theoretical reasoning and indirect evidence from downstream benchmarks. **[weight=-0.23]**

- **Quantified compute cost needed for RoPE++_EC.** RoPE++_EC doubles attention computation (both real and imaginary scores), but the paper only quantifies cache benefits, not FLOPs or throughput cost. **[weight=5.85]**

### Trivial
None.

## Nice-to-Haves
- Run at least 3 seeds for the primary comparisons to establish statistical reliability.
- Add a perplexity-vs-length curve to support the extrapolation claims.
- Report FLOPs or throughput for RoPE++_EC to quantify the compute tradeoff.
- Analyze why RoPE++_EH underperforms on specific tasks (e.g., GPQA at 776M).

## Removed Points
These points are flagged to be removed, treat them with caution:
- Weakness about "few work revisits intrinsic computation" claim being overstated — the paper cites the relevant prior work it claims is scarce; this is a minor imprecision. Removed as overly nitpicky.
- Weakness about missing comparison with learned position embeddings (T5 relative bias, XPos, etc.) — these are outside the paper's stated scope. Removed as scope creep.
- Weakness about efficiency analysis being unfair because RoPE++_EH is a differently-sized model — the paper is transparent about the parameter difference, and the comparison is valid for showing what is achievable at half cache. Removed.
- Weakness about missing analysis of where imaginary attention fails — would be nice-to-have but not a core gap. Removed.

## Novel Insights
None beyond the paper's own contributions. The main insight from the review process is that the missing head-count control experiment is the critical gap that needs to be addressed to validate the central claim.

## Suggestions
1. **Add the head-count control experiment** — this is the single most important thing the authors could do. Compare RoPE++_EC against standard RoPE with the same number of heads (doubled), and RoPE++_EH against standard RoPE with the same per-head dimension (halved). If imaginary attention provides genuinely different positional information, RoPE++ should outperform the control.
2. **Run multiple seeds** (at least 3) for the primary comparisons.
3. **Replace the "discarded information" framing** with a more precise description: "computing a complementary sine-based attention score alongside the standard cosine-based score."
4. **Add perplexity-vs-length curves** beyond the training window to directly test the extrapolation claims.

---

**Calibration Report:**

All anchors retrieved across rounds (15 total), with the most relevant being:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Wavelet-based Positional Encoding (OhauMUNW8T.md) | 5.25 | 1 | Yes | Marginally weaker evaluation; more damaging weaknesses (marginal improvement weight -1.62). My paper is stronger in evaluation breadth and has less damaging weaknesses. |
| Long-context Extrapolation via Periodic Extension (jp4pxKqCRW.md) | 2.50 | 1 | Yes | Much weaker paper; poorly written, limited experiments. My paper is clearly superior. |
| STRING (eoln5WgrPx.md) | 6.50 | 1 | Yes | Stronger paper overall. Similar strength weights but STRING's weaknesses are barely damaging (all >0.88), while my paper has a damaging missing-control weakness (0.95). |
| Scaling Laws of RoPE Extrapolation (JO7k0SJ5V6.md) | 5.00 | 2 | Yes | Split scores (1,6,8). Strengths high (7.92-9.87) but weaknesses very damaging (0.01, 1.74). My paper's weaknesses are less damaging overall. |
| Contextual Position Encoding (sIGWTd1DcW.md) | 5.25 | 2 | No | Different focus (context-dependent counting). Comparable overall quality. |

**Round 1 bracket**: The paper sits between 5.00 (Scaling Laws) and 6.50 (STRING). Compared to the 5.25 wavelet anchor, my paper has less damaging weaknesses (most negative weight -0.23 vs -1.62). Compared to the 6.50 STRING anchor, my paper has more damaging weaknesses (0.95 vs STRING's mostly positive weights).

**Round 2 narrowing**: The Scaling Laws anchor (5.00) has more damaging weaknesses than my paper (0.01, 1.74 vs my 0.95, -0.23, 0.86). The CoPE anchor (5.25) is broadly comparable. Weighted-item comparison places this paper above 5.00 and below 6.50.

**Final score**: 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>