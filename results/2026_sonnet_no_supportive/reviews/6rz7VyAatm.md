**Round 1 Bracket:** Based on calibration anchors, I place this paper in the **5.5–6.5** range. Papers scoring 4.75 ("Backdoor in Seconds") and 5.75 ("Efficient Backdoor Attacks in Real-world Scenarios") are the closest topical comparisons. BadDet+ is stronger than the 4-5 range papers due to: (1) genuine new metric (TDR), (2) comprehensive multi-architecture/multi-dataset evaluation with physical-world validation, and (3) explicit methodological critique of the field's evaluation practices. The threat model asymmetry and YOLO failure prevent it from reaching 7+. I narrow to **6.0**.

---

## Summary
BadDet+ proposes a log-barrier penalty that unifies backdoor region misclassification (RMA) and object disappearance (ODA) for object detection under a single training-time loss augmentation. Alongside the method, the paper introduces True Detection Rate (TDR) as a complementary metric to ASR, exposes systematic evaluation blind spots in prior work (duplicate detections in RMA, mAP confounds in ODA), and validates physical-world transfer on the PTSD benchmark across four architectures and two datasets.

## Strengths
- **TDR metric and evaluation critique (Section 3, Table 2):** The paper identifies a concrete failure mode — duplicate detections where the original class persists alongside the target class. Table 2 quantifies this precisely: BadDet achieves TDR@50 of 44–76% despite near-perfect ASR@50 (≥99%), meaning the original detection survives the majority of the time. The TDR metric is well-motivated and directly actionable as a field correction.
- **Physical-world transfer gap (Table 3, PTSD):** BadDet+ achieves 59–85% ASR@50 across architectures on PTSD; UBA reaches 0.53% on Faster R-CNN and Morph reaches 7.72%. This is a qualitative rather than marginal improvement and validates the practical motivation concretely.
- **Unified and architecturally careful formulation (Eqs. 1–2):** The log-barrier penalty is technically sound, with separate sigmoid-independent (Eq. 1) and one-vs-rest log-odds (Eq. 2) variants for sigmoid-head vs. softmax-head detectors. The ODA-as-special-case-of-RMA insight is clean.
- **Poisoning-ratio analysis (Figure 3):** The paper shows that increasing the poisoning ratio for data-poisoning baselines either fails to suppress duplicate detections (FCOS/Faster R-CNN) or catastrophically degrades mAP. This is a principled empirical argument for why training-time intervention is necessary, not merely convenient.
- **Honest self-reporting:** The paper explicitly flags YOLO as a failure case (λ=0 optimal) and acknowledges BadDet outperforms BadDet+ under fine-tuning-based defenses in the RMA setting. This is unusual and creditable.

## Weaknesses

### Fatal
None.

