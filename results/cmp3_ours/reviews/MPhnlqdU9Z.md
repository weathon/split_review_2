Now I have comprehensive calibration. Let me write the final review.

## Summary

This paper introduces *monitorability*, a novel concept capturing the intrinsic ability of a neural network's internal features to enable runtime error detection. It provides a formal definition (Definition 1, l-monitorability) and proposes the MIRA Score, a metric that quantifies monitorability by perturbing ID inputs toward decision boundaries via FGSM, measuring how separable the perturbed features are from clean features using Mahalanobis distance, and integrating over a range of perturbation magnitudes. The paper validates MIRA by comparing it against best-of-three OoD detection performance (ODIN, Mahalanobis, Energy) across CV (CIFAR-10/100), tabular (Sensorless Drive), and NLP (SST-2) domains with diverse architectures.

## Strengths

- **First formalization of monitorability as a distinct property.** The paper correctly identifies that existing OoD detection methods assume the model's features are already high-quality, but no prior work asks whether features are intrinsically detectable in the first place. Definition 1 (l-monitorability) is a reasonable first formalization that captures a real gap in the literature. This is a genuinely novel conceptual contribution independent of the specific metric proposed.

- **Clear motivating examples and intuition.** The toy example in Figure 1 (two models with identical accuracy but different feature-space organization for OoD data) is effective at communicating why monitorability can differ independently of accuracy. The t-SNE visualizations in Figure 2 provide qualitative support linking MIRA scores to actual feature-space structure. These make the central claim tangible.

- **Multi-domain evaluation with diverse architectures.** Testing across CV (ResNet-18, DenseNet, CustomNet, ViT), tabular (MLPs, Transformers), and NLP (RoBERTa, DistilBERT, ELECTRA, DeBERTaV3) shows the authors took generality seriously. This breadth is appropriate for a first paper on a new concept.

## Weaknesses

### Fatal

None.

### Major

1. **Validation circularity undermines the central claim.** MIRA uses Mahalanobis distance on penultimate-layer features (Eq. 3) and is validated against "best-of-3" OoD detection (ODIN, Mahalanobis, Energy). In the tabular (Table 2) and NLP (Table 3) experiments, the Mahalanobis OoD detector is the best method in nearly every model × dataset cell, dominating the "best" proxy. Even in the CV experiments (Table 1), Mahalanobis is the dominant single method for ViT (7/7 datasets on CIFAR-10, 6/7 on CIFAR-100). Since MIRA shares the same mathematical machinery (Mahalanobis distance under class-conditional Gaussian assumptions) as one of the three validation methods, the claimed "correlation" may partially reflect that MIRA predicts Mahalanobis-compatibility rather than detector-agnostic monitorability. The paper claims MIRA is "detector-agnostic" (Section 4.4), but does not report correlation with ODIN and Energy separately, nor with the average across all three methods excluding Mahalanobis. This needs to be addressed to substantiate the detector-agnostic claim.

2. **No statistical quantification of the claimed correlation.** The paper repeatedly asserts that MIRA "correlates" or "aligns" with OoD detection performance (abstract, RQ1, Section 4.4, conclusion), but reports zero correlation coefficients, p-values, confidence intervals, or significance tests. With only 4–5 models per domain, the visual/qualitative trend could be driven by outlier architectures — e.g., ViT achieves both the highest MIRA and near-perfect detection, and removing it may substantially weaken the apparent relationship. For a paper whose central validation claim is correlational, the absence of even a Spearman rank correlation is a critical omission.

### Minor

3. **The metric conflates Gaussian fit quality with separability.** MIRA = (1/S₀) × ∫[E[S(perturbed)] − S₀] dε (Eq. 4), where S₀ is the average surprisal of clean ID data under a class-conditional Gaussian model. If a model's features are poorly described by Gaussians, S₀ will reflect this misfit, affecting the MIRA score independently of whether perturbed and clean features are actually separable. The paper references Lee et al. (2018b) for the GDA assumption, but does not verify that this assumption holds comparably across the diverse architectures evaluated (especially smaller models like CustomNet, which shows anomalous negative MIRA). A goodness-of-fit analysis or a nonparametric alternative would clarify whether MIRA measures genuine monitorability or Gaussian-fit quality.

4. **The perturbation range is a free parameter with no sensitivity analysis.** ε_min is defined as "the smallest value that reduces accuracy to a certain threshold" and ε_max = 2·ε_min (Section 4.2). The accuracy threshold used to define ε_min is a free parameter that could affect the relative ranking of models (e.g., more robust models may require larger ε to reach the accuracy threshold, shifting their perturbation range and potentially inflating separability). The paper acknowledges this as a limitation and defers to future work, but does not provide any sensitivity analysis showing that the relative ordering of MIRA scores is stable across reasonable threshold choices.

5. **Over-claiming in the conclusion.** The conclusion states that "MIRA can guide design decisions such as selecting the most suitable layer for feature-based monitoring... and identifying class-specific vulnerabilities where monitorability may be weak." No experiments support either claim — all results use only the penultimate layer and all are at the model level, not the class level. These are forward-looking research directions stated as demonstrated findings.

6. **No ablation study of MIRA's components.** MIRA combines: FGSM perturbation direction, Mahalanobis distance, chi-squared conversion to surprisal, integration over ε, and normalization by S₀. No analysis isolates which design choices matter. A simplified version (e.g., Mahalanobis distance on perturbed features at a single ε without normalization) might work equally well, which would undercut the justification for MIRA's complexity.

