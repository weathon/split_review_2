Now I have all the information I need. Let me construct the final review.

## Summary

This paper trains a stable sparse autoencoder on DINOv2-B/4 to extract a 32,000-atom concept dictionary, then analyzes how three downstream tasks (classification, segmentation, depth estimation) recruit functionally specialized concept subsets, characterizes the dictionary's geometric and statistical properties against random and Grassmannian baselines, and proposes the Minkowski Representation Hypothesis (MRH) — that token embeddings lie in Minkowski sums of convex polytopes around archetypal landmarks.

## Strengths

- **Large-scale SAE-based concept dictionary for DINOv2.** The paper trains a stable SAE (32k atoms, k=8, convex-hull atom constraint) on 1.4M ImageNet-1K images with R² > 88% reconstruction fidelity. This is a technically sound contribution that advances the scale of interpretability analyses for vision foundation models, and the stability guarantee (atoms constrained to the convex hull of activations) addresses a known reproducibility problem with naive SAEs.

- **Systematic geometric characterization against properly motivated baselines.** Section 4 compares the learned dictionary's pairwise inner-product distribution against random vectors and a Grassmannian frame (via TAAP), finding heavier tails, sharper spectral decay, and higher coherence than the near-orthogonal ideal. The Grassmannian baseline is the theoretically appropriate null for the LRH's "near-orthogonal feature packing" claim, making this a principled quantitative test rather than a casual observation.

- **Discovery of "Elsewhere" concepts with causal evidence.** The paper identifies a functionally specific concept type in classification: concepts that fire off-object but depend causally on the object's presence (they "vanish if the object is removed" via causal masking). This is a non-trivial mechanistic finding — it goes beyond correlational attribution and suggests a learned conditional negation mechanism.

- **Controlled perturbation methodology for monocular depth cue isolation.** The depth analysis (Section 3) uses targeted image perturbations (median blurring, edge-preserving smoothing, high-pass filtering) to selectively ablate specific monocular cues, then tracks which concepts change activation. This perturbation-based causal approach yields three interpretable cue families (projective, shadow-based, frequency transitions) that align with known principles from visual neuroscience.

- **Clean separation of positional from non-positional structure.** Section 5 trains linear decoders to predict token coordinates per layer, shows the positional subspace compresses to ~2D in final layers, and demonstrates that projecting tokens orthogonally to the positional subspace leaves PCA organization largely unchanged. This carefully addresses the obvious confound that smooth PCA maps could simply reflect position.

- **Proposition 1 and Proposition 2 are formally sound.** Proposition 1 shows that multi-head attention constructively yields Minkowski-sum geometry (each head produces a convex set; head summation is a Minkowski sum). Proposition 2 honestly establishes that Minkowski decompositions are non-identifiable from final activations alone — a useful negative result with practical implications for interpretability.

## Weaknesses

### Fatal
None.

### Major

1. **The MRH empirical evidence is too thin to carry the weight the paper places on it.** The three empirical tests (k-NN geodesics, Archetypal Analysis reconstruction, code Gram matrix block structure) are described in a single paragraph and referenced to a single figure (Fig. 26). No quantitative metrics are reported: what quantitative threshold defines Archetypal Analysis "matching or exceeding" SAE reconstruction? How was "block structure" in the Gram matrix measured (e.g., modularity score, silhouette score of blocks)? The geodesic test (straight-line vs. k-NN paths staying near data) is consistent with any nonlinear manifold, not specifically with Minkowski sums of polytopes. Given that MRH appears in the title, abstract, and is framed as the paper's culminating contribution, this level of evidence is insufficient. The paper itself acknowledges MRH as a "working hypothesis," but the structural prominence given to it suggests a stronger empirical basis than is actually provided.

