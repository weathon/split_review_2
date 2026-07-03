## Summary
This paper builds a 32,000-concept sparse autoencoder (SAE) dictionary for DINOv2-B using a stability-constrained method (D ∈ conv(A)), applies it to characterize task-specific concept recruitment for classification, segmentation, and monocular depth estimation, analyzes concept geometry to identify departures from the Linear Representation Hypothesis, and proposes the Minkowski Representation Hypothesis (MRH) as a geometry where token embeddings lie in Minkowski sums of convex polytopes realized by multi-head attention.

## Strengths
- **Largest SAE-based vision interpretability artifact to date**: The 32k-concept dictionary with R² > 88% reconstruction fidelity is a genuine contribution at scale; the stability-constrained design (D ∈ conv(A)) directly addresses known instability in vision SAEs (Paulo & Belrose, 2025; Papadimitriou et al., 2025).
- **Concrete and specific task-specialized findings (Section 3)**: "Elsewhere" concepts for classification (off-object activations that disappear when the object is removed via RISE masking, Figure 2 left) are a non-obvious and substantive observation implementing conditional negation. Border concepts for segmentation (all top-50 concepts localize to object contours across diverse ADE20K classes and cluster tightly in embedding space, Figure 2 right/Figure 10, with faster-decaying eigenspectrum than random subsets) are quantitatively corroborated. Three monocular depth cue clusters (projective geometry, shadow-based, frequency transitions) confirmed by controlled perturbations in Figure 3 align with visual neuroscience categorization.
- **Honest geometric accounting (Section 4)**: The paper reports dictionary coherence exceeding both random and Grassmannian baselines (Figure 4A), sharply decaying singular values (Figure 4B), and only weak correlation between co-activation geometry and dictionary geometry (Figure 13), leading honestly to MRH motivation rather than selectively confirming LRH.
- **Appropriately scoped theoretical framing**: MRH is explicitly labeled a "working hypothesis" in the title, abstract, and Discussion, with testable predictions listed and non-identifiability (Proposition 2) openly acknowledged.

## Weaknesses

### Fatal
None.

### Major
- **Proposition 1 is a near-tautology and does not substantiate MRH as a validated framework**: Proposition 1 shows that multi-head attention outputs lie in a Minkowski sum of per-head value polytopes. This follows directly from the definition of attention and holds for *any* standard transformer, regardless of what DINOv2 has learned. The non-trivial MRH claims — that the decomposition is *sparse*, *interpretable*, and *semantically structured* — are not addressed by Proposition 1. The paper provides three empirical tests: (i) k-NN geodesic paths stay near the data support (consistent with a manifold, not specifically Minkowski polytope structure); (ii) ~10 AA archetypes match SAE reconstruction (explained by low intrinsic dimensionality); (iii) block structure in code Grams (consistent with MRH but also with clustered factor models). These tests appear primarily in the appendix and are insufficient to establish MRH as a principled advance over LRH. The paper's framing in Sections 6–7 — presenting MRH as a better account of DINOv2 geometry than LRH — goes beyond what the evidence supports.
- **Non-identifiability (Proposition 2) undermines stated practical implications without adequate resolution**: Proposition 2 establishes that the Minkowski decomposition is non-unique from final activations alone. This directly undermines MRH implications (i) ("concepts as landmarks") and (ii) ("archetypal steering admits a strict maximum"), which implicitly require access to the individual polytope factors. The one-paragraph resolution ("exploiting intermediate signals and per-head outputs") is suggestive but does not close the gap.

### Minor
- **Task alignment score definition entirely deferred to appendix**: Section 3 states "the precise definition and its theoretical justification are deferred to Appendix C.1," yet this score is the analytical backbone of all task-specific quantitative results. At least a compressed definition belongs in the main body.
- **No main-body comparison of stable vs. naive SAE stability**: Stability is cited as the primary motivation for the SAE design, but no ablation showing concept overlap across independent runs (stable vs. naive) appears in the main body. The claim of "reproducible, geometrically faithful dictionaries" is asserted rather than demonstrated within the paper.
- **Speculative causal claim about steering plateaus**: Section 6 (implication ii) states MRH "helps explain why SAE-style steering plateaus." Steering plateaus also occur in LRH models for independent reasons; presenting this as an MRH-specific explanation requires evidence not provided.

### Trivial
None.

## Nice-to-Haves
- A more targeted empirical test distinguishing MRH from LRH would substantially strengthen Section 6: e.g., checking whether concept activation boundaries are sharp (consistent with polytope faces) or gradual as a function of interpolation path through activation space — this would transform suggestive signals into diagnostic evidence.
- Moving the three MRH empirical tests from the appendix into the main body, with effect sizes and explicit LRH-consistent baselines, would allow readers to evaluate the evidence directly.
- A brief main-body ablation (concept overlap across runs, stable vs. naive SAE) to substantiate the stability claim.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Concern about "causal" language for RISE perturbation**: The critic raises this, but the paper already uses careful language: "evidence suggestive of a causal effect." No weakness warranted.
- **"Largest interpretability demonstration" claim needs hedging**: Minor scope-of-definition issue; the paper's claim is plausible given cited work. Removed as a nitpick.
- **Comment that "PCA cannot fabricate curvature" is too strong**: The critic flags this passage but it is stated correctly in the paper. Not a weakness.

