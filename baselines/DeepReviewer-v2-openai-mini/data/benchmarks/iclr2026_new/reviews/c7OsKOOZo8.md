## Summary
# Final Review Report

## Summary

This paper proposes an end-to-end framework for multi-view diabetic retinopathy (DR) grading that generates lesion-aware cues without requiring external annotations. The framework consists of two novel modules: (1) Grade-Activated Lesion Proposal (GALP), which attaches stage-wise auxiliary classifiers to multi-resolution feature maps and selects top-K high-evidence regions as lesion proposals via grade-conditioned evidence maps (CAM-based); and (2) Cross-View Lesion Expert Guided Regional Fusion (LGRF), which uses mixture-of-experts routing and top-K-weighted cross-view attention to fuse lesion proposals across views. The method is evaluated on two multi-view DR datasets (MFIDDR with four-view, DRTiD with two-view) and achieves 83.9% accuracy without lesion annotations and 84.6% with lesion annotations on MFIDDR, outperforming several end-to-end and externally-informed baselines. The core claim is that self-generated lesion proposals can substitute costly expert annotations while maintaining competitive performance.

**Manuscript Type:** Application-focused method paper (medical image analysis + deep learning system)

**Novelty Verdict:** Deferred — external literature verification unavailable in this run (Retrieval-Disabled Mode). Provisional assessment: the GALP+LGRF pipeline combines existing techniques (CAM, MoE, cross-attention) in a novel arrangement for DR grading, but the individual components are well-established. The main research contribution is the demonstration that self-derived lesion proposals from auxiliary classifiers can reduce annotation dependency without significant performance loss.

**Overall Score:** 6/10 (see detailed justification in Score section)

## Strengths
1. **Clear Problem Framing and Clinical Motivation.** The paper articulates a well-defined practical problem: end-to-end DR grading pipelines lose fine-grained lesion information due to spatial downsampling, while externally-augmented methods require costly annotations. The introduction effectively establishes the clinical stakes (DR screening demand, specialist shortage) and connects them to a concrete technical gap.

2. **Novel Integration of Self-Derived Lesion Proposals.** The GALP module's strategy of generating lesion proposals from grade-conditioned evidence maps via auxiliary classifiers is a clever approach that avoids external annotation dependencies. Using CAM-based evidence maps as a surrogate for lesion detection during both training and inference is technically sound and well-motivated.

3. **Comprehensive Experimental Evaluation on Two Datasets.** The paper evaluates on two multi-view DR datasets (MFIDDR with 8,613 eyes and DRTiD with 3,100 eyes), comparing against a broad range of end-to-end and externally-informed baselines. The results show that the lesion-free variant (83.9% accuracy on MFIDDR) is competitive with several annotation-dependent methods, supporting the claim that self-derived proposals can reduce annotation needs.

4. **Well-Designed Ablation Study.** Table 4 cleanly decomposes the contributions of GALP, LGRF, and the expert pool, showing each module's impact on accuracy, specificity, kappa, and F1. The hyperparameter study (Fig. 3) explores retention ratio, number of activated experts, and total experts, providing practical guidance for configuration.

5. **Modular and Flexible Architecture.** The framework supports both annotation-free and annotation-augmented modes (via SPADE fusion with lesion masks), demonstrating adaptability. The LGRF module's gated expert routing conditioned on cross-view features is a principled approach to selective fusion.

## Weaknesses
### Major

**1. No Variance or Statistical Significance Reported (Issue — Missing Control).** All experiments (Tables 1-4) report only single-run point estimates without standard deviation, confidence intervals, or significance tests. The accuracy differences between the proposed method and the strongest baselines are small (83.9% vs 84.2% for WGLIN, or 83.9% vs 84.0% for SMVDR-M). Without multi-seed runs or statistical testing, the claimed improvements cannot be distinguished from random variation. **Risk:** Invalid comparison conclusions; the core claim of "SOTA competitiveness" is not statistically supported.

**2. GALP Lesion-Proposal Assumption Not Validated (Issue — Unverified Causal Assumption).** The GALP module interprets high CAM activation regions as "lesion proposals" based on the unverified premise that grade-discriminative regions are identical to lesion locations. The paper provides no quantitative evidence (e.g., IoU with provided lesion segmentation masks) that the selected top-K regions correspond to actual microaneurysms, hemorrhages, or exudates. Since CAMs can highlight spurious correlations (image background, illumination artifacts, vessel shadows), the "lesion proposal" label may be misleading. **Risk:** Overclaiming lesion-awareness; the method may work well without actually detecting lesions.

