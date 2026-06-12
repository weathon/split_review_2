Now I have sufficient calibration data to finalize the score. Let me write the final review.

## Summary
This paper trains a 32,000-atom stable SAE on DINOv2-B, releasing what is billed as the largest interactive interpretability demo for a vision foundation model. Using this dictionary, the authors analyze how downstream tasks (classification, segmentation, depth estimation) recruit different concepts, revealing functional specialization including "Elsewhere" concepts for classification, border detectors for segmentation, and three families of monocular depth cues. The paper then examines the statistics and geometry of the concept dictionary, finding departures from idealized sparse-linear assumptions (higher coherence, sharp spectral decay, task-aligned clustering). Motivated by these findings, the authors propose the Minkowski Representation Hypothesis (MRH)—that token embeddings are Minkowski sums of convex polytopes around archetypal landmarks—supported by a theoretical connection to multi-head attention and preliminary empirical evidence.

## Strengths
- **Task-specific concept analysis with causal perturbation**: Section 3 identifies "Elsewhere" concepts that fire off-object yet depend on the object's presence, with evidence from causal masking. This goes beyond correlational analysis to suggest a learned negation mechanism in DINO's concept dictionary — a genuinely novel empirical finding about how the model represents negation.
- **Perturbation-based decomposition of depth cues**: The controlled perturbation methodology (median blurring, edge-preserving smoothing, high-pass filtering) isolates three functionally distinct clusters of depth-related concepts (projective geometry, shadow-based, frequency transitions), showing that DINO learns interpretable 3D perception primitives without explicit 3D supervision. The use of systematic perturbation rather than correlation-only analysis makes this more principled than typical concept attribution studies.
- **Formal connection between multi-head attention and Minkowski sums (Proposition 1)**: A clean theoretical observation that each attention head outputs a convex combination of its values, and multi-head outputs sum to a Minkowski sum of projected head polytopes. This provides a formal bridge between the attention mechanism and convex geometry that is independent of whether the full MRH holds empirically.
- **Non-identifiability theorem (Proposition 2)**: Proves that Minkowski decompositions of final activations into constituent polytopes are generically non-unique due to support-function additivity. This has practical implications for interpretability: it implies that single-layer concept extraction is fundamentally underdetermined and that architectural intermediate signals are necessary for unique decomposition.
- **Quantitative diagnostics against proper baselines**: Section 4 compares the dictionary against Grassmannian (TAAP) and random baselines on multiple metrics (pairwise coherence, singular-value spectrum, Hoyer scores), providing concrete quantitative evidence for departures from the sparse near-orthogonal ideal rather than just showing anecdotal examples.
- **Clean separation of positional and semantic structure**: Section 5 tracks positional decoding accuracy across layers, showing compression to a ~2D sheet, and demonstrates that projecting out the positional subspace leaves per-image PCA structure largely intact — providing a methodological template for disentangling positional from semantic organization in future work.

## Weaknesses

### Major
- **MRH evidence is too thin for the weight placed on it**: The three empirical tests for MRH are all deferred to Figure 26 in the appendix and described only briefly (lines 163-164). (i) Geodesic vs. straight-line interpolation is consistent with any non-linear manifold embedding, not specifically MRH. (ii) Archetypal Analysis matching SAE reconstruction tests whether data lies in a convex hull—a *weaker* condition than the full MRH with tiled polytopes and block-convex codes, and corresponds only to the |S|=1 special case. (iii) "Clear block structure" in Gram matrices is stated without any quantitative metric. The paper presents MRH as a "working hypothesis" (line 9, 141), which is intellectually honest, but the abstract and introduction frame it more assertively as an established alternative ("advance a different view," "tokens are formed by combining convex mixtures..."). Proposition 1 is a correct formal observation about attention but does not provide empirical evidence that DINOv2's representations *actually instantiate* this geometry. The imbalance between the boldness of the MRH claims and the thinness of the supporting evidence is the paper's most significant weakness.

