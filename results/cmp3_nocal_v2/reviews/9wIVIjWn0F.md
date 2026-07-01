Now I have all the information needed to write the final consolidated review. Let me compose it.

## Summary
The paper proposes Regression-based Test-Time Adaptation (RTA) for CLIP. The key idea is to train a lightweight regression model (LightGBM decision tree) that maps augmented view logits to their corresponding pseudo-cross-entropy loss, then use this model at test time to select confident views for ensembling — replacing the entropy-based selection used in prior TTA methods. The method is trained once on ImageVal-12k data and applied without per-instance updates.

## Strengths

1. **The ceiling TTA finding (Tables 1, 2) is striking and well-motivates the approach.** Using ground-truth cross-entropy loss for view selection on ImageNet-A with ViT-B/16 and 64 views gives 90.2% vs 64.3% for entropy — a 25.9 point gap. This clean empirical observation is the paper's strongest intellectual contribution.

2. **The method is computationally lightweight.** A decision tree with max_depth=5 and 16 leaves is trivially cheap at test time, and training requires only a forward pass through CLIP on 1,000 samples. This contrasts favorably with methods requiring per-instance prompt tuning or diffusion sampling.

3. **The experimental scope is broad.** Evaluation spans 5 ImageNet variants + 10 cross-domain datasets + 3 multi-label datasets, for two backbones (RN50, ViT-B/16). The results are competitive, often matching or exceeding prior methods on average accuracy.

## Weaknesses

### Fatal
None.

### Major

1. **The regression tree's training and test input dimensionalities are inconsistent, and the paper never explains how this is resolved.** The regression tree (Algorithm 1) is trained on ImageVal-12k logits — a 1000-dimensional input space (one logit per ImageNet class). During test-time evaluation on cross-domain datasets (Table 4), the per-view logits would have a different number of dimensions corresponding to the target dataset's class count (e.g., 37 for Pets, 20 for VOC2007 in multi-label). The same issue applies to multi-label evaluations (Tables 5, 6). The paper contains no explanation of how the tree, having learned splits on a 1000-dimensional space, processes vectors of varying dimensionality. This is not a minor implementation detail — it is a prerequisite for the method to function on these benchmarks. As described, the cross-domain and multi-label results in Tables 4-6 are not reproducible from the stated method. *(The ImageNet / ImageNet-variant results in Table 3 are unaffected because they share the 1000-class label space.)*

2. **A critical ablation — comparing the regression-based selector against entropy selection within the same pipeline — is missing.** The paper compares RTA against prior methods (Zero, TDA, BCA, etc.), but each uses different augmentation strategies, filtering mechanisms, and adaptation protocols. To isolate whether the regression model itself provides a meaningful advantage over entropy, the paper should compare: (a) RTA's full pipeline, (b) the same pipeline with views selected by lowest entropy, and (c) the same pipeline with views selected by directly computed pseudo-LCE (without a regression model). Without this ablation, the reported gains cannot be attributed to the regression mapping rather than to other aspects of the pipeline (augmentation set, ensembling strategy, filtering ratio).

3. **The paper conflates the ceiling finding (true-label LCE) with what the method actually implements (pseudo-LCE), and the gap between them is never analyzed.** The ceiling motivation (Section 4.1, Tables 1-2) uses ground-truth labels to select views, achieving dramatic gains (e.g., 90.2% on IN-A). RTA instead trains on pseudo-LCE derived from CLIP's own high-confidence predictions (threshold ≥ 0.8 on argmax probability). For such high-confidence predictions, pseudo-LCE = −log(p_argmax) is a monotonic function of the model's confidence — fundamentally similar to what entropy measures for a peaked distribution. The gap between ceiling (90.2%) and actual RTA performance (65.65% on IN-A, ViT-B/16) is ~25 points, yet the paper never discusses whether the pseudo-LCE proxy captures the same view-selection signal as true LCE, or whether it is meaningfully different from entropy for this purpose.

### Minor

4. **The t-SNE motivation (Figure 2) uses true LCE as the coloring variable, but the actual regression model is trained on pseudo-LCE.** The visualization showing structural correlation between logits and *true* label loss does not directly support the claim that the same structure exists with *pseudo*-label loss. This weakens the connection between the motivation and the method.

