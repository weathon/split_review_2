Now I have all the information needed. Let me compose the final authoritative review.

## Summary

This paper introduces *monitorability* — a formal concept capturing how intrinsically detectable a neural network's failures are from its internal representations — and proposes MIRA (Monitorability via Input peRturbAtion Score), a metric that quantifies this property using only in-distribution data and norm-bounded input perturbations. MIRA perturbs inputs toward decision boundaries via FGSM, measures separability of perturbed vs. unperturbed penultimate-layer features using Mahalanobis distance, and produces a single score. The paper validates MIRA by comparing it against the "best achievable" OoD detection performance (across ODIN, Mahalanobis, and Energy detectors) on vision, tabular, and NLP benchmarks.

## Strengths

- **The concept of monitorability is genuinely novel and well-motivated.** The paper identifies a real gap: prior work focuses on runtime detection of anomalies but lacks a way to characterize, pre-deployment, how inherently detectable failures are from a model's internal representations. The toy example in Section 3.1 (Figure 1), where two models with identical ID accuracy differ dramatically in how they represent OoD data, cleanly demonstrates that standard accuracy metrics miss this dimension.

- **MIRA is conceptually simple and has practical appeal.** The idea of using only ID data with norm-bounded perturbations to probe feature-space structure is elegant. Computing MIRA does not require collecting OoD data or tuning multiple detectors, making it potentially useful for pre-deployment model selection. The χ²-based dimension calibration (Eq. 3) is a thoughtful design choice.

- **The evaluation spans three modalities and multiple architectures.** The diversity of settings (CIFAR-10/100 for vision, Sensorless Drive for tabular, SST-2 for NLP) and architectures (ResNet, DenseNet, ViT, MLPs, Transformers, RoBERTa, etc.) lends breadth to the investigation. The t-SNE visualizations (Figure 2) provide intuitive qualitative support linking higher MIRA scores to more structured feature representations.

## Weaknesses

### Fatal
None.

### Major

- **No quantitative correlation measure for a claim centered on correlation.** The paper's central validation claim is that MIRA "correlates" with OoD detection performance (Abstract, RQ1 in Section 4.1, Section 4.4, Conclusion), yet it provides no quantitative correlation statistic of any kind — no Spearman ρ, Pearson r, Kendall τ, p-value, or confidence interval. The evidence consists entirely of qualitative statements like "higher MIRA scores consistently align with stronger OoD detection" (Section 4.4) and visual table inspection. This is a fundamental evidential gap for a paper whose primary claim is correlation. The rank orderings in the tables are suggestive but a proper correlation analysis is needed to determine whether the patterns are statistically meaningful.

- **Confounded validation with the Mahalanobis-based detector.** MIRA computes separability via Mahalanobis distance on penultimate-layer features (Eq. 1, Section 3.3), which is the same core machinery as the Mahalanobis-based OoD detector (Lee et al., 2018b) used for validation. The shared components — penultimate layer, Mahalanobis distance, class-conditional Gaussian modeling — mean that the observed "correlation" between MIRA and Mahalanobis-detector performance is partially built in. While the paper includes two other detectors (ODIN, Energy) that do not share this mechanism, the Mahalanobis detector is frequently the best performer across datasets (e.g., 7/7 OoD datasets for ViT on CIFAR-10, 6/7 for ResNet-18 on CIFAR-10, all tabular and NLP cases), so the "best achievable" target that MIRA correlates with is often the Mahalanobis detector's performance. The relationship is not convincingly disentangled from the shared methodology.

- **Perturbation range selection is unablated.** The perturbation range [ε_min, ε_max] is determined by an accuracy-reduction threshold: ε_min is the smallest value that reduces accuracy to a threshold, and ε_max = 2·ε_min (Section 4.2). Different models have different accuracy-ε curves, so fixing a threshold means models are compared over different effective perturbation ranges. The paper acknowledges this as a limitation in the Conclusion but provides no ablation showing sensitivity to the threshold choice. Without this, it is unclear whether MIRA rankings reflect genuine differences in feature-space separability or artifacts of threshold selection.

