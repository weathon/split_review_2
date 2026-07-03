The calibration search tool is unavailable due to index issues. I will proceed with direct assessment using the ICLR scoring guidelines.

Now let me produce the final consolidated review.

## Summary

SpatialBoost proposes a framework to inject 3D spatial knowledge into pre-trained vision encoders by converting dense geometric information from images into linguistic expressions and fine-tuning encoders through an LLM with a dual-channel attention mechanism and hierarchical multi-turn Chain-of-Thought reasoning. The method preserves pre-trained knowledge while adding spatial capabilities, and is evaluated across depth estimation, semantic segmentation, 3D scene understanding, robot learning, classification, and retrieval tasks, showing consistent improvements across four base encoders (OpenCLIP, SigLIPv2, DINOv2, DINOv3).

## Strengths

- **Consistent improvements across all encoders and all tasks**: Tables 1–5 show that SpatialBoost improves every single metric across all four base encoders and all evaluation settings (depth, segmentation, 3D understanding, robot learning, classification, retrieval). This universality is stronger evidence than isolated gains on a few tasks.

- **Dual-channel attention demonstrably prevents catastrophic forgetting**: Figure 6 shows that on DINOv2, full fine-tuning drops classification accuracy from 86.3% to 79.5%, LoRA drops to 83.7%, but dual-channel attention improves to 87.6% — concretely validating that the mechanism delivers on its stated purpose of preserving pre-trained knowledge while adding new spatial capabilities.

- **LLM-based supervision outperforms pixel-level alternatives**: Table 6 shows that LLM (language) supervision is the only method that improves on all four metrics (classification +2.32%, segmentation +7.97%, depth RMSE −15.79%, VLR +2.04%), while pixel-level alternatives (linear heads, SAM decoder, VGGT decoder) often degrade performance. This directly validates the core claim that language is a more effective medium for dense spatial knowledge transfer.

- **Systematic ablations validate design choices**: Table 7 shows the forward (pixel→object→scene) multi-turn order achieves the best results, confirming the CoT hierarchy is empirically motivated. Table 8 shows that continuing pre-training with original SSL objectives (Simple FT) does not yield gains while SpatialBoost does, separating the benefit of the framework from additional training data. Figure 5 shows monotonic improvement with more data, indicating scalability.

- **Broad and challenging evaluation suite**: The paper evaluates on depth estimation (NYUv2, KITTI), semantic segmentation (ADE20K, Pascal VOC), 3D scene understanding (Lexicon3D benchmark with ScanQA, SQA3D, ScanRefer, geometric understanding, 3D semantic understanding), robot learning (CortexBench with 4 domains), and image classification/retrieval (ImageNet-1K, Oxford, Paris, Met, AmsterTime) — covering both spatial and general vision capabilities.

## Weaknesses

### Fatal
None.

### Major

- **Data overlap between QA generation source and 3D evaluation benchmark (Table 3)**: The paper states that multi-view QA training data is generated from "3D dataset (Jensen et al., 2014; **Dai et al., 2017**; Mildenhall et al., 2021; Barron et al., 2022)" (line 162–163). Dai et al., 2017 is ScanNet, which is also the source of scenes used in the 3D-centric evaluation (Table 3, titled "Results on 3D-centric tasks from **ScanNet (Dai et al., 2017)** scenes"). While the QA data is derived from VGGT's 3D reconstructions rather than ground-truth labels, this overlap means the encoder's features may benefit from having been trained on spatial QA about the same scenes it is later evaluated on. This is a legitimate concern that the paper does not acknowledge or discuss. It does not affect the other evaluations (depth on NYU/KITTI, segmentation on ADE20K/Pascal VOC, robot learning on CortexBench, classification/retrieval on ImageNet).

- **No variance estimates for most results**: Tables 1, 2, 3, 5, 6, 7, and 8 report only point estimates. Many improvements are modest (1–3 percentage points), and without variance, the reader cannot assess whether they are meaningful. Only the CortexBench results (Table 4) include error bars. For deterministic evaluation protocols, variance from training initialization (multiple seeds) should be reported.

### Minor

- **Missing control for spatial content vs. QA training format**: Table 8 compares SpatialBoost to "Simple FT" (continuing pre-training with the original SSL objective). This shows that additional training alone is not sufficient, but it does not isolate whether the improvement comes from the spatial content of the data or from the LLM-based QA training format. A control using the same pipeline (LLM, dual-channel attention) trained on an equal amount of *non-spatial* QA data would strengthen the causal attribution.

