## Summary

This paper proposes HFPrune, a structured pruning method for Large Language Models that replaces the standard one-hot cross-entropy loss criterion with the information entropy of the model's output distribution for Taylor-based neuron importance evaluation. The key insight is that cross-entropy only considers the single ground-truth next token, while information entropy captures the model's predictive confidence across the entire vocabulary, leading to a more holistic importance assessment. The method focuses on pruning MLP neurons, and experiments on LLaMA and Qwen series models show consistent improvements over existing pruning methods across multiple zero-shot benchmarks.

## Strengths

- **Novel and well-motivated criterion**: The information entropy criterion is a simple yet elegant solution to a known limitation of Taylor-based pruning. The paper clearly articulates why cross-entropy is insufficient (focusing only on the single next token) and provides a principled alternative that considers the full output distribution without requiring labels or a teacher model.

- **Strong empirical results**: The method consistently outperforms existing pruning methods (LLM-pruner, LoRAPrune, LoRAP, SDMPrune) across multiple model families (LLaMA-2-7B, LLaMA3.2-3.2B, LLaMA3.2-1.2B, Qwen2.5-7B, Qwen2.5-1.5B, Qwen3-1.7B) and at various pruning ratios (20%, 30%, 40%). Notably, at 20% pruning on LLaMA2-7B, the pruned model even exceeds the original model's performance after fine-tuning.

- **Computational efficiency**: The method is substantially more efficient than the closest competitor SDMPrune, being approximately 3x faster and consuming 31% less peak GPU memory for LLaMA2-7B. This practical advantage is important for real-world deployment.

- **Thorough ablation studies**: The paper provides convincing ablation studies that isolate the effect of the information entropy criterion (Table 6), validate that it better preserves output distribution (Table 7), and justify the MLP-only pruning strategy (Table 8).

## Weaknesses

### Major

- **Limited comparison with state-of-the-art unstructured pruning methods**: The paper only compares with structured pruning methods (LLM-pruner, LoRAPrune, LoRAP, SDMPrune). Given that methods like SparseGPT and Wanda are widely used and achieve strong results, the absence of comparison with these methods (even if they are unstructured) weakens the claim of superiority. The paper mentions these in related work but does not include them in experiments.

- **Fine-tuning protocol may favor the proposed method**: All methods are fine-tuned on the LaMini dataset using LoRA for 2 epochs. However, different pruning methods may benefit from different fine-tuning strategies or durations. The paper does not investigate whether the reported improvements are robust to different fine-tuning hyperparameters or datasets. The fact that the method already outperforms without fine-tuning (Table 6) mitigates this concern, but the fine-tuning results could still be influenced by the specific protocol.

- **Missing statistical significance**: The paper reports single runs without error bars or statistical significance tests. Given that zero-shot benchmarks can have variance, it would be helpful to know whether the improvements (e.g., 0.8% average improvement at 20% pruning on LLaMA2-7B) are statistically significant.

### Minor

- **Limited analysis of failure cases**: The method does not uniformly outperform on all individual benchmarks. For example, on Crows-Pairs and Wino, the method sometimes underperforms baselines. The paper does not discuss why the entropy criterion might be less effective for certain types of tasks.

- **Theoretical justification could be deeper**: While the intuition for using entropy is clear, the paper does not provide a theoretical analysis of why entropy is a better criterion than cross-entropy for preserving model capabilities. For example, is there a connection to information-theoretic principles or generalization bounds?

### Trivial

- The paper states "our pruned model not only recovers but even exceed the performance of the original dense model" (Section 1), but this is only shown for one specific setting (LLaMA2-7B at 20% pruning). The claim could be more precisely scoped.

## Nice-to-Haves

- Comparison with unstructured pruning methods like SparseGPT and Wanda, even if adapted to structured pruning or if the comparison is limited to post-pruning performance without fine-tuning.
- Error bars or confidence intervals for the main results.
- Analysis of how the entropy-based importance scores correlate with other importance metrics (e.g., weight magnitude, activation norms).
- Investigation of whether the method can be extended to prune attention modules as well, perhaps with a different criterion.

## Novel Insights

The paper's core insight is that the choice of criterion for Taylor-based importance evaluation fundamentally shapes what the pruning process preserves. By shifting from a label-dependent criterion (cross-entropy) to a label-free, distributional criterion (entropy), the pruning process naturally aims to preserve the model's full predictive distribution rather than just its ability to predict the correct token. This is a conceptually clean solution that avoids the computational overhead and gradient issues of self-distillation approaches while achieving better results. The finding that entropy-based pruning can sometimes yield models that outperform the original after fine-tuning suggests that removing neurons that contribute to "uncertain" predictions may actually regularize the model.

## Suggestions

- Include comparisons with SparseGPT and Wanda (even if adapted to structured pruning or with a note about the different pruning granularity) to strengthen the empirical evaluation.
- Report results with standard deviations or confidence intervals across multiple runs or seeds.
- Add a discussion of when the entropy criterion might be less effective (e.g., on tasks where the single correct token is much more important than the distribution shape).

## Score and Decision

The paper presents a novel, well-motivated, and empirically validated method for LLM pruning. The information entropy criterion is a simple but effective idea that addresses a genuine limitation of existing Taylor-based approaches. The experimental results are strong and consistent across multiple model families and pruning ratios. The main limitations are the lack of comparison with unstructured pruning methods and the absence of statistical significance measures, but these do not invalidate the core contribution. The paper is clearly written and the experiments are well-designed.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>