- **The paper tests an overly narrow version of LRH and overstates what the evidence shows**: The paper equates LRH with "sparse, quasi-orthogonal directions" (line 9, 29) and tests this against a Grassmannian frame baseline. However, the core LRH claim in the cited literature (Elhage et al. 2022; Park et al. 2024) is that features correspond to *linear directions in activation space* — sparsity and near-orthogonality are recognized design goals for minimizing interference, not definitional commitments. The paper's finding of higher coherence than a Grassmannian baseline and a sharply decaying SVD spectrum does not refute the central LRH claim (features as linear directions); it only challenges a specific idealization about incoherence. The conclusion that these results "question a purely sparse-coding view of representation" (line 9, 34) is appropriately scoped, but the abstract's framing that they reveal "departures from LRH" (line 9) conflates the operationalization (Grassmannian frames) with the hypothesis itself.

- **No SAE baseline comparison**: The RA-SAE's reconstruction quality (R² > 88%) is reported, but there is no comparison to a standard TopK SAE or other common SAE variants at the same dictionary size and sparsity level. Without this, the reader cannot assess whether the RA-SAE's design choices (convex hull constraint, BatchTopK) are beneficial or neutral. The "stability" advantage of RA-SAE is claimed (line 43: "they face a persistent challenge in stability... To address this, we adopt a stable SAE") but no stability metrics (e.g., Jaccard overlap of top-activating examples across random seeds) are reported, making this claim unverifiable.

- **Circularity tension between SAE framing and anti-LRH argument**: The paper operationalizes LRH via an SAE dictionary (Section 2: "If the LRH is valid, then concept extraction amounts to an overcomplete dictionary learning problem"), then uses findings from this SAE to argue against LRH. The paper acknowledges this tension ("We therefore step beyond the SAE lens," line 109) and does move to model-native token geometry in Sections 5-6. However, the SAE-based findings in Section 4 (higher coherence, spectral decay, etc.) are still used as primary evidence motivating MRH, and the independent validation in Section 6 is too preliminary to break the circularity. The paper would be stronger if it more carefully separated SAE-dependent claims from SAE-independent ones.

### Minor
- **Qualitative claims need quantification**: Descriptions like "Across many ImageNet classes" (Elsewhere concepts, line 79), "all the concepts among the top-50 consistently localize along object contours" (segmentation, line 81), and "visibly tight cluster" (border concepts, line 81) are based on visual inspection without reported statistics (e.g., fraction of classes showing the Elsewhere pattern, silhouette scores, inter-rater agreement). These qualitative interpretations are interesting and worth reporting, but the paper would benefit from quantitative support.

- **Stability metrics for RA-SAE not reported**: The RA-SAE's main claimed advantage is stability (line 43). No stability metrics (e.g., Jaccard similarity of top-activating examples across random seeds, feature overlap rates) are provided, making it impossible to verify this claimed advantage.

- **Proposition 2 (non-identifiability) is not a unique limitation of MRH**: The observation that Minkowski decomposition is non-unique from final activations alone is mathematically correct (line 167-168), but sparse dictionary learning also yields non-unique decompositions in general. The practical significance specific to MRH (versus LRH-based SAE approaches) could be clarified; the conclusion that "estimating individual concept contributions... from final activations alone is underdetermined" (line 173) applies to both frameworks.

- **"Elsewhere" concept causal claim is overstated**: The abstract states Elsewhere concepts "implement" object negation (line 9, 33), and the body says "indicating a conditional negation" (line 79). The evidence is correlational activation patterns plus a causal masking perturbation. The figure caption's parenthetical ("another interpretation being distributed off-object evidence," line 51) is more measured but undercuts the stronger body text claims. A causal intervention (steering or ablating the concept to affect classification behavior) would be needed to substantiate the "implement" language.

### Trivial
None.

