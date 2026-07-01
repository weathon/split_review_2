## Summary

This paper makes two main contributions: (1) it diagnoses evaluation blind spots in prior object detection backdoor research—specifically that ASR overstates RMA success by ignoring retained duplicate detections, and that mAP is a poor proxy for ODA effectiveness—and (2) it proposes BadDet+, a unified attack framework that augments the detector loss with a log-barrier penalty to suppress true-class predictions on trigger-bearing objects. BadDet+ operates under a stronger threat model (training-time loss manipulation) than prior data-poisoning-only attacks. It is evaluated across COCO and MTSD/PTSD (physical-world transfer) on four architectures (FCOS, Faster RCNN, DINO, YOLOv5m6) and two attack types (RMA and ODA).

## Strengths

1. **Concrete diagnosis of evaluation blind spots (Section 3).** The paper makes a well-documented, example-illustrated case that existing RMA evaluations rely on ASR while ignoring "retained labels" (duplicate detections where the original class survives alongside the target class), and that ODA evaluations using mAP as a proxy can be depressed by localization artifacts and phantom boxes rather than genuine disappearance. The introduction of TDR (True Detection Rate) as a complementary metric operationalizes this critique into a measurable quantity.

2. **Physical-world validation (MTSD → PTSD).** Evaluating on the real-world PTSD traffic-sign dataset provides meaningful evidence of synthetic-to-physical transfer. BadDet+ maintains substantially higher ASR on PTSD than baselines (Tables 3 and 4), demonstrating that the attack transfers beyond the lab setting—a step beyond prior work (including BadDet, UBA, Align) that evaluates only on synthetic test splits.

3. **Comprehensive experimental scope.** Evaluation spans two datasets (COCO, MTSD/PTSD), four detector architectures (FCOS, Faster RCNN, DINO, YOLOv5m6), multiple trigger positions (fixed high/low/both and random), and two attack types (RMA and ODA). This breadth makes results harder to dismiss as architecture- or dataset-specific artifacts.

4. **Principled formulation.** The log-barrier penalty (Eq. 1/2) is mathematically clean: it activates only when the original-class logit exceeds a threshold τ and imposes an unbounded penalty as σ(·)→1. The unification of RMA and ODA by treating background as a target class is conceptually elegant rather than ad-hoc.

## Weaknesses

### Fatal
None.

### Major

1. **Threat-model asymmetry in head-to-head comparisons.** BadDet+ operates under a strictly stronger threat model (training-time loss manipulation) than the baselines it is compared against (pure data poisoning). The paper is transparent about this (lines 84–88, 262), but the narrative throughout—"outperforming existing RMA and ODA baselines" (abstract), "yields more robust behavior compared to existing object-detection backdoor attacks" (line 36)—presents the comparison as if the attacks were operating under equal capabilities. Fig. 3 compounds this: it shows that increasing the poisoning ratio of prior data-poisoning methods still fails, while BadDet+ has the additional lever of loss manipulation, so the comparison is not controlled. The paper lacks an ablation that isolates BadDet+ under the weaker threat model (data poisoning only, without the loss penalty) to separate whether improvement comes from the penalty's specific form or simply from having more control over training. This does not invalidate the method—the stronger threat model is realistic—but it means the headline performance comparisons conflate a capability advantage with an algorithmic one.

2. **Missing controlled ablation of the log-barrier penalty form.** The paper's core algorithmic claim is that the log-barrier penalty is better than prior data-poisoning approaches. But the comparison conflates two variables: (a) the specific mathematical form of the penalty, and (b) the fact that the penalty is applied via loss modification rather than through data. To isolate (a), the paper would need to compare the log-barrier penalty against alternative loss-level penalties (e.g., a margin-based hinge loss, direct logit subtraction, or an MSE penalty pushing the logit below τ). Without this, we cannot tell whether the improvement comes from the log-barrier shape or simply from *any* direct loss manipulation—which would be a much weaker claim.

