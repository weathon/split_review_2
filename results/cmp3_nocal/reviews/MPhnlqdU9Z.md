## Summary

This paper introduces the concept of *monitorability*—the intrinsic ability of a neural network's internal features to reveal errors—and proposes the MIRA score, a metric that quantifies this property by perturbing ID inputs with FGSM and measuring how separable the resulting perturbed and unperturbed activations become in a Mahalanobis-based surprisal space. The validation across vision (CIFAR-10/100), tabular (Sensorless Drive), and NLP (SST-2) domains shows that MIRA rankings broadly align with the best OoD detection AUROC among three detectors (ODIN, Mahalanobis, Energy).

## Strengths

- **Novel conceptual framing.** The idea that two models with identical accuracy can differ in how *detectable* their errors are from internal features is clearly articulated. The toy example in Figure 1, where two networks achieve 100% ID accuracy but produce very different OoD feature separability, is the paper's most effective pedagogical device. This framing is genuinely new and could influence how practitioners think about model selection.

- **Multi-modal evaluation spanning vision, tabular, and NLP.** The paper covers three distinct data modalities with multiple architectures per domain, supporting the claim that MIRA's behavior is not an artifact of a single domain.

- **Sensible validation strategy for a first-of-its-kind metric.** Since no existing "monitorability" baseline exists, benchmarking MIRA against the best achievable OoD detection performance across three detectors with different principles (confidence-based, distance-based, energy-based) is a reasonable approach, and taking the best-of-three removes some detector-specific confounding.

## Weaknesses

### Fatal
None.

### Major

1. **Validation sample is too small and lacks statistical rigor.** Each domain evaluates only 3–5 models. The paper claims "strong correlation" and "good correlation" (lines 153, 271) based on visual rank-ordering, but reports no correlation coefficient (Spearman's ρ, Kendall's τ), no confidence intervals, no error bars on any metric, and no test of statistical significance. With 3–5 data points, a rank ordering can be driven by a single outlier or by a confound like model capacity (in the vision experiments, ViT is both the most expressive architecture and the highest-scoring). This makes it impossible to assess whether MIRA adds information beyond what model size already predicts.

2. **Validation establishes convergent validity, but the independence of this validation is limited.** MIRA is validated by correlating it with OoD detection methods (ODIN, Mahalanobis, Energy) that themselves depend on the geometric structure of the feature space—the same structure MIRA measures. In particular, both MIRA and the Mahalanobis detector use Mahalanobis distance to evaluate separability in activation space. The correlation therefore shows that a measure of feature-space separability correlates with other measures of feature-space separability. An independent validation would require showing that MIRA *predicts* detection performance in a setting where the detectors cannot yet be evaluated (e.g., ranking models on a held-out set of OoD datasets not used to compute the correlation). As written, the paper establishes convergent validity, which is evidence in the right direction but not sufficient to support the strong claim that MIRA is a "reliable tool for evaluating and comparing monitorability across different models" (abstract).

### Minor

1. **Definition 1 is an existential statement that imposes no constraint on the model.** Definition 1 (lines 65–71) states that a model is *l*-monitorable if there *exists* a set Z^l and threshold ε such that loss ≤ ε iff the layer-l activation falls in Z^l. The paper acknowledges Z^l "may be arbitrarily complex" (line 73). For any model, one can always construct such a Z^l by brute force (e.g., Z^l = {f^l(x) : L(f(x), y) ≤ ε}). The definition therefore does not distinguish monitorable from non-monitorable models. A meaningful definition would need to constrain the complexity of Z^l. The paper's practical contribution (MIRA) does not depend heavily on this definition, but the paper claims "the first formalization" as a contribution (line 23), and this formalization is empty as stated.

2. **No comparison to simpler static feature-space baselines.** The paper never tests whether a straightforward measure of feature-space quality—such as the average pairwise Mahalanobis distance between class centroids, the Fisher discriminant ratio, or the silhouette score on the penultimate layer—correlates equally well with OoD detection performance. Without such a baseline, it is unclear whether the complexity of the MIRA perturbation procedure (FGSM, integration over ε, chi-squared surprisal conversion) adds value beyond a static snapshot of the feature space. This is the most impactful missing ablation.

3. **MIRA scores differ across domains by orders of magnitude without explanation.** Vision MIRA scores range from about −0.07 to 89, tabular from 4 to 63, and NLP from 2,015 to 3,793. The paper does not discuss why the scale varies so dramatically or whether cross-domain comparisons are meaningful. This suggests the metric is not calibrated across domains, and the reader cannot tell whether a score of 3,000 in NLP means "highly monitorable" or simply reflects higher-dimensional feature spaces that produce larger chi-squared surprisal values.

4. **Missing ablations.** The paper uses FGSM perturbations without comparing to other perturbation strategies (random perturbations, PGD, or no perturbation). It also only evaluates the penultimate layer. The conclusion (line 287) acknowledges both as future work, but even a small experiment—e.g., comparing two perturbation types or two layers—would substantially strengthen the paper. Similarly, the ε_min selection procedure (line 131) is described but never analyzed for sensitivity.

### Trivial
None.

## Nice-to-Haves

- **Predictive (rather than correlational) validation:** Split models into a development set and a held-out set, compute MIRA on the development set, and show it predicts which model achieves the best detection performance on held-out OoD data.
- **Control for model capacity:** Compare models of similar parameter counts to show MIRA captures something beyond "bigger model = better features."
- **Ablation on the perturbation direction** (FGSM vs. random vs. no perturbation) to justify why the adversarial direction is necessary.
- **Analysis of which layer(s) best capture monitorability** beyond the penultimate layer.

## Novel Insights

None beyond the paper's own contributions.

## Removed Points

- **"Validation is circular"** (from Critical Issue 1): This is too strong. The paper establishes *convergent validity* between MIRA and OoD detection performance, which is a standard approach when no ground-truth metric exists. The concern is real but is about insufficient independence, not circularity. This concern is retained in Major weakness #2 (reduced severity) and moved out of a "circular" framing.
- **"Ordering flips between ResNet-18 and DenseNet across CIFAR-10 and CIFAR-100"** (from Critical Issue 2): Factually incorrect. DenseNet scores higher than ResNet-18 in both CIFAR-10 (16.01 vs. 6.05) and CIFAR-100 (2.806 vs. 0.657). The ordering is consistent, not flipped.
- **"Cannot be independently verified"** (from Critical Issue 4 framing): The paper includes a reproducibility statement and links to code; the claim is unsubstantiated.
- **Strengths removed:** "Sensible validation strategy for a first-of-its-kind metric" is retained; generic praise about the problem being "important" is already covered.
- Various formatting/style/jargon nitpicks from the section-by-section notes that do not affect substance.

## Suggestions

1. Expand the model set to at least 8–10 models per domain and report rank correlation coefficients with confidence intervals.
2. Add a static feature-space baseline (e.g., Fisher discriminant ratio or silhouette score on the penultimate layer) and show that MIRA adds signal beyond it.
3. Fix Definition 1 by constraining Z^l to a tractable hypothesis class (e.g., Mahalanobis balls, convex sets) so that the definition carries content.
4. Explain or normalize the cross-domain scale differences in MIRA scores.
5. Add an ablation on perturbation strategy (at minimum: FGSM vs. random perturbation vs. no perturbation).

## Score and Decision

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Borderline Reject</decision>