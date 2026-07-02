## Summary

The paper proposes **LoRA-Mixer**, a mixture-of-experts framework that routes task-specific LoRA experts into the attention projection layers (Q, K, V) rather than the usual FFN blocks. To train the router, they introduce **Routing Specialization Loss (RSL)**, which combines a global load-balancing term with entropy regularization to encourage input-aware specialization. The framework supports both joint training and plug-and-play reuse of pre-trained LoRAs, and is architecture-agnostic (Transformers and SSMs). Experiments on 15 benchmarks show consistent improvements over LoRAHub, MoLE, MixLoRA, and other baselines with reduced trainable parameters.

## Strengths

- **Novel placement of LoRA-MoE**: Routing LoRA experts inside the attention projection layers is a clean departure from the dominant FFN-focused designs, directly leveraging the attention mechanism for richer token-level specialization.
- **Principled routing loss**: RSL is well-motivated from an information bottleneck perspective, and the paper provides gradient derivation and theoretical justification (convergence and generalization bounds in appendix). The entropy regularization explicitly addresses the over-averaging problem of standard auxiliary losses.
- **Strong empirical results**: Across 15 benchmarks and three base models (LLaMA3-8B, Mistral-7B, Falcon-Mamba-7B), LoRA-Mixer outperforms strong baselines, often with significantly fewer trainable parameters (48% of MixLoRA etc.). Gains of +3.79% on GSM8K, +2.90% on CoLA, and +3.95% on ARC-C are meaningful.
- **Architecture agnostic and plug-and-play**: The method works on both Transformers and SSMs (Falcon-Mamba), and supports direct reuse of publicly available LoRA modules with minimal additional data, enhancing practical applicability.
- **Thorough ablation and analysis**: The paper studies the impact of LoRA rank, expert load balance, training data size, and the RSL component. Cross-model transfer experiments (Mistral → LLaMA3) demonstrate robustness of the learned routing.

## Weaknesses

### Fatal
None.

### Major

1. **Parameter efficiency claim is imprecise**. The paper states “48% of their trainable parameters” but does not provide a clear table comparing total trainable parameter counts for each method under the same settings. The claim is hard to verify and the baseline parameter counts are not reported in a uniform way.
2. **Comparison with “LoRA” as a baseline is misleading**. In Table 2, the row labeled “LoRA” appears alongside MoE methods, but standard LoRA is not a routing method—it is simply a single LoRA adapter. This comparison conflates the effect of having multiple experts versus the routing mechanism. The paper should clearly distinguish “LoRA (single adapter)” from LoRA-MoE baselines.

### Minor

- The paper mentions that RSL requires less training data (Table 9 shows +1.97% at 2K, but -0.37% at 4K) and explains the 4K dip in the appendix. However, the explanation is not in the main text, making the result appear inconsistent without further reading.
- The cross-model transfer experiment (Table 5) uses Zero-Shot CoT for GSM8K, while the base LLaMA3-8B performance is reported with the same protocol—this is reasonable, but the paper should explicitly state the evaluation protocol to avoid confusion.
- Some baselines (e.g., GMoE, DS-MoE, AESL in Table 8) are only compared on a subset of tasks with 2K data, while the main comparison uses different data sizes. It is unclear whether the advantages of RSL are robust across data regimes and tasks.

### Trivial
- The phrase “the routing training is guided by RSL loss for balancing experts loads and specificity” is slightly redundant.

## Nice-to-Haves

- A detailed parameter count table comparing all methods (MoLE, MixLoRA, LoRA-Mixer, etc.) with the same base model and LoRA rank would strengthen the parameter efficiency claim.
- An experiment that ablates the effect of placing experts in projection layers versus FFN layers (holding everything else constant) would directly validate the central design choice.
- A discussion or experiment on the sensitivity of the α and λ hyperparameters in RSL would be helpful for practitioners.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that applying mixture-of-experts to attention projection layers rather than feed-forward layers can yield better task specialization with fewer parameters, because the projection layers control the flow of information into the core attention mechanism. The RSL loss further demonstrates that entropy regularization can naturally resolve the load-balance versus specialization trade-off in routing, which is a general insight applicable beyond LoRA-MoE.

## Suggestions

- Provide a full table of trainable parameter counts for each method to substantiate the “48%” claim.
- Clarify in Table 2 what “LoRA” refers to (single-adapter LoRA) and consider renaming the row to “LoRA (single)” to avoid confusion.
- Move the explanation for the 4K data dip in Table 9 into a footnote or the main text to improve readability.

## Score and Decision

MY FINAL SCORE: 8.0
MY FINAL DECISION: Accept