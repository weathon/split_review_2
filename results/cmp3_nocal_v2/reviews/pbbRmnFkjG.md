---

## Summary

This paper trains a stable sparse autoencoder (SAE) with 32,000 atoms on DINOv2-B activations, producing a large-scale concept dictionary. It uses this dictionary to study how downstream tasks (classification, segmentation, depth estimation) recruit different concept subsets, revealing several interesting empirical patterns. The paper then documents departures from an idealized sparse-coding picture (higher-than-expected coherence, sharp spectral decay, task-aligned anisotropy) and, motivated by these departures, proposes the Minkowski Representation Hypothesis (MRH) — the idea that token embeddings lie in Minkowski sums of convex polytopes. The MRH is accompanied by a theoretical formalism (Definition 1, Propositions 1–2) and preliminary empirical evidence.

---

## Strengths

- **Large-scale, stable SAE dictionary (Section 2).** Training a convex-hull-constrained SAE with 32,000 atoms on DINOv2-B (768-dim, k=8 active codes, R² > 88%) is a nontrivial engineering achievement. The dictionary and its interactive visualization constitute a meaningful resource for the interpretability community.

- **Task-specific empirical findings are genuinely novel (Section 3).** Three specific discoveries stand out: (i) "Elsewhere" concepts that fire off-object but depend on object presence, suggesting a form of contextual modulation; (ii) segmentation concepts that consistently localize to object boundaries and form a tight cluster with sharply decaying spectrum (Figure 11), indicating a dedicated low-dimensional submanifold for contour processing; (iii) identification of three distinct monocular depth cue families (projective, shadow-based, frequency transitions) via perturbation analysis (Figure 3). These are concrete, falsifiable observations that extend what was known about DINOv2's internal organization.

- **Theoretical formalism for MRH (Section 6, Definition 1, Propositions 1–2).** The formal definition of MRH as a Minkowski sum of convex polytopes is mathematically precise. Proposition 1 — that multi-head attention realizes MRH because each head outputs a convex combination of its values and heads sum to a Minkowski sum — is a clean theoretical observation. Proposition 2 (non-identifiability of Minkowski decomposition) is a useful cautionary result for interpretability practitioners.

---

## Weaknesses

### Fatal

None.

### Major

- **The empirical evidence for MRH is thin relative to the prominence given to it in the paper's framing.** The MRH is referenced in the title, abstract, contributions list, and Section 6, yet the entire empirical case occupies ~6 sentences in the main text (lines 163–164). Three pieces of evidence are offered, each with significant limitations: (a) the geodesic comparison (k-NN vs. straight-line interpolation) is consistent with any non-convex data manifold and does not specifically support MRH — no quantitative comparison or baseline is reported in the main text; (b) the Archetypal Analysis comparison is presented without clarifying the crucial difference in units (AA uses ~10 archetypes per *image* of ~260 tokens, while the SAE uses k=8 active codes per *token*), making the comparison difficult to interpret; (c) the "clear block structure" in Gram matrices (Figure 26) is claimed visually without any quantitative clustering metric. For a hypothesis that anchors the paper's title and narrative arc, this level of evidence is insufficient. The paper acknowledges MRH as a "working hypothesis," but the framing (title, contribution list, separate theory section) conveys a stronger claim than the evidence supports.

- **The "Elsewhere concept" negation claim is overstated in the abstract.** The abstract (line 9) presents "classification exploits 'Elsewhere' concepts that implement 'object negation'" as a settled finding. The contributions list (line 33) similarly states "classification repeatedly uses 'Elsewhere' concepts that implement learned negation." However, the evidence only shows that these concepts activate off-object and "vanish if the object is removed" — i.e., they depend on object presence. This is consistent with multiple mechanisms (distributed off-object evidence, contrast coding, etc.), as the paper itself acknowledges in the Figure 2 caption. The abstract should reflect this ambiguity rather than assert a mechanistic interpretation as fact.

### Minor

- **No ablation of SAE hyperparameters that directly affect the geometric claims.** The departure from LRH is the paper's central motivation for proposing MRH, but this departure is measured using a single SAE configuration (k=8 sparsity, 42× overcompleteness, BatchTopK). The observed coherence statistics may be partially determined by these design choices rather than by the underlying representation geometry. An ablation varying k (e.g., 4, 8, 16, 32) would substantially strengthen or qualify the critique of the sparse-coding view.

- **No cross-architecture validation.** All experiments use DINOv2-B. The paper acknowledges this limitation (line 179) but understates its scope: claims about MRH purport to describe attention-based representations generally, yet no other model (DINOv2-S/L/g, CLIP-ViT, MAE) is tested. A single additional variant would significantly strengthen the generality of the findings.

