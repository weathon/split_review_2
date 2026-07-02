## Summary
# Final Review Report

## Summary

This paper presents EmbodiedMAE, a unified 3D multi-modal representation learning framework for robot manipulation. The authors construct DROID-3D, a large-scale supplement to the DROID dataset with high-quality depth maps and point clouds extracted via the proprietary ZED SDK, then train a multi-modal masked autoencoder that jointly learns representations across RGB, depth, and point cloud modalities via stochastic masking (Dirichlet-distributed allocation) and cross-modal decoder fusion. A ViT-Giant teacher is pre-trained on DROID-3D and distilled into Small/Base/Large student variants using a combination of MAE reconstruction loss and feature-level alignment loss. The authors evaluate EmbodiedMAE against several VFM baselines (DINOv2, SigLIP, R3M, VC-1, SPA) across 40 LIBERO tasks, 30 MetaWorld tasks, and 20 real-world tasks on SO100 and xArm robot platforms, using a compact RDT diffusion policy backbone. Results show that EmbodiedMAE variants achieve higher average success rates than the evaluated baselines, with particular advantages in tasks requiring spatial understanding and when using RGBD input. The cross-modal reconstruction visualizations (Figure 3) provide qualitative evidence of multi-modal fusion capability.

**Overall assessment:** The paper addresses an important and timely problem—learning effective 3D multi-modal representations for embodied AI. The technical approach is well-motivated, and the evaluation scope (90 tasks across simulation and real-world) is commendable. However, the manuscript has significant weaknesses in claim-evidence alignment, statistical rigor, and reproducibility that limit its current contribution level. The most critical issues are: (1) "consistently outperforms" claims are contradicted by tied results and lack statistical significance testing; (2) real-world experiments use only 10 trials per task without confidence intervals; (3) the DROID-3D pipeline depends on proprietary software; (4) key ablation results (Table 4) are missing from the visible manuscript; and (5) the training efficiency claim is asserted without quantitative measurement. The paper would benefit from more cautious claim-bounding, addition of statistical rigor, and a more comprehensive ablation of architectural choices.

--- 

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: No effective 3D VFM for embodied AI]
    |
    |--> Gap 1: Dataset domain mismatch (static scenes vs tabletop)
    |--> Gap 2: Naive 3D integration degrades policy performance
    |
    v
[Solution: EmbodiedMAE]
    |-- Component 1: DROID-3D dataset (76K trajs, ZED SDK depth)
    |-- Component 2: Multi-modal MAE (RGB + Depth + PC)
    |       |-- Dirichlet stochastic masking
    |       |-- Cross-attention decoder fusion
    |       |-- MSE reconstruction loss
    |-- Component 3: Teacher-student distillation
    |       |-- Feature alignment at 3 depths
    |       |-- Combined L_MAE + beta*L_Align loss
    |
    v
[Evidence Chain]
    |-- RQ1: Cross-modal reconstructions (qualitative only)
    |-- RQ2: MetaWorld Table 1 + LIBERO Figure 6
    |       |-- Missing: variance, significance tests
    |       |-- Weakness: duplicate columns, ties not discussed
    |-- RQ3: Real-world SO100 + xArm (10 trials/task, no CI)
    |-- Ablations: masking ratio, alignment, loss ratio (Table 4 MISSING)
    |
    v
[Key Gaps]
    |-- No statistical significance or confidence intervals
    |-- Training efficiency claimed but never measured
    |-- Point cloud modality underperforms RGBD (contradicts design goal)
    |-- Proprietary ZED SDK hinders reproducibility
    |-- Missing ablations of core architectural choices
