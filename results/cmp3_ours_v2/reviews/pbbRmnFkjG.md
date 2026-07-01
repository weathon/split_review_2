Now I have all the information I need. Let me finalize the review.

## Summary

This paper trains a stable sparse autoencoder (SAE) on DINOv2-B to produce a 32,000-unit concept dictionary and uses it to study how downstream tasks (classification, segmentation, depth estimation) recruit concepts. It reports several genuinely interesting findings: "Elsewhere" concepts for classification that fire off-object and vanish when the object is removed, segmentation relying exclusively on boundary-detector concepts, and three families of monocular depth cues (projective, shadow-based, frequency transitions) identified via controlled perturbations. After documenting departures from a pure sparse, near-orthogonal view of representations, the paper proposes the Minkowski Representation Hypothesis (MRH) as an alternative geometry where tokens are Minkowski sums of convex polytopes.

## Strengths

- **Genuinely interesting and non-obvious task-specific findings.** The discovery of "Elsewhere" concepts (Section 3, Figure 2), the observation that segmentation's top-50 concepts are all boundary detectors forming a coherent subspace, and the identification of three monocular depth cue families via controlled perturbations (Figure 3) are concrete, interpretable results that advance understanding of how DINOv2 works internally. These are the kind of specific findings that the interpretability community needs.

- **Large-scale concept dictionary as a community resource.** The 32,000-atom dictionary trained with a stable SAE (convex-hull constraint, R² > 88% reconstruction) represents a substantial methodological and practical contribution. The scale and the in-distribution guarantee (atoms constrained to the convex hull of real activations) distinguish this from prior concept extraction efforts for vision models.

- **Proposition 1 is a clean formal observation.** Showing that each attention head's output lies in a convex combination of its values and that multi-head summation yields a Minkowski sum provides a direct architectural grounding for the MRH, connecting the hypothesis to a concrete mechanism in ViTs. Proposition 2's acknowledgment of non-identifiability is a useful intellectual discipline.

- **Intellectual honesty about alternative interpretations.** The paper notes the alternative interpretation of "Elsewhere" concepts as "distributed off-object evidence" (Figure 2 caption) and explicitly acknowledges (footnote 1) that the co-activation-geometry correlation may be an artifact of linear reconstructive methods.

## Weaknesses

### Fatal
None.

### Major

- **MRH is presented as a central contribution (title, abstract, Section 6) but its empirical support in the main text consists entirely of qualitative, non-quantified claims.** The three "empirical evidences" in Section 6 (lines 163-164) are: (i) "straight-line interpolation... only the latter remain near the data support" — no metric or comparison reported; (ii) "with about ten archetypes per image AA matches or exceeds SAE reconstruction" — no reconstruction quality numbers (R²? MSE?), no comparison values; (iii) "clear block structure" in the Gram matrix — no quantitative measure (silhouette score, modularity score). All three reference Figure 26 in the appendix. For a hypothesis that appears in the paper's title and is presented as the culminating contribution, this is insufficient. Proposition 1 is an architectural-capacity observation (not evidence that the trained model *actually* uses this geometry), and Proposition 2 is a caution about non-identifiability, not positive evidence.

- **Key empirical claims in the strongest part of the paper (Section 3) are supported primarily by qualitative examples, with quantitative results deferred to the appendix.** The Elsewhere concept "vanishes if the object is removed" via causal masking (line 79) is asserted without reporting any quantitative result (effect size, percentage of variance explained, comparison to a null model). The claim that tasks recruit concepts with "minimal overlap" (line 65) is never given a concrete fraction. The depth cue clustering claim (Figure 3) lacks any quantitative cluster-separation metric (silhouette score, adjusted Rand index). The paper acknowledges an alternative interpretation for Elsewhere concepts in the figure caption but states the stronger interpretation in the main text.

- **No stability or sensitivity analysis for the central methodological tool.** The SAE is the backbone of all analysis in Sections 2–5, but the paper provides no demonstration that the 32,000-concept dictionary is stable across training seeds, initialization, or data subsampling — despite citing the SAE stability literature (Paulo & Belrose, 2025). Similarly, there is no analysis of how the key findings depend on hyperparameter choices (k=8 active codes, c=32,000 atoms).

- **No comparison to alternative concept extraction methods.** Concept extraction via SAE is one approach (operationalizing LRH). The paper does not compare to PCA, ICA, non-negative matrix factorization, or other dictionary learning methods. This makes it difficult to assess whether the findings are specific to SAE-based decomposition or reflect genuine properties of DINOv2's representations.

### Minor

- **The "Elsewhere" concept interpretation as "conditional negation" / "object negation" (abstract, Figure 2 caption) goes beyond what the evidence supports.** The paper itself acknowledges "distributed off-object evidence" as an alternative in the caption, yet asserts the stronger claim prominently. A more measured framing would better serve the paper.

- **Footnote 1 is a significant caveat for Section 4's geometric claims.** Acknowledging that the co-activation-geometry correlation "may be an intrinsic property of linear reconstructive methods" undermines some of the departures-from-LRH claims, but this caveat is buried in a footnote rather than discussed prominently.

- **The "largest interpretability demonstration for a vision foundation model to date" claim conflates scale with validation.** A 32,000-atom dictionary is large, but interpretability is demonstrated through rigorous validation (e.g., human rating studies, concept description accuracy), not dictionary size alone.

