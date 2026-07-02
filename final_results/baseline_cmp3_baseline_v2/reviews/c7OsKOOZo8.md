## Summary

This paper proposes an end-to-end multi-view diabetic retinopathy (DR) grading framework that generates lesion proposals internally via a Grade-Activated Lesion Proposal (GALP) module and performs cross-view fusion guided by a Lesion Expert Guided Regional Fusion (LGRF) module. The key idea is to use grade-conditioned evidence maps from stage-wise auxiliary classifiers to identify discriminative regions, treat them as surrogate lesion proposals, and fuse them across views using a mixture-of-experts mechanism with cross-view routing. Experiments on two multi-view datasets show that the method matches or surpasses several externally-informed baselines without requiring lesion or vessel annotations at inference.

## Strengths

- **Reduced annotation dependency**: The paper directly addresses a practical limitation of existing externally-informed methods by generating lesion-aware cues within the grading pipeline itself, removing the need for costly expert annotations at inference time while maintaining competitive accuracy.
- **Comprehensive evaluation**: The method is compared against a wide range of both end-to-end and externally-informed baselines on two multi-view DR datasets (MFIDDR and DRTiD), with results broken down by grade and metric.
- **Ablation study supports design choices**: Removing GALP or LGRF clearly degrades performance, and hyperparameter analysis on token retention ratio, number of experts, and number of activated experts provides insight into the trade-offs.
- **Cross-view fusion with selective attention**: The LGRF module’s design—routing only lesion proposals through gated experts and applying Top-K-weighted attention—is a well-motivated approach to focus computation on grade-relevant regions while suppressing background.

## Weaknesses

### Fatal
None.

### Major
1. **The claim that the selected regions are “lesion proposals” is not validated.** The paper uses CAM-like grade-conditioned evidence maps to select top-K regions and calls them lesion proposals. However, these regions are only discriminative for the grade classifier; they may correspond to artifacts, background patterns, or non-lesion anatomical structures. Without qualitative examples or comparison to real lesion segmentation masks, the premise that these are lesion-specific is unsupported. This overclaim weakens the core motivation of the paper.
2. **Backbone mismatch may confound performance comparisons.** The proposed method uses Swin-B, while many baselines (MVCINN, MVCNN variants, Binocular Network) use older CNN backbones (ResNet, VGG). The gains reported (e.g., 83.9% vs. 80.1% for MVCINN on MFIDDR) could partly come from a stronger feature extractor. The paper should include a baseline that uses the same Swin-B backbone with a simple fusion strategy (e.g., token concatenation or average) to isolate the benefit of GALP/LGRF.
3. **Auxiliary loss weight \(\lambda_{\text{aux}}=1\) is not justified.** The auxiliary loss is also a classification loss, but it operates on intermediate features; its weight relative to the main loss is set without ablation. A sensitivity analysis on \(\lambda_{\text{aux}}\) and \(\lambda_{\text{load}}\) is missing.

### Minor
- The “with lesion” variant uses SPADE to fuse lesion segmentation maps, but the integration is described only briefly. It is unclear whether this introduces extra parameters or training complexity compared to other externally-informed methods.
- On DRTiD, the method does not achieve the best AUC for every grade (e.g., Grade 1 AUC is lower than Cv-Transformer), and no statistical significance tests are reported.
- The hyperparameter analysis only shows accuracy; other metrics (F1, Kappa) could reveal different optimal settings.

### Trivial
- Some figure captions appear duplicated in the extracted text due to parsing artifacts.
- The notation uses superscripts and subscripts that are occasionally confusing (e.g., \(\mathbf{w}_{s_n,c}^{(s_n)}\)).

## Nice-to-Haves
- Qualitative visualizations of the top-K evidence regions overlaid on fundus images, with comparison to actual lesion segmentation masks, to substantiate the “lesion proposal” claim.
- Inference time or FLOPs comparison against baselines to assess computational cost of the MoE and cross-view attention.
- Ablation on the loss weights \(\lambda_{\text{aux}}\) and \(\lambda_{\text{load}}\) to verify that the chosen values are reasonable.

## Novel Insights
The paper demonstrates that grade-discriminative regions derived from intermediate auxiliary classifiers can serve as effective surrogates for expert lesion annotations in multi-view fusion, and that cross-view expert routing conditioned on the current view’s features provides a selective fusion mechanism that outperforms naive concatenation or full cross-attention. This insight is valuable for reducing annotation burdens in medical image analysis, though the claim that these regions are “lesion” proposals requires stronger evidence.

## Suggestions
- Add a qualitative study showing examples of the top-K regions from GEMs and compare them with available lesion segmentation masks (e.g., from MFIDDR) to support the lesion proposal interpretation.
- Include a stronger baseline that uses the same Swin-B backbone with a simple multi-view fusion (e.g., feature concatenation and a classifier) to measure the net gain from the proposed modules.
- Report confidence intervals or run multiple seeds for the main results to indicate statistical reliability.
- Consider renaming “lesion proposals” to “grade-discriminative region proposals” unless direct lesion correspondence is verified.

## Score and Decision
The paper makes a useful contribution by reducing annotation requirements for multi-view DR grading while maintaining strong performance. However, the lack of validation that the selected regions correspond to lesions and the potential confounding due to backbone choice are major concerns. The work is technically sound and the results are promising, but these weaknesses prevent a strong accept.

**Score**: 6.0  
**Decision**: Accept

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>