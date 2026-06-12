## Summary

This paper identifies that standard Rotary Position Embedding (RoPE) discards the imaginary part of the complex-valued attention computation. The authors propose **RoPE++**, which re-incorporates this imaginary component as additional attention heads (Imaginary Attention) that naturally capture long-range dependencies. Two configurations are introduced—RoPE++_EH (equal number of heads, halved KV cache) and RoPE++_EC (equal cache, doubled heads)—both preserving the unified absolute–relative position embedding format. Pre-training experiments at 376M and 776M scales demonstrate consistent improvements over vanilla RoPE and other baselines on short- and long-context benchmarks, with larger gains at longer contexts.

## Strengths

- **Novel and elegant idea**: The observation that the discarded imaginary part of RoPE can be useful for long-context modeling is insightful. The method itself is simple: rotating query vectors by -π/2 before applying standard RoPE requires almost no additional parameters or change to KV cache.
- **Two practical configurations**: RoPE++_EH and RoPE++_EC offer a clean trade-off between KV-cache savings (half the cache) and performance gains (more heads at the same cache cost), giving practitioners flexibility.
- **Comprehensive empirical validation**: Experiments cover two model sizes (376M, 776M), multiple baselines (RoPE, FoPE, Pythia, ALiBi), short-context and long-context benchmarks (RULER, BABILong up to 64k), and combinations with interpolation methods (YaRN, Linear PI). Results consistently show RoPE++ outperforms vanilla RoPE, especially on long-context tasks.
- **Insightful analysis**: Attention-pattern visualizations confirm that imaginary heads attend more globally, and noise-perturbation experiments demonstrate that degrading imaginary attention hurts long-context accuracy more than degrading real attention, supporting the claim that imaginary attention is dominant for long-range modeling.
- **Efficiency gains clearly demonstrated**: For RoPE++_EH, memory cost and decoding speed are improved, with the margin widening as context length increases.

## Weaknesses

### Fatal
None.

### Major
1. **Limited model scale**: Experiments are only carried out up to 776M parameters. While this is acceptable for a methods paper, the long-context community typically works with much larger models (7B+). The paper does not discuss potential scaling issues or provide evidence that the benefits transfer to larger models. This limitation reduces confidence in the method’s practical impact.
2. **Theoretical justification is heuristic**: The characteristic-curve analysis relies on an integral approximation of the sine function over frequency range, and the argument that imaginary attention “captures longer dependency” is qualitative (the sine integral decays slowly but does not monotonically separate from real attention in a rigorous way). The empirical evidence is stronger, but the paper would benefit from a more formal or bound-based treatment.
3. **Incomplete comparison with recent RoPE variants**: The paper compares with basic baselines (RoPE, FoPE, Pythia, ALiBi) and combines RoPE++ with YaRN/PI, but it does not directly compare RoPE++ (without interpolation) against other recent long-context position-embedding designs such as ReRoPE, NTK-aware scaling (without the proposed extension), or other works that modify RoPE’s intrinsic computation (e.g., HFPE). While the paper focuses on the imaginary part, a head-to-head against more SOTA RoPE modifications would strengthen the contribution.

### Minor
- The claim that configurations with arbitrary ratios of imaginary/real heads are “impossible” could be clarified. Since real and imaginary heads share query parameters but can have different output projections, one could in principle allocate more heads to the imaginary group. The paper’s reasoning (rotating back gives real attention) is not entirely convincing and may be a limitation of the specific design.
- The integral approximation in Equation 5 uses the range \([10^{-4},1]\) but the actual RoPE frequency distribution is discretized over \(d/2\) values; the approximation is rough, especially for small model dimensions. The qualitative conclusion is likely unaffected, but the derivation could be more precise.

### Trivial
None.

## Nice-to-Haves
- Experiments on larger models (e.g., 7B) to verify scalability.
- Direct comparison with other recent RoPE modifications that also aim at long-context (e.g., NTK-aware scaling alone, YaRN alone, ReRoPE) without combining with the proposed method.
- Ablation study varying the number of imaginary heads (if feasible under the current design) to better understand the trade-off.

## Novel Insights
The paper provides a clean and previously overlooked perspective: the imaginary component of the complex-valued RoPE attention score, which is discarded in standard implementations, naturally encodes long-range positional information (through the sine integral’s slow decay). By re-introducing it as a separate set of attention heads, the model gains a built-in mechanism for attending to distant tokens without any new positional parameters. This is a genuinely novel insight that goes beyond typical “add more frequencies” or “interpolate” approaches.

## Suggestions
- Include at least one experiment at a larger scale (e.g., 1.4B or 3B) to demonstrate that the benefits persist with more capacity.
- In the main comparison tables, add a column for “RoPE + YaRN” (without RoPE++) so that readers can see the gain from RoPE++ alone above the interpolation baseline.
- Clarify the “impossible” claim about ratio configurations with a more detailed explanation or an empirical test of a mixed allocation.

## Score and Decision
**Score**: 6

**Decision**: Accept

**Rationale**: The paper presents a simple, well-motivated, and empirically validated improvement to the most widely used positional encoding in modern LLMs. The idea is novel and the experimental evidence is solid, though limited in model scale. The weaknesses are not fatal and can be addressed in future work. The contribution is significant enough for acceptance at ICLR, where novel architectural insights are valued.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>