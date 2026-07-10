## Summary

This paper trains a 32,000-atom stable sparse autoencoder (SAE) on DINOv2-B activations to extract a concept dictionary, then uses it to characterize how different downstream tasks recruit concepts. The empirical core reveals: (i) classification uses "Elsewhere" concepts that fire off-object but depend on object presence, (ii) segmentation draws on border detectors forming coherent subspaces, and (iii) depth estimation relies on three monocular cue families (projective, shadow-based, frequency transitions). The paper documents how the learned dictionary departs from idealized Linear Representation Hypothesis (LRH) assumptions, and proposes the Minkowski Representation Hypothesis (MRH) as a geometric account where tokens lie in Minkowski sums of convex polytopes around archetypal landmarks.

---

## Strengths

- **Detailed empirical characterization of task-specific concept usage (Section 3).** The finding that classification, segmentation, and depth estimation recruit qualitatively different subsets of the concept dictionary — with "Elsewhere" concepts for classification, border concepts for segmentation, and three distinct monocular cue families for depth — is genuinely informative. The depth cue analysis (projective, shadow-based, frequency transitions) is striking given DINOv2 receives no 3D supervision, making this a nontrivial discovery about emergent representation structure. [favorability: 1.00]

- **Systematic documentation of departures from idealized LRH (Section 4).** The paper provides several quantitative diagnostics showing that the learned dictionary is more coherent, has sharper spectral decay, and is more task-clustered than a purely sparse, near-orthogonal picture would predict. The comparison to Grassmannian baselines (via TAAP) is well-motivated and goes beyond random baselines. These findings serve as concrete empirical grounding for theoretical discussions about real vs. idealized representations. [favorability: 1.00]

- **Scale and reproducibility of the analysis infrastructure.** Training a 32,000-atom stable SAE on DINOv2-B with R² > 88% reconstruction fidelity and releasing an interactive visualization is a non-trivial engineering contribution. The use of a stable SAE (constraining atoms to the convex hull of activations) is a principled choice addressing known reproducibility issues. [favorability: 1.00]

---

## Weaknesses

### Major

- **Abstract claims "object negation" for Elsewhere concepts stronger than evidence supports.** The abstract states that Elsewhere concepts "implement 'object negation'" without qualification. The body (Figure 2 caption) is more cautious, noting "another interpretation being distributed off-object evidence." The causal masking experiment shows the concept disappears when the object is removed, but this is also consistent with the concept firing on background textures that correlate with object presence — the paper does not control for this alternative. Calling this "negation" (a logical operation with negation semantics) is a much stronger claim than the evidence justifies. Since Elsewhere concepts are a marquee finding featured in the abstract, this overclaim matters. [favorability: 0.00]

- **MRH is elevated to a central contribution in the title and abstract, but the evidence remains preliminary.** The title ("TO MINKOWSKI GEOMETRY") and abstract give MRH co-billing with the empirical findings. However, Proposition 1 shows multi-head attention *can* realize MRH — a necessary condition that says nothing about whether it *does*. The three empirical tests (geodesic interpolation, archetypal analysis, Gram block structure) are consistent with MRH but also with other geometric accounts (e.g., any model where data lies on a curved manifold for geodesics, or non-linear embeddings more broadly). The paper internally frames MRH as "a working hypothesis" (which is appropriate), but the packaging inflates it to a co-equal contribution alongside well-supported empirical results. This creates a mismatch between what is claimed and what is supported. [favorability: 0.32]

### Minor

- **Distribution shift not discussed.** The SAE dictionary was trained exclusively on ImageNet-1K but is used to analyze ADE20K (segmentation) and NYU DepthV2 (depth) without acknowledging how this might bias concept discovery toward ImageNet-relevant features. Concepts useful for ADE20K boundaries or NYU depth cues may be under-represented in a dictionary learned purely from ImageNet. [favorability: 0.44]

- **Key caveat relegated to a footnote.** The observation that the weak correlation between Z^T Z and DD^T "may be an intrinsic property of linear reconstructive methods" (footnote 1, line 123) is a significant caveat — it means the weak correlation might be a methodological artifact rather than a substantive finding — and should appear in the main text. [favorability: 0.53]

