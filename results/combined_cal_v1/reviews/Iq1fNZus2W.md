Now I have sufficient calibration data. Let me compile the final review.

## Summary

The paper introduces Patch-Wise and Keyword-Aware Attention (PKA), a framework for efficient multi-condition control in Diffusion Transformers. PKA comprises two modules: Position-Aligned Attention (PAA) that reduces spatial-condition attention from O(N²) to O(N) by exploiting diagonal-dominant attention patterns, and Keyword-Scoped Attention (KSA) that confines subject-condition attention to keyword-activated regions using a temporally-reused mask. Combined with a condition KV cache and an early-timestep training sampling strategy, the method achieves up to 10× end-to-end inference speedup and 5.12× VRAM reduction for the attention module at high condition counts.

## Strengths

- **The attention pattern analysis grounds the design choices in observed structure.** Figures 2 and 3 provide concrete empirical evidence that spatial-condition attention matrices are diagonal-dominant and subject-condition attention is sparse. This is the strongest part of the paper's motivation — the modules are derived from observed structure rather than generic sparsity heuristics.

- **PAA is a clean, well-reasoned design.** Reducing N² attention to N by exploiting the diagonal structure of spatial-condition attention (Section 3.2.1, Equation 2) is a direct mapping of empirical observation to architectural choice. The ablation (Section 4.3.1) confirms it beats sliding-window attention in both speed and memory at comparable quality.

- **The efficiency numbers are substantial.** Up to 10× end-to-end inference speedup (Figure 7) and 5.12× VRAM reduction for the attention module (Figure 8) at high condition counts (16 conditions) represent a meaningful practical improvement. These results appear robust across condition counts.

- **The problem is well-motivated.** The O(c²n²) scaling bottleneck of the "concatenate-and-attend" paradigm (Section 1, line 19) is a genuine obstacle for deploying multi-condition DiTs, and the paper articulates this clearly.

## Weaknesses

### Major

- **Central quality-maintenance claim is overstated relative to evidence.** The paper repeatedly claims PKA "maintains or improves" generative quality and controllability (Abstract, Contributions line 49, Conclusion). However, on the Subject-Canny task, edge controllability (F1) drops from **0.551 (UniCombine) to 0.414 (PKA)** — a 25% relative degradation. The paper dismisses this as "the minor exception of a narrow margin" (line 249), which is a misleading characterization of a 0.137 F1 gap. This is the only task where edge controllability is evaluated alongside subject conditions, precisely where the efficiency-controllability trade-off would surface. The paper needs to honestly characterize and explain this trade-off rather than minimize it.

- **Early-timestep sampling (Section 3.3) lacks quantitative validation.** The perturbation analysis in Figure 5 is an interesting observation about early-timestep importance, but the paper claims this training strategy "accelerates convergence and enhances the final model's control fidelity" (line 41-42, line 302) with only qualitative support (Figure 11 — three rows of alarm clocks at varying iterations). Missing: (a) loss curves or FID over training iterations, (b) comparison of final model quality with vs. without early-timestep sampling using the full evaluation suite (Table 1 metrics), (c) a control experiment isolating the sampling strategy from the PKA architecture. Without quantitative evidence, this claimed contribution is not substantiated.

- **The condition KV cache involves an architectural change with unexamined implications.** The paper states condition tokens "only perform self-attention within their respective conditions" (line 81), which enables the cache. This fundamentally changes information flow: condition representations are decoupled from the image state during the forward pass and cannot interact across conditions. This architectural restriction may contribute to quality degradations (e.g., the Subject-Canny F1 drop), but the paper never discusses it as a potential limitation or ablates it separately from the cache benefit. Efficiency gains and architectural changes are conflated.

### Minor

- **FID scores are not contextualized.** The FID values in Table 1 range from 52.99 to 80.20, which is unusually high compared to standard benchmarks. The paper does not specify the reference set size, explain why these values are expected given the evaluation protocol, or clarify whether FID is computed on the full reference distribution vs. per-prompt. This makes the absolute numbers difficult to interpret.

- **Keyword identification for KSA is underspecified.** Section 3.2.2 states the keyword set "typically contains just 1 to 2 tokens" (line 128) but does not describe how these keywords are extracted from the text prompt — automatically via parsing, or manually specified. This is critical for reproducibility.

- **The specific μ and δ values for early-timestep sampling used in the main experiments (Table 1) are not reported.** Figure 11 uses μ=0.5, δ=1.5 as a demonstration, but it is unclear whether these same values were used for the main quantitative results, or whether the sampling was used at all in Table 1.

- **The "swa condition" column in Figure 9 is unexplained.** This column shows even better efficiency numbers (13.58s latency, 198MB VRAM) than the proposed PAA (13.63s, 237MB), but it is never described in the paper's text (Section 4.3.1).

- **No statistical significance reported.** None of the metrics in Table 1 include confidence intervals or multiple-run variance. For a method paper making comparative claims, this makes it unclear whether observed differences are stable or within run-to-run noise.

