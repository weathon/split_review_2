## Summary

DND (Dynamic Nested Depth) introduces a post-training method that identifies "critical" tokens via a learned router and reprocesses them through an additional pass of the same transformer layer, while leaving easy tokens undisturbed. The method adds a linear router, a dual-objective training loss (entropy dispersion + MSE preservation), and a threshold-control scheme with EMA synchronization. Validated on three dense 1B-class models (Qwen3, Llama3.2, Gemma3) and one 30B MoE model (Qwen3-30B-A3B), DND achieves average gains of 1.88–2.61% on small models and +0.87% on the 30B model across 17 benchmarks, with minimal parameter and FLOPs overhead.

## Strengths

- **Practical post-training design validated across architectures.** DND operates as a plug-in on existing pretrained models — a genuine practical advantage over methods like MOR that require pretraining from scratch on 200B tokens (Section 2.2, lines 58–59). The method is validated on three distinct dense architectures (Qwen3, Llama3.2, Gemma3) and a 30B MoE model, demonstrating generalizability.

- **Router training strategy is well-designed and cleanly ablated.** The dual-objective loss (score dispersion via entropy maximization + distribution preservation via MSE pull toward 0.5) directly addresses sigmoid-gated routing collapse. Table 4 convincingly shows that removing either component degrades performance: full method achieves +1.88 average gain, while removing router control drops to +1.01 and removing threshold control drops to +1.05.

- **Mechanistic analysis (Section 4.5) provides evidence for the claimed behavior.** Figure 4a shows positive correlation between token selection frequency and the vanilla model's logit entropy (r = 0.336), and Figure 4b shows that selected tokens have reduced entropy after DND processing (r = −0.581). This ties the mechanism to the claimed "review hard tokens" narrative, going beyond pure accuracy metrics.

## Weaknesses

### Fatal
None.

### Major

- **No variance or significance reporting for the 30B model results (Table 2).** All results are single numbers with no confidence intervals, standard errors, or multi-seed runs. This is especially consequential for the 30B MoE model, where several per-task deltas are very small (BBH +0.13, MATH +0.15, MATH-500 +0.20, DROP +0.27, CMMLU +0.37). While the consistency of positive improvements across all 17 benchmarks (+0.87 average) provides some evidence against pure noise (binomial probability ~7.6×10⁻⁶ if the method had no effect), the paper's scaling claim would be substantially strengthened by variance estimates or multi-seed runs. This is the most significant limitation of the paper.

### Minor

- **The "around 5%" claim on BBH and GPQA (line 203) is overstated for one model.** The paper states all three models show "around 5%" improvement on BBH and GPQA. While Qwen (+5.02/+5.80) and Gemma (+4.69/+5.30) are near this mark, Llama3.2-1B achieves only +3.70 on BBH and +3.86 on GPQA — substantially below 5%.

- **ITT baseline compared on only one model (Qwen3-1.7B); MOR not empirically compared.** ITT is evaluated only on Qwen3-1.7B in Table 1, not on the other architectures. MOR is not empirically compared, with the paper citing the requirement for pretraining from scratch (lines 58–59). This justification is valid, but the paper could strengthen its positioning with a simplified "recurrent token refinement" baseline that controls for the effect of extra computation itself.

- **FLOPs vs. throughput gap unexplained.** The paper claims "only about 6% extra FLOPs" (line 245), but Table 3 shows actual throughput at 91.6–93.1% of baseline (7–9% slowdown). The gap is not acknowledged or discussed (e.g., kernel launch overhead, memory-bound attention). Throughput is also measured only at batch size 1.

- **Layer range L_s:L_e for the 30B model (42 layers) not explicitly stated.** The paper reports 4:23 for the 1.7B model (24 layers) but only says "keeping about four layers at both the beginning and the end" for the 30B model (line 253–254), without giving the specific range. This is a minor reproducibility gap.

- **Training dataset composition vaguely described.** The SFT data is described as "a comprehensive and diverse dataset" with "1-2 million instances" from "human annotations and open-source materials" (line 199). It is not clarified whether the baseline SFT and DND+SFT use identical data, training budgets, and optimizer settings.

- **Figure 4a correlation r = 0.336 is weak-to-moderate.** The paper states "tokens with higher logit entropy are frequently selected" but does not discuss the substantial scatter — many high-entropy tokens are infrequently selected and vice versa. This does not invalidate the analysis but warrants discussion of other driving factors.

### Trivial
None.

