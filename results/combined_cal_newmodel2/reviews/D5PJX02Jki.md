Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes RoPE++, an extension to Rotary Position Embeddings that computes an additional sine-based ("imaginary") attention score alongside the standard cosine-based ("real") RoPE attention. The derivation shows that this can be implemented by simply rotating the query by −π/2 before applying standard RoPE. The paper introduces two configurations — RoPE++_EC (equal cache, doubled heads) and RoPE++_EH (equal heads, halved cache) — and evaluates them at 376M and 776M scales on short- and long-context benchmarks.

## Strengths

- **A genuinely novel mathematical insight into RoPE's complex formulation.** The paper identifies that the imaginary component of the complex-valued formulation yields a sine-based positional attention pattern that standard RoPE does not compute. The derivation showing this can be implemented by simply rotating the query by −π/2 before applying standard RoPE (Equation 4) is clean and elegant. This is a legitimate observation about an underexplored direction in RoPE research.

- **Well-motivated dual-configuration design addressing a real practical trade-off.** RoPE++_EC (equal cache, doubled heads) and RoPE++_EH (equal heads, halved cache) target different deployment constraints. The efficiency measurements in Figure 4 confirm that RoPE++_EH reduces memory and improves TPOT, especially for longer contexts, providing a genuine engineering contribution for memory-constrained long-context deployment.

- **Clever diagnostic experiment in Section 5.2.** The noise-injection study — adding Gaussian noise to real vs. imaginary attention separately and measuring the impact on RULER-4k — is a well-designed test of the claim that imaginary attention is more important for long context. The finding that corrupting imaginary attention hurts performance more (5–8 points at σ=1.0) provides the strongest causal evidence in the paper and genuinely supports the authors' thesis that the two attention components play different roles.

## Weaknesses

### Major

- **Missing critical ablation to isolate the imaginary rotation from architectural confounds.** RoPE++_EC doubles the number of attention heads and the output projection W_o; RoPE++_EH halves QKV parameters and KV cache. In neither configuration is the comparison controlled for the architectural change itself. The paper does not include the most important baseline: standard RoPE with the same number of extra heads but **without** the −π/2 rotation. For RoPE++_EC, the comparison confounds at least three variables — the imaginary rotation, head count, and W_o size — and none are isolated. If adding any extra heads (even without the rotation) produces similar long-context gains, then the core contribution collapses to "more heads help." The noise-injection experiment partially mitigates this concern but does not substitute for the controlled head-count ablation.

- **The paper's central framing of "discarded information" is rhetorically inflated.** RoPE operates on real-valued 2D subspaces followed by a real-valued dot product; there is no complex-valued intermediate scalar whose imaginary part gets "thrown away" in the actual computation. The complex representation is a mathematical convenience for analysis. What the paper actually does is define a new sine-based bilinear form that can be implemented via a −π/2 rotation — a legitimate and potentially useful extension. But characterizing this as "recovering lost information" (abstract, Section 1) misleads interpretation and sets the expectation of universal gains, which the mixed results do not support. The pattern is more consistent with "added a new computation that sometimes helps" than with "recovered lost signal."

### Minor

- **RoPE++_EH's performance trade-offs are underreported.** The paper claims EH achieves "comparable or even superior results" (Section 3.3), but the detailed results show notable degradations: 376M Long RULER (RoPE 18.8 vs EH 18.2), 776M Long BABILong (RoPE 22.8 vs EH 19.4, a 3.4-point drop), and several PI/YaRN configurations where EH is substantially worse (e.g., 376M YaRN BABILong: RoPE 14.4 vs EH 10.5). The "win" for EH relies on averaging across benchmarks in a way that masks these specific failures. The paper should acknowledge these as documented trade-offs rather than presenting improvements as consistent.

- **No error bars, multiple seeds, or statistical significance reported.** Every result in Tables 1, 2, and 3 is a single number. Given the modest model sizes (376M, 776M) and training budgets (50B tokens pre-training), differences of 0.3–0.9 points on short-context tasks could plausibly fall within run-to-run variance. Reporting results over at least 2–3 seeds would substantially strengthen confidence.

- **The length extrapolation argument in Section 3.4 is plausible but not empirically verified.** The claim that exposing dimensions to different sign patterns via imaginary attention "implicitly improves length extrapolation" is theoretically motivated, but the paper does not provide direct causal evidence isolating this mechanism (e.g., a controlled extrapolation experiment). The separate-heads computation also means the argument about individual dimensions benefiting is less direct than claimed; a more precise mathematical treatment would help.

- **No wall-clock speed measurement for RoPE++_EC's combined forward pass.** The paper claims efficient single-pass FlashAttention implementation (Section 3.3) but provides no timing data for RoPE++_EC. Since this configuration doubles the number of attention heads, it could increase FLOPs even with equal cache; timing measurements are needed to verify the efficiency claim.

### Trivial

None.

## Nice-to-Haves