2. **Key qualitative findings lack quantification.** The "Elsewhere" concept analysis — while genuinely interesting — relies on visual inspection without reporting how many ImageNet classes exhibit the pattern, reproducibility across SAE runs or seeds, or inter-annotator agreement. The depth cue clustering uses UMAP + visual inspection to identify three families but reports no cluster validation metrics (silhouette scores, cluster stability under perturbation, statistical comparison of 2 vs. 3 vs. 4 clusters). The claim that "all the concepts among the top-50 consistently localize along object contours" for segmentation is presented without specifying a systematic measurement protocol, sample size, or consistency statistics across images. While qualitative analysis is common and valuable in interpretability work, the paper's definitive language ("classification exploits 'Elsewhere' concepts," "segmentation relies exclusively on boundary detectors," "DINO internally encodes a diverse, interpretable set of monocular depth cues") implies more certainty and quantification than the evidence supports.

### Minor

3. **Several comparisons lack statistical rigor.** Statements such as "intra-task concepts are significantly more aligned with one another compared to randomly selected concepts" (Section 3) are presented without p-values, confidence intervals, or bootstrap estimates. Similarly, claims about the dictionary "departing from the LRH" would benefit from quantitative effect sizes rather than qualitative comparison to baselines.

4. **No analysis of pattern-level stability across SAE runs.** The paper uses a "stable SAE" to address atom-level reproducibility, but it does not report whether the key patterns (task-specific recruitment profiles, geometric properties, Elsewhere/border/depth-cue families) replicate across SAE initializations or data splits. Without this, it is unclear whether the findings reflect robust properties of DINOv2 or artifacts of a particular training run.

5. **The paper's framing somewhat overstates the case against LRH.** The paper consistently uses qualifiers like "purely sparse-coding view" and repeatedly acknowledges findings that are compatible with LRH (distributed atoms, antipodal pairs as signed semantic axes). However, passages such as "departing from the LRH" (Section 4, line 97) without the "purely" qualifier suggest a stronger refutation than is warranted by the evidence — which documents quantitative deviations from an idealized baseline, not a qualitative refutation. The framing would benefit from consistently presenting these as nuanced departures from an idealization, which is what the evidence actually supports.

### Trivial
None.

## Nice-to-Haves

- A comparison to alternative concept discovery methods (e.g., network dissection, PCA/ICA baselines) would strengthen the claim that observed geometric properties reflect DINOv2's representations rather than the SAE training objective. This is scope-expanding and not a core flaw.
- Discussion of dictionary completeness and the choice of k=8 active codes per token would be informative but does not undermine the paper's main claims.

## Novel Insights

The most novel observation emerging from cross-referencing the reviews is that the paper's strongest contribution may be its empirical characterization of task-specific concept subspaces (the fact of differential recruitment and the geometric anisotropy it reveals), rather than either the LRH critique or the MRH proposal. The "Elsewhere" concept finding — if replicated quantitatively across a larger set of classes and SAE runs — could have significant implications for how attribution methods in vision interpretability are designed (since these concepts fire off-object yet carry object information). The weak correlation between co-activation geometry and geometric affinity (Section 4) is also a non-obvious result worth highlighting.

## Suggestions

1. **Expand the MRH empirical section substantially** or reposition it as a brief discussion/outlook section. If MRH remains a headline contribution, provide: (a) quantitative metrics for each of the three empirical tests, (b) a direct test that distinguishes MRH predictions (proximity-to-landmark) from LRH predictions (linear direction), and (c) ideally a replication on another vision transformer (e.g., MAE, CLIP).

2. **Quantify the qualitative findings:** report the frequency of Elsewhere patterns across ImageNet classes with confidence intervals, silhouette scores for depth cue clusters (including comparison to alternative k values), and systematic inter-image statistics for border concept localization.

3. **Reframe the contribution arc** to better balance between the well-supported empirical characterization (Sections 2–5, which are the paper's genuine strength) and the more speculative MRH proposal (Section 6). The empirical findings are worth publishing on their own terms.

4. **Add bootstrap confidence intervals** or significance tests for key comparisons (task alignment, spectral decay comparisons, coherence differences from baselines).

5. **Report pattern-level stability** across at least one additional SAE training run.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>