The paper indeed defines the DeformAtt operation but never describes how the resulting features are fed into the motion model — verified. The final review is ready.

---

## Summary

This paper identifies three problems with the emerging online-map-based motion-prediction evaluation protocol: (1) the default data split creates a train-val gap because the map model generates near-perfect maps on its training set but much worse maps at evaluation time; (2) the perception range of online mapping models (e.g., 30×60m) is too small for motion prediction, which considers agents >100m away; (3) metrics evaluate only the ego vehicle, making them non-discriminative. The authors propose OMMP-Bench with a geographically disjoint split, refined metrics (non-ego moving agents, close/far breakdown), and a boundary-free baseline using image features to cover out-of-range agents.

## Strengths

- **The range-mismatch problem is cleanly demonstrated.** Table 2 shows mAP collapses when extending MapTR/MapTRv2-CL to 100×100m (e.g., 0.164→0.002 for MapTRv2-CL), while Table 3 shows that using GT maps at this range improves downstream prediction. This convincingly exposes a bottleneck that the prior protocol sidesteps by evaluating only the ego vehicle.

- **The evaluation-metrics critique is sound and well-evidenced.** Table 6 shows minADE=0.002 for static agents (near-perfect) vs. 0.6997 for moving non-ego far agents — a 350× difference that the old metrics completely obscure. The proposed separation into moving non-ego close/far aligns evaluation with the actual purpose of motion prediction (collision avoidance).

- **The map-element-type analysis (Table 5) provides useful empirical guidance.** Showing that feeding all element types together achieves best performance, and that centerlines contribute meaningfully, gives concrete recommendations for practitioners designing the map→motion interface.

## Weaknesses

### Major

- **The data-split claim is weaker than presented, and the paper overlooks a natural control experiment.** The paper asserts that the proposed geographically disjoint split eliminates the train-validation gap (line 145) and that the improvement over the default split demonstrates the importance of this fix. However, Table 1 row 4 — a simple 50/50 random partition of nuScenes training data (one half for map training, the other for motion training, evaluated on the original validation set) — achieves **minADE=0.6373**, nearly identical to the proposed split's **0.6308**. This 50/50 split does *not* enforce geographic disjointness, so the near-identical performance strongly suggests that the main driver of the improvement is separating map and motion training sets (so the map model generates maps on unseen data during motion training), not geographic disjointness per se. The paper does not acknowledge this comparison or discuss what the 50/50 control implies. The proposed split may still be *preferable* (geographic disjointness is beneficial for measuring generalization), but the narrative that the split *solves* the train-val gap through geographic separation overstates the evidence on the page.

- **No variance or statistical significance reporting anywhere.** Every result table reports single-run point estimates. Table 4 shows differences as small as 0.012 minADE (img vs. bev for HiVT+MapTR). Table 7 reports dozens of entries without error bars, confidence intervals, or multi-seed runs. For a paper whose central deliverable is a benchmark intended to standardize future comparisons, the absence of any uncertainty quantification is a significant gap — readers cannot tell whether the reported improvements (e.g., proposed split vs. default, image baseline vs. BEV features) are meaningful or within the noise of a single run.

- **The image-feature baseline integration is underspecified for reproducibility.** Equation (1) defines a Deformable Attention operation extracting features around each agent from image feature maps, but the paper does not describe how these extracted features are subsequently integrated into the motion prediction model — concatenation with map features? addition? a separate modality? This detail is essential for reproduction and for future work to build on the method.

### Minor

- **The "SOTA" claim for the image-feature baseline is not well-supported.** Line 198 states the baseline "achieves SOTA performance," but the improvements in Table 4 are marginal (~2% relative on minADE) and reported without variance estimates. The largest relative gain (12.7% on far agents for MapTRv2-CL+HiVT, line 313) cannot be directly verified from Table 7 (computing from table values gives ~10.4%). The language should be tempered.

- **The proposed split reduces the map model's training data from ~700 to 367 scenes, which changes the benchmark's upstream quality level.** The paper does not discuss whether performance rankings of downstream methods might shift with a stronger map model, nor whether this trade-off is desirable or merely a consequence of the split design.

- **The image-feature baseline's failure modes are not discussed.** Agents outside the camera frustum (e.g., behind the ego vehicle at multi-view edges) cannot be serviced by image features. The paper assumes image features are always available, which is not true in practice.

- **Table 5 has an apparent inconsistency:** rows 2 and 3 show identical element-type configurations (Boundary only) but different minADE values (0.6829 vs. 0.6558). The text also states that centerlines are "most helpful" yet "only achieve the second best performance" — these need clarification.

### Trivial

None.

## Nice-to-Haves

- Multi-seed experiments with variance reporting would substantially strengthen the benchmark's utility.
- An ablation showing performance with the map model trained on the full 700 scenes (under both the default and proposed protocols) would clarify whether the split changes method rankings.
- Characterizing the distribution of agent types, speeds, and scene types across the three proposed splits would help readers assess whether the motion validation set (86 scenes) is representative.
- A comparison of inference-time cost for the image-feature baseline vs. BEV-based methods would help practitioners evaluate the practical trade-off.

## Removed Points

- *"In the limit, you could train the map model on 1 scene and get perfect train-val alignment"* — removed as a speculative extreme case unconnected to any experiment in the paper.
- *Section-by-section organizational observations* — these are commentary, not weaknesses.
- *Criticism that the paper cites only two papers defining the sub-field* — not a weakness.
- *Formatting/PDF-parsing artifact speculation about Table 5* — retained only the empirically verifiable inconsistency (same config, different values), not speculation about the cause.

## Novel Insights

The observation that the 50/50 random split (Table 1, row 4) serves as a natural control and achieves nearly the same result as the proposed geographic split reframes what the data actually shows: the bulk of the train-val gap improvement comes from separating map and motion training sets (so the map model predicts on unseen data during motion training), not from geographic disjointness. This is a more honest interpretation than the paper's claim that the split "eliminates" the gap through spatial separation.

## Suggestions

1. Add the 50/50 random split to the discussion in Section 3.2 and honestly interpret what the data shows about the source of improvement.
2. Report standard deviations across multiple seeds for all main results (Tables 4, 7).
3. Specify how the Deformable Attention image features are integrated into the motion prediction model.
4. Temper the "SOTA" language for the image baseline, or provide stronger evidence.
5. Clarify the apparent inconsistency in Table 5 rows 2/3 and the "most helpful"/"second best" phrasing.
6. Acknowledge the map-model training-data reduction as a trade-off.

## Score and Decision

Score: **6** — borderline accept. The diagnosis of the three problems (range mismatch, metric non-discrimination, data-split issues) is genuinely valuable and will likely influence future work in this niche. The proposed metrics (non-ego moving agents with close/far breakdown) are a clear improvement over the existing protocol. However, the core experimental claim about the data split is weaker than presented, and the absence of variance reporting makes it difficult to assess the reliability of the benchmark. With a more honest discussion of what the split actually accomplishes and basic statistical reporting, this could be a solid contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>