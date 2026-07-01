## Summary

This paper proposes NuSA-CL, a memory-free continual learning framework for vision-language models (VLMs) like CLIP. It identifies an approximate null space of the current weight matrices via SVD, constrains low-rank (LoRA-like) updates to this low-energy subspace throughout training, and merges the update back into the backbone to maintain a fixed parameter budget. Experiments show that NuSA-CL outperforms other storage-free methods on MTIL and CIFAR100 benchmarks and approximates the performance of storage-based approaches with dramatically lower compute and memory costs.

## Strengths

- **Strong practical motivation and clear problem identification.** The paper correctly argues that existing CL paradigms face a scalability wall (linear storage/parameter growth) that limits truly lifelong deployment. NuSA-CL directly addresses this by enabling adaptation within a fixed-capacity model without replay buffers, distillation, or expanding modules.
- **Well-designed method with sound intuition.** Using the low-energy (null) subspace of the current weights to confine updates is a clean, principled way to minimise interference with prior knowledge. The persistent constraint (freezing the null-space bases) is a key innovation over related work that uses such subspaces only for initialization.
- **Comprehensive empirical evaluation across multiple settings.** The paper evaluates on both the MTIL benchmark (full-shot and 5-shot) and long-sequence CIFAR100 (10/20/50 steps). NuSA-CL consistently outperforms all storage-free baselines (LoRA, MiLoRA) and achieves competitive performance with storage-based methods at orders-of-magnitude lower cost.
- **Clear ablations validating design choices.** The subspace selection experiment (Tail vs. Top vs. Random) convincingly shows that the low-energy subspace yields the lowest forgetting. The persistent constraint ablation demonstrates that freezing the null-space bases is critical for retention. These ablations directly support the core mechanism.
- **Excellent efficiency profile.** 1.5M trainable parameters (vs. 15.7M for LoRA, 59.8M for MoE-Adapters), zero additional storage, low peak GPU memory, and fast training time (1.21 GPU-hours) make the method practical for resource-constrained deployment.

## Weaknesses

### Fatal
None.

### Major
1. **Missing error bars and statistical significance.** Results are reported as single numbers without standard deviations or confidence intervals across multiple runs. Given that continual learning results can be sensitive to initialization, data ordering, and random seeds, this omission makes it difficult to assess the reliability and significance of the reported improvements. This is a standard expectation for empirical papers at top venues.
2. **Limited architectural scope.** All experiments use CLIP ViT-B/16. While the paper briefly discusses scaling to larger models in the practical guidance section, no experiments on larger VLMs (e.g., ViT-L, ViT-g, or alternative architectures like SigLIP) are provided. The claim that “the same scaling behavior extends naturally” is speculative without evidence. The method’s SVD overhead on larger projection matrices could become non-negligible.

### Minor
1. **Theoretical contribution is modest.** Lemma 1 and Theorem 2 bound parameter-space interference but are straightforward consequences of the SVD construction. The authors themselves acknowledge that these are not function-level guarantees. While the theory cleanly motivates the approach, it does not provide deep insight into forgetting dynamics or plasticity.
2. **The “zero auxiliary model load” claim is slightly imprecise.** The null-space bases (U_n, V_n) are computed and stored during training for each task; this is part of the model weights themselves. The method is truly memory-free for *external storage* (no replay buffers, no gradient memories), which is the intended claim, but the wording could be clarified.
3. **Forgetting metric in Figure 3a is not fully defined in the paper.** “Average drop from post-task to final performance” is stated but it would be helpful to provide the exact formula, especially since the ablation analysis relies on this metric.

### Trivial
None.

## Nice-to-Haves

- An analysis of sensitivity to task order (e.g., random vs. fixed ordering of the MTIL datasets) would strengthen the claim of practical robustness.
- A small-scale experiment on a larger VLM backbone (e.g., ViT-L) to demonstrate that the SVD overhead remains manageable and that the null-space mechanism does not collapse would increase confidence in scalability.
- Reporting backward transfer (BWT) and forward transfer (FWT) metrics on the MTIL benchmark would provide additional insight into the method’s behavior beyond the Avg./Last/Transfer metrics used.

## Novel Insights

The paper’s key insight is that a persistent, data-agnostic constraint to the intrinsic null space of the current weights can serve as a scalable and effective forgetting-mitigation strategy for continual learning on VLMs. This contrasts with prior SVD-guided adaptation methods that use the null space only for initialization, allowing updates to drift during training. The ablation showing that unfreezing the null-space bases harms performance (Table 4a) empirically validates that *persistence* of the constraint is the critical component. The null-space dynamics analysis (Figure 2) further reveals that NuSA-CL progressively utilises previously underused spectral dimensions, converting the learning process from overwriting (as in LoRA/Full-FT) to accumulation.

## Suggestions

- Add standard deviations over at least 3 runs for all main experimental tables (Tables 1, 2, 3). This is the most impactful change for increasing confidence in the results.
- Conduct a brief experiment on a larger CLIP backbone (e.g., ViT-L/14) on at least the MTIL benchmark to demonstrate that the method and its efficiency advantages transfer.
- Clarify the forgetting definition used in Figure 3a and include the formula explicitly in the captions or main text.

## Score and Decision

**Score:** 6

**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept