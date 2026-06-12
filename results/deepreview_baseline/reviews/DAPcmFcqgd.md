## Summary

The paper proposes MoEP (Modular Expert Paths), a decoder-only architecture that combines layer-level top‑k routing across parallel Transformer blocks with mixture‑of‑experts (MoE) feed‑forward projections. The key design goal is to introduce sparsity without increasing the total number of parameters relative to a dense baseline—achieved by operating the parallel layers at a reduced hidden dimension. The model is evaluated on the BabyLM strict‑small track and compared against GPT‑2 and GPT‑BERT baselines. The authors claim that MoEP outperforms all BabyLM baselines, release code and checkpoints, and provide an analysis of training dynamics indicating faster early learning.

## Strengths

- **Idea of fixed‑parameter sparsity via parallel layers.** Combining layer‑level routing with smaller‑dimension parallel blocks is a relatively novel way to introduce sparsity without the parameter overhead typical of standard MoE. This design direction could be useful for resource‑constrained settings.
- **Use of a standardized evaluation pipeline.** Following the BabyLM strict‑small track ensures a fair and reproducible comparison against the provided baselines, and the release of code and model weights supports reproducibility.
- **Training dynamics analysis.** The paper shows that MoEP reaches near‑peak evaluation scores earlier in training (at 30M words) than GPT‑2, suggesting better initial sample efficiency from the modular routing.

## Weaknesses

### Fatal

- **False or misleading claim of outperforming all baselines.** The abstract and introduction state that “MoEP was able to outperform all BabyLM strict‑small baseline models, including the GPT‑2 and GPT‑BERT models.” However, Table 1 shows that **GPT‑BERT (causal) achieves a macro average of 54.10 (excluding AoA), while MoEP achieves 49.00**—a clear underperformance. The claim can only be sustained by including the AoA task, yet the author’s own text acknowledges that AoA is handled separately and the no‑AoA average is the primary comparison point (e.g., “Even when excluding AoA … MoEP still outperformed the BabyLM GPT‑2 baseline”). The blanket statement is not supported by the data and undermines the paper’s core contribution.

### Major

- **No comparison against a standard MoE baseline.** The paper never compares MoEP to a conventional MoE architecture that activates the same number of parameters per token. Without this, it is unclear whether any gains come from the specific modular design or simply from having more representational capacity (the parallel blocks, even at reduced dimension, may still encode more unique patterns than a single dense layer). This is a critical missing control.
- **No ablation study.** The architecture contains three main components (MoE shrink/grow blocks, parallel layers with top‑k routing, and auxiliary balancing loss). No experiment isolates their individual contributions—e.g., removing the MoE blocks, using dense parallel layers without routing, or varying the number of parallel blocks. The paper cannot attribute performance to any specific design choice.
- **Single‑small‑scale evaluation.** Experiments are limited to BabyLM (≈10M words). The paper itself acknowledges uncertainty about scaling, but provides no larger‑scale experiment or even a preliminary analysis on a medium‑sized corpus. For an architecture that targets efficiency, it is essential to show behavior under more realistic data sizes.
- **Reliance on AoA for overall ranking.** The claim of “outperforming all baselines” depends on the macro average that includes AoA, a single task with large variance across models (MoEP 53.70 vs. GPT‑2 baseline 11.7 vs. GPT‑BERT causal –3.9). Using a single, highly variable task to tip the overall score is questionable; the more standard no‑AoA average gives a different picture.

### Minor

- The architecture description in Section 3.1 is somewhat ambiguous: “2 / 10” layers in Table 2 means 2 full‑size layers and 10 parallel layers, but this mapping is not explained clearly in the main text.
- MoEP‑SwiGLU increases total parameters to 38M vs. 28M for MoEP/GPT‑2, so the “fixed parameter” property does not hold for all variants.

### Trivial

- None.

## Nice‑to‑Haves

- A direct comparison with a standard MoE transformer of equivalent total parameters and equivalent activated parameters (matching the dense baseline’s FLOPs).
- Ablation experiments that remove the MoE shrink/grow blocks, disable routing among parallel blocks, or vary the number of parallel blocks.
- A scaling study on a larger dataset (e.g., C4 slice of a few hundred million tokens) to see if the relative advantages persist.

## Novel Insights

Beyond the paper’s own contributions, the observation that layer‑level routing with reduced‑dimension parallel blocks can match or exceed a dense baseline of the same parameter count is noteworthy, but it is not deeply explained *why* this happens. The paper reports faster early learning but offers no theoretical or empirical analysis of why sparser pathways at layer level are more sample‑efficient. The insight remains at the “it works” level.

## Suggestions

1. **Correct the overclaim.** Rewrite the abstract and conclusion to accurately report that MoEP outperforms GPT‑2 and is competitive with GPT‑BERT when AoA is included, but does not surpass GPT‑BERT under the standard no‑AoA metric.
2. **Add a standard MoE baseline.** Train a transformer where the FFN is replaced by an MoE of the same total parameter count (e.g., more experts, smaller hidden dimension) under the same compute budget. This is essential to distinguish the effect of layer‑level routing from MoE‑style sparsity alone.
3. **Include ablation experiments.** Systematically remove components: (a) dense parallel layers without routing, (b) only one MoE block (shrink + grow removed), (c) varying \(k\) in top‑k routing, (d) no auxiliary loss. This would substantiate the claimed benefits.
4. **Evaluate on a larger dataset.** At a minimum, train on the full BabyLM (10M words) but also on a 100M‑word corpus (e.g., a subset of C4) to test whether the parallel‑layer sparsity scales.

## Score and Decision

The paper proposes a creative combination of parallel layers and MoE routing with a constant parameter budget, which is a potentially valuable idea. However, the central claim of outperforming all BabyLM baselines is contradicted by the paper’s own data (MoEP has a lower macro average than GPT‑BERT causal when excluding AoA). This fatal flaw, compounded by the lack of ablation studies and the absence of a standard MoE baseline, makes the current evidence insufficient to support the paper’s main conclusions. The contribution is not convincingly validated.

MY FINAL SCORE: 3.0</score>  
MY FINAL DECISION: Reject</decision>