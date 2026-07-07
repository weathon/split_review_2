## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA) for CLIP-based image classification. The key insight is a "Ceiling TTA" observation: using ground-truth cross-entropy loss (LCE) to select confident views from augmented views dramatically outperforms standard entropy-based selection (e.g., +35.2% on ImageNet-A). RTA trains a lightweight LightGBM regressor on pseudo-labeled ImageVal-12k data to predict per-view cross-entropy loss from logits, then selects the top-k views with lowest predicted loss at test time. Experiments span single-label ImageNet variants (5 datasets), cross-domain transfer (10 datasets), and multi-label (3 datasets) with RN50 and ViT-B/16 backbones.

## Strengths

- **The "Ceiling TTA" analysis (Section 4.1, Tables 1–2) is genuinely insightful.** The observation that LCE-based view selection outperforms entropy-based selection by enormous margins (e.g., +35.2% on ImageNet-A, +24.6% on ImageNet-V for RN50 with 64 views) is striking and serves as compelling motivation. The near-saturation behavior as view count increases is also informative. This is the paper's most original finding.

- **The method is computationally efficient and creatively motivated.** Training a LightGBM regressor on 1,000 pseudo-labeled samples and using it fixed at test time without per-instance updates is genuinely lightweight. The choice of tree-based regression for the small-data regime is sensible and avoids overfitting.

- **The experimental scope is broad.** The evaluation covers single-label ImageNet variants (5 datasets), cross-domain transfer (10 datasets), and multi-label (3 datasets) with two CLIP backbones (RN50, ViT-B/16). RTA consistently achieves competitive or state-of-the-art results across most settings — e.g., 65.84% OOD average (ViT-B/16) vs 65.03% for the prior best (Zero).

## Weaknesses

### Fatal

None.

### Major

- **The logit dimensionality mismatch between training and test is unresolved.** The regression model is trained on 1000-dimensional logits (ImageNet classes from ImageVal-12k). However, Algorithm 2 computes logits for the test set's *L* classes (e.g., 37 for Pets, 80 for MSCOCO, 20 for VOC2007). The paper never explains how a model trained on fixed 1000-dim inputs can process variable-dimension inputs, nor how this is reconciled with the claim that the mapping is "independent of any downstream classification task" (line 330). Without this clarification, the mechanism producing the cross-domain results (Table 4) and multi-label results (Tables 5–6) is unclear. The paper must specify: (a) whether the regression model always receives 1000-dim logits computed against ImageNet class prompts regardless of the target dataset, (b) whether it is retrained per task, or (c) whether some other adaptation is used. This is the most important issue to address.

- **The paper claims RTA "only needs to be trained once" and "can directly adapt to test instances with arbitrary distributions" (line 24), but the evidence for "arbitrary distributions" is limited.** While 10 cross-domain datasets are tested, they are all standard natural-image benchmarks (e.g., Pets, Flowers, Aircraft, EuroSAT). A genuine test of distribution-agnostic claims would include domains with fundamentally different visual structure (e.g., medical, satellite, or sketch imagery). Combined with the unresolved class-count issue above, this claim is overstated relative to the evidence.

### Minor

- **The paper does not describe how the single-label regression framework (softmax CE, Eq. 4) is adapted for multi-label classification**, which uses per-class binary CE with sigmoid rather than softmax over classes. This omission makes it impossible to verify that the multi-label results (Tables 5–6) are produced by the same described method. Clarification is needed on how the regression model is applied in the multi-label setting.

- **A critical baseline is missing: view selection by max softmax confidence** (i.e., selecting views with the highest CLIP softmax probability, equivalently lowest -log(max probability)). Since the regression model is trained on pseudo-labeled samples where the pseudo-label is the max-confidence class (threshold ≥ 0.8), its training target is essentially -log(max softmax probability). A direct comparison against this simple baseline is needed to establish that the regression model learns something beyond what is already available in CLIP's output probabilities.

- **No statistical significance measures** (error bars, confidence intervals) are reported. For small-margin wins (e.g., RTA 66.90 vs Zero 66.24 on ViT-B/16 OOD average), it is unclear whether the improvements are meaningful or within run-to-run noise.

- **The pseudo-labeling pipeline (confidence threshold ≥ 0.8, filtering to 1,000 out of 5,000 samples) introduces selection bias whose impact is not analyzed.** The paper does not report pseudo-label accuracy on the training set nor how regressor prediction errors correlate with incorrect pseudo-labels.

### Trivial

None.

## Nice-to-Haves

