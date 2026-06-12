## Summary

This paper identifies several misconceptions and methodological issues in the emerging protocol of online map-based motion prediction for autonomous driving: (1) inappropriate data splits that create a severe train-validation gap due to the two-stage training paradigm, (2) misaligned perception ranges between online mapping models and motion prediction needs, and (3) non-discriminative metrics that only evaluate the ego vehicle and include trivial static agents. The authors propose OMMP-Bench with a new spatially-disjoint three-way data split, corrected metrics evaluating all moving non-ego agents at different distances, and a boundary-free baseline that supplements distant agents with image features via deformable attention.

## Strengths

- **Well-identified train-val gap problem**: The core insight that inferring the online mapping model on its own training set creates artificially accurate maps during motion model training, while validation maps are much noisier, is clearly articulated and convincingly demonstrated. Table 1 shows that the proposed split yields consistent improvements (minADE from 0.6839→0.6308) and that the motion training/validation accuracy becomes comparable (mAP 48.9 vs 50.3), directly validating the distribution shift hypothesis.

- **Practical and well-motivated metric corrections**: The criticism that existing protocols only evaluate ego vehicle trajectories is well-reasoned given that motion prediction's purpose is collision avoidance with *other* agents. The breakdown into Ego/Moving-Non-Ego-Close/Moving-Non-Ego-Far categories (Table 6) reveals meaningful performance degradation patterns that were previously hidden—the far agents have 25%+ higher minADE than close agents for HiVT+MapTR.

- **Simple yet effective baseline**: The deformable-attention-based image feature integration (Eq. 1) addresses the out-of-scope issue without requiring extended perception ranges that degrade map quality (Table 2). Table 7 shows consistent improvements across map/motion model combinations, with a 12.7% minADE reduction on far agents for MapTRv2-CL+HiVT.

- **Thorough map element analysis**: Table 5 provides useful insights about the relative value of different map element types, with centerlines being most informative—findings that directly benefit the online mapping community's design choices.

## Weaknesses

### Fatal
None.

### Major

- **Limited experimental scope for a benchmark paper**: Only MapTR and MapTRv2-CL are evaluated as online mapping models, and only HiVT and DenseTNT as motion prediction models. This is a narrow coverage for a paper positioning itself as "OMMP-Bench." More recent motion prediction models (e.g., MTR++, QCNet) and online mapping models (e.g., StreamMapNet, LanSegNet—both discussed in the related work but never evaluated) would significantly strengthen the benchmark's utility and the generalizability of the claimed insights.

- **Reduced training data from the new split**: The three-way split yields only 367 scenes for map training and 397 for motion training out of 850 total. While this eliminates the train-val gap, it substantially reduces available training data. The paper does not analyze whether the performance improvements are partly attributable to the split design itself rather than solely to gap elimination—setting 4 in Table 1 (random 50% splits) also achieves strong results (0.6373), suggesting that a cleaner train-val gap from any non-overlapping split may matter more than the specific three-way partitioning.

### Minor

- **Sparse ablation on the image feature baseline**: The paper proposes deformable attention for image feature aggregation but does not ablate key design choices—e.g., number of attention layers, query initialization strategy, whether to combine with map features or replace them for distant agents. Table 4 shows the "img" method outperforming alternatives, but the analysis of *why* is limited.

- **No comparison with end-to-end approaches**: While the paper explicitly scopes itself to online-map-based motion prediction, it would strengthen the contribution to at least discuss or partially benchmark how the proposed corrections affect the comparison trajectory toward end-to-end systems like UniAD or ViP3D.

### Trivial

- Some table headers use "minDE" (Tables 4, 7) while others use "minFDE"—likely OCR/parsing artifacts but could also be an inconsistency worth checking in the source.

## Nice-to-Haves

- An analysis of how the proposed metrics and split affect the *relative ranking* of methods compared to the original protocol, to show that the old protocol was not just suboptimal but actively misleading about which approaches are superior.
- Exploration of whether temporal features from the online mapping model (e.g., BEV features across frames as in StreamMapNet) could provide richer context for distant agents than single-frame image features.

## Novel Insights

The identification of the two-stage train-val gap is genuinely novel and important: the observation that inferring on the map model's own training data creates an unrealistically clean input distribution for motion model training, while validation introduces a severe distribution shift, is a systematic flaw that affects all prior work in this paradigm. This insight generalizes beyond nuScenes to any two-stage pipeline where an upstream model's outputs train a downstream model on overlapping data. The additional finding that simply expanding map perception range degrades performance (Table 2-3) while image features can compensate is a practical insight that could redirect research effort from wider BEV prediction toward feature-level information sharing.

## Suggestions

- Expand the benchmark to include at least StreamMapNet and LanSegNet as online mapping models and MTR++ or QCNet as motion prediction models to establish OMMP-Bench as a comprehensive evaluation suite.
- Add a study on how many scenes are needed for map training vs. motion training to better understand the data efficiency trade-offs of the three-way split.
- Provide a deeper ablation on the image feature baseline architecture choices to guide future improvements.

## Score and Decision

The paper makes a genuine and well-supported contribution by identifying real methodological flaws in an emerging research protocol and proposing practical corrections. The train-val gap insight alone is valuable enough to change how the community approaches this problem. However, the benchmark's limited scope (only 2 map models × 2 motion models) and insufficient analysis of the data reduction trade-off prevent it from being a definitive contribution. This is solid work for a benchmark/protocol paper with clear practical impact.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <score>Accept</score>