## Nice-to-Haves
- Causal validation of Elsewhere concepts: steering or ablating along the concept direction to test whether it causally affects classification behavior.
- Quantitative analysis of how many ImageNet classes exhibit the Elsewhere pattern and what fraction of top-k concepts per class are of this type.
- Silhouette or Davies-Bouldin scores for the border concept cluster relative to random baselines, to quantify the "visibly tight cluster" claim.
- Ablation showing how results change at different layers of DINOv2 (all experiments use the final layer).

## Removed Points
These points were flagged by reviewers but are removed from the main review for the reasons stated below. Treat them with caution if referenced elsewhere.

- **"Circular logic" framed as fatal/structural**: The Harsh Critic called this a "structural" critical issue. However, the paper does acknowledge this tension (line 109: "We therefore step beyond the SAE lens") and moves to model-native token geometry in Sections 5-6. The criticism is retained as **Major** (not Fatal) because the paper partially addresses it and the empirical findings have value independent of the LRH-vs-MRH framing debate. A fatal flaw must be unambiguous given what is on the page; this one is acknowledged and partially addressed.
- **LRH as "straw man"**: Retained as **Major** but reframed as testing an overly narrow version of LRH rather than a "straw man." The paper does cite Park et al. (2024) for its definition; the issue is about the scope of what the evidence actually challenges.
- **"Proposition 2's practical significance is unclear — the same is true for any dictionary learning method"**: Retained as **Minor** since the non-identifiability result is still meaningful for practitioners, even if it's not unique to MRH.
- **Missing appendix/supplementary material criticisms**: Removed per instructions — the parser strips appendices; they exist in the original submission.
- **Formatting, typo, and style nitpicks**: Removed per instructions — these are parser artifacts, not author errors.
- **Questions about model/data release status**: The paper states "will be publicly released upon acceptance" — standard pre-release statement. Removed per Hard Rules.
- **Strength Finder: Generic strengths about "important problem" or "addressed significant question"**: Removed — these are generic and not specific to the paper's evidence. Only concrete, citation-anchored strengths are retained.

## Novel Insights
The most novel observation emerging from this review that is not fully articulated in the paper itself is the **mismatch between the paper's empirical architecture and its rhetorical architecture**. The paper's strongest empirical contribution — the discovery that different downstream tasks recruit distinct low-dimensional subspaces from a shared SAE dictionary — stands independently of the LRH-vs-MRH theoretical debate. The task-specific concept analysis (Section 3) is a clean demonstration that the functional organization of DINOv2's representational space is task-aligned and low-dimensional, which is interesting regardless of whether the underlying geometry is sparse-linear or Minkowski. Yet the paper packages this finding as ammunition in a theoretical debate where neither side has decisive evidence. Detaching the empirical discovery from the theory debate would yield a stronger, more defensible paper.

## Suggestions
1. **Restructure to separate empirical contributions from theory**: The task-specific concept analysis (Section 3) and geometric diagnostics (Section 4) are the paper's strongest contributions. Consider presenting them as the main empirical findings, and reposition the MRH as a concluding "Discussion / Future Directions" section rather than a culminating contribution.
2. **Add standard SAE baselines**: Compare the RA-SAE against a standard TopK SAE at the same dictionary size on reconstruction fidelity (R²), and report stability metrics (Jaccard overlap across seeds). Without this, the tool contribution is difficult to evaluate relative to the existing SAE literature.
3. **Quantify qualitative claims**: Provide statistics for the Elsewhere concept prevalence (fraction of ImageNet classes), silhouette scores for border concept clusters, and inter-rater agreement for the depth cue family classification.
4. **Sharpen the LRH discussion**: Acknowledge explicitly that the evidence targets the near-orthogonal/sparse idealization of LRH rather than the core linearity claim. The paper's diagnostics regarding coherence and spectral decay are interesting findings about DINOv2's geometry; they don't need to be framed as refuting LRH to be valuable.
5. **Strengthen or reposition MRH evidence**: Either (a) provide quantitative metrics for the three empirical tests (e.g., reconstruction error vs. number of archetypes, geodesic vs. straight-line path deviation statistics, Gram block clustering scores) or (b) explicitly reframe MRH as a "geometric lens" with testable predictions for future work, removing the implication that it is already empirically established.