- **No hyperparameter robustness analysis.** The results depend on SAE hyperparameters (k=8, c=32,000, training seed), but no sensitivity analysis is provided. The departures from LRH could partially reflect SAE training dynamics rather than genuine representation geometry. [favorability: 0.42]

- **Preliminary MRH empirical tests lack crucial baselines.** The geodesic interpolation result lacks a null model comparison beyond the straight-line vs. k-NN contrast. The Gram block structure is described qualitatively without quantifying block strength relative to shuffled baselines. These would strengthen the already-tentative evidence. [favorability: 0.42]

### Trivial

- The "largest interpretability demonstration for a vision foundation model to date" claim (abstract) is a comparative statement without supporting citation or comparison. [favorability: 0.00]

---

## Nice-to-Haves

- Present MRH as a speculation/discussion section rather than giving it top billing alongside well-supported empirical findings. The title and abstract would better reflect the paper's genuine contribution by foregrounding the empirical characterization.
- Strengthen the "Elsewhere" analysis by quantifying: (a) what fraction of ImageNet classes exhibit such concepts, (b) controlled experiments ruling out the "correlated background" alternative (e.g., showing the concept does *not* fire on background patches when the same background appears without the object).

---

## Removed Points

These points were removed from the original review; treat them with caution:

- **"Logical gap from LRH departures to MRH"** — The original harsh critic claimed the paper's narrative flows from "departures from LRH" to "therefore MRH" with a logical gap. However, the paper's language is explicitly tentative: "Guided by these departures, we propose" and "we advance a different view" — framing MRH as a proposal inspired by observations, not a deduction. Removed — mischaracterizes the paper.
- **"Proposition 2 implications underplayed"** — The paper devotes a full paragraph to discussing the non-identifiability limitation and suggests using intermediate architectural signals to mitigate it. The discussion is proportional for a hypothesis section. Removed — already addressed.
- **"Section 3 analysis is largely qualitative"** — The section provides quantitative validation (pairwise similarities, eigenvalue spectra, Figure 11 baselines) alongside qualitative visualizations. Removed — inaccurate characterization.
- **"Missing error bars / statistical rigor"** — Generic criticism; single-run evaluation without error bars is standard practice in this type of representation analysis. Removed — not a standard requirement for this work.

---

## Novel Insights

The key insight from reviewing this paper is that it contains two contributions of very different evidentiary weight bundled together under a single framing. The empirical core (Sections 2–5) — task-specific concept characterization, LRH departure documentation — is well-supported, genuinely informative, and stands on its own. The Minkowski Representation Hypothesis (Section 6) is presented transparently as a working hypothesis but the title, abstract, and introduction give it equal prominence. The paper would be significantly stronger if it aligned its packaging with the evidence: the empirical characterization is the real contribution; MRH is a speculative geometric interpretation that would need substantially more evidence to bear the weight the current framing gives it.

---

## Suggestions

1. **Reframe the abstract and title** to reflect the paper's primary contribution: an empirical characterization of DINOv2's concept space, with MRH as a working hypothesis offered for discussion — not a settled contribution.
2. **Qualify or remove the "object negation" claim** in the abstract, or add controlled experiments ruling out the "correlated background" alternative.
3. **Move footnote 1** (Z^T Z / DD^T correlation caveat) to the main text.
4. **Add a limitations paragraph** acknowledging the ImageNet-only SAE training for cross-domain analyses (ADE20K, NYU DepthV2).
5. **Add quantitative baselines** for the MRH empirical tests (null model for geodesics, quantified block structure scores vs. shuffled baselines).

---

## Score and Decision

**Score:** 7

**Decision:** Accept

**Rationale:** The paper's empirical core (task-specific concept characterization, LRH departure documentation) is solid, novel, and well-executed — supported by a large-scale engineering effort with strong reconstruction fidelity. The three strengths identified above all received maximum (1.00) favorability from the scoring model, indicating a genuinely strong contribution. The weaknesses are real but predominantly about overclaiming and presentation: the "object negation" abstraction (favorability 0.00) is the most serious issue, and the MRH framing (favorability 0.28–0.38) creates a mismatch between claims and support. However, neither weakness invalidates the empirical findings — they are fixable through reframing and qualification. The paper's genuine contribution (task-specific concept geometry in DINOv2, documented LRH departures, the analysis infrastructure itself) is sufficiently strong to warrant acceptance, with the expectation that the authors address the overclaiming issues in a revision.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>