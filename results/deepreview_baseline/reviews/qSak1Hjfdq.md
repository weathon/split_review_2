## Summary

This paper formalizes the all-day multi-scenes lifelong vision-and-language navigation (AML-VLN) problem, where agents must adapt across diverse scenes and illumination conditions (normal, low-light, overexposed, scattering) without catastrophic forgetting. The authors propose Tucker Adaptation (TuKA), a parameter-efficient method that represents multi-hierarchical navigation knowledge as a high-order tensor and uses Tucker decomposition to decouple shared subspaces from scene-specific and environment-specific experts. They further develop the AllDayWalker agent with a Decoupled Knowledge Incremental Learning strategy and extend the Habitat simulator with imaging models to create a new benchmark. Experiments demonstrate consistent and sizable improvements over a range of continual learning and test-time adaptation baselines.

## Strengths

- **Novel problem formalization and benchmark:** The AML-VLN setting is practically motivated and fills an important gap in VLN research by considering both scene variation and environmental degradation. The extension of Habitat with physically motivated imaging models (scattering, low-light, overexposure) provides a valuable testbed for lifelong learning under distribution shift.
- **Methodological innovation:** TuKA is a principled approach that lifts LoRA-style adaptation into higher-order tensor space via Tucker decomposition. This naturally decouples multi-hierarchical knowledge (shared navigation skills, scene experts, environment experts) that existing 2D matrix-based adapters cannot capture. The fourth-order tensor design is well motivated and ablation confirms its advantage over a third-order alternative.
- **Strong empirical results:** AllDayWalker consistently outperforms a comprehensive set of baselines (including modern MoE-LoRA variants, EWC, and test-time adaptation methods) across SR, SPL, OSR, and corresponding forgetting metrics. The gains are large—e.g., 65% avg. SR vs. 44% for BranchLoRA—and hold under generalization to unseen scenarios and when scaling from 24 to 30 tasks.
- **Thorough ablation and analysis:** The paper systematically investigates key design choices: shared core tensor/encoder/decoder, order of the tensor, orthogonal constraints, and scalability to more tasks. These experiments convincingly validate the architecture and learning strategy.

## Weaknesses

### Fatal
None.

### Major
- **Hyperparameter sensitivity not fully explored:** The method introduces several balancing hyperparameters (λ₁, λ₂, λ₃, ω, and ranks r₁–r₄) that likely interact in complex ways. While some ablation is present (shared components, tensor order), a systematic sensitivity analysis over the loss weights is missing. The parameter settings (λ₁=0.2, λ₂=0.2, λ₃=0.1) may not generalize to other task sequences or backbone choices without retuning.
- **Limited real-world validation:** Although the paper claims “additional real-world deployments” as a contribution, only two real-world scenes appear in the benchmark (as part of the 24-task sequence), and generalization results include two additional real-world scenes. Detailed results, deployment conditions, and failure cases for real-world experiments are not reported. The claim of robust real-world capability is not strongly supported.

### Minor
- **CLIP-based expert retrieval during inference:** The two-step matching relies on storing vision features per scene/environment and cosine similarity. No analysis is provided on retrieval accuracy or the impact of retrieval errors on final navigation performance. A failure case or confusion matrix would strengthen this component.
- **Fisher Information computation cost:** EWC-based consolidation uses per-parameter Fisher information, which requires second-order information and adds non-trivial overhead during continual learning. The paper does not discuss computational cost or training time compared to simpler baselines.

### Trivial
- In Table 1, the row for SD-LoRA appears to have missing values in the last four columns (T21–T24), which may be a formatting artifact from parsing but could affect reproducibility reading.

## Nice-to-Haves
- A deeper analysis of expert specialization: how different do the learned scene/environment expert vectors become? Visualization via t-SNE or similarity matrices could illustrate knowledge decoupling.
- Evaluation of the “step-by-step fine-tune” upper bound (multi-task joint training on all tasks) as a performance ceiling, rather than only the multi-task per-task performance used in the forgetting metric.
- Comparison to replay-based continual learning methods (e.g., episodic memory) which are popular in robotics settings, to contextualize the performance of regularization-based TuKA.

## Novel Insights
Beyond the paper’s own contributions, a key insight is that high-order tensor decomposition can serve as a natural inductive bias for decoupling multiple independent axes of variation in continual learning problems. The Tucker decomposition factors the tensor along dimensions corresponding to different knowledge hierarchies (scene, environment), enabling shared and specific parameters to be learned simultaneously. This provides a principled alternative to manually designed MoE gating or per-task parameter isolation, and may inspire tensor-based adaptation methods in other multimodal lifelong learning domains where the task structure has multiple latent factors.

## Suggestions
- Provide a sensitivity analysis over λ₁, λ₂, λ₃ (e.g., grid over [0.05, 0.5]) to show how performance and forgetting trade off.
- Include a small-scale real-world deployment study with more scenes (e.g., 3–5) and report quantitative metrics with error bars.
- Analyze retrieval accuracy for the inference-time expert selection and discuss potential failure modes (e.g., confusion between normal and low-light features in a similar scene).
- Compare trainable parameter count and training/inference wall-clock time against the strongest baselines to contextualize efficiency.

## Score and Decision
The paper presents a well-motivated problem, a novel tensor-based adaptation method, a new benchmark, and strong experimental results with thorough ablations. The contributions are significant and clearly demonstrated. The identified weaknesses are manageable and do not undermine the core claims.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>