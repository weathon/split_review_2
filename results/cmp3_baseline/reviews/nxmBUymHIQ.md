## Summary

The paper proposes LoLoRA, a memory-efficient fine-tuning method for LLMs that combines local unsupervised updates (e.g., Hebbian PCA) for the LoRA A matrix with gradient-based backpropagation for the B matrix. The authors provide theoretical justification that optimal A should span the top eigenspace of the input covariance, and they empirically compare LoLoRA against LoRA, LoRA-FA, and EVA-initialized variants on GLUE, math reasoning, and multimodal tasks.

## Strengths

- **Theoretical analysis of optimal A initialization**: Theorem 4.4 formally characterizes the set of optimal A matrices under a random regression assumption, showing that A should span the dominant eigenspace of the input covariance. This provides a principled foundation for data-driven initialization and local update rules.
- **Comprehensive experimental setup**: The paper evaluates on multiple domains (NLU, math reasoning, multimodal) with several model sizes (RoBERTa-large, LLaMA-3.1-8B, LLaVA-v1.5-7B, TinyLlama-1.1B) and includes ablations over initialization methods and local update rules.
- **Clear motivation for activation memory reduction**: The paper correctly identifies that standard LoRA still requires storing activations for the A matrix, and proposes a method to avoid this by using forward-pass-only updates for A.

## Weaknesses

### Major

1. **No clear advantage over LoRA-FA with good initialization**: The empirical results show that LoLoRA does not consistently outperform LoRA-FA with EVA initialization. On GLUE, LoLoRA HPCA is often worse than LoRA-FA (uniform) and comparable to LoRA-FA (EVA). On math reasoning, LoLoRA ties with LoRA-FA (EVA). On multimodal, LoLoRA is slightly worse than LoRA-FA (EVA). The paper claims "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups," but this is not supported by the tables—LoRA-FA (uniform) is better on most GLUE tasks, and LoRA-FA (EVA) ties or outperforms LoLoRA on the other two setups.

2. **Incremental memory savings over LoRA-FA**: LoRA-FA already eliminates activation storage for A and achieves the same memory reduction (e.g., 26 GB vs 30 GB in Table 3). LoLoRA adds extra optimizer state for the local updates, so its memory footprint is slightly larger than LoRA-FA (e.g., 24.1 GB vs 23.9 GB in Table 4). The paper's claim of "further reducing memory" is misleading—the main memory benefit comes from freezing A, not from the local updates themselves.

3. **Theoretical assumptions limit practical relevance**: The analysis assumes stationary targets and isolated submodules (Definition 4.2), which is not true in multilayer Transformer fine-tuning where representations shift during training. The paper acknowledges this as a limitation, but the core theoretical justification for the local update method relies on these assumptions. The connection between the theory and the actual empirical behavior is not validated.

4. **Local updates do not demonstrate adaptation to distribution shifts**: The paper motivates local updates as a way to "adapt to input distribution shifts without storing activations," but no experiment measures distribution shift or compares how well LoLoRA adapts compared to a frozen A. The ablations show that HPCA (svd first)—which initializes A via PCA on the first batch and then applies HPCA—performs similarly to HPCA (uniform), suggesting that the online adaptation may not be crucial.

### Minor

- The paper states "LoLoRA achieves slightly better results than LoRA-FA (EVA)" on GLUE, but Table 1 shows LoLoRA is lower on CoLA (66.3 vs 64.7? Actually LoRA-FA EVA is 64.7, LoLoRA 66.3—so better on CoLA, but worse on RTE, MRPC, STS-B, MNLI, QQP, SST-2). The claim is not consistently supported.
- The ablation results (Table 6) show that Full LoRA (standard backprop on both A and B) significantly outperforms all LoLoRA variants (e.g., 2.521 vs 2.535 at r=8), yet the paper does not discuss this gap or why the local update method cannot close it.

## Nice-to-Haves

- An experiment explicitly measuring adaptation to distribution shift (e.g., fine-tuning on a sequence of different tasks or with noisy inputs) would strengthen the motivation for online local updates.
- A comparison of LoLoRA against other memory-efficient methods like VeRA or adaptive rank methods would better contextualize the contribution.

## Novel Insights

None beyond the paper's own contributions. The theoretical characterization of optimal A (Theorem 4.4) is a useful formalization, but it largely confirms the intuition behind existing methods like EVA. The idea of using local Hebbian updates for A is novel in the LoRA context, but the empirical results do not demonstrate a practical advantage over simpler freezing strategies.

## Suggestions

- Clarify the memory comparison: report memory savings relative to LoRA-FA, not just LoRA, and discuss the overhead of local optimizer state.
- Provide a more balanced interpretation of results: acknowledge that LoLoRA does not outperform LoRA-FA with EVA initialization and that the main benefit is theoretical or conceptual rather than empirical.
- Consider evaluating on a scenario where input distribution shifts are present (e.g., continual fine-tuning or domain adaptation) to test the claimed advantage of online adaptation.

## Score and Decision

**Score**: 4.0

**Decision**: Reject

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>