- Report regression quality (R² or MSE on held-out labeled data from ImageNet validation) to demonstrate how well the decision tree actually predicts LCE.
- Analyze sensitivity to the confidence threshold (0.8) used for pseudo-label filtering.
- Compare RTA against Kim et al. (2020) on a common benchmark to clarify the advantage of the unsupervised regression approach over the supervised loss predictor.
- Test on at least one domain outside natural images (e.g., medical) to substantiate the "arbitrary distributions" claim.

## Removed Points

These points were flagged in the harsh review but are removed with justification:
- **"Free lunch framing is overstated"** → generic scope creep; does not harm core claims.
- **"Duplicate TDA row in Table 4"** → parser artifact; instruction says not to penalize formatting/parser issues.
- **"Spearman analysis examines only top 10 features"** → acknowledged in the paper; the regression model uses the full logit vector.
- **"No comparison with Kim et al. (2020) on same benchmarks"** → the paper discusses the difference (supervised vs. unsupervised); moved to nice-to-have.
- **"Should discuss standard TTA methods with confidence-based selection"** → not required for a paper introducing its own method.
- **"Ablation of confidence threshold"** → merged into existing pseudo-label point above.
- **"Narrow y-axis ranges in Figures 4–5"** → presentation observation that does not affect results.

## Novel Insights

None beyond the paper's own contributions. The "Ceiling TTA" finding (that LCE-based selection drastically outperforms entropy-based selection) is the most novel observation, and the application of a lightweight regression model to predict view quality is a creative adaptation of the loss prediction idea (Kim et al., 2020) to the CLIP TTA setting. The reviews do not surface additional insights beyond what the paper already claims.

## Suggestions

1. **Clarify the logit dimensionality handling** — this is the most critical issue. Explicitly describe how logit vectors of different dimensionalities are processed by the regression model trained on 1000-dim inputs.
2. **Describe the multi-label adaptation explicitly** — state whether the same regression model is used, whether logits are computed against target-class prompts or ImageNet prompts, and whether the loss function changes.
3. **Add the max softmax confidence baseline** — this directly tests whether the regression model adds value beyond a simple function already present in the logits.
4. **Report statistical significance** — provide standard deviations over multiple runs (at least 3) for the main tables.
5. **Analyze pseudo-label accuracy** on the training set and report R² or MSE of the regression model on held-out labeled data.

## Score and Decision

**Calibration Anchors:**
| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| RLCF (kIP0duasBb) | 6.67 | 1 | Yes | CLIP reward-based TTA; had major novelty concerns (-7.05) but accepted. RTA has stronger novelty (Ceiling TTA) but clarity issues. |
| ML-TTA (75PhjtbBdr) | 6.25 | 1 | Yes | Multi-label TTA with theoretical grounding. RTA has broader evaluation but less rigorous theoretical analysis. |
| DOTA (yD2JMeKumt) | 6.00 | 1 | Yes | Distributional TTA for VLMs; rejected despite 6.0 scores due to accumulated clarity concerns. RTA is comparable but has a stronger central finding. |
| BAT-CLIP (z7PhIgVmZU) | 5.50 | 2 | Yes | Bimodal TTA with fatal experimental flaws (used ground-truth labels at test time). RTA has no such fatal issues. |
| Noisy TTA (iylpeTI0Ql) | 6.00 | 2 | No | Noisy TTA for VLMs; accepted at 6.0. RTA has comparable evaluation breadth and a more novel finding. |
| Few-shot TTA (TD3SGJfBC7) | 6.25 | 2 | No | Few-shot TTA for CLIP; accepted. RTA does not require few-shot supervision. |

**Round 1 bracket:** [5.5, 6.5] — based on weighted-item comparison. The paper's strongest positive item (Ceiling TTA, +5.80) exceeds any single strength in DOTA (max +4.44) and is comparable to ML-TTA's strongest items. Its most negative item (dimensionality, -3.15) is less severe than the fatal issues in BAT-CLIP (-9.14, -7.82) or the novelty concern in RLCF (-7.05). The paper's overall profile — novel observation, broad evaluation, but clarifications needed — aligns most closely with the DOTA/Noisy TTA/ML-TTA cluster (6.0–6.25), though the missing clarification about logit dimensionality is a genuine gap that prevents full assessment of the cross-domain and multi-label results.

**Final score: 6.0** — The paper makes a genuinely interesting contribution (Ceiling TTA finding) and shows consistent improvements across a broad set of benchmarks. However, the unresolved logit dimensionality mismatch and missing description of multi-label adaptation prevent the method from being fully evaluated as described. These issues are fixable in revision but, in their current form, weaken the paper's claims.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>