7. **Negative MIRA for CustomNet is unexplained.** CustomNet scores −0.07 on CIFAR-10 — perturbed features become *less* detectable than clean features. The paper notes this indicates "very bad monitoring capabilities" but does not analyze whether this arises from Gaussian assumption violations, the perturbation scheme, or a genuine structural property. This anomalous regime deserves scrutiny to confirm the metric behaves correctly.

### Trivial

- Definition 1's equivalence condition (ℒ(f(x), y) ≤ ε ⇔ f^l(x) ∈ Z^l) is an idealization that does not accommodate false positives/negatives in practice. The authors acknowledge Z^l "may be arbitrarily complex," but the framing is worth noting as a limitation of the formalization.

- The claim that "the strength of the attack is not critical" (Section 4.2) is unsubstantiated — the perturbation range definition is itself tied to an accuracy threshold, so the attack strength matters by construction.

## Nice-to-Haves

- A computational cost comparison (wall-clock time) against alternatives like training an OoD detector on held-out OoD data would calibrate expectations for practitioners. The paper claims efficiency (RQ4) but provides no runtime measurements.
- A controlled experiment where MIRA is shown to predict the *average* detection performance across methods (not just the best) would strengthen the claim that it measures monitorability rather than compatibility with a specific detection framework.

## Removed Points

The following points from the input review are removed with justification:

1. **Formatting nitpicks about table presentation** (e.g., missing average values, unclear labeling) — These are parser artifacts from PDF extraction, not author errors.
2. **Generic concern about "the evaluation lacks rigor" without concrete anchors** — The specific sub-concerns are preserved in the Major/Minor items above; the general framing is removed.
3. **The specific claim that "Mahalanobis is the dominant method across nearly every model and class"** — This is overstated for the CV experiments (where CustomNet and ResNet-18 on CIFAR-100 show ODIN/Energy outperforming Mahalanobis on many datasets); however, the core concern about validation circularity is valid and preserved.
4. **Demand for "more principled strategies" for perturbation range** — The paper already acknowledges this limitation and frames it as future work, making this a nice-to-have rather than a weakness.
5. **Computational cost comparison suggestion** — Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the validation-circularity concern more sharply than the paper acknowledges, and the absence of any statistical correlation measure is a genuine gap in the empirical argument, but these are critique points rather than novel observations.

## Suggestions

1. **Disentangle validation from the metric's own machinery.** Compute Spearman correlation between MIRA and (a) average performance across all three detection methods, (b) ODIN and Energy performance alone (excluding Mahalanobis). Report these with confidence intervals. If the correlation holds for ODIN/Energy, the detector-agnostic claim is supported.
2. **Control for Gaussian fit quality.** Compute a normality statistic (e.g., multivariate kurtosis or a density ratio) for each model's class-conditional features and show that MIRA predicts detection performance even after conditioning on Gaussian fit.
3. **Perform sensitivity analysis on the accuracy threshold** used to define ε_min, showing that the relative ordering of MIRA scores across models is stable.
4. **Conduct an ablation** comparing MIRA against simpler variants (e.g., raw Mahalanobis distance at fixed ε, without chi-squared conversion, without S₀ normalization) to justify the design choices.
5. **Analyze the negative MIRA case** (CustomNet) to determine whether it reflects a genuine monitorability failure or an artifact of violated assumptions.

## Score and Decision

**Round 1 bracket:** [4.0, 6.0] — plausible range based on the paper's genuine conceptual novelty offset by validation weaknesses.

**Anchor papers retrieved across all rounds:**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nSDOkm0SKo.md` | 1.00 | R1 | Unrelated financial paper (strong reject); not comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/l5ouuojPGe.md` | 3.00 | R1 | NN monitoring thresholding paper; less conceptual novelty than MIRA |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VAmVEghgoC.md` | 4.50 | R1 | Neural Collapse OOD detector; rejected for limited novelty vs. existing work |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Gr8nHvOivO.md` | 4.50 | R1 | Similar Neural Collapse OOD paper; weak novelty |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YMgMGPjUPg.md` | 4.75 | R1 | NAP OOD detection; rejected for novelty concerns despite SOTA results |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9ROuKblmi7.md` | 5.75 | R1 | NECO OOD detection; accepted with solid evaluation, some generalization concerns |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mUXdysoxEP.md` | 6.75 | R1 | Pursuing Feature Separation; accepted with SOTA results |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ljwoQ3cvQh.md` | 7.00 | R1 | Deep NN extrapolation; strong empirical+theoretical paper |

**Final calibration reasoning:** Among the strong-reject anchors (score < 1.5), no topically similar papers exist, confirming the paper is not a strong reject. The 3.0 anchor (Red Pill or Blue Pill) has less novelty than MIRA. The 4.5–4.75 anchors (Neural Collapse OOD, NAP) were rejected primarily for limited novelty; MIRA has substantially more conceptual novelty (first formalization of monitorability). The 5.75 anchor (NECO) was accepted with some evaluation concerns but stronger empirical support than MIRA. MIRA's validation weaknesses (circularity, no statistics) are more significant than NECO's, but its conceptual contribution is more novel. The score of 5.0 reflects a paper with genuine foundational novelty whose current empirical evidence does not convincingly validate its central claim.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>