### Major
- **Threat model asymmetry vs. all baselines (Section 4):** BadDet+ requires direct training-loss manipulation; every baseline (BadDet, UBA, Align, Morph) operates under data-poisoning only. This is a strictly stronger threat model. The paper motivates this by showing data-poisoning alone is unreliable (Figure 3), which is a reasonable argument. However, the comparisons in Tables 1–4 are not apples-to-apples: the critical missing piece is an ablation isolating the log-barrier penalty from the general privilege of training-time access. A simpler training-time suppression loss (e.g., direct cross-entropy on triggered objects' true class) could potentially yield similar gains. Without this, readers cannot determine whether the log-barrier formulation specifically is the key contribution or whether any training-time loss manipulation would work as well.

- **YOLO failure without mechanistic diagnosis (Table 4):** BadDet+ underperforms BadDet on YOLO RMA in both ASR@50 (91.97 vs. 96.57 Fixed) and TDR@50 (7.54 vs. 3.14 Fixed). The paper notes "λ=0 is optimal for this architecture" and defers explanation to future work (Section 5.3, Appendix A.8). YOLO is one of four tested architectures; claiming "consistent applicability across RMA and ODA" (abstract) without identifying why this architecture is incompatible leaves a notable gap in the generality claim.

### Minor
- **Defense evaluation scope partially cuts against the paper:** Defense evaluation is restricted to FT and FT-SAM (explicitly scoped in Section 2.2). Within this narrow scope, "For RMA, BadDet generally outperforms BadDet+ under both FT and FT-SAM" (Section 5.3). The paper acknowledges this honestly, but it weakens the "stronger and more robust" framing of the abstract for the RMA task specifically. The ODA results post-defense are stronger.

### Trivial
- The empirical mAP-confound demonstration is deferred to Appendix A.2.3; even a one-row summary in the main text would strengthen this diagnostic contribution.

## Nice-to-Haves
- An ablation controlling for threat model level: train with training-time access but substitute a simpler suppression loss to isolate whether the log-barrier form specifically drives gains.
- Mechanistic diagnosis of YOLO's incompatibility with the log-barrier (e.g., which head design, anchor strategy, or regression formulation interacts poorly) and whether a modified λ schedule or formulation variant resolves it.
- Variance/confidence intervals for Tables 1–4, especially for narrow gaps like DINO RMA where BadDet already achieves low TDR.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Critic's abstract accuracy complaint:** The abstract says BadDet+ "outperforms existing RMA and ODA baselines." This is accurate for 3 of 4 architectures in RMA and all architectures in ODA. The YOLO failure is flagged in the paper and is a real limitation, but the abstract is not technically misleading enough to warrant formal criticism.
- **Trigger breadth criticism:** The paper uses a blue square because PTSD evaluation requires it (explicitly stated in Section 5.1). Alternative triggers are tested in Appendix A.4. This is reasonable and not a methodological flaw.
- **Variance/confidence intervals as methodological flaw:** Standard practice in large-scale OD benchmarking is single-run evaluation. This belongs as a nice-to-have, not a weakness.

## Novel Insights
The most underappreciated contribution of this paper is the Figure 3 poisoning-ratio experiment, which provides a principled empirical argument — not merely intuition — for why training-time loss manipulation is necessary rather than optional in the OD backdoor setting. Unlike image classification, where high poisoning rates reliably implant backdoors, OD models trained with data poisoning either fail to suppress duplicate detections (FCOS/Faster R-CNN even at 100% poisoning) or do so only by catastrophically degrading clean mAP. This positions BadDet+'s threat-model extension not as scope creep but as a response to a documented structural failure of existing paradigms. The paper does not foreground this argument as strongly as it deserves.

## Suggestions
- Add an ablation with a simple baseline training-time suppression loss (no log-barrier) to isolate the penalty formulation's contribution from the broader benefit of training-time access. This directly addresses the main structural critique.
- Diagnose the YOLO incompatibility: identify the architectural feature that interacts poorly with the log-barrier and propose a potential fix, even if tested only on YOLO.
- Move the mAP-confound empirical demonstration (Appendix A.2.3) into the main text as a compact table — this is one of the paper's central diagnostic contributions and deserves main-body visibility.

## Score and Decision

**Anchor papers retrieved:**
| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| 7vKWg2Vdrs.md (LeBD, YOLO backdoor defense) | 3.25 | R1 | Narrower scope, YOLO-only defense; weaker than BadDet+ |
| S5JCqTJyKj.md (Deferred Backdoor Functionality) | 3.00 | R1 | Classification-only, limited baselines |
| 66e22qCU5i.md (Certified Copy) | 3.00 | R1 | Training-time loss attack for classification, narrower |
| ZyPRwskBli.md (Backdoor in Seconds, model editing) | 4.75 | R1/R2 | Different threat model, less evaluation breadth |
| H6XiAoyugv.md (VSSC triggers) | 4.33 | R1 | Physical triggers for classification, less diagnostic contribution |
| s56xikpD92.md (BaDExpert) | 6.25 | R1 | Strong defense paper, accepted; comparable rigor |
| 1OfAO2mes1.md (Backdoor Secrets) | 6.00 | R1 | Defense paper, accepted |
| VNMJfBBUd5.md (Activation Gradient detection) | 6.00 | R1 | Defense paper, accepted |
| vRyp2dhEQp.md (Efficient Backdoor Attacks real-world) | 5.75 | R2 | Attack under realistic constraints, accepted; similar scope |
| tZozeR3VV7.md (VLOOD, OOD backdoor) | 6.33 | R2 | Backdoor attack under realistic constraints, accepted |
| rK0YJwL69S.md (Protecting against simultaneous poisoning) | 5.50 | R2 | Defense, accepted |
| LsTIW9VAF7.md (Less is More, clean-image backdoor) | 5.80 | R2 | Efficient backdoor attack, rejected |
| Gf4KZIqLHD.md (DIFF2) | 5.50 | R2 | Attack on security models, rejected |

**Round 1 bracket:** 5.5–6.5, based on comparison with accepted backdoor attack papers at 5.75–6.33 that similarly address realistic attack scenarios with practical justification.

**Narrowing:** BadDet+ compares favorably to "Efficient Backdoor Attacks in Real-world Scenarios" (5.75, accepted) and "VLOOD" (6.33, accepted) in terms of evaluation breadth and practical contribution. The threat model asymmetry without ablation and the undiagnosed YOLO failure pull it toward the lower end. The TDR metric as a field-level contribution and the physical-world validation strength push it upward. I settle at **6.0**: a borderline accept. The paper makes a genuine contribution to OD backdoor evaluation methodology and provides a competitive attack framework, but the core method comparison is confounded by the threat model asymmetry and the universality claim is weakened by the YOLO failure.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>