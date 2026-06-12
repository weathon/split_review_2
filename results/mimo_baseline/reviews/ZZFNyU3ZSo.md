## Summary

The paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers that assigns separate routers for different tasks (generation vs. understanding) rather than using a single shared router. The approach is motivated by empirical analyses showing that token redundancy patterns differ significantly across tasks and layers. Applied to Show-o and Emu3, UniMoD reduces training FLOPs by approximately 15% and 40% respectively while maintaining or improving performance on multimodal understanding and generation benchmarks.

## Strengths

- **Thorough empirical analysis as motivation.** The paper provides three complementary analyses—attention weight patterns across 4 models (Fig. 2), ARank-based token redundancy measurements across layers (Fig. 3), and task interaction experiments (Tab. 2, Fig. 4)—that build a well-structured case for why a single router is insufficient for unified transformers. This multi-perspective analysis is genuinely informative and provides a sound foundation for the proposed method.

- **Broad experimental scope.** The method is validated on two architecturally different unified transformers (Show-o with diffusion+AR and Emu3 with fully AR), and additionally shown to extend to pure generation models (DiT, PixArt) in the appendix. This demonstrates reasonable generality across the unified transformer design space.

- **Ablation studies isolate component contributions.** Tab. 5 systematically removes each design element, revealing that the layer switch module is the most critical component (its removal causes severe generation degradation from 0.61 to 0.50 on GenEval), while the task-aware router primarily benefits generation performance. This provides useful design guidance for practitioners.

## Weaknesses

### Fatal
None.

### Major

- **The ablation reveals a surprising inversion for understanding tasks.** In Tab. 5, the variant "w/o task-aware router" (single router at selected layers) achieves 1052.0 MME, 54.4 GQA, 80.2 POPE, and 65.5 VQAv2, which are competitive with or even close to the full UniMoD method (1093.7, 54.5, 80.3, 66.2). The task-aware router's main benefit appears concentrated on generation (0.50→0.61 GenEval). This raises a question about whether the task-aware routing contributes meaningfully to understanding performance, or whether the layer selection alone is carrying most of the method's value. The paper should discuss this more explicitly.

- **Modest efficiency gains for Show-o.** For Show-o, the method reduces TFLOPs by only ~15% (51.1→43.3). Tab. 4 shows this translates to a reduction from 1.30x/iter to 1.25-1.27x/iter (only ~3-5% wall-clock improvement) with memory reduction from 67G to 61-64G. For practical adoption, these gains are relatively marginal for a 1.3B model. The 8B results (20% FLOPs reduction) are mentioned but relegated to the appendix. Including the 8B scaling results in the main paper would significantly strengthen the efficiency argument.

- **Evaluation on Show-o full model is non-standard.** The paper reports Show-o full computation at 1056.0 MME, 56.3 GQA, 79.8 POPE, 0.62 GenEval (Tab. 3), while Table 2 shows 1032.0 MME, 52.5 GQA, 77.9 POPE, 0.63 GenEval for Show-o*. The discrepancy is not clearly explained. This inconsistency makes it harder to assess whether UniMoD's improvements are relative to a well-established baseline or a retrained version.

### Minor

- **Layer selection uses only 50 samples per task.** While pragmatic, the paper does not analyze sensitivity to this choice. A brief analysis of whether ARank-based layer selection is stable across different data samples would strengthen confidence in the method's robustness.

- **The Emu3 comparison uses different training data.** The authors acknowledge this limitation but it weakens the Emu3 results somewhat, as improvements could partly stem from dataset effects rather than the pruning method.

### Trivial
None.

## Nice-to-Haves

- An analysis of how UniMoD's pruning patterns evolve during training (e.g., do the routers converge quickly, or does the pruning strategy shift over epochs?)
- A comparison with structured pruning or quantization methods that could be complementary to UniMoD
- Discussion of whether the method could be applied retroactively to already-trained unified transformers as a fine-tuning efficiency tool

## Novel Insights

The key novel insight is that in unified transformers with mixed task types (e.g., diffusion-based generation + autoregressive understanding in Show-o), the competitive token selection experiment (Sec. 3.4) reveals that generation tokens systematically dominate when competing for capacity, which suggests that naively applying a shared router creates an implicit bias that harms understanding performance. This task-competition perspective is a genuinely useful lens for understanding multi-task transformer architectures beyond just the efficiency question.

## Suggestions

- Include the 8B model scaling results in the main paper (Sec. 5.2) rather than the appendix, as stronger efficiency gains at larger scales would significantly bolster the contribution.
- Add a brief sensitivity analysis for the number of samples used in ARank computation (currently 50) and the half-layer selection criterion.
- Clarify the discrepancy between the Show-o baselines in Tab. 2 and Tab. 3.

## Score and Decision

The paper presents a well-motivated and practical method for efficient training of unified multimodal transformers. The empirical analysis is thorough, the method is simple and well-designed, and the experiments cover multiple architectures. However, the ablation reveals that much of the benefit comes from layer selection rather than the core "task-aware" contribution, the Show-o efficiency gains are relatively modest, and some experimental details need clarification. The contribution is solid but not transformative—representing a useful engineering insight applied to an important problem, with room for stronger empirical validation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>