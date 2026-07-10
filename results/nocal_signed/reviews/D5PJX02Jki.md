Now let me compose the final review based on this analysis.

## Summary

This paper identifies a novel aspect of Rotary Position Embeddings (RoPE): the imaginary component of the complex-valued formulation, which is discarded in standard RoPE, corresponds to a −π/2 pre-rotation of the query and produces attention heads with different positional characteristics (more global, sine-integral decay). The authors propose RoPE++, which computes this imaginary attention in parallel with standard real attention, and introduce two practical configurations (EH: equal heads with halved KV cache; EC: equal cache with doubled heads). Experiments at 376M and 776M scales show that RoPE++_EC consistently outperforms vanilla RoPE on long-context benchmarks, while RoPE++_EH offers a favorable efficiency-accuracy trade-off.

## Strengths

- **Genuinely novel theoretical insight.** Identifying that the imaginary component of RoPE's complex-valued computation corresponds to a −π/2 pre-rotated query, and that this yields attention heads with different positional preferences (sine-integral decay, more global focus), is an original observation not present in prior RoPE analyses. The mathematical derivation (Equations 1–4) is clean and sound. *(Impact: +10.0)*

- **Two architecturally motivated configurations.** RoPE++_EH (equal heads, halved KV cache) and RoPE++_EC (equal cache, doubled heads) directly address the practical KV-cache bottleneck in long-context LLMs. They are clearly explained via Figure 2, and the efficiency benefits of RoPE++_EH are validated empirically (Figure 4 shows consistent memory and latency reductions). *(Impact: +7.6)*

- **Attention-pattern analysis.** Figure 5 provides compelling visual evidence that imaginary heads attend more globally while real heads focus locally. The analysis is grounded in specific layer/head visualizations across two model scales, offering qualitative support for the method's design intuition. *(Impact: +7.5)*

- **Theoretical analysis of length extrapolation.** Section 3.4 provides a concrete argument for why imaginary attention improves extrapolation: it exposes query/key dimensions to both positive and negative position embeddings during training, so dimensions observe the full cos/sin value range more quickly than in standard RoPE. *(Impact: +7.8)*

## Weaknesses

### Fatal
None.

### Major
- **Missing baselines on long-context evaluation.** FoPE, Pythia, and ALiBi are compared on short-context tasks (Table 1) but are entirely absent from the long-context evaluation (Table 2). The paper claims RoPE++ "outperform[s] vanilla RoPE and other position embeddings on average across short- and long-context benchmarks" (Contributions). Since only RoPE appears in the long-context results, the claim about outperforming "other position embeddings" in the long-context setting is unsupported by the experimental design as presented. This is an addressable gap — evaluating at least one competing method on a single long-context benchmark would substantiate the claim. *(Impact: -9.6)*

- **Parameter count not reported per variant.** The paper explicitly states that RoPE++_EC's output projection W_o is "double-sized" (Section 3.3), giving it strictly more parameters than vanilla RoPE at the same nominal model size label (376M/776M). However, exact parameter counts per variant are never reported. Since RoPE++_EC produces the paper's strongest gains (Tables 2 and 3), the contribution from increased model capacity vs. the imaginary mechanism itself is unclear. Reporting exact counts and/or comparing against a vanilla RoPE baseline with matched parameters would resolve this. *(Impact: -1.6)*

### Minor
- **RoPE++_EH's performance characterization is somewhat overstated.** The paper claims EH achieves "comparable performance" with vanilla RoPE (Section 4.3, Conclusion) and "comparable or even superior results" (Section 3.3). While this fits some benchmarks (e.g., RULER 776M: 28.6 vs 27.4), on BABILong the deficits are notable (776M: 19.4 vs 22.8, ~15% relative drop; Table 3, 376M YaRN BABILong: 10.5 vs 14.4). Half the KV cache makes this a legitimate trade-off, but the claims should be more precisely quantified. *(Impact: -0.4)*

- **Noise-perturbation experiment does not fully control for attention score variance.** Section 5.2 adds equal-σ Gaussian noise to real and imaginary attention scores. If the two sets of scores have systematically different variances, the same σ represents a different relative perturbation. The paper does not report or normalize by score distributions, so the conclusion that imaginary attention "plays a more dominant role" is not fully robust to this alternative explanation. (The consistent gap across multiple σ values partly mitigates this concern.) *(Impact: -0.7)*

### Trivial
None.

## Nice-to-Haves
- Adding confidence intervals or variance estimates for the main benchmark results would help assess whether the small margins on some short-context tasks (e.g., <1 point differences in Table 1) are meaningful.
- Evaluating on a broader set of long-context benchmarks (e.g., LongBench, NarrativeQA) would strengthen the empirical contribution, though RULER and BABILong are already standard choices.

## Removed Points
- *"Discarded information" framing is misleading* (Harsh Critic Issue 1): **Removed.** The complex-valued formulation is the standard mathematical framing of RoPE (Su et al., 2024). The paper's description that standard RoPE "keeps only the real part of the complex-valued dot product" is mathematically accurate in this context. The framing does not affect the method's validity or results.
- *No inference cost analysis*: **Removed.** The paper does provide efficiency analysis in Figure 4 (memory cost and TPOT) for RoPE++_EH.
- *No LongBench/NarrativeQA evaluation*: **Removed.** RULER and BABILong are standard long-context benchmarks; requesting additional ones is scope creep given the already-extensive evaluation.
- *No statistical significance tests*: **Removed from weaknesses.** Single-run evaluation at this pretraining scale (50B tokens) is standard practice. Noted as a nice-to-have.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- **Report exact parameter counts** for all variants (RoPE, RoPE++_EH, RoPE++_EC) to resolve the parameter-count confound. If the variants differ in total parameters, add a controlled baseline (e.g., vanilla RoPE with proportionally more heads matched to EC's parameter count).
- **Evaluate FoPE, Pythia, or ALiBi on at least one long-context benchmark** (e.g., RULER-4k) to substantiate the claim of outperforming other position embeddings in long-context settings, or revise the contribution claim to scope it to RoPE.
- **Characterize RoPE++_EH's performance more precisely** — e.g., "achieves competitive results with half the cache, with an average X-point improvement on RULER and Y-point degradation on BABILong" — rather than stating "comparable" broadly.
- Report attention score magnitudes or normalize by head-wise variance in the noise-perturbation experiment.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>