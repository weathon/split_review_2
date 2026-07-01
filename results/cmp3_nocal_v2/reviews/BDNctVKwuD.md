## Summary

This paper makes a theoretical observation about HiResCAMs — that they are not uniquely determined because adding a common matrix *M* to all class-level CAMs leaves softmax probabilities unchanged (Theorem 3.2) — and proposes ContrastiveCAMs (pairwise HiResCAM differences) to remove this redundancy. The paper then leverages ContrastiveCAMs to design Core-Focused Cross-Entropy (CFCE), a modified training loss that suppresses contributions from non-core image regions, and demonstrates improved feature alignment on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC.

## Strengths

1. **A genuine theoretical observation about HiResCAM non-uniqueness (Theorem 3.2).** The paper correctly identifies that HiResCAMs are not uniquely determined from probability predictions due to softmax shift-invariance. The observation is clear, formally stated, and novel to the reviewer's knowledge.

2. **An elegant, minimal fix in ContrastiveCAMs (Definitions 3.3, 3.4).** Taking pairwise differences of HiResCAMs removes the *M* shift by construction. The additional granularity of class-versus-class explanations is a genuine byproduct that standard CAM methods do not provide.

3. **A cleverly designed Core-Focused Cross-Entropy loss (Definition 4.5).** Rather than a standard post-hoc regularizer, CFCE rewrites cross-entropy in terms of ContrastiveCAMs and modifies the non-core contribution inside the log-sum-exp structure, turning it into an additive penalty via the absolute value. This is a non-obvious design that goes beyond typical mask-based regularization.

4. **Strong and consistent empirical signal across multiple datasets and settings.** Results are reported on Hard-ImageNet (multiclass), Oxford-IIIT Pets (binary and multiclass), and PASCAL VOC (multilabel + downstream segmentation). Across all settings, CFCE substantially improves alignment metrics (IoU, RFS, accuracy under core-region ablation) and the downstream segmentation transfer result provides independent evidence that the feature alignment generalizes beyond the classification task.

5. **The method works with approximate masks.** Experiments with SAM-generated masks and bounding boxes (Oxford Pets table, lines 288–298) show that CFCE does not require expensive ground-truth segmentation masks, substantially increasing practical applicability.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Accuracy trade-off is acknowledged but not analyzed.** On Hard-ImageNet (Table 2), primary accuracy drops from 94.25% (CE) to 90.53% (CFCE) — a ~4% absolute drop. On Oxford Pets multiclass validation, CFCE+KL drops from 94.41% to 90.08%. The paper mentions this only in the Table 2 caption ("at the cost of some un-ablated performance") without analyzing whether the trade-off is acceptable, whether it can be mitigated by tuning, or whether it is fundamental. This pattern suggests that enforcing core-region attention consistently reduces classification performance on some datasets, which deserves honest discussion.

2. **ContrastiveCAM IoU evaluation is partially circular.** The CFCE loss explicitly trains the model to align its ContrastiveCAMs with core-region masks, and then the paper measures ContrastiveCAM IoU against those same masks (Table 2: 30.27% CE → 89.22% CFCE; 93.39% CFCE+KL). This improvement is expected by construction. However, this concern is partially mitigated by (a) the GradCAM IoU metric, which provides a somewhat independent signal and also improves (16.25% → 51.52% for CFCE+KL), (b) the ablation accuracy metrics (Gray Mask, Gray BBOX, Tile) which are independent of the training objective, and (c) the downstream segmentation transfer results.

3. **Missing ablation: are ContrastiveCAMs actually necessary for CFCE?** The paper claims a tight link between ContrastiveCAMs and CFCE, but the loss could in principle be formulated using differences of standard HiResCAMs (since ContrastiveCAMs *are* HiResCAM differences). The *M*-invariance property does not matter for the loss during training because the loss operates on CAMs from a single model. The paper does not test whether CFCE with standard HiResCAMs (or GradCAMs) would work as well. Proposition 4.1 provides a theoretical justification for ContrastiveCAMs specifically (connecting them to probabilities rather than logits), but an empirical ablation would strengthen the claimed dependency.

4. **No analysis of KL regularization hyperparameters.** Definition 4.7 introduces λ₁, λ₂, λ₃ without any sensitivity analysis (lines 220–224). The KL term substantially changes the loss, and its behavior depends on the scaling constants λ₂ and λ₃ which control the "softness" of the target and prediction distributions. The paper would benefit from an ablation showing how results vary with these choices.

