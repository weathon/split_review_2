Now I have all the calibration information I need. Let me compile the final review.

## Summary

This paper introduces BadDet+, a backdoor attack framework for object detection that unifies region misclassification (RMA) and object disappearance (ODA) under a single log-barrier penalty mechanism. The paper makes three contributions: (1) a careful diagnosis of evaluation blind spots in prior object-detection backdoor work (Section 3), (2) a new penalty-based formulation that suppresses original-class predictions on trigger-bearing objects, and (3) a comprehensive evaluation across two datasets, four architectures, multiple trigger placements, and a physical-transfer benchmark.

## Strengths

- **Careful diagnosis of evaluation blind spots (Section 3).** The identification of four specific limitations — ASR ignoring retained labels in RMA, mAP as a misleading proxy for ODA, absence of trigger-scaling and placement robustness checks, and reliance on curated datasets — is precise and well-supported. The TDR metric (Section 5.2) is a simple but effective fix for the duplicate-detection problem in RMA evaluation, and the instance-level ASR for ODA is clearly superior to dataset-level mAP. These diagnostic contributions are architecture- and dataset-agnostic and will outlive any specific attack method. *(favorability=9.09)*

- **Principled and clean formulation (Equations 1–2, Section 4.1).** The log-barrier penalty around a threshold τ is a well-motivated design choice. The separate softmax-compatible formulation (Eq. 2) for detectors like Faster R-CNN shows attention to architectural detail. *(favorability=9.85)*

- **Evaluation breadth (Section 5).** Two datasets (COCO + MTSD/PTSD), four architectures (FCOS, Faster R-CNN, DINO, YOLOv5), multiple trigger positions (fixed + random), and a real-world physical transfer benchmark (PTSD) make this the most comprehensive evaluation of object-detection backdoor attacks I am aware of. The defense evaluation with 10 runs per condition (Fig. 2) is a methodological step up from prior work. *(favorability=10.05)*

## Weaknesses

### Fatal
None.

### Major

- **Asymmetric threat model undermines the central comparative claim (Tables 1–4, Abstract).** BadDet+ operates under a strictly stronger threat model (data poisoning + training-time loss manipulation) than every baseline it is compared against (data-poisoning-only). The paper acknowledges this in the threat-model discussion (Section 4: "our design assumes a stronger adversarial setting") and the conclusion, but the abstract states BadDet+ is "outperforming existing RMA and ODA baselines" without this qualification, and Tables 1–4 captions do not mention the asymmetry. A reader scanning the abstract and bolded numbers would reasonably conclude BadDet+ is a better attack under the same conditions. The paper would be stronger if it explicitly framed this as "we show data-poisoning-only attacks are weaker than previously believed, and demonstrate what is achievable when the attacker additionally controls the training loss." *(favorability=3.93)*

- **No variance reporting for the central experimental results (Tables 1–4).** The main attack-evaluation tables report single-point estimates with no indication of variability across random seeds or training runs. This is a significant evidential gap for a paper that criticizes prior work for "inconsistent evaluation protocols" and proposes a "rigorous evaluation protocol." Object-detection training is stochastic; differences of a few percentage points in ASR between methods (e.g., BadDet+ vs. UBA Box on DINO ODA ASR@50: 97.60 vs. 97.43) may fall within run-to-run noise. The defense evaluation (Fig. 2) does report distributions over 10 runs, but the core results substantiating the paper's primary claims do not. *(favorability=2.58)*

### Minor

- **The YOLO failure case is more consequential than the paper treats it (Table 4, line 221–222).** BadDet+ underperforms BadDet on YOLOv5 for RMA on both ASR@50 (91.97 vs. 96.57) and TDR@50 (7.54 vs. 3.14). The paper dismisses this with "indicating that λ = 0 is optimal for this architecture" — i.e., the proposed penalty should not be used for this architecture. This directly contradicts the paper's framing of a "unified" approach that "consistently" works. YOLO is one of the most widely deployed detector families. The paper does not investigate why the method fails on this architecture (single-stage, anchor-based design? training pipeline? loss structure?), which limits the claimed generality. *(favorability=0.04)*

- **The theoretical analysis promised in the abstract is absent from the main text.** The abstract claims "a theoretical analysis showing that the proposed penalty acts selectively within a trigger-specific feature subspace." The main text (Section 4.1) provides an intuitive description and references Appendix A.7. For a paper that self-describes as "principled," the absence of any substantive theoretical development in the main body — even a sketch of the feature-subspace argument — makes the abstract an over-sell relative to what the main paper delivers. *(favorability=0.23)*

- **Poisoning ratios for baseline methods are not reported in the main tables or text.** Line 131 states "we adopt the default poisoning ratios reported in the original works" without specifying what those ratios are. Without this information in the main tables, readers cannot assess whether the comparisons are confounded by different poisoning rates (e.g., if BadDet+ uses 50% while UBA uses 10%, the comparison is harder to interpret even aside from the threat-model asymmetry). The related Figure 3 analysis is helpful but placed later. *(favorability=5.97)*

### Trivial