## Novel Insights
The paper's most genuinely novel observation is the "Elsewhere" concept phenomenon: off-object activations in classification that vanish when the focal object is removed, suggesting learned conditional negation rather than straightforward object or background detection. This challenges attribution-map interpretations that assume localized feature fire at the labeled token. The tripartite depth cue structure (projective/shadow/frequency) emerging from controlled perturbation in a model trained without 3D supervision is a clean and reproducible empirical result with direct neuroscience connections. The non-identifiability result (Proposition 2) is an underappreciated structural limitation of any Minkowski-based interpretability framework and deserves wider attention.

## Suggestions
- Restructure Section 6 to explicitly distinguish what follows from the architectural tautology (Proposition 1) versus what requires empirical validation. Label implications (i–iii) accordingly so readers can assess which are earned.
- Add a compressed task alignment score definition in Section 3 (one equation, one sentence) so the quantitative results are self-contained.
- Add a brief main-body ablation (concept overlap across two independent SAE runs, stable vs. naive variant) to substantiate the stability motivation.
- Develop a sharper empirical test specifically distinguishing MRH from LRH: examine whether interpolation paths exhibit sharp activation boundaries (polytope faces) vs. smooth gradients (consistent with linear directions).

---

## Score and Decision

### Calibration Anchors

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| `tcsZt9ZNKD.md` | 8.20 | R1 | SAE scaling paper for LLMs — larger scope, but less domain-specific interpretability content than this paper |
| `Wxl0JMgDoU.md` | 2.50 | R1 | Chess SAE paper — narrower setting, weaker findings, no theoretical framework |
| `89wVrywsIy.md` | 3.40 | R1 | Hierarchical circuit tracing with SAEs — weaker methodology and contributions than this paper |
| `Ch8s4FdUXS.md` | 4.40 | R1 | SAE for SDXL Turbo (text-to-image) — comparable scale but less specific/novel task-specialized findings |
| `F76bwRSLeK.md` | 4.80 | R1 | SAE for LLM features (foundational study) — influential but less sophisticated analysis than this paper |
| `ghH6YYDs15.md` | 4.67 | R1 | Theoretical analysis of SAE amortization gap — narrower scope |
| `J9eKm7j6KD.md` | 4.80 | R1 | Control vectors for motion transformers — narrower and weaker claims |
| `imT03YXlG2.md` | 6.50 | R1 | PatchSAE for CLIP ViT — closest analog: vision SAE with task analysis; this paper has broader and more novel findings |
| `9ca9eHNrdH.md` | 7.00 | R1 | SAE canonicality analysis — focused, clean argument; comparable quality to this paper's empirical sections |
| `XAjfjizaKs.md` | 6.50 | R1 | Multi-layer SAE for residual stream — focused, clean methodology, similar caliber |
| `1Njl73JKjB.md` | 7.00 | R1 | Principled SAE evaluation framework — rigorous methodology, arguably more methodologically tight |
| `I4e82CIDxv.md` | 8.00 | R1 | Sparse feature circuits — clean causal framework, actionable, strong execution |
| `2dnO3LLiJ1.md` | 8.00 | R1 | Vision Transformers Need Registers — clean, impactful, directly actionable findings |
| `5Ca9sSzuDp.md` | 8.00 | R1 | Interpreting CLIP via text decomposition — tight, actionable, specific findings directly comparable to this paper |

**Round 1 bracket**: 5.5 – 7.0. The paper has genuine strengths (scale of SAE, specific task-specialized findings, honest geometry analysis) that clearly place it above the 4.4–4.8 band of SAE papers with weaker findings. The MRH weakness (tautological proposition, thin empirical validation, unresolved non-identifiability) prevents it from reaching the 7.5–8.0 band occupied by papers with clean, actionable findings and rigorous methodology.

**Round 2 narrowing**: The closest comparators are `imT03YXlG2` (PatchSAE for CLIP, avg 6.5), `9ca9eHNrdH` (SAE canonicality, avg 7.0), and `XAjfjizaKs` (multi-layer SAE, avg 6.5). This paper's empirical Section 3 findings are more specific and novel than `imT03YXlG2`; its theoretical ambition exceeds `XAjfjizaKs` but the MRH section is substantially weaker than the clean contributions of the 7.0-band papers. The two major weaknesses (tautological proposition, unresolved non-identifiability) weigh against a 7.0 score. Final score: **6.0** (borderline accept).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>