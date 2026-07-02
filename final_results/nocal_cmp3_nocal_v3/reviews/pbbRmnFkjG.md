Here is the final consolidated review:

---

## Summary

This paper trains a stable sparse autoencoder (SAE) on DINOv2-B to obtain a 32,000-atom concept dictionary, then analyzes how downstream tasks (classification, segmentation, depth estimation) recruit different concept subsets. It finds functional specialization — e.g., "Elsewhere" concepts for classification, boundary detectors for segmentation, three monocular-cue families for depth — and documents geometric properties of the dictionary (coherence, spectral decay, antipodal pairs) that challenge a purely sparse, near-orthogonal view. Motivated by these departures, it proposes the Minkowski Representation Hypothesis (MRH), in which token embeddings are Minkowski sums of convex polytopes around archetypal landmarks, and shows that multi-head attention constructively realizes this geometry.

## Strengths

- **Task-specific concept recruitment analysis (Section 3) is novel and well-supported.** The identification of "Elsewhere" concepts (off-object activations that vanish when the object is removed), border detectors forming coherent subspaces for segmentation, and three families of monocular depth cues (projective, shadow-based, frequency transitions) is the kind of specific, falsifiable finding that moves SAE interpretability beyond feature dashboards toward functional organization. Each finding is backed by quantitative evidence (eigenspectrum decay, intra-task cosine similarity, perturbation analysis).

- **Proposition 1 (multi-head attention realizes MRH) is a clean theoretical observation.** Showing that each attention head outputs a convex combination of its values and that multi-head summation yields a Minkowski sum connects MRH directly to the architecture, giving it mechanistic plausibility beyond pure geometric intuition. Lemma 1 and Lemma 2 (deferred to Appendix K) provide formal grounding.

- **The paper is intellectually honest about the limits of its evidence.** MRH is repeatedly called a "working hypothesis"; the empirical signals are described as "preliminary"; Proposition 2 explicitly states the non-identifiability problem; Footnote 1 calls out a mathematical constraint on one of the paper's own claims. This framing discipline is maintained throughout and gives the reader a clear sense of where the authors believe stronger evidence is needed.

## Weaknesses

### Major

- **MRH receives disproportionate structural weight relative to its empirical support.** The hypothesis appears in the title, dominates the abstract, occupies an entire section (Section 6) with a formal definition and two propositions, and is presented as a co-equal contribution alongside the empirical analysis. Yet the empirical evidence for MRH in the main text consists of a single paragraph citing three analyses (straight-line vs. k-NN geodesics, AA vs. SAE reconstruction, Gram block structure) that are all relegated to Figure 26 in the appendix. The theoretical connection (Proposition 1) is genuine, but the gap between the prominence of the hypothesis and the thinness of its evidence creates an expectation mismatch. This is fixable by demoting MRH to a focused discussion/speculation section or by adding substantially more empirical validation to the main text.

- **The claim that "concept geometry is only weakly shaped by co-activation" (Section 4) is not properly supported and is undercut by the paper's own math.** Footnote 1 shows that the correlation between \(Z^T Z\) and \(DD^T\) is "roughly proportional to \(\text{tr}(A^T A) \propto \text{cov}(A)\), which is guaranteed to be positive" — meaning there is an unavoidable mathematical floor on the correlation from the reconstruction identity \(A \approx ZD\). The paper says the correlation is "weak" but never reports its actual value, never specifies what "weak" means relative to this mathematical baseline, and never tests whether the observed correlation is distinguishable from what any linear reconstruction would produce by construction. The conclusion may be correct, but the evidence as presented cannot support it without addressing this baseline.

### Minor

- **The SAE's sparsity prior conflates the tool with the object of study.** The SAE enforces k=8 active codes out of 32,000 — a strong sparsity constraint. The paper then finds that the resulting dictionary has heavier-tailed coherence, sharper spectral decay, and task-aligned clusters than a Grassmannian baseline, and attributes these departures to DINOv2's representation space. But these patterns could reflect properties of the SAE's learned dictionary under its particular training objective rather than properties of DINOv2's actual activation space. The paper acknowledges this tension (stepping "beyond the SAE lens" in Section 5) but never runs a control — e.g., training an SAE on random features with the same sparsity constraint — to check which patterns are specific to DINOv2.

- **The alignment score (Section 3), which is the quantitative backbone of the task-recruitment analysis, is fully deferred to Appendix C.1 with no summary definition in the main text.** This makes the central quantitative claims of Section 3 non-self-contained.

- **Reconstruction fidelity (R² > 88%) is reported without specifying training vs. held-out data.** This matters for assessing whether the dictionary generalizes beyond its training distribution.

- **No comparison to simpler decomposition methods (PCA, NMF, ICA) for the same analyses.** This would help determine whether the SAE provides unique insight or reproduces patterns any linear method would find.

### Trivial

- **Variance across SAE training seeds is not reported.** The paper cites the stable SAE (Fel et al. 2025) for reproducibility but does not report whether key geometric patterns (coherence, spectral decay, task alignment) are consistent across runs.

## Nice-to-Haves

- Run a control SAE on random Gaussian data (matched dimensionality and sparsity level) to distinguish DINOv2-specific patterns from generic SAE artifacts.
- Address the co-activation/geometry correlation baseline: report the actual correlation value and compare it to the mathematical floor identified in Footnote 1.
- Compare task-recruitment and geometric analyses against simpler decompositions (PCA, NMF, ICA) to contextualize the SAE's added value.
- Include a brief summary of the alignment score definition in the main text for self-containedness.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"No human or automated evaluation of concept interpretability."** The paper's contribution is geometric analysis of representation structure, not building an annotated concept library. The "largest interpretability demonstration" refers to the scale of the dictionary and interactive visualization, not to a formal human-grounded evaluation. This criticism demands scope outside the paper's stated goals.

2. **The "Strengthening the Paper on Its Own Terms" section from the input review.** These are editorial restructuring suggestions, not weaknesses. The relevant substantive concerns (correlation baseline, SAE confound, MRH framing) are already captured above.

## Novel Insights

The reviews surface a genuine tension that the paper itself identifies but does not resolve: the SAE is both the tool that enables the analysis and a potential source of confounding inductive biases. The paper uses a method that enforces extreme sparsity (k=8/32,000) to produce findings that challenge the sparse-coding view, but never fully disentangles whether the observed "departures from LRH" are properties of DINOv2's representation or artifacts of the SAE's optimization. The co-activation/geometry correlation issue (Footnote 1) further reveals a subtle mathematical floor on a claim the paper asserts as an empirical finding — a good-faith acknowledgment that actually undermines the claim's interpretability. None of these issues invalidate the paper's strongest contributions (the task-specific concept analysis in Sections 3–5), but they prevent the paper from cleanly transitioning from empirical findings to the proposed hypothesis.

## Suggestions

- Restructure the paper so that MRH is presented as a concluding discussion/speculation rather than as a co-equal contribution alongside the empirical analysis. The empirical findings in Sections 3–5 are strong enough to carry the paper on their own.
- Report the actual correlation value for the co-activation/geometry analysis and explicitly compare it against the mathematical floor identified in Footnote 1.
- Add a paragraph in Section 2 or 4 acknowledging the SAE sparsity confound with more specificity, explaining which conclusions are robust to it and which patterns are likely DINOv2-specific.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>