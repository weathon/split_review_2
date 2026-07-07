## Summary

This paper proposes RoPE++, an extension of Rotary Position Embeddings (RoPE) that reintroduces the imaginary component of the complex-valued dot product as a separate attention head. The imaginary attention is computed by simply rotating query vectors by -π/2 before applying standard RoPE, yielding a sine-integral-based attention pattern that theoretically decays slower with distance. Two configurations are introduced: RoPE++_EH (equal head count, half KV cache) and RoPE++_EC (equal cache, doubled attention heads). The method is evaluated at 376M and 776M scales on 11 short-context and two long-context benchmarks (RULER, BABILong) plus combination with PI/YaRN interpolation.

## Strengths

1. **Clean mathematical derivation and elegant implementation.** The paper correctly identifies that what corresponds to the imaginary component of the complex RoPE dot product can be realized as a -π/2 pre-rotation of query vectors (Equation 4). This is a genuinely simple modification — no new modules, no learned parameters — and can be interleaved with real attention in a single FlashAttention pass.

2. **Genuinely extensive evaluation.** Two model sizes (376M, 776M), 11 short-context tasks, two long-context benchmarks at six context lengths each, combination with PI and YaRN interpolation, plus an independent noise perturbation diagnostic. This is a thorough empirical effort for a proof-of-concept paper.

3. **Theoretical analysis with mechanistic intuition.** The characteristic-curve analysis (Section 3.2, Equation 5) showing that imaginary attention's sine-integral envelope decays more slowly than the cosine-based real envelope provides a plausible intuition for why imaginary attention might benefit long-context modeling.

4. **Concrete efficiency demonstration for RoPE++_EH.** Figure 4 clearly shows RoPE++_EH reducing memory cost and improving TPOT at both model sizes, with the gap widening as context length grows.

## Weaknesses

### Fatal
None.

### Major

1. **RoPE++_EC conflates the imaginary-attention mechanism with increased representational capacity.** RoPE++_EC doubles the number of attention heads and doubles the output projection W_o while keeping KV cache fixed (Section 3.3, Figure 2b). The paper attributes the gains shown in Table 2 (RULER average 25.0 vs. 18.8 at 376M; BABILong 16.1 vs. 11.0) to the imaginary-attention mechanism, but this comparison is not controlled: a vanilla RoPE model with the same number of heads and W_o size could plausibly achieve similar gains purely from increased capacity. Without a baseline using the same head count and W_o size *without* the imaginary mechanism, the contribution of imaginary attention itself cannot be isolated. Given that the paper's most impressive results come from this configuration, this is a significant evidential gap that undermines the central claim.

2. **RoPE++_EH, which does control for head count, shows mixed and sometimes worse long-context performance, contradicting the paper's theoretical narrative.** On BABILong at 776M (Table 2), RoPE++_EH averages 19.4 vs. RoPE's 22.8 — a 3.4-point degradation. On RULER at 376M, RoPE++_EH (18.2) is below RoPE (18.8). These results are not outliers in Table 3 either: with YaRN at 376M, RoPE++_EH averages 10.5 on BABILong vs. RoPE's 14.4. The paper's claim that RoPE++_EH achieves "comparable results" is broadly accurate for short-context tasks, but on the long-context benchmarks where the method should theoretically excel, the evidence is mixed. The paper does not discuss these failure cases.

3. **The noise perturbation experiment (Section 5.2) does not control for signal-variance differences between components.** Adding Gaussian noise with equal standard deviation to real vs. imaginary attention does not account for potential differences in the intrinsic variance (and hence signal-to-noise ratio) of each component. If real-attention scores have higher variance or benefit from more redundancy (e.g., because there are more real heads), equal-σ noise would perturb them proportionally less. The conclusion that imaginary attention is "more dominant" in long-context modeling is therefore overstated given this confound.

### Minor

1. **The framing as "recovering discarded information" is rhetorically inflated.** The abstract and introduction claim standard RoPE "discards" the imaginary part of the complex-valued dot product. However, standard RoPE never computes a complex-valued attention score and then discards half — it computes a real-valued rotation-and-dot-product. The complex representation is a mathematical re-description, not an architectural computation. What the paper calls the imaginary part is a *new* computation (a -π/2 query rotation) that yields a different linear combination of the same dimension pairs. The paper's own Section 3.3 implicitly acknowledges this, but the central framing overstates what has been "recovered."

2. **No statistical significance or variance is reported for any result.** With ~40 metrics across Tables 1-3, most showing small absolute differences (e.g., 40.1 vs. 40.3 in Table 1), the reader cannot assess reliability. Standard errors or confidence intervals would be especially important for the "Avg." columns that drive the paper's headline claims.

3. **The characteristic-curve analysis (Section 3.2) is an average over random q,k, not an empirical measure of actual attention distributions.** The paper never directly verifies the predicted slower decay pattern by measuring average attention distances for real vs. imaginary heads on actual trained models. This would be a straightforward and informative analysis.

### Trivial
None.

