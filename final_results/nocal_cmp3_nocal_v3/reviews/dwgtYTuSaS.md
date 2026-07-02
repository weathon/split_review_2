Here is my final consolidated review.

---

## Summary

This paper introduces Continuous Online Action Detection (COAD), a task formulation where OAD models continuously learn and adapt from streaming video in a single pass without storing data. The authors curate Ego-OAD, a large-scale egocentric OAD benchmark (87 classes, 22,991 instances, 263h) from Ego4D, and propose three training strategies — state continuity, orthogonal gradient projection, and non-uniform loss — designed for the online streaming setting. Experiments show that continuous training improves over a static pretrained model, with the proposed components providing secondary refinements.

---

## Strengths

1. **The COAD task formulation is well-motivated and timely.** The gap between offline-trained OAD models and the deployment reality of wearable devices — where environments shift and data cannot be stored or revisited — is clearly articulated in Sections 1 and 4. Reframing OAD as a continual learning problem under single-pass, no-replay constraints is a genuine conceptual contribution.

2. **Ego-OAD fills a real gap in benchmarks.** Existing OAD benchmarks are predominantly exocentric (THUMOS14, TVSeries) or narrow-domain (EPIC-KITCHENS). Ego-OAD provides 87 classes, 22,991 instances across 263h of varied egocentric activity with a three-way split (pretrain/in-stream/out-of-stream) that separately measures adaptation and generalization.

3. **The ablation study (Table 3) is well-structured.** Separately ablating state continuity, orthogonal gradient, and non-uniform loss gives a clear picture of each component's contribution, and the results are interpretable (non-uniform loss dominates generalization gains; orthogonal gradient adds a secondary boost).

---

## Weaknesses

### Fatal
None.

### Major

1. **No comparison to any existing OAD method on Ego-OAD.** The paper describes LSTR, TeSTra, GateHub, IDN, and others in Section 2 but never compares against any of them — not even in the offline (pretraining-only) setting. The only baselines are the paper's own GRU model without adaptation ("Pretrained Only") and the same model with naive continuous training ("w/o COAD"). Without a reference point from established methods, the reader cannot assess whether the underlying GRU model is competitive or whether the benchmark presents a useful challenge. This is a structural gap that limits the paper's value to the community.

2. **The proposed training components provide modest gains over the simple continuous-training baseline, while the paper's framing overstates their importance.** On the paper's own preferred setting (Ego pretrain, out-of-stream), full COAD achieves 26.0 mAP vs. 25.5 for w/o COAD — a 0.5 mAP gain. On in-stream mAP, COAD (36.8) *loses* to w/o COAD (39.0). The gains are more visible on Top-5 Recall (76.0 vs. 71.6 out-of-stream), but the overall picture is that COAD's specific mechanisms provide a secondary refinement on top of simple continuous training. The abstract's claim of "up to 20% improvement" refers to the comparison between COAD and the static Pretrained Only model, which conflates the effect of adaptation generally with the effect of the specific proposed components. The ablation confirms this: removing state continuity changes mAP by 0.1 points (Table 3, Rows 1 vs. 4), and removing orthogonal gradient leaves out-of-stream mAP essentially unchanged (26.0→25.3).

3. **No efficiency measurements despite the resource-constrained motivation.** The paper motivates COAD by the hardware constraints of wearable devices (Sections 1, 4.5), arguing that standard offline retraining is infeasible due to limited storage and compute. Yet no measurements of FLOPs, memory usage during COAD training, or the overhead of orthogonal gradient projection are reported. Without these numbers, the paper's core motivating argument remains unsubstantiated.

4. **The experimental split design advantages the method.** Pretraining uses only 186 videos while in-stream uses 1,177 — meaning the model starts from a deliberately weak initialization trained on roughly 10% of available data. This makes any improvement from continuous adaptation look large relative to the poor pretrained baseline. A fairer evaluation would include a comparison where the model is pretrained on more data to see whether COAD's advantages persist from a stronger base.

### Minor

1. **The EPIC-KITCHENS results receive insufficient analysis.** While COAD generally outperforms Pretrained Only on out-of-stream metrics (Verb mAP 11.8 vs. 11.4, Noun mAP 37.1 vs. 31.4, Action mAP 9.9 vs. 8.6), the naive w/o COAD baseline crashes below Pretrained Only on several metrics (Verb mAP 10.7, Noun mAP 25.7). Additionally, the Pretrained Only model shows Noun mAP of 31.4 out-of-stream vs. 3.8 in-stream — a 10× gap that is not explained. The paper attributes the difficulties to "fine-grained actions" but does not analyze why continuous learning degrades performance on this dataset.

