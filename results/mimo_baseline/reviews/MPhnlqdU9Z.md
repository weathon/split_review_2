## Summary

This paper introduces the concept of *monitorability* for neural networks — the intrinsic ability of a model's internal representations to enable runtime detection of erroneous predictions. The authors formalize this property (Definition 1), propose a practical metric called the MIRA Score that quantifies monitorability using norm-bounded input perturbations and Mahalanobis distance-based surprisal scores, and validate it empirically across computer vision, tabular, and NLP domains by correlating MIRA scores with the best achievable OoD detection performance across three established methods.

## Strengths

- **Genuinely novel concept with formal grounding.** Monitorability as a property of neural network representations is, to the best of my knowledge, not previously formalized in the literature. Definition 1 provides a clear mathematical characterization, and the distinction from both OoD detection (a method) and robustness (a property of predictions) is well articulated. This fills a real conceptual gap.

- **Practical metric requiring only ID data.** The MIRA Score is designed to be computed pre-deployment without external OoD datasets, which is a significant practical advantage over evaluation approaches that require curated OoD benchmarks. The use of FGSM perturbations is computationally efficient and well-motivated by prior work on decision boundary behavior (Lee et al., 2018a).

- **Multi-modal experimental evaluation.** The authors evaluate across vision (CIFAR-10/100 with 4 architectures), tabular (Sensorless Drive Diagnosis with 5 architectures), and NLP (SST-2 with 4 transformer variants), demonstrating consistent trends across modalities. The monotonic ordering of MIRA scores aligns with detection performance in all cases (e.g., on CIFAR-10: ViT 89.25 → DenseNet 16.01 → ResNet-18 6.05 → CustomNet -0.07).

- **t-SNE visualizations provide intuitive support.** Figure 2 effectively illustrates that higher MIRA scores correspond to more structured and separable feature spaces, grounding the quantitative metric in visual intuition.

## Weaknesses

### Fatal
None.

### Major

- **No formal correlation statistics.** The paper repeatedly claims that "MIRA Score correlates with the strongest actual detection performance" but never reports a formal correlation coefficient (e.g., Spearman's ρ or Pearson's r). With only 4 models in vision/NLP and 5 in tabular, the reader is left to eyeball tables rather than verify the statistical strength of the relationship. This is a significant gap for a paper whose central claim is correlational. Reporting Spearman ρ with confidence intervals (or at minimum a scatter plot of MIRA vs. best AUROC) would substantially strengthen the paper.

- **Inherent circularity in validation methodology.** Monitorability is defined as the intrinsic ability to detect failures from internal activations, yet it is validated exclusively against OoD detection performance — which is precisely the task monitorability is supposed to characterize. The paper partially acknowledges this by using a "best-of" aggregation across three methods (ODIN, Mahalanobis, Energy), arguing this approximates the "most favorable monitoring potential." However, this argument would be considerably stronger with evidence that MIRA captures something beyond what any single well-calibrated detector can achieve, or with validation against a qualitatively different downstream task (e.g., predicting calibration error, confidence misalignment, or reliability under distribution shift).

- **Small model count per domain limits generalizability claims.** Testing 4-5 architectures per modality provides suggestive but not compelling evidence. The architecture families tested (ResNet, DenseNet, ViT, custom CNN for vision; MLP variants and transformers for tabular/NLP) are reasonable, but adding more architectures — particularly varying capacity within a family (e.g., ResNet-18 vs. ResNet-50 vs. ResNet-152) — would help distinguish whether MIRA captures genuinely monitorability-related variation or simply correlates with model capacity/accuracy.

### Minor

- **Definition 1 is effectively vacuous without the metric.** The biconditional $\mathcal{L}(f(x), y) \leq \epsilon \iff f^l(x) \in Z^l$ holds for any model given a sufficiently expressive $Z^l$, as the authors implicitly acknowledge ("$Z^l$ may be arbitrarily complex"). The definition serves primarily as motivation for the metric rather than as a substantive analytical tool. The paper would benefit from discussing conditions under which monitorability (per the definition) is guaranteed to hold with tractable $Z^l$, e.g., under the GDA assumption.

- **No ablation on key design choices.** Several design decisions are not ablated: (a) the choice of FGSM as perturbation method vs. alternatives (PGD, random perturbations); (b) the specific strategy for selecting $[\epsilon_{\min}, \epsilon_{\max}]$; (c) the choice of uniform $p(\epsilon)$; (d) sensitivity to layer selection (the paper always uses the penultimate layer). While the paper acknowledges the perturbation range limitation, a basic ablation on perturbation method would strengthen confidence in the metric's robustness.

- **Scale of MIRA varies enormously across domains** (e.g., ~6-89 for vision, ~2000-3800 for NLP), raising questions about interpretability and cross-domain comparability. While within-domain comparisons are sufficient for the current claims, discussing normalization or calibration for cross-domain use would be valuable for practitioners.

### Trivial
None.

## Nice-to-Haves

- A scatter plot of MIRA Score vs. best achievable AUROC (across all three modalities on a single figure) with reported Spearman/Pearson correlation coefficients would be a compelling addition to Section 4.4.
- An ablation comparing FGSM perturbations against random noise perturbations of equivalent magnitude, to verify that the directional component (toward the boundary) matters.
- Analysis of how MIRA Score varies across layers (not just the penultimate), which could provide practical guidance for monitoring system design.

## Novel Insights

The paper's central insight — that neural network models with identical accuracy can differ fundamentally in the detectability of their failures, and that this is an intrinsic, measurable property of learned representations — is genuinely novel and practically important. The observation that this property can be estimated without external OoD data by probing local boundary sensitivity through perturbations is clever. If validated more rigorously, this could provide practitioners with a principled tool for model selection in safety-critical settings, complementing accuracy-based evaluation with a "monitorability-aware" evaluation paradigm.

## Suggestions

- **Add formal correlation statistics.** Compute Spearman's ρ between MIRA Score and best average AUROC for each domain (and across domains). With only 4-5 data points, also report exact p-values and consider adding more architectures to strengthen statistical power.
- **Address the validation circularity more explicitly.** Consider an additional validation strategy: e.g., show that MIRA predicts *calibration error* or *reliability under natural corruptions* (Hendrycks & Dietterich, 2019), which are related but distinct from OoD detection.
- **Add a layer-wise analysis.** Computing MIRA at multiple layers would demonstrate its utility for monitoring system design (as mentioned in the conclusion) and provide additional experimental depth.

## Score and Decision

The paper introduces a genuinely novel and practically relevant concept with a sound methodology. The multi-modal experiments show consistent and promising trends. However, the central correlational claim is not backed by formal statistics, the validation methodology has acknowledged circularity concerns, and the model counts are small. These issues collectively prevent me from recommending strong acceptance, but the novelty and potential impact warrant a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>