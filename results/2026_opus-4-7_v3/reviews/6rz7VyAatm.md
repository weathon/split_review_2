Now I have read the full paper. Let me verify some specific claims more carefully before drafting.Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me begin calibration. Round 1 — Bracketing across score bands:Let me read the most relevant anchor papers for comparison:Based on my reading of the anchors, I can form the initial bracket. Let me now read one more anchor in the 5.5-6.5 range for closer comparison:Now I have sufficient information to finalize my review. Let me compile the final consolidated review.

---

## Summary
BadDet+ proposes a penalty-based backdoor attack framework for object detection that unifies region misclassification (RMA) and object disappearance (ODA) under a single log-barrier mechanism. The paper first diagnoses concrete evaluation blind spots in prior OD backdoor work (Section 3), introduces the True Detection Rate (TDR) metric to capture dual-detection failures missed by ASR, and demonstrates that BadDet+ achieves stronger and more consistent attack performance across COCO, MTSD, and physical-world PTSD datasets on 3 of 4 tested architectures.

## Strengths
- **Diagnostic critique of prior evaluation protocols (Section 3) is the paper's strongest and most original contribution.** The identification of specific, verifiable failure modes — dual detections in RMA inflating ASR (Figure 1a), mAP confounding true disappearance in ODA (Figures 1b–1c), and trigger scale sensitivity in Align — is concrete, demonstrated with failure-case images, and confirmed by Tables 1–4 showing existing methods achieve much lower ASR@50 under corrected protocols than prior reports suggested.

- **TDR metric fills a genuine evaluation gap.** Table 2 makes this vivid: BadDet achieves 99.45 ASR@50 on FCOS but retains 75.94 TDR@50, meaning the correct detection persists in ~76% of cases. Without TDR, this attack would be reported as near-perfect. This metric is useful beyond this specific paper.

- **Conceptually clean unification of RMA and ODA.** The insight that ODA is RMA-to-background, combined with the observation that the key failure is insufficient suppression of the original-class logit, leads naturally to the log-barrier formulation. Equations 1–2 demonstrate architectural awareness by handling sigmoid-based and softmax-based detectors separately.

- **Evaluation breadth is substantial and principled.** Four architectures (FCOS, Faster RCNN, DINO, YOLOv5), two datasets plus physical-world validation (PTSD), fixed vs. random trigger placement, poisoning ratio analysis (Figure 3), and principled baseline variants (UBA Box, Align Random) to test whether simple fixes to prior methods resolve the identified problems. The per-object evaluation protocol (Section 5.2) is more rigorous than prior work.

## Weaknesses

### Fatal
None

### Major
- **Threat model asymmetry confounds the central comparison.** BadDet+ modifies the training loss (Equations 1–2, with λ > 0), while baselines (BadDet, UBA, Align, Morph) only modify training data. The paper acknowledges this stronger threat model (Section 4, "Threat Model" paragraph) and argues it is realistic and standard in classification backdoor literature. However, the headline comparisons in Tables 1–4 conflate two effects: (i) the log-barrier penalty is a better mechanism, and (ii) loss-level access is a more powerful attack surface. The poisoning ratio analysis (Figure 3) partially addresses this by showing data-poisoning alone fails at high ratios, and the YOLO case implicitly provides a λ=0 data point. However, a systematic ablation of λ=0 vs. λ>0 across all four architectures — which would directly isolate the penalty's marginal contribution — is absent, leaving the relative importance of these two effects unquantified.

- **Method fails on YOLOv5 for RMA.** Table 4 shows BadDet outperforms BadDet+ on every RMA metric for YOLOv5: ASR@50 96.57 vs. 91.97 (Fixed), TDR@50 3.14 vs. 7.54 (Fixed). The paper acknowledges "λ=0 is optimal for this architecture" (Section 5.3), meaning the proposed penalty provides zero benefit on this architecture. YOLOv5 is arguably the most practically deployed architecture among those tested. The main text defers explanation to Appendix A.8 without providing a mechanistic account of *why* the penalty interferes with YOLO's architecture (e.g., its separate objectness and class prediction heads).