```

## Strengths
**1. Important problem with practical relevance.** The paper targets a genuine bottleneck in embodied AI: the lack of 3D multi-modal vision foundation models pre-trained on domain-aligned robot manipulation data. Tabletop manipulation is a high-impact application area, and the observation that existing 3D VFMs are trained on static scenes with incompatible spatial scales is well-taken. The motivation for a dedicated embodied 3D VFM is sound.

**2. Large-scale dataset contribution (DROID-3D).** The creation of DROID-3D—processing the full 76K trajectories (350 hours) of DROID with ZED SDK to produce synchronized RGB, metric depth, and point clouds—is a practically valuable contribution. The scale (full dataset vs. SPA's 1/15 subset) and the use of hardware-calibrated stereo with temporal fusion are clear improvements over prior depth estimation approaches for this data. If released, this dataset could benefit the broader embodied AI community.

**3. Comprehensive evaluation scope.** The evaluation covers 70 simulation tasks (LIBERO + MetaWorld) and 20 real-world tasks on two distinct robot platforms (low-cost SO100 with dual RGB cameras and higher-precision xArm with LiDAR camera). This breadth is substantially more extensive than many prior embodied VFM papers. The consistent use of a unified policy backbone (RDT 40M) across all comparisons ensures that differences are attributable to the visual representation rather than policy architecture. Additional evaluation with ACT policy in the ablation section further strengthens generalizability claims.

**4. Well-designed cross-modal masking strategy.** The use of a Dirichlet distribution to stochastically allocate mask ratios across modalities is a principled approach that avoids modality bias. The symmetric Dirichlet(α) formulation allows the model to learn both intra-modal completion and cross-modal inference within a single training objective. The qualitative re-coloring experiment (Figure 3, column 12) provides compelling visual evidence that the model learns object-level semantics rather than just pixel-level correlations.

**5. Clear scaling analysis.** The paper evaluates four model scales (Small, Base, Large, Giant) and demonstrates monotonic improvement with capacity. The distillation pipeline (feature alignment at bottom/middle/top layers) is well-motivated and follows established best practices from DINOv2 and MAE distillation. The ablation on mask ratio and loss balance provides useful practical guidance for training multi-modal MAEs.

**6. Reproducibility-oriented code release.** The commitment to release code following HuggingFace Transformers conventions and the inclusion of a usage example (Figure 4) lower the barrier for adoption. The model's compatibility with existing robotics pipelines is a practical strength.

## Weaknesses
The weaknesses are organized from highest to lowest severity-impact.

### W1. Overclaimed performance without statistical rigor (Critical)

The abstract and introduction repeatedly state that EmbodiedMAE "consistently outperforms state-of-the-art VFMs" and "establishes EmbodiedMAE as a reliable unified 3D multi-modal VFM." These claims are not adequately supported by the evidence.

- **Tied results contradict the claim:** On MetaWorld (Table 1), EmbodiedMAE RGB (Avg 73.0) ties exactly with SPA (Avg 73.0). The word "consistently" is unsupported by this result.
- **No variance or significance testing:** No standard deviations, confidence intervals, or statistical significance tests are reported for any experiment. On LIBERO, learning curves (Figure 6) show "average across 150 trials," but without variance shading or multi-seed runs, readers cannot assess whether observed gaps are reliable. On MetaWorld, each cell is a single number without variance.
- **Training efficiency claimed but never measured:** Finding 1 claims advantage in "training efficiency," but no wall-clock time, iterations-to-convergence, or sample efficiency metrics are reported anywhere. Figure 6 shows success rate vs. gradient steps but no quantitative efficiency extraction is performed.
- **Real-world experiments have very low statistical power:** Each real-world task is evaluated across only 10 trials (Figure 8 caption). With 10 trials, a single failure changes the success rate by 10 percentage points. No confidence intervals, bootstrap estimates, or significance tests are reported. The 95% Clopper-Pearson confidence interval width for N=10 is approximately ±31%, meaning most reported differences between methods are within the noise floor.

**Severity: Critical. Impact:** The core contribution claim ("consistently outperforms SOTA") is not statistically substantiated, which would undermine the paper's main thesis if challenged during review.

### W2. Reproducibility concerns with DROID-3D pipeline (Major)

The DROID-3D depth extraction uses the proprietary ZED SDK (closed-source, commercial). This creates a fundamental reproducibility barrier:

- Researchers without ZED SDK licenses or Stereolabs hardware cannot reproduce the dataset.
- The ZED SDK version is not specified.
- No open-source alternative pipeline is discussed or provided.
- The "500 hours of processing time" lacks hardware context (GPU model, parallelization), making the computational cost non-interpretable.
- Temporal consistency of the depth is claimed but only supported by qualitative comparison (Figure 2). No quantitative temporal consistency metrics are provided.

**Severity: Major.** For a paper where the dataset is a primary contribution, the dependency on proprietary software is a significant limitation. The authors should at minimum commit to releasing an open-source processing pipeline or provide depth from an alternative open-source method as a baseline.

### W3. Table presentation errors and missing data (Major)

Table 1 (MetaWorld benchmark) has significant presentation issues:
- **Duplicate DINOv2 columns:** DINOv2 RGB appears twice (columns 3 and 6) with different values (Avg 70.7 vs Avg 54.4). The second column likely corresponds to DINOv2-RGBD, but the header does not indicate this.
- **Duplicate EmbodiedMAE columns:** EmbodiedMAE RGB appears twice (columns 5 and 7, Avg 73.0 vs Avg 76.2), again without header distinction between RGB-only and RGBD variants.
- **Table 4 is missing:** The ablation studies section repeatedly references "Table 4" for quantitative results on masking ratio, feature alignment, and loss ratio, but this table is not present in the provided manuscript.

**Severity: Major.** These errors make the main results table difficult to interpret and prevent verification of the ablation claims.

### W4. Incomplete ablation of core architectural choices (Major)

The ablation studies focus exclusively on distillation-related hyperparameters (masking ratio, feature alignment positions, loss ratio β). However, the following critical architectural decisions are not ablated:

- **Modality contribution during pre-training:** Does three-modality pre-training (RGB+Depth+PC) outperform two-modality (RGB+Depth) or single-modality (RGB only) pre-training when evaluated downstream? Without this ablation, the value of the point cloud modality in pre-training is unclear—especially since the real-world results show PC policies underperform RGBD.
- **Decoder design:** Is the cross-attention decoder superior to a simpler MLP decoder or a single shared decoder without cross-attention?
- **Dirichlet α parameter:** The concentration parameter α controls the masking diversity but its value is never reported.
- **DINOv2 initialization impact:** The encoder is initialized from DINOv2. How much of the downstream performance comes from this initialization vs. the embodied-specific pre-training? A scratch-trained baseline at the same scale would disentangle these factors.
- **No non-distilled baseline at student scales:** The student models are only trained with distillation + MAE. Without a non-distilled variant at Small/Base/Large scale, performance differences between scales could be partially attributed to distillation effectiveness rather than model capacity.

**Severity: Major.** Without these ablations, the paper cannot convincingly attribute its gains to the proposed multi-modal MAE architecture as distinct from the DINOv2 initialization or the distillation recipe.

### W5. Cross-modal fusion evidence is entirely qualitative (Major)

RQ1 evaluates multi-modal fusion capability solely through visual inspection of reconstruction examples (Figure 3). While the re-coloring experiment is insightful, there are no quantitative reconstruction metrics (PSNR, SSIM for RGB; RMSE, δ1 for depth; Chamfer distance for point clouds). Without these, readers cannot assess:
- Whether the examples are representative or cherry-picked,
- The reconstruction quality distribution across the dataset,
- How the model compares to alternative multi-modal MAE approaches (e.g., MultiMAE).

**Severity: Major.** This weakens one of the three stated research questions (RQ1).

### W6. Point cloud modality underperformance undermines design claims (Major)

Finding 2 in Section 3.4 states that "PC-based policies even underperform RGB-only inputs" due to sensor noise. This directly contradicts the paper's stated design goal of a "unified 3D multi-modal representation" that includes point clouds. If the point cloud branch is harmful at inference time, the paper should provide evidence that PC pre-training still benefits RGB-only or RGBD downstream performance (e.g., via representation quality improvements). Currently no such evidence is provided.

**Severity: Major.** The inclusion of point cloud processing without measurable benefit raises questions about the efficiency of the design.

### W7. Claim-evidence mismatch in abstract and introduction (Moderate)

Several statements in the abstract and introduction go beyond what the experiments demonstrate:
- "Establish EmbodiedMAE as a reliable unified 3D multi-modal VFM for embodied AI systems" — overbroad, as only tabletop manipulation is tested.
- "Consistently outperforms SOTA VFMs in both training efficiency and final performance" — training efficiency is not measured; final performance ties with SPA on MetaWorld.
- The third contribution bullet describes evaluation benchmarks, which is an evaluation protocol rather than a research contribution.

**Severity: Moderate.** These issues can be fixed with revised wording.

### W8. Sparse limitation discussion (Minor)

The limitations section mentions only one limitation (no language support). Other important limitations—statistical power, proprietary depth pipeline, untested generalization beyond tabletop, sensor noise affecting PC performance—are not acknowledged.

**Severity: Minor.** Adding a more comprehensive limitations paragraph would improve scientific transparency.

---

```text
ASCII Diagram — Revision Strategy Roadmap

