##Summary

This paper introduces the concept of *monitorability* for deep neural networks—the intrinsic ability of a model’s internal representations to support runtime error detection. The authors propose the MIRA Score, a practical metric that quantifies monitorability by applying norm-bounded input perturbations (FGSM) to in-distribution data and measuring the separability of perturbed versus unperturbed activations using a Mahalanobis-based surprisal score. Experiments across vision, tabular, and NLP domains show that MIRA correlates with the best achievable out-of-distribution (OoD) detection performance across three representative methods, suggesting it can serve as a pre-deployment tool for model selection.

## Strengths

- **Novel problem formalization.** The paper provides the first formal definition of monitorability (Definition 1) as a distinct property of neural networks, separate from accuracy or OoD detection performance. This fills a clear gap in the literature.
- **Practical and efficient metric.** MIRA requires only in-distribution data and lightweight FGSM perturbations, making it computationally feasible for pre-deployment evaluation without needing external OoD datasets or detector-specific tuning.
- **Broad empirical validation.** Experiments span three data modalities (vision, tabular, NLP) and multiple architectures (CNNs, ViTs, MLPs, Transformers), demonstrating consistent alignment between MIRA and the best OoD detection performance across diverse settings.
- **Intuitive grounding.** The use of input perturbations to probe decision-boundary behavior is well motivated by prior work (Lee et al., 2018a) and the t-SNE visualizations provide clear qualitative support for the metric’s interpretation.

## Weaknesses

### Fatal
None.

### Major
1. **Validation relies on an indirect proxy.** The paper validates MIRA by comparing it to the “best achievable OoD detection performance” across three methods. However, monitorability (Definition 1) is about detecting *any* error (loss > ε), not just OoD inputs. The experiments do not evaluate MIRA’s ability to predict detection of in-distribution misclassifications, which is a core part of the definition. This gap weakens the claim that MIRA measures monitorability as defined.
2. **No quantitative correlation measure.** The paper only provides qualitative alignment (e.g., “higher MIRA scores consistently align with stronger OoD detection”). A Spearman rank correlation (or similar) between MIRA and the best AUROC across models would strengthen the validation and allow readers to assess the strength of the relationship.
3. **MIRA scores are not normalized and vary drastically across domains** (e.g., NLP scores in the thousands, vision scores below 100). This makes cross-domain comparison meaningless and raises questions about the metric’s scaling. The paper does not discuss normalization or provide guidance on interpreting absolute values.
4. **Perturbation strategy and epsilon selection are ad-hoc.** The choice of FGSM (rather than stronger attacks) and the procedure for setting ε_min (based on an accuracy threshold) are not rigorously justified. The paper acknowledges this as a limitation but does not study sensitivity to these choices, which could affect the metric’s reliability.
5. **Table presentation is confusing.** The “Average” column in Tables 1–3 is described as “the average of the AUROC scores among the three monitoring methods,” but the table shows per-method averages across OoD datasets, not an average across methods. This inconsistency makes it hard to verify the claimed correlation.

### Minor
- Only three OoD detection methods are used as the proxy baseline. While they are diverse, the paper does not justify why these are sufficient to capture the “best achievable” performance.
- Results are reported as point estimates without confidence intervals or error bars, which is common but limits the ability to assess variability.
- The claim of being “the first formalization of monitorability” is strong; the paper should more carefully distinguish its contribution from prior work on activation monitoring (e.g., NAPs, box abstraction) that also characterizes internal representations for error detection.

### Trivial
None.

## Nice-to-Haves
- Provide Spearman rank correlation between MIRA and best AUROC across all models in each domain.
- Study sensitivity of MIRA to the choice of perturbation method (e.g., compare FGSM with PGD or Carlini-Wagner) and to the epsilon selection procedure.
- Evaluate MIRA’s ability to predict detection of in-distribution misclassifications (e.g., using label-flipping or synthetic errors) to directly validate Definition 1.
- Propose a normalization scheme (e.g., dividing by the expected χ² surprisal under the null) to make MIRA scores comparable across layers and domains.

## Novel Insights

The key insight is that monitorability can be quantified by measuring how separable perturbed (boundary-proximal) activations are from clean activations in feature space, using a dimension-calibrated surprisal score. This connects the geometry of the learned feature space to the detectability of errors, and the paper shows that this simple, data-free metric correlates well with the best OoD detection performance across diverse models and modalities. The idea of using controlled perturbations to probe the model’s own sensitivity, rather than relying on external OoD data, is both elegant and practical.

## Suggestions
- Add a quantitative correlation analysis (e.g., Spearman ρ) between MIRA and the best AUROC across models for each domain, and report it in the main paper.
- Clarify the “Average” column in the tables: either compute a single average across methods and OoD datasets, or clearly label the per-method averages.
- Discuss the limitation that MIRA is validated only against OoD detection, not against detection of in-distribution errors, and outline how future work could address this.
- Provide guidance on interpreting MIRA values (e.g., what constitutes a “good” score) and consider a normalization that makes scores comparable across architectures and domains.

## Score and Decision

**Score:** 6  
**Decision:** Accept

The paper introduces a novel and well-motivated concept with a practical metric, supported by extensive experiments across multiple domains. However, the validation is indirect (relying solely on OoD detection as a proxy) and lacks quantitative rigor (no correlation measure, ad-hoc perturbation choices). These issues are significant but not fatal; they can be addressed in revision. The contribution is valuable enough to warrant acceptance at a borderline level.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>