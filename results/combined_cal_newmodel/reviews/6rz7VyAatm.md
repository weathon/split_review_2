Now I have a clear picture. Let me construct the final consolidated review.

## Summary

This paper introduces BadDet+, a unified backdoor attack framework for object detection that augments the training loss with a log-barrier penalty to simultaneously achieve region misclassification (RMA) and object disappearance (ODA). The paper makes three core contributions: (1) diagnosing evaluation blind spots in prior object-detection backdoor work (ASR ignoring retained labels, mAP as a poor ODA proxy, lack of trigger scaling/placement robustness checks, curated dataset dependence), (2) introducing the True Detection Rate (TDR) metric to complement ASR for RMA evaluation, and (3) proposing the log-barrier penalty formulation that unifies RMA and ODA under a single mechanism. The method is evaluated on COCO and MTSD with physical-world validation on PTSD, across four detector architectures.

## Strengths

- **Diagnosis of evaluation blind spots (Section 3).** The paper identifies four concrete, well-documented limitations in prior object-detection backdoor work: ASR ignoring retained labels causing overestimation of RMA success (Figure 1a shows duplicate detections), mAP being a poor proxy for ODA (Figure 1b–c shows UBA's phantom boxes), the absence of robustness checks for trigger scaling and placement, and dependence on curated datasets (MORPH's grid-augmentation). This diagnostic work is specific, well-illustrated, and genuinely valuable to the community regardless of the proposed method's merits.

- **Introduction of the TDR metric for RMA (Section 5.2).** The True Detection Rate cleanly addresses a real blind spot that ASR alone cannot capture. Tables 2 and 4 present a compelling demonstration: existing methods (BadDet, Morph) achieve high ASR@50 but also high TDR@50 (44–75% on COCO, meaning the original class detection survives alongside the target), while BadDet+ drives TDR@50 down to 1.54–3.18% on COCO. This is the paper's most convincing quantitative result.

- **Clean mathematical formulation (Section 4.1).** The log-barrier penalty (Eq. 1–2) is elegant and well-motivated. The insight that ODA is a special case of RMA with background as the target class is theoretically sound. The two formulations — per-class logits for FCOS/YOLO/DINO, and one-vs-rest log-odds for softmax-based detectors like Faster R-CNN — demonstrate careful attention to architectural differences.

- **Thorough experimental scope.** Two datasets (COCO, MTSD) with physical-world transfer (PTSD), four architectures (FCOS, Faster R-CNN, DINO, YOLOv5), multiple trigger placements (fixed positions, random), and poisoning ratio sweeps (Fig. 3). This is more comprehensive than prior work in this sub-area.

## Weaknesses

### Fatal

None.

### Major

- **Threat-model asymmetry in comparative framing.** BadDet+ assumes **training-process control** (the attacker can modify the loss function during training), while all baselines — BadDet, UBA, Align, Morph — assume only **data-poisoning access** (the attacker can only modify training data). These are fundamentally different threat models with different strengths. The paper acknowledges this (line 84: "our design assumes a stronger adversarial setting") but the abstract ("outperforming existing RMA and ODA baselines") and Tables 1–4 present results as if the methods are directly comparable. A method that can rewrite the loss function has a structural advantage over methods that can only stamp pixels on images; this is baked into the threat-model difference, not necessarily a meaningful algorithmic advance. The paper's attempted justification — that data poisoning alone is insufficient (contributions iv) — contextualizes but does not resolve the asymmetry. The contribution should be framed as demonstrating the capability of a training-process-controlled attacker rather than as straightforward "outperforming" of data-poisoning methods. This does not invalidate the technical work but affects how the results should be interpreted.

### Minor

- **Narrow defense evaluation.** The defense study (Figure 2) tests only fine-tuning (FT and FT-SAM) with 50–100 clean samples (2–4% of MTSD). The paper acknowledges this scope explicitly (line 58: "deliberately restricted") and notes that no model-agnostic object-detection-specific defense exists. However, the finding that "ASR@50 remains above 0.4" after this weak defense is not strong evidence of robustness. Moreover, the paper's own results show that BadDet (not BadDet+) is generally more robust to fine-tuning for RMA (line 256: "For RMA, BadDet generally outperforms BadDet+ under both FT and FT-SAM"). The limitation is transparent but means the defense claims carry limited weight.

- **Edge cases where the method does not outperform baselines.** On YOLO RMA (Table 4), BadDet+ underperforms BadDet on both ASR@50 (91.97 vs. 96.57) and TDR@50 (7.54 vs. 3.14 — lower is better). The paper acknowledges this ("λ=0 is optimal for this architecture," line 221), but this means for a major architecture (YOLO), BadDet+ provides no benefit over the baseline. On DINO ODA (Table 1), UBA achieves 97.89 ASR@50 vs. BadDet+'s 97.60 — essentially equivalent. These do not invalidate the method but weaken the "consistently strong results across all tested settings" (line 172) framing.

- **The claim of "position- and scale-invariant behavior" (Abstract) is not directly tested.** The random-trigger evaluation partially addresses placement variation, but degradation between Fixed and Random settings can be substantial (e.g., Table 4 FCOS BadDet+ TDR@50: 6.75 Fixed vs. 16.96 Random; ASR@50: 96.41 Fixed vs. 93.13 Random). A direct invariance test across positions/scales within an object would provide cleaner evidence for this claim.

