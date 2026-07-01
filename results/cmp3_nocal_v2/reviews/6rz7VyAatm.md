Now let me write the final consolidated review.

---

## Summary

This paper identifies four evaluation blind spots in existing object-detection backdoor attacks (ASR ignoring duplicate detections in RMA, reliance on mAP for ODA, lack of trigger scaling/placement robustness tests, and dependence on curated datasets) and proposes BadDet+, a unified attack framework using a log-barrier penalty that suppresses true-class predictions on trigger-bearing objects. The method unifies region misclassification (RMA) and object disappearance (ODA) under a single mechanism, treating ODA as RMA where the target class is background. Experiments across COCO, MTSD, and PTSD with four architectures (FCOS, Faster R-CNN, DINO, YOLOv5) show strong ASR with low TDR for RMA and high ASR for ODA, with modest clean mAP degradation.

## Strengths

1. **Well-diagnosed evaluation blind spots (Section 3).** The paper identifies four concrete problems in prior evaluations — ASR ignoring duplicate detections in RMA, mAP conflating disappearance with other failures in ODA, absence of trigger scaling/placement robustness checks, and reliance on curated datasets or scene-sparsity assumptions. These are clearly articulated, illustrated with examples (Figure 1), and constitute a useful methodological contribution that stands independently of the proposed attack method.

2. **Principled unified formulation (Section 4).** Viewing ODA as a special case of RMA where the target is background is well-motivated. The log-barrier penalty (Equations 1–2) sharply penalizes original-class logits above a threshold only where a predicted box overlaps a trigger-bearing ground-truth object. The dual sigmoid/softmax formulations show design consideration for architectural differences in logit normalization. The approach is conceptually clean and the design rationale is clearly explained.

3. **Consistently strong empirical results across multiple settings.** On COCO RMA (Table 2), BadDet+ achieves ASR@50 of 97–99% while reducing TDR@50 to 1.5–3.2% (vs. 44–76% for BadDet). On MTSD/PTSD (Tables 3–4), BadDet+ substantially outperforms Morph, UBA, and Align on ODA across FCOS, Faster R-CNN, and DINO, with meaningful transfer to the physical domain. Clean mAP degradation is modest (~1–2 points on COCO).

## Weaknesses

### Fatal

None.

### Major

1. **Cross-threat-model comparison is not consistently flagged as such.** BadDet+ operates under a strictly stronger threat model (training-time loss manipulation; Section 4, line 84) than all baselines (data-poisoning-only). The paper acknowledges this in Section 4 and the Conclusion, but the abstract and introduction frame the comparison as head-to-head ("outperforming existing RMA and ODA baselines") without marking the asymmetry. This gives the impression of a within-threat-model comparison when it is not. The evidence that "data poisoning alone is insufficient" (used to justify the stronger threat model) is itself drawn from comparisons against data-poisoning-only baselines — a framing that would benefit from being more clearly separated. The diagnostic contributions (Section 3) and the unified formulation remain valuable regardless, but the headline attack comparisons need transparent qualification.

### Minor

2. **Framing of defense robustness is partially inconsistent with RMA results.** The introduction claims BadDet+ "yields more robust behavior... under fine-tuning-based defenses." For ODA this holds (ASR@50 remains above 0.4 after FT/FT-SAM). However, for RMA, the paper honestly reports that "BadDet generally outperforms BadDet+ under both FT and FT-SAM" (line 256). The abstract's "improved robustness to physical triggers" correctly refers to synthetic-to-physical transfer (PTSD), not defenses, but the introduction's broader claim about fine-tuning robustness conflates the two settings. The paper would benefit from precisely distinguishing which kind of robustness (physical-transfer vs. anti-defense) it claims for which attack type.

3. **YOLO RMA limitation is acknowledged but under-explained.** On YOLOv5 RMA (Table 4), BadDet underperforms BadDet+ on ASR@50 (96.57 vs. 91.97 Fixed) and TDR@50 (3.14 vs. 7.54 Fixed). The paper notes that "λ = 0 is optimal for this architecture" (line 221) and flags this for future investigation (line 242), but the abstract claims "consistent applicability across RMA and ODA." While BadDet+ still achieves 92% ASR@50 on YOLO RMA (it does not "fail"), the advantage over the simpler baseline disappears, and the paper does not explain why this architecture behaves differently.

