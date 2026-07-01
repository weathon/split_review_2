## Summary

This paper diagnoses evaluation blind spots in prior object-detection backdoor work (ASR ignoring retained labels in RMA, mAP as a confounded proxy for ODA, lack of trigger scaling/placement robustness checks, and reliance on curated datasets) and proposes BadDet+, a penalty-based attack framework that augments the detector loss with a log-barrier term to suppress original-class predictions on trigger-bearing objects. The method unifies RMA and ODA under a single mechanism, introduces TDR as a complementary metric, and is evaluated across 4 architectures, 2 datasets, and physical-world transfer.

## Strengths

- **Diagnosis of evaluation flaws (Section 3) is specific and well-supported.** The identification of four concrete limitations—ASR ignoring retained labels (backdoored models produce duplicate detections under both target and original class), mAP as a confounded proxy for ODA (mAP drops from phantom boxes and localization errors rather than actual disappearance), lack of trigger scaling/placement checks, and curated dataset dependence—is backed by failure examples (Figure 1) and quantitative evidence (Tables 1-4 showing dramatic performance drops when blind spots are corrected). This is a genuine and useful service to the community.

- **The log-barrier formulation (Equations 1-2) is clean and principled.** Treating ODA as RMA toward background and suppressing the original-class logit via a soft constraint wall (unbounded penalty as σ(·)→1) is conceptually elegant. The formulation naturally handles both sigmoid-based (FCOS, YOLO, DINO) and softmax-based (Faster R-CNN) detectors through the one-vs-rest log-odds in Equation 2.

- **TDR as a complementary metric is a genuine methodological improvement.** Tables 2 and 4 cleanly expose the duplicate-detection failure mode: BadDet achieves ASR@50 >99% but TDR@50 of 75.94 (FCOS COCO) and 85.74 (Faster R-CNN MTSD), while BadDet+ suppresses TDR to single digits (2.78 and 3.18 respectively). This gap was invisible in prior ASR-only evaluations.

- **Broad evaluation scope.** Evaluation spans COCO and MTSD/PTSD, 4 architectures (FCOS, Faster R-CNN, DINO, YOLOv5m6), both fixed and random trigger placements, and physical-world transfer to PTSD—substantially exceeding prior object-detection backdoor work in breadth.

## Weaknesses

### Fatal
None.

### Major

- **Missing ablation: no baselines under the same threat model.** BadDet+ operates under a strictly stronger threat model (loss-level control, acknowledged in Section 4: "our design assumes a stronger adversarial setting in which the training process can be controlled") than the baselines it is compared against (data-poisoning-only). The paper acknowledges this distinction but does not evaluate whether simpler loss-term baselines (e.g., BadDet augmented with a cross-entropy penalty pushing triggered-object predictions toward background/target, or a margin-based hinge loss) would match BadDet+'s performance under the same threat model. Without this control, the reader cannot tell whether the advantage comes from the specific log-barrier formulation or simply from having loss-level control. The paper's "outperforming" framing (Abstract, Introduction) is factually true of the results, but the comparison conflates method quality with threat-model strength.

### Minor

- **YOLO failure case limits generality.** On YOLOv5m6 RMA (Table 4), BadDet outperforms BadDet+ in ASR@50 (96.57 vs. 91.97 Fixed) and TDR@50 (3.14 vs. 7.54 Fixed). The paper notes that "λ = 0 is optimal for this architecture," meaning BadDet+ degenerates to the standard detector loss. This is a genuine limitation for a method claiming consistent applicability; the paper acknowledges it and defers investigation to the appendix.

- **Defense evaluation is narrow.** Only FT and FT-SAM are tested (on 2–4% of clean MTSD data). Results are mixed: "For RMA, BadDet generally outperforms BadDet+ under both FT and FT-SAM" and "ASR@50 remains above 0.4 across all architectures." The paper is transparent about this scope (Section 2 line 58: "deliberately restricted to fine-tuning-style defenses"; Conclusion), but the claim in the introduction that the method "yields more robust behavior under fine-tuning-based defenses" should be read against this limited evidence.

- **Hyperparameter λ spans three orders of magnitude** (λ=1 for FCOS, Faster R-CNN, DINO; 0.001 for YOLO), suggesting architecture sensitivity. The paper references Appendix A.5 for sensitivity analysis, which cannot be evaluated in the main text.

- **The justification that "treating training as the attack surface is standard in the backdoor literature for image classification" is debatable.** Most image-classification backdoor papers assume data poisoning, not loss-manipulation. This is a minor imprecision in the threat-model motivation.

### Trivial
None.

## Nice-to-Haves

- An ablation comparing the log-barrier penalty against a simpler hinge-based or cross-entropy-based penalty under the same threat model would substantiate the claim that the specific functional form of the penalty matters.
- A basic input-level defense baseline (e.g., JPEG compression, Gaussian blur) would broaden the defense evaluation without requiring architecture-specific adaptations and would strengthen the robustness discussion.

## Removed Points

These points from the input review are excluded per the filtering rules:

1. **"Threat model mismatch invalidates 'outperforming' claims [Structural]"** — Downgraded from Fatal to Major. The paper acknowledges the threat model difference explicitly (Section 4 lines 84-88; Conclusion). Comparing across threat models is standard when a stronger threat model is motivated by demonstrated weaknesses of the weaker one. The missing ablation (same-threat-model baselines) is a real gap, but calling it "structural" or "fatal" overstates it.

2. **"Theoretical analysis referenced but not evaluable"** — Removed (hard rule: parser strips appendices from all papers). Appendix A.7 is cited for the theoretical analysis.

3. **"Align failure under scaled triggers only supported by appendix reference"** — Removed (hard rule: same rationale).

4. **"Abstract's theoretical analysis claim cannot be evaluated"** — Removed (hard rule: same rationale).

5. **"Defense evaluation is too narrow to support robustness claims [Evidential]"** — Downgraded from the reviewer's "evidential" tier to Minor. The abstract's "improved robustness to physical triggers" refers to robustness of the attack when *physical-world triggers* are used (synthetic-to-physical transfer), not robustness against defenses. The paper explicitly scopes its defense evaluation (line 58). The reviewer's claim partially rests on a misreading of the abstract.

6. **Strengths removed:** None—all four listed strengths are concrete and evidence-backed.

## Novel Insights

The reviews surface a useful observation that the paper's diagnostic contribution (Section 3) is arguably its strongest and most original part, while the method-level comparisons are weaker due to the missing same-threat-model control. An additional nuanced point: the TDR metric alone does not fully distinguish "object not detected at all" from "object detected only as target class"—the paper relies on the combination of ASR and TDR to make this distinction, which works in practice but could be made more explicit.

## Suggestions

1. Add a baseline under the same threat model: augment BadDet, UBA, or Align with a simple loss term (e.g., cross-entropy penalty pushing toward background/target) and compare against BadDet+ under matched conditions. This would disentangle whether the advantage comes from the log-barrier formulation or from loss-level control generally.
2. Clarify in the abstract and introduction that the comparative claims hold across different threat models, and position the result as "what is achievable under a stronger, justified threat model" rather than implying apples-to-apples superiority over data-poisoning-only approaches.
3. Add at least one simple input-level defense (e.g., JPEG compression) to broaden the defense evaluation beyond fine-tuning.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>