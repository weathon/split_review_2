## Summary
# Final Review Report

## Summary

This paper introduces ProteinVista, a 3D convolutional neural network that operates directly on voxelized full-atom protein structures. The model encodes protein structures as 5-channel density grids at 1.0Å resolution, processes them through five 3D convolutional blocks, and is pre-trained on ~500,000 AlphaFold-2 predicted structures using contrastive alignment with ESM-2 sequence embeddings. The paper evaluates ProteinVista on three protein-ligand interaction tasks (enzyme-substrate classification, transporter-substrate classification, and drug-target IC50 regression) and one homology-driven task (GO term prediction). 

The main findings are: (1) ProteinVista matches or exceeds ESM-2 on binding prediction tasks while using 5x fewer parameters and 2-3 orders of magnitude less pretraining data; (2) an ensemble of ProteinVista and ESM-2 yields further improvements on classification tasks, demonstrating complementarity; (3) on the homology-driven GO prediction task, ProteinVista underperforms ESM-2, honestly bounding the method's applicability; (4) the model is compute-efficient (20s per 1000 proteins on A100) but storage-intensive (~75 GB for 5800 proteins as voxel grids).

The paper addresses a timely question — whether full-atom 3D structure encoders can complement or outperform sequence-based models for structure-dependent tasks. The results provide evidence that 3D CNNs are indeed tractable at scale and offer complementary information to sequence transformers, particularly for tasks requiring fine-grained geometric information.

## Strengths
**1. Timely and well-motivated research question.** The paper tackles an important and underexplored question: whether full-atom 3D convolutional neural networks, pretrained at scale, can match or surpass sequence-based protein language models for structure-dependent prediction tasks. This question has practical relevance as AlphaFold DB makes millions of predicted structures available, yet most prediction pipelines still rely on sequence-only embeddings. The paper provides some of the first evidence that a properly designed 3D CNN can be both tractable and complementary to PLMs.

**2. Honest bounding of method applicability.** Section 3.4 (GO term prediction) is a particular strength — the authors test ProteinVista on a task where homology-based methods are known to excel and find that the structure encoder underperforms ESM-2. This negative result, rather than being hidden, is clearly presented and honestly interpreted. Similarly, the pLDDT stratification analysis (Section 4.1) shows that ProteinVista's advantage is largest on high-confidence structures, providing practical guidance about when the method should be applied.

**3. Compute efficiency analysis.** The compute comparison (Section 4.3) is thorough and informative. Showing that ProteinVista requires only 20s per 1000 proteins on A100 vs 215-426s for ESM-2, while using only ~1% of the pre-training GPU-hours, makes a compelling case for the method's efficiency. The honest disclosure of the storage trade-off (75 GB vs 3 MB) adds credibility.

**4. Ablation studies that disentangle design choices.** The ablation analysis (Section 4.2) systematically tests key architectural decisions: inference-time multi-view averaging (6.4% R² gain over single-view), pre-training objectives (contrastive vs Rosetta regression), and voxel resolution. The finding that fine-tuning augmentation is unnecessary if pre-training augmentation was used is informative for practitioners.

**5. Statistical rigor in comparisons.** The use of McNemar's test for classification and Wilcoxon signed-rank test for regression provides statistical validation that observed differences are not random noise. The reported p-values (p < 10^-13 for TSP, p < 10^-17 for ESP, p < 10^-304 for IC50) strongly support the significance of the improvements.

**6. Open-source release.** The commitment to release an open-source Python implementation enhances reproducibility and community impact.

## Weaknesses
**W1. Unsupported novelty claim ("first") and missing literature verification (Major).** 
Contribution C1 claims "the first compute-efficient full-atom 3D CNN pretrained on large-scale AlphaFold-2 structures." The word "first" requires comprehensive literature verification that was not possible in this review (Retrieval-Disabled Mode). Prior 3D CNN methods for proteins (3DCNN_MQA, EnzyNet, DeepSite, VoroCNN) used full-atom or backbone-atom representations, and while none combined large-scale pretraining with 3D CNNs at ProteinVista's scale, the architectural novelty of the voxel-based approach itself may be incremental. The authors should either provide a systematic literature comparison demonstrating what exactly is novel (scale, architecture, pretraining objective, or task combination) or downgrade the claim to a bounded statement (Page 1 - Introduction/Contributions). The paper's open-source release and compute efficiency are genuine strengths that do not rely on a "first" claim.

**W2. SOTA comparison conflates multiple changes (Major).**
Section 3.3 (optimized pipeline OP) compares ESM-ProteinVista_OP against published SOTA methods, but the OP introduces three simultaneous changes: (i) fine-tuning the small-molecule encoder, (ii) training a contrastive network on extracted embeddings, and (iii) averaging predictions from both ESM-2 and ProteinVista. This ensemble cannot be directly attributed to ProteinVista alone. To support the claim that "ProteinVista serves as a strong foundation," the authors should provide an incremental ablation showing the contribution of each component: ProteinVista alone vs ESM-2 alone vs ensembled vs ensembled+contrastive under the OP condition. Without this, the SOTA comparison is difficult to interpret (Page 5 - Section 3.3).

**W3. Formula error and ambiguity in voxel density encoding (Major).**
Section 2.1 describes the voxel density contribution as exp(-||v - r||/σ²) with σ = 1. The formula has three issues: (1) The distance in a Gaussian function is typically squared (||v-r||²), not linear; (2) The denominator should include a factor of 2 for a standard Gaussian (2σ²); (3) The notation "c ∈ ℝ³" for atom type is contradictory — c should be an atom type index (∈ {C,N,O,S,P}) rather than a vector. These issues, while individually minor, collectively create confusion about a core part of the method and can affect reproducibility (Page 2 - Section 2.1).

