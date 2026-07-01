Now I have all the information I need. Let me write the final consolidated review.

---

## Summary

This paper introduces the concept of *monitorability* — the intrinsic ability of a neural network's internal representations to support runtime error detection — and proposes the MIRA score, a practical metric that quantifies this property using only in-distribution data and FGSM perturbations. MIRA works by measuring how separable perturbed and unperturbed internal activations are via Mahalanobis distance. The authors validate MIRA by comparing it against the best OoD detection performance across three diverse methods (ODIN, Mahalanobis, Energy), in vision, tabular, and NLP domains, showing a consistent qualitative ranking agreement.

## Strengths

- **Genuinely novel conceptual contribution.** The observation that two models with identical ID accuracy can have dramatically different feature-space structure that supports or resists error detection (Figure 1) is both true and underexplored. The paper is the first to formalize monitorability as a distinct property.

- **Clean and practically efficient metric.** MIRA requires only ID data and single-step (FGSM) perturbations, making it feasible as a pre-deployment evaluation tool. This is a real practical advantage over methods requiring OoD data or expensive attack procedures.

- **Evaluation across three modalities** (vision: CIFAR-10/100 with 4 architectures; tabular: Sensorless Drive with 5 architectures; NLP: SST-2 with 4 transformers) with consistent qualitative trends, supporting the claim that the metric captures something general rather than domain-specific.

- **Qualitative t-SNE validation (Figure 2)** provides an interpretable check that higher MIRA scores correspond to visibly better feature-space organization.

## Weaknesses

### Fatal
None.

### Major
1. **Validation is against a proxy (OoD detection), not error detection, creating a gap with the paper's own framing.**  
   The paper motivates monitorability as error detectability ("the intrinsic ability of a model to highlight potential inference errors," Abstract; "even when misclassifications occur on ID inputs," §3.1). Yet the validation exclusively uses OoD detection performance as a proxy (§4.1). The paper itself notes that "misclassifications may also occur for ID inputs, which is a distinct scenario not directly addressed by OoD detection" (§2). This is not a concealed flaw — the paper is candid about the proxy — but it means the central claim that MIRA measures *error detectability* (as opposed to *distributional shift detectability*) remains untested. A model could have strong OoD detection but weak error detection on ambiguous ID inputs, or vice versa.

2. **No quantitative correlation metric is reported.**  
   The headline empirical claim is that "MIRA correlates with the best achievable OoD detection performance" (§4.4). The evidence consists of visual inspection of 3–5 models per domain with a consistent rank ordering. No Spearman rank correlation, Pearson correlation, or any quantitative agreement measure is computed. With 4–5 data points per domain, the ordering could change with different OoD datasets or detection methods. The claim of "correlation" requires a quantitative measure of its strength and statistical reliability.

3. **MIRA shares a core methodological component (Mahalanobis distance) with one of the three validation detectors, creating a potential confound.**  
   MIRA measures feature-separability via Mahalanobis distance (§3.3). One of the three OoD detectors used for validation — the Mahalanobis detector (Lee et al., 2018b) — also computes Mahalanobis distance in feature space. Examining Table 1, the Mahalanobis detector is often (though not always) the best-performing method. The paper does not attempt to disentangle whether MIRA's apparent success reflects genuine monitorability or partly arises because both MIRA and the best-performing detector share the same geometric tool. The confound is partial (e.g., CustomNet's best detector is ODIN, not Mahalanobis, and MIRA still ranks lowest), but it merits explicit discussion and an ablation with alternative distance measures.

4. **The perturbation range calibration ties MIRA to model robustness in a way that is not disentangled.**  
   The perturbation interval [ε_min, ε_max] is calibrated per model based on accuracy degradation: ε_min is the smallest perturbation reducing accuracy to a threshold, and ε_max = 2·ε_min (§4.2). Less robust models are probed with smaller absolute perturbations, while more robust ones receive larger perturbations. Since FGSM perturbation magnitude scales with ε, more robust models get a larger perturbation budget, likely producing more detectable feature shifts. The observed correlation could partly reflect robustness rather than feature-space structure per se. The paper acknowledges this as a "current limitation" (§6), but does not quantify or control for the confound in the current experiments.

### Minor
1. **Definition 1 is framing only and does not do substantive work.** The formal definition of monitorability (Def. 1) quantifies over the data distribution and is not trivially satisfiable, but it is never used to derive MIRA or any subsequent result. The MIRA score is introduced as an operational heuristic with no formal link back to Definition 1. The definition could be removed without affecting the paper's technical contributions.

