Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper identifies three critical misconceptions in the emerging online-map-based motion prediction protocol: (1) inappropriate data splits causing a train-validation gap in the two-stage training pipeline, (2) mismatched perception ranges between online mapping models and motion prediction that are masked by ego-vehicle-only evaluation, and (3) non-discriminative metrics inflated by static agents. The authors propose OMMP-Bench, a benchmark with a new spatially-disjoint three-way data split, stratified evaluation on all moving non-ego agents grouped by distance, and a boundary-free baseline that uses deformable attention to extract image features for out-of-range agents. Experiments validate each proposed correction and provide reference results.

## Strengths

1. **Train-val gap diagnosis is concrete and well-supported (Table 1).** The paper cleanly demonstrates a genuine flaw: motion prediction models train on highly accurate maps produced by a mapper inferring on its own training set, but evaluate on much less accurate maps from the validation set. The experiment in Table 1 is convincing — the default split (Row 3) yields minADE 0.6839 while the proposed split (Row 1) yields 0.6308, even though the map model trains on less data. The split comparison showing that the default split and the "map train + motion train → motion train → motion val" setting both underperform the proposed split (0.6839 and 0.7006 vs. 0.6308) is strong evidence.

2. **Ego-vehicle-only evaluation critique is important and well-argued (Table 6).** The paper correctly argues that motion prediction's purpose is collision avoidance with other agents, and restricting evaluation to the ego vehicle obscures the impact of map range mismatch on faraway agents. Table 6 starkly illustrates this: ego minADE is 0.4015 while Moving Non-Ego Far is 0.6997 for the same model — a ~75% relative degradation that the prior protocol would never surface. The division into Close/Far groups within non-ego moving agents is insightful.

3. **The finding that static agents dominate and inflate metrics is correct and actionable (Table 6).** Both models achieve minADE of ~0.002 on static agents — essentially perfect prediction of trivial cases. Removing these from evaluation is the right call, consistent with Argoverse and Waymo protocols.

4. **The boundary-free baseline addresses a real gap with a sensible approach (Table 7).** Using deformable attention to let agents outside the online map's perception range extract image features directly is a natural solution. The improvements in the "Far" column are consistent (e.g., 0.6997→0.6318 for MapTR+HiVT, a 9.7% relative improvement; 12.7% for MapTRv2-CL+HiVT).

5. **Analysis of different map element types on motion prediction (Table 5)** provides useful guidance for the online mapping community, showing that centerlines are particularly informative and that feeding all available map elements yields the best performance.

## Weaknesses

### Major

1. **"SOTA" claim on the proposed baseline is unsupported (line 198).** The paper states the baseline "achieves SOTA performance." But OMMP-Bench is a *new* benchmark with a new split, new metrics, and no prior published results to compare against. The comparisons in Table 4 are all re-runs on the proposed protocol. "SOTA" is undefined here — it can only mean "best among the compared methods," which is trivial since the paper introduces the benchmark. This overclaim is unnecessary and should be removed or replaced with "best among methods evaluated on OMMP-Bench."

2. **No statistical significance or variance reported across any experiment.** Table 7 contains dozens of results with small differences (e.g., MapTR+HiVT unc vs. bew on Moving Non-Ego Close minADE: 0.5560 vs. 0.5328; on Moving Non-Ego Far MR: 0.1795 vs. 0.1772). Without multiple runs or error bars, the reader cannot assess whether these differences are meaningful or within training stochasticity. For a paper whose core contribution includes new *evaluation* practices, the absence of basic uncertainty quantification is a significant gap that undermines the reliability of the benchmark's reference results.

3. **Data split construction methodology is underspecified for reproducibility.** The paper states "we manually check the whole dataset and split it into three spatially disjoint sets" (Section 3.2). "Manually check" is not a reproducible methodology — there is no description of what spatial criteria or thresholds were used, how overlaps were determined, or what algorithm assigned scenes to splits. The caption of Figure 4 mentions "only 5% of the motion train data has overlap with map train data" but the main text never states the exact overlap figure or method for computing it. While releasing scene IDs would mitigate this, the main paper should at minimum provide the decision rules for the split.

