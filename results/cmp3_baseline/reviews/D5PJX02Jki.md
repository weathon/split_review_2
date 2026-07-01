## Summary

This paper identifies that standard Rotary Position Embeddings (RoPE) discard the imaginary component of the complex-valued attention score, losing potentially useful phase information. To address this, the authors propose **RoPE++**, which re-incorporates the imaginary part as a separate set of attention heads (imaginary attention) computed in parallel with the real attention. Two configurations are introduced: RoPE++<sub>EH</sub> (equal number of attention heads, halved KV cache) and RoPE++<sub>EC</sub> (equal cache size, doubled attention heads). Theoretical analysis and pre-training experiments at 376M and 776M parameter scales show that RoPE++ consistently outperforms vanilla RoPE and other position embeddings on both short- and long-context benchmarks, with the imaginary heads playing a dominant role in long-context modeling.

## Strengths

- **Novel and well-motivated idea**: The paper identifies a previously overlooked limitation of standard RoPE—the discarding of the imaginary component—and provides a simple yet effective method to re-introduce it. This is a conceptually clean extension that preserves the elegant rotation formulation of RoPE.
- **Two practical configurations**: RoPE++<sub>EH</sub> and RoPE++<sub>EC</sub> offer a useful efficiency–performance trade-off. The empirical results show that RoPE++<sub>EH</sub> can match or exceed vanilla RoPE performance while halving the KV cache, and RoPE++<sub>EC</sub> yields significant gains at the same cache cost.
- **Solid experimental validation**: The paper evaluates at two model sizes (376M and 776M) across a wide range of short-context (11 tasks) and long-context (RULER, BABILong) benchmarks. The results consistently show improvements, especially on long-context tasks where the gains are substantial. The ablation study (Gaussian noise on real vs. imaginary attention) convincingly demonstrates that imaginary attention is more critical for long-context performance.
- **Compatibility with existing techniques**: RoPE++ is shown to combine well with other long-context methods (Linear PI, YaRN) and with NTK-aware scaling, indicating its generality and practical applicability.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical justification of long-context capture is not fully rigorous**: The paper argues that imaginary attention captures longer dependencies because its characteristic curve (approximated by a sine integral) decays more slowly than the cosine integral of real attention. However, the sine integral is oscillatory and does not have a monotonic decay; the claim that it “assigns more weight to the long-context region” needs stronger support, either through a more careful mathematical analysis (e.g., average over frequencies in a specific regime) or additional empirical analysis of attention distance distributions on real data. The current argument, while plausible, is somewhat hand-wavy.
- **Limited model scale**: Experiments are conducted only up to 776M parameters. While this is acceptable for a method paper, the community would benefit from seeing results at larger scales (e.g., 7B+), where position-embedding effects may differ and where the KV-cache savings of RoPE++<sub>EH</sub> would be even more impactful. Scalability is not addressed.
- **Parameter and cache reduction claim for RoPE++<sub>EH</sub> is insufficiently clarified**: The paper states that RoPE++<sub>EH</sub> “keeps equal attention head number while halving QKV parameters as well as KV cache”, but the description of how heads are shared and how the output projection size changes is somewhat ambiguous. A concrete example with parameter counts (e.g., original H=32 vs. RoPE++<sub>EH</sub> configuration) would greatly improve clarity. The efficiency experiments (Figure 4) are helpful but do not fully resolve the architectural confusion.

### Minor
- **Lack of baselines**: The main short-context evaluation compares RoPE++ with RoPE, FoPE, Pythia, and ALiBi, but does not include other important RoPE variants such as NTK-aware scaling or dynamic NTK as direct baselines (these only appear in combination with RoPE++ in Table 3). While the paper focuses on the core idea, a direct comparison with these widely used methods would strengthen the experimental section.
- **The negative imaginary part notation**: The paper uses the negative imaginary part as the “imaginary attention”. While this is explained, the reason for this convention could be better justified beyond the semantic-aggregation argument. The notation could be streamlined to avoid confusion.

### Trivial
- Some equation formatting appears garbled (e.g., summation indices in Equations 1 and 2), but this is likely a PDF parsing artifact and does not affect understanding.

## Nice-to-Haves

- Extend experiments to a 7B-scale model to demonstrate scalability and confirm the benefits at larger sizes.
- Provide a more rigorous theoretical analysis of the imaginary attention’s long-context behavior, perhaps by analyzing the expected attention distance under a uniform distribution of query–key dot products.
- Include a direct comparison with other RoPE variants (e.g., NTK-aware, dynamic NTK) in the main short-context table to solidify the performance advantage.

## Novel Insights

Beyond the paper’s own contributions, the most interesting insight is that the *discarded* part of the RoPE computation carries complementary positional information that is especially valuable for long-range dependencies. This suggests that complex-valued representations in attention may have underutilized potential beyond their conventional use for absolute–relative position encoding. The idea of treating the real and imaginary components as separate but coupled attention heads is elegant and could inspire further work on richer position-encoding designs that make full use of the complex plane.

## Suggestions

- In Section 3.3, add a concrete parameter-count example to clarify the mechanism of RoPE++<sub>EH</sub>. For instance, if the original model has 32 heads per layer, RoPE++<sub>EH</sub> would have 16 real heads and 16 imaginary heads? Actually the description suggests the same query is used for both real and imaginary, so the number of head groups changes. A clear schematic with dimensions would help.
- In Section 3.2, strengthen the theoretical argument by analyzing the area under the sine integral vs. cosine integral over the trained range, or by showing that the imaginary attention has a slower decay in expectation under plausible attention-weight distributions.

## Score and Decision

Score: 7

Decision: Accept

MY FINAL SCORE: 7
MY FINAL DECISION: Accept