**3. Missing Robustness and Interpretability Validation for Claim (2) (Issue — Evidence Gap).** Contribution (2) explicitly claims "superior robustness and interpretability," yet the paper contains zero robustness experiments (no noise injection, domain shift, image corruption tests) and zero interpretability metrics (no lesion localization accuracy, no attention-map fidelity evaluation). The ablation study measures accuracy only, leaving robustness and interpretability claims entirely unsupported. **Risk:** Scientific misrepresentation; the claim must be removed or validated.

**4. Load-Balancing Loss (Eq. 11) Uses Non-Standard Formulation (Issue — Mathematical Concern).** The load-balancing loss multiplies the standard auxiliary loss by an extra factor of $M$ (total number of experts) without justification. The standard MoE auxiliary loss (Shazeer et al., 2017; Fedus et al., 2022) uses $L = \alpha \cdot \sum_{m} f_m \cdot P_m$ without the outer $M$ factor. The paper's formulation with $M$ and $\lambda_{\text{load}}=0.1$ may arbitrarily amplify the regularization when the number of experts changes, breaking the intended loss balance. **Risk:** Potentially incorrect gradient weighting; the loss behavior may not generalize to different expert counts.

**5. Comparison Fairness Concerns (Issue — Confounded Evaluation).** The compared methods use different backbones and pretraining strategies (e.g., Swin-B with ImageNet pretraining vs. ResNet/VGG with other pretraining). The paper does not control for backbone capacity, training budget, or computational cost when drawing comparative conclusions. The claim that "our method matches or surpasses strong baselines" is confounded by these architectural differences. **Risk:** The relative ranking may reflect implementation choices rather than genuine methodological superiority.

### Minor

**6. Missing Computational Cost Reporting.** The paper does not report FLOPs, parameter count, inference time, or GPU memory for any method, making it impossible to assess the computational overhead of GALP and LGRF modules against baselines. Given the claimed "practical potential for clinical deployment," efficiency metrics are essential.

**7. Missing Implementation Reproducibility Details.** Critical training hyperparameters are absent: optimizer type, learning rate schedule, number of epochs, batch size, weight decay, gradient clipping, data augmentation strategy, and hardware specification. Without these, the experiments cannot be independently reproduced.

**8. Related Work is List-Style Rather Than Thematic.** The Related Work section (Section 2) reads as a chronological summary of methods rather than a structured comparison organized by technical axes (e.g., fusion strategy, supervision regime, resolution handling). This weakens the paper's novelty positioning.

**9. Introduction Paragraph 1 Lacks Precise Technical Gap.** The opening paragraph strongly establishes clinical motivation but ends on a generic note ("deep learning emerging as a prominent approach") without specifying the precise technical gap that the paper addresses.

**10. Conclusion Omits Limitations.** The Conclusion claims "SOTA performance" and "practical potential for clinical deployment" without any acknowledgment of the unvalidated lesion-proposal assumption, the single-run experiments, the limited OOD evaluation, or the computational complexity.

## Score
**Final Score: 6/10**

### Scoring Rationale

**Research Value (Primary): 6/10** — The paper addresses a practically relevant problem (reducing annotation dependency in DR grading) and proposes a technically coherent solution. The demonstrated performance is competitive, but the lack of statistical validation, unverified core assumption (CAM regions = lesions), and missing robustness evidence significantly weaken the demonstrated scientific value. The contribution is more about system engineering and empirical demonstration than fundamental methodological insight.

**Novelty (Primary): 5/10** — The combination of CAM-based proposal generation with MoE-guided cross-view fusion is novel in the DR grading literature, but each component (CAM for weakly-supervised localization, MoE routing, cross-attention fusion) is individually well-established. The primary novelty lies in the integration and task-specific application rather than in new algorithmic principles. External literature verification is deferred due to Retrieval-Disabled Mode.

**Validity/Soundness: 6/10** — The experimental design has three critical gaps: (1) no multi-seed variance reporting makes all comparisons statistically ungrounded, (2) the GALP lesion-proposal assumption is not validated against ground-truth lesion masks available in MFIDDR, and (3) contribution claim (2) claims "robustness and interpretability" without any supporting experiments. The method section is technically well-specified and the overall pipeline is reproducible given full implementation details.

**Reproducibility: 5/10** — The paper specifies the backbone, patch sizes, loss weights, and expert parameters, but omits optimizer, learning rate schedule, epochs, batch size, hardware, and training time. These are fixable with a supplementary reproducibility table.

**Presentation: 7/10** — The paper is generally well-written and well-structured, with clear figures and tables. The main weaknesses in presentation are the list-style Related Work section, missing limitation discussion in the Conclusion, and the absence of quantitative result preview in the Abstract.