3. **BadDet+ is not consistently better than BadDet—YOLO failure case and weaker defense robustness.** (a) On YOLOv5 for RMA (Table 4), BadDet achieves higher ASR@50 (96.57 vs. 91.97) and lower TDR@50 (3.14 vs. 7.54) than BadDet+, and the paper concedes "λ = 0 is optimal for this architecture" (line 222)—meaning the penalty actively harms performance on a widely deployed detector. (b) Under fine-tuning defenses (Fig. 2), "For RMA, BadDet generally outperforms BadDet+ under both FT and FT-SAM" (line 256). These two findings substantially narrow the settings where BadDet+ is advantageous and are acknowledged but not analyzed in depth.

### Minor

1. **Unprincipled λ selection across architectures.** The penalty weight λ is set to 1 for FCOS, Faster RCNN, and DINO but 0.001 for YOLO—a 1000× difference—and is chosen "to balance mAP and ASR@50/TDR@50" (line 131). This is a post-hoc selection criterion that could introduce selection bias. For YOLO, λ=0.001 is described as effectively no penalty, suggesting the log-barrier interacts poorly with dense prediction heads. Without a principled rule, applying BadDet+ to a new architecture requires extensive per-architecture grid search.

2. **Substantial synthetic-to-physical performance drop without discussion.** BadDet+ ODA on FCOS drops from MTSD Fixed ASR@50 = 93.77 to PTSD Fixed ASR@50 = 59.59 (Table 3), a 34+ point gap. While PTSD results are still much better than baselines, the magnitude of this drop—which somewhat qualifies the abstract's "position- and scale-invariant behavior" claim—is not discussed in the paper.

3. **Statistical variance not reported for main results.** The defense evaluation (Fig. 2) uses 10 runs with box plots, which is good practice. But the main results (Tables 1–4) report single numbers with no indication of variance across training runs or data splits. Given that the paper critiques prior work for unreliable evaluation, reporting variance would strengthen its own claims.

### Trivial
None.

## Nice-to-Haves

- Add an "equal-capability" ablation where BadDet+ is trained with only data poisoning (removing the loss penalty) to isolate whether improvement comes from the penalty's form or from the stronger threat model.
- Compare the log-barrier penalty against alternative loss-level penalties (e.g., hinge-based suppression, direct logit subtraction) to validate the specific design choice.
- Discuss why YOLO behaves differently under the log-barrier penalty (e.g., interaction with dense prediction heads) to provide architectural insight rather than treating it as an afterthought.
- Comment on the MTSD→PTSD performance drop to clarify the practical limits of the method's position/scale invariance.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"ASR numbers for baselines were measured under this paper's protocol, not under original papers' protocols"** — The paper clearly explains its evaluation protocol in Section 5.2 (independent object-wise evaluation). This is a reasonable methodological decision for fair comparison under a unified protocol, not a weakness.
- **"The mAP-as-ODA-proxy issue was already acknowledged by BadDet authors"** — Cannot be verified without the BadDet paper; the paper's systematization of *multiple* blind spots (retained labels, mAP confounds, trigger scaling/placement, dataset dependencies) is a contribution regardless of partial prior awareness of individual points.
- **"Alternative triggers not discussed in main text"** — The paper references Appendix A.4 for alternative trigger results; the appendix exists in the original submission but is stripped by the parser, making this criticism unverifiable.
- **"Reproducibility of λ selection"** — Appendix A.5 (also parser-stripped) addresses λ sensitivity; the remaining concern about post-hoc selection is folded into Minor Weakness #1 above.

## Novel Insights

The harsh critic's observation that the paper's diagnostic contributions (Section 3) may ultimately be more impactful than the BadDet+ method itself is a useful reframing: the paper could be restructured so that the improved evaluation protocol (TDR, object-level ASR, trigger scaling/placement robustness checks) is positioned as the primary contribution, with BadDet+ as a case study demonstrating why the protocol matters. This structural suggestion is not present in the paper and is worth the authors' consideration.