## Nice-to-Haves
- **Controlled ablation for RoPE++_EC**: Compare against a vanilla RoPE baseline with the same number of attention heads and W_o size (i.e., adding heads without the imaginary mechanism). If RoPE++_EC still outperforms, the benefit comes from the *mix* of real and imaginary attention; if not, the claim is unsupported.
- **Normalized noise perturbation**: For the Section 5.2 experiment, normalize noise by the standard deviation of each component's scores and include a proportional-noise control.
- **Empirical attention-distance verification**: Directly measure the average attention distance for real vs. imaginary heads on trained models to confirm the characteristic-curve prediction.

## Removed Points
- **Missing appendix content (larger-scale results, limitations)** — The parser strips appendices; these exist in the original submission. Not a valid criticism.
- **Criticism that model sizes are too small (376M, 776M)** — Standard for a proof-of-concept; larger scales are cited as in the appendix.
- **Criticism that the characteristic-curve analysis "is not proof"** — The paper frames it as providing intuition, not formal proof. Already appropriately scoped.
- **Section-by-section notes about individual sections being "dense" or "hard to verify"** — Purely subjective and not actionable.
- **"Strengthening the Paper on Its Own Terms" section** — These suggestions are captured in the Nice-to-Haves above.

## Novel Insights

The most striking pattern across the reviews is the tension between RoPE++_EC and RoPE++_EH: the configuration that confounds mechanism with capacity shows the strongest gains, while the cleaner-controlled configuration shows mixed results on the very task (long-context) where the theory predicts the clearest advantage. This suggests that whether imaginary attention helps may depend on the interaction between the mechanism and available representational capacity — a more nuanced story than "imaginary attention is better for long contexts." A direct investigation of this interaction (e.g., does the imaginary attention's benefit scale with the number of real heads available to complement it?) could yield a substantially stronger paper.

## Suggestions

1. **Add a controlled baseline for RoPE++_EC** — this is the single highest-leverage improvement. A vanilla RoPE model with the same number of heads and W_o size would cleanly separate the effect of imaginary attention from the effect of increased capacity.
2. **Acknowledge and analyze the RoPE++_EH failures** — the BABILong degradation at 776M and the PI/YaRN results in Table 3 should be discussed, not glossed over. Understanding *when* imaginary attention hurts would be more valuable than claiming consistent improvement.
3. **Report confidence intervals or error bars** for at least the main results (Table 2), and normalize the noise perturbation experiment by component-wise variance.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| jp4pxKqCRW.md (Periodic Extension) | 2.50 | R1 | Yes | RoPE long-context paper, weaker evaluation, experiments in appendix |
| OhauMUNW8T.md (Wavelet PE) | 5.25 | R1 | Yes | Similar-tier: clean derivation, marginal improvement, some novelty concerns |
| sIGWTd1DcW.md (Contextual PE) | 5.25 | R1 | Yes | Similar-tier: novel PE approach, scalability concerns |
| GtvuNrk58a.md (Round & Round) | 6.20 | R1 | Yes | Stronger theoretical contribution, cleaner experiment, but less evaluation |
| gwZ90hFSL2.md | 1.00 | R1 | No | Not relevant (unrelated topic) |
| u1cQYxRI1H.md | 10.00 | R1 | No | Not relevant (diffusion) |
| P49gSPmrvN.md | 1.00 | R1 | No | Not relevant |
| bEgDEyy2Yk.md | 1.00 | R1 | No | Not relevant |
| 5dDYhvt6dY.md | 3.00 | R1 | No | Not relevant (translation) |
| 56mg1JFd3n.md | 6.00 | R1 | No | Not relevant (inference pattern) |
| ReccFdn4zE.md | 2.00 | R1 | No | Not relevant |
| t717joHHSc.md | 4.75 | R1 | No | Position bias, different focus |
| 4GD7a9Bo9A.md | 4.50 | R1 | No | Position bias, different focus |
| Us1RXG1Ji2.md | 6.00 | R1 | No | Different PE approach |
| fvkElsJOsN.md | 6.60 | R1 | No | Different approach |
| eoln5WgrPx.md | 6.50 | R1 | No | Different approach |
| OvoCm1gGhN.md | 8.00 | R1 | No | Much stronger (Diff Transformer) |
| aWXnKanInf.md | 8.00 | R1 | No | Much stronger |
| EytBpUGB1Z.md | 8.00 | R1 | No | Much stronger |
| tyEyYT267x.md | 8.00 | R1 | No | Much stronger |

**Round-1 bracket**: 4.5 – 5.5. The paper is clearly stronger than the 2.50 reject-level RoPE paper (which had limited evaluation and key results in the appendix) but falls below the 6.20 paper (whose mechanistic contribution is cleaner, without a capacity confound). It sits alongside the 5.25 anchors: similar in having a clean idea and decent evaluation, but with a more central evidential gap (the confound affecting the main performance claim).

**Score**: 5.0 — The paper identifies a genuinely interesting and overlooked aspect of RoPE, provides a clean derivation and elegant implementation, and conducts an extensive evaluation. However, the central experimental comparison (RoPE++_EC vs. RoPE) is confounded with a doubling of attention heads and W_o size, making it impossible to attribute the gains to the imaginary-attention mechanism itself. The cleaner-controlled configuration (RoPE++_EH) shows mixed long-context results that the paper does not adequately discuss. The contribution is plausible and worth exploring, but the evidence as presented does not convincingly isolate the claimed effect.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>