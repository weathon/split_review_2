## Summary

This paper trains a 32,000-atom sparse autoencoder (SAE) on DINOv2-B activations to study how downstream tasks recruit learned concepts. It reports several interesting findings — "Elsewhere" concepts for classification, border detectors for segmentation, three families of monocular depth cues, and a geometric analysis showing departures from sparse-coding ideals. Based on these observations, it proposes the Minkowski Representation Hypothesis (MRH), which posits that tokens are Minkowski sums of convex polytopes around archetypal landmarks, and shows that multi-head attention mathematically realizes this construction. The paper releases an interactive visualization of the learned dictionary.

## Strengths

- **Scale of the concept dictionary and interactive visualization.** The paper trains a 32,000-atom SAE on DINOv2-B and releases an interactive visualization — a substantial practical resource for the community studying DINOv2's internal representations. **[impact=+8.51]**

- **Interesting qualitative discoveries about task-specific concept usage (Section 3).** The "Elsewhere" concept (fires off-object, disappears when the object is removed) is a genuinely non-trivial phenomenon. Segmentation's top-50 concepts being almost exclusively boundary detectors forming a tight cluster is a clean finding. The decomposition of monocular depth cues into projective, shadow-based, and frequency-transition families is compelling as an existence proof that DINOv2's unsupervised representations factor 3D perception primitives. **[impact=+7.44 to +9.79]**

- **Clean quantitative evidence for task-specific low-dimensional subspaces (Figure 11, Section 3).** The finding that intra-task concepts are more aligned than random sets, and that the eigenvalue spectra of task sub-dictionaries decay faster than random subsets, provides a quantitative anchor for the qualitative observations. This is the strongest piece of empirical evidence in the paper. **[impact=+9.18]**

- **Elegant theoretical connection between multi-head attention and Minkowski sums (Proposition 1, Section 6).** The observation that each head outputs a convex combination, and that multi-head attention sums these to realize a Minkowski sum of convex polytopes, is mathematically clean and connects the MRH to a known architectural mechanism. **[impact=+9.91]**

## Weaknesses

### Fatal
None.

### Major

- **The MRH is the paper's headline contribution (title, abstract, Section 6) but is supported by only the thinnest empirical evidence — three qualitative observations in a single paragraph (line 163), none with quantitative metrics, baselines, or error bars.** The straight-line vs. k-NN geodesic comparison reports no metric for "nearness to data support"; the Archetypal Analysis vs. SAE comparison reports no reconstruction metrics (R², MSE); the "clear block structure" claim in the Gram matrix has no quantitative modularity score. For a paper whose title foregrounds the MRH, this level of evidence is insufficient. **[impact=-10.00]**

- **The paper's central chain of evidence — SAE → critique of LRH → MRH — has a structural circularity problem.** The SAE itself instantiates the Linear Representation Hypothesis that the paper critiques (sparse, overcomplete linear decomposition with k=8, c=32k, ℓ₀ constraint). The departures from LRH idealizations (higher coherence, sharp spectral decay) could equally be artifacts of the SAE's particular hyperparameter choices rather than properties of DINOv2's actual representations. The paper achieves R² > 88% reconstruction fidelity, meaning 12% of activation variance is not captured and could contain structure relevant to the debate. While the paper partially addresses this by moving beyond the SAE lens in Section 5, the core narrative depends on SAE-derived findings. **[impact=-9.96]**

### Minor

- **Several mechanistic claims are supported mainly by correlational evidence.** The "Elsewhere" concept is described in the abstract and contributions as implementing "learned negation," but the evidence is that the concept fires off-object and disappears under causal masking, with limited detail on the masking procedure, prevalence across ImageNet classes, or ruling out of alternative explanations (e.g., texture/background features that covary with object presence). The paper does hedge in the main text ("another interpretation being distributed off-object evidence"), but the abstract is more definitive. **[impact=-2.46]**

- **The depth cue perturbation analysis (Section 3) lacks specification of filter parameters (kernel sizes, thresholds), details on how perturbation-induced activation changes were measured, and how the three functional clusters were identified from the UMAP visualization.** The analysis relies substantially on qualitative visual inspection. **[impact=-0.38]**

- **The per-image PCA analysis (Section 5) showing tokens "lie on a consistent low-dimensional set aligned with objects" is illustrated with five cat images (Figure 5).** While the qualitative pattern is visually striking, the paper does not quantify how general this is across the diverse ImageNet-1K validation set. **[impact=-0.01]**

- **The paper's critique of LRH uses a Grassmannian (maximally incoherent) frame as a baseline, but LRH only requires nearly orthogonal features, not maximally incoherent ones.** The paper's own finding that "most atoms are near orthogonal, with small tight clusters" (Section 4) is arguably consistent with the nearly-orthogonal qualifier in LRH, somewhat undermining the strength of the claimed departure. **[impact=-0.01]**