## Score and Decision

**Calibration Anchors Retrieved (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| gwZ90hFSL2 (cross-lingual robotics) | 1.00 | R1 bracketing | Much weaker — not a valid research paper; does not apply here |
| 5lUdTogEL3 (person re-id) | 1.00 | R1 | Much weaker; unrelated topic |
| wZiH43e5Ah (concept extraction framework) | 3.00 | R1 | Similar topic (concept-based explainability) but less ambitious scope and thinner empirical content |
| ky2JYPKkml (multi-modality concept space) | 3.00 | R1 | Similar topic; our paper has richer empirical findings and a more ambitious theoretical proposal |
| HXwrppoSPc (COMiX compositional explanations) | 3.25 | R1 | Similar vein; our paper has more extensive experiments |
| jGGylopiO8 (geometry estimation benchmarking) | 4.75 | R1 | Different topic but similar score neighborhood; technically competent but limited novelty |
| Ch8s4FdUXS (SDXL Turbo SAE interpretability) | 4.40 | R1, R2 | **Most directly comparable** — SAE on vision model with similar methodology. Our paper has more findings and a theoretical proposal, but also more speculative framing. SDXL paper was rejected. |
| 4aJg9e4nvF (what ViTs learn) | 4.75 | R1 | Similar topic (ViT analysis); our paper is more systematic but also more speculative |
| F76bwRSLeK (SAEs find interpretable features) | 4.80 | R2 | Similar SAE methodology on language models; accepted but with wide score spread. Our paper has richer downstream task analysis. |
| OeHSkJ58TG (Incidental Polysemanticity) | 5.67 | R2 | Theoretically clean paper on interpretability; rejected despite clear contribution. Our paper has more empirical breadth. |
| imT03YXlG2 (SAE concept remapping during adaptation) | 6.50 | R1 | **Stronger paper** — clean SAE-on-vision study with well-scoped claims and solid execution. Our paper is more ambitious but less rigorous. |
| 9ca9eHNrdH (SAEs don't find canonical units) | 7.00 | R1 | **Stronger paper** — clear negative result with rigorous experiments. Our paper's theoretical proposal is more speculative. |
| 1Njl73JKjB (principled SAE evaluations) | 7.00 | R1 | **Stronger paper** — careful methodology with ground-truth evaluations. Our paper lacks this level of evaluation rigor. |

**Round 1 bracket:** 4.0 – 6.0 (the paper is substantially better than the 3.0-level concept extraction papers, but less rigorous and more speculative than the 6.5+ SAE papers)

**Narrowing to final score:** Within this bracket, the paper sits below cleanly-executed SAE papers like "Sparse autoencoders reveal selective remapping" (6.50) because the MRH claims outrun the evidence and key baselines are missing. It sits above papers like "Unpacking SDXL Turbo" (4.40) and "What do vision transformers learn" (4.75) because the task-specific concept analysis is more systematic and reveals genuinely novel phenomena (Elsewhere concepts, three depth cue families). The paper's empirical contributions are real and interesting, but the framing overreaches significantly.

**Final Score: 5.5**

This is a borderline paper with genuine empirical contributions (task-specific concept subspaces, geometric diagnostics, Proposition 1) that are undermined by a theoretical framing that substantially overclaims what the evidence supports. The MRH is presented as a culminating contribution but supported by only preliminary evidence. With restructuring to separate the solid empirical findings from the speculative theory, and with added baselines and quantification, the paper could be substantially stronger. In its current form, the contribution is real but the framing requires major revision.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>