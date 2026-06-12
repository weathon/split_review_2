## Summary

This paper addresses the question of how close current image watermarking methods are to the theoretical limits of message-carrying capacity. It derives upper bounds on watermarking capacity under PSNR and robustness constraints using a geometric framework (counting integer lattice points in intersections of PSNR balls and image cubes), revealing that theoretical capacities are orders of magnitude above what current methods achieve. Through controlled experiments, the paper isolates the source of the gap to architectural limitations rather than data distribution or robustness constraints, and demonstrates this by training "Chunky Seal," a scaled-up Video Seal that achieves 1024-bit capacity with comparable quality and robustness.

## Strengths

- **Well-formulated research question with clear significance.** The paper identifies an important and previously under-studied question—whether current watermarking methods approach fundamental limits—and provides a systematic framework to answer it. The finding that theoretical capacity is 2+ bpp while practical methods achieve ~0.001 bpp is striking and actionable.

- **Rigorous experimental design for isolating causes.** The paper methodically eliminates explanations A–D (complex robustness, perceptual constraints, data distribution, and unrealistic bounds) through a series of controlled experiments on simplified setups. The progression from VideoSeal failing at 1024 bits to linear models succeeding at 2048 bits, to tiling achieving 32,768 bits, to the handcrafted method reaching 456,509 bits (Table 1) is compelling and well-executed.

- **Practical contribution with Chunky Seal.** The 4× capacity increase to 1024 bits while maintaining quality and robustness (Table 3) demonstrates that capacity improvements are achievable without sacrificing the other watermarking desiderata. The proposed sanity checks (linear capacity scaling with resolution, predictable drops under stronger augmentations, etc.) provide useful guidance for the field.

- **Clear and comprehensive theoretical treatment.** The geometric framework (box-ball intersection analysis) is intuitive and well-presented with multiple bounds for different regimes (low/medium/high PSNR, gray vs. arbitrary images, with/without robustness). The progression from absolute capacity through increasingly constrained scenarios is logical.

## Weaknesses

### Fatal

None.

### Major

- **Heuristic robustness bounds weaken the main narrative.** The PSNR-only bounds are rigorous and their achievability is demonstrated experimentally. However, the bounds under robustness constraints (Bounds 10–12) are explicitly described as heuristic, with acknowledged cases of both over- and under-approximation. While the conservative Bound 13 still suggests meaningful capacity, the paper's central Figure 1 comparison between theoretical bounds and empirical methods relies substantially on these heuristic bounds, making the precise magnitude of the gap under realistic robustness constraints uncertain. This limits the strength of the conclusion that even robust models are underperforming relative to theory.

- **Architectural innovation claim is only weakly demonstrated.** Chunky Seal achieves 0.0052 bpp at 1024 bits, while the theoretical bound at 40 dB PSNR without robustness is ~2 bpp. Even under robustness constraints, the heuristic bounds suggest ~0.5 bpp. Chunky Seal thus achieves only ~1% of the robust bound's capacity, achieved through a 90× larger embedder and 23× larger extractor. The paper acknowledges this and notes the purpose was feasibility demonstration rather than deployment, but this leaves open whether the remaining ~100× gap is closable with architectural innovation or represents a more fundamental barrier under realistic constraints.

### Minor

- **The handcrafted method's practical relevance is limited.** The handcrafted cube-in-ball embedder (Equation 2) achieves impressive capacity on gray images with PSNR-only constraints but exploits a setup (fixed gray cover, no robustness requirements, pixel-level redundancy) that is far from any realistic watermarking scenario. While it effectively demonstrates the bounds are achievable, it provides little guidance for closing the gap under realistic conditions.

- **Single-image training may not capture important loss landscape properties.** The simplified gray-image experiments could be affected by the triviality of the data distribution in ways that don't generalize. The linear embedder succeeding here doesn't necessarily imply that architectural modifications to VideoSeal alone are the bottleneck under realistic training conditions.

### Trivial

None.

## Nice-to-Haves

- A visualization or analysis of what the learned VideoSeal embedder actually does on the gray-image task (e.g., what spatial patterns it uses) could illuminate why it fails where linear models succeed, offering more actionable architectural insights.
- Experiments on the middle ground between the simplified gray-image setup and full robustness (e.g., adding one robustness constraint at a time) would help quantify how much each realistic constraint narrows the gap.
- Discussion of whether the linearly-approximated JPEG (LinJPEG) faithfully captures the capacity-reducing effects of real JPEG quantization, which involves highly nonlinear rounding.

## Novel Insights

The paper's most novel insight is the systematic demonstration that the capacity gap in watermarking is primarily an architectural and training-methodology problem rather than a fundamental information-theoretic limitation. By bringing models to the simplified theoretical setup rather than trying to make theory more realistic, the paper effectively flips the usual approach—showing that even under maximally simplified conditions, state-of-the-art models fail to approach achievable capacities. The observation that VideoSeal performs identically at 256×256px and 32×32px (failing to exploit resolution scaling) is a particularly striking diagnostic that points to specific architectural deficiencies. The proposed sanity checks for future watermarking methods (linear scaling, outperforming simple baselines, predictable degradation) constitute a useful methodological contribution beyond the specific results.

## Suggestions

- Include experiments interpolating between the simplified setup and full robustness to quantify how much each constraint type contributes to the empirical gap, which would strengthen the argument about where architectural innovation is most needed.
- Provide more analysis of why the VideoSeal architecture fails in the simplified setup—e.g., ablations on specific architectural components (skip connections, activation functions, normalization) to identify the bottleneck.
- Discuss the practical implications of Chunky Seal's 1024-bit capacity for concrete applications (e.g., the C2PA manifest embedding mentioned in the discussion) to better motivate why closing the remaining gap matters.

## Score and Decision

This paper makes a valuable contribution by rigorously establishing that current watermarking methods operate far below theoretical capacity limits, providing a clear experimental methodology for diagnosing the gap, and demonstrating that scaling can partially close it. The theoretical analysis is comprehensive and the experiments are well-designed. The main weakness—the heuristic nature of robustness bounds and the limited demonstration that the gap is closable under realistic constraints—prevents a higher score but does not undermine the core contributions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>