## Summary

This paper introduces UniMoD, a task-aware token pruning method for unified multimodal transformers that handle both generation and understanding tasks. Through empirical analysis of attention weight patterns, layer importance, token redundancy (using the ARank metric), and task interactions across models like Show-o and Emu3, the authors observe that token redundancy varies significantly across tasks and layers. Based on these observations, they propose using separate task-specific routers for pruning tokens differently per task, along with an ARank-based layer selection module. Their method achieves 15-40% FLOPs reductions while maintaining or slightly improving performance on several benchmarks.

## Strengths

- **Well-motivated problem and thorough empirical analysis**: Training unified multimodal transformers is computationally expensive, and efficient training methods for these models are underexplored. The paper provides a multi-perspective analysis (attention weights, ARank across layers/tasks, task interaction experiments) across four different models (Show-o, JanusFlow, Emu3, Lumina-mgpt), which gives solid grounding for the method design.

- **Clear logical flow from observations to method**: The paper draws five explicit observations from the empirical analysis, and the UniMoD design follows directly from these observations. The task-specific routers target the observed task-dependent redundancy patterns, and the layer switch module addresses the observed layer-dependent redundancy.

- **Good coverage of model types and tasks**: Evaluating on Show-o (diffusion+autoregressive) and Emu3 (fully autoregressive) demonstrates applicability across different unified architectures. The experiments cover both understanding benchmarks (MME, GQA, POPE, MMMU, VQAv2) and generation benchmarks (GenEval, DSG, CLIP score).

- **Practical efficiency gains**: FLOPs reductions of 15% (Show-o) and 40% (Emu3) with maintained or improved performance are practically meaningful. The training cost analysis in Table 4 shows actual speed improvements and memory savings.

## Weaknesses

### Fatal
None.

### Major

**1. Limited novelty — task-specific routing is an incremental extension of existing techniques**

The core idea of using separate routers per task is a fairly direct extension of Mixture of Depths (MoD). The ARank-based layer selection was already proposed in γ-MoD (Luo et al., 2024) for multimodal LLMs, and MoD was already applied to a unified transformer (Chameleon) in MoMa (Lin et al., 2024b). The paper acknowledges MoMa but characterizes it as "only a simplistic combination, without a design tailored for unified transformers." However, the paper does not provide a direct comparison against MoMa-style MoD applied to the same models, and the actual proposed improvement (separate per-task routers) is conceptually straightforward once one recognizes task-dependent redundancy. The method contribution over prior work is incremental rather than foundational.

**2. Ablation study does not strongly support the necessity of the claimed key components**

In Table 5, the "w/o task-aware router" variant (single shared router with layer selection) achieves nearly identical understanding results to UniMoD: MME 1052.0 vs. 1093.7, GQA 54.4 vs. 54.5, POPE 80.2 vs. 80.3, MMMU 25.6 vs. 25.7, VQAv2 65.5 vs. 66.2. The main benefit of task-specific routers appears on the generation task (GenEval 0.50 vs. 0.61). This substantially weakens the paper's central claim that task-aware routing is critical for both tasks. Moreover, "Basic MoD" uses 40.8 TFLOPs while UniMoD uses 43.3 TFLOPs — the comparison is not at matched compute budgets. It is plausible that Basic MoD with the same FLOPs budget would perform better.

**3. Method hyperparameters are tuned based on analysis that may not generalize**

The layer selection and pruning ratio estimation are performed using ARank computed on 50 samples per task from the Show-o model itself, and then the method is evaluated on the same model. This creates a potential overfitting concern — the layer selection and pruning ratios are essentially tailored to observations from that specific model instance. It is unclear whether the ARank-based selection would generalize to different training runs, different random seeds, or different data distributions without re-running the analysis.

**4. Comparison to the most directly related prior work (MoMa) is insufficient**

MoMa (Lin et al., 2024b) applies MoD to Chameleon, which is also a unified transformer. The paper acknowledges MoMa but dismisses it without a direct experimental comparison. Given that MoMa is the most closely related work applying MoD to unified transformers, a comparison (at least on understanding tasks, where MoMa has reported results) would help position the contribution. Without this, it is difficult to assess whether the task-specific router design provides benefits beyond what a carefully tuned MoMa-style MoD would achieve.

### Minor

**1. Training data differences for Emu3 limit the strength of results**

The paper states "Our full Emu3 results differ from the original paper because we use alternative training datasets." This means the baseline numbers (Full Computation Emu3 in Table 3) are from a model fine-tuned with different data, not the original Emu3. While the comparison between with/without UniMoD on the same fine-tuning setup is valid, the absolute performance numbers cannot be compared to the original model, making the "maintains or improves performance" claim weaker than it appears.

**2. Competitive token pruning experiment (Section 3.4) uses a specific artificial setup**

Setting a hard router capacity of 0.5 and forcing competition between tasks creates a specific experimental condition. The observation that T2I tokens dominate may partly reflect this hard capacity constraint rather than inherent task importance. The authors should discuss whether this observation would hold under different capacity settings or alternative competitive mechanisms.

**3. Training details need clarification**

The paper mentions the model is "finetuned" on 8 H100 GPUs, but it is unclear whether UniMoD is applied during continued pre-training, fine-tuning from a pre-trained checkpoint, or training from scratch. These different settings would affect the practical value of the method. Additionally, a batch size of 10 is quite small and may affect the stability of the router training.

### Trivial

- The paper claims "first work to propose a task-aware token pruning method for unified transformers" — given MoMa's prior application of MoD to Chameleon, this claim should be more carefully scoped.

## Nice-to-Haves

- A direct comparison against MoMa-style MoD applied to Show-o or Emu3 would greatly strengthen the paper.
- Results from training from scratch (not just fine-tuning) would demonstrate broader applicability.
- An analysis of how many samples are needed for reliable ARank-based layer selection would address generalizability concerns.
- More discussion on why the batch size of 10 was chosen and whether results are stable across different batch sizes.

## Novel Insights

The paper's primary insight is that token redundancy patterns are task-dependent in unified multimodal transformers, especially when different modeling approaches (diffusion vs. autoregressive) are used for different tasks. This is validated through ARank analysis across multiple models. However, the insight itself — that different tasks benefit from different pruning strategies — is intuitive once articulated, and the paper's main methodological contribution (separate per-task routers) is a natural and fairly straightforward implementation of this insight. The empirical characterization of redundancy patterns across layers and tasks is the most valuable contribution, more so than the specific method.

## Suggestions

1. Strengthen the ablation by comparing all variants at matched FLOPs budgets (e.g., increase capacity of Basic MoD to match UniMoD's FLOPs).
2. Provide evidence that the ARank-based layer selection is robust across random seeds or training runs, rather than tuned on a single model instance.
3. Add a comparison against a variant that uses task-specific pruning ratios with a shared router, to isolate the benefit of having separate routers versus just task-specific capacities.
4. Clarify the training setting (fine-tuning vs. from-scratch) and discuss implications for practical usage.

## Score and Decision

**Score**: 5

**Decision**: Borderline Reject

**Reasoning**: The paper presents a well-motivated and reasonably executed empirical analysis of token redundancy in unified multimodal transformers, and the proposed method achieves practical efficiency gains. However, the novelty is limited — task-specific routing is an incremental extension of prior MoD work, and the ablations do not strongly support the necessity of the claimed key design components (particularly task-aware routers for understanding tasks). The paper would benefit from stronger experimental comparisons against the most directly related prior work (MoMa) and from demonstrating that the method's design choices generalize beyond the specific analysis setup. The contribution is adequate but falls short of the bar for top-tier acceptance at ICLR.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>