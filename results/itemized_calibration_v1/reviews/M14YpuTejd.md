Now I have all the calibration data I need. Let me produce the final consolidated review.

**Round 1 Bracket:** Based on the calibration anchors, the narrowest plausible score range is between 5.5 and 7.0. The paper is clearly above RedMotion (5.33, rejected due to wrong experiment settings) and NoisyTraj (5.40, rejected due to unrealistic problem formulation) — it has no fatal flaws and its core diagnostic contribution is genuine. It sits below SmartPretrain (6.75, accepted) which had stronger extensibility claims and more comprehensive experiments. The paper's closest anchor is SmartPretrain, but its issues are lighter (fixable) whereas SmartPretrain's negatives included fundamental concerns about incremental contribution.

**Final Score:** 6.5. Grounding: the paper shares SmartPretrain's heavy-weight positives (well-motivated problem, clear contribution) but lacks its extensibility/combining-datasets positives. It lacks SmartPretrain's heavy-weight negatives (incremental SSL contribution, missing reproducibility details) — the paper's core diagnostic contribution is not incremental. The paper's own negatives (SOTA label, split underspecification) are minor and fixable. 6.5 is above the borderline-accept threshold (6) but below the confident-accept (8) given the specification gaps.

---

## Summary

This paper identifies three genuine misconceptions in the emerging online map based motion prediction protocol: (1) the default data split creates a train-val gap because the motion prediction model trains on high-quality maps (inferred on the mapping model's training set) and evaluates on lower-quality maps (inferred on the validation set); (2) the perception range of online mapping models (e.g., 30×60m for MapTR) is insufficient for motion prediction, which considers agents over 100m away; (3) evaluating only ego vehicles and aggregating over static/dynamic agents yields non-discriminative metrics. The authors propose **OMMP-Bench** with a geographically-disjoint three-way split, refined metrics (moving non-ego agents stratified by distance), and a boundary-free baseline using image features from the mapping model's backbone for out-of-range agents. Experiments across 2 map models × 2 motion models × 4 method variants validate the proposed corrections.

## Strengths

- **Train-val gap finding is well-diagnosed and experimentally supported.** Table 1 shows Split 1 (proposed) outperforming Split 3 (default) despite using *less* map training data (367 vs 700 scenes), providing strong evidence that the distribution shift — not data quantity — is the dominant artifact. The spatial overlap issue (87% of validation data overlaps with training data, Figure 4) is properly documented. This is the paper's strongest contribution.

- **Range misalignment is clearly motivated and empirically grounded.** Table 2 shows that extending map model perception range from 30×60m to 100×100m collapses mAP (MapTR: 0.124→0.014), while Table 3 shows motion prediction benefits from longer-range *GT* maps (minADE 0.6154→0.6003). This cleanly establishes that the map model's output range is a bottleneck that cannot be trivially solved by increasing the map model's detection range.

- **Metric refinements are well-justified.** Table 6 shows static agents have minADE of 0.002 (trivially predictable), motivating the focus on moving agents. The close/far stratification exposes performance differences masked by aggregated metrics. These changes make the benchmark more informative.

- **Comprehensive evaluation across multiple configurations.** Table 7 covers 2 map models × 2 motion models × 4 method variants = 16 configurations across three agent groups, providing a solid baseline for the corrected benchmark.

- **Genuine insight: improvements on ego prediction do not transfer.** The finding (Section 4.2) that methods improving ego prediction sometimes *degrade* performance on non-ego agents underscores that the existing ego-only protocol provides a misleading signal — validating the proposed protocol's design.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Unsupported "SOTA" claim (lines 197–198).** The paper states the proposed baseline "achieves SOTA performance." Since OMMP-Bench is defined in this same paper, there is no prior work evaluated under the same conditions to compare against. The improvements (e.g., 12.7% minADE reduction) are substantive and should be reported as relative gains over baselines — the "SOTA" label adds nothing and is technically vacuous here.
- **Data split construction is underspecified for a benchmark paper (line 121).** The paper says "we manually check the whole dataset and split it into three spatially disjoint sets." How geographic boundaries were drawn, what criteria assigned scenes to sets, and whether whole regions or individual scenes were assigned are not specified in the main text. The appendix (referenced for pipeline details) may contain this, but the main text should at minimum summarize the split algorithm for critical assessment. For a paper whose contribution includes a new benchmark split, this risks reproducibility.
- **No analysis of the image feature baseline's mechanism.** The paper claims image features "supplement environmental information" for distant agents (line 9) and shows empirical gains (12.7% minADE reduction on far agents), but provides no analysis of what information is actually extracted. For an agent 100m away in a camera image, the projected region is small; the paper does not visualize close vs. far feature content, identify failure cases, or discuss whether the baseline primarily benefits from low-level visual cues vs. structured geometry. This limits understanding of when and why the method works.
- **No limitations discussion.** The paper lacks any self-critique (e.g., sensitivity of the split to the specific geographic partition, failure modes when agents are occluded or outside the camera's field of view, how the close/far threshold is precisely determined).

### Trivial
- **Table 5 duplicate row.** Two consecutive rows show "Boundary only" with different results (0.6829 and 0.6558). Likely a formatting artifact (one row should be "Divider only"), but confusing as presented.

## Nice-to-Haves
- Show the full causal chain for range misalignment by evaluating motion prediction with online maps at extended range (currently Table 2 shows map-level degradation, Table 3 shows GT-map benefit; the reader connects them mentally).
- Add computational cost comparison (training/inference time) for the img baseline vs. base and bev baselines.
- State the explicit distance threshold for close/far and justify it with respect to the map model's perception range.
- Test split robustness with multiple random geographically-disjoint splits.
- Add failure/success case visualizations for the image feature baseline.

## Removed Points
- **"The boundary-free baseline does not solve the problem it claims to solve (structural issue)"** — REMOVED. The paper claims the baseline "mitigates" and "supplements" (lines 77, 153), not that it fully solves the problem. The empirical results (3–12% minADE reduction across settings) demonstrate meaningful improvement. The reviewer's argument that image features at long range are "vanishingly small" and cannot encode structured geometry is speculative — the paper shows the method works empirically, and the absence of analysis is already captured as a Minor weakness. This criticism as framed (structural/fatal) is not supported by evidence in the paper. The remaining concern about lack of mechanism analysis is retained as Minor.
- **Generic "reproducibility" nitpicks** — REMOVED per hard rules (the appendix was stripped by parser; hyperparameters and pipeline details may be there).
- **Missing related works concerns** — REMOVED per hard rules (cannot verify existence of unlisted works).

## Novel Insights
The paper's own insight — that methods improving ego-vehicle prediction do not necessarily improve (or can even harm) prediction of other agents, and that this is masked by existing ego-only evaluation — is the most striking finding. It directly validates the proposed metric refinements. Beyond this, the reviewers did not surface additional novel observations.

## Suggestions
1. **Remove the "SOTA" claim** (lines 197–198). Report improvements as relative gains over baselines, which the paper already does — the SOTA label adds nothing and is misleading on a new benchmark.
2. **Formalize the split construction** in the main text: provide a clear, algorithmic description of how the three geographically-disjoint sets were derived, including the geographic partition criteria.
3. **Add a mechanism analysis** for the image feature baseline: e.g., visualize feature activations for close vs. far agents, or ablate with synthetic image features to probe what information is being used.
4. **Add a limitations paragraph** discussing boundary cases and failure modes of each contribution.
5. **Fix the duplicate row in Table 5** and verify all table values against the intended experimental design.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>