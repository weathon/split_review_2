## Summary

This paper identifies and addresses three misconceptions in the emerging two-stage protocol for online map-based motion prediction: inappropriate dataset splits that cause a train-validation gap, a mismatch between the limited perception range of online mapping models and the larger area required for motion prediction, and non-discriminative metrics that only evaluate the ego vehicle. The authors propose OMMP-Bench, a corrected benchmark that introduces a spatially disjoint three-part dataset split, refined metrics evaluating all moving non-ego agents with separate close/far categories, and a simple image-feature baseline to provide environmental context for agents outside the map’s range. Comprehensive experiments with two online mapping models and two motion prediction backbones validate the proposed fixes and provide insights for future co-development.

## Strengths

- **Clear identification of critical flaws** in the existing online map-based motion prediction protocol, including data leakage via spatial overlap and a train-val gap caused by using the same scenes for map model training and motion model training.
- **Well-motivated benchmark design** that systematically addresses each identified issue: the new spatial split significantly reduces overlap (to 5%), the metrics focus on moving non-ego agents (which are more challenging and practically relevant), and the boundary-free baseline offers a straightforward way to compensate for limited map perception.
- **Thorough experimental validation** across multiple map models (MapTR, MapTRv2-CL) and motion backbones (HiVT, DenseTNT), demonstrating that the proposed changes lead to more meaningful evaluation and that the image-feature baseline consistently improves performance, especially for far-away agents.
- **Actionable insights** for the community, such as the importance of centerlines relative to other map element types and the observation that methods improving ego-motion prediction do not necessarily benefit prediction of other agents.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- The new data split is created by manually checking the dataset; while effective, the lack of a formal algorithmic procedure may limit reproducibility. The promise to open-source code and splits mitigates this concern.
- The boundary-free baseline, while effective, is not deeply novel as a method; it is a straightforward application of deformable attention to raw image features. Its main value is as a diagnostic baseline rather than a core contribution.
- The evaluation is conducted only on nuScenes; the generalizability of the benchmark’s design choices (e.g., threshold for moving agents, definition of close/far) to other datasets (Waymo, Argoverse) is not discussed.

### Trivial
None.

## Nice-to-Haves
- A formal statistical analysis of the split’s spatial overlap (e.g., number of scenes with overlap in map train vs. motion train) would strengthen the argument.
- Ablation on the moving-agent threshold (2m / 3s) could show sensitivity of metrics.

## Novel Insights

Beyond the paper’s own contributions, the most novel insight is that **the existing online mapping based motion prediction protocol conflates map estimation accuracy on in-distribution scenes with generalization to out-of-distribution scenes**, and the reported metrics are dominated by easy static/ego cases. The paper demonstrates that strong performance on the ego vehicle does not translate to strong performance on other agents, especially those farther away—a crucial observation for safe autonomous driving. This decoupling of evaluation dimensions (close vs. far, ego vs. others) provides a more honest assessment of model capabilities and should influence future research in this area.

## Suggestions
- Release the split definitions and code promptly to enable reproduction and adoption.
- Consider including a lightweight analysis of computational overhead introduced by the image-feature baseline.
- Discuss potential limitations of the “moving” agent threshold and whether using velocity-based criteria might be more robust.

## Score and Decision
Score: 8  
Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>