**W4. Missing experimental reproducibility details (Major).**
Section 3.1 states that models were fine-tuned under "identical conditions" with "optimal learning rate" search and early stopping, but does not report: optimizer choice, learning rate search range, batch size, number of seeds, train/validation/test split ratios, or wall-clock training time per model. Multi-seed variance is entirely absent from all reported results (Tables 1 and 2 show only single-point metrics). Given that model performance differences on ESP are marginal (91.8% vs 91.9%), variance reporting is essential to assess whether observed differences are meaningful. Adding 3-5 seed runs with mean±std would substantially improve reliability (Page 4 - Section 3.1).

**W5. IC50 ensemble interpretation slightly overstated (Minor).**
The text states that "the ESM-ProteinVista ensemble performs worse" than ProteinVista alone on IC50 prediction. Examining Table 2, the ensemble R²=0.68 vs ProteinVista R²=0.69 — a difference of 0.01 that is well within noise range given no variance reporting. Similarly, Pearson r is 0.82 vs 0.83, MAE is 0.63 vs 0.62. The ensemble does not "perform worse" in a meaningful sense; it simply does not further improve upon ProteinVista alone. The current phrasing could mislead readers into thinking the ensemble is detrimental (Page 5 - Section 3.2).

**W6. Ablation has minor numerical inconsistency (Minor).**
The text (Section 4.2) reports that replacing contrastive with Rosetta pretraining decreases R² by 1.0%, while Figure 2e's table caption shows "Rosetta vs. CL pretraining ~1.2%." These should match. Additionally, ablation results lack multi-seed variance, so it is unclear whether observed changes of 0.4-1.2% are statistically significant. The finding that fine-tuning augmentation has "virtually no impact (-0.1%)" is interesting but the interpretation is limited — it may indicate that pre-training augmentation suffices, or that the fine-tuning data has enough natural variation, but this is not tested (Page 6 - Section 4.2).

**W7. Data augmentation limited to discrete rotations (Minor).**
The augmentation strategy uses only 90° rotations and mirroring along Cartesian axes (24 discrete orientations). While this is computationally efficient, it does not provide true rotation invariance — the model sees only a finite set of orientations. The ablation showing that inference-time multi-view averaging is critical (6.4% R² drop with 1 vs 5 views) suggests that the augmentation alone does not achieve invariance. The authors should discuss whether denser (continuous) rotation augmentation would further improve robustness (Page 3 - Section 2.4).

**W8. GO term analysis lacks depth (Minor).**
Section 3.4 reports that ProteinVista underperforms ESM-2 on GO term prediction (F_max 0.57 vs 0.62). This is an important negative result, but the analysis does not explore why structure fails here. Possible explanations include: (1) GO annotations are historically derived from sequence homology experiments; (2) many GO terms describe broad functions not tied to localized 3D pockets; (3) 3D CNN's local receptive field may miss long-range residue interactions. A deeper failure analysis would strengthen the paper's contribution (Page 5 - Section 3.4).

**W9. Storage cost documentation is ambiguous (Minor).**
Section 4.3 states that "5,800 proteins... require ~75 GB as float32 coordinate NumPy arrays." It is unclear whether this refers to raw PDB coordinates (N×3 arrays) or pre-computed voxel grids (up to 160³×5 channels). The former would be much smaller than 75 GB; the latter is more plausible. Clarifying what exactly is stored would help reproducibility (Page 7 - Section 4.3).

**W10. Conclusion language overgeneralizes (Minor).**
The conclusion states that full-atom 3D CNNs have a "decisive advantage" for structure-dependent tasks, but the actual gains over ESM-2 are modest: +1.5% accuracy on TSP, matching performance on ESP, and +0.08 R² on IC50. Moreover, ProteinVista underperforms on GO prediction. The word "decisive" is not supported by the evidence and should be replaced with bounded language (Page 7 - Discussion).

## Score
**Final Score: 6/10**

**Scoring rationale:**
This paper has clear strengths: it addresses a timely research question with a well-designed empirical study, provides honest bounding of method applicability, and demonstrates compute efficiency. The ablation analysis and statistical testing are commendable.

However, the paper is held back by several significant weaknesses. The novelty claim ("first") cannot be verified without a literature search (W1). The SOTA comparison conflates multiple changes (W2), making the claimed superiority difficult to attribute. The formula error in the core voxel encoding (W3) and missing reproducibility details (W4) affect scientific reliability. The observed performance gains are modest (1-2% on classification, 0.08 R² on regression), and the method underperforms on GO prediction, honestly limiting applicability but also tempering enthusiasm.

The research value is moderate: if the claims hold after revision, the paper shows that 3D CNNs are a viable and complementary alternative to PLMs for structure-dependent tasks. The compute efficiency finding is practically useful. With a careful revision addressing the formula errors, adding variance reporting, and bounding the claims more precisely, the paper could reach higher impact.

**Score components (informal breakdown):**
- Research value / Contribution: 6/10 (timely question, moderate gains, honest limitations)
- Novelty: 5/10 (incremental — 3D CNNs for proteins are established; large-scale pretraining is the main novelty)
- Technical soundness: 6/10 (good experimental design but formula errors and missing variance reduce confidence)
- Reproducibility: 5/10 (missing key training details, no multi-seed reporting)
- Clarity and presentation: 7/10 (well-written overall, with clear figures and tables)

**Revision priority summary:**
- P0 (Must fix before acceptance): Correct formula error in Section 2.1; add multi-seed variance to all tables; add missing training details (optimizer, batch size, LR range, split ratios); remove or verify the "first" claim.
- P1 (Should fix): Add incremental ablation for the optimized pipeline; clarify storage numbers.
- P2 (Nice to have): Expand GO failure analysis; discuss discrete vs continuous rotation augmentation.