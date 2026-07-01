## Summary

The paper proposes UniMoD, a task-aware token pruning method for unified multimodal transformers (models handling both generation and understanding). The authors first conduct an empirical analysis of attention weights, layer importance, token redundancy, and task interactions across several unified transformers, finding that token redundancy varies significantly across tasks and layers. Based on these observations, they introduce separate Mixture-of-Depths routers for generation and understanding tasks, along with a layer switch module that uses the ARank metric to decide which layers to sparsify. Applied to Show-o and Emu3, UniMoD reduces training FLOPs by 15% and 40% respectively while maintaining or slightly improving benchmark performance on several metrics.

## Strengths

- **Addresses an important and practical problem** – Unified multimodal transformers are computationally expensive, and efficient training methods for these models are under-explored. Reducing training cost without sacrificing quality is a valuable direction.
- **Thorough empirical analysis** – The paper provides a systematic investigation of attention weight patterns, ARank-based token redundancy, layer importance, and task interactions across multiple unified transformers (Show-o, JanusFlow, Emu3, Lumina-mgpt). This analysis is informative and grounds the method's design.
- **Clean design with good ablation support** – The proposed task-aware routing (separate routers for generation and understanding) is logically motivated by the empirical findings. The ablation studies in Table 5 clearly demonstrate that both the layer switch module and the task-aware router contribute to the final performance.
- **General applicability** – The method is tested on two structurally different unified transformers (diffusion+AR and fully AR) and also extended to diffusion-only models (DiT, PixArt), demonstrating versatility.

## Weaknesses

### Major

- **Limited novelty** – The core idea is a straightforward application of Mixture-of-Depths with separate routers per task. Prior work (MoMa, γ-MoD) has already applied MoD to multimodal and unified models. The main contribution is task-specific routing, which is an incremental extension. The claim of being "the first work to propose a task-aware token pruning method for unified transformers" is overstated given MoMa applied MoD to Chameleon, a unified transformer.
- **Weak baselines** – The paper compares only against naive baselines (interleaved layer skipping, early exit). No comparison is made to other efficient training or inference methods for multimodal models (e.g., γ-MoD, token merging, adaptive computation). Without stronger baselines, it is unclear how UniMoD compares to existing alternatives.
- **Modest practical gains** – For Show-o, FLOPs reduction is only 15%, and several understanding benchmarks show slight degradation (GQA: 56.3→54.5, VQAv2: 68.3→66.2). This raises the question of whether the added complexity (multiple routers, ARank computation, auxiliary loss) is justified by the savings.
- **The layer selection and pruning ratio rely on ARank computed from the base model before MoD training** – It is unclear whether these choices remain optimal during finetuning when the model's redundancy patterns may shift. No analysis of the stability or robustness of the ARank-based selection is provided.
- **Comparison to the original Emu3 is weakened** – Because official Emu3 resources are not available, the paper compares its finetuned version to its own re-implementation using alternative datasets. This makes it difficult to assess whether the results are representative of the original model's performance.

### Minor

- The competitive token pruning experiment (Figure 4) shows generation tokens receiving higher weights, but this is almost tautological since generation tokens are directly tied to the diffusion loss while understanding tokens are autoregressive; the experiment does not reveal a non-trivial insight.
- The analysis of layer importance (skipping odd layers, Table 1) shows surprising behavior (layer 3 dropping to 0.0 while layer 1 only drops to 35.0) that is not discussed or interpreted beyond "early layers are more critical."
- The method introduces an auxiliary loss and extra routers, but the computational overhead of these components is not quantified, making the reported FLOPs reduction somewhat optimistic.

### Trivial

None.

## Nice-to-Haves

- Compare against γ-MoD or other MoD variants applied to multimodal models to better situate the contribution.
- Include an analysis of how the selected layers and pruning ratios change if ARank is recomputed during training, to verify stability.
- Evaluate on a pure text-generation task (as mentioned in the appendix) and discuss cross-task interference more thoroughly.

## Novel Insights

None beyond the paper's own contributions. The empirical results confirm that different tasks in unified transformers exhibit different token redundancy patterns, which is expected given their distinct modeling objectives (diffusion vs. autoregression). The insight that task-specific routers can improve upon a single shared router is a natural consequence of this observation rather than a surprising discovery.

## Suggestions

- Add a comparison to γ-MoD and/or other token pruning methods (e.g., selecting tokens based on attention scores) to demonstrate that task-aware routing provides non-trivial gains over existing approaches.
- Provide a sensitivity analysis of the ARank-based layer selection (e.g., what happens if suboptimal layers are chosen or if the pruning ratio is varied by 10%).
- Discuss the computational overhead of the routers themselves and clarify whether the reported FLOPs account for this.

## Score and Decision

Score: **4** – borderlines reject. The paper tackles a relevant problem and provides a solid empirical analysis, but the contribution is incremental and the experimental evaluation lacks comparison to strong baselines.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>