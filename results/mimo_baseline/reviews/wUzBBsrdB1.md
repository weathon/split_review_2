## Summary

This paper investigates the effect of the L0 hyperparameter (average number of active SAE features per token) on Sparse Autoencoders used for LLM interpretability. The authors demonstrate through toy models and LLM experiments that L0 is not a free parameter: too-low L0 causes SAEs to mix correlated features into latents (feature hedging), while too-high L0 produces degenerate solutions, and they propose a decoder pairwise cosine similarity metric (c_dec) to help identify the correct L0.

## Strengths

- **Compelling core insight with broad practical impact.** The paper convincingly argues that the common practice of treating L0 as a free parameter in "sparsity-reconstruction tradeoff" plots is fundamentally flawed. The demonstration that a ground-truth SAE achieves *worse* reconstruction than an incorrect SAE at low L0 (Figure 4) is a striking and well-supported result that challenges standard evaluation methodology across the field.

- **Well-designed toy model experiments with clear causal evidence.** The toy model setup is clean and the experiments are carefully controlled. Initializing the low-L0 SAE to the ground-truth solution (Section 3.1) and showing it still converges to mixed features provides strong evidence that gradient pressure from MSE loss, not just local minima, drives the feature mixing. The positive/negative correlation experiments (Figures 2-3) clearly demonstrate the mechanism.

- **Validation on real LLMs with external downstream metrics.** The paper trains SAEs on Gemma-2-2b and Llama-3.2-1b and validates the c_dec metric against sparse probing performance (Figure 8), providing evidence that the toy model findings transfer to real settings. The comparison between JumpReLU and BatchTopK SAEs (Section 4.1) adds useful nuance.

- **Clear and well-structured writing.** The paper builds its argument methodically from toy models to LLM experiments, and the figures are informative and well-chosen.

## Weaknesses

### Fatal
None.

### Major

- **The c_dec metric has significant practical limitations.** In the Gemma-2-2b layer 5 results (Figure 8, top-left), c_dec is essentially flat over a wide range of L0 values (roughly 200-2000), making it difficult to pinpoint the correct L0 in practice. The paper acknowledges this but doesn't fully address it. The metric reliably detects when L0 is *clearly too low* (the sharp elbow), but its utility for fine-tuning L0 in the regime that matters most is limited. This weakens the paper's practical contribution of a "proxy metric."

- **Limited LLM scale.** The LLM experiments use only relatively small models (2B and 1B parameters). Given that SAEs are widely used on much larger models (7BB+), and that the feature correlation structure may differ substantially at scale, the generalizability of these findings to larger models remains uncertain.

- **The "correct L0" concept is underspecified for real LLMs.** The paper assumes a single correct L0 exists, but real LLM features likely have heterogeneous firing rates, and the "true L0" is an average over a distribution. Section 4.2 touches on this (some latents may be too high while others are too low simultaneously), but the paper doesn't fully grapple with the implications. If different layers or different feature subsets have different optimal L0 values, the practical guidance becomes less clear.

### Minor

- **Sparse probing as the sole LLM validation metric.** The paper relies exclusively on k-sparse probing F1 to validate the c_dec metric on LLMs. Other downstream tasks (e.g., steering, causal intervention, circuit analysis) might have different optimal L0 values, and the paper doesn't explore this.

- **The JumpReLU "sticking" behavior is interesting but underexplored.** The observation that JumpReLU SAEs naturally converge to the correct L0 across a wide range of λ_s (Section 3.6) is potentially very important but receives only a brief mention. Understanding why this happens could be more valuable than the c_dec metric itself.

### Trivial
None.

## Nice-to-Haves

- A comparison of c_dec with other potential metrics (e.g., MDL-based approaches) on the same LLM experiments would strengthen the paper's practical recommendations.
- Analysis of how the optimal L0 varies across layers within the same model would provide more actionable guidance for practitioners.
- Discussion of whether the "correct L0" might differ depending on the downstream use case (interpretability vs. steering vs. probing).

## Novel Insights

The paper's most novel contribution is the demonstration that the sparsity-reconstruction tradeoff, a standard evaluation tool in the SAE literature, is actively misleading: at low L0, an SAE with the correct dictionary achieves worse reconstruction than an incorrect SAE that mixes correlated features. This is a genuinely important methodological critique that, if taken seriously, would change how the field evaluates SAE architectures. The observation that feature hedging occurs for both positively and negatively correlated features, meaning *every* latent in a low-L0 SAE is corrupted, is also a strong and somewhat surprising finding.

## Suggestions

- The c_dec metric's flat region could potentially be addressed by computing it on a per-latent basis and looking at the distribution rather than just the mean, or by combining it with the decoder projection histogram approach from Section 4.2 into a composite metric.
- The paper would benefit from a concrete practical recommendation: given the c_dec curve, what specific procedure should a practitioner follow to choose L0? The current guidance ("look for the elbow") is somewhat vague.
- Investigating whether the JumpReLU "sticking" behavior can be leveraged to automatically find the correct L0 during training (rather than post-hoc via c_dec) would be a high-impact extension.

## Score and Decision

The paper presents a clear, well-supported argument that L0 is not a free parameter in SAE training, with convincing toy model evidence and reasonable LLM validation. The critique of sparsity-reconstruction tradeoff plots is an important methodological contribution. The c_dec metric, while limited in practice, provides useful guidance. The main weaknesses are the metric's flat regions limiting its practical utility and the limited scale of LLM experiments, but these don't invalidate the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>