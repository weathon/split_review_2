Now I have verified everything carefully. Let me write the final review.

## Summary

This paper proposes RoPE++, an extension of Rotary Position Embeddings that adds "imaginary" attention heads (queries pre-rotated by −π/2 before standard RoPE) alongside standard "real" heads. Two configurations are introduced: RoPE++<sub>EC</sub> (equal KV cache, double attention heads) and RoPE++<sub>EH</sub> (equal head count, half KV cache and QKV parameters). Experiments at 376M and 776M parameter scales show that RoPE++<sub>EC</sub> substantially improves performance on long-context benchmarks (RULER, BABILong), while RoPE++<sub>EH</sub> achieves roughly comparable results with half the KV cache.

## Strengths

1. **Clean mathematical derivation (Section 3.1, Eq. 3→4).** The paper correctly shows that the imaginary component of the complex-valued RoPE dot product corresponds to applying a −π/2 pre-rotation to the query vector before the standard RoPE operation. This derivation is clear and provides a solid foundation for the architectural modification.

2. **Two well-motivated architectural configurations (Section 3.3).** RoPE++<sub>EH</sub> (equal heads, half cache) and RoPE++<sub>EC</sub> (equal cache, double heads) offer concrete, practical trade-offs. The efficiency gains of RoPE++<sub>EH</sub> — halving KV cache at the same attention head count — are demonstrated convincingly in Figure 4 across context lengths from 2k to 32k.

3. **Noise-injection experiment (Section 5.2, Figure 5).** The experiment adding Gaussian noise to either real or imaginary attention separately provides causal evidence that imaginary heads are disproportionately important for long-context performance (5–8 point gaps at σ=1.0 on RULER-4k). This is the most direct evidence for the paper's core claim.

4. **RoPE++<sub>EC</sub> achieves substantial long-context gains.** On RULER, RoPE++<sub>EC</sub> outperforms vanilla RoPE by 6.2 points (376M) and 2.0 points (776M) on average. On BABILong, the gains are 5.1 points (376M) and 1.3 points (776M). These are meaningful improvements that hold across model sizes and context lengths, and they persist when combined with other long-context techniques (YaRN, Linear PI) in Table 3.

## Weaknesses

### Fatal
None.

### Major

1. **No control isolating whether gains come from the imaginary component or from increased model capacity.** RoPE++<sub>EC</sub> doubles the number of attention heads relative to the vanilla RoPE baseline (with a correspondingly larger W<sub>o</sub>). Without a control experiment — vanilla RoPE trained with the same number of heads at the same cache cost — it is impossible to determine whether the long-context improvements (Table 2) are driven by the −π/2 pre-rotation or simply by having more attention capacity. The paper argues (line 103) that a clean separation is impossible under its architectural constraints, but this does not excuse the absence of the obvious control (vanilla RoPE with 2× heads). The magnitude of the EC gains (e.g., 25.0 vs. 18.8 on RULER at 376M) suggests the imaginary component likely contributes, but the evidence is not conclusive without this comparison.

2. **No ablation experiments.** The paper contains zero ablation studies. Given (a) the small margins on short-context tasks (often <1%, Table 1), (b) the mixed long-context results for RoPE++<sub>EH</sub>, and (c) the multiple architectural variables changed at once (head count, W<sub>o</sub> size, shared vs. separate projections), ablations are essential. The most critical missing ablations are: (i) standard RoPE with the same head count as RoPE++<sub>EC</sub> (2× heads), (ii) varying the pre-rotation angle away from −π/2, and (iii) ablating the effect of the doubled W<sub>o</sub> in the EC configuration.

3. **RoPE++<sub>EH</sub> results are inconsistent on long-context tasks, weakening claims of "comparable or even superior" performance (line 101).** On BABILong at 776M, RoPE++<sub>EH</sub> (19.4 avg) is substantially worse than vanilla RoPE (22.8 avg) — a 3.4-point gap. On RULER at 376M, it is slightly worse (18.2 vs. 18.8). At 776M on RULER, it is slightly better (28.6 vs. 27.4). The "comparable" framing is fair as an average statement, but the paper's stronger language is not supported across all settings.

### Minor

1. **No statistical significance or variance information.** Every result in Tables 1–3 is a single number without error bars or multiple seeds. While single training runs are common at this scale, the small margins (often <1% on short-context tasks) and the inconsistency in RoPE++<sub>EH</sub> results make it difficult to assess which differences are reliable.

2. **The "discarded information" framing is misleading.** The paper claims standard RoPE "discards the imaginary component" (Abstract, line 15), implying information is being thrown away. However, standard RoPE is computed as a purely real operation — the complex-valued representation is an alternative mathematical lens, not a signal that was computed and then discarded. What RoPE++ actually does is **add a new attention head** whose query is pre-rotated by −π/2 before applying standard RoPE. This is a legitimate architectural innovation that does not need the "recovering lost information" framing. The paper would be more accurate to describe the contribution this way from the outset.

3. **No efficiency analysis for RoPE++<sub>EC</sub>.** The paper provides memory and latency benchmarks for RoPE++<sub>EH</sub> (Figure 4) but not for RoPE++<sub>EC</sub>, which has double the attention heads and a double-sized W<sub>o</sub>. These incur non-negligible computational costs (softmax over 2× heads, larger output projection) that are material for practical use but are not quantified or discussed.

4. **The noise experiment (Section 5.2) admits an alternative interpretation.** Damaging globally-attending heads (which the imaginary heads empirically are, as shown in Figure 5) naturally harms long-context tasks more than damaging locally-attending heads. The experiment demonstrates that imaginary heads are important for long-context, but does not distinguish between "imaginary heads are valuable because of the −π/2 rotation" and "globally-attending heads are valuable for long-context, and these heads happen to be the imaginary ones." The theoretical analysis in Section 3.2 (sine vs. cosine integral kernels) partially addresses this by providing a mechanistic reason for why imaginary heads attend globally, but the experiment alone does not clinch causation.

