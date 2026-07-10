Now I have all the calibration data needed. Let me write the final review.

## Summary

The paper trains a 32,000-concept sparse autoencoder dictionary on DINOv2-B and uses it to analyze how different downstream tasks (classification, segmentation, depth estimation) recruit concepts. It discovers novel phenomena — "Elsewhere" concepts that implement conditional negation for classification, border concepts for segmentation, and three families of monocular depth cues — and analyzes the geometry of the resulting dictionary. Based on observed departures from idealized sparse, near-orthogonal structure, the paper proposes the Minkowski Representation Hypothesis (MRH): that token embeddings lie in Minkowski sums of convex polytopes around archetypal landmarks, a construction naturally realizable by multi-head attention.

## Strengths

- **"Elsewhere" concept finding (Section 3, Figure 2).** The discovery that classification heads recruit concepts that fire off-object but vanish when the object is causally removed is genuinely novel and non-obvious. The paper correctly notes this could be evidence of conditional negation and has practical implications for interpretability methods that assume concept activations localize to relevant objects. **[favorability=15.08]**

- **Depth cue decomposition (Section 3, Figure 3).** The perturbation-based identification of three families of monocular cues (projective, shadow-based, frequency transitions) is methodologically clean and produces interpretable, neuroscience-aligned clusters. This demonstrates real value in the dictionary approach. **[favorability=11.69]**

- **Proposition 1 (multi-head attention → Minkowski sum) in Section 6.** The observation that multi-head attention naturally yields Minkowski sums of convex polytopes (each head → convex combination of values → Minkowski sum across heads) is geometrically elegant and worth stating formally. **[favorability=13.33]**

