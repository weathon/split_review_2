## Summary

This paper trains a stable sparse autoencoder on DINOv2 to extract a 32,000-atom concept dictionary and uses it to analyze how downstream tasks (classification, segmentation, depth estimation) recruit task-specific functional subspaces. It then characterizes the statistical and geometric properties of these concepts, finding departures from the idealized Linear Representation Hypothesis (LRH)—higher coherence, sharp spectral decay, and dense positional signals. Motivated by these findings, the paper proposes the Minkowski Representation Hypothesis (MRH), in which token embeddings are Minkowski sums of convex polytopes spanned by archetypal landmarks, a geometry that multi-head attention naturally implements. Theoretical propositions and preliminary empirical evidence are provided, along with implications for interpretability and steering.

## Strengths

- **Large-scale concept extraction from a major vision foundation model.** The 32,000-atom dictionary trained on DINOv2 is, to the author’s knowledge, the largest such interpretability demonstration for a vision foundation model. The stable SAE with convex-hull constraints ensures in-distribution atoms and reproducibility, and the dictionary is released with an interactive demo.
- **Novel and insightful task-specific analyses.** The identification of “Elsewhere” concepts for classification (conditional negation), border concepts for segmentation, and three families of monocular depth cues (projective, shadow-based, frequency transitions) provides compelling qualitative evidence of functional specialization within the concept space. These findings are well-illustrated and grounded in known visual processing principles.
- **Careful geometric characterization that challenges pure sparse-coding views.** The paper systematically measures coherence, singular-value spectra, Hoyer scores, and co-occurrence structure, showing that the learned dictionary is more coherent and anisotropic than random or Grassmannian baselines, and that dense positional features coexist with sparse ones. These diagnostics move beyond simply claiming “features are sparse” and reveal a richer organization.
- **Proposition of a mechanistically plausible alternative hypothesis (MRH).** The Minkowski Representation Hypothesis connects attention (convex combination per head, Minkowski sum across heads) to a landmark-based geometric account of representation, drawing on conceptual spaces and convex polytopes. The theoretical propositions (multi-head attention realizes MRH, non-identifiability of decomposition) are clearly stated and provide a formal foundation for future work.
- **Clarity and depth of presentation.** The paper is well structured, figures are informative, and the reasoning from empirical observations to hypotheses is clearly laid out. The discussion of implications for steering and decomposition is thoughtful.

## Weaknesses

### Fatal

None.

### Major

- **MRH remains a weakly supported speculation.** The paper presents MRH as a “working hypothesis” but the empirical evidence for it is preliminary and largely indirect (AA outperforming SAE with few archetypes, \(k\)-NN geodesics staying near data, block structure in the Gram matrix). These observations are consistent with MRH but do not rule out other geometrically structured densities, nor do they provide a quantitative test that discriminates MRH from LRH. The paper’s central claim—that MRH is a better account than LRH—needs stronger validation, such as explicitly testing its predictions (e.g., saturation of steering, convex decomposition into known head polytopes) on held-out tasks.
- **Equivocation between SAE concepts and MRH archetypes.** The paper first operationalizes LRH via an SAE and then uses that same dictionary to motivate MRH, but MRH is a fundamentally different geometric claim (convex regions vs. sparse linear directions). The relationship between the learned SAE atoms and the archetypal landmarks of MRH is not clarified: are the SAE atoms to be identified with archetypes, or with something else? This ambiguity weakens the narrative arc from “we extracted concepts” to “we propose a new hypothesis.”
- **Limited quantitative validation of the concept dictionary.** The SAE reconstruction fidelity is reported (\(R^2 > 88\%\)), but there is no evaluation of concept interpretability (e.g., human ratings, downstream probe performance compared to other concept banks, sensitivity to hyperparameters). The analysis of task-specific concept usage relies on alignment scores that are defined in the appendix but not compared against baselines (e.g., random concept subsets, alternative dictionary learning methods). The qualitative findings are interesting but lack statistical rigor.
- **Non-identifiability proposition is a known fact, not a novel insight.** Proposition 2 (non-uniqueness of Minkowski decomposition) follows directly from the additivity of support functions and is a standard property of zonotope generators. While it provides context for the difficulty of factor analysis, it does not constitute a new technical result and is overstated as a limitation specific to MRH.

### Minor

- The paper sometimes uses informal or evocative language (“Elsewhere concepts,” “Rabbit Hull”) that, while engaging, can obscure precise meaning. The connection between “Elsewhere” and conditional negation is suggestive but not rigorously established (e.g., through controlled causal interventions beyond masking).
- The analysis of task-specific concepts is primarily qualitative. Quantitative measures of overlap (e.g., Jaccard index between top concepts of different tasks) or significance tests would strengthen the claim of functional specialization.
- The paper does not compare its method to other existing large-scale concept extraction approaches in vision (e.g., from CLIP or other ViTs), nor does it benchmark the dictionary’s usefulness beyond descriptive analysis.

### Trivial

None to note.

## Nice-to-Haves

- A direct empirical test of MRH: for example, check whether steering toward a landmark saturates as predicted, while directional (LRH) steering continues to increase in effect. This would distinguish the two hypotheses.
- Release of the full concept dictionary and interactive demo will be a valuable community resource; including a small case study of how researchers can use it for probing would increase impact.
- Compare MRH-based probes (barycentric coordinates within convex cells) to standard linear probes on downstream tasks to demonstrate practical advantages.

## Novel Insights

The paper offers two genuinely novel insights. First, the discovery that DINOv2’s classification heads recruit “Elsewhere” concepts that implement a form of learned negation is a subtle and surprising finding about how object boundaries and contrast are encoded. Second, the Minkowski Representation Hypothesis reframes representation geometry as convex composition around landmarks, providing a mechanistic link between multi-head attention and conceptual spaces that goes beyond the purely linear sparse-coding picture. Even if MRH is not fully validated, the geometric diagnostics (coherence tails, sharp spectral decay, dense positional outliers) convincingly show that the activation space is richer than a simple Grassmannian frame, opening new directions for interpretability research.

## Suggestions

- Strengthen the empirical case for MRH by designing a targeted experiment: e.g., train a linear probe with an explicit convex hull constraint and compare its steering behavior to an unconstrained probe. Show that the convex probe saturates and stays on manifold, while the linear probe extrapolates off manifold.
- Clarify the relationship between the SAE-derived concepts and the MRH archetypes. If the SAE atoms are not directly archetypes, how should researchers connect the two frameworks? A simple mapping would help readers bridge Parts 2–4 with Part 6.
- Add quantitative overlap measures and significance tests for the task-specific analyses to make the specialization claims more rigorous.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>