[W1: Overclaimed performance without statistics]
    |-> Fix 1a: Remove "consistently outperforms" wording
    |-> Fix 1b: Add multi-seed variance and significance tests
    |-> Fix 1c: Report training efficiency quantitatively
    |-> Expected: Claims become defensible; core contribution remains strong

[W2: ZED SDK reproducibility]
    |-> Fix 2: Release open-source processing alternative, specify SDK version
    |-> Expected: Reproducibility restored

[W3: Table errors + missing Table 4]
    |-> Fix 3a: Correct column headers for Table 1
    |-> Fix 3b: Include Table 4 with ablation numbers
    |-> Expected: Main results become interpretable

[W4: Missing architecture ablations]
    |-> Fix 4a: Add modality ablation (RGB vs RGBD vs RGB+Depth+PC)
    |-> Fix 4b: Report Dirichlet α value
    |-> Fix 4c: Add scratch-trained baseline at Small scale
    |-> Expected: Causal attribution of architectural choices becomes clear

[W5: Qualitative-only RQ1 evidence]
    |-> Fix 5: Add PSNR/SSIM/RMSE/Chamfer metrics for reconstructions
    |-> Expected: RQ1 becomes quantitatively grounded

[W6: PC underperformance contradiction]
    |-> Fix 6: Analyze whether PC pre-training helps RGBD downstream
    |-> Expected: Design motivation for PC modality is clarified