### Trivial
None.

## Nice-to-Haves
- Causal validation of SAE concepts (e.g., activation patching) would strengthen the mechanistic claims, though this goes beyond what is standard for a large-scale dictionary study.
- A hyperparameter sensitivity analysis (varying c=32k, k=8) would help assess whether the geometric findings are robust or SAE-specific.

## Removed Points
These points are flagged to be removed; treat them with caution.
- The structural suggestion that the paper "choose a lane" (empirical study vs. MRH proposal) — moved to Suggestions.
- The request for hyperparameter sensitivity analysis (c=32k, k=8) — moved to Suggestions.
- The request for comparison to alternative LRH operationalizations (NMF, ICA) — speculative and not standard practice.
- The criticism about the paper not providing a comparison point for "largest interpretability demo" — the claim is hedged ("to our knowledge"), and cross-modal scale comparisons are not meaningful.
- The section notes about the paper leaning heavily on the appendix — the parser strips appendices, which exist in the original submission.
- The generic "no statistical significance reported" criticism — applies to most work in this area.
- The criticism that Proposition 2's non-identifiability undermines MRH testability — the paper explicitly addresses this by noting intermediate signals (attention weights, per-head outputs) can render the factorization tractable; the reviewer overstates this concern.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Substantially strengthen the MRH empirical evidence with a quantitative, discriminative test between MRH and LRH predictions — e.g., showing that SAE-style linear steering plateaus or reverses in ways predictable from MRH geometry.
2. Add quantitative metrics to the three MRH tests: reconstruction R² for AA vs. SAE, geodesic deviation scores, and Gram block modularity with null-model comparisons.
3. Quantify the prevalence of the Elsewhere phenomenon across ImageNet classes and report causal masking details.
4. Report filter parameters and cluster identification methodology for the depth cue perturbation analysis.
5. Validate the per-image PCA findings (Section 5) with a quantitative measure of low-dimensional structure across a larger random sample of images.
6. Consider either de-emphasizing the MRH as a speculative discussion point or providing it with commensurate empirical support — the current mismatch between the title/abstract emphasis and the thin evidence is the paper's most significant weakness.

## Score and Decision

### Calibration Anchors

| Anchor Path | Avg Human Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/imT03YXlG2.md` (SAE on CLIP vision transformer, concept remapping during adaptation) | 6.50 | 1 | Yes | Topically similar (SAE on vision model, concept analysis). This paper has weaker quantitative evaluation for its headline claim but more theoretical ambition. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9ca9eHNrdH.md` (SAE canonical units analysis) | 7.00 | 1 | Yes | Methodologically rigorous with clear experiments. This paper has interesting empirical observations but lacks the same experimental precision. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Ch8s4FdUXS.md` (Unpacking SDXL Turbo with SAEs) | 4.40 | 1 | Yes | Similar qualitative-over-quantitative issues (impact -9.86 for heavy reliance on qualitative analysis). This paper has broader scope and stronger theoretical component. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bVTM2QKYuA.md` (Representation Geometry of Features and Hierarchy in LLMs) | 6.75 | 2 | Yes | Similar in extending LRH to polytope geometry, but with rigorous theory+experiments. This paper's MRH empirical validation is much weaker by comparison. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KJFyOwAnLR.md` (Emergent Geometry in Neural Representations) | 4.00 | 2 | Yes | Geometric hypothesis with limited evidence. Claims too broad for evidence (impact -9.98). This paper has stronger empirical contributions. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/F76bwRSLeK.md` (SAEs Find Highly Interpretable Features) | 4.80 | 3 | No | Simple SAE application with mixed ratings. This paper has more novel findings. |

### Scoring Rationale

**Round 1 bracket:** 4.0 – 6.5, based on comparison with topically similar SAE-on-vision papers.

**Round 2 narrowing:** The paper's two major weaknesses (MRH evidence gap at impact -10.00 and SAE circularity at impact -9.96) are structurally severe — the headline contribution is not adequately supported, and the central analytical chain has a logical circularity. However, the empirical study of DINOv2 representations (task-specific concept usage, geometric analysis) is genuinely novel and the dictionary scale is a practical contribution. The paper sits above "Emergent Geometry" (4.00) and "Unpacking SDXL Turbo" (4.40) due to richer empirical content and a clever theoretical observation. It sits below "Remapping" (6.50) and "Representation Geometry" (6.75) because those papers' central claims are backed by commensurate evidence. The closest comparison is "SAEs Find Highly Interpretable Features" (4.80), but this paper has more novel qualitative findings offset by a weaker central hypothesis. **Final score: 5.0.**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>