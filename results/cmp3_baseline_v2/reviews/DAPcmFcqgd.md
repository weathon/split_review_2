## Summary

The paper proposes MoEP (Modular Expert Paths), a decoder-only architecture that combines model parallelism with Mixture-of-Experts (MoE) style routing to introduce sparsity while keeping the total parameter count fixed. The architecture interleaves dense GPT-2 layers with a sparse middle stack consisting of MoE shrink/grow blocks and parallel layers with top-k token routing. The authors evaluate on the BabyLM strict-small track and claim to outperform all baseline models including GPT-2 and GPT-BERT.

## Strengths

- The core idea of maintaining a fixed parameter budget while adding sparsity through parallel layers with reduced dimensionality is a sensible and practically motivated direction, addressing a known limitation of standard MoE (parameter explosion).
- The paper provides a clear architectural description, releases code and models, and follows the BabyLM evaluation pipeline, which supports reproducibility.
- The analysis of training dynamics (Figures 3-4) offers some insight into how MoEP learns faster early in training compared to the dense GPT-2 baseline.

## Weaknesses

### Fatal

- **The paper's central claim that MoEP "outperformed all BabyLM strict-small baseline models, including the GPT-2 and GPT-BERT models" is false.** Table 1 shows that on the macro average *excluding* AoA (the primary metric reported for most models), MoEP scores 49.00, while GPT-BERT (causal) scores 54.10, GPT-BERT (focus-causal) 53.65, and GPT-BERT (mixed-causal) 52.40. MoEP is clearly worse than all GPT-BERT variants on this metric. The claim is only true when including AoA, which is a single outlier task where MoEP scores 53.70 while GPT-BERT variants score negative or near zero. This misrepresentation invalidates the paper's main advertised result.

### Major

- **Unfair comparison for MoEP-SwiGLU:** The SwiGLU variant has 38M parameters vs. 28M for GPT-2 and the linear MoEP, a 36% increase. The paper claims to keep parameter count fixed, but this variant violates that premise. The conclusion that "lightweight linear experts are more effective at small scale" is confounded by the parameter mismatch.
- **Lack of ablation studies:** The paper does not isolate the contribution of each component (parallel layers, MoE shrink/grow, top-k routing, load-balancing loss). Without ablations, it is unclear whether the performance gains come from the proposed sparsity mechanism or from other architectural differences (e.g., the specific layer count distribution, reduced dimensionality in the middle stack).
- **Limited evaluation scope:** The experiments are confined to the small-scale BabyLM benchmark. The paper acknowledges this limitation but does not provide any evidence or theoretical argument that the approach would scale. Given that the method does not outperform the best baseline (GPT-BERT) even at this small scale, the practical significance is questionable.

### Minor

- The paper states that MoEP "obtained the best score in five individual tasks, the highest count among all models evaluated." Counting from Table 1, MoEP achieves the best score in Entity (35.65), Reading (6.70), RTE (tied 62.60), WSC (67.30), and AoA (53.70) — that is five tasks, but AoA is a task where most baselines have negative scores, making it an unusual benchmark. The claim is technically correct but somewhat cherry-picked.
- The analysis of training dynamics claims MoEP shows "stable training," but Figure 3 indicates that after peaking at 30M words, MoEP's performance degrades (overfitting), while GPT-2 continues to improve on some tasks. The term "stable" is misleading.
- The load-balancing loss is introduced but never analyzed. There is no evidence that expert collapse was avoided or that the auxiliary loss had any effect.

### Trivial

- Minor formatting issues (e.g., "textbfAdamW" in Section 4, "Ex" in Figure 1 caption).

## Nice-to-Haves

- Ablation studies varying the number of parallel blocks (P), top-k values, and the presence of the MoE shrink/grow blocks.
- Analysis of expert utilization and load balancing over training.
- Comparison with other parameter-matched sparse architectures (e.g., standard MoE with reduced total experts to match parameter count).
- Scaling experiments to larger model sizes or datasets to test whether the approach generalizes.

## Novel Insights

None beyond the paper's own contributions. The observation that linear experts outperform SwiGLU at small scale is mildly interesting but expected given the parameter count difference and the simplicity of the BabyLM data.

## Suggestions

- Correct the central claim to accurately reflect that MoEP outperforms GPT-2 but not GPT-BERT on the standard macro average (excluding AoA). The paper should clearly state which baseline it beats and under which metric.
- Add ablation studies to disentangle the effects of parallel layers, MoE routing, and dimensionality reduction.
- Ensure fair parameter count comparisons for all model variants, or explicitly discuss the trade-offs when parameter counts differ.
- Provide analysis of routing behavior and load balancing to support the claim that the architecture avoids expert collapse.

## Score and Decision

The paper presents an interesting architectural idea, but the fatal misrepresentation of results (claiming to outperform all baselines when it does not) undermines the core contribution. The lack of ablations and the unfair comparison for the SwiGLU variant further weaken the paper. The contribution is not sufficiently supported to warrant acceptance.

MY FINAL SCORE: 3.0<score>3.0</score>
MY FINAL DECISION: Reject<decision>Reject</decision>