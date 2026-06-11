## Summary
# Final Review Report

## Summary

This paper presents **PIRN**, a prototype-driven framework for few-shot multimodal anomaly detection (MAD) that uses RGB and surface-normal (3D) data. The core idea is to reconstruct each modality's features through a compact set of learnable prototype vectors, acting as an information bottleneck that filters out anomaly-specific patterns while faithfully reconstructing normal ones. Three technical innovations are proposed: (1) **Balanced Prototype Assignment (BPA)** uses optimal transport with uniform mass constraints to prevent codebook collapse and encourage diverse prototype usage; (2) **Adaptive Prototype Refinement (APR)** employs a GRU-based gating mechanism to update prototypes at test time using the normal context of the input, aiming to bridge the train-test distribution gap; and (3) **Multimodal Normality Communication (MNC)** exchanges aligned prototype knowledge between RGB and surface-normal branches via graph attention and cross-attention to exploit complementary texture-geometry cues.

Experiments on MVTec-3D-AD, Eyecandies, and Real-IAD D3 demonstrate consistent gains over existing MAD baselines under 5-shot, 10-shot, and 50-shot settings. The method also reports significantly lower FLOPs (103G) and latency (17ms) compared to the nearest competitor FIND (728G, 76ms). The paper addresses a practically relevant problem (few-shot industrial anomaly detection) and proposes a conceptually clean combination of prototype learning, optimal transport, and cross-modal communication. However, several methodological assumptions need stronger empirical validation, the experimental reporting lacks statistical rigor (no variance or significance tests), and the ablation analysis contains unresolved inconsistencies that affect confidence in the component-level claims.

## Strengths
1. **Problem relevance and positioning.** Few-shot multimodal anomaly detection is a practically important problem for industrial quality control where collecting abundant normal samples is expensive. The paper clearly identifies the limitations of existing cross-modal alignment and memory-bank approaches under data-scarce conditions, and motivates prototype-based reconstruction as an alternative paradigm.

2. **Technically coherent framework.** The three components (BPA, APR, MNC) are well-motivated and address distinct challenges in prototype-based few-shot MAD: codebook collapse (BPA), train-test distribution gap (APR), and cross-modal information sharing (MNC). The use of optimal transport for balanced prototype assignment is a technically sound choice that aligns with the few-shot constraint.

3. **Strong empirical results.** Under 5-shot and 10-shot settings, PIRN consistently outperforms existing baselines by nontrivial margins (3.6–4.0 AUROC_I improvement over the best prior method on MVTec-3D-AD and Eyecandies). Gains are reported across three different benchmarks, suggesting generalizability.

4. **Computational efficiency.** PIRN achieves these results while using 85% fewer FLOPs than the nearest SOTA competitor (FIND) and with 4.35× lower latency. This combination of accuracy and efficiency is a meaningful practical advantage for deployment in resource-constrained industrial settings.

5. **Interpretability analysis.** The t-SNE visualization (Fig. 1) and OT displacement analysis (Fig. 4) provide useful insights into prototype behavior, showing that BPA leads to more balanced prototype utilization and that anomalous tokens undergo larger feature displacements, supporting the core mechanism intuition.

## Weaknesses
### W1. Critical: No variance or significance reporting (W1 — Severity: Critical)
All results in Tab. 1, Tab. 2, and Tab. 8 are reported as single-point estimates without standard deviations, confidence intervals, or significance tests. This is especially problematic for few-shot settings (5/10-shot), where results can vary substantially depending on which samples are drawn. The margins of improvement (3.6–4.0 AUROC_I) could be within noise range without variance reporting. **Required action:** Report mean ± std over at least 3 independent few-shot sample draws for all main results. Add a paired significance test (e.g., Wilcoxon signed-rank) for the comparison against the strongest baseline.

