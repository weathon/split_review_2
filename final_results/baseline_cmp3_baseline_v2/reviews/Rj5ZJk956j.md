## Summary
This paper introduces a mechanistic interpretability method for gated neurons in transformers based on cosine similarities between input (reading) and output (writing) weight vectors. Applying this method to nine LLMs, the authors discover a class of "weakening" neurons that are few in number but activate frequently and have outsized influence on model behavior, particularly through negative gate values—a mechanism previously unexplored. The paper also introduces conditional ablation to isolate which activations drive specific behaviors.

## Strengths
- **Novel and simple method with striking results**: The cosine-similarity-based read-write analysis is elegantly simple yet reveals universal cross-model patterns (strengthening in early layers, weakening in late layers) that are non-obvious and empirically robust across nine diverse LLMs.
- **Discovery of a functionally important neuron class**: The identification of weakening neurons as a small but disproportionately influential class is a genuine contribution. The finding that negative gate values (previously considered only relevant for training dynamics) encode meaningful functionality is novel and challenges common assumptions about SwiGLU activations.
- **Conditional ablation as a methodological contribution**: The conditional ablation technique (ablating only activations with specific sign patterns of gate and input) is a useful tool for mechanistic analysis that goes beyond standard ablation and could be applied more broadly.
- **Thorough empirical validation**: The paper validates its claims across multiple models (9+ LLMs), uses appropriate baselines (random neurons from same layers), and provides both quantitative (entropy, attribute rate) and qualitative (case studies) evidence.

## Weaknesses
### Fatal
None.

### Major
- **Limited mechanistic depth**: The paper identifies that weakening neurons exist and are influential, but does not provide a mechanistic explanation of *how* they implement their function. The case study (neuron 31.9634) is acknowledged as "much harder to interpret" and the most interpretable activations are weak. The claim that weakening neurons "work together in superposition" is speculative and unsupported. The paper would be stronger with a more concrete mechanistic account or a clearer articulation of what "weakening" means functionally beyond the weight cosine similarity.
- **The "weakening" label may be misleading**: The paper defines weakening as cos(w_in, w_out) < -0.5, but the actual functional effect of these neurons depends on the sign of the gate and input activations. As shown in section 6.2, when x_gate < 0, weakening neurons can *strengthen* directions. The paper acknowledges this but the terminology and framing (e.g., "weakening neurons have outsized influence") may overstate the specificity of the class. A more precise functional characterization is needed.
- **Single model for ablation experiments**: All ablation experiments are conducted on OLMo-7B only. While the weight-based analysis is cross-model, the critical behavioral claims (outsized influence, negative gate value mechanism) are only tested on one model. This weakens the generality of the claims, especially given that the paper emphasizes universal patterns.

### Minor
- **The taxonomy in Table 1 is somewhat arbitrary**: The threshold of ±0.5 for cosine similarity is reasonable but not well-justified. The paper acknowledges that many neurons fall between these thresholds, and the "atypical" subcategories add complexity without clear benefit. A continuous analysis (e.g., scatter plots) seems more informative than the discrete classification.
- **Activation frequency analysis (Section 7) is underdeveloped**: The finding that weakening neurons activate more frequently is interesting but the analysis is limited to a single layer (Layer 15) and a single model. The paper mentions "other results in Section J" but these are in the appendix and not discussed in the main text. The correlation with Gurnee et al. (2024) is noted but not deeply explored.

### Trivial
- The paper uses "weakening" to describe both a neuron class (based on weight cosines) and a functional effect (reducing a direction in the residual stream). This dual usage could cause confusion.

## Nice-to-Haves
- A more detailed mechanistic analysis of how weakening neurons interact with attention heads or other MLP neurons to produce their effects.
- Testing the ablation results on at least one additional model (e.g., Llama-3.2-3B) to confirm the generality of the behavioral findings.
- A clearer explanation of why negative gate values produce the observed sharpening effect, perhaps with a toy example or mathematical derivation.

## Novel Insights
The paper's most novel insight is that negative gate values in SwiGLU activations—previously dismissed as artifacts of training dynamics—can encode meaningful functionality. This challenges the common practice of treating Swish as a smooth ReLU and suggests that mechanistic interpretability of gated architectures must account for the full range of gate values. The discovery that a small number of weakening neurons (defined by weight cosine similarity) have outsized influence on model behavior is also genuinely novel, though the mechanistic basis for this influence remains unclear.

## Suggestions
- Strengthen the mechanistic account of weakening neurons. What specific computational role do they play? Are they implementing a form of error correction, normalization, or something else?
- Validate the ablation results on at least one additional model to support the claim of universality.
- Consider renaming "weakening" to something more neutral (e.g., "negative-cosine neurons") to avoid implying a specific functional role that may not always hold.

## Score and Decision
The paper presents a novel, simple, and empirically grounded method that reveals genuinely surprising patterns across multiple LLMs. The discovery of weakening neurons and the role of negative gate values are significant contributions to mechanistic interpretability. However, the paper's main weakness is the lack of mechanistic depth: it identifies *that* weakening neurons are important but does not convincingly explain *how* they work. The single-model ablation experiments also limit the generality of the behavioral claims. Despite these limitations, the paper's contributions are substantial and well-supported within their scope.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>