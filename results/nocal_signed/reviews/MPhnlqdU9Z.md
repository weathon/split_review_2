Now let me analyze the scoring model's output and finalize my review.

The impact scores reveal a clear picture:
- **Strengths**: The conceptual novelty (+9.9) and formal definition (+9.0) are the paper's strongest assets. The multi-modality breadth (+6.9) is solid but secondary.
- **Weaknesses**: The lack of uncertainty quantification (−9.2) is the single most impactful weakness identified. The "best achievable proxy" oracle issue (−3.8) is moderately impactful. The validation confound (−1.6), perturbation range (−0.2), and cross-modal scale (−1.3) are relatively minor.

The strengths substantially outweigh the weaknesses in both magnitude and fundamentality. The core conceptual contribution (formalizing monitorability) is genuinely novel and well-executed. The main empirical gap (no uncertainty quantification) is a standard methodological concern that is addressable in revision. The validation confound, while real, is not fatal — MIRA and Mahalanobis OoD detection share a mathematical component but measure different quantities, and the CustomNet case shows MIRA can correlate with non-Mahalanobis detectors.

**Score: 6** — The paper introduces a genuinely novel concept with a clean formal definition and broad multi-domain experiments. The empirical validation has meaningful gaps (no uncertainty quantification, validation confound) that prevent a higher score, but these are addressable. The conceptual contribution is strong enough to warrant borderline acceptance.

Here is my final consolidated review:

---

## Summary

The paper introduces *monitorability* — the intrinsic property of a neural network to support runtime error detection through its internal activations — and proposes the MIRA Score, a metric that quantifies this property by measuring how distinguishable perturbed vs. unperturbed features are using Mahalanobis distance in penultimate-layer space. The metric requires only in-distribution data and controlled perturbations, avoiding the need for external OoD datasets. Experiments across vision, tabular, and NLP domains show that MIRA rank-orders models similarly to the best achievable OoD detection performance across three standard detectors.

## Strengths

- **Novel and well-motivated concept.** The observation that two models with identical accuracy can have radically different internal representations (Figure 1), leading to very different detectability of errors, is real and important. Section 3.1 effectively builds the case that accuracy alone is an insufficient criterion for model selection in safety-critical settings. No prior work has formalized this as a distinct property of neural networks.

- **Mathematically precise formal definition.** Definition 1 defines monitorability cleanly in terms of an internal layer and a loss-based threshold. Using a general loss function $\mathcal{L}$ (rather than hardwiring classification) makes the definition applicable beyond classification, and the explicit connection to runtime monitors ($Z^l$ can be the acceptance region of any given monitor) is conceptually sharp.

- **Broad multi-modality evaluation.** The experimental scope is unusually broad for a first paper on a new concept: vision (CIFAR-10/100 with 4 architectures and 7 OoD datasets), tabular (Sensorless Drive with 5 architectures), and NLP (SST-2 finetuning with 4 models and 4 OoD datasets). This demonstrates that the notion generalizes beyond a single domain.

## Weaknesses

### Fatal

None.

### Major

- **No uncertainty quantification for any reported value.** Every MIRA score and AUROC in Tables 1–3 is a point estimate with no standard deviation, confidence interval, or statistical significance test. For a paper whose central claim is a *correlation* between two quantities, this is a significant gap — the reader cannot assess whether the observed rank orderings are statistically reliable or could be driven by noise. This is especially concerning for the tabular results (Table 2), where per-class AUROCs fluctuate wildly (e.g., ODIN ranges from 0.0 to 91.46), suggesting high variance that should be quantified. The paper states algorithms are deterministic and random seeds are fixed, which mitigates but does not eliminate the need for reported variability.

### Minor

- **The validation strategy has a confound with Mahalanobis distance.** MIRA uses Mahalanobis distance to compute feature separability (Eq. 3), and it is validated against a "best achievable" OoD detection aggregate that includes the Mahalanobis-distance detector (Lee et al., 2018b). Across Tables 1–3, the Mahalanobis detector is the dominant best performer (57% of vision cases, 100% of tabular and NLP cases). This shared mathematical core creates a confound: the observed correlation may partly reflect that a Mahalanobis-based metric correlates with Mahalanobis-based detection, rather than establishing MIRA as a general measure of intrinsic monitorability. The paper would be strengthened by validating MIRA against non-Mahalanobis detectors individually (ODIN, Energy) rather than only in a best-of aggregate, or against activation-pattern-based monitors (box abstraction, NAP methods) that operate on different principles. *(Note: this is not fatal — MIRA measures separability of perturbed vs. unperturbed features, which is a different quantity from Mahalanobis OoD detection on real OoD data; and the CustomNet case shows MIRA correlating with ODIN, not Mahalanobis — but the confound weakens the core validation nonetheless.)*