### Minor
- **Physical-world TDR degradation partially resurfaces the dual-detection problem.** For RMA on PTSD (Table 4), BadDet+ TDR@50 jumps from 6.75 (MTSD Fixed, FCOS) to 44.41 (PTSD Fixed, FCOS), meaning the dual-detection problem the method was designed to solve partially returns in physical settings. While BadDet+ still outperforms baselines, the abstract's claim of "stronger synthetic-to-physical transfer" would benefit from more transparent discussion of absolute degradation, not just relative improvement.

- **Architecture-specific λ tuning weakens the "single mechanism" narrative.** λ=1 for three architectures and λ=0.001 for YOLOv5 (a 1000× difference, Section 5.1) suggests the penalty's behavior is not architecture-agnostic as the unified formulation implies.

- **Per-object evaluation protocol makes comparison attribution difficult.** The paper evaluates each poisonable object independently ("for every object, we create a separate test instance in which only that object is poisoned," Section 5.2). While more principled than prior protocols, this methodological change makes it difficult to attribute how much of baselines' poor performance reflects the stricter evaluation vs. genuine attack weakness. The paper would benefit from a clearer quantification of this decomposition.

### Trivial
None

## Nice-to-Haves
- A mechanistic explanation of why the penalty interacts poorly with YOLOv5's objectness-confidence architecture would turn a weakness into an architectural insight and could point toward a fix.
- Analysis of *why* TDR increases on PTSD (trigger fidelity, viewpoint variation, or lighting?) would make the physical-world evaluation genuinely informative rather than a pass/fail benchmark.
- Broader defense evaluation (pruning, Neural Cleanse, STRIP, test-time detectors) — explicitly scoped out in Section 2.2, so not a core flaw — would strengthen the robustness claims.
- Stating the main theoretical result from Appendix A.7 in the main body (at least the statement and key assumptions) would help readers assess the "trigger-specific feature subspace" claim.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Section 3's fourth limitation is overstated as a general problem"** — The paper actually writes "some approaches require curated auxiliary datasets" and specifically names Morph (Section 3). It is not framed as a general claim about all prior work.

- **"Theoretical analysis advertised in abstract but absent from main text"** — The paper provides design rationale and intuition in Section 4 and defers formal analysis to Appendix A.7, which was stripped by the parser. The main text states the key intuition; this is a standard paper organization choice. Removed per the rule about missing appendix content.

- **"Threshold τ not discussed in main text"** — Sensitivity analysis is in Appendix A.5 (stripped by parser). Standard practice to defer hyperparameter sensitivity to supplementary material. Removed per appendix rule.

- **"The argument that data poisoning is insufficient is circular"** — The paper provides empirical evidence (Figure 3) showing that increasing poisoning ratios across multiple architectures and methods fails to reliably implant strong backdoors. This is an empirical demonstration, not purely circular reasoning.

- **"Defense evaluation is thin"** — The paper explicitly scopes this out in Section 2.2 and acknowledges it in the conclusion. An attack paper evaluating two fine-tuning defenses at two data budgets across multiple architectures is reasonable for its stated scope.

- **"Dense scenes concern for Equation 1"** — The paper acknowledges computational analysis in Appendix A.6 (stripped). Without evidence this is a practical issue in the experiments, this is speculative.

## Novel Insights
The paper's most novel insight is that existing OD backdoor evaluations systematically overstate attack success by ignoring dual detections (captured by the new TDR metric) and conflating mAP degradation with true object disappearance. The TDR metric is a genuinely useful contribution applicable beyond this specific paper. The observation that ODA is a special case of RMA-to-background under modern detector architectures provides a clean unifying perspective. The poisoning-ratio analysis (Figure 3) yields the practical insight that for object detection, unlike classification, simply increasing the poisoning ratio is insufficient to overcome data-poisoning-only limitations.