- **Independent-object evaluation protocol (line 164) creates an artificial test setting.** Each trigger-bearing object is evaluated in isolation (one poisoned object per test instance). In real-world deployment, an adversary would want all trigger-bearing objects to fail simultaneously in a single image. This scenario is not tested, leaving it unclear whether the attack generalizes to dense, multi-object poisoned scenes.

### Trivial

None.

## Nice-to-Haves

- An ablation that restricts BadDet+ to data-poisoning access (without loss-function modification) would help isolate the benefit of training-process control.
- Testing the all-objects-poisoned scenario would bridge the gap between the independent-object protocol and real-world deployment.
- Adding a stronger defense (e.g., pruning-based, or neural cleanse with ~10% clean data) would give the robustness claims more weight.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Defense evaluation is too weak to support the abstract's robustness claims about physical triggers"** — The harsh critic conflated "robustness to physical triggers" (abstract, meaning physical-world trigger transfer validated via PTSD experiments) with defense robustness (FT/FT-SAM). The abstract's claim about physical triggers refers to synthetic-to-physical transfer (PTSD), not defense evaluation. Removed because it rests on a misreading of the abstract.
- **"ODA as special case of RMA is practically limited because detectors lack explicit background class"** — The paper addresses this via two separate formulations (per-class logits for FCOS/YOLO/DINO; one-vs-rest log-odds for softmax-based detectors like Faster R-CNN). Removed because the paper already handles this concern.
- **"No comparison under the same threat model"** — This is a nice-to-have, not a weakness. The paper's contribution (v) is the method for the stronger threat model; comparing against baselines that inherently cannot match is a presentation issue (addressed under Major weaknesses), not a missing experiment.
- **"Contributions (iii) and (iv) are premises not findings"** — Subjective framing opinion; the paper's diagnostic contributions (i–iv) are presented as evaluation insights motivating the method (v).
- **Missing appendix content and formatting/style nitpicks** — Parser artifacts; not valid criticisms.

## Novel Insights

None beyond the paper's own contributions. The key observation from the harsh review — that the threat-model asymmetry undermines direct comparative framing — is valid and carried into the Major weakness. The remaining observations (narrow defense evaluation, edge cases where the method doesn't outperform, position/scale invariance claim not directly tested, artificial evaluation protocol) are straightforward readings of the paper's reported results.

## Suggestions

- Reframe the headline comparison: present BadDet+ as demonstrating the upper bound of what a training-process-controlled attacker can achieve, rather than as "outperforming" data-poisoning methods. Label comparative tables explicitly as showing the capability gap between two different threat models.
- Explicitly test the position/scale invariance claim with a controlled experiment varying trigger position and scale within objects, reporting invariance quantitatively.
- Investigate and report why BadDet+ underperforms on YOLO RMA (beyond noting λ=0 is optimal), or concede architecture-dependence in the claims.
- Add a supplementary experiment testing the all-objects-poisoned scenario to bridge the gap between the independent-object protocol and real-world deployment.

## Score and Decision

**Calibration anchors retrieved across rounds:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| LeBD (YOLO backdoor defense) | 3.25 | R1 | Yes | Substantially weaker — limited to one architecture, technical novelty concerns |
| Certified Copy (backdoor attack) | 3.00 | R1 | Yes | Weaker — limited novelty, insufficient experiments, outdated baselines |
| Backdoor in Seconds (model editing) | 4.75 | R1, R2 | Yes | Similar threat-model asymmetry issue; my paper has stronger diagnostic contributions and more thorough experiments |
| Robust Backdoor VSSC triggers | 4.33 | R1, R2 | Yes | Weaker — marginal performance gains, insufficient depth |
| VLOOD (VLM backdoor OOD) | 6.33 | R1, R2 | Yes | Stronger — novel setting, well-received; my paper has comparable thoroughness but a more significant framing issue |
| Efficient Backdoor Attacks (data-constrained) | 5.75 | R1, R2 | Yes | Similar quality level — both have solid methodology with some framing/scope concerns |
| Wicked Oddities (clean-label backdoor) | 6.00 | R2 | Yes | Accepted despite multiple negative-favorability weaknesses (−1.36, −3.01, −0.52, −0.36, −2.99); my paper has only one negative-favorability weakness (−0.67) |
| A Closer Look at Backdoor Attacks on CLIP | 5.25 | R2 | No | Purely analytical; my paper has both diagnostic and methodological contributions |

**Round-1 bracket:** 4.0–6.0 (eliminated >6.0 due to the threat-model asymmetry issue being more significant than typical minor weaknesses in 6+ papers; eliminated <4.0 because the diagnostic contributions, TDR metric, and thorough experiments clearly exceed papers in that range).

**Round-2 narrowing:** Compared favorability profiles. My paper's single negative weakness (−0.67) is less severe than the multiple negatives in Wicked Oddities (6.0, accepted) but the threat-model asymmetry is a more *structural* issue than Wicked Oddities' novelty concerns. Papers at 4.75 (Backdoor in Seconds) have similar threat-model issues but lack the diagnostic and metric contributions. Papers at 5.75 (Efficient Backdoor) are most comparable in overall quality, with my paper having slightly stronger diagnostic contributions but a more salient framing problem.

**Final score: 5.5.** The paper has genuine contributions — the diagnostic work and TDR metric alone are valuable — but the threat-model asymmetry in comparative framing needs to be addressed before the paper can be recommended for acceptance. The technical work is sound; the presentation is somewhat misleading.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>