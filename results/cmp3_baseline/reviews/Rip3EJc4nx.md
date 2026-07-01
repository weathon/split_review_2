## Summary

This paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy loss with the information entropy of the model's output distribution as the criterion for Taylor-based neuron importance estimation. By considering the entire prediction distribution rather than only the single ground-truth token, the method aims to better preserve the model's global predictive behavior after pruning. Experiments on LLaMA and Qwen series models across multiple zero-shot benchmarks show consistent improvements over existing structured pruning methods, with modest gains (0.5–1% average accuracy) and reduced computational overhead compared to self-distillation baselines.

## Strengths

- **Simple and well-motivated idea**: Replacing cross-entropy with entropy in Taylor pruning is conceptually clean, label-free, and avoids the zero-gradient issue of self-distillation methods. The motivation is clearly explained with Figure 1.
- **Comprehensive empirical evaluation**: Experiments cover multiple model families (LLaMA-2, LLaMA-3.2, Qwen2.5, Qwen3) at various scales (1.2B–7B) and pruning ratios (20%–40%), with 10 zero-shot benchmarks. The method consistently outperforms baselines.
- **Good ablation studies**: The paper isolates the effect of the entropy criterion (Table 6), measures output distribution preservation (Table 7), and justifies the MLP-only pruning choice (Table 8). These ablations support the core claims.
- **Efficiency advantage**: Table 5 shows HFPrune is substantially faster and more memory-efficient than the self-distillation baseline SDMPrune during the pruning process itself.

## Weaknesses

### Fatal
None.

### Major
- **Overstated motivation regarding cross-entropy**: The paper claims cross-entropy "ignores all other potential predictions" and only focuses on the single next token. In reality, the gradient of cross-entropy w.r.t. hidden activations involves all logits (through the softmax), so the importance score does indirectly consider the full distribution. The argument is technically imprecise and the claimed advantage is less stark than presented. The entropy criterion is still a valid alternative, but the paper's framing exaggerates the limitation of cross-entropy.
- **Modest practical gains**: The average accuracy improvements over the best baseline (SDMPrune) are typically 0.5–1.0 percentage points. While consistent, these gains are small and may not justify a paradigm shift in pruning practice. The paper does not report statistical significance or variance across runs, making it hard to assess reliability.

### Minor
- **Limited comparison scope**: The paper only compares with structured pruning methods that also fine-tune after pruning. It does not compare with popular one-shot unstructured methods like SparseGPT or Wanda, nor with other structured methods that prune both attention and MLP (e.g., LLM-Pruner). While the focus on structured MLP pruning is justified, the absence of these baselines limits the context.
- **Fine-tuning details**: The paper uses LoRA fine-tuning for 2 epochs on LaMini. It is unclear whether baselines use the same fine-tuning protocol (same data, epochs, LoRA rank, etc.). If baselines use different fine-tuning, the comparison may not be fully fair. The paper should explicitly state that all methods share the same fine-tuning setup.

### Trivial
- Table 3 has formatting issues: some rows appear duplicated (e.g., Qwen2.5-1.5B 20% results are identical to Qwen2.5-7B 40% results). This is likely a copy-paste error and should be corrected.

## Nice-to-Haves

- Provide per-run variance or confidence intervals for the main results to assess statistical significance.
- Include a comparison with a method that prunes both attention and MLP using the same entropy criterion, to further validate the MLP-only design choice.
- Show results on a broader set of tasks (e.g., MMLU, GSM8K) to test generalization beyond zero-shot benchmarks.

## Novel Insights

None beyond the paper's own contributions. The key insight—using entropy of the output distribution as a Taylor pruning criterion—is novel and well-executed, but the underlying idea is a straightforward extension of existing Taylor pruning frameworks.

## Suggestions

- Clarify the gradient argument: acknowledge that cross-entropy gradients do involve all logits, but emphasize that entropy is label-free and directly measures distributional uncertainty, which is a different and potentially more holistic signal.
- Ensure all baselines use identical fine-tuning protocols and report this explicitly.
- Fix the duplicated rows in Table 3 and verify all numerical entries.

## Score and Decision

The paper presents a clean, well-motivated modification to Taylor pruning with solid empirical support. The contribution is incremental but practically useful, and the experiments are thorough. However, the modest gains and the slightly overstated motivation prevent a higher score.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>