## Summary

This paper introduces NuSA-CL, a memory-free continual learning framework for CLIP-based vision-language models. At the start of each task, it performs SVD on the frozen weight matrices to identify a low-energy null subspace, then learns a LoRA-style update that is *persistently constrained* to lie within that subspace. After training, the update is merged into the backbone, so the parameter budget remains fixed and no external storage or auxiliary modules accumulate. Experiments on MTIL and CIFAR100 benchmarks show that NuSA-CL outperforms other storage-free methods (e.g., LoRA, MiLoRA) by clear margins and competes strongly with storage-based methods while being orders of magnitude more efficient in parameters, memory, and computation.

## Strengths

- **Genuinely memory-free and highly efficient.** NuSA-CL requires no replay buffer, no stored gradients, and no task-specific modules. It uses only 1.5M trainable parameters (vs. 149.6M for full fine‑tuning), consumes 6.6 GB peak GPU memory, and trains in 1.21 GPU‑hours. This is a fraction of the cost of storage‑based competitors, making the method practical for resource‑constrained settings.

- **Clear and well‑motivated design.** The idea of constraining updates to a dynamically identified null space (low‑energy subspace) of the current weights is novel and principled. The paper provides a theoretical bound (Lemma 1) that shows interference measured by the Frobenius inner product is controlled by the largest singular value in the null space. The ablation studies convincingly show that the persistent constraint (keeping $U_n,V_n$ frozen) is critical and that the “tail” (null) subspace yields the least forgetting.

- **Strong empirical performance across multiple settings.** On the MTIL benchmark (11 tasks), NuSA‑CL achieves Transfer/Avg/Last of 68.6/75.1/82.8, which is the best among storage‑free methods and competitive with storage‑based methods. On the challenging 50‑step CIFAR100 setting, it reaches 71.85% Last accuracy, outperforming ZSCL by more than 4 points. The few‑shot (5‑shot) results also show consistent advantages.

- **Informative analysis of learning dynamics.** Figure 2 visualizes how NuSA‑CL progressively fills the null space (increasing effective rank and null ratio) rather than overwriting principal components as LoRA or full fine‑tuning do. This provides direct evidence that the method accumulates new knowledge in previously underutilized spectral directions.

## Weaknesses

### Fatal

None.

### Major

- **Theoretical guarantee is only in parameter space, not function space.** The interference bound (Lemma 1) is for the Frobenius inner product of weight matrices. While the authors acknowledge this limitation and present empirical evidence, the paper would be stronger with a function‑level bound (e.g., under Lipschitz smoothness of the network). Without such a guarantee, it remains possible that updates confined to the null space in parameter space could still significantly change the model’s predictions on past tasks.

### Minor

- **SVD overhead for very large models is not fully evaluated.** The paper claims negligible SVD overhead and reports <1 min for ViT‑B/16, but attention projections are only 768×768. For larger backbones (e.g., ViT‑L, ViT‑H) the cost of full SVD on larger matrices could become non‑negligible, especially when performed for every layer before each task. The paper acknowledges this as future work but does not provide estimates or mitigations beyond suggesting truncated SVD.

- **Gap to storage‑based state‑of‑the‑art in Last accuracy.** On MTIL, the best storage‑free method (NuSA‑CL) achieves 82.8% Last, while MoE‑Adapters and DIKI reach 85.0% and 85.1%. Though the paper correctly emphasises the efficiency advantage, a discussion of the remaining gap (≈2 points) and whether it can be closed with a slightly larger rank is missing.

- **Evaluation is limited to one backbone (CLIP ViT‑B/16).** It is unclear how well the method transfers to other VLM architectures (e.g., SigLIP, ALIGN) or to larger variants. While the experiments are thorough for the chosen setting, the general claim about applicability to “vision‑language foundation models” would be strengthened by at least one additional backbone.

### Trivial

None.

## Nice-to-Haves

- Provide a function‑level forgetting bound under standard Lipschitz assumptions (e.g., using Lemma 1 together with the smoothness of the encoder).
- Evaluate on a larger CLIP variant (e.g., ViT‑L) to verify scalability of the SVD step and the performance retention.
- Include a comparison with more recent storage‑free PEFT methods such as O‑LoRA or FourierFT for a more complete picture.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that *persistently* confining weight updates to the low‑energy (null) subspace of the current weights, rather than using it only for initialization, turns the model’s own spectral structure into a lifelong learning mechanism. The analysis of effective rank evolution (Figure 2) reveals that conventional fine‑tuning methods (LoRA, full‑FT) leave the null space largely unused, while NuSA‑CL actively exploits it, converting previously underexploited directions into a source of plasticity without overwriting dominant knowledge. This suggests a new principle for continual learning in foundation models: exploit the inherent “slack” in learned representations to accommodate new tasks, rather than expanding capacity or externalising memory.

## Suggestions

1. Provide a bound on the change in the network’s output (e.g., $\|f_{W_t}(x)-f_{W_{t-1}}(x)\|$) under the null‑space constraint, building on Lemma 1 and Lipschitz continuity of the encoder layers. This would strengthen the theoretical motivation.
2. Add a simple experiment that varies the SVD threshold $\rho$ over a wider range (e.g., 0.7 to 0.9999) and reports the resulting rank distribution across layers, to give practitioners a clearer sense of how to set this hyperparameter.
3. Discuss the possibility of “null space exhaustion” more quantitatively by measuring the remaining null directions after larger sequences (e.g., 100 tasks) on a synthetic or realistic long‑horizon scenario.

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>