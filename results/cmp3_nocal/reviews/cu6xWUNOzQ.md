## Summary

This paper introduces a nonlinear multimodal encoding model for speech fMRI, combining text features from LLaMA and audio features from Whisper through PCA dimensionality reduction followed by a single-hidden-layer MLP. The approach achieves moderate but consistent improvements over linear baselines, and the authors introduce a Relative Error Difference (RED) metric for spatiotemporal clustering analysis. The work addresses an underexplored direction—nonlinear multimodal encoding in speech fMRI—with a clean ablation design that isolates the contributions of nonlinearity, dimensionality reduction, and multimodality.

## Strengths

- **Addresses a genuine gap.** Nonlinear multimodal encoding for naturalistic continuous speech fMRI is under-explored compared to vision, and the paper provides the first systematic investigation of this direction (Section 1, lines 21–23).

- **Principled control architectures.** The inclusion of MLLinear (same architecture without nonlinear activations) and DIMLP (within-modality nonlinearity only, linear cross-modal fusion) cleanly isolates the contributions of (a) dimensionality reduction vs. nonlinearity, and (b) within-modality vs. cross-modal nonlinear interactions (Section 2.4, lines 58–61). This is a well-designed ablation that provides meaningful signal about where improvements come from.

- **RED metric is a genuine methodological contribution.** The Relative Error Difference preserves temporal dynamics that standard voxel-wise analyses discard, enabling joint spatiotemporal clustering (Section 2.5, line 92). This analytical tool has potential utility beyond this specific study.

- **Open data and models.** The paper uses the public LeBel et al. (2023) dataset and off-the-shelf LLaMA/Whisper features, supporting reproducibility and follow-up work.

## Weaknesses

### Fatal
None.

### Major

1. **The "7.7% and 14.4% improvement over prior SOTA" claims are not traceable from the reported data.** The abstract (line 9) and contribution bullet (line 27) state that the approach "outperforms prior state-of-the-art linear ensembles by 7.7% and 14.4%." The Discussion (line 208) specifies "a 14.4% increase in mean normalized correlation compared to previous state-of-the-art models (Antonello et al., 2024)." However, Table 1 does not include a row corresponding to the "weighted averaging of linear unimodal predictions" that defines the prior SOTA. From Table 1, the improvement of the best model (MLP, PCA: CC_norm=34.32%) over the multimodal Linear all-voxels model (CC_norm=31.36%) is 9.44%, not 14.4%. The 7.7% figure appears in Table 1 as the improvement of the multimodal Linear all-voxels model over the unimodal baseline, not over prior SOTA. These numbers need to be explicitly reconciled: which specific model or published result is being compared, and the authors should either include those numbers in the table or clearly explain the derivation.

2. **PCA fitting procedure is underspecified, raising a potential information leakage concern.** Line 52 states: "PCA was applied to the aggregate response matrix Y_org ∈ ℝ^{N_TR × N_voxels} to obtain Y_PCA." The paper does not state whether the PCA transformation was fit on the training data only and then applied to the test data, or fit on the full dataset including test stories. If the latter, information from the test stories would influence the PCA basis, giving an unfair advantage in evaluation. This is a standard methodological pitfall. The paper must explicitly clarify this, and if PCA was fit on the full dataset, the evaluation is invalid.

### Minor

3. **The headline improvement numbers conflate two distinct factors.** The abstract and contributions (lines 9, 27) lead with "17.2% and 17.9% improvement over the standard semantic linear baseline." But this comparison differs in two ways: it adds audio features *and* replaces linear regression with an MLP. The paper's own controls show that the *incremental gain from nonlinearity alone*—comparing multimodal MLP (PCA) against multimodal Linear (all voxels)—is 4.6% in r² and 9.4% in CC_norm (from Table 1: 4.29% vs. 4.10%; 34.32% vs. 31.36%). These are real but substantially more modest. The paper does disentangle these factors via DIMLP and MLLinear controls, which is commendable, but the headline framing gives a misleading impression about the source and size of the nonlinearity-specific improvement.

4. **RED-based clustering modularity differences are reported without statistical testing.** The paper reports modularity Q values of 0.155 (nonlinear), 0.145 (linear), and 0.068 (FC) (line 122). The difference between nonlinear and linear clustering (ΔQ = 0.01) is small, and no significance test (e.g., bootstrapping over subjects or voxels) is provided. With only N=3 subjects, the reliability of this comparison is unclear. The paper includes significance testing for some analyses (e.g., Figure 2e uses FDR-corrected p-values), but this key comparison lacks any such assessment.