## Suggestions

- Restructure the paper to more clearly separate the evaluation-protocol contribution (Section 3) from the method contribution (BadDet+). The protocol can be applied to any attack regardless of threat model, which would also resolve the threat-model asymmetry concern in the narrative.
- Add the missing ablation experiments (data-poisoning-only BadDet+, alternative loss-level penalties) to strengthen empirical support for the specific design choices.
- Discuss the YOLO failure case and defense-robustness findings as meaningful scientific results about how different detection paradigms interact with loss-level backdooring, rather than treating them as limitations to be glossed over.
- Report variance across multiple seeds for main-table results.

## Score and Decision

**Calibration anchors** (all retrieved from the backdoor-attack literature within the deepreview_13k_calibration set):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| `5lUdTogEL3.md` (L-ReID) | 1.00 | R1, band <1.5 | Irrelevant topic; outlier anchor only |
| `7vKWg2Vdrs.md` (LeBD YOLO defense) | 3.25 | R1, band 1.5–3.5 | Much weaker technical depth and scope; our paper is clearly above this |
| `ZyPRwskBli.md` (Backdoor in Seconds) | 4.75 | R1, band 3.5–5.5 | Comparable threat-model concerns but narrower evaluation; our paper is stronger |
| `Ud7I21wHnl.md` (CLIP backdoor analysis) | 5.25 | R1, band 3.5–5.5 | Analysis-only paper with limited novelty; our paper has a concrete method + evaluation |
| `vRyp2dhEQp.md` (Efficient Backdoor Attacks) | 5.75 | R2, band 5.5–7.5 | Practical threat model contribution; similar profile but our paper has more thorough evaluation |
| `tZozeR3VV7.md` (VLOOD) | 6.33 | R1, band 5.5–7.5 | Strong paper with similar issues (loss justification gap); our paper is comparably positioned |
| `s56xikpD92.md` (BaDExpert) | 6.25 | R2, band 5.5–7.5 | Defense paper with thorough evaluation; similar rigor level |
| `1Z3C49JQVf.md` (Wicked Oddities) | 6.00 | R2, band 5.5–7.5 | Practical threat model, limited dataset scope; our paper has broader evaluation |
| `BPHcEpGvF8.md` (Demystifying Backdoor) | 5.75 | R2, band 5.5–7.5 | Theoretical paper with split reviews; different contribution type |
| `KmQEsIfhr9.md` (Detecting Backdoor in CLIP) | 6.00 | R1, band 5.5–7.5 | Detection paper with specific focus; comparable rigor |

**Bracket reasoning:** Round 1 bracketing placed the paper between 4 and 7. The paper is clearly above the 3.25 anchor (LeBD, which has limited technical contribution and narrow scope). It is stronger than the 4.75–5.25 papers (Backdoor in Seconds, CLIP analysis) because it includes both diagnostic insights and a concrete method with comprehensive physical-world evaluation. The closest peers are the 5.75–6.33 papers (VLOOD, Wicked Oddities, BaDExpert, Efficient Backdoor Attacks), which are accepted papers with clear contributions but also identifiable methodological weaknesses. Our paper's diagnostic contributions and evaluation thoroughness place it in the upper half of this band, but the threat-model asymmetry and missing ablations keep it from reaching the 7+ range.

**Final score:** 6.5 — a solid paper with genuine contributions (diagnosis of evaluation blind spots, principled unified attack formulation, thorough physical-world validation) that is nevertheless held back by a structural issue in how its evaluation narrative handles the stronger threat model, and by the absence of key ablations that would isolate the specific contribution of the log-barrier penalty form.

**MY FINAL SCORE:** <score>6.5</score>
**MY FINAL DECISION:** <decision>Accept</decision>