- Run the control experiment: train standard RoPE with the same number of heads as RoPE++_EC but without the −π/2 rotation, to isolate the imaginary mechanism from the head-count confound.
- Provide wall-clock timing measurements for RoPE++_EC.
- Report results with 2–3 random seeds and error bars.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"No limitations section in the main paper"** — The paper states limitations are discussed in Appendix D. The parser strips appendices; this exists in the original submission.
- **"The length extrapolation argument fails because each head must extrapolate independently"** — Different heads in the same model can benefit from diverse training signals across heads; the argument that the model learns from the combined signal is reasonable.
- **"Semantic aggregation claim is asserted but not shown"** — The claim is supported by mathematical derivation (expected value under random q,k) and partially by the noise-injection experiment; sufficient for the paper's scope.
- **"No comparison to other methods using the imaginary component"** — The paper cites related work on complex-valued neural networks; this criticism was not in the original review but would be speculative.
- **"Y-axis values not reported numerically in parsed text"** — This is a parser artifact; values are visible in the figure.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the motivation to honestly describe the contribution as "defining a complementary sine-based attention score" rather than "recovering discarded information."
2. Run the critical control experiment (standard RoPE with the same number of extra heads but without the rotation) to cleanly attribute gains to the imaginary mechanism.
3. Report results with 2–3 seeds and error bars to account for training variance.
4. Provide wall-clock timing for RoPE++_EC and acknowledge RoPE++_EH's specific failure cases (BABILong, PI/YaRN) as a documented trade-off.
5. Add a more precise mathematical treatment of the extrapolation argument, making explicit the relationship between training length, sinusoidal period per dimension, and the resulting benefit.

## Score and Decision

**Calibration Anchors (listed from all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| gwZ90hFSL2.md (Cross-lingual robots) | 1.00 | R1 | No | Unrelated paper; score-1 reject not comparable |
| 8QTpYC4smR.md (Systematic review) | 1.00 | R1 | No | Unrelated survey; not comparable |
| 5kMwiMnUip.md (NEMESIS jailbreaking) | 1.40 | R1 | No | Unrelated topic |
| jp4pxKqCRW.md (Periodic Extension) | 2.50 | R1 | Yes | Topically similar. Much weaker: strengths are generic (favorability 9.18, 7.91), weaknesses go to -4.17. My paper's strengths (14.62, 14.39) vastly exceed this anchor. |
| 5dDYhvt6dY.md (Reinforced PE) | 3.00 | R1 | No | Distant topic; lower quality |
| 56mg1JFd3n.md (Writing in Margins) | 3.00 | R1 | No | Inference pattern paper; less topical |
| JO7k0SJ5V6.md (Scaling Laws of RoPE) | 5.00 | R1+R2 | Yes | Most comparable anchor. Strengths: 13.62, 13.55, 12.30. Worst weakness: -1.92. My paper's best strength (14.62) is higher; worst weakness (-1.81) is similar in magnitude. |
| OhauMUNW8T.md (Wavelet-based PE) | 5.25 | R1 | Yes | Topically similar. Worst weakness: -4.31 (marginal empirical improvement). My paper's weaknesses are less severe. |
| sIGWTd1DcW.md (Contextual PE) | 5.25 | R1 | No | Different approach; scores 5,6,5,5 |
| t717joHHSc.md (Mitigate Position Bias) | 4.75 | R1 | No | Different approach |
| VkqqZcofEu.md (Controlled Study) | 5.75 | R2 | Yes | Empirical study paper; strengths up to 12.13, worst weakness -2.98. My paper's worst weakness (-1.81) is less damaging but my strengths are higher. |
| GtvuNrk58a.md (Round and Round) | 6.20 | R2 | Yes | RoPE analysis paper with 8/5/8/5/5 scores. Strengths up to 12.08. Weaknesses: -2.50, -2.21. My paper's strengths are higher but the missing ablation is a more fundamental methodological gap. |
| Us1RXG1Ji2.md (TAPE equivariant PE) | 6.00 | R2 | No | Contextualized PE; different approach |
| wXpSidPpc5.md (CLEX) | 6.50 | R2 | No | Continuous length extrapolation |
| eoln5WgrPx.md (STRING) | 6.50 | R2 | Yes | Training-free method. Weaknesses all non-damaging (lowest 2.77). My missing ablation (-1.81) is notably more damaging. |
| EytBpUGB1Z.md (Retrieval Head) | 8.00 | R1 | No | Mechanistic analysis; higher tier |
| OvoCm1gGhN.md (Differential Transformer) | 8.00 | R1 | No | Architectural contribution; higher tier |

**Bracket determination:** Round 1 bracketing placed the paper between 4.5 and 6.5. Round 2 narrowing compared itemized favorability against the 5.00 (Scaling Laws), 5.75 (Controlled Study), and 6.50 (STRING) anchors. My paper's strongest items (strength favorabilities 14.62, 14.39, 13.04) match or exceed the 5.00 and 5.75 anchors. However, the missing-ablation weakness (-1.81) is a genuine methodological gap that is more severe than any weakness in the 5.75 or 6.50 anchors, preventing full confidence in causal attribution. This places the paper between 5.0 and 6.0.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>