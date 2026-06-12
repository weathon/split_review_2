## Summary

This paper presents a large-scale interpretability analysis of DINOv2 using a stable sparse autoencoder (RA-SAE) to extract a 32,000-concept dictionary. The authors analyze how downstream tasks (classification, segmentation, depth estimation) recruit different concept subspaces, revealing functional specialization including "Elsewhere" concepts for classification, border detectors for segmentation, and monocular cue families for depth. Based on observed departures from the Linear Representation Hypothesis (LRH)—including higher coherence than expected, sharp spectral decay, and dense positional features—the authors propose the Minkowski Representation Hypothesis (MRH), where token embeddings are Minkowski sums of convex polytopes around archetypal landmarks, with multi-head attention naturally implementing this construction.

## Strengths

- **Scale and methodological rigor**: The paper presents the largest interpretability demonstration for a vision foundation model to date (32,000 concepts), with careful attention to SAE stability through the RA-SAE approach, achieving R² > 88% reconstruction fidelity. The dictionary is released as an interactive visualization tool.
- **Novel empirical findings**: The discovery of "Elsewhere" concepts for classification (conditional negation), the identification of three distinct monocular cue families in depth estimation (projective, shadow-based, frequency transitions), and the systematic characterization of departures from LRH are genuinely interesting and well-supported by the analysis.
- **Theoretical contribution**: The Minkowski Representation Hypothesis is a creative and well-motivated proposal that connects observed phenomena (convex combinations from attention, smooth token geometry, steering saturation) to a formal geometric framework. Proposition 1 showing that multi-head attention naturally realizes MRH is a clean theoretical result.
- **Comprehensive multi-level analysis**: The paper moves from task-level concept usage, through statistical and geometric properties of the dictionary, to per-image token geometry, and finally to a new representational hypothesis—providing a coherent narrative across scales of analysis.

## Weaknesses

### Major

- **The MRH is presented as a "working hypothesis" but the empirical evidence remains preliminary and somewhat thin.** The three empirical tests (straight-line vs. piecewise-linear geodesics, Archetypal Analysis vs. SAE reconstruction, Gram block structure) are suggestive but not conclusive. The AA comparison showing ~10 archetypes per image matching SAE reconstruction is interesting, but the paper does not systematically compare MRH against alternative geometric models (e.g., manifold learning baselines, hyperbolic embeddings, or other convex decomposition methods). The Gram block structure evidence (Figure 26, right) is mentioned but not quantitatively evaluated against baselines.
- **The paper overclaims the novelty of the MRH relative to existing work.** The observation that attention heads produce convex combinations and that multi-head outputs sum is well-known in the transformer literature. The connection to Gärdenfors' conceptual spaces and convex concept regions is acknowledged but the paper does not clearly delineate what is genuinely new in MRH versus a restatement of known properties of attention. The non-identifiability result (Proposition 2) is mathematically trivial given the properties of Minkowski sums and support functions.
- **The evaluation of task-specific concept usage lacks rigorous quantification.** The paper identifies "Elsewhere" concepts, border concepts, and monocular cue families through qualitative examination and UMAP visualization, but does not provide systematic metrics for how consistently these patterns appear across the full dataset, how many concepts belong to each family, or statistical tests for the significance of the observed specialization. The depth cue analysis using controlled perturbations is clever but the clustering into three families relies on visual inspection of UMAP projections rather than quantitative validation.

### Minor

- The paper would benefit from a more direct comparison between the SAE-based concept dictionary and alternative concept discovery methods (e.g., PCA, ICA, non-negative matrix factorization) to establish that the observed properties are not artifacts of the SAE training procedure.
- The analysis of concept geometry (Section 4) is thorough but somewhat descriptive; the paper could strengthen the argument by testing specific predictions of LRH versus MRH more directly (e.g., testing whether concept directions are truly linear in the sense of superposition versus proximity-based).
- The discussion of "Elsewhere" concepts acknowledges two possible interpretations (causal negation vs. distributed off-object evidence) but does not attempt to disambiguate them experimentally.

### Trivial

- Figure references in the text occasionally point to figures that are not clearly labeled in the extracted content (e.g., "Figure 11" is referenced before it appears in the text).

## Nice-to-Haves

- A systematic comparison of the SAE dictionary properties against alternative sparse coding methods (e.g., K-SVD, ISTA-based dictionaries) would strengthen the claim that the observed departures from LRH are properties of DINOv2's representation rather than the specific SAE training procedure.
- Quantitative metrics for the task-specific concept families (e.g., precision/recall of border concept detection, statistical significance of depth cue clustering) would make the qualitative findings more rigorous.
- A small-scale experiment testing a specific prediction of MRH (e.g., whether steering toward archetypal landmarks produces different effects than directional steering in a controlled setting) would substantially strengthen the hypothesis.

## Novel Insights

The paper's most novel insight is the observation that DINOv2's representation space exhibits properties that are inconsistent with a purely sparse, near-orthogonal "feature packing" view (LRH) while simultaneously being explainable by a convex-geometric structure where tokens are Minkowski sums of head-specific polytopes. The identification of "Elsewhere" concepts as implementing a form of learned conditional negation is a genuinely new finding that has implications for understanding how classification works in vision transformers. The three families of monocular depth cues (projective, shadow-based, frequency transitions) provide a concrete, interpretable decomposition of how DINOv2 achieves 3D understanding from 2D data alone, which is valuable for both scientific understanding and practical applications.

## Suggestions

- Strengthen the empirical case for MRH by providing quantitative comparisons against alternative geometric models (e.g., testing whether the data is better described by a Minkowski sum of convex polytopes versus a single convex set, a union of low-dimensional manifolds, or a hyperbolic space).
- Add systematic statistical tests for the task-specific concept families, including measures of consistency across images and datasets, and quantitative validation of the depth cue clustering (e.g., using held-out perturbation types to test cluster assignments).
- Clarify what specific predictions of MRH distinguish it from LRH in a falsifiable way, and design at least one experiment that could potentially reject MRH.

## Score and Decision

The paper makes a substantial contribution to interpretability research for vision foundation models through its scale, careful empirical analysis, and the proposal of a new geometric framework. The weaknesses—particularly the preliminary nature of the MRH evidence and some overclaiming of novelty—prevent it from being a top-tier paper, but the core empirical findings (task-specific concept specialization, departures from LRH) are solid and valuable. The paper is clearly written, methodologically sound in its main analyses, and the released interactive visualization is a significant community resource.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>