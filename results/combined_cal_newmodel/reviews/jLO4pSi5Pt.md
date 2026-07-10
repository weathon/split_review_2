## Summary

This paper addresses a genuinely novel problem — Test-Time Adaptation (TTA) for Vision-Language Models (VLMs) under long-tailed test distributions, where head classes dominate tail classes. The authors propose L-TTA, a system with three co-designed components: Synergistic Prototypes (SyPs) with Deterministic and Exclusionary Prototypes to enrich tail-class representations, Rebalancing Shortcuts (RSs) with a class re-allocation (CRA) loss for dynamic rebalancing, and Balanced Entropy Minimization (BEM) — a modified entropy loss that down-weights confident head-class predictions via a confidence-weighted class prior penalty. The evaluation spans 15 datasets across three benchmarks, three imbalance ratios, five backbones, and 12+ baselines, with consistent improvements reported.

## Strengths

- **Well-motivated problem formulation with grounded failure-mode analysis.** The paper identifies two specific failure modes — Text-induced Tail Erosion (pre-training text priors interact with long-tailed class distributions) and Modality-bias Amplification (unimodal TTA methods harm the multi-modal manifold) — that are testable claims connecting VLM architecture to the long-tailed setting. This is a genuine gap, as existing VLM TTA methods assume balanced test distributions.
- **Extensive and well-structured evaluation.** 15 datasets organized into OOD, Cross-Domain, and Corruption benchmarks; three imbalance ratios (10, 20, 50); five backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG); 12+ baselines. Including macro-F1 alongside accuracy is appropriate for the paper's central concern. The efficiency analysis (Table 4) shows L-TTA is competitive with lightweight methods (1.45h, 1.89G) while outperforming them.
- **The BEM formulation is principled.** The penalized entropy formulation \(z' = z - (1 - \tilde{\mathbb{P}})^\beta\log(\pi)\) has a clear rationale: the \((1 - \tilde{\mathbb{P}})^\beta\) term down-weights the logit adjustment for confident (head-class) predictions, so BEM primarily guides tail-class and uncertain samples. The ablation on \(\beta\) (Figure 4d) shows a sensible U-shaped curve.
- **Robustness analysis to dynamic head/tail class shifts** (Table 7) shows stable performance across different sample orderings — a thoughtful experiment that addresses a practical concern for streaming TTA.

## Weaknesses

### Fatal

None.

### Major

- **Missing measures of variance despite 5 runs.** The paper states it conducts 5 runs for each experiment (Table 1 caption) but reports only point estimates throughout Tables 1–3 and 5, with no standard deviations or confidence intervals. This prevents assessing whether the reported improvements (some as small as ~0.36% accuracy for BEM vs. SyP+RS) are statistically significant. Given the large number of baselines, some differences could arise from noise. This is the single most impactful missing piece.

- **Class prior specification creates an ambiguity about experimental fairness.** The BEM loss (Eq. 9) requires class priors \(\pi\). The paper states \(\pi\) is "set to the cardinality of all classes" and "continually updated based on the current predicted pseudo-labels" (line 138). Because the test sets are constructed by subsampling with known imbalance ratios, initializing \(\pi\) from ground-truth class cardinalities would give L-TTA privileged distribution information that none of the baselines (TPT, TDA, DPE, SCAP, etc.) have access to. The paper should (a) state exactly what information is used for initialization, (b) if ground-truth counts are used, provide an ablation where \(\pi\) is estimated entirely from pseudo-labels from the start, and (c) show that the pseudo-label-based estimates converge to the true distribution over the stream.

### Minor

- **The Exclusionary Prototype (EP) naming is misleading relative to the actual mechanism.** Eq. 5 defines \(\phi_c = (\max_{c'}\mathbb{P}(y_{c'}|\tilde{x}_i) - \mathbb{P}(y_c|\tilde{x}_i)) / \max_{c'}\mathbb{P}(y_{c'}|\tilde{x}_i)\). For the predicted class (highest probability), \(\phi_c = 0\), so the EMA update applies fully; for low-probability classes, \(\phi_c \approx 1\), and the update approaches zero. This means each EP primarily accumulates features from samples where that class **is** the predicted class — not "most improbable features" as claimed. The mechanism is better described as confidence-weighted prototypes. The genuine difference from TDA's cache is the scope (all classes vs. predicted class), not "exclusion." This affects clarity and reproducibility.

- **The CRA loss's connection to class rebalancing is asserted but not directly demonstrated.** The loss enforces uniformity of expert utilization (an MoE-style load-balancing term), but the paper does not show that head-class prototypes specifically dominate the hyper-class vectors before CRA or that CRA specifically reduces this dominance. While the \(\eta\) ablation (Figure 4b) shows CRA contributes to overall performance, it does not isolate whether this contribution comes from rebalancing or from better feature clustering generally. An ablation comparing "SyP+RS without CRA" vs. "SyP+RS with CRA" on per-class head/tail accuracy would substantiate the claim.

- **Presentation inconsistency about \(K\).** The implementation details (line 208) state \(K = 0.3\); the ablation text (line 334) says "\(K = 0.2\) yields the best performance"; but the x-axis label in Figure 4c uses "\(b\)" instead of \(K\). Also, \(K=0.3\) as a fraction suggests it is a ratio (fraction of classes?) rather than a count, but this is never explicitly defined. Clarify what \(K\) physically represents and ensure consistent notation.

- **The relationship between BEM and the prototype-based components is underspecified.** BEM operates on logits (Eq. 9), SyPs/RSs operate on prototype feature representations. The paper claims "co-design" (Abstract and Section 3.2), but BEM could be described as a separate loss applied on top of the SyP-based prediction. The interplay — how BEM's gradient signal affects the prototypes vs. the logits directly — is not discussed.

