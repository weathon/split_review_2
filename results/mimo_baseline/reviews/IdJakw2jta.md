## Summary
This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the task from ~20-second videos to 1–5 minute videos. The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with memory-augmented spatial and temporal decoders, text-similarity-based spatial memory selection, event-boundary-based temporal memory selection, and a cascaded spatio-temporal decoder design. They extend the HCSTVG-v2 validation set to create five LF-STVG benchmarks and demonstrate significant improvements over existing methods.

## Strengths
- **Well-motivated problem formulation.** The gap between short-form STVG research (20–35 second videos) and real-world applications (minutes to hours) is clearly articulated and practically relevant. The progressive degradation of existing methods on longer videos (Fig. 2, Table 1) convincingly motivates the need for dedicated long-form approaches.
- **Comprehensive ablation studies.** Tables 2–6 systematically validate each proposed component: selective temporal memory (+13.4% m.tIoU over using all memories), selective spatial memory (+0.9%), cascaded vs. parallel design (+1.5%), and the effect of training video length. The ablations are well-structured and informative.
- **Competitive short-form performance.** Despite being designed for long-form, ART-STVG achieves 59.2/39.2 m.tIoU/m.vIoU on short-form HCSTVG-v2 (Table 7), only 1.2/1.0 points behind the SOTA, demonstrating that the autoregressive design does not sacrifice short-form capability.

## Weaknesses
### Fatal
None.

### Major
- **Evaluation limited to a single extended dataset.** Only the HCSTVG-v2 validation set is extended to create LF-STVG benchmarks. The paper acknowledges this is because HCSTVG-v2 is the only dataset with available source videos, but this significantly limits the generalizability of the findings. The results could be specific to the characteristics of this particular dataset (complex multi-person surveillance scenes).
- **Training never sees long videos.** All models are trained exclusively on 20-second clips (64 frames at 3.2 FPS). While Table 6 shows a brief experiment with 40-second training videos, the core model is never trained on the 1–5 minute videos it is evaluated on. This raises questions about whether the improvements come from the architecture genuinely handling long-form content or simply from the autoregressive structure being more robust to distribution shift at test time.
- **Low absolute performance.** On LF-STVG-3min, the best m.tIoU is 23.0% and m.vIoU is 15.3%. On LF-STVG-5min, these drop to 15.0% and 10.0%. While the relative improvements over baselines are large, the absolute numbers suggest the task remains largely unsolved and the method's practical utility is limited.

### Minor
- **No comparison with general long-video memory methods.** The paper cites MA-LMM (He et al., 2024) and other memory-augmented video understanding methods in related work but does not adapt or compare against them. Even a simple baseline using these memory mechanisms for STVG would strengthen the claims about the specific design choices in ART-STVG.
- **Memory selection strategies are relatively simple heuristics.** Spatial memory selection uses text-query similarity to pick top-N memories; temporal memory selection uses adjacent-frame cosine similarity for event boundary detection. While effective, these are straightforward heuristics without theoretical justification for why they are optimal. The paper would benefit from more analysis of failure cases or limitations of these strategies.
- **The "first" claim is overstated.** The paper claims to be "the first to explore the LF-STVG problem." While technically this specific formulation may be new, long-video understanding with memory mechanisms is well-studied, and the autoregressive frame-by-frame processing with memory is a natural adaptation rather than a fundamentally new paradigm.

### Trivial
None.

## Nice-to-Haves
- A comparison showing how the method scales with even longer videos (10+ minutes) would strengthen the long-form motivation.
- Analysis of computational cost (inference time, memory usage) compared to existing methods processing the same long videos would be valuable, since the autoregressive approach trades GPU memory for sequential processing time.
- Visualization of the temporal memory selection process on actual long videos to show how event boundaries are detected would complement Fig. 6.

## Novel Insights
The key insight—that existing STVG methods degrade dramatically as video length increases, and that this degradation accelerates non-linearly (Fig. 2)—is genuinely useful for the community. The finding that using *all* temporal memories actually *hurts* performance (Table 2, row ❷ vs ❶: 9.6% vs 16.7% m.tIoU) is a striking result that highlights how naively accumulating context in long videos introduces harmful noise, making the case for selective memory mechanisms.

## Suggestions
- Extend the evaluation to at least one additional dataset (e.g., create long-form versions of VidSTG or other STVG benchmarks) to demonstrate generalizability.
- Include a computational analysis comparing ART-STVG's sequential processing against baselines that must process all frames at once, as this is a key practical advantage claimed but never quantified.
- Consider training on a mix of short and long videos to better bridge the domain gap between training and evaluation.

## Score and Decision
The paper presents a reasonable problem formulation and a technically sound method with thorough ablations. However, the evaluation is limited to a single extended dataset, the model is never trained on long videos, absolute performance remains low, and the individual components (memory banks, top-N selection, event boundary detection) are relatively simple adaptations of existing ideas. The contribution is incremental rather than transformative.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject