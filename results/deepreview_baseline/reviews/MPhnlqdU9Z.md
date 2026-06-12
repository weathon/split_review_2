## Summary

This paper introduces the concept of *monitorability* for neural networks—the intrinsic ability of a model's internal representations to reveal inference errors. The authors propose a formal definition of monitorability and develop a practical metric, the MIRA Score, which quantifies this property by applying norm-bounded input perturbations (FGSM) and measuring the separability of resulting penultimate-layer activations using a calibrated Mahalanobis distance. Experiments across vision, tabular, and NLP domains show that MIRA correlates with the best achievable out-of-distribution detection performance across multiple detectors, suggesting it can serve as a pre-deployment evaluation tool for comparing models' monitoring potential without requiring external OOD data.

## Strengths
1. **Novel problem formulation.** The paper is the first to formally define "monitorability" as a distinct property of neural networks, separating it from inference accuracy and standard OOD detection. This opens up a new axis for model evaluation and selection.
2. **Principled metric with practical appeal.** The MIRA Score is well-motivated, uses only in-distribution data and efficient FGSM perturbations, and avoids the need for external OOD datasets or detector tuning at evaluation time. The use of a surprisal transformation to handle varying layer dimensionalities is a sensible design choice.
3. **Broad empirical evaluation.** Experiments span three modalities (vision, tabular, NLP) and multiple architectures (CNNs, ViTs, MLPs, Transformers). The consistent correlation between MIRA and best OOD detection performance across diverse settings provides reasonable initial evidence for the metric's utility.
4. **Visual confirmation.** t-SNE visualizations of feature spaces qualitatively support the claim that higher MIRA scores correspond to better-organized, more separable representations.

## Weaknesses
### Fatal
None.

### Major
1. **Proxy validation methodology.** The paper validates MIRA by comparing it to the "best achievable OOD detection performance" across three methods. However, OOD detection performance is itself a measure of runtime detection quality, not an established ground truth for monitorability. The argument that this proxy is appropriate relies on the assumption that effective OOD detection *requires* monitorability, but the opposite direction is not proven. A model could be highly monitorable yet perform poorly on a specific OOD detector due to detector limitations, making the "best-of" aggregation noisy. Without a formal or causal link, the validation is indirect and correlational.

2. **Metric sensitivity to hyperparameters.** The MIRA Score depends on several choices: the perturbation method (FGSM), the distribution \(p(\epsilon)\) over perturbation magnitudes, and the heuristic for determining \([\epsilon_{\min}, \epsilon_{\max}]\) (smallest \(\epsilon\) reducing accuracy to a threshold, with \(\epsilon_{\max} = 2\epsilon_{\min}\)). The paper does not analyze how these choices affect the score or whether the ranking of models is robust. For example, different thresholds or integration distributions could change the ordering. This is critical because the metric is intended for model comparison.

3. **Weak formal definition.** Definition 1 states a model is \(l\)-monitorable if there exists a set \(Z^l\) such that correct predictions correspond to activations in \(Z^l\). Because \(Z^l\) can be arbitrarily complex, any model is trivially monitorable at the output layer (e.g., by defining \(Z^l\) as the set of activations that yield correct logits). This renders the definition vacuous and provides no theoretical guidance for the MIRA Score's design. The paper acknowledges this but does not refine the definition to include constraints (e.g., \(Z^l\) must be efficiently computable or geometrically simple).

### Minor
1. **Lack of uncertainty quantification.** MIRA scores are reported as single numbers without error bars or confidence intervals. Given that the metric involves sampling over perturbations and integration over \(\epsilon\), reporting variances across random seeds or bootstrapping would strengthen the results.
2. **Unbounded scale.** The surprisal score \(S\) can become arbitrarily large for points far from the class-conditional Gaussian. This makes MIRA scores difficult to interpret across domains (e.g., NLP scores > 3000 vs. vision scores < 100) and may amplify outliers. A normalized or bounded variant could improve practical interpretability.
3. **Penultimate layer fixation.** All experiments use only the penultimate layer. The paper claims MIRA can be applied to any layer, but no empirical evidence is provided. A study of layer-wise MIRA and its correlation with detection performance is missing.
4. **No comparison to simpler baselines.** While no prior monitorability metric exists, the paper could compare MIRA to simple feature-space statistics (e.g., per-class intra/inter variance ratios) to benchmark whether the perturbation-based approach adds value.

### Trivial
None.

## Nice-to-Haves
1. Formal statistical correlation measures (e.g., Spearman rank correlation) between MIRA and average OOD AUROC across models, to quantify the claimed relationship.
2. Ablation on the choice of perturbation (e.g., PGD vs. FGSM, different norms) and the distribution \(p(\epsilon)\) (e.g., uniform vs. concentrated near \(\epsilon_{\min}\)).
3. Investigation of when MIRA fails (e.g., models where correlation breaks down) would deepen understanding of the metric's limitations.

## Novel Insights
Beyond the paper's own contributions, a genuinely novel observation is that the local decision boundary geometry, probed via simple FGSM perturbations, can serve as a proxy for the global separability of ID and OOD features in the penultimate layer. This connection between local adversarial sensitivity and broader monitoring potential is not explicitly established in the OOD detection literature and may inspire further theoretical analysis.

## Suggestions
1. Strengthen the definition of monitorability by requiring \(Z^l\) to be efficiently representable (e.g., as a simple geometric region or a set with low description complexity) to make it non-trivial.
2. Include a robustness analysis of MIRA to its hyperparameters (especially \(\epsilon_{\min}\) threshold and \(p(\epsilon)\)), showing that model rankings are stable over a reasonable range.
3. Add error bars to MIRA scores and report rank correlations to quantitatively support the validation claim.

## Score and Decision

**Score:** 6  
**Decision:** Accept  

The paper introduces a novel and well-motivated concept with a practical metric, supported by broad empirical evidence. The major weakness is the indirect validation methodology and lack of sensitivity analysis, but these do not invalidate the core contribution. With improvements to the formal definition and additional robustness studies, the work has clear value to the community.

MY FINAL SCORE: 6<score>6</score>
MY FINAL DECISION: Accept