## Summary

This paper develops a theoretical framework for understanding how semantic associations emerge in attention-based transformers during training on natural language data. By analyzing gradient leading terms at early training stages, the authors derive closed-form expressions for transformer weights as compositions of three basis functions: bigram mapping, interchangeability mapping, and context mapping. The theory is validated on both a 3-layer attention-only transformer trained on TinyStories and on the practical Pythia-1.4B model trained on OpenWebText, showing strong cosine similarity between theoretical predictions and learned weights.

## Strengths

- **Novel theoretical contribution with practical relevance**: The paper provides the first explicit closed-form characterization of transformer weights trained on real natural language data (not synthetic languages) under standard training procedures, significantly reducing the gap between theory and practice compared to prior work that relied on unrealistic assumptions.

- **Elegant decomposition into interpretable basis functions**: The identification of bigram, interchangeability, and context mappings as building blocks that compose to form all weight matrices is conceptually clean and provides genuine mechanistic insight into how transformers learn associations.

- **Strong empirical validation across scales**: The theory is validated on a small controlled transformer (cosine similarities >0.99) and extended to Pythia-1.4B, a practical LLM with multi-head attention and MLPs, demonstrating that the theoretical features persist even beyond the theoretical assumptions.

- **Per-head analysis provides additional insight**: Figure 7's analysis of individual attention heads across layers reveals differential specialization rates, showing the theory can serve as a tool for understanding model internals beyond just matching aggregate statistics.

## Weaknesses

### Major

- **The theoretical results rely on an extremely small learning rate regime that may not reflect practical training**: Theorem 4.1 requires η ≥ 1/T (e.g., η ≥ 0.005 for T=200) and s ≤ η^{-1} * min(5/(8√T), 1/(12L)). For T=200 and L=3, this gives s ≤ η^{-1} * 0.022. With η=0.005, this allows only ~4.4 steps. The paper's own experiments use 100 epochs with batch size 2048, which is far more steps than the theory guarantees. While the empirical results hold, the theoretical justification for why the approximation remains valid beyond the proven regime is not provided.

- **The connection between the theoretical weight characterizations and actual model behavior is indirect**: The paper shows that weight matrices match theoretical predictions, but does not demonstrate that the *computation* or *outputs* of the model are well-described by the theory. Showing that weights have high cosine similarity to theoretical matrices does not guarantee that the model's behavior (e.g., attention patterns, predictions) is governed by the claimed semantic associations. A more direct behavioral validation (e.g., probing attention patterns, analyzing model predictions) would strengthen the claims.

- **The Pythia experiments compare covariance matrices rather than the weights themselves**: Because Pythia has different dimensions and multi-head attention, the authors compare covariance matrices of embeddings rather than the weight matrices directly. This is a reasonable adaptation, but it weakens the directness of the validation. The covariance comparison could be driven by shared statistical properties of the data rather than the specific theoretical mechanism claimed.

### Minor

- **The paper does not discuss how the three basis functions interact with the residual stream**: The analysis focuses on individual weight matrices, but the residual connection (h^{(l-1)} added in Eq. 2) plays a crucial role in how information flows. The end-to-end analysis in Section 4.2.3 is brief and does not fully account for how residual connections affect the composition of features across layers.

- **The "interchangeability mapping" terminology could be misleading**: The mapping Σ_Ḃ captures similarity of previous-token distributions, which is a statistical property that may correlate with but is not equivalent to semantic interchangeability. The paper acknowledges this implicitly but the terminology may overclaim the semantic nature of the feature.

### Trivial

- The paper uses "leading term" and "leading-order approximation" somewhat interchangeably without precisely defining the expansion being truncated.

## Nice-to-Haves

- A behavioral validation experiment where the theoretical weight characterizations are used to predict model outputs on specific semantic association tasks (e.g., "bird" → "flew" completion) would significantly strengthen the mechanistic interpretability claims.
- An analysis of how quickly the theoretical approximation degrades as training progresses, with error bounds that could be checked empirically.
- A discussion of whether the three basis functions are sufficient to characterize all semantic associations or whether higher-order interactions are needed for more complex relationships.

## Novel Insights

The paper's key insight is that the training dynamics of transformers on natural language can be understood through a gradient expansion where the leading terms decompose into interpretable corpus statistics. This is genuinely novel because prior theoretical work either required synthetic data or simplified architectures. The finding that all layers learn the same associative features early in training (before specializing) provides a concrete mechanistic hypothesis for how semantic knowledge is first acquired. The composition structure—where bigram, interchangeability, and context mappings combine multiplicatively across weight matrices—offers a principled way to think about how different components of a transformer contribute to semantic understanding. This framework could serve as a foundation for more detailed mechanistic interpretability studies, as it provides explicit mathematical targets for what features should be present in trained models.

## Suggestions

- Add a behavioral validation experiment: freeze the model at an early checkpoint, replace the weights with the theoretical leading-term approximations, and measure whether the model's predictions on semantic association tasks are preserved. This would directly test whether the weight similarity translates to functional similarity.
- Provide a more precise characterization of when the gradient leading-term approximation breaks down, perhaps with empirical measurements of the higher-order terms.
- Clarify in the main text the number of steps for which the theory is guaranteed to hold under the given learning rates, and discuss why the empirical results hold for much longer.

## Score and Decision

The paper makes a significant theoretical contribution by providing the first closed-form characterization of transformer weights trained on natural language data, with clear interpretable structure. The empirical validation is thorough across both controlled and practical settings. The major weakness is the gap between the theoretical guarantees (which hold for very few steps) and the empirical validation (which extends much further), but this is partially mitigated by the strength of the empirical results. The paper opens a promising direction for mechanistic interpretability grounded in training dynamics.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>