- **Task-recruitment analysis uses SAE-reconstructed activations, not original activations.** Since the SAE has R² > 88%, ~12% of variance is discarded. If the discarded variance is task-relevant (e.g., diffuse but important features suppressed by the sparsity prior), the task-recruitment analysis could be systematically biased. A control experiment using original DINOv2 activations directly would be informative.

- **The PCA/horseshoe caveat.** The paper claims "PCA is a linear operator, it cannot fabricate curvature" (Figure 5 caption), but PCA can produce apparent curved/arch structure in low-dimensional projections through the well-known horseshoe effect (especially in high-dimensional data with gradient structure). This doesn't invalidate the paper's observations but the claim should be qualified.

- **Depth cue perturbation analysis lacks validation.** The controlled perturbations (median blurring, edge-preserving smoothing, high-pass filtering) are described as isolating specific monocular cues, but no quantitative validation is provided that these perturbations actually isolate the claimed cues rather than producing correlated but distinct effects.

### Trivial

None.

---

## Nice-to-Haves

- Comparison of the SAE-learned concepts with those from alternative methods (ICA, NMF, standard dictionary learning) would clarify which geometric properties are SAE-specific.
- A proper causal test of the Elsewhere concept's role (e.g., concept activation/suppression intervention) would strengthen the "negation" interpretation.
- Comparison of MRH against alternative geometric models (e.g., simple low-rank linear model) on held-out data would provide a stronger case for MRH as a distinctive hypothesis.

---

## Removed Points

- **Critic's claim that the AA vs. SAE comparison "is evidence against concentration on low-dimensional polytopes" because "ten is larger than eight."** This misunderstands the comparison: AA uses ~10 archetypes per *image* (~260 tokens), while the SAE uses k=8 active codes per *token* (~2080 per image). That AA with far fewer components matches the SAE actually *supports* low-dimensional concentration, not refutes it. Removed as factually incorrect.

- **Critic's claim that "there is no direct path from the SAE dictionary properties to MRH."** The paper explicitly presents MRH as a *hypothesis motivated by* observed departures from LRH, not as proven by SAE data. The paper's framing ("Motivated by these departures, we advance a different view") is transparent about this logic. Removed as strawman.

- **Critic's claim about the abstract conflating two distinct LRH claims.** The paper operationalizes LRH in a specific, clearly stated way (sparse, near-orthogonal directions). Whether this matches every definition in the literature is a framing preference, not a paper weakness. Removed.

- **Critic's note that Footnote 1 weakens geometric conclusions.** The paper is being transparent about a known mathematical property. This is intellectual honesty, not a weakness. Removed.

- **Critic's characterization of the MRH evidence as lacking "any quantitative metrics."** The paper references Figure 26 (in the appendix, stripped by the parser) which likely contains the quantitative values. The critic's stronger claim (no numbers at all) cannot be verified from the available text. The surviving weakness focuses on what *is* verifiable: the evidence in the main text is thin, not that it is absent. Point subsumed into the first Major weakness.

- **Strengths about the problem being "important" or the paper being "well-motivated."** These are generic. Only the three concrete strengths listed above are retained.

---

## Novel Insights

The critic's key insight — that the MRH framing over-promises relative to the evidence provided — is a structural observation about the paper's architecture. The suggestion to restructure the paper to foreground the empirical findings and treat MRH as a speculative direction is constructive and specific. Beyond this, the reviews do not contribute novel scientific insights beyond the paper's own contributions.

---

## Suggestions

- Restructure the paper so that the empirical findings (task-specific concept usage, departures from LRH ideals) are the primary contribution, with the MRH reframed as a forward-looking discussion section or "Towards a New Hypothesis" rather than a central claim. This would eliminate the mismatch between the strength of the evidence and the prominence of the framing.
- Tone down the "Elsewhere as object negation" claim in the abstract to match the actual evidence (e.g., "Elsewhere concepts that depend on object presence in a manner consistent with conditional negation").
- Add an ablation varying SAE sparsity k (and, if possible, dictionary size) to assess whether the observed departures from near-orthogonality are stable across hyperparameter choices.
- Test at least one additional ViT variant (e.g., CLIP ViT-B or DINOv2-S) to validate the generality of the geometric observations.
- Add a control experiment for the task-recruitment analysis using original (non-reconstructed) activations.

---

## Score and Decision

**MY FINAL SCORE:** <score>6.0</score>
**MY FINAL DECISION:** <decision>Accept</decision>