Based on my reading of the paper and calibration against human-reviewed anchors, here is the final consolidated review:

---

## Summary
The paper introduces COAD (Continuous Online Action Detection), a task formulation enabling OAD models to learn on-the-fly from streaming egocentric video after deployment, without data replay or multi-pass training. The authors curate Ego-OAD—a large-scale egocentric OAD benchmark (263h, 87 classes, 22,991 instances) derived from Ego4D MQ—and apply a combination of existing streaming training techniques (orthogonal gradient projection, state continuity, non-uniform loss) to an RNN-based OAD model. Results on Ego-OAD show modest but consistent improvements in generalization; results on EPIC-KITCHENS show in-stream adaptation failing.

---

## Strengths
- **Ego-OAD dataset (Section 3):** A concrete and useful contribution—263 hours, 87 fine-grained action classes, 22,991 instances with multi-label temporally grounded annotations derived from Ego4D MQ. The union-of-annotators annotation strategy to capture label ambiguity is principled and addresses a real gap: publicly available egocentric OAD benchmarks are scarce.
- **Training-inference consistency insight (Section 4.5):** The observation that standard offline OAD training (shuffled windows, reset hidden states) creates a systematic mismatch with inference (continuous stream, preserved state) is well-motivated and clearly articulated.
- **Ablation honesty (Table 3):** The ablation does not hide unfavorable cases—e.g., the configuration without non-uniform loss achieves better in-stream mAP (42.4 vs. 36.8) than full COAD, revealing a genuine trade-off that the paper discusses openly.
- **Figure 4 convergence analysis:** The demonstration that COAD steadily narrows the gap to the IID training upper bound under single-pass constraints is a substantive empirical finding.

---

## Weaknesses

### Fatal
None.

### Major

- **Limited technical novelty:** All four COAD technical components are drawn from prior work: single-pass streaming training and the three-split evaluation protocol from Carreira et al. (2024a); orthogonal gradient projection directly from Han et al. (2025) (Eq. on p. 5, "we apply an orthogonal gradient projection technique Han et al. (2025)"); non-uniform loss from An et al. (2023); and state continuity as the natural inference-time behavior of any RNN. The paper frames these as "OAD-specific training strategies," but the only genuine OAD-specific element is applying these existing techniques to an OAD model on a new dataset. For ICLR, the gap between claimed methodological novelty and actual novelty is substantial.

- **EPIC-KITCHENS in-stream failure is undiagnosed:** Table 2 shows that both COAD and w/o COAD degrade in-stream relative to Pretrained Only on verb mAP (29.0 → 29.0 for COAD; the w/o COAD baseline collapses to 16.6), action mAP (9.6 → 7.9 for COAD), and action Top-5 Recall (22.9 → 20.5 for COAD). The paper's dismissal—"We attribute this to the fine-grained nature of the actions and annotations in EPIC-KITCHENS"—is unsupported. In-stream adaptation is the core claimed benefit of COAD; its failure on the only external validation dataset is a meaningful weakness. The paper does not explain why the approach degrades, does not relate the failure to measurable dataset properties, and does not discuss how the method should be modified.

- **No continual learning baselines:** COAD is framed as enabling continuous adaptation without forgetting. The natural comparison class includes established continual learning methods (e.g., EWC, online EWC). The only comparisons are "Pretrained Only" and "w/o COAD" (naive streaming). Without at least one principled CL baseline, the specific design choices of COAD cannot be justified relative to the problem class the paper is addressing—and it is unclear whether simpler or more standard methods would perform comparably.

### Minor

- **Backbone comparison conflates architecture and pretraining data (Table 4, Section 5.2):** The paper states "we pretrain [TSN] on Ego-OAD using a standard offline action recognition setup," while TimeSformer uses EgoVLP pretrained on a much larger egocentric corpus. The conclusion that "TimeSformer significantly outperforms TSN" cannot be attributed to architecture (clip-level vs. frame-level modeling) since pretraining data scale is entirely confounded.

- **In-stream evaluation conflates adaptation and overfitting (Section 5.1):** Measuring "adaptation" by evaluating on the same data the model was trained on is ambiguous. Figure 3 directly shows that higher learning rates improve in-stream performance at the cost of generalization—a signature of overfitting. A held-out portion of each in-stream video would provide a cleaner measure.

