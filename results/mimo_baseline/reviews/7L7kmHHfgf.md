## Summary
This paper proposes PIRN, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection (MAD) using RGB and 3D modalities. PIRN introduces three core components: Balanced Prototype Assignment (BPA) via optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) using gated updates to handle unseen normal variations at inference, and Multimodal Normality Communication (MNC) for cross-modal knowledge exchange via graph-based prototype alignment and cross-attention. Extensive experiments on MVTec 3D-AD, Eyecandies, and Real-IAD D3 demonstrate consistent improvements over strong baselines, particularly in few-shot settings.

## Strengths
- **Well-motivated problem with clear technical solutions.** The paper identifies three specific failure modes of existing MAD methods in few-shot settings (codebook collapse, train-test distribution gap, isolated modality processing) and proposes targeted solutions for each. The motivation flows naturally from observed limitations to proposed designs.
- **Comprehensive and thorough experimental evaluation.** The paper evaluates across three benchmarks (MVTec 3D-AD, Eyecandies, Real-IAD D3), multiple shot settings (5, 10, 50, all-shot), three evaluation metrics (AUROC_I, AUROC_P, AUPRO), component ablations, hyperparameter sensitivity studies, modality availability analysis, and computational efficiency comparisons. The improvements are consistent and substantial: +3.7 AUROC_I on MVTec 3D-AD (10-shot) and +4.0 on Eyecandies (10-shot) over the strongest baseline.
- **Notable computational efficiency.** As shown in Table 4, PIRN achieves comparable or better accuracy than FIND while requiring 85% fewer FLOPs (103.36G vs 728.46G) and 4.35× lower latency (17.49ms vs 76.09ms), which is practically significant for deployment.
- **Clear framework design with complementary components.** The three modules address orthogonal challenges: BPA handles representation diversity, APR handles test-time adaptation, and MNC handles cross-modal synergy. The ablation in Table 2 confirms each component contributes independently, with cumulative improvements.

## Weaknesses
### Fatal
None.

### Major
- **Robustness of APR to anomalous test inputs lacks rigorous analysis.** The paper claims that OT-based context extraction causes anomalous patches to be "assigned more diffusely across prototypes" and the GRU gating "leaves p_k essentially unchanged." However, when an entire test image contains subtle anomalies, many patch tokens are still normal, and the OT plan could still assign some anomalous patches to prototypes. The paper does not quantify APR's robustness under varying anomaly severity or provide evidence that prototype corruption is avoided in practice. An ablation comparing APR behavior on normal-only vs. mixed test batches would strengthen this claim.
- **Moderate hyperparameter sensitivity.** Table 5 shows AUROC_I drops from 0.963 (K=10) to 0.901 (K=100), a 6.2-point gap, and Table 6 shows a 5.5-point drop from L=2 to L=8. While the optimal settings are reasonable, the sensitivity suggests the method requires careful tuning per dataset, which could limit practical adoption.

### Minor
- **Inconsistent comparison baselines across tables.** FIND (Li et al., 2025) appears in the efficiency comparison (Table 4) achieving 0.921 AUROC_I, nearly matching PIRN's 0.922, but is absent from the main comparison in Table 1. Including FIND in Table 1 would provide a more complete picture, especially since it appears to be a strong competitor.
- **Table 2 ablation has a confusing entry.** Row 4 shows BPA+APR+MNC achieving 0.967 AUROC_I, which exceeds both the full model's 10-shot result (0.922 in Row 5) and even the all-shot result (0.963 in Table 1). This likely represents a parser issue with the table structure, but if genuine, it warrants explanation.

### Trivial
- The training loss is briefly described as "a soft mining loss (Luo et al., 2025)" without providing the actual formulation, which makes exact reproduction slightly harder.

## Nice-to-Haves
- A failure case analysis showing where PIRN still struggles (e.g., specific anomaly types or object categories) would provide useful guidance for future work.
- An analysis of how the learned prototypes map to semantic normal patterns (e.g., do specific prototypes correspond to specific surface types like flat regions, edges, or curved surfaces?) would enhance interpretability.
- Discussion of how the method performs when 3D point cloud quality varies (e.g., noisy or sparse point clouds) would be valuable for real-world deployment.

## Novel Insights
The paper's core insight—that prototype-based intra-modal reconstruction with balanced assignment can serve as an effective information bottleneck for anomaly detection even under extreme data scarcity—is well-supported by the results. The demonstration that cross-modal communication at the prototype level (rather than dense patch-to-patch alignment) is more robust in few-shot settings is a valuable finding for the MAD community. The feature displacement visualization (Figure 4) provides a novel and intuitive way to understand how prototype-based reconstruction discriminates normal from anomalous patterns.

## Suggestions
- Add FIND to the main comparison table (Table 1) for completeness, since it appears to be the closest competitor.
- Include a dedicated robustness analysis of APR under varying anomaly contamination levels in the test set.
- Clarify Table 2 to resolve the apparent discrepancy between Row 4 and Row 5.
- Consider reporting standard deviations across runs to assess statistical significance, especially for marginal improvements (e.g., +0.1 AUROC_I in all-shot setting).

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>