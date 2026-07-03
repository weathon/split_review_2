## Summary

This paper introduces a nonlinear multimodal encoding model (PCA + single-hidden-layer MLP over concatenated LLaMA and Whisper features) for fMRI speech prediction. It shows that this simple approach outperforms linear baselines and prior multimodal linear ensembles, and uses the improved predictions to reveal distributed multimodal processing patterns across the cortex that align with several neurolinguistic theories.

## Strengths

- **Clean ablation design (Linear → MLLinear → DIMLP → MLP) that systematically disentangles the contributions of dimensionality reduction, within-modality nonlinearity, and cross-modal nonlinear interactions.** No prior speech-encoding paper constructs this factorial decomposition. The MLP (4.29% r²) strictly outperforms DIMLP (4.18%), which outperforms MLLinear (4.10%), showing that nonlinear cross-modal interactions contribute beyond both dimensionality reduction and within-modality nonlinearity.

- **RED-based spatiotemporal clustering (Section 2.5) is a genuine methodological advance.** By preserving temporal dynamics at each voxel rather than collapsing to spatial-only analyses, it reveals functional groupings (modularity Q=0.155 vs. 0.145 for linear and 0.068 for standard functional connectivity) that are invisible to standard approaches and track coherent functional organization (motor/somatosensory by body part, speech areas along the dorsal stream).

- **Demonstrates cortex-wide multimodal integration beyond what prior work detected.** Antonello et al. (2024) reported localized auditory-driven improvements restricted to AC and M1M. The present paper shows 68.5% of significantly predicted voxels exhibit joint audio-semantic representation, with gains in high-level visual areas (OFA, EBA, FFA, PPA, RSC) during purely auditory listening—directly supporting the Convergence-Divergence Zone model with evidence linear approaches could not produce.

- **The MLLinear control is a rigorous baseline.** By equating parameter count and architecture with the nonlinear MLP while removing only nonlinearity (identity activation), it isolates nonlinearity as the driver of gains rather than reduced dimensionality or increased model capacity.

- **Per-ROI variance partitioning provides granular quantitative support for theoretical claims** (e.g., AC: 83.3% joint; M1M: 32.4% unique audio, 14.1% unique semantic, 53.5% joint) that goes beyond qualitative region-level comparisons.

## Weaknesses

### Major

- **Claimed improvement percentages (7.7%, 14.4%) do not clearly map to Table 1.** The abstract claims "7.7% and 14.4% improvement over prior state-of-the-art models relying on weighted averaging of linear unimodal predictions." Comparing the best multimodal MLP (PCA: 4.29% r², 34.32% CC_norm) to the multimodal linear (all voxels) model (4.10% r², 31.36% CC_norm) yields 4.6% r² and 9.4% CC_norm improvement—neither matches the claimed numbers. The 14.4% figure reappears in the Discussion (line 208) as a comparison to Antonello et al. (2024), which may reference a specific result not replicated in Table 1. The abstract and contribution list should explicitly state which baseline each percentage refers to, as readers cross-checking against Table 1 will find apparent discrepancies that erode trust in the numerical framing.

- **PCA fitting procedure may leak test set information.** Line 52 states PCA was applied to "the aggregate response matrix Y_org ∈ ℝ^(N_TR × N_voxels)." The phrase "aggregate response matrix" is ambiguous: if PCA is fit on the full dataset (training + test time points combined), the dimensionality reduction incorporates test-set variance structure, potentially inflating metrics even if the encoding model itself never sees test responses. This affects nearly every result in the paper. Appendix B.4 (stripped) may clarify this, but the main text is insufficient. The authors must explicitly state whether PCA was fit on training data only.

### Minor

- **Training details are insufficient for reproducibility.** No information is provided about: loss function, optimizer, learning rate, number of epochs, batch size, early stopping criteria, or ridge regularization strength λ for linear models. Optuna (Akiba et al., 2019) is cited in references but never described in terms of what was tuned or on which validation split. For the linear models, ridge λ is particularly important since a poorly tuned linear baseline could inflate the relative gains of the MLP.

