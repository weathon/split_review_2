## Summary

This paper proposes AutoNFS, a neural architecture for feature selection that uses Gumbel-Sigmoid relaxation to learn a differentiable binary mask, trained end-to-end with a cardinality penalty that automatically determines the number of features to retain. The method is evaluated on 11 OpenML datasets with three corruption scenarios, plus 24 real-world metagenomic datasets.

## Strengths

- **The paper identifies a practical pain point in feature selection.** Existing methods typically require the user to specify the number of features a priori, and the proposed approach automatically determines feature count through optimization, which is a genuinely useful design goal.

- **Gumbel-Sigmoid is a technically sound choice for differentiable masking.** Using the two-class specialization of Gumbel-Softmax for binary mask learning is well-grounded in prior work (Jang et al., 2017; Maddison et al., 2017), and the temperature annealing schedule (τ₀=2.0, α=0.997) is a standard instantiation of exploration-to-exploitation transition.

- **Evaluation on 24 real-world metagenomic datasets (308–718 features, Table 2) demonstrates practical applicability** in a domain where feature selection is critical due to high dimensionality, noise, and expensive data collection. The finding that AutoNFS maintains or slightly improves predictive performance while reducing features to ~7.7% of the original count has genuine practical value.

## Weaknesses

### Major

- **Unfair baseline comparison (undermines headline claims).** The paper states (Section 4.1, line 204): *"all baseline methods select the same number of features as were in the initial representation (before corruption), whereas our method automatically chooses a much smaller subset."* On a benchmark where the goal is to discard corrupted features (50% of features are artificial noise), the method allowed to select fewer features has an inherent structural advantage. Baselines like Lasso and LassoNet that naturally determine feature count through regularization are stripped of this capability by being forced to select the original D features. The headline result (Figure 2, AutoNFS ranked #1) does not demonstrate that AutoNFS is a better feature selector — it demonstrates that selecting *fewer* features wins when baselines are denied that ability. To support the claimed superiority, the paper needs comparisons at matched sparsity levels or with baselines using their own natural feature-count determination (e.g., cross-validated regularization for Lasso).

- **Missing directly comparable neural FS baselines.** The paper cites STG (Yamada et al., 2020), Hard-Concrete gates (Louizos et al., 2017), and Concrete Autoencoders (Balın et al., 2019) in the Related Work as the most closely related differentiable masking methods, yet none appear in the experiments (Figure 2, Table 2). Without comparison against these methods, it is impossible to determine whether AutoNFS's Gumbel-Sigmoid approach offers any advantage over existing differentiable masking techniques. This is a critical omission for a paper claiming a new neural FS architecture.

- **Asymmetric misselection metric.** Figure 3a reports "misselection errors" as the fraction of selected features that are *not* original features — measuring only false positives. The paper claims "zero misselection errors" for two corruption scenarios (line 206), but Table 1 shows AutoNFS discards roughly half of valid features (e.g., 65/128 AL features, 8/26 EY features, 5/8 CH features). No recall or F-score is reported. The "zero error" claim is misleadingly incomplete without also reporting what fraction of the *original* features were correctly retained.

### Minor

- **The "nearly constant computational overhead" claim is partially misleading.** Figure 4a measures only "Feature Time" (mask computation), not total training time. The task network's input layer is D-dimensional, and its forward/backward passes scale at least linearly with D — total training time is not constant. While α≈0.08 for mask computation alone is plausible (D^0.08 grows slowly), the paper repeatedly claims "nearly constant computational overhead" (Abstract, Sections 1, 3.1) for the overall method, overstating what the evidence actually covers.

- **No ablation studies for architectural choices.** The masking network f maps a fixed embedding to D logits. There is no ablation comparing this against the simpler baseline of directly learning logits w ∈ ℝᴰ (removing the MLP). The penalty coefficient λ=1 and temperature schedule parameters are given without sensitivity analysis in the main paper.

- **No statistical significance for main ranking results.** The ranking improvements (0.7–0.9 ranking points in Figure 2) and metagenomic improvements (0.7 pp MLP, 1.2 pp RF) are reported without confidence intervals, significance tests, or paired comparisons. Given the small absolute improvements, it is unclear whether these are statistically reliable.

- **Algorithm 1 / text inconsistency.** Section 3.3 defines L_select = (1/D) Σ m_j (line 83), but Algorithm 1 line 118 uses (1/B) Σ m_j. These are different normalizations — either a bug or a typo that needs correction.

### Trivial

None.

## Nice-to-Haves

- Compare against STG and Hard-Concrete at sparsity levels those methods naturally produce, and also at matched sparsity levels to show that AutoNFS does not solely win by selecting fewer features.
- Report precision and recall (or F-score) on the corruption benchmarks alongside misselection error.
- Ablate the masking network by comparing directly-learned logits w ∈ ℝᴰ against the MLP-based approach.
- Report total training time (not just mask computation time) to support the computational efficiency claims.
- Add statistical significance measures for the main ranking results.

## Removed Points

These points from the input review were removed after cross-checking against the paper:
- "Physically impossible" framing for constant overhead: factually incorrect — α≈0.08 is plausible for mask computation.
- λ sensitivity analysis: removed because the paper defers this to Appendix F (stripped by parser; per policy, missing appendix content is not a valid criticism).
- Masking network architecture details missing from main text: removed because these are deferred to Appendix C (stripped by parser).
- Naming inconsistency (AutoNFS vs GFS-NetWork in figures): removed as a potential parser artifact from image OCR.
- Claim that Introduction overstates existing methods' inability to detect feature count: removed because the paper qualifies this with "often" and discusses L1 methods in Related Work.
- Global vs instance-wise mask tradeoff undiscussed: removed because the paper explicitly states in Section 2 that it "focuses on learning a single global mask."

## Novel Insights

None beyond the paper's own contributions. The reviews raise concerns about evaluation fairness and missing comparisons but do not identify new capabilities or connections the paper itself missed.

## Suggestions

1. **Re-run the benchmark at matched sparsity levels.** Force all methods (including AutoNFS) to select the same number of features to disentangle the effect of feature-count reduction from selection quality.
2. **Add STG, Hard-Concrete, and Concrete Autoencoder to the experimental comparison.** These are the most direct peers and are required to substantiate claims of superiority over differentiable FS methods.
3. **Report precision and recall** for the corruption benchmarks alongside the asymmetric misselection error.
4. **Ablate the masking network** — compare directly learning logits w ∈ ℝᴰ vs. the proposed MLP-based mapping.
5. **Correct the L_select formula inconsistency** between Section 3.3 (1/D) and Algorithm 1 (1/B).

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>