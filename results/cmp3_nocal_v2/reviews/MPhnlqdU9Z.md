## Summary

This paper introduces *monitorability* — an intrinsic property of a neural network that determines how detectable its failures are from internal activations, independent of any specific detection method — and proposes MIRA, a practical metric that quantifies it using only in-distribution data and norm-bounded input perturbations. Experiments across 13 models in vision, tabular, and NLP domains show that MIRA rankings perfectly align with rankings by best OoD detection performance, suggesting the metric captures something real about a model's feature-space structure.

## Strengths

1. **Novel and well-motivated concept.** The notion of monitorability as a model-intrinsic property distinct from both accuracy and specific detector performance is genuinely new and practically important. The toy example (Section 3.1, Figure 1) cleanly illustrates the core intuition: two models with identical classification accuracy can have very different feature-space structures, making one much easier to monitor than the other. This framing is the paper's primary intellectual contribution.

2. **Multi-domain evaluation with consistent qualitative signal.** The paper evaluates across three distinct modalities (vision, tabular, NLP) with 4–5 architectures per domain (13 models total). The pattern is fully consistent: in every domain, the MIRA ranking of models matches the ranking by best OoD detection performance. This level of consistency across diverse architectures and modalities is strong evidence that MIRA captures a genuine property.

3. **Practical design decisions.** MIRA requires only ID data and efficient FGSM perturbations, making it usable at pre-deployment time without access to OoD datasets or detector tuning. The dimension-calibrated surprisal score (Equation 3) is a thoughtful detail that addresses the otherwise problematic comparison of Mahalanobis distances across layers with different dimensionalities.

## Weaknesses

### Fatal
None.

### Major

1. **Correlation is claimed but never quantified.** The paper uses "correlates" or "correlation" to describe the MIRA–detection-performance relationship at least six times (Abstract, Section 4.1 RQ1, Section 4.4 Discussion, Section 6, table captions). Yet **no correlation coefficient of any kind is reported** — no Spearman's ρ, no Pearson's r, no Kendall's τ. The qualitative pattern in the tables is visually compelling, but the paper's central claim rests on a reader's manual verification rather than a quantitative analysis. A single scatter plot (MIRA vs. best AUROC per domain) or a reported Spearman correlation would turn a strong qualitative observation into a precise quantitative claim. This is the most significant evidential gap.

2. **Partial circularity in the validation design.** MIRA computes separability of perturbed-vs-clean features using **Mahalanobis distance** (Section 3.3). One of the three "ground truth" OoD detectors used for validation is also **Mahalanobis-based OoD detection** (Lee et al., 2018b). The validation therefore partly measures whether a method based on Mahalanobis distance correlates with a detection method also based on Mahalanobis distance. This is not fully circular — the perturbation-based approach and the surprisal calibration are distinct — but it substantially reduces the independence of the validation. The concern is amplified by the observation that in Tables 2 and 3 (tabular and NLP), Mahalanobis-based detection is the best-performing method for *every single model*, meaning the "best-of" aggregate is essentially a Mahalanobis comparison. Reporting correlations with each of the three detectors separately (ODIN, Mahalanobis, Energy) would address this.

3. **No ablation studies on key design choices.** Several design decisions could affect MIRA rankings, and none are ablated:
   - **Perturbation range.** ε_min is determined by an accuracy threshold (Section 4.2, details in Appendix B.6). The choice of threshold is arbitrary, and no sensitivity analysis is reported.
   - **Perturbation method.** Only FGSM is used. Would PGD or random perturbations (no directional component) change rankings?
   - **Layer choice.** Only the penultimate layer is evaluated (Section 4). Other layers might give different pictures.
   - **Norm choice.** Only ℓ_∞ (via FGSM) is used. The paper acknowledges alternative norms as future work (Section 6), but the current results' sensitivity to this choice is unknown.

   The paper acknowledges the perturbation range limitation (Section 6), but ablations are critical for establishing the metric's robustness.

### Minor

1. **Definition 1 is not operational.** Definition 1 states a model is *l*-monitorable if there exists a set Z^l such that correct prediction ⇔ activation in Z^l. As the paper acknowledges ("Z^l may be arbitrarily complex," Section 3.2), such a set always exists by construction (e.g., the image of correctly classified inputs). The definition imposes no constraints on the complexity or learnability of Z^l, so it does no substantive formal work. The abstract's claim of "theoretical grounding" overstates what this definition provides. The paper would be more accurate presenting it as an intuitive framing rather than a formalization.

2. **No variance or statistical uncertainty.** The paper reports single deterministic MIRA values and single AUROC values per model–detector–OoD combination. While the Reproducibility Statement notes that seeds were fixed (making replication exact), this does not address whether rankings are stable under different training initializations or data subsets. With 3–5 models per domain, a single rank flip would weaken the evidence considerably.

### Trivial
None.

## Nice-to-Haves

- Ablations on the perturbation range threshold (e.g., accuracy thresholds of 70%, 80%, 90%) to test rank stability.
- Reporting correlations (Spearman's ρ) with each of the three OoD detectors separately, not just the best-of aggregate.
- A pooled scatter plot (MIRA vs. best AUROC) across all models with domain labels.
- Clarifying how the integral in Equation (4) is discretized in practice (how many ε values, whether p(ε) is uniform).

## Removed Points

- **"Average column is ambiguous"** — The formatting ambiguity is likely a parser artifact (the caption states the column's meaning). Removed.
- **"Related work connection not drawn tightly"** — Vague/subjective assessment. Removed.
- **"Move limitations earlier"** — Presentation suggestion, not a weakness. Moved to Nice-to-Haves.
- **"Appendix B.6 details stripped"** — Not a paper flaw; acknowledged as a parser issue by the reviewer. Removed.
- **"Strength of attack claim is under-explored"** — Duplicates the ablation concern about perturbation range (Major weakness 3). Merged.

## Novel Insights

The most insightful observation from the reviews is the near-perfect rank alignment between MIRA and best OoD AUROC across all 13 models and 3 domains. This is not a noisy trend — it holds uniformly — and it suggests that monitorability (as measured by MIRA) and OoD detection performance are closely linked, potentially through the geometry of the learned feature space. The reviews also surface the concern that MIRA's validation is partially circular due to shared reliance on Mahalanobis distance with one of the three reference detectors, which the paper should address directly with per-detector correlations. None of these observations go beyond what the paper's own data and design permit, but together they sharpen the required revision path.

## Suggestions

1. **Quantify the correlation.** Compute and report Spearman's rank correlation between MIRA and the best OoD AUROC (per domain and pooled). A scatter plot with one point per model, colored by domain, would make the evidence immediate and quantitative.
2. **Disentangle the validation circularity.** Report the correlation of MIRA with each of the three detectors (ODIN, Mahalanobis, Energy) separately. If MIRA correlates strongly with ODIN- and Energy-based detection alone, the circularity concern is largely resolved.
3. **Add at least one ablation.** Show that MIRA rankings are stable under different choices of ε_min (e.g., thresholds corresponding to 70%, 80%, 90% accuracy). This would significantly increase confidence in the metric's robustness.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>