## Summary

This paper introduces the concept of *monitorability* for neural networks—the intrinsic ability of a model to highlight potential inference errors through its internal activations. The authors propose the MIRA Score, a practical metric that quantifies monitorability by applying norm-bounded input perturbations toward the decision boundary and measuring the separability of the resulting internal representations using Mahalanobis distance and a surprisal score. Experiments across vision, tabular, and NLP domains show that MIRA correlates with the best achievable out-of-distribution (OoD) detection performance among three representative methods, suggesting it can serve as a pre-deployment evaluation tool.

## Strengths

- **Novel formalization of monitorability.** The paper provides the first formal definition of monitorability as a distinct property of neural networks, separate from inference accuracy or OoD detection performance. This conceptual contribution is timely and relevant for safety-critical applications.
- **Simple, efficient, and data-efficient metric.** MIRA requires only in-distribution data and lightweight FGSM perturbations, making it practical for pre-deployment model selection without needing external OoD datasets or extensive detector tuning.
- **Broad empirical evaluation.** Experiments span three data modalities (vision, tabular, NLP) and multiple architectures (CNNs, ViTs, MLPs, Transformers), demonstrating the generality of the approach. The t-SNE visualizations provide intuitive support for the metric.

## Weaknesses

### Fatal
None.

### Major

- **Validation relies on qualitative correlation, not quantitative evidence.** The paper claims MIRA “correlates with the best achievable OoD detection performance” but provides no correlation coefficient (e.g., Spearman rank correlation) or statistical test. The tables show that higher MIRA generally aligns with higher average AUROC, but the relationship is not rigorously quantified, and there are exceptions (e.g., DenseNet on CIFAR-100 has MIRA 2.81 but average AUROC comparable to ViT’s 53.23? Actually ViT has much higher AUROC; but the ordering is not perfect across all models). Without a quantitative measure, the strength of the claimed correlation is unclear.
- **Ad-hoc perturbation range selection.** The choice of \(\epsilon_{\min}\) (smallest value reducing accuracy to a threshold) and \(\epsilon_{\max}=2\epsilon_{\min}\) is empirically motivated but not justified theoretically. No sensitivity analysis is performed to show how MIRA changes with different range choices or whether the metric is robust to this design decision. This is a core component of the metric and its arbitrariness weakens the claim of a principled measure.
- **No comparison to simpler intrinsic baselines.** The paper validates MIRA only against OoD detection methods. It does not compare MIRA to other simple model properties that might also correlate with OoD detection, such as average softmax confidence on ID data, feature space compactness (e.g., average intra-class distance), or gradient magnitude. Without such comparisons, it is unclear whether MIRA provides unique information beyond these simpler statistics.
- **Validation limited to three OoD detectors.** The “best achievable” performance is taken from only ODIN, Mahalanobis, and Energy-based scoring. It is possible that a model with high MIRA could still perform poorly with other monitoring methods, or that a model with low MIRA could be effectively monitored by a different detector. The paper does not discuss this limitation or test additional detectors.

### Minor

- **MIRA scores are not comparable across domains.** The scores vary dramatically (e.g., NLP models yield values in the thousands, vision models below 100). While the paper does not claim cross-domain comparison, the lack of a normalized scale could be confusing and limits the metric’s interpretability.
- **Definition 1 uses an “iff” condition** that is unlikely to hold exactly in practice. The paper does not discuss how to relax this condition or what approximation error is acceptable. The MIRA metric is a practical proxy, but the gap between the formal definition and the metric is not analyzed.
- **The choice of \(p(\epsilon)\) in the integral is not specified** in the experimental section. It is presumably uniform, but this should be stated explicitly, and the impact of different distributions should be discussed.

### Trivial

- The paper could more clearly separate the conceptual contribution (monitorability) from the specific metric (MIRA) in the abstract and introduction.

## Nice-to-Haves

- An ablation study comparing FGSM to stronger perturbations (e.g., PGD) or random perturbations to justify the choice of FGSM.
- Sensitivity analysis of the \(\epsilon\) range and \(p(\epsilon)\) distribution to demonstrate robustness.
- Comparison to other feature-space metrics such as Fisher discriminant ratio or silhouette score on ID vs. perturbed features.

## Novel Insights

The paper reframes the problem of runtime monitoring from “how to detect failures” to “how detectable failures are in principle given the model’s internal representation.” This shift in perspective is valuable: it suggests that before deploying a monitor, one should first assess whether the model’s feature space is structured enough to support monitoring. The MIRA score operationalizes this by linking local boundary behavior (via perturbations) to global separability, providing a bridge between adversarial robustness and OoD detection that is not explicitly made in prior work.

## Suggestions

1. Provide a quantitative correlation measure (e.g., Spearman rank correlation) between MIRA and the average OoD AUROC across all models in each domain, and report confidence intervals.
2. Include an ablation study varying the perturbation range (e.g., different accuracy thresholds for \(\epsilon_{\min}\)) to show that MIRA rankings are stable.
3. Compare MIRA to at least one simple baseline (e.g., average softmax confidence on ID data) to demonstrate that MIRA captures information beyond what is already available.
4. Clarify the choice of \(p(\epsilon)\) in the experiments and consider using a distribution that emphasizes small perturbations (e.g., exponential decay) to align with the intuition that local behavior matters most.

## Score and Decision

**Score:** 6  
**Decision:** Borderline Accept

The paper introduces a novel and potentially useful concept with a practical metric. However, the validation is not yet rigorous enough to fully support the central claim of correlation. The major weaknesses—lack of quantitative correlation, ad-hoc perturbation range, and absence of baseline comparisons—prevent a stronger recommendation. These issues are addressable in revision, and the core idea has clear value to the community.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>