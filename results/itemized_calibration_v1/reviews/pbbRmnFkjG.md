Now let me write the final review with the calibrated score.

## Summary

This paper trains a 32,000-atom sparse autoencoder (SAE) on DINOv2-B activations to build a large-scale concept dictionary, then uses it to analyze how downstream tasks (classification, segmentation, depth estimation) recruit concepts. The analysis reveals three novel task-specific patterns: "Elsewhere" concepts for classification (conditional negation), exclusive border detectors for segmentation, and three families of monocular depth cues. The geometric characterization shows departures from the idealized Linear Representation Hypothesis (LRH). These findings motivate the Minkowski Representation Hypothesis (MRH) — that tokens behave as sums of convex regions around archetypal landmarks — which is connected theoretically to multi-head attention.

## Strengths

- **Large-scale concept dictionary for DINOv2.** Training a 32,000-atom SAE on DINOv2-B activations from 1.4M ImageNet-1K images with reconstruction R² > 88% is a substantial empirical effort that enables the subsequent analyses. This is a genuine resource for the vision interpretability community.

- **Novel task-specific concept recruitment analysis (Section 3).** The finding that different downstream tasks recruit largely disjoint, low-dimensional concept subspaces is genuinely informative. Three discovered patterns — "Elsewhere" concepts for classification (conditional negation), exclusive border detectors for segmentation forming coherent subspaces, and three families of monocular depth cues (projective, shadow-based, frequency transitions) — are empirically grounded and visually compelling. The depth cue analysis using controlled perturbations is a clever experimental design.

- **Careful geometric characterization (Section 4).** The comparison of the learned dictionary against random and Grassmannian baselines uses multiple appropriate diagnostics (pairwise coherence, singular-value spectrum, Hoyer scores, antipodal pairs, co-activation Gram matrix) that paint a consistent picture. The observation that positional features are dense yet low-norm, and that concept geometry is only weakly shaped by co-activation, are well-supported findings.

- **Theoretical connection between multi-head attention and Minkowski sums (Section 6).** Proposition 1 showing that attention's convex combination mechanism naturally yields Minkowski sum structure is mathematically sound and provides a clean formal link between architecture and representation geometry.

## Weaknesses

### Fatal
None.

### Major

- **MRH empirical support is disproportionately thin for the weight it carries.** The Minkowski Representation Hypothesis appears in the paper's title, abstract, and contributions list as a central offering. Yet the empirical evidence in Section 6 consists of ~5 qualitative sentences describing three tests on a single appendix figure (Fig. 26): straight-line vs. k-NN geodesic interpolation, Archetypal Analysis vs. SAE reconstruction, and Gram block structure. No quantitative reconstruction numbers, no baselines for the geodesic analysis, no statistical evaluation of the block structure are reported in the main text. The paper does frame MRH as a "working hypothesis" and the evidence as "preliminary," but the gap between the prominence of MRH (title, abstract, conclusion) and the thinness of its empirical support remains significant. This creates a mismatch: the paper presents MRH as a headline contribution while providing evidence more appropriate for a brief speculative discussion.

- **The claimed departures from LRH may be confounded with SAE architecture.** The observed "departures from LRH" (higher coherence, sharper spectral decay relative to Grassmannian baselines) are attributed to properties of DINOv2's representation. However, the SAE imposes strong geometric constraints: atoms are constrained to lie in conv(A) (the convex hull of real activations), the encoder uses non-negativity + BatchTopK sparsity (k=8 active codes per token out of 32,000 — an *extremely* sparse regime), and D is parametrized as D = SC with S row-stochastic. These constraints could themselves produce the observed deviations from a Grassmannian frame, even if DINOv2's activation space were LRH-compliant. The paper compares against random and Grassmannian baselines, but these are ideal mathematical distributions, not SAE-learned dictionaries under controlled conditions (e.g., trained on synthetic LRH-compliant data). Without disentangling whether the departures reflect properties of DINOv2's representation versus properties induced by the SAE's architecture, a central empirical claim is weakened.

### Minor