4. **Limited model and dataset scope weakens the benchmark's initial reference results.** The benchmark evaluates only 2 motion prediction models (HiVT, DenseTNT) and 2 online mapping models (MapTR, MapTRv2-CL), all from 2022–2023. More recent and stronger models exist (QCNet, MTR++/MTR+++, StreamMapNet). For a benchmark aiming to serve as a community standard, establishing reference results only on a narrow set of models limits its immediate usefulness. Additionally, the benchmark is restricted to nuScenes alone, which the paper notes is the only available dataset with the required combination of raw camera data, HD maps, and agent trajectories, but this limitation should be explicitly discussed.

### Minor

1. **The boundary-free baseline method description is thin.** The baseline is presented as a contribution but described in only one equation and its surrounding text (Eq. 1). While using deformable attention to sample image features is a standard operation, the implementation details (feature dimensions, how features are fused with map features, architectural specifics for integration into different motion prediction backbones) are not discussed in the main paper.

2. **"Close" vs. "far" boundary is not precisely stated.** The paper says these are "decided by whether within the perception range of online mapping models" (Section 3.4). The online map perception range is 30×60m (±15×±30m), but it is unclear whether "within" means within 30m longitudinal, 60m lateral, the intersection, or the union. This needs clarification for reproducibility.

3. **The proposed split's scene allocation is not justified.** In the proposed split, the map model trains on only 367 scenes vs. the full nuScenes training set (~700 scenes) — a ~48% reduction. The paper does not discuss whether different allocations would change the conclusions, and the specific 367/397/86 breakdown appears arbitrary.

4. **No limitations section is present.** For a benchmark paper, the absence of explicit discussion of limitations (single-dataset scope, narrow model selection, computational overhead of the image feature baseline) is a missed opportunity.

### Trivial

- The title is overly long ("UNDERSTANDING THE TASK AND DATA MISCONCEPTIONS IN ONLINE MAP BASED MOTION PREDICTION FOR AUTONOMOUS DRIVING AND A BOUNDARY-FREE BASELINE") and grammatically awkward. Consider splitting into a main title and subtitle.

## Nice-to-Haves

- Expanding reference results to include at least one more modern motion prediction model (QCNet, MTR++) and one more modern online mapping model (StreamMapNet).
- Reporting results with multiple seeds (2–3 runs) to establish the noise floor.
- Providing a precise, automated procedure for the data split, or at minimum releasing exact scene IDs for each subset.
- Including a discussion of the added computational cost of the image feature baseline versus the clean two-stage pipeline.
- Discussing that image features may not provide the same geometric precision as BEV map features, and the trade-offs involved.

## Removed Points

These points from the harsh critic input were removed after cross-checking against the paper:

- **"The comparison in Table 1 is asymmetric"** — The criticism suggests Row 3 vs Row 1 is unfair because the map model in Row 3 trains on more data. But the fact that Row 3 (using ~700 scenes for the map model) still underperforms Row 1 (367 scenes for the map model, but eliminating the train-val gap) actually *strengthens* the paper's thesis. The asymmetry is the point of the experiment. This is not a weakness.

- **"The image feature baseline is not novel"** — The paper does not claim architectural novelty for the deformable attention operation itself. The novelty is in applying it specifically to address the out-of-range agent problem in this specific two-stage protocol. Using standard building blocks appropriately is not a weakness.

- **"Table 5 duplicate rows make the table confusing"** — This is a parser artifact from PDF extraction. Rows 2 and 3 appear identical in the extracted text but report different minADE values (0.6829 and 0.6558), suggesting they differ in some column not captured by the parser. This is not an author error.

- **"Always feed all possible map elements without considering trade-offs"** — The paper provides experimental evidence in Table 5 showing all map elements yields the best performance (0.6308 minADE), with centerlines alone achieving the second best (0.6631). The decision is supported by the data.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one non-obvious insight: the finding that "methods that improve ego prediction do not necessarily improve non-ego prediction" (Table 7 shows MapUncertaintyPrediction and MapBEVPrediction sometimes hurt close non-ego performance while improving ego performance). This directly justifies the paper's stratified evaluation proposal — if improvements on the old metric (ego) can mask degradations on the more important metric (non-ego), the field needs exactly this kind of diagnostic breakdown.

