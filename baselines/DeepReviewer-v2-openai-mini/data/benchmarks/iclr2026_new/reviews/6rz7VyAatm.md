## Summary
# Final Review Report

## Summary

This paper addresses the underexplored problem of backdoor attacks in object detection. The authors make three main contributions: (1) a systematic diagnosis of evaluation blind spots in prior object-detection backdoor work (ASR ignoring retained labels in RMA, mAP confounds in ODA, missing trigger-scale/position robustness checks, and dependence on curated datasets); (2) a disciplined evaluation protocol introducing the True Detection Rate (TDR) metric that captures label-replacement fidelity; and (3) BadDet+, a unified log-barrier penalty framework that handles both Region Misclassification Attacks (RMA) and Object Disappearing Attacks (ODA) by suppressing true-class predictions on trigger-bearing objects during training. The method assumes a stronger threat model (training-time loss manipulation) than standard data poisoning, justified by empirical evidence that data-poisoning-only approaches are unreliable for consistent backdoor implantation in object detectors. Experiments across COCO, MTSD, and the physical-world PTSD benchmark demonstrate that BadDet+ achieves high ASR@50 with low TDR@50 while maintaining clean mAP.

The paper has genuine strengths: the diagnostic analysis of evaluation pitfalls is thorough and practically valuable, the TDR metric fills a real gap, and the empirical demonstration that data-poisoning alone is insufficient provides a principled justification for stronger threat models. However, significant concerns include: the unverifiable theoretical claim in the abstract (appendix removed), missing normalization details and threshold mapping in the penalty formulation, an asymmetric comparison between training-control and data-poisoning methods, and interpretation errors in the poisoning-ratio analysis. External novelty verification is deferred due to retrieval unavailability in this run.

## Strengths
**S1. Systematic diagnosis of evaluation blind spots.** The paper identifies four concrete, well-articulated weaknesses in prior object-detection backdoor evaluations: ASR fails to capture duplicate detections in RMA, mAP is a poor proxy for ODA success, trigger-scale/position robustness is neglected, and dependence on curated datasets limits real-world applicability. This diagnostic contribution is independent of the proposed method and is valuable for the community regardless of whether BadDet+ is adopted.

**S2. Introduction of TDR metric.** True Detection Rate (TDR) is a simple but effective complement to ASR that directly quantifies whether an RMA attack actually replaces the original label or merely adds a target-class detection atop it. The metric fills a genuine measurement gap and is likely to be adopted in future object-detection backdoor research.

**S3. Principled empirical justification for stronger threat model.** Through systematic poisoning-ratio experiments (Fig. 3), the paper shows that data-poisoning-only methods either fail to achieve consistent backdoor behavior or degrade clean mAP unacceptably. This evidence directly motivates why training-time loss manipulation is warranted for reliable backdoor implantation — an argument that goes beyond mere assumption and is grounded in empirical data.