### Minor

- **The "best achievable" OoD proxy is non-standard and potentially inflated.** The validation target is defined as the maximum AUROC across three detectors per OoD dataset (Section 4.1). This creates an upper envelope that no single detector could achieve in practice — a model could have ODIN performing well on one dataset and Mahalanobis on another, and the "best achievable" combines them. The paper should also report average AUROC across methods or show MIRA's relationship to each detector individually.

- **No variance or error bars.** All results appear to be single-run (the paper states fixed seeds but reports no variance). Without error bars or multiple seeds, the reader cannot assess whether AUROC differences between models are meaningful or within noise. This is particularly relevant for the tabular data (Table 2) where some values exhibit extreme variation between detectors (e.g., Class 7 for MLP: ODIN=0.08, Energy=0.12, Mahalanobis=99.56).

- **Gap between the formal definition and the metric.** Definition 1 (Section 3.2) requires a set Z^l such that loss ≤ ε iff f^l(x) ∈ Z^l — a strong bijection condition. MIRA measures separability of perturbed from unperturbed features, which is related but not formally shown to bound the existence of such Z^l. The paper would benefit from clarifying how MIRA operationalizes the formal definition.

- **MIRA scores are on incomparable scales across domains.** The χ²-based calibration (Eq. 3) depends on penultimate-layer dimensionality, producing vastly different scales (vision ~0–90, tabular ~4–64, NLP ~2000–3800). The paper does not discuss how practitioners should interpret these values or whether cross-domain comparisons are meaningful.

### Trivial
None.

## Nice-to-Haves

- Provide guidance on what constitutes a "good" MIRA score in absolute terms within a given domain.
- Add a comparison of computational cost between computing MIRA and tuning even one OoD detector.
- Extend the "detector-agnostic" analysis by showing MIRA's relationship to the minimum or variance across detectors, not just the maximum.

## Removed Points

These were filtered from the input review as not meeting the evidence standard:

1. **"t-SNE distorts global structure"** — removed because the paper uses t-SNE only for qualitative illustration (Figure 2), not as quantitative evidence. This is well-known and does not affect the paper's claims.
2. **"Missing comparison to specific related works"** — removed per policy; I cannot verify the existence of unmentioned works.
3. **"The paper claims MIRA is efficient but provides no runtime comparison"** — partially addressed: the Discussion section (end of 4.4) does claim efficiency qualitatively. A more detailed comparison would be a nice-to-have, not a weakness.
4. **Miscellaneous section-by-section style notes** (e.g., "literature review could be expanded") — removed as generic or speculative critiques lacking concrete evidence of harm to the paper's core claims.

## Novel Insights

The most penetrating observation from the reviews is that MIRA's validation is structurally confounded: MIRA uses Mahalanobis distance to measure feature separability (its core metric), and one of the three validation detectors (Lee et al., 2018b) also uses Mahalanobis distance on penultimate-layer features. Because MIRA isn't independently validated against a non-Mahalanobis separability measure, the observed correlation could partially reflect the fact that both MIRA and the best-performing detector are measuring how well features fit class-conditional Gaussian assumptions, rather than general-purpose "monitorability." The reviewer's suggestion to replace Mahalanobis distance in MIRA with an alternative separability measure (e.g., a linear classifier trained on perturbed vs. unperturbed features, or a kernel two-sample test) is a concrete, actionable path to disentangling this confound and would substantially strengthen the paper's central claim if the ranking were preserved.

## Suggestions