### W2. Major: Ablation inconsistency and table error (W2 — Severity: Major)
Tab. 2 contains the following issues: (a) The column header reads "BFA" instead of "BPA" (typo). (b) The checkmark pattern across rows is ambiguous due to formatting, making it unclear which components are active in each row. (c) Row 4 (0.967 AUROC_I) exceeds the full model (row 5, 0.922 AUROC_I) by +4.5 points, which contradicts the claim that "Removing each component from the full model results in a consistent performance drop." This discrepancy either indicates a data error, a mislabeled row, or that a subset of components outperforms the full combination — any of which undermines the central ablation claim. **Required action:** Verify the ablation numbers, correct the table (fix "BFA" → "BPA", ensure checkmark clarity), and explain why a partial configuration appears to outperform the full model.

### W3. Major: Unverifiable "first" claim and limited novelty verification (W3 — Severity: Major)
Section 3.1 claims that PIRN is "the first multimodal anomaly detection framework to integrate a vector-quantized prototype codebook into a ViT encoder-decoder architecture." This claim combines three pre-existing components (VQ codebooks, ViT, MAD) and cannot be independently verified in this review due to disabled external retrieval. The related-work section cites HVQ-Trans (VQ for 2D AD) and INP-Former (prototype-based 2D AD), but does not systematically compare against potential MAD variants of these methods. **Required action:** Replace the "first" claim with scoped wording that acknowledges known related work, e.g., "To the best of our knowledge, PIRN is the first MAD framework to jointly use VQ-based intra-modal reconstruction with cross-modal prototype communication."

### W4. Major: APR core assumption lacks empirical verification (W4 — Severity: Major)
APR's test-time prototype refinement relies on the assumption that anomalous patches are "assigned more diffusely across prototypes" and thus contribute weakly to prototype context vectors. This diffusion property is stated but never empirically verified. For subtle anomalies near normal prototypes, OT assignment may concentrate rather than diffuse, potentially corrupting prototypes via the GRU update. The ablation "wo APR module" (0.916 vs. 0.922 full) suggests APR's contribution is modest (~0.6 points), raising questions about whether the added complexity is justified. **Required action:** (a) Design a synthetic experiment to visualize OT assignment entropy for normal vs. anomalous patches. (b) Report the gating scalar values $g_{rgb}, g_{sn}$ at inference to show when APR actually modifies prototypes. (c) Consider removing APR if its marginal benefit is small and its assumption is unverifiable.

### W5. Major: Training loss specification is incomplete (W5 — Severity: Major)
The loss function is described only as "minimizing the cosine distance" plus a reference to "soft mining loss (Luo et al., 2025)." Missing details include: (a) exact loss formulation (summed or averaged across patches/modalities?), (b) whether a VQ commitment loss is used (standard practice for prototype codebooks), (c) whether the two modalities are weighted equally, (d) definition of the soft mining loss for readers unfamiliar with INP-Former. Without this specification, the method cannot be exactly reproduced. **Required action:** Provide the complete loss equation with all terms and hyperparameters.

### W6. Major: FLOPs counting methodology and Sinkhorn iteration cost (W6 — Severity: Major)
PIRN reports 103.36G FLOPs, claiming 85% fewer than FIND. However, the Sinkhorn algorithm used for balanced OT (in both BPA and APR) is iterative, and its computational cost depends on the number of iterations. The paper does not specify whether Sinkhorn iterations are included in the FLOPs count, how many iterations are used, or whether the cost is amortized across decoder layers. If unaccounted, the FLOPs advantage may be overestimated. **Required action:** Clarify FLOPs counting methodology: specify Sinkhorn iterations, report FLOPs with and without OT components, and provide runtime breakdown.

### W7. Major: Incomplete failure-case analysis on Real-IAD D3 (W7 — Severity: Major)
The Real-IAD D3 results highlight PIRN's strong average performance but omit discussion of categories where it significantly underperforms competitors (e.g., humidity_sensor: 0.734 vs. 0.991 best; miniature_filling_sensor: 0.604 vs. 0.975 best). Additionally, the metric name "AUROC_J" in Tab. 8 differs from "AUROC_I" in Tab. 1, creating inconsistency. **Required action:** Add failure-case analysis for underperforming categories, discuss potential causes, and harmonize metric naming.

