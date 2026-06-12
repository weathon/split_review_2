## Summary
This paper identifies that standard RoPE discards the imaginary component of the complex-valued attention score, and proposes RoPE++ to re-incorporate it as additional attention heads. Two configurations are introduced: RoPE++EC (equal cache, doubled heads) and RoPE++EH (equal heads, halved KV cache). Experiments at 376M and 776M scales demonstrate consistent improvements over standard RoPE and other position embeddings on both short- and long-context benchmarks, with the gains becoming more pronounced at longer context lengths.

## Strengths
- **Clean theoretical motivation with novel analysis.** The paper provides a rigorous decomposition of RoPE's complex attention into real and imaginary components, showing that imaginary attention has a sine-integral characteristic curve (Equation 5) that decays more slowly than the cosine-integral curve of real attention, thereby better capturing long-range dependencies. This is a genuinely insightful mathematical observation that has not been previously highlighted.
- **Preservation of RoPE's key property.** The imaginary attention retains the unified absolute–relative position embedding format (Equation 3-4), requiring only a −π/2 rotation on queries. This makes the method a minimal, elegant modification that integrates seamlessly with existing RoPE-based architectures, FlashAttention, and GQA.
- **Comprehensive experimental evaluation.** The paper evaluates across two model sizes, multiple short-context benchmarks (WikiText, LAMBADA, Open LLM Leaderboard suite), two long-context benchmarks (RULER up to 64k, BABILong up to 64k), and combinations with existing interpolation methods (YaRN, Linear PI). The noise-injection ablation in Section 5.2 provides strong evidence that imaginary attention plays a more dominant role in long-context modeling (5–8 point gap at σ=1.0).
- **Practical efficiency benefits.** RoPE++EH halves KV cache while maintaining comparable or better performance, with measured reductions in memory cost and TPOT (Figure 4). This positions the method as both a performance improvement and an efficiency tool.

## Weaknesses
### Fatal
None.

### Major
- **Limited scale of experiments.** The models are trained at 376M and 776M parameters on only 50B tokens, which is far below the regime of modern LLMs. While the authors note this limitation, the improvements are modest on short-context tasks (~0.8-1.0 points on average), and it remains unclear whether these gains would persist, diminish, or grow at larger scales. This significantly limits confidence in the practical impact of the contribution.
- **Confounding factors in EC comparison.** RoPE++EC doubles the number of attention heads (doubling the output projection Wo) while keeping cache size equal to RoPE. This means the model has additional parameters, making the comparison with vanilla RoPE not purely about position encoding. The paper acknowledges this but does not isolate the contribution of extra parameters from the benefit of imaginary attention.

### Minor
- **No ablation on the 50/50 split constraint.** The paper states that configurations like 75% imaginary / 25% real are "impossible" since rotating q by π/2 maps imaginary back to real. This limits the design space and could benefit from discussion of whether partial rotations or other modifications could relax this constraint.
- **Length extrapolation claims lack direct experimental validation.** Section 3.4 provides an interesting theoretical argument that RoPE++ exposes dimensions to both positive and negative embeddings earlier, but Table 2 shows that extrapolation beyond 32k still degrades substantially (e.g., 376M RoPE++EC RULER drops from 17.7 at 32k to 9.0 at 64k). A dedicated extrapolation experiment (training at 4k, evaluating at 8k/16k/32k without continued training) would strengthen this claim.

### Trivial
None.

## Nice-to-Haves
- Experiments at 1B+ scale or with longer training would substantially strengthen the paper's impact claims.
- Analysis of whether the imaginary heads learn different frequency spectra than real heads during training would deepen understanding.
- A comparison with simply doubling the number of standard RoPE heads (same total parameters as EC) would help isolate the contribution of the imaginary component versus just having more heads.

## Novel Insights
The paper's most novel insight is the mathematical characterization of imaginary attention's characteristic curve as a sine integral that maintains stronger long-range coupling than the cosine integral of real attention. The observation that RoPE++ exposes query-key dimensions to both positive and negative position embeddings during pre-training (expanding the trained embedding range) is a clean theoretical contribution that explains the improved length extrapolation. Additionally, the noise-injection experiment provides compelling evidence that real and imaginary attention heads specialize differently—imaginary heads for global/long-context information and real heads for local semantics—offering a new lens for understanding attention head specialization in transformer models.

## Suggestions
- Scale experiments to at least 1.3B parameters with longer pre-training to establish that improvements hold at practical model sizes.
- Add an ablation where RoPE++EC's extra parameters are compensated by reducing the base model's head count, to disentangle the effect of imaginary attention from simply having more heads.
- Include a direct extrapolation evaluation (train at 4k, test at longer lengths without continued pre-training) to validate the theoretical claims in Section 3.4.

## Score and Decision
The paper presents an elegant and well-motivated modification to RoPE with solid theoretical analysis and consistent experimental results. However, the modest model scales and the confounding factor of extra parameters in the EC variant limit the strength of the contribution. The core idea is clean and the mathematical analysis adds genuine value to the understanding of RoPE, but the practical impact remains uncertain at current experimental scales.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>