- **The claim of "position- and scale-invariant behavior" (abstract) is overstated.** The method uses a fixed penalty around threshold τ and a fixed IoU threshold ρ; there is no explicit mechanism for position or scale invariance. The results show that BadDet+ works across different positions and scales, which is generalization, not invariance. The paper's own analysis (Section 3) correctly criticizes prior work for lacking robustness checks on this dimension, but the "invariant" framing claims more than the evidence supports. *(favorability=1.08)*

## Nice-to-Haves

- Include a brief analysis of the computational cost of the IoU-based penalty term compared to standard training, to help practitioners assess practical overhead.
- Consider testing at least one alternative trigger shape or pattern beyond the blue square, especially for the physical-world transfer experiments.
- Move at least a short sketch of the feature-subspace theoretical argument from the appendix into the main text to substantiate the "principled" framing.

## Removed Points

These points are flagged to be removed; treat them with caution if encountered in the input review:

- **Unification claim overstatement (Critic's Critical Issue #5):** The critic argued that RMA still requires poisoned labels while ODA does not, so the unification is only at the penalty level. The paper's claim is about a "single mechanism" (the penalty term), which is accurate — ODA arises as a special case of RMA by treating background as the target class. The unification claim is valid at the mechanism level.
- **Defense evaluation framing (0.4 ASR point):** The critic claimed that ASR@50=0.4 means 60% of attacks fail and the framing is "rosier than the numbers justify." The paper is presenting an attack paper and shows the attack maintains 40%+ ASR after fine-tuning — a meaningful residual threat. The critic misinterprets the paper's framing.
- **Formatting/presentation nitpicks:** Comments about figure readability, axis descriptions, and legend reconstructibility are parser artifacts, not author errors.
- **Missing critical analysis of defenses in Related Work:** The critic requests more detailed analysis of cited defenses. This is scope creep for an attack paper.
- **2-4% clean data justification:** Follows standard FT-based defense evaluation practice in the classification literature. Not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the abstract and conclusion to separate the diagnostic contribution (evaluation blind spots, TDR metric) from the method contribution, and clearly qualify that BadDet+'s comparative advantage over baselines is partially due to operating under a stronger threat model.
2. Add variance estimates (standard deviation over 3+ random seeds) to Tables 1–4.
3. Investigate why BadDet+ fails on YOLO for RMA and discuss the architectural boundary condition in depth, rather than treating it as a simple λ-tuning issue.
4. Move at least a concise sketch of the theoretical analysis (what the "trigger-specific feature subspace" is and how the penalty acts selectively on it) from the appendix into the main text.
5. Replace "position- and scale-invariant" with "generalizes across positions and scales" in the abstract.

## Calibration Anchors

The following anchors were retrieved across two rounds of calibration searches:

| Path | Avg Human Score | Round | Itemized | Comparison |
|------|----------------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5lUdTogEL3.md` | 1.00 | 1 | No | Irrelevant topic (person ReID); score too low to be informative |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7vKWg2Vdrs.md` | 3.25 | 1 | Yes | Backdoor defense for YOLO; our paper is clearly stronger — better diagnostic contributions, broader evaluation, and no fatal novelty issues |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/H6XiAoyugv.md` | 4.33 | 1 | Yes | Backdoor attack with VSSC triggers; had methodological gaps and marginal performance gains. Our paper has better-grounded contributions |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vRyp2dhEQp.md` | 5.75 | 1, 2 | Yes | Backdoor attack in data-constrained scenarios; accepted but had a weakness at -5.60 favorability. Our paper has higher high-end strengths and less severe low-end weaknesses |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tZozeR3VV7.md` | 6.33 | 1, 2 | Yes | Backdooring VLMs with OOD data; accepted. Strengths comparable but our diagnostic contributions are more architecture-agnostic |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1OfAO2mes1.md` | 6.00 | 2 | Yes | Backdoor data identification; accepted. Weaknesses include -3.81 favorability (incremental novelty concern), worse than any of our weaknesses |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LsTIW9VAF7.md` | 5.80 | 1 | No | Clean-image backdoor attack; accepted. Insufficiently similar topic for close comparison |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uqxf2YH9LZ.md` | 5.75 | 2 | No | Backdoor detection for CLIP; defense paper, not directly comparable |

**Bracket reasoning (Round 1):** The topic-relevant anchors in the reject range (3.25–4.33) have weaker contributions and more severe weaknesses than our paper. The accept-range anchors (5.75–6.33) are the closest peers. Our paper's strengths are at or above the best anchors' strengths, while our lowest weakness (0.04) is higher than the worst weaknesses in the 5.75 (Efficient Backdoor, -5.60) and 6.00 (Backdoor Secrets, -3.81) anchors. Initial bracket: **5.5–6.5**.

**Narrowing (Round 2):** The 6.00 anchor (Backdoor Secrets) has an identical highest-strength favorability (~10) but its lowest weakness is -3.81 (novelty/incrementality), which is far more damaging than our lowest (0.04, YOLO failure). The 6.33 anchor (VLOOD) has strengths up to 9.52 and weaknesses down to 1.32 — our strengths are slightly higher but weaknesses slightly lower. Our paper sits between these, closer to the upper end because the diagnostic contributions (favorability 9.09, 10.05) are genuinely novel and the weaknesses, while real, are presentation/scoping issues rather than fundamental technical flaws. Final score: **6.0**.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>