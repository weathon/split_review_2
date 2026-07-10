Here is the final consolidated review.

---

## Summary

This paper introduces Continuous Online Action Detection (COAD), a new task formulation requiring models to perform online action detection while simultaneously adapting from a single continuous video stream without data storage. The authors curate Ego-OAD, a 263-hour egocentric OAD benchmark from Ego4D with 87 fine-grained action classes and multi-label annotations. They propose three training strategies for COAD — state continuity, orthogonal gradient projection, and non-uniform loss — and evaluate on Ego-OAD and EPIC-KITCHENS.

## Strengths

- **The COAD formulation is well-motivated and timely.** The gap between offline-trained OAD models and real-world deployment on wearable devices is clearly articulated, and framing the problem as requiring single-pass adaptation without data storage correctly identifies a genuine constraint that prior work has not addressed. (Section 1, lines 13–16)

- **Ego-OAD is a meaningful dataset contribution.** Egocentric OAD datasets are scarce, and curating 263 hours of video with 87 fine-grained action classes from Ego4D MQ fills a real gap. The multi-label annotation scheme that preserves overlapping annotations (36% of instances overlap) is a thoughtful design choice reflecting the complexity of first-person video. (Section 3, lines 52–62)

- **The evaluation protocol (pretrain / in-stream / out-of-stream splits) is principled.** Adopting the Carreira et al. (2024a) framework cleanly separates initial knowledge, online adaptation, and generalization to unseen data, providing a clear structure for evaluation. (Section 5.1)

- **Figure 4 provides compelling evidence** that COAD steadily improves out-of-stream generalization as more in-stream data is processed, narrowing the gap to the IID training upper bound despite the single-pass constraint.

## Weaknesses

### Fatal
None.

### Major

- **Missing continual learning baselines.** The "w/o COAD" baseline is vanilla SGD on streaming data — it uses none of the three proposed components (line 148). The paper does not compare against any standard continual learning method (e.g., Elastic Weight Consolidation, replay with a small memory buffer, Synaptic Intelligence, or the method from Carreira et al., 2024a adapted to the OAD setting). This means we only know that COAD outperforms naive streaming SGD, which is trivially expected. We do not know whether COAD's specific design choices beat existing adaptation strategies. (Table 1, line 148)

### Minor

- **The EPIC-KITCHENS analysis is shallow.** Table 2 shows COAD often underperforms the non-adapting Pretrained Only baseline on in-stream data (e.g., Action mAP: Pretrained Only = 9.6, COAD = 7.9). The paper provides only one sentence of post-hoc explanation ("the fine-grained nature of the actions and annotations") without analysis or investigation. This weakens claims about the method's generality. (Table 2, line 188)

- **No variance, error bars, or multiple seeds** are reported for any result. Many reported differences are small (e.g., 26.0 vs 25.5 mAP on out-of-stream, Ego pretrained) and could be within noise. The pipeline involves stochastic elements (initialization, stream order, gradient projection) that make single-run reporting unreliable. (Table 1)

- **In-stream mAP trade-off is understated.** On Ego-OAD with Ego pretraining (Table 1), w/o COAD achieves higher in-stream mAP (39.0) than COAD (36.8). The paper acknowledges this trade-off but the headline "up to 20% improvement" is based on Top-5 Recall where COAD wins, while on mAP — the primary metric in the OAD literature — the adaptation advantage is negative in this setting. (Table 1, lines 186–187)

- **The orthogonal gradient projection** only decorrelates against the immediately preceding gradient (Eq. 1, line 130), which does not address longer-range gradient interference across many steps. This limitation is not discussed.

### Trivial

- **The "up to 20% improvement" claim in the abstract/introduction is imprecise.** The actual Table 1 numbers show a 22.5pp absolute gain (Exo in-stream Top-5: 57.5→80.0) or 16.0pp (Ego in-stream), neither of which cleanly maps to "20%." The paper should clarify whether this is absolute or relative improvement. (Abstract, line 9; Table 1)

## Nice-to-Haves

