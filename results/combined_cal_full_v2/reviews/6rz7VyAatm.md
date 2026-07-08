Now I have all the data I need. Let me compile the final review.

## Summary

This paper identifies several evaluation blind spots in prior object-detection backdoor research and introduces BadDet+, a log-barrier penalty-based attack framework that unifies region misclassification (RMA) and object disappearance (ODA) under a single mechanism. The diagnostic contributions in Section 3—particularly the identification that ASR overstates RMA success by ignoring duplicate detections, and that mAP is a poor proxy for ODA—are well-evidenced and independently valuable. The proposed TDR metric and instance-level ASR cleanly expose these failure modes. The method is evaluated extensively across two datasets, four architectures, multiple trigger placements, and physical-world transfer, substantially exceeding the scope of prior work.

## Strengths

- **Genuine diagnostic contributions (Section 3).** The paper identifies four real, non-obvious evaluation blind spots in prior object-detection backdoor work: (i) ASR overstates RMA success because it counts a detection of the target class as success even when the original-class detection persists (duplicate detections, documented in Figure 1a); (ii) mAP is a poor proxy for ODA, since reductions can come from localization errors or phantom boxes (Figures 1b–c) rather than actual disappearance; (iii) prior work tests triggers at a single fixed position and scale, ignoring real-world variation; (iv) some methods rely on curated auxiliary datasets with scene-sparsity assumptions. The proposed TDR metric for RMA and instance-level ASR for ODA cleanly expose failure modes that prior metrics hide. **[weight=8.67]**

- **Principled and clean method design (Section 4).** The log-barrier penalty formulation (Eqs. 1–2) is mathematically well-motivated. The insight that ODA can be treated as RMA with background as the target class, unified under a single loss term that suppresses original-class logits, is elegant. The two variants—sigmoid-based for per-class detectors (FCOS, YOLO, DINO) and softmax-compatible via log-odds for Faster R-CNN—show genuine architectural awareness rather than a one-size-fits-all approach. **[weight=9.81]**

- **Extensive and carefully controlled evaluation.** The paper evaluates across two datasets (COCO, MTSD), four architectures (FCOS, Faster R-CNN, DINO, YOLOv5), multiple trigger placements (fixed high/low/both, random), and includes physical-world transfer to PTSD. This is substantially more comprehensive than any single prior work in this area and establishes a strong benchmarking foundation for the field. **[weight=9.02]**

- **Real-world validation is genuine.** The synthetic-to-physical transfer gap identified by prior work is a real problem, and BadDet+'s consistently higher PTSD ASR@50 compared to baselines (Table 3) provides meaningful evidence that the penalty-based training induces more robust trigger associations that survive the digital-to-physical domain shift. **[weight=8.66]**

## Weaknesses

### Fatal
None.

### Major

- **Threat-model asymmetry in comparisons.** BadDet+ assumes the adversary can modify the training loss function directly (Section 4, line 84: "our design assumes a stronger adversarial setting in which the training process can be controlled"), while all baselines (BadDet, UBA, Align, Morph) are data-poisoning-only. The paper acknowledges this asymmetry (lines 84–88, 262–263), but the abstract and comparison tables present BadDet+ as "outperforming" prior work without clearly flagging which methods operate under which constraints. The comparison is between methods with fundamentally different capabilities. Adding a loss-manipulation baseline would isolate the value of the specific log-barrier design from the advantage of the stronger threat model. **[weight=2.42]**

- **YOLO results undermine the "unified" and "consistent" framing.** In Table 4 (RMA on MTSD), BadDet+ underperforms BadDet on YOLOv5 across both ASR@50 (91.97 vs. 96.57) and TDR@50 (7.54 vs. 3.14). The paper states that λ = 0 is optimal for this architecture (line 221–222), meaning the penalty should be turned off entirely—the method reduces to no attack. This is a genuine failure mode on a supported architecture that directly weakens the abstract's claim of "consistent applicability across RMA and ODA." The paper provides no architectural explanation for why this occurs beyond deferring to an appendix. **[weight=2.65]**

### Minor

- **Poisoning ratios not controlled across methods in main tables.** BadDet+ uses a fixed 50% poisoning ratio, while baselines use their "default" ratios (unspecified in main text). The poisoning ratio analysis (Figure 3) partially addresses this for a subset of methods, but readers cannot determine from Tables 1–4 whether BadDet+'s advantage stems from the loss penalty or simply from using a more favorable poisoning ratio. **[weight=4.42]**

- **The λ hyperparameter varies by 1000× across architectures** (λ=1.0 for FCOS/Faster R-CNN/DINO, λ=0.001 for YOLO). This extreme discrepancy suggests the penalty interacts fundamentally differently with YOLO's loss structure, yet the main text presents this without analysis of why. The λ sensitivity study is deferred to Appendix A.5. **[weight=3.32]**

- **The abstract promises a theoretical analysis** ("the proposed penalty acts selectively within a trigger-specific feature subspace") but the main text contains no formal statement (theorem, proposition, or even a formal claim) of this result. Section 4 provides only intuitive design rationale and defers to Appendix A.7. Even a brief formal statement in the main text would better align the abstract's promise with what the paper delivers. **[weight=1.53]**

### Trivial
None.

