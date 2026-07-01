Good — confirmed: Table 2 format is "out/in", so the critic's specific action out-of-stream claim is factually incorrect. My review correctly handles this. The final review is ready.

---

## Summary

The paper introduces Continuous Online Action Detection (COAD), a task formulation where models not only perform online action detection but also continuously learn from streaming video in a single pass without data storage. The authors curate Ego-OAD, a large-scale egocentric OAD benchmark from Ego4D (87 classes, 263 hours), and propose a training pipeline combining state continuity, orthogonal gradient projection, and non-uniform loss to enable online adaptation.

## Strengths

1. **Well-motivated problem formulation.** The gap between offline-trained OAD models and the dynamic, personalized environments of wearable devices is real and clearly articulated. COAD formalizes an important under-explored setting.

2. **Ego-OAD is a useful benchmark.** Prior OAD benchmarks are exocentric or domain-specific (EPIC-KITCHENS). Curation from Ego4D's diverse scenarios yields 87 classes across 263 hours with multi-label annotations capturing annotator disagreement, filling a genuine gap.

3. **Principled evaluation design.** The three-way split (pretrain / in-stream / out-of-stream) follows Carreira et al. (2024a) and cleanly separates adaptation (in-stream) from generalization (out-of-stream).

## Weaknesses

### Major

1. **Headline improvements conflate data scale with algorithmic contribution.** The "up to 20% in top-5 accuracy" (abstract, line 9; contributions, line 30) compares COAD against the "Pretrained Only" baseline, which trains on 186 videos, while COAD trains on 186 + 1,177 videos. The fair comparison is COAD vs. the "w/o COAD" baseline, which also trains on the 1,177 in-stream videos. Under this comparison, gains shrink dramatically: out-of-stream, COAD vs. w/o COAD is 26.0 vs. 25.5 mAP (Ego pretrain, +0.5) and 20.5 vs. 19.0 (Exo pretrain, +1.5). In-stream, w/o COAD *outperforms* COAD on mAP (39.0 vs. 36.8). The headline 20% figure reflects the benefit of adding 1,177 training videos, not the COAD method specifically. The abstract and contributions should report gains against the appropriate baseline.

2. **Method novelty is primarily in the task formulation, not the training strategies.** Every component of the training pipeline is directly adopted from prior work: orthogonal gradient projection from Han et al. (2025, line 128), non-uniform loss from An et al. (2023, line 134), and the three-way evaluation protocol from Carreira et al. (2024a). State continuity is a necessary change when moving from shuffled to streaming windows. The paper's primary contributions are therefore the COAD task formulation and the Ego-OAD dataset, with the method being a reasonable baseline combination of existing techniques. The contributions list (Section 1) should reflect this honestly rather than claiming "effective training strategies tailored to COAD" as a novel contribution.

3. **EPIC-KITCHENS results raise generality concerns.** While COAD consistently matches or beats Pretrained Only on out-of-stream metrics (the critic's specific claim about action out-of-stream losing is incorrect — it is based on a misreading of the out/in format in Table 2; the actual out-of-stream action mAP is COAD 9.9 vs. Pretrained Only 8.6), the w/o COAD baseline severely underperforms Pretrained Only on almost every metric (e.g., Verb out: 10.7/14.0 vs. 11.4/15.5; Action out: 9.3/4.9 vs. 8.6/9.6). This indicates the single-pass training protocol itself degrades performance, and COAD only partially recovers it. The paper attributes this to "the fine-grained nature of the actions and annotations in EPIC-KITCHENS" (line 188) without supporting evidence, making the explanation ad hoc. This limits confidence in the method's generality.

### Minor

4. **"Adaptation" is measured on the training set.** The in-stream set is the data the model trains on. The paper is transparent about this (line 146: "On the in-stream split, we evaluate adaptation by measuring performance at each optimization step"), but the abstract's "improves adaptation to the user's environment by up to 20%" reads like a held-out generalization claim. A proper adaptation experiment would hold out segments of the in-stream data for evaluation.

5. **No statistical significance reported.** Standard deviations across multiple seeds are absent. Given that key COAD vs. w/o COAD out-of-stream differences are 0.5–1.5 mAP points (Table 1), and ablation differences are as small as 0.1–0.5 points (Table 3), it is impossible to assess which differences are meaningful.

6. **Efficiency claims are unsubstantiated.** The paper motivates RNNs as "lightweight" and suitable for "resource-constrained devices" (line 36) but reports no measurements of inference speed, memory, or FLOPs.

### Trivial

- None.

## Nice-to-Haves

- Compare against a multi-pass offline-trained standard OAD method on Ego-OAD to contextualize the absolute mAP numbers.
- Report efficiency metrics (latency, memory, model size) to substantiate the RNN suitability claim.
- Acknowledge that the orthogonal gradient projection requires storing \(g_{t-1}\), which is a modest but real form of memory.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *"The baseline wins on both metrics for action out-of-stream on EPIC-KITCHENS"* — Factually incorrect. The critic confused the out/in format. Actual out-of-stream action mAP: COAD (9.9) > Pretrained Only (8.6).
- *"IID Training upper bound is not meaningful"* — Removed. The IID baseline controls for data quantity and isolates the single-pass vs. multi-pass effect on the same data, which is informative.
- *"No comparison to any prior OAD method"* — Removed. The Pretrained Only baseline is based on MiniROD (An et al., 2023), a prior OAD method. Direct comparison to offline-trained methods in the COAD setting offers limited additional informativeness.
- *"RNN contradiction in Section 2"* — Removed. The paper acknowledges RNN limitations and argues for their use on efficiency grounds; this is a trade-off, not a contradiction.
- *"g_{t-1} storage inconsistency"* — Removed. Storing one gradient vector is trivially different from storing video data for replay.
- All typos, formatting nitpicks, and parser artifacts — removed per guidelines.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the abstract and contributions to compare against the w/o COAD baseline rather than Pretrained Only. Report the modest but real out-of-stream gains (0.5–1.5 mAP) against the appropriate baseline.
2. Either add a held-out adaptation experiment or clarify in the abstract that in-stream results reflect training-stream performance, not held-out adaptation.
3. Report standard deviations across multiple seeds for all main results and ablations.
4. Provide a more rigorous analysis of why COAD struggles on EPIC-KITCHENS rather than a brief ad hoc explanation.

## Score and Decision

The paper makes a genuine contribution by formalizing an important under-explored problem (COAD) and providing a substantial benchmark (Ego-OAD). The method, while composed of existing components, serves as a reasonable baseline for this new setting. However, the paper substantially overstates its findings — the headline 20% improvement reflects data scale rather than the method, and the main results against the appropriate baseline show modest gains (0.5–1.5 mAP). The EPIC-KITCHENS results raise additional generality concerns. With honest reframing and appropriate baselines, this would be a solid contribution. The core scientific contributions (task formulation and benchmark) are genuine and worth accepting.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>