2. **No variance or statistical significance is reported.** All results are single numbers. With a single-pass training protocol where the order of data matters, variance across runs could be substantial. Given that the claimed improvements involve differences as small as 0.5 mAP, significance testing would help.

3. **No analysis of catastrophic forgetting.** A continuous learning system training on a stream without replay is at risk of forgetting earlier patterns. The paper never measures this — not even through a simple split-test on early vs. late in-stream data.

4. **The "label efficiency" claim for non-uniform loss is unsupported.** Section 4.5 states the non-uniform loss "allows training with sparse instead of dense frame-level annotations." However, all experiments use dense annotations. No experiment demonstrates the method working with fewer labels.

5. **The orthogonal gradient projection is myopic.** It decorrelates only against the single preceding gradient g_{t-1}. Temporal correlations in video can span much longer timescales, and the mechanism cannot address them. The ablation confirms the effect is modest (out-of-stream mAP essentially unchanged when removed).

### Trivial

1. The "up to 20%" claim in the abstract is loosely stated. The Top-5 gains on Ego-OAD are 22.5 points (Exo-pretrained in-stream) and 16.0 points (Ego-pretrained in-stream) — neither is precisely "20%", though "up to" technically covers both.
2. The IID training upper bound in Figure 4 is referenced but never given a numerical value, making the "approaching" claim imprecise.

---

## Nice-to-Haves

- Extending orthogonal gradient projection to decorrelate against a moving window of recent gradients (not just g_{t-1}) would address longer-term temporal correlations.
- Adding existing OAD methods as baselines on Ego-OAD's pretraining-only setting would calibrate the community on the benchmark's difficulty.

---

## Removed Points

These points from the input review were removed. Treat them with caution:

- **"EPIC-KITCHENS results actively undermine the paper's claims — Pretrained Only often matches or beats COAD on out-of-stream metrics"**: This criticism is based on a misreading of Table 2. The caption states the format is "out/in" (out-of-stream / in-stream). The reviewer treated in-stream values as out-of-stream. In fact, COAD matches or beats Pretrained Only on **every** out-of-stream metric in Table 2 (Verb mAP: 11.8 vs. 11.4; Verb Top-5: 17.0 vs. 15.5; Noun mAP: 37.1 vs. 31.4; Noun Top-5: 50.2 vs. 37.5; Action mAP: 9.9 vs. 8.6; Action Top-5: tied at 21.9). The valid sub-points (w/o COAD crashing, unexplained Noun mAP gap) are retained in Minor Weaknesses above.

- **"The claim that RNNs achieve competitive performance is unsupported"**: This claim is supported by the experiments showing continuous adaptation substantially outperforms the static baseline. While comparison to transformer-based methods would strengthen it, the claim is not unsupported.

- **"Section 3 label merging needs inter-annotator statistics"**: The grouping methodology is deferred to Appendix A, which the parser stripped. The paper cannot be penalized for appendix content.

---

## Novel Insights

None beyond the paper's own contributions. The most useful observation from review is that the paper's real empirical finding — that any form of continuous training substantially improves over a static model — is under-foregrounded relative to the specific component claims. The EPIC-KITCHENS results, if analyzed more deeply (e.g., isolating catastrophic forgetting vs. overfitting), could strengthen rather than weaken the paper by revealing where and why continuous learning can fail.

---

## Suggestions

1. Reframe the paper to separate: (a) the COAD task and Ego-OAD benchmark as standalone contributions; (b) the main finding that continuous training from streaming video substantially improves over static models; (c) the specific proposed components as secondary refinements, with appropriately hedged claims.
2. Add at least one established OAD method (e.g., LSTR, TeSTra) as a baseline on Ego-OAD in the offline setting.
3. Report efficiency metrics (FLOPs, memory, training overhead) to substantiate the wearable-device motivation.
4. Include variance estimates and a catastrophic forgetting analysis.
5. Investigate why naive continuous training (w/o COAD) degrades performance on EPIC-KITCHENS.

---

## Score and Decision

MY FINAL SCORE: 4.5
MY FINAL DECISION: Reject