### Trivial
None.

## Nice-to-Haves

- Train vanilla RoPE with 2× heads (same model dimension, same cache) as a control for RoPE++<sub>EC</sub>.
- Add ablations varying the pre-rotation angle and using separate W<sub>q</sub> projections for real and imaginary heads.
- Report results from at least 2 seeds for key experiments.
- Include FLOPs/runtime analysis for RoPE++<sub>EC</sub>.
- More clearly separate the two distinct contributions: (a) adding complementary attention heads with a −π/2 query rotation and (b) the efficiency trade-offs enabled by this addition.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Criticism about W<sub>o</sub> sizing (Section 3.3):** The harsh critic claimed "W<sub>o</sub> is d<sub>model</sub> × d<sub>model</sub> in standard transformers regardless of head count." This is factually incorrect — W<sub>o</sub> dimensions scale with total head output dimension (n<sub>heads</sub> × d<sub>head</sub>). The paper's description of W<sub>o</sub> sizing is accurate.
- **Criticism that separate W<sub>q</sub> for imaginary heads would not collapse to standard RoPE:** The paper's argument (line 103) is mathematically sound — since the −π/2 rotation is a fixed linear transformation applied after W<sub>q</sub>, any separate W<sub>q</sub> for an imaginary head can be absorbed into an equivalent standard-RoPE head by composing with the inverse rotation. However, the broader concern about confounded comparisons (Weakness #1 above) remains valid and is retained.
- **Missing related work references:** Removed per instructions (cannot verify completeness).
- **Formatting/style nitpicks and appendix availability complaints:** Removed per instructions.
- **Criticism about Section 3.3 W<sub>o</sub> discussion being "confusing":** The paper's description is correct; the confusion was in the reviewer's understanding of standard transformer architecture.
- **Training cost criticism for RoPE++<sub>EC</sub> (doubled attention compute):** This is valid and retained as Minor Weakness #3 (formulated appropriately).

## Novel Insights

None beyond the paper's own contributions.

The reviews do not surface a critique that identifies a genuinely novel insight the authors missed. The harsh critic's most interesting observation — that the noise experiment confounds head type with attention range — is a reasonable methodological caveat but not a novel discovery.

## Suggestions

1. **Add the missing control (most important):** Train standard RoPE with 2× attention heads (same total model dimension, same KV cache configuration) as a direct comparison to RoPE++<sub>EC</sub>. If it performs worse than RoPE++<sub>EC</sub>, the imaginary component is clearly the source of the gains. If it matches RoPE++<sub>EC</sub>, the contribution reduces to an efficient way of utilizing additional heads — still a valid result, but with a weaker claim.

2. **Ablate pre-rotation angle:** Train variants using rotation angles other than −π/2 (e.g., −π/4, −π/3) to test whether this specific angle is optimal or merely a convenient choice.

3. **Report variability:** Even a second seed for the main experimental conditions would substantially increase confidence in the reported results.

4. **Reframe the contribution:** Describe RoPE++ as adding complementary attention heads with a −π/2 query pre-rotation that provides a sine-kernel inductive bias favoring longer-range dependencies, rather than as "recovering discarded information."

5. **Quantify EC computational cost:** Include a table or figure showing the FLOPs, memory, and latency for RoPE++<sub>EC</sub> versus vanilla RoPE, similar to Figure 4 for RoPE++<sub>EH</sub>.

## Score and Decision

### Round 1 Bracket

Based on comparison with calibration anchors, the initial bracket was [4, 6]. The most topically similar anchor — "Scaling Laws of RoPE-based Extrapolation" (avg 5.0, accept) — has strong theoretical contributions and larger-scale experiments. Our paper has a more novel architectural modification but weaker empirical validation (no ablations, missing control). The anchor "Mitigate Position Bias via Scaling a Single Dimension" (avg 4.75, reject) has comprehensive experiments but weaker theory. Our paper sits between these.

### Narrowing

The missing control experiment that would isolate the imaginary component's contribution is the decisive weakness. Without it, the paper's central claim — that the imaginary component drives the observed improvements — remains plausible but not conclusively demonstrated. This places the paper below the ~6-level papers (PoSE, CLEX, Shifting RoPE) that cleanly validate their core claims, and in the 4–5 range where ideas are interesting but validation is incomplete.

### Anchors Used

| Path | Score | Round | Comparison |
|------|-------|-------|------------|
| `jp4pxKqCRW` (Periodic Extension) | 2.50 | R1 | Poorly executed; our paper is stronger. |
| `JO7k0SJ5V6` (Scaling Laws of RoPE) | 5.00 | R1,R2 | Stronger theory and larger scale; our paper has more novel architecture. |
| `sIGWTd1DcW` (Contextual PE) | 5.25 | R1,R2 | Comparable novelty; similar concerns about evaluation. |
| `t717joHHSc` (Mitigate Position Bias) | 4.75 | R2,R3 | Comprehensive experiments but weak theory; our paper is roughly comparable. |
| `GtvuNrk58a` (Round and Round We Go) | 6.20 | R1,R2 | Stronger mechanistic analysis; our paper has a clearer practical contribution. |
| `wXpSidPpc5` (CLEX) | 6.50 | R1 | Stronger empirical validation; our paper falls short. |
| `3Z1gxuAQrA` (PoSE) | 6.00 | R2 | Cleaner validation; our paper is weaker. |

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>