4. **UBA baseline essentially ties BadDet+ on DINO for ODA.** On COCO ODA (Table 1), UBA achieves 97.89% ASR@50 on DINO vs. BadDet+'s 97.60%. The paper describes this as "marginal improvements over BadDet+ on DINO" (line 172), which understates that a data-poisoning-only attack matches the proposed method on one architecture. (BadDet+ maintains substantially better clean mAP, 44.43 vs. 41.58, but the ASR parity deserves more direct discussion.)

5. **No variance reporting for main results.** The main results (Tables 1–4) report single runs without error bars or confidence intervals. The defense evaluation uses 10 random runs with box plots (Figure 2), showing the infrastructure exists. Reporting variance for core attack results would strengthen credibility.

### Trivial

6. **Post-defense clean mAP not reported.** Figure 2 shows post-defense ASR/TDR/mAP but does not include clean mAP after FT/FT-SAM. This is useful for understanding the defense-vs-attack tradeoff.

## Nice-to-Haves

- A within-threat-model comparison (e.g., a different penalty function or direct logit manipulation under training-process control) would clarify whether the specific log-barrier formulation is necessary or whether simpler approaches achieve similar results.
- The paper could report what BadDet+ achieves under data-poisoning-only constraints (no loss modification) to better delineate the two threat models.
- A sensitivity analysis showing how baseline performance varies when their hyperparameters are tuned per architecture (rather than using default settings) would strengthen the fairness claim.

## Removed Points

These points from the input review are removed per filtering rules, with brief justification:

- **Theoretical contribution in appendix not assessable.** The paper cites Appendix A.7 for the theoretical analysis. The appendix exists in the original submission but was stripped by the parser. Per the hard filtering rules, criticisms about content that appears only in the appendix are removed — the authors cannot be penalized for parser-induced inaccessibility.
- **"BadDet+ does not work on YOLO."** This is factually inaccurate. BadDet+ achieves 91.97% ASR@50 on YOLO RMA (Fixed) — it underperforms BadDet but does not "fail." The paper acknowledges the caveat.
- **Five contributions are "inflated."** This is a meta-comment about presentation rather than a technical weakness. The contributions list is a matter of organization, not substance.
- **"Penalty requires trigger knowledge during training."** This is a description of the method and its threat model, not a weakness. The attacker knows which objects are poisoned.
- **"UBA Box and Align Random are authors' own constructions."** The paper clearly states "we introduce two variants" — this is transparent.
- **"Comparison is circular."** The paper motivates the stronger threat model by separately demonstrating (Figure 3) that data-poisoning-only approaches are unreliable. This is a standard motivation structure, not a circular argument. The cross-threat-model comparison remains a valid concern (see Major weakness #1), but the claim of circularity is not supported by the paper text.
- **Various formatting/presentation nitpicks** (figure prose description, absence of table for defense numbers, section organization comments) are removed as minor or irrelevant to the paper's technical contribution.

## Novel Insights

None beyond the paper's own contributions. The input review did surface one concrete observation not fully articulated in the paper: the RMA defense results showing BadDet is more robust than BadDet+ under FT/FT-SAM create a tension with the framing of BadDet+ as a uniformly stronger attack. This is a legitimate point that the paper partially discusses but could analyze more directly.

## Suggestions

1. **Restructure the threat model discussion.** Clearly separate (a) the evaluation diagnostics (Section 3), which are threat-model-independent, from (b) the attack comparison. Flag the abstract and introduction comparisons as cross-threat-model. Consider adding a figure or table that delineates the threat model assumptions of each method side by side.

2. **Analyze, not just flag, the YOLO RMA limitation.** A brief architectural analysis (e.g., examining how YOLO's per-grid-cell classification or NMS differs from FCOS/DINO) would turn a caveat into a finding.

3. **Add error bars to the main results tables.** At minimum, standard deviations from a few repeated runs would substantially strengthen credibility. The 10-run defense infrastructure demonstrates feasibility.

4. **Bring the theoretical sketch into the main body.** If Appendix A.7 contains a substantive analysis, a one-paragraph summary (the key assumption, the subspace claim, and the conclusion) would let readers assess its value without navigating to the appendix.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>