## Suggestions

1. **Remove or replace the "SOTA" claim** (line 198) with "achieves the best performance among methods evaluated on OMMP-Bench."
2. **Report results with at least 2–3 seeds** to establish the noise floor, or explicitly state variance from preliminary runs if available.
3. **Provide precise scene IDs, spatial overlap criteria, and an automated procedure** for the data split to enable exact reproduction.
4. **Clarify the exact distance threshold** for "close" vs. "far" agents.
5. **Add a limitations section** discussing single-dataset scope, narrow model selection, and computational overhead of the image feature baseline.
6. **Consider expanding reference models** to include at least one more recent architecture (e.g., QCNet, StreamMapNet) to make the benchmark more immediately useful.

## Calibration Report

**Round 1 bracket:** 5.5 – 7.0 (borderline accept to accept)

**Anchor papers retrieved:**

| Path | Score | Round | Comparison |
|------|-------|-------|------------|
| `5lUdTogEL3.md` (person re-id) | 1.00 | R1,<1.5 | Unrelated topic; strong reject. Not comparable. |
| `gwZ90hFSL2.md` (cross-lingual robotics) | 1.00 | R1,<1.5 | Unrelated; strong reject. |
| `pzZjyYee6L.md` (trajectory prediction, kinematic) | 2.50 | R1,1.5-3.5 | Reject-range motion prediction paper with fundamental framing issues. Our paper has clearer, better-supported contributions. |
| `324fOKW1wO.md` (decision transformer) | 3.33 | R1,1.5-3.5 | Reject. Our paper is stronger. |
| `sEJYPiVEt4.md` **(ESDMotion)** | **5.25** | R1,3.5-5.5 | **Most directly comparable.** Proposed end-to-end motion prediction with SD maps. Rejected with weaknesses about old baselines (same issue), incremental novelty (our diagnostic contributions are more novel), and unfair comparisons (our paper has SOTA overclaim). Our paper is slightly stronger due to clearly original diagnostic contributions. |
| `lgDrVM9Rpx.md` (P-MapNet) | 5.00 | R1,3.5-5.5 | Online mapping with priors. Rejected with concerns about old baselines and incremental gains. Our paper has stronger diagnostic novelty. |
| `72MSbSZtHv.md` (RedMotion) | 5.33 | R1,3.5-5.5 | Motion prediction representation learning. Mixed reviews (5,8,3). Our paper has clearer, less controversial contributions. |
| `ZPCBcR7Drg.md` (MapDR) | 5.00 | R1,3.5-5.5 | Benchmark+dataset paper for traffic rules. Mixed reviews. Our paper is similarly positioned as a benchmark but has cleaner diagnostics. |
| `mDIXfHvoqH.md` (ITPNet) | 6.75 | R1,5.5-7.5 | Instantaneous trajectory prediction. Reviewer split (5,6,8,8). Strong motivation but rejected. Our paper has similarly clear motivation but weaker method contribution and narrower scope. |
| `LsURkIPYR5.md` (LaneSegNet) | **6.00** | R1,5.5-7.5 | Map learning with lane segments. Accepted. Clear contribution, solid experiments. Our paper has comparable clarity and experimental rigor but narrower model scope. |

**Narrowing:** The most directly comparable paper is ESDMotion (5.25, Reject) — same area of online mapping + motion prediction — but our paper is diagnostically stronger with more clearly original contributions. LaneSegNet (6.00, Accept) represents the quality level our paper approaches in clarity and experimental support, though our paper has narrower model scope. The core diagnostic contributions are well-supported and the weaknesses (SOTA overclaim, no variance, limited models) are addressable and do not invalidate the central thesis. Given the combination of genuine diagnostic value and addressable weaknesses, the paper sits at borderline accept level.

**Final score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>