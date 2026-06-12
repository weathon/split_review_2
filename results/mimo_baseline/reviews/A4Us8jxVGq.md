## Summary

This paper develops a gradient leading-term analysis of training dynamics for attention-based transformers trained on natural language, showing that the early-stage learned weights can be expressed as closed-form compositions of three interpretable basis functions: bigram mapping, interchangeability mapping, and context mapping. The authors validate their theoretical weight characterizations both in a controlled 3-layer attention-only transformer on TinyStories (cosine similarity >0.99) and in Pythia-1.4B, demonstrating that the theory captures real features learned by practical LLMs.

## Strengths

- **Rigorous closed-form characterization under realistic assumptions.** Unlike prior works that rely on synthetic data, simplified architectures, or non-standard training, this paper analyzes transformers with causal masking, relative positional encodings, residual streams, cross-entropy loss, and standard gradient descent on natural language. The resulting Theorem 4.1 provides explicit Frobenius norm bounds relating each weight matrix to corpus statistics, valid for O(1/η) gradient steps with L layers.

- **Empirical validation at scale is convincing.** The cosine similarity between theoretical and learned weights exceeds 0.999 for all matrices in the controlled setting (Table 1) and remains above 0.9 for 30+ epochs. More importantly, the Pythia-1.4B analysis (Figure 6) shows strong agreement between theoretical features and actual model representations across all layers at early training stages, demonstrating generalizability beyond attention-only architectures.

- **Interpretable basis function decomposition.** The identification of three basis functions—bigram, interchangeability (token functional similarity via previous-token distribution overlap), and context (prefix-suffix co-occurrence)—provides a principled vocabulary for understanding what semantic features transformers learn. The qualitative examples in Figure 5 show these capture meaningful linguistic structure (e.g., "fish" → "pond"/"lake" under context mapping).

- **End-to-end analysis of weight cooperation.** Equation (12)-(13) show how all weight matrices collaborate: the residual stream provides bigram predictions while the attention block refines predictions by attending to tokens most predictive of the next-token distribution. This compositional view goes beyond analyzing individual weights in isolation.

## Weaknesses

### Fatal

None.

### Major

- **Narrow validity regime.** The theorem requires s ≤ η⁻¹ min(5/(8√T), 1/(12L)), which limits the analysis to a small number of gradient steps relative to convergence. While the authors argue early training is empirically important and show the cosine similarity remains high beyond this regime, the theory itself makes no formal guarantees about when or why the leading-term approximation breaks down, and what the higher-order terms capture semantically. This limits the mechanistic utility—the theory tells us what happens initially but not how these features evolve or are refined.

- **Architecture gap between theory and Pythia.** The theoretical model is attention-only with a single head and |V|×|V| weight matrices, while Pythia-1.4B has MLPs, multi-head attention (32 heads), and low-dimensional residual streams. The empirical bridge relies on projecting through embeddings and comparing covariance matrices, which is reasonable but indirect. The MLP ablation (Section 5.2) hints that MLPs may function similarly to the value mapping, but this is speculative and not derived from theory.

### Minor

- **The comparison methodology for Pythia is somewhat coarse.** Cosine similarity of covariance matrices across layers and training steps (Figure 6) provides aggregate agreement but does not reveal which specific token associations are preserved versus lost. A more fine-grained analysis (e.g., comparing top-k correlations for specific tokens) would strengthen the practical relevance claim.

- **The model architecture omits LayerNorm.** Standard transformers use layer normalization, which affects gradient dynamics. The paper does not discuss how LayerNorm interacts with the leading-term approximation, and Pythia includes it, adding another source of theory-practice gap.

- **Early-stage bigram learning is relatively unsurprising.** The observation that output weights approximate bigram statistics and that early features capture shallow co-occurrences is somewhat expected given the loss function and initialization. The contribution is more in the *precision and explicitness* of the characterization than in the qualitative finding.

### Trivial

None.

## Nice-to-Haves

- A discussion of when and why the leading-term approximation breaks down, even qualitative, would significantly increase the paper's mechanistic utility.
- Analysis of how the theoretical features at early stages relate to downstream task performance (e.g., do models whose early weights better match the theory also perform better at later stages?).
- Extension to multi-head attention, even at the level of averaging across heads within the theoretical framework.

## Novel Insights

The most novel insight is the precise decomposition of all four weight matrices (output, value, query-key, positional encoding) into compositions of exactly three basis functions derived from corpus statistics, with the interchangeability mapping (Σ_B̄ = B̄ᵀB̄) being particularly interesting as it captures functional similarity between tokens via previous-token distribution overlap—an interpretable proxy for word-sense similarity. The finding that this single matrix family characterizes weights *uniformly across all layers* at early stages is also noteworthy, suggesting all layers start from a common representational basis before diverging. The Pythia analysis showing that intermediate layers specialize faster than early or late layers (Figure 7) provides a useful empirical observation about the progression of feature learning.

## Suggestions

- Provide a formal characterization (even a conjecture with empirical support) of the transition regime where weights begin to deviate from leading terms, as this would bridge the gap between the early-stage theory and the practical question of how semantic features persist through full training.
- Add token-level comparisons for Pythia (e.g., which specific associations are captured by theoretical vs. learned representations) to make the practical relevance more tangible.
- Consider discussing the relationship between the context mapping Φ̄ and established distributional semantics representations (e.g., PMI-based word embeddings), as this would connect the theoretical framework more directly to the NLP literature.

## Score and Decision

The paper makes a solid theoretical contribution with explicit closed-form characterizations of transformer weights under realistic assumptions, supported by strong empirical validation in both controlled and practical settings. The three-basis-function decomposition is clean and interpretable. The main limitation is the narrow validity regime and the architecture gap for practical LLMs, which temper the mechanistic utility. The work is a meaningful advance over prior theoretical analyses of transformer training dynamics, though its practical impact is constrained by the early-stage focus.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>