- **The "w/o PAA" baseline description is ambiguous.** It is unclear whether "w/o PAA" means the standard concatenate-and-attend multi-modal attention or simply replacing PAA with full cross-attention while retaining the self-attention-only condition design.

### Trivial

- The "w/o subject" column in Figure 10 (KSA ablation) is included in the table but not mentioned in the text discussion (Section 4.3.2).

## Nice-to-Haves

- Provide a controlled ablation isolating the early-timestep sampling strategy from the PKA architecture, with quantitative convergence metrics.
- Disentangle the condition self-attention restriction from the KV cache benefit via an ablation.
- Specify the number of inference denoising steps used in the experiments.
- Report the specific μ, δ values used in the main experiments.

## Removed Points

These points from the harsh critic input are excluded from the main review with justification:

1. **"End-to-end efficiency vs. attention-only efficiency"** — **REMOVED (factually wrong).** The harsh critic claimed the 10× speedup is "specifically for the attention module, not end-to-end." Figure 7 clearly compares end-to-end inference time between full methods (UniCombine, OminiControl2, Ours). Only the 5.12× VRAM reduction is attention-module specific, as stated in the paper.

2. **"OminiControl2 description too brief"** — **REMOVED (style nitpick).** Positioning against prior work is adequate.

3. **"Quantitative measure of redundancy needed"** — **REMOVED (beyond scope).** Qualitative attention map evidence is sufficient to motivate the design.

4. **"How many timesteps can the same mask be reused?"** — **REMOVED (speculative gap).** The paper specifies t→t+1 reuse. Extrapolating further is beyond the paper's claims.

5. **Missing related works** — **REMOVED (per instructions).**

6. **Formatting/style nitpicks (typos, appendix references, grammar)** — **REMOVED (parser artifacts or stripped sections).**

## Novel Insights

The harsh critic's most valuable observation is that the Subject-Canny F1 drop (0.551→0.414) directly contradicts the paper's "maintaining or improving" quality claim, and that the paper's characterization of this as a "narrow margin" is misleading. This is a genuine insight that the authors should address. The other criticisms largely recapitulate what the paper itself would need to provide but does not.

## Suggestions

- Temper the central claim: clearly state that PKA achieves substantial efficiency gains with a modest controllability trade-off on some tasks (particularly Subject-Canny) while improving or matching quality on others.
- Provide quantitative evidence (loss curves, FID over training iterations) for the early-timestep sampling contribution.
- Run an ablation that separates the architectural restriction (condition self-attention only) from the caching benefit.

## Score and Decision

Let me finalize my calibration analysis.

**Calibration Anchors Considered:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Highlight Diffusion (Jt1gGIumJo) | 3.00 | 1 | Yes | Much weaker: 1.52× speedup vs 10×, severe experiment limitations (-8.49, -8.35), far lower positive weights. Paper under review is clearly stronger. |
| SparseDM (3kADTLbKmm) | 4.00 | 1 | Yes | Comparable weight magnitudes but weaker positive weights (+5.03 vs +6.76), comparable negative weights (-5.01 vs -3.80). Paper has stronger efficiency claims but similar evidence gaps. Paper is slightly stronger. |
| DyDiT (taHwqSrbrb) | 5.50 | 2 | Yes | Most comparable: both propose efficient DiT architectures. DyDiT has more thorough experiments (+5.25) but smaller speedup (1.73× vs 10×). Paper under review has stronger efficiency numbers but larger evidence gaps for quality claims. Comparable overall. |
| Qihoo-T2X (lTrrnNdkOX) | 6.40 | 1 | Yes | Stronger positive weights (+7.90 vs +6.76), more comprehensive experiments across multiple tasks, but severe novelty weakness (-8.87). Paper under review has less extreme negatives. Roughly comparable tier but Qihoo has stronger experimental validation. |
| CtrLoRA (3Gga05Jdmj) | 6.00 | 1 | Yes | Stronger positive weights for experiments (+5.22), but severe novelty weakness (-10.51). Paper under review has stronger positive weights for core design (+5.76) and less severe negatives. |

**Round 1 Bracket:** 5.0–6.5

**Narrowing:** The paper's strongest items (PAA design +5.76, efficiency +6.76) are comparable to or stronger than DyDiT's top items (thorough experiments +5.25, extensive experiments +5.25) which scored 5.50. However, the paper has three moderately severe weaknesses (-3.04 to -3.80) that DyDiT does not share. Compared to Qihoo-T2X (6.40), the paper has weaker experiment breadth and larger evidence gaps.

**Final Score:** 5.5 — The efficiency contribution and PAA design are genuine strengths that place this paper above the reject threshold. However, the overstated quality-maintenance claim, the unvalidated early-timestep sampling component, and the unexamined architectural implications of the condition KV cache are substantive weaknesses that prevent it from reaching the accept range in its current form. With honest characterization of trade-offs and additional quantitative evidence, it could become a solid accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>