2. **No variance or uncertainty quantification for any reported number.** All experiments use a single fixed seed (§Reproducibility Statement). No error bars, confidence intervals, or multiple-run statistics are reported. For a metric intended to guide model selection, the stability of MIRA under different data splits, initialization seeds, or perturbation configurations is essential.

3. **No ablation studies on MIRA's design choices.** The paper tests only one configuration of MIRA. It does not explore alternative perturbations beyond FGSM, alternative distance metrics (e.g., Euclidean, cosine), different layer choices, or alternative integration schemes for p(ε). This makes it impossible to assess whether the reported results are robust or an artifact of specific settings.

4. **The FGSM direction concern is dismissed too quickly.** The paper argues that "the strength of the attack is not critical" (§4.2), but the *direction* of the perturbation (not just its magnitude) determines which region of feature space is probed. For models with highly non-linear boundaries, single-step FGSM can produce different perturbation directions than iterative methods. This warrants a discussion or empirical check.

5. **The detector-agnostic claim in §4.4 is not substantiated systematically.** The paper cites the case where "the Mahalanobis detector failed with Places365 for DenseNet, yet the other methods were still achieving performance in line with the average" as evidence of detector-agnostic insight. This example merely shows that other methods performed well — it does not establish that MIRA captures a deeper property beyond the average of the three detectors.

### Trivial
- The ℓ_p norm used in experiments is not explicitly stated: equation (2) defines a general ℓ_p-perturbed dataset with p ∈ [1, ∞], and FGSM (ℓ_∞) is used, but the paper does not confirm which p was applied.
- The "Average" column caption in Table 1 ("the average of the AUROC scores among the three monitoring methods") is ambiguous — it actually reports per-method averages across OoD datasets, not a single aggregated "best achievable" number per model, making the claimed correlation with MIRA harder to verify directly from the tables.

## Nice-to-Haves
- **Compare MIRA against simpler baselines**, such as the average class-conditional Mahalanobis distance on unperturbed ID features, or the average softmax confidence on ID data, to establish that MIRA's rankings are not already captured by trivially simpler measures.
- **Validate MIRA against direct error detection** (e.g., using the perturbation method itself to construct an error-detection evaluation on ID misclassifications), which would directly test the paper's stated motivation.
- **Ablate alternative distance/separability measures** (Euclidean distance, cosine distance, classifier-based separability) to disentangle the Mahalanobis confound and strengthen the generality claim.
- **Discuss the absolute scale of MIRA across domains** (vision: −0.07 to 89; tabular: 4–63; NLP: 2000–3800) and whether cross-domain comparisons are meaningful.

## Removed Points
- *MIRA scale changes unpredictably across domains* — This is expected due to different feature dimensionalities and is a natural consequence of the chi-square calibration; it is an observation, not a weakness.
- *No mention of prior work on representation quality metrics* — This is a related-work scope expansion that the paper is not obligated to cover.
- *Definition 1 is "vacuous" (critic's characterization)* — The definition quantifies over the entire data distribution P_in, not a finite dataset, so it is not trivially satisfiable as claimed. However, the substantive point (the definition does no work) is retained as a Minor weakness above.

## Novel Insights
The reviews surface that the paper's core tension — validating an error-detectability metric against OoD detection — is the single most important gap, and that the lack of quantitative correlation statistics leaves the headline claim unmeasured. A further insight is that the perturbation-range calibration may inadvertently bake in a robustness confound; the paper's own acknowledgment of this as a limitation is honest but does not resolve it. The Mahalanobis confound between MIRA and one of the three validation detectors is noted, but a careful reading of Table 1 shows the confound is partial (the best detector is not always Mahalanobis), which actually strengthens MIRA's case rather than weakening it in those instances.

## Suggestions
1. **Report Spearman rank correlation** (and ideally a pooled analysis across all models) for each domain to quantify the claimed correlation.
2. **Add a direct error-detection validation experiment** — e.g., use the perturbation method to create near-boundary ID samples that are misclassified, then test whether MIRA predicts their detectability.
3. **Run an ablation with an alternative distance metric** (e.g., cosine distance instead of Mahalanobis) in MIRA to rule out the Mahalanobis confound.
4. **Report all numbers with error bars** (at least 3 random seeds) to establish stability.
5. **Include a controlled experiment** where two models with the same robustness (same ε_min) but different feature-space structure are compared, to disentangle MIRA from robustness.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>