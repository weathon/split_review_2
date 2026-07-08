## Summary

This paper diagnoses three misconceptions in the emerging online-map-based motion prediction protocol (Gu et al., 2024a): (1) a train-val gap arising because motion prediction models train on highly accurate maps from the mapping model's training set but evaluate on lower-accuracy maps from the validation set; (2) a range mismatch between mapping models (30×60m perception range) and motion prediction (agents >100m away); and (3) non-discriminative metrics that evaluate only the ego vehicle and include trivially predictable static agents. The authors propose OMMP-Bench, a corrected benchmark with a spatially-disjoint data split, evaluation on moving non-ego agents with close/far breakdown, a boundary-free image-feature baseline, and an analysis of map element types.

## Strengths

1. **The train-val gap critique is well-identified and empirically demonstrated.** The paper correctly shows that under the existing protocol, motion prediction models train on maps from the mapping model's training set (high mAP ~87.6) but evaluate on maps from the validation set (mAP ~50.3). Table 1 quantifies this: the default split yields minADE 0.6839 while the proposed split yields 0.6308 — an ~8% reduction.

2. **The range-mismatch diagnosis is genuine and practically motivated.** The paper concretely shows (Tables 2–3) that (a) extending mapping range to 100×100m catastrophically degrades map quality (mAP drops from 0.124 to 0.014 for MapTR), and (b) GT maps at longer range improve motion prediction (0.6154→0.6003 minADE), but online maps cannot exploit this because their long-range quality is too poor.

3. **The evaluation refinements (moving non-ego agents, close/far breakdown) are sensible.** The paper correctly observes that static agents are trivially predictable (minADE ~0.002 for both models in Table 6), making aggregate metrics misleading. The close/far breakdown usefully separates the range-mismatch effect from other sources of difficulty. These design choices are appropriate for this protocol.

## Weaknesses

### Fatal
None.

### Major

1. **Range-mismatch rhetoric exceeds what the evidence supports.** Table 3 shows that even with *perfect* GT maps, extending the range from 30×60m to 100×100m produces only a 2.5% improvement in minADE (0.6154→0.6003). The improvement with online maps would be smaller since long-range online map quality is near-zero (Table 2). The paper's framing (e.g., "could significantly degenerate the accuracy," Sec. 1) overstates the practical severity relative to its own data. Additionally, the "SOTA performance" claim (line 198) is inflated: the image-feature baseline (3.3% improvement on HiVT+MapTR in Table 4) is compared against only two prior methods from the same research group.

2. **The new split's benefit is not cleanly isolated.** Split 4 in Table 1 (a random half-half split of nuScenes training data) achieves minADE 0.6373 — very close to Split 1's 0.6308 (a ~1% difference). The paper does not acknowledge that simply using any disjoint training subsets achieves most of the benefit, without requiring the elaborate spatial-disjoint partitioning. Furthermore, the comparison of Split 1 vs. Split 3 conflates two changes: fixing the train-val gap and changing which scenes are used for each purpose.

### Minor

3. **No statistical significance or variance information is reported.** Every numerical result in Tables 1, 4, 5, 6, and 7 is a single point estimate with no standard deviations, confidence intervals, or multi-seed averages. The validation set has only 86 scenes, raising variance concerns that are especially consequential for interpreting small differences (e.g., the ~1% gap between Split 1 and Split 4).

4. **The interesting observation that methods improving ego prediction do not necessarily help non-ego prediction (line 311) is stated but not analyzed.** Why do MapUncertaintyPrediction and MapBEVPrediction sometimes hurt non-ego performance while helping ego? This is precisely the kind of insight a benchmark paper should probe, but it is left as a surface-level observation.

5. **No limitations section is included.** A benchmark paper would benefit from acknowledging scope limitations: the benchmark is nuScenes-only with untested generalizability, evaluation uses GT agent histories so results may not transfer to settings with noisy detection/tracking, and the validation set is small (86 scenes).

### Trivial

6. **The threshold for classifying agents as "moving" (more than 2 meters within 3 seconds, ~0.67 m/s, line 259) is stated but not justified.** It is unclear how sensitive the results are to this choice.