### W8. Minor: Introduction lacks practical stakes framing (W8 — Severity: Minor)
The first introduction paragraph reads as a literature critique without first establishing why few-shot MAD matters in practice (e.g., high cost of collecting many normal samples per product class in industrial inspection). **Required action:** Restructure the opening to first establish the practical scenario and stakes, then describe technical limitations.

### W9. Minor: Related work reads as a flat list (W9 — Severity: Minor)
The 2D AD related work paragraph lists methods chronologically without grouping them by methodological axis (VQ-codebook, prototype-based, reference-guided). **Required action:** Reorganize into 2-3 subcategories with explicit comparison axes.

### W10. Minor: Conclusion is incomplete (W10 — Severity: Minor)
The conclusion restates contributions without discussing limitations, failure cases, or future work directions. **Required action:** Restructure into validated findings, bounded limitations, and concrete next steps.

### W11. Minor: Contribution bullets conflate BPA and APR (W11 — Severity: Minor)
The second contribution bullet combines BPA (codebook collapse prevention) and APR (test-time adaptation) into one claim, reducing clarity. **Required action:** Separate into two distinct contribution statements.

### W12. Minor: MNC purification mechanism ambiguous (W12 — Severity: Minor)
The channel-wise sigmoid gating for feature purification is described as an "attention mask," which is misleading since $z_n^{\text{bpa}}$ is a feature vector, not an attention map. The intuition for why $\sigma(z_n^{\text{bpa}})$ magnitude correlates with normality is not explained. **Required action:** Clarify the element-wise operation and provide intuition/evidence for the normality-indicator property.

## Score
**Final Score: 6/10**

### Score Rationale

**Research Value (primary):** 7/10. Few-shot multimodal anomaly detection is a practically relevant problem. PIRN demonstrates consistent gains across three benchmarks with significant efficiency advantages (85% fewer FLOPs). The prototype-based approach is well-motivated for data-scarce settings.

**Novelty (primary):** 5/10. The combination of balanced OT assignment, GRU-based test-time adaptation, and cross-modal prototype communication is novel in the MAD context. However, individual components are well-established (VQ codebooks, Sinkhorn OT, GAT, cross-attention). The "first" claim is overreaching without external verification. The novelty is in the integration rather than in any single algorithmic breakthrough.

**Validity & Soundness:** 5/10. The empirical results are promising but critically lack variance reporting. The ablation table contains an unexplained inconsistency (row 4 outperforming the full model). The APR mechanism's core assumption is unverified.

**Reproducibility:** 5/10. The loss function is underspecified. Sinkhorn iteration details and FLOPs counting methodology need clarification.

**Overall:** The paper addresses an important problem with a well-structured framework and competitive results, but is held back by insufficient statistical rigor, an unresolved ablation inconsistency, and several unverified methodological assumptions. A revision addressing W1 (variance reporting), W2 (ablation correction), and W4 (APR assumption verification) would substantially strengthen the paper.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Few-shot MAD with limited normal samples]
    |
    ├── [Failure Mode 1: Cross-modal alignment fails with scarce data]
    │       → Evidence: Fig. 1 Left (baseline drop in low-data regime)
    │
    ├── [Failure Mode 2: Memory banks miss unseen normal variations]
    │       → Evidence: Tab. 1 (M3DM/CFM degrade from All→5-shot)
    │
    └── [Proposed: PIRN - Prototype-based reconstruction]
            │
            ├── BPA: Balanced OT assignment → prevents codebook collapse
            │       → Evidence: Fig. 1 Right (t-SNE), Tab. 2 (ablation)
            │       → Gap: OT ensures uniform mass, not necessarily distinct prototypes
            │
            ├── APR: GRU-based test-time prototype refinement
            │       → Evidence: Tab. 7 (0.916 wo/ vs 0.922 w/ APR)
            │       → Gap: Diffusion assumption unverified; gain is modest (0.6 pts)
            │
            └── MNC: Cross-modal prototype exchange (GAT + cross-attention)
                    → Evidence: Tab. 3 (RGB+SN > SN-only > RGB-only)
                    → Gap: Purification via σ(z^{bpa}) intuition unclear
                            |
                            v
                    [Output: Anomaly score = 1 - cos(E, Z_rec)]
                            |
                            v
                    [Evaluation: MVTec-3D-AD, Eyecandies, Real-IAD]
                            |
                            v
                    [Key Risk: No variance reported; single-point estimates]
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority | Issue                | Fix Action                          | Expected Gain
---------|----------------------|-------------------------------------|---------------------
P0 (Must)| W1: No variance      | Report mean±std over 3+ seeds       | Statistical credibility
P0 (Must)| W2: Ablation error   | Verify Tab. 2, fix typo, explain    | Core claim integrity
                                   row 4 > full model discrepancy       |
