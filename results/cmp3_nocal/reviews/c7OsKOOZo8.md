## Summary

This paper proposes an end-to-end framework for multi-view diabetic retinopathy (DR) grading that generates lesion proposals internally (via GALP) rather than relying on costly external annotations. A second module, LGRF, uses a gated mixture-of-experts with Top-K-weighted cross-view attention to fuse these proposals across views. Evaluated on two multi-view DR datasets (MFIDDR, DRTiD), the method achieves competitive accuracy against both end-to-end and externally-informed baselines, with an ablation study confirming the contribution of each proposed module.

## Strengths

- **Well-motivated problem and clear framing.** The paper correctly identifies the practical drawbacks of externally-informed multi-view DR methods (annotation cost, workflow complexity, brittleness from upstream model errors) and targets reducing this dependence. This is a genuine need.

- **Ablation study controls for backbone.** Table 4 holds the Swin-B backbone constant and shows that removing GALP drops accuracy from 83.9% to 82.7%, removing LGRF drops it to 82.3%, and removing the expert pool drops it to 82.6%. The magnitudes (~1–1.6% absolute) are modest but consistent across all four metrics (Acc, Spe, Kappa, F1), providing credible evidence that the proposed modules contribute *within the chosen architecture*.

- **Hyperparameter analysis is informative and supports design choices.** Fig. 3 shows interpretable patterns: retaining 50% of tokens as proposals outperforms both keeping all tokens (dilution) and keeping too few (information loss); activating K₂=2 experts in a pool of M=6 provides the best trade-off. These sweeps support the paper's central premise that selective proposal-based fusion is beneficial and that performance is not overly sensitive to precise tuning.

- **Method description is clear and well-specified.** The GALP and LGRF modules are described with sufficient mathematical detail (Equations 1–20), and the data flow through the four-stage architecture is clearly traceable in Section 3.

## Weaknesses

### Major

- **Backbone confound undermines the SOTA comparison.** The method uses Swin-B, a substantially stronger backbone than the ResNet50/VGG19/ViT architectures used by most baselines in Tables 1 and 3. The 2.4% gap over the best end-to-end baseline (ETMC, 81.5%) and the 0.3% gap against WGLIN (84.2%) could partially or entirely arise from the backbone advantage. No experiment isolates how much the reported gains come from the proposed modules vs. the backbone upgrade. The paper does not include a baseline that matches the backbone (e.g., Swin-B with standard multi-view fusion).  
  *Note: the DRTiD comparison against CrossFIT (75.6% vs. 76.0%) is less affected since both use Swin-B pretrained on EyePACS, but the other baselines on DRTiD still use different backbones.*

- **No qualitative validation that GALP proposals correspond to lesions.** The paper repeatedly interprets the Top-K selected regions as "lesion proposals" (Section 3.2: *"regions with higher activation... are more likely to contain lesion evidence"*; Conclusion: *"transforms grade-conditioned evidence maps into lesion proposals, which act as surrogates for costly expert cues"*). However, no heatmaps, no comparison with ground-truth lesion masks (which the MFIDDR dataset provides, per line 185), and no failure-case analysis are provided. The CAM-based selection picks regions most predictive of the grade by the auxiliary classifier — these could be lesions, but could also be brightness artifacts, optic disc pallor, or any other discriminant pattern correlated with grade. The paper's central narrative rests on this interpretation, but it remains untested.

- **No variance or statistical significance reported.** All results in Tables 1–4 and Fig. 3 are point estimates with no confidence intervals, standard deviations, or mention of how many runs were performed. Given the small margins involved (0.3% against WGLIN, 1.2–1.6% ablation drops, 0.4% over CrossFIT), we cannot distinguish meaningful differences from random seed variation. On a test set of ~2,584 eyes, a 0.3% difference could arise from a single seed.

### Minor

- **Adjacent-only cross-view fusion is not justified or ablated.** For N=4 views, fusion is restricted to a ring topology (view 1↔2, 2↔3, 3↔4, 4↔1) as stated in line 123. The paper does not ablate alternative fusion patterns (e.g., fusing with all views), even though this architectural constraint could limit the cross-view interaction that LGRF is designed to enable.

- **Weak "w/o LGRF" ablation baseline.** The ablation removes the fusion module entirely and simply concatenates lesion proposals with cross-view tokens (line 286). A stronger control would replace LGRF with standard multi-head cross-attention (no MoE, no Top-K weighting), isolating the benefit of the expert-routing mechanism. As designed, the 1.6% drop conflates the removal of learned fusion with the removal of MoE routing.

- **No computational cost comparison.** The method adds auxiliary classifiers at stages 1–3, an MoE pool of 6 Transformer experts with 2 activated per step, cross-view attention at each of 4 stages, and load-balancing regularization. No parameter counts, FLOPs, or inference times are reported versus baselines. For a method with clear architectural overhead, this omission weakens the practical contribution assessment.

### Trivial

None.

## Nice-to-Haves

- A simple baseline of Swin-B with standard multi-view fusion (e.g., concatenation + GAP + classifier, or average cross-view pooling) would directly control for the backbone advantage and clarify what the proposed modules add.
- Qualitative visualization of GALP-selected regions overlaid on fundus images, compared to available lesion segmentation masks on MFIDDR, would directly validate (or refute) the "lesion proposal" interpretation.
- Reporting results over 3 random seeds with mean and std would address the variance concern, especially given the small margins.

## Removed Points

These points were flagged in the input review but are removed per the filtering criteria:

- **"External annotations break end-to-end training is overstated"** — The reviewer argues that methods like CVSA still train end-to-end. However, the paper's broader point (inference requires external inputs, increasing workflow burden and brittleness) is well-supported in the introduction. This is a framing nuance, not a substantive weakness.
- **"No code is released"** — Code release at submission time is not standard practice for ICLR (it is typically provided at publication). This is a reproducibility expectation that applies post-acceptance, not a review weakness.
- **"Missing related works"** — Not verifiable without external sources; removed per instructions.
- **"Abstract claim about micro-lesions is overblown"** — This was not raised as a distinct criticism but as an implicit concern; the reviewer does not anchor it to a specific sentence that can be verified as unsupported.

## Novel Insights

None beyond the paper's own contributions. The review surface does not surface a contradiction or synthesis that goes beyond what the paper already states.

## Suggestions

1. **Add backbone-controlled comparisons.** Re-implement the strongest end-to-end competitor (e.g., ETMC) using Swin-B as a drop-in backbone, or at minimum add a "Swin-B + GAP + classifier" baseline to Table 1. This single addition would resolve the most consequential ambiguity in the evaluation.

2. **Add qualitative visualizations.** Overlay GALP's Top-K selected regions on fundus images and compare with available ground-truth lesion masks from MFIDDR. Even a small set of illustrative examples would substantially strengthen the claim that these proposals correspond to clinically meaningful structures.

3. **Report variance estimates.** Provide results over 3 random seeds with means and standard deviations for the main tables. This is critical given the small margins.

4. **Ablate the adjacent-view fusion constraint.** Compare the current cyclic scheme against full pairwise fusion to either justify or relax this design choice.

5. **Report computational cost.** Include parameter counts and inference time for the proposed method versus key baselines.

---

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>