5. **No discussion of limitations.** Section 6 (lines 322–324) is only four sentences and reads as a conclusion rather than a limitations discussion. The paper does not discuss: (a) the accuracy-alignment trade-off, (b) the requirement for mask annotations, (c) the single-layer classifier assumption (line 49), (d) the impact of zeroing the bias vector for the CFCE derivation (line 166), or (e) failure cases.

6. **The CFBCE multilabel adaptation is underspecified.** The PASCAL VOC experiments (lines 306–314) use "CFBCE" but the paper never defines how CFCE is adapted to multilabel settings — it is presumably applied per positive class, but this should be stated explicitly.

7. **The HiResCAM non-uniqueness significance is somewhat overstated relative to the evidence.** The paper claims that the *M*-shift "can, in principle, completely corrupt HiResCAM explanations" (line 18) and that HiResCAMs "fail to guarantee a faithful interpretation" (line 89). These are conditional/mathematical claims, which are technically correct, but the paper does not demonstrate the practical impact — e.g., by showing that realistically similar models yield substantially different HiResCAMs. The γ values in Table 1 provide some evidence that the redundancy exists in practice, but the language still overreaches slightly. This does not affect the CFCE contribution, which relies on the mathematical properties of ContrastiveCAMs rather than a demonstrated failure of HiResCAMs.

8. **Large variance for one baseline.** In the Oxford Pets table, "CE w/ Arch" binary IoU has a validation standard deviation of 16.98% (line 293), suggesting this baseline comparison is less informative.

### Trivial
1. In Table 2, standard deviations are reported for CFCE and CE w/ Arch runs but not for the simpler baselines (Cross-Entropy, CORM, DFR, CORM+DFR). This makes it harder to assess the variability of those comparisons.

## Nice-to-Haves

- An ablation study varying the strength of the non-core penalty to trace the accuracy vs. alignment Pareto frontier would help practitioners calibrate the trade-off.
- A quantitative faithfulness comparison of ContrastiveCAM vs. HiResCAM (e.g., deletion/insertion, pointing game) would strengthen the claim that ContrastiveCAMs are "more faithful," though this is secondary to the paper's main contribution.

## Removed Points

These points were raised in the input review but are removed with justification below:

- **"Proposition 4.2 is just algebraic manipulation, not a new theoretical insight"** — This is a subjective opinion, not a weakness. The decomposition serves a clear purpose in the paper's argument and is not presented as a major theoretical breakthrough.
- **"Request for broader baselines (LISA, CutMix, etc.)"** — This is scope creep. The paper compares against the most directly related baselines (CORM, DFR). Adding more methods would be nice but is not a flaw in the existing evaluation.
- **"Segmentation transfer figure legend not informative enough"** — This is a formatting artifact from PDF extraction; the original figure contains proper labels.
- **"CAM faithfulness comparison missing"** — The paper's main evaluation is about alignment improvement via CFCE, not about benchmarking ContrastiveCAMs as a standalone explanation method. The faithfulness claim for ContrastiveCAMs is theoretical (Proposition 4.1), not empirical.
- **"Scope limitation of single-layer classifiers not discussed"** — The paper explicitly states this assumption (line 49) and many modern architectures satisfy it. The practical impact of MLP heads is worth noting but the paper is transparent about its scope.
- **"The contrastiveness observation is a restatement of softmax shift invariance"** — The paper correctly credits Proposition 3.1 to standard softmax properties; the novelty is applying it to the specific HiResCAM setting via Theorem 3.2.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a brief analysis of the accuracy-alignment trade-off, including a discussion of whether the ~4% accuracy drop on Hard-ImageNet is inherent or can be mitigated.
2. Run an ablation replacing ContrastiveCAMs with standard HiResCAM differences in the CFCE loss to test whether the claimed dependency holds.
3. Include a limitations paragraph covering the mask requirement, the single-layer classifier assumption, the accuracy trade-off, and the bias-free classifier assumption.
4. Clarify how CFCE is adapted to multilabel settings (CFBCE).
5. Add a brief hyperparameter sensitivity study for λ₁, λ₂, λ₃.

## Score and Decision

This paper makes two genuine contributions: a clean theoretical observation about HiResCAMs and a cleverly designed CFCE loss. The experiments are broad, consistent, and include multiple independent evaluation signals (GradCAM IoU, ablation accuracy, RFS, downstream segmentation). The weaknesses are all Minor: the accuracy trade-off should be discussed more thoroughly, the circularity in the ContrastiveCAM IoU evaluation is partially mitigated by other metrics, and the missing ablation of standard vs. Contrastive CAMs in CFCE is an addressable gap. None of these issues threaten the paper's core claims or empirical evidence. The paper would benefit from an honest limitations paragraph and a few additional ablations, but in its current form it represents solid, publishable work.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>