### Revision Priority Summary

| Priority | Action | Expected Impact on Score |
|----------|--------|-------------------------|
| **P0 (Must)** | Add multi-seed variance and statistical significance tests | +0.5 |
| **P0 (Must)** | Validate GALP proposals against lesion masks (IoU/Dice) | +0.5 |
| **P0 (Must)** | Remove or experimentally support "robustness and interpretability" claim | +0.3 |
| **P1 (Must)** | Fix load-balancing loss formulation (Eq. 11) and provide sensitivity analysis | +0.2 |
| **P1 (Must)** | Add computational cost comparison (FLOPs, params, latency) | +0.2 |
| **P1 (Must)** | Complete implementation details for reproducibility | +0.2 |
| **P2 (Nice-to-have)** | Restructure Related Work thematically | +0.1 |
| **P2 (Nice-to-have)** | Add limitation paragraph to Conclusion | +0.1 |
| **P2 (Nice-to-have)** | Add OOD/generalization experiments | +0.3 |

### ASCII Diagrams

```text
ASCII Diagram — Paper Structure & Evidence Map

[Clinical Problem: DR screening demand > specialist supply]
    |
    v
[Technical Gap: End-to-end CNNs lose fine-grained lesion info]
    |
    v
[Proposed Solution: GALP + LGRF]
    |
    +-- GALP: Auxiliary classifiers -> CAM -> Top-K lesion proposals
    |   [Claim: recovers small lesions without external annotations]
    |   [Evidence gap: no validation that proposals match real lesions]
    |
    +-- LGRF: MoE routing + cross-attention fusion of proposals
    |   [Claim: enables precise, selective cross-view integration]
    |   [Evidence gap: claims "robustness & interpretability" untested]
    |
    v
[Experiments: MFIDDR (4-view), DRTiD (2-view)]
    |
    +-- Main tables: 83.9% (w/o lesion), 84.6% (w/ lesion)
    |   [Evidence gap: single-run, no variance, no significance]
    |
    +-- Ablation (Table 4): each module contributes 0.8-1.6% Acc
    |   [Evidence gap: no seed variance for ablation either]
    |
    v
[Conclusion: "SOTA performance, clinical potential"]
    [Gap: No limitations discussed; OOD generalization untested]
```

```text
ASCII Diagram — Revision Strategy Roadmap

Problem Area            | Immediate Fix (Stage 1)      | Medium-Term (Stage 2)        | Long-Term (Stage 3)
------------------------|-----------------------------|------------------------------|---------------------
Statistical reliability | Add 3-seed variance ± std   | Add significance tests       | Multi-site validation
Lesion-proposal validation | IoU with segmentation masks | Clinician evaluation of proposals | Weakly-supervised lesion detection benchmark
Robustness claim       | Remove from contribution (2)| Add noise/corruption tests   | OOD camera generalization
Load-balancing loss     | Clarify M factor in Eq. 11  | Sensitivity analysis on λ    | Alternative loss formulations
Comparison fairness    | Add compute cost table       | Controlled re-implementation | Cross-dataset generalization
Reproducibility        | Add optimizer/hardware table | Release code                 | Standardized benchmark integration
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Multi-View DR Grading (Root)
|
+-- Branch 1: Fusion Strategy
|   +-- Leaf 1a: Self-attention based (MVCINN, Luo 2023)
|   +-- Leaf 1b: Evidential fusion (ETMC, Han 2022)
|   +-- Leaf 1c: Cross-attention + MoE (Ours)
|
+-- Branch 2: Supervision / Annotation Dependency
|   +-- Leaf 2a: Fully end-to-end (RETFound, MVCNN, DeepDR)
|   +-- Leaf 2b: Vessel-guided (CVSA, Lin 2025a)
|   +-- Leaf 2c: Lesion-guided (SMVDR, LFMVDR, Luo 2024/25)
|   +-- Leaf 2d: Coordinate-guided (CrossFIT, Hou 2022)
|   +-- Leaf 2e: Self-derived proposals (Ours — unique leaf)
|
+-- Branch 3: Spatial Resolution Handling
    +-- Leaf 3a: Fixed-resolution CNNs (MVCNN)
    +-- Leaf 3b: Hierarchical ViT (Swin-B — Ours and others)
    +-- Leaf 3c: Wavelet-based multiscale (WGLIN, Hu 2025)

Value Contribution of This Work:
  - Introduces self-derived proposal branch (Leaf 2e) that reduces annotation dependency
  - Combines CAM-based localization with MoE routing for lesion-aware cross-view fusion
  - Achieves competitive accuracy without external annotations at inference time
```