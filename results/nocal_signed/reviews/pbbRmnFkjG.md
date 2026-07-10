Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper trains a 32,000-atom stable SAE on DINOv2-B to extract a concept dictionary, then analyzes how downstream tasks (classification, segmentation, depth estimation) recruit these concepts, studies their geometric and statistical properties, and proposes the Minkowski Representation Hypothesis (MRH) — the idea that token embeddings lie in Minkowski sums of convex polytopes, naturally realized by multi-head attention. The paper makes substantial empirical and theoretical contributions, but also has notable gaps.

## Strengths

- **Scale of analysis.** Training a 32,000-atom stable SAE on DINOv2-B and analyzing task-specific concept recruitment at this scale is a genuinely substantial empirical effort — one of the largest concept-level analyses of a vision foundation model to date. (impact: +9.7)

- **Proposition 1 (multi-head attention realizes MRH).** Showing that multi-head attention naturally yields a Minkowski sum of headwise convex sets is elegant, formally clear, and connects an architectural primitive to a geometric hypothesis. This is the paper's most novel conceptual contribution. (impact: +9.9)

- **Proposition 2 (non-identifiability of Minkowski decomposition).** This is an honest and important theoretical observation that directly informs the feasibility of decomposition-based interpretability. (impact: +8.4)

- **Monocular depth cue decomposition (Section 3, Figure 3).** The perturbation-based analysis identifying three distinct families (projective geometry, shadow-based cues, frequency transitions) is cleanly motivated and aligns with established psychophysical categories. Showing that these emerge without labels and are linearly accessible from DINO's features is a nice contribution. (impact: +7.3)

- **The "Elsewhere" concept finding (Section 3, Figure 2).** The observation that certain concepts fire off-object yet depend on the object's presence — vanishing when the object is causally masked — is a genuinely non-obvious empirical phenomenon that could stimulate follow-up work on how ViTs encode contrast or boundary evidence. (impact: +6.5)

## Weaknesses

### Major

- **Missing layer specification (impact: -8.8).** The paper never specifies which layer of DINOv2-B the SAE operates on. Section 2 gives `d=768`, `t=261` and defines `a = f(x)`, but `f` is never resolved to a specific layer (e.g., final block output, layer 11, post-LN, residual stream). Early vs. middle vs. late layers have radically different properties (local texture vs. object parts vs. semantic categories), and the choice directly determines what the 32,000 "concepts" actually represent. The entire empirical analysis (Sections 3–5) is unanchored without this detail. The appendix may contain this information (the paper notes it was stripped), but it must be in the main text.

- **Thin empirical evidence for MRH relative to its prominence (impact: -10.0).** The Minkowski Representation Hypothesis is the paper's headline contribution (title, abstract), yet the main-text empirical evidence (line 163) describes three tests purely qualitatively with no numerical values: "k-NN geodesics remain near the data support" (no quantitative deviation metric), "AA matches or exceeds SAE reconstruction" (no R² numbers), "clear block structure in the Gram matrix" (no block-structure metric). All details are deferred to Figure 26 (appendix). Moreover, Proposition 1 already shows that multi-head attention structurally *realizes* MRH as a theorem, so the interesting empirical question is whether the *learned* archetypes and tiles correspond to interpretable factors — and that question is not addressed. The paper would be substantially stronger with either quantitative empirical evidence or an explicit reframing of MRH as a theoretical observation with pilot evidence.

### Minor

- **Potential circularity: using an LRH-based method to challenge LRH (impact: -1.8).** The paper trains an SAE (a method designed under the Linear Representation Hypothesis) and uses the geometry of the learned dictionary to argue LRH is incomplete. The observed departures (heavier-tailed inner products, sharp spectral decay) may partly reflect the SAE's specific design choices (convex-hull constraint `D ∈ conv(A)`, `k=8` active-code limit, non-negativity, k-means approximation with 128k centroids) rather than intrinsic properties of DINO's representations. Validation against at least one alternative dictionary method (e.g., standard SAE without the convex hull constraint, PCA+ICA) would address this.

- **Unexamined reconstruction residual (impact: -0.5).** R² > 88% means 12% of activation variance is unexplained. Concepts encoding the missing 12% could be invisible to the task-specific analysis (Section 3), potentially biasing conclusions. The paper does not discuss whether the residual has structure (low-rank, high-frequency, task-specific) that could change the conclusions.

- **Over-strong interpretation of Elsewhere concepts (impact: -0.5).** The abstract states Elsewhere concepts "implement conditional negation," while the figure caption (Figure 2) acknowledges "another interpretation being distributed off-object evidence." The main text should match the more cautious framing.

- **Clustering method for depth cue families not described (impact: -0.1).** The paper does not describe how the three monocular cue clusters were identified from UMAP (manual labeling? clustering on UMAP coordinates?). Since UMAP distorts global structure, this warrants clarification.

- **Grassmannian baseline comparison unclear (impact: -0.0).** The TAAP algorithm used for the Grassmannian baseline (Figure 4A) is not explained in the main text, making it hard to assess whether the comparison is fair given the SAE dictionary's structural constraints.

- **Important mathematical observation in a footnote (impact: -0.0).** Footnote 1 (line 123) notes that `corr(Z^T Z, DD^T)` is proportional to `tr(A^T A)`, suggesting the weak correlation between co-activation and geometry may be a mathematical necessity. This should be discussed in the main text.

### Trivial

- Naming inconsistency: "RA-SAE" (Discussion, line 177) vs. "stable SAE" (Section 2, line 43) should be harmonized.

## Nice-to-Haves

- Quantify the three MRH empirical tests numerically in the main text (geodesic vs. straight-line deviation, AA vs. SAE reconstruction metrics, Gram block-structure quantification).
- Validate geometric findings against at least one alternative dictionary method.
- Analyze the structure of the 12% reconstruction residual.
- Discuss the mathematical relationship in Footnote 1 in the main body.

## Removed Points

The following points from the input review were removed under the filtering rules:
- "The paper would be substantially stronger if it chose two rather than three contributions" — removed as scope advice/speculation.
- Speculative claims about what "may" be in the appendix — removed as not grounded in the paper text (the paper confirms the appendix was stripped by the parser).
- Various section-by-section notes that were restatements of content rather than weaknesses.

## Novel Insights

None beyond the paper's own contributions. The input reviews largely recapitulate the paper's own claims rather than adding novel interpretive insights.

## Suggestions

1. Specify the exact DINOv2-B layer used for SAE training in Section 2 of the main paper.
2. Add quantitative results for the three MRH empirical tests to the main text.
3. Validate geometric conclusions against at least one alternative dictionary-learning method.
4. Harmonize the "conditional negation" claim for Elsewhere concepts with the more cautious framing already present in the figure caption.

**MY FINAL SCORE:** <score>7.0</score>
**MY FINAL DECISION:** <decision>Accept</decision>