Now I'll produce the final consolidated review.

## Summary

The paper proposes RoPE++, an extension of Rotary Position Embeddings that recovers the imaginary component of the complex-valued attention dot product discarded by standard RoPE. The imaginary attention is computed by pre-rotating the query by -π/2 and computing an additional attention score. Two configurations are introduced: RoPE++_EH (equal heads, half KV cache) and RoPE++_EC (equal cache, doubled heads). The method is validated at 376M and 776M scales on short- and long-context benchmarks. The paper includes a noise-ablation experiment providing causal evidence that imaginary heads are important for long-context performance.

## Strengths

1. **Clean mathematical derivation of a principled, parameter-free modification**: The paper identifies that the complex-valued formulation of RoPE produces both real and imaginary components (Section 3.1, Equations 1–4), and shows the discarded imaginary term reduces to a simple -π/2 pre-rotation of the query. No new learned parameters are introduced.

2. **Noise ablation provides causal evidence that imaginary heads matter for long-context**: Section 5.2 shows that corrupting imaginary attention with Gaussian noise (σ=1.0) degrades RULER-4k by 5 points (376M) and 8 points (776M) more than corrupting real attention by the same amount. This directly demonstrates that the imaginary component is functionally important for long-context performance, not just architectural overhead.

3. **RoPE++_EC shows consistent and often large improvements on long-context benchmarks**: On RULER at 376M, EC improves the average from 18.8 (RoPE) to 25.0; on BABILong from 11.0 to 16.1 (Table 2). The gains are systematic across 4k–64k lengths.

4. **RoPE++_EH provides a practically useful efficiency-performance trade-off**: At matched head count, EH achieves roughly comparable long-context performance to RoPE while using half the KV cache. Figure 4 confirms consistent memory reduction and decoding speedup that grows with context length.

5. **Compatibility with existing context-extension methods validated**: Table 3 shows RoPE++ works with both Linear PI and YaRN interpolation, improving over RoPE under both schemes at both model sizes.

## Weaknesses

### Major

1. **RoPE++_EC comparison is confounded by doubled attention head count** — The EC configuration keeps KV cache equal to RoPE but doubles the number of attention heads (from 12 to 24 at the reported model sizes). The paper does not include the natural control: a RoPE baseline with the same (doubled) number of attention heads. Without this control, the large gains observed in Tables 2 and 3 could plausibly come from increased model capacity (more heads) rather than from the imaginary component specifically. This is the single most serious experimental gap and directly affects the paper's central claim that recovering the imaginary component drives long-context improvements.

2. **"Outperform" framing for RoPE++_EH is not supported by the long-context data** — In Table 2, RoPE++_EH is worse than RoPE on 2 of 4 long-context averages (376M RULER: 18.2 vs. 18.8; 776M BABILong: 19.4 vs. 22.8). The margins are small and inconsistent. The introduction appropriately says "comparable results," but the abstract and conclusion claim both configurations "outperform vanilla RoPE," which is not accurate for EH on long-context. The correct framing — "roughly comparable to RoPE at half the KV cache" — is a genuinely useful efficiency result that does not need overstatement.

### Minor

3. **No variance or statistical significance reported** — All results are single-run without confidence intervals. Given small margins on several comparisons (0.1–0.9 points on averages) and modest model sizes, it is unclear which differences are meaningful versus within noise. Partially mitigated by the consistent direction of EC improvements, but the interpretability of individual per-task comparisons is limited.

4. **Shared W_q constraint acknowledged but its implications not discussed** — Line 103 states that real and imaginary heads share W_q, meaning the imaginary head's query is always a fixed -π/2 rotation of the real head's query. This prevents independent content allocation between the two types of heads, a genuine architectural limitation that should be discussed.

5. **Alternative interpretation of the noise ablation experiment** — The finding that corrupting imaginary attention degrades performance more could partly reflect that broadly-attending heads (imaginary) are inherently more sensitive to uniform noise than locally-focused heads, not necessarily that imaginary attention is "more dominant" for long-context. This does not invalidate the experiment, but weakens the strong causal claim drawn from it.

### Trivial

None.

## Nice-to-Haves

- Compare RoPE++_EC against a RoPE baseline with the same (doubled) number of attention heads to isolate the specific benefit of the -π/2 rotation.
- Report results from multiple training seeds (2–3) for the main comparisons.
- Add a discussion of the shared W_q limitation and its consequences.
- Include training loss curves to verify that convergence behavior does not differ between RoPE++ and RoPE.

## Removed Points

These points were raised in the input reviews but are not included as weaknesses in the main review for the following reasons:

- **Harsh Critic #1 ("framing is misleading")**: Removed. The paper is mathematically accurate. The complex-valued dot product formulation of RoPE (Equation 1) explicitly has an imaginary term that the standard implementation discards. Whether a particular efficient implementation computes it or not is a separate question; the mathematical framing is standard and correct.
- **Harsh Critic #6 ("theoretical analysis is thin")**: Removed. The characteristic-curve analysis follows the same methodology used in standard RoPE analysis and is standard practice for this type of positional encoding work. The paper also supplements it with empirical attention visualizations.
- **Harsh Critic #7 ("length extrapolation argument flaw")**: Removed. The critic's claim that "the rotation matrix already mixes dimensions" does not correctly account for the specific dimension-index pairings. The paper's claim about which query/key dimension pairs see which trigonometric values in real vs. imaginary attention is correct based on Equations 3 and the standard RoPE decomposition.
- **Harsh Critic's terminology critique ("imaginary is mystifying")**: Removed. This is a presentation preference, not a substantive weakness.
- **Strength Finder's generic/superficial strengths** (e.g., "this paper addressed an important problem"): Removed per filtering rules. Only strengths with specific, concrete content are retained.

## Novel Insights

None beyond the paper's own contributions. The two input reviews largely converge on the same observations. The most useful cross-cutting insight is the harsh critic's identification of the confound between doubled head count and the imaginary component in the EC configuration — this is a genuine experimental design gap that the paper's own framing and the strength finder both fail to adequately address.

## Suggestions

1. **The decisive experiment**: Compare RoPE++_EC against a RoPE baseline with the same (doubled) number of standard attention heads. If the imaginary-head variant still outperforms, the central claim is strongly supported. If not, the benefit comes from more heads, not from the imaginary component.
2. Calibrate claims throughout: for RoPE++_EH, use "comparable performance at half KV cache" rather than "outperforms."
3. Run 2–3 seeds for the main comparisons and report variance.
4. Add a discussion of the shared W_q limitation.
5. Include training loss curves.

## Score and Decision

**Score: 4** — Borderline Reject

**Decision: Reject**

**Reasoning**: The paper proposes a mathematically valid and clean modification to RoPE with some genuinely useful properties. The EH configuration's efficiency gains (comparable performance at half KV cache) are a practical contribution, and the noise-ablation experiment provides interesting evidence that the imaginary heads behave differently. However, the central weakness is unresolved: the EC configuration's doubled attention heads confound the interpretation of its strong results, and the paper overstates the evidence for EH "outperforming" RoPE. The claims about discovering and recovering "discarded imaginary information" as the driver of long-context gains are not adequately separated from the trivial confound of having more attention heads. A controlled ablation isolating the rotation from the head-count increase is necessary before the paper's core thesis can be accepted.