### Trivial

None.

## Nice-to-Haves

- Adding head/tail accuracy breakdowns (currently in Appx. C) for a representative subset of datasets in the main paper would substantially strengthen the core rebalancing argument.
- Expanding the corruption benchmark beyond Gaussian noise to the full ImageNet-C (15 corruption types) in the main text would increase robustness claims' credibility.
- A short analysis of whether the self-referential entropy threshold \(\theta\) (Eq. 4) can collapse in early adaptation steps.

## Removed Points

These points from the input review were removed, treat with caution:

- "Abstract/Introduction overclaim about first attempt" — Removed because the paper's scope is clearly about *VLM* TTA under long-tailed settings, which is not addressed by prior non-i.i.d. TTA methods (SAR, DELTA) that focus on unimodal models. The claim is reasonable in context.
- "Proposition scope as plausibility arguments" — Removed because proofs are deferred to appendix (standard practice) and the propositions serve as motivation, not rigorous theorems. This is not a weakness unique to this paper.
- "Self-referential threshold in DP update may collapse" — Removed because this is a standard EMA setup used widely in TTA; a potential concern but not demonstrated as a real problem.
- "Corruption benchmark only evaluates Gaussian noise" — Removed because this is standard practice; the full 16-type ImageNet-C evaluation is in Appendix J.
- "SyP+RS vs SyP+RS+BEM gap is modest" — Removed because a 0.36%/0.66% improvement on top of an already strong system is a reasonable incremental gain.
- "EP is just a deterministic prototype" — Removed because EPs update *all* classes per sample (not just the predicted class like DPs), which IS a genuine difference in scope.
- Missing related works, formatting nitpicks, and reproducibility nitpicks about undisclosed hyperparameters — Removed per instructions.

## Novel Insights

Beyond the paper's own contributions, the key cross-review insight is that the class prior ambiguity is the single most consequential unresolved question: if \(\pi\) is initialized from ground-truth counts (known because the test sets are artificially subsampled), the main empirical comparison could be confounded by an information asymmetry that favors L-TTA. If resolved in the authors' favor (e.g., by showing that pseudo-label-based estimation from scratch achieves comparable results), the paper is solid and well-supported. The missing variance reporting is a secondary but straightforward rigor gap. These two issues — not methodology or evaluation scope — are what separate this paper from a clearly strong accept.

## Suggestions

1. **Clarify the class prior immediately.** State exactly how \(\pi\) is initialized and updated. If initialized from ground-truth cardinalities, provide an ablation where \(\pi\) is estimated entirely from pseudo-labels from the start, and show whether performance degrades.
2. **Add standard deviations** to all main tables (Tables 1–3, 5) from the 5 runs already conducted.
3. **Add an ablation** comparing "SyP+RS without CRA" vs. "SyP+RS with CRA" (varying \(\eta\) already partially addresses this, but show per-class head/tail accuracy).
4. **Fix the \(K\) inconsistency** in implementation details (0.3 vs. 0.2 vs. Figure 4c label "b") and clarify whether \(K\) is a count or ratio.
5. **Rename "Exclusionary Prototypes"** to confidence-weighted prototypes, or clearly state that EP updates all classes with a soft weighting, and remove the "most improbable features" description.

## Score and Decision

**Calibration anchors (across all rounds):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Concept Drift (MLLM) | b20VK2GnSs | 7.00 | R1 | Yes | Addressed long-tailed + OOD in VLMs with stronger theoretical framework but more severe experimental fairness issues (-1.76, -2.27 favorability) than this paper. |
| Multi-Label TTA/BEM | 75PhjtbBdr | 6.25 | R1 | Yes | Proposed BEM for multi-label TTA; weaker evaluation scope (3 datasets) and similar-magnitude clarity issues (-0.01 worst item). |
| Noisy TTA (AdaND) | iylpeTI0Ql | 6.00 | R2 | Yes | VLM TTA with novel noisy setting; method novelty concerns (-0.26) comparable to our paper's worst items. |
| PROGRAM | x5LvBK43wg | 6.20 | R2 | Yes | Prototype-based TTA; more severe weaknesses (-2.42, -2.03) than this paper. |
| ROSITA | lF9QXpfNHm | 4.67 | R1 | Yes | Open-world VLM TTA; rejected primarily for incremental contribution (-5.10) and missing error bars (0.68). |

**Round-1 bracket:** 5.5–7.5 (between well-executed but flawed VLM TTA papers at ~4.5–5.0 and strong accept at 7.5+).
**Round-2 narrowing:** Compared against Multi-Label TTA/BEM (6.25), Noisy TTA (6.00), PROGRAM (6.20), and Concept Drift (7.00). Our paper has milder worst-item favorability (-0.11 variance, -0.06 EP naming) than PROGRAM and Concept Drift, but more multiple weakness items than Multi-Label TTA. The evaluation is more extensive than any of these anchors. The class prior ambiguity is the main unresolved concern.

**Final placement:** This paper's worst weaknesses (missing variance at -0.11 favorability, EP naming at -0.06) are comparable to Multi-Label TTA's worst (-0.01) and much milder than PROGRAM's worst (-2.42) and Concept Drift's worst (-2.27). The evaluation scope (15 datasets, 5 backbones) exceeds all anchors. However, the class prior ambiguity and missing variance together prevent a higher score. The paper sits between Multi-Label TTA (6.25) and Concept Drift (7.00).

**MY FINAL SCORE: <score>6.5</score>**
**MY FINAL DECISION: <decision>Accept</decision>**