## Nice-to-Haves
- Provide a clean ablation that isolates the train-val gap effect from scene-composition changes (e.g., hold scene composition fixed while varying only whether the mapping model saw those scenes during its own training).
- Add variance reporting (standard deviations from multi-seed runs) for key numerical comparisons.
- Explicitly discuss the relationship between Split 1 and Split 4 — does the spatial-disjointness constraint add value beyond a random disjoint split, and if so, what value?
- Calibrate claims about range-mismatch severity to match the measured effect sizes.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **Baseline underspecified (details in Appendix):** The harsh critic notes the image-feature baseline description is thin. REMOVED per system prompt — the paper explicitly references Appendix A for details, and the parser strips appendix content from all papers.
2. **Framing of "misconceptions"/"misunderstandings" as too strong:** REMOVED as a presentation/style point that does not affect technical substance.
3. **"Inappropriate Dataset Splits" label as over-broad:** REMOVED as a minor presentation point.
4. **"Always feed all possible map elements" as trivial:** REMOVED — while not surprising, it is a useful empirical confirmation and a reasonable benchmark recommendation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Add a clean ablation isolating the train-val gap effect from scene composition changes.
- Report standard deviations or confidence intervals for all main numerical comparisons (Tables 1, 4, 7).
- Discuss why Split 4 (random half-half) achieves nearly the same minADE as Split 1, and whether the spatial-disjointness constraint is necessary.
- Tone down the range-mismatch rhetoric to match the measured 2.5% effect size with GT maps.
- Add a limitations section covering nuScenes-only scope, GT agent history assumption, and small validation set.

---

## Calibration Report

### Round 1 — Bracketing

| Anchor Paper | Path | Avg Human Score | Round | Itemized | Comparison to this paper |
|---|---|---|---|---|---|
| Driving by the Rules (MapDR) | ZPCBcR7Drg.md | 5.00 | 1 | Yes | Benchmark paper for HD map + traffic rules. Similar type of contribution (diagnostic benchmark), but weaker motivation led to Reject. Our paper has clearer motivation but less data. |
| RedMotion | 72MSbSZtHv.md | 5.33 | 1 | Yes | Motion prediction method paper. More negative-weighted weaknesses than ours (-4.95 novelty concern). Our weaknesses are milder. |
| Large Trajectory Models (STR) | r125wFo0L3.md | 5.00 | 1 | Yes | Motion prediction method paper with scaling analysis. Strongest negative weights (-4.95, -2.28) exceed ours. |
| SmartPretrain | Bmzv2Gch9v.md | 6.75 | 1 | Yes | SSL for motion prediction. Thorough experiments (weight 9.26, 9.80) but negative weights (-4.80, -2.91) more severe than ours. |
| LaneSegNet | LsURkIPYR5.md | 6.00 | 2 | Yes | HD map learning method. All weakness weights positive; strong experimental validation. Our paper has one moderately negative weakness (-0.93) they lack. |
| MGMapNet | E8S5Upr6oO.md | 6.00 | 2 | Yes | HD map construction method. All weakness weights positive. Clean, well-scoped experimental section. |

**Round-1 bracket:** The paper sits between 5.5 and 6.5. It is clearly above the 1.0–3.0 range (papers with fundamental flaws) and above the 5.0 anchors (Driving by the Rules: rejected due to weaker motivation; RedMotion/STR: more negative-weighted flaws). It is below the 6.75 anchors (SmartPretrain: significantly more thorough experiments). The closest band is the 5.75–6.0 region occupied by LaneSegNet and Trajectory-LLM.

### Round 2 — Narrowing

| Anchor Paper | Path | Avg Human Score | Round | Itemized | Comparison to this paper |
|---|---|---|---|---|---|
| Trajectory-LLM | UapxTvxB3N.md | 5.75 | 2(Narrow) | Yes | LLM-based trajectory generation. More negative weakness weights (-2.50 clarity, -1.09 insufficient experiments) than our paper's most negative (-0.93). Accepted despite issues. |

**Narrowing:** Compared to Trajectory-LLM (5.75, accepted), this paper has a less severe negative-weight weakness (-0.93 vs. -2.50) and comparable positive strengths. Compared to LaneSegNet (6.00), this paper has one genuinely negative weakness (range-mismatch overstatement) that LaneSegNet lacks, but makes a different type of contribution (protocol diagnosis vs. new method). The train-val gap diagnosis is a genuinely useful contribution that the community will benefit from, and all weaknesses are addressable without undermining the core claims. The paper fits naturally in the 5.75–6.0 band, and given that the core diagnostic contributions are sound and will likely influence the field, a score at the upper end of the band is warranted.

**Final score determination:** My draft's most damaging weakness weight (-0.93 for range-mismatch overstatement) is milder than the most negative weights in rejected papers at score 5.0 (Driving by the Rules: -3.82; Large Trajectory Models: -4.95) and comparable to accepted papers at 5.75 (Trajectory-LLM: -2.50). The paper lacks the thorough experimental rigor of LaneSegNet (6.00) and SmartPretrain (6.75), which have all-positive weakness weights and fully elaborated ablations. However, the paper's core contribution — identifying and empirically demonstrating the train-val gap in two-stage map-based motion prediction — is clear, significant for the community, and unlikely to be invalidated by the listed weaknesses. This places it at **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>