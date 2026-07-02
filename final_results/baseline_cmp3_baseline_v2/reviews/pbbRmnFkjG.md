## Summary

This paper presents a large-scale interpretability analysis of DINOv2 using a stable sparse autoencoder (RA-SAE) to extract a 32,000-concept dictionary. The authors analyze how downstream tasks (classification, segmentation, depth estimation) recruit different concept subsets, revealing functional specialization including "Elsewhere" concepts for classification, border concepts for segmentation, and monocular cue families for depth. Based on observed departures from the Linear Representation Hypothesis (LRH)—including higher coherence than expected, sharp spectral decay, and dense positional features—the authors propose the Minkowski Representation Hypothesis (MRH), where tokens are Minkowski sums of convex polytopes around archetypal landmarks, and show that multi-head attention naturally implements this construction.

## Strengths

- **Scale and methodological rigor**: The paper presents what appears to be the largest interpretability demonstration for a vision foundation model (32,000 concepts), using a stable SAE variant (RA-SAE) that addresses reproducibility issues common in prior SAE work. The dictionary is released as an interactive visualization, which is a valuable community resource.

- **Novel empirical findings**: The discovery of "Elsewhere" concepts for classification (conditional negation), the identification of three distinct monocular cue families for depth estimation (projective, shadow-based, frequency transitions), and the systematic characterization of departures from LRH (higher coherence, sharp spectral decay, dense positional features) are genuinely interesting and well-supported by the experiments.

- **Theoretical contribution**: The Minkowski Representation Hypothesis is a novel and principled alternative to the linear sparse-coding view. The connection to multi-head attention (Proposition 1) is elegant and mechanistically grounded, showing that attention heads naturally produce convex combinations that sum to Minkowski sums. The non-identifiability result (Proposition 2) is a useful cautionary note for interpretability practitioners.

## Weaknesses

### Major

- **The MRH is presented as a "working hypothesis" but the empirical evidence for it is thin relative to the claims.** The paper provides only three preliminary tests (straight-line vs. piecewise-linear geodesics, Archetypal Analysis vs. SAE reconstruction, and Gram block structure), all on ImageNet-1k tokens. These are suggestive but far from conclusive. The paper would benefit from more direct tests: e.g., verifying that token embeddings actually lie in the predicted Minkowski sum of head polytopes, or demonstrating that the block-convex code structure is recoverable from attention weights.

- **The relationship between the SAE-based analysis (Sections 2-4) and the MRH (Section 6) is unclear.** The paper uses SAEs to extract concepts under the LRH framework, then argues that LRH is insufficient and proposes MRH as an alternative. However, it never reconciles the two: are the SAE-discovered concepts compatible with MRH? If concepts are regions rather than directions, what do the SAE atoms represent? The paper would be stronger if it explicitly addressed how the SAE dictionary relates to the proposed archetype set in MRH.

- **The "Elsewhere" concept analysis for classification lacks rigorous causal validation.** The paper claims these concepts implement "conditional negation" and provides evidence via causal masking, but the description is brief and the mechanism is unclear. The alternative interpretation ("distributed off-object evidence") is mentioned but not properly addressed. Stronger causal evidence (e.g., intervention studies showing that modifying these concepts changes classification decisions in predictable ways) would significantly strengthen this claim.

### Minor

- **The paper's structure is somewhat disjointed.** It reads as three separate studies (task-specific usage, concept geometry, MRH) rather than a unified narrative. The transition from the SAE-based analysis to the MRH is abrupt, and the connection between the two parts could be better motivated.

- **The depth cue analysis (Figure 3) is qualitative.** While the identification of three cue families is interesting, the perturbation analysis is described briefly and the clustering is based on UMAP, which is known to distort global structure. Quantitative validation (e.g., showing that the identified clusters predict depth estimation performance under specific perturbations) would strengthen this analysis.

- **The paper claims the dictionary is "the largest interpretability demonstration for a vision foundation model to date" but does not compare to prior work in terms of scale or quality.** How does 32,000 concepts compare to existing SAE-based analyses of vision models? What is the reconstruction fidelity relative to other methods?

### Trivial

- The paper uses "concept" to refer to SAE dictionary atoms, which is a reasonable operationalization but could be confused with the broader notion of concepts in cognitive science. A brief clarification would help.

## Nice-to-Haves

- A more systematic comparison between the SAE dictionary and the proposed MRH archetype set would strengthen the paper's coherence. For example, do the SAE atoms correspond to vertices of the head polytopes in MRH?
- The paper could benefit from a discussion of how the MRH relates to other geometric frameworks for representation learning, such as hyperbolic embeddings or simplicial complexes.
- The interactive visualization (mentioned as released upon acceptance) would be a valuable resource; including a screenshot or description of its capabilities would help readers appreciate its utility.

## Novel Insights

The paper's most novel insight is the observation that DINOv2's representation space departs systematically from the idealized sparse, near-orthogonal picture of the Linear Representation Hypothesis, and that these departures—higher coherence, sharp spectral decay, dense positional features, and smooth per-image token geometry—are naturally explained by a Minkowski sum of convex polytopes. The connection between multi-head attention and Minkowski sums is elegant and provides a mechanistic foundation for the hypothesis. The non-identifiability result (Proposition 2) is a valuable caution: if MRH holds, then interpreting representations from final activations alone is fundamentally underdetermined, which has practical implications for the design of interpretability tools.

## Suggestions

1. Strengthen the empirical evidence for MRH by providing more direct tests: verify that token embeddings lie in the predicted Minkowski sum of head polytopes, or demonstrate that the block-convex code structure is recoverable from attention weights.
2. Clarify the relationship between the SAE-based analysis and MRH: are the SAE-discovered concepts compatible with MRH? If so, how? If not, what do they represent?
3. Provide stronger causal validation for the "Elsewhere" concept analysis, e.g., by showing that modifying these concepts changes classification decisions in predictable ways.
4. Add quantitative validation for the depth cue clustering, e.g., by showing that the identified clusters predict depth estimation performance under specific perturbations.

## Score and Decision

The paper makes a solid contribution to interpretability of vision transformers, with a large-scale dictionary, interesting empirical findings about task-specific concept usage, and a novel theoretical hypothesis (MRH) that is mechanistically grounded. However, the empirical support for MRH is preliminary, and the relationship between the two main parts of the paper (SAE analysis and MRH) is not fully resolved. The paper is above the acceptance threshold but has room for improvement.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Accept</decision>