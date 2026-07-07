## Summary

The paper introduces **inverse protocol prediction (IPP)**: given a single bright-field spheroid image, infer the experimental conditions that produced it (cell line, culture medium, seeding density, timepoint, formation method, microscope, magnification). Using the SLiMIA dataset (~8,000 images), the authors benchmark eight segmentation models, five classification architectures (ConvNeXt, ViT, CoAtNet, a shape-fusion transformer, and a hierarchical multi-task transformer), and four spatiotemporal prediction models. They report 95.23% average accuracy across protocol components, supplemented by Grad-CAM interpretability and cross-dataset experiments on RxRx1 and the Cell Tracking Challenge.

---

## Strengths

- **Novel problem framing.** The IPP paradigm—using morphological cues as an inverse signature of culture conditions—is genuinely new and has clear downstream value for reproducibility checks and automated experiment validation in cell biology.
- **Comprehensive benchmarking.** The authors systematically cover convolutional, transformer, hybrid, feature-augmented, and dependency-aware architectures for both segmentation and classification, providing a useful comparative reference for the community working with spheroid data.
- **Transparent interpretability analysis.** The Grad-CAM section is honest: it not only confirms biologically plausible attention (necrotic cores at later timepoints, compactness for seeding density) but explicitly identifies when high accuracy stems from dataset artifacts (microscope signatures, magnification cues), which is scientifically responsible.
- **Protocol-aware temporal conditioning.** The MetadataFusion model outperforms all temporal baselines, validating the utility of experimental metadata as conditioning for spatiotemporal prediction. This finding is conceptually clean and practically useful.

---

## Weaknesses

### Fatal
None.

### Major

1. **Headline accuracy is inflated by artifact-driven labels.** The paper's own Grad-CAM analysis reveals that microscope and magnification labels—two of the nine protocol components—are predicted nearly perfectly because the model attends to instrumental imaging artifacts (illumination patterns, resolution), not biology. Yet these are counted equally in the aggregate 95.23% accuracy. No experiment isolates performance on the biologically meaningful subset (cell line, medium, formation method, seeding density, timepoint), leaving the central claim poorly supported. A per-label breakdown exists in the appendix, but the main-text framing is misleading as presented.

2. **Cross-dataset "validation" on RxRx1 is scientifically incoherent.** RxRx1 contains 2D monolayer cells subject to siRNA perturbation—a fundamentally different biological system, imaging modality, and task than 3D spheroids with culture protocols. Applying SLiMIA-trained IPP models zero-shot to this dataset and reporting 65–76% accuracy does not constitute a meaningful test of cross-domain generalization; there is no shared ground-truth protocol structure between the datasets. The interpretation ("fusion-based models yield stronger robustness under severe cross-dataset shifts") is not justified by this experimental design.

### Minor

1. **HMTT's "causal ordering" is only partially motivated.** The imposed ordering (cell line → medium → seeding density → magnification → microscope → timepoint → replicates) is described as biologically causal, but the directionality from magnification/microscope into biological variables is unclear from the text, and no ablation tests whether the ordering actually improves biological consistency versus random orderings.

2. **Temporal prediction results are poor (SSIM < 0.40 on SLiMIA).** The authors acknowledge this and attribute it to sparse longitudinal data, which is fair. However, the value of this component to the paper is limited; as currently executed, the temporal models are not useful for real applications, and the section reads as exploratory rather than a validated contribution.

### Trivial

- The confidence interval computation assumes the 8,000 images are i.i.d., but images grouped within the same biological replicate/microscope are correlated; the reported intervals may be overly narrow.

---

## Nice-to-Haves

- A main-text table reporting per-label accuracy for the five biologically meaningful protocol components (excluding microscope and magnification) would make the performance claims much more interpretable.
- Ablation of the HMTT causal ordering (e.g., random vs. biologically motivated) would clarify whether hierarchy adds value beyond multi-task learning.

---

## Novel Insights

The Grad-CAM analysis provides a genuinely useful methodological insight: in multi-label protocol prediction tasks, some labels will inevitably be near-trivially predictable from imaging artifacts (microscope signature, resolution), while others require biological reasoning. Conflating these into a single aggregate metric obscures whether a model has learned biology or memorized instrument properties. This observation—that interpretability audits should precede claims of "protocol recovery"—is broadly applicable to the emerging field of experiment-to-image inverse problems in microscopy.

---

## Suggestions

- Decouple the accuracy report into "artifact-driven labels" (microscope, magnification) and "biology-driven labels" (cell line, medium, formation method, seeding density, timepoint) both in the abstract and main results table.
- Replace or significantly reframe the RxRx1 cross-dataset experiment. A more meaningful cross-dataset test would use another spheroid dataset (even if smaller) with overlapping protocol variables.
- Add a simple baseline (e.g., majority-class or nearest-centroid on morphometrics alone) to calibrate whether deep models provide meaningful gains over feature engineering for the harder labels.

---

## Score and Decision

The IPP framing is novel and practically motivated, and the benchmarking is thorough. However, the headline accuracy is substantially inflated by labels that are trivially solved via imaging artifacts—a fact the paper discloses in the interpretability section but does not correct in its primary claims. The RxRx1 cross-dataset experiment does not support its stated purpose. These are major issues that weaken the paper's core empirical contribution. The temporal prediction component is too underdeveloped to compensate. Overall this is a borderline paper that requires significant revision to its claims and experimental validation before the main contributions hold up.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>