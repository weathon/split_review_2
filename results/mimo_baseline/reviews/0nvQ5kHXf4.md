## Summary

The paper proposes Weight-Activation Subspace Iteration (WASI), a method for efficient resource-constrained training of transformer models that jointly compresses both weight matrices and activation maps via subspace iteration. The key insight is that during fine-tuning, the essential parameter subspace remains stable, allowing SVD-computed subspaces to be reused across iterations rather than recomputed, while simultaneously applying Tucker decomposition to activation maps. Experiments on ViT, SwinT, and TinyLlama demonstrate memory reductions up to 62× and real-world 1.4× speedups on a Raspberry Pi 5.

## Strengths

- **Genuine technical contribution extending subspace-based on-device learning to transformers.** Prior work (ASI, AMC, Gradient Filter) was confined to CNN architectures. WASI bridges this gap by combining weight subspace iteration with activation subspace iteration, enabling transformer fine-tuning on edge devices. The extension to 3D activation tensors (Appendix A.1) and the dynamic programming rank selection are non-trivial engineering contributions.

- **Strong empirical validation of the stability hypothesis.** Figures 3a and 3b provide clear evidence that (a) layer ranks K_i remain remarkably stable across training iterations under a fixed ε, and (b) reusing the SVD subspace via WSI requires 1.36× fewer FLOPs than full recomputation while achieving 35% higher accuracy at matched compute. This validates the paper's central assumption.

- **Extensive efficiency gains across diverse settings.** WASI achieves up to 62× memory savings on ViT/SwinT and up to 953× activation memory reduction on TinyLlama, without accuracy loss. The Raspberry Pi 5 deployment (Section 4.4) provides concrete, real-world evidence that the method translates to actual hardware speedups (~1.4× faster training/inference), which is directly relevant to the on-device learning application domain.

- **Clear and well-structured presentation.** The method is motivated step-by-step from bottleneck identification through activation-only compression to the full joint framework, with a helpful architectural diagram (Figure 1) and complexity analysis (Figure 2).

## Weaknesses

### Fatal
None.

### Major

- **Narrow and incomplete baseline comparison.** The primary baselines are ASI, SVD-LLM, and vanilla training. Several important alternative approaches for efficient training on edge devices are absent: gradient checkpointing (which directly addresses the activation storage bottleneck), mixed-precision training (standard for memory reduction), and quantization-aware methods. Without these comparisons, it is difficult to assess WASI's true advantage. The paper acknowledges some related methods are out of scope, but gradient checkpointing in particular is a direct competitor for the activation memory reduction claim.

- **TinyLlama experiment appears preliminary and non-standard.** Only the last 5 layers are fine-tuned, ε is set to 0.1 (extremely aggressive), and there is no comparison against SVD-LLM or other baselines for this model—only vanilla training. The extraordinary compression ratios (953× activation memory) likely reflect this aggressive ε and limited fine-tuning rather than broad applicability. This experiment reads as a proof-of-concept rather than rigorous evaluation, yet the introduction positions WASI as applicable to transformers generally.

- **Small-scale evaluation limits generalizability claims.** All vision experiments use relatively compact models (ViT-Base, SwinT) on standard benchmarks. The paper does not provide any scaling analysis showing how WASI performs as model size increases (e.g., ViT-Large, ViT-Huge), which would be essential for the transformer-focused claim. The TinyLlama experiment partially addresses this but is not conclusive for the reasons above.

### Minor

- **The "62× memory reduction" headline claim requires qualification.** This appears to be the training memory compression at the most aggressive ε setting on SwinT with a specific dataset. Across experiments, the compression ratios vary significantly by ε, model, and dataset. More prominent disclosure of the conditions under which extreme compressions are achievable (and when they come with accuracy loss) would improve transparency.

- **Inference claims are less distinctive.** For inference, ASI behaves similarly to vanilla training since activation compression is primarily a training-time benefit, while both WASI and SVD-LLM achieve similar inference FLOPs reductions. The paper does not clearly delineate which of its contributions are training-specific versus deployment-specific.

### Trivial
None.

## Nice-to-Haves

- A comparison against gradient checkpointing and mixed-precision training would substantially strengthen the practical relevance claims.
- Experiments on larger ViT variants (Large, Huge) or more challenging tasks would help establish the method's scalability.
- An ablation isolating the individual contributions of WSI versus ASI versus their combination would clarify the value of the joint framework.
- Discussion of the sensitivity of the stability assumption to learning rate and fine-tuning duration.

## Novel Insights

The paper's most interesting finding is the counterintuitive result that WSI (reusing the SVD subspace) outperforms full SVD recomputation at matched FLOPs by 35% in accuracy. This suggests that the incremental subspace updates in WSI act as a form of implicit regularization or momentum, rather than simply being a computational shortcut. This finding extends beyond the paper's own stated contributions and warrants deeper investigation.

## Suggestions

- Add gradient checkpointing as a baseline, as it is the most direct competitor for the activation memory reduction claim.
- For the TinyLlama experiment, use ε comparable to the vision experiments and include SVD-LLM comparisons for fairness.
- Provide a supplementary table explicitly listing, for each model and ε setting, the actual ranks K_i achieved, to help practitioners understand the compression levels.

## Score and Decision

MY FINAL SCORE: 5.5
MY FINAL DECISION: Accept