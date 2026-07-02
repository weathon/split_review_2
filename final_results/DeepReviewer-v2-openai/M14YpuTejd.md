## Summary
# Final Review Report

## Summary

This paper identifies and addresses three methodological misconceptions in the emerging "online map based motion prediction" protocol for autonomous driving. The authors propose OMMP-Bench, a benchmark with (1) a spatially disjoint data split to reduce the train-validation gap caused by two-stage training, (2) refined metrics that evaluate moving non-ego agents with distance-stratified reporting, and (3) a boundary-free baseline using image features for agents beyond the online map's perception range. The paper also analyzes how different online map element types (dividers, boundaries, pedestrian crossings, centerlines) affect motion prediction quality.

**Core strengths:** The paper identifies a genuine and timely protocol-level issue — the existing evaluation protocol for online map based motion prediction conflates map quality with motion prediction performance in ways that can lead to misleading conclusions. The proposed spatially disjoint data split is a sensible methodological correction. The focus on evaluating all moving agents (not just the ego vehicle) aligns the benchmark with the practical purpose of motion prediction for collision avoidance.

**Core weaknesses:** (1) The technical contribution is diagnostic/evaluative rather than algorithmic — the "boundary-free baseline" is critically underspecified (single equation) and its SOTA claim is overstated. (2) The train-validation gap analysis conflates two distinct issues (distribution shift and spatial overlap), and the claim that the gap is "eliminated" is contradicted by the paper's own Table 1. (3) Table 5 contains a data integrity error (duplicated rows with different values). (4) The causal claim that "stronger mapping models benefit motion prediction" is confounded by the fact that MapTRv2-CL provides additional map element types (centerlines) rather than just higher accuracy. (5) The overall experimental scope is narrow (one dataset, two mapping models, two motion models), limiting generalizability. (6) External literature verification was not available in this run, so novelty conclusions are deferred.

## Strengths
1. **Timely problem identification.** The paper correctly identifies that the existing two-stage evaluation protocol for online map based motion prediction has methodological flaws — particularly the train-validation gap from using the same split for both map and motion models, and the conflation of map quality effects with motion prediction performance. These are genuine concerns that the community should address as the field grows.

2. **Sensible data split design.** The proposed spatially disjoint three-way split (map train / motion train / motion val) is a clean and practical fix for the spatial overlap issue in nuScenes. Reducing overlap from 87% to 5% (as reported in Figure 4) is a meaningful improvement that better evaluates map model generalization. The concept of splitting based on geographic regions rather than driving logs is methodologically sound and could inform future dataset construction.

