## Summary
This paper identifies and addresses several misconceptions in the emerging field of online map-based motion prediction for autonomous driving. The authors propose OMMP-Bench, a benchmark that introduces a spatially-disjoint data split to eliminate train-validation gaps, refined metrics that evaluate all moving agents (not just the ego vehicle) and separate close/far agents, and a boundary-free baseline that uses image features to provide environmental context for agents outside the online map's perception range. The paper provides extensive experimental analysis validating these corrections and offers insights into how different map element types affect motion prediction performance.

## Strengths
- **Important problem identification**: The paper correctly identifies three significant issues in the existing online map-based motion prediction protocol: inappropriate data splits causing train-val gaps, misaligned perception ranges between mapping and prediction, and non-discriminative metrics that only evaluate ego vehicle trajectories. These are genuine methodological flaws that could lead to misleading conclusions in prior work.
- **Well-motivated and practical solutions**: The proposed solutions are principled and directly address the identified issues. The spatially-disjoint data split (Table 1 shows clear evidence of the train-val gap), the focus on moving non-ego agents, and the separate reporting for close/far agents all represent meaningful improvements to experimental rigor.
- **Novel boundary-free baseline**: The image feature integration using Deformable Attention is a simple yet effective approach that demonstrably improves prediction for faraway agents (Table 7 shows 12.7% minADE reduction for MapTRv2-CL+HiVT on far agents), directly addressing the range misalignment problem without requiring larger map perception ranges that degrade map quality.
- **Comprehensive experimental analysis**: The paper provides thorough experiments across multiple map models (MapTR, MapTRv2-CL), motion models (HiVT, DenseTNT), and methods (base, uncertainty, BEV, image), with clear ablation studies on map element types (Table 5) and agent groups (Table 6).

## Weaknesses
### Fatal
None.

### Major
- **Limited scope of evaluation**: The benchmark is built exclusively on nuScenes, which the paper acknowledges is the only dataset providing raw camera data, HD maps, and agent trajectories simultaneously. However, this limits the generalizability of findings. The paper does not discuss whether the identified issues (e.g., spatial overlap between train/val sets) are specific to nuScenes or likely to appear in other datasets, nor does it propose how to adapt OMMP-Bench to future datasets.
- **Insufficient analysis of the image feature baseline's limitations**: While the image feature baseline shows strong results, the paper does not discuss potential failure modes. For example, image features from distant agents may have low resolution or be occluded, and the Deformable Attention mechanism may struggle with agents near image boundaries. The paper also does not compare computational cost of the image feature approach versus map-based approaches.

### Minor
- **The "boundary-free" claim is slightly overstated**: The image feature baseline still relies on the camera's field of view, which has its own boundaries. Agents outside all camera views would still lack features. The paper could clarify that the approach removes the *map perception range* boundary but inherits camera field-of-view limitations.
- **Limited discussion of practical deployment implications**: The paper focuses on benchmarking but does not discuss how the findings translate to real-world deployment, such as whether the image feature approach is feasible under computational constraints or how the spatially-disjoint split affects model training efficiency.

### Trivial
- The paper uses "OMPBench" and "OMMP-Bench" inconsistently in Section 3.2.

## Nice-to-Haves
- An analysis of how the image feature baseline performs under different weather/lighting conditions, which affect image quality.
- A discussion of whether the proposed split could be extended to other datasets (e.g., Waymo, Argoverse) if they provided camera data.
- An investigation of whether the image features could be combined with map features for agents within the map range, rather than replacing them.

## Novel Insights
The paper's most novel insight is that the two-stage training paradigm for online map-based motion prediction introduces a systematic train-validation gap because the motion prediction model trains on highly accurate maps (inferred on the map model's training set) but evaluates on less accurate maps (inferred on unseen data). This is a subtle but critical methodological flaw that prior work overlooked. The paper also provides the first systematic demonstration that the limited perception range of online mapping models (30x60m) is fundamentally misaligned with motion prediction requirements (agents up to 100m away), and that simply expanding the map range degrades map quality without improving prediction. The image feature baseline offers a practical workaround that avoids this trade-off entirely.

## Suggestions
- Add a discussion of the computational overhead of the image feature baseline compared to map-only approaches, including inference time and memory usage.
- Clarify in the abstract or introduction that the proposed benchmark and findings are specific to the nuScenes dataset, and discuss what would be needed to extend OMMP-Bench to other datasets.
- Consider adding an ablation study that combines image features with map features for agents within the map range, to understand whether the image features are complementary or redundant.

## Score and Decision
The paper makes a solid contribution by identifying and correcting methodological flaws in an emerging research area. The proposed benchmark is well-designed, the experiments are thorough, and the image feature baseline is a practical solution to a real problem. The main limitation is the single-dataset scope, but this is acknowledged and justified. The paper is clearly written and the contributions are significant for the subfield.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>