## Nice-to-Haves

- Add multi-seed variance estimates at least for the 30B model to secure the scaling claim.
- Provide a simplified "recurrent token refinement" baseline (select k% of tokens by an alternative criterion and reprocess them) to control for the effect of extra computation itself.
- Discuss whether the learnable β parameter in Equation (4) is constrained (β·p^i can exceed 1 if β > 1 and p^i is close to 1).
- Discuss the FLOPs/throughput gap and report throughput at batch sizes > 1.
- Clarify SFT data composition and training budgets for reproducibility.

## Removed Points (filtered from input review)

These points are flagged to be removed; treat them with caution.

- **"CMMMLU" typo (line 195):** Per policy, remove all formatting/typo nitpicks. The paper lists "CMMMLU" in Section 4.1 but uses "CMMLU" in Table 2 — likely a typo.
- **Hyperparameter values deferred to appendix (λ_sd, λ_dp, α, γ, buffer size):** The paper states these are in Appendix Sec. B, which the parser stripped. Per policy, remove criticisms about missing appendix content.
- **Layer normalization interaction question (re-applying the same layer's normalization):** This is a technical question about a design detail, not a demonstrated weakness. The paper describes the architecture at the appropriate level of detail for a conference paper.
- **Score dispersion normalization issue (p^i/Σp^j discarding absolute scale):** A theoretical observation; the distribution preservation loss (pulling scores toward 0.5) addresses this by preventing uniformly low scores from having high entropy.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the severity of the variance issue for the 30B scaling claim and the strength of the mechanistic entropy analysis, but these align with observations the paper itself raises.

## Suggestions

1. **Add multi-seed variance estimates** for the 30B model results (Table 2). Even two seeds would allow the reader to assess whether the small per-task deltas are real.
2. **Explicitly state L_s:L_e** for the 30B model (42 layers per Fig. 7a).
3. **Discuss the FLOPs/throughput gap** and report throughput at batch sizes > 1.
4. **Provide a simplified recurrent refinement baseline** to isolate the effect of DND's routing strategy from the benefit of extra computation.
5. **Clarify SFT data composition** and whether baseline SFT and DND+SFT use identical data and budgets.

---

**Calibration summary.** All retrieved anchors:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to DND |
|---|---|---|---|---|---|
| Learning How Hard to Think | 6qUUgw9bAZ.md | 6.50 | R1 | Yes | Weaker strength profile (+9.83 vs +10.00/+9.99), more severe weaknesses (-9.99, -10.00, -9.28 vs DND's one -9.11) |
| LazyLLM | am5Z8dXoaV.md | 5.00 | R1 | Yes | Similar token-selection theme but multiple -9+ weaknesses and a Reject decision |
| EfficientSkip | 7DY2DFDT0T.md | 2.50 | R1 | Yes | Very limited experiments (single model, single benchmark), no baselines |
| CoTFormer | 7igPXQFupX.md | 5.75 | R1 | Yes | Moderate strengths but weak downstream results, misleading claims, unclear architecture |
| Selective Attention | v0FzmPCd1e.md | 6.75 | R2 | Yes | Four severe weaknesses (-9.99, -9.93, -9.61, -8.69) vs DND's one; DND has cleaner profile |
| SWIFT | EKJhH5D5wA.md | 6.25 | R2 | Yes | Weaker strengths; multiple moderate weaknesses |
| Unreasonable Ineffectiveness | ngmEcEer8a.md | 6.50 | R2 | Yes | Two -9+ weaknesses; strengths comparable |
| FlexPrefill | OfjIlbelrT.md | 8.00 | R1 | No | Sparse attention method; higher average scores but different evaluation standard |
| Demystifying Token Dynamics | qtTIP5Gjc5.md | 7.50 | R2 | No | Theoretical SSM paper; not directly comparable |
| ReDeEP | ztzDzdgfrh.md | 7.33 | R2 | No | Hallucination detection for RAG; different subfield |

**Round 1 bracket:** 6.0–7.0 (based on comparable adaptive-computation papers). **Narrowing:** DND's strength profile (+10.00, +9.99, +8.91) exceeds that of comparable 6.25–6.75 anchors, and its weakness profile (one -9.11, one -8.50, remainder near 0) is cleaner than any anchor in that range. The 30B model's consistent positive improvement across 17 benchmarks mitigates the main weakness's severity. DND is placed clearly above Selective Attention (6.75) but below the 7.5+ tier.

**Final score: 7.0**

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>