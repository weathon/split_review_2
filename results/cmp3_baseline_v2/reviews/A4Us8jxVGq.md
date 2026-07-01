## Summary

This paper studies how semantic associations (e.g., "bird"→"flew") emerge during training of attention-based transformers on natural language. Using a gradient leading-term approximation, the authors derive closed-form expressions for weight matrices (output, value, query-key, positional) as compositions of three corpus-level basis functions: bigram mapping, interchangeability mapping, and context mapping. Experiments on a small 3-layer transformer (TinyStories) and the larger Pythia-1.4B model show high cosine similarity between theoretical predictions and learned weights, especially during early training, suggesting the theory captures key aspects of how semantic associations form.

## Strengths

- **Realistic theoretical setting.** Unlike prior theoretical works that assume synthetic languages or simplified architectures (no positional encodings, no causal masking, no residual streams), this paper analyzes transformers with positional encodings, causal masking, and residual connections trained on natural language data—substantially narrowing the gap between theory and practice.
- **Novel closed-form characterization of weights.** The gradient leading-term analysis yields explicit expressions for the output, value, query-key, and positional matrices as simple functions of bigram statistics, token co-occurrence, and their compositions. This is a significant step toward mechanistic interpretability grounded in training dynamics.
- **Convincing experimental validation across scales.** The theory is verified on a 3-layer attention-only model (TinyStories) with near-perfect cosine similarity (>0.99), and on Pythia-1.4B (which includes MLPs and multi-head attention) using covariance-based comparisons that show strong agreement early in training, with interpretable patterns across layers and training steps.
- **Clear interpretability of the basis functions.** The three basis functions (bigram, interchangeability via Σ\_B̄, context via Φ̄) are intuitive and linguistically meaningful, as demonstrated by concrete token examples (e.g., "fish" correlated with "pond", "lake"; pronouns grouped under interchangeability). This provides a tangible understanding of what each weight component captures.

## Weaknesses

### Major

No fatal weaknesses. The paper is methodologically sound and its claims are well-supported by the evidence presented.

### Minor

- **Early-training limitation is inherent but underdiscussed.** The theoretical guarantee holds only for a bounded number of gradient steps (s ≤ O(1/η)). While experiments show the approximation remains informative much longer, the paper does not analyze *why* it persists beyond the guaranteed regime or characterize the conditions under which it eventually breaks down. A discussion of this limitation and potential failure modes would strengthen the paper.
- **Pythia experiments use covariance proxies, not direct weight comparisons.** Because Pythia uses multi-head attention and MLPs, the authors compare covariance matrices of token embeddings (derived from the model's representations) with those of the theoretical leading-term matrices. This is a reasonable and necessary adaptation, but it is indirect—the connection between the theoretical weight characterizations and the observed embedding correlations relies on assumptions (e.g., about the effect of the residual stream and layer normalization) that are not fully formalized.
- **The per-head attention analysis (Figure 7) is descriptive rather than explanatory.** The figure shows that different layers and heads evolve at different rates relative to the leading-term prediction, but the paper offers no deeper analysis of *why* layer 2 behaves differently from layer 13, or what drives head specialization. This feels like an under-exploited observation.
- **The "interchangeability mapping" (Σ\_B̄ = B̄^T B̄) is simply a Gram matrix of bigram statistics.** Its interpretation as capturing functional interchangeability is plausible and supported by examples, but the paper does not rigorously connect this matrix to linguistic notions of synonymy or grammatical role similarity beyond the heuristic in Eq. (10).

### Trivial

None.

## Nice-to-Haves

- A more detailed theoretical or empirical characterization of when and why the leading-term approximation begins to degrade (e.g., at what training step and under what data properties).
- An analysis of how the three basis functions combine across multiple layers to produce more complex behaviors (e.g., induction heads), linking the current single-step leading-term results to known emergent phenomena.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight is that the early-stage training dynamics of transformers on natural language reduce to a small set of interpretable corpus statistics that compose in a transparent way across weight matrices. The output matrix learns a bigram mapping; the value matrix learns a product of context and bigram mappings; and the query-key matrix learns a higher-order interaction based on interchangeability and context. This suggests that the first phase of learning in transformers is essentially a "corpus statistics encoding" phase, where the model internalizes the most salient distributional properties of the training data in a predictable and decomposable manner—providing a concrete starting point for understanding later, more complex representational changes.

## Suggestions

- Add a discussion section that explicitly addresses the limitations of the early-time approximation and speculates on how later training phases (where higher-order gradient corrections dominate) might build upon or modify the semantic associations established early on.
- For the per-head analysis, compute the cosine similarity of each head's attention covariance with the theoretical Q̄ *separately* for early, middle, and late layers, and provide a hypothesis about the observed specialization patterns (e.g., do later layers diversify because they receive different inputs from earlier layers?).

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>