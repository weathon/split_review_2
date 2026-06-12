Now I have sufficient calibration data. Let me write the final review.

## Summary

KOALA proposes an adversarial detector that flags inputs when class predictions from KL divergence and an L0-based similarity disagree. The paper provides a formal proof (Theorem 1) that under normalized embeddings, bounded perturbations, and sufficient inter-class prototype separation, the KL and L0 stability bands are mutually exclusive, guaranteeing detection. Only clean-image fine-tuning is required, making it a lightweight, plug-and-play approach.

## Strengths

- **Formal proof of correctness with perfect empirical validation on compliant samples**: Theorem 1 proves mutual exclusivity of KL and L0 stability bands under assumptions A1-A4. Table 1 validates this directly: all theorem-compliant samples achieve perfect 1.0 accuracy, precision, recall, and F1 across all four settings (ResNet/CIFAR-10 and CLIP/Tiny-ImageNet, both ε=2/255 and ε=4/255). This is a rare contribution in adversarial detection—most prior methods offer only empirical evidence without formal guarantees. The proof sketch (Section 3.2) conveys the core intuition clearly: KL and L0 require fundamentally different types of perturbation energy, making simultaneous fooling impossible under sufficient prototype separation.

- **Systematic ablation validating metric complementarity on ResNet/CIFAR-10**: Table 2 compares seven metric combinations (single, paired, and triple) across three attacks (PGD, CW, AutoAttack) and two perturbation budgets, consistently showing KL+L0 as the best pairing on ResNet/CIFAR-10 (e.g., F1=0.87 at ε=2/255 vs. 0.53–0.74 for alternatives). This well-designed ablation directly validates the paper's central design insight.

- **Lightweight, plug-and-play design**: KOALA replaces only the classifier head with a nearest-prototype module using KL and L0 metrics, and requires only clean-image fine-tuning (Section 3.3). No adversarial training is needed. This is a genuine practical advantage over adversarial training methods (Madry et al., 2017b) that require expensive iterative attacks during training, and over add-on detectors (Metzen et al., 2017) that need adversarial examples for training.

## Weaknesses

### Fatal
None.

### Major

- **Non-standard confusion matrix conflates detection with classification robustness**: The TP definition (line 188) counts an attacked input as a true positive if it is EITHER correctly detected (â=1, ŷ=⊥) OR missed by the detector but still classified correctly (â=0, ŷ=y*). FN only occurs when the attack is missed AND classification is wrong (â=0, ŷ≠y*). This means the reported precision/recall in Table 2 (e.g., "precision 0.94, recall 0.81" for ResNet/CIFAR-10) measure *defense effectiveness* (did the system ultimately produce the right answer?) rather than *detection capability* (did the system flag the attack?). Some "successful detections" may be cases where the detector completely missed the attack but the perturbation happened not to change the nearest-prototype classification. The paper's framing throughout—"KOALA: KL-L0 Adversarial Detector," "adversarial detection rate"—is about detection, but the evaluation does not cleanly measure detection.

- **Tables 3–4 compare incommensurable metrics between baseline and fine-tuned models**: For the baseline ResNet-18 (no KOALA detector), adversarial accuracy is computed over ALL adversarial examples. For fine-tuned KOALA models, adversarial accuracy is explicitly defined as "performance on successfully attacked images that were not detected" (line 236)—a conditional metric on an easier subset. Yet the paper directly compares: "KL+L0 achieves the strongest adversarial performance" at 57.32% vs. baseline 45.5% (Table 3). This comparison is misleading because the KOALA numbers benefit from excluding detected adversarial examples. The anomalous KL-only CLIP result of 60.02% adversarial accuracy under PGD 2/255 (Table 4) exceeding its own clean accuracy of 57.65% is a stark signal of this metric pathology: if adversarial perturbations can "improve" accuracy, the conditional metric is actively distorting the picture.

- **No comparison with any existing adversarial detector**: The Related Work discusses numerous detection methods (Mahalanobis, NIC, feature squeezing, MagNet, CADet, etc.) at length, yet the experiments contain zero external comparisons. Experiment 2 (Table 2) only compares different internal metric combinations for KOALA. Without any external baselines, it is impossible to assess whether KOALA is practically competitive with, better than, or worse than existing approaches. This is a significant gap for a paper that claims practical contribution.

### Minor

- **No adaptive attack evaluation**: The paper only evaluates against standard attacks (PGD, CW, AutoAttack) designed to fool the original classifier, not the KOALA detector. While the theoretical guarantee suggests adaptive attacks should fail when conditions are met, the empirical validation of this is missing, especially for the ~90% of CLIP samples that are non-compliant.

- **KL+L0 is not consistently the best combination**: On CLIP/Tiny-ImageNet, KL+L0+Cosine outperforms on detection metrics (Table 2: F1=0.79 vs 0.74 at ε=2/255), and L0 alone achieves the best adversarial robustness (Table 4: 53.31% vs. 26.50% for KL+L0). The paper acknowledges this (Section 4.3-4.4) and provides thoughtful analysis about CLIP's pre-training creating sparse structure, but it still represents a gap between the theory's universal prediction and empirical reality.