- **Large-scale interpretability resource.** The paper trains and releases (by the authors' account) the largest interactive interpretability visualization for a vision foundation model, a genuine community asset. **[favorability=12.12]**

- **Honest treatment of limitations.** The paper repeatedly qualifies MRH as a "working hypothesis," explicitly states that Minkowski decomposition is non-identifiable from final activations (Proposition 2), and acknowledges the preliminary nature of the empirical evidence. **[favorability=8.73]**

## Weaknesses

### Major

- **Mismatch between MRH prominence and evidence.** The title ("INTO THE RABBIT HULL: FROM TASK-RELEVANT CONCEPTS IN DINO TO MINKOWSKI GEOMETRY"), abstract, and Section 6 position MRH as the culminating contribution. However, the empirical support consists of three tests described in a single paragraph: (i) straight-line vs. k-NN geodesics (indirect — piecewise paths are consistent with polytope faces but do not confirm MRH specifically), (ii) Archetypal Analysis matching SAE reconstruction at the |S|=1 degenerate case, (iii) block structure in code Gram matrices. The paper is candid that MRH is a "working hypothesis," but the structural emphasis creates a gap between framing and evidence. The paper would be stronger if it recentered on its empirical findings (task-specific concept analysis + geometric characterization) and presented MRH as a forward-looking discussion rather than the headline result.

- **Potential circularity in SAE-based argument against LRH.** The geometric analyses in Section 4 (spectral decay, coherence, task-aligned clusters) depend on an SAE that instantiates LRH-style assumptions (sparsity k=8, non-negativity, convex hull constraint on atoms). The paper does not systematically disentangle whether the observed dictionary properties reflect DINOv2's internal geometry or SAE inductive biases / finite-sample training artifacts. For example, the sharp singular-value decay of D could arise from the convex hull constraint (which forces atoms toward data centroids), and higher coherence than Grassmannian baselines could reflect the natural-image training distribution rather than model feature geometry. The paper acknowledges this at a high level ("step beyond the SAE lens" in Section 5) but does not provide a controlled analysis — e.g., training SAEs with varied sparsity regimes (k=4,16,32) or comparing against a control SAE on a randomized model.

- **Insufficiently diagnostic comparison baselines.** Section 4 compares dictionary coherence to "random and Grassmannian baselines" and interprets higher coherence as a departure from LRH. The Grassmannian baseline is a set of maximally incoherent vectors by construction. The relevant null for the claim "DINOv2's dictionary has more structure than expected under LRH" would include SAEs trained on the same activations under different sparsity regimes, or the PCA basis of the activations themselves. The fact that a dictionary trained on natural-image activations has higher coherence than random frames is not informative about whether DINOv2's representations specifically depart from the LRH picture.

### Minor

- **Unquantified "largely unchanged" claim.** Section 5 states that projecting tokens orthogonally to the positional subspace "leaves the PCA organization largely unchanged (Figure 25)" without a quantitative criterion (e.g., cosine similarity between original and projected PCs, or reconstruction ratio). This claim is the key transition to the MRH discussion and needs numerical support.

- **Task overlap claim lacks quantitative metrics.** The paper states that task-recruited concept sets "only weakly overlap" (Section 3, abstract) but does not provide quantitative overlap metrics (e.g., Jaccard similarity with a null distribution). The claim is supported by visual UMAP inspection and a span comparison, but direct concept-set overlap is not measured.

- **Compatibility of task-specific subspaces with LRH.** Section 3 shows that task-specific concepts form low-dimensional subspaces and presents this as evidence of rich structure. However, finding that a task uses only a subset of near-orthogonal features is entirely compatible with LRH — this does not challenge the sparse-coding view. The framing could be more precise about what observations actually constitute evidence against a purely sparse-coding account.

### Trivial

None.

## Nice-to-Haves

- Clarify whether MRH and LRH are competing or complementary at different levels of analysis. LRH describes a global feature basis (linear directions in activation space), while MRH describes token geometry (convex mixtures within that space). A token could simultaneously be a convex combination of archetypes and have its features read out by linear directions. The paper should address this explicitly.
- If MRH is to remain a central claim, expanding the empirical evidence (e.g., showing that token activations are better approximated by Minkowski sums of head-specific polytopes than by linear combinations of global dictionary atoms, using held-out quantitative comparison) would substantially strengthen the paper.
- SAE stability analysis across training seeds would strengthen confidence, though the paper cites the "stable SAE" method designed to address this.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Centroid selection not reported (from Harsh Critic):** The critic claimed the paper does not report how the 128,000 centroids were selected. The paper explicitly states they were extracted via "k-means over 1.4M ImageNet-1K images (with augmentation)" (Section 2). Removed as factually incorrect.
- **MRH evidence "all relegated to the appendix":** The core weakness (thin evidence) is kept above, but the framing that this is problematic *because* the evidence is in the appendix is removed per hard rules — missing appendix content should not be a weakness. The substance (the evidence is preliminary and indirect) is retained.
- **SAE training seed variance as reproducibility nitpick:** Demoted from the critic's list; the paper cites a "stable SAE" method. Moved to nice-to-have rather than a core weakness.
- **Section 5 PCA transition is "abrupt":** The critic's subjective assessment of rhetorical flow is removed as insufficiently specific.

## Novel Insights

The reviews' most penetrating observation is that the paper bundles two contributions of quite different evidential weight: (a) a substantial empirical characterization of DINOv2's concept dictionary with genuinely novel findings (Elsewhere concepts, depth cue families), and (b) a speculative theoretical proposal (MRH) that rests on preliminary evidence. This diagnosis is accurate and points to a concrete path for improvement. The reviews' other key insight is that using an SAE (which embodies LRH-style assumptions) to argue *against* a purely sparse-coding view creates a potential circularity that the paper should address through controlled analyses (e.g., varying sparsity regimes, comparing against a randomized-model baseline). The finding that the weak correlation between Z^T Z and DD^T (co-activation vs. geometric affinity) is partially an algebraic artifact of linear reconstructive methods (footnote 1) is another valuable observation not fully developed by the authors.

## Suggestions

1. **Reframe the paper's emphasis.** Recenter on the strong empirical findings (Elsewhere concepts, depth cues, geometric characterization) and present MRH as a discussion/hypothesis section rather than the culminating contribution flagged in the title.
2. **Address the SAE circularity.** Include analyses that separate model properties from SAE artifacts: train SAEs with different sparsity levels (k=4, 16, 32) or compare against a control SAE on a model with randomized weights, and check whether the geometric patterns (spectral decay, coherence) are stable.
3. **Add more diagnostic baselines.** Compare dictionary coherence not just to Grassmannian frames but to SAEs trained on the same activations with different sparsity regimes, and to the PCA basis of the activations themselves.
4. **Quantify the qualitative claims.** Add Jaccard similarity for task overlap, a numerical criterion for "largely unchanged" in the positional ablation, and more precise framing of what observations do and do not challenge the LRH picture.

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| imT03YXlG2.md (Selective remapping of visual concepts) | 6.50 | 1 | Yes | Closest topical match; similar SAE-on-ViT methodology. That paper had cleaner framing but less novel empirical findings. My paper has stronger novel discoveries but MRH overclaiming is a structural weakness. Comparable overall. |
| bVTM2QKYuA.md (Representation Geometry of Features) | 6.75 | 2 | Yes | Formalizes polytope concept representations, topically related to MRH. Stronger theoretical grounding and cleaner execution. My paper's empirical findings are more varied but its theoretical proposal is less well-supported. |
| F76bwRSLeK.md (SAEs Find Highly Interpretable Features) | 4.80 | 1 | Yes | SAE for LLM interpretability. Divergent reviews (one 1, others 5-6). My paper has stronger empirical findings and better presentation. |
| Ch8s4FdUXS.md (Unpacking SDXL Turbo) | 4.40 | 1 | Yes | SAE for text-to-image diffusion. Limited scope, qualitative reliance. My paper is stronger empirically and better scoped. |
| uDIiL89ViX.md (Scientific discovery with DL) | 5.60 | 1 | Yes | DL for microscopy. Mixed reviews (8,5,5,5,5). My paper has clearer contributions and more striking findings. |
| 9ca9eHNrdH.md (SAEs Do Not Find Canonical Units) | 7.00 | 1 | Yes | Clean experiments on SAE limitations. My paper is less focused and has weaker evidence for its central claim. |
| ih3BJmIZbC.md (Representational Similarity via Concepts) | 6.80 | 2 | Yes | Concept-based model comparison. Mixed reviews. Similar weaknesses about qualitative claims. |

**Bracketing:** Round 1 placed the paper in the 5.5–7.5 band, with the 6.50 "Selective remapping" paper as the closest topical anchor. **Narrowing (Round 2):** Comparing my draft's itemized favorability ratings against the 6.50 anchor — my paper's strengths are stronger (Elsewhere concepts at 15.08 vs. the anchor's best at 13.72), but my three major weaknesses (MRH evidence mismatch, SAE circularity, weak baselines) are more severe than any single weakness in the 6.50 anchor (worst there: -5.29, but that's about cherry-picking claims). The 5.60 anchor paper had weaker findings and similar methodological concerns. My paper sits between these, with stronger novel discoveries but also the MRH framing issue. The final score of **6.0** reflects a paper with genuinely valuable empirical contributions that is held back by a framing-evidence mismatch and methodological gaps that are fixable but non-trivial.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>