[W7: Overclaims in abstract/intro]
    |-> Fix 7: Bound claims to evaluated baselines and settings
    |-> Expected: Objectivity and scientific credibility improve

[W8: Sparse limitations]
    |-> Fix 8: Expand limitations to 4-5 specific points
    |-> Expected: Transparency improves

=== Priority matrix ===
| Priority | Low Effort | High Effort |
|---|---|---|
| High Impact | W3 (fix table), W7 (tighten claims) | W1 (add stats), W4 (add ablations) |
| Medium Impact | W8 (expand limitations) | W2 (open-source depth), W5 (quant metrics) |
```

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses an important problem (3D multi-modal representations for embodied AI) and presents a technically sound framework (multi-modal MAE with stochastic masking and cross-modal fusion). The evaluation breadth across 90 tasks is commendable. However, the score is limited by five critical factors:

1. **Claim-evidence misalignment (most impactful):** The central claim of "consistently outperforming SOTA VFMs" is contradicted by a tied result on MetaWorld and lacks any statistical significance testing. The training efficiency advantage is asserted without measurement.

2. **Statistical gaps:** No variance, confidence intervals, or significance tests are reported anywhere. Real-world results use only 10 trials per task, making the reported differences statistically unreliable.

3. **Reproducibility barrier:** The DROID-3D dataset—a primary contribution—depends on proprietary ZED SDK without disclosed version or open-source alternative.

4. **Incomplete ablations:** The core architectural decisions (modality contribution, decoder design, DINOv2 initialization impact) are not ablated. The ablation results table (Table 4) is missing from the manuscript.

5. **Presentation errors:** Table 1 has unlabeled duplicate columns, making main results difficult to interpret.

The paper has genuine strengths—the problem framing is relevant, the evaluation is broad, and the cross-modal re-coloring experiment is clever. With revisions to address the claim-evidence gap, addition of statistical rigor, and resolution of the table/ablation issues, the paper could reach a score of 7-8/10. In its current form, the overclaims and missing evidence prevent a higher score.

**Novelty assessment (deferred):** External literature verification was not available in this run (Retrieval-Disabled Mode due to API token unavailability). Novelty and related-work adequacy judgments are deferred for manual verification. From manuscript-grounded analysis alone, the idea of a multi-modal MAE for embodied 3D representations appears reasonably novel, though the individual components (MAE, Dirichlet masking, cross-attention decoder, feature distillation) are separately known. The main novelty lies in their combination and the embodied-specific pre-training data.

---

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
(Manual verification deferred; taxonomy built from manuscript internal references only)

Related Work Taxonomy (Root: Visual Representations for Embodied AI)
├── Branch 1: Pre-training Paradigms
│   ├── Leaf 1.1: Contrastive Learning (He et al., 2019; Chen et al., 2020)
│   ├── Leaf 1.2: Masked Autoencoding (He et al., 2022; Bachmann et al., 2022; Tong et al., 2022)
│   ├── Leaf 1.3: Self-Distillation (Caron et al., 2021; Oquab et al., 2024)
│   └── Leaf 1.4: Language-Image Contrastive (Radford et al., 2021; Zhai et al., 2023)
├── Branch 2: Embodied-Specific Representations
│   ├── Leaf 2.1: Robot-dataset pre-training (Nair et al., 2022; Majumdar et al., 2023)
│   ├── Leaf 2.2: 3D-aware pre-training (Zhu et al., 2025 — SPA)
│   └── Leaf 2.3: Multi-modal MAE for embodied (This paper — EmbodiedMAE)
├── Branch 3: 3D Perception for Manipulation
│   ├── Leaf 3.1: Point cloud policies (Ze et al., 2024 — DP3)
│   ├── Leaf 3.2: RGBD fusion (Zhu et al., 2024)
│   └── Leaf 3.3: Depth estimation from stereo (Weinzaepfel et al., 2023)
└── Branch 4: Robot Learning Datasets
    ├── Leaf 4.1: DROID (Khazatsky et al., 2024)
    ├── Leaf 4.2: BridgeDataV2 (Walke et al., 2023)
    ├── Leaf 4.3: RH20T (Fang et al., 2023)
    └── Leaf 4.4: DROID-3D (This paper — supplement)

Contribution-level Novelty Conclusion (deferred):
- C1 (EmbodiedMAE framework): Novelty unclear without external verification. MultiMAE [Bachmann 2022] uses multi-task MAE but not embodied data. SPA [Zhu 2025] uses embodied pre-training but with 2D-3D implicit priors rather than explicit multi-modal MAE. The combination appears potentially novel pending literature check.
- C2 (DROID-3D dataset): Dataset contribution is clear and useful (full DROID processing with metric depth), though the ZED SDK dependency is a concern.
- C3 (Evaluation benchmarks): This is an evaluation protocol, not a research contribution.
```