Now I have sufficient calibration. Let me produce the final consolidated review.

---

## Summary

This paper trains a 32,000-unit sparse autoencoder on DINOv2-B (the largest interpretability demo for a vision foundation model to date) and systematically characterizes how different downstream tasks recruit concepts from the learned dictionary. It reveals functional specialization (Elsewhere concepts for classification implementing conditional negation, border concepts for segmentation, three monocular depth cue families for depth estimation), analyzes the geometry and statistics of the learned dictionary against random and Grassmannian baselines, and proposes the Minkowski Representation Hypothesis (MRH) as a speculative geometric reinterpretation of how multi-head attention constructs token representations via convex combinations and Minkowski sums.

## Strengths

- **Scale and scope of the empirical analysis:** Training a 32,000-unit SAE on DINOv2-B and analyzing concept usage across three diverse tasks (ImageNet classification, ADE20K segmentation, NYU depth estimation) constitutes a substantial effort — the largest interpretability demonstration for a vision foundation model to date.

- **Rigorous geometric diagnostics with meaningful baselines:** The comparison of dictionary coherence against both random and Grassmannian baselines (Figure 4), the spectrum analysis, and the finding that pairwise similarities are heavier-tailed than a Grassmannian frame predicts are concrete empirical observations that raise substantive questions about how well a pure near-orthogonal features story describes DINOv2.

- **Interesting qualitative discoveries with practical value:** The Elsewhere concept (conditional negation for classification), the finding that segmentation concepts form tight clusters of boundary detectors, and the identification of three families of monocular depth cues (projective, shadow-based, frequency transitions) are genuinely novel and potentially valuable for the interpretability and vision communities.

- **Clean formalization connecting attention to geometry:** Proposition 1 showing that multi-head attention produces convex combinations per head whose sum is a Minkowski sum is a well-posed and pedagogically useful connection between architecture and geometric structure.

- **Intellectual honesty about limitations:** Proposition 2 (non-identifiability of Minkowski decomposition) and the accompanying discussion of why estimating individual concept contributions from final activations alone is underdetermined reflects genuine intellectual rigor that most papers in this area omit.

## Weaknesses

### Fatal
None.

### Major

- **Framing mismatch between the empirical characterization and the MRH.** The Minkowski Representation Hypothesis is prominently featured in the title, abstract, and contribution list as a co-equal contribution, but the empirical support in the visible text is thin — three observations (geodesic comparison, archetypal analysis, Gram block structure) described in ~5 sentences without any quantitative results, error bars, or statistical tests. While the paper explicitly calls MRH a "working hypothesis" (abstract), the prominence of its positioning relative to the well-supported empirical work creates a mismatch between what the paper claims and what it demonstrates. The paper would be substantially stronger if it clearly separated the (solid) empirical characterization as its primary contribution and positioned the MRH as a speculative direction in the discussion.

### Minor

- **No comparison to alternative concept discovery methods (PCA, ICA, non-negative matrix factorization)** to test whether the observed task-specific subspaces and geometric properties are specific to the SAE-based decomposition or are general properties of the activation space that any linear decomposition would reveal. This is the single largest gap in the evaluation.

- **Reconstruction fidelity (R² > 88%, line 57) is not specified as training or held-out.** With k=8 active codes out of 32,000, 12% unexplained variance is not negligible; if the residual is structured, it could be driving some of the observed "departures from LRH."

- **Single model (DINOv2-B), single SAE training run.** The paper acknowledges this (line 179) but the limitation is substantive: we cannot tell whether the findings generalize across vision architectures or even across SAE hyperparameters.

- **The characterization of LRH as a "purely sparse, near-orthogonal" account** (lines 35, 109, 177) over-simplifies the LRH literature (Elhage et al., 2022), which describes features as directions in activation space with superposition and does not claim perfect near-orthogonality. Many of the paper's observed departures are compatible with a sophisticated understanding of sparse coding with superposition.

- **The convex hull constraint on D (D ∈ conv(A), line 55)** prevents dictionary atoms from representing directions outside the convex hull of observed activations. This could artifactually influence the observed geometry (antipodal pairs, coherence patterns) and should be discussed as a potential confound rather than presented purely as a stability benefit.

- **The Elsewhere concept causality claim** ("they vanish if the object is removed," line 79) is stated as a causal assertion but depends on the quality and faithfulness of the causal masking method, supported by a single reference (Petsiuk et al., 2018). Additional validation or caveats would strengthen this finding.

- **The footnote (line 123)** noting that the correlation between ZᵀZ and DDᵀ "may be an intrinsic property of linear reconstructive methods" partially undermines the Section 4 claim that "usage influences geometry but is not the dominant organizing principle." This caveat deserves treatment in the main body.

### Trivial

- **No quantified negative results or failure cases** (e.g., what fraction of top-50 concepts in segmentation are NOT border detectors; how much task overlap exists between recruited concept sets).

## Nice-to-Haves

- Include at least one alternative concept discovery method (PCA, ICA, or NMF) to verify that the observed properties are not SAE-specific artifacts.
- Report train vs. held-out reconstruction error and analyze whether the unexplained residual has structure.
- Move the footnote about guaranteed-positive correlation into the main text and discuss its implications.
- For the MRH specifically, sharpen what concrete, falsifiable predictions distinguish it from LRH + superposition, and report quantitative results for the three empirical tests in the main text.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about the task-concept alignment score being deferred to Appendix C.1:** REMOVED per the rule that the parser strips appendices from all papers; the definition exists in the original submission.
- **Claim that Proposition 1 is "a restatement of known properties":** While attention producing convex combinations is individually known, the packaging as a coherent representational hypothesis is novel and preserved as a strength.
- **Criticism about MRH tests being relegated to the appendix:** The figures are in the appendix (parser-stripped), but the core concern about thin quantitative descriptions in the visible text is preserved in the Major weakness above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure to clearly separate the (solid) empirical characterization of DINOv2's concept geometry from the (speculative) MRH framing.
2. Add baseline comparisons to PCA/ICA/NMF for the task-specific concept analysis.
3. Report training vs. held-out reconstruction fidelity.
4. Move the footnote caveat about the guaranteed-positive correlation into the main text.
5. For the MRH empirical tests, report actual quantitative numbers (R², reconstruction quality, effect sizes) in the main text.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>