5. **Several implementation details are under-specified.** (a) "sampling by logit-based equal-interval" from the 5,000 confident samples to obtain the 1,000 training samples is not explained. (b) For multi-label classification, it is unclear how pseudo-labels are determined — a single argmax ignores the multi-label nature, but the paper never describes a multi-label-compatible procedure. (c) The paper states that RTA "follows the settings of Zero and ML-TTA" for the TTA process, but does not specify whether the class prompts used at test time are from the target dataset or always from ImageNet's 1000 classes, which relates directly to weakness #1.

6. **No analysis of the regression model's internal behavior.** The paper never reports the regression model's prediction error (MSE on held-out data), the correlation between predicted loss and actual view accuracy, or which logit dimensions the decision tree actually splits on. With max_depth=5 and 16 leaves, the tree can use at most 5-16 of the 1000 input features — reporting which features are selected would provide insight into what the model learns.

7. **Results are reported as point estimates without variance.** Given randomness in augmentations and sampling, some measure of variance (e.g., error bars across multiple runs) would strengthen the claims, particularly for the smaller cross-domain datasets.

### Trivial
None that survive filtering.

## Nice-to-Haves
- Analyze the relationship between pseudo-LCE and true LCE on a labeled validation set (e.g., how often does selecting by lowest pseudo-LCE agree with selecting by lowest true LCE?).
- Compare with a variant that uses CLIP image features (rather than class logits) as regression input — this would naturally handle variable class counts.
- Report the regression tree's feature importance to show which logits drive the splits.

## Removed Points
The following points from the input review are removed after verification against the paper:

- **"Regression tree input dimensionality mismatch is a structural/fatal flaw"** → Kept but downgraded from "structural/unverifiable" to Major. The ImageNet results (Table 3) are unaffected, and there are plausible resolutions the authors could clarify (e.g., always using 1000 ImageNet prompts for regression input). The cross-domain/multi-label results remain unverifiable as described.
- **"The paper does not discuss that RTA solves an easier problem (no parameter updates)"** → Removed. The paper is transparent about being a view-selection method; comparing against methods that also do prompt tuning is standard practice and fairly exposes RTA's relative strengths.
- **"The tree with 16 leaves can only use a fraction of 1000 features"** → Downgraded to Minor #6 (merged). This is a characteristic of decision trees, not a flaw, but reporting which features are used would strengthen the paper.
- **"Regression data shares distribution with ImageNet test data, weakening the claimed advantage"** → Removed. The paper's claim is about adapting to *arbitrary* downstream tasks, and the regression data is from ImageNet, which is a different distribution from e.g., IN-A, IN-R, Pets, etc. The cross-domain experiments genuinely test generalization.
- **"No comparison with Kim et al. (2020)"** → Removed. The paper cites and discusses this work in the related work section. An experimental comparison would be nice but is not required — Kim et al. operates in a supervised setting.
- **"Algorithm formatting is poor (parser issue)"** → Removed per formatting-artifact rule.
- **"Framing of entropy methods is misleading"** → Removed as a framing nitpick that doesn't affect the paper's technical validity.

## Novel Insights
None beyond the paper's own contributions. The reviewer's observations about the pseudo-LCE / true-LCE gap and the need for controlled ablations frame the paper's weaknesses clearly but do not introduce independent technical insight.

## Suggestions
1. Clarify how the regression tree handles test inputs with different numbers of classes. If you always compute 1000 ImageNet logits (using ImageNet prompts) as regression features regardless of the target dataset, state this explicitly in the method section and algorithm pseudocode.
2. Add the critical ablation: compare RTA against the same pipeline using entropy-based view selection and directly-computed pseudo-LCE view selection.
3. Analyze the relationship between pseudo-LCE and true LCE on a labeled set, and discuss why the large gap between ceiling and actual results does not invalidate the approach.
4. Report regression model MSE on held-out data and the most important features/feature splits learned by the tree.
5. Clarify how pseudo-labels are obtained for multi-label datasets.

## Score and Decision

**Score**: 4.5  
**Decision**: Reject

**Rationale**: The core idea — learning a regression mapping from logits to loss for view selection — is interesting and the ceiling finding is genuinely compelling. However, the paper has a significant gap in its experimental exposition: the dimensionality mismatch between the regression tree's training input (1000-class ImageNet logits) and its test-time input for cross-domain and multi-label datasets is never addressed, making a substantial portion of the reported results unverifiable as described. Combined with the missing controlled ablation and the unanalyzed gap between the ceiling and actual performance, the paper in its current form does not sufficiently support its claims. The method and motivation are strong enough that these issues could potentially be resolved with clarification and additional experiments, but as presented the paper is not ready for acceptance.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>