3. **Distance-stratified evaluation.** Reporting performance separately for "close" and "far" agents (relative to the online map's perception range) provides useful diagnostic information. This stratification helps the community understand where the bottleneck lies — whether the map model's range or the motion model's robustness is the limiting factor. Table 6 clearly illustrates that far-agent prediction is substantially harder, confirming the value of this granular reporting.

4. **Map element type analysis.** Table 5 (despite the data error noted in Weaknesses) provides an informative ablation of how different map element types affect motion prediction. The finding that centerlines are the most individually informative element type is practically useful for online mapping model design, suggesting that future models should prioritize centerline prediction even when other elements are imperfect.

5. **Clear motivation and narrative structure.** The paper is well-organized around three identified misconceptions, each with a clear diagnosis and proposed remedy. Figure 1 provides an effective visual overview of the paper's logic, and the introduction clearly signposts the contributions.

## Weaknesses
### W1. Boundary-free baseline is critically underspecified (Major)
The core technical contribution — the boundary-free image feature baseline — is described in a single equation (Eq. 1, Page 6) with minimal supporting detail. Critical missing information includes: (a) the backbone architecture used for image feature extraction (e.g., ResNet-50, ViT, etc.) and its pretraining; (b) how the agent feature $A_i$ is initialized and integrated with the motion prediction model's pipeline; (c) training hyperparameters (learning rate, batch size, optimizer, loss weighting); (d) computational overhead (runtime, FLOPs, parameter count) vs. prior methods. **Without these details, the method cannot be reproduced.** The claim that this baseline "achieves SOTA performance" (Page 6) is unsupported — Table 4 compares against only two prior methods (MapUncertaintyPrediction, MapBEVPrediction) on a single base model (HiVT+MapTR), which is not a comprehensive SOTA comparison. **Fix:** Provide a full architecture description, replace "SOTA" with bounded performance claims, add runtime comparisons, and report multi-seed variance.

### W2. Train-validation gap analysis conflates two distinct issues (Major)
Section 3.2 discusses two problems — (i) distribution mismatch from the map model seeing its training data during motion model training, and (ii) spatial overlap between nuScenes train/val sets — but treats them as a single "inappropriate split" issue. The new split primarily addresses (ii) while only partially mitigating (i). The claim that the "train-val gap is eliminated" (Section 4.1) is contradicted by Table 1, where Setting 1 (OMMP-Bench split) still shows a non-trivial gap compared to Setting 2 (where the map model is also trained on the motion training set). **Fix:** Separate the two issues analytically, replace "eliminated" with "substantially reduced," and quantify the residual gap.

### W3. Table 5 data integrity error (Major)
Table 5 (Page 7) contains two rows with identical map element combinations (Divider=✗, Boundary=✓, Ped. Crossing=✗, Centerline=✗) but different minADE values (0.6829 vs. 0.6558). This appears to be a data aggregation or formatting error — likely one row was intended to represent a different element combination. **This undermines the central ablation experiment that informs the benchmark's design choice to use all map elements.** Without corrected data, the conclusion about centerlines being "most helpful" cannot be verified. **Fix:** Correct the duplicated rows, verify all reported values, and provide explicit textual descriptions for each configuration.

### W4. Causal claim confounded by map element type differences (Major)
Section 4.2 claims that "a stronger online mapping model benefits motion prediction" based on MapTRv2-CL outperforming MapTR (4.0% minADE reduction with DenseTNT). However, MapTRv2-CL predicts centerlines in addition to the elements that MapTR predicts. The paper's own Table 5 shows that adding centerlines significantly improves performance (from minADE 0.6500 to 0.6308). Therefore, the **performance gain may be due to richer semantic information rather than higher map accuracy** — a confounded comparison. **Fix:** Compare MapTRv2-CL vs. MapTR when both predict the same element types, or re-frame the claim as "richer map semantics benefit motion prediction."

### W5. Limited experimental scope (Moderate)
All experiments are conducted on a single dataset (nuScenes) with only two motion prediction models (HiVT, DenseTNT) and two online mapping models (MapTR, MapTRv2-CL). The paper acknowledges this limitation only implicitly ("Note that all existing online mapping based motion prediction models are conducted only on nuScenes"). The generalizability of OMMP-Bench to other datasets (Waymo, Argoverse) and stronger baselines (MTR, QCNet, LaneGCN) is untested. **Fix:** Add at least one additional dataset or a stronger recent motion prediction model to validate the benchmark design.

### W6. Range mismatch evidence is weaker than claimed (Moderate)
Table 3 shows that even with perfect GT maps, extending from 30x60m to 100x100m improves minADE by only 2.5% (0.6154→0.6003). This modest improvement from the oracle upper bound suggests that the practical impact of range mismatch may be smaller than the paper implies. Meanwhile, the online mapping mAP at standard 30x60m range is already very low (MapTR: 0.124, Table 2), raising the question of whether **online map quality at any range** is the more fundamental bottleneck. **Fix:** Add discussion of the modest GT-map gain and position the range mismatch as one of several bottlenecks, not the dominant one.

### W7. Overclaiming in abstract and contributions (Minor)
The abstract claims "thorough experiments" and the potential to "solve the long-standing mis-usage and misunderstanding of the emerging field." Given the limited experimental scope (one dataset, four model combinations), these claims overstate the paper's impact. Similarly, the boundary-free baseline is claimed to "achieve SOTA performance" (Page 6) based on a comparison with only two prior methods. **Fix:** Tone down the claims to match the evidence scope.

### W8. Moving agent threshold lacks justification (Minor)
The threshold of 2 meters movement within 3 seconds (~2.4 km/h) for classifying agents as "moving" is stated without justification or sensitivity analysis (Page 7). This threshold directly affects the composition of the evaluation set. **Fix:** Provide justification with reference to prior work (Argoverse/Waymo thresholds differ) and add a sensitivity analysis.

### W9. Conclusion is too brief (Minor)
The conclusion (Page 8) is only three sentences that essentially repeat the abstract. It lacks quantitative findings summary, limitation acknowledgment, and concrete future research directions. **Fix:** Expand to include key numerical results, bounded limitations, and prioritized future work.

### W10. Novelty verification deferred (Deferred)
External literature verification was not possible in this run (Retrieval-Disabled Mode). The paper's claims about being the first to identify these protocol-level misconceptions cannot be independently verified from publicly available literature. The authors should confirm that no prior work (e.g., concurrent workshop papers, technical reports) has independently identified the same train-val gap or range mismatch issues. All novelty-related conclusions in this review are marked as provisional pending manual literature verification.

## Score
**Final Score: 5/10**

**Rationale:** The paper identifies a genuine and timely problem in the evaluation methodology for online map based motion prediction, and the proposed data split and stratified metrics are sensible methodological improvements. However, the score is limited by several factors: (1) the core technical contribution (boundary-free baseline) is critically underspecified, (2) the experimental scope is narrow (one dataset, four model combinations), (3) Table 5 contains a data integrity error that undermines a key ablation analysis, (4) a central causal claim is confounded, and (5) the train-val gap analysis conflates distinct issues. The paper's primary value is in its diagnostic/evaluative contributions rather than its algorithmic novelty. The overall research value is moderate — useful as a community checkpoint but requiring significant strengthening for broader impact.

**Novelty assessment (provisional — deferred manual verification):** The problem diagnosis appears to be a valid critique of the existing protocol, but without external literature verification, the degree of novelty relative to concurrent or prior unpublished work cannot be fully assessed.

---

## ASCII Diagrams

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Core Claim: Existing online map motion prediction protocol has methodological flaws]
    |
    ├── Claim 1: Data splits cause train-val gap
    │   ├── Evidence: Table 1 shows minADE gap between Setting 1 (0.6308) vs Setting 2 (0.7006)
    │   ├── Gap: Issues conflated; "eliminated" claim contradicts table
    │   └── Fix: Separate distribution shift from spatial overlap
    │
    ├── Claim 2: Range mismatch harms far-agent prediction
    │   ├── Evidence: Table 2 (map mAP collapses at 100x100m), Table 3 (GT map minADE: 0.6154 vs 0.6003)
    │   ├── Gap: GT gain only 2.5%; map mAP already very low at 30x60m (0.124)
    │   └── Fix: Acknowledge modest oracle gain; position range as one bottleneck among many
    │
    ├── Claim 3: Metrics are non-discriminative
    │   ├── Evidence: Table 6 (static minADE 0.002 vs moving 0.6307)
    │   ├── Gap: Over-correction — ego prediction excluded unnecessarily
    │   └── Fix: Keep ego as complementary metric
    │
    └── Claim 4: Boundary-free baseline improves far-agent prediction
        ├── Evidence: Table 4 (minADE 0.6163 vs 0.6375 baseline)
        ├── Gap: Single equation insufficient for reproducibility; SOTA claim overreaches
        └── Fix: Full architecture + bounded claim + runtime analysis
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority    | Issue                              | Fix                                              | Expected Gain
P0          | Table 5 data integrity error        | Correct duplicated rows; verify all minADE values | Restore confidence in ablation analysis
P0          | Boundary-free baseline underspecified| Add full arch, training details, runtime          | Enable reproducibility & fair comparison
P1          | Causal claim confounded              | Add centerline-controlled ablation                | Correct attribution of gain source
P1          | Train-val gap "eliminated" overclaim | Quantify residual gap; separate two issues        | Align claims with evidence
P2          | Limited experimental scope            | Add 1+ dataset or stronger motion model           | Improve generalizability
P2          | Moving threshold unjustified          | Add justification + sensitivity analysis          | Increase metric robustness
P3          | Abstract/conclusion overclaiming      | Tone down language; add limitations                | Improve credibility
P3          | Ego metric over-correction            | Keep ego + non-ego as complementary               | Increase benchmark completeness
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Related Work Taxonomy (Root: Autonomous Driving Motion Prediction)
│
├── Branch 1: Map Representation
│   ├── Leaf 1.1: Rasterized maps
│   │   ├── MultiPath [Chai et al., 2020]
│   │   ├── Cui et al. [2019]
│   │   └── Hong et al. [2019]
│   └── Leaf 1.2: Vectorized maps
│       ├── VectorNet [Gao et al., 2020a]
│       ├── LaneGCN [Liang et al., 2020]
│       ├── SceneTransformer [Ngiam et al., 2021]
│       ├── HiVT [Zhou et al., 2022]
│       ├── MTR [Shi et al., 2022]
│       ├── QCNet [Zhou et al., 2023]
│       └── MTR++ [Shi et al., 2023]
│
├── Branch 2: Online Map Estimation
│   ├── Leaf 2.1: BEV segmentation
│   │   └── Zhou & Krähenbühl [2022]
│   └── Leaf 2.2: Vectorized map prediction
│       ├── HDMapNet [Li et al., 2022]
│       ├── VectorMapNet [Liu et al., 2023]
│       ├── MapTR [Liao et al., 2023a,b]
│       ├── StreamMapNet [Yuan et al., 2024]
│       └── LanSegNet [Li et al., 2024]
│
└── Branch 3: Online Map Based Motion Prediction
    ├── Leaf 3.1: Two-stage protocol
    │   ├── MapUncertaintyPrediction [Gu et al., 2024a] ← Baseline
    │   └── MapBEVPrediction [Gu et al., 2024b] ← Baseline
    └── Leaf 3.2: End-to-end models
        ├── ViP3D [Gu et al., 2023]
        ├── PIP [Jiang et al., 2022]
        ├── UniAD [Hu et al., 2023]
        └── VAD [Jiang et al., 2023]
        └── (Excluded: couples detection with prediction)

Key: [OMMP-Bench contribution] identifies misconceptions in Leaf 3.1
and proposes corrected protocol with disjoint split + stratified metrics.
```

**Note:** External literature verification was unavailable in this run (Retrieval-Disabled Mode). All novelty and comparison conclusions are deferred for manual verification. The related-work taxonomy above is constructed from the paper's own citations and represents the author-provided landscape, not an independently verified literature search.