- **Theorem conditions met for only ~10% of CLIP samples**: Table 1 shows 510/5000 (10.2%) CLIP/Tiny-ImageNet samples at ε=2/255 are compliant. The paper explains this via CLIP's compact embedding space, but this means the theoretical guarantee is nearly vacuous for the CLIP setup—a setup the paper itself chose to demonstrate versatility.

- **L∞ attacks vs. L2 theory**: The experiments use ℓ∞ attacks (line 178), while Figure 1 explicitly references ℓ2-bounded perturbations (‖δ‖₂ ≤ ε, line 40). Assumption A2 uses generic ‖δ‖ (line 114). The mismatch between the attack norm and the theoretical norm should be clarified or the theorem should be stated under ℓ∞ bounds.

### Trivial

- **Hyperparameters τ and φ not specified for CLIP**: For ResNet, τ=0.75 and φ=0.5 are explicitly stated (line 173). For CLIP, only loss weights and optimizer settings are given (line 177); τ and φ are omitted, affecting reproducibility.

- **KL divergence direction unexplained**: KL(c‖p) is used (line 79) without justification for why KL(p‖c) was not chosen. The asymmetric nature of KL means this choice affects how coordinates are weighted.

## Nice-to-Haves
- Report pure detection metrics (TP = cases where the detector actually flags the attack, â=1 when a=1) alongside the current defense-efficiency metrics.
- Include at least one standard adversarial detection baseline (e.g., Mahalanobis distance or feature squeezing) to situate KOALA's performance.
- Add an adaptive attack that jointly minimizes KL and L0 distances to the adversarial class prototype, directly testing the incompatibility claim.
- Investigate and explain why KL-only CLIP adversarial accuracy exceeds clean accuracy.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **Missing appendix/proofs**: The paper states the full proof is in Appendix B (line 124). Parser strips appendices; they exist in the original submission. Removed per hard rule.
- **Generic "evaluation could be stronger" sweep**: Removed as category-driven noise without specific anchors beyond the concrete points already listed.

## Novel Insights

The paper's genuinely novel insight is the formal proof that KL divergence and L0-based similarity define mutually exclusive stability bands under bounded perturbations and sufficient prototype separation (Theorem 1). This is distinct from prior empirical detectors—it provides a *mathematical guarantee* that no single perturbation can simultaneously fool both metrics. The perfect 1.0 validation on all compliant samples in Table 1 is strong, direct evidence that the theory works when its conditions are met. However, the insight's practical significance is tempered by the limited coverage of the theorem's conditions (~10% on CLIP) and the evaluation's conflation of detection with classification robustness.

## Suggestions
- Add a row in all tables reporting pure detection metrics (TP = â=1 when a=1) to let readers assess detection power independently of classification accuracy.
- Include at least one standard detection baseline (e.g., Mahalanobis) for direct comparison.
- Add an adaptive attack that jointly perturbs to maintain both KL and L0 agreement, directly testing the incompatibility claim.
- Clarify the ℓ∞ attack / ℓ2 theory relationship.
- Specify τ and φ for the CLIP setup.
- Investigate the KL-only CLIP adversarial accuracy exceeding clean accuracy anomaly.

## Calibration Report

**Anchors retrieved across all rounds:**

