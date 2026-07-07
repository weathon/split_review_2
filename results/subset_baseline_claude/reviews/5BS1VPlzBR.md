## Summary

The paper proposes **Supervised Mask Modulation (SMM)**, an architecture-agnostic training strategy for image segmentation that dynamically modifies ground truth masks during training to address the FNR > FPR imbalance prevalent in medical and specialized segmentation tasks. The core module, **Miss-Aware Mask Modulation (MAMM)**, identifies false negative regions in each epoch, dilates them, and unions the result with the original ground truth to produce a modulated mask that encourages the model to predict additional positives. Two training variants are introduced: SMMv1 (hard), which applies this modulation every epoch with a dedicated Elevated Sensitivity Loss (ESL), and SMMv2 (soft), which triggers mask updates only when the trend in recall stagnates. The method is evaluated on four diverse datasets using U-Net as the backbone, benchmarked against standard loss-based baselines.

---

## Strengths

- **Simple, well-motivated idea**: The observation that FNR systematically exceeds FPR in many segmentation tasks is grounded in multiple literature references and confirmed empirically in Table 1. The MAMM strategy follows naturally from this observation: expand the supervision signal around missed regions to focus learning there.
- **Architecture-agnostic and training-stage compatible**: SMM requires no changes to the model itself, only to how the training target is constructed. This makes integration into existing pipelines straightforward, and the paper explicitly validates this on a second architecture (SegNet) in the appendix.
- **Solid evaluation protocol**: Experiments use five random seeds with mean ± std reporting across four structurally diverse datasets (medical retinal, histopathology, crack detection, aerial drone). This provides reliable variance estimates and partially addresses reproducibility concerns.
- **Complementary metrics**: The paper reports DSC, JSI, cDice, FNR, and FPR, giving a multi-dimensional view of segmentation quality and appropriately tracking the FNR–FPR trade-off the method targets.

---

## Weaknesses

### Fatal
None.

### Major

1. **Inconsistent and marginal improvements across variants and datasets.** The two SMM variants do not consistently outperform each other or the best baseline across datasets. SMMv2 performs *below Vanilla U-Net* on DRIVE (78.93% DSC vs. 79.63%, 82.71% cDice vs. 83.48%) and Cracks (62.93% DSC vs. 64.57%). SMMv1 underperforms SMMv2 on BoMBR and Drone but outperforms it on DRIVE and Cracks. This creates a situation where the practitioner must choose the right variant per dataset, undermining the claim of a "unified framework." No guidance is provided for this selection.

2. **Gains are often within noise.** On BoMBR, SMMv2's DSC is 67.46 ± 1.24 vs. BL's 67.09 ± 1.06 — an improvement of 0.37 with overlapping standard deviations. Similarly on Cracks, SMMv1 improves by 0.17 DSC over Vanilla. Statistical significance analysis is deferred to an appendix that is unavailable to reviewers; the main paper provides no quantitative significance claim. Given overlapping standard deviations across many cells, it is unclear how many improvements are statistically meaningful.

3. **Dilation kernel design is unjustified and unablated.** The diamond-shaped dilation kernel of radius 2 is a key hyperparameter determining how aggressively label noise is introduced. Expanding FN regions inevitably incorporates background pixels into the positive mask (deliberate false positives), yet no ablation is presented in the main paper varying this radius or kernel shape. This is critical because the entire method rests on the hypothesis that this controlled introduction of label noise is beneficial rather than harmful.

4. **Thin theoretical grounding for the ESL.** The ESL in Eq. (1) resembles a precision-like term with N in the denominator: −(TP)/(N + FN). The normalization by N (total pixels) rather than a natural term like TP + FP is non-standard and the justification is deferred entirely to an unavailable appendix. The functional relationship between ESL and recall maximization is not derived or explained in the main text.

### Minor

- **Only U-Net tested in the main paper.** The claim of architecture-agnosticism is supported primarily by a single backbone. The SegNet evidence is in an appendix not available to reviewers. Including even a brief result from a second architecture in the main body would materially strengthen this claim.
- **No ablation of warm-up duration, queue length L, or γ decay schedule** in the main paper. These are non-trivial hyperparameters that likely influence both SMM variants' behavior, yet their sensitivity is unexplored in accessible content.
- **The formula for β (Eq. 2) uses non-standard axis labeling.** The paper defines x as recall values and y as epoch indices, which is the opposite of the usual convention (independent variable x = epoch, dependent variable y = recall). While mathematically consistent internally, it is confusing and prone to misinterpretation.

### Trivial
None that would affect the decision.

---

## Nice-to-Haves

- An ablation comparing fixed dilation radii vs. adaptive dilation would clarify the contribution of the expansion step.
- A direct comparison with Tversky loss tuned more carefully (α sweep beyond α=0.3) would address whether SMM provides gains beyond what a well-tuned Tversky loss offers.
- A computational cost comparison (extra training time per epoch from mask recomputation) would help practitioners assess the practical overhead.

---

## Novel Insights

The core idea of using epoch-by-epoch predicted FN regions to adaptively expand supervision targets is a practically motivated and relatively underexplored approach to training-time label perturbation. While soft labeling and label smoothing are established techniques, using the model's own current errors as a guide to expand the ground truth boundary—rather than applying fixed dilation or uncertainty-based soft labels—is a meaningful methodological distinction. The recall-trend-based trigger in SMMv2 for deciding *when* to update the mask (rather than doing so every epoch) is an additional practical refinement inspired by adaptive thresholding from semi-supervised learning, applied here to the supervised setting.

---

## Suggestions

- Move at minimum one ablation (dilation radius sweep) into the main paper to give reviewers evidence for the key design choice.
- Provide a rule-of-thumb or lightweight criterion (e.g., dataset FNR/FPR ratio threshold) for choosing SMMv1 vs. SMMv2, or unify them.
- Derive or sketch the connection between ESL and recall optimization analytically, even briefly, rather than deferring entirely to the appendix.
- Report whether gains are statistically significant (e.g., Wilcoxon signed-rank test p-values) in the main table or a companion table.

---

## Score and Decision

The paper addresses a real and well-motivated problem with a clean, architecture-agnostic mechanism. The method is straightforward to implement and the evaluation covers multiple datasets. However, the improvements are marginal and inconsistent across the two proposed variants and four datasets, key design choices (dilation radius, ESL normalization) are unjustified in accessible content, and the claim of a "unified framework" is weakened by the need to choose between variants. The contribution is incremental relative to established FN-focused loss strategies.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>