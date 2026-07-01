## Summary

This paper investigates the effect of the L0 hyperparameter (average number of active latents per token) in Sparse Autoencoders (SAEs) for LLM interpretability. Using toy models and LLM experiments, the authors show that setting L0 incorrectly—either too low or too high—causes the SAE to mix correlated features, producing polysemantic and incorrect latents. They demonstrate that the common sparsity-reconstruction tradeoff is misleading because at low L0, an SAE with incorrect features can achieve better reconstruction than a ground-truth SAE. The paper proposes a proxy metric, decoder pairwise cosine similarity (c_dec), which is minimized at the correct L0 and correlates with peak sparse probing performance, and finds that most commonly used SAEs have too low L0.

## Strengths

- **Clear and important research question**: The paper addresses a fundamental hyperparameter choice in SAE training that has been largely overlooked. Showing that L0 is not a free parameter and that incorrect L0 leads to incorrect features is a significant contribution to the interpretability community.
- **Well-designed toy model experiments**: The toy models provide ground-truth knowledge of underlying features, allowing the authors to conclusively demonstrate the feature mixing phenomenon at both low and high L0. The sparsity-reconstruction tradeoff plot (Figure 4) is particularly compelling, showing that a ground-truth SAE can be outperformed on reconstruction by an incorrect SAE.
- **Practical proxy metric**: The decoder pairwise cosine similarity (c_dec) is intuitive, simple to compute, and validated on both toy models and LLMs. The correlation with sparse probing performance (Figures 8 and 9) provides strong evidence that c_dec can guide L0 selection in practice.
- **Thorough experimental validation**: The paper validates findings across two SAE architectures (BatchTopK and JumpReLU), two LLMs (Gemma-2-2b and Llama-3.2-1b), and multiple layers. The JumpReLU experiments showing that L0 "sticks" near the correct value are an interesting additional insight.
- **Clear implications for practitioners**: The paper directly addresses the common practice of using low L0 SAEs and provides actionable guidance for setting L0 correctly.

## Weaknesses

### Fatal
None.

### Major
- **c_dec metric is not a perfect guide**: The authors acknowledge that c_dec can remain nearly flat over a wide L0 range (e.g., Gemma-2-2b layer 5 in Figure 8), and the global minimum does not always coincide with the best L0. The "elbow" heuristic is somewhat ad-hoc and may require subjective judgment. The paper would benefit from a more principled way to identify the correct L0 from the c_dec curve, or a discussion of when the metric is reliable.
- **Requires expensive L0 sweep**: The proposed method for finding the correct L0 involves training a sweep of SAEs at different L0 values, which is computationally expensive (500M tokens per SAE in the LLM experiments). The paper mentions the possibility of optimizing c_dec during training (Appendix A.11) but does not implement or validate this, limiting immediate practical utility.

### Minor
- **Limited theoretical justification**: The formal theoretical justification for c_dec in Appendix A.6 is brief and relies on simplifying assumptions (e.g., orthogonal true features). A more rigorous analysis of why c_dec is minimized at the correct L0 would strengthen the paper.
- **Generalization to other SAE architectures**: The paper focuses on BatchTopK and JumpReLU SAEs. It is unclear whether the findings extend to other popular architectures like Gated SAEs or standard L1 SAEs. The authors mention L1 SAEs in the background but do not test them.
- **Claim about most SAEs having too low L0**: The evidence for this claim (Appendix A.13) is described as a "cursory search of open source SAEs on Neuronpedia." A more systematic survey or quantitative analysis would make this claim more convincing.

### Trivial
None.

## Nice-to-Haves

- A method to automatically optimize c_dec during training (as suggested in Appendix A.11) would greatly increase the practical impact of the paper.
- Experiments on more diverse LLMs (e.g., larger models, different architectures) would strengthen the generality of the findings.
- A comparison of c_dec with other potential metrics (e.g., based on encoder activations or reconstruction residuals) could provide a more comprehensive guide for L0 selection.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the sparsity-reconstruction tradeoff, which is the standard evaluation paradigm for SAEs, can be actively misleading: an SAE that mixes correlated features can achieve better reconstruction than a ground-truth SAE at the same L0. This means that reconstruction quality alone is insufficient to judge SAE quality, and that the field's reliance on these tradeoff plots may have led to the adoption of SAEs with incorrect features. The paper also provides a concrete mechanism (feature hedging due to insufficient L0) that explains why low-L0 SAEs underperform on downstream tasks, connecting the dots between earlier observations of degraded performance and the underlying cause.

## Suggestions

- Provide a more detailed analysis of when c_dec is reliable vs. when it is flat, and offer guidelines for practitioners on how to interpret the curve (e.g., use the elbow rather than the global minimum, and cross-validate with sparse probing if possible).
- Implement and evaluate the automatic optimization of c_dec during training, or at least provide a more detailed roadmap for how this could be done.
- Include experiments with L1 SAEs or Gated SAEs to demonstrate that the findings generalize beyond BatchTopK and JumpReLU.

## Score and Decision

Score: 8

Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>