- **Misleading claim about EPIC-KITCHENS results (Section 5.3):** The text states "Table 1 confirms the trends observed for Ego-OAD" when discussing EPIC-KITCHENS (which appears in Table 2). More substantively, in-stream degradation on EPIC-KITCHENS does not "confirm positive trends"—it contradicts the paper's main in-stream adaptation claim.

### Trivial
- Section 4 first paragraph introduces "CODA" (typo for COAD), creating brief confusion.

---

## Nice-to-Haves
- The paper repeatedly motivates COAD for "resource-constrained devices" but provides no runtime, memory footprint, or FLOPs comparison. A rough efficiency analysis would support this motivation.
- Diagnosing the EPIC-KITCHENS in-stream failure by relating COAD gain to action frequency distribution or label diversity within a stream would transform a failure into a conditional insight about when and why the method works.
- Quantifying in tables (not only graphically in Figure 4) how much of the Pretrained Only–to–IID Training gap is closed by COAD versus w/o COAD would sharpen the generalization argument.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Headline "up to 20%" selectivity:** The reviewer noted this selects the most favorable number (Exo/In-stream Top-5 Recall +22.5%). While it does pick the peak number, the value appears correctly in Table 1 and is accompanied by other reported figures. This is mild framing, not a factual error—removed as a weakness.
- **Reproducibility concerns about hyperparameters:** Removed per policy on trivial implementation details.
- **Missing related works on continual learning:** Retained only as a missing-baselines concern, not as a related-work gap, since we cannot verify external sources.

---

## Novel Insights
The most interesting empirical finding in the paper is the in-stream vs. out-of-stream tradeoff at very large strides (Figure 3, Section 5.4): at a stride of 128, the model performs a gradient update approximately once every 68 seconds of video, yet still improves out-of-stream generalization substantially while sacrificing little on out-of-stream metrics. This suggests that the streaming training constraint itself—not the frequency of gradient updates—is the primary driver of generalization improvement, which has practical implications for on-device deployment and warrants further investigation.

---

## Suggestions
1. Add at least one principled continual learning baseline (e.g., EWC applied to the OAD head) to contextualize COAD's design choices against the problem class it addresses.
2. Diagnose the EPIC-KITCHENS in-stream failure with concrete analysis—e.g., action frequency histograms, label diversity per stream, or temporal autocorrelation of annotations—rather than dismissing it as a dataset characteristic.
3. Separate the backbone comparison (Table 4) into architecture-controlled and pretraining-controlled ablations by using a common pretraining corpus for TSN and TimeSformer.
4. Add a held-out in-stream evaluation split to distinguish genuine adaptation from overfitting.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `7L2bpe7lfm.md` | 4.50 | R1 | Video continual learning with bootstrapped compression—more technically novel than COAD but similarly rejected for unclear gains over simpler baselines |
| `jawV7vhGHw.md` | 4.25 | R1 | Real-time video classification adaptation—rejected for missing baselines and similar scope |
| `MSxCBXD5C8.md` | 3.00 | R1 | Anomalous action recognition—weaker technical contribution, rejected |
| `P6G1Z6jkf3.md` | 6.00 | R1 | Egocentric video fine-grained hand-object dynamics—accepted; stronger methodological novelty than COAD |
| `1L52bHEL5d.md` | 6.00 | R1 | Test-time adaptation for egocentric video—accepted; similar deployment motivation but cleaner contribution boundary |
| `M8gXSFGkn2.md` | 7.00 | R1 | Egocentric video-language models for hand-object interactions—accepted; strong benchmark + method novelty |
| `dl34rOnbqJ.md` | 4.40 | R1 | Egocentric action anticipation with RNNs—rejected; similar incremental framing |

**Round 1 bracket:** The paper sits between the 4–5 range. It is stronger than 3.0 anchors (genuine dataset contribution, clear motivation, real experiments) but weaker than the 6.0 anchors (borrowed technical components, EPIC-KITCHENS failure, no CL baselines). The 4.5 anchor (`7L2bpe7lfm`) is the closest match: a streaming video + continual learning application paper with a real contribution but insufficient novelty and missing baseline comparisons to justify an accept. This paper has a slightly stronger dataset contribution (Ego-OAD is more novel than adapting existing benchmarks) but a clearer in-stream failure and no CL baselines.

**Final score: 4.0** — The dataset contribution (Ego-OAD) is genuine and useful, but the task formulation assembles pre-existing components without methodological novelty, the core in-stream adaptation claim fails on EPIC-KITCHENS, and the absence of continual learning baselines leaves the method unjustified relative to its problem class. This does not reach the bar for ICLR acceptance in its current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>