- **The "best achievable OoD detection" proxy uses an oracle-level selection.** The proxy selects the maximum over three detectors per OoD dataset, which a practitioner cannot replicate without knowing which detector will work best ahead of time. This inflates apparent monitorability by measuring "what performance could be with perfect detector selection" rather than "what performance a practitioner would actually achieve." The paper should also report correlations with individual detectors separately.

- **MIRA scores are on vastly different scales across modalities** (vision: ~−0.07 to 89; tabular: ~4 to 64; NLP: ~2000 to 3800). The chi-square survival function calibration (Eq. 3) is meant to normalize for feature dimensionality, but it clearly does not produce comparable scores across very different dimensionalities. The paper only uses MIRA for within-modality rank ordering, which limits its utility as a general-purpose tool and suggests the calibration needs revisiting.

- **The perturbation range selection introduces a confound with model robustness.** $\epsilon_{\min}$ is defined as "the smallest value that reduces accuracy to a certain threshold" and $\epsilon_{\max} = 2 \cdot \epsilon_{\min}$ (Sec. 4.2), meaning different models are evaluated at different perturbation magnitudes. A more robust model (requiring larger perturbations to degrade accuracy) will be evaluated at larger $\epsilon$, where perturbations are more likely to cross decision boundaries. The gap between WideMLP (MIRA=63.51) and DeepTransformer (MIRA=4.37) in the tabular experiments could partially reflect different perturbation magnitudes rather than intrinsic feature separability. The paper acknowledges this limitation in the conclusion but does not quantify its impact.

### Trivial

None.

## Nice-to-Haves

- Report Spearman/Pearson correlation coefficients (with confidence intervals) between MIRA and detection AUROC across models, rather than relying on visual rank-order inspection.
- Validate against a prediction-style holdout task: compute MIRA before seeing OoD data, then check whether the ranking matches OoD detection ranking on a held-out set.
- Add sensitivity analysis for the choice of $p(\epsilon)$ distribution, perturbation method (FGSM vs. PGD vs. random noise), and layer choice.

## Removed Points

These points were flagged in the input review but are removed for the following reasons:

- **"Validation is nearly tautological"** — Removed. This overstates the case. MIRA measures separability of *synthetic perturbed* vs. unperturbed features, while the Mahalanobis OoD detector measures distance of *real OoD test points* from class centroids. These are different quantities sharing a mathematical building block. The CustomNet case (CIFAR-10: MIRA = −0.07, best detector = ODIN, not Mahalanobis) directly contradicts the tautology claim. The valid confound concern is retained in the Minor weaknesses above.

- **Gaussian assumption unvalidated** — Removed. The paper cites Lee et al. (2018b) which established this assumption for neural network features. Relying on established prior results is standard practice.

- **Missing appendix content criticisms** (no sensitivity analysis for $p(\epsilon)$, perturbation method, layer choice; perturbation threshold unspecified) — Removed. The appendix was stripped during PDF parsing; these details may exist in the original submission. Per the rules, missing appendix content cannot be verified.

- **"No discussion of failure cases"** — Removed. This is a reasonable suggestion for future work but not a weakness of the paper as presented.

- **t-SNE stability concern** — Removed. t-SNE is used purely for visualization intuition; the quantitative claims do not depend on it.

- **Definition 1 requiring a perfect monotonic relationship** — Removed. The definition is intentionally idealized; the paper's contribution is providing MIRA as a practical approximation, not proving that perfect monitorability exists in practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add uncertainty quantification: run experiments with multiple random seeds and report standard deviations or confidence intervals for both MIRA and AUROC values.
2. Validate MIRA against non-Mahalanobis detectors individually (ODIN, Energy), and/or against activation-pattern-based monitors (box abstraction, NAP methods) that operate on different principles.
3. Control for perturbation magnitude by reporting MIRA at a fixed set of $\epsilon$ values across all models, to disentangle robustness from feature separability.
4. Clarify the specific accuracy threshold used for $\epsilon_{\min}$ selection in the main text.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>