## Nice-to-Haves

- Adding a simple loss-manipulation baseline (e.g., directly modifying the classification loss for triggered objects without the log-barrier structure) would convert the comparison from "our method with stronger assumptions beats methods with weaker assumptions" into "our specific design choice beats other designs under the same assumptions."
- Including variance or confidence intervals for the main results (Tables 1–4) would help assess whether reported differences are meaningful.
- An architectural explanation for why the penalty fails on YOLO (rather than deferring to an appendix) would strengthen the paper's contribution and help future work.

## Removed Points

- **Defense evaluation is too narrow:** Removed because the paper explicitly scopes this out (Section 2.2, lines 58: "our robustness evaluation is deliberately restricted to fine-tuning-style defenses (FT and FT-SAM)"). The abstract's robustness claims are qualified as "under fine-tuning-based defenses." The paper is transparent about this limitation.
- **Single trigger type concern:** Removed because (a) alternative triggers are tested in Appendix A.4, and (b) the blue square is required for PTSD physical-world evaluation, a core contribution of the paper.
- **Statistical significance:** Removed as a generic concern that applies broadly to this subfield; not specific enough to warrant a distinct weakness item.
- **Unstated circularity in Eq. 1 (coupling between penalty and detector localization):** Speculative—the paper does not discuss this, but there is no evidence it occurs in practice.
- **"UBA Box and Align Random are also data-poisoning-only":** These are introduced as controlled evaluation variants, not as claims of superiority. Not a weakness.

## Novel Insights

None beyond the paper's own contributions. The meta-observation from the reviews is that the diagnostic contributions (Section 3) and evaluation protocol improvements (TDR, instance-level ASR) are the most robust and defensible parts of the paper, while the comparative claims about the method are tempered by the threat-model asymmetry and the YOLO failure mode. Reframing BadDet+ as a case study demonstrating the importance of proper evaluation—rather than as a direct outperformance claim—would better align the paper's framing with its evidence.

## Suggestions

1. Add a clear annotation (footnote or column) to all comparison tables indicating which methods assume data-poisoning-only vs. loss-manipulation capability.
2. Provide at least a brief architectural explanation for the YOLO failure (what property of YOLO's loss structure causes the penalty to be ineffective?) rather than only deferring to an appendix.
3. Include a formal statement of the theoretical claim in the main text, or soften the abstract's language.
4. State the baseline poisoning ratios in the main text, and consider reporting a controlled comparison where all methods use the same poisoning ratio.

## Score and Decision

**Calibration.** All anchors retrieved across rounds:

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| LeBD (7vKWg2Vdrs) | 3.25 | R1 | Yes | Simplistic extension of GradCAM→LayerCAM; weak novelty. BadDet+ is substantially stronger in method and evaluation. |
| Certified Copy (66e22qCU5i) | 3.00 | R1 | Yes | Limited novelty; similar idea pre-explored. BadDet+ has clearer novel contributions (diagnostics + unified formulation). |
| VSSC (H6XiAoyugv) | 4.33 | R1 | Yes | Good trigger design but insufficient depth; performance not clearly superior. BadDet+ has stronger empirical support. |
| Backdoor in Seconds (ZyPRwskBli) | 4.75 | R1 | Yes | Interesting training-free attack but concerns about threat model realism. BadDet+'s threat model is well-justified. |
| Efficient Backdoor (vRyp2dhEQp) | 5.75 | R1 | Yes | Practical data-constrained scenario; strengths 7.50–9.07, weaknesses include -5.60 (missing theory). BadDet+ has comparable strengths, somewhat milder weaknesses. |
| GCB (LsTIW9VAF7) | 5.80 | R2 | Yes | Strong method and evaluation; one reviewer gave 8. Weaknesses about novelty (-5.05) and missing FT-SAM. BadDet+'s weaknesses have lower severity weights. |
| VLOOD (tZozeR3VV7) | 6.33 | R1 | Yes | Novel OOD-data setting for VLM backdoors; well-validated across architectures. Strengths 7.53–9.52, weaknesses 3.79–6.46. Slightly above BadDet+ in overall assessment. |

**Bracket (Round 1):** 5.5–6.5. The paper is clearly above LeBD (3.25), Certified Copy (3.00), VSSC (4.33), and Backdoor in Seconds (4.75). It is comparable to Efficient Backdoor (5.75) and GCB (5.80), and slightly below VLOOD (6.33).

**Narrowing (Round 2):** Comparing weighted items: BadDet+ shares with Efficient Backdoor and GCB the pattern of high-weight strengths (8.67–9.81) and moderate-weight weaknesses (1.53–4.42). Its strongest weakness weight (4.42 for poisoning-ratio control) is lower than the most damaging weaknesses in Efficient Backdoor (-5.60 for missing theory) and GCB (-5.05 for novelty concerns). However, the threat-model asymmetry and YOLO failure are structural limitations that prevent the paper from reaching VLOOD's level (6.33), where weaknesses were primarily about methodology details rather than core comparison fairness.

**Final score: 6.0.** The paper has genuine contributions—the diagnostic analysis alone is a meaningful advance for the field—but the comparative claims are weakened by the asymmetric threat model and the YOLO failure, both of which the authors acknowledge but do not fully resolve.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>