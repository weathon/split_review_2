Here is my final consolidated review:

## Summary

This paper proposes RoPE++, an extension of Rotary Position Embeddings (RoPE) that re-introduces the imaginary component of the complex-valued dot product, which standard RoPE discards. The imaginary attention is shown to be equivalent to a -π/2 rotation applied to queries before the standard RoPE computation, yielding attention heads with sine-based position-dependent weights. The paper derives theoretical properties, configures two variants (RoPE++_EC with equal cache but doubled heads, and RoPE++_EH with equal heads but halved cache), and validates through pre-training 376M and 776M models on 50B tokens with follow-up long-context training.

## Strengths

- **Genuinely novel observation.** The insight that the discarded imaginary component of the complex RoPE product corresponds to a simple -π/2 query rotation producing attention heads with useful sine-based position biases is original and well-articulated. This is a clean, underexplored angle on a widely used mechanism.

- **Clean mathematical derivation.** The derivation showing that imaginary attention decomposes into the same absolute-position-embedding form as real attention, with only a -π/2 rotation on the query vector (Equations 2–4), is correct and well-structured. The two configurations (RoPE++_EC and RoPE++_EH) provide distinct practical trade-offs that are clearly motivated.

- **Interesting length-extrapolation argument (Section 3.4).** The observation that the imaginary attention exposes low-frequency dimensions to negative position-embedding values during training (which vanilla RoPE's real attention does not) provides a concrete, mechanistic reason why RoPE++ might improve extrapolation. This connects the proposed method to a known OOD problem in RoPE extrapolation.

- **Large-scale pre-training experiments.** Pre-training two model sizes (376M and 776M) on 50B tokens, followed by long-context continual pre-training, is a serious experimental investment. The evaluation covers both short-context (Open LLM Leaderboard tasks) and long-context (RULER, BABILong) benchmarks across multiple context lengths up to 64k.

## Weaknesses

### Major

- **RoPE++_EC gains are confounded with increased attention capacity.** RoPE++_EC doubles the number of attention output heads while keeping the KV cache fixed. As the paper notes (Section 3.3), "W_o in RoPE++_EC is double-sized" and the method works by "doubling the attention head group size" (Figure 2 caption). This means the EC configuration has roughly 2× the attention computation FLOPs and a larger output projection. The strongest results in the paper come from this configuration (e.g., RULER avg 25.0 vs. RoPE 18.8 at 376M; BABILong avg 16.1 vs. RoPE 11.0 at 376M), but there is no controlled comparison: a vanilla RoPE model with the same number of attention heads (and thus comparable capacity) is not included. Without this baseline, the reader cannot determine whether the gains come from the specific sin-based imaginary encoding or simply from having more attention capacity.

- **RoPE++_EH results are marginal and lack statistical confidence measures.** RoPE++_EH is the less confounded comparison (same total head count, half the QKV parameters and cache), but its gains over vanilla RoPE are small: on short-context averages, +0.2 (376M Short), +0.2 (376M Long), +0.5 (776M Short), +0.7 (776M Long). On long-context benchmarks the results are mixed — RoPE++_EH is worse than vanilla RoPE on BABILong at 776M (19.4 vs. 22.8). These differences are within typical benchmark variance, yet **no error bars, standard deviations, or multiple-seed experiments are reported anywhere in the paper.** The claim that "RoPE++_EH surpasses standard RoPE with only half the KV-cache and QKV parameters" is not convincingly supported by margins of 0.2–0.7 avg points without any measure of variance, especially when the paper itself notes that on some tasks RoPE performs better.

### Minor

- **The theoretical length-extrapolation mechanism (Section 3.4) is not empirically validated at the dimension level.** The paper argues that for low-frequency dimensions, the imaginary attention exposes queries/keys to a wider range (both negative and positive) of position-embedding values during training, whereas vanilla RoPE sees only non-negative values. This makes a strong, testable prediction about which dimensions benefit most. However, the paper does not provide per-dimension analysis (e.g., the range of positional embedding values encountered during training for each frequency) to confirm the mechanism operates as claimed.

- **The summary claim that "RoPE++_EH surpasses standard RoPE" is overstated.** The paper's own results show that on several individual benchmarks (e.g., BABILong at 776M: 19.4 vs. 22.8; RULER at 376M: 18.2 vs. 18.8), RoPE++_EH performs comparably or worse than vanilla RoPE. The averages mask these individual failures. A more accurate characterization would be "RoPE++_EH achieves roughly comparable performance to vanilla RoPE while using half the cache."

### Trivial

None.

## Nice-to-Haves

- Adding a vanilla RoPE baseline with the same number of attention heads as RoPE++_EC (to control for increased capacity) would substantially strengthen the paper's core claim.
- Reporting results from 2–3 random seeds (at least at one model size) with standard deviations would allow readers to assess whether the small EH improvements are reliable.
- A per-dimension analysis of position-embedding values encountered during training (as predicted in Section 3.4) would directly validate the proposed extrapolation mechanism.

## Removed Points

1. **Critique that the noise-injection experiment "does not establish what it claims"** — REMOVED (strawman). The paper's claim is that imaginary heads (with sine-based encoding) attend globally and are thus more important for long-context tasks. The noise experiment (Section 5.2) and attention visualizations (Figure 5) together demonstrate precisely this: the imaginary heads have a global attention pattern, and disrupting them causes greater performance degradation. The critic argued the experiment conflates "any set of globally-attending heads" with the imaginary component, but the paper's derivation (Equation 4) shows that the global bias is a direct mathematical consequence of the sine-based encoding from the imaginary component. The experiment supports the paper's stated claim.

2. **Critique that the paper's framing about "discarding" the imaginary component is overstated** — REMOVED. The paper explicitly acknowledges in Section 1 that "taking the real part preserves the direct equivalence between complex multiplication and vector rotation" and frames the imaginary component as an additive extension, not a fix. The rhetorical framing is appropriate for a new-method paper.

3. **Critique about averaging diverse benchmarks in Table 1** — REMOVED. This is standard practice for reporting overall trends, and the paper provides per-task breakdowns alongside the average.

4. **Section 3.1 critique that the method doesn't "recover" new information** — REMOVED. The paper is fully transparent that the imaginary attention is equivalent to a -π/2 rotation (Equation 4). The novelty is in recognizing that this mathematically equivalent transformation produces heads with different positional biases, not in claiming the recovery of hidden information.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a controlled baseline:** vanilla RoPE with the same total number of attention heads as RoPE++_EC. This is the single highest-leverage experiment to determine whether the sin-based imaginary encoding itself (as distinct from increased capacity) drives the observed gains.

2. **Add multiple seeds / error bars:** Run at least 2–3 seeds at one model size (e.g., 376M) with standard deviations reported for the main benchmarks, particularly for RoPE++_EH where margins are thin.

3. **Validate the extrapolation mechanism directly:** Provide per-dimension analysis showing the range of position-embedding values (cos and sin terms) seen during training for low- vs. high-frequency dimensions in both vanilla RoPE and RoPE++.

4. **Calibrate the claims about EH:** Replace "surpasses" with "achieves comparable performance to standard RoPE while using half the cache and QKV parameters."

---

**Calibration report:**

Round-1 bracket: [4.0, 6.5].

Anchor papers retrieved:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Periodic Extension (jp4pxKqCRW) | 2.50 | R1 | Much weaker: poor writing, limited experiments, no theory rigor → our paper is clearly above |
| Contextual PE (sIGWTd1DcW) | 5.25 | R1, R2 | Similar setting (novel PE), accepted, but had concerns about experimental validation |
| Wavelet Positional (OhauMUNW8T) | 5.25 | R1, R2 | Similar setting (novel PE for long context), accepted with a 5-6 range |
| Scaling Laws RoPE (JO7k0SJ5V6) | 5.00 | R2 | Directly relevant (RoPE extrapolation), accepted, strong theory but some reviewers disagreed |
| TAPE (Us1RXG1Ji2) | 6.00 | R2 | Rejected due to split reviews despite decent avg score |
| STRING (eoln5WgrPx) | 6.50 | R1 | Stronger: training-free method, tested on large models (70B), cleaner setup, accepted |
| Round and Round (GtvuNrk58a) | 6.20 | R2 | Analysis paper about RoPE internals, accepted |

Our paper has a genuinely novel contribution and clean theory comparable to the 5.0–5.25 range, but the experimental validation is weaker than those papers because of the confounding in EC and the lack of error bars for EH. The idea is stronger than the 2.50 paper but the evidence is less definitive than the 6.5 STRING paper. Score is calibrated at 5.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>