- Report Spearman rank correlation between MIRA and each detector's average AUROC across models, with confidence intervals, to quantitatively substantiate the central "correlation" claim.
- Add an ablation showing MIRA rankings are stable across different accuracy-reduction thresholds (e.g., 70%, 80%, 90%) for the perturbation range selection.
- Replace the Mahalanobis distance in MIRA with an alternative separability measure (e.g., a linear classifier or kernel MMD) to disentangle MIRA from shared methodology with the Mahalanobis detector, or at minimum show that MIRA independently correlates with ODIN and Energy performance.
- Report results with error bars across multiple seeds and include per-detector correlation analyses alongside the "best achievable" aggregation.
- Clarify how MIRA relates to Definition 1, since MIRA measures feature separability while Definition 1 requires an exact bijection between feature regions and prediction correctness.

## Score and Decision

**Bracket derivation.** Round 1 bracketing compared this paper against three bands of anchors. The strongest band (scores 6–8, e.g., mUXdysoxEP.md at 6.75) contains papers with thorough experimental validation including ablations, error bars, and comprehensive baselines — the MIRA paper lacks all three. The mid band (scores 3.5–5.5, e.g., todLTYB1I7.md at 5.00, lHBQrqVYji.md at 5.00) contains papers with interesting ideas but validation that is either incomplete or contains confounds. The lower band (scores 1.5–3.5, e.g., l5ouuojPGe.md at 3.00, lvHHWDJCcr.md at 3.40) contains papers with unclear contributions or more fundamental framing issues. The MIRA paper's novelty is stronger than the lower-band papers, placing it above 3.5. However, its two most heavily weighted weaknesses — no quantitative correlation measure (-5.18) and confounded validation (-4.05) — are more central to the paper's core claim than the weaknesses of the 5.0 anchors. **Round 1 bracket: 3.5–5.0.** Round 2 compared against lHBQrqVYji.md (5.00) and lower-band anchors (2.0–3.4). The MIRA paper shares the 5.0 anchor's pattern of an interesting idea with validation issues, but its central validation gap (no correlation statistic for a correlation claim) is more fundamental to the paper's thesis than the 5.0 anchor's scope/coverage issues. This places it below 5.0, in the 3.5–4.5 range. Weighted-item comparison: against the 5.0 anchor, the MIRA paper's strongest positive (novel concept, +4.59) is comparable, but its strongest negative (no correlation measure, -5.18) is more damaging to the central claim than the 5.0 anchor's strongest negative (poor lit review, -8.71, which pertains to coverage rather than core evidence).

**Final score: 4.0.** The concept of monitorability and the MIRA metric are genuinely novel contributions. However, the paper's central claim — that MIRA correlates with monitoring performance — is not adequately substantiated. The absence of any quantitative correlation measure, combined with the confound between MIRA's core machinery and a primary validation detector, means the evidence does not currently support the strength of the claims. The paper presents a promising direction but requires substantially stronger validation before the claims can be accepted.

**Anchors used for calibration:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| l5ouuojPGe.md | 3.00 | 1 | Yes | Similar domain (NN monitoring), weaker novelty, comparable validation rigor. MIRA paper has stronger concept. |
| lvHHWDJCcr.md | 3.40 | 1 | Yes | Model selection metric. MIRA paper has more novel concept but similar validation gaps. |
| mUXdysoxEP.md | 6.75 | 1 | Yes | OOD detection via feature separation. Much stronger empirical validation (ablations, error bars, comprehensive comparisons). MIRA paper weaker on validation. |
| todLTYB1I7.md | 5.00 | 1 | Yes | Evaluation framework. Comparable mixed reception; MIRA paper's concept is more novel but validation is weaker relative to claims. |
| lHBQrqVYji.md | 5.00 | 2 | Yes | Post-deployment monitoring. Interesting idea with validation concerns. MIRA paper's validation gap is more central to its core claim. |
| i28ZjVxl81.md | 2.50 | 2 | No | Unrelated OOD tabular paper. Lower quality. |
| KK29oh8jZs.md | 3.00 | 2 | No | OOD detection synthetic datasets. Less relevant. |
| 3ZdGSTxKuy.md | 2.00 | 2 | No | Unrelated video representation learning. |

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>