- **Evidence for "nonlinear cross-modal interactions drive gains" is weaker than claimed.** The comparison between MLP (4.29% r²) and DIMLP (4.18% r²) shows a 0.11 percentage point absolute difference (2.6% relative). These architectures differ in multiple aspects beyond just cross-modal interaction (concatenation order, number of hidden layers before fusion), making the attribution less than unique. The paper does not report statistical significance in the main text (Appendix C is referenced but stripped). The claim is plausible but overstated relative to the evidence presented in the main text.

- **LLaMA model size for main results is not specified.** Table 1 says "text inputs (from LLaMA-1)" but does not state which size (7B, 13B, or 65B) was used. Since feature quality scales with model size, this matters for reproducibility and interpretation.

### Trivial

- "unnormlized" → "unnormalized" typo in the abstract
- MLP activation function is not explicitly stated (can be inferred from MLLinear description but should be explicit)

## Nice-to-Haves

- Per-subject results alongside averages (N=3 subjects; showing consistency would strengthen claims)
- Confidence intervals or bootstrapped error bars on key comparisons (MLP vs. linear gap, DIMLP vs. MLP gap)
- Sensitivity analysis on the noise ceiling regularization (CC_max < 0.25 → 0.25)
- Clarify which LLaMA layer `l` was used and whether it was selected based on validation performance

## Removed Points

The following points were flagged during review and removed after verification against the paper:

- **"Nonlinear unimodal encoding has been explored before"** — The paper explicitly scopes its novelty to nonlinear *multimodal* encoding for naturalistic continuous speech (lines 23, 27). This is an acknowledged prior-work scope issue that the paper addresses directly.
- **"For the first time claim too strong"** — The paper's text is appropriately hedged: "for the first time, that nonlinear *multimodal* encoding is feasible for naturalistic speech" (line 27). The multimodal qualifier limits the scope.
- **"In-silico testing and decoding claimed but not performed"** — The abstract and introduction mention these as motivations ("a major step towards future robust in-silico testing"), not as achieved contributions. This framing is appropriate.
- **"RED modularity values lack confidence intervals"** — Requesting CIs for hierarchical clustering modularity goes beyond standard practice.
- **"Missing related works"** — Cannot verify without external sources; rule prohibits mentioning this.
- **"Unfair comparison with baselines"** — If the asymmetry exists, it favors the baseline (linear models), not the proposed method. This asymmetry is intentionally conservative.
- **Strength about "well-motivated" or "addresses important problem"** — Generic; removed.
- **Strength about "linear encoders being standard"** — Generic; removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the PCA ambiguity**: State explicitly whether PCA was fit on training data only or on the aggregate matrix. If the latter, re-run all experiments with a proper train-only PCA fit.
2. **Add a clear mapping** between the claimed improvement percentages (7.7%, 14.4%) and specific baseline models or prior results from Antonello et al. (2024).
3. **Add a hyperparameter table** listing: optimizer, learning rate, epochs (or early stopping criterion), loss function, ridge λ for each linear model, MLP activation function, and validation procedure.
4. **Specify the LLaMA model size** (7B, 13B, or 65B) used for the main results in Table 1.
5. **Soften the claim** that "nonlinear cross-modal interactions contribute most significantly" unless statistical significance can be demonstrated for the MLP vs. DIMLP comparison.

## Score and Decision

**Calibration note**: The calibration search tool was unavailable due to a filesystem error, so I could not retrieve human-reviewed anchor papers. The score below is based on my independent assessment following the ICLR scoring guidelines.

This paper makes a solid empirical contribution: a simple nonlinear multimodal encoding model that convincingly outperforms linear baselines for fMRI speech prediction, backed by a clean ablation design and thoughtful neuroscientific analysis. The two major weaknesses—ambiguous PCA fitting and misaligned percentage claims in the abstract—are clarifiable but need to be addressed before the paper's claims can be fully trusted. The methodological novelty is incremental (PCA + single-hidden-layer MLP), but the empirical and analytical contributions (RED-based clustering, variance partitioning, systematic ablation) are meaningful.

I rate this paper as a borderline accept. The core findings are plausible and well-supported by the overall pattern of results, but the presentation issues and PCA ambiguity prevent a stronger recommendation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>