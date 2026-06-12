Now I have all the calibration information I need. Let me produce the final review.

## Summary

This paper makes three interconnected contributions to backdoor attacks in object detection: (1) a diagnostic analysis identifying critical evaluation blind spots in prior work (ASR ignoring duplicate detections in RMA, mAP as a confound for ODA, lack of trigger-placement robustness), (2) a more rigorous evaluation protocol including the True Detection Rate (TDR) metric and random trigger placement tests, and (3) BadDet+, a log-barrier penalty-based attack framework that unifies region misclassification (RMA) and object disappearance (ODA) under a single mechanism. Experiments across COCO and MTSD/PTSD with four detector architectures show BadDet+ dramatically reduces TDR@50 (from 44–76% to 1.5–7%) on COCO RMA while maintaining clean mAP, and outperforms prior data-poisoning baselines on both synthetic and physical-world benchmarks.

## Strengths

1. **Diagnosis and empirical validation of duplicate-detection failure in prior RMA evaluations (Section 3, Table 2)**: The paper identifies that ASR alone overstates RMA success because detectors can output both the target class and the original class for the same triggered object. Table 2 concretely validates this: BadDet achieves 99.45% ASR@50 on FCOS but retains TDR@50 of 75.94%; BadDet+ reduces this to 2.78% at comparable ASR@50 (99.28%). This diagnosis translates directly into a measurable improvement.

2. **Single unified log-barrier formulation for RMA and ODA (Section 4.1, Eqs. 1–2)**: The paper provides a unified mathematical framework where ODA emerges as a special case of RMA (background as target class). The log-barrier penalty is a principled soft constraint that sharply penalizes confident original-class predictions on trigger-bearing objects. Two variants handle both sigmoid-based (FCOS/YOLO/DINO) and softmax-based (Faster R-CNN) architectures. Prior work used separate ad-hoc mechanisms; BadDet+ replaces these with a single generalizable loss term.

3. **Systematic evaluation of trigger placement and scale robustness with physical-world validation (Tables 3–4)**: Prior work tested only fixed trigger positions and sizes. BadDet+ evaluates both fixed and random placements across four architectures on MTSD and physically validates on PTSD. BadDet+ maintains 83.68–92.31% ASR@50 under random placements (vs. 7.44–57.44% for Morph and 0.00–32.79% for UBA), and achieves 59.59–85.16% ASR@50 on PTSD (vs. 7.72–54.87% for Morph). This is the most thorough evaluation of trigger-robustness for object-detection backdoors in the reviewed literature.

4. **Introduction of True Detection Rate (TDR) as a complementary evaluation metric (Section 5.2)**: TDR measures the proportion of poisoned objects for which the original class is still detected, directly addressing the duplicate-detection blind spot in RMA. This is a simple but principled improvement that should become standard practice in future object-detection backdoor work.

5. **Empirical demonstration that increasing poisoning ratio cannot fix existing data-only attacks (Figure 3)**: The paper shows that pushing UBA/UBA Box to 100% poisoning yields at best modest ASR gains while severely degrading clean mAP. For RMA, FCOS and Faster R-CNN retain residual duplicate detections even at 100% poisoning. This empirically motivates why the stronger training-time-loss-manipulation threat model is necessary — a nontrivial claim supported with data rather than asserted.

6. **Defense evaluation with statistical rigor (Figure 2, 10 runs per configuration)**: The paper evaluates robustness against FT and FT-SAM with 10 random subsets per configuration, providing distributions rather than point estimates. This level of statistical reporting exceeds what prior object-detection backdoor papers typically provide.

## Weaknesses

### Major

None.

### Minor

1. **"Position- and scale-invariant" overstates the evidence (Abstract, Table 3)**: The abstract claims "position- and scale-invariant behavior," but the paper's own results show consistent ASR@50 drops from Fixed to Random trigger placements across all architectures. On MTSD ODA (Table 3): FCOS drops from 93.77 → 83.68, Faster R-CNN from 94.90 → 89.38, DINO from 97.75 → 92.31, YOLOv5 from 92.95 → 87.08. BadDet+ is clearly *robust* to placement variation — substantially more so than all baselines — but "invariant" implies a stronger property than what is measured. The claim should be softened to "robust to variation in position and scale."

2. **UBA matches/exceeds BadDet+ on DINO ODA (Table 1)**: On COCO DINO ODA, UBA achieves 97.89 ASR@50 vs. BadDet+'s 97.60. The paper describes BadDet+ as "consistently strong across all tested settings" but does not acknowledge that a simpler data-only baseline slightly edges out the proposed method on this architecture. This competitive case deserves discussion, especially since DINO is the strongest of the three COCO architectures.

3. **YOLOv5 RMA where BadDet (data-only) outperforms BadDet+ (Table 4)**: The paper acknowledges that on YOLOv5 RMA, BadDet achieves higher ASR@50 (96.57 vs. 91.97) and lower TDR@50 (3.14 vs. 7.54), and that "λ=0 is optimal for this architecture." This is a significant finding — the proposed penalty mechanism is counterproductive on one of four architectures — but receives only a single sentence. A deeper investigation into why the log-barrier penalty fails on YOLO (e.g., architectural differences in how YOLO handles confidence thresholds or the penalty term) would substantially strengthen the paper.