## Suggestions
- Provide a systematic λ=0 vs. λ>0 ablation across all four architectures to cleanly disentangle the penalty's marginal contribution from the threat model advantage. This is the single highest-leverage improvement.
- Add a mechanistic explanation for the YOLOv5 failure to the main text (e.g., interaction with YOLO's separate objectness and class prediction heads).
- Discuss physical-world TDR degradation more transparently, with analysis of contributing factors (trigger fidelity, viewpoint, lighting).
- State the main theoretical result from Appendix A.7 in Section 4, even if the proof is deferred.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to BadDet+ |
|-------|------|-----------|-------|-----------------------|
| LeBD (OD backdoor defense) | 7vKWg2Vdrs | 3.25 | 1 | Much weaker: limited to single architecture (YOLO), limited novelty (GradCAM→LayerCAM extension). BadDet+ has broader scope and more original contributions. |
| Certified Copy (backdoor attack) | 66e22qCU5i | 3.00 | 1 | Weaker: novelty concerns about cost function approach. BadDet+ has stronger diagnostic contribution and broader evaluation. |
| Deferred Backdoor | S5JCqTJyKj | 3.00 | 1 | Weaker: limited evaluation, less mature methodology. BadDet+ is more rigorous. |
| Adversarial Instance Attacks | zQXX3ZV2HE | 3.00 | 1 | Different focus (scene interaction attacks). Weaker methodology and evaluation. |
| VSSC trigger (physical backdoor) | H6XiAoyugv | 4.33 | 1 | Weaker: results don't convincingly beat baselines per reviewers. BadDet+ has clearer improvements on 3/4 architectures. |
| Backdoor in Seconds | ZyPRwskBli | 4.75 | 1 | Similar tier but different domain (pre-trained models). BadDet+ has more original diagnostic contributions. |
| AnyDoor (test-time backdoor) | 9Orm76dUuT | 4.50 | 1 | Different threat model. Similar quality concerns about practical impact. |
| Learnable Invisible Backdoor | scFfMOOGD8 | 4.25 | 1 | Diffusion model backdoor. BadDet+ has stronger evaluation breadth. |
| Efficient Backdoor (data-constrained) | vRyp2dhEQp | 5.75 | 1 | Accepted but with novelty concerns (one reviewer: 3). BadDet+ has more original diagnostic contributions and broader evaluation. |
| Less is More (clean-image backdoor) | LsTIW9VAF7 | 5.80 | 1 | Rejected despite similar score range. Comparable quality but different focus. |
| Wicked Oddities (selective poisoning) | 1Z3C49JQVf | 6.00 | 1 | Accepted. Novel threat model but limited datasets (CIFAR-10, GTSRB). BadDet+ has broader evaluation, more original diagnostic contributions, but confounded comparison is a bigger weakness. |
| VLOOD (VLM backdoor) | tZozeR3VV7 | 6.33 | 1 | Accepted. Practical OOD scenario. Similar overall quality; BadDet+ has stronger diagnostic contribution, VLOOD has cleaner threat model alignment. |
| Dataset Bias | SctfBCLmWo | 8.00 | 1 | Clearly stronger paper with novel surprising findings. BadDet+ is not at this level. |
| MOS (3D OD adaptation) | Y6aHdDNQYD | 8.00 | 1 | Clearly stronger: novel, well-received. BadDet+ is below this tier. |
| Balancing ReID | 5lUdTogEL3 | 1.00 | 1 | Much weaker. Not comparable. |
| NEMESIS jailbreaking | 5kMwiMnUip | 1.40 | 1 | Much weaker. Not comparable. |

**Round 1 bracket: 5.5 to 7.0**

BadDet+ is clearly above the 3–5 range rejected papers — it has genuine, well-documented contributions (diagnostic analysis, TDR metric, principled method). It is competitive with the accepted papers in the 5.75–6.33 range, which have similar levels of real contribution tempered by clear weaknesses. The confounded comparison and YOLOv5 failure are meaningful concerns but do not invalidate the contribution. The diagnostic analysis (Section 3) and TDR metric would stand as contributions on their own, and the method works well on 3 of 4 architectures.

**Final score: 6.0** — The paper makes genuine, well-evidenced contributions to an understudied problem. The diagnostic critique and TDR metric are the strongest parts and are independently valuable. The method is principled and effective on most architectures. The confounded comparison due to threat model asymmetry and the YOLOv5 failure are real Major weaknesses that prevent a stronger score, but neither invalidates the contribution. The paper is above average for the backdoor attack subfield and comparable to accepted papers in the 5.75–6.33 range.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>