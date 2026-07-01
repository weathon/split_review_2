## Summary

The paper proposes NuSA-CL, a memory-free continual learning method for vision-language models that constrains low-rank updates to the approximate null space of the current weight matrices (identified via SVD). By persistently freezing the null-space basis vectors and learning only a small intermediate matrix, the method preserves zero-shot capabilities while incrementally adapting to new tasks, all within a fixed parameter budget and without replay buffers or distillation. Experiments on the MTIL and CIFAR100 benchmarks show that NuSA-CL outperforms other storage-free PEFT methods and competes with storage-based approaches at a fraction of the computational cost.

## Strengths

- **Practical and efficient design**: NuSA-CL requires no replay buffer, no knowledge distillation, and no growing parameter set. The update-and-merge cycle keeps the model’s total parameter budget fixed, making it suitable for resource-constrained deployment. The memory/FLOPs savings versus storage-based methods (40× fewer parameters, 3× faster training) are compelling.
- **Clear and novel core idea**: The persistent constraint that locks updates into the null space is a principled departure from prior work (e.g., MiLoRA) that only uses the low-energy subspace for initialization. The ablation (Table 4a) confirms that unfreezing the basis vectors significantly degrades performance, validating the necessity of the persistent constraint.
- **Strong empirical results**: NuSA-CL achieves the best performance among storage-free methods on the MTIL benchmark and establishes a new state-of-the-art on the CIFAR100 50-step split (71.85% Last accuracy, beating ZSCL by 4.4%). The analysis of null-space dynamics (Figure 2) provides direct evidence that the method accumulates knowledge rather than overwriting it.
- **Rigorous ablation and analysis**: The subspace selection study (Figure 3a) convincingly shows that the tail (null-like) subspace minimizes forgetting across all tested ranks. The ablation of energy cutoff ρ (Table 4b) demonstrates robustness to hyperparameter choices.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical support is limited to a parameter-space inner-product bound.** Lemma 1 bounds interference in the Frobenius inner product of the weight matrices, but forgetting is a function-level phenomenon. The bound does not directly control how predictions on past tasks change, and the paper acknowledges this limitation. While the empirical results are strong, the theoretical motivation is weaker than it initially appears.
- **Long-sequence evaluation is still modest.** The CIFAR100 50-step split uses only 100 classes; after 50 tasks the model has seen each class twice on average. The claim of “lifelong learning” scalability would be strengthened by experiments on longer sequences (e.g., hundreds of tasks) or on streaming settings with non-repeating classes. The guarantee that the null space does not saturate (Appendix Table 12) is based on CIFAR100; it remains unclear whether the null space would survive thousands of highly diverse tasks.
- **Computational cost of SVD per task is under-scrutinized.** The paper reports that SVD initialization takes <1 min, but this is for ViT-B/16 where attention projections are at most 768×768. For larger backbones (e.g., ViT-L with 1024-dim projections, or models with many more layers), the cumulative SVD overhead could become non-negligible. The suggestion of truncated SVD is not evaluated, leaving a practical concern for scaling.

### Minor
- The comparison against storage-based baselines could be more nuanced. InLoRA uses only 9 MB of gradient projection memory; DIKI uses 159 MB of task statistics. While NuSA-CL is truly storage-free, the practical memory savings over these methods is relatively small compared to the factor of 40× in trainable parameters. The paper’s emphasis on “40× fewer parameters” is somewhat misleading because the baseline methods store additional modules (routers, task stats) that are not part of the backbone parameter count.
- The method is evaluated only on attention projection matrices. The paper does not discuss whether the null-space strategy could benefit other components (e.g., MLP layers, embedding layers). This limits the generality of the claim that NuSA-CL can be applied to arbitrary weight matrices.
- The definition of “effective rank” uses a 95% energy cutoff averaged across layers. Fractional values are reported (e.g., 447.42), which is a mathematical convenience but could benefit from clearer justification.

### Trivial
None.

## Nice-to-Haves

- Extending the evaluation to longer task sequences (e.g., 200 tasks) would further validate the claim of lifelong learning.
- Analyzing the sensitivity to task order (e.g., random permutations) would strengthen the paper’s conclusions about robustness.
- Demonstrating NuSA-CL on a larger backbone (e.g., ViT-L/14) with timing and memory breakdowns would address the potential SVD bottleneck concern.

## Novel Insights

Beyond the method itself, the most interesting insight is the demonstration that effective rank increases over tasks under NuSA-CL while remaining static under standard LoRA or full fine-tuning (Figure 2). This provides direct evidence that the model actively expands into low-energy subspaces rather than overwriting principal components, offering a spectral perspective on how catastrophic forgetting is mitigated. The observation that the null space does not saturate even after 10 diverse tasks (and 50 CIFAR100 tasks) is a useful empirical finding for future work on spectral approaches to continual learning.

## Suggestions

- Strengthen the theoretical section by providing a function-level forgetting bound under Lipschitz smoothness assumptions, or at least clearly delineate why the parameter-space bound is a useful proxy (e.g., connecting to model outputs via the NTK or similar).
- Add a small experiment on a larger backbone (e.g., ViT-L) to demonstrate that the SVD initialization overhead remains negligible and to confirm that the performance trends hold.
- Re-frame the “40× fewer parameters” claim to separate backbone parameters from auxiliary storage, so readers can directly compare the storage-free nature of NuSA-CL versus the small-storage nature of methods like InLoRA and DIKI.

## Score and Decision

**Score**: 8  
**Decision**: Accept  

This paper presents a clean, well-motivated, and empirically validated method for continual learning in vision-language models. The null-space persistent constraint is a novel contribution that yields strong results without the scalability pitfalls of storage-based or expansion-based approaches. The weaknesses (limited theoretical guarantee, modest long-sequence scope) are acknowledged and do not invalidate the paper’s core contribution. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>