- **Table 6 comparison confounds supervision type with data richness**: The comparison between LLM fine-tuning and pixel-level decoders (linear, SAM, VGGT) varies both the decoder architecture and the richness of supervision (multi-turn spatial QA vs. simple pixel targets). The finding that LLM works better could be due to richer supervision content rather than the decoder format alone. This does not invalidate the conclusion that language-based supervision is more effective, but the "decoder only" framing is imprecise.

- **Large improvements on 3D tasks lack mechanistic explanation**: Table 3 shows OpenCLIP's 3D SU mIoU jumping from 6.9 to 54.9 and RR@0.05m from 22.6% to 78.8%. While these plausibly reflect adding a capability that was near-absent in the baseline, the paper offers no analysis of how the vision encoder's internal representations change (e.g., whether attention heads specialize to spatial features, or whether feature maps become more correlated with depth/3D structure). The dual-channel attention ablation (Figure 6) only evaluates on classification and segmentation, not on the 3D tasks where the improvements are largest.

- **No discussion of limitations**: The paper does not discuss the ScanNet data overlap, reliance on proprietary models (GPT-4o) for dataset generation, failure modes of the data generation pipeline (e.g., when Depth Pro or SAM produce inaccurate outputs), or the computational cost of the three-stage pipeline.

### Trivial
None.

## Nice-to-Haves

- Evaluate on at least one depth, segmentation, or 3D understanding benchmark that is provably disjoint from the training data of Depth Pro, SAM, and VGGT to strengthen the evidence that improvements reflect genuine spatial understanding.
- Provide a mechanistic analysis (e.g., attention head specialization, feature map correlation with 3D structure) to explain how the encoder's representations change after SpatialBoost training.
- Run the pipeline with non-spatial QA data as a control to isolate the contribution of spatial content.

## Removed Points

- **Harsh Critic Point 2 (implausibly large improvements)**: The critic claimed the improvements on 3D tasks (Table 3) were "implausibly large" and suggested they reflect data contamination. However, baselines like OpenCLIP start near-random (6.9 mIoU), so large relative gains are expected when adding a near-absent capability. The claim that improvements "look less like genuine spatial learning" is speculative and not independently verifiable from the paper. Removed per rule: "If a weakness depends on information not present in the paper... REMOVE it."

- **Harsh Critic Point 1 (part about Depth Pro training data on NYU Depth)**: The paper does not state what Depth Pro was trained on. The critic's assertion that "Depth Pro was trained on NYU Depth v2" is an assumption not present in the paper. Removed per rule: speculative-fatal claims should be demoted or removed.

- **Strength Finder's generic strengths**: Some overly generic phrasings were dropped (e.g., "the paper addressed an important problem") and merged into the concrete strengths listed above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Acknowledge and address the ScanNet overlap**: Discuss the fact that ScanNet scenes are used both for multi-view QA generation and for 3D evaluation. Provide an evaluation on at least one held-out 3D scene dataset (e.g., Matterport3D or a held-out split of ScanNet) to show that improvements generalize beyond seen scenes.
2. **Add variance estimates**: Report results across multiple seeds (at least 3) for the linear probing and DPT head experiments to establish statistical reliability.
3. **Add a non-spatial QA control**: Train the full SpatialBoost pipeline on generic caption/VQA data (same size, same format) to confirm that spatial content specifically drives the improvements.
4. **Include a limitations section** discussing failure modes, reliance on GPT-4o, and computational requirements.
5. **Provide mechanistic analysis**: Visualize attention patterns, feature map correlations with depth/3D structure, or similarity analysis to explain how the encoder's representations change.

## Score and Decision

**Score: 6 — Borderline Accept**

**Decision: Accept** (conditionally, pending author response on the ScanNet data overlap concern)

**Rationale:** SpatialBoost presents a well-motivated, technically sound approach with an admirably broad evaluation showing consistent improvements across 8+ task settings and 4 encoder backbones. The dual-channel attention mechanism is cleanly validated, and the multi-turn CoT dataset design is thoughtful. However, the paper has two significant weaknesses that prevent a higher score: (1) the undisclosed overlap between ScanNet as a source for multi-view QA generation and as the 3D evaluation benchmark, and (2) the widespread absence of variance estimates for most results. These are addressable in rebuttal. The paper's contributions are genuine (consistent improvements on tasks without data overlap concerns, such as robot learning and classification/retrieval), and the core idea is novel and well-executed.

<score>6</score>
<decision>Accept</decision>