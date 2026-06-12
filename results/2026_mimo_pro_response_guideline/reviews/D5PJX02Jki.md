Now I have enough data. Let me compile the final review with calibration.

**Calibration round 1 bracket**: Based on the anchors, I initially bracket this paper between 5.5 and 6.5. The most relevant anchors are:
- "Scaling Laws of RoPE-based Extrapolation" (5.0, Accept) — similar RoPE theory work but weaker empirical validation
- "Wavelet-based Positional Representation" (5.25, Accept) — related PE innovation with marginal results
- "Round and Round We Go!" (6.20, Accept) — analysis paper about RoPE internals, no new PE proposed
- "STRing" (6.50, Accept) — RoPE-based improvement with much larger scale experiments

This paper has a cleaner theoretical contribution than Scaling Laws and Wavelet, and more practical novelty than Round and Round, but less scale evidence than STRing. It sits between 5.5 and 6.5.

---

## Summary
This paper proposes RoPE++, which re-incorporates the discarded imaginary component of RoPE's complex-valued attention score as a parallel group of attention heads. The authors show theoretically that the imaginary attention has a sine-integral characteristic curve that decays much more slowly than the real part's cosine-integral curve, making it better suited for capturing long-range dependencies. Two configurations are proposed: RoPE++_EC (equal cache, doubled heads) and RoPE++_EH (equal heads, halved cache), evaluated at 376M and 776M model scales.

## Strengths
- **Elegant mathematical formulation**: The −π/2 query rotation trick (Equation 4) cleanly recovers the imaginary component while preserving RoPE's relative/absolute PE duality. The characteristic curve analysis (Equation 5) showing Si(Δt) converges to π/2 rather than decaying to zero is a genuine, non-obvious insight that provides principled motivation for the method.
- **Consistent long-context gains from RoPE++_EC**: Table 2 shows EC outperforms RoPE on RULER at all context lengths for both 376M (Avg 25.0 vs 18.8) and 776M (Avg 29.4 vs 27.4), with growing margins at longer contexts. On BABILong at 776M, EC achieves 24.1 vs RoPE's 22.8.
- **Novel length extrapolation argument**: Section 3.4's observation that imaginary attention exposes even-index query dimensions to both positive and negative position embeddings during pre-training (Figure 3), eliminating OOD negative embeddings at extrapolation lengths, is an independently valuable theoretical contribution.
- **Practical efficiency with no KV cache overhead**: Since key embeddings are unchanged, real and imaginary attention can be computed in a single FlashAttention pass. RoPE++_EH halves KV cache with demonstrated memory/throughput gains (Figure 4).
- **Complementary to existing techniques**: Table 3 shows RoPE++_EC consistently improves when combined with Linear PI and YaRN, demonstrating the method is not merely subsuming existing approaches.
- **Causal ablation via noise injection**: Figure 5(e,j) shows 5–8 point larger drops when imaginary attention is corrupted vs. real attention, providing direct evidence for imaginary heads' dominance in long-context tasks.

## Weaknesses

### Fatal
None.

### Major
- **RoPE++_EH significantly regresses on BABILong at 776M without discussion**: In Table 2, EH achieves BABILong avg 19.4 vs RoPE's 22.8 — a consistent regression across nearly all context lengths (31.9 vs 33.5 at 2k, 26.5 vs 30.7 at 4k, 18.6 vs 23.6 at 8k, 16.2 vs 22.0 at 16k, 11.0 vs 15.1 at 32k). This is concerning because the paper's central theoretical claim is that imaginary attention's slower-decaying characteristic curve inherently improves long-context modeling. If this were sufficient, EH should not regress on a long-context benchmark. The paper does not discuss or explain this regression. While EC is the primary variant and EH is presented as an efficiency alternative, this result raises the question of whether the imaginary attention benefit depends primarily on having doubled head capacity rather than being an inherent property of the imaginary component itself.

- **No variance or error bars reported; small margins may be within noise**: The average improvements of RoPE++_EC over RoPE on short-context tasks are roughly 0.5–1.0 points (Table 1: 41.0 vs 40.5 at 376M Short, 42.8 vs 42.6 at 776M Short). At these small model scales with 50B tokens, pre-training is sensitive to random seeds. Without any measure of variance, it is impossible to assess whether these differences are meaningful. This directly affects whether Table 1 supports the claim that RoPE++ "outperforms vanilla RoPE and other position embeddings on average."