P1 (Must)| W4: APR assumption   | Add OT entropy analysis, report     | Mechanism validation
                                   gating values at inference           |
P1 (Must)| W3: "First" claim    | Replace with scoped wording         | Reviewer defensibility
P1 (Must)| W5: Loss spec        | Provide full loss equation +        | Reproducibility
                                   commitment loss detail               |
P2 (Nice)| W6: FLOPs count      | Clarify Sinkhorn inclusion,         | Fair efficiency comparison
                                   report breakdown                     |
P2 (Nice)| W7: Real-IAD gaps   | Add failure-case analysis,          | Balanced presentation
                                   harmonize AUROC naming               |
P3 (Nice)| W8-W12: Writing      | Restructure intro, related work,    | Readability & impact
                                   conclusion, contribution bullets     |
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Multimodal Anomaly Detection (MAD)
│
├── Cross-modal Alignment Methods
│   ├── CFM (Costanzino et al., 2024): Dense RGB↔3D feature alignment
│   └── LSFA (Tu et al., 2024): Local feature alignment
│   └── Limitation: Fail with few normal samples (narrow cross-modal correlations)
│
├── Memory-bank Methods
│   ├── M3DM (Wang et al., 2023): Multi-modal memory bank
│   ├── SG-DM (Chu et al., 2023): Semantic-guided memory
│   └── Limitation: Miss unseen normal variations → false positives
│
├── Architecture Search Methods
│   └── 3D-ADNAS (Long et al., 2025): NAS-optimized fusion
│
└── (Proposed) Prototype-based Reconstruction Methods
    ├── 2D-only: HVQ-Trans (VQ codebook), MemAE (memory AE),
    │            INP-Former (per-image prototypes), DPDL (Gaussian prototypes)
    │            └── Limitation: No cross-modal interaction
    └── PIRN (Ours): VQ codebook + balanced OT + cross-modal communication
                    └── Novelty Dimension: First to combine VQ prototypes with
                        explicit cross-modal knowledge transfer for MAD
                    └── Value: 85% fewer FLOPs than FIND, gains under few-shot
                    └── Key Risk: Prior art may exist combining VQ + MAD
                        (deferred verification due to retrieval unavailability)
```

### Final Score Summary

| Dimension | Score (0-10) | Basis |
|-----------|-------------|-------|
| Research Value & Impact | 7 | Practical problem, consistent gains, efficiency advantage |
| Novelty | 5 | Novel integration but known components; "first" claim unverifiable |
| Validity & Rigor | 5 | No variance; ablation inconsistency; unverified APR assumption |
| Reproducibility | 5 | Loss spec incomplete; FLOPs methodology unclear |
| Presentation | 7 | Generally clear writing; good visualizations; some gaps in intro/related work |
| **Final Score** | **6/10** | Strong results but significant rigor gaps that need addressing |

**Note:** External literature verification was unavailable in this run (paper_search not started due to missing API token). All novelty/comparison conclusions that depend on external evidence are marked for deferred manual verification.