5. **The framing of improvement magnitude is disproportionate to the absolute effect sizes.** The absolute r² increases from 3.66% to 4.29% (a gain of 0.63 percentage points), and CC_norm from 29.12% to 34.32% (a gain of 5.2 percentage points). The paper describes these as "substantial" (line 9), "transformative" (line 208), and claims "current linear, unimodal practice leaves a substantial amount of structured, explainable variance... on the table" (line 27). While relative improvements are conventional in fMRI encoding due to low noise ceilings, the rhetoric is significantly stronger than the absolute numbers warrant. Reporting the fraction of noise-ceiling variance captured (which the normalized correlation partly addresses) would help readers calibrate.

### Trivial
None.

## Nice-to-Haves

- The choice of 256 hidden units for the MLP is stated without rationale. A brief note on how this was selected (e.g., validation-set sweep, reference to Appendix E for deeper models) would strengthen the main text.
- Per-subject variability is relegated to the appendix. Given N=3, a brief summary of cross-subject consistency for the main result would be valuable in the main text.
- Adding a significance test (bootstrap or permutation) for the modularity comparison would substantially strengthen the RED clustering analysis.

## Removed Points
The following points from the input review were removed with justification:
- **Missing training details (optimizer, learning rate, regularization):** These details are standardly placed in the appendix, which was stripped by the parser. Per policy, criticisms that hinge on absent appendix content are not valid weaknesses of the paper as submitted.
- **PCA linear models may not be well-tuned (text+audio Linear PCA: 28.92% vs. text unimodal Linear all-voxels: 29.12%):** The PCA-reduced models use a different response representation (PCA components vs. all voxels), so directly comparing these numbers is not a clean test of tuning quality. The concern is speculative.
- **Section-by-section notes on novelty scope, circular validation, and post-hoc theorizing:** These are largely stylistic observations or minor scope-creep critiques. The paper is appropriately cautious in its limitations section (lines 190–191, 218–222), and the neurolinguistic alignment claims are acknowledged as correlational.
- **"DMLP" vs. "DIMLP" naming inconsistency:** Parser artifact; the original paper uses "DIMLP" consistently.
- **"At time of writing" / "not yet released" type criticisms:** Removed per policy; all cited models and datasets are assumed to exist.

## Novel Insights

The input review correctly identifies that the paper's controlled architecture design (MLLinear, DIMLP) is the strongest element, and that the headline numbers need recalibration. However, the review's most important contribution is the observation that the 7.7%/14.4% SOTA comparison numbers cannot be verified from Table 1—this is a concrete, specific inconsistency that the paper must resolve. The reviewer's suggestion to reframe the main comparison as "multimodal MLP vs. multimodal linear" (showing 4.6–9.4% gains) is sound, but the paper's existing DIMLP analysis already provides a cleaner isolate of cross-modal nonlinearity (MLP vs. DIMLP: ~2.6% relative gain), which the review underemphasizes. The PCA information leakage concern is the most structurally significant issue raised.

## Suggestions

1. **Clarify the PCA fitting procedure explicitly.** State whether PCA was fit on training data only or on the full dataset. If standard practice was followed, a one-sentence clarification resolves this. If not, the evaluation must be redone.

2. **Make the prior-SOTA comparison traceable.** Add a row to Table 1 (or a footnote) showing the actual performance of the "weighted averaging of linear unimodal predictions" baseline from Antonello et al. (2024), and verify that the 7.7% and 14.4% improvements match. Alternatively, remove these claims if they cannot be cleanly supported.

3. **Recalibrate the headline framing.** Lead with the comparison against the matched multimodal linear baseline (4.6–9.4% gains) to accurately reflect the contribution of nonlinearity, while keeping the unimodal baseline comparison as secondary context. The paper's strongest evidence is the DIMLP vs. MLP comparison (~2.6% gain from cross-modal nonlinearity), which is the cleanest isolate—consider foregrounding it.

4. **Add a statistical test for the RED modularity comparison.** A bootstrap over subjects or a simple permutation test would address the concern about the small ΔQ=0.01.

5. **Report the fraction of noise-ceiling variance captured** alongside CC_norm, to help readers calibrate the absolute improvement magnitude.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>