- **The transition from SAE-based analysis to MRH creates an unresolved conceptual tension.** Section 6 (Proposition 2) argues that Minkowski decomposition from final activations is non-identifiable. If decomposition is fundamentally ill-posed under MRH, the paper does not explicitly discuss why the SAE-based findings in Sections 2–4 should be trusted as revealing genuine structure. (The paper's implicit narrative — SAE operates under LRH; non-identifiability applies to MRH decomposition — is coherent but needs to be stated explicitly to avoid reader confusion.)

- **No discussion of how the sparsity level (k=8) affects the findings.** With only 8 active codes per token from 32,000 atoms, this is an extremely sparse choice. The observed departures from LRH (coherence, spectral decay) could vary with k. An ablation across different sparsity levels would help establish robustness.

- **No statistical uncertainty estimates for quantitative claims.** All quantitative claims — "intra-task concepts are significantly more aligned," spectrum comparisons, coherence comparisons — are reported as point values without confidence intervals, standard deviations, or significance tests. For an empirical characterization paper, this limits the reader's ability to assess reliability.

- **The "Elsewhere" concept causal claim lacks quantitative support.** The paper states that these concepts "vanish if the object is removed" via causal masking (citing Petsiuk et al. 2018 in a figure caption), but does not report how many images/classes were tested, what proportion of Elsewhere concepts show this behavior, or the effect size. This claim would benefit from systematic quantification.

- **No semantic validation of concept quality beyond reconstruction.** The dictionary is validated through reconstruction fidelity (R² > 88%) and qualitative visual inspection of top-activating patches. There is no human evaluation of concept interpretability, alignment with labeled semantic concepts, or test-retest reliability across SAE training seeds. Some systematic semantic validation would strengthen confidence that the atoms carve the representation at meaningful joints.

- **Depth cue families identified via specific perturbations, but generalization is unvalidated.** The perturbation analysis is clever but may produce clusters that are artifacts of the perturbation families rather than genuine feature groupings. No evidence is provided that the three identified families generalize beyond the specific perturbations used.

### Trivial
None beyond what is covered in Minor above.

## Nice-to-Haves
- Train SAEs with different sparsity levels (k = 4, 8, 16, 32) to test robustness of LRH-departure claims.
- Compare the stable SAE to a vanilla SAE to isolate the effect of the convex-hull constraint.
- Expand the MRH empirical validation with quantitative reconstruction metrics, baseline comparisons, and statistical evaluation, or reframe MRH as a brief speculative coda.
- Provide quantitative support for the Elsewhere-concept causal claim with systematic counts and effect sizes.
- Report variance or confidence intervals for key quantitative comparisons.

## Removed Points
These points are flagged as removed; treat them with caution:

1. **Reviewer's concern about Fel et al. (2025) citation status.** The reviewer wrote "this work may be contemporary or unpublished." Per hard rules, all cited works are assumed to exist. Removed.

2. **Reviewer's claim that the SAE/MRH tension is "structural" and "undermines coherence."** The paper has a coherent narrative (LRH operationalization → departures → MRH as alternative). Non-identifiability applies specifically to MRH decomposition, not to all decomposition. The reviewer's fatal/structural framing is overblown; demoted to Minor.

3. **Reviewer's claim that evidence is "dramatically insufficient" and that MRH is in the "paper's title, abstract, and conclusion as a central contribution."** The paper does frame MRH as a "working hypothesis" with "preliminary empirical evidence" and acknowledges this limitation. The criticism is legitimate in direction but the "dramatic" severity is somewhat tempered by the paper's own hedging. Kept as Major but with calibrated framing.

4. **Reviewer's "no systematic evaluation of concept quality" framed as a "significant gap" for a "paper whose central offering is a 'concept dictionary' for interpretability."** The dictionary is primarily a tool for the representation analysis, not the paper's end goal. However, some semantic validation would help. Demoted from "significant gap" to Minor.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Address the SAE/MRH transition explicitly: explain why SAE-based findings are informative about DINOv2's representation despite MRH's non-identifiability result.
- Add an ablation varying sparsity level k to test whether LRH-departure claims are robust to this choice.
- Provide quantitative evidence for the MRH empirical tests (reconstruction numbers, baselines, block-structure metrics) or reframe MRH as a brief speculative discussion.
- Add systematic quantification for the Elsewhere-concept causal claim (number of classes tested, proportion showing the effect, effect size).
- Add uncertainty estimates or confidence intervals for key quantitative comparisons.
- Consider restructuring the paper to foreground the SAE-based characterization (Sections 2–5) as the core contribution, with MRH presented as a forward-looking hypothesis rather than a headline result.

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison to this paper |
|------|-----------|-------|----------|--------------------------|
| imT03YXlG2.md — SAE on CLIP for visual concept remapping | 6.50 | Round 1 | Yes | Most topically similar. Both use SAEs on vision transformers to extract concepts; both criticized for qualitative-heavy analysis. Our paper has broader analysis (task recruitment, geometry, MRH) but similar issues with thin quantitative validation. Slightly weaker on MRH overreach but stronger on breadth of contribution. |
| Ch8s4FdUXS.md — SAE for text-to-image diffusion interpretability | 4.40 | Round 1 | Yes | Heavy criticism about limited scope, qualitative-heavy analysis, and cherry-picking. Our paper is stronger in analysis breadth and depth, and uses more rigorous baselines. Well above this anchor. |
| 9ca9eHNrdH.md — SAEs do not find canonical units of analysis | 7.00 | Round 1 | Yes | More focused and rigorous experiments addressing a clear question. Our paper is broader but less tightly executed. Below this anchor in experimental rigor. |
| bkdWThqE6q.md — Interpretable transformer for classification | 6.00 | Round 2 | No | Less directly relevant (architectural approach). Similar mid-range score. |
| 0ULf242ApE.md — Concept encoding in ICL | 6.00 | Round 2 | No | Concept analysis in LLMs, similar score range. |
| ih3BJmIZbC.md — Representational similarity via visual concepts | 6.80 | Round 2 | No | Visual concept analysis. Stronger quantitative evaluation. Slightly above our paper. |
| 1Njl73JKjB.md — Principled evaluations of SAEs | 7.00 | Round 2 | No | Rigorous SAE evaluation framework. More principled experimental design. Above our paper. |

**Bracket reasoning.** Round 1 bracketing placed the paper between 5.5 and 6.5 based on comparison with imT03YXlG2.md (6.50) and Ch8s4FdUXS.md (4.40). Round 2 narrowed using additional anchors in the 5.5–7.5 range. The paper is below the 7.00-level anchors (9ca9eHNrdH.md, 1Njl73JKjB.md) due to less rigorous experimental design and the MRH overreach, but above the 4.40 anchor (Ch8s4FdUXS.md) due to broader and more careful analysis. Compared to imT03YXlG2.md (6.50), this paper shares similar qualitative-heavy evaluation patterns and similar "strong claims with thin quantitative backing" criticisms, but has broader analysis scope. The MRH overreach is an additional weakness this paper has that the anchor does not. Final score of 6.0 reflects a borderline-accept paper with genuine contributions that is held back by the mismatch between the prominence of MRH and its evidence, and by the LRH confound that needs resolution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>