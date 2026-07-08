## Summary

This paper operationalizes the Linear Representation Hypothesis (LRH) in DINOv2 by training a stable sparse autoencoder (SAE) with 32,000 concept atoms — the largest interpretability demonstration for a vision foundation model to date. Using this dictionary, the paper characterizes task-specific concept utilization (classification's "Elsewhere" concepts, segmentation's border detectors, depth estimation's monocular cue families), documents geometric departures from idealized LRH predictions (higher coherence, sharp spectral decay, antipodal pairs), and proposes the Minkowski Representation Hypothesis (MRH) as a formal alternative in which token embeddings arise from convex mixtures of archetypal landmarks.

---

## Strengths

- **Large-scale, reproducible concept dictionary release.** Training a 32k-atom stable SAE on DINOv2 and releasing it with an interactive demo is a concrete resource contribution. The scale claim ("largest interpretability demonstration for a vision foundation model to date") appears substantiated relative to prior work.

- **Genuinely novel empirical finding: "Elsewhere" concepts.** Section 3's discovery that classification tasks recruit concepts firing off-object yet object-dependent is the most striking result in the paper. The observation that these vanish under causal masking is non-trivial and suggests a learned negation mechanism that, if confirmed, would be an important architectural discovery.

- **Depth cue decomposition is well-executed.** The perturbation analysis in Section 3 — using median blurring, edge-preserving smoothing, and high-pass filtering to isolate shadow, projective, and frequency-based depth cues — is a creative and disciplined experimental design that yields clean, interpretable clusters. The finding that three cue families emerge without any 3D supervision is substantive.

- **MRH is a well-motivated and formally grounded hypothesis.** The departure from LRH is documented with multiple converging diagnostics (coherence, spectral decay, task-aligned clusters, dense positional signals). The formal definition (Definition 1) and the connection to multi-head attention (Proposition 1) are mathematically sound and connect naturally to established convex geometry results and prior work on conceptual spaces. This is more than speculation — it is a genuinely testable alternative.

---

## Weaknesses

### Major

- **The causal evidence for "Elsewhere" concepts is too thin to support the prominent claim.** The abstract states concepts "implement object negation" and the contributions list says "implement learned negation," but the evidence amounts to a single sentence in the main text (line 79) and a figure caption. No quantitative details are provided: sample size, how object removal was performed (inpainting? masking? cropping?), effect size, statistical tests, or how many concepts/ImageNet classes were tested. The caption hedges ("another interpretation being distributed off-object evidence"), but the abstract and contributions do not reflect this nuance. This is a significant mismatch between rhetorical prominence and evidential support.

- **The empirical evidence for MRH is too preliminary for a concept named in the title.** The empirical section (one paragraph, lines 163–164) presents three measurements — k-NN geodesics, Archetypal Analysis, Gram matrix block structure — all referenced to figures in the appendix, with no error bars, statistical comparisons, or quantification of key claims. For example, "AA matches or exceeds SAE reconstruction" is stated without reporting AA's actual R² (SAE achieves R² > 88%). While the paper appropriately calls MRH a "working hypothesis" in the abstract, the evidence provided in the main text is insufficient to establish it as a core contribution; the framing exceeds what is demonstrated.

- **The critique of LRH via Grassmannian comparison is partially confounded by the SAE's own constraints.** Dictionary atoms are constrained to lie in the convex hull of real activations (D = SC with S row-stochastic), so they are not free to be maximally incoherent like Grassmannian frames — they inherit the anisotropy of the activation space. A Grassmannian frame is the optimal packing on a sphere, but DINOv2 activations are not on a sphere. The departures from LRH may reflect SAE inductive biases rather than properties of DINOv2's representations. The paper acknowledges this only obliquely (footnote 1) but does not grapple with it as a limitation for the central argument that LRH is insufficient.

### Minor

- **The paper says "Multi-head attention directly implements this construction" (abstract), but Proposition 1 shows that attention outputs *admit* MRH representations (i.e., *can* be represented in MRH form), not that DINOv2 actually *uses* MRH.** This is a meaningful difference in register that overstates what is proven.

- **The sparsity level k=8 is not motivated or ablated.** At k=8 active codes out of 32k per token (~0.025% of the dictionary), many geometric findings (coherence, spectral decay, Hoyer scores) could be sensitive to this choice. There is no discussion of how k was selected or what the impact would be at different sparsities.

- **Task-specific analyses lack statistical quantification.** "Classification draws from a broader span" — how much broader? "Intra-task concepts are significantly more aligned" — what is the significance test? The paper reports differences without confidence intervals, p-values, or effect sizes. Since the SAE was trained on 1.4M images with 261 tokens each, almost any difference will be statistically significant, but the reader needs to know *how large* these effects are.

- **The per-image PCA analysis in Section 5 is entirely qualitative with no quantitative metric of smoothness or alignment.** Similar PCA visualizations are well-known from prior DINO work (Oquab et al., 2023); the novel contribution (projecting out the positional subspace) would benefit from a quantitative measure.

- **The Discussion (Section 7) is brief and does not acknowledge the limitations identified above** (SAE confounding, thin MRH evidence, Elsewhere causal evidence).

### Trivial

None.

---

## Nice-to-Haves

- Replace or supplement the Grassmannian baseline with a null model trained on the same activation data but with SAE constraints relaxed (e.g., varying sparsity levels k, no convex-hull constraint) to distinguish properties of DINOv2's representations from SAE inductive biases.
- Provide quantitative SAE-independent tests for MRH — e.g., fit Archetypal Analysis directly on raw DINOv2 activations and report reconstruction quality with error bars.
- Elaborate the Elsewhere causal experiment with sample sizes, methodology details (inpainting vs. masking), effect sizes, and number of classes tested.

---

## Removed Points

These points from the input review were removed after verification:

- **"No SAE quality evaluation beyond R²... no comparison of the learned dictionary against alternative SAE formulations"** — The paper's stated scope is not a comprehensive SAE benchmark but an application of SAE to characterize DINOv2. Requesting exhaustive SAE architecture comparisons is scope creep for this paper. The stable SAE is a published method; the paper appropriately cites it.
- **Logical tension ("the SAE dictionary is itself an LRH-motivated factorization... this is not circular")** — The reviewer acknowledges the argument is not circular, and the paper explicitly steps "beyond the SAE lens" in Section 5 with SAE-independent per-image PCA. The concern is noted but not a structural weakness.
- **"No quantification of task-specific subspace dimensionality"** — The paper states task subspaces are low-dimensional (fast spectral decay) and shows this visually; explicit dimensionality numbers would strengthen the paper but their absence is not a major weakness.
- **Missing related works** — Cannot be verified without external sources.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Recalibrate the Elsewhere claims.** Either (a) provide rigorous causal evidence with sample sizes, effect sizes, and methodology, or (b) hedge the abstract and contributions to match what is actually demonstrated ("evidence suggestive of conditional negation" rather than "implements object negation").

2. **Either substantially expand the MRH empirical section or recalibrate its prominence.** If MRH remains in the title, the main text needs quantitative evidence with error bars. Alternatively, frame MRH explicitly as a discussion/speculative hypothesis (consistent with "working hypothesis" language) and match the paper's rhetoric to that framing.

3. **Acknowledge the SAE confounding issue explicitly as a limitation** in the Discussion and, ideally, provide a control experiment (e.g., varying SAE constraints to show the geometric findings are robust).

4. **Motivate or ablate the sparsity level k** to assure readers that the geometric findings are not artifacts of the specific sparsity regime.

---

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| imT03YXlG2.md (SAE reveals visual concepts in CLIP) | 6.50 | R1+R2 | Yes | Most similar: SAE+ViT concept dictionary. Our strengths are stronger (higher weights), our worst negatives are milder. |
| Ch8s4FdUXS.md (Unpacking SDXL Turbo) | 4.40 | R1 | No | Less comprehensive scope, limited to single diffusion model. Our paper is substantially stronger. |
| 1Njl73JKjB.md (Principled Evaluations of SAEs) | 7.00 | R1 | Yes | More rigorous evaluation framework but different focus. Our paper's claims-to-evidence ratio is weaker. |
| 9ca9eHNrdH.md (SAEs Do Not Find Canonical Units) | 7.00 | R2 | Yes | Strong methodological contribution with clear experiments. Not directly comparable to empirical characterization. |
| fmWVPbRGC4.md (Local vs distributed representations) | 5.67 | R2 | Yes | Limited novelty, single network, rejected. Our paper has stronger technical contributions. |

**Bracket determination (Round 1):** 5.5–7.5. The paper is far stronger than 1.0–3.0 band papers and the 4.40 anchor (limited scope). It does not match the methodological rigor of 7.0+ papers (e.g., SAE evaluation paper).

**Narrowing (Round 2):** Comparing weighted items against the closest anchor (imT03YXlG2, 6.50): our strengths (max weight 11.48 vs. 10.71) are stronger and our most negative weaknesses (-0.86 and -0.19 vs. -2.90) are milder. However, the gap between central claims and evidence for both Elsewhere concepts and MRH prevents the paper from reaching the 7.0+ tier.

**Final score: 6.5, Accept.** The paper's empirical characterization of DINOv2's concept space is substantive, and the MRH proposal is a genuinely novel theoretical perspective. The primary weakness is a mismatch between rhetorical framing and evidential support in two places (Elsewhere causal claims, MRH evidence). These issues are addressable through recalibration of claims or expanded experiments.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>