| Paper Path | Avg Score | Round | Comparison |
|---|---|---|---|
| 5kMwiMnUip.md (NEMESIS jailbreaking) | 1.40 | R1 | Unrelated topic; low quality. Not comparable. |
| Uj0h13lVrR.md (KL divergence GFlowNets) | 1.00 | R1 | Unrelated. Not comparable. |
| nSDOkm0SKo.md (Financial markets NN) | 1.00 | R1 | Unrelated. Not comparable. |
| 5lUdTogEL3.md (Lifelong Re-ID) | 1.00 | R1 | Unrelated. Not comparable. |
| kz78RIVL7G.md (Statistical attack detection) | 2.60 | R1 | Adversarial detection with statistical method. KOALA has much stronger theory. KOALA clearly stronger. |
| KAWlH5pfQu.md (Detecting Adversarial Examples) | 3.00 | R1 | Adversarial detection with theoretical justification but weak evaluation (no adaptive attacks, no SOTA baselines). KOALA has stronger proof and perfect validation. KOALA clearly stronger. |
| 85X9awoVtv.md (Data withdrawal auditing) | 2.50 | R1 | Different topic. Not directly comparable. |
| lEsNGN1SjG.md (Bias classifier adversarial) | 2.00 | R1 | Adversarial defense with proof but narrow scope. KOALA stronger. |
| r5d8zkYizS.md (Near-zero eigenvalues) | 5.33 | R1 | Strong mathematical framework for adversarial examples with proofs but weak experiments. Comparable theoretical ambition; KOALA has better empirical validation on compliant samples but worse overall evaluation design. Roughly comparable. |
| G3OCarOfxx.md (Clean generalization and robust overfitting) | 4.80 | R1 | Adversarial training theory. KOALA has more novel detection-specific theory. |
| R1crLHQ4kf.md (Output distribution adversarial audio) | 5.00 | R1 | Adversarial detection for ASR. Empirical, no formal guarantees. KOALA stronger in theory. |
| N5ID99rsUq.md (Free adversarial training stability) | 5.25 | R1 | Generalization theory for adversarial training. Different focus. |
| RzdtpxL0H5.md (DDAD) | 6.20 | R1 | Two-pronged defense with MMD theory. Better evaluation (baselines + adaptive attacks), but KOALA's theoretical guarantee (perfect on compliant samples) is stronger. KOALA weaker overall due to evaluation gaps. |
| 8CJDYx8GwF.md (Gradient flow robust classifiers) | 6.25 | R1 | Provable robustness with restrictive assumptions. KOALA has more empirical validation but messier evaluation. |
| inLUnCpDIB.md (Adversarial training feature learning) | 6.00 | R1 | **Accepted.** Clean theory with consistent experiments across datasets. KOALA has comparable theoretical novelty but significantly messier evaluation. KOALA weaker. |
| ExUC9dQJhQ.md (Certified robustness poisoning) | 6.00 | R1 | Certified robustness framework. Different scope but comparable rigor. |
| EWP9BVRRbA.md (NEARSIDE detection) | 4.00 | R1 | Adversarial detection for VLMs. Weak evaluation like KOALA but less theory. KOALA stronger. |
| 4Hf5pbk74h.md (Nearest neighbor decision boundaries) | 2.33 | R1 | Different topic. Not directly comparable. |
| rlsWIBDWhW.md (Cluster-driven adversarial contrastive) | 5.50 | R1 | Adversarial contrastive learning. Different scope. |
| J2we1sVd9m.md (Prototype-based OOD detection) | 4.60 | R1 | OOD detection with prototypes. KOALA has stronger theory. |
| VAmVEghgoC.md (Neural collapse OOD detection) | 4.50 | R1 | OOD detection. Different scope. |
| SuH5SdOXpe.md (Robustness reprogramming) | 7.50 | R1 | Stronger accepted paper. More complete evaluation. KOALA weaker. |
| IGzaH538fz.md (GNNCert) | 8.00 | R1 | Strong accepted paper with formal certification. KOALA much weaker. |
| I5lcjmFmlc.md (Robust diffusion classifier) | 8.00 | R1 | Strong paper. Not comparable in scope. |
| mXpNp8MMr5.md (Two-faced attacks) | 7.33 | R1 | Accepted paper. Stronger overall. |

**Round 1 bracket:** Between 4.5 and 6.0. The paper has a genuinely novel theoretical contribution (formal proof + perfect validation on compliant samples) that separates it from the 3-4 range papers, but its evaluation issues (non-standard metrics, no external baselines, no adaptive attacks, incommensurable comparisons) prevent it from reaching the 6+ range of accepted papers.

**Final calibration reasoning:** Comparing to the "Near-zero eigenvalues" paper (5.33, rejected) which has similar strengths (strong mathematical framework) and weaknesses (insufficient experiments), KOALA has better empirical validation on its compliant subset but worse overall evaluation design. Comparing to "Adversarial Training Can Provably Improve Robustness" (6.0, Accepted) which has clean theory with consistent experiments, KOALA has comparable novelty but messier evaluation. The non-standard TP metric and incommensurable Tables 3-4 comparisons are real problems that prevent a higher score. The paper sits squarely in the 5.0 range: a genuine contribution with significant but addressable evaluation issues.

## Scoring anchors comparison

| Anchor | Score | Decision | Relevance |
|---|---|---|---|
| kz78RIVL7G.md (Statistical attack detection) | 2.60 | Reject | KOALA clearly stronger (formal proof vs. empirical) |
| KAWlH5pfQu.md (Detecting Adv. Examples) | 3.00 | Reject | KOALA clearly stronger (proof + perfect validation) |
| EWP9BVRRbA.md (NEARSIDE) | 4.00 | Reject | KOALA stronger (better theory) |
| J2we1sVd9m.md (Prototype OOD) | 4.60 | Reject | KOALA stronger (novel proof) |
| R1crLHQ4kf.md (Output distribution detection) | 5.00 | Reject | Comparable; KOALA has stronger theory |
| N5ID99rsUq.md (Free adv training stability) | 5.25 | Reject | Different focus but comparable rigor |
| r5d8zkYizS.md (Near-zero eigenvalues) | 5.33 | Reject | Most comparable: strong theory, weak experiments |
| rlsWIBDWhW.md (Cluster adversarial contrastive) | 5.50 | Reject | Different focus |
| inLUnCpDIB.md (Adv training feature learning) | 6.00 | Accept | KOALA weaker evaluation, comparable theory |
| RzdtpxL0H5.md (DDAD) | 6.20 | Reject | KOALA has stronger guarantee but weaker evaluation |
| 8CJDYx8GwF.md (Gradient flow robust) | 6.25 | Reject | KOALA has more validation but messier eval |

**Round 1 bracket: 4.5–6.0. No Round 2 narrowing needed — the anchors within this bracket are clear enough. Final score: 5.0.**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>