**S4. Comprehensive evaluation across diverse settings.** The experiments cover two datasets (COCO, MTSD), four architectures (FCOS, Faster R-CNN, DINO, YOLOv5), multiple trigger positions and scales, and physical-world transfer (PTSD). This breadth strengthens the generality of the findings and reveals architecture-specific behaviors (e.g., YOLO's different response to λ).

**S5. Honest limitation discussion.** The conclusion openly acknowledges scenarios where BadDet may be preferred over BadDet+, the restriction to RMA/ODA (excluding OGA), the stronger threat model assumption, and the narrow defense evaluation scope. This transparency improves the paper's scientific credibility.

**S6. Unified formulation insight.** The observation that ODA can be treated as a special case of RMA (with background as target class) is conceptually elegant and leads to a single mechanism that handles both attack types without separate branches. The design rationale (Section 4, Design rationale) is clearly explained before the formal definition, following good expository practice.

## Weaknesses
### W1. Unverifiable theoretical claim (Major, Severity: High)

**Evidence:** Page 1 - Abstract claims "a theoretical analysis showing that the proposed penalty acts selectively within a trigger-specific feature subspace, reliably inducing backdoor behavior without degrading normal predictions."

**Impact:** The appendix containing this analysis (Appendix A.7) is explicitly marked as removed ("Rest of paper (reference and Appendix) is removed"). This means the claimed theoretical analysis is entirely unverifiable by reviewers. A theoretical claim about feature-subspace selectivity is a strong assertion that requires proof steps, assumptions, and boundary conditions to be evaluated. Without access to this content, the abstract overstates the paper's contribution.

**Repair:** Either (a) include the full theoretical analysis in the main submission, or (b) remove the claim from the abstract and replace with a more modest statement such as "We provide a formal characterization of the penalty's optimization behavior in the appendix."

### W2. Missing normalization and threshold mapping in penalty formulation (Major, Severity: High)

**Evidence:** Page 4-5 - Section 4.1, Equations (1)-(2). The penalty $\mathcal{P}_{\text{atk}}$ is an unnormalized sum over all valid (i,j) prediction-ground-truth pairs.

**Issue:** In dense detectors (FCOS, YOLO), the number of predictions $\hat{N}$ can exceed $10^4$ per image. Without normalization (e.g., dividing by the number of valid pairs or batch size), the penalty magnitude scales with image complexity and batch composition, making $\lambda$ non-transferable across datasets. Additionally, the softmax-compatible formulation (Eq. 2) introduces a new threshold $\tau'$ without specifying how it relates to $\tau$ in the sigmoid case. Since $s_{j,y_i}$ (one-vs-rest log-odds) has a fundamentally different range from $z_{j,y_i}$ (raw logits), $\tau'$ cannot equal $\tau$, yet the paper does not specify the relationship or report the value used.

**Repair:** (Must) Add normalization factor $1/|S|$ where $S$ is the set of valid (i,j) pairs. (Must) Specify how $\tau'$ is chosen, e.g., $\tau' = \tau - \log(C-1)$ to approximately match the effective probability threshold. (Nice-to-have) Report $\tau'$ values used in experiments.

### W3. Asymmetric comparison confound (Major, Severity: High)

**Evidence:** Page 1 - Abstract claims "outperforming existing RMA and ODA baselines." Page 4 - Threat model paragraph states BadDet+ assumes "training-time loss manipulation."

**Issue:** BadDet+ operates under a fundamentally stronger threat model (training-process control) than the data-poisoning-only baselines (BadDet, UBA, Align). The comparison is therefore asymmetric: BadDet+ has access to a strictly larger attack surface. The paper acknowledges this asymmetry in the threat model paragraph but does not control for it in the experimental comparisons or the abstract. The claimed "outperformance" conflates the advantage of having a stronger attack budget with genuine algorithmic superiority. A fairer comparison would include a baseline where data-poisoning methods are also given access to training loss manipulation (e.g., using the same log-barrier penalty but without the RMA/ODA unification insight).

**Repair:** (Must) Explicitly acknowledge the asymmetric comparison in the abstract and conclusion. (Nice-to-have) Include an ablation where the log-barrier penalty is applied to a data-poisoning-only pipeline without the unified formulation, to isolate the benefit of the penalty mechanism from the benefit of the stronger threat model.

### W4. TDR confidence-threshold dependency (Major, Severity: Medium)

**Evidence:** Page 5 - Section 5.2, TDR definition: "proportion of poisoned objects for which the original class $y_i$ is still detected."

**Issue:** TDR depends on the detection confidence threshold, but the paper does not specify the threshold used to consider a detection as "detected." Different detectors have different default confidence thresholds (e.g., 0.05 for FCOS, 0.005 for YOLO, 0.0 for Faster R-CNN with NMS). If a low threshold is used, many low-confidence duplicate detections are counted, inflating TDR. If a high threshold is used, a genuinely unsuccessful attack might show low TDR simply because the original-class confidence is below threshold but still present. Without specifying this threshold, TDR values across different detectors may not be comparable.

**Repair:** (Must) Report the confidence threshold used for TDR computation. (Must) Analyze sensitivity of TDR to confidence threshold choice (or reference Appendix A.2.1 if this analysis exists there).

### W5. Interpretation error in poisoning-ratio analysis (Major, Severity: High)

**Evidence:** Page 9 - Section 5.3, Poisoning Ratio paragraph: "BadDet+... yields a more stable cluster in the top-right region of the RMA plots, sustaining high TDR@50 and mAP ratio."

**Issue:** TDR@50 measures the proportion of poisoned objects still detected under their original class. For an attack, **lower** TDR@50 is better (indicating successful label replacement). The text describes "high TDR@50" as desirable, which is internally inconsistent. The ideal region for RMA plots should be top-left (high mAP ratio, low TDR@50), not top-right. This error could mislead readers about the relative performance of methods. The Fig. 3 caption describes the x-axis as TDR@50 for RMA methods, confirming the axis orientation.

**Repair:** (Must) Correct the text to state "low TDR@50" for the ideal region and adjust the directional description of the plots accordingly.

### W6. Related work is a chronological list rather than thematic comparison (Minor, Severity: Medium)

**Evidence:** Pages 1-2 - Section 2.1 Backdoor Attacks and 2.2 Backdoor Defense.

**Issue:** The related work section reads as a paper-by-paper chronological summary ("BadDet is the seminal work...", "Building on BadDet, Luo et al. extend...", "Cheng et al. further demonstrate..."). It does not organize prior work by comparison axes (e.g., threat-model strength, attack objective, evaluation methodology). This makes it harder for readers to understand where BadDet+ fits in the landscape and what the key differentiating dimensions are. The defense section is better organized but still relatively shallow.

**Repair:** Restructure around 2-3 thematic axes: (a) threat-model assumptions (data-poisoning vs training-control), (b) attack objectives (RMA/ODA/OGA), (c) evaluation rigor (metrics used, robustness checks). For each axis, state what prior work does and how BadDet+ differs.

### W7. Defense evaluation scope is narrow (Minor, Severity: Medium)

**Evidence:** Page 9 - Defense evaluation paragraph. Only 2-4% clean data (50-100 samples) used for fine-tuning.

**Issue:** The defense evaluation uses very little clean data for fine-tuning, which makes the defense weak by design. While the authors explicitly acknowledge this scope limitation, the claim "BadDet+ sustains strong performance after both FT and FT-SAM" should be qualified as "against weak defenses with severely limited clean data." Additionally, the asymmetric finding (BadDet+ ODA robust under FT, but BadDet+ RMA less robust than BadDet) is reported without mechanistic explanation.

**Repair:** (Must) Add mechanism hypothesis for asymmetric ODA vs RMA robustness (e.g., ODA enforces hard background constraint harder to override). (Nice-to-have) Include one experiment with more realistic defense data (e.g., 20% clean data) to test whether the pattern holds.

### W8. Introduction narrative is generic (Minor, Severity: Low)

**Evidence:** Pages 0-1 - Introduction paragraphs 1-3.

**Issue:** The first two paragraphs cover general deep-learning security and standard classification backdoors — well-known background that could be condensed. The paper's specific problem focus (object detection backdoors) only emerges in paragraph 3. Losing the first paragraph and half of the second would not affect the technical contribution. A tighter introduction would open directly with the underexplored threat in object detection and the unique challenges it poses.

**Repair:** Condense paragraphs 1-2 into one short paragraph that directly transitions from "deep learning security concerns" to "backdoor attacks in object detection are especially concerning because..."

### W9. Novelty/comparison verification deferred (Info, Severity: Low)

**Evidence:** External literature search was disabled for this review run due to API token unavailability.

**Issue:** Key novelty and state-of-the-art comparison claims — such as "position- and scale-invariant behavior," "improved robustness to physical triggers," and "stronger synthetic-to-physical transfer than prior work" — could not be independently verified against the literature. While the empirical results appear internally consistent, the relative positioning against related work requires manual verification by the authors and reviewers.

**Repair:** Authors should provide a more detailed comparison table with relevant prior work, explicitly stating what is novel in BadDet+ versus each baseline along each claimed dimension.

## Score
**Final Score: 5.5/10**

**Scoring rationale:**
This paper has genuine scientific value through its systematic diagnosis of evaluation blind spots in object-detection backdoor research and the introduction of the TDR metric. The empirical demonstration that data-poisoning-only approaches are unreliable provides a principled justification for exploring stronger threat models. The evaluation breadth across datasets and architectures is commendable.

However, several significant issues prevent a higher score. The unverifiable theoretical claim in the abstract (appendix removed) weakens the paper's credibility. The penalty formulation lacks critical details (normalization, threshold mapping) that affect reproducibility. The asymmetric comparison between training-control and data-poisoning methods is not adequately controlled. The interpretation error in the poisoning-ratio analysis (W5) indicates a lapse in data analysis rigor. External novelty verification could not be performed in this review run.

The paper's strongest contribution is the diagnostic analysis and evaluation protocol, not the technical novelty of BadDet+ itself. The core idea — a log-barrier penalty to suppress true-class predictions — is conceptually straightforward, and the unification insight (ODA as special case of RMA with background class) is elegant but incremental. With major revisions addressing the formulation details, interpretation errors, and claim scope, the paper could potentially reach 7/10.

**Summary judgment:** Publishable after major revision. The diagnostic contributions and TDR metric are valuable enough to warrant publication, but the technical presentation of BadDet+ needs significant improvement in clarity, completeness, and honest claim-scoping before the paper is ready for acceptance.