4. **No variance or uncertainty reporting for main results (Tables 1–4)**: All main tables report single-run performance. Object detector training has meaningful stochasticity. Standard deviations over 3–5 seeds for key comparisons (at minimum the COCO results) would allow readers to assess whether observed differences between methods are meaningful rather than noise.

### Trivial

1. **Poisoning ratio analysis (Figure 3) described only qualitatively**: The text says "lighter points drift towards the bottom-right" without providing specific numerical anchor points (e.g., "at 100% poisoning, UBA achieves ASR@50 = X on FCOS while mAP drops to Y"). Including key numbers would make the argument more precise and independently verifiable from the text.

2. **Threat model difference could be flagged more prominently**: The paper explicitly discusses the different threat model (BadDet+ assumes training-time loss manipulation; baselines use data poisoning only) in Sections 4 and 6. However, the abstract states "outperforming existing RMA and ODA baselines" without noting this asymmetry. A brief qualification in the abstract and table captions would prevent misinterpretation by casual readers.

## Nice-to-Haves

- A "BadDet+_dataonly" ablation (implementing the same penalty insight purely through data manipulation) would isolate whether the gains come from the log-barrier idea itself or from the expanded threat model. This would make the comparison to baselines more apples-to-apples.
- Defense evaluation with larger clean subsets (10–20%) and/or more modern defenses would be more informative, though the paper explicitly scopes this out.
- Numerical anchor points for Figure 3 trends would strengthen the poisoning-ratio motivation.

## Removed Points

- **"Unifies" claim is overstated**: The Harsh Critic argued the unification claim is ambitious because the penalty only suppresses the original class and doesn't actively steer. However, the paper clearly states "the standard classification objective then naturally steers the model towards either predicting the attacker's target class (RMA) or predicting background (ODA)." This is logically sound and well-explained. Removed as not a genuine weakness.
- **Physical-world transfer presentation is misleading**: The Harsh Critic argued the abstract's claim about "stronger synthetic-to-physical transfer" could mislead. The claim is technically correct as a relative comparison (BadDet+ substantially outperforms all baselines on PTSD). Removed as factually accurate.
- **Missing λ sensitivity analysis (Appendix A.5)**: Removed per instruction — parser strips appendix sections from all papers; they exist in the original submission.
- **Defense evaluation uses too-small clean subsets**: The paper explicitly acknowledges this limitation and scopes out larger defense benchmarks. Removed as already addressed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Soften "position- and scale-invariant" to "position- and scale-robust" throughout.
2. Add discussion of the competitive UBA DINO ODA case and a deeper analysis of why the penalty mechanism fails on YOLOv5 RMA.
3. Report standard deviations for key results (at least COCO Tables 1–2) over multiple seeds.
4. Add a brief threat-model qualification to the abstract (e.g., "under a training-time loss-manipulation threat model").
5. Include specific numerical values from Figure 3 in the main text for the poisoning-ratio argument.

## Score and Decision

**Calibration anchors:**
- **LeBD** (3.25, Reject, Round 1): Backdoor *defense* for YOLO only; narrow scope, simple extension. BadDet+ is substantially stronger in breadth, novelty, and rigor.
- **Certified Copy** (3.00, Reject, Round 1): Classifier backdoor with a new cost function; scores mostly 3. BadDet+ has stronger evaluation and diagnostic contribution.
- **VSSC** (4.33, Reject, Round 1): Trigger design for robust backdoors; performance not impressive vs baselines. BadDet+ has clearer empirical advantage.
- **CLIP Backdoor Analysis** (5.25, Reject, Round 1): Empirical study of backdoor effects on CLIP; analytical contribution only, no method. BadDet+ matches the analytical depth and adds a novel method.
- **Efficient Backdoor Attacks** (5.75, Accept, Round 1): CLIP-based method for data-constrained scenarios; scores 6/3/8/6. Comparable quality, but BadDet+ has stronger diagnostic contribution.
- **VLOOD** (6.33, Accept, Round 1): OOD-based VLM backdoor; scores 6/5/8. Comparable in rigor and contribution quality.

**Round 1 bracket:** The paper clearly sits above the 3–4 range (reject-level anchors like LeBD and Certified Copy are much weaker) and somewhat above the 4–5.5 range. The closest comparators are Efficient Backdoor Attacks (5.75, Accept) and VLOOD (6.33, Accept). The paper has no fatal flaws; its weaknesses are presentation overclaims and missing discussion of counterexamples, all addressable in revision. The core contributions (diagnostic analysis, TDR metric, unified formulation) are solid and independently valuable. Final score anchored at **6.0**, reflecting a borderline-accept paper with genuine contributions that can be strengthened with revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>