Now I have all the verification I need. Let me write the final consolidated review.

## Summary

This paper proposes RoPE++, an extension of Rotary Position Embeddings that computes an additional "imaginary" attention score alongside standard RoPE's "real" attention. The imaginary attention is equivalent to applying a π/2 rotation to the query vector before standard RoPE, yielding attention scores with a sine-based characteristic curve that (unlike the cosine-based real attention) decays slowly at large distances. Two configurations are introduced: RoPE++_EH (equal heads, halved KV cache) and RoPE++_EC (equal cache, doubled heads). Pre-training experiments at 376M and 776M show that both configurations improve over vanilla RoPE, especially on long-context benchmarks, and a noise ablation suggests the imaginary heads are functionally distinct and disproportionately important for long-context performance.

## Strengths

1. **Mathematically clean formulation.** The derivation in Section 3.1 (Equations 1–4) is sound. The observation that imaginary attention reduces to a π/2 rotation of the query before standard RoPE is simple and elegant, requiring no new positional machinery. This is a legitimate mathematical extension, not an ad-hoc modification.

2. **Practical EH configuration with validated efficiency gains.** RoPE++_EH halves KV cache and QKV parameters while keeping head count fixed. Figure 4 provides measured memory cost and TPOT improvements at context lengths up to 128k, with the gap widening as context grows. This is a practically useful contribution independent of whether imaginary attention is theoretically superior to real attention.

3. **Noise ablation provides functional evidence for the imaginary mechanism.** Section 5.2 adds Gaussian noise separately to real and imaginary attention components and measures the impact on RULER scores. The finding that corrupting imaginary attention degrades long-context performance more than corrupting real attention (5–8 point gap at σ=1.0) is the strongest direct evidence in the paper that the imaginary heads are behaviorally distinct and not simply a parameter-count artifact. This experiment partially addresses the head-count confound concern.

## Weaknesses

### Fatal
None.

### Major

1. **Head-count confound undermines the core claim for RoPE++_EC.** RoPE++_EC keeps the same KV cache as vanilla RoPE but doubles the number of attention heads (Section 3.3, Figure 2b). The paper's headline long-context gains (Table 2: RULER avg 25.0 vs 18.8 at 376M; BABILong avg 16.1 vs 11.0) could plausibly come from having twice as many attention heads rather than from the imaginary attention mechanism specifically. **There is no control experiment where standard RoPE is given 2N heads under the same KV cache budget.** The paper attributes gains to "imaginary attention specifically capturing long-context dependencies," but without this control, the improvement cannot be cleanly attributed to the mechanism versus the architecture. This is the most significant weakness in the paper.

   *Why this is Major, not Fatal:* The noise ablation (Section 5.2) provides convergent evidence that imaginary attention is functionally distinct and disproportionately important for long-context tasks, partially mitigating the concern. And the EH configuration (same total heads, half imaginary) does not suffer from this confound and still shows competitive results. But the EC claim remains incompletely supported.

### Minor

2. **No variance or statistical significance reported.** All results in Tables 1, 2, and 3 are single-point estimates with no error bars, standard deviations, or indication of random seeds. On short-context benchmarks where margins are thin (Table 1, 776M Short: RoPE=42.0, FoPE=42.0, RoPE++_EH=42.5, RoPE++_EC=42.8), run-to-run noise could affect interpretation. While multiple seeds at this training scale (50B tokens, 8 GPUs) is expensive, the paper should at minimum acknowledge this limitation.

3. **EH underperformance on BABILong at 776M is downplayed.** At 776M on BABILong (Table 2), EH scores 19.4 vs RoPE's 22.8 — a ~15% relative degradation. The paper frames this as "comparable results with vanilla RoPE with half the cache" (Section 4.3), which overstates the equality. No analysis is provided for when or why EH underperforms, which would strengthen the paper's credibility.

4. **FlashAttention integration claim is stated but not substantiated.** Section 3.3 says "we can interleave the −π/2-rotated q_t with the original q_t and perform the real and imaginary attention in a single pass in FlashAttention." The paper provides no implementation details, kernel benchmarks, or evidence that FlashAttention was used in the experiments. If a naive implementation was used instead, the efficiency claims remain valid (since they are measured) but the FlashAttention claim itself is unsupported.

5. **Noise ablation methodology is incompletely specified.** Section 5.2 describes adding Gaussian noise to "the imaginary and real attention components separately" but does not specify the injection point — whether noise is added to pre-softmax logits, post-softmax scores, or the query/key vectors. The interpretation of the results depends on this detail.

6. **Oscillatory potential downside of the sine characteristic curve is not discussed.** Section 3.2 shows the imaginary attention uses sin(θΔt), which oscillates rather than monotonically decaying like cos(θΔt). This could introduce unwanted periodicity where distant tokens receive non-uniform attention based on distance parity. The paper acknowledges the "counter-intuitive" nature but does not analyze this as a potential weakness.

7. **No discussion of computational FLOPs overhead.** RoPE++_EC doubles attention heads, which doubles attention computation FLOPs even though the KV cache is unchanged. RoPE++_EH computes two attention scores per head (real + imaginary). The paper focuses on cache efficiency but does not discuss the compute trade-off.

### Trivial

8. **"Impossible" overstatement about head allocation.** Section 3.3 claims that "configurations such as 75% imaginary vs. 25% real or 100% imaginary are impossible under RoPE++." The reasoning — that rotating an imaginary-head query by π/2 gives a real-head query — shows mathematical equivalence, not architectural impossibility. One could train a model with only π/2-rotated queries (which would be a different position encoding, not the same as RoPE). The claim conflates equivalence with impossibility.

## Nice-to-Haves

- A discussion of computational overhead (FLOPs) for both configurations.
- Analysis of when RoPE++_EH underperforms (e.g., BABILong 776M) would strengthen credibility.
- Clarification on whether FlashAttention was actually used, and if so, what kernel modifications were required.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper:

1. **"Discarded information" framing is misleading.** REMOVED. The paper's analysis uses the complex-number formulation of RoPE, which is standard in the literature (used in the original RoPE paper, Su et al., 2024). From this perspective, the attention score equals the real part of a complex product; the imaginary part is mathematically present in the complex product and not computed in the real-valued 2×2 rotation implementation. The framing is mathematically valid, not misleading.

2. **"Few work" claim contradicted by own citations.** REMOVED. The paper says "few work revisits the intrinsic computation" and cites Hua et al. and Dai et al. as examples of the small set of work that does. This is consistent, not contradictory — the reviewer misread the sentence.

3. **Efficiency evaluation limited to 32k.** REMOVED. Figure 4 shows measurements at context lengths of 32, 48, 64, 96, and 128 (in thousands). The caption confirms testing extends well beyond 32k.

4. **Missing related work.** REMOVED per guidelines: cannot verify without external sources.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run the critical control experiment:** Compare RoPE++_EC against a vanilla RoPE model with 2N attention heads and the same KV cache budget (e.g., by halving KV head dimension). This would directly disentangle whether the gains come from the imaginary mechanism or from increased head count. This single experiment would either validate or invalidate the paper's central claim.

2. Report results from at least 2–3 random seeds for the main comparisons (or explicitly acknowledge single-seed results and discuss the risk).

3. Add variance estimates (error bars or stdev ranges) particularly for short-context benchmarks where margins are thin.

4. Discuss the EH underperformance on BABILong at 776M (Table 2) and provide analysis.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>