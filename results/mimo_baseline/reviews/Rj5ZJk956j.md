## Summary
This paper introduces a weight-based method for analyzing gated neurons in transformers by computing cosine similarities between input and output weight vectors, revealing their "read-write" functionality. The method uncovers "weakening neurons" — a small class that activates very frequently and has outsized influence on model behavior — and shows that this pattern (strengthening in early layers, weakening in late layers) is consistent across 12 LLMs. Through conditional ablation experiments, the authors discover that negative gate values of the Swish activation function play a previously unrecognized functional role.

## Strengths
- **Genuinely novel and clean method.** The cosine similarity approach for gated neurons is simple yet insightful. While Gurnee et al. (2024) computed similar cosines for GPT-2, the authors develop a full taxonomy of RW functionalities (strengthening, conditional strengthening, proportional change, etc.) and systematically apply it to gated architectures (SwiGLU/GEGLU), which have not received this kind of analysis.
- **Universality across 12 models.** The finding that early-middle layers contain conditional strengthening neurons while late layers contain weakening neurons is demonstrated across Llama, Gemma, OLMo, Mistral, Qwen, and Yi families. This cross-model consistency is a strong empirical contribution.
- **Surprising finding about negative gate values.** The conditional ablation experiments (Section 6.2) convincingly show that negative gate values — previously thought to matter only for training dynamics — have strong functional effects. This challenges the common assumption that Swish is "like ReLU for inference purposes."
- **Well-designed ablation experiments.** The use of random-neuron baselines from the same layers controls for layer-level effects, isolating the contribution of weakening neurons specifically. The results (Figure 3) clearly show that weakening neurons have a disproportionate effect on attribute rate and entropy compared to random neurons of equal count.
- **Methodological contribution of conditional ablation.** Partitioning a neuron's activations by the signs of x_gate and x_in is a useful technique that enables fine-grained causal analysis of individual neuron contributions.

## Weaknesses
### Fatal
None.

### Major
- **Ablation experiments limited to one model.** All functional experiments (attribute rate, entropy, conditional ablation) are conducted only on OLMo-7B. While the weight-based RW patterns are universal across 12 models, the functional impact findings could differ across architectures. This significantly limits the strength of the claim that weakening neurons have "outsize influence" in general.
- **Incomplete mechanistic explanation.** The case study in Section 8 reveals that even interpretable weakening neurons exhibit complex behavior that is difficult to fully understand. The paper acknowledges this but doesn't resolve it — weakening neurons are discovered to be important, but *why* they work remains somewhat opaque. The "superposition" explanation in Section 6.3 is speculative.

### Minor
- **Threshold sensitivity.** The classification uses τ = 0.5, but no sensitivity analysis is provided. How robust are the reported patterns to different threshold choices? The scatter plots in Figure 2 suggest the patterns are real, but a quantitative robustness check would strengthen confidence.
- **Preprocessing step justification.** The sign-based preprocessing in Section 3.2 (multiplying w_in and w_out by the sign of cos(w_gate, w_in)) is argued in Appendix C, but since this is core to the method and can affect all downstream cosine comparisons, a brief in-paper justification would help readers.

### Trivial
None.

## Nice-to-Haves
- Ablation experiments on at least one additional model (even a smaller one) to confirm the functional impact findings generalize.
- A sensitivity analysis on the threshold τ, showing how neuron classification counts change.
- Analysis of how weakening neuron patterns evolve during training (the authors mention this as future work, but even preliminary results would be valuable).

## Novel Insights
The most genuinely novel insight is that negative gate values in Swish activations are not merely artifacts of smooth training dynamics but carry real functional significance for model behavior. The conditional ablation method elegantly isolates this: when x_gate < 0 and x_in < 0 (case iii), weakening neurons behave as strengthening neurons, and this case accounts for much of their entropy-reducing effect. This challenges the widespread interpretive shortcut of treating Swish as functionally equivalent to ReLU during inference — a finding with broad implications for mechanistic interpretability of all gated models.

## Suggestions
- Conduct ablation experiments on at least one more model to test generalizability of functional impact claims.
- Add a brief sensitivity analysis of the τ threshold on the classification results.
- Explore whether weakening neurons exhibit systematic token-level or semantic patterns (e.g., do they tend to suppress particular types of predictions?), which would deepen the mechanistic understanding beyond "they are important but hard to interpret."

## Score and Decision
The paper presents a clean, novel method that yields genuinely surprising and universal findings about transformer internals. The discovery about negative gate values is a meaningful contribution to mechanistic interpretability. However, the functional analysis is limited to a single model, and the mechanistic understanding of weakening neurons remains incomplete. These are solvable weaknesses rather than fundamental flaws, and the core contributions — the RW taxonomy, the universal layer patterns, and the negative gate finding — are valuable to the community.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>