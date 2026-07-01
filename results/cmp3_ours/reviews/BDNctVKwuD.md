Now I have enough calibration context. Let me write the final review.

**Calibration Bracket:** After the first round, I narrowed the plausible range to 4–6. Round 2 narrowed it to 5–6 based on comparison with anchors like "How to Probe" (avg 6.25, accepted with a clean evaluation framework) and "Explaining Time Series via Contrastive and Locally Sparse Perturbations" (avg 5.75, accepted despite evaluation scope limitations). The paper under review has a stronger theoretical contribution than either anchor, but the circular validation concern is a structural evaluation weakness that those papers did not share.

**Anchor papers used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/57NfyYxh5f.md` (avg 6.25, Round 1+2) — "How to Probe": cleaner evaluation, weaker theory; accepted.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/hr4HTShC6l.md` (avg 3.00, Round 1) — "Detecting Shortcuts using MI": fundamentally flawed method; rejected.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GjfIZan5jN.md` (avg 7.33, Round 1) — "Enhancing Pre-trained Representation...": more extensive experiments across architectures; accepted.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/qDdSRaOiyb.md` (avg 5.75, Round 2) — "Explaining Time Series via Contrastive...": similar scope, accepted despite limited architecture coverage.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6u6GjS0vKZ.md` (avg 4.25, Round 1) — "Coloring Deep CNN Layers...": modest empirical contribution; rejected.

---

## Summary

This paper makes a theoretical observation that HiResCAM explanations are not uniquely determined (they admit an additive matrix M shared across classes due to softmax shift-invariance), proposes ContrastiveCAM (pairwise HiResCAM differences) to remove this redundancy, and then leverages ContrastiveCAM to reveal that models rely substantially on non-core image regions. Building on this, the authors introduce Core-Focused Cross-Entropy (CFCE), a loss that uses ContrastiveCAMs and per-image core-region masks to suppress non-core contributions during training. Experiments on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC show improved alignment metrics, with some accuracy trade-offs.

## Strengths

1. **Clean theoretical observation about HiResCAM (Theorem 3.2).** The paper correctly identifies and proves that HiResCAMs are not uniquely determined — because softmax is invariant to constant shifts, infinitely many HiResCAMs can correspond to the same probability prediction. This is a genuine limitation that is not widely discussed. The proof is a straightforward consequence of Eq. (3) + softmax shift-invariance, but stating it explicitly and formally is useful for the community.

2. **ContrastiveCAM as a principled fix (Definitions 3.3, 3.4, Theorem 3.5).** Taking pairwise differences of HiResCAMs cleanly removes the M redundancy. The M-invariance proof is immediate from the definition. The connection to softmax probabilities (Proposition 4.1) ties the explanation back to what the model actually outputs — this is conceptually stronger than logit-based explanations.

3. **Proposition 4.2 — cross-entropy expressed as a function of ContrastiveCAMs and core/non-core masks.** This decomposition is the paper's most interesting analytical result. It formally shows that cross-entropy does not distinguish between core and non-core contributions, providing a clear lens for understanding why models may learn non-core shortcuts.

4. **Qualitative results (Figure 3) are genuinely compelling.** The per-example comparison on Hard-ImageNet (Balance Beam: core contribution ratio 0.4078→0.9849; Howler Monkey: 0.0265→0.9652) shows dramatic differences that are visually corroborated by heatmaps.

## Weaknesses

### Major

1. **Circular validation: ContrastiveCAM IoU is the headline alignment metric, but it operates in the same space as the CFCE training objective.** 
   The CFCE loss (Eq. 15) directly penalizes non-core ContrastiveCAM contributions and rewards core contributions. ContrastiveCAM IoU then measures overlap between ContrastiveCAMs and core masks — it is essentially measuring what the loss optimized for. For Hard-ImageNet (Table 2), ContrastiveCAM IoU is reported as 89.22% (CFCE) and 93.39% (CFCE+KL), but it is explicitly not computed for baselines ("—" entries). The paper explains this by stating it uses GradCAMs for cross-method consistency. 
   
   The independent metrics tell a more mixed story. GradCAM IoU: CFCE achieves 18.88 (barely above CE's 18.44), and only CFCE+KL shows substantial improvement (51.52). Ablation metrics do show genuine improvement (Gray Mask: 75.94%→41.78% for CFCE) but at a 3.7-point accuracy drop (94.25%→90.53% for CFCE). The paper would be significantly stronger if alignment improvements were demonstrated primarily through metrics independent of the explanation space used in training.

2. **Per-image core-region masks H are a significant practical limitation.** 
   The method requires binary masks for every training image (Section 4.1). While the paper experiments with approximate SAM masks and bounding boxes on Oxford-IIIT Pets (Table 3), results degrade: CFCE+KL with SAM achieves 83.54% valid IoU vs. 92.72% with ground-truth masks — a ~10-point drop. Additionally, KL regularization "must not be applied when bounding boxes are used" (Section 5.2), limiting its applicability. This dependency constrains practical utility to settings where high-quality masks are available, and the paper does not quantify how mask quality affects downstream performance.

3. **Accuracy-alignment trade-off is under-discussed.**
   On Hard-ImageNet (Table 2), CFCE drops unablated accuracy by 3.7 points (94.25%→90.53%). On Oxford-IIIT Pets multiclass, CFCE+KL drops accuracy from 94.41%→90.08%. The Discussion (Section 6) does not engage with this trade-off, nor does it mention the computational overhead of computing ContrastiveCAMs during training. The paper acknowledges the accuracy loss implicitly by reporting it in tables but never analyzes when the trade-off is justified.

### Minor

4. **Overstated practical consequence of HiResCAM non-uniqueness.**
   The paper states that "HiResCAMs for a given input are not uniquely determined" (abstract) and that the shift M can "completely corrupt HiResCAM explanations" (Section 1). However, for a *fixed trained model* with fixed weights, the HiResCAM for a given input *is* uniquely determined — the gradients and feature maps are deterministic functions of the input. The non-uniqueness means that *different* logit configurations yielding the same softmax probabilities can produce different HiResCAMs. This is a genuine theoretical concern about interpretability across models, not a flaw that makes a single model's explanations unreliable. The paper's framing slightly overstates the practical severity of the issue for end-users of a fixed model.

5. **The "theoretical basis for feature misalignment" (Section 4.1) is a static decomposition, not a dynamical claim.**
   Proposition 4.2 shows that cross-entropy does not *explicitly* penalize non-core contributions. The paper concludes this "presents a theoretical basis for feature misalignment." However, this is a static observation about the loss function's form — it shows that CE is *agnostic* to where contributions come from, not that it *actively encourages* non-core learning. The empirical observation (Table 1) that non-core contributions are large is real, but attributing this primarily to CE's form (rather than to dataset statistics, optimization dynamics, or model capacity) is not theoretically established.

### Trivial

6. **No hyperparameter sensitivity analysis.** The CFCE+KL loss (Eq. 18) introduces λ₁, λ₂, λ₃ with no ablation, sensitivity analysis, or stated default values. This makes it difficult to assess the method's robustness.

7. **No computational cost discussion.** Computing ContrastiveCAMs during training requires additional gradient computations through the feature extractor. The overhead is not quantified, making it hard to assess practical deployability.

## Nice-to-Haves

- Compare against a simpler baseline: training with feature maps masked by H during training (suppresses non-core activations before they reach the classifier). The paper mentions region masking as prior work (Kc et al., 2021) but does not include it as a baseline. This comparison is essential to justify the added complexity of the CAM-based loss.
- Analyze why CFCE+KL sometimes underperforms unregularized CFCE on ablation metrics (e.g., Hard-ImageNet Gray Mask: 41.78% for CFCE vs. 45.49% for CFCE+KL).
- Investigate why the redundancy ratio γ varies across datasets (0.201 for Hard-ImageNet vs. 0.367 for Oxford Pets) — this could affect generalizability.

## Removed Points

- **Criticism about missing appendix content (CE w/Arch modifications, Appendix C).** The appendix is stripped by the PDF parser; this is not an author error.
- **Critique that the abstract doesn't cite usage statistics for HiResCAM "popularity."** Minor nitpick with no substantive weight; the paper lists several application domains.
- **"The paper overstates the connection between the theoretical HiResCAM limitation and the feature-misalignment problem."** Too vague to verify as a specific error; the connection is reasonable even if the framing is slightly overblown (addressed in Weakness #4).
- **Criticism that baseline comparisons are unfair because they favor the author's method.** The asymmetry (ContrastiveCAM IoU only reported for CFCE models) is the paper's explicit choice; it's a real concern but one addressed in Weakness #1 rather than a separate unfair-comparison point.

## Novel Insights

The reviewer's most valuable insight is the circular-validation diagnosis: the paper trains models to suppress non-core ContrastiveCAM contributions and then evaluates alignment using ContrastiveCAM IoU, creating a tight coupling between treatment and metric. While the paper includes independent metrics, the headline improvement numbers (89.22%, 93.39% ContrastiveCAM IoU) are the ones most likely to be cited, and they overstate the actual improvement. This structural issue means the paper's central empirical claim (that CFCE substantially improves feature alignment) is less convincingly supported than it first appears. The theoretical contribution (HiResCAM limitation + ContrastiveCAM) stands on its own and is well-supported.

## Suggestions

1. Decouple validation: present alignment improvements primarily through metrics *independent* of ContrastiveCAM (GradCAM IoU, ablation accuracy, downstream segmentation performance), and report ContrastiveCAM IoU only as a secondary diagnostic.
2. Include input-masking as a baseline to justify the CAM-based loss's added complexity.
3. Report hyperparameter sensitivity for λ₁, λ₂, λ₃ and analyze the accuracy-IoU Pareto frontier.
4. Discuss the accuracy-alignment trade-off, computational overhead, and practical applicability conditions honestly in the Discussion section.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>