### Trivial
None.

## Nice-to-Haves

- Bring at least one MRH empirical test into the main text with full quantitative results (the AA-vs-SAE comparison is the most promising candidate).
- Report concrete overlap percentages between task-recruited concept sets and cluster separation metrics for depth cue families.
- Add SAE stability analysis across training seeds and brief hyperparameter sensitivity checks.
- Either reposition MRH as a discussion/hypothesis or substantially strengthen its empirical evidence in the main text.

## Removed Points

- **"The paper's two main contributions are in unresolved tension"** — The paper's narrative is a coherent progression: SAE operationalizes LRH, findings reveal departures from LRH, which motivate MRH as a better-fitting geometry. The SAE is used as a tool; the paper acknowledges its limitations. This is a standard scientific narrative, not a contradiction.
- **"No systematic evaluation of concept interpretability" as a fatal flaw** — Downgraded to minor (see Minor #3). Most concept-based interpretability papers at ICLR rely on qualitative examples; the critical missing element is quantitative support for the *claims* made from these examples, not a human evaluation study per se.
- **Various formatting/style nitpicks, reproducibility concerns about undisclosed hyperparameters, and missing appendix content** — Removed per hard rules (parser artifacts, not author errors; missing appendix is a parser issue, not a paper problem).
- **Pure speculation presented as weaknesses** (e.g., "assuming Y is the case… could this be problematic?") — Removed as unfounded speculation.

## Novel Insights

The most interesting structural insight from the reviews is that this paper has a clear "split personality" problem: its strongest contribution is the task-specific empirical findings (Section 3), but it frames itself around the MRH (title, abstract, Section 6) which is currently the weakest part. This is an unusual inversion — typically papers overclaim on implications, not on the theoretical framing of an otherwise solid empirical study. The resolution is straightforward: reposition MRH as a discussion/hypothesis and elevate the empirical findings as the main contribution. The paper's actual value lies in what it *found* about DINOv2's representations, not in the theoretical framework it proposes for them.

## Suggestions

1. Either substantially strengthen the MRH empirical case in the main text (at minimum, move one quantitative test with full numbers into Section 6) or reposition MRH as a discussion/hypothesis section rather than a central contribution. The current title promises more than the evidence delivers.
2. Report concrete quantitative numbers for the main empirical claims: task overlap fractions, actual cosine similarity values (not just "higher than random"), effect sizes for the Elsewhere masking experiment, and cluster separation metrics for the depth cue families.
3. Add a brief SAE stability demonstration (2-3 training seeds, measure dictionary overlap) and note whether the task-specific findings are sensitive to k and c choices.
4. Tone down the "Elsewhere as conditional negation" framing or balance it more prominently with the acknowledged alternative interpretation.
5. Move the key quantitative results currently relegated to the appendix (Figures 9, 10, 11) into the main text with numerical values.

## Score and Decision

**My calibration bracket:** Round 1 placed the paper in the 5.5–7.5 range against human-reviewed anchors. I inspected the closest topical anchor — "Sparse autoencoders reveal selective remapping of visual concepts during adaptation" (avg 6.50, accepted, similar SAE-on-ViT methodology) — and found it has comparable weaknesses (qualitative evidence, no hyperparameter sensitivity) but a cleaner narrative without an overclaimed theoretical framework. A second anchor, "Unpacking SDXL Turbo: Interpreting Text-to-Image Models with Sparse Autoencoders" (avg 4.40, rejected), was less ambitious and had less interesting findings. The paper under review has more novel empirical findings than either but also a more significant overclaiming problem (MRH in title, absent from main-text evidence). I also inspected "A Simple Interpretable Transformer for Fine-Grained Image Classification" (avg 6.00, accepted) and "Sparse Autoencoders Find Highly Interpretable Features in Language Models" (avg 4.80, accepted with an outlier). The paper under review sits between these — its empirical contributions are real and valuable, but the MRH overclaiming and lack of quantitative support for key claims pull it down.

**Final score determination:** The paper's empirical findings are genuinely novel and would benefit the community. However, the MRH overclaiming (title-level contribution with no quantitative evidence in main text) and the reliance on qualitative support for the paper's most interesting claims are significant weaknesses. The paper would clearly be stronger with revisions, but as submitted it does not fully deliver on its framing. I place it between the 4.40 (rejected) and 6.50 (accepted) anchors I inspected — closer to the 6.50 paper in terms of contribution novelty but pulled down by the framing-evidence mismatch.

**Calibration anchors consulted:**
- imT03YXlG2.md (avg 6.50, accepted) — Similar SAE-on-ViT concept analysis; cleaner narrative but less ambitious findings. This paper's findings are more novel.
- Ch8s4FdUXS.md (avg 4.40, rejected) — SAE on text-to-image models; less ambitious and less interesting findings than the paper under review.
- F76bwRSLeK.md (avg 4.80, accepted with outlier) — SAE for LLM interpretability; comparable methodology applied to different domain.
- bkdWThqE6q.md (avg 6.00, accepted) — Interpretable transformer for image classification; different approach but same community standards.
- tcsZt9ZNKD.md (avg 1.75 aggregate, individual scores 3,10,10,8,10) — SAE scaling paper; not directly comparable.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>