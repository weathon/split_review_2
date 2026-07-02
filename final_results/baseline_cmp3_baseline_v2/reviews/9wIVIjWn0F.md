## Summary

The paper proposes Regression-based Test-Time Adaptation (RTA) for vision-language models. The key idea is to train a regression model (LightGBM) on pseudo-labeled data to predict the cross-entropy loss of augmented views directly from their logits. During test-time adaptation, views with the smallest predicted loss are selected as confident views and ensembled. The method is evaluated on single-label, multi-label, and cross-domain benchmarks, showing consistent improvements over existing entropy-based TTA methods.

## Strengths

- **Novel perspective on view selection:** The paper identifies a strong empirical relationship between augmented-view logits and label cross-entropy loss, and proposes to directly regress this mapping rather than relying on entropy. This is a clean and intuitive departure from existing TTA approaches.
- **Simple and efficient method:** RTA uses a lightweight decision-tree regressor (LightGBM) trained once offline, then applied at test time without any parameter updates. The computational overhead beyond standard augmentation is negligible.
- **Extensive experimental evaluation:** The method is tested on a wide range of benchmarks (single-label, multi-label, cross-domain) with two CLIP backbones (RN50, ViT-B/16) and compared against many recent TTA methods. The results show consistent gains, especially on out-of-distribution datasets.

## Weaknesses

### Major

- **Unaddressed class-number mismatch between regression training and test sets:** The regression model is trained on logits from ImageVal-12k, which has 1000 classes. The input feature dimension is therefore 1000. However, the method is applied to datasets with different numbers of classes (e.g., Pets: 37, Flowers: 102, Aircraft: 100, etc.). A decision tree trained on 1000-dimensional inputs cannot accept inputs of a different dimensionality. The paper does not explain how this mismatch is handled. If separate regression models were trained per dataset (using that dataset’s own pseudo-labeled data), the claim of “trained once and adapts to any test distribution” is invalid. This is a critical omission that undermines the core contribution.

- **Lack of justification for the regression model choice:** The paper uses LightGBM without any ablation or comparison to other regressors (e.g., MLP, random forest, linear regression). Given that the regression mapping is claimed to be non-linear, the choice of a tree-based model is plausible but not empirically supported. The sensitivity of results to the regression model is unexplored.

### Minor

- **Pseudo-label quality and selection bias:** The regression training data is filtered by CLIP confidence ≥0.8. This may introduce a selection bias toward easy samples, potentially limiting the regression model’s ability to handle hard or ambiguous test views. The paper does not analyze the impact of this threshold or the diversity of the training set.
- **Overstated “free lunch” claim:** While the regression model is cheap to train, it still requires a separate dataset (ImageVal-12k) and pseudo-labeling. This is not entirely “free” and may not be available in all deployment scenarios. The paper acknowledges this but the framing is somewhat misleading.
- **Modest gains on in-distribution data:** On ImageNet-1k, the improvement over the best baseline (Zero) is only 0.24% for ViT-B/16. The more substantial gains are on OOD datasets, which is positive, but the in-distribution advantage is marginal.

### Trivial

- The paper uses “regression mapping” and “regression relationship” interchangeably; the terminology could be tightened.

## Nice-to-Haves

- An ablation study comparing different regression models (e.g., MLP, random forest, linear regression) would strengthen the method’s generality.
- Analysis of how the regression model’s performance degrades when the test set has a very different number of classes from the training set (if a single model is used).
- A discussion of the computational cost of the regression training stage relative to the test-time savings.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- **Clarify the class-number mismatch issue explicitly.** If a single regression model is used across all datasets, explain how inputs of varying dimensionality are handled (e.g., by using only the logits corresponding to the test set’s classes, or by training on a fixed set of class logits). If separate models are trained per dataset, state this clearly and adjust the claims accordingly.
- **Add an ablation on the regression model choice** (e.g., compare LightGBM with a simple MLP or linear regression) to demonstrate that the non-linear tree model is necessary.
- **Report the sensitivity to the confidence threshold** used for pseudo-label selection in the regression training set.

## Score and Decision

**Score:** 4.0  
**Decision:** Reject

The paper presents a novel and intuitive idea with strong experimental breadth. However, the critical omission regarding how the regression model handles datasets with different numbers of classes (a necessary condition for the claimed “train once, adapt anywhere” property) makes the core claim unverifiable. Until this issue is resolved, the paper cannot be accepted.

MY FINAL SCORE: <score>4.0</score>  
MY FINAL DECISION: <decision>Reject</decision>