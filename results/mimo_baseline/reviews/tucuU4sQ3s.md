## Summary

This paper introduces NuSA-CL, a memory-free continual learning framework for vision-language models that constrains task-specific weight updates to lie within the approximate null space of the model's current parameters, identified via SVD. The method uses a persistent constraint where only a small intermediate matrix is trained while the null-space basis vectors remain frozen, and updates are merged back into the backbone after each task, maintaining a fixed parameter budget. Experiments on MTIL and CIFAR100 benchmarks demonstrate that NuSA-CL outperforms other storage-free methods and achieves competitive performance with storage-based approaches at a fraction of the cost.

## Strengths

- **Clean and principled method design.** The persistent null-space constraint (Eq. 3) is a well-motivated architectural choice that provides a mathematical guarantee that updates are orthogonal to the principal subspace. The distinction from prior work like MiLoRA, which only uses the null space for initialization, is clearly articulated and validated through ablations (Table 4a), where unfreezing the basis vectors causes significant performance degradation.

- **Comprehensive and convincing experimental evaluation.** The paper evaluates across three distinct settings: full-shot MTIL (11 tasks), 5-shot MTIL, and class-incremental CIFAR100 with 10/20/50-step splits. NuSA-CL achieves the best performance among storage-free methods on MTIL (Transfer: 68.6%, Avg.: 75.1%, Last: 82.8%) while using 40× fewer parameters than MoE-Adapters and requiring zero additional storage. On the most challenging 50-step CIFAR100, it surpasses ZSCL by 4.4% in Last accuracy (71.85% vs. 67.36%).

- **Thorough analysis of null-space dynamics.** Figure 2 provides insightful visualization showing that NuSA-CL progressively increases effective rank across tasks, demonstrating knowledge accumulation rather than overwriting. The ablation on subspace choice (Figure 3a) convincingly shows that the Tail (null-like) subspace yields consistently lower forgetting than Top or Random alternatives across all tested ranks.

- **Practical efficiency.** The method requires only 1.5M trainable parameters, zero additional storage, and 1.21 GPU-hours on MTIL—matching LoRA's computational cost while significantly outperforming it. The SVD initialization overhead is negligible (<1 minute per task), as validated in Table 4b.

## Weaknesses

### Fatal
None.

### Major

- **Limited backbone evaluation.** All experiments use only CLIP ViT-B/16. The paper does not validate on larger CLIP variants (ViT-L/14, ViT-H/14) or other VLM architectures. Given that the paper claims to provide "a practical and scalable solution for continually evolving zero-shot VLMs," demonstrating scalability to larger models is important. The authors briefly discuss this in Section 6.3 but provide no concrete experimental evidence.

- **Theoretical analysis is limited to parameter space.** Lemma 1 and Theorem 2 bound interference via the Frobenius inner product ⟨W, ΔW⟩_F, which measures alignment in parameter space rather than function-level forgetting. The authors acknowledge this ("should be viewed as a local stability condition rather than a full function-level guarantee"), but the gap between parameter-space orthogonality and actual prediction preservation on past tasks is not quantified. The bounds are also relatively straightforward consequences of the SVD structure.

### Minor

- **Mixed results on CIFAR100 Avg. metric.** While NuSA-CL dominates on Last accuracy, on the 10-step CIFAR100 split, ZSCL achieves 82.15% Avg. vs. NuSA-CL's 80.25%. This suggests that in shorter sequences, the storage-based approach may still have advantages in average performance that the paper could discuss more explicitly.

- **Energy threshold ρ is a heuristic.** The choice of ρ determines the boundary between principal and null subspaces. While Table 4b shows robustness across a range (0.80–0.99), the extreme case ρ=0.999 shows significant degradation (Avg. 72.89% vs. 75.08%), indicating sensitivity at the boundaries. A more principled or adaptive selection strategy could strengthen the method.

- **Only attention projection matrices are adapted.** The method applies SVD and updates only to attention projection matrices (W_q, W_k, W_v, W_o). The paper does not justify why MLP layers or other components are excluded, nor does it analyze the impact of this choice.

### Trivial
None.

## Nice-to-Haves

- Experiments on larger CLIP backbones (ViT-L/14) to validate scalability claims
- Analysis of sensitivity to task ordering and semantic relatedness between tasks
- Comparison with more recent continual learning methods for VLMs (e.g., from 2024-2025)
- A function-level analysis connecting parameter-space orthogonality to actual forgetting on past task predictions

## Novel Insights

The paper's key novel insight is that the null space of a VLM's weight matrices is not a finite, depletable resource but rather a low-energy spectral region that can be progressively utilized across tasks without inducing spectral collapse. The empirical evidence in Figure 2 and Appendix Tables 11-12, showing stable null-space availability even after 50 highly correlated CIFAR-100 steps, provides meaningful evidence for this claim. This distinguishes NuSA-CL from methods that treat the parameter space as a fixed-capacity container and suggests that spectral-guided adaptation has longer viability than intuition might suggest.

## Suggestions

- Add experiments on at least one larger CLIP variant (e.g., ViT-L/14) to substantiate scalability claims, even if using truncated SVD as mentioned in Section 6.3.
- Provide a brief function-level analysis: measure prediction changes on held-out past task data as a function of the parameter-space interference bound, to bridge the gap between the theoretical analysis and empirical results.
- Include an ablation on which layers are adapted (attention-only vs. attention+MLP vs. all) to justify the current design choice.

## Score and Decision

The paper presents a clean, well-motivated method with strong empirical results and insightful analysis. The persistent null-space constraint is a genuine contribution over prior work, and the memory-free property addresses a real practical need. The main limitations are the single-backbone evaluation and the parameter-space-only theoretical analysis, but these do not invalidate the contribution. The experiments are comprehensive within the evaluated setting, and the ablation studies effectively validate the design choices.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>