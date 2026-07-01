## Summary

This paper identifies and addresses several misconceptions in the emerging field of online map-based motion prediction for autonomous driving. The authors propose OMMP-Bench, a benchmark that introduces a spatially-disjoint data split to eliminate train-validation gaps, refined metrics that evaluate all moving agents (not just the ego vehicle) and separate close/far agents, and a boundary-free baseline that uses image features to provide environmental context for agents outside the limited perception range of online mapping models. The paper provides extensive experiments validating these corrections and analyzing how different map element types influence motion prediction performance.

## Strengths

- **Important problem identification**: The paper correctly identifies critical methodological flaws in the existing online map-based motion prediction protocol, including the train-validation gap from overlapping data splits, the misaligned perception ranges between mapping and prediction models, and the non-discriminative nature of evaluating only ego-vehicle trajectories. These are genuine issues that undermine the validity of prior work in this area.

- **Well-motivated and practical solutions**: The proposed solutions—spatially disjoint data splits, evaluation of all moving agents with close/far stratification, and the image-feature baseline—are directly motivated by the identified problems and are practical to implement. The boundary-free baseline is a clever approach that leverages existing image features without requiring extended map perception ranges.

- **Comprehensive experimental validation**: The paper provides thorough experimental evidence for each identified issue (Tables 1-3, 6) and evaluates multiple method combinations (MapTR/MapTRv2-CL with HiVT/DenseTNT) on the proposed benchmark (Table 7), yielding clear insights about the impact of different design choices.

## Weaknesses

### Fatal
None.

### Major

- **Limited novelty of individual components**: While the paper's contribution as a benchmark/analysis is valuable, each individual component (spatially-disjoint splits, evaluating non-ego agents, using image features) is relatively straightforward. The spatially-disjoint split follows directly from Yuan et al. (2024)'s observation about spatial overlap. Evaluating non-ego agents is standard practice in motion prediction benchmarks like Argoverse and Waymo. The image-feature baseline using deformable attention is a natural extension of existing techniques. The paper's primary novelty lies in identifying and systematically addressing these issues together, which is valuable but incremental.

- **The boundary-free baseline is under-explained**: The image feature integration (Equation 1) is described very briefly. Key implementation details are missing: How are agent positions projected onto multi-view images? What is the architecture of the deformable attention module? How are the aggregated features fused with the motion prediction model? The paper claims this achieves "SOTA performance" but only compares against the base/unc/bew variants within the same framework, not against a broader set of methods.

- **Limited scope of motion prediction models evaluated**: Only HiVT and DenseTNT are used as motion prediction backbones. While these are reasonable choices, the field has more recent and stronger models (e.g., MTR, QCNet) that could provide different insights. The paper's conclusions about "stronger online mapping models benefit motion prediction" might be model-dependent.

### Minor

- **The "non-discriminative metrics" issue is somewhat overstated**: While evaluating only ego vehicle is indeed a limitation, the paper's own results (Table 6) show that ego vehicle prediction is still meaningful and discriminative (minADE ranges from 0.38 to 1.21 across methods). The claim that existing metrics are "non-discriminative" is too strong.

- **The analysis of map element types (Table 5) has a confusing presentation**: The table appears to have inconsistent checkmark patterns (e.g., row 2 and row 3 both show only "Boundary" checked but have different minADE values). This needs clarification.

- **The paper does not discuss potential limitations of the proposed split**: The map train set has 367 scenes, motion train set has 397 scenes, and motion val set has 86 scenes. This reduces the amount of data available for training the map model compared to the original split (which uses all training scenes). The impact of this reduction on map model quality is not discussed.

### Trivial
None.

## Nice-to-Haves

- An ablation study showing the contribution of each component of OMMP-Bench (new split, new metrics, image features) independently would strengthen the paper.
- Analysis of how much the spatial overlap in the original split actually inflates motion prediction performance (beyond what Table 1 shows) would be informative.
- Discussion of whether the proposed split could be extended to other datasets (e.g., Waymo, Argoverse) would increase the benchmark's impact.

## Novel Insights

Beyond the paper's own contributions, the most interesting insight is the demonstration that methods improving ego-vehicle prediction do not necessarily improve prediction for other agents (Table 7). For example, MapUncertaintyPrediction and MapBEVPrediction improve ego prediction but sometimes degrade performance on close non-ego agents. This reveals that the existing evaluation protocol may have been optimizing for the wrong objective, and that the challenges of multi-agent prediction under imperfect maps are fundamentally different from single-agent prediction. The finding that centerlines are the most informative single map element type for motion prediction (Table 5) is also practically useful for the community.

## Suggestions

- Clarify the presentation of Table 5 to resolve the apparent inconsistency in checkmark patterns.
- Provide more implementation details for the image-feature baseline, including how agent-to-image projection handles occlusions and how the deformable attention features are integrated into the motion prediction model architecture.
- Consider evaluating on at least one additional motion prediction backbone (e.g., MTR or QCNet) to strengthen the generality of the conclusions.

## Score and Decision

The paper makes a solid contribution by systematically identifying and addressing methodological flaws in an emerging research area. The benchmark is well-designed and will likely be useful for the community. However, the individual components are relatively straightforward extensions of existing ideas, and the experimental scope is somewhat limited. The paper is a clear accept at a good venue like ICLR, but it is not a breakthrough contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>