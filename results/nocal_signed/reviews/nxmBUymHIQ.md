Now I have all the information needed to produce the final consolidated review. Let me compile it.

---

## Summary

This paper proposes LoLoRA, a LoRA variant that combines gradient-free local updates (HPCA) to adapter matrix A during the forward pass with standard gradient-based updates to adapter B, aiming to avoid storing activations for A's backward pass. The paper also provides a theoretical characterization (Theorem 4.4) showing that under a random regression assumption, the optimal A spans the top-r principal subspace of the input covariance — connecting to and extending the EVA initialization method.

## Strengths

- **Clean theoretical characterization of optimal A (Theorem 4.4).** Under the stated assumptions (i.i.d. Gaussian ΔW₀, known input covariance), this theorem rigorously characterizes the set of optimal A matrices as spanning the top-r principal subspace. This provides principled theoretical grounding for the EVA initialization (Paischer et al., 2024) and clarifies why certain initializations work better for frozen-A settings. This is a genuine formal contribution.

- **Well-motivated core idea.** The paper identifies a real trade-off: LoRA-FA saves memory by freezing A but risks performance degradation, and the idea of using forward-pass-only local updates to A that don't require storing activations is a sensible approach. The framing in Section 3.2–3.3 is internally consistent and coherent.

- **Breadth of evaluation.** The paper tests on three qualitatively different settings — NLU (GLUE/RoBERTa-large), math reasoning (GSM8K/LLaMA-3.1-8B), and multimodal (LLaVA-v1.5-7B) — plus careful ablations on TinyLlama comparing multiple local update rules and initializations. This is more extensive than many PEFT papers.

## Weaknesses

### Fatal
None.

### Major

- **The method does not demonstrate a clear performance advantage over the simpler LoRA-FA baseline it claims to improve upon.** Across all three experimental settings, LoLoRA is statistically comparable to LoRA-FA variants:
  - **GLUE (Tables 1–2):** LoLoRA never beats the best LoRA-FA variant on any of the 8 tasks. It is indistinguishable from LoRA-FA (uniform) on most comparisons (e.g., RTE: LoRA-FA 86.4 vs LoLoRA 84.6; MRPC: 89.8 vs 89.9; MNLI: 90.6 vs 90.3; QQP: 90.8 vs 90.6).
  - **GSM8K (Table 3):** LoLoRA (0.829) ties LoRA-FA (EVA) (0.829 ± 0.004 vs ± 0.005) within noise.
  - **LLaVA (Table 4):** LoLoRA (perplexity 2.93) sits between LoRA-FA (EVA) (2.92) and LoRA-FA (uniform) (2.97).
  
  The paper's central motivation — that LoRA-FA "has limitations in performance due to the suboptimal feature extraction by a randomly initialized low-rank matrix A" (Section 3.1) and that LoLoRA addresses this — is not supported by the evidence.

- **The local HPCA updates are not shown to add value beyond proper EVA initialization.** Theorem 4.4 shows that optimal A spans the top-r eigenvectors of the input covariance — exactly what EVA initialization provides. The paper explicitly concedes (Section 5.3) that "HPCA updates do not improve EVA-initialized adapters." The only claimed advantage over EVA is "not requiring a separate incremental PCA pass before training" (Section 5.4). This is a convenience benefit rather than a performance improvement, and it means the entire machinery of local forward-pass updates (HPCA, SNL, running mean subtraction, local optimizer state) is redundant when EVA initialization is available. This undermines the paper's central methodological contribution.

### Minor

- **The theoretical analysis has limited applicability to the actual problem.** Theorem 4.4 assumes i.i.d. Gaussian ΔW₀ (Assumption 4.1) and stationary targets — assumptions the paper acknowledges as unrealistic (Conclusion). While mathematically sound, the theory characterizes the optimal *fixed* A for a stationary regression problem, and does not directly support the iterative local update dynamics during actual fine-tuning where task-specific weight changes are structured and inputs/targets are non-stationary. The results are valid within their assumptions but their relevance to real fine-tuning is limited.

- **Memory comparisons could be clearer.** LoLoRA introduces additional optimizer state for local updates (acknowledged in the Conclusion), yet Table 3 reports identical extra memory (26 GB) for both LoRA-FA and LoLoRA, suggesting measurement granularity masks the overhead. The "up to 20% less" claim (Section 5.1) is relative to extra memory excluding the base model; reporting absolute savings as a fraction of total GPU usage would provide better context.

- **The conclusion's claim is overstated.** The paper states that "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" (Conclusion). If "standard LoRA-FA" means uniform initialization, this is defensible, but the practical significance is marginal — on GSM8K the gap (0.003) is within one standard deviation, and on GLUE there is no improvement at all. The phrasing "consistently outperforms" implies a clearer advantage than the data support.

### Trivial
None.

## Nice-to-Haves

- An empirical analysis comparing the subspace learned by the local HPCA updates vs. the EVA-initialized A subspace during training, to establish whether the iterative updates actually move A toward a different or better subspace than initialization alone.
- Ablation of HPCA hyperparameters (smoothing factor of 0.98, local optimizer choices).
- A more detailed runtime breakdown isolating the computational overhead of the local update rule from the rest of forward/backward pass.
- Settings where LoRA-FA degrades substantially (e.g., very low rank, long training, distribution shift) and LoLoRA recovers the gap — this would substantiate the claimed advantage.

## Removed Points

These points from the input review were removed as factually incorrect, noise, or not grounded in the paper:

- The claim that LoLoRA (LLaVA) is "closer to the worse one (uniform) than to the better one (EVA)" — this is **factually wrong**. LoLoRA (2.93) differs from LoRA-FA (EVA) (2.92) by 0.01 and from LoRA-FA (uniform) (2.97) by 0.04. LoLoRA is strictly closer to EVA.
- The assertion that the Conclusion's claim about "consistently outperforms" is simply "not true" — this overstates the error. The claim is defensible if "standard LoRA-FA" means uniform initialization, though the practical significance is marginal.
- The estimate that memory savings are "approximately 5% of total capacity" — this is a rough external computation, not a flaw in the paper itself. Reporting extra memory (excluding model weights) is a common convention in the field.
- Various formatting nitpicks and generic scope-creep criticisms (e.g., demanding analysis of streaming/online settings that are outside the paper's scope).

## Novel Insights

None beyond the paper's own contributions. The reviews surface a significant gap between the paper's empirical claims and the evidence, but this is a shortcomings analysis rather than a novel insight.

## Suggestions

- Either (a) identify settings where LoRA-FA degrades substantially and LoLoRA recovers the gap, or (b) reframe the paper's contribution to honestly acknowledge that the main advantage of LoLoRA over EVA is the convenience of not requiring a pre-training PCA pass, rather than claiming performance improvements over LoRA-FA.
- Add a precise breakdown of total GPU memory consumption (including base model weights) to contextualize the memory savings.
- Report and analyze what the locally-updated A converges to during actual training, especially relative to the EVA-initialized subspace.

## Score and Decision

The paper has a genuine theoretical contribution (Theorem 4.4) and a well-motivated idea, evaluated across diverse settings. However, the central empirical claim — that LoLoRA improves over the simpler LoRA-FA baseline — is not supported by the evidence. The local HPCA updates are shown not to improve over EVA initialization, reducing the core methodological contribution to a convenience advantage. The paper overstates its empirical findings relative to what the data show.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>