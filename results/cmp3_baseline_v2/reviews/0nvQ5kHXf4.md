## Summary

The paper introduces WASI (Weight-Activation Subspace Iteration), a method for resource-constrained training of transformer models that jointly compresses both weights and activation maps into low-rank subspaces during fine-tuning. By exploiting the observed stability of parameter and activation subspaces throughout training, WASI uses a one-time SVD followed by efficient subspace iteration, achieving up to 62× memory reduction and 1.4× speedup on a Raspberry Pi 5 while maintaining competitive accuracy on vision transformer tasks.

## Strengths

- **Novel and practical unified compression framework**: WASI is the first method to jointly compress both weights and activations in a single subspace-based training framework for transformers, addressing the two primary memory bottlenecks (weight storage and activation map storage) simultaneously rather than separately.
- **Strong empirical validation of core assumptions**: Section 4.2 provides direct experimental evidence supporting the key hypothesis that weight subspaces remain stable during fine-tuning (Fig. 3a), that subspace iteration (WSI) outperforms repeated full SVD in accuracy-efficiency trade-off (Fig. 3b), and that activation map energy concentrates in few components (Fig. 4). These validation experiments are crucial and well-executed.
- **Comprehensive evaluation across multiple architectures and settings**: The paper evaluates WASI on ViT, SwinT, and TinyLlama across five downstream vision datasets and one language dataset, includes real-device latency measurements on Raspberry Pi 5, and compares against three relevant baselines (ASI, SVD-LLM, vanilla training).

## Weaknesses

### Fatal
None.

### Major
- **Missing key comparisons with parameter-efficient fine-tuning (PEFT) methods**: The paper positions WASI against SVD-LLM, ASI, and vanilla training but does not compare with standard PEFT baselines such as LoRA or its variants under the same transformer fine-tuning setting. LoRA is discussed in related work as having different limitations (adapter coexistence, no inference compression), but a direct empirical comparison on the same tasks would strengthen the evaluation. Without this, it is unclear whether WASI's gains come primarily from weight compression or activation compression, and whether LoRA with activation compression would be competitive.

- **Lack of clarity on how the rank selection strategy interacts with the explained variance threshold**: The paper uses an explained variance threshold ε to determine ranks for both weights and activations. However, it is not clear whether the same ε is applied independently to each layer or globally, and how the tuning of ε in practice would work for a new model or dataset (e.g., is there a systematic way to choose ε without validation on multiple values?). The dynamic programming strategy mentioned for activation ranks (Section 3.3) is only briefly described with a reference to the appendix.

- **The TinyLlama experiment is limited and potentially cherry-picked**: The experiment uses only ε=0.1 (very aggressive compression) and fine-tunes only the last 5 layers. While the results show large memory savings, the accuracy is only compared within a narrow 64-66% range. The paper should include experiments with multiple ε values for TinyLlama, and the observation that WASI even slightly outperforms vanilla at such high compression warrants more careful explanation (noise due to regularization?).

### Minor
- The analysis of memory efficiency and computational complexity (Section 3.4) assumes the same optimal rank for both weights and activations, but in practice these ranks may differ significantly. The derived formulas are useful but their connection to actual experimental results is not clearly drawn.
- The on-device latency experiment (Section 4.4) only reports time per iteration, not total fine-tuning time or convergence speed in terms of epochs to a target accuracy.

### Trivial
- Figure 2 is challenging to interpret because both the axes and the curves are densely packed with information; a clearer visualization would help.
- The paper claims "up to 100× higher memory efficiency than SVD-LLM at similar accuracy" (Section 4.3), but this claim appears in the ViT-on-CIFAR-10 paragraph and seems to rely on a specific ε setting; it is not a headline claim.

## Nice-to-Haves
- An ablation study separating the contribution of weight compression (WSI) from activation compression (ASI) would clarify the marginal benefit of the joint approach.
- Including a convergence comparison (epochs to reach target accuracy) in the on-device experiments would strengthen the practical relevance.

## Novel Insights

The key conceptual contribution is the observation and empirical confirmation that not only activation maps but also weight matrices maintain stable low-rank subspaces during fine-tuning of transformers, enabling the one-time SVD + subspace iteration strategy without accuracy degradation. This insight is non-trivial because weights change during training (unlike activations which are intermediate computational artifacts), yet the paper shows that the changes are confined to a stable intrinsic subspace. The joint compression framework that emerges from this insight is valuable for the on-device learning community, where both activation and weight memory matter.

## Suggestions
1. Include LoRA (or a representative PEFT method) as an additional baseline in at least one experiment (e.g., ViT on CIFAR-10) to contextualize WASI's performance relative to standard parameter-efficient methods.
2. Provide a sensitivity analysis showing how the results vary with the explained variance threshold ε, perhaps with a recommended heuristic for setting ε on a new model/dataset.
3. Clarify in the main text how the dynamic programming for activation ranks works (currently only referenced to appendix), and whether the same ε is applied to both weights and activations.

## Score and Decision

The paper presents a well-motivated and empirically sound method for an important problem (on-device training of transformers). The strengths outweigh the weaknesses, and the missing comparisons and clarity issues are addressable. I recommend acceptance with a moderate score.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>