- **Incomplete cost accounting for RoPE++_EC**: The paper states EC operates "under the fixed QKV parameter budget" (line 99) and describes this as "the only cost," but then acknowledges W_o is doubled (line 101). Additionally, EC roughly doubles the attention compute (twice as many query heads). The framing as having minimal cost is misleading; a clear FLOPs and total-parameter comparison with baseline RoPE would be more transparent.

### Minor
- **Experiments limited to 376M–776M with 50B training tokens**: These are roughly three orders of magnitude smaller than current frontier models. While this is an evidential limitation rather than a methodological flaw, the claims about practical significance for long-context LLMs are currently unsupported at representative scales.
- **Long-context comparison excludes baselines other than RoPE**: FoPE, Pythia, and ALiBi appear only in Table 1 (4k short-context). Table 2 compares only RoPE vs RoPE++ variants. While RoPE is the most relevant baseline, excluding other methods from the long-context setting narrows the evaluation.
- **Noise experiment does not normalize for attention score scale**: Adding Gaussian noise with equal σ to both real and imaginary attention could be more disruptive to whichever operates at a smaller scale. Reporting the ratio of noise σ to attention score σ would strengthen the claim that imaginary heads are more important (Section 5.2).

### Trivial
None.

## Nice-to-Haves
- Discussion of how RoPE++ interacts with attention sinks (the phenomenon where initial tokens receive disproportionately high attention), especially given the attention patterns shown in Figure 5.
- Reporting training loss curves to show whether the imaginary component introduces optimization challenges.
- Hyperparameter sensitivity analysis (learning rate, rotary base) for a new PE method.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Criticism about missing related works: cannot verify external sources.
- Any formatting/style issues: parser artifacts, not paper problems.
- Reproducibility concerns about hyperparameter disclosure: trivial for this type of paper.

## Novel Insights
The characteristic curve analysis (Equation 5) showing the sine integral's slower decay is genuinely novel — it provides a principled, non-obvious mathematical explanation for why a complementary positional signal would benefit long-context modeling. The length extrapolation argument about OOD negative embeddings (Section 3.4, Figure 3) is also independently valuable, offering a mechanistic explanation for improved extrapolation that differs from the standard approach of scaling the rotary base.

## Suggestions
- Add seed variance for main results (even 2–3 seeds) to validate the 0.5–1.0 point short-context margins.
- Directly address the EH regression on BABILong at 776M — is it the halved value capacity? Is BABILong more sensitive to value diversity? This analysis would deepen understanding of when imaginary attention helps.
- Provide an explicit FLOPs and total-parameter comparison table for RoPE, RoPE++_EC, and RoPE++_EH to transparently communicate EC's compute overhead.

---

**Calibration anchors retrieved:**

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| Scaling Laws of RoPE-based Extrapolation | JO7k0SJ5V6.md | 5.00 | 1 | Similar RoPE theory, but weaker empirical validation and overlap with YaRN |
| Wavelet-based Positional Representation | OhauMUNW8T.md | 5.25 | 1 | Related PE innovation, marginal improvements, accepted |
| Contextual Position Encoding (COPE) | sIGWTd1DcW.md | 5.25 | 1 | Position encoding improvement, rejected |
| DAPE V2 | XT1Cx6cH2a.md | 5.33 | 1 | Length extrapolation via attention score processing |
| Round and Round We Go! | GtvuNrk58a.md | 6.20 | 1 | RoPE analysis paper with novel insights, no new PE proposed |
| Why Does Effective Context Length Fall Short? (STRing) | eoln5WgrPx.md | 6.50 | 1 | RoPE-based improvement with much larger scale (Llama 70B) |
| CLEX | wXpSidPpc5.md | 6.50 | 1 | Continuous length extrapolation, accepted |
| TAPE | Us1RXG1Ji2.md | 6.00 | 1 | Contextualized equivariant PE, rejected |

**Round 1 bracket**: 5.5–6.5. This paper sits above Wavelet (5.25) due to cleaner theory and more convincing empirical results, near Round and Round (6.20) which has comparable novelty but only analysis (no method), and below STRing (6.50) which validates at much larger scale.

**Final score reasoning**: 6.0. The core theoretical contribution (imaginary attention characteristic curve) is strong and novel, and EC shows convincing long-context improvements. However, the EH regression on BABILong without explanation, the lack of variance for small margins, and the limited scale prevent a higher score. The paper is clearly above the "marginal improvement" threshold of Wavelet (5.25) but below the "strong practical impact" threshold of STRing (6.50).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>