- An analysis of why COAD struggles on EPIC-KITCHENS in-stream data beyond a one-sentence attribution to fine-grained actions (e.g., per-class breakdown, forgetting analysis).
- A comparison to standard (non-continuous) OAD performance on the same benchmarks to quantify the cost of the single-pass constraint.
- Discussion of the runtime/memory footprint on resource-constrained devices, since on-device deployability is part of the motivation.

## Removed Points

These points from the input review were removed for the following reasons:
1. **Missing related works on continual learning** — per rule, dropped (cannot independently verify gaps in external literature).
2. **Dataset curation detail questions** (inter-annotator agreement, guidelines for grouping action classes) — likely addressed in Appendix A which was stripped by the parser.
3. **Confounded ablation comparison** — the critic's claim about comparing rows 2 and 4 in Table 3 to isolate orthogonal gradient contribution is factually incorrect (those rows differ by two components); the paper's clean ablation (row 1 vs row 3) correctly reports the same 4.5pp figure.
4. **Runtime/compute analysis request** — a nice-to-have not standard for a task-formulation+dataset paper.
5. **Offline OAD upper bound request** — Figure 4 already includes an IID Training upper bound.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a clear structural gap — the absence of standard continual learning baselines — that the paper's own analysis does not anticipate or address.

## Suggestions

1. Add at least one strong continual learning baseline (e.g., EWC, replay with a small buffer adapted to the single-pass streaming constraint) to establish whether COAD's specific design matters beyond "any adaptation helps."
2. For EPIC-KITCHENS, conduct an investigation into why in-stream adaptation fails (e.g., catastrophic forgetting analysis, per-class performance breakdown, or t-SNE visualization of feature drift).
3. Report all main results with at least 3 random seeds with mean and standard deviation.
4. Clarify whether the "20%" claim refers to absolute percentage points or relative improvement.

## Score and Decision

**Calibration anchors (all retrieved rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/.../7L2bpe7lfm.md` (Video CL) | 4.50 | R1 | Yes | Weaker method contribution with similar missing-baseline weakness (-2.18, -4.09 favorability) |
| `/home/.../Kh5OS3oNlg.md` (PARSE-Ego4D) | 5.50 | R2 | Yes | Similar new-task+dataset structure but simpler tasks and dataset quality issues |
| `/home/.../Y7jJN0VQ4y.md` (Anomalies Streaming) | 5.71 | R2 | Yes | Similar new continual-learning paradigm with evaluation gaps; split decision (5,5,5,6,6,8) |
| `/home/.../M8gXSFGkn2.md` (EgoHOIBench) | 7.00 | R1 | Yes | Stronger experimental validation with proper baselines and broader evaluation |
| `/home/.../67sSPPAZiG.md` (MMEgo) | 6.00 | R1/R2 | No | Strong dataset+model paper with clean evaluation |
| `/home/.../P6G1Z6jkf3.md` (Hand-Object Dynamics) | 6.00 | R1/R2 | No | Clean experimental validation against appropriate baselines |

**Round 1 bracket:** Initially placed this paper between the 3.5–5.5 band (closest to the 4.50 Video CL anchor) and the 5.5–7.5 band (with PARSE-Ego4D at 5.50 and EgoHOIBench at 7.00).

**Narrowing (Round 2):** Compared against PARSE-Ego4D (5.50, Reject) and Anomalies are Streaming (5.71, Reject). Both share the structural pattern of a novel task formulation with evaluation gaps. My paper has a stronger core contribution (richer task + cleaner dataset) but a comparable missing-baseline weakness (favorability -3.23). The 6.00 anchors (MMEgo, Hand-Object Dynamics) have cleaner evaluation with proper baselines, which my paper lacks.

**Final placement:** The paper's strongest weakness (missing continual learning baselines, favorability -3.23) is comparable to the critical weaknesses in the 4.50–5.71 reject anchors. The core contribution (new task + dataset) is genuinely valuable and lifts the paper above the 4.50 anchor, but the evaluation gap prevents it from reaching the 6.00+ level where evaluation rigor is higher. The paper is closest to PARSE-Ego4D (5.50) in the balance of contribution strength vs. evaluation weakness.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>