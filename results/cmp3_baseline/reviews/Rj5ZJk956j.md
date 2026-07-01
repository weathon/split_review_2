## Summary

This paper introduces a novel mechanistic interpretability method for gated neurons (SwiGLU/GeGLU) based on the cosine similarities between their input (w_gate, w_in) and output (w_out) weight vectors. Using this weight-based perspective, the authors discover a class of "weakening neurons" (negative cos(w_in, w_out)) that appear predominantly in late layers, activate extremely often, and have a disproportionately large impact on model behavior when ablated. The paper also introduces "conditional ablation" to isolate the effect of different activation regimes and shows that negative gate values—previously thought to be only a training artifact—play a functional role in these weakening neurons.

## Strengths

- **Novel and simple weight-based approach**: Using cosine similarities between weight vectors to analyze gated neurons is methodologically simple yet reveals non-obvious structure. This contrasts with activation-based methods and provides a complementary perspective that is computationally cheap to compute.
- **Surprising discovery with cross-model validity**: The identification of weakening neurons and their distinctive properties (high activation frequency, outsized ablation impact, late-layer concentration) is genuinely interesting. The pattern holds across 12 different LLMs (including OLMo, Llama, Gemma, Mistral, Qwen, Yi), suggesting a fundamental property of gated architectures.
- **Conditional ablation as a useful technique**: The method of ablating only subsets of activations based on the signs of x_gate and x_in is a simple but powerful tool for attributing effects to specific regimes, and it convincingly demonstrates that negative gate values contribute meaningfully to model behavior.
- **Clear and well-structured exposition**: The paper is generally well-written, with intuitive explanations of the taxonomy, figures that support the main claims, and a clear narrative from method discovery to ablation experiments to case studies.

## Weaknesses

### Fatal

None.

### Major

- **Ablation results may conflate activation frequency with neuron class**: The paper shows that weakening neurons have the largest effect when zero-ablated, and notes they activate very often (Section 7). However, the baseline (random neurons from the same layers) is not matched for activation frequency. High-frequency neurons trivially have larger effects under zero ablation. Without controlling for activation frequency (e.g., by matching baselines on activation frequency or using mean ablation as the primary analysis), the claim that weakening neurons have "outsized influence" is not fully disentangled from their high firing rate. Mean ablation results are relegated to an appendix and not shown for the key metrics (attribute rate, entropy histograms).
- **Cosine similarity threshold is arbitrary**: The taxonomy uses τ = ±0.5 for classification into strengthening/weakening/conditional/etc. (Table 1, line "or > 0.5" etc.). The paper does not justify this threshold or show robustness to its variation. While the continuous analysis (median plots, scatter plots) is more robust, the categorical breakdown in Figure 1(b) and some ablation analyses rely on this threshold, and it is unclear whether the categories are stable under small perturbations.
- **Case study evidence is thin**: Section 8 presents only one strengthening neuron and one weakening neuron. The weakening neuron's behavior is described as "much harder to interpret" and the most interpretable activations are "weaker positive activations" in the negative gate case. This single example does not convincingly demonstrate that weakening neurons are systematically meaningful—only that one such neuron can sometimes be interpreted. More systematic evaluation (e.g., automatic interpretability scores, human evaluation across multiple weakening neurons) would strengthen the claim.

### Minor

- **Limited architectural scope**: The paper exclusively studies gated activation functions (SwiGLU, GeGLU). The findings are relevant for modern LLMs but the "universality" claim is confined to this family. The paper does not discuss whether similar phenomena might occur in ReLU/GeLU models (e.g., GPT-2) or how the method would generalize.
- **Overclaim on novelty of negative gate mechanism**: The paper claims to be "the first to observe a mechanism involving negative values of the Swish activation function" but acknowledges concurrent work (Kong et al., 2025) and the possibility of prior overlooked work. The novelty is marginal given that the importance of negative gating is known from the training dynamics literature, and the demonstration here is limited to one neuron and one text example.
- **Conditional ablation results could be better contextualized**: The entropy histograms (Figure 3b) show small absolute differences (<10 nats) on a log scale. While the effect is statistically distinct from baseline, its practical significance is unclear. The paper would benefit from connecting these entropy changes to downstream task performance.

### Trivial

None.

## Nice-to-Haves

- **Activation-frequency-matched ablation baselines**: Repeat the key ablation experiments (attribute rate, entropy) with a baseline set of random neurons selected to have the same average activation frequency as the weakening neurons in each layer.
- **Threshold robustness analysis**: Show that the qualitative patterns (e.g., Figure 1b) hold for different cosine similarity thresholds (e.g., 0.3, 0.7, or a continuous coloring).
- **Automated interpretability evaluation**: Apply a metric like logit-lens interpretability (Gurnee et al., 2024) to compare weakening vs. strengthening neurons systematically, rather than relying on a single case study.
- **Investigate whether weakening neurons are "error-correcting"**: The case study suggests weakening neurons may suppress premature predictions. The paper could test this hypothesis across more examples or tasks.

## Novel Insights

Beyond the paper's own contributions, the most novel insight is that the weight-based cosine similarity method reveals a clear "strengthening-then-weakening" pattern across layers in gated LLMs, which is universal across many models. This suggests that early layers build up evidence for certain directions, while later layers can subtract or weaken those directions—a plausible mechanistic story for iterative refinement. The additional insight that negative gate values in weakening neurons can effectively turn them into strengthening-like behavior (since Swish(x_gate < 0) is small and positive, and with x_in also negative the product becomes positive) is a subtle but clever observation that explains why ablation of those activations hurts performance. This challenges the oversimplified view that negative gate values are noise.

## Suggestions

1. **Address the activation frequency confound** by repeating the ablation experiments with a baseline matched on activation frequency, or by using mean ablation as the primary analysis and showing that the effect persists.
2. **Provide a robustness analysis** for the cosine similarity threshold, or use the continuous cosine value directly in ablation analyses to avoid arbitrary discretization.
3. **Expand the case study analysis** to include a small-scale systematic evaluation of interpretability across several weakening neurons (e.g., 10–20 neurons) using the same methods (projection to vocabulary, activation examples), to demonstrate that the observed interpretability is not an isolated fluke.

## Score and Decision

MY FINAL SCORE: <score>8</score>

MY FINAL DECISION: <decision>Accept</decision>