## Summary
This paper trains a stable sparse autoencoder on DINOv2-B's final-layer activations to produce a 32k-concept dictionary, then studies how downstream tasks (classification, segmentation, depth estimation) recruit these concepts. It finds functional specialization — including "Elsewhere" concepts for classification (off-object yet object-dependent), border detectors for segmentation, and three monocular cue families for depth. The geometric analysis reveals departures from idealized Linear Representation Hypothesis (LRH) predictions (higher coherence than Grassmannian baselines, sharp spectral decay, task-aligned clustering). Motivated by these observations, the paper proposes the Minkowski Representation Hypothesis (MRH): tokens lie in Minkowski sums of convex polytopes around archetypal landmarks, with multi-head attention as a natural realization mechanism. MRH is presented as a working hypothesis with preliminary evidence and testable predictions.

## Strengths
- **32k-concept dictionary as a resource contribution.** The paper provides (by its own claim) the largest concept-level interpretability demonstration for a vision foundation model, releasing the dictionary and an interactive visualization. This is a genuine asset for the community regardless of how the dictionary is used or interpreted.
- **Task-specific concept analysis reveals non-trivial functional specialization.** The breakdown across three tasks is the paper's strongest empirical contribution. The "Elsewhere" concept for classification (off-object firing that depends causally on the object's presence) is a genuinely interesting and non-obvious finding that surfaces a failure mode for standard attribution methods. The border-concept subspace for segmentation and the three monocular depth cue families (projective, shadow, frequency) are concrete, interpretable discoveries validated across tasks.
- **The MRH is a well-motivated theoretical framing.** Proposition 1 (multi-head attention's output as a Minkowski sum of convex sets) is a clean mechanistic observation connecting architectural structure to geometric predictions. The paper correctly identifies that this yields testable implications (bounded steering, non-identifiability of decomposition) and is transparent about MRH being a working hypothesis rather than a validated theory.
- **Model-native token geometry analysis (Section 5).** The per-image PCA maps and positional subspace analysis provide complementary evidence independent of the SAE, showing that DINOv2's token embeddings exhibit smooth, low-dimensional structure not explained by positional encoding alone.

## Weaknesses

### Fatal
None.

### Major
- **Geometric departures from LRH are diagnosed on the SAE dictionary without validation against DINOv2's raw activation space.** The core evidence that DINOv2 departs from LRH (higher coherence than Grassmannian baselines, sharp spectral decay, heavy-tailed pairwise similarities) comes entirely from the SAE dictionary. While Section 5 steps beyond the SAE to examine model-native token geometry (per-image PCA, positional subspace), this analysis does not directly verify whether the specific LRH-departure claims (coherence, spectral statistics) replicate in the raw activation space. Without this validation, it remains unclear whether the observed geometric patterns reflect genuine properties of DINOv2's representations or SAE training artifacts (sparsity constraint k=8, non-negativity, optimization trajectory). This gap weakens the empirical motivation for moving from LRH to MRH. The paper would be substantially strengthened by running the same coherence and spectral diagnostics on raw DINOv2 activations.

- **No quantitative validation of the dictionary beyond reconstruction fidelity.** The paper reports R² > 88% for reconstruction, but this alone does not establish that the 32k concepts correspond to meaningful or stable features. Standard diagnostics such as downstream probe performance using SAE features vs. raw features, concept consistency across training seeds, or interpretability evaluations (e.g., do individual atoms respond to coherent visual patterns?) are absent. Without them, the reader cannot assess whether the dictionary is a valid basis for the geometric analysis that follows.

### Minor
- **The MRH empirical evidence is thin and deferred.** The three empirical tests (straight-line vs. k-NN geodesics, AA vs. SAE reconstruction, Gram block structure) are described in a single paragraph referencing an appendix figure, with no quantitative results in the main text. The paper does not compare MRH against LRH on any direct metric. This is acceptable given that MRH is presented as a "working hypothesis" (the paper is transparent about this), but the imbalance between the space devoted to MRH framing and the empirical support for it is notable. The paper's observational contributions do not depend on MRH being correct.

- **The "Elsewhere" causal claim is slightly over-stated in the body text.** Line 79 states concepts "vanish if the object is removed, indicating a conditional negation." The figure caption (line 51) hedges appropriately ("suggestive of a causal effect… another interpretation being distributed off-object evidence"), but the body text does not match this caution. The causal masking experiment is only referenced, not described with quantitative results in the main paper.

- **Key geometric comparisons lack effect sizes and quantitative specificity.** Throughout Section 4, comparisons are described qualitatively: "higher coherence than random or Grassmannian baselines" (by how much?), "spectrum decays sharply" (what decay rate?), "correlate only weakly" (what ρ?). The figures contain this information but the text would benefit from reporting a few summary statistics (mean coherence, spectral decay exponent, correlation coefficient) to let readers assess effect magnitudes directly.

- **No hyperparameter sensitivity analysis.** The dictionary is trained with k=8 active codes out of 32k (0.025% sparsity) and c=32,000 atoms. The paper does not discuss how the results in Sections 3–4 depend on these choices. Different sparsity levels or dictionary sizes could materially change the observed geometry.

- **Single model, single layer.** All analysis uses the final [CLS] token of DINOv2-B. DINOv2's distinctive self-distillation training (iBOT + DINO heads with 128k prototypes) may produce representation properties specific to this architecture. The paper acknowledges this (line 179) but does not discuss whether the findings might be layer-specific or architecture-specific.

### Trivial
None.

## Nice-to-Haves
- Testing at least one MRH prediction directly on DINOv2 activations (e.g., steering saturation at landmarks) would transform MRH from a motivated speculation to a testable claim.
- Sensitivity analysis varying k (sparsity) and c (dictionary size) would strengthen the geometric conclusions.
- Quantifying the fraction of total activation energy accounted for by the three dense positional outliers would clarify their significance.
- A parallel analysis on an intermediate layer (e.g., layer 6 or 9) would help establish whether the observed properties are layer-specific.

## Removed Points
These points are flagged by the reviewer as potentially problematic but are removed with justification:

1. **"The conv(A) constraint by construction prevents atoms from being maximally separated and will naturally produce higher pairwise coherence."** — This specific claim is technically incorrect. The constraint D ∈ conv(A) keeps atoms in-distribution but does not force higher coherence: if DINOv2's activations were near-Grassmannian, conv(A) would contain near-orthogonal vectors and the SAE could find them. The presence of higher coherence reflects either a genuine property of DINOv2's geometry or an SAE training artifact (from sparsity/non-negativity/optimization), not the conv(A) constraint itself. The broader concern about SAE artifacts is valid and retained as a Major weakness above.

2. **"The paper would need to either (a) validate the dictionary against model-intrinsic features… or (b) test MRH predictions on model activations directly. It does neither."** — This is inaccurate. Section 5 explicitly attempts (a) by examining model-native token geometry (per-image PCA, positional subspace, token sheets) independent of the SAE. The concern is that this analysis does not directly validate the *specific* LRH-departure claims of Section 4, which is a different (and valid) criticism retained above.

3. **"Proposition 2 (non-identifiability) undercuts the paper's own project."** — The paper acknowledges this limitation and positions it as a call for structure-aware tools using intermediate signals rather than final activations alone. This is a feature of the framing, not a flaw.

4. **"Proposition 1 describes the forward pass of any ViT — it is not specific to DINOv2."** — True, but the paper uses Proposition 1 to motivate MRH as a general geometric consequence of multi-head attention, not as evidence specific to DINOv2. This is appropriate framing.

5. **"All quantitative evidence deferred to figures 10–11 in the appendix"** — Standard practice for page-limited conference papers; the main text provides sufficient qualitative framing and the appendix is available for details.

6. **"PCA claims observational without quantification"** — PCA is used as a qualitative visualization tool in this context (per-image token geometry), which is standard practice. Quantifying correspondence to segmentation masks would be a nice addition but is not required for the qualitative claim being made.

## Novel Insights
The most valuable observation from the review process is the concrete, verifiable gap between the SAE-based geometric claims and the model-native analysis. The Section 4 claims (higher coherence, sharp spectral decay) are treated as evidence against LRH, but the Section 5 analysis (per-image PCA smoothness, positional subspace) works at a different granularity and does not directly support or refute the coherence/spectral claims. A single experiment — computing pairwise coherence and spectral statistics on raw DINOv2 activations (or on the token set A itself, before SAE factorization) — would either validate or refute the paper's central empirical motivation for MRH. This is a well-scoped, actionable experiment the authors could run in a day.

## Suggestions
- Run the coherence and spectral diagnostics from Section 4 directly on DINOv2's raw activation matrix A (not the SAE dictionary D) to verify that the departures from LRH are intrinsic to the model rather than SAE artifacts. If they replicate, the motivation for MRH is substantially strengthened.
- Add a few summary statistics (mean/median coherence, spectral decay coefficient, correlation ρ for co-activation vs. geometric affinity) to the main text so readers can assess effect sizes without zooming into density plots.
- Tone down the "Elsewhere" body text claim to match the caption's hedging, or cite the quantitative causal